#!/usr/bin/env python3
"""Exact GF(3) audit of the fixed-Wallis C17 degree equalities.

This independently reduces all 4,200 phase equations, 8,400 prescribed-hole
cross equations, and 1,785 vertex-degree equations modulo 3.  Coefficient
vectors and (when requested) row-combination certificates are represented by
two disjoint Python bitsets, so Gaussian elimination is exact.

An inconsistent augmented system would exclude the necessary Boolean degree
relaxation.  A consistent system is only a failed linear-obstruction test; it
is not a witness and says nothing by itself about the full radius-five
quotient or Erdos--Rosenfeld problem 835.
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
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    forbidden_shifts,
    translate,
    zero_positions,
)
from global_latin_audit import construct_golf17


def add_vectors(
    first_ones: int,
    first_twos: int,
    second_ones: int,
    second_twos: int,
) -> tuple[int, int]:
    """Add two disjoint-bitset coefficient vectors modulo 3."""

    first_nonzero = first_ones | first_twos
    second_nonzero = second_ones | second_twos
    result_ones = (
        (second_ones & ~first_nonzero)
        | (first_ones & ~second_nonzero)
        | (first_twos & second_twos)
    )
    result_twos = (
        (second_twos & ~first_nonzero)
        | (first_twos & ~second_nonzero)
        | (first_ones & second_ones)
    )
    assert not (result_ones & result_twos)
    return result_ones, result_twos


class GF3Eliminator:
    def __init__(self, *, track_certificate: bool) -> None:
        self.pivots: dict[
            int, tuple[int, int, int, int, int]
        ] = {}
        self.track_certificate = track_certificate
        self.row_names: list[str] = []
        self.contradiction: tuple[int, int] | None = None

    def add(self, ones: int, rhs: int, name: str) -> None:
        if self.contradiction is not None:
            return
        row_id = len(self.row_names)
        self.row_names.append(name)
        twos = 0
        rhs %= 3
        combination_ones = 1 << row_id if self.track_certificate else 0
        combination_twos = 0
        while ones | twos:
            pivot = (ones | twos).bit_length() - 1
            previous = self.pivots.get(pivot)
            if previous is None:
                # Store every pivot normalized to coefficient one.
                if (twos >> pivot) & 1:
                    ones, twos = twos, ones
                    rhs = (-rhs) % 3
                    combination_ones, combination_twos = (
                        combination_twos,
                        combination_ones,
                    )
                self.pivots[pivot] = (
                    ones,
                    twos,
                    rhs,
                    combination_ones,
                    combination_twos,
                )
                return
            (
                previous_ones,
                previous_twos,
                previous_rhs,
                previous_combination_ones,
                previous_combination_twos,
            ) = previous
            if (ones >> pivot) & 1:
                # current <- current - previous = current + 2*previous.
                ones, twos = add_vectors(
                    ones,
                    twos,
                    previous_twos,
                    previous_ones,
                )
                rhs = (rhs - previous_rhs) % 3
                if self.track_certificate:
                    combination_ones, combination_twos = add_vectors(
                        combination_ones,
                        combination_twos,
                        previous_combination_twos,
                        previous_combination_ones,
                    )
            else:
                assert (twos >> pivot) & 1
                # current <- current - 2*previous = current + previous.
                ones, twos = add_vectors(
                    ones,
                    twos,
                    previous_ones,
                    previous_twos,
                )
                rhs = (rhs - 2 * previous_rhs) % 3
                if self.track_certificate:
                    combination_ones, combination_twos = add_vectors(
                        combination_ones,
                        combination_twos,
                        previous_combination_ones,
                        previous_combination_twos,
                    )
        if rhs:
            self.contradiction = combination_ones, combination_twos

    @property
    def rank(self) -> int:
        return len(self.pivots)

    @property
    def rows(self) -> int:
        return len(self.row_names)

    def contradiction_rows(self) -> list[dict[str, object]]:
        if self.contradiction is None:
            return []
        ones, twos = self.contradiction
        return [
            {
                "coefficient": (
                    1 if (ones >> row_id) & 1 else 2
                ),
                "row": self.row_names[row_id],
            }
            for row_id in range(len(self.row_names))
            if ((ones | twos) >> row_id) & 1
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
        help="write a named GF(3) row combination if inconsistent",
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

    eliminator = GF3Eliminator(
        track_certificate=args.certificate is not None
    )
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

    contradiction_rows = eliminator.contradiction_rows()
    certificate_sha256 = None
    if contradiction_rows:
        encoded = (
            json.dumps(contradiction_rows, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        certificate_sha256 = hashlib.sha256(encoded).hexdigest()
        if args.certificate is not None:
            args.certificate.write_bytes(encoded)

    report = {
        "status": (
            "INCONSISTENT_GF3"
            if eliminator.contradiction is not None
            else "CONSISTENT_GF3"
        ),
        "primary_variables": len(variable),
        "phase_rows": 4_200,
        "cross_rows": 8_400,
        "degree_rows": 1_785,
        "phase_rank_gf3": phase_rank,
        "phase_cross_rank_gf3": phase_cross_rank,
        "full_rank_gf3": full_rank,
        "nullity_gf3": len(variable) - full_rank,
        "contradiction_row_count": len(contradiction_rows),
        "contradiction_certificate_sha256": certificate_sha256,
        "scope": (
            "linear modulo-3 relaxation only; consistency is not a witness"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
