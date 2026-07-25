#!/usr/bin/env python3
"""Sparse exact GF(p) diagnostic for the C17 degree equalities.

This constructs the augmented linear system consisting of all phase,
prescribed-hole cross, and vertex-degree equalities on the 47,880 primary
phase variables, then computes an exact sparse RREF over a requested prime
field using SymPy's domain-matrix implementation.

This is a diagnostic complement to the stdlib GF(2) and bit-sliced GF(3)
audits.  Consistency is only a failed linear-obstruction test, not a Boolean
witness.  If an inconsistency is ever reported, a separately checkable
named-row certificate is still required before treating it as an
impossibility result.  Nothing here addresses residual-edge collisions or
the full Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sympy.polys.domains import GF
from sympy.polys.matrices.sdm import SDM


EVIDENCE = Path(__file__).resolve().parent
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from audit_cyclic17_vertex_degree_structure import (
    FIXED_PAIRS,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    forbidden_shifts,
    translate,
    zero_positions,
)
from global_latin_audit import construct_golf17


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
    parser.add_argument("--prime", type=int, required=True)
    args = parser.parse_args()
    if not is_prime(args.prime):
        parser.error("--prime must be prime")

    golf = construct_golf17()
    forbidden = forbidden_shifts(zero_positions(golf))
    domains = {
        (i, j, orbit_index): tuple(
            shift
            for shift in POINTS
            if shift not in forbidden[i, orbit_index]
            and shift not in forbidden[j, orbit_index]
        )
        for i, j in FIXED_PAIRS
        for orbit_index in range(len(REPRESENTATIVES))
    }
    variable = {}
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in domains[i, j, orbit_index]:
                variable[i, j, orbit_index, shift] = len(variable)
    assert len(variable) == 47_880

    field = GF(args.prime)
    rows = {}
    row_id = 0

    def add(indices, rhs: int) -> None:
        nonlocal row_id
        row = {index: field.one for index in indices}
        reduced_rhs = rhs % args.prime
        if reduced_rhs:
            row[len(variable)] = field(reduced_rhs)
        rows[row_id] = row
        row_id += 1

    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            add(
                (
                    variable[i, j, orbit_index, shift]
                    for shift in domains[i, j, orbit_index]
                ),
                1,
            )
    assert row_id == 4_200

    for fixed_point in SQUARES:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in POINTS:
                if shift in forbidden[fixed_point, orbit_index]:
                    continue
                literals = []
                for other in SQUARES:
                    if other == fixed_point:
                        continue
                    i, j = sorted((fixed_point, other))
                    index = variable.get((i, j, orbit_index, shift))
                    if index is not None:
                        literals.append(index)
                assert literals
                add(literals, 1)
    assert row_id == 4_200 + 8_400

    for i, j in FIXED_PAIRS:
        for moving_point in POINTS:
            add(
                (
                    variable[i, j, orbit_index, shift]
                    for orbit_index, representative
                    in enumerate(REPRESENTATIVES)
                    for shift in domains[i, j, orbit_index]
                    if moving_point in translate(representative, shift)
                ),
                8 if moving_point == 0 else 7,
            )
    assert row_id == 4_200 + 8_400 + 1_785

    matrix = SDM(
        rows,
        (row_id, len(variable) + 1),
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
        "prime": args.prime,
        "primary_variables": len(variable),
        "phase_rows": 4_200,
        "cross_rows": 8_400,
        "degree_rows": 1_785,
        "coefficient_rank": coefficient_rank,
        "nullity": len(variable) - coefficient_rank,
        "augmented_column_is_pivot": inconsistent,
        "portable_named_row_certificate": False,
        "scope": (
            "linear finite-field relaxation only; "
            "consistency is not a witness"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
