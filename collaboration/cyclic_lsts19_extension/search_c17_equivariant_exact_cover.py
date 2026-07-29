#!/usr/bin/env python3
"""Algorithm-X witness search for the C17-equivariant extension.

The 228 orbit phases form an exact-cover instance: a chosen phase covers its
block-orbit column and four triple-star/colour columns.  There are 2,964 rows,
1,140 columns, and exactly five columns per row.

Any emitted model still requires the independent semantic verifier.  Timeout
or exhausted bounded search is not an UNSAT certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from evidence.verify_defect_cross_link_lsts19 import construct_lsts19  # noqa: E402
from generate_c17_equivariant_cnf import (  # noqa: E402
    COLOURS,
    P,
    POINTS,
    canonical,
    orbit_representatives,
    representative_and_shift,
    variable,
)


class TimedOut(Exception):
    """The bounded witness search reached its wall-clock deadline."""


def build_exact_cover() -> tuple[
    dict[int, set[int]],
    dict[int, tuple[int, ...]],
]:
    link = construct_lsts19()
    blocks = orbit_representatives(4)
    triples = orbit_representatives(3)
    block_index = {block: index for index, block in enumerate(blocks)}
    incidences: list[list[tuple[int, int]]] = [[] for _ in blocks]
    forbidden: list[set[int]] = [set() for _ in blocks]

    # Columns 0..227 choose one phase per block orbit.  The remaining columns
    # require each of the sixteen non-root colours in each triple orbit.
    star_colour_columns = {}
    next_column = len(blocks)
    for star, triple in enumerate(triples):
        root_colour = link[triple]
        for colour in COLOURS:
            if colour != root_colour:
                star_colour_columns[(star, colour)] = next_column
                next_column += 1
        for point in POINTS:
            if point in triple:
                continue
            orbit, shift = representative_and_shift(
                canonical(triple + (point,)), block_index
            )
            incidences[orbit].append((star, shift))
            forbidden[orbit].add((root_colour - shift) % P)

    if next_column != 1_140:
        raise AssertionError("wrong exact-cover column count")
    if any(len(items) != 4 for items in incidences):
        raise AssertionError("each block orbit must have four face incidences")
    if any(len(values) != 4 for values in forbidden):
        raise AssertionError("each block orbit must forbid four distinct phases")

    rows: dict[int, tuple[int, ...]] = {}
    columns: dict[int, set[int]] = {column: set() for column in range(next_column)}
    for orbit in range(len(blocks)):
        for phase in COLOURS:
            if phase in forbidden[orbit]:
                continue
            row = variable(orbit, phase)
            covered = [orbit]
            for star, shift in incidences[orbit]:
                colour = (phase + shift) % P
                covered.append(star_colour_columns[(star, colour)])
            if len(covered) != 5 or len(set(covered)) != 5:
                raise AssertionError("a row does not cover five distinct columns")
            rows[row] = tuple(covered)
            for column in covered:
                columns[column].add(row)

    if len(rows) != 2_964:
        raise AssertionError("wrong exact-cover row count")
    sizes = sorted({len(options) for options in columns.values()})
    if sizes != [13]:
        raise AssertionError(f"unexpected exact-cover column sizes: {sizes}")
    return columns, rows


def select(
    columns: dict[int, set[int]],
    rows: dict[int, tuple[int, ...]],
    chosen_row: int,
) -> list[tuple[int, set[int]]]:
    removed = []
    for column in rows[chosen_row]:
        options = columns.pop(column)
        removed.append((column, options))
        for row in options:
            for other in rows[row]:
                if other != column and other in columns:
                    columns[other].remove(row)
    return removed


def deselect(
    columns: dict[int, set[int]],
    rows: dict[int, tuple[int, ...]],
    removed: list[tuple[int, set[int]]],
) -> None:
    for column, options in reversed(removed):
        columns[column] = options
        for row in options:
            for other in rows[row]:
                if other != column and other in columns:
                    columns[other].add(row)


def algorithm_x(
    columns: dict[int, set[int]],
    rows: dict[int, tuple[int, ...]],
    solution: list[int],
    deadline: float,
    rng: random.Random,
    counters: list[int],
) -> list[int] | None:
    counters[0] += 1
    if not columns:
        return list(solution)
    if not counters[0] % 1_024:
        if time.monotonic() >= deadline:
            raise TimedOut
    if not counters[0] % 100_000:
        print(
            f"nodes={counters[0]} depth={len(solution)} columns={len(columns)}",
            file=sys.stderr,
            flush=True,
        )

    column = min(columns, key=lambda item: (len(columns[item]), item))
    options = list(columns[column])
    rng.shuffle(options)
    for row in options:
        solution.append(row)
        removed = select(columns, rows, row)
        result = algorithm_x(columns, rows, solution, deadline, rng, counters)
        if result is not None:
            return result
        deselect(columns, rows, removed)
        solution.pop()
    return None


def write_model(path: Path, selected_rows: list[int]) -> None:
    assignment = [-1] * 228
    for row in selected_rows:
        zero_based = row - 1
        orbit, phase = divmod(zero_based, P)
        if assignment[orbit] != -1:
            raise AssertionError("two selected phases for one orbit")
        assignment[orbit] = phase
    if any(phase < 0 for phase in assignment):
        raise AssertionError("selected rows omit a block orbit")
    literals = [variable(orbit, phase) for orbit, phase in enumerate(assignment)]
    path.write_text(
        "s SATISFIABLE\nv " + " ".join(map(str, literals)) + " 0\n",
        encoding="ascii",
    )


def write_matrix(path: Path, rows: dict[int, tuple[int, ...]]) -> str:
    lines = [f"p exact 1140 {len(rows)}"]
    for row in sorted(rows):
        lines.append(f"{row} " + " ".join(str(column) for column in rows[row]))
    content = ("\n".join(lines) + "\n").encode("ascii")
    path.write_bytes(content)
    return hashlib.sha256(content).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=1_800.0)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dump-matrix", type=Path)
    parser.add_argument("--dump-only", action="store_true")
    args = parser.parse_args()
    deadline = time.monotonic() + args.seconds
    columns, rows = build_exact_cover()
    if args.dump_matrix is not None:
        digest = write_matrix(args.dump_matrix, rows)
        print(f"matrix SHA-256: {digest}")
    if args.dump_only:
        if args.dump_matrix is None:
            raise ValueError("--dump-only requires --dump-matrix")
        return
    if args.output.exists():
        raise FileExistsError(
            f"refusing to reuse pre-existing model path: {args.output}"
        )
    counters = [0]
    try:
        if time.monotonic() >= deadline:
            raise TimedOut
        solution = algorithm_x(
            columns,
            rows,
            [],
            deadline,
            random.Random(args.seed),
            counters,
        )
    except TimedOut:
        print(f"UNKNOWN timeout nodes={counters[0]}")
        raise SystemExit(2) from None
    if solution is None:
        # This exhaustiveness claim is process-local and not a portable proof.
        print(f"EXHAUSTED_WITHOUT_CERTIFICATE nodes={counters[0]}")
        raise SystemExit(3)
    write_model(args.output, solution)
    print(f"SAT_CANDIDATE rows={len(solution)} nodes={counters[0]} seed={args.seed}")


if __name__ == "__main__":
    main()
