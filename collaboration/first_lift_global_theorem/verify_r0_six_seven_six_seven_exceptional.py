#!/usr/bin/env python3
"""Verify the six- and seven-non-K6 endgame for six/seven cores."""

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


def candidate_data(
    pattern: tuple[str, ...],
) -> tuple[
    frozenset[int],
    frozenset[int],
    list[
        tuple[
            int,
            list[tuple[frozenset[int], frozenset[int]]],
        ]
    ],
    list[tuple[frozenset[int], frozenset[int]]],
]:
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
    return (
        first_support,
        first_edges,
        groups,
        compatible_pool(first, "6"),
    )


def scan_pattern(
    pattern: tuple[str, ...],
    core_count: int,
) -> list[tuple[int, int]]:
    exceptional_count = len(pattern)
    first_support, first_edges, groups, d_pool = candidate_data(pattern)
    rows = []
    for union_order in range(
        max(SUPPORT_SIZE[kind] for kind in pattern),
        14,
    ):
        status, edge_count = minimum_edges(
            core_count,
            union_order,
            first_support,
            first_edges,
            groups,
            d_pool,
            exceptional_count=exceptional_count,
        )
        if edge_count is None:
            assert status == "INFEASIBLE", (
                pattern,
                core_count,
                union_order,
                status,
            )
            continue
        assert status == "OPTIMAL", (
            pattern,
            core_count,
            union_order,
            status,
        )

        exceptional_slots = [
            min(3, union_order - SUPPORT_SIZE[kind])
            for kind in pattern
        ]
        d_slots = min(3, union_order - 6)
        triple_slots = (
            sum(exceptional_slots)
            + (core_count - exceptional_count) * d_slots
        )
        if core_count == 6:
            eligible_extras = [
                exceptional_slots[index]
                for index, kind in enumerate(pattern)
                if REUSE_CAPACITY[kind] >= 2
            ]
            assert eligible_extras
            triple_slots += max(eligible_extras)

        lower_occurrences = 2 * edge_count - 2 * union_order
        upper_occurrences = 15 + triple_slots
        assert lower_occurrences > upper_occurrences, (
            pattern,
            core_count,
            union_order,
            edge_count,
            lower_occurrences,
            upper_occurrences,
        )
        rows.append((union_order, edge_count))
    return rows


def main() -> None:
    six_core_histogram: Counter[tuple[int, int]] = Counter()
    seven_core_six_exceptional_histogram: Counter[tuple[int, int]] = Counter()
    for pattern in combinations_with_replacement(KINDS, 6):
        if all(REUSE_CAPACITY[kind] < 2 for kind in pattern):
            assert pattern == ("3311",) * 6
            assert sum(REUSE_CAPACITY[kind] for kind in pattern) < 7
        else:
            six_core_histogram.update(scan_pattern(pattern, 6))
        seven_core_six_exceptional_histogram.update(
            scan_pattern(pattern, 7)
        )

    assert six_core_histogram == Counter(
        {
            (7, 21): 1,
            (8, 22): 3,
            (8, 23): 1,
            (8, 24): 2,
            (8, 25): 21,
            (9, 27): 1,
            (9, 28): 4,
            (9, 30): 1,
        }
    )
    assert seven_core_six_exceptional_histogram == Counter(
        {
            (7, 21): 1,
            (8, 23): 4,
            (8, 24): 1,
            (8, 25): 23,
            (9, 27): 1,
            (9, 28): 4,
            (9, 30): 1,
        }
    )

    seven_core_histogram: Counter[tuple[int, int]] = Counter()
    for pattern in combinations_with_replacement(KINDS, 7):
        seven_core_histogram.update(scan_pattern(pattern, 7))
    assert seven_core_histogram == Counter(
        {
            (7, 21): 1,
            (8, 22): 2,
            (8, 24): 3,
            (8, 25): 31,
            (9, 27): 1,
            (9, 28): 4,
        }
    )

    print("PASS rebuilt all 28 six-exceptional type multisets")
    print("PASS six-core B^6 branch fails its reuse ceiling")
    print("PASS rebuilt all 36 seven-exceptional type multisets")
    print("PASS exact feasible-union histograms match the note")
    print("PASS every unlisted union order is graph-screen infeasible")
    print("PASS full row-rank inequality excludes every surviving branch")
    print("SCOPE: six/seven cores with six or seven non-K6 cores")


if __name__ == "__main__":
    main()
