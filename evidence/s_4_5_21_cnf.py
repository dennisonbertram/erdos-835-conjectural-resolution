#!/usr/bin/env python3
"""DIMACS encoder and witness decoder for unrestricted S(4,5,21).

The encoding is the direct exact-cover formulation: one Boolean variable for
each admissible 5-set and, for every 4-set, exactly one of its 5-set
extensions is selected.  It uses the same lossless normalizations as
``search_s_4_5_21_extension.py``:

* the block 01234 is fixed;
* the full link at 012 is fixed up to relabelling;
* the link at 013 is split into its seven exhaustive alternating-cycle types.

A SAT result is decoded and checked by the independent combinatorial
``verify`` routine.  An UNSAT result is decisive for one cycle type only; all
seven types must be certified UNSAT to rule out S(4,5,21).
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_s_4_5_21_extension import (
    ANCHOR,
    OUTSIDE_PAIRS,
    POINTS,
    SECOND_LINK_CYCLE_TYPES,
    verify,
)


def parse_cycles(text: str) -> tuple[int, ...]:
    cycles = tuple(int(item) for item in text.split(","))
    canonical = tuple(sorted(cycles, reverse=True))
    allowed = {
        tuple(sorted(item, reverse=True))
        for item in SECOND_LINK_CYCLE_TYPES
    }
    if canonical not in allowed:
        raise ValueError(f"invalid cycle type: {cycles}")
    return cycles


def fixed_blocks(cycles: tuple[int, ...]) -> set[tuple[int, ...]]:
    fixed = {ANCHOR}
    fixed.update(
        (0, 1, 2, left, right)
        for left, right in OUTSIDE_PAIRS
    )

    start = 0
    for length in cycles:
        indices = list(range(start, start + length))
        for current, following in zip(
            indices, indices[1:] + indices[:1]
        ):
            left = OUTSIDE_PAIRS[current][1]
            right = OUTSIDE_PAIRS[following][0]
            fixed.add(tuple(sorted((0, 1, 3, left, right))))
        start += length

    assert len(fixed) == 17
    return fixed


def candidates() -> list[tuple[int, ...]]:
    anchor_points = set(ANCHOR)
    return [
        block
        for block in combinations(POINTS, 5)
        if len(set(block) & anchor_points) < 4 or block == ANCHOR
    ]


def write_instance(
    cycles: tuple[int, ...],
    cnf_path: Path,
    map_path: Path,
) -> None:
    blocks = candidates()
    variable_of = {
        block: index
        for index, block in enumerate(blocks, start=1)
    }
    extensions: dict[tuple[int, ...], list[int]] = {
        four: [] for four in combinations(POINTS, 4)
    }
    for block, variable in variable_of.items():
        for four in combinations(block, 4):
            extensions[four].append(variable)

    rows = list(extensions.values())
    assert len(rows) == 5985
    assert all(row for row in rows)
    units = [variable_of[block] for block in sorted(fixed_blocks(cycles))]
    clause_count = len(units) + sum(
        1 + len(row) * (len(row) - 1) // 2
        for row in rows
    )

    with cnf_path.open("w", encoding="ascii") as stream:
        stream.write(
            f"c S(4,5,21), second-link half-cycle type {cycles}\n"
        )
        stream.write(f"p cnf {len(blocks)} {clause_count}\n")
        for variable in units:
            stream.write(f"{variable} 0\n")
        for row in rows:
            stream.write(" ".join(map(str, row)) + " 0\n")
            for left, right in combinations(row, 2):
                stream.write(f"-{left} -{right} 0\n")

    map_path.write_text(
        json.dumps(
            {
                "cycles": cycles,
                "variables": blocks,
                "fixed": sorted(fixed_blocks(cycles)),
                "clauses": clause_count,
            },
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        {
            "cycles": cycles,
            "variables": len(blocks),
            "clauses": clause_count,
            "cnf": str(cnf_path),
            "map": str(map_path),
        }
    )


def read_positive_literals(solution_path: Path) -> set[int]:
    positives: set[int] = set()
    status = None
    for line in solution_path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            status = line[2:].strip()
        if not line.startswith("v "):
            continue
        for token in line[2:].split():
            literal = int(token)
            if literal > 0:
                positives.add(literal)
    if status != "SATISFIABLE":
        raise ValueError(f"solution status is {status!r}, not SATISFIABLE")
    return positives


def decode(
    map_path: Path,
    solution_path: Path,
    witness_path: Path,
) -> None:
    metadata = json.loads(map_path.read_text(encoding="utf-8"))
    blocks = [tuple(block) for block in metadata["variables"]]
    positives = read_positive_literals(solution_path)
    selected = {
        block
        for index, block in enumerate(blocks, start=1)
        if index in positives
    }
    verify(selected)
    witness_path.write_text(
        "\n".join(
            " ".join(map(str, block))
            for block in sorted(selected)
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        {
            "status": "PASS",
            "scope": "genuine S(4,5,21) witness; not a solution of ER #835",
            "blocks": len(selected),
            "witness": str(witness_path),
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycles", required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--map", dest="map_path", type=Path, required=True)
    parser.add_argument("--decode", type=Path)
    parser.add_argument("--witness", type=Path)
    args = parser.parse_args()

    cycles = parse_cycles(args.cycles)
    if args.decode:
        if not args.witness:
            parser.error("--decode requires --witness")
        decode(args.map_path, args.decode, args.witness)
    else:
        write_instance(cycles, args.cnf, args.map_path)


if __name__ == "__main__":
    main()
