#!/usr/bin/env python3
"""Emit/verify the six-colour point-link CNF after dropping four EH systems.

Retaining eleven SQS(20)s leaves a 2-(19,3,6) design at a point.  A packing of
five disjoint STS(19)s automatically leaves the sixth, so the five-pack and
full six-colouring questions are equivalent.  The six-colour encoding is
direct, propagation-friendly, and has a sound root-star colour normalization.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from collections import Counter, defaultdict
from pathlib import Path

from point_link_cnf import BLOCKS, POINTS, load_source


N_COLOURS = 6
N_TRIPLES = 342
N_VARIABLES = N_TRIPLES * N_COLOURS
N_CLAUSES = 21_894


def parse_drop_four(raw: str) -> tuple[int, int, int, int]:
    values = tuple(sorted(map(int, raw.split(","))))
    if len(values) != 4 or len(set(values)) != 4 or not set(values) <= set(range(15)):
        raise argparse.ArgumentTypeError("expected four distinct labels from 0,...,14")
    return values


def build_instance(
    systems: tuple[frozenset[tuple[int, ...]], ...],
    dropped: tuple[int, int, int, int],
    point: int,
) -> tuple[
    tuple[tuple[int, int, int], ...],
    dict[tuple[int, int], tuple[int, ...]],
]:
    if point not in POINTS:
        raise ValueError("point must lie in 0,...,19")
    retained = set().union(
        *(system for number, system in enumerate(systems) if number not in dropped)
    )
    triples = tuple(
        tuple(value for value in block if value != point)
        for block in BLOCKS
        if point in block and block not in retained
    )
    if not len(triples) == len(set(triples)) == N_TRIPLES:
        raise AssertionError("six-fold derived leave has the wrong size")

    rows_by_pair: dict[tuple[int, int], list[int]] = defaultdict(list)
    for row, triple in enumerate(triples):
        for pair in itertools.combinations(triple, 2):
            rows_by_pair[pair].append(row)
    by_pair = {pair: tuple(rows) for pair, rows in rows_by_pair.items()}
    expected_pairs = set(
        itertools.combinations((value for value in POINTS if value != point), 2)
    )
    if set(by_pair) != expected_pairs or set(map(len, by_pair.values())) != {6}:
        raise AssertionError("derived leave is not 2-(19,3,6)")
    return triples, by_pair


def variable(row: int, colour: int) -> int:
    return N_COLOURS * row + colour + 1


def clauses_for(
    triples: tuple[tuple[int, int, int], ...],
    by_pair: dict[tuple[int, int], tuple[int, ...]],
) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []
    for row in range(len(triples)):
        clauses.append(tuple(variable(row, colour) for colour in range(6)))
        clauses.extend(
            (-variable(row, left), -variable(row, right))
            for left, right in itertools.combinations(range(6), 2)
        )
    for rows in by_pair.values():
        for colour in range(6):
            clauses.append(tuple(variable(row, colour) for row in rows))
            clauses.extend(
                (-variable(left, colour), -variable(right, colour))
                for left, right in itertools.combinations(rows, 2)
            )

    # Every six-colouring can be globally relabelled so that the six rows on
    # the lexicographically first pair receive colours 0,...,5 in row order.
    for colour, row in enumerate(by_pair[min(by_pair)]):
        clauses.append((variable(row, colour),))
    if len(triples) != N_TRIPLES or len(clauses) != N_CLAUSES:
        raise AssertionError("six-colour CNF has unexpected dimensions")
    return clauses


def write_cnf(output: Path, clauses: list[tuple[int, ...]]) -> str:
    text = [f"p cnf {N_VARIABLES} {len(clauses)}\n"]
    text.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    content = "".join(text).encode("ascii")
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
) -> tuple[int, ...]:
    colours: list[int] = []
    for row in range(len(triples)):
        assigned = [colour for colour in range(6) if variable(row, colour) in positives]
        if len(assigned) != 1:
            raise AssertionError(f"triple row {row} has {len(assigned)} colours")
        colours.append(assigned[0])
    for pair, rows in by_pair.items():
        if {colours[row] for row in rows} != set(range(6)):
            raise AssertionError(f"pair {pair} is not rainbow")
    for colour in range(6):
        selected = [
            triples[row] for row, value in enumerate(colours) if value == colour
        ]
        if len(selected) != 57:
            raise AssertionError(f"colour {colour} has {len(selected)} triples")
        covered = Counter(
            pair for triple in selected for pair in itertools.combinations(triple, 2)
        )
        if set(covered) != set(by_pair) or set(covered.values()) != {1}:
            raise AssertionError(f"colour {colour} is not an STS(19)")
    return tuple(colours)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", type=parse_drop_four, required=True)
    parser.add_argument("--point", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()

    _, systems = load_source()
    triples, by_pair = build_instance(systems, args.drop, args.point)
    clauses = clauses_for(triples, by_pair)
    digest = write_cnf(args.cnf, clauses)
    print(
        f"drop={args.drop} point={args.point} vertices={len(triples)} "
        f"pairs={len(by_pair)} vars={N_VARIABLES} clauses={len(clauses)} "
        f"sha256={digest}"
    )
    if args.model is not None:
        colours = decode_and_verify(triples, by_pair, parse_solver_model(args.model))
        colour_digest = hashlib.sha256(bytes(colours)).hexdigest()
        print(f"model verified; colour_sha256={colour_digest}")


if __name__ == "__main__":
    main()
