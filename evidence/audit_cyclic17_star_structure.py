#!/usr/bin/env python3
"""Independent structural audit of the centre-0 cyclic Wallis star.

The 6,384 primary choices form a 2,800-row exact-cover matrix.  This audit
checks three exact reformulations:

1. Every orbit column is a permutation between the fourteen outer rows and
   the fourteen phases whose translated triple avoids the centre matching.
2. Exact row solutions are forty-slot sets; their pairwise intersections
   are precisely the collision matrix, and a star is exactly fourteen
   pairwise-disjoint sets (hence a partition of all 560 slots).
3. An explicit family of 280 counting dependencies spans the entire
   272-dimensional left kernel in characteristics 3, 5, and 17.

The dependency family consists of eight difference-class balances in each
of fourteen rows, forty orbit-sum balances, and one balance for each of the
128 moving edges outside the centre zero matching.  Eight relations occur
among these 280 balances.

This is only the centre-0 necessary star of the fixed-Wallis C17 ansatz.
It neither proves star feasibility nor infeasibility and does not settle
Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent
BALL = EVIDENCE / "odd_graph_local_ball"
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from audit_cyclic17_vertex_degree_mod3 import GF3Eliminator
from global_latin_audit import construct_golf17
from search_radius5_golf_cyclic_compact import (
    MOVING_EDGES,
    P,
    POINTS,
    REPRESENTATIVE_EDGE_COORDINATES,
    REPRESENTATIVES,
    SQUARES,
    translate,
    zero_positions,
)


CENTRE = 0
OUTERS = tuple(square for square in SQUARES if square != CENTRE)
ORBITS = tuple(range(len(REPRESENTATIVES)))
DIFFERENCES = tuple(range(1, 9))


def triple_edges(triple):
    return tuple(combinations(triple, 2))


def edge_coordinate(edge):
    x, y = edge
    forward = (y - x) % P
    if forward <= 8:
        return forward, x
    return P - forward, y


def add_coefficient(row, column, value):
    result = row.get(column, 0) + value
    if result:
        row[column] = result
    elif column in row:
        del row[column]


def sparse_rank(rows, prime: int) -> int:
    pivots = {}
    for source in rows:
        row = {
            column: value % prime
            for column, value in source.items()
            if value % prime
        }
        while row:
            pivot = max(row)
            factor = row[pivot]
            previous = pivots.get(pivot)
            if previous is None:
                inverse = pow(factor, -1, prime)
                pivots[pivot] = {
                    column: value * inverse % prime
                    for column, value in row.items()
                }
                break
            for column, value in previous.items():
                reduced = (
                    row.get(column, 0) - factor * value
                ) % prime
                if reduced:
                    row[column] = reduced
                elif column in row:
                    del row[column]
    return len(pivots)


def main() -> None:
    golf = construct_golf17()
    zeros = zero_positions(golf)
    zero_matchings = {
        square: {
            edge
            for edge in MOVING_EDGES
            if golf[square][edge[0]][edge[1]] == 0
        }
        for square in SQUARES
    }
    assert all(len(matching) == 8 for matching in zero_matchings.values())
    centre_matching = zero_matchings[CENTRE]

    translated = {
        (orbit, shift): translate(REPRESENTATIVES[orbit], shift)
        for orbit in ORBITS
        for shift in POINTS
    }
    centre_allowed = {
        orbit: tuple(
            shift
            for shift in POINTS
            if not (
                set(triple_edges(translated[orbit, shift]))
                & centre_matching
            )
        )
        for orbit in ORBITS
    }
    assert all(len(values) == 14 for values in centre_allowed.values())

    hole_size_distribution = Counter()
    candidate_count_from_holes = 0
    for orbit in ORBITS:
        for shift in centre_allowed[orbit]:
            edges = set(triple_edges(translated[orbit, shift]))
            holes = tuple(
                outer
                for outer in OUTERS
                if edges & zero_matchings[outer]
            )
            assert len(holes) in (1, 3)
            hole_size_distribution[len(holes)] += 1
            candidate_count_from_holes += len(OUTERS) - len(holes)
    assert hole_size_distribution == Counter({1: 112, 3: 448})
    assert candidate_count_from_holes == 6_384

    residual_edges = {
        outer: tuple(
            edge
            for edge in MOVING_EDGES
            if edge not in centre_matching
            and edge not in zero_matchings[outer]
        )
        for outer in OUTERS
    }
    assert all(len(edges) == 120 for edges in residual_edges.values())

    equations = []
    equation_index = {}

    def new_equation(key):
        equation_index[key] = len(equations)
        equations.append(0)

    for outer in OUTERS:
        for orbit in ORBITS:
            new_equation(("cell", outer, orbit))
    for outer in OUTERS:
        for edge in residual_edges[outer]:
            new_equation(("edge", outer, edge))
    for orbit in ORBITS:
        for shift in centre_allowed[orbit]:
            new_equation(("cross", orbit, shift))
    assert len(equations) == 2_800

    variables = []
    variable_incidence = []
    for outer in OUTERS:
        for orbit in ORBITS:
            for shift in centre_allowed[orbit]:
                triple = translated[orbit, shift]
                edges = triple_edges(triple)
                if any(
                    edge in zero_matchings[outer]
                    for edge in edges
                ):
                    continue
                incidence = [
                    equation_index["cell", outer, orbit],
                    *(
                        equation_index["edge", outer, edge]
                        for edge in edges
                    ),
                    equation_index["cross", orbit, shift],
                ]
                assert len(incidence) == 5
                variables.append((outer, orbit, shift))
                variable_incidence.append(tuple(incidence))
                bit = 1 << (len(variables) - 1)
                for equation in incidence:
                    equations[equation] |= bit
    assert len(variables) == 6_384

    eliminator = GF3Eliminator(track_certificate=False)
    for index, bits in enumerate(equations):
        eliminator.add(bits, 1, f"incidence:{index}")
    assert eliminator.contradiction is None
    assert eliminator.rank == 2_528
    left_nullity = len(equations) - eliminator.rank
    assert left_nullity == 272

    dependencies = []
    dependency_names = []

    # For a fixed outer row and cyclic difference, every exact row uses all
    # fifteen residual edges of that difference.  Orbit cells contribute
    # their invariant multiplicity of the same difference.
    orbit_difference_multiplicity = {
        (orbit, difference): sum(
            coordinate_difference == difference
            for coordinate_difference, _ in
            REPRESENTATIVE_EDGE_COORDINATES[orbit]
        )
        for orbit in ORBITS
        for difference in DIFFERENCES
    }
    for outer in OUTERS:
        for difference in DIFFERENCES:
            dependency = {}
            for edge in residual_edges[outer]:
                if edge_coordinate(edge)[0] == difference:
                    add_coefficient(
                        dependency,
                        equation_index["edge", outer, edge],
                        1,
                    )
            assert sum(value > 0 for value in dependency.values()) == 15
            for orbit in ORBITS:
                multiplicity = orbit_difference_multiplicity[
                    orbit, difference
                ]
                if multiplicity:
                    add_coefficient(
                        dependency,
                        equation_index["cell", outer, orbit],
                        -multiplicity,
                    )
            dependencies.append(dependency)
            dependency_names.append(
                f"difference:{outer}:{difference}"
            )

    # In one orbit, the fourteen centre-allowed phase slots and the
    # fourteen outer-row cells count the same variables.
    for orbit in ORBITS:
        dependency = {}
        for shift in centre_allowed[orbit]:
            add_coefficient(
                dependency,
                equation_index["cross", orbit, shift],
                1,
            )
        for outer in OUTERS:
            add_coefficient(
                dependency,
                equation_index["cell", outer, orbit],
                -1,
            )
        dependencies.append(dependency)
        dependency_names.append(f"orbit:{orbit}")

    # For one moving edge outside the centre matching, sum all cross slots
    # whose translated triple contains the edge.  This is the same variable
    # count as summing that residual-edge equation over every eligible row.
    for edge in MOVING_EDGES:
        if edge in centre_matching:
            continue
        dependency = {}
        cross_terms = 0
        for orbit in ORBITS:
            for shift in centre_allowed[orbit]:
                if set(edge) <= set(translated[orbit, shift]):
                    add_coefficient(
                        dependency,
                        equation_index["cross", orbit, shift],
                        1,
                    )
                    cross_terms += 1
        edge_terms = 0
        for outer in OUTERS:
            if edge in residual_edges[outer]:
                add_coefficient(
                    dependency,
                    equation_index["edge", outer, edge],
                    -1,
                )
                edge_terms += 1
        assert cross_terms == edge_terms
        assert cross_terms in (13, 14)
        dependencies.append(dependency)
        dependency_names.append(
            f"moving_edge:{edge[0]},{edge[1]}"
        )

    assert len(dependencies) == 14 * 8 + 40 + 128 == 280
    assert len(dependency_names) == len(dependencies)

    # Verify each dependency over the integers, including its right-hand
    # side (every exact-one equation has right-hand side one).
    for dependency in dependencies:
        assert sum(dependency.values()) == 0
        for incidence in variable_incidence:
            assert sum(
                dependency.get(equation, 0)
                for equation in incidence
            ) == 0

    dependency_ranks = {
        prime: sparse_rank(dependencies, prime)
        for prime in (3, 5, 17)
    }
    assert set(dependency_ranks.values()) == {272}
    assert dependency_ranks[3] == left_nullity

    report = {
        "status": "PASS",
        "centre": CENTRE,
        "outer_rows": len(OUTERS),
        "orbits": len(ORBITS),
        "centre_allowed_phase_slots": sum(
            len(values) for values in centre_allowed.values()
        ),
        "singleton_hole_slots": hole_size_distribution[1],
        "triple_hole_slots": hole_size_distribution[3],
        "primary_choices": len(variables),
        "exact_cover_rows": len(equations),
        "cell_rows": 560,
        "residual_edge_rows": 1_680,
        "cross_phase_rows": 560,
        "incidence_rank_gf3": eliminator.rank,
        "left_nullity_gf3": left_nullity,
        "explicit_counting_dependencies": len(dependencies),
        "explicit_dependency_rank": dependency_ranks,
        "row_difference_dependencies": 14 * 8,
        "orbit_sum_dependencies": 40,
        "moving_edge_dependencies": 128,
        "relations_among_explicit_dependencies": (
            len(dependencies) - dependency_ranks[3]
        ),
        "permutation_form": (
            "one outer-row permutation of 14 centre-allowed phases "
            "in each orbit"
        ),
        "collision_form": (
            "star iff 14 exact-row 40-slot sets are pairwise disjoint"
        ),
        "scope": (
            "centre-0 fixed-Wallis C17 star only; "
            "no star witness or infeasibility result"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
