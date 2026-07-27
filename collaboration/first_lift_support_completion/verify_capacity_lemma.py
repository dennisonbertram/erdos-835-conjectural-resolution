#!/usr/bin/env python3
"""Deterministic controls for the first-lift matching-capacity lemma.

Stdlib only.  This proves no universal K13 completion or fan theorem.
"""

from __future__ import annotations

import functools
import itertools
from collections import Counter


def round_robin_one_factorization(n):
    assert n % 2 == 0
    infinity = n - 1
    modulus = n - 1
    factors = {}
    edge_colour = {}
    for colour in range(modulus):
        matching = {frozenset((infinity, colour))}
        for delta in range(1, n // 2):
            matching.add(
                frozenset(
                    (
                        (colour - delta) % modulus,
                        (colour + delta) % modulus,
                    )
                )
            )
        assert len(matching) == n // 2
        factors[colour] = matching
        for edge in matching:
            assert edge not in edge_colour
            edge_colour[edge] = colour
    return factors, edge_colour


def maximum_matching_size(vertices, available_edges):
    ordered = tuple(sorted(vertices))
    index = {vertex: position for position, vertex in enumerate(ordered)}
    neighbor_masks = [0] * len(ordered)
    for edge in available_edges:
        left, right = tuple(edge)
        if left not in index or right not in index:
            continue
        i, j = index[left], index[right]
        neighbor_masks[i] |= 1 << j
        neighbor_masks[j] |= 1 << i

    @functools.lru_cache(maxsize=None)
    def solve(mask):
        if not mask:
            return 0
        bit = mask & -mask
        i = bit.bit_length() - 1
        rest = mask ^ bit
        best = solve(rest)
        choices = neighbor_masks[i] & rest
        while choices:
            partner = choices & -choices
            choices ^= partner
            best = max(best, 1 + solve(rest ^ partner))
        return best

    return solve((1 << len(ordered)) - 1)


def capacity_demand(supports, forbidden):
    all_edges = {
        frozenset(edge)
        for edge in itertools.combinations(range(13), 2)
    }
    available = all_edges - set(forbidden)
    return sum(
        len(support) // 2
        - maximum_matching_size(support, available)
        for support in supports
    )


def verify_histograms():
    histograms = []
    for q in range(6):
        n8, n10, n12 = 7 + q, 10 - 2 * q, q
        assert n8 + n10 + n12 == 17
        assert 8 * n8 + 10 * n10 + 12 * n12 == 156
        assert n10 + 2 * n12 == 10
        histograms.append((n8, n10, n12))
    print(f"six target support histograms {histograms}: PASS")


def verify_small_strict_counterexample():
    supports = [
        {0, 1},
        {0, 1},
        {0, 2, 3, 4},
        {1, 2, 3, 4},
        {0, 2},
        {1, 3},
        {2, 4},
        {3, 4},
        set(),
    ]
    assert all(len(support) % 2 == 0 for support in supports)
    assert [
        sum(vertex in support for support in supports)
        for vertex in range(5)
    ] == [4] * 5
    forbidden = {frozenset((0, 1))}
    # The two repeated two-point supports each force the forbidden edge.
    demand = 0
    for support in supports:
        available = {
            frozenset(edge)
            for edge in itertools.combinations(support, 2)
        } - forbidden
        demand += (
            len(support) // 2
            - maximum_matching_size(support, available)
        )
    assert demand == 2 > len(forbidden)
    print(
        "small even-support counterexample:",
        f"capacity demand {demand} > |F|={len(forbidden)}: PASS",
    )


def target_round_robin_control():
    factors, edge_colour = round_robin_one_factorization(18)
    P = set(range(5))
    A = tuple(range(5, 18))
    relabel = {vertex: index for index, vertex in enumerate(A)}
    supports = []
    hole_matchings = []
    internal_matchings = []
    cross_edges_by_colour = []
    for colour in range(17):
        hole = {
            frozenset(relabel[vertex] for vertex in edge)
            for edge in factors[colour]
            if edge.isdisjoint(P)
        }
        support = {
            vertex
            for edge in hole
            for vertex in edge
        }
        assert len(hole) * 2 == len(support)
        supports.append(support)
        hole_matchings.append(hole)

        internal = {
            edge
            for edge in factors[colour]
            if edge.issubset(P)
        }
        cross = {
            edge
            for edge in factors[colour]
            if len(edge & P) == 1
        }
        internal_matchings.append(internal)
        cross_edges_by_colour.append(cross)

        # The cross edges give the five-label line-colouring of the
        # missing-incidence graph.  At this colour, precisely the labels
        # unused on cross edges are paired by the internal matching.
        cross_a = {
            relabel[next(iter(edge - P))]
            for edge in cross
        }
        cross_p = {
            next(iter(edge & P))
            for edge in cross
        }
        internal_p = {
            vertex
            for edge in internal
            for vertex in edge
        }
        assert cross_a == set(range(13)) - support
        assert len(cross_a) == len(cross)
        assert len(cross_p) == len(cross)
        assert internal_p == P - cross_p
        assert len(internal_p) == 2 * len(internal)

    all_hole_edges = {
        frozenset(edge)
        for edge in itertools.combinations(range(13), 2)
    }
    assert set().union(*hole_matchings) == all_hole_edges
    assert sum(map(len, hole_matchings)) == len(all_hole_edges)
    assert all(
        sum(vertex in support for support in supports) == 12
        for vertex in range(13)
    )
    # At every A-vertex all five labels occur once in its five missing
    # incidences.  Across colours the internal matchings are exactly K5,
    # equivalently the paired-unused-label multigraph is simple.
    for vertex in A:
        labels = {
            next(iter(edge & P))
            for cross in cross_edges_by_colour
            for edge in cross
            if vertex in edge
        }
        assert labels == P
    all_internal_edges = set().union(*internal_matchings)
    assert all_internal_edges == {
        frozenset(edge)
        for edge in itertools.combinations(P, 2)
    }
    assert sum(map(len, internal_matchings)) == len(all_internal_edges)
    internal_degrees = Counter(
        vertex
        for edge in all_internal_edges
        for vertex in edge
    )
    assert internal_degrees == Counter({vertex: 4 for vertex in P})
    histogram = Counter(map(len, supports))
    assert set(histogram).issubset({8, 10, 12})

    # Every ordinary cut, exhaustively.
    for mask in range(1 << 13):
        X = {vertex for vertex in range(13) if mask & (1 << vertex)}
        odd = sum(len(support & X) % 2 for support in supports)
        assert odd <= len(X) * (13 - len(X))

    # A deterministic family including non-cut edge sets.
    edge_families = []
    for size in range(1, 13):
        X = set(range(size))
        edge_families.append(
            {
                frozenset(edge)
                for edge in itertools.combinations(X, 2)
            }
        )
        edge_families.append(
            {
                frozenset((left, right))
                for left in X
                for right in set(range(13)) - X
            }
        )
    edge_families.extend(
        {
            edge
            for index, edge in enumerate(sorted(all_hole_edges, key=sorted))
            if (index * multiplier + offset) % modulus == 0
        }
        for multiplier, offset, modulus in (
            (1, 0, 2),
            (3, 1, 5),
            (5, 2, 7),
            (7, 3, 11),
            (11, 4, 13),
        )
    )
    for forbidden in edge_families:
        demand = capacity_demand(supports, forbidden)
        assert demand <= len(forbidden)
        # Directly confirm the proof's stronger witness count.
        used = sum(
            len(matching & forbidden)
            for matching in hole_matchings
        )
        assert demand <= used <= len(forbidden)

    print(
        "target round-robin control:",
        f"support histogram {dict(sorted(histogram.items()))};",
        "middle-tier K5 partition;",
        f"8192 cuts and {len(edge_families)} edge families: PASS",
    )


if __name__ == "__main__":
    verify_histograms()
    verify_small_strict_counterexample()
    target_round_robin_control()
    print(
        "scope: necessary-condition controls only; no universal first lift,",
        "fan, or #835 conclusion",
    )
