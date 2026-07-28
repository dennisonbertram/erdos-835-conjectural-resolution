#!/usr/bin/env python3
"""Exact audit of the K6-free r=0 three-size-ten obstruction."""

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


def main():
    c = tuple(f"c{i}" for i in range(6))
    o = tuple(f"o{i}" for i in range(7))
    c_set = frozenset(c)
    vertices = frozenset(c + o)

    c_rows = (
        ((1, 4), (2, 3)),
        ((0, 4), (3, 5), (1, 2)),
        ((0, 3), (2, 4), (1, 5)),
        ((0, 2), (4, 5)),
        ((2, 5), (3, 4)),
        ((0, 5), (1, 3)),
    )
    o_rows = (
        ((0, 2), (1, 3), (4, 5)),
        ((0, 5), (1, 2)),
        ((0, 6), (2, 3)),
        ((1, 6), (2, 4)),
        ((3, 4), (5, 6)),
        ((3, 5), (4, 6)),
    )
    selected = tuple(
        translate("c", c_row) | translate("o", o_row)
        for c_row, o_row in zip(c_rows, o_rows)
    )
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
    assert [degrees[vertex] for vertex in o] == [3, 3, 4, 4, 4, 4, 4]
    assert max(degrees.values()) == 5
    assert all(len(item & c_set) != 1 for item in prefix)

    expected_c_edges = {
        edge(u, v) for u, v in combinations(c, 2)
    } - {edge("c0", "c1")}
    expected_o_edges = translate(
        "o",
        (
            (0, 2),
            (0, 5),
            (0, 6),
            (1, 2),
            (1, 3),
            (1, 6),
            (2, 3),
            (2, 4),
            (3, 4),
            (3, 5),
            (4, 5),
            (4, 6),
            (5, 6),
        ),
    )
    assert prefix == expected_c_edges | expected_o_edges

    for six_set in combinations(vertices, 6):
        clique_edges = {
            edge(u, v) for u, v in combinations(six_set, 2)
        }
        assert not clique_edges <= prefix

    forced_triples = tuple(
        frozenset(f"o{i}" for i in digits)
        for digits in (
            (0, 1, 2),
            (1, 2, 3),
            (2, 4, 6),
            (3, 4, 5),
            (3, 5, 6),
            (4, 5, 6),
        )
    )
    good_triple = frozenset(("c2", "c3", "o0"))
    remaining_triples = forced_triples + (good_triple,)
    remaining_fives = tuple(c_set - {f"c{i}"} for i in range(4))
    all_complements = (
        selected_complements + remaining_triples + remaining_fives
    )

    assert len(all_complements) == 17
    assert len(set(all_complements)) == 17
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

    all_edges = frozenset(
        edge(u, v) for u, v in combinations(vertices, 2)
    )
    residual = all_edges - prefix
    families = tuple(
        perfect_matchings(vertices - triple, residual)
        for triple in remaining_triples
    )
    assert [len(family) for family in families] == [24] * 6 + [132]

    forced_edge = edge("c0", "c1")
    assert all(
        all(forced_edge in matching for matching in family)
        for family in families[:6]
    )
    good_witness = frozenset(
        (
            edge("c0", "o2"),
            edge("c1", "o3"),
            edge("c4", "o5"),
            edge("c5", "o6"),
            edge("o1", "o4"),
        )
    )
    assert good_witness in families[6]

    packable_triples = []
    for indices in combinations(range(7), 3):
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
            packable_triples.append(indices)
    assert packable_triples == []

    mixed_extension = (
        frozenset(
            (
                edge("c0", "c1"),
                edge("c2", "o3"),
                edge("c3", "o4"),
                edge("c4", "o5"),
                edge("c5", "o6"),
            )
        ),
        frozenset(
            (
                edge("c0", "o1"),
                edge("c1", "o2"),
                edge("c4", "o4"),
                edge("c5", "o5"),
                edge("o3", "o6"),
            )
        ),
        frozenset(
            (
                edge("c0", "o3"),
                edge("o0", "o4"),
                edge("o1", "o5"),
                edge("o2", "o6"),
            )
        ),
    )
    mixed_supports = (
        vertices - forced_triples[0],
        vertices - good_triple,
        vertices - remaining_fives[0],
    )
    assert all(is_matching(row) for row in mixed_extension)
    assert tuple(support(row) for row in mixed_extension) == mixed_supports
    assert all(row <= residual for row in mixed_extension)
    assert all(
        mixed_extension[i].isdisjoint(mixed_extension[j])
        for i, j in combinations(range(3), 2)
    )

    print("K6-free r=0 three-size-ten obstruction audit: PASS")


if __name__ == "__main__":
    main()
