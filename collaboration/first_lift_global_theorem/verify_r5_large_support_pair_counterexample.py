#!/usr/bin/env python3
"""Verify the r=5 two-large-support abstract class-B counterexample."""

from __future__ import annotations

from collections import Counter
from itertools import combinations


V = frozenset(range(13))
C = frozenset(range(8))
OUTSIDE = V - C


def edge(a: int, b: int) -> tuple[int, int]:
    return tuple(sorted((a, b)))


def clique(vertices: frozenset[int]) -> set[tuple[int, int]]:
    return set(combinations(sorted(vertices), 2))


def endpoints(matching: set[tuple[int, int]]) -> frozenset[int]:
    return frozenset(vertex for pair in matching for vertex in pair)


def is_matching(matching: set[tuple[int, int]]) -> bool:
    return len(endpoints(matching)) == 2 * len(matching)


def perfect_matching(
    vertices: frozenset[int],
    available: set[tuple[int, int]],
) -> tuple[tuple[int, int], ...] | None:
    if not vertices:
        return ()
    first = min(vertices)
    for second in sorted(vertices - {first}):
        pair = edge(first, second)
        if pair not in available:
            continue
        rest = perfect_matching(vertices - {first, second}, available)
        if rest is not None:
            return (pair, *rest)
    return None


def round_robin_factors() -> list[set[tuple[int, int]]]:
    factors = []
    for residue in range(7):
        factor = {edge(residue, 7)}
        for offset in range(1, 4):
            factor.add(
                edge(
                    (residue + offset) % 7,
                    (residue - offset) % 7,
                )
            )
        factors.append(factor)
    return factors


def main() -> None:
    factors = round_robin_factors()
    assert all(len(factor) == 4 and is_matching(factor) for factor in factors)
    assert set().union(*factors) == clique(C)
    assert sum(map(len, factors)) == len(clique(C)) == 28

    additions = [
        {edge(9, 10), edge(11, 12)},
        {edge(8, 11), edge(10, 12)},
        {edge(8, 12), edge(9, 11)},
    ]
    assert all(len(extra) == 2 and is_matching(extra) for extra in additions)
    assert sum(map(len, additions)) == len(set().union(*additions)) == 6

    prefix = [
        factors[3],
        factors[4],
        factors[5],
        factors[6],
        factors[0] | additions[0],
        factors[1] | additions[1],
        factors[2] | additions[2],
    ]
    assert [len(matching) for matching in prefix] == [4, 4, 4, 4, 6, 6, 6]
    assert all(is_matching(matching) for matching in prefix)
    prefix_union = set().union(*prefix)
    assert sum(map(len, prefix)) == len(prefix_union) == 34
    assert prefix_union == clique(C) | set().union(*additions)

    selected_complements = [
        OUTSIDE,
        OUTSIDE,
        OUTSIDE,
        OUTSIDE,
        {8},
        {9},
        {10},
    ]
    selected_supports = [V - complement for complement in selected_complements]
    assert all(
        endpoints(matching) == support
        for matching, support in zip(prefix, selected_supports)
    )

    triples = [
        frozenset({index, (index + 1) % 8, (index + 3) % 8}) for index in range(8)
    ]
    five_sets = [C - triple for triple in triples]
    remaining_complements = [*five_sets, {11}, {12}]
    all_complements = [*selected_complements, *remaining_complements]
    assert Counter(map(len, all_complements)) == {5: 12, 1: 5}
    assert all(
        sum(vertex in complement for complement in all_complements) == 5 for vertex in V
    )
    all_supports = [V - complement for complement in all_complements]
    assert Counter(map(len, all_supports)) == {8: 12, 12: 5}

    degrees = {vertex: sum(vertex in pair for pair in prefix_union) for vertex in V}
    assert [degrees[vertex] for vertex in sorted(C)] == [7] * 8
    assert [degrees[vertex] for vertex in sorted(OUTSIDE)] == [2, 2, 2, 3, 3]
    assert min(degrees.values()) == 2
    assert max(degrees.values()) == 7
    assert all(
        sum(vertex in complement for complement in remaining_complements)
        == degrees[vertex] - 2
        for vertex in V
    )

    e0 = clique(C) - clique(frozenset({0, 1, 2}))
    e1 = clique(C) - clique(frozenset({0, 1, 3}))
    g0 = clique(C - {0})
    g1 = clique(C - {1})
    assert len(e0) == len(e1) == 25
    assert len(g0) == len(g1) == 21
    assert e0 != e1 and g0 != g1
    assert all(core <= prefix_union for core in (e0, e1, g0, g1))

    large_supports = [V - {11}, V - {12}]
    core_pairs = {
        "EE": (e0, e1),
        "EG": (e0, g0),
        "GG": (g0, g1),
    }
    for pair in core_pairs.values():
        for core, support in zip(pair, large_supports):
            assert endpoints(core) <= support

    residual = clique(V) - prefix_union
    assert not (residual & clique(C))
    assert all(
        perfect_matching(support, residual) is None for support in large_supports
    )

    small_supports = [V - complement for complement in five_sets]
    small_witnesses = [
        perfect_matching(support, residual) for support in small_supports
    ]
    assert all(witness is not None for witness in small_witnesses)
    assert residual & clique(OUTSIDE) == {
        edge(8, 9),
        edge(8, 10),
        edge(9, 12),
        edge(10, 11),
    }

    print("PASS seven prefix matchings have type 8^4 12^3 and 34 edges")
    print("PASS seventeen complements form a class-B profile (12,0,5)")
    print("PASS remaining complement rows equal d_F(v)-2 exactly")
    print("PASS distinct EE, EG, and GG core pairs coexist in both large supports")
    print("PASS both size-12 residual graphs have no perfect matching")
    print("PASS all eight remaining size-8 residual graphs have perfect matchings")
    print("SCOPE: large-support-only propagation fails; eighth extension survives")


if __name__ == "__main__":
    main()
