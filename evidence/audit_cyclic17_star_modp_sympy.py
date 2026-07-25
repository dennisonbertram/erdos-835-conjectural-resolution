#!/usr/bin/env python3
"""Exact finite-field incidence audit for one cyclic Wallis star.

For a chosen fixed centre this independently reconstructs the 6,384 primary
choice variables and the 2,800 exact-one equations of the necessary star
exact-cover problem:

* 560 phase-cell equations;
* 1,680 residual-moving-edge equations; and
* 560 allowed centre-phase cross equations.

It computes the exact augmented sparse RREF over a requested prime field.  An
augmented-column pivot would prove that the star exact cover is impossible,
and hence exclude the full fixed-Wallis C17 ansatz.  Consistency is only a
failed linear-obstruction test, not a star witness.  This does not address
the unrestricted Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

from sympy.polys.domains import GF
from sympy.polys.matrices.sdm import SDM


EVIDENCE = Path(__file__).resolve().parent
BALL = EVIDENCE / "odd_graph_local_ball"
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from improve_radius5_golf_cyclic_slice_lns import domains_for_seed
from search_radius5_golf_cyclic_compact import (
    MOVING_EDGES,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    translate,
)


def incident_pair(first: int, second: int) -> tuple[int, int]:
    return min(first, second), max(first, second)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--centre", type=int, default=0)
    parser.add_argument("--prime", type=int, required=True)
    args = parser.parse_args()
    if args.centre not in SQUARES:
        parser.error("--centre must lie in 0,...,14")
    if not is_prime(args.prime):
        parser.error("--prime must be prime")

    golf = construct_golf17()
    domains = domains_for_seed(golf)
    pairs = tuple(
        incident_pair(args.centre, other)
        for other in SQUARES
        if other != args.centre
    )
    primary_keys = tuple(
        (fixed_pair, orbit_index, shift)
        for fixed_pair in pairs
        for orbit_index in range(len(REPRESENTATIVES))
        for shift in sorted(domains[fixed_pair + (orbit_index,)])
    )
    variable = {
        key: index for index, key in enumerate(primary_keys)
    }
    assert len(variable) == 6_384

    field = GF(args.prime)
    rows = {}
    row_names = []

    def add(indices, name: str) -> None:
        row = {index: field.one for index in indices}
        row[len(variable)] = field.one
        rows[len(rows)] = row
        row_names.append(name)

    for fixed_pair in pairs:
        for orbit_index in range(len(REPRESENTATIVES)):
            add(
                (
                    variable[fixed_pair, orbit_index, shift]
                    for shift in domains[fixed_pair + (orbit_index,)]
                ),
                f"cell:{fixed_pair[0]},{fixed_pair[1]}:{orbit_index}",
            )
    cell_rows = len(rows)
    assert cell_rows == 560

    translated = {
        (orbit_index, shift): translate(representative, shift)
        for orbit_index, representative in enumerate(REPRESENTATIVES)
        for shift in POINTS
    }
    for fixed_pair in pairs:
        i, j = fixed_pair
        leave = {
            edge
            for edge in MOVING_EDGES
            if golf[i][edge[0]][edge[1]] == 0
            or golf[j][edge[0]][edge[1]] == 0
        }
        assert len(leave) == 16
        for edge in MOVING_EDGES:
            if edge in leave:
                continue
            literals = [
                variable[fixed_pair, orbit_index, shift]
                for orbit_index in range(len(REPRESENTATIVES))
                for shift in domains[fixed_pair + (orbit_index,)]
                if set(edge) <= set(translated[orbit_index, shift])
            ]
            assert literals
            add(
                literals,
                f"residual:{fixed_pair[0]},{fixed_pair[1]}:"
                f"{edge[0]},{edge[1]}",
            )
    residual_rows = len(rows) - cell_rows
    assert residual_rows == 1_680

    for orbit_index in range(len(REPRESENTATIVES)):
        forbidden = {
            shift
            for shift in POINTS
            if any(
                golf[args.centre][x][y] == 0
                for x, y in combinations(
                    translated[orbit_index, shift], 2
                )
            )
        }
        assert len(forbidden) == 3
        for shift in POINTS:
            if shift in forbidden:
                continue
            literals = [
                variable[fixed_pair, orbit_index, shift]
                for fixed_pair in pairs
                if (fixed_pair, orbit_index, shift) in variable
            ]
            assert literals
            add(
                literals,
                f"cross:{args.centre}:{orbit_index}:{shift}",
            )
    cross_rows = len(rows) - cell_rows - residual_rows
    assert cross_rows == 560
    assert len(rows) == 2_800

    matrix = SDM(
        rows,
        (len(rows), len(variable) + 1),
        field,
    )
    _, pivots = matrix.rref()
    inconsistent = len(variable) in pivots
    coefficient_rank = len(pivots) - int(inconsistent)
    report = {
        "status": (
            f"INCONSISTENT_GF{args.prime}"
            if inconsistent
            else f"CONSISTENT_GF{args.prime}"
        ),
        "centre": args.centre,
        "prime": args.prime,
        "primary_variables": len(variable),
        "cell_rows": cell_rows,
        "residual_edge_rows": residual_rows,
        "cross_phase_rows": cross_rows,
        "total_rows": len(rows),
        "coefficient_rank": coefficient_rank,
        "nullity": len(variable) - coefficient_rank,
        "augmented_column_is_pivot": inconsistent,
        "portable_named_row_certificate": False,
        "scope": (
            "centre-star linear finite-field relaxation only; "
            "consistency is not a star witness"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
