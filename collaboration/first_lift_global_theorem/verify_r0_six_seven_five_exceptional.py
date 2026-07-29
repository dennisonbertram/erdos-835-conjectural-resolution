#!/usr/bin/env python3
"""Verify six-/seven-core branches with five non-K6 cores."""

from __future__ import annotations

from collections import Counter
from itertools import combinations_with_replacement

from verify_r0_core_pairs import embeddings
from verify_r0_six_seven_four_exceptional import minimum_edges
from verify_r0_six_seven_two_exceptional import (
    KINDS,
    REUSE_CAPACITY,
    SUPPORT_SIZE,
    compatible_pool,
    core_data,
)


def main() -> None:
    expected = {
        ("5111", "5111", "5111", "5111", "5111"): {
            6: {8: 25, 9: 28},
            7: {8: 25, 9: 28},
        },
        ("5111", "5111", "5111", "5111", "3311"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "5111", "5111", "5111", "31111"): {
            6: {8: 23, 9: 28},
            7: {8: 24, 9: 28},
        },
        ("5111", "5111", "5111", "3311", "3311"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "5111", "5111", "3311", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "5111", "5111", "31111", "31111"): {
            6: {8: 23, 9: 28},
            7: {8: 24, 9: 28},
        },
        ("5111", "5111", "3311", "3311", "3311"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "5111", "3311", "3311", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "5111", "3311", "31111", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "5111", "31111", "31111", "31111"): {
            6: {8: 23, 9: 27},
            7: {8: 24, 9: 27},
        },
        ("5111", "3311", "3311", "3311", "3311"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "3311", "3311", "3311", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "3311", "3311", "31111", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "3311", "31111", "31111", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "31111", "31111", "31111", "31111"): {
            6: {8: 23, 9: 28},
            7: {8: 23, 9: 28},
        },
        ("3311", "3311", "3311", "3311", "3311"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("3311", "3311", "3311", "3311", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("3311", "3311", "3311", "31111", "31111"): {
            6: {8: 25, 9: 30},
            7: {8: 25},
        },
        ("3311", "3311", "31111", "31111", "31111"): {
            6: {8: 25, 9: 29},
            7: {8: 25},
        },
        ("3311", "31111", "31111", "31111", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("31111", "31111", "31111", "31111", "31111"): {
            6: {7: 20, 8: 24},
            7: {7: 20, 8: 24},
        },
    }

    for pattern in combinations_with_replacement(KINDS, 5):
        first_kind = pattern[0]
        first = embeddings(first_kind)[0]
        first_support, first_edges = core_data(first)
        counts = Counter(pattern)
        counts[first_kind] -= 1
        groups = []
        for kind, count in counts.items():
            if count:
                groups.append((count, compatible_pool(first, kind)))
        d_pool = compatible_pool(first, "6")

        for core_count in (6, 7):
            first_order = max(SUPPORT_SIZE[kind] for kind in pattern)
            for union_order in range(first_order, 14):
                status, edge_count = minimum_edges(
                    core_count,
                    union_order,
                    first_support,
                    first_edges,
                    groups,
                    d_pool,
                    exceptional_count=5,
                )
                minima = expected[pattern][core_count]
                if union_order in minima:
                    assert status == "OPTIMAL", (
                        pattern,
                        core_count,
                        union_order,
                        status,
                    )
                    assert edge_count == minima[union_order], (
                        pattern,
                        core_count,
                        union_order,
                        edge_count,
                    )
                else:
                    assert status == "INFEASIBLE", (
                        pattern,
                        core_count,
                        union_order,
                        status,
                        edge_count,
                    )
                    assert edge_count is None
                if edge_count is None:
                    continue

                exceptional_slots = [
                    min(3, union_order - SUPPORT_SIZE[kind])
                    for kind in pattern
                ]
                d_slots = min(3, union_order - 6)
                triple_slots = (
                    sum(exceptional_slots)
                    + (core_count - 5) * d_slots
                )
                if core_count == 6:
                    extras = [d_slots]
                    extras.extend(
                        exceptional_slots[index]
                        for index, kind in enumerate(pattern)
                        if REUSE_CAPACITY[kind] >= 2
                    )
                    triple_slots += max(extras)

                lower_occurrences = 2 * edge_count - 2 * union_order
                upper_occurrences = 15 + triple_slots
                assert lower_occurrences > upper_occurrences

    print("PASS rebuilt all twenty-one five-exceptional type quintuples")
    print("PASS exact minimum union orders and edge counts match the note")
    print("PASS every unlisted union order is graph-screen infeasible")
    print("PASS full row-rank inequality excludes every surviving branch")
    print("SCOPE: six/seven cores with exactly five non-K6 cores")


if __name__ == "__main__":
    main()
