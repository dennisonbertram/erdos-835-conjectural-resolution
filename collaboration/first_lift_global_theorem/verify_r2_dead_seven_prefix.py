#!/usr/bin/env python3
"""Dependency-free semantic verifier for an r=2 dead seven-prefix."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations


VERTICES = frozenset(range(13))
CORE = frozenset(range(6))
OUTSIDE = VERTICES - CORE
ALL_EDGES = frozenset(combinations(sorted(VERTICES), 2))
FULL_COMPLETION = (
    ((2, 12), (3, 5), (4, 11), (9, 10)),
    ((0, 12), (2, 4), (5, 11), (7, 9)),
    ((1, 11), (2, 5), (4, 8), (9, 12)),
    ((0, 7), (1, 8), (3, 10), (5, 12)),
    ((0, 6), (1, 9), (2, 10), (3, 8), (7, 11)),
    ((0, 2), (1, 10), (3, 11), (4, 12), (5, 7), (8, 9)),
    ((0, 9), (1, 3), (2, 6), (4, 10), (7, 12), (8, 11)),
    ((1, 7), (6, 9), (8, 10), (11, 12)),
    ((0, 8), (6, 12), (7, 10), (9, 11)),
    ((2, 9), (3, 7), (6, 10), (8, 12)),
    ((0, 5), (1, 4), (3, 12), (6, 8)),
    ((4, 9), (5, 10), (6, 11), (7, 8)),
    ((0, 11), (1, 5), (2, 3), (4, 6), (10, 12)),
    ((0, 3), (1, 12), (2, 8), (4, 5), (6, 7)),
    ((0, 4), (1, 2), (3, 6), (5, 9), (10, 11)),
    ((0, 1), (2, 11), (3, 9), (4, 7), (5, 6)),
    ((0, 10), (1, 6), (2, 7), (3, 4), (5, 8)),
)


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def round_robin_colour(left: int, right: int) -> int:
    return 4 * (left + right) % 7


@lru_cache(maxsize=None)
def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            result.append((edge(first, second), *tail))
    return tuple(result)


def residual_matching(
    support: frozenset[int],
    forbidden: frozenset[tuple[int, int]],
) -> tuple[tuple[int, int], ...] | None:
    for current in perfect_matchings(tuple(sorted(support))):
        if forbidden.isdisjoint(current):
            return current
    return None


def endpoints(
    matching: frozenset[tuple[int, int]],
) -> frozenset[int]:
    return frozenset(vertex for current in matching for vertex in current)


def build_certificate() -> tuple[
    tuple[frozenset[tuple[int, int]], ...],
    tuple[frozenset[int], ...],
]:
    """Construct the literal r=2 witness from two round-robin colourings."""
    colours = [set() for _ in range(7)]
    core_residue = {vertex: vertex + 1 for vertex in CORE}
    for left, right in combinations(sorted(CORE), 2):
        colour = round_robin_colour(
            core_residue[left],
            core_residue[right],
        )
        colours[colour].add(edge(left, right))

    removed_star = frozenset(
        edge(6, 6 + leaf) for leaf in (1, 2, 3, 4)
    )
    for left, right in combinations(sorted(OUTSIDE), 2):
        current = edge(left, right)
        if current in removed_star:
            continue
        colour = round_robin_colour(left - 6, right - 6)
        colours[colour].add(current)

    # Colour 3 originally has size ten and omits 2, 9, and 12.  Adding
    # 2--9 changes it to a size-twelve selected layer.
    assert edge(2, 9) not in frozenset().union(*colours)
    assert {2, 9}.isdisjoint(
        frozenset(vertex for current in colours[3] for vertex in current)
    )
    colours[3].add(edge(2, 9))

    selected_order = (1, 2, 4, 5, 6, 0, 3)
    prefix = tuple(
        frozenset(colours[index]) for index in selected_order
    )

    triples = (
        frozenset({7, 8, 9}),
        frozenset({7, 10, 11}),
        frozenset({8, 10, 12}),
        frozenset({9, 11, 12}),
        frozenset({7, 8, 12}),
        frozenset({9, 10, 11}),
    )
    old_fives = (
        CORE - {0},
        CORE - {1},
        (CORE - {2, 3}) | {11},
        (CORE - {4, 5}) | {12},
    )
    # Replacing the second triple by this five-set adds one remaining
    # complement occurrence at each endpoint of the added prefix edge.
    new_five = triples[1] | {2, 9}
    def binary_code(values: frozenset[int]) -> int:
        return sum(1 << vertex for vertex in values)

    complements = (
        *sorted((new_five, *old_fives), key=binary_code),
        *sorted((triples[0], *triples[2:]), key=binary_code),
    )
    return prefix, complements


def verify_certificate(
    prefix: tuple[frozenset[tuple[int, int]], ...],
    complements: tuple[frozenset[int], ...],
) -> tuple[frozenset[int], ...]:
    assert tuple(map(len, prefix)) == (4, 4, 4, 4, 5, 6, 6)
    assert all(len(endpoints(current)) == 2 * len(current) for current in prefix)
    prefix_union = frozenset().union(*prefix)
    assert sum(map(len, prefix)) == len(prefix_union) == 33

    selected_supports = tuple(endpoints(current) for current in prefix)
    assert Counter(map(len, selected_supports)) == {8: 4, 10: 1, 12: 2}
    assert tuple(map(len, complements)) == (5,) * 5 + (3,) * 5
    remaining_supports = tuple(VERTICES - current for current in complements)
    all_supports = (*selected_supports, *remaining_supports)
    assert Counter(map(len, all_supports)) == {8: 9, 10: 6, 12: 2}
    assert all(
        sum(vertex in support for support in all_supports) == 12
        for vertex in VERTICES
    )

    degrees = {
        vertex: sum(vertex in current for current in prefix_union)
        for vertex in VERTICES
    }
    assert all(
        sum(vertex in complement for complement in complements)
        == degrees[vertex] - 2
        for vertex in VERTICES
    )
    assert all(
        residual_matching(support, prefix_union) is None
        for support in remaining_supports
    )
    return tuple(all_supports)


def verify_full_completion(
    supports: tuple[frozenset[int], ...],
    prefix: tuple[frozenset[tuple[int, int]], ...],
) -> None:
    completion = tuple(
        frozenset(edge(*current) for current in matching)
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
    completion_union = frozenset().union(*completion)
    assert sum(map(len, completion)) == len(completion_union) == 78
    assert completion_union == ALL_EDGES
    assert completion[:7] != prefix


def main() -> None:
    prefix, complements = build_certificate()
    supports = verify_certificate(prefix, complements)
    verify_full_completion(supports, prefix)
    print("PASS seven prefix matchings have type 8^4 10 12^2 and 33 edges")
    print("PASS seventeen supports have r=2 profile (9,6,2) and row sum 12")
    print("PASS exact remaining-complement identity d_F(v)-2")
    print("PASS exhaustive matching recursion blocks all ten remaining supports")
    print("PASS same support instance has a literal full 17-matching completion")
    print("SCOPE: dead arbitrary r=2 prefix; not global noncompletion")


if __name__ == "__main__":
    main()
