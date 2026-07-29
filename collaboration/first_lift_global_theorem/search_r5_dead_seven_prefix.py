#!/usr/bin/env python3
"""Exact CP-SAT/CEGAR search for an r=5 dead seven-prefix.

SAT output must be exported as literal data and replayed independently.
UNKNOWN is telemetry only and is never reported as infeasibility.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations

from ortools.sat.python import cp_model

from verify_r5_large_support_pair_counterexample import (
    C,
    V,
    edge,
    round_robin_factors,
)


EDGES = tuple(combinations(sorted(V), 2))
EDGE_INDEX = {current: index for index, current in enumerate(EDGES)}
INCIDENT = {
    vertex: tuple(
        index for index, current in enumerate(EDGES) if vertex in current
    )
    for vertex in V
}
PREFIX_SIZES = (4, 4, 4, 4, 6, 6, 6)
COMPLEMENT_SIZES = (5,) * 8 + (1,) * 2
Matching = tuple[tuple[int, int], ...]


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for rest in perfect_matchings(remaining):
            result.append((edge(first, second), *rest))
    return tuple(result)


def code(vertices: frozenset[int]) -> int:
    return sum(1 << vertex for vertex in vertices)


def seed_certificate() -> tuple[
    tuple[frozenset[tuple[int, int]], ...],
    tuple[frozenset[int], ...],
]:
    factors = round_robin_factors()
    additions = (
        {edge(9, 10), edge(11, 12)},
        {edge(8, 11), edge(10, 12)},
        {edge(8, 12), edge(9, 11)},
    )
    prefix = (
        frozenset(factors[3]),
        frozenset(factors[4]),
        frozenset(factors[5]),
        frozenset(factors[6]),
        frozenset(factors[0] | additions[0]),
        frozenset(factors[1] | additions[1]),
        frozenset(factors[2] | additions[2]),
    )
    triples = (
        frozenset({index, (index + 1) % 8, (index + 3) % 8})
        for index in range(8)
    )
    five_sets = tuple(sorted((C - triple for triple in triples), key=code))
    complements = (*five_sets, frozenset({11}), frozenset({12}))
    return prefix, complements


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
            for vertex in V
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
                    y[colour, edge(vertex, other)]
                    for other in support
                    if other != vertex
                )
                == 1
            )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 8355
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


def partial_factorization(
    supports: tuple[frozenset[int], ...],
    seconds: float,
) -> tuple[
    int,
    tuple[tuple[int, ...], ...] | None,
    tuple[tuple[int, int, int], ...] | None,
    cp_model.CpSolver,
]:
    outside_size = 5
    model = cp_model.CpModel()
    missing = frozenset(
        (vertex, colour)
        for colour, support in enumerate(supports)
        for vertex in V - support
    )
    cross = {
        (outside, vertex, colour): model.new_bool_var(
            f"cross_{outside}_{vertex}_{colour}"
        )
        for vertex, colour in missing
        for outside in range(outside_size)
    }
    outside_edges = tuple(combinations(range(outside_size), 2))
    internal = {
        (left, right, colour): model.new_bool_var(
            f"internal_{left}_{right}_{colour}"
        )
        for left, right in outside_edges
        for colour in range(17)
    }
    for vertex, colour in missing:
        model.add(
            sum(
                cross[outside, vertex, colour]
                for outside in range(outside_size)
            )
            == 1
        )
    for outside in range(outside_size):
        for vertex in V:
            model.add(
                sum(
                    cross[outside, vertex, colour]
                    for colour in range(17)
                    if (vertex, colour) in missing
                )
                == 1
            )
    for left, right in outside_edges:
        model.add(
            sum(
                internal[left, right, colour]
                for colour in range(17)
            )
            == 1
        )
    for outside in range(outside_size):
        for colour in range(17):
            model.add(
                sum(
                    cross[outside, vertex, colour]
                    for vertex in V
                    if (vertex, colour) in missing
                )
                + sum(
                    internal[
                        min(outside, other),
                        max(outside, other),
                        colour,
                    ]
                    for other in range(outside_size)
                    if other != outside
                )
                == 1
            )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 8355
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return status, None, None, solver
    cross_rows = tuple(
        tuple(
            next(
                colour
                for colour in range(17)
                if (outside, vertex, colour) in cross
                and solver.value(cross[outside, vertex, colour])
            )
            for outside in range(outside_size)
        )
        for vertex in V
    )
    internal_rows = tuple(
        (
            left,
            right,
            next(
                colour
                for colour in range(17)
                if solver.value(internal[left, right, colour])
            ),
        )
        for left, right in outside_edges
    )
    return status, cross_rows, internal_rows, solver


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--max-rounds", type=int, default=10_000)
    parser.add_argument("--cuts-per-row", type=int, default=16)
    parser.add_argument("--no-seed-objective", action="store_true")
    parser.add_argument("--completion-seconds", type=float, default=300.0)
    parser.add_argument("--partial-seconds", type=float, default=300.0)
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
        for vertex in V:
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
        for vertex in V
    }
    for row, size in enumerate(COMPLEMENT_SIZES):
        model.add(sum(omitted[row, vertex] for vertex in V) == size)
    for vertex in V:
        model.add(
            sum(omitted[row, vertex] for row in range(10))
            == sum(used[index] for index in INCIDENT[vertex]) - 2
        )

    weights = {vertex: 1 << vertex for vertex in V}
    for row in range(7):
        model.add(
            sum(weights[v] * omitted[row, v] for v in V)
            <= sum(weights[v] * omitted[row + 1, v] for v in V)
        )
    model.add(
        sum(weights[v] * omitted[8, v] for v in V)
        <= sum(weights[v] * omitted[9, v] for v in V)
    )

    seed_prefix, seed_complements = seed_certificate()
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
        for vertex in V:
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
    solver.parameters.random_seed = 8355

    cuts = 0
    for round_index in range(1, args.max_rounds + 1):
        status = solver.solve(model)
        if status == cp_model.INFEASIBLE:
            print(f"MASTER_UNSAT rounds={round_index} cuts={cuts}")
            return
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(
                f"MASTER_UNKNOWN rounds={round_index} cuts={cuts} "
                f"status={solver.status_name(status)} "
                f"wall={solver.wall_time:.3f}"
            )
            return

        prefix, complements = extract_candidate(solver, x, used, omitted)
        selected_union = frozenset().union(*prefix)
        violations = []
        for row, complement_set in enumerate(complements):
            support = V - complement_set
            row_violations = []
            for current in perfect_matchings(tuple(sorted(support))):
                if selected_union.isdisjoint(current):
                    row_violations.append(current)
                    if len(row_violations) == args.cuts_per_row:
                        break
            violations.extend(
                (row, complement_set, current)
                for current in row_violations
            )

        if not violations:
            selected_supports = tuple(
                frozenset(vertex for current in layer for vertex in current)
                for layer in prefix
            )
            supports = (
                *selected_supports,
                *(V - complement_set for complement_set in complements),
            )
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
                supports,
                args.completion_seconds,
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
            partial_status, cross, internal, partial_solver = (
                partial_factorization(supports, args.partial_seconds)
            )
            print(
                "PARTIAL_FACTORIZATION "
                f"status={partial_solver.status_name(partial_status)} "
                f"wall={partial_solver.wall_time:.3f}"
            )
            if cross is not None and internal is not None:
                print("PARTIAL_CROSS =", cross)
                print("PARTIAL_INTERNAL =", internal)
            return

        for row, complement_set, current in violations:
            mismatch = len(complement_set) - sum(
                omitted[row, vertex] for vertex in complement_set
            )
            model.add(
                sum(used[EDGE_INDEX[pair]] for pair in current)
                + mismatch
                >= 1
            )
            cuts += 1
        if round_index % 25 == 0:
            print(
                f"PROGRESS rounds={round_index} cuts={cuts} "
                f"objective={solver.objective_value:.0f}",
                flush=True,
            )

    print(f"MASTER_UNKNOWN rounds={args.max_rounds} cuts={cuts}")


if __name__ == "__main__":
    main()
