#!/usr/bin/env python3
"""CEGAR screen for the three prescribed near-factor lemma.

For one of the three equality patterns among missing vertices x_0,x_1,x_2,
search for a graph H on 13 vertices with minimum degree at least seven that
does not contain three edge-disjoint matchings M_i, where M_i is perfect on
V(H) - {x_i}.

This is a discovery search, not a proof by itself.  Each master cut is a
literal 18-edge triple-packing found by the independently rebuilt subproblem.
An INFEASIBLE master would be a finite CP-SAT result requiring a separate
certificate before it could be used as a theorem.
"""

from __future__ import annotations

import argparse
import json
import random
import time
from itertools import combinations

from ortools.sat.python import cp_model

VERTICES = tuple(range(13))
EDGES = tuple(combinations(VERTICES, 2))


def missing_pattern(name: str) -> tuple[int, int, int]:
    patterns = {
        "same": (0, 0, 0),
        "two": (0, 0, 1),
        "distinct": (0, 1, 2),
    }
    return patterns[name]


def find_triple_packing(
    present: frozenset[tuple[int, int]],
    missing: tuple[int, int, int],
    *,
    time_limit: float,
    seed: int,
) -> tuple[str, frozenset[tuple[int, int]] | None]:
    model = cp_model.CpModel()
    selected: dict[tuple[int, tuple[int, int]], cp_model.IntVar] = {}

    for colour, omitted in enumerate(missing):
        support = set(VERTICES) - {omitted}
        for edge in present:
            if edge[0] in support and edge[1] in support:
                selected[colour, edge] = model.new_bool_var(
                    f"m_{colour}_{edge[0]}_{edge[1]}",
                )
        for vertex in support:
            incident = [
                variable
                for (index, edge), variable in selected.items()
                if index == colour and vertex in edge
            ]
            model.add_exactly_one(incident)

    for edge in present:
        variables = [
            selected[colour, edge]
            for colour in range(3)
            if (colour, edge) in selected
        ]
        if len(variables) >= 2:
            model.add_at_most_one(variables)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = seed
    status = solver.solve(model)
    status_name = solver.status_name(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return status_name, None

    used = frozenset(
        edge
        for (colour, edge), variable in selected.items()
        if solver.value(variable)
    )
    assert len(used) == 18
    return status_name, used


def search(
    missing: tuple[int, int, int],
    *,
    total_time: float,
    master_time: float,
    subproblem_time: float,
    seed: int,
    orbit_cuts: int,
) -> None:
    model = cp_model.CpModel()
    present = {
        edge: model.new_bool_var(f"h_{edge[0]}_{edge[1]}")
        for edge in EDGES
    }
    degrees = {
        vertex: sum(
            variable
            for edge, variable in present.items()
            if vertex in edge
        )
        for vertex in VERTICES
    }
    for degree in degrees.values():
        model.add(degree >= 7)

    # Relabelling inside a missing-pattern orbit preserves the question.
    fixed = set(missing)
    free_orbit = sorted(set(VERTICES) - fixed)
    for left, right in zip(free_orbit, free_orbit[1:]):
        model.add(degrees[left] <= degrees[right])

    model.minimize(sum(present.values()))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = seed

    started = time.monotonic()
    generator = random.Random(seed)
    cuts = 0
    while time.monotonic() - started < total_time:
        remaining = total_time - (time.monotonic() - started)
        solver.parameters.max_time_in_seconds = min(master_time, remaining)
        master_status = solver.solve(model)
        master_name = solver.status_name(master_status)
        if master_status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(
                json.dumps(
                    {
                        "result": "MASTER_" + master_name,
                        "missing": missing,
                        "cuts": cuts,
                        "elapsed": time.monotonic() - started,
                    },
                    sort_keys=True,
                ),
            )
            return

        graph = frozenset(
            edge for edge, variable in present.items() if solver.value(variable)
        )
        sub_name, packing = find_triple_packing(
            graph,
            missing,
            time_limit=min(subproblem_time, remaining),
            seed=seed + cuts + 1,
        )
        if packing is None:
            result = "COUNTEREXAMPLE" if sub_name == "INFEASIBLE" else "UNKNOWN"
            print(
                json.dumps(
                    {
                        "result": result,
                        "subproblem_status": sub_name,
                        "missing": missing,
                        "cuts": cuts,
                        "edge_count": len(graph),
                        "degrees": [
                            sum(vertex in edge for edge in graph)
                            for vertex in VERTICES
                        ],
                        "edges": sorted(graph),
                        "elapsed": time.monotonic() - started,
                    },
                    sort_keys=True,
                ),
            )
            return

        images = {packing}
        free = sorted(set(VERTICES) - set(missing))
        while len(images) < orbit_cuts:
            image = free.copy()
            generator.shuffle(image)
            permutation = dict(zip(free, image))
            permutation.update({vertex: vertex for vertex in set(missing)})
            relabelled = frozenset(
                tuple(sorted((permutation[left], permutation[right])))
                for left, right in packing
            )
            images.add(relabelled)
        for image in images:
            model.add(sum(present[edge] for edge in image) <= 17)
        cuts += len(images)
        if cuts % 100 == 0:
            print(
                json.dumps(
                    {
                        "result": "PROGRESS",
                        "missing": missing,
                        "cuts": cuts,
                        "master_edges": len(graph),
                        "elapsed": time.monotonic() - started,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    print(
        json.dumps(
            {
                "result": "TIME_LIMIT",
                "missing": missing,
                "cuts": cuts,
                "elapsed": time.monotonic() - started,
            },
            sort_keys=True,
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pattern",
        choices=("same", "two", "distinct"),
        required=True,
    )
    parser.add_argument("--total-time", type=float, default=300.0)
    parser.add_argument("--master-time", type=float, default=10.0)
    parser.add_argument("--subproblem-time", type=float, default=10.0)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--orbit-cuts", type=int, default=8)
    args = parser.parse_args()
    search(
        missing_pattern(args.pattern),
        total_time=args.total_time,
        master_time=args.master_time,
        subproblem_time=args.subproblem_time,
        seed=args.seed,
        orbit_cuts=args.orbit_cuts,
    )


if __name__ == "__main__":
    main()
