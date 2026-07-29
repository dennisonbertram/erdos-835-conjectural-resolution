#!/usr/bin/env python3
"""Exact controls for the unrestricted layer-tower reduction.

Stdlib only.  This verifies combinatorial indexing, the automatic parity
identity on the committed LS(2,3,19), and a positive local K_18
one-factorization control.  It does not construct a simultaneous fan or solve
Erdos--Rosenfeld Problem #835.
"""

from __future__ import annotations

import itertools
import math
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CYCLIC = REPO / "collaboration" / "cyclic_lsts19_extension"
sys.path.insert(0, str(CYCLIC))

from verify_fixed_link_cnf import construct_link  # noqa: E402


def canonical(values):
    return tuple(sorted(values))


def verify_tower_indexing_control():
    """Exhaust the coordinate/star dictionary for the k=6 analogue."""

    k = 6
    palette_size = k + 1
    U = tuple(range(k + 3))
    A = tuple(range(k + 3, 2 * k))
    V = U + A
    vertices = tuple(itertools.combinations(V, k))

    coordinates = {}
    for vertex in vertices:
        vertex_set = set(vertex)
        B = canonical(set(A) & vertex_set)
        Q = canonical(set(U) - vertex_set)
        assert len(Q) == len(B) + 3
        coordinates[vertex] = (B, Q)
    assert len(coordinates) == len(vertices)
    assert len(set(coordinates.values())) == len(vertices)

    stars = {}
    for base in itertools.combinations(V, k - 1):
        base_set = set(base)
        B = canonical(set(A) & base_set)
        P = canonical(set(U) - base_set)
        assert len(P) == len(B) + 4
        extensions = {
            canonical(base_set | {point})
            for point in V
            if point not in base_set
        }
        assert len(extensions) == palette_size

        tower_extensions = {
            canonical((set(U) - (set(P) - {x})) | set(B))
            for x in P
        }
        tower_extensions |= {
            canonical((set(U) - set(P)) | set(B) | {a})
            for a in A
            if a not in B
        }
        assert tower_extensions == extensions
        stars[base] = extensions

    adjacent_pairs = set()
    for base, extensions in stars.items():
        for left, right in itertools.combinations(sorted(extensions), 2):
            assert len(set(left) & set(right)) == k - 1
            pair = (left, right)
            assert pair not in adjacent_pairs, (
                "an adjacent pair must have a unique intersection star",
                base,
                pair,
            )
            adjacent_pairs.add(pair)

    direct_pairs = {
        (left, right)
        for left, right in itertools.combinations(vertices, 2)
        if len(set(left) & set(right)) == k - 1
    }
    assert adjacent_pairs == direct_pairs
    print(
        "k=6 tower indexing:",
        f"{len(vertices)} vertices, {len(stars)} stars,",
        f"{len(adjacent_pairs)} uniquely covered adjacencies: PASS",
    )


def verify_link_parity_identity():
    """Check Theorem 4 on every five-set and colour of the cyclic link."""

    points = tuple(range(19))
    colours = tuple(range(17))
    link = construct_link()
    assert len(link) == 969

    support_histogram = Counter()
    t_histogram = Counter()
    checked = 0
    for P in itertools.combinations(points, 5):
        four_sets = tuple(itertools.combinations(P, 4))
        for colour in colours:
            t = sum(
                link[canonical(T)] == colour
                for T in itertools.combinations(P, 3)
            )
            assert t <= 2
            forbidden_four_sets = sum(
                any(
                    link[canonical(T)] == colour
                    for T in itertools.combinations(Q, 3)
                )
                for Q in four_sets
            )
            assert forbidden_four_sets == 2 * t
            m = sum(
                all(
                    link[canonical(T)] != colour
                    for T in itertools.combinations(Q, 3)
                )
                for Q in four_sets
            )
            assert m == 5 - 2 * t
            support = 13 - m
            assert support == 8 + 2 * t
            assert support in (8, 10, 12) and support % 2 == 0
            t_histogram[t] += 1
            support_histogram[support] += 1
            checked += 1

    assert checked == 11_628 * 17
    assert sum(t_histogram.values()) == checked
    print(
        "LS(2,3,19) parity identity:",
        f"{checked:,} (five-set, colour) pairs;",
        f"support histogram {dict(sorted(support_histogram.items()))}: PASS",
    )


def round_robin_one_factorization(n):
    """Return the standard n-1 one-factorization of K_n for even n."""

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
        assert len({v for edge in matching for v in edge}) == n
        factors[colour] = matching
        for edge in matching:
            assert edge not in edge_colour
            edge_colour[edge] = colour
    assert len(edge_colour) == n * (n - 1) // 2
    return factors, edge_colour


def verify_k18_hole_control():
    """Restrict a K18 one-factorization and reconstruct Theorem 3 data."""

    factors, edge_colour = round_robin_one_factorization(18)
    colours = tuple(range(17))
    P = tuple(range(5))
    A = tuple(range(5, 18))

    # Local link/fan values derived from the already complete factorization.
    link = {}
    for triple in itertools.combinations(P, 3):
        complement_edge = frozenset(set(P) - set(triple))
        link[triple] = edge_colour[complement_edge]

    fan = {}
    for a in A:
        for x in P:
            Q = canonical(set(P) - {x})
            fan[a, Q] = edge_colour[frozenset((x, a))]

    missing = {}
    for a in A:
        values = {
            fan[a, canonical(set(P) - {x})]
            for x in P
        }
        assert len(values) == 5
        missing[a] = values

    # Equation (8) on each of the five local four-sets.
    for x in P:
        Q = canonical(set(P) - {x})
        face_colours = {
            link[canonical(set(Q) - {y})]
            for y in Q
        }
        cross_colours = {fan[a, Q] for a in A}
        assert len(face_colours) == 4
        assert len(cross_colours) == 13
        assert face_colours.isdisjoint(cross_colours)
        assert face_colours | cross_colours == set(colours)

    # The K13 restriction is exactly a proper prescribed-missing completion.
    hole_colouring = {
        frozenset((a, b)): edge_colour[frozenset((a, b))]
        for a, b in itertools.combinations(A, 2)
    }
    assert len(hole_colouring) == 78
    for a in A:
        incident = {
            colour
            for edge, colour in hole_colouring.items()
            if a in edge
        }
        assert len(incident) == 12
        assert incident == set(colours) - missing[a]

    support_histogram = Counter()
    for colour in colours:
        t = sum(value == colour for value in link.values())
        m = sum(colour in missing[a] for a in A)
        support = {a for a in A if colour not in missing[a]}
        assert m == 5 - 2 * t
        assert len(support) == 8 + 2 * t
        colour_edges = {
            edge
            for edge, value in hole_colouring.items()
            if value == colour
        }
        touched = {v for edge in colour_edges for v in edge}
        assert touched == support
        assert len(colour_edges) * 2 == len(support)
        support_histogram[len(support)] += 1

        # Adding the precoloured edges recovers the full perfect matching.
        precoloured = {
            edge
            for edge, value in edge_colour.items()
            if value == colour and not edge.issubset(A)
        }
        assert precoloured | colour_edges == factors[colour]

    print(
        "K18/K13-hole one-factorization control:",
        f"78 hole edges; support histogram {dict(sorted(support_histogram.items()))}: PASS",
    )


def verify_all_lift_divisibility_arithmetic():
    """Check the binomial divisibility used in Theorem 5 at every lift."""

    checked = 0
    for j in range(1, 13):
        for i in range(j):
            divisor = j + 1 - i
            total_degree = math.comb(j + 17 - i, j - i)
            assert total_degree % divisor == 0
            checked += 1
    assert checked == sum(range(1, 13))
    print(
        "all-lift design divisibility arithmetic:",
        f"{checked} (level, link-size) cases through j=12: PASS",
    )


def verify_j2_triangle_control():
    """Realize Theorem 5 and formulas (27)--(29) in a local large set."""

    # A fixed six-set R and thirteen-set A partition the 19 points of a
    # complete LS(2,3,19).  Complementing inside R turns its triple colours
    # into exact local tower data through level 3.
    R = tuple(range(6))
    A = tuple(range(6, 19))
    colours = tuple(range(17))
    large_set = construct_link()

    def tower_value(B, Q):
        triple = canonical((set(R) - set(Q)) | set(B))
        assert len(triple) == 3
        return large_set[triple]

    # Tower laws through level 1 and top properness at level 2.
    for j in (0, 1):
        for B in itertools.combinations(A, j):
            for P in itertools.combinations(R, j + 4):
                values = [
                    tower_value(B, canonical(set(P) - {x}))
                    for x in P
                ]
                values += [
                    tower_value(canonical(set(B) | {a}), P)
                    for a in A
                    if a not in B
                ]
                assert len(values) == 17
                assert set(values) == set(colours)

    for B in itertools.combinations(A, 2):
        values = [
            tower_value(B, canonical(set(R) - {x}))
            for x in R
        ]
        assert len(values) == len(set(values)) == 6

    t_histogram = Counter()
    edge_histogram = Counter()
    all_coloured_triangles = set()
    for colour in colours:
        leave = {
            frozenset(B)
            for B in itertools.combinations(A, 2)
            if colour not in {
                tower_value(B, canonical(set(R) - {x}))
                for x in R
            }
        }

        u = {}
        for a in A:
            coloured_four_sets = {
                frozenset(Q)
                for Q in itertools.combinations(R, 4)
                if tower_value((a,), Q) == colour
            }
            complement_edges = {
                frozenset(set(R) - set(Q))
                for Q in coloured_four_sets
            }
            touched = [x for edge in complement_edges for x in edge]
            assert len(touched) == len(set(touched))
            u[a] = len(coloured_four_sets)
            assert u[a] <= 3

            degree = sum(a in edge for edge in leave)
            assert degree == 6 + 2 * u[a]
            assert degree % 2 == 0

        t = sum(
            tower_value((), T) == colour
            for T in itertools.combinations(R, 3)
        )
        assert sum(u.values()) == 15 - 3 * t
        assert len(leave) == 39 + sum(u.values()) == 54 - 3 * t
        assert len(leave) % 3 == 0

        # The all-A triples of the same LS(2,3,19) provide an actual
        # triangle decomposition of this leave.
        blocks = {
            frozenset(B)
            for B in itertools.combinations(A, 3)
            if tower_value(B, R) == colour
        }
        covered = Counter(
            frozenset(edge)
            for block in blocks
            for edge in itertools.combinations(block, 2)
        )
        assert set(covered) == leave
        assert set(covered.values()) == {1}
        assert len(blocks) * 3 == len(leave)
        assert all_coloured_triangles.isdisjoint(blocks)
        all_coloured_triangles.update(blocks)

        t_histogram[t] += 1
        edge_histogram[len(leave)] += 1

    assert len(all_coloured_triangles) == math.comb(13, 3)
    print(
        "j=2 triangle-leave control:",
        f"286 triples partitioned; t histogram {dict(sorted(t_histogram.items()))};",
        f"leave-edge histogram {dict(sorted(edge_histogram.items()))}: PASS",
    )


if __name__ == "__main__":
    verify_tower_indexing_control()
    verify_link_parity_identity()
    verify_k18_hole_control()
    verify_all_lift_divisibility_arithmetic()
    verify_j2_triangle_control()
    print(
        "scope: exact reduction controls only; no simultaneous fan or",
        "J(32,16) colouring constructed; #835 remains open",
    )
