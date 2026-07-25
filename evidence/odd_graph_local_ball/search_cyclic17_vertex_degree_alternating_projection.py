#!/usr/bin/env python3
"""Alternate exact degree-row and exact cross-column projections.

For the fixed-Wallis, C17-equivariant necessary vertex-degree system, the
constraints decompose in two complementary directions:

* each of the 105 fixed-pair rows independently chooses forty translated
  triples having degree 8 at moving point 0 and degree 7 elsewhere;
* each of the forty orbit columns independently forms a prescribed-list
  proper edge-colouring of K_15 (equivalently, the prescribed-hole
  one-factorizations).

This heuristic alternately computes a minimum-Hamming row projection and a
minimum-Hamming column projection.  Both projected arrays are independently
audited.  A nonzero Hamming distance, a repeated state, or a timeout has no
mathematical meaning.  Only a common array is passed to the exact semantic
degree verifier and reported as a witness for the necessary degree
relaxation.  Even such a witness would omit residual-edge collision
constraints and would not solve the full radius-five quotient or
Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from improve_cyclic17_vertex_degree_kempe import degree_l1, make_degrees
from improve_radius5_golf_cyclic_slice_lns import (
    State,
    audit_static,
    domains_for_seed,
    dump_phases,
    load_state,
)
from search_cyclic17_vertex_degree_sat import verify_relaxation
from search_radius5_golf_cyclic_alternating_projection import (
    cross_distinct,
)
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    translate,
)


def encoded_state(state: State) -> bytes:
    return (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def state_sha256(state: State) -> str:
    return hashlib.sha256(encoded_state(state)).hexdigest()


def write_state(path: Path, state: State) -> str:
    encoded = encoded_state(state)
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def hamming(left: State, right: State) -> int:
    if set(left) != set(right):
        raise ValueError("states have different cells")
    return sum(left[key] != right[key] for key in left)


def audit_degree_exact(state: State) -> None:
    degrees = make_degrees(state)
    if degree_l1(degrees) != 0:
        raise ValueError("state is not degree exact")
    if any(sum(values) != 120 for values in degrees.values()):
        raise ValueError("fixed-pair degree sum is not 120")


def project_one_row(
    target: State,
    fallback: State,
    domains,
    fixed_pair: tuple[int, int],
    *,
    seconds: float,
    seed: int,
) -> tuple[tuple[int, int], list[int], dict[str, object]]:
    model = cp_model.CpModel()
    choose = {}
    objective = []
    for orbit_index, representative in enumerate(REPRESENTATIVES):
        literals = []
        for shift in sorted(domains[fixed_pair + (orbit_index,)]):
            literal = model.NewBoolVar(
                f"x_{fixed_pair[0]}_{fixed_pair[1]}_{orbit_index}_{shift}"
            )
            choose[orbit_index, shift] = literal
            literals.append(literal)
            if shift == target[fixed_pair + (orbit_index,)]:
                objective.append(literal)
                model.AddHint(literal, 1)
        model.AddExactlyOne(literals)

    for moving_point in POINTS:
        literals = []
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            for shift in domains[fixed_pair + (orbit_index,)]:
                if moving_point in translate(representative, shift):
                    literals.append(choose[orbit_index, shift])
        model.Add(
            sum(literals) == (8 if moving_point == 0 else 7)
        )

    model.Maximize(sum(objective))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return fixed_pair, [
            fallback[fixed_pair + (orbit_index,)]
            for orbit_index in range(len(REPRESENTATIVES))
        ], {
            "status": solver.StatusName(status),
            "used_fallback": True,
            "branches": solver.NumBranches(),
            "conflicts": solver.NumConflicts(),
        }

    shifts = []
    for orbit_index in range(len(REPRESENTATIVES)):
        selected = [
            shift
            for shift in domains[fixed_pair + (orbit_index,)]
            if solver.Value(choose[orbit_index, shift])
        ]
        if len(selected) != 1:
            raise AssertionError("row projection selected != 1 value")
        shifts.append(selected[0])
    return fixed_pair, shifts, {
        "status": solver.StatusName(status),
        "matches": round(solver.ObjectiveValue()),
        "used_fallback": False,
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }


def project_rows(
    target: State,
    fallback: State,
    domains,
    *,
    seconds: float,
    workers: int,
    seed: int,
) -> tuple[State, dict[str, int]]:
    rng = random.Random(seed)
    answer: State = {}
    reports = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                project_one_row,
                target,
                fallback,
                domains,
                fixed_pair,
                seconds=seconds,
                seed=rng.randrange(1, 2**31),
            )
            for fixed_pair in FIXED_PAIRS
        ]
        for future in as_completed(futures):
            fixed_pair, shifts, report = future.result()
            reports.append(report)
            for orbit_index, shift in enumerate(shifts):
                answer[fixed_pair + (orbit_index,)] = shift
    audit_degree_exact(answer)
    return answer, {
        "hamming_to_target": hamming(answer, target),
        "optimal_subproblems": sum(
            report["status"] == "OPTIMAL" for report in reports
        ),
        "feasible_subproblems": sum(
            report["status"] == "FEASIBLE" for report in reports
        ),
        "fallback_subproblems": sum(
            bool(report["used_fallback"]) for report in reports
        ),
        "total_branches": sum(int(report["branches"]) for report in reports),
        "total_conflicts": sum(
            int(report["conflicts"]) for report in reports
        ),
    }


def project_one_column(
    target: State,
    previous: State,
    domains,
    orbit_index: int,
    *,
    seconds: float,
    seed: int,
    force_change: bool,
) -> tuple[int, dict[tuple[int, int], int], dict[str, object]]:
    """Project one orbit, breaking primary-objective ties reproducibly.

    There are 105 selected literals.  A target match has weight 1,000 and
    every selected literal has a pseudorandom secondary weight in [0, 7].
    Since the total secondary range is at most 735, one additional target
    match always dominates every possible secondary change.
    """

    rng = random.Random(seed)
    model = cp_model.CpModel()
    choose = {}
    target_literals = []
    previous_literals = []
    objective = []
    for i, j in FIXED_PAIRS:
        literals = []
        for shift in sorted(domains[i, j, orbit_index]):
            literal = model.NewBoolVar(f"x_{i}_{j}_{shift}")
            choose[i, j, shift] = literal
            literals.append(literal)
            is_target = shift == target[i, j, orbit_index]
            if is_target:
                target_literals.append(literal)
            coefficient = 1_000 * int(is_target) + rng.randrange(8)
            if coefficient:
                objective.append(coefficient * literal)
            if shift == previous[i, j, orbit_index]:
                previous_literals.append(literal)
                model.AddHint(literal, 1)
        model.AddExactlyOne(literals)
    if force_change:
        # The previous column selects exactly 105 literals.  Requiring at most
        # 104 of them moves to the nearest distinct exact cross-colouring.
        model.Add(sum(previous_literals) <= len(FIXED_PAIRS) - 1)

    for fixed_point in SQUARES:
        incident = [
            (min(fixed_point, other), max(fixed_point, other))
            for other in SQUARES
            if other != fixed_point
        ]
        for shift in POINTS:
            literals = [
                choose[i, j, shift]
                for i, j in incident
                if (i, j, shift) in choose
            ]
            if len(literals) > 1:
                model.AddAtMostOne(literals)

    model.Maximize(sum(objective))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(
            f"column solver {orbit_index} returned "
            f"{solver.StatusName(status)}"
        )

    assignment = {}
    for i, j in FIXED_PAIRS:
        selected = [
            shift
            for shift in domains[i, j, orbit_index]
            if solver.Value(choose[i, j, shift])
        ]
        if len(selected) != 1:
            raise AssertionError("column projection selected != 1 value")
        assignment[i, j] = selected[0]
    return orbit_index, assignment, {
        "status": solver.StatusName(status),
        "matches": sum(solver.Value(literal) for literal in target_literals),
        "changed_from_previous": sum(
            not solver.Value(literal) for literal in previous_literals
        ),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }


def project_columns(
    target: State,
    previous: State,
    domains,
    *,
    seconds: float,
    workers: int,
    seed: int,
    force_change: bool,
) -> tuple[State, dict[str, int]]:
    rng = random.Random(seed)
    answer: State = {}
    reports = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                project_one_column,
                target,
                previous,
                domains,
                orbit_index,
                seconds=seconds,
                seed=rng.randrange(1, 2**31),
                force_change=force_change,
            )
            for orbit_index in range(len(REPRESENTATIVES))
        ]
        for future in as_completed(futures):
            orbit_index, assignment, report = future.result()
            reports.append(report)
            for fixed_pair, shift in assignment.items():
                answer[fixed_pair + (orbit_index,)] = shift
    audit_static(answer, domains)
    return answer, {
        "hamming_to_target": hamming(answer, target),
        "optimal_subproblems": sum(
            report["status"] == "OPTIMAL" for report in reports
        ),
        "feasible_subproblems": sum(
            report["status"] == "FEASIBLE" for report in reports
        ),
        "total_branches": sum(int(report["branches"]) for report in reports),
        "total_conflicts": sum(
            int(report["conflicts"]) for report in reports
        ),
        "changed_from_previous": sum(
            int(report["changed_from_previous"]) for report in reports
        ),
    }


def verify_common(
    state: State,
    domains,
    output: Path | None,
) -> dict[str, object]:
    audit_static(state, domains)
    audit_degree_exact(state)
    phases = dump_phases(state)
    verify_relaxation(
        phases,
        {key: tuple(values) for key, values in domains.items()},
    )
    phase_sha = (
        write_state(output, state)
        if output is not None
        else state_sha256(state)
    )
    return {
        "status": "FEASIBLE_RELAXATION",
        "phase_sha256": phase_sha,
        "semantic_relaxation_verifier": "PASS",
        "scope": "necessary vertex-degree relaxation only",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cross_seed", type=Path)
    parser.add_argument(
        "--row-fallback",
        type=Path,
        required=True,
        help="independently checked degree-exact array",
    )
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--row-seconds", type=float, default=3.0)
    parser.add_argument("--column-seconds", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument(
        "--force-column-change",
        action="store_true",
        help="project each column to its nearest distinct exact colouring",
    )
    parser.add_argument("--row-output", type=Path)
    parser.add_argument("--cross-output", type=Path)
    parser.add_argument("--phase-output", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    domains = domains_for_seed(construct_golf17())
    cross_state = load_state(args.cross_seed)
    audit_static(cross_state, domains)
    fallback = load_state(args.row_fallback)
    audit_degree_exact(fallback)
    if args.audit_only:
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "cross_seed_degree_l1": degree_l1(
                        make_degrees(cross_state)
                    ),
                    "cross_seed_cross_distinct": cross_distinct(cross_state),
                    "row_fallback_degree_l1": 0,
                    "rows": len(FIXED_PAIRS),
                    "columns": len(REPRESENTATIVES),
                    "cells": len(cross_state),
                    "scope": "necessary vertex-degree relaxation only",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    rng = random.Random(args.seed)
    seen = {state_sha256(cross_state)}
    best_degree_l1 = degree_l1(make_degrees(cross_state))
    best_distance = len(cross_state) + 1
    print(
        json.dumps(
            {
                "status": "START",
                "cross_seed_sha256": state_sha256(cross_state),
                "cross_seed_degree_l1": best_degree_l1,
                "cross_seed_cross_distinct": cross_distinct(cross_state),
            },
            sort_keys=True,
        ),
        flush=True,
    )

    for iteration in range(1, args.iterations + 1):
        row_state, row_report = project_rows(
            cross_state,
            fallback,
            domains,
            seconds=args.row_seconds,
            workers=args.workers,
            seed=rng.randrange(1, 2**31),
        )
        distance = hamming(row_state, cross_state)
        best_distance = min(best_distance, distance)
        row_cross = cross_distinct(row_state)
        if args.row_output is not None:
            write_state(args.row_output, row_state)
        print(
            json.dumps(
                {
                    "status": "ROW_PROJECTION",
                    "iteration": iteration,
                    "distance": distance,
                    "best_distance": best_distance,
                    "row_degree_l1": 0,
                    "row_cross_distinct": row_cross,
                    "row_cross_target": 8400,
                    "row_sha256": state_sha256(row_state),
                    **row_report,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if distance == 0 or row_cross == 8400:
            print(
                json.dumps(
                    verify_common(row_state, domains, args.phase_output),
                    sort_keys=True,
                )
            )
            return

        next_cross, column_report = project_columns(
            row_state,
            cross_state,
            domains,
            seconds=args.column_seconds,
            workers=args.workers,
            seed=rng.randrange(1, 2**31),
            force_change=args.force_column_change,
        )
        audit_static(next_cross, domains)
        distance = hamming(row_state, next_cross)
        best_distance = min(best_distance, distance)
        next_degree_l1 = degree_l1(make_degrees(next_cross))
        if next_degree_l1 < best_degree_l1:
            best_degree_l1 = next_degree_l1
            if args.cross_output is not None:
                write_state(args.cross_output, next_cross)
        print(
            json.dumps(
                {
                    "status": "COLUMN_PROJECTION",
                    "iteration": iteration,
                    "distance": distance,
                    "best_distance": best_distance,
                    "cross_degree_l1": next_degree_l1,
                    "best_cross_degree_l1": best_degree_l1,
                    "cross_distinct": cross_distinct(next_cross),
                    "cross_sha256": state_sha256(next_cross),
                    **column_report,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if distance == 0 or next_degree_l1 == 0:
            print(
                json.dumps(
                    verify_common(next_cross, domains, args.phase_output),
                    sort_keys=True,
                )
            )
            return

        cross_sha = state_sha256(next_cross)
        if cross_sha in seen:
            print(
                json.dumps(
                    {
                        "status": "CYCLE",
                        "iteration": iteration,
                        "best_distance": best_distance,
                        "best_cross_degree_l1": best_degree_l1,
                        "semantic_relaxation_verifier": "NOT_RUN",
                    },
                    sort_keys=True,
                )
            )
            return
        seen.add(cross_sha)
        cross_state = next_cross

    print(
        json.dumps(
            {
                "status": "DONE",
                "iterations": args.iterations,
                "best_distance": best_distance,
                "best_cross_degree_l1": best_degree_l1,
                "semantic_relaxation_verifier": "NOT_RUN",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
