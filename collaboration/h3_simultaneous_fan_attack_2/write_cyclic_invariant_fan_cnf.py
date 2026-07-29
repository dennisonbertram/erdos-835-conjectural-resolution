#!/usr/bin/env python3
"""Write the deterministic C17-invariant simultaneous-fan CNF.

The encoding uses one primary variable per (orbit cell, fan label), a Sinz
sequential at-most-one encoding for every cell, group-label coverage clauses,
and a lossless global label normalization on the first group.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations
from pathlib import Path

from verify_fan_kernel_reduction import (
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


LABELS = 13


def primary(cell: int, label: int) -> int:
    return cell * LABELS + label + 1


def auxiliary(cell: int, position: int, cell_count: int) -> int:
    """Sequential-counter variable s_position, with position in 0..11."""
    return cell_count * LABELS + cell * (LABELS - 1) + position + 1


def build_clauses(
    cell_count: int,
    groups: tuple[tuple[int, ...], ...],
    redundant_group_amo: bool = False,
    pairwise_cell_amo: bool = False,
) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []

    for cell in range(cell_count):
        xs = tuple(primary(cell, label) for label in range(LABELS))
        ss = tuple(
            auxiliary(cell, position, cell_count) for position in range(LABELS - 1)
        )
        clauses.append(xs)
        if pairwise_cell_amo:
            clauses.extend(
                (-xs[left], -xs[right])
                for left, right in combinations(range(LABELS), 2)
            )
        else:
            clauses.append((-xs[0], ss[0]))
            for position in range(1, LABELS - 1):
                clauses.append((-xs[position], ss[position]))
                clauses.append((-ss[position - 1], ss[position]))
                clauses.append((-xs[position], -ss[position - 1]))
            clauses.append((-xs[-1], -ss[-1]))

    for group in groups:
        for label in range(LABELS):
            clauses.append(tuple(primary(cell, label) for cell in group))

    if redundant_group_amo:
        conflict_edges = {
            tuple(sorted(edge)) for group in groups for edge in combinations(group, 2)
        }
        for left, right in sorted(conflict_edges):
            for label in range(LABELS):
                clauses.append((-primary(left, label), -primary(right, label)))

    for label, cell in enumerate(groups[0]):
        clauses.append((primary(cell, label),))
    return clauses


def write_cnf(
    path: Path,
    redundant_group_amo: bool = False,
    pairwise_cell_amo: bool = False,
) -> tuple[int, int, str]:
    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    clauses = build_clauses(
        len(cells),
        groups,
        redundant_group_amo,
        pairwise_cell_amo,
    )
    variables = len(cells) * (LABELS if pairwise_cell_amo else 2 * LABELS - 1)
    if pairwise_cell_amo:
        expected_clauses = (
            len(cells)
            + len(cells) * (LABELS * (LABELS - 1) // 2)
            + len(groups) * LABELS
            + LABELS
        )
    else:
        expected_clauses = 121_537
    if redundant_group_amo:
        conflict_edges = {
            tuple(sorted(edge)) for group in groups for edge in combinations(group, 2)
        }
        expected_clauses += LABELS * len(conflict_edges)
    expected_variables = 38_532 if pairwise_cell_amo else 74_100
    if (variables, len(clauses)) != (expected_variables, expected_clauses):
        raise AssertionError("unexpected invariant-fan CNF dimensions")

    digest = hashlib.sha256()
    with path.open("wb") as handle:
        header = f"p cnf {variables} {len(clauses)}\n".encode("ascii")
        handle.write(header)
        digest.update(header)
        for clause in clauses:
            line = (" ".join(map(str, clause)) + " 0\n").encode("ascii")
            handle.write(line)
            digest.update(line)
    return variables, len(clauses), digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--redundant-group-amo",
        action="store_true",
        help="add direct conflict-edge clauses for stronger propagation",
    )
    parser.add_argument(
        "--pairwise-cell-amo",
        action="store_true",
        help="replace the sequential cell AMO with direct pairwise clauses",
    )
    args = parser.parse_args()
    variables, clauses, digest = write_cnf(
        args.output,
        args.redundant_group_amo,
        args.pairwise_cell_amo,
    )
    print(f"path={args.output}")
    print(f"variables={variables}")
    print(f"clauses={clauses}")
    print(f"redundant_group_amo={args.redundant_group_amo}")
    print(f"pairwise_cell_amo={args.pairwise_cell_amo}")
    print(f"sha256={digest}")
    print("PASS")


if __name__ == "__main__":
    main()
