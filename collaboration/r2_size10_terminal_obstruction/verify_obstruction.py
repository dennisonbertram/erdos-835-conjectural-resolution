#!/usr/bin/env python3
"""Verify the class-B r=2 arbitrary-size10-matching obstruction."""

from __future__ import annotations

from itertools import combinations

V = frozenset(range(13))
ALL_EDGES = frozenset(combinations(range(13), 2))

PREFIX = (
    ((7, 10), (0, 3), (1, 4), (2, 6)),
    ((3, 4), (0, 5), (1, 6), (8, 10)),
    ((1, 2), (3, 5), (11, 12), (7, 8)),
    ((0, 4), (7, 9), (2, 5), (3, 6)),
    ((2, 4), (1, 5), (8, 12), (0, 6), (7, 11)),
    ((4, 6), (5, 7), (0, 2), (1, 3), (8, 11)),
)

SELECTED_COMPLEMENTS = (
    frozenset((5, 8, 9, 11, 12)),
    frozenset((2, 7, 9, 11, 12)),
    frozenset((0, 4, 6, 9, 10)),
    frozenset((1, 8, 10, 11, 12)),
    frozenset((3, 9, 10)),
    frozenset((9, 10, 12)),
)

FIVES = (
    frozenset((4, 5, 6, 7, 8)),
    frozenset((3, 5, 6, 7, 8)),
    frozenset((3, 4, 5, 6, 7)),
    frozenset((2, 3, 4, 5, 6)),
    frozenset((0, 1, 2, 3, 4)),
)

TRIPLES = (
    frozenset((10, 11, 12)),
    frozenset((0, 1, 11)),
    frozenset((0, 1, 2)),
    frozenset((0, 1, 2)),
)

SINGLETONS = (
    frozenset((7,)),
    frozenset((8,)),
)

CANDIDATE = frozenset(
    {(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)}
)


def perfect_matchings(
    vertices: frozenset[int],
    edges: frozenset[tuple[int, int]],
) -> list[frozenset[tuple[int, int]]]:
    if not vertices:
        return [frozenset()]
    first = min(vertices)
    result: list[frozenset[tuple[int, int]]] = []
    for second in sorted(vertices - {first}):
        edge = (first, second)
        if edge not in edges:
            continue
        for tail in perfect_matchings(vertices - {first, second}, edges):
            result.append(tail | {edge})
    return result


def main() -> None:
    used: set[tuple[int, int]] = set()
    assert len(PREFIX) == len(SELECTED_COMPLEMENTS)
    for matching, complement in zip(PREFIX, SELECTED_COMPLEMENTS):
        endpoints = [vertex for edge in matching for vertex in edge]
        assert len(endpoints) == len(set(endpoints))
        assert V - set(endpoints) == complement
        for edge in matching:
            edge = tuple(sorted(edge))
            assert edge not in used
            used.add(edge)
    assert len(used) == 26
    degrees = tuple(sum(vertex in edge for edge in used) for vertex in V)
    assert degrees == (5, 5, 5, 5, 5, 5, 5, 5, 4, 1, 2, 3, 2)
    assert max(degrees) == 5
    assert set().union(*SELECTED_COMPLEMENTS) == V
    print("PASS literal complement-cover six-prefix: 8^4 10^2")

    all_complements = SELECTED_COMPLEMENTS + FIVES + TRIPLES + SINGLETONS
    assert sorted(map(len, all_complements)) == [1] * 2 + [3] * 6 + [5] * 9
    assert all(
        sum(vertex in complement for complement in all_complements) == 5
        for vertex in V
    )
    print("PASS exact class-B r=2 inventory and row sums")

    assert not (CANDIDATE & used)
    candidate_endpoints = [
        vertex for edge in CANDIDATE for vertex in edge
    ]
    assert V - set(candidate_endpoints) == TRIPLES[0]
    residual = ALL_EDGES - frozenset(used) - CANDIDATE
    u_set = frozenset(range(7))
    assert residual & frozenset(combinations(u_set, 2)) == {(5, 6)}

    missing7 = perfect_matchings(V - {7}, residual)
    missing8 = perfect_matchings(V - {8}, residual)
    assert missing7 and missing8
    assert all((5, 6) in matching for matching in missing7)
    assert all((5, 6) in matching for matching in missing8)
    assert not any(
        left.isdisjoint(right) for left in missing7 for right in missing8
    )
    print(
        "PASS all near-factor pairs intersect: "
        f"{len(missing7)} x {len(missing8)} checked"
    )
    print("SCOPE: arbitrary candidate PM fails; coordinated nine remains open")


if __name__ == "__main__":
    main()
