#!/usr/bin/env python3
"""Dependency-free semantic verifier for an r=4 dead seven-prefix."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations


VERTICES = frozenset(range(13))
ALL_EDGES = frozenset(combinations(sorted(VERTICES), 2))
PREFIX = (
    ((0, 5), (2, 6), (3, 4), (7, 10)),
    ((0, 4), (1, 3), (2, 5), (7, 9)),
    ((1, 2), (3, 5), (4, 6), (10, 12)),
    ((0, 2), (1, 4), (3, 6), (8, 12)),
    ((0, 6), (1, 5), (2, 3), (7, 12), (8, 9)),
    ((0, 1), (2, 4), (3, 11), (5, 6), (7, 8), (9, 10)),
    ((0, 3), (1, 6), (2, 11), (4, 5), (8, 10), (9, 12)),
)
COMPLEMENTS = (
    (0, 1, 2, 3, 5),
    (1, 2, 3, 4, 5),
    (0, 1, 2, 4, 6),
    (0, 2, 3, 4, 6),
    (1, 2, 3, 5, 6),
    (0, 3, 4, 5, 6),
    (7, 8, 9, 10, 12),
    (8, 9, 10),
    (7,),
    (12,),
)
FULL_COMPLETION = (
    ((0, 6), (2, 5), (3, 7), (4, 10)),
    ((0, 4), (1, 7), (2, 3), (5, 9)),
    ((1, 2), (3, 4), (5, 10), (6, 12)),
    ((0, 2), (1, 6), (3, 8), (4, 12)),
    ((0, 8), (1, 9), (2, 12), (3, 5), (6, 7)),
    ((0, 3), (1, 5), (2, 4), (6, 10), (7, 9), (8, 11)),
    ((0, 10), (1, 8), (2, 6), (3, 9), (4, 11), (5, 12)),
    ((4, 9), (6, 11), (7, 8), (10, 12)),
    ((0, 7), (6, 9), (8, 10), (11, 12)),
    ((3, 11), (5, 8), (7, 10), (9, 12)),
    ((1, 10), (5, 7), (8, 12), (9, 11)),
    ((0, 12), (4, 7), (8, 9), (10, 11)),
    ((1, 11), (2, 8), (7, 12), (9, 10)),
    ((0, 5), (1, 3), (2, 11), (4, 6)),
    ((0, 11), (1, 4), (2, 7), (3, 12), (5, 6)),
    ((0, 9), (1, 12), (2, 10), (3, 6), (4, 8), (5, 11)),
    ((0, 1), (2, 9), (3, 10), (4, 5), (6, 8), (7, 11)),
)


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def endpoints(
    matching: frozenset[tuple[int, int]],
) -> frozenset[int]:
    return frozenset(vertex for current in matching for vertex in current)


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


def build_certificate() -> tuple[
    tuple[frozenset[tuple[int, int]], ...],
    tuple[frozenset[int], ...],
]:
    prefix = tuple(
        frozenset(edge(*current) for current in matching)
        for matching in PREFIX
    )
    complements = tuple(frozenset(current) for current in COMPLEMENTS)
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
    assert tuple(map(len, complements)) == (5,) * 7 + (3,) + (1,) * 2
    remaining_supports = tuple(VERTICES - current for current in complements)
    all_supports = (*selected_supports, *remaining_supports)
    assert Counter(map(len, all_supports)) == {8: 11, 10: 2, 12: 4}
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
    print("PASS seventeen supports have r=4 profile (11,2,4) and row sum 12")
    print("PASS exact remaining-complement identity d_F(v)-2")
    print("PASS exhaustive matching recursion blocks all ten remaining supports")
    print("PASS same support instance has a literal full 17-matching completion")
    print("SCOPE: dead arbitrary r=4 prefix; not global noncompletion")


if __name__ == "__main__":
    main()
