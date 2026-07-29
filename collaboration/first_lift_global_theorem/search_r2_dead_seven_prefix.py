#!/usr/bin/env python3
"""Exact CP-SAT/CEGAR search for an r=2 dead seven-prefix.

SAT is exported as literal prefix/support data and must be replayed by
``verify_r2_dead_seven_prefix.py``.  A bounded UNKNOWN is never a theorem.
"""

from __future__ import annotations

import argparse
from itertools import combinations

from ortools.sat.python import cp_model

from verify_r2_dead_seven_prefix import (
    ALL_EDGES,
    VERTICES,
    build_certificate,
    perfect_matchings,
    verify_certificate,
)


EDGES = tuple(sorted(ALL_EDGES))
EDGE_INDEX = {current: index for index, current in enumerate(EDGES)}
INCIDENT = {
    vertex: tuple(
        index for index, current in enumerate(EDGES) if vertex in current
    )
    for vertex in VERTICES
}
PREFIX_SIZES = (4, 4, 4, 4, 5, 6, 6)
COMPLEMENT_SIZES = (5,) * 5 + (3,) * 5


def extract_candidate(
    solver: cp_model.CpSolver,
    x: dict[tuple[int, int], cp_model.IntVar],
    used: list[cp_model.IntVar],
    omitted: dict[tuple[int, int], cp_model.IntVar],
) -> tuple[
    tuple[frozenset[tuple[int, int]], ...],
    tuple[frozenset[int], ...],
]:
    prefix = tuple(
        frozenset(
            EDGES[edge_index]
            for edge_index in range(len(EDGES))
            if solver.value(x[colour, edge_index])
        )
        for colour in range(7)
    )
    assert frozenset().union(*prefix) == frozenset(
        EDGES[index]
        for index in range(len(EDGES))
        if solver.value(used[index])
    )
    complements = tuple(
        frozenset(
            vertex
            for vertex in VERTICES
            if solver.value(omitted[row, vertex])
        )
        for row in range(10)
    )
    return prefix, complements


def completion(
    supports: tuple[frozenset[int], ...],
    seconds: float,
) -> tuple[
    int,
    tuple[frozenset[tuple[int, int]], ...] | None,
    cp_model.CpSolver,
]:
    model = cp_model.CpModel()
    y = {
        (colour, current): model.new_bool_var(
            f"y_{colour}_{current[0]}_{current[1]}"
        )
        for colour, support in enumerate(supports)
        for current in combinations(sorted(support), 2)
    }
    for current in EDGES:
        model.add(
            sum(
                y[colour, current]
                for colour, support in enumerate(supports)
                if current[0] in support and current[1] in support
            )
            == 1
        )
    for colour, support in enumerate(supports):
        for vertex in support:
            model.add(
                sum(
                    y[colour, tuple(sorted((vertex, other)))]
                    for other in support
                    if other != vertex
                )
                == 1
            )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 8352
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return status, None, solver
    result = tuple(
        frozenset(
            current
            for current in combinations(sorted(support), 2)
            if solver.value(y[colour, current])
        )
        for colour, support in enumerate(supports)
    )
    return status, result, solver


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--max-rounds", type=int, default=10_000)
    parser.add_argument("--no-seed-objective", action="store_true")
    parser.add_argument("--completion-seconds", type=float, default=300.0)
    args = parser.parse_args()

    model = cp_model.CpModel()
    x = {
        (colour, edge_index): model.new_bool_var(
            f"x_{colour}_{edge_index}"
        )
        for colour in range(7)
        for edge_index in range(len(EDGES))
    }
    used = [
        model.new_bool_var(f"used_{edge_index}")
        for edge_index in range(len(EDGES))
    ]
    for colour, size in enumerate(PREFIX_SIZES):
        model.add(
            sum(x[colour, edge_index] for edge_index in range(len(EDGES)))
            == size
        )
        for vertex in VERTICES:
            model.add(
                sum(x[colour, edge_index] for edge_index in INCIDENT[vertex])
                <= 1
            )
    for edge_index in range(len(EDGES)):
        model.add(
            sum(x[colour, edge_index] for colour in range(7))
            == used[edge_index]
        )

    omitted = {
        (row, vertex): model.new_bool_var(f"omitted_{row}_{vertex}")
        for row in range(10)
        for vertex in VERTICES
    }
    for row, size in enumerate(COMPLEMENT_SIZES):
        model.add(
            sum(omitted[row, vertex] for vertex in VERTICES) == size
        )
    for vertex in VERTICES:
        model.add(
            sum(omitted[row, vertex] for row in range(10))
            == sum(used[index] for index in INCIDENT[vertex]) - 2
        )

    weights = {vertex: 1 << vertex for vertex in VERTICES}
    for row in range(len(COMPLEMENT_SIZES) - 1):
        if COMPLEMENT_SIZES[row] == COMPLEMENT_SIZES[row + 1]:
            model.add(
                sum(weights[v] * omitted[row, v] for v in VERTICES)
                <= sum(weights[v] * omitted[row + 1, v] for v in VERTICES)
            )

    seed_prefix, seed_complements = build_certificate()
    verify_certificate(seed_prefix, seed_complements)
    distance_terms = []
    seed_union = frozenset().union(*seed_prefix)
    for colour in range(7):
        for edge_index, current in enumerate(EDGES):
            value = int(current in seed_prefix[colour])
            model.add_hint(x[colour, edge_index], value)
            distance_terms.append(
                1 - x[colour, edge_index] if value else x[colour, edge_index]
            )
    for edge_index, current in enumerate(EDGES):
        model.add_hint(used[edge_index], int(current in seed_union))
    for row in range(10):
        for vertex in VERTICES:
            value = int(vertex in seed_complements[row])
            model.add_hint(omitted[row, vertex], value)
            distance_terms.append(
                1 - omitted[row, vertex] if value else omitted[row, vertex]
            )
    if not args.no_seed_objective:
        model.minimize(sum(distance_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 8352

    cuts = 0
    for round_index in range(1, args.max_rounds + 1):
        status = solver.solve(model)
        if status == cp_model.INFEASIBLE:
            print(f"MASTER_UNSAT rounds={round_index} cuts={cuts}")
            return
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(
                f"MASTER_UNKNOWN rounds={round_index} cuts={cuts} "
                f"status={solver.status_name(status)}"
            )
            return

        prefix, complements = extract_candidate(
            solver, x, used, omitted
        )
        selected_union = frozenset().union(*prefix)
        violations = []
        for row, complement_set in enumerate(complements):
            support = VERTICES - complement_set
            matching = next(
                (
                    current
                    for current in perfect_matchings(tuple(sorted(support)))
                    if selected_union.isdisjoint(current)
                ),
                None,
            )
            if matching is not None:
                violations.append((row, complement_set, matching))

        if not violations:
            supports = verify_certificate(prefix, complements)
            objective = (
                int(round(solver.objective_value))
                if not args.no_seed_objective
                else None
            )
            print(
                f"SAT_DEAD_PREFIX rounds={round_index} cuts={cuts} "
                f"seed_distance={objective}"
            )
            print(
                "PREFIX =",
                tuple(tuple(sorted(current)) for current in prefix),
            )
            print(
                "COMPLEMENTS =",
                tuple(tuple(sorted(current)) for current in complements),
            )
            full_status, full, full_solver = completion(
                supports, args.completion_seconds
            )
            print(
                "FULL_COMPLETION "
                f"status={full_solver.status_name(full_status)} "
                f"wall={full_solver.wall_time:.3f}"
            )
            if full is not None:
                print(
                    "COMPLETION =",
                    tuple(tuple(sorted(current)) for current in full),
                )
            return

        for row, complement_set, matching in violations:
            mismatch = len(complement_set) - sum(
                omitted[row, vertex] for vertex in complement_set
            )
            model.add(
                sum(used[EDGE_INDEX[current]] for current in matching)
                + mismatch
                >= 1
            )
            cuts += 1
        if round_index % 100 == 0:
            print(f"PROGRESS rounds={round_index} cuts={cuts}", flush=True)

    print(f"MASTER_UNKNOWN rounds={args.max_rounds} cuts={cuts}")


if __name__ == "__main__":
    main()
