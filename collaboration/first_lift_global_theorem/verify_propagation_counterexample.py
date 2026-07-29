#!/usr/bin/env python3
"""Verify the exact locally maximal 15-prefix propagation counterexample."""

from itertools import combinations


N = 13
U = frozenset(range(8))
H = {
    (0, 1),
    (0, 2),
    (1, 2),
    (3, 4),
    (3, 7),
    (4, 5),
    (5, 6),
    (6, 7),
}

PREFIX = (
    ((1, 10), (4, 6), (7, 8), (9, 11)),
    ((0, 11), (5, 7), (6, 8), (9, 12)),
    ((1, 12), (2, 9), (4, 7), (5, 8)),
    ((3, 8), (5, 9), (6, 10), (7, 11)),
    ((2, 4), (5, 12), (7, 10), (8, 9)),
    ((0, 6), (2, 5), (3, 12), (7, 9), (8, 10)),
    ((0, 10), (2, 8), (3, 5), (4, 11), (6, 12)),
    ((0, 12), (1, 7), (3, 11), (4, 10), (6, 9)),
    ((0, 8), (1, 9), (2, 6), (3, 10), (5, 11)),
    ((0, 5), (1, 4), (2, 11), (3, 6), (10, 12)),
    ((0, 7), (1, 8), (2, 10), (3, 9), (11, 12)),
    ((0, 9), (1, 5), (2, 7), (4, 12), (10, 11)),
    ((0, 4), (1, 11), (2, 3), (8, 12), (9, 10)),
    ((1, 3), (2, 12), (4, 8), (5, 10), (6, 11)),
    ((0, 3), (1, 6), (4, 9), (7, 12), (8, 11)),
)


def support(matching: tuple[tuple[int, int], ...]) -> frozenset[int]:
    return frozenset(vertex for edge in matching for vertex in edge)


def main() -> None:
    complete = set(combinations(range(N), 2))
    used: set[tuple[int, int]] = set()
    prefix_supports = []

    for colour, matching in enumerate(PREFIX):
        normalized = {tuple(sorted(edge)) for edge in matching}
        assert len(normalized) == len(matching)
        assert all(0 <= u < v < N for u, v in normalized)
        assert len(support(matching)) == 2 * len(matching)
        assert used.isdisjoint(normalized), f"colour {colour} repeats an edge"
        used.update(normalized)
        prefix_supports.append(support(matching))

    assert used == complete - H
    assert [len(s) for s in prefix_supports].count(8) == 5
    assert [len(s) for s in prefix_supports].count(10) == 10

    all_supports = prefix_supports + [U, U]
    assert [len(s) for s in all_supports].count(8) == 7
    assert [len(s) for s in all_supports].count(10) == 10
    assert all(sum(v in s for s in all_supports) == 12 for v in range(N))

    residual_degrees = {
        v: sum(v in edge for edge in H)
        for v in range(N)
    }
    remaining_counts = {
        v: sum(v in s for s in (U, U))
        for v in range(N)
    }
    assert residual_degrees == remaining_counts

    components = ({0, 1, 2}, {3, 4, 5, 6, 7})
    assert all(len(component) % 2 == 1 for component in components)
    assert H == {
        edge
        for component in components
        for edge in combinations(sorted(component), 2)
        if edge in H
    }
    # There are no edges between the two odd components, so no perfect
    # matching of either remaining support U exists.
    assert not any(
        u in components[0] and v in components[1]
        for u, v in H
    )

    print("PASS prefix: five size-8 and ten size-10 matchings partition K13-H")
    print("PASS class-B profile: (n8,n10,n12)=(7,10,0), every row sum is 12")
    print("PASS residual identity: d_H(v) equals remaining-support incidence")
    print("PASS obstruction: both remaining supports induce C3 disjoint-union C5")
    print("SCOPE: invariant-only propagation fails; full completion is unresolved")


if __name__ == "__main__":
    main()
