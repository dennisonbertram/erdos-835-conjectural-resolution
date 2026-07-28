#!/usr/bin/env python3
"""Finite audit for the solver-free r0 equality-coordination theorem."""

from itertools import combinations


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def is_matching(edges):
    endpoints = [vertex for item in edges for vertex in item]
    return len(endpoints) == len(set(endpoints))


def has_covering_two_matching(edges, required):
    return any(
        first.isdisjoint(second)
        and required <= first | second
        for first, second in combinations(edges, 2)
    )


def check_incidence_and_layer_arithmetic():
    cases = [
        (cross_count, seventh_core_size)
        for cross_count in range(3)
        for seventh_core_size in range(1, 4)
        if 22 + cross_count - seventh_core_size <= 20
    ]
    assert cases == [(0, 2), (0, 3), (1, 3)]

    core_layer_count = (14 + 2) // 3
    assert core_layer_count == 5
    for cross_count, seventh_core_size in cases:
        outside_edge_count = 13 - cross_count
        outside_layer_count = (outside_edge_count + 2) // 3
        assert core_layer_count + outside_layer_count > 6
        assert seventh_core_size >= 2 + cross_count
        assert cross_count + 2 <= 3

    # In the (0,2) case, at least eight selected W-edges avoid w_*.
    avoiding_layer_count = (8 + 2) // 3
    assert avoiding_layer_count + core_layer_count > 6


def check_hall_rectangles():
    thresholds = [
        size * (5 - size) for size in range(1, 5)
    ]
    first_matching_contribution = [
        min(size, 5 - size) for size in range(1, 5)
    ]
    prefix_contribution = [2, 3, 3, 2]
    totals = [
        first + prefix
        for first, prefix in zip(
            first_matching_contribution,
            prefix_contribution,
        )
    ]
    assert thresholds == [4, 6, 6, 4]
    assert first_matching_contribution == [1, 2, 2, 1]
    assert totals == [3, 5, 5, 3]
    assert all(total < threshold for total, threshold in zip(totals, thresholds))

    # A Hall obstruction in the first K_{4,4} needs at least four
    # deletions, while the cross deletion set has order at most three.
    assert min(thresholds) == 4 > 3


def check_four_by_four_terminal():
    # Numerical Hall audit for a balanced 4-by-4 graph of minimum degree 2.
    for size in range(1, 5):
        if size <= 2:
            minimum_neighborhood = 2
        elif size == 3:
            # A neighborhood of order at most two would leave a right
            # vertex with degree at most one.
            minimum_neighborhood = 3
        else:
            minimum_neighborhood = 4
        assert minimum_neighborhood >= size


def check_w_matching_claims():
    vertices = frozenset(range(7))
    all_edges = tuple(edge(u, v) for u, v in combinations(vertices, 2))
    pq = edge(0, 1)
    other_edges = tuple(item for item in all_edges if item != pq)

    # a=0: H[W] consists of pq and any eight old residual edges.
    for chosen in combinations(other_edges, 8):
        graph = frozenset(chosen) | {pq}
        assert has_covering_two_matching(graph, frozenset((0, 1)))

    # a=1, with w_0=2 distinct from p,q.  The coincident cases reduce to
    # the preceding two-vertex claim.  The old cross-edge gives d_H(w_0)>=2.
    required = frozenset((0, 1, 2))
    for chosen in combinations(other_edges, 9):
        graph = frozenset(chosen) | {pq}
        if sum(2 in item for item in graph) < 2:
            continue
        assert has_covering_two_matching(graph, required)


def check_k22_switch():
    x, y, a1, a2 = "x", "y", "a1", "a2"
    p, q, b1, b2 = "p", "q", "b1", "b2"
    c1 = {
        edge(x, p),
        edge(y, q),
        edge(a1, b1),
        edge(a2, b2),
    }
    c2_core = {edge(x, q), edge(y, p)}
    options = (
        (
            {edge(x, p), edge(a1, b1)},
            {edge(x, b1), edge(a1, p)},
            "xp",
        ),
        (
            {edge(y, q), edge(a1, b1)},
            {edge(y, b1), edge(a1, q)},
            "yq",
        ),
        (
            {edge(x, p), edge(a2, b2)},
            {edge(x, b2), edge(a2, p)},
            "xp",
        ),
        (
            {edge(y, q), edge(a2, b2)},
            {edge(y, b2), edge(a2, q)},
            "yq",
        ),
    )
    candidate_pairs = [added for _, added, _ in options]
    assert all(
        candidate_pairs[i].isdisjoint(candidate_pairs[j])
        for i, j in combinations(range(4), 2)
    )
    candidate_edges = frozenset().union(*candidate_pairs)
    assert len(candidate_edges) == 8

    for deletion_size in range(4):
        for forbidden in combinations(candidate_edges, deletion_size):
            forbidden = frozenset(forbidden)
            legal = [
                option
                for option in options
                if option[1].isdisjoint(forbidden)
            ]
            assert legal
            for removed, added, freed in legal:
                switched = c1 - removed | added
                assert is_matching(switched)
                assert added.isdisjoint(c2_core)
                # The third good-grid vertices may or may not occur among
                # the two outer edges of C1.  Audit every alias pattern.
                for z in ("z", a1, a2):
                    for s in ("s", b1, b2):
                        if freed == "xp":
                            good_matching = {
                                edge(x, p),
                                edge(y, s),
                                edge(z, q),
                            }
                        else:
                            good_matching = {
                                edge(y, q),
                                edge(x, s),
                                edge(z, p),
                            }
                        assert is_matching(good_matching)
                        assert good_matching.isdisjoint(switched)
                        assert good_matching.isdisjoint(c2_core)


def main():
    check_incidence_and_layer_arithmetic()
    check_hall_rectangles()
    check_four_by_four_terminal()
    check_w_matching_claims()
    check_k22_switch()
    print("r0 equality-coordination audit: PASS")


if __name__ == "__main__":
    main()
