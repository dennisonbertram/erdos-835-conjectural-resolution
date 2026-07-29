#!/usr/bin/env python3
"""Emit and independently check SAT encodings for EH derived point-links.

For three discarded Etzion--Hartman systems and a point ``p``, the blocks in
the five-fold leave through ``p`` become 285 triples on the other 19 points.
Every pair lies in exactly five of those triples.  A partition into five
Steiner triple systems is therefore exactly a proper five-colouring of the
triple-intersection graph, equivalently a rainbow assignment on every
five-triple pair-star.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_seed.txt"
SOURCE_SHA256 = "b1ea090d3e3b88366c87e95660c1c82a406d2c3b100cc1d39bcc2c7e8fde47f9"

POINTS = tuple(range(20))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
ALL_TRIPLES = tuple(itertools.combinations(POINTS, 3))
N_COLOURS = 5


def load_source() -> tuple[
    dict[tuple[int, ...], int], tuple[frozenset[tuple[int, ...]], ...]
]:
    """Authenticate the seed and verify its fifteen complete EH systems."""

    raw = SOURCE.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != SOURCE_SHA256:
        raise AssertionError(f"source digest {actual} != {SOURCE_SHA256}")
    lines = raw.decode("ascii").splitlines()
    if len(lines) != len(BLOCKS):
        raise AssertionError("source does not contain C(20,4) rows")

    owner: dict[tuple[int, ...], int] = {}
    for expected, line in zip(BLOCKS, lines):
        fields = tuple(map(int, line.split()))
        if len(fields) != 5 or fields[:4] != expected:
            raise AssertionError(f"malformed source row at {expected}")
        owner[expected] = fields[4]

    if Counter(owner.values()) != Counter({label: 285 for label in range(17)}):
        raise AssertionError("source labels do not have the authenticated census")

    systems = tuple(
        frozenset(block for block, label in owner.items() if label == system)
        for system in range(15)
    )
    used: set[tuple[int, ...]] = set()
    for number, system in enumerate(systems):
        if len(system) != 285 or used.intersection(system):
            raise AssertionError(f"EH system {number} is not disjoint")
        covered = Counter(
            triple for block in system for triple in itertools.combinations(block, 3)
        )
        if set(covered) != set(ALL_TRIPLES) or set(covered.values()) != {1}:
            raise AssertionError(f"EH system {number} is not an SQS(20)")
        used.update(system)
    return owner, systems


def build_instance(
    systems: tuple[frozenset[tuple[int, ...]], ...],
    dropped: tuple[int, int, int],
    point: int,
) -> tuple[
    tuple[tuple[int, int, int], ...],
    dict[tuple[int, int], tuple[int, ...]],
]:
    """Build the exact 2-(19,3,5) derived leave at ``point``."""

    if tuple(sorted(dropped)) != dropped or len(set(dropped)) != 3:
        raise ValueError("drop must be three distinct increasing labels")
    if not set(dropped) <= set(range(15)):
        raise ValueError("drop labels must lie in 0,...,14")
    if point not in POINTS:
        raise ValueError("point must lie in 0,...,19")

    kept = set().union(
        *(system for number, system in enumerate(systems) if number not in dropped)
    )
    triples = tuple(
        tuple(x for x in block if x != point)
        for block in BLOCKS
        if point in block and block not in kept
    )
    if len(triples) != 285 or len(set(triples)) != 285:
        raise AssertionError("derived leave does not have 285 distinct triples")

    other_points = tuple(x for x in POINTS if x != point)
    by_pair_lists: dict[tuple[int, int], list[int]] = defaultdict(list)
    for row, triple in enumerate(triples):
        for pair in itertools.combinations(triple, 2):
            by_pair_lists[pair].append(row)
    by_pair = {pair: tuple(rows) for pair, rows in by_pair_lists.items()}
    if set(by_pair) != set(itertools.combinations(other_points, 2)):
        raise AssertionError("derived leave misses a pair")
    if set(map(len, by_pair.values())) != {5}:
        raise AssertionError("derived leave is not five-fold")
    return triples, by_pair


def variable(row: int, colour: int) -> int:
    """DIMACS variable for assigning ``colour`` to triple row ``row``."""

    return N_COLOURS * row + colour + 1


def clauses_for(
    triples: tuple[tuple[int, int, int], ...],
    by_pair: dict[tuple[int, int], tuple[int, ...]],
) -> list[tuple[int, ...]]:
    """Return the transparent one-hot/rainbow CNF."""

    clauses: list[tuple[int, ...]] = []
    for row in range(len(triples)):
        clauses.append(tuple(variable(row, colour) for colour in range(N_COLOURS)))
        for left, right in itertools.combinations(range(N_COLOURS), 2):
            clauses.append((-variable(row, left), -variable(row, right)))

    for rows in by_pair.values():
        for colour in range(N_COLOURS):
            # Redundant under the row one-hot and pair-star at-most-one
            # constraints, but explicit rainbow coverage greatly strengthens
            # unit propagation and keeps proof certificates smaller.
            clauses.append(tuple(variable(row, colour) for row in rows))
            for left, right in itertools.combinations(rows, 2):
                clauses.append((-variable(left, colour), -variable(right, colour)))

    # Every colouring can be relabelled so that the lexicographically first
    # pair-star receives colours 0,...,4 in its row order.
    root_pair = min(by_pair)
    for colour, row in enumerate(by_pair[root_pair]):
        clauses.append((variable(row, colour),))
    return clauses


def write_cnf(
    output: Path,
    triples: tuple[tuple[int, int, int], ...],
    clauses: list[tuple[int, ...]],
) -> str:
    """Write DIMACS deterministically and return its SHA-256 digest."""

    text = [f"p cnf {len(triples) * N_COLOURS} {len(clauses)}\n"]
    text.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    output.write_text("".join(text), encoding="ascii")
    return hashlib.sha256(output.read_bytes()).hexdigest()


def parse_solver_model(path: Path) -> set[int]:
    """Read the positive literals from a DIMACS competition witness."""

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
    """Decode a SAT model and verify five STS(19)s without trusting the CNF."""

    colours: list[int] = []
    for row in range(len(triples)):
        assigned = [
            colour for colour in range(N_COLOURS) if variable(row, colour) in positives
        ]
        if len(assigned) != 1:
            raise AssertionError(f"triple row {row} has {len(assigned)} colours")
        colours.append(assigned[0])

    for pair, rows in by_pair.items():
        if {colours[row] for row in rows} != set(range(N_COLOURS)):
            raise AssertionError(f"pair {pair} is not rainbow")
    for colour in range(N_COLOURS):
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


def parse_drop(raw: str) -> tuple[int, int, int]:
    values = tuple(sorted(map(int, raw.split(","))))
    if len(values) != 3 or len(set(values)) != 3:
        raise argparse.ArgumentTypeError("expected three comma-separated labels")
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", type=parse_drop, required=True)
    parser.add_argument("--point", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()

    _, systems = load_source()
    triples, by_pair = build_instance(systems, args.drop, args.point)
    clauses = clauses_for(triples, by_pair)
    digest = write_cnf(args.cnf, triples, clauses)
    print(
        f"drop={args.drop} point={args.point} vertices={len(triples)} "
        f"pairs={len(by_pair)} vars={len(triples) * N_COLOURS} "
        f"clauses={len(clauses)} sha256={digest}"
    )
    if args.model is not None:
        colours = decode_and_verify(triples, by_pair, parse_solver_model(args.model))
        colour_digest = hashlib.sha256(bytes(colours)).hexdigest()
        print(f"model verified; colour_sha256={colour_digest}")


if __name__ == "__main__":
    main()
