#!/usr/bin/env python3
"""Verify every zero-B five-core branch by support-union row rank."""

from __future__ import annotations

from collections import Counter
from itertools import combinations_with_replacement, product

from verify_r0_core_pairs import embeddings
from verify_r0_six_seven_four_exceptional import minimum_edges as mixed_minimum
from verify_r0_six_seven_k6 import (
    compatible_candidates,
    minimum_edges as pure_d_minimum,
)
from verify_r0_six_seven_two_exceptional import (
    REUSE_CAPACITY,
    SUPPORT_SIZE,
    compatible_pool,
    core_data,
)


KINDS = ("5111", "31111", "6")


def minimum_for_pattern(
    kinds: tuple[str, ...],
    union_order: int,
) -> tuple[str, int | None]:
    exceptional = tuple(kind for kind in kinds if kind != "6")
    if not exceptional:
        first_support, first_edges, d_pool = compatible_candidates("6")
        return pure_d_minimum(
            5,
            union_order,
            first_support,
            first_edges,
            d_pool,
        )

    first_kind = exceptional[0]
    first = embeddings(first_kind)[0]
    first_support, first_edges = core_data(first)
    counts = Counter(exceptional)
    counts[first_kind] -= 1
    groups = [
        (count, compatible_pool(first, kind))
        for kind, count in counts.items()
        if count
    ]
    return mixed_minimum(
        5,
        union_order,
        first_support,
        first_edges,
        groups,
        compatible_pool(first, "6"),
        exceptional_count=len(exceptional),
    )


def maximum_triple_supply(
    kinds: tuple[str, ...],
    union_order: int,
) -> int:
    slots = [
        min(3, union_order - SUPPORT_SIZE[kind])
        for kind in kinds
    ]
    return max(
        sum(
            multiplicity * slot
            for multiplicity, slot in zip(split, slots)
        )
        for split in product(
            *[
                range(1, REUSE_CAPACITY[kind] + 1)
                for kind in kinds
            ]
        )
        if sum(split) == 7
    )


def main() -> None:
    histogram: Counter[tuple[int, int]] = Counter()
    patterns = tuple(combinations_with_replacement(KINDS, 5))
    assert len(patterns) == 21

    for kinds in patterns:
        for union_order in range(
            max(SUPPORT_SIZE[kind] for kind in kinds),
            14,
        ):
            status, edge_count = minimum_for_pattern(
                kinds,
                union_order,
            )
            if edge_count is None:
                assert status == "INFEASIBLE", (
                    kinds,
                    union_order,
                    status,
                )
                continue
            assert status == "OPTIMAL", (
                kinds,
                union_order,
                status,
            )
            histogram[union_order, edge_count] += 1

            lower_occurrences = 2 * edge_count - 2 * union_order
            upper_occurrences = 15 + maximum_triple_supply(
                kinds,
                union_order,
            )
            assert lower_occurrences > upper_occurrences, (
                kinds,
                union_order,
                edge_count,
                lower_occurrences,
                upper_occurrences,
            )

    assert histogram == Counter(
        {
            (7, 20): 3,
            (7, 21): 3,
            (8, 22): 4,
            (8, 23): 6,
            (8, 24): 6,
            (8, 25): 4,
            (8, 26): 1,
            (9, 27): 4,
            (9, 28): 10,
        }
    )

    print("PASS rebuilt all twenty-one zero-B five-core type multisets")
    print("PASS exact feasible-union histogram matches the note")
    print("PASS every unlisted union order is graph-screen infeasible")
    print("PASS all positive multiplicity vectors were maximized")
    print("PASS full support-union row rank excludes every branch")
    print("SCOPE: all exactly-five-core type multisets over A,C,D")


if __name__ == "__main__":
    main()
