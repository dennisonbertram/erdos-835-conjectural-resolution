#!/usr/bin/env python3
"""Verify the r=0 all-35 size-ten obstruction and its mixed escape."""

from __future__ import annotations

from collections import Counter
from itertools import combinations


VERTICES = frozenset(range(13))
U = frozenset(range(3, 9))
W = VERTICES - U
PREFIX = (
    ((0, 12), (1, 2), (3, 5), (9, 10)),
    ((0, 10), (1, 11), (4, 6), (7, 8)),
    ((0, 2), (1, 12), (3, 8), (6, 7)),
    ((2, 10), (3, 6), (4, 7), (5, 8), (11, 12)),
    ((0, 11), (1, 10), (4, 8), (5, 7), (9, 12)),
    ((0, 1), (2, 11), (3, 7), (4, 5), (6, 8)),
)
REPAIRED_PREFIX = (
    PREFIX[0],
    ((0, 7), (1, 11), (4, 6), (8, 10)),
    *PREFIX[2:],
)
REMAINING_TRIPLES = (
    frozenset((0, 1, 2)),
    frozenset((1, 10, 11)),
    frozenset((1, 10, 11)),
    frozenset((1, 9, 10)),
    frozenset((0, 11, 12)),
    frozenset((0, 2, 12)),
    frozenset((0, 2, 12)),
)
REMAINING_FIVE_SETS = (
    U - frozenset((3,)),
    U - frozenset((4,)),
    U - frozenset((5,)),
    U - frozenset((6,)),
)
MIXED_WITNESS_COLOURS = (0, 1, 7)
MIXED_WITNESS = (
    frozenset(((3, 4), (5, 9), (6, 10), (7, 11), (8, 12))),
    frozenset(((0, 3), (2, 4), (5, 6), (7, 12), (8, 9))),
    frozenset(((0, 9), (1, 3), (2, 12), (10, 11))),
)
REPAIRED_TEN_WITNESS_COLOURS = (0, 1, 2)
REPAIRED_TEN_WITNESS = (
    frozenset(((3, 4), (5, 9), (6, 10), (7, 11), (8, 12))),
    frozenset(((0, 3), (2, 4), (5, 6), (7, 12), (8, 9))),
    frozenset(((0, 4), (2, 3), (5, 12), (6, 9), (7, 8))),
)


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
    assert degrees == (5, 5, 4, 4, 4, 4, 4, 5, 5, 2, 4, 4, 4)
    assert min(degrees) == 2 and max(degrees) == 5

    internal_u = frozenset(combinations(sorted(U), 2)) & deleted
    internal_w = frozenset(combinations(sorted(W), 2)) & deleted
    cross = frozenset(
        edge
        for edge in deleted
        if len(frozenset(edge) & U) == 1
    )
    assert len(internal_u) == 13
    assert frozenset(combinations(sorted(U), 2)) - internal_u == {
        (3, 4),
        (5, 6),
    }
    assert len(internal_w) == 14
    assert not cross

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
    supports = tuple(
        VERTICES - complement for complement in remaining_complements
    )
    families = tuple(
        perfect_matchings(tuple(sorted(support)), available_edges)
        for support in supports
    )
    assert tuple(map(len, families)) == (
        54,
        54,
        54,
        50,
        52,
        54,
        54,
        2,
        2,
        2,
        2,
    )

    # Every pair of size-ten occurrences coordinates, despite the global
    # failure of every three-size-ten choice.
    assert all(
        any(left.isdisjoint(right) for left in families[i] for right in families[j])
        for i, j in combinations(range(7), 2)
    )
    assert all(
        first_disjoint_triple(families, colours) is None
        for colours in combinations(range(7), 3)
    )

    # Independently verify the structural pigeonhole premise: every
    # size-ten perfect matching uses at least one of the only two residual
    # U-edges.
    residual_u_edges = frozenset(((3, 4), (5, 6)))
    assert all(
        matching & residual_u_edges
        for family in families[:7]
        for matching in family
    )

    packable = {
        colours
        for colours in combinations(range(11), 3)
        if first_disjoint_triple(families, colours) is not None
    }
    expected_mixed = {
        (*ten_colours, eight_colour)
        for ten_colours in combinations(range(7), 2)
        for eight_colour in range(7, 11)
    }
    assert packable == expected_mixed
    assert len(packable) == 84

    assert all(
        is_perfect_matching(matching, supports[colour], deleted)
        for colour, matching in zip(MIXED_WITNESS_COLOURS, MIXED_WITNESS)
    )
    assert all(
        left.isdisjoint(right)
        for left, right in combinations(MIXED_WITNESS, 2)
    )

    repaired_prefix_edges = tuple(frozenset(layer) for layer in REPAIRED_PREFIX)
    assert repaired_prefix_edges[1] == (
        prefix_edges[1] - {(0, 10), (7, 8)}
    ) | {(0, 7), (8, 10)}
    assert tuple(map(len, repaired_prefix_edges)) == (4, 4, 4, 5, 5, 5)
    assert all(
        len({vertex for edge in layer for vertex in edge}) == 2 * len(layer)
        for layer in repaired_prefix_edges
    )
    assert all(
        left.isdisjoint(right)
        for left, right in combinations(repaired_prefix_edges, 2)
    )
    repaired_deleted = frozenset().union(*repaired_prefix_edges)
    assert frozenset(combinations(sorted(U), 2)) - repaired_deleted == {
        (3, 4),
        (5, 6),
        (7, 8),
    }
    assert {
        edge
        for edge in repaired_deleted
        if len(frozenset(edge) & U) == 1
    } == {(0, 7), (8, 10)}

    repaired_available_edges = all_edges - repaired_deleted
    repaired_families = tuple(
        perfect_matchings(tuple(sorted(support)), repaired_available_edges)
        for support in supports
    )
    assert tuple(map(len, repaired_families)) == (
        78,
        77,
        77,
        65,
        70,
        77,
        77,
        4,
        4,
        4,
        4,
    )
    repaired_packable = {
        colours
        for colours in combinations(range(11), 3)
        if first_disjoint_triple(repaired_families, colours) is not None
    }
    expected_repaired = expected_mixed | set(combinations(range(7), 3))
    assert repaired_packable == expected_repaired
    assert len(repaired_packable) == 119
    assert all(
        is_perfect_matching(matching, supports[colour], repaired_deleted)
        for colour, matching in zip(
            REPAIRED_TEN_WITNESS_COLOURS,
            REPAIRED_TEN_WITNESS,
        )
    )
    assert all(
        left.isdisjoint(right)
        for left, right in combinations(REPAIRED_TEN_WITNESS, 2)
    )

    print("PASS six-prefix and disconnected K6-2K2 plus 14-edge structure")
    print("PASS exact r=0 class-B inventory and rho(v)=d_D(v)-1")
    print("PASS all seven size-ten families live and every pair coordinates")
    print("PASS all 35 three-size-ten choices fail by the two-edge bottleneck")
    print("PASS mixed escape: exactly all 84 choices of two tens plus one eight pack")
    print("PASS explicit mixed coordinated-nine witness on colours (0,1,7)")
    print("PASS support-preserving two-edge switch repairs all 35 size-ten routes")
    print("PASS complete repaired audit: exactly 119 of 165 remaining triples pack")


if __name__ == "__main__":
    main()
