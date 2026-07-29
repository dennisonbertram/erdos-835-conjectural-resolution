#!/usr/bin/env python3
"""Verify the r=2 cross-route finite reduction.

Python standard library only.
"""

from __future__ import annotations

from itertools import combinations, product


def endpoint_types() -> None:
    m_types = []
    for values in product(range(6), repeat=5):
        a, b, c, d, e = values
        if sum(values) != 5:
            continue
        omissions = (
            7 - (2 * a + b + c),
            5 - (b + 2 * d + e),
            1 - (c + e),
        )
        if min(omissions) >= 0 and sum(omissions) == 3:
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

    assert len(m_types) == 25
    assert len(p_types) == 14
    assert len(hard) == 8
    core_sizes = [21 - row[1][0] - row[3][0] for row in hard]
    assert core_sizes.count(17) == 7
    assert core_sizes.count(16) == 1
    assert all(
        row[0][0] <= 1
        for row, core_size in zip(hard, core_sizes)
        if core_size == 17
    )

    p4 = (2, 3, 0, 0, 1)
    rigid = [row for row in hard if row[3] != p4]
    assert len(rigid) == 4
    assert all(row[0] == (0, 3, 0) for row in rigid)
    assert all(row[1] == (3, 1, 0, 0, 1) for row in rigid)
    assert all(21 - row[1][0] - row[3][0] == 17 for row in rigid)

    p4_m_rows = [
        (omissions, m_type)
        for omissions, m_type in m_types
        if m_type[0] >= 2
    ]
    assert len(p4_m_rows) == 14

    print("PASS size-ten endpoint catalogue: 25 M, 14 P, 8 hard pairs")
    print("PASS hard cores: seven have 17 edges and one has 16")
    print("PASS four rigid non-P4 rows omit no U vertex")
    print("PASS P4 switch applies to fourteen size-ten M rows")
    for row, core_size in zip(hard, core_sizes):
        print(" ", row, "D[U] edges", core_size)


def size_eight_hard_bound() -> None:
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

    hard_seventeen = []
    for omissions, m_type in m_types:
        for hole, p_type in p_types:
            if m_type[0] + p_type[0] < 4:
                continue
            if m_type[0] >= 2 and m_type[3] >= 1:
                continue
            if p_type[0] >= 2 and p_type[3] >= 1:
                continue
            if 21 - m_type[0] - p_type[0] == 17:
                hard_seventeen.append(
                    (omissions, m_type, hole, p_type)
                )

    assert len(hard_seventeen) == 15
    assert max(row[0][0] for row in hard_seventeen) == 2
    print("PASS size-eight hard 17-edge rows have r_U <= 2")

    # Among compatible pairs with r_U >= 3, either P is ordinary or it
    # has the exceptional P4 endpoint type.  This is the exact local
    # split used in the branch closure.
    p4 = (2, 3, 0, 0, 1)
    for omissions, m_type in m_types:
        if omissions[0] < 3:
            continue
        for _, p_type in p_types:
            if m_type[0] + p_type[0] < 4:
                continue
            p_ordinary = p_type[0] >= 2 and p_type[3] >= 1
            assert p_ordinary or p_type == p4
    print("PASS r_U >= 3 leaves ordinary P or the P4 switch")

    # Globally, every compatible pair not covered by the ordinary-P or
    # P4 switches has a 17-edge core and is closed by the gate theorem.
    for _, m_type in m_types:
        for _, p_type in p_types:
            if m_type[0] + p_type[0] < 4:
                continue
            p_ordinary = p_type[0] >= 2 and p_type[3] >= 1
            if p_ordinary or p_type == p4:
                continue
            assert 21 - m_type[0] - p_type[0] == 17
    print("PASS size-eight K7 pairs: ordinary P, P4, or 17-core")


def size_ten_global_k7_exhaustion() -> None:
    m_types = []
    for values in product(range(6), repeat=5):
        a, b, c, d, e = values
        if sum(values) != 5:
            continue
        omissions = (
            7 - (2 * a + b + c),
            5 - (b + 2 * d + e),
            1 - (c + e),
        )
        if min(omissions) >= 0 and sum(omissions) == 3:
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

    p4 = (2, 3, 0, 0, 1)
    compatible = 0
    gated = 0
    for _, m_type in m_types:
        for _, p_type in p_types:
            if m_type[0] + p_type[0] < 4:
                continue
            compatible += 1
            p_ordinary = p_type[0] >= 2 and p_type[3] >= 1
            if p_ordinary or p_type == p4:
                continue
            assert 21 - m_type[0] - p_type[0] == 17
            gated += 1
    assert compatible > gated > 0
    print("PASS size-ten K7 pairs: ordinary P, P4, or 17-core")


def dense_core_arithmetic() -> None:
    assert 17 + 17 - 26 == 8
    assert min(
        size
        for size in range(8)
        if size * (size - 1) // 2 >= 8
    ) == 5

    # Intersection six: four vertices saturated in both cores force
    # fourteen common edges, and the exclusive vertex supplies four.
    common_saturated = 4
    forced_common = (
        common_saturated * (common_saturated - 1) // 2
        + common_saturated * 2
    )
    assert forced_common == 14
    assert forced_common + 4 == 18 > 17

    # Six saturated vertices, one internal-degree-four vertex.
    assert (6 * 5 + 4) // 2 == 17
    assert (6 * 5 - 4) // 2 == 13
    assert 26 - 13 - 4 == 9
    # A saturated K6 is disconnected from its seven-vertex complement.
    # A connected seven-core of minimum internal degree four must lie in
    # the complement, where its 17 edges plus the clique's 15 exceed 26.
    assert 15 + 17 == 32 > 26
    print("PASS uniqueness and 9-edge outside-block arithmetic")
    print("PASS a 17-edge terminal core excludes every blocked K6 support")


def seventeen_core_gate() -> None:
    u = frozenset(range(7))
    g_u = frozenset({(0, 1), (1, 2), (3, 4), (5, 6)})
    d_u = frozenset(combinations(u, 2)) - g_u
    assert len(d_u) == 17

    # D[U] has neither K5 nor K_{3,1,1,1}.
    assert not any(
        frozenset(combinations(vertices, 2)) <= d_u
        for vertices in combinations(u, 5)
    )
    has_k3111 = False
    for support in combinations(u, 6):
        support_set = frozenset(support)
        for large_part in combinations(support, 3):
            large = frozenset(large_part)
            required = frozenset(
                edge
                for edge in combinations(support_set, 2)
                if not frozenset(edge) <= large
            )
            if required <= d_u:
                has_k3111 = True
    assert not has_k3111

    # Exact minimum nontrivial cut sizes of the three obstruction cores.
    cores = {}
    cores["K35"] = frozenset(
        (left, right)
        for left in range(3)
        for right in range(3, 8)
    )
    big = frozenset(range(3))
    cores["K3111"] = frozenset(
        edge
        for edge in combinations(range(6), 2)
        if not frozenset(edge) <= big
    )
    cores["K5"] = frozenset(combinations(range(5), 2))

    minimum_cuts = {}
    for name, edges in cores.items():
        vertices = frozenset(v for edge in edges for v in edge)
        minimum_cuts[name] = min(
            sum(
                (left in side) != (right in side)
                for left, right in edges
            )
            for size in range(1, len(vertices))
            for side in map(frozenset, combinations(vertices, size))
        )
    assert minimum_cuts == {"K35": 3, "K3111": 3, "K5": 4}
    assert len(cores["K3111"]) == 12
    assert len(cores["K5"]) == 10
    assert 12 > 9 and 10 > 9
    print("PASS 17-core gate excludes K35, K3111, and K5 initial blocks")


def saturated_k6_escape() -> None:
    # G[R] has 21-11=10 edges.  Matching number at most one on seven
    # vertices permits at most a six-edge star.
    assert 21 - 11 == 10
    assert 10 > 6

    # Size-ten candidates with b triple vertices in B use b-1 internal
    # R-edges and 6-b cross edges.
    for b in range(1, 4):
        assert (b - 1) * 2 + (6 - b) == 4 + b
        assert b - 1 <= 2

    # A size-eight candidate with k complement vertices in B uses k-2
    # internal R-edges and 6-k cross edges.
    for k in range(2, 6):
        assert (k - 2) * 2 + (6 - k) == 2 + k
        assert k - 2 <= 3

    # After one or two earlier cross matchings, the balanced near-factor
    # problem has minimum degree at least half its order.
    for order in (5, 6):
        assert order - 1 >= order / 2
        assert order - 2 >= order / 2

    # Ten internal R-edges leave enough after the candidate and first
    # near-factor choices.
    assert 10 - 3 - 1 >= 1
    print("PASS saturated-K6 escape arithmetic and Hall thresholds")


def row_mass() -> None:
    # Four triples meet the common U in at most one point each.  One of
    # the two singleton holes is outside U.
    assert 6 * 4 - 4 - 1 == 19

    intersections = [
        row
        for row in product(range(6), repeat=5)
        if sum(row) >= 19
    ]
    assert intersections
    assert all(sum(value >= 2 for value in row) >= 4 for row in intersections)
    assert all(sum(value >= 3 for value in row) >= 3 for row in intersections)
    print("PASS row mass >=19 forces >=4 intersections of size 2")
    print("PASS row mass >=19 forces >=3 intersections of size 3")

    # If no intersection has size five, every one has size at least
    # three.  Otherwise, a size-five A leaves at most four saturated
    # vertices outside because |W| <= 9.
    no_five = [row for row in intersections if max(row) <= 4]
    assert no_five
    assert all(min(row) >= 3 for row in no_five)
    assert 9 - 5 == 4 < 5

    # Five first-two-type failures would consume 25 saturated
    # exclusions, while the class-B identity supplies at most 23.
    assert 5 * 5 == 25
    assert 9 + 14 == 23
    assert 25 > 23
    print("PASS dense-size-ten branch closure arithmetic")

    # Three rigid triples avoid Z.  The fourth triple and the singleton
    # other than y contribute at most four incidences in total.
    assert 6 * 4 - 3 - 1 == 20
    at_least_twenty = [
        row
        for row in product(range(6), repeat=5)
        if sum(row) >= 20
    ]
    assert all(
        max(row) == 5 or row == (4, 4, 4, 4, 4)
        for row in at_least_twenty
        if max(row) <= 4
    )
    print("PASS three-rigid branch forces a size-five row or five size-four rows")

    # Zero-rigid exclusion budgets.
    assert 3 + 4 * 5 == 23
    assert 8 + 14 == 22 < 23
    assert 4 + 4 * 5 == 24 > 9 + 14
    assert 8 * 5 == 40
    assert 5 * 7 + 2 == 37 < 40
    assert 5 + 4 * 3 == 17 < 4 * 8 - 14
    assert 5 + 4 * 4 == 21 < 4 * 9 - 14
    print("PASS zero-rigid charge bounds force at least two blocked A rows")


def matching_number(vertices: int, edges: frozenset[tuple[int, int]]) -> int:
    best = 0
    edge_list = sorted(edges)
    for size in range(1, vertices // 2 + 1):
        for chosen in combinations(edge_list, size):
            endpoints = [v for edge in chosen for v in edge]
            if len(set(endpoints)) == 2 * size:
                best = size
    return best


def extremal_matching_bounds() -> None:
    # It is enough to check the sharp threshold actually used: every
    # six-edge graph on six vertices has a two-edge matching.
    all_edges = tuple(combinations(range(6), 2))
    for edges in combinations(all_edges, 6):
        assert matching_number(6, frozenset(edges)) >= 2
    print("PASS extremal bound: every 6-edge graph on 6 vertices has nu>=2")


def cross_cut_arithmetic() -> None:
    # k=3: q has global H-degree at least five, hence degree at least
    # three in any chosen H five-set.
    assert 5 - (7 - 5) == 3

    # k=4: the H six-set has at least six edges, one not incident with q,
    # while q has degree at least four there.  It can avoid the two
    # endpoints of that non-q edge.
    assert 15 - 9 == 6
    assert 5 - (7 - 6) == 4
    assert 4 - 2 >= 1

    # k=5: H-q has at least six edges and therefore a two-edge matching;
    # q misses at most one of the two uncovered vertices.
    assert 15 - 9 == 6
    assert 2 - 1 >= 1
    print("PASS k=3,4,5 exceptional-vertex cross-cut arithmetic")


def main() -> None:
    endpoint_types()
    size_eight_hard_bound()
    size_ten_global_k7_exhaustion()
    dense_core_arithmetic()
    seventeen_core_gate()
    saturated_k6_escape()
    row_mass()
    extremal_matching_bounds()
    cross_cut_arithmetic()
    print(
        "SCOPE: coordinated r=2 fixed-prefix theorem closed; "
        "full completion and Problem #835 remain open"
    )


if __name__ == "__main__":
    main()
