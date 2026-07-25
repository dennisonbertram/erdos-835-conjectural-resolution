#!/usr/bin/env python3
"""Decode MathCheck2's 396 K_10 one-factorizations.

MathCheck2 stores one representative per line as positive SAT literals for a
partially fixed incidence matrix.  This script combines those literals with
the fixed matrix and emits a small, directly checkable catalogue.

Output format:

    CASE<TAB>FACTOR;FACTOR;...;FACTOR

Each factor consists of five comma-separated two-digit edges on vertices
0,...,9.  For example, ``01,23,45,67,89`` is the fixed first factor.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

MATRIX_WIDTH = 111
BLOCK_COLUMNS = tuple(range(21, 30))
RAW_VERTICES = (1, 3, 4, 5, 6, 7, 8, 9, 10, 11)
RAW_TO_VERTEX = {raw: vertex for vertex, raw in enumerate(RAW_VERTICES)}


def variable(row: int, column: int) -> int:
    return MATRIX_WIDTH * row + column + 1


def read_initial_matrix(path: Path) -> list[str]:
    rows = path.read_text().splitlines()
    if len(rows) != 66:
        raise ValueError(f"expected 66 matrix rows, found {len(rows)}")
    if any(len(row) != MATRIX_WIDTH for row in rows):
        raise ValueError("initial matrix does not have width 111")
    return rows


def row_edge(row: str) -> tuple[int, int]:
    endpoints = [index for index, entry in enumerate(row[:12]) if entry == "1"]
    if len(endpoints) != 2 or any(v not in RAW_TO_VERTEX for v in endpoints):
        raise ValueError(f"row is not an edge of the normalized K10: {row[:12]}")
    return tuple(sorted(RAW_TO_VERTEX[v] for v in endpoints))


def is_normalized_k10_edge(row: str) -> bool:
    endpoints = [index for index, entry in enumerate(row[:12]) if entry == "1"]
    return len(endpoints) == 2 and all(v in RAW_TO_VERTEX for v in endpoints)


def decode_case(
    initial: list[str],
    literal_line: str,
) -> tuple[tuple[tuple[int, int], ...], ...]:
    fields = literal_line.split()
    if fields[:1] != ["a"] or fields[-1:] != ["0"]:
        raise ValueError("expected a MathCheck assumption line")
    literals = {int(field) for field in fields[1:-1]}
    if len(literals) != 36 or any(literal <= 0 for literal in literals):
        raise ValueError("expected 36 distinct positive literals")

    factors: list[tuple[tuple[int, int], ...]] = []
    for column in BLOCK_COLUMNS:
        selected_rows = [
            row
            for row in range(len(initial))
            if is_normalized_k10_edge(initial[row])
            and (
                initial[row][column] == "1"
                or variable(row, column) in literals
            )
        ]
        if len(selected_rows) != 5:
            raise ValueError(
                f"column {column} has {len(selected_rows)} selected rows"
            )
        edges = tuple(sorted(row_edge(initial[row]) for row in selected_rows))
        flattened = [endpoint for edge in edges for endpoint in edge]
        if sorted(flattened) != list(range(10)):
            raise ValueError(f"column {column} is not a perfect matching")
        factors.append(edges)

    all_edges = [edge for factor in factors for edge in factor]
    expected = set(combinations(range(10), 2))
    if len(all_edges) != 45 or set(all_edges) != expected:
        raise ValueError("nine factors do not partition E(K10)")
    return tuple(factors)


def encode_case(
    case_number: int,
    factors: tuple[tuple[tuple[int, int], ...], ...],
) -> str:
    factor_strings = [
        ",".join(f"{left}{right}" for left, right in factor)
        for factor in factors
    ]
    return f"{case_number}\t" + ";".join(factor_strings)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_matrix", type=Path)
    parser.add_argument("assumptions", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    initial = read_initial_matrix(args.initial_matrix)
    assumption_lines = args.assumptions.read_text().splitlines()
    if len(assumption_lines) != 396:
        raise ValueError(
            f"expected 396 representatives, found {len(assumption_lines)}"
        )

    decoded = [
        decode_case(initial, line)
        for line in assumption_lines
    ]
    if len(set(decoded)) != 396:
        raise ValueError("decoded representatives are not all distinct")
    if any(
        factors[0] != ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9))
        for factors in decoded
    ):
        raise ValueError("fixed first-factor normalization was not recovered")

    output_lines = [
        "# MathCheck2 K10 one-factorizations, decoded and validated",
        "# format: case<TAB>five_edges;...;five_edges",
        *[
            encode_case(case_number, factors)
            for case_number, factors in enumerate(decoded, start=1)
        ],
    ]
    args.output.write_text("\n".join(output_lines) + "\n")
    print(f"decoded_factorizations={len(decoded)}")
    print("distinct_factorizations=396")
    print("edge_partition_checks=PASS")
    print("fixed_first_factor_checks=PASS")


if __name__ == "__main__":
    main()
