#!/usr/bin/env python3
"""Verify a dead but fully completable r=5 arbitrary seven-prefix."""

from __future__ import annotations

from collections import Counter
from itertools import combinations


VERTICES = frozenset(range(13))
ALL_EDGES = frozenset(combinations(sorted(VERTICES), 2))


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
        rest = perfect_matching(support - {first, second}, allowed)
        if rest is not None:
            return (current, *rest)
    return None


def components(
    vertices: frozenset[int],
    allowed: frozenset[tuple[int, int]],
) -> tuple[frozenset[int], ...]:
    unseen = set(vertices)
    result = []
    while unseen:
        start = min(unseen)
        component = {start}
        frontier = [start]
        unseen.remove(start)
        while frontier:
            current = frontier.pop()
            neighbours = {
                other
                for other in tuple(unseen)
                if edge(current, other) in allowed
            }
            component.update(neighbours)
            unseen.difference_update(neighbours)
            frontier.extend(neighbours)
        result.append(frozenset(component))
    return tuple(sorted(result, key=lambda current: tuple(sorted(current))))


def first_tutte_barrier(
    support: frozenset[int],
    allowed: frozenset[tuple[int, int]],
) -> tuple[frozenset[int], tuple[frozenset[int], ...]] | None:
    for size in range(len(support)):
        for chosen in combinations(sorted(support), size):
            separator = frozenset(chosen)
            current_components = components(support - separator, allowed)
            odd_components = tuple(
                current
                for current in current_components
                if len(current) % 2
            )
            if len(odd_components) > len(separator):
                return separator, current_components
    return None


PREFIX = (
    matching((0, 2), (3, 6), (4, 7), (8, 10)),
    matching((0, 7), (1, 3), (2, 6), (8, 11)),
    matching((0, 6), (1, 4), (2, 7), (8, 9)),
    matching((0, 4), (1, 6), (2, 3), (9, 12)),
    matching(
        (0, 1),
        (2, 4),
        (3, 7),
        (5, 6),
        (8, 12),
        (10, 11),
    ),
    matching(
        (0, 3),
        (1, 7),
        (2, 5),
        (4, 6),
        (9, 11),
        (10, 12),
    ),
    matching(
        (1, 2),
        (3, 4),
        (5, 8),
        (6, 7),
        (9, 10),
        (11, 12),
    ),
)


REMAINING_COMPLEMENTS = (
    frozenset({0, 1, 2, 3, 4}),
    frozenset({0, 2, 3, 4, 6}),
    frozenset({1, 2, 3, 4, 6}),
    frozenset({0, 2, 3, 5, 7}),
    frozenset({0, 1, 4, 6, 7}),
    frozenset({6, 7, 8, 9, 11}),
    frozenset({1, 7, 8, 10, 11}),
    frozenset({2, 6, 9, 10, 12}),
    frozenset({8}),
    frozenset({12}),
)


TUTTE_SEPARATORS = (
    frozenset({5, 6, 7}),
    frozenset({1, 5, 7}),
    frozenset({0, 5, 7}),
    frozenset({1, 4, 6}),
    frozenset({2, 3, 5}),
    frozenset({5, 10, 12}),
    frozenset({5, 9, 12}),
    frozenset({5, 8, 11}),
    frozenset({5, 9, 10, 11, 12}),
    frozenset({5, 8, 9, 10, 11}),
)


FULL_COMPLETION = (
    matching((0, 10), (2, 8), (3, 7), (4, 6)),
    matching((0, 11), (1, 8), (2, 7), (3, 6)),
    matching((0, 9), (1, 7), (2, 6), (4, 8)),
    matching((0, 12), (1, 6), (2, 9), (3, 4)),
    matching(
        (0, 8),
        (1, 12),
        (2, 11),
        (3, 10),
        (4, 5),
        (6, 7),
    ),
    matching(
        (0, 7),
        (1, 11),
        (2, 12),
        (3, 9),
        (4, 10),
        (5, 6),
    ),
    matching(
        (1, 10),
        (2, 5),
        (3, 12),
        (4, 11),
        (6, 9),
        (7, 8),
    ),
    matching((5, 12), (6, 11), (7, 10), (8, 9)),
    matching((1, 9), (5, 11), (7, 12), (8, 10)),
    matching((0, 5), (7, 9), (8, 11), (10, 12)),
    matching((1, 4), (6, 10), (8, 12), (9, 11)),
    matching((2, 10), (3, 8), (5, 9), (11, 12)),
    matching((0, 3), (1, 2), (4, 12), (5, 10)),
    matching((0, 6), (2, 4), (3, 5), (9, 12)),
    matching((0, 4), (1, 3), (5, 8), (7, 11)),
    matching(
        (0, 1),
        (2, 3),
        (4, 9),
        (5, 7),
        (6, 12),
        (10, 11),
    ),
    matching(
        (0, 2),
        (1, 5),
        (3, 11),
        (4, 7),
        (6, 8),
        (9, 10),
    ),
)


# A saturated proper 17-colouring of K_18-E(K_13) inducing the same supports.
# PARTIAL_CROSS[target][outside] is the colour on the edge from target
# vertex 0..12 to outside vertex 0..4.  PARTIAL_INTERNAL lists the ten
# outside K_5 edges and their colours.
PARTIAL_CROSS = (
    (10, 8, 7, 6, 11),
    (7, 13, 9, 11, 0),
    (14, 9, 10, 7, 8),
    (2, 10, 8, 9, 7),
    (8, 7, 11, 1, 9),
    (0, 2, 3, 10, 1),
    (9, 11, 14, 8, 12),
    (11, 12, 13, 3, 10),
    (13, 5, 15, 12, 3),
    (1, 0, 12, 14, 4),
    (3, 14, 1, 13, 2),
    (12, 3, 0, 2, 13),
    (16, 1, 2, 0, 14),
)


PARTIAL_INTERNAL = (
    (0, 1, 15),
    (0, 2, 4),
    (0, 3, 5),
    (0, 4, 6),
    (1, 2, 6),
    (1, 3, 4),
    (1, 4, 16),
    (2, 3, 16),
    (2, 4, 5),
    (3, 4, 15),
)


def supports() -> tuple[frozenset[int], ...]:
    selected = tuple(endpoints(current) for current in PREFIX)
    remaining = tuple(
        VERTICES - complement
        for complement in REMAINING_COMPLEMENTS
    )
    return (*selected, *remaining)


def verify_partial_factorization(
    all_supports: tuple[frozenset[int], ...],
) -> None:
    colours = frozenset(range(17))
    outside = frozenset(range(5))
    missing = tuple(
        frozenset(
            colour
            for colour, support in enumerate(all_supports)
            if vertex not in support
        )
        for vertex in VERTICES
    )
    assert all(len(current) == 5 for current in missing)
    assert len(PARTIAL_CROSS) == 13
    assert all(len(row) == 5 for row in PARTIAL_CROSS)
    assert all(
        frozenset(row) == missing[vertex]
        for vertex, row in enumerate(PARTIAL_CROSS)
    )

    internal_edges = {
        edge(left, right): colour
        for left, right, colour in PARTIAL_INTERNAL
    }
    assert len(PARTIAL_INTERNAL) == len(internal_edges) == 10
    assert frozenset(internal_edges) == frozenset(combinations(sorted(outside), 2))
    for outside_vertex in outside:
        seen = {
            PARTIAL_CROSS[target][outside_vertex]
            for target in VERTICES
        }
        seen.update(
            colour
            for (left, right), colour in internal_edges.items()
            if outside_vertex in (left, right)
        )
        assert seen == colours


def verify() -> tuple[frozenset[int], ...]:
    assert tuple(map(len, PREFIX)) == (4, 4, 4, 4, 6, 6, 6)
    assert all(len(endpoints(current)) == 2 * len(current) for current in PREFIX)
    prefix_union = frozenset().union(*PREFIX)
    assert sum(map(len, PREFIX)) == len(prefix_union) == 34

    all_supports = supports()
    assert Counter(map(len, all_supports)) == {8: 12, 12: 5}
    selected_complements = tuple(
        VERTICES - support
        for support in all_supports[:7]
    )
    all_complements = (*selected_complements, *REMAINING_COMPLEMENTS)
    assert Counter(map(len, all_complements)) == {5: 12, 1: 5}
    assert all(
        sum(vertex in complement for complement in all_complements) == 5
        for vertex in VERTICES
    )
    assert all(
        sum(vertex in support for support in all_supports) == 12
        for vertex in VERTICES
    )

    degrees = {
        vertex: sum(vertex in current for current in prefix_union)
        for vertex in VERTICES
    }
    assert all(
        sum(vertex in complement for complement in REMAINING_COMPLEMENTS)
        == degrees[vertex] - 2
        for vertex in VERTICES
    )

    residual = ALL_EDGES - prefix_union
    remaining_supports = all_supports[7:]
    blocked_matchings = tuple(
        perfect_matching(support, residual)
        for support in remaining_supports
    )
    assert blocked_matchings == (None,) * 10
    barriers = tuple(
        first_tutte_barrier(support, residual)
        for support in remaining_supports
    )
    assert all(barrier is not None for barrier in barriers)
    for support, separator, barrier in zip(
        remaining_supports,
        TUTTE_SEPARATORS,
        barriers,
    ):
        assert separator <= support
        explicit_components = components(support - separator, residual)
        assert all(len(current) == 1 for current in explicit_components)
        assert len(explicit_components) > len(separator)
        assert barrier is not None
        found_separator, current_components = barrier
        assert (
            sum(len(current) % 2 for current in current_components)
            > len(found_separator)
        )

    assert len(FULL_COMPLETION) == len(all_supports) == 17
    assert all(
        endpoints(current) == support
        for current, support in zip(FULL_COMPLETION, all_supports)
    )
    assert all(
        len(endpoints(current)) == 2 * len(current)
        for current in FULL_COMPLETION
    )
    completion_union = frozenset().union(*FULL_COMPLETION)
    assert sum(map(len, FULL_COMPLETION)) == len(completion_union) == 78
    assert completion_union == ALL_EDGES
    assert FULL_COMPLETION[:7] != PREFIX
    verify_partial_factorization(all_supports)
    return all_supports


def main() -> None:
    verify()
    print("PASS seven prefix matchings have type 8^4 12^3 and 34 edges")
    print("PASS seventeen supports form a class-B profile (12,0,5)")
    print("PASS remaining complement rows equal d_F(v)-2 exactly")
    print("PASS all eight remaining size-8 supports are blocked")
    print("PASS both remaining size-12 supports are blocked")
    print("PASS same support matrix has a literal full 17-matching completion")
    print("PASS support matrix has a saturated partial K18 factorization")
    print("SCOPE: arbitrary seven-prefix extension fails at r=5")


if __name__ == "__main__":
    main()
