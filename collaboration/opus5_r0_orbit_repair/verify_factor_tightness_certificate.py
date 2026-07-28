#!/usr/bin/env python3
"""Verify Opus 5's full-row factor tightness certificate.

The certificate is not a counterexample to cut sufficiency: it violates one
six-set cut by one edge.  It demonstrates that the six-set part of the cut
family is load-bearing even after all class-B row equations are imposed.
"""

from __future__ import annotations

from itertools import combinations


VERTICES = frozenset(range(1, 14))
EDGES = frozenset(combinations(sorted(VERTICES), 2))
PREFIX = (
    ((6, 11), (7, 10), (8, 13), (1, 2), (3, 4)),
    ((7, 11), (6, 8), (9, 10), (1, 12), (4, 13)),
    ((8, 11), (7, 9), (6, 10), (2, 12), (1, 5)),
    ((9, 11), (8, 10), (6, 12), (3, 13)),
    ((10, 11), (6, 9), (7, 8), (12, 13)),
    ((7, 12), (9, 13), (2, 3), (4, 5)),
)
TRIPLES = (
    (1, 2, 5),
    (1, 3, 4),
    (2, 3, 4),
    (6, 10, 11),
    (7, 12, 13),
    (8, 10, 12),
    (9, 11, 13),
)
FIVE_SETS = (
    (6, 7, 8, 10, 11),
    (6, 7, 9, 12, 13),
    (6, 8, 9, 10, 12),
    (7, 8, 9, 11, 13),
)
SELECTED = TRIPLES[:3]


def main() -> None:
    assert sorted(map(len, PREFIX)) == [4, 4, 4, 5, 5, 5]
    for layer in PREFIX:
        endpoints = [vertex for edge in layer for vertex in edge]
        assert len(endpoints) == len(set(endpoints)) == 2 * len(layer)
    deleted = frozenset(edge for layer in PREFIX for edge in layer)
    assert len(deleted) == sum(map(len, PREFIX)) == 27

    degrees = {
        vertex: sum(vertex in edge for edge in deleted) for vertex in VERTICES
    }
    assert tuple(degrees[vertex] for vertex in sorted(VERTICES)) == (
        3,
        3,
        3,
        3,
        2,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
    )
    rows = TRIPLES + FIVE_SETS
    rho = {
        vertex: sum(vertex in row for row in rows) for vertex in VERTICES
    }
    assert all(rho[vertex] == degrees[vertex] - 1 for vertex in VERTICES)
    assert sum(rho.values()) == 41

    available = EDGES - deleted
    supports = tuple(VERTICES - frozenset(row) for row in SELECTED)
    violations = []
    for size in range(14):
        for subset_tuple in combinations(sorted(VERTICES), size):
            subset = frozenset(subset_tuple)
            required = sum(max(0, len(support & subset) - 5) for support in supports)
            internal = sum(set(edge) <= subset for edge in available)
            if required > internal:
                violations.append((subset, required, internal))
    target = frozenset(range(6, 12))
    assert violations == [(target, 3, 2)]

    # The degree requirement of the union of three selected matchings.
    b = {
        vertex: 3 - sum(vertex in row for row in SELECTED)
        for vertex in VERTICES
    }
    outside = VERTICES - target
    assert sum(b[vertex] for vertex in target) == 18
    assert sum(b[vertex] for vertex in outside) == 12
    assert sum(set(edge) <= target for edge in available) == 2
    assert 18 > 12 + 2 * 2

    # One displayed individual perfect matching for the first support.
    individual = ((3, 6), (4, 7), (8, 9), (10, 12), (11, 13))
    assert not set(individual) & deleted
    assert frozenset(vertex for edge in individual for vertex in edge) == supports[0]

    print("PASS: prefix layers are disjoint matchings of sizes 4,4,4,5,5,5")
    print("PASS: all eleven rows satisfy rho(v)=d_D(v)-1")
    print("PASS: exactly one of 2^13 cuts fails, by 3>2 on {6,...,11}")
    print("PASS: the same cut rules out the required degree-constrained union")
    print("PASS: the first selected support is individually matchable")


if __name__ == "__main__":
    main()
