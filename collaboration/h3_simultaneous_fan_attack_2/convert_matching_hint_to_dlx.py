#!/usr/bin/env python3
"""Convert a quotient-cell matching hint to exact-cover matrix row labels.

The local and CP-SAT searches identify the 2,964 quotient cells by their
canonical sorted-cell indices.  The audited Algorithm-X matrix instead keeps
the original sparse row labels.  This script reconstructs both incidence
streams and matches them by their five exact-cover columns, checking a full
bijection before converting a 228-line one-per-Q-group hint.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from search_cyclic_invariant_matching_local import QUAD_GROUPS
from verify_fan_kernel_reduction import (
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


def read_matrix(path: Path) -> tuple[int, dict[tuple[int, ...], int]]:
    lines = path.read_text(encoding="ascii").splitlines()
    header = lines[0].split()
    if header != ["p", "exact", "1140", "2964"]:
        raise ValueError("unexpected exact-cover matrix header")
    by_columns: dict[tuple[int, ...], int] = {}
    for line in lines[1:]:
        values = [int(value) for value in line.split()]
        label, columns = values[0], tuple(sorted(values[1:]))
        if len(columns) != 5 or len(set(columns)) != 5:
            raise ValueError("matrix row does not contain five distinct columns")
        if columns in by_columns:
            raise ValueError("two matrix rows have identical incidence")
        by_columns[columns] = label
    if len(by_columns) != 2_964:
        raise ValueError("matrix does not contain 2,964 rows")
    return len(lines) - 1, by_columns


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hint", type=Path)
    parser.add_argument("matrix", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    _, matrix_rows = read_matrix(args.matrix)

    incidence: list[list[int]] = [[] for _ in cells]
    for group_index, group in enumerate(groups):
        for cell in group:
            incidence[cell].append(group_index)
    signatures = [tuple(sorted(columns)) for columns in incidence]
    if any(len(columns) != 5 for columns in signatures):
        raise AssertionError("a quotient cell does not have degree five")
    if len(set(signatures)) != len(cells):
        raise AssertionError("two quotient cells have the same incidence")
    if set(signatures) != set(matrix_rows):
        raise AssertionError("canonical and matrix incidence streams differ")

    hinted_cells = [
        int(line)
        for line in args.hint.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    hinted = set(hinted_cells)
    if len(hinted_cells) != QUAD_GROUPS or len(hinted) != QUAD_GROUPS:
        raise ValueError(
            f"hint must contain {QUAD_GROUPS} distinct quotient-cell indices"
        )
    if any(cell < 0 or cell >= len(cells) for cell in hinted):
        raise ValueError("hint contains an out-of-range quotient-cell index")
    if any(
        len(hinted & set(group)) != 1 for group in groups[:QUAD_GROUPS]
    ):
        raise ValueError("hint is not a one-per-Q-group transversal")

    labels = [matrix_rows[signatures[cell]] for cell in hinted_cells]
    if len(set(labels)) != QUAD_GROUPS:
        raise AssertionError("converted row labels are not distinct")
    args.output.write_text(
        "".join(f"{label}\n" for label in labels),
        encoding="ascii",
    )
    print(f"quotient_cells={len(cells)}")
    print(f"matrix_rows={len(matrix_rows)}")
    print("full_incidence_bijection=PASS")
    print(f"hinted_rows={len(labels)}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
