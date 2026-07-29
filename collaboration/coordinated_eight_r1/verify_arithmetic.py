#!/usr/bin/env python3
"""Verify the finite arithmetic in the coordinated r=1 proof."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import comb


def choose(top: int, bottom: int) -> int:
    if top < bottom or bottom < 0:
        return 0
    return comb(top, bottom)


def miss_probability(
    five_degree: int,
    triple_degree: int,
) -> Fraction:
    return (
        Fraction(choose(8 - five_degree, 4), choose(8, 4))
        * Fraction(choose(8 - triple_degree, 2), choose(8, 2))
    )


def verify_covering_lemma() -> None:
    nonsingleton = tuple(
        miss_probability(five_degree, 5 - five_degree)
        for five_degree in range(6)
    )
    singleton = tuple(
        miss_probability(five_degree, 4 - five_degree)
        for five_degree in range(5)
    )
    assert nonsingleton == (
        Fraction(3, 28),
        Fraction(3, 28),
        Fraction(15, 196),
        Fraction(15, 392),
        Fraction(3, 280),
        Fraction(0),
    )
    assert singleton == (
        Fraction(3, 14),
        Fraction(5, 28),
        Fraction(45, 392),
        Fraction(3, 56),
        Fraction(1, 70),
    )
    assert all(
        probability <= Fraction(3 * (5 - five_degree), 112)
        for five_degree, probability in enumerate(nonsingleton)
    )

    expectation_bounds = tuple(
        Fraction(3 * (20 + singleton_five_degree), 112)
        + singleton[singleton_five_degree]
        for singleton_five_degree in range(5)
    )
    assert expectation_bounds == (
        Fraction(3, 4),
        Fraction(83, 112),
        Fraction(69, 98),
        Fraction(75, 112),
        Fraction(23, 35),
    )
    assert max(expectation_bounds) == Fraction(3, 4) < 1
    assert 8 * 5 == 40
    print("PASS r=1 six-complement cover has expectation at most 3/4")


def odd_partitions(total: int, parts: int, minimum: int = 1):
    if parts == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, total + 1, 2):
        for rest in odd_partitions(total - first, parts - 1, first):
            yield (first, *rest)


def core_edge_count(blocks: tuple[int, ...]) -> int:
    total = sum(blocks)
    return (
        total * total - sum(block * block for block in blocks)
    ) // 2


def core_maximum_degree(blocks: tuple[int, ...]) -> int:
    return sum(blocks) - min(blocks)


def verify_size_ten_cores() -> None:
    survivors = []
    for separator_size in range(5):
        outside = 10 - separator_size
        block_count = separator_size + 2
        for blocks in odd_partitions(outside, block_count):
            if core_maximum_degree(blocks) <= 5:
                survivors.append((separator_size, blocks))
    assert survivors == [
        (0, (5, 5)),
        (4, (1, 1, 1, 1, 1, 1)),
    ]
    assert core_edge_count((5, 5)) == 25
    assert core_edge_count((1, 1, 1, 1, 1, 1)) == 15

    selected_edges = 4 * 4 + 2 * 5
    other_remaining_complement_capacity = 4 * 5 + 1
    assert selected_edges == 26
    assert selected_edges - 25 == 1
    assert selected_edges - 15 == 11
    assert 10 * (5 - 1) == 40 > other_remaining_complement_capacity
    assert 6 * (5 - 1) == 24 > other_remaining_complement_capacity
    print("PASS only K5,5 and K6 survive the size-ten core screen")
    print("PASS saturated-core complement capacities exclude total blockage")


def least_odd_at_least(value: int) -> int:
    value = max(value, 1)
    return value if value % 2 else value + 1


def verify_twelve_vertex_resilience() -> None:
    possible = []
    for separator_size in range(12):
        odd_component_count = separator_size + 2
        outside = 12 - separator_size
        if odd_component_count > outside:
            continue
        minimum_order = least_odd_at_least(6 - separator_size)
        if odd_component_count * minimum_order <= outside:
            possible.append(
                (
                    separator_size,
                    odd_component_count,
                    minimum_order,
                    outside,
                )
            )
    assert possible == [(5, 7, 1, 7)]

    # A matching cannot saturate all seven singleton components.
    assert all(2 * matching_edges != 7 for matching_edges in range(7))
    print("PASS order-12 minimum-degree-six graph survives any matching deletion")


def verify_profile_arithmetic() -> None:
    assert (8, 8, 1) == (7 + 1, 10 - 2, 1)
    assert 8 * 8 + 8 * 10 + 12 == 156
    assert 4 * 5 + 2 * 3 == 26
    assert 6 * 13 - (4 * 8 + 2 * 10) == 26
    assert 12 - 5 == 7
    assert 7 - 1 == 6

    # Exhaust the identity rho=d_D-1 at every possible selected-complement
    # multiplicity sigma>=1.
    for sigma, degree in product(range(1, 6), range(6)):
        if degree != 6 - sigma:
            continue
        remaining_complements = 5 - sigma
        assert remaining_complements == degree - 1
    print("PASS profile, selected-degree, and remaining-complement identities")


def main() -> None:
    verify_covering_lemma()
    verify_size_ten_cores()
    verify_twelve_vertex_resilience()
    verify_profile_arithmetic()
    print("PASS universal coordinated eight-packing arithmetic for r=1")
    print("SCOPE: proof arithmetic; final nine colours remain open")


if __name__ == "__main__":
    main()
