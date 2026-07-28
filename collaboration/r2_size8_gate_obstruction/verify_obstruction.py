#!/usr/bin/env python3
"""Verify the exact r=2 obstruction to the size-eight terminal route."""

from __future__ import annotations

from itertools import combinations

V = frozenset(range(13))
ALL_EDGES = frozenset(combinations(range(13), 2))

MATCHINGS = (
    ((0, 4), (1, 5), (2, 3), (8, 11)),
    ((1, 6), (2, 9), (4, 8), (10, 11)),
    ((0, 8), (2, 6), (3, 5), (9, 10)),
    ((1, 9), (3, 6), (4, 10), (11, 12)),
    ((0, 11), (1, 2), (3, 9), (5, 6), (8, 10)),
    ((0, 10), (1, 3), (2, 5), (4, 11), (7, 12)),
)

SELECTED_COMPLEMENTS = (
    frozenset((6, 7, 9, 10, 12)),
    frozenset((0, 3, 5, 7, 12)),
    frozenset((1, 4, 7, 11, 12)),
    frozenset((0, 2, 5, 7, 8)),
    frozenset((4, 7, 12)),
    frozenset((6, 8, 9)),
)

REMAINING_FIVES = (
    frozenset((1, 2, 3, 5, 9)),
    frozenset((1, 2, 3, 6, 12)),
    frozenset((0, 4, 9, 10, 11)),
    frozenset((0, 4, 8, 10, 11)),
    frozenset((2, 3, 5, 6, 9)),
)

REMAINING_TRIPLES = (
    frozenset((1, 8, 11)),
    frozenset((3, 6, 10)),
    frozenset((4, 8, 10)),
    frozenset((1, 2, 11)),
)

REMAINING_SINGLETONS = (
    frozenset((5,)),
    frozenset((0,)),
)

K_CORE = frozenset((0, 4, 8, 10, 11))
L_CORE = frozenset((1, 2, 3, 5, 6))

EXTENSION_MATCHINGS = (
    ((0, 12), (1, 11), (2, 8), (3, 4), (6, 10), (7, 9)),
    ((1, 12), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7)),
    ((0, 9), (2, 10), (3, 12), (4, 6), (5, 7)),
)

EXTENSION_COMPLEMENTS = (
    frozenset((5,)),
    frozenset((0,)),
    frozenset((1, 8, 11)),
)


def perfect_matching_exists(
    vertices: frozenset[int],
    edges: frozenset[tuple[int, int]],
) -> bool:
    if not vertices:
        return True
    first = min(vertices)
    for second in vertices - {first}:
        edge = tuple(sorted((first, second)))
        if edge in edges and perfect_matching_exists(
            vertices - {first, second}, edges
        ):
            return True
    return False


def main() -> None:
    used: set[tuple[int, int]] = set()
    assert len(MATCHINGS) == len(SELECTED_COMPLEMENTS)
    for matching, complement in zip(MATCHINGS, SELECTED_COMPLEMENTS):
        endpoints = [vertex for edge in matching for vertex in edge]
        assert len(endpoints) == len(set(endpoints))
        assert V - set(endpoints) == complement
        for edge in matching:
            edge = tuple(sorted(edge))
            assert edge not in used
            used.add(edge)
    assert len(used) == 26
    degrees = tuple(sum(vertex in edge for edge in used) for vertex in V)
    assert degrees == (4, 5, 5, 5, 4, 4, 4, 1, 4, 4, 5, 5, 2)
    assert max(degrees) == 5
    assert set().union(*SELECTED_COMPLEMENTS) == V
    print("PASS literal complement-cover six-prefix: 8^4 10^2")

    all_complements = (
        SELECTED_COMPLEMENTS
        + REMAINING_FIVES
        + REMAINING_TRIPLES
        + REMAINING_SINGLETONS
    )
    assert sorted(map(len, all_complements)) == [1] * 2 + [3] * 6 + [5] * 9
    assert all(
        sum(vertex in complement for complement in all_complements) == 5
        for vertex in V
    )
    print("PASS exact class-B r=2 inventory and row sums")

    assert all(edge in used for edge in combinations(K_CORE, 2))
    assert all(edge in used for edge in combinations(L_CORE, 2))
    residual = ALL_EDGES - frozenset(used)
    for index, complement in enumerate(REMAINING_FIVES):
        support = V - complement
        core = K_CORE if index in (0, 1, 4) else L_CORE
        assert core <= support
        assert not (frozenset(combinations(core, 2)) & residual)
        assert not perfect_matching_exists(support, residual)
    print("PASS all five remaining size-8 supports have no residual PM")

    extension_used: set[tuple[int, int]] = set()
    assert len(EXTENSION_MATCHINGS) == len(EXTENSION_COMPLEMENTS)
    for matching, complement in zip(
        EXTENSION_MATCHINGS, EXTENSION_COMPLEMENTS
    ):
        endpoints = [vertex for edge in matching for vertex in edge]
        assert len(endpoints) == len(set(endpoints))
        assert V - set(endpoints) == complement
        for edge in matching:
            edge = tuple(sorted(edge))
            assert edge not in used
            assert edge not in extension_used
            extension_used.add(edge)
    assert tuple(map(len, EXTENSION_MATCHINGS)) == (6, 6, 5)
    assert len(used | extension_used) == 43
    print("PASS explicit instance-specific nine-packing: 8^4 10^3 12^2")
    print("SCOPE: blocks only the universal 8+12+12 terminal route")


if __name__ == "__main__":
    main()
