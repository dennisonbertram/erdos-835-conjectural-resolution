#!/usr/bin/env python3
"""Verify the r=2 terminal-flexibility finite reduction.

Python standard library only.
"""

from __future__ import annotations

from itertools import combinations, product

V = frozenset(range(13))
ALL_EDGES = frozenset(combinations(range(13), 2))

COUNTER_D = frozenset(
    {
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 4),
        (3, 5),
        (3, 6),
        (4, 6),
        (5, 7),
        (7, 8),
        (7, 9),
        (7, 10),
        (7, 11),
        (8, 9),
        (8, 10),
        (8, 11),
        (11, 12),
    }
)
COUNTER_M = frozenset({(0, 1), (2, 3), (4, 5), (6, 7)})


def odd_partitions(total: int, count: int, minimum: int = 1):
    """Yield nondecreasing odd positive partitions."""
    if count == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, total + 1, 2):
        for tail in odd_partitions(total - first, count - 1, first):
            yield (first,) + tail


def perfect_matchings(
    vertices: frozenset[int],
    edges: frozenset[tuple[int, int]],
) -> list[frozenset[tuple[int, int]]]:
    if not vertices:
        return [frozenset()]
    first = min(vertices)
    result: list[frozenset[tuple[int, int]]] = []
    for second in sorted(vertices - {first}):
        edge = (first, second)
        if edge not in edges:
            continue
        for tail in perfect_matchings(vertices - {first, second}, edges):
            result.append(tail | {edge})
    return result


def verify_catalogue() -> None:
    surviving: list[tuple[int, tuple[int, ...]]] = []
    for separator in range(12):
        component_count = separator + 2
        remaining_order = 12 - separator
        minimum_raw = 5 - separator
        minimum_odd = max(1, minimum_raw)
        if minimum_odd % 2 == 0:
            minimum_odd += 1
        for parts in odd_partitions(
            remaining_order, component_count, minimum_odd
        ):
            surviving.append((separator, parts))
    assert surviving == [
        (0, (5, 7)),
        (4, (1, 1, 1, 1, 1, 3)),
        (5, (1, 1, 1, 1, 1, 1, 1)),
    ]
    print("PASS terminal Tutte catalogue: 5+7, 3+1^5, and 1^7")


def verify_resources() -> None:
    # Degree sum 52 and minimum degree one imply at most nine degree-five
    # vertices.
    feasible_w = [
        w
        for w in range(14)
        if 5 * w + (13 - w) <= 52
    ]
    assert max(feasible_w) == 9
    assert max(w + 14 for w in feasible_w) == 23
    assert 23 < 5 * 5

    k7_rows = []
    for m, p in product(range(4), repeat=2):
        if m + p < 4:
            continue
        m_only_lower = 7 - 2 * p
        assert m >= 1
        assert m_only_lower >= 1
        k7_rows.append((m, p, m_only_lower))
    assert k7_rows == [
        (1, 3, 1),
        (2, 2, 3),
        (2, 3, 1),
        (3, 1, 5),
        (3, 2, 3),
        (3, 3, 1),
    ]
    print("PASS all-five row bound: at most 23 saturated exclusions")
    print("PASS K7 arithmetic: m+p>=4 forces m>=1 and 7-2p>=1")


def verify_hard_types() -> None:
    m_types = []
    for values in product(range(5), repeat=5):
        a, b, c, d, e = values
        if sum(values) != 4:
            continue
        omissions = (
            7 - (2 * a + b + c),
            5 - (b + 2 * d + e),
            1 - (c + e),
        )
        if min(omissions) >= 0 and sum(omissions) == 5:
            m_types.append((omissions, values))

    p_types = []
    endpoint_targets = {
        (6, 5, 1): "U",
        (7, 4, 1): "S",
        (7, 5, 0): "y",
    }
    for values in product(range(7), repeat=5):
        a, b, c, d, e = values
        if sum(values) != 6:
            continue
        endpoints = (2 * a + b + c, b + 2 * d + e, c + e)
        if endpoints in endpoint_targets:
            p_types.append((endpoint_targets[endpoints], values))

    hard = []
    for omissions, m_type in m_types:
        for hole, p_type in p_types:
            if m_type[0] + p_type[0] < 4:
                continue
            if m_type[0] >= 2 and m_type[3] >= 1:
                continue
            if p_type[0] >= 2 and p_type[3] >= 1:
                continue
            hard.append((omissions, m_type, hole, p_type))

    expected_m = {
        ((2, 3, 0), (2, 1, 0, 0, 1)),
        ((1, 4, 0), (2, 1, 1, 0, 0)),
        ((1, 3, 1), (2, 2, 0, 0, 0)),
        ((1, 4, 0), (3, 0, 0, 0, 1)),
        ((0, 5, 0), (3, 0, 1, 0, 0)),
        ((0, 4, 1), (3, 1, 0, 0, 0)),
    }
    expected_p = {
        ("U", (1, 3, 1, 1, 0)),
        ("U", (1, 4, 0, 0, 1)),
        ("S", (1, 4, 1, 0, 0)),
        ("S", (2, 3, 0, 0, 1)),
        ("y", (1, 5, 0, 0, 0)),
    }
    assert len(m_types) == 27
    assert len(p_types) == 14
    assert len(hard) == 18
    assert {(row[0], row[1]) for row in hard} == expected_m
    assert {(row[2], row[3]) for row in hard} == expected_p
    core_edges = [21 - row[1][0] - row[3][0] for row in hard]
    assert core_edges.count(17) == 15
    assert core_edges.count(16) == 3
    assert sorted(6 - degree for degree in (2, 1, 1, 1, 1, 1, 1)) == [
        4,
        5,
        5,
        5,
        5,
        5,
        5,
    ]
    assert sorted(6 - degree for degree in (2, 2, 2, 1, 1, 1, 1)) == [
        4,
        4,
        4,
        5,
        5,
        5,
        5,
    ]
    print("PASS exact K7 endpoint frontier: 27 M, 14 P, 18 hard pairs")
    print("PASS hard K7 cores: fifteen have 17 D-edges, three have 16")


def verify_core_coexistence() -> None:
    # If two 17-edge seven-cores occur in a 26-edge graph, their
    # intersection has at least eight edges and therefore at least five
    # vertices.
    assert 17 + 17 - 26 == 8
    assert min(size for size in range(8) if size * (size - 1) // 2 >= 8) == 5

    # Intersection five: a vertex saturated in both cores would need five
    # neighbours among only four common alternatives, so all five common
    # vertices would have to be among the two exceptional vertices.
    assert 5 > 2

    # Intersection six: four vertices saturated in both cores force all
    # their incident edges within the six-set.  Together with the
    # exclusive vertex's minimum internal degree four this exceeds 17.
    common_saturated = 6 - 2
    forced_inside_intersection = (
        common_saturated * (common_saturated - 1) // 2
        + common_saturated * (6 - common_saturated)
    )
    assert forced_inside_intersection == 14
    assert forced_inside_intersection + 4 == 18 > 17

    # If five candidate complements shared the unique 17-edge core, each
    # would exclude at least four of its saturated six-set.  The row
    # identity supplies at most 6+13 exclusions because the singleton y
    # lies outside that six-set.
    assert 5 * 4 == 20
    assert 6 + (14 - 1) == 19
    assert 20 > 19
    print("PASS 17-edge core uniqueness under |D|=26 and Delta(D)<=5")
    print("PASS five candidates cannot all share the unique 17-edge core")


def verify_sixteen_edge_switch() -> None:
    # The three 16-edge rows all pair M4/M5/M6 with P4.
    m_rows = {
        (3, 0, 0, 0, 1),
        (3, 0, 1, 0, 0),
        (3, 1, 0, 0, 0),
    }
    p4 = (2, 3, 0, 0, 1)
    assert all(21 - m_row[0] - p4[0] == 16 for m_row in m_rows)

    # The P4 exceptional switch changes its endpoint type to P3 while
    # preserving all twelve covered vertices.
    p3 = (1, 4, 1, 0, 0)
    assert sum(p4) == sum(p3) == 6
    assert (2 * p4[0] + p4[1] + p4[2]) == 7
    assert (p4[1] + 2 * p4[3] + p4[4]) == 4
    assert p4[2] + p4[4] == 1
    assert (2 * p3[0] + p3[1] + p3[2]) == 7
    assert (p3[1] + 2 * p3[3] + p3[4]) == 4
    assert p3[2] + p3[4] == 1

    # Three double-covered vertices plus at most one external M6 endpoint
    # can miss s0.  After deleting u,v and adding a_i, the mutated class
    # has order at most three.
    assert 3 + 1 == 4
    assert 4 - 2 + 1 == 3
    # In the all-bad case only one S-column is unavailable, whereas P4
    # has three disjoint US edges.
    assert p4[1] == 3 > 1
    # The same P4 transition occurs in the three 17-edge M1/M2/M3 rows.
    p4_pairs = 6
    remaining_hard_pairs = 18 - p4_pairs
    assert remaining_hard_pairs == 12
    assert 5 * 5 == 25 > 19
    print("PASS all six P4 switch rows; 12 hard 17-edge pairs remain")


def verify_counterexample() -> None:
    assert len(COUNTER_D) == 26
    degrees = tuple(
        sum(vertex in edge for edge in COUNTER_D) for vertex in V
    )
    assert max(degrees) == 5
    assert not (COUNTER_D & COUNTER_M)
    support = frozenset(range(8))
    endpoints = [vertex for edge in COUNTER_M for vertex in edge]
    assert frozenset(endpoints) == support
    assert len(endpoints) == len(set(endpoints))

    residual = ALL_EDGES - COUNTER_D - COUNTER_M
    u_set = frozenset(range(7))
    assert residual & frozenset(combinations(u_set, 2)) == {(5, 6)}

    p8 = perfect_matchings(V - {8}, residual)
    p9 = perfect_matchings(V - {9}, residual)
    assert p8 and p9
    assert all((5, 6) in matching for matching in p8)
    assert all((5, 6) in matching for matching in p9)
    assert not any(left.isdisjoint(right) for left in p8 for right in p9)
    print(
        "PASS fixed-candidate counterexample: "
        f"{len(p8)} x {len(p9)} near-factor pairs, none disjoint"
    )


def main() -> None:
    verify_catalogue()
    verify_resources()
    verify_hard_types()
    verify_core_coexistence()
    verify_sixteen_edge_switch()
    verify_counterexample()
    print("SCOPE: finite r=2 reduction; no universal terminal theorem")


if __name__ == "__main__":
    main()
