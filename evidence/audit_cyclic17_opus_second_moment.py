#!/usr/bin/env python3
"""Audit the ambiguous Opus second-moment identity over F_17.

This checks only the fixed-Wallis, C17-equivariant radius-five quotient.  It
does not construct that quotient and says nothing by itself about the full
Erdos--Rosenfeld problem.

For each moving-triple orbit we use its unique representative whose three
points sum to zero.  If z[i,d] is the cyclic position of the zero edge of
difference d in Wallis square i, an edge with coordinate (d,p) forbids phase
z[i,d]-p.  The script evaluates the first and second forbidden-phase moments
directly and also verifies their short starter-algebra explanation.
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from audit_cyclic17_phase_sums_mod17 import (
    DIFFERENCES,
    MOVING_TRIPLES,
    P,
    POINTS,
    SQUARES,
    edge_coordinate,
    translate,
    zero_positions,
)
from global_latin_audit import FIRST_HALF_COLUMNS, construct_golf17


def zero_sum_triple_representatives() -> list[tuple[int, int, int]]:
    unseen = set(MOVING_TRIPLES)
    representatives = []
    inverse_three = pow(3, -1, P)
    while unseen:
        seed = min(unseen)
        representative = translate(
            seed, (-sum(seed) * inverse_three) % P
        )
        assert sum(representative) % P == 0
        representatives.append(representative)
        for shift in POINTS:
            unseen.discard(translate(representative, shift))
    assert len(representatives) == 40
    return representatives


def main() -> None:
    representatives = zero_sum_triple_representatives()
    zeros = zero_positions(construct_golf17())

    position_count = {difference: 0 for difference in DIFFERENCES}
    position_sum = {difference: 0 for difference in DIFFERENCES}
    position_square_sum = {difference: 0 for difference in DIFFERENCES}
    coordinates = []
    for representative in representatives:
        current = tuple(
            edge_coordinate(edge)
            for edge in combinations(representative, 2)
        )
        coordinates.append(current)
        for difference, position in current:
            position_count[difference] += 1
            position_sum[difference] = (
                position_sum[difference] + position
            ) % P
            position_square_sum[difference] = (
                position_square_sum[difference] + position**2
            ) % P

    assert position_count == {difference: 15 for difference in DIFFERENCES}
    assert position_sum == {
        difference: difference for difference in DIFFERENCES
    }
    assert sum(position_square_sum.values()) % P == 0

    forbidden_first = []
    forbidden_second = []
    zero_factor_first = []
    starter_first = []
    starter_second_relation = []
    for square in SQUARES:
        first = 0
        second = 0
        for current in coordinates:
            forbidden = {
                (zeros[square, difference] - position) % P
                for difference, position in current
            }
            assert len(forbidden) == 3
            first = (first + sum(forbidden)) % P
            second = (second + sum(value**2 for value in forbidden)) % P
        forbidden_first.append(first)
        forbidden_second.append(second)

        z_values = [zeros[square, difference] for difference in DIFFERENCES]
        a_values = [(-value) % P for value in z_values]
        zero_factor_first.append(sum(z_values) % P)
        starter_first.append(sum(a_values) % P)
        starter_second_relation.append(
            (
                sum(value**2 for value in a_values)
                - sum(
                    difference * value
                    for difference, value in zip(DIFFERENCES, a_values)
                )
            )
            % P
        )

    # These are forced by the cyclic starter being a permutation:
    # sum_d a_d = 1 and sum_d a_d^2 = sum_d d*a_d.
    assert starter_first == [1] * len(SQUARES)
    assert zero_factor_first == [P - 1] * len(SQUARES)
    assert starter_second_relation == [0] * len(SQUARES)

    # Consequently both aggregate forbidden moments vanish.
    assert forbidden_first == [0] * len(SQUARES)
    assert forbidden_second == [0] * len(SQUARES)

    # With the only natural scalar supplied by the expansion,
    # s_i = sum_d z[i,d] (or its sign-reversed starter convention), the
    # proposed Phi_i - Phi_j + 5(s_i^2-s_j^2) identity is 0=0.
    natural_identity = [
        (
            forbidden_second[i]
            - forbidden_second[j]
            + 5 * (zero_factor_first[i] ** 2 - zero_factor_first[j] ** 2)
        )
        % P
        for i, j in combinations(SQUARES, 2)
    ]
    assert natural_identity == [0] * len(natural_identity)

    # If s_i instead means the visibly varying Wallis square label a_i(1),
    # the statement is false; this guards against silently changing meanings.
    square_labels = list(FIRST_HALF_COLUMNS[0])
    label_identity = [
        (
            forbidden_second[i]
            - forbidden_second[j]
            + 5 * (square_labels[i] ** 2 - square_labels[j] ** 2)
        )
        % P
        for i, j in combinations(SQUARES, 2)
    ]
    label_violations = sum(value != 0 for value in label_identity)
    assert label_violations > 0

    print("Opus fixed-Wallis second-moment audit over F_17: PASS")
    print("zero-sum triple representatives: 40")
    print(f"aggregate forbidden first moments: {forbidden_first}")
    print(f"aggregate forbidden second moments Phi_i: {forbidden_second}")
    print(f"natural zero-factor first moments s_i: {zero_factor_first}")
    print("natural-s_i identity: VALID BUT TAUTOLOGICAL")
    print(
        "varying-label interpretation: FALSE "
        f"({label_violations}/105 pairs violate it)"
    )
    print("new independent constraint: NONE")


if __name__ == "__main__":
    main()
