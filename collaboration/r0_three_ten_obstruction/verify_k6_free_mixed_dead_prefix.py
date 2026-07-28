#!/usr/bin/env python3
"""Audit the K6-free mixed dead prefix and its repairing trade."""

from itertools import combinations


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def translate(prefix, pairs):
    return frozenset(edge(f"{prefix}{a}", f"{prefix}{b}") for a, b in pairs)


def support(edges):
    return frozenset().union(*edges)


def is_matching(edges):
    endpoints = [vertex for item in edges for vertex in item]
    return len(endpoints) == len(set(endpoints))


def perfect_matchings(vertices, allowed_edges):
    vertices = tuple(sorted(vertices))
    result = []

    def rec(remaining, chosen):
        if not remaining:
            result.append(frozenset(chosen))
            return
        u = remaining[0]
        for index in range(1, len(remaining)):
            v = remaining[index]
            item = edge(u, v)
            if item in allowed_edges:
                rec(
                    remaining[1:index] + remaining[index + 1 :],
                    chosen + [item],
                )

    rec(vertices, [])
    return result


def maximum_matching_size(vertices, allowed_edges):
    vertices = tuple(sorted(vertices))

    def rec(remaining):
        if not remaining:
            return 0
        u = remaining[0]
        best = rec(remaining[1:])
        for index in range(1, len(remaining)):
            v = remaining[index]
            if edge(u, v) in allowed_edges:
                best = max(
                    best,
                    1 + rec(remaining[1:index] + remaining[index + 1 :]),
                )
        return best

    return rec(vertices)


def packable_triples(families):
    result = []
    for indices in combinations(range(len(families)), 3):
        family_a, family_b, family_c = (families[i] for i in indices)
        packable = any(
            matching_a.isdisjoint(matching_b)
            and matching_a.isdisjoint(matching_c)
            and matching_b.isdisjoint(matching_c)
            for matching_a in family_a
            for matching_b in family_b
            for matching_c in family_c
        )
        if packable:
            result.append(indices)
    return result


def check_equality_core_arithmetic():
    cases = [
        (outside_cross_edges, seventh_triple_core_size)
        for outside_cross_edges in range(3)
        for seventh_triple_core_size in range(1, 4)
        if 22 + outside_cross_edges - seventh_triple_core_size <= 20
    ]
    assert cases == [(0, 2), (0, 3), (1, 3)]
    for outside_cross_edges, _ in cases:
        core_layer_count = (14 + 2) // 3
        outside_layer_count = (13 - outside_cross_edges + 2) // 3
        assert core_layer_count + outside_layer_count > 6
        assert outside_cross_edges + 2 <= 3

    # If Hall fails in K_{4,4}, a set of s left vertices must lose every
    # edge to 4-(s-1) right vertices.  Even the smallest such cut has size 4.
    hall_deletion_sizes = [
        size * (4 - size + 1) for size in range(1, 5)
    ]
    assert min(hall_deletion_sizes) == 4


def main():
    check_equality_core_arithmetic()

    c = tuple(f"c{i}" for i in range(6))
    o = tuple(f"o{i}" for i in range(7))
    c_set = frozenset(c)
    o_set = frozenset(o)
    vertices = frozenset(c + o)
    all_edges = frozenset(
        edge(u, v) for u, v in combinations(vertices, 2)
    )

    c_rows = (
        ((1, 4), (2, 3)),
        ((0, 4), (3, 5), (1, 2)),
        ((0, 3), (2, 4), (1, 5)),
        ((0, 2), (4, 5)),
        ((2, 5), (3, 4)),
        ((0, 5), (1, 3)),
    )
    o_rows = (
        ((4, 5), (2, 3), (0, 6)),
        ((4, 6), (2, 5)),
        ((2, 6), (3, 4)),
        ((5, 6), (2, 4)),
        ((3, 5), (1, 4)),
        ((3, 6), (1, 5)),
    )
    selected = [
        translate("c", c_row) | translate("o", o_row)
        for c_row, o_row in zip(c_rows, o_rows)
    ]
    assert [len(row) for row in selected] == [5, 5, 5, 4, 4, 4]
    assert all(is_matching(row) for row in selected)
    assert all(
        selected[i].isdisjoint(selected[j])
        for i, j in combinations(range(6), 2)
    )

    selected_supports = tuple(support(row) for row in selected)
    selected_complements = tuple(vertices - item for item in selected_supports)
    assert [len(item) for item in selected_complements] == [3, 3, 3, 5, 5, 5]
    assert frozenset().union(*selected_complements) == vertices

    prefix = frozenset().union(*selected)
    assert len(prefix) == 27
    degrees = {
        vertex: sum(vertex in item for item in prefix)
        for vertex in vertices
    }
    assert [degrees[vertex] for vertex in c] == [4, 4, 5, 5, 5, 5]
    assert [degrees[vertex] for vertex in o] == [1, 2, 4, 4, 5, 5, 5]
    assert max(degrees.values()) == 5
    assert all(len(item & c_set) != 1 for item in prefix)
    assert {
        edge(u, v) for u, v in combinations(c, 2)
    } - prefix == {edge("c0", "c1")}

    residual = all_edges - prefix
    residual_o = frozenset(item for item in residual if item <= o_set)
    expected_residual_o = translate(
        "o",
        ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 6)),
    )
    assert residual_o == expected_residual_o
    assert all("o0" in item or "o1" in item for item in residual_o)
    assert maximum_matching_size(o, residual_o) == 2

    for six_set in combinations(vertices, 6):
        clique_edges = {
            edge(u, v) for u, v in combinations(six_set, 2)
        }
        assert not clique_edges <= prefix

    remaining_fives = tuple(c_set - {f"c{i}"} for i in range(4))
    forced_triples = tuple(
        frozenset(f"o{i}" for i in digits)
        for digits in (
            (2, 3, 4),
            (2, 4, 5),
            (2, 5, 6),
            (3, 4, 6),
            (3, 5, 6),
            (4, 5, 6),
        )
    )
    good_triple = frozenset(("c2", "c3", "o1"))
    remaining_complements = (
        remaining_fives + forced_triples + (good_triple,)
    )
    all_complements = selected_complements + remaining_complements
    assert len(all_complements) == len(set(all_complements)) == 17
    assert sorted(map(len, all_complements)) == [3] * 10 + [5] * 7
    assert all(
        sum(vertex in item for item in all_complements) == 5
        for vertex in vertices
    )
    all_supports = tuple(vertices - item for item in all_complements)
    assert sorted(map(len, all_supports)) == [8] * 7 + [10] * 10
    assert all(
        sum(vertex in item for item in all_supports) == 12
        for vertex in vertices
    )

    families = tuple(
        perfect_matchings(vertices - item, residual)
        for item in remaining_complements
    )
    assert [len(family) for family in families] == [0] * 4 + [24] * 6 + [96]
    forced_edge = edge("c0", "c1")
    assert all(
        all(forced_edge in matching for matching in family)
        for family in families[4:10]
    )
    good_witness = frozenset(
        (
            edge("o0", "o2"),
            edge("c0", "o3"),
            edge("c1", "o4"),
            edge("c4", "o5"),
            edge("c5", "o6"),
        )
    )
    assert good_witness in families[10]
    assert packable_triples(families) == []

    removed = {edge("c1", "c4"), edge("o0", "o6")}
    added = {edge("c1", "o6"), edge("c4", "o0")}
    assert removed <= selected[0]
    assert added.isdisjoint(prefix)
    old_support = support(selected[0])
    selected[0] = selected[0] - removed | added
    assert is_matching(selected[0])
    assert support(selected[0]) == old_support
    assert all(
        selected[i].isdisjoint(selected[j])
        for i, j in combinations(range(6), 2)
    )

    switched_prefix = frozenset().union(*selected)
    switched_degrees = {
        vertex: sum(vertex in item for item in switched_prefix)
        for vertex in vertices
    }
    assert switched_degrees == degrees
    switched_residual = all_edges - switched_prefix
    switched_families = tuple(
        perfect_matchings(vertices - item, switched_residual)
        for item in remaining_complements
    )
    assert [len(family) for family in switched_families] == (
        [0] * 4 + [42] * 6 + [96]
    )

    witnesses = (
        frozenset(
            (
                edge("c0", "c1"),
                edge("c2", "o0"),
                edge("c3", "o1"),
                edge("c4", "o5"),
                edge("c5", "o6"),
            )
        ),
        frozenset(
            (
                edge("c0", "o0"),
                edge("c1", "c4"),
                edge("c2", "o1"),
                edge("c3", "o6"),
                edge("c5", "o3"),
            )
        ),
        frozenset(
            (
                edge("c0", "o2"),
                edge("c1", "o3"),
                edge("c4", "o4"),
                edge("c5", "o5"),
                edge("o0", "o6"),
            )
        ),
    )
    witness_indices = (4, 5, 10)
    for index, witness in zip(witness_indices, witnesses):
        assert witness in switched_families[index]
    assert all(
        witnesses[i].isdisjoint(witnesses[j])
        for i, j in combinations(range(3), 2)
    )

    print("K6-free mixed dead-prefix and repair audit: PASS")


if __name__ == "__main__":
    main()
