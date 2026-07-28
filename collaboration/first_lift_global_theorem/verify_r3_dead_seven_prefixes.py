#!/usr/bin/env python3
"""Verify two dead-but-fully-completable r=3 seven-prefixes."""

from __future__ import annotations

from collections import Counter
from itertools import combinations


VERTICES = frozenset(range(13))
ALL_EDGES = frozenset(combinations(sorted(VERTICES), 2))
U = frozenset(range(7))


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def matching(*pairs: tuple[int, int]) -> frozenset[tuple[int, int]]:
    return frozenset(edge(*pair) for pair in pairs)


def endpoints(edges: frozenset[tuple[int, int]]) -> frozenset[int]:
    return frozenset(vertex for current in edges for vertex in current)


def perfect_matching(
    support: frozenset[int],
    allowed: frozenset[tuple[int, int]],
) -> tuple[tuple[int, int], ...] | None:
    if not support:
        return ()
    first = min(support)
    for second in sorted(support - {first}):
        current = edge(first, second)
        if current not in allowed:
            continue
        rest = perfect_matching(
            support - {first, second},
            allowed,
        )
        if rest is not None:
            return (current, *rest)
    return None


CASES = {
    "C_in_G": {
        "prefix": (
            matching((0, 5), (2, 6), (3, 4), (7, 10)),
            matching((0, 4), (1, 3), (2, 5), (7, 9)),
            matching((1, 2), (3, 5), (4, 6), (10, 12)),
            matching((0, 2), (1, 4), (3, 6), (8, 12)),
            matching((0, 6), (1, 5), (2, 3), (7, 12), (8, 9)),
            matching(
                (0, 1),
                (2, 4),
                (3, 11),
                (5, 6),
                (7, 8),
                (9, 10),
            ),
            matching(
                (0, 3),
                (1, 6),
                (2, 11),
                (4, 5),
                (8, 10),
                (9, 12),
            ),
        ),
        "remaining_complements": (
            frozenset({0, 1, 2, 3, 5}),
            frozenset({1, 2, 3, 4, 5}),
            frozenset({0, 1, 2, 4, 6}),
            frozenset({0, 2, 3, 4, 6}),
            frozenset({1, 2, 3, 5, 6}),
            frozenset({0, 3, 4, 5, 6}),
            frozenset({7, 8, 9}),
            frozenset({7, 10, 12}),
            frozenset({8, 9, 10}),
            frozenset({12}),
        ),
        "full_completion": (
            matching((0, 4), (2, 10), (3, 5), (6, 7)),
            matching((0, 1), (2, 9), (3, 4), (5, 7)),
            matching((1, 4), (2, 3), (5, 6), (10, 12)),
            matching((0, 3), (1, 2), (4, 8), (6, 12)),
            matching((0, 8), (1, 12), (2, 7), (3, 6), (5, 9)),
            matching(
                (0, 7),
                (1, 10),
                (2, 4),
                (3, 9),
                (5, 11),
                (6, 8),
            ),
            matching(
                (0, 2),
                (1, 3),
                (4, 9),
                (5, 8),
                (6, 10),
                (11, 12),
            ),
            matching((4, 7), (6, 9), (8, 12), (10, 11)),
            matching((0, 10), (6, 11), (7, 8), (9, 12)),
            matching((3, 8), (5, 12), (7, 11), (9, 10)),
            matching((1, 9), (5, 10), (7, 12), (8, 11)),
            matching((0, 11), (4, 12), (7, 9), (8, 10)),
            matching((1, 11), (2, 12), (7, 10), (8, 9)),
            matching((0, 12), (1, 5), (2, 6), (3, 10), (4, 11)),
            matching((0, 9), (1, 8), (2, 5), (3, 11), (4, 6)),
            matching((0, 6), (1, 7), (2, 11), (3, 12), (4, 5)),
            matching(
                (0, 5),
                (1, 6),
                (2, 8),
                (3, 7),
                (4, 10),
                (9, 11),
            ),
        ),
        "size_ten_core": (
            frozenset(combinations(sorted(U), 2))
            - frozenset(combinations((0, 1, 2), 2))
        ),
    },
    "D_in_G": {
        "prefix": (
            matching((0, 6), (1, 2), (3, 5), (8, 12)),
            matching((0, 5), (1, 6), (2, 4), (7, 11)),
            matching((1, 3), (2, 5), (4, 6), (7, 12)),
            matching((0, 1), (3, 4), (5, 6), (9, 11)),
            matching((0, 4), (1, 5), (2, 3), (7, 9), (8, 11)),
            matching(
                (0, 3),
                (2, 6),
                (4, 5),
                (7, 8),
                (9, 12),
                (10, 11),
            ),
            matching(
                (0, 2),
                (1, 4),
                (3, 6),
                (7, 10),
                (8, 9),
                (11, 12),
            ),
        ),
        "remaining_complements": (
            frozenset({0, 1, 2, 3, 4}),
            frozenset({1, 2, 3, 4, 5}),
            frozenset({0, 1, 2, 5, 6}),
            frozenset({0, 1, 3, 5, 6}),
            frozenset({2, 3, 4, 5, 6}),
            frozenset({0, 4, 7, 11, 12}),
            frozenset({6, 7, 8}),
            frozenset({7, 9, 11}),
            frozenset({8, 9, 11}),
            frozenset({12}),
        ),
        "full_completion": (
            matching((0, 8), (1, 3), (2, 6), (5, 12)),
            matching((0, 4), (1, 6), (2, 5), (7, 11)),
            matching((1, 7), (2, 4), (3, 12), (5, 6)),
            matching((0, 6), (1, 4), (3, 11), (5, 9)),
            matching((0, 5), (1, 2), (3, 7), (4, 11), (8, 9)),
            matching(
                (0, 2),
                (3, 10),
                (4, 5),
                (6, 7),
                (8, 12),
                (9, 11),
            ),
            matching(
                (0, 7),
                (1, 12),
                (2, 11),
                (3, 9),
                (4, 10),
                (6, 8),
            ),
            matching((5, 11), (6, 9), (7, 12), (8, 10)),
            matching((0, 10), (6, 11), (7, 8), (9, 12)),
            matching((3, 8), (4, 7), (9, 10), (11, 12)),
            matching((2, 12), (4, 9), (7, 10), (8, 11)),
            matching((0, 11), (1, 8), (7, 9), (10, 12)),
            matching((1, 9), (2, 8), (3, 5), (6, 10)),
            matching((0, 3), (1, 5), (2, 9), (4, 12), (10, 11)),
            matching((0, 12), (1, 10), (2, 3), (4, 6), (5, 8)),
            matching((0, 1), (2, 7), (3, 4), (5, 10), (6, 12)),
            matching(
                (0, 9),
                (1, 11),
                (2, 10),
                (3, 6),
                (4, 8),
                (5, 7),
            ),
        ),
        "size_ten_core": frozenset(combinations(range(6), 2)),
    },
}


def verify_case(name: str, case: dict[str, object]) -> None:
    prefix = case["prefix"]
    remaining_complements = case["remaining_complements"]
    full_completion = case["full_completion"]
    size_ten_core = case["size_ten_core"]
    assert isinstance(prefix, tuple)
    assert isinstance(remaining_complements, tuple)
    assert isinstance(full_completion, tuple)
    assert isinstance(size_ten_core, frozenset)

    assert tuple(map(len, prefix)) == (4, 4, 4, 4, 5, 6, 6)
    assert all(len(endpoints(current)) == 2 * len(current) for current in prefix)
    prefix_union = frozenset().union(*prefix)
    assert sum(map(len, prefix)) == len(prefix_union) == 33

    selected_supports = tuple(endpoints(current) for current in prefix)
    assert Counter(map(len, selected_supports)) == {8: 4, 10: 1, 12: 2}
    assert tuple(map(len, remaining_complements)) == (
        5,
        5,
        5,
        5,
        5,
        5,
        3,
        3,
        3,
        1,
    )
    remaining_supports = tuple(
        VERTICES - complement for complement in remaining_complements
    )
    all_supports = (*selected_supports, *remaining_supports)
    assert Counter(map(len, all_supports)) == {8: 10, 10: 4, 12: 3}
    assert all(
        sum(vertex in support for support in all_supports) == 12
        for vertex in VERTICES
    )

    degrees = {
        vertex: sum(vertex in current for current in prefix_union)
        for vertex in VERTICES
    }
    assert all(
        sum(vertex in complement for complement in remaining_complements)
        == degrees[vertex] - 2
        for vertex in VERTICES
    )

    large_core = frozenset(combinations(sorted(U), 2))
    assert large_core <= prefix_union
    assert size_ten_core <= prefix_union
    assert all(
        endpoints(size_ten_core) <= support
        for support in remaining_supports[6:9]
    )
    assert endpoints(large_core) <= remaining_supports[9]

    residual = ALL_EDGES - prefix_union
    assert all(
        perfect_matching(support, residual) is None
        for support in remaining_supports
    )

    assert len(full_completion) == len(all_supports) == 17
    assert all(
        len(endpoints(current)) == 2 * len(current)
        for current in full_completion
    )
    assert all(
        endpoints(current) == support
        for current, support in zip(full_completion, all_supports)
    )
    full_union = frozenset().union(*full_completion)
    assert sum(map(len, full_completion)) == len(full_union) == 78
    assert full_union == ALL_EDGES
    assert full_completion[:7] != prefix

    print(f"PASS {name}: dead seven-prefix blocks all ten remaining supports")
    print(f"PASS {name}: same support instance has a full 17-matching completion")


def main() -> None:
    for name, case in CASES.items():
        verify_case(name, case)
    print("PASS both class-B profiles are (10,4,3) with row sum twelve")
    print("SCOPE: two dead arbitrary prefixes; both instances fully complete")


if __name__ == "__main__":
    main()
