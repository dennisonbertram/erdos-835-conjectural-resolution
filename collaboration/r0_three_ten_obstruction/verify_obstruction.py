#!/usr/bin/env python3
"""Exact audit for the sharp r=0 three-size-ten obstruction."""

from itertools import combinations


C = tuple(f"c{i}" for i in range(6))
OUTSIDE = tuple(f"o{i}" for i in range(7))
V = frozenset(C + OUTSIDE)


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def translate(prefix, pairs):
    return frozenset(edge(f"{prefix}{a}", f"{prefix}{b}") for a, b in pairs)


def is_matching(edges):
    ends = [v for e in edges for v in e]
    return len(ends) == len(set(ends))


def support(edges):
    return frozenset().union(*edges)


def has_perfect_matching(vertices, allowed_edges):
    vertices = tuple(sorted(vertices))

    def rec(remaining):
        if not remaining:
            return True
        u = remaining[0]
        for i in range(1, len(remaining)):
            v = remaining[i]
            if edge(u, v) not in allowed_edges:
                continue
            if rec(remaining[1:i] + remaining[i + 1 :]):
                return True
        return False

    return rec(vertices)


def main():
    c_rows = (
        ((0, 5), (1, 4), (2, 3)),
        ((0, 4), (3, 5), (1, 2)),
        ((0, 3), (2, 4), (1, 5)),
        ((1, 3), (4, 5)),
        ((0, 1), (2, 5)),
        ((0, 2), (3, 4)),
    )
    o_rows = (
        ((2, 5), (3, 4)),
        ((3, 6), (4, 5)),
        ((0, 4), (5, 6)),
        ((1, 5), (0, 6)),
        ((2, 6), (0, 1)),
        ((0, 3), (1, 2)),
    )
    matchings = tuple(
        translate("c", c_row) | translate("o", o_row)
        for c_row, o_row in zip(c_rows, o_rows)
    )
    assert [len(m) for m in matchings] == [5, 5, 5, 4, 4, 4]
    assert all(is_matching(m) for m in matchings)
    assert all(
        matchings[i].isdisjoint(matchings[j])
        for i, j in combinations(range(6), 2)
    )

    d_edges = frozenset().union(*matchings)
    assert len(d_edges) == 27
    assert translate("c", combinations(range(6), 2)) <= d_edges
    degrees = {v: sum(v in e for e in d_edges) for v in V}
    assert max(degrees.values()) == 5
    assert {v: degrees[v] for v in C} == {v: 5 for v in C}
    assert [degrees[v] for v in OUTSIDE] == [4, 3, 3, 3, 3, 4, 4]

    selected_complements = tuple(V - support(m) for m in matchings)
    assert [len(a) for a in selected_complements] == [3, 3, 3, 5, 5, 5]
    assert frozenset().union(*selected_complements) == V

    remaining_fives = tuple(
        frozenset(C) - {f"c{i}"} for i in range(4)
    )
    blocked_triples = tuple(
        frozenset(f"o{i}" for i in digits)
        for digits in ((0, 1, 3), (1, 2, 4), (2, 5, 6), (3, 5, 6), (4, 5, 6))
    )
    good_triples = (
        frozenset(("c0", "c1", "o0")),
        frozenset(("c2", "c3", "o0")),
    )

    five_sets = selected_complements[3:] + remaining_fives
    triples = selected_complements[:3] + blocked_triples + good_triples
    assert len(five_sets) == 7
    assert len(triples) == 10
    assert all(len(a) == 5 for a in five_sets)
    assert all(len(a) == 3 for a in triples)
    assert len(set(five_sets)) == 7
    assert len(set(triples)) == 10
    assert all(
        sum(v in a for a in five_sets + triples) == 5 for v in V
    )

    all_edges = frozenset(edge(u, v) for u, v in combinations(V, 2))
    residual = all_edges - d_edges

    for triple in blocked_triples:
        target = V - triple
        assert frozenset(C) <= target
        assert len(target & frozenset(OUTSIDE)) == 4
        assert not has_perfect_matching(target, residual)

    forced_triple = frozenset(("o0", "o1", "o3"))
    forced_edge = edge("o1", "o3")
    assert forced_triple in blocked_triples
    assert forced_edge in residual
    # A near-factor missing o0 and containing o1o3 is exactly this forced
    # edge plus a perfect matching on V minus the displayed triple.
    assert not has_perfect_matching(V - forced_triple, residual - {forced_edge})

    witnesses = (
        (
            edge("c2", "o1"),
            edge("c3", "o2"),
            edge("c4", "o3"),
            edge("c5", "o5"),
            edge("o4", "o6"),
        ),
        (
            edge("c0", "o1"),
            edge("c1", "o2"),
            edge("c4", "o3"),
            edge("c5", "o5"),
            edge("o4", "o6"),
        ),
    )
    for triple, witness in zip(good_triples, witnesses):
        witness = frozenset(witness)
        target = V - triple
        assert len(witness) == 5
        assert is_matching(witness)
        assert support(witness) == target
        assert witness <= residual
        assert has_perfect_matching(target, residual)

    print("sharp r=0 three-size-ten obstruction audit: PASS")


if __name__ == "__main__":
    main()
