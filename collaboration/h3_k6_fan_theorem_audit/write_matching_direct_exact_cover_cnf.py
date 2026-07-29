#!/usr/bin/env python3
"""Write a propagation-strong CNF for the audited invariant matching matrix.

The canonical matrix has 2,964 allowed rows (orbit-cell choices), 1,140 exact
cover columns, thirteen rows per column, and five columns per row.  This
encoding writes an at-least-one clause and all pairwise at-most-one clauses
for every exact-cover column.  It retains the canonical 1..3876 phase-variable
labels so any SAT assignment can be decoded with the existing orbit map.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations
from pathlib import Path


COLUMNS = 1_140
ROWS = 2_964
PHASE_VARIABLES = 3_876
GROUP_SIZE = 13
ROW_DEGREE = 5


def read_matrix(path: Path) -> tuple[tuple[int, ...], ...]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != f"p exact {COLUMNS} {ROWS}":
        raise AssertionError("unexpected exact-cover matrix header")
    columns: list[list[int]] = [[] for _ in range(COLUMNS)]
    labels = set()
    for line in lines[1:]:
        values = tuple(map(int, line.split()))
        if len(values) != ROW_DEGREE + 1:
            raise AssertionError("a matrix row does not contain five columns")
        label, *covered = values
        if label not in range(1, PHASE_VARIABLES + 1) or label in labels:
            raise AssertionError("invalid or repeated canonical phase label")
        if len(set(covered)) != ROW_DEGREE:
            raise AssertionError("a matrix row repeats a column")
        labels.add(label)
        for column in covered:
            if column not in range(COLUMNS):
                raise AssertionError("matrix column outside declared range")
            columns[column].append(label)
    if len(labels) != ROWS:
        raise AssertionError("wrong number of allowed phase rows")
    if {len(group) for group in columns} != {GROUP_SIZE}:
        raise AssertionError("every exact-cover column should have thirteen rows")

    # Columns 0..227 are the block-orbit choice groups.
    for orbit in range(228):
        if {(label - 1) // 17 for label in columns[orbit]} != {orbit}:
            raise AssertionError("block-orbit column contains another orbit's phase")
    return tuple(tuple(sorted(group)) for group in columns)


def write_cnf(
    path: Path,
    groups: tuple[tuple[int, ...], ...],
    fixed_rows: tuple[int, ...],
) -> str:
    clauses_per_group = 1 + GROUP_SIZE * (GROUP_SIZE - 1) // 2
    clause_count = COLUMNS * clauses_per_group + len(fixed_rows)
    if clause_count != 90_060 + len(fixed_rows):
        raise AssertionError("unexpected direct exact-cover clause count")
    digest = hashlib.sha256()
    with path.open("wb") as stream:
        header = f"p cnf {PHASE_VARIABLES} {clause_count}\n".encode("ascii")
        stream.write(header)
        digest.update(header)
        for group in groups:
            lines = [
                (" ".join(map(str, group)) + " 0\n").encode("ascii"),
                *(
                    f"-{left} -{right} 0\n".encode("ascii")
                    for left, right in combinations(group, 2)
                ),
            ]
            for line in lines:
                stream.write(line)
                digest.update(line)
        for row in fixed_rows:
            line = f"{row} 0\n".encode("ascii")
            stream.write(line)
            digest.update(line)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--fixed-row", type=int, action="append", default=[])
    args = parser.parse_args()
    groups = read_matrix(args.matrix)
    fixed_rows = tuple(args.fixed_row)
    allowed = set().union(*map(set, groups))
    if len(set(fixed_rows)) != len(fixed_rows) or any(
        row not in allowed for row in fixed_rows
    ):
        raise AssertionError("fixed rows are repeated or not canonical allowed rows")
    if any(
        len(set(group) & set(fixed_rows)) > 1
        for group in groups
    ):
        raise AssertionError("fixed rows conflict in an exact-cover column")
    digest = write_cnf(args.cnf, groups, fixed_rows)
    print(f"variables={PHASE_VARIABLES}")
    print("allowed_primary_rows=2964")
    print(f"exact_cover_groups={len(groups)} group_size=13 row_degree=5")
    print(f"clauses={90_060 + len(fixed_rows)}")
    print(f"fixed_rows={len(fixed_rows)}")
    print(f"sha256={digest}")
    print("scope=one invariant matching only; UNKNOWN has no mathematical status")


if __name__ == "__main__":
    main()
