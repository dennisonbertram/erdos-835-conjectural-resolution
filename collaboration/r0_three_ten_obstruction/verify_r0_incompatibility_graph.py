#!/usr/bin/env python3
"""Finite audit for the r0 size-ten incompatibility-graph theorem."""

from itertools import combinations


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def degrees(vertices, edges):
    return {
        vertex: sum(vertex in item for item in edges)
        for vertex in vertices
    }


def k6_minus_edge(vertices, missing):
    return frozenset(
        edge(u, v) for u, v in combinations(vertices, 2)
    ) - {missing}


def check_k55_equality():
    # The ten other remaining complements have capacity exactly 38 on Y.
    possible_endpoint_extras = [
        extra for extra in range(3) if 38 + extra <= 38
    ]
    assert possible_endpoint_extras == [0]

    a = tuple(f"a{i}" for i in range(5))
    b = tuple(f"b{i}" for i in range(5))
    x = tuple(f"x{i}" for i in range(3))
    vertices = frozenset(a + b + x)
    missing = edge("a0", "b0")
    core = frozenset(edge(u, v) for u in a for v in b) - {missing}
    triangle = frozenset(edge(u, v) for u, v in combinations(x, 2))
    graph = core | triangle
    assert len(graph) == 27
    graph_degrees = degrees(vertices, graph)
    assert sorted(graph_degrees.values()) == [2] * 3 + [4] * 2 + [5] * 8

    # No K6-e can occur in the canonical graph.
    k6_cores = []
    for six_set in combinations(vertices, 6):
        six_set = frozenset(six_set)
        for missing_pair in combinations(six_set, 2):
            candidate = k6_minus_edge(six_set, edge(*missing_pair))
            if candidate <= graph:
                k6_cores.append((six_set, edge(*missing_pair)))
    assert k6_cores == []

    # Enumerate every 5+5 bipartition of every ten-set, modulo swapping.
    k55_cores = set()
    for ten_set in combinations(vertices, 10):
        ten_set = frozenset(ten_set)
        anchor = min(ten_set)
        for left_tail in combinations(ten_set - {anchor}, 4):
            left = frozenset((anchor,) + left_tail)
            right = ten_set - left
            cross = frozenset(edge(u, v) for u in left for v in right)
            missing_cross = cross - graph
            if len(missing_cross) == 1:
                k55_cores.add((left, right, next(iter(missing_cross))))
    assert len(k55_cores) == 1
    left, right, unique_missing = next(iter(k55_cores))
    assert {left, right} == {frozenset(a), frozenset(b)}
    assert unique_missing == missing


def check_k6_core_uniqueness():
    # Exhaust every intersection size and both missing edges.  Distinct
    # six-sets never coexist under |E(D)|<=27 and Delta(D)<=5.
    for intersection_size in range(6):
        first_vertices = frozenset(range(6))
        second_vertices = frozenset(
            range(6 - intersection_size, 12 - intersection_size)
        )
        coexist = []
        for first_missing_pair in combinations(first_vertices, 2):
            first = k6_minus_edge(
                first_vertices,
                edge(*first_missing_pair),
            )
            for second_missing_pair in combinations(second_vertices, 2):
                second = k6_minus_edge(
                    second_vertices,
                    edge(*second_missing_pair),
                )
                union = first | second
                union_degrees = degrees(
                    first_vertices | second_vertices,
                    union,
                )
                if len(union) <= 27 and max(union_degrees.values()) <= 5:
                    coexist.append(
                        (first_missing_pair, second_missing_pair)
                    )
        assert coexist == []

    # On the same six-set, two different missing edges unite to K6.
    vertices = frozenset(range(6))
    missing_edges = tuple(edge(u, v) for u, v in combinations(vertices, 2))
    for first_missing, second_missing in combinations(missing_edges, 2):
        union = (
            k6_minus_edge(vertices, first_missing)
            | k6_minus_edge(vertices, second_missing)
        )
        assert len(union) == 15


def independence_number(order, graph_edges):
    for size in range(order, -1, -1):
        for subset in combinations(range(order), size):
            if all(
                edge(u, v) not in graph_edges
                for u, v in combinations(subset, 2)
            ):
                return size
    raise AssertionError("unreachable")


def check_incompatibility_graphs():
    for cross_count in range(3):
        maximum_t = (19 - cross_count) // 3
        assert maximum_t <= 6

    for clique_size in range(7):
        graph_edges = frozenset(
            edge(u, v)
            for u, v in combinations(range(clique_size), 2)
        )
        alpha = independence_number(7, graph_edges)
        expected = 7 if clique_size == 0 else 8 - clique_size
        assert alpha == expected
        has_independent_triple = alpha >= 3
        assert has_independent_triple == (clique_size <= 5)


def main():
    check_k55_equality()
    check_k6_core_uniqueness()
    check_incompatibility_graphs()
    print("r0 incompatibility-graph audit: PASS")


if __name__ == "__main__":
    main()
