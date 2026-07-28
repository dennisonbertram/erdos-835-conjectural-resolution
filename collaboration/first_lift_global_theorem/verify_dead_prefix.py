#!/usr/bin/env python3
"""Verify an exact target-order dead-prefix certificate.

Standard library only.  The certificate is a class-B-prime support instance
at n=13, q=17, a five-colour prefix satisfying the dense-prefix numerical
criterion, a sixth support that the displayed prefix blocks, and a different
full completion of the same support instance.
"""

from __future__ import annotations

import itertools


N = 13
Q = 17
VERTICES = frozenset(range(N))
ALL_EDGES = frozenset(itertools.combinations(range(N), 2))

# S_a is represented columnwise: MISSING_BY_COLOUR[c] is the set of a for
# which c lies in S_a.  There are seven columns of size five and ten of size
# three, hence supports of sizes eight and ten.
MISSING_BY_COLOUR = (
    frozenset({6, 7, 10, 11, 12}),
    frozenset({3, 7, 8, 11, 12}),
    frozenset({3, 4, 8, 9, 12}),
    frozenset({4, 5, 8, 9, 10}),
    frozenset({5, 6, 9}),
    frozenset({8, 9, 10, 11, 12}),
    frozenset({0, 1, 2, 8, 9}),
    frozenset({0, 3, 10, 11, 12}),
    frozenset({0, 3, 10}),
    frozenset({1, 4, 11}),
    frozenset({1, 2, 3}),
    frozenset({1, 2, 4}),
    frozenset({0, 4, 5}),
    frozenset({0, 5, 6}),
    frozenset({1, 5, 7}),
    frozenset({2, 6, 7}),
    frozenset({2, 6, 7}),
)

# A class-B-prime witness.  ARRAY[a][p] is the colour of cross edge a--p.
# INTERNAL_PAIR_COLOUR colours K_5 on the p-side.
ARRAY = (
    (13, 12, 8, 7, 6),
    (6, 9, 10, 14, 11),
    (15, 16, 6, 11, 10),
    (10, 7, 2, 1, 8),
    (12, 11, 9, 2, 3),
    (14, 13, 4, 3, 12),
    (16, 4, 13, 15, 0),
    (0, 1, 14, 16, 15),
    (1, 6, 3, 5, 2),
    (2, 3, 5, 6, 4),
    (3, 0, 7, 8, 5),
    (7, 5, 0, 9, 1),
    (5, 2, 1, 0, 7),
)
INTERNAL_PAIR_COLOUR = {
    (0, 1): 8,
    (0, 2): 11,
    (0, 3): 4,
    (0, 4): 9,
    (1, 2): 15,
    (1, 3): 10,
    (1, 4): 14,
    (2, 3): 12,
    (2, 4): 16,
    (3, 4): 13,
}

# The bad greedy choice.  These are perfect matchings on supports 0,...,4.
DEAD_PREFIX = {
    0: ((0, 3), (1, 4), (2, 5), (8, 9)),
    1: ((0, 4), (1, 5), (2, 6), (9, 10)),
    2: ((0, 5), (1, 6), (2, 7), (10, 11)),
    3: ((0, 6), (1, 7), (2, 3), (11, 12)),
    4: ((0, 7), (1, 3), (2, 4), (8, 11), (10, 12)),
}

# A different choice of all seventeen matchings completes exactly the same
# supports.  This is an explicit certificate, not solver output trusted on
# faith: check_full_completion rechecks it from the definitions.
FULL_COMPLETION = {
    0: ((0, 1), (2, 3), (4, 5), (8, 9)),
    1: ((0, 5), (1, 6), (2, 4), (9, 10)),
    2: ((0, 7), (1, 2), (5, 6), (10, 11)),
    3: ((0, 2), (1, 3), (6, 11), (7, 12)),
    4: ((0, 4), (1, 10), (2, 7), (3, 12), (8, 11)),
    5: ((0, 3), (1, 4), (2, 5), (6, 7)),
    6: ((3, 6), (4, 7), (5, 10), (11, 12)),
    7: ((1, 5), (2, 6), (4, 8), (7, 9)),
    8: ((1, 7), (2, 9), (4, 6), (5, 11), (8, 12)),
    9: ((0, 6), (2, 10), (3, 8), (5, 7), (9, 12)),
    10: ((0, 12), (4, 11), (5, 9), (6, 10), (7, 8)),
    11: ((0, 10), (3, 7), (5, 12), (6, 8), (9, 11)),
    12: ((1, 8), (2, 11), (3, 9), (6, 12), (7, 10)),
    13: ((1, 9), (2, 8), (3, 4), (7, 11), (10, 12)),
    14: ((0, 8), (2, 12), (3, 11), (4, 10), (6, 9)),
    15: ((0, 9), (1, 11), (3, 5), (4, 12), (8, 10)),
    16: ((0, 11), (1, 12), (3, 10), (4, 9), (5, 8)),
}


def edge_set(edges):
    normalized = []
    for a, b in edges:
        assert 0 <= a < b < N
        normalized.append((a, b))
    assert len(normalized) == len(set(normalized))
    return frozenset(normalized)


def supports():
    return tuple(VERTICES - missing for missing in MISSING_BY_COLOUR)


def check_instance_shape():
    assert len(MISSING_BY_COLOUR) == Q
    row_missing = [
        {colour for colour, missing in enumerate(MISSING_BY_COLOUR) if a in missing}
        for a in range(N)
    ]
    assert all(len(row) == 5 for row in row_missing)
    multiplicities = [len(missing) for missing in MISSING_BY_COLOUR]
    assert multiplicities.count(5) == 7
    assert multiplicities.count(3) == 10
    assert all(value in {1, 3, 5} for value in multiplicities)
    sizes = [len(support) for support in supports()]
    assert sizes.count(8) == 7
    assert sizes.count(10) == 10
    assert sum(sizes) == N * (N - 1) == 156
    print("PASS class-B target shape: row sums 5, profile (n8,n10,n12)=(7,10,0)")
    return row_missing


def check_class_b_prime(row_missing):
    assert len(ARRAY) == N and all(len(row) == 5 for row in ARRAY)
    for a, row in enumerate(ARRAY):
        assert len(set(row)) == 5
        assert set(row) == row_missing[a]
    for p in range(5):
        column = [ARRAY[a][p] for a in range(N)]
        assert len(set(column)) == N

    p_edges = set(itertools.combinations(range(5), 2))
    assert set(INTERNAL_PAIR_COLOUR) == p_edges
    for p in range(5):
        incident = [ARRAY[a][p] for a in range(N)]
        incident.extend(
            colour
            for pair, colour in INTERNAL_PAIR_COLOUR.items()
            if p in pair
        )
        assert sorted(incident) == list(range(Q))

    # Globally, each cross edge and each internal K5 edge is assigned once.
    # Properness at A was checked by distinct array rows; properness and
    # saturation at P were checked by the preceding incident-colour census.
    print("PASS explicit proper K18-E(K13) colouring: the instance is class B-prime")


def check_matching(colour, edges, expected_support):
    used = set()
    for edge in edge_set(edges):
        for vertex in edge:
            assert vertex not in used
            used.add(vertex)
    assert used == set(expected_support), (colour, used, expected_support)


def has_perfect_matching(vertices, available_edges):
    vertices = frozenset(vertices)
    if not vertices:
        return True
    a = min(vertices)
    rest = vertices - {a}
    for b in sorted(rest):
        if tuple(sorted((a, b))) not in available_edges:
            continue
        if has_perfect_matching(rest - {b}, available_edges):
            return True
    return False


def check_dead_prefix():
    support = supports()
    sizes = [len(support[colour]) for colour in range(5)]
    assert sizes == [8, 8, 8, 8, 10]
    assert all(size >= 2 * index for index, size in enumerate(sizes, start=1))

    used = set()
    for colour in range(5):
        check_matching(colour, DEAD_PREFIX[colour], support[colour])
        matching_edges = edge_set(DEAD_PREFIX[colour])
        assert used.isdisjoint(matching_edges)
        used.update(matching_edges)

    target = support[5]
    assert target == frozenset(range(8))
    remaining = ALL_EDGES - used
    induced = frozenset(edge for edge in remaining if set(edge) <= target)
    x = frozenset({0, 1, 2})
    y = frozenset({3, 4, 5, 6, 7})
    expected = frozenset(itertools.combinations(x, 2)) | frozenset(
        itertools.combinations(y, 2)
    )
    assert induced == expected
    assert not has_perfect_matching(target, induced)
    print("PASS dense-criterion five-prefix is dead: colour 5 sees K3 disjoint-union K5")


def check_full_completion():
    support = supports()
    used = set()
    assert set(FULL_COMPLETION) == set(range(Q))
    for colour in range(Q):
        check_matching(colour, FULL_COMPLETION[colour], support[colour])
        matching_edges = edge_set(FULL_COMPLETION[colour])
        assert used.isdisjoint(matching_edges)
        used.update(matching_edges)
    assert used == set(ALL_EDGES)
    print("PASS different explicit 17-matching certificate partitions all 78 edges")


def main():
    print("Exact verifier: target-order dense-prefix non-extension")
    print("=" * 57)
    row_missing = check_instance_shape()
    check_class_b_prime(row_missing)
    check_dead_prefix()
    check_full_completion()
    print("SCOPE: counterexample to arbitrary greedy prefix extension only;")
    print("       no counterexample to class-B, class-B-prime, or fan completion.")


if __name__ == "__main__":
    main()
