#!/usr/bin/env python3
"""Verify the full-row r=0 three-family Helly counterexample."""

from __future__ import annotations

from collections import Counter
from itertools import combinations


VERTICES = frozenset(range(13))
PREFIX = (
    ((0, 1), (2, 11), (4, 6), (5, 12)),
    ((0, 2), (3, 6), (4, 10), (7, 9)),
    ((0, 12), (3, 7), (6, 10), (8, 9)),
    ((0, 3), (1, 2), (4, 9), (7, 10), (8, 12)),
    ((1, 5), (2, 8), (3, 10), (6, 9), (7, 12)),
    ((1, 12), (3, 4), (5, 8), (6, 7), (9, 10)),
)
REMAINING_TRIPLES = (
    frozenset((0, 1, 2)),
    frozenset((0, 1, 2)),
    frozenset((0, 1, 2)),
    frozenset((3, 7, 9)),
    frozenset((7, 9, 12)),
    frozenset((6, 7, 12)),
    frozenset((4, 6, 8)),
)
REMAINING_FIVE_SETS = (
    frozenset((6, 7, 8, 10, 12)),
    frozenset((3, 5, 6, 9, 10)),
    frozenset((3, 4, 5, 8, 10)),
    frozenset((3, 4, 9, 10, 12)),
)
PAIR_WITNESSES = (
    frozenset(((3, 5), (4, 7), (6, 8), (9, 11), (10, 12))),
    frozenset(((3, 9), (4, 5), (6, 12), (7, 8), (10, 11))),
)
GLOBAL_WITNESS_COLOURS = (0, 1, 3)
GLOBAL_WITNESS = (
    PAIR_WITNESSES[0],
    PAIR_WITNESSES[1],
    frozenset(((0, 4), (1, 6), (2, 5), (8, 10), (11, 12))),
)
PARITY_EDGE = (3, 9)


def perfect_matchings(
    vertices: tuple[int, ...],
    available_edges: frozenset[tuple[int, int]],
) -> tuple[frozenset[tuple[int, int]], ...]:
    if not vertices:
        return (frozenset(),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        edge = tuple(sorted((first, second)))
        if edge not in available_edges:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest, available_edges):
            result.append(frozenset((edge, *tail)))
    return tuple(result)


def is_perfect_matching(
    matching: frozenset[tuple[int, int]],
    support: frozenset[int],
    deleted: frozenset[tuple[int, int]],
) -> bool:
    endpoints = [vertex for edge in matching for vertex in edge]
    return (
        len(matching) == len(support) // 2
        and len(endpoints) == len(set(endpoints))
        and frozenset(endpoints) == support
        and matching.isdisjoint(deleted)
    )


def first_disjoint_triple(
    families: tuple[tuple[frozenset[tuple[int, int]], ...], ...],
    colours: tuple[int, int, int],
) -> tuple[frozenset[tuple[int, int]], ...] | None:
    left_family, middle_family, right_family = (
        families[colour] for colour in colours
    )
    for left in left_family:
        for middle in middle_family:
            if left & middle:
                continue
            union = left | middle
            for right in right_family:
                if union.isdisjoint(right):
                    return left, middle, right
    return None


def main() -> None:
    prefix_edges = tuple(frozenset(layer) for layer in PREFIX)
    assert tuple(map(len, prefix_edges)) == (4, 4, 4, 5, 5, 5)
    assert all(
        len({vertex for edge in layer for vertex in edge}) == 2 * len(layer)
        for layer in prefix_edges
    )
    assert all(
        left.isdisjoint(right)
        for left, right in combinations(prefix_edges, 2)
    )
    deleted = frozenset().union(*prefix_edges)
    assert len(deleted) == 27
    degrees = tuple(
        sum(vertex in edge for edge in deleted) for vertex in sorted(VERTICES)
    )
    assert degrees == (4, 4, 4, 5, 4, 3, 5, 5, 4, 5, 5, 1, 5)
    assert min(degrees) == 1 and max(degrees) == 5

    selected_complements = tuple(
        VERTICES - frozenset(vertex for edge in layer for vertex in edge)
        for layer in prefix_edges
    )
    all_complements = (
        *selected_complements,
        *REMAINING_TRIPLES,
        *REMAINING_FIVE_SETS,
    )
    assert Counter(map(len, all_complements)) == Counter({3: 10, 5: 7})
    assert all(
        sum(vertex in complement for complement in all_complements) == 5
        for vertex in VERTICES
    )
    remaining_complements = REMAINING_TRIPLES + REMAINING_FIVE_SETS
    assert tuple(
        sum(vertex in complement for complement in remaining_complements)
        for vertex in sorted(VERTICES)
    ) == tuple(degree - 1 for degree in degrees)

    all_edges = frozenset(combinations(sorted(VERTICES), 2))
    available_edges = all_edges - deleted
    supports = tuple(VERTICES - triple for triple in REMAINING_TRIPLES)
    families = tuple(
        perfect_matchings(tuple(sorted(support)), available_edges)
        for support in supports
    )
    assert tuple(map(len, families)) == (42, 42, 42, 138, 162, 162, 129)

    repeated_family = families[0]
    assert all(witness in repeated_family for witness in PAIR_WITNESSES)
    assert PAIR_WITNESSES[0].isdisjoint(PAIR_WITNESSES[1])

    # Exact compact no-triple certificate.  There are 190 disjoint pairs
    # among the 42 perfect matchings, and every such pair contains the edge
    # (3,9) in exactly one member.  Three pairwise disjoint matchings are
    # therefore impossible: at most one can use (3,9), leaving a disjoint
    # pair in which neither uses it.
    disjoint_pairs = tuple(
        (left, right)
        for left, right in combinations(repeated_family, 2)
        if left.isdisjoint(right)
    )
    assert len(disjoint_pairs) == 190
    assert all(
        (PARITY_EDGE in left) ^ (PARITY_EDGE in right)
        for left, right in disjoint_pairs
    )
    assert first_disjoint_triple(families, (0, 1, 2)) is None

    packable_colour_triples = {
        colours
        for colours in combinations(range(7), 3)
        if first_disjoint_triple(families, colours) is not None
    }
    assert len(packable_colour_triples) == 34
    assert set(combinations(range(7), 3)) - packable_colour_triples == {
        (0, 1, 2)
    }
    assert all(
        is_perfect_matching(matching, supports[colour], deleted)
        for colour, matching in zip(GLOBAL_WITNESS_COLOURS, GLOBAL_WITNESS)
    )
    assert all(
        left.isdisjoint(right)
        for left, right in combinations(GLOBAL_WITNESS, 2)
    )

    print("PASS six-prefix: matching sizes 4,4,4,5,5,5 and degrees 1..5")
    print("PASS exact r=0 class-B inventory and rho(v)=d_D(v)-1")
    print("PASS repeated support: 42 perfect matchings and explicit disjoint pair")
    print("PASS no-triple certificate: 190 disjoint pairs, (3,9)-parity bipartition")
    print("PASS complete seven-family audit: 34 of 35 triples pack")
    print("PASS explicit global witness on colours (0,1,3)")


if __name__ == "__main__":
    main()
