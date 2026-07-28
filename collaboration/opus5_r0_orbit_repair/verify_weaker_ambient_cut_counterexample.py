#!/usr/bin/env python3
"""Audit Opus 5's weaker-ambient counterexample to cut sufficiency.

The example deliberately omits the eleven-row class-B inventory.  This
verifier checks the six-layer prefix, all 2^13 capacity cuts, the absence of a
perfect matching on the repeated support, and the incidence-count reason the
repeated row cannot occur in a full class-B instance.
"""

from __future__ import annotations

from itertools import combinations


VERTICES = tuple(range(13))
LEFT = frozenset(range(5))
RIGHT = frozenset(range(5, 10))
ROW = frozenset((10, 11, 12))
SUPPORT = LEFT | RIGHT

LAYERS = (
    ((0, 5), (1, 6), (2, 7), (3, 8), (4, 9)),
    ((0, 6), (1, 7), (2, 8), (3, 9), (4, 5)),
    ((0, 7), (1, 8), (2, 9), (3, 5), (4, 6)),
    ((0, 8), (1, 9), (2, 5), (3, 6)),
    ((4, 7), (0, 9), (1, 5), (10, 11)),
    ((2, 6), (3, 7), (4, 8), (11, 12)),
)


def normalized(edge: tuple[int, int]) -> tuple[int, int]:
    return tuple(sorted(edge))


def has_perfect_matching(
    vertices: frozenset[int],
    edges: frozenset[tuple[int, int]],
) -> bool:
    if not vertices:
        return True
    first = min(vertices)
    for second in sorted(vertices - {first}):
        edge = normalized((first, second))
        if edge in edges and has_perfect_matching(vertices - {first, second}, edges):
            return True
    return False


def main() -> None:
    layer_edges = tuple(
        tuple(normalized(edge) for edge in layer) for layer in LAYERS
    )
    assert sorted(map(len, layer_edges)) == [4, 4, 4, 5, 5, 5]
    for layer in layer_edges:
        assert len(set(vertex for edge in layer for vertex in edge)) == 2 * len(layer)

    deleted = frozenset(edge for layer in layer_edges for edge in layer)
    assert sum(map(len, layer_edges)) == len(deleted) == 27
    expected_deleted = frozenset(
        normalized((left, right)) for left in LEFT for right in RIGHT
    ) | {normalized((10, 11)), normalized((11, 12))}
    assert deleted == expected_deleted

    complete = frozenset(combinations(VERTICES, 2))
    available = complete - deleted
    degrees = {
        vertex: sum(vertex in edge for edge in deleted) for vertex in VERTICES
    }
    assert tuple(degrees[vertex] for vertex in VERTICES) == (
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        1,
        2,
        1,
    )
    assert len(available) == 51
    assert min(12 - degree for degree in degrees.values()) == 7

    # The selected support induces two odd cliques and has no perfect matching.
    support_edges = frozenset(
        edge for edge in available if edge[0] in SUPPORT and edge[1] in SUPPORT
    )
    assert support_edges == frozenset(combinations(sorted(LEFT), 2)) | frozenset(
        combinations(sorted(RIGHT), 2)
    )
    assert not has_perfect_matching(SUPPORT, support_edges)

    # All positive capacity inequalities hold for three repeated copies of
    # SUPPORT.  Applying the same loop to V\U also checks the negative half.
    for mask in range(1 << len(VERTICES)):
        subset = frozenset(
            vertex for vertex in VERTICES if mask & (1 << vertex)
        )
        required = 3 * max(0, len(SUPPORT & subset) - 5)
        internal = sum(edge[0] in subset and edge[1] in subset for edge in available)
        assert required <= internal

    # A full class-B row inventory has total incidence 7*3+4*5=41 and
    # rho(v)=d_D(v)-1.  The ten support vertices consume 40 incidences, so
    # the three omitted vertices receive only one in total.  Therefore ROW,
    # which would contribute one incidence at each of them, cannot be a row.
    rho = {vertex: degrees[vertex] - 1 for vertex in VERTICES}
    assert sum(rho.values()) == 41
    assert sum(rho[vertex] for vertex in SUPPORT) == 40
    assert sum(rho[vertex] for vertex in ROW) == 1 < len(ROW)

    print("PASS: six matching layers have sizes 4,4,4,5,5,5")
    print("PASS: D is K_5,5 plus a two-edge path and has degree range 1..5")
    print("PASS: G has 51 edges, minimum degree 7, and G[S] has no perfect matching")
    print("PASS: all 2^13 positive and complementary capacity cuts hold")
    print("PASS: the full class-B row inventory excludes the repeated row")


if __name__ == "__main__":
    main()
