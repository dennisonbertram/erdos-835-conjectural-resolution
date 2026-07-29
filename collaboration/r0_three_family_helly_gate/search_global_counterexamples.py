#!/usr/bin/env python3
"""Exact CEGIS search for an r=0 prefix where all 35 triple routes fail.

The seven remaining triple complements and four remaining five-set
complements are SAT variables satisfying the exact class-B row equations.
The first triple is fixed to {0,1,2}, without loss by vertex and row
symmetry.  Equal-size prefix layers and remaining rows are lexicographically
ordered to remove label symmetry.

The search always excludes a K6.  It excludes a K6-e only when at least six
of the seven triple rows avoid its six-vertex core, which is precisely the
already-routed t=6 equality boundary.  The row-avoidance literals are included
in each lazy equality clause, so K6-e occurrences with t<=5 remain searchable.
These constraints, and the clauses excluding discovered coordinated triples,
are generated lazily.  Every lazy clause is globally valid.

This is a search program, not a proof certificate.  Any reported
counterexample is independently checkable.  An UNSAT result should be
regenerated as DIMACS and certified before being used as a theorem.
"""

from __future__ import annotations

import argparse
import json
import time
from itertools import combinations

from pysat.solvers import Cadical195

from search_counterexamples import Cnf, EDGES, EDGE_INDEX, PREFIX_SIZES, VERTICES


VERTEX_SET = frozenset(VERTICES)


def perfect_matchings(
    vertices: tuple[int, ...],
    deleted: frozenset[tuple[int, int]],
) -> tuple[frozenset[tuple[int, int]], ...]:
    if not vertices:
        return (frozenset(),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        edge = tuple(sorted((first, second)))
        if edge in deleted:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest, deleted):
            result.append(frozenset((edge, *tail)))
    return tuple(result)


def disjoint_triples(
    families: tuple[tuple[frozenset[tuple[int, int]], ...], ...],
    colours: tuple[int, int, int],
    limit: int,
) -> tuple[tuple[frozenset[tuple[int, int]], ...], ...]:
    found = []
    left_family, middle_family, right_family = (
        families[colour] for colour in colours
    )
    for left in left_family:
        for middle in middle_family:
            if left & middle:
                continue
            union = left | middle
            for right in right_family:
                if union.isdisjoint(right):
                    found.append((left, middle, right))
                    if len(found) >= limit:
                        return tuple(found)
    return tuple(found)


def lexicographic_leq(cnf: Cnf, tag: tuple, left: list[int], right: list[int]) -> None:
    """Encode the bit vector ``left`` as lexicographically <= ``right``."""
    if len(left) != len(right):
        raise ValueError("lexicographic vectors have different lengths")
    prefix_equal = cnf.true
    for position, (left_bit, right_bit) in enumerate(zip(left, right)):
        # If the earlier bits agree, 1 followed by 0 is forbidden.
        cnf.add(-prefix_equal, -left_bit, right_bit)
        next_equal = cnf.variable(("lex_equal", tag, position))
        # next_equal <-> prefix_equal AND (left_bit == right_bit).
        cnf.add(-next_equal, prefix_equal)
        cnf.add(-next_equal, -left_bit, right_bit)
        cnf.add(-next_equal, left_bit, -right_bit)
        cnf.add(-prefix_equal, -left_bit, -right_bit, next_equal)
        cnf.add(-prefix_equal, left_bit, right_bit, next_equal)
        prefix_equal = next_equal


def build_instance() -> Cnf:
    cnf = Cnf()

    def colour_edge(colour: int, edge_index: int) -> int:
        return cnf.variable(("colour_edge", colour, edge_index))

    def deleted(edge_index: int) -> int:
        return cnf.variable(("deleted_edge", edge_index))

    def remaining_row(row: int, vertex: int) -> int:
        return cnf.variable(("remaining_row", row, vertex))

    for colour, size in enumerate(PREFIX_SIZES):
        colour_edges = [
            colour_edge(colour, edge_index) for edge_index in range(len(EDGES))
        ]
        cnf.cardinality(
            ("colour_size", colour),
            colour_edges,
            lower=size,
            upper=size,
        )
        for vertex in VERTICES:
            cnf.cardinality(
                ("colour_vertex", colour, vertex),
                [
                    colour_edge(colour, edge_index)
                    for edge_index, edge in enumerate(EDGES)
                    if vertex in edge
                ],
                upper=1,
            )

    # Prefix colours of equal size are labels for an unordered set of rows.
    for left, right in ((0, 1), (1, 2), (3, 4), (4, 5)):
        lexicographic_leq(
            cnf,
            ("prefix", left, right),
            [colour_edge(left, edge_index) for edge_index in range(len(EDGES))],
            [colour_edge(right, edge_index) for edge_index in range(len(EDGES))],
        )

    for edge_index, edge in enumerate(EDGES):
        colours = [
            colour_edge(colour, edge_index) for colour in range(len(PREFIX_SIZES))
        ]
        cnf.cardinality(("edge_colour", edge), colours, upper=1)
        for literal in colours:
            cnf.add(-literal, deleted(edge_index))
        cnf.add(-deleted(edge_index), *colours)

    for vertex in VERTICES:
        cnf.cardinality(
            ("deleted_degree", vertex),
            [
                deleted(edge_index)
                for edge_index, edge in enumerate(EDGES)
                if vertex in edge
            ],
            lower=1,
            upper=5,
        )

    remaining_sizes = (3,) * 7 + (5,) * 4
    for row, size in enumerate(remaining_sizes):
        literals = [remaining_row(row, vertex) for vertex in VERTICES]
        cnf.cardinality(
            ("remaining_row_size", row),
            literals,
            lower=size,
            upper=size,
        )

    # Choose one of the seven triple rows and relabel its vertices.
    for vertex in VERTICES:
        literal = remaining_row(0, vertex)
        cnf.add(literal if vertex in (0, 1, 2) else -literal)

    # The other six triples, and independently the four five-sets, are
    # unordered multisets.  Repetitions remain allowed.
    for left, right in tuple(zip(range(1, 6), range(2, 7))) + tuple(
        zip(range(7, 10), range(8, 11))
    ):
        lexicographic_leq(
            cnf,
            ("remaining", left, right),
            [remaining_row(left, vertex) for vertex in VERTICES],
            [remaining_row(right, vertex) for vertex in VERTICES],
        )

    for vertex in VERTICES:
        incident_deletions = [
            deleted(edge_index)
            for edge_index, edge in enumerate(EDGES)
            if vertex in edge
        ]
        absent_from_rows = [
            -remaining_row(row, vertex) for row in range(11)
        ]
        cnf.cardinality(
            ("class_b_column", vertex),
            incident_deletions + absent_from_rows,
            lower=12,
            upper=12,
        )

    return cnf


def solve(
    *,
    max_rounds: int,
    witnesses_per_combo: int,
) -> dict[str, object]:
    start = time.monotonic()
    cnf = build_instance()
    initial_clauses = len(cnf.clauses)
    solver = Cadical195(bootstrap_with=cnf.clauses)
    coordination_cuts = 0
    core_cuts = 0
    rounds = 0
    result: dict[str, object]
    try:
        while max_rounds == 0 or rounds < max_rounds:
            rounds += 1
            if not solver.solve():
                result = {
                    "status": "unsat",
                    "rounds": rounds,
                    "coordination_cuts": coordination_cuts,
                    "core_cuts": core_cuts,
                }
                break
            model = {literal for literal in solver.get_model() if literal > 0}
            deleted = frozenset(
                edge
                for edge_index, edge in enumerate(EDGES)
                if cnf.variable(("deleted_edge", edge_index)) in model
            )
            rows = tuple(
                frozenset(
                    vertex
                    for vertex in VERTICES
                    if cnf.variable(("remaining_row", row, vertex)) in model
                )
                for row in range(11)
            )

            added_core_cuts = 0
            for six_set in combinations(VERTICES, 6):
                internal = tuple(
                    edge
                    for edge in combinations(six_set, 2)
                    if edge in deleted
                )
                if len(internal) == 15:
                    clause = tuple(
                        -cnf.variable(("deleted_edge", EDGE_INDEX[edge]))
                        for edge in internal
                    )
                    solver.add_clause(clause)
                    cnf.add(*clause)
                    added_core_cuts += 1
                    continue
                if len(internal) != 14:
                    continue
                avoiding_rows = tuple(
                    row
                    for row in range(7)
                    if rows[row].isdisjoint(six_set)
                )
                for six_rows in combinations(avoiding_rows, 6):
                    clause = [
                        -cnf.variable(("deleted_edge", EDGE_INDEX[edge]))
                        for edge in internal
                    ]
                    clause.extend(
                        cnf.variable(("remaining_row", row, vertex))
                        for row in six_rows
                        for vertex in six_set
                    )
                    solver.add_clause(tuple(clause))
                    cnf.add(*clause)
                    added_core_cuts += 1
            if added_core_cuts:
                core_cuts += added_core_cuts
                continue

            supports = tuple(VERTEX_SET - row for row in rows[:7])
            families = tuple(
                perfect_matchings(tuple(sorted(support)), deleted)
                for support in supports
            )
            added_coordination_cuts = 0
            packable_combinations = 0
            for colours in combinations(range(7), 3):
                witnesses = disjoint_triples(
                    families,
                    colours,
                    witnesses_per_combo,
                )
                if witnesses:
                    packable_combinations += 1
                for witness in witnesses:
                    clause = []
                    for colour in colours:
                        clause.extend(
                            -cnf.variable(("remaining_row", colour, vertex))
                            for vertex in rows[colour]
                        )
                    for edge in frozenset().union(*witness):
                        clause.append(
                            cnf.variable(("deleted_edge", EDGE_INDEX[edge]))
                        )
                    solver.add_clause(tuple(clause))
                    cnf.add(*clause)
                    added_coordination_cuts += 1

            if not packable_combinations:
                prefix = [
                    [
                        edge
                        for edge_index, edge in enumerate(EDGES)
                        if cnf.variable(("colour_edge", colour, edge_index)) in model
                    ]
                    for colour in range(len(PREFIX_SIZES))
                ]
                result = {
                    "status": "counterexample",
                    "rounds": rounds,
                    "coordination_cuts": coordination_cuts,
                    "core_cuts": core_cuts,
                    "prefix": prefix,
                    "remaining_complements": [sorted(row) for row in rows],
                    "perfect_matching_counts": [len(family) for family in families],
                }
                break
            coordination_cuts += added_coordination_cuts
        else:
            result = {
                "status": "round-limit",
                "rounds": rounds,
                "coordination_cuts": coordination_cuts,
                "core_cuts": core_cuts,
            }
    finally:
        solver.delete()

    result.update(
        {
            "variables": cnf.top,
            "initial_clauses": initial_clauses,
            "final_clauses": len(cnf.clauses),
            "elapsed_seconds": round(time.monotonic() - start, 3),
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=0,
        help="zero means no round limit",
    )
    parser.add_argument("--witnesses-per-combo", type=int, default=10)
    args = parser.parse_args()
    result = solve(
        max_rounds=args.max_rounds,
        witnesses_per_combo=args.witnesses_per_combo,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
