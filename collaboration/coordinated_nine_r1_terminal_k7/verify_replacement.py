#!/usr/bin/env python3
"""Audit the no-WW replacement-triple repair at the r=1 K7 terminal."""

from functools import lru_cache
from itertools import combinations, permutations


U = tuple(range(7))
W = tuple(range(7, 13))
S = tuple(range(7, 12))
HUB = 0

P0 = frozenset(((0, 1), (2, 3)))
P1 = frozenset(((0, 4), (5, 6)))
M0_CROSS_LEFT = (4, 5, 6)
N_CROSS_LEFT = (1, 2, 3, 5, 6)
N_CORE_EDGE = (0, 4)

CROSS_INDEX = {
    (u, w): index
    for index, (u, w) in enumerate((u, w) for u in U for w in W)
}


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield frozenset()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:index] + vertices[index + 1 :]
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(rest):
            yield frozenset((edge, *tail))


def cross_mask(edges):
    mask = 0
    for edge in edges:
        mask |= 1 << CROSS_INDEX[edge]
    return mask


@lru_cache(maxsize=None)
def bijection_masks(left, right, forbidden):
    """All bijective cross matchings, encoded as 42-bit masks."""
    left = tuple(left)
    right = tuple(right)
    forbidden_edge = None if forbidden == (-1, -1) else forbidden
    masks = []
    for image in permutations(right):
        edges = tuple(zip(left, image))
        if forbidden_edge is not None and forbidden_edge in edges:
            continue
        masks.append(cross_mask(edges))
    return tuple(masks)


def masks(left, right, forbidden):
    marker = (-1, -1) if forbidden is None else forbidden
    return bijection_masks(tuple(left), tuple(right), marker)


def base_unions(triple0):
    """Cross-edge unions available for the retained matching and N."""
    side0 = tuple(sorted(set(W) - set(triple0)))
    m0_masks = masks(M0_CROSS_LEFT, side0, None)
    n_masks = masks(N_CROSS_LEFT, S, None)
    unions = {
        m0_mask | n_mask
        for m0_mask in m0_masks
        for n_mask in n_masks
        if not (m0_mask & n_mask)
    }
    assert unions
    return tuple(unions)


def has_coordination(unions, replacement_masks):
    return any(
        not (base_mask & replacement_mask)
        for replacement_mask in replacement_masks
        for base_mask in unions
    )


def verify_terminal_equalities():
    # With no WW edge, a_i = 2-r_i.  Covering all seven core vertices
    # forces r_0+r_1=0.
    feasible = []
    for r0 in range(3):
        for r1 in range(3):
            a0, a1 = 2 - r0, 2 - r1
            if 2 * (a0 + a1) >= 7:
                feasible.append((r0, r1))
    assert feasible == [(0, 0)]

    # Four core edges cover seven vertices, so the degree sequence is
    # uniquely (2,1,1,1,1,1,1).  The displayed coloured representative
    # realizes it.
    degrees = {u: 0 for u in U}
    for edge in P0 | P1:
        for u in edge:
            degrees[u] += 1
    assert sorted(degrees.values(), reverse=True) == [2, 1, 1, 1, 1, 1, 1]
    assert degrees[HUB] == 2
    assert P0.isdisjoint(P1)
    assert N_CORE_EDGE in P1
    assert N_CORE_EDGE not in P0

    # D[U]=K7-L has 17 edges.  Its degree sequence leaves room for at
    # most one D-cross-edge, incident only with HUB.
    assert 21 - len(P0 | P1) == 17
    d_core = {u: 6 - degrees[u] for u in U}
    assert d_core[HUB] == 4
    assert all(d_core[u] == 5 for u in U if u != HUB)
    assert sum(5 - d_core[u] for u in U) == 1

    # Unused-complement incidence on U is at least 27; after four
    # five-sets, four remaining triples carry at least seven incidences.
    for epsilon in (0, 1):
        remaining_incidence = 2 * 17 + epsilon - 7
        four_triples = remaining_incidence - 4 * 5
        assert remaining_incidence == 27 + epsilon
        assert four_triples >= 7
        assert (four_triples + 3) // 4 >= 2
        assert 15 - (9 - epsilon) == 6 + epsilon

    print("PASS no-WW equality structure and replacement incidence")


def verify_all_bad_k8():
    core8 = tuple(range(8))
    factors = tuple(perfect_matchings(core8))
    pairs = 0
    for first in factors:
        for second in factors:
            if first & second:
                continue
            choices = [
                (edge0, edge1)
                for edge0 in first
                for edge1 in second
                if set(edge0).isdisjoint(edge1)
            ]
            assert choices
            pairs += 1

    # Audit one literal instance of the two switches and final matching.
    edge0 = (0, 1)
    edge1 = (2, 3)
    outside0 = (8, 9)
    outside1 = (8, 10)
    repaired0 = {(0, 8), (1, 9)}
    repaired1 = {(2, 8), (3, 10)}
    final = {edge0, edge1, (4, 8), (5, 9), (6, 10), (7, 11)}
    assert not (repaired0 & repaired1)
    assert not (repaired0 & final)
    assert not (repaired1 & final)
    assert len({vertex for edge in final for vertex in edge}) == 12
    assert len({vertex for edge in repaired0 for vertex in edge}) == 4
    assert len({vertex for edge in repaired1 for vertex in edge}) == 4
    print("PASS all-bad K8 factor switches", pairs, "factor pairs")


def verify_r2():
    checked = 0
    for triple0 in combinations(W, 3):
        unions = base_unions(triple0)
        for missing_vertex in (None, *W):
            forbidden = (
                None if missing_vertex is None else (HUB, missing_vertex)
            )
            for omitted_u in combinations(U, 2):
                left = tuple(sorted(set(U) - set(omitted_u)))
                for omitted_w in W:
                    right = tuple(w for w in W if w != omitted_w)
                    replacement_masks = masks(left, right, forbidden)
                    assert replacement_masks
                    assert has_coordination(unions, replacement_masks), (
                        triple0,
                        forbidden,
                        omitted_u,
                        omitted_w,
                    )
                    checked += 1
    assert checked == 17_640
    print("PASS r'=2 replacement configurations", checked)


def verify_r3():
    base_checked = 0
    edge_checked = 0
    minimum_usable_edges = 15
    for triple0 in combinations(W, 3):
        unions = base_unions(triple0)
        for missing_vertex in (None, *W):
            forbidden = (
                None if missing_vertex is None else (HUB, missing_vertex)
            )
            for omitted_u in combinations(U, 3):
                left = tuple(sorted(set(U) - set(omitted_u)))
                usable_edges = 0
                for ww_edge in combinations(W, 2):
                    right = tuple(w for w in W if w not in ww_edge)
                    replacement_masks = masks(left, right, forbidden)
                    assert replacement_masks
                    assert has_coordination(unions, replacement_masks), (
                        triple0,
                        forbidden,
                        omitted_u,
                        ww_edge,
                    )
                    usable_edges += 1
                    edge_checked += 1
                minimum_usable_edges = min(minimum_usable_edges, usable_edges)
                base_checked += 1
    assert base_checked == 4_900
    assert edge_checked == 73_500
    assert minimum_usable_edges == 15
    print(
        "PASS r'=3 replacement configurations",
        base_checked,
        "edge-specific checks",
        edge_checked,
        "minimum usable W-edges",
        minimum_usable_edges,
    )


if __name__ == "__main__":
    verify_terminal_equalities()
    verify_all_bad_k8()
    verify_r2()
    verify_r3()
    print("PASS r=1 K7 no-WW replacement-triple repair")
