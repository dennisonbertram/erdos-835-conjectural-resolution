#!/usr/bin/env python3
"""Emit the exact CNF for four disjoint STS(19)s in an EH point-link.

Unlike a full five-colouring, a four-packing omits one of the five triples on
the root pair.  Fixing that omitted row would not be without loss of
generality.  This encoding instead has five selector variables, one for each
possible omitted root row.  Within each selector branch only the global
permutation of the four packing labels is fixed.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from collections import Counter
from pathlib import Path

from point_link_cnf import build_instance, load_source, parse_drop


N_PACKED_SYSTEMS = 4
N_TRIPLES = 285
N_SELECTORS = 5
BASE_VARIABLES = N_TRIPLES * N_PACKED_SYSTEMS
SELECTOR_VARIABLES = BASE_VARIABLES + N_SELECTORS
SELECTOR_CLAUSES = 9_265
FIXED_BRANCH_CLAUSES = 9_238
PRECEDENCE_CLAUSES = 9_294


def assignment_variable(row: int, system: int) -> int:
    return N_PACKED_SYSTEMS * row + system + 1


def selector_variable(omitted_root_row: int) -> int:
    return BASE_VARIABLES + omitted_root_row + 1


def clauses_for_four_packing(
    triples: tuple[tuple[int, int, int], ...],
    by_pair: dict[tuple[int, int], tuple[int, ...]],
    omitted_root: int | None = None,
    selector_disjunction: bool = False,
) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []

    # The four systems are block-disjoint.  A triple may be unused.
    for row in range(len(triples)):
        clauses.extend(
            (-assignment_variable(row, left), -assignment_variable(row, right))
            for left, right in itertools.combinations(range(N_PACKED_SYSTEMS), 2)
        )

    # Each system is an STS(19): on every pair it uses exactly one of the five
    # available triples.
    for rows in by_pair.values():
        for system in range(N_PACKED_SYSTEMS):
            clauses.append(tuple(assignment_variable(row, system) for row in rows))
            clauses.extend(
                (
                    -assignment_variable(left, system),
                    -assignment_variable(right, system),
                )
                for left, right in itertools.combinations(rows, 2)
            )

    root_rows = by_pair[min(by_pair)]
    if omitted_root is not None and selector_disjunction:
        raise ValueError("choose a fixed root branch or selector disjunction")
    if selector_disjunction:
        # Exactly one of the five root rows is omitted.
        selectors = tuple(selector_variable(row) for row in range(N_SELECTORS))
        clauses.append(selectors)
        clauses.extend(
            (-left, -right) for left, right in itertools.combinations(selectors, 2)
        )

        # Conditional colour normalization.  If root position ``omitted`` is
        # not used, the other positions in increasing order receive labels
        # 0,...,3.
        for omitted in range(N_SELECTORS):
            used_rows = [
                row for position, row in enumerate(root_rows) if position != omitted
            ]
            for system, row in enumerate(used_rows):
                clauses.append(
                    (
                        -selector_variable(omitted),
                        assignment_variable(row, system),
                    )
                )
        expected_clauses = SELECTOR_CLAUSES
    elif omitted_root is not None:
        if omitted_root not in range(N_SELECTORS):
            raise ValueError("omitted root position must lie in 0,...,4")
        used_rows = [
            row for position, row in enumerate(root_rows) if position != omitted_root
        ]
        for system, row in enumerate(used_rows):
            clauses.append((assignment_variable(row, system),))
        expected_clauses = FIXED_BRANCH_CLAUSES
    else:
        # The four occupied root rows appear in increasing row order.  Relabel
        # the four systems by that order, then forbid every inversion.  This
        # handles all five possible omitted rows without selectors or a
        # privileged omitted position.
        for left_position, right_position in itertools.combinations(
            range(N_SELECTORS), 2
        ):
            left_row = root_rows[left_position]
            right_row = root_rows[right_position]
            clauses.extend(
                (
                    -assignment_variable(left_row, left_system),
                    -assignment_variable(right_row, right_system),
                )
                for left_system in range(N_PACKED_SYSTEMS)
                for right_system in range(N_PACKED_SYSTEMS)
                if left_system > right_system
            )
        expected_clauses = PRECEDENCE_CLAUSES

    if len(triples) != N_TRIPLES or len(clauses) != expected_clauses:
        raise AssertionError("unexpected four-packing CNF dimensions")
    return clauses


def serialize_cnf(
    clauses: list[tuple[int, ...]],
    selector_disjunction: bool = False,
) -> bytes:
    variables = SELECTOR_VARIABLES if selector_disjunction else BASE_VARIABLES
    text = [f"p cnf {variables} {len(clauses)}\n"]
    text.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(text).encode("ascii")


def write_cnf(
    output: Path,
    clauses: list[tuple[int, ...]],
    selector_disjunction: bool = False,
) -> str:
    content = serialize_cnf(clauses, selector_disjunction)
    output.write_bytes(content)
    return hashlib.sha256(content).hexdigest()


def parse_solver_model(path: Path) -> set[int]:
    positives: set[int] = set()
    saw_sat = False
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            saw_sat = "SATISFIABLE" in line and "UNSATISFIABLE" not in line
        elif line.startswith("v "):
            positives.update(value for value in map(int, line[2:].split()) if value > 0)
    if not saw_sat:
        raise AssertionError("solver output is not SATISFIABLE")
    return positives


def decode_and_verify(
    triples: tuple[tuple[int, int, int], ...],
    by_pair: dict[tuple[int, int], tuple[int, ...]],
    positives: set[int],
) -> tuple[tuple[int, ...], ...]:
    packed: list[tuple[int, ...]] = []
    used_rows: set[int] = set()
    for system in range(N_PACKED_SYSTEMS):
        rows = tuple(
            row
            for row in range(len(triples))
            if assignment_variable(row, system) in positives
        )
        if len(rows) != 57:
            raise AssertionError(f"packed system {system} has {len(rows)} triples")
        if used_rows.intersection(rows):
            raise AssertionError("packed systems are not triple-disjoint")
        used_rows.update(rows)
        covered = Counter(
            pair for row in rows for pair in itertools.combinations(triples[row], 2)
        )
        if set(covered) != set(by_pair) or set(covered.values()) != {1}:
            raise AssertionError(f"packed system {system} is not an STS(19)")
        packed.append(rows)
    return tuple(packed)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", type=parse_drop, required=True)
    parser.add_argument("--point", type=int, required=True)
    parser.add_argument("--omitted-root", type=int)
    parser.add_argument("--selector-disjunction", action="store_true")
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()

    _, systems = load_source()
    triples, by_pair = build_instance(systems, args.drop, args.point)
    clauses = clauses_for_four_packing(
        triples,
        by_pair,
        args.omitted_root,
        args.selector_disjunction,
    )
    digest = write_cnf(args.cnf, clauses, args.selector_disjunction)
    variables = SELECTOR_VARIABLES if args.selector_disjunction else BASE_VARIABLES
    print(
        f"drop={args.drop} point={args.point} vertices={len(triples)} "
        f"pairs={len(by_pair)} vars={variables} clauses={len(clauses)} "
        f"omitted_root={args.omitted_root} sha256={digest}"
    )
    if args.model is not None:
        packed = decode_and_verify(triples, by_pair, parse_solver_model(args.model))
        packed_digest = hashlib.sha256(
            b"\xff\xff".join(
                b"".join(row.to_bytes(2, "big") for row in rows) for rows in packed
            )
        ).hexdigest()
        print(f"model verified; packing_sha256={packed_digest}")


if __name__ == "__main__":
    main()
