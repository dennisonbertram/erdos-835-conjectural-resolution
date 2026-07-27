#!/usr/bin/env python3
"""Exhaust the n=5 analogue of support-matching completion.

The target first lift asks for one perfect matching on each prescribed even
support, with all chosen matchings partitioning the edges of a complete
graph.  The matching-deletion inequalities are necessary.  This script
tests their sufficiency in the smallest nontrivial odd order:

* the ground graph is K5;
* each vertex belongs to four supports;
* supports are the nonempty even subsets (sizes 2 and 4);
* support families are unordered multisets.

The search is standard-library-only and exhaustive.
"""

from __future__ import annotations

import functools
import itertools


N = 5
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ALL_EDGE_MASK = (1 << len(EDGES)) - 1
SUPPORTS = tuple(
    frozenset(vertices)
    for size in (4, 2)
    for vertices in itertools.combinations(VERTICES, size)
)


def cardinality(mask):
    return bin(mask).count("1")


def edge_mask(edges):
    return sum(
        1 << EDGE_INDEX[tuple(sorted(edge))]
        for edge in edges
    )


def perfect_matchings(support):
    support = frozenset(support)

    @functools.cache
    def build(vertices):
        if not vertices:
            return (0,)
        first = min(vertices)
        rest = vertices - {first}
        results = []
        for partner in sorted(rest):
            bit = 1 << EDGE_INDEX[tuple(sorted((first, partner)))]
            for tail in build(rest - {partner}):
                results.append(bit | tail)
        return tuple(results)

    return build(support)


MATCHINGS = tuple(perfect_matchings(support) for support in SUPPORTS)


def completes(counts):
    choices = [
        MATCHINGS[index]
        for index, count in enumerate(counts)
        for _ in range(count)
    ]
    choices.sort(key=len)

    @functools.cache
    def search(position, used):
        if position == len(choices):
            return used == ALL_EDGE_MASK
        return any(
            not (matching & used)
            and search(position + 1, used | matching)
            for matching in choices[position]
        )

    return search(0, 0)


def deficiency_table():
    table = []
    for index, support in enumerate(SUPPORTS):
        support_edge_mask = edge_mask(itertools.combinations(support, 2))
        row = []
        for forbidden in range(1 << len(EDGES)):
            available = support_edge_mask & ~forbidden
            best = 0
            for matching in MATCHINGS[index]:
                best = max(
                    best,
                    cardinality(matching & available)
                    if not (matching & ~available)
                    else 0,
                )
            # A maximum matching need not be perfect.  For K2/K4, enumerate
            # all subsets directly to avoid importing a graph package.
            for subset in range(1 << len(EDGES)):
                if subset & ~available:
                    continue
                used_vertices = set()
                valid = True
                for edge_index, edge in enumerate(EDGES):
                    if not subset & (1 << edge_index):
                        continue
                    if not set(edge).issubset(support):
                        valid = False
                        break
                    if used_vertices & set(edge):
                        valid = False
                        break
                    used_vertices.update(edge)
                if valid:
                    best = max(best, cardinality(subset))
            row.append(len(support) // 2 - best)
        table.append(tuple(row))
    return tuple(table)


DEFICIENCIES = deficiency_table()


def passes_all_capacity_inequalities(counts):
    for forbidden in range(1 << len(EDGES)):
        demand = sum(
            count * DEFICIENCIES[index][forbidden]
            for index, count in enumerate(counts)
        )
        if demand > cardinality(forbidden):
            return False, forbidden, demand
    return True, None, None


def support_multisets():
    residual = [N - 1] * N
    counts = [0] * len(SUPPORTS)

    def generate(index):
        if index == len(SUPPORTS):
            if residual == [0] * N:
                yield tuple(counts)
            return
        support = SUPPORTS[index]
        maximum = min(residual[vertex] for vertex in support)
        for count in range(maximum + 1):
            counts[index] = count
            for vertex in support:
                residual[vertex] -= count
            if all(value >= 0 for value in residual):
                yield from generate(index + 1)
            for vertex in support:
                residual[vertex] += count
        counts[index] = 0

    yield from generate(0)


def describe(counts):
    return [
        (sorted(SUPPORTS[index]), count)
        for index, count in enumerate(counts)
        if count
    ]


def main():
    total = 0
    complete = 0
    incomplete = 0
    capacity_rejected = 0
    capacity_pass_incomplete = []
    first_rejected = None

    for counts in support_multisets():
        total += 1
        if completes(counts):
            complete += 1
            continue
        incomplete += 1
        passes, forbidden, demand = passes_all_capacity_inequalities(counts)
        if passes:
            capacity_pass_incomplete.append(counts)
        else:
            capacity_rejected += 1
            if first_rejected is None:
                first_rejected = (counts, forbidden, demand)

    print(
        f"n=5 multisets={total} complete={complete} incomplete={incomplete} "
        f"capacity_rejected={capacity_rejected} "
        f"capacity_pass_incomplete={len(capacity_pass_incomplete)}"
    )
    if first_rejected:
        counts, forbidden, demand = first_rejected
        print(
            "first capacity-rejected incomplete instance:",
            describe(counts),
        )
        print(
            f"  F={[EDGES[i] for i in range(len(EDGES)) if forbidden & (1 << i)]} "
            f"demand={demand} |F|={cardinality(forbidden)}"
        )
    if capacity_pass_incomplete:
        print(
            "COUNTEREXAMPLE TO SUFFICIENCY:",
            describe(capacity_pass_incomplete[0]),
        )
        return 2
    print(
        "No n=5 counterexample to sufficiency; this does not address n=13."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
