#!/usr/bin/env python3
"""Boolean CP-SAT exact-cover model for one cyclic Wallis star.

This is the same 6,384-candidate, 2,800-column exact cover as the direct SAT
and DLX implementations, expressed with native CP-SAT ExactlyOne constraints.
It exists as a solver-diversity check; its mathematical scope is only one
necessary 14-row star of the fixed-Wallis C17 radius-five ansatz.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from improve_radius5_golf_cyclic_slice_lns import (
    audit_static,
    domains_for_seed,
    dump_phases,
    load_state,
    slice_scores,
)
from search_radius5_golf_cyclic_alternating_projection import cross_distinct
from search_radius5_golf_cyclic_compact import (
    MOVING_EDGES,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    translate,
)


def incident_pair(first: int, second: int) -> tuple[int, int]:
    return min(first, second), max(first, second)


def build_model(centre: int, hint_state):
    golf = construct_golf17()
    domains = domains_for_seed(golf)
    pairs = [
        incident_pair(centre, other)
        for other in SQUARES
        if other != centre
    ]
    model = cp_model.CpModel()
    choose = {}
    for fixed_pair in pairs:
        for orbit_index in range(len(REPRESENTATIVES)):
            literals = []
            for shift in sorted(domains[fixed_pair + (orbit_index,)]):
                literal = model.NewBoolVar(
                    f"x_{fixed_pair[0]}_{fixed_pair[1]}_"
                    f"{orbit_index}_{shift}"
                )
                choose[fixed_pair, orbit_index, shift] = literal
                literals.append(literal)
                if hint_state is not None:
                    model.AddHint(
                        literal,
                        int(
                            hint_state[fixed_pair + (orbit_index,)]
                            == shift
                        ),
                    )
            model.AddExactlyOne(literals)

    translated = {
        (orbit_index, shift): translate(representative, shift)
        for orbit_index, representative in enumerate(REPRESENTATIVES)
        for shift in POINTS
    }
    residual_constraints = 0
    for fixed_pair in pairs:
        i, j = fixed_pair
        leave = {
            edge
            for edge in MOVING_EDGES
            if golf[i][edge[0]][edge[1]] == 0
            or golf[j][edge[0]][edge[1]] == 0
        }
        for edge in MOVING_EDGES:
            if edge in leave:
                continue
            literals = [
                choose[fixed_pair, orbit_index, shift]
                for orbit_index in range(len(REPRESENTATIVES))
                for shift in domains[fixed_pair + (orbit_index,)]
                if set(edge) <= set(translated[orbit_index, shift])
            ]
            model.AddExactlyOne(literals)
            residual_constraints += 1

    cross_constraints = 0
    for orbit_index in range(len(REPRESENTATIVES)):
        forbidden = {
            shift
            for shift in POINTS
            if any(
                golf[centre][x][y] == 0
                for x, y in combinations(
                    translated[orbit_index, shift],
                    2,
                )
            )
        }
        for shift in POINTS:
            if shift in forbidden:
                continue
            literals = [
                choose[fixed_pair, orbit_index, shift]
                for fixed_pair in pairs
                if (fixed_pair, orbit_index, shift) in choose
            ]
            model.AddExactlyOne(literals)
            cross_constraints += 1
    stats = {
        "centre": centre,
        "primary_booleans": len(choose),
        "cell_exactly_one": 560,
        "residual_edge_exactly_one": residual_constraints,
        "cross_phase_exactly_one": cross_constraints,
    }
    if stats != {
        "centre": centre,
        "primary_booleans": 6384,
        "cell_exactly_one": 560,
        "residual_edge_exactly_one": 1680,
        "cross_phase_exactly_one": 560,
    }:
        raise AssertionError("wrong Boolean star counts")
    return model, choose, domains, pairs, stats


def write_state(path: Path, state) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--centre", type=int, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--phase-hint", type=Path)
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    if args.centre not in SQUARES:
        parser.error("--centre must lie in 0,...,14")
    source = load_state(args.source)
    if set(slice_scores(source).values()) != {120}:
        raise ValueError("source must contain 105 exact rows")
    hint_state = (
        load_state(args.phase_hint)
        if args.phase_hint is not None
        else source
    )
    model, choose, domains, pairs, stats = build_model(
        args.centre,
        hint_state,
    )
    if args.phase_hint is not None:
        audit_static(hint_state, domains)
    if args.audit_only:
        print(json.dumps({"status": "PASS", "counts": stats}, sort_keys=True))
        return

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    report: dict[str, object] = {
        "status": solver.StatusName(status),
        "counts": stats,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        state = dict(source)
        for fixed_pair in pairs:
            for orbit_index in range(len(REPRESENTATIVES)):
                selected = [
                    shift
                    for shift in domains[fixed_pair + (orbit_index,)]
                    if solver.Value(choose[fixed_pair, orbit_index, shift])
                ]
                if len(selected) != 1:
                    raise AssertionError("Boolean star selected != 1 phase")
                state[fixed_pair + (orbit_index,)] = selected[0]
        scores = slice_scores(state)
        if any(scores[fixed_pair] != 120 for fixed_pair in pairs):
            raise AssertionError("Boolean star has a nonexact row")
        for orbit_index in range(len(REPRESENTATIVES)):
            if len(
                {
                    state[fixed_pair + (orbit_index,)]
                    for fixed_pair in pairs
                }
            ) != 14:
                raise AssertionError("Boolean star has a cross collision")
        report["verified_exact_rows"] = 14
        report["verified_cross_groups"] = 40
        report["global_cross_distinct"] = cross_distinct(state)
        report["global_cross_target"] = 8400
        if args.output is not None:
            report["phase_sha256"] = write_state(args.output, state)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
