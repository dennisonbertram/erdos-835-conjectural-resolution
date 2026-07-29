#!/usr/bin/env python3
"""Stdlib-only audit of the fixed-Wallis C17 degree reduction.

This independently reconstructs the objects used by the reduced degree
models.  It checks the prescribed-hole multidesign, the forced aggregate
degrees, and the nonsingular fifteen-edge basis which reduces 1,785 degree
equations to 1,440.  It does not solve the degree system or the full
radius-five quotient.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from global_latin_audit import construct_golf17


P = 17
POINTS = tuple(range(P))
SQUARES = tuple(range(15))
FIXED_PAIRS = tuple(combinations(SQUARES, 2))
MOVING_EDGES = tuple(combinations(POINTS, 2))
MOVING_TRIPLES = tuple(combinations(POINTS, 3))


def translate(subset, amount):
    return tuple(sorted((value + amount) % P for value in subset))


def triple_representatives():
    representatives = []
    unseen = set(MOVING_TRIPLES)
    while unseen:
        seed = min(unseen)
        representative = min(
            translate(seed, shift) for shift in POINTS
        )
        representatives.append(representative)
        for shift in POINTS:
            unseen.discard(translate(representative, shift))
    assert len(representatives) == 40
    return tuple(representatives)


REPRESENTATIVES = triple_representatives()


def edge_coordinate(edge):
    x, y = edge
    forward = (y - x) % P
    if forward <= 8:
        return forward, x
    return P - forward, y


REPRESENTATIVE_EDGE_COORDINATES = tuple(
    tuple(
        edge_coordinate(edge)
        for edge in combinations(representative, 2)
    )
    for representative in REPRESENTATIVES
)


def zero_positions(golf):
    answer = {}
    for square in SQUARES:
        for edge in MOVING_EDGES:
            if golf[square][edge[0]][edge[1]] != 0:
                continue
            difference, position = edge_coordinate(edge)
            key = square, difference
            assert key not in answer
            answer[key] = position
    assert len(answer) == 15 * 8
    return answer


def forbidden_shifts(zeros):
    answer = {}
    for square in SQUARES:
        for orbit_index, coordinates in enumerate(
            REPRESENTATIVE_EDGE_COORDINATES
        ):
            values = frozenset(
                (zeros[square, difference] - offset) % P
                for difference, offset in coordinates
            )
            assert len(values) == 3
            answer[square, orbit_index] = values
    return answer


def rational_rank(matrix):
    rows = [
        [Fraction(value) for value in row]
        for row in matrix
    ]
    rank = 0
    columns = len(rows[0]) if rows else 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, len(rows))
                if rows[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                left - scale * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def matching_cycle_profile(first, second):
    adjacency = {point: [] for point in range(1, 17)}
    for matching in (first, second):
        for point, mate in matching.items():
            if point < mate:
                adjacency[point].append(mate)
                adjacency[mate].append(point)
    assert all(len(neighbours) == 2 for neighbours in adjacency.values())
    unseen = set(adjacency)
    lengths = []
    while unseen:
        start = min(unseen)
        previous = None
        current = start
        length = 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            left, right = adjacency[current]
            following = left if left != previous else right
            previous, current = current, following
        lengths.append(length)
    return tuple(sorted(lengths))


def main() -> None:
    golf = construct_golf17()
    zeros = zero_positions(golf)
    forbidden = forbidden_shifts(zeros)

    matchings = []
    for square in SQUARES:
        matching = {}
        for x, y in combinations(range(1, 17), 2):
            if golf[square][x][y] == 0:
                matching[x] = y
                matching[y] = x
        assert len(matching) == 16
        matchings.append(matching)

    pair_profiles = {
        (i, j): matching_cycle_profile(matchings[i], matchings[j])
        for i, j in FIXED_PAIRS
    }
    factor_signatures = {}
    for i in SQUARES:
        factor_signatures[i] = tuple(
            sorted(
                Counter(
                    pair_profiles[min(i, j), max(i, j)]
                    for j in SQUARES
                    if j != i
                ).items()
            )
        )
    signature_classes = {}
    for square, signature in factor_signatures.items():
        signature_classes.setdefault(signature, []).append(square)
    assert len(signature_classes) == 14
    assert sorted(
        tuple(values)
        for values in signature_classes.values()
        if len(values) > 1
    ) == [(2, 11)]
    assert factor_signatures[1] not in {
        factor_signatures[2],
        factor_signatures[11],
    }
    assert pair_profiles[1, 2] != pair_profiles[1, 11]

    # The cycle-profile fingerprints force every matching label to be fixed.
    # A point automorphism fixing all labels is determined by the image q of
    # point 1: it must send mate_i(1) to mate_i(q) for all fifteen factors.
    label_fixed_point_automorphisms = []
    for image_of_one in range(1, 17):
        permutation = {1: image_of_one}
        for matching in matchings:
            permutation[matching[1]] = matching[image_of_one]
        if len(permutation) != 16:
            continue
        if len(set(permutation.values())) != 16:
            continue
        if all(
            matchings[square][permutation[point]]
            == permutation[matchings[square][point]]
            for square in SQUARES
            for point in range(1, 17)
        ):
            label_fixed_point_automorphisms.append(permutation)
    assert len(label_fixed_point_automorphisms) == 1
    assert label_fixed_point_automorphisms[0] == {
        point: point for point in range(1, 17)
    }

    singleton_holes = Counter()
    triple_vertex_counts = Counter()
    triple_pair_counts = Counter()
    triple_hole_multiplicities = Counter()
    for orbit_index in range(len(REPRESENTATIVES)):
        for shift in POINTS:
            holes = tuple(
                square
                for square in SQUARES
                if shift in forbidden[square, orbit_index]
            )
            assert len(holes) in (1, 3)
            if len(holes) == 1:
                singleton_holes[holes[0]] += 1
            else:
                triple_hole_multiplicities[holes] += 1
                triple_vertex_counts.update(holes)
                triple_pair_counts.update(combinations(holes, 2))

    assert singleton_holes == Counter(
        {square: 8 for square in SQUARES}
    )
    assert sum(triple_hole_multiplicities.values()) == 560
    assert triple_vertex_counts == Counter(
        {square: 112 for square in SQUARES}
    )
    assert triple_pair_counts == Counter(
        {fixed_pair: 16 for fixed_pair in FIXED_PAIRS}
    )

    domain_totals = Counter()
    domain_size_distribution = Counter()
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            domain_size = sum(
                shift not in forbidden[i, orbit_index]
                and shift not in forbidden[j, orbit_index]
                for shift in POINTS
            )
            domain_totals[i, j] += domain_size
            domain_size_distribution[domain_size] += 1
    assert set(domain_totals.values()) == {456}
    assert domain_size_distribution == Counter(
        {11: 2658, 12: 1407, 13: 132, 14: 3}
    )

    target = tuple(
        14 * (8 if point == 0 else 7)
        for point in POINTS
    )
    for square in SQUARES:
        aggregate = Counter()
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            for shift in POINTS:
                if shift in forbidden[square, orbit_index]:
                    continue
                aggregate.update(translate(representative, shift))
        assert tuple(aggregate[point] for point in POINTS) == target

    omitted_pairs = (
        (0, 1),
        (1, 2),
        (0, 2),
        *((0, square) for square in range(3, 15)),
    )
    incidence = [
        [
            int(square in fixed_pair)
            for fixed_pair in omitted_pairs
        ]
        for square in SQUARES
    ]
    omitted_basis_rank = rational_rank(incidence)
    assert omitted_basis_rank == 15

    report = {
        "status": "PASS",
        "scope": (
            "fixed-Wallis C17 vertex-degree structure only; "
            "no degree witness and no full radius-five result"
        ),
        "triple_orbits": len(REPRESENTATIVES),
        "singleton_holes": sum(singleton_holes.values()),
        "singleton_holes_per_square": 8,
        "triple_holes_with_multiplicity": sum(
            triple_hole_multiplicities.values()
        ),
        "distinct_triple_holes": len(
            triple_hole_multiplicities
        ),
        "triple_hole_vertex_multiplicity": 112,
        "triple_hole_pair_multiplicity": 16,
        "allowed_phases_per_fixed_pair": 456,
        "phase_domain_size_distribution": dict(
            sorted(domain_size_distribution.items())
        ),
        "primary_phase_literals": sum(domain_totals.values()),
        "aggregate_degree_at_zero": target[0],
        "aggregate_degree_at_nonzero": target[1],
        "omitted_pair_basis_rank": omitted_basis_rank,
        "zero_factorization_automorphism_group_order": 1,
        "raw_degree_equalities": 105 * 17,
        "independent_degree_equalities": 90 * 16,
    }
    assert report["primary_phase_literals"] == 47880
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
