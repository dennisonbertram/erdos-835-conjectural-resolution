#!/usr/bin/env python3
"""Prove that the committed 132-row packing cannot extend to the full cover.

This excludes one literal partial packing only.  It does not bound the
maximum finite packing size or exclude another C17-equivariant exact cover.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CYCLIC = REPO / "collaboration" / "cyclic_lsts19_extension"
sys.path[:0] = [str(CYCLIC), str(REPO)]

from search_c17_equivariant_exact_cover import build_exact_cover  # noqa: E402


EXPECTED_EMPTY_COLUMNS = (
    0,
    1,
    29,
    31,
    43,
    61,
    78,
    156,
    220,
    381,
    593,
    704,
    829,
    979,
)


def main() -> None:
    columns, rows = build_exact_cover()
    data = json.loads((HERE / "packing.json").read_text())
    selected = tuple(data["selected_rows"])
    assert len(selected) == len(set(selected)) == 132

    covered_list = [
        column
        for row in selected
        for column in rows[row]
    ]
    covered = frozenset(covered_list)
    assert len(covered_list) == len(covered) == 660

    active_rows = frozenset(
        row
        for row, current_columns in rows.items()
        if covered.isdisjoint(current_columns)
    )
    empty_columns = tuple(
        column
        for column in sorted(columns)
        if column not in covered and not (columns[column] & active_rows)
    )
    assert empty_columns == EXPECTED_EMPTY_COLUMNS

    # Every one of the thirteen rows originally covering each empty column
    # conflicts with an already selected row on another required column.
    assert all(len(columns[column]) == 13 for column in empty_columns)
    assert all(
        any(other in covered for other in rows[row] if other != column)
        for column in empty_columns
        for row in columns[column]
    )

    print("PASS committed 132 rows cover 660 distinct quotient columns")
    print("PASS 14 uncovered columns have no compatible remaining row")
    print("PASS every blocked option has a literal selected-column conflict")
    print(
        "SCOPE: this fixed 132-row packing has no full 228-row extension; "
        "other packings remain open"
    )


if __name__ == "__main__":
    main()
