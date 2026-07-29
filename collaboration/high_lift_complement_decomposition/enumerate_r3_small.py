#!/usr/bin/env python3
"""Exhaust small switching classes for the r=3 divisibility problem.

Fix vertex 0 isolated in the graph representative G.  Every two-graph
(3-graph with even edge count on each 4-set) has exactly one such
representative.  We test the higher conditions

    |H*[T]| == 0 mod (|T|-2),  |T| >= 5,

where H* consists of triples spanning an odd number of G-edges.  We then
test whether G is the canonical representative of a matching switching
class.  Results are exhaustive only for the printed orders.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter


def canonical_edges(n):
    return tuple(itertools.combinations(range(1, n), 2))


def graph_from_mask(n, mask):
    edges = canonical_edges(n)
    return {
        edge
        for index, edge in enumerate(edges)
        if mask & (1 << index)
    }


def odd_triples(n, graph):
    return {
        triple
        for triple in itertools.combinations(range(n), 3)
        if sum(
            tuple(sorted(edge)) in graph
            for edge in itertools.combinations(triple, 2)
        )
        % 2
    }


def satisfies_divisibility(n, triples):
    for size in range(5, n + 1):
        divisor = size - 2
        for vertices in itertools.combinations(range(n), size):
            vertex_set = set(vertices)
            count = sum(set(triple) <= vertex_set for triple in triples)
            if count % divisor:
                return False
    return True


def is_matching_switching_class(n, graph):
    degrees = Counter(
        vertex
        for edge in graph
        for vertex in edge
    )
    if max((degrees[vertex] for vertex in range(1, n)), default=0) <= 1:
        return True
    for center in range(1, n):
        if all(
            tuple(sorted((center, vertex))) in graph
            for vertex in range(1, n)
            if vertex != center
        ):
            remaining_degrees = Counter(
                vertex
                for edge in graph
                if center not in edge
                for vertex in edge
            )
            if max(
                (
                    remaining_degrees[vertex]
                    for vertex in range(1, n)
                    if vertex != center
                ),
                default=0,
            ) <= 1:
                return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=7)
    args = parser.parse_args()

    for n in range(4, args.max_n + 1):
        edge_count = (n - 1) * (n - 2) // 2
        passing = 0
        matching_class = 0
        nonmatching = None
        triple_size_histogram = Counter()
        for mask in range(1 << edge_count):
            graph = graph_from_mask(n, mask)
            triples = odd_triples(n, graph)
            if not satisfies_divisibility(n, triples):
                continue
            passing += 1
            triple_size_histogram[len(triples)] += 1
            if is_matching_switching_class(n, graph):
                matching_class += 1
            elif nonmatching is None:
                nonmatching = (sorted(graph), sorted(triples))
        print(
            f"n={n} switching_classes={1 << edge_count} "
            f"divisible={passing} matching_class={matching_class} "
            f"nonmatching={passing-matching_class} "
            f"h_sizes={dict(sorted(triple_size_histogram.items()))}"
        )
        if nonmatching is not None:
            print(f"  first_nonmatching_graph={nonmatching[0]}")
            print(f"  first_nonmatching_H={nonmatching[1]}")
    print(
        "scope: exhaustive only through the requested max-n; "
        "no K13 or tower conclusion"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
