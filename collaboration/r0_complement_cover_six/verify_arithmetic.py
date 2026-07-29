#!/usr/bin/env python3
"""Exact audit for NOTE.md; the mathematical proof is solver-free."""

from fractions import Fraction
from itertools import combinations
from math import comb


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def is_matching(edges):
    ends = [v for e in edges for v in e]
    return len(ends) == len(set(ends))


def is_perfect_matching(edges, vertices):
    return (
        len(edges) * 2 == len(vertices)
        and is_matching(edges)
        and set().union(*edges) == set(vertices)
    )


def all_perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield frozenset()
        return
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for matching in all_perfect_matchings(rest):
            yield matching | {edge(u, v)}


def check_counterexample():
    x = {("x", i) for i in range(7)}
    y = {("y", i) for i in range(6)}
    five_sets = []
    for i in range(7):
        five_sets.append(x - {("x", i), ("x", (i + 1) % 7)})

    triples = []
    for i in range(6):
        triples.append(
            {
                ("y", i),
                ("y", (i + 1) % 6),
                ("y", (i + 3) % 6),
            }
        )
    for digits in ((0, 1, 2), (0, 4, 5), (1, 3, 5), (2, 3, 4)):
        triples.append({("y", i) for i in digits})

    assert len({frozenset(a) for a in five_sets}) == 7
    assert len({frozenset(t) for t in triples}) == 10
    assert all(len(a) == 5 for a in five_sets)
    assert all(len(t) == 3 for t in triples)
    assert all(sum(v in a for a in five_sets) == 5 for v in x)
    assert all(sum(v in t for t in triples) == 5 for v in y)
    assert all(a <= x for a in five_sets)
    assert all(t <= y for t in triples)

    # On six vertices, disjoint triples are complementary.
    assert all(t1 & t2 for t1, t2 in combinations(triples, 2))
    universe = x | y
    assert all(
        set().union(*a_choice, *t_choice) != universe
        for a_choice in combinations(five_sets, 4)
        for t_choice in combinations(triples, 2)
    )


def check_cover_probabilities():
    probabilities = []
    for a in range(6):
        p = (
            Fraction(comb(7 - a, 3), comb(7, 3))
            * Fraction(comb(5 + a, 3), comb(10, 3))
        )
        probabilities.append(p)

    expected = [
        Fraction(1, 12),
        Fraction(2, 21),
        Fraction(1, 12),
        Fraction(4, 75),
        Fraction(1, 50),
        Fraction(0),
    ]
    assert probabilities == expected
    assert all(probabilities[a] <= Fraction(5 - a, 36) for a in range(6))
    assert Fraction(13 * 5 - 35, 36) == Fraction(5, 6)

    # Exact dynamic-programming audit of the relaxed integer maximum.
    states = {(0, 0): (Fraction(0), ())}
    for _ in range(13):
        new_states = {}
        for (count, total), (value, values) in states.items():
            for a in range(6):
                key = (count + 1, total + a)
                candidate = (value + probabilities[a], values + (a,))
                if key not in new_states or candidate[0] > new_states[key][0]:
                    new_states[key] = candidate
        states = new_states
    value, values = states[(13, 35)]
    assert value == Fraction(5, 6)
    assert values.count(2) == 10
    assert values.count(5) == 3


def odd_component_partitions(total, count, minimum):
    """Nondecreasing odd tuples with the requested sum and lower bound."""
    result = []

    def rec(prefix, remaining, last):
        if len(prefix) == count:
            if remaining == 0:
                result.append(tuple(prefix))
            return
        slots = count - len(prefix)
        for value in range(last, remaining + 1, 2):
            if value < minimum:
                continue
            if value * slots > remaining:
                break
            rec(prefix + [value], remaining - value, value)

    first = minimum if minimum % 2 else minimum + 1
    rec([], total, max(1, first))
    return result


def check_tutte_catalogue():
    feasible = []
    for q in range(10):
        component_count = q + 2
        available = 10 - q
        minimum = max(1, 5 - q)
        # Odd components may use at most the available vertices; append
        # arbitrary even-component vertices by allowing every smaller sum.
        patterns = []
        for used in range(component_count, available + 1):
            patterns.extend(
                odd_component_partitions(used, component_count, minimum)
            )
        if patterns:
            feasible.append((q, patterns))

    assert [q for q, _ in feasible] == [0, 4]
    assert feasible[0][1] == [(5, 5)]
    assert feasible[1][1] == [(1, 1, 1, 1, 1, 1)]


def check_k5_switch():
    a = [("a", i) for i in range(5)]
    b = [("b", i) for i in range(5)]
    m1 = {edge(a[i], b[i]) for i in range(5)}
    m2 = {edge(a[i], b[(i + 1) % 5]) for i in range(5)}
    assert m1.isdisjoint(m2)

    m1_new = (
        m1
        - {edge(a[0], b[0]), edge(a[1], b[1])}
        | {edge(a[0], a[1]), edge(b[0], b[1])}
    )
    m3 = {
        edge(a[0], b[0]),
        edge(a[1], a[2]),
        edge(a[3], a[4]),
        edge(b[1], b[2]),
        edge(b[3], b[4]),
    }
    vertices = set(a + b)
    assert is_perfect_matching(m1_new, vertices)
    assert is_perfect_matching(m2, vertices)
    assert is_perfect_matching(m3, vertices)
    assert m1_new.isdisjoint(m2)
    assert m1_new.isdisjoint(m3)
    assert m2.isdisjoint(m3)


def check_separator_switch():
    u = [("u", i) for i in range(6)]
    q = [("q", i) for i in range(4)]
    outside = [("o", i) for i in range(7)]
    u_matchings = list(all_perfect_matchings(u))

    # Every possible pair of disjoint U-perfect matchings has the forced
    # degree-two union.  Audit the generic switch for every such pair and
    # every choice of the freed U-edge.
    checked = 0
    for p1 in u_matchings:
        for p2 in u_matchings:
            if not p1.isdisjoint(p2):
                continue
            assert all(sum(v in e for e in p1 | p2) == 2 for v in u)
            for uv in p1:
                uu = tuple(uv)
                pq = edge(outside[0], outside[1])
                m1 = p1 | {
                    pq,
                    edge(outside[2], outside[3]),
                }
                m1_new = (
                    m1 - {uv, pq}
                    | {
                        edge(uu[0], outside[0]),
                        edge(uu[1], outside[1]),
                    }
                )
                remaining_u = [v for v in u if v not in uv]
                assert len(remaining_u) == len(q) == 4
                m3 = {uv} | {
                    edge(v, w) for v, w in zip(remaining_u, q)
                }
                assert is_perfect_matching(
                    m1_new, set(u) | set(outside[:4])
                )
                assert is_perfect_matching(m3, set(u) | set(q))
                assert m1_new.isdisjoint(p2)
                assert m1_new.isdisjoint(m3)
                assert p2.isdisjoint(m3)
                checked += 1
    assert checked > 0


def main():
    check_counterexample()
    check_cover_probabilities()
    check_tutte_catalogue()
    check_k5_switch()
    check_separator_switch()
    print("r=0 complement-cover six-prefix audit: PASS")


if __name__ == "__main__":
    main()
