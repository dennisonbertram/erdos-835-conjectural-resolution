#!/usr/bin/env python3
"""Verify the full completion of the dead-prefix support instance."""

from itertools import combinations


C = tuple(f"c{i}" for i in range(6))
OUTSIDE = tuple(f"o{i}" for i in range(7))
V = frozenset(C + OUTSIDE)


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def matching(pairs):
    return frozenset(edge(u, v) for u, v in pairs)


def support(edges):
    return frozenset().union(*edges)


def is_matching(edges):
    ends = [v for e in edges for v in e]
    return len(ends) == len(set(ends))


def main():
    selected_complements = (
        frozenset(("o2", "o4", "o6")),
        frozenset(("o1", "o3", "o5")),
        frozenset(("o1", "o2", "o4")),
        frozenset(("c0", "c2", "o1", "o2", "o3")),
        frozenset(("c3", "c4", "o0", "o1", "o2")),
        frozenset(("c1", "c5", "o0", "o1", "o2")),
    )
    remaining_fives = tuple(
        frozenset(C) - {f"c{i}"} for i in range(4)
    )
    blocked_triples = tuple(
        frozenset(f"o{i}" for i in digits)
        for digits in ((0, 5, 6), (3, 4, 5), (3, 4, 6), (3, 5, 6), (4, 5, 6))
    )
    good_triples = (
        frozenset(("c0", "c1", "o0")),
        frozenset(("c2", "c3", "o0")),
    )
    complements = (
        selected_complements
        + remaining_fives
        + blocked_triples
        + good_triples
    )
    assert len(complements) == 17
    assert all(sum(v in a for a in complements) == 5 for v in V)

    rows = (
        (("c0", "c2"), ("c1", "c5"), ("c3", "o0"), ("c4", "o3"), ("o1", "o5")),
        (("c0", "c4"), ("c1", "c3"), ("c2", "o6"), ("c5", "o4"), ("o0", "o2")),
        (("c0", "c1"), ("c2", "c3"), ("c4", "o6"), ("c5", "o0"), ("o3", "o5")),
        (("c1", "o6"), ("c3", "c4"), ("c5", "o5"), ("o0", "o4")),
        (("c0", "c5"), ("c1", "c2"), ("o3", "o4"), ("o5", "o6")),
        (("c0", "c3"), ("c2", "o3"), ("c4", "o5"), ("o4", "o6")),
        (("c0", "o5"), ("o0", "o1"), ("o2", "o4"), ("o3", "o6")),
        (("c1", "o4"), ("o0", "o5"), ("o1", "o3"), ("o2", "o6")),
        (("c2", "o4"), ("o0", "o3"), ("o1", "o6"), ("o2", "o5")),
        (("c3", "o5"), ("o0", "o6"), ("o1", "o4"), ("o2", "o3")),
        (("c0", "o4"), ("c1", "o3"), ("c2", "c4"), ("c3", "o1"), ("c5", "o2")),
        (("c0", "o6"), ("c1", "c4"), ("c2", "o0"), ("c3", "o2"), ("c5", "o1")),
        (("c0", "o2"), ("c1", "o0"), ("c2", "o5"), ("c3", "c5"), ("c4", "o1")),
        (("c0", "o1"), ("c1", "o2"), ("c2", "c5"), ("c3", "o4"), ("c4", "o0")),
        (("c0", "o0"), ("c1", "o1"), ("c2", "o2"), ("c3", "o3"), ("c4", "c5")),
        (("c2", "o1"), ("c3", "o6"), ("c4", "o2"), ("c5", "o3"), ("o4", "o5")),
        (("c0", "o3"), ("c1", "o5"), ("c4", "o4"), ("c5", "o6"), ("o1", "o2")),
    )
    matchings = tuple(matching(row) for row in rows)
    assert all(is_matching(row) for row in matchings)
    assert all(
        support(row) == V - complement
        for row, complement in zip(matchings, complements)
    )
    assert all(
        matchings[i].isdisjoint(matchings[j])
        for i, j in combinations(range(17), 2)
    )

    all_edges = frozenset(edge(u, v) for u, v in combinations(V, 2))
    used_edges = frozenset().union(*matchings)
    assert len(used_edges) == 78
    assert used_edges == all_edges

    print("full completion of dead-prefix support instance: PASS")


if __name__ == "__main__":
    main()
