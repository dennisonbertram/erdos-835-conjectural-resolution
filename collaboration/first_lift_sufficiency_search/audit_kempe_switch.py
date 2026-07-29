#!/usr/bin/env python3
"""Audit the naive one-chain Kempe realization of incidence 2-switches.

An abstract 2-switch exchanges colours c,d at vertices u,v while preserving
all support sizes.  It is tempting to realize every such switch by swapping
one c/d alternating path.  This deterministic round-robin control searches
for a counterexample to that *one-chain* claim.  It does not rule out a
longer sequence using other colours.
"""

from __future__ import annotations

import itertools


def round_robin_one_factorization(n):
    assert n % 2 == 0
    infinity = n - 1
    modulus = n - 1
    factors = {}
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
        factors[colour] = matching
    return factors


def components(edges, vertices):
    neighbours = {vertex: set() for vertex in vertices}
    for edge in edges:
        left, right = tuple(edge)
        neighbours[left].add(right)
        neighbours[right].add(left)
    component_of = {}
    for start in vertices:
        if start in component_of:
            continue
        stack = [start]
        component = len(set(component_of.values()))
        while stack:
            vertex = stack.pop()
            if vertex in component_of:
                continue
            component_of[vertex] = component
            stack.extend(neighbours[vertex] - component_of.keys())
    return component_of


def main():
    factors = round_robin_one_factorization(18)
    outside = set(range(5))
    vertices = set(range(5, 18))
    matchings = {
        colour: {
            edge for edge in factor if edge.isdisjoint(outside)
        }
        for colour, factor in factors.items()
    }
    supports = {
        colour: set().union(*matching) if matching else set()
        for colour, matching in matchings.items()
    }

    switches = 0
    direct = 0
    first_indirect = None
    for left, right in itertools.combinations(range(17), 2):
        left_only = supports[left] - supports[right]
        right_only = supports[right] - supports[left]
        component_of = components(
            matchings[left] | matchings[right], vertices
        )
        for u in sorted(left_only):
            for v in sorted(right_only):
                switches += 1
                if component_of[u] == component_of[v]:
                    direct += 1
                elif first_indirect is None:
                    first_indirect = {
                        "colours": (left, right),
                        "vertices": (u, v),
                        "support_sizes": (
                            len(supports[left]),
                            len(supports[right]),
                        ),
                        "components": (
                            component_of[u],
                            component_of[v],
                        ),
                    }

    assert first_indirect is not None
    print(
        f"abstract_size_preserving_2_switches={switches} "
        f"one_chain_realizable={direct} "
        f"not_one_chain={switches-direct}"
    )
    print(f"first_not_one_chain={first_indirect}")
    print(
        "Conclusion: the naive one-chain Kempe lemma is false even for a "
        "round-robin-completable target instance; multi-step connectivity "
        "remains open."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
