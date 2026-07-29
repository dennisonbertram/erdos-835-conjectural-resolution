#!/usr/bin/env python3
"""Verify the exact three-layer full repair of the r=1 dead prefix."""

from __future__ import annotations

from itertools import combinations

from verify_r1_minimum_layer_repair import build_instance


VERTICES = frozenset(range(13))
CORE = frozenset(range(6))
OUTSIDE = VERTICES - CORE
ALL_EDGES = frozenset(combinations(sorted(VERTICES), 2))

FULL_COMPLETION = (
    ((0, 12), (1, 11), (2, 10), (3, 9), (4, 8), (5, 7)),
    ((2, 12), (3, 11), (4, 10), (5, 9)),
    ((0, 11), (2, 9), (4, 7), (5, 12)),
    ((0, 4), (1, 3), (6, 12), (7, 11), (8, 10)),
    ((1, 5), (2, 4), (8, 12), (9, 11)),
    ((0, 1), (3, 5), (7, 8), (10, 12)),
    ((0, 3), (1, 2), (6, 11), (7, 10), (8, 9)),
    ((0, 10), (1, 12), (2, 11), (3, 6), (4, 5)),
    ((0, 9), (1, 8), (2, 5), (3, 12), (4, 6)),
    ((0, 7), (1, 9), (2, 6), (3, 4), (5, 11)),
    ((0, 6), (1, 4), (2, 8), (3, 7), (5, 10)),
    ((0, 5), (1, 6), (2, 3), (4, 11), (9, 10)),
    ((0, 2), (1, 7), (3, 8), (4, 12), (5, 6)),
    ((0, 8), (6, 10), (7, 9), (11, 12)),
    ((1, 10), (6, 9), (7, 12), (8, 11)),
    ((2, 7), (3, 10), (6, 8), (9, 12)),
    ((4, 9), (5, 8), (6, 7), (10, 11)),
)


def endpoints(matching: frozenset[tuple[int, int]]) -> frozenset[int]:
    return frozenset(vertex for current in matching for vertex in current)


def cross_capacity(support: frozenset[int]) -> int:
    return min(len(support & CORE), len(support & OUTSIDE))


def main() -> None:
    selected, selected_supports, remaining_supports = build_instance()
    supports = (*selected_supports, *remaining_supports)
    cut = frozenset(
        (left, right)
        for left in CORE
        for right in OUTSIDE
    )

    assert len(cut) == len(CORE) * len(OUTSIDE) == 42
    assert all(current.isdisjoint(cut) for current in selected)

    remaining_capacities = tuple(map(cross_capacity, remaining_supports))
    selected_capacities = tuple(map(cross_capacity, selected_supports))
    assert remaining_capacities == (4, 4, 4, 4, 4, 4, 1, 1, 2, 2)
    assert sum(remaining_capacities) == 30
    assert selected_capacities == (6, 4, 4, 4, 4, 4, 4)
    assert (
        sum(remaining_capacities)
        + sum(sorted(selected_capacities, reverse=True)[:2])
        == 40
        < len(cut)
    )

    completion = tuple(
        frozenset(tuple(sorted(current)) for current in matching)
        for matching in FULL_COMPLETION
    )
    assert len(completion) == len(supports) == 17
    assert all(
        len(current) * 2 == len(endpoints(current))
        for current in completion
    )
    assert all(
        endpoints(current) == support
        for current, support in zip(completion, supports)
    )
    assert completion[3:7] == tuple(selected[3:7])
    assert all(completion[index] != selected[index] for index in range(3))

    completion_union = frozenset().union(*completion)
    assert sum(map(len, completion)) == len(completion_union) == 78
    assert completion_union == ALL_EDGES

    print("PASS original seven-prefix uses no edge of the 42-edge 6:7 cut")
    print("PASS ten unselected supports have total cut capacity 30")
    print("PASS any two changed selected layers raise capacity to at most 40")
    print("PASS displayed completion changes exactly selected colours 0,1,2")
    print("PASS displayed seventeen matchings partition all 78 edges of K13")
    print("PASS exact full-completion repair distance is three")
    print("SCOPE: this r=1 dead prefix only; not a universal switching theorem")


if __name__ == "__main__":
    main()
