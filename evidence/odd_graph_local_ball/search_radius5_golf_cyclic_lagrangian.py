#!/usr/bin/env python3
"""Lagrangian row/column decomposition for the cyclic radius-five layer.

Let R be the 105-row exact-cover family and C the 40-column proper
list-edge-colouring family, both encoded by one-hot phase indicators.  For
integer multipliers lambda, the concave dual bound is

    min_{y in R} <lambda,y> - max_{z in C} <lambda,z>.

A positive value, computed with *all* subproblems proved optimal, would
certify that R and C are disjoint inside the fixed-Wallis C17 ansatz.  A
common minimizing/maximizing array is a witness.  This implementation is
primarily a search heuristic because weighted subproblems may time out; it
labels a dual value rigorous only when every one of the 105 row and 40 column
oracles reports optimal.

The subgradient update lambda += step * (y-z) pushes the complementary exact
families toward consensus.  Any nonzero Hamming gap or timeout has no
mathematical status.  Even a verified common array would settle only this
radius-five symmetry ansatz, not Erdos-Rosenfeld #835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from ortools.sat.python import cp_model

from improve_radius5_golf_cyclic_slice_lns import (
    State,
    audit_static,
    domains_for_seed,
    dump_phases,
    load_state,
    slice_scores,
)
from global_latin_audit import construct_golf17
from search_radius5_golf_cyclic_alternating_projection import (
    cross_distinct,
    hamming,
    verify_common,
)
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    REPRESENTATIVES,
    SQUARES,
)


Multiplier = dict[tuple[int, int, int, int], int]


def state_sha256(state: State) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_state(path: Path, state: State) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def initialize_multipliers(
    domains,
    row_state: State,
    cross_state: State,
    scale: int,
) -> Multiplier:
    multipliers = {
        (i, j, orbit_index, shift): 0
        for i, j in FIXED_PAIRS
        for orbit_index in range(len(REPRESENTATIVES))
        for shift in domains[i, j, orbit_index]
    }
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            row_shift = row_state[i, j, orbit_index]
            cross_shift = cross_state[i, j, orbit_index]
            if row_shift == cross_shift:
                continue
            multipliers[i, j, orbit_index, row_shift] -= scale
            multipliers[i, j, orbit_index, cross_shift] += scale
    return multipliers


def solve_weighted_row(
    binary: Path,
    multipliers: Multiplier,
    domains,
    fallback: State,
    fixed_pair: tuple[int, int],
    *,
    seconds: float,
    nodes: int,
    seed: int,
) -> tuple[tuple[int, int], list[int], dict[str, object]]:
    normalized = []
    constant = 0
    for orbit_index in range(len(REPRESENTATIVES)):
        allowed = domains[fixed_pair + (orbit_index,)]
        minimum = min(
            multipliers[fixed_pair + (orbit_index, shift)]
            for shift in allowed
        )
        constant += minimum
        normalized.append(
            [
                (
                    multipliers[fixed_pair + (orbit_index, shift)]
                    - minimum
                    if shift in allowed
                    else 0
                )
                for shift in range(P)
            ]
        )
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="cyclic17-lagrangian-row-",
        suffix=".weights",
    ) as stream:
        for values in normalized:
            stream.write(" ".join(map(str, values)) + "\n")
        stream.flush()
        completed = subprocess.run(
            [
                str(binary),
                "--pair",
                f"{fixed_pair[0]},{fixed_pair[1]}",
                "--seconds",
                str(seconds),
                "--nodes",
                str(nodes),
                "--seed",
                str(seed),
                "--weights",
                stream.name,
                "--optimize-weight",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    if not completed.stdout.strip():
        raise RuntimeError(
            f"row oracle {fixed_pair} returned no JSON: "
            f"{completed.stderr.strip()}"
        )
    report = json.loads(completed.stdout)
    if report.get("status") == "SAT":
        shifts = report["selected_shifts"]
    else:
        shifts = [
            fallback[fixed_pair + (orbit_index,)]
            for orbit_index in range(len(REPRESENTATIVES))
        ]
        report["used_fallback"] = True
    raw_value = sum(
        multipliers[fixed_pair + (orbit_index, shift)]
        for orbit_index, shift in enumerate(shifts)
    )
    if report.get("status") == "SAT":
        expected = constant + int(report["weight"])
        if raw_value != expected:
            raise AssertionError("row weight normalization mismatch")
    report["raw_value"] = raw_value
    return fixed_pair, list(shifts), report


def solve_rows(
    binary: Path,
    multipliers: Multiplier,
    domains,
    fallback: State,
    *,
    seconds: float,
    nodes: int,
    workers: int,
    seed: int,
) -> tuple[State, dict[str, int]]:
    rng = random.Random(seed)
    state: State = {}
    reports = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                solve_weighted_row,
                binary,
                multipliers,
                domains,
                fallback,
                fixed_pair,
                seconds=seconds,
                nodes=nodes,
                seed=rng.randrange(1, 2**63),
            )
            for fixed_pair in FIXED_PAIRS
        ]
        for future in as_completed(futures):
            fixed_pair, shifts, report = future.result()
            reports.append(report)
            for orbit_index, shift in enumerate(shifts):
                state[fixed_pair + (orbit_index,)] = shift
    if set(slice_scores(state).values()) != {120}:
        raise AssertionError("row oracle family did not remain exact")
    return state, {
        "raw_minimum": sum(int(report["raw_value"]) for report in reports),
        "optimal_subproblems": sum(
            bool(report.get("optimal")) for report in reports
        ),
        "fallback_subproblems": sum(
            bool(report.get("used_fallback")) for report in reports
        ),
        "total_nodes": sum(int(report.get("nodes", 0)) for report in reports),
    }


def solve_weighted_column(
    multipliers: Multiplier,
    domains,
    previous: State,
    orbit_index: int,
    *,
    seconds: float,
    seed: int,
) -> tuple[int, dict[tuple[int, int], int], dict[str, object]]:
    model = cp_model.CpModel()
    choose = {}
    objective = []
    constant = 0
    for i, j in FIXED_PAIRS:
        allowed = domains[i, j, orbit_index]
        minimum = min(
            multipliers[i, j, orbit_index, shift]
            for shift in allowed
        )
        constant += minimum
        literals = []
        for shift in sorted(allowed):
            literal = model.NewBoolVar(f"x_{i}_{j}_{shift}")
            choose[i, j, shift] = literal
            literals.append(literal)
            coefficient = (
                multipliers[i, j, orbit_index, shift] - minimum
            )
            if coefficient:
                objective.append(coefficient * literal)
            if shift == previous[i, j, orbit_index]:
                model.AddHint(literal, 1)
        model.AddExactlyOne(literals)
    for fixed_point in SQUARES:
        incident = [
            (min(fixed_point, other), max(fixed_point, other))
            for other in SQUARES
            if other != fixed_point
        ]
        for shift in range(P):
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
    solver.parameters.hint_conflict_limit = 50_000
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        assignment = {
            fixed_pair: previous[fixed_pair + (orbit_index,)]
            for fixed_pair in FIXED_PAIRS
        }
        return orbit_index, assignment, {
            "status": solver.StatusName(status),
            "used_fallback": True,
            "raw_value": sum(
                multipliers[fixed_pair + (orbit_index, shift)]
                for fixed_pair, shift in assignment.items()
            ),
            "branches": solver.NumBranches(),
        }
    assignment = {}
    for i, j in FIXED_PAIRS:
        selected = [
            shift
            for shift in domains[i, j, orbit_index]
            if solver.Value(choose[i, j, shift])
        ]
        if len(selected) != 1:
            raise AssertionError("column oracle selected != 1 phase")
        assignment[i, j] = selected[0]
    raw_value = sum(
        multipliers[fixed_pair + (orbit_index, shift)]
        for fixed_pair, shift in assignment.items()
    )
    if raw_value != constant + round(solver.ObjectiveValue()):
        raise AssertionError("column weight normalization mismatch")
    return orbit_index, assignment, {
        "status": solver.StatusName(status),
        "raw_value": raw_value,
        "branches": solver.NumBranches(),
    }


def solve_columns(
    multipliers: Multiplier,
    domains,
    previous: State,
    *,
    seconds: float,
    workers: int,
    seed: int,
) -> tuple[State, dict[str, int]]:
    rng = random.Random(seed)
    state: State = {}
    reports = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                solve_weighted_column,
                multipliers,
                domains,
                previous,
                orbit_index,
                seconds=seconds,
                seed=rng.randrange(1, 2**31),
            )
            for orbit_index in range(len(REPRESENTATIVES))
        ]
        for future in as_completed(futures):
            orbit_index, assignment, report = future.result()
            reports.append(report)
            for fixed_pair, shift in assignment.items():
                state[fixed_pair + (orbit_index,)] = shift
    audit_static(state, domains)
    return state, {
        "raw_maximum": sum(int(report["raw_value"]) for report in reports),
        "optimal_subproblems": sum(
            report["status"] == "OPTIMAL" for report in reports
        ),
        "fallback_subproblems": sum(
            bool(report.get("used_fallback")) for report in reports
        ),
        "total_branches": sum(int(report["branches"]) for report in reports),
    }


def update_multipliers(
    multipliers: Multiplier,
    row_state: State,
    cross_state: State,
    step: int,
) -> None:
    for cell in row_state:
        row_shift = row_state[cell]
        cross_shift = cross_state[cell]
        if row_shift == cross_shift:
            continue
        multipliers[cell + (row_shift,)] += step
        multipliers[cell + (cross_shift,)] -= step


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("row_seed", type=Path)
    parser.add_argument("cross_seed", type=Path)
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--row-seconds", type=float, default=8.0)
    parser.add_argument("--column-seconds", type=float, default=5.0)
    parser.add_argument("--row-nodes", type=int, default=1_000_000_000)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--initial-scale", type=int, default=2)
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--row-output", type=Path)
    parser.add_argument("--cross-output", type=Path)
    parser.add_argument("--phase-output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()

    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    domains = domains_for_seed(construct_golf17())
    row_state = load_state(args.row_seed)
    if set(slice_scores(row_state).values()) != {120}:
        raise ValueError("row seed does not contain 105 exact rows")
    cross_state = load_state(args.cross_seed)
    audit_static(cross_state, domains)
    multipliers = initialize_multipliers(
        domains,
        row_state,
        cross_state,
        args.initial_scale,
    )
    rng = random.Random(args.seed)
    best = hamming(row_state, cross_state)
    print(
        json.dumps(
            {
                "status": "START",
                "hamming": best,
                "row_cross_distinct": cross_distinct(row_state),
                "cross_coverage": sum(slice_scores(cross_state).values()),
                "row_sha256": state_sha256(row_state),
                "cross_sha256": state_sha256(cross_state),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    for iteration in range(args.iterations):
        row_state, row_report = solve_rows(
            args.binary,
            multipliers,
            domains,
            row_state,
            seconds=args.row_seconds,
            nodes=args.row_nodes,
            workers=args.workers,
            seed=rng.randrange(1, 2**63),
        )
        cross_state, cross_report = solve_columns(
            multipliers,
            domains,
            cross_state,
            seconds=args.column_seconds,
            workers=args.workers,
            seed=rng.randrange(1, 2**63),
        )
        distance = hamming(row_state, cross_state)
        best = min(best, distance)
        dual_value = (
            row_report["raw_minimum"] - cross_report["raw_maximum"]
        )
        rigorous_dual = (
            row_report["optimal_subproblems"] == len(FIXED_PAIRS)
            and cross_report["optimal_subproblems"]
            == len(REPRESENTATIVES)
        )
        if args.row_output is not None:
            write_state(args.row_output, row_state)
        if args.cross_output is not None:
            write_state(args.cross_output, cross_state)
        print(
            json.dumps(
                {
                    "status": "ITERATION",
                    "iteration": iteration,
                    "hamming": distance,
                    "best_hamming": best,
                    "dual_value": dual_value,
                    "dual_value_rigorous": rigorous_dual,
                    "row_cross_distinct": cross_distinct(row_state),
                    "cross_coverage": sum(slice_scores(cross_state).values()),
                    "row_sha256": state_sha256(row_state),
                    "cross_sha256": state_sha256(cross_state),
                    "row_oracle": row_report,
                    "column_oracle": cross_report,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if distance == 0:
            print(
                json.dumps(
                    verify_common(
                        row_state,
                        domains,
                        args.phase_output,
                        args.certificate,
                    ),
                    sort_keys=True,
                )
            )
            return
        if rigorous_dual and dual_value > 0:
            print(
                json.dumps(
                    {
                        "status": "RIGOROUS_SCOPED_DUAL_OBSTRUCTION",
                        "dual_value": dual_value,
                        "scope": "fixed-Wallis C17 radius-five layer only",
                        "portable_certificate": (
                            "requires recording every exact oracle optimum"
                        ),
                    },
                    sort_keys=True,
                )
            )
            return
        update_multipliers(
            multipliers,
            row_state,
            cross_state,
            args.step,
        )
    print(
        json.dumps(
            {
                "status": "NO_WITNESS_OR_RIGOROUS_DUAL_BOUND",
                "iterations": args.iterations,
                "best_hamming": best,
                "mathematical_status": "heuristic only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
