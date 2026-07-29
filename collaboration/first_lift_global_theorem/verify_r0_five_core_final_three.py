#!/usr/bin/env python3
"""Verify the final three zero-B five-core type patterns."""

from __future__ import annotations

from collections import Counter
from itertools import product

from verify_r0_core_pairs import embeddings
from verify_r0_six_seven_four_exceptional import minimum_edges
from verify_r0_six_seven_two_exceptional import (
    REUSE_CAPACITY,
    SUPPORT_SIZE,
    compatible_pool,
    core_data,
)


def main() -> None:
    cases = {
        ("5111", "31111", "31111", "31111", "31111"): {
            "d_count": 0,
            "minima": {8: 22, 9: 28},
        },
        ("31111", "31111", "31111", "31111", "31111"): {
            "d_count": 0,
            "minima": {7: 20, 8: 24},
        },
        ("31111", "31111", "31111", "31111"): {
            "d_count": 1,
            "minima": {7: 20, 8: 23},
        },
    }

    for pattern, case in cases.items():
        d_count = case["d_count"]
        minima = case["minima"]
        first_kind = pattern[0]
        first = embeddings(first_kind)[0]
        first_support, first_edges = core_data(first)
        counts = Counter(pattern)
        counts[first_kind] -= 1
        groups = [
            (count, compatible_pool(first, kind))
            for kind, count in counts.items()
            if count
        ]
        d_pool = compatible_pool(first, "6")
        support_sizes = [SUPPORT_SIZE[kind] for kind in pattern]
        capacities = [REUSE_CAPACITY[kind] for kind in pattern]
        support_sizes.extend([6] * d_count)
        capacities.extend([REUSE_CAPACITY["6"]] * d_count)

        for union_order in range(max(support_sizes), 14):
            status, edge_count = minimum_edges(
                5,
                union_order,
                first_support,
                first_edges,
                groups,
                d_pool,
                exceptional_count=len(pattern),
            )
            if union_order in minima:
                assert status == "OPTIMAL"
                assert edge_count == minima[union_order]
            else:
                assert status == "INFEASIBLE"
                assert edge_count is None
            if edge_count is None:
                continue

            slots = [
                min(3, union_order - support_size)
                for support_size in support_sizes
            ]
            maximum_triple_incidence = max(
                sum(
                    multiplicity * slot
                    for multiplicity, slot in zip(split, slots)
                )
                for split in product(
                    *[
                        range(1, capacity + 1)
                        for capacity in capacities
                    ]
                )
                if sum(split) == 7
            )
            lower_occurrences = 2 * edge_count - 2 * union_order
            upper_occurrences = 15 + maximum_triple_incidence
            assert lower_occurrences > upper_occurrences

    print("PASS exact minima for AC^4, C^5, and C^4D match the note")
    print("PASS every unlisted union order is graph-screen infeasible")
    print("PASS all positive multiplicity vectors were maximized")
    print("PASS full support-union row rank excludes every branch")
    print("SCOPE: final three zero-B five-core type patterns")


if __name__ == "__main__":
    main()
