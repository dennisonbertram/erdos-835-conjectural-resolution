#!/usr/bin/env python3
"""Deterministic controls for the high-lift complement theorems.

Standard library only.  The proofs are in NOTE.md; these computations audit
the complement dictionary, the r=1 and r=2 classifications, the local r=3
four-vertex table, small switching classes, and the relevant inclusion
matrix ranks.  They do not construct a tower or solve Problem #835.
"""

from __future__ import annotations

import itertools
from collections import Counter

from enumerate_r3_small import (
    graph_from_mask,
    is_matching_switching_class,
    odd_triples,
    satisfies_divisibility,
)


def subsets(vertices, size):
    return tuple(itertools.combinations(vertices, size))


def upper_shadow(vertices, family):
    family = {frozenset(member) for member in family}
    if not family:
        return set()
    r = len(next(iter(family))) + 1
    return {
        edge_set
        for edge in itertools.combinations(vertices, r)
        for edge_set in [frozenset(edge)]
        if any(member < edge_set for member in family)
    }


def matchings(vertices):
    vertices = tuple(vertices)

    def build(available):
        yield frozenset()
        if len(available) < 2:
            return
        first = available[0]
        rest = available[1:]
        for index, partner in enumerate(rest):
            edge = frozenset((first, partner))
            tail_vertices = rest[:index] + rest[index + 1 :]
            for tail in build(tail_vertices):
                yield frozenset(set(tail) | {edge})
        # Matchings in which the first vertex is unmatched.
        for tail in build(rest):
            if tail:
                yield tail

    # The recursive presentation can produce duplicates through its empty
    # branches, so canonicalize.
    return set(build(vertices))


def verify_complement_dictionary():
    vertices = tuple(range(7))
    vertex_set = set(vertices)
    family_counts = {}
    for r in (1, 2, 3):
        j = len(vertices) - r
        if r == 1:
            families = [frozenset(), frozenset({frozenset()})]
        elif r == 2:
            families = [frozenset()]
            families += [
                frozenset({frozenset((vertex,))})
                for vertex in vertices
            ]
        else:
            families = matchings(vertices)
        family_counts[r] = len(families)
        for family in families:
            shadow = upper_shadow(vertices, family)
            blocks = {
                frozenset(vertex_set - set(member))
                for member in family
            }
            block_edges = []
            for block in blocks:
                edges = {
                    frozenset(edge)
                    for edge in itertools.combinations(block, j)
                }
                block_edges.append(edges)
                assert {
                    frozenset(vertex_set - set(edge))
                    for edge in edges
                } == {
                    r_edge
                    for r_edge in shadow
                    if member_of_shadow_base(
                        r_edge, vertex_set - set(block)
                    )
                }
            assert sum(map(len, block_edges)) == len(
                set().union(*block_edges) if block_edges else set()
            )
            complemented_shadow = {
                frozenset(vertex_set - set(edge))
                for edge in shadow
            }
            assert (
                set().union(*block_edges)
                if block_edges
                else set()
            ) == complemented_shadow
    print(
        "complement dictionary on n=7:",
        f"packing families by r={family_counts}: PASS",
    )


def member_of_shadow_base(edge, base):
    return frozenset(base) < frozenset(edge)


def verify_r1_exhaustive():
    vertices = tuple(range(6))
    passing = []
    for mask in range(1 << len(vertices)):
        selected = {
            vertex
            for vertex in vertices
            if mask & (1 << vertex)
        }
        valid = all(
            len(selected & set(T)) % len(T) == 0
            for size in range(2, len(vertices) + 1)
            for T in itertools.combinations(vertices, size)
        )
        if valid:
            passing.append(selected)
    assert passing == [set(), set(vertices)]
    print("r=1 exhaustive n=6: only empty and complete: PASS")


def verify_r2_exhaustive():
    vertices = tuple(range(6))
    edges = tuple(itertools.combinations(vertices, 2))
    passing = []
    for mask in range(1 << len(edges)):
        graph = {
            edge
            for index, edge in enumerate(edges)
            if mask & (1 << index)
        }
        valid = True
        for size in range(3, len(vertices) + 1):
            for T in itertools.combinations(vertices, size):
                T = set(T)
                count = sum(set(edge) <= T for edge in graph)
                if count % (size - 1):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            passing.append(graph)
    expected = [set()]
    expected += [
        {
            tuple(sorted((center, other)))
            for other in vertices
            if other != center
        }
        for center in vertices
    ]
    assert {frozenset(graph) for graph in passing} == {
        frozenset(graph) for graph in expected
    }
    print(
        "r=2 exhaustive n=6:",
        f"{len(passing)} graphs = empty plus six stars: PASS",
    )


def graph_type(graph, vertices):
    degrees = tuple(
        sorted(
            (
                sum(vertex in edge for edge in graph)
                for vertex in vertices
            ),
            reverse=True,
        )
    )
    return len(graph), degrees


def verify_r3_four_vertex_table():
    vertices = tuple(range(4))
    edges = tuple(itertools.combinations(vertices, 2))
    type_counts = Counter()
    passing_types = set()
    passing_graphs = 0
    for mask in range(1 << len(edges)):
        graph = {
            edge
            for index, edge in enumerate(edges)
            if mask & (1 << index)
        }
        odd = sum(
            sum(edge in graph for edge in itertools.combinations(T, 2))
            % 2
            for T in itertools.combinations(vertices, 3)
        )
        kind = graph_type(graph, vertices)
        type_counts[kind] += 1
        if (len(graph) + odd) % 3 == 0:
            passing_types.add(kind)
            passing_graphs += 1
    expected = {
        (0, (0, 0, 0, 0)),
        (1, (1, 1, 0, 0)),
        (2, (1, 1, 1, 1)),
        (3, (3, 1, 1, 1)),
        (4, (3, 2, 2, 1)),
    }
    assert passing_types == expected
    assert passing_graphs == 26
    assert sum(type_counts.values()) == 64
    print(
        "r=3 four-vertex table:",
        "64 labelled graphs, exactly 26 in five allowed types: PASS",
    )


def recover_matching(n, graph):
    vertices = set(range(1, n))
    degrees = Counter(
        vertex
        for edge in graph
        for vertex in edge
    )
    if max((degrees[vertex] for vertex in vertices), default=0) <= 1:
        return {frozenset(edge) for edge in graph}
    for center in vertices:
        if not all(
            tuple(sorted((center, vertex))) in graph
            for vertex in vertices - {center}
        ):
            continue
        remaining = {
            frozenset(edge)
            for edge in graph
            if center not in edge
        }
        remaining_degrees = Counter(
            vertex
            for edge in remaining
            for vertex in edge
        )
        if max(
            (
                remaining_degrees[vertex]
                for vertex in vertices - {center}
            ),
            default=0,
        ) <= 1:
            return remaining | {frozenset((0, center))}
    raise AssertionError("graph is not in a matching switching class")


def verify_r3_small_switching_classes():
    expected_counts = {
        4: 8,
        5: 26,
        6: 76,
        7: 232,
    }
    summaries = {}
    for n, expected in expected_counts.items():
        graph_edge_count = (n - 1) * (n - 2) // 2
        passing = 0
        for mask in range(1 << graph_edge_count):
            graph = graph_from_mask(n, mask)
            triples = odd_triples(n, graph)
            if not satisfies_divisibility(n, triples):
                continue
            passing += 1
            assert is_matching_switching_class(n, graph)
            matching = recover_matching(n, graph)
            assert {
                frozenset(triple) for triple in triples
            } == upper_shadow(tuple(range(n)), matching)
            for size in range(4, n + 1):
                for T in itertools.combinations(range(n), size):
                    T = set(T)
                    matching_edges = sum(
                        set(edge) <= T for edge in matching
                    )
                    triple_edges = sum(
                        set(triple) <= T for triple in triples
                    )
                    assert triple_edges == (size - 2) * matching_edges
        assert passing == expected
        summaries[n] = passing
    print(
        "r=3 switching classes exhaustive through n=7:",
        f"{summaries}, all matching shadows: PASS",
    )


def rank_mod_prime(matrix, prime):
    matrix = [
        [entry % prime for entry in row]
        for row in matrix
    ]
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, rows)
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], prime - 2, prime)
        matrix[rank] = [
            value * inverse % prime
            for value in matrix[rank]
        ]
        for row in range(rows):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % prime
                for left, right in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def inclusion_matrix(n, lower):
    vertices = tuple(range(n))
    columns = subsets(vertices, lower)
    rows = subsets(vertices, lower + 1)
    return [
        [int(set(column) < set(row)) for column in columns]
        for row in rows
    ]


def verify_cross_colour_ranks():
    prime = 1_000_003
    results = {}
    for lower in (1, 2):
        matrix = inclusion_matrix(13, lower)
        rank = rank_mod_prime(matrix, prime)
        column_count = len(matrix[0])
        assert rank == column_count
        results[f"W_{lower},{lower+1}"] = (
            len(matrix),
            column_count,
            rank,
        )
    print(
        "cross-colour inclusion ranks mod 1,000,003:",
        f"{results}: PASS",
    )


def main():
    verify_complement_dictionary()
    verify_r1_exhaustive()
    verify_r2_exhaustive()
    verify_r3_four_vertex_table()
    verify_r3_small_switching_classes()
    verify_cross_colour_ranks()
    print(
        "scope: local complement/decomposition theorems only; "
        "no full tower or #835 conclusion"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
