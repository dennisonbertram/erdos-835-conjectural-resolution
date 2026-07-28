#!/usr/bin/env python3
"""Verify the exact r=2 obstruction to a fixed six-prefix route.

Python standard library only.
"""

from __future__ import annotations

from itertools import combinations

V = frozenset(range(13))
A = frozenset(range(7))
C = frozenset(range(2, 7))
B = frozenset(range(7, 13))

MATCHINGS = (
    ((7, 11), (9, 12), (2, 6), (4, 5)),
    ((8, 9), (10, 12), (3, 5), (4, 6)),
    ((7, 8), (10, 11), (2, 4), (5, 6)),
    ((7, 9), (8, 10), (11, 12), (3, 4)),
    ((7, 10), (8, 12), (9, 11), (2, 3), (0, 1)),
    ((7, 12), (8, 11), (9, 10), (2, 5), (3, 6)),
)

SELECTED_COMPLEMENTS = (
    frozenset((0, 1, 3, 8, 10)),
    frozenset((0, 1, 2, 7, 11)),
    frozenset((0, 1, 3, 9, 12)),
    frozenset((0, 1, 2, 5, 6)),
    frozenset((4, 5, 6)),
    frozenset((0, 1, 4)),
)

REMAINING_FIVES = (
    frozenset((8, 9, 10, 11, 12)),
    frozenset((7, 9, 10, 11, 12)),
    frozenset((7, 8, 10, 11, 12)),
    frozenset((7, 8, 9, 11, 12)),
    frozenset((6, 7, 8, 9, 10)),
)

REMAINING_TRIPLES = (
    frozenset((3, 5, 6)),
    frozenset((2, 4, 6)),
    frozenset((2, 3, 5)),
    frozenset((2, 3, 4)),
)

REMAINING_SINGLETONS = (
    frozenset((4,)),
    frozenset((5,)),
)

EXTENSION_MATCHINGS = (
    ((0, 5), (1, 4), (2, 11), (3, 12)),
    ((0, 12), (1, 10), (2, 9), (3, 7), (5, 8), (6, 11)),
    ((0, 8), (1, 11), (2, 7), (3, 9), (4, 10), (6, 12)),
)

EXTENSION_COMPLEMENTS = (
    frozenset((6, 7, 8, 9, 10)),
    frozenset((4,)),
    frozenset((5,)),
)


def normalized(edge: tuple[int, int]) -> tuple[int, int]:
    return tuple(sorted(edge))


def has_perfect_matching(
    vertices: frozenset[int],
    edges: frozenset[tuple[int, int]],
) -> bool:
    """Tiny exact recursion, used only as an independent certificate check."""
    if not vertices:
        return True
    u = min(vertices)
    for v in vertices - {u}:
        if normalized((u, v)) in edges and has_perfect_matching(
            vertices - {u, v}, edges
        ):
            return True
    return False


def main() -> None:
    used: set[tuple[int, int]] = set()
    assert len(MATCHINGS) == len(SELECTED_COMPLEMENTS)
    for matching, complement in zip(MATCHINGS, SELECTED_COMPLEMENTS):
        flat = [vertex for edge in matching for vertex in edge]
        assert len(flat) == len(set(flat))
        assert V - set(flat) == complement
        for edge in matching:
            edge = normalized(edge)
            assert edge not in used
            used.add(edge)

    expected_d = (
        set(combinations(B, 2))
        | set(combinations(C, 2))
        | {(0, 1)}
    )
    assert used == expected_d
    assert len(used) == 26
    degrees = tuple(sum(vertex in edge for edge in used) for vertex in V)
    assert degrees == (1, 1, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5)
    assert max(degrees) == 5
    assert set().union(*SELECTED_COMPLEMENTS) == V
    print("PASS six-prefix: types 8^4 10^2, complements cover V, |D|=26")
    print("PASS exact union: D=K6[B] disjoint-union K5[C] disjoint-union K2")

    all_complements = (
        SELECTED_COMPLEMENTS
        + REMAINING_FIVES
        + REMAINING_TRIPLES
        + REMAINING_SINGLETONS
    )
    sizes = sorted(map(len, all_complements))
    assert sizes == [1] * 2 + [3] * 6 + [5] * 9
    row_sums = tuple(
        sum(vertex in complement for complement in all_complements)
        for vertex in V
    )
    assert row_sums == (5,) * 13
    remaining = (
        REMAINING_FIVES + REMAINING_TRIPLES + REMAINING_SINGLETONS
    )
    remaining_rows = tuple(
        sum(vertex in complement for complement in remaining)
        for vertex in V
    )
    assert remaining_rows == tuple(degree - 1 for degree in degrees)
    print("PASS class-B r=2 inventory: 5^9 3^6 1^2 and every row sum is 5")
    print("PASS residual identity: rho(v)=d_D(v)-1")

    complete = frozenset(combinations(range(13), 2))
    residual = complete - frozenset(used)
    assert not (set(combinations(B, 2)) & residual)
    for triple in REMAINING_TRIPLES:
        assert triple <= C
        support = V - triple
        assert len(support & A) == 4
        assert len(support & B) == 6
        assert not has_perfect_matching(support, residual)
    print("PASS all four remaining size-10 residual supports have no PM")
    print("SCOPE: blocks this six-prefix route; not coordinated nine globally")

    extension_edges: set[tuple[int, int]] = set()
    assert len(EXTENSION_MATCHINGS) == len(EXTENSION_COMPLEMENTS)
    for matching, complement in zip(
        EXTENSION_MATCHINGS, EXTENSION_COMPLEMENTS
    ):
        flat = [vertex for edge in matching for vertex in edge]
        assert len(flat) == len(set(flat))
        assert V - set(flat) == complement
        for edge in matching:
            edge = normalized(edge)
            assert edge not in used
            assert edge not in extension_edges
            extension_edges.add(edge)
    assert tuple(map(len, EXTENSION_MATCHINGS)) == (4, 6, 6)
    assert len(used | extension_edges) == 42
    print("PASS explicit nine-packing: support-size pattern 8^5 10^2 12^2")
    print("SCOPE: instance-specific repair; not a universal r=2 theorem")


if __name__ == "__main__":
    main()
