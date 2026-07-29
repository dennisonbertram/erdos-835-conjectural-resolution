#!/usr/bin/env python3
"""Verify the exact dead seven-prefix in the r=1 support profile."""

from __future__ import annotations

from collections import Counter
from itertools import combinations


VERTICES = tuple(range(13))
CORE_VERTICES = frozenset(range(6))
OUTSIDE_VERTICES = frozenset(range(6, 13))
EDGES = tuple(combinations(VERTICES, 2))
FULL_COMPLETION = (
    ((0, 12), (1, 11), (2, 10), (3, 9), (4, 8), (5, 7)),
    ((2, 3), (4, 12), (5, 11), (9, 10)),
    ((0, 11), (2, 12), (4, 7), (5, 9)),
    ((0, 10), (1, 12), (3, 11), (4, 6), (7, 8)),
    ((1, 9), (2, 11), (4, 5), (8, 12)),
    ((0, 8), (1, 10), (3, 7), (5, 12)),
    ((0, 9), (1, 8), (2, 7), (3, 10), (6, 11)),
    ((0, 6), (1, 5), (2, 4), (3, 12), (10, 11)),
    ((0, 4), (1, 2), (3, 5), (6, 8), (9, 12)),
    ((0, 1), (2, 5), (3, 6), (4, 11), (7, 9)),
    ((0, 5), (1, 3), (2, 8), (4, 10), (6, 7)),
    ((0, 3), (1, 4), (2, 6), (5, 10), (9, 11)),
    ((0, 2), (1, 7), (3, 4), (5, 8), (6, 12)),
    ((0, 7), (6, 9), (8, 11), (10, 12)),
    ((1, 6), (7, 10), (8, 9), (11, 12)),
    ((2, 9), (3, 8), (6, 10), (7, 12)),
    ((4, 9), (5, 6), (7, 11), (8, 10)),
)


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def round_robin_colour(left: int, right: int) -> int:
    """Colour an edge of K7 on Z/7 by half its endpoint sum."""
    return 4 * (left + right) % 7


def has_perfect_matching(
    support: frozenset[int],
    allowed: frozenset[tuple[int, int]],
) -> bool:
    if not support:
        return True
    first = min(support)
    for second in support:
        if second == first or edge(first, second) not in allowed:
            continue
        if has_perfect_matching(
            support - {first, second},
            allowed,
        ):
            return True
    return False


def main() -> None:
    colour_classes = [set() for _ in range(7)]

    # K6 is obtained from the round-robin K7 after deleting residue 0.
    c_residue = {vertex: vertex + 1 for vertex in CORE_VERTICES}
    for left, right in combinations(CORE_VERTICES, 2):
        colour = round_robin_colour(
            c_residue[left],
            c_residue[right],
        )
        colour_classes[colour].add(edge(left, right))

    # On O, remove four differently coloured edges incident with residue 0.
    removed_star = frozenset(
        edge(6, 6 + leaf)
        for leaf in (1, 2, 3, 4)
    )
    assert {
        round_robin_colour(0, leaf)
        for leaf in (1, 2, 3, 4)
    } == {1, 2, 4, 5}
    for left, right in combinations(OUTSIDE_VERTICES, 2):
        current = edge(left, right)
        if current in removed_star:
            continue
        colour = round_robin_colour(left - 6, right - 6)
        colour_classes[colour].add(current)

    expected_sizes = {
        0: 6,
        1: 4,
        2: 4,
        3: 5,
        4: 4,
        5: 4,
        6: 5,
    }
    assert {
        colour: len(matching)
        for colour, matching in enumerate(colour_classes)
    } == expected_sizes
    for matching in colour_classes:
        endpoints = [
            vertex
            for current in matching
            for vertex in current
        ]
        assert len(endpoints) == len(set(endpoints))

    selected_edges = frozenset().union(*colour_classes)
    assert len(selected_edges) == 32
    assert selected_edges == (
        frozenset(combinations(CORE_VERTICES, 2))
        | (
            frozenset(combinations(OUTSIDE_VERTICES, 2))
            - removed_star
        )
    )
    assert sum(map(len, colour_classes)) == len(selected_edges)

    selected_supports = [
        frozenset(vertex for current in matching for vertex in current)
        for matching in colour_classes
    ]
    assert Counter(map(len, selected_supports)) == {
        8: 4,
        10: 2,
        12: 1,
    }

    triple_residues = (
        (1, 2, 3),
        (1, 4, 5),
        (2, 4, 6),
        (3, 5, 6),
        (1, 2, 6),
        (3, 4, 5),
    )
    triple_complements = [
        frozenset(6 + residue for residue in triple)
        for triple in triple_residues
    ]
    assert Counter(
        vertex
        for complement in triple_complements
        for vertex in complement
    ) == Counter({vertex: 3 for vertex in range(7, 13)})

    five_complements = [
        CORE_VERTICES - {0},
        CORE_VERTICES - {1},
        (CORE_VERTICES - {2, 3}) | {11},
        (CORE_VERTICES - {4, 5}) | {12},
    ]
    assert all(len(complement) == 5 for complement in five_complements)

    remaining_complements = [
        *triple_complements,
        *five_complements,
    ]
    remaining_supports = [
        frozenset(VERTICES) - complement
        for complement in remaining_complements
    ]
    assert Counter(map(len, remaining_supports)) == {8: 4, 10: 6}

    all_supports = [*selected_supports, *remaining_supports]
    assert len(all_supports) == 17
    assert Counter(map(len, all_supports)) == {8: 8, 10: 8, 12: 1}
    assert {
        vertex: sum(vertex in support for support in all_supports)
        for vertex in VERTICES
    } == {vertex: 12 for vertex in VERTICES}

    degrees = {
        vertex: sum(vertex in current for current in selected_edges)
        for vertex in VERTICES
    }
    assert degrees == {
        **{vertex: 5 for vertex in CORE_VERTICES},
        6: 2,
        7: 5,
        8: 5,
        9: 5,
        10: 5,
        11: 6,
        12: 6,
    }
    assert {
        vertex: sum(
            vertex in complement
            for complement in remaining_complements
        )
        for vertex in VERTICES
    } == {
        vertex: degrees[vertex] - 2
        for vertex in VERTICES
    }

    allowed = frozenset(EDGES) - selected_edges
    assert (
        frozenset(combinations(OUTSIDE_VERTICES, 2)) & allowed
        == removed_star
    )
    blocked = [
        support
        for support in remaining_supports
        if not has_perfect_matching(support, allowed)
    ]
    assert blocked == remaining_supports

    completion = [
        frozenset(edge(left, right) for left, right in matching)
        for matching in FULL_COMPLETION
    ]
    assert len(completion) == len(all_supports) == 17
    for matching, support in zip(completion, all_supports):
        endpoints = [
            vertex
            for current in matching
            for vertex in current
        ]
        assert len(endpoints) == len(set(endpoints))
        assert frozenset(endpoints) == support
    completion_union = frozenset().union(*completion)
    assert sum(map(len, completion)) == len(completion_union) == 78
    assert completion_union == frozenset(EDGES)

    print("PASS reconstructed seven disjoint matchings of type 8^4 10^2 12")
    print("PASS all seventeen supports have profile (8,8,1) and row sum 12")
    print("PASS exact remaining-complement identity d_F(v)-2")
    print("PASS exhaustive matching recursion blocks all ten remaining supports")
    print("PASS separate full completion partitions all 78 edges of K13")
    print("SCOPE: dead class-B seven-prefix; not global noncompletion")


if __name__ == "__main__":
    main()
