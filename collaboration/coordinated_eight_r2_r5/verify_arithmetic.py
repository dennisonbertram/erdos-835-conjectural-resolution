#!/usr/bin/env python3
"""Verify the finite arithmetic in the coordinated r=2,3,4,5 proof."""

from __future__ import annotations

from fractions import Fraction
from math import comb


def choose(top: int, bottom: int) -> int:
    if top < bottom or bottom < 0:
        return 0
    return comb(top, bottom)


def miss_probability(
    five_set_count: int,
    triple_count: int,
    five_degree: int,
    triple_degree: int,
) -> Fraction:
    return (
        Fraction(
            choose(five_set_count - five_degree, 4),
            choose(five_set_count, 4),
        )
        * Fraction(
            choose(triple_count - triple_degree, 2),
            choose(triple_count, 2),
        )
    )


def maxima_by_singleton_degree(r: int) -> tuple[Fraction, ...]:
    five_set_count = 7 + r
    triple_count = 10 - 2 * r
    maxima = []
    for singleton_degree in range(r + 1):
        values = []
        for five_degree in range(6 - singleton_degree):
            triple_degree = 5 - singleton_degree - five_degree
            if triple_degree > triple_count:
                continue
            values.append(
                miss_probability(
                    five_set_count,
                    triple_count,
                    five_degree,
                    triple_degree,
                )
            )
        maxima.append(max(values))
    return tuple(maxima)


def integer_partitions(total: int, maximum: int | None = None):
    if total == 0:
        yield ()
        return
    if maximum is None:
        maximum = total
    for first in range(min(total, maximum), 0, -1):
        for rest in integer_partitions(total - first, first):
            yield (first, *rest)


def expected_bound(
    singleton_partition: tuple[int, ...],
    maxima: tuple[Fraction, ...],
) -> Fraction:
    return sum(
        (maxima[degree] for degree in singleton_partition),
        start=Fraction(0),
    ) + (13 - len(singleton_partition)) * maxima[0]


def verify_covering_arithmetic() -> None:
    maxima_r2 = maxima_by_singleton_degree(2)
    assert maxima_r2 == (
        Fraction(1, 18),
        Fraction(1, 9),
        Fraction(2, 9),
    )
    r2_bounds = {
        partition: expected_bound(partition, maxima_r2)
        for partition in integer_partitions(2)
    }
    assert r2_bounds == {
        (2,): Fraction(8, 9),
        (1, 1): Fraction(5, 6),
    }
    assert max(r2_bounds.values()) < 1

    maxima_r3 = maxima_by_singleton_degree(3)
    assert maxima_r3 == (
        Fraction(1, 28),
        Fraction(1, 12),
        Fraction(1, 6),
        Fraction(1, 3),
    )
    r3_bounds = {
        partition: expected_bound(partition, maxima_r3)
        for partition in integer_partitions(3)
    }
    assert r3_bounds == {
        (3,): Fraction(16, 21),
        (2, 1): Fraction(9, 14),
        (1, 1, 1): Fraction(17, 28),
    }
    assert max(r3_bounds.values()) < 1

    maxima_r4 = maxima_by_singleton_degree(4)
    assert maxima_r4 == (
        Fraction(1, 22),
        Fraction(7, 66),
        Fraction(7, 33),
        Fraction(21, 55),
        Fraction(7, 11),
    )
    r4_bounds = {
        partition: expected_bound(partition, maxima_r4)
        for partition in integer_partitions(4)
    }
    assert r4_bounds[(3, 1)] == Fraction(163, 165)
    assert all(
        bound < 1
        for partition, bound in r4_bounds.items()
        if partition != (4,)
    )
    assert r4_bounds[(4,)] > 1

    # Exceptional fourfold singleton: either the repeated vertex lies in
    # a selected triple, or its unique five-set is selected first.
    assert 12 * Fraction(1, 22) == Fraction(6, 11) < 1
    assert 8 * Fraction(choose(5, 3), choose(10, 3)) == Fraction(2, 3) < 1

    miss_r5 = tuple(
        Fraction(choose(7 + singleton_degree, 4), choose(12, 4))
        * Fraction(choose(5 - singleton_degree, 2), choose(5, 2))
        for singleton_degree in range(6)
    )
    assert miss_r5 == (
        Fraction(7, 99),
        Fraction(14, 165),
        Fraction(21, 275),
        Fraction(7, 165),
        Fraction(0),
        Fraction(0),
    )
    r5_bounds = {
        partition: expected_bound(partition, miss_r5)
        for partition in integer_partitions(5)
    }
    assert len(r5_bounds) == 7
    assert max(r5_bounds.values()) == Fraction(98, 99)
    assert r5_bounds[(1, 1, 1, 1, 1)] == Fraction(98, 99)
    assert all(bound < 1 for bound in r5_bounds.values())
    print("PASS complement-cover expectation bounds for r=2,3,4,5")


def verify_profile_and_degree_arithmetic() -> None:
    for r in (2, 3, 4):
        profile = (7 + r, 10 - 2 * r, r)
        assert sum(profile) == 17
        assert 8 * profile[0] + 10 * profile[1] + 12 * profile[2] == 156
        assert profile[0] >= 4
        assert profile[1] >= 2
        assert profile[2] >= 2

        selected_support_incidence = 4 * 8 + 2 * 10
        selected_complement_incidence = 4 * 5 + 2 * 3
        assert selected_support_incidence == 52
        assert selected_complement_incidence == 26
        assert 6 * 13 - selected_support_incidence == 26

    r = 5
    profile = (7 + r, 10 - 2 * r, r)
    assert profile == (12, 0, 5)
    assert sum(profile) == 17
    assert 8 * profile[0] + 12 * profile[2] == 156
    selected_support_incidence = 4 * 8 + 2 * 12
    selected_complement_incidence = 4 * 5 + 2
    assert selected_support_incidence == 56
    assert selected_complement_incidence == 22
    assert 6 * 13 - selected_support_incidence == 22
    assert 8 >= 2 * 4
    assert 12 >= 2 * 5
    assert 12 >= 2 * 6
    assert profile[2] - 2 >= 2

    # Four size-eight matchings delete at most four incident edges from a
    # size-ten clique, leaving minimum degree at least five.
    assert 9 - 4 == 5

    # A complement cover makes every vertex occur in at most five of the
    # selected six supports.  The residual K13 therefore has minimum
    # degree seven, meeting Ore's n+1 degree-sum threshold.
    assert 12 - 5 == 7
    assert 2 * 7 == 13 + 1

    # If the two singleton complements coincide, deleting that vertex
    # leaves the Dirac threshold on twelve vertices.
    assert 7 - 1 == 12 // 2
    print("PASS support counts and Hamiltonian degree thresholds")


def main() -> None:
    verify_covering_arithmetic()
    verify_profile_and_degree_arithmetic()
    print("PASS universal coordinated-eight arithmetic for r=2,3,4,5")
    print("SCOPE: proof arithmetic; r=1 and full completion remain open")


if __name__ == "__main__":
    main()
