#!/usr/bin/env python3
"""Alternate exact-row and exact-column projections in the cyclic layer.

The two constraint families in the fixed-Wallis, C17-equivariant radius-five
model decompose in complementary directions:

* fixing a pair of the fifteen golf squares gives one 40-orbit exact-cover
  problem; the 105 pair rows are independent;
* fixing one moving-triple orbit gives one prescribed-list proper
  edge-colouring of K_15; the 40 orbit columns are independent.

This script keeps two complete phase arrays.  It projects a cross-compatible
array onto the row-exact family by 105 weighted Algorithm-X solves, then
projects that row-exact array onto the cross-compatible family by 40 CP-SAT
edge-colouring solves.  The objective in both directions is Hamming distance.

This is a witness heuristic.  A nonzero distance, a cycle, or a timeout has no
mathematical meaning.  Equality of the two arrays is checked by the canonical
73,457-vertex semantic converter before being reported as a radius-five
candidate.  Even a verified candidate is only for this symmetry ansatz, not
the full Erdos-Rosenfeld problem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from convert_cyclic17_r3_to_radius5 import convert
from global_latin_audit import construct_golf17
from improve_radius5_golf_cyclic_slice_lns import (
    State,
    audit_static,
    domains_for_seed,
    dump_phases,
    load_state,
    slice_scores,
)
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    REPRESENTATIVES,
    SQUARES,
)


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


def hamming(left: State, right: State) -> int:
    if set(left) != set(right):
        raise ValueError("states have different cells")
    return sum(left[key] != right[key] for key in left)


def cross_distinct(state: State) -> int:
    return sum(
        len(
            {
                state[
                    min(fixed_point, other),
                    max(fixed_point, other),
                    orbit_index,
                ]
                for other in SQUARES
                if other != fixed_point
            }
        )
        for fixed_point in SQUARES
        for orbit_index in range(len(REPRESENTATIVES))
    )


def project_one_row(
    binary: Path,
    target: State,
    fallback: State,
    fixed_pair: tuple[int, int],
    *,
    seconds: float,
    nodes: int,
    seed: int,
) -> tuple[tuple[int, int], list[int], dict[str, object]]:
    weights = [
        [
            int(shift != target[fixed_pair + (orbit_index,)])
            for shift in range(P)
        ]
        for orbit_index in range(len(REPRESENTATIVES))
    ]
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="cyclic17-row-projection-",
        suffix=".weights",
    ) as stream:
        for row in weights:
            stream.write(" ".join(map(str, row)) + "\n")
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
            f"row solver {fixed_pair} returned no JSON: "
            f"{completed.stderr.strip()}"
        )
    result = json.loads(completed.stdout)
    if result.get("status") != "SAT":
        shifts = [
            fallback[fixed_pair + (orbit_index,)]
            for orbit_index in range(len(REPRESENTATIVES))
        ]
        result["used_fallback"] = True
        return fixed_pair, shifts, result
    shifts = result.get("selected_shifts")
    if (
        not isinstance(shifts, list)
        or len(shifts) != len(REPRESENTATIVES)
        or not all(isinstance(value, int) and 0 <= value < P for value in shifts)
    ):
        raise ValueError(f"row solver {fixed_pair} returned invalid shifts")
    return fixed_pair, shifts, result


def project_rows(
    binary: Path,
    target: State,
    fallback: State,
    *,
    seconds: float,
    nodes: int,
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
                binary,
                target,
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
                answer[fixed_pair + (orbit_index,)] = shift
    scores = slice_scores(answer)
    if set(scores.values()) != {120}:
        raise AssertionError("row projection did not produce 105 exact rows")
    return answer, {
        "hamming_to_target": hamming(answer, target),
        "optimal_subproblems": sum(
            bool(report.get("optimal")) for report in reports
        ),
        "timed_out_subproblems": sum(
            bool(report.get("timed_out")) for report in reports
        ),
        "fallback_subproblems": sum(
            bool(report.get("used_fallback")) for report in reports
        ),
        "total_nodes": sum(int(report.get("nodes", 0)) for report in reports),
    }


def project_one_column(
    target: State,
    previous: State,
    domains,
    orbit_index: int,
    *,
    seconds: float,
    seed: int,
) -> tuple[int, dict[tuple[int, int], int], dict[str, object]]:
    model = cp_model.CpModel()
    choose = {}
    objective = []
    for i, j in FIXED_PAIRS:
        literals = []
        for shift in sorted(domains[i, j, orbit_index]):
            literal = model.NewBoolVar(f"x_{i}_{j}_{shift}")
            choose[i, j, shift] = literal
            literals.append(literal)
            if shift == target[i, j, orbit_index]:
                objective.append(literal)
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
        "matches": round(solver.ObjectiveValue()),
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
        "total_branches": sum(int(report["branches"]) for report in reports),
        "total_conflicts": sum(int(report["conflicts"]) for report in reports),
    }


def verify_common(
    state: State,
    domains,
    phase_output: Path | None,
    certificate: Path | None,
) -> dict[str, object]:
    audit_static(state, domains)
    if set(slice_scores(state).values()) != {120}:
        raise AssertionError("common array is not row exact")
    phase_sha = (
        write_state(phase_output, state)
        if phase_output is not None
        else state_sha256(state)
    )
    payload = convert(dump_phases(state))
    if certificate is not None:
        certificate.write_text(
            json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
    return {
        "status": "VERIFIED_RADIUS5_ANSATZ_WITNESS",
        "phase_sha256": phase_sha,
        "semantic_vertices": 73_457,
        "semantic_constrained_centres": 14_657,
        "certificate_sha256_without_hash": payload["sha256_without_hash"],
        "scope": "fixed-Wallis C17 radius-five layer only",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("cross_seed", type=Path)
    parser.add_argument(
        "--row-fallback",
        type=Path,
        required=True,
        help="verified 105-row exact seed used if a weighted row solve times out",
    )
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--row-seconds", type=float, default=3.0)
    parser.add_argument("--column-seconds", type=float, default=3.0)
    parser.add_argument("--row-nodes", type=int, default=1_000_000_000)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--row-output", type=Path)
    parser.add_argument("--cross-output", type=Path)
    parser.add_argument("--phase-output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()

    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    golf = construct_golf17()
    domains = domains_for_seed(golf)
    cross_state = load_state(args.cross_seed)
    audit_static(cross_state, domains)
    row_fallback = load_state(args.row_fallback)
    if set(slice_scores(row_fallback).values()) != {120}:
        raise ValueError("row fallback does not contain 105 exact rows")
    rng = random.Random(args.seed)
    seen = {state_sha256(cross_state)}
    best_distance = len(cross_state) + 1
    print(
        json.dumps(
            {
                "status": "START",
                "cross_seed_sha256": state_sha256(cross_state),
                "cross_seed_coverage": sum(slice_scores(cross_state).values()),
                "cross_seed_exact_rows": sum(
                    value == 120 for value in slice_scores(cross_state).values()
                ),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    for iteration in range(args.iterations):
        row_state, row_report = project_rows(
            args.binary,
            cross_state,
            row_fallback,
            seconds=args.row_seconds,
            nodes=args.row_nodes,
            workers=args.workers,
            seed=rng.randrange(1, 2**63),
        )
        row_cross = cross_distinct(row_state)
        distance = hamming(row_state, cross_state)
        best_distance = min(best_distance, distance)
        if args.row_output is not None:
            write_state(args.row_output, row_state)
        print(
            json.dumps(
                {
                    "status": "ROW_PROJECTION",
                    "iteration": iteration,
                    "distance": distance,
                    "best_distance": best_distance,
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
        next_cross, column_report = project_columns(
            row_state,
            cross_state,
            domains,
            seconds=args.column_seconds,
            workers=args.workers,
            seed=rng.randrange(1, 2**63),
        )
        distance = hamming(row_state, next_cross)
        best_distance = min(best_distance, distance)
        if args.cross_output is not None:
            write_state(args.cross_output, next_cross)
        cross_scores = slice_scores(next_cross)
        cross_sha = state_sha256(next_cross)
        print(
            json.dumps(
                {
                    "status": "COLUMN_PROJECTION",
                    "iteration": iteration,
                    "distance": distance,
                    "best_distance": best_distance,
                    "cross_coverage": sum(cross_scores.values()),
                    "cross_exact_rows": sum(
                        value == 120 for value in cross_scores.values()
                    ),
                    "cross_sha256": cross_sha,
                    **column_report,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if distance == 0:
            print(
                json.dumps(
                    verify_common(
                        next_cross,
                        domains,
                        args.phase_output,
                        args.certificate,
                    ),
                    sort_keys=True,
                )
            )
            return
        if cross_sha in seen:
            print(
                json.dumps(
                    {
                        "status": "CYCLE_WITHOUT_WITNESS",
                        "iteration": iteration,
                        "best_distance": best_distance,
                        "mathematical_status": "heuristic only",
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
                "status": "NO_WITNESS",
                "iterations": args.iterations,
                "best_distance": best_distance,
                "mathematical_status": "heuristic only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
