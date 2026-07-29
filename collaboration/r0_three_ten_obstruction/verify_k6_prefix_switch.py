#!/usr/bin/env python3
"""Exact audit for the support-preserving K6 prefix switch."""

from itertools import combinations


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def translate(prefix, pairs):
    return frozenset(edge(f"{prefix}{a}", f"{prefix}{b}") for a, b in pairs)


def support(edges):
    return frozenset().union(*edges)


def is_matching(edges):
    ends = [v for e in edges for v in e]
    return len(ends) == len(set(ends))


def perfect_matching_count(vertices, allowed_edges):
    vertices = tuple(sorted(vertices))

    def rec(remaining):
        if not remaining:
            return 1
        u = remaining[0]
        count = 0
        for i in range(1, len(remaining)):
            v = remaining[i]
            if edge(u, v) in allowed_edges:
                count += rec(remaining[1:i] + remaining[i + 1 :])
        return count

    return rec(vertices)


def odd_partitions(total, length, minimum=1):
    result = []

    def rec(prefix, remaining, lower):
        if len(prefix) == length:
            if remaining == 0:
                result.append(tuple(prefix))
            return
        slots = length - len(prefix)
        for value in range(lower, remaining + 1, 2):
            if value * slots > remaining:
                break
            rec(prefix + [value], remaining - value, value)

    first = minimum if minimum % 2 else minimum + 1
    rec([], total, max(1, first))
    return result


def check_catalogue_and_capacities():
    survivors = []
    for separator in range(5):
        for blocks in odd_partitions(10 - separator, separator + 2):
            core_degree = sum(blocks) - min(blocks)
            if core_degree <= 5:
                survivors.append((separator, blocks))
    assert survivors == [(0, (5, 5)), (4, (1, 1, 1, 1, 1, 1))]

    rows = {
        0: ((4, 7, 0), 41, 38, 27),
        1: ((4, 6, 1), 39, 36, 26),
        2: ((5, 4, 2), 39, 36, 26),
    }
    for _r, ((fives, triples, singletons), total, after, edge_count) in rows.items():
        assert 5 * fives + 3 * triples + singletons == total
        assert total - 3 == after < 40
        assert edge_count - 15 <= 12 < 15


def check_abstract_new_k6():
    c = tuple(f"c{i}" for i in range(6))
    o = tuple(f"o{i}" for i in range(7))
    uv = edge("c0", "c1")
    pq = edge("o0", "o1")
    up = edge("c0", "o0")
    vq = edge("c1", "o1")

    # Use every O-edge as a permissive supergraph.  The only all-O K6s
    # are excluded in the theorem by the <=12 outside-edge budget.
    graph = (
        {edge(u, v) for u, v in combinations(c, 2)}
        | {edge(u, v) for u, v in combinations(o, 2)}
    )
    graph = graph - {uv, pq} | {up, vq}
    for vertices in combinations(c + o, 6):
        if not (set(vertices) & set(c)):
            continue
        clique_edges = {edge(u, v) for u, v in combinations(vertices, 2)}
        assert not clique_edges <= graph


def check_concrete_switch():
    c = tuple(f"c{i}" for i in range(6))
    o = tuple(f"o{i}" for i in range(7))
    vertices = frozenset(c + o)
    c_rows = (
        ((0, 5), (1, 4), (2, 3)),
        ((0, 4), (3, 5), (1, 2)),
        ((0, 3), (2, 4), (1, 5)),
        ((1, 3), (4, 5)),
        ((0, 1), (2, 5)),
        ((0, 2), (3, 4)),
    )
    o_rows = (
        ((0, 3), (1, 5)),
        ((0, 4), (2, 6)),
        ((0, 5), (3, 6)),
        ((0, 6), (4, 5)),
        ((3, 4), (5, 6)),
        ((3, 5), (4, 6)),
    )
    selected = [
        translate("c", c_row) | translate("o", o_row)
        for c_row, o_row in zip(c_rows, o_rows)
    ]
    old_supports = [support(matching) for matching in selected]
    old_degrees = {
        v: sum(v in e for matching in selected for e in matching)
        for v in vertices
    }

    removed = {edge("c0", "c5"), edge("o0", "o3")}
    added = {edge("c0", "o0"), edge("c5", "o3")}
    assert removed <= selected[0]
    selected[0] = selected[0] - removed | added

    assert all(is_matching(matching) for matching in selected)
    assert [support(matching) for matching in selected] == old_supports
    assert all(
        selected[i].isdisjoint(selected[j])
        for i, j in combinations(range(6), 2)
    )
    switched_edges = frozenset().union(*selected)
    switched_degrees = {
        v: sum(v in e for e in switched_edges) for v in vertices
    }
    assert switched_degrees == old_degrees
    assert max(switched_degrees.values()) == 5

    for six_set in combinations(vertices, 6):
        clique_edges = {edge(u, v) for u, v in combinations(six_set, 2)}
        assert not clique_edges <= switched_edges

    all_edges = frozenset(
        edge(u, v) for u, v in combinations(vertices, 2)
    )
    residual = all_edges - switched_edges
    triples = tuple(
        frozenset(f"o{i}" for i in digits)
        for digits in ((0, 5, 6), (3, 4, 5), (3, 4, 6), (3, 5, 6), (4, 5, 6))
    ) + (
        frozenset(("c0", "c1", "o0")),
        frozenset(("c2", "c3", "o0")),
    )
    counts = [
        perfect_matching_count(vertices - triple, residual)
        for triple in triples
    ]
    assert counts == [24, 24, 24, 24, 24, 138, 152]


def check_r2_concrete_switch():
    vertices = frozenset(range(13))
    rows = (
        ((7, 11), (9, 12), (2, 6), (4, 5)),
        ((8, 9), (10, 12), (3, 5), (4, 6)),
        ((7, 8), (10, 11), (2, 4), (5, 6)),
        ((7, 9), (8, 10), (11, 12), (3, 4)),
        ((7, 10), (8, 12), (9, 11), (2, 3), (0, 1)),
        ((7, 12), (8, 11), (9, 10), (2, 5), (3, 6)),
    )
    selected = [{edge(u, v) for u, v in row} for row in rows]
    old_support = support(selected[0])
    removed = {edge(7, 11), edge(2, 6)}
    added = {edge(7, 2), edge(11, 6)}
    selected[0] = selected[0] - removed | added
    assert support(selected[0]) == old_support
    assert all(is_matching(matching) for matching in selected)
    assert all(
        selected[i].isdisjoint(selected[j])
        for i, j in combinations(range(6), 2)
    )

    switched_edges = frozenset().union(*selected)
    for six_set in combinations(vertices, 6):
        clique_edges = {edge(u, v) for u, v in combinations(six_set, 2)}
        assert not clique_edges <= switched_edges

    all_edges = frozenset(
        edge(u, v) for u, v in combinations(vertices, 2)
    )
    residual = all_edges - switched_edges
    triples = (
        frozenset((3, 5, 6)),
        frozenset((2, 4, 6)),
        frozenset((2, 3, 5)),
        frozenset((2, 3, 4)),
    )
    counts = [
        perfect_matching_count(vertices - triple, residual)
        for triple in triples
    ]
    assert counts == [24, 24, 24, 24]


def main():
    check_catalogue_and_capacities()
    check_abstract_new_k6()
    check_concrete_switch()
    check_r2_concrete_switch()
    print("support-preserving K6 prefix switch audit: PASS")


if __name__ == "__main__":
    main()
