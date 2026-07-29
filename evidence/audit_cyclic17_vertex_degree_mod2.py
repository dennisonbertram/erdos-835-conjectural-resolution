#!/usr/bin/env python3
"""Exact GF(2) audit of the fixed-Wallis C17 degree equalities.

The Boolean degree relaxation has 47,880 primary phase variables.  Every
phase exactly-one constraint, prescribed-hole cross exactly-one constraint,
and vertex-degree equality is also a linear equality modulo 2.  This script
constructs those equalities independently and performs exact bit-vector
Gaussian elimination.

If the augmented system were inconsistent, the recorded XOR of named input
rows would be a portable obstruction to the necessary degree relaxation.
If it is consistent, that is only a negative obstruction test: it is neither
a Boolean witness nor evidence for the full radius-five quotient or
Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from audit_cyclic17_vertex_degree_structure import (
    FIXED_PAIRS,
    P,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    forbidden_shifts,
    translate,
    zero_positions,
)
from global_latin_audit import construct_golf17


class GF2Eliminator:
    def __init__(self) -> None:
        self.pivots: dict[int, tuple[int, int, int]] = {}
        self.row_names: list[str] = []
        self.contradiction: tuple[int, str] | None = None

    def add(self, bits: int, rhs: int, name: str) -> None:
        if self.contradiction is not None:
            return
        row_id = len(self.row_names)
        self.row_names.append(name)
        combination = 1 << row_id
        rhs &= 1
        while bits:
            pivot = bits.bit_length() - 1
            previous = self.pivots.get(pivot)
            if previous is None:
                self.pivots[pivot] = (bits, rhs, combination)
                return
            previous_bits, previous_rhs, previous_combination = previous
            bits ^= previous_bits
            rhs ^= previous_rhs
            combination ^= previous_combination
        if rhs:
            self.contradiction = combination, name

    @property
    def rank(self) -> int:
        return len(self.pivots)

    @property
    def rows(self) -> int:
        return len(self.row_names)

    def contradiction_names(self) -> list[str]:
        if self.contradiction is None:
            return []
        combination, _ = self.contradiction
        return [
            self.row_names[row_id]
            for row_id in range(len(self.row_names))
            if (combination >> row_id) & 1
        ]


def mask(indices) -> int:
    answer = 0
    for index in indices:
        answer |= 1 << index
    return answer


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certificate",
        type=Path,
        help="write named XOR rows if a contradiction is found",
    )
    args = parser.parse_args()

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

    eliminator = GF2Eliminator()
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            eliminator.add(
                mask(
                    variable[i, j, orbit_index, shift]
                    for shift in domains[i, j, orbit_index]
                ),
                1,
                f"phase:{i},{j}:{orbit_index}",
            )
    phase_rank = eliminator.rank
    assert eliminator.rows == 4_200

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
                eliminator.add(
                    mask(literals),
                    1,
                    f"cross:{fixed_point}:{orbit_index}:{shift}",
                )
    phase_cross_rank = eliminator.rank
    assert eliminator.rows == 4_200 + 8_400

    for i, j in FIXED_PAIRS:
        for moving_point in POINTS:
            eliminator.add(
                mask(
                    variable[i, j, orbit_index, shift]
                    for orbit_index, representative
                    in enumerate(REPRESENTATIVES)
                    for shift in domains[i, j, orbit_index]
                    if moving_point in translate(representative, shift)
                ),
                8 if moving_point == 0 else 7,
                f"degree:{i},{j}:{moving_point}",
            )
    full_rank = eliminator.rank
    assert eliminator.rows == 4_200 + 8_400 + 1_785

    contradiction_names = eliminator.contradiction_names()
    certificate_sha256 = None
    if contradiction_names:
        encoded = (
            json.dumps(contradiction_names, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        certificate_sha256 = hashlib.sha256(encoded).hexdigest()
        if args.certificate is not None:
            args.certificate.write_bytes(encoded)

    report = {
        "status": (
            "INCONSISTENT_GF2"
            if contradiction_names
            else "CONSISTENT_GF2"
        ),
        "primary_variables": len(variable),
        "phase_rows": 4_200,
        "cross_rows": 8_400,
        "degree_rows": 1_785,
        "phase_rank_gf2": phase_rank,
        "phase_cross_rank_gf2": phase_cross_rank,
        "full_rank_gf2": full_rank,
        "nullity_gf2": len(variable) - full_rank,
        "contradiction_row_count": len(contradiction_names),
        "contradiction_certificate_sha256": certificate_sha256,
        "scope": (
            "linear parity relaxation only; consistency is not a witness"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
