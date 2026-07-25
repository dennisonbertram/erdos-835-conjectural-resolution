#!/usr/bin/env python3
"""Global CP-SAT minimization of cyclic Wallis vertex-degree deviation.

All 4,200 phase cells, exact phase domains, and 8,400 cross-phase
permutations are hard constraints.  The objective is the total L1 deviation
of the 1,785 selected-triple vertex degrees from 8 at moving point 0 and 7
at every other moving point.

Unlike hard degree feasibility, this model can start from any valid
cross-compatible phase seed and report improved incumbents.  Only objective
zero is a semantically verified witness for the necessary degree relaxation.
Residual-edge collision constraints are omitted, so even objective zero is
not a full radius-five or Erdos--Rosenfeld 835 result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from search_cyclic17_vertex_degree_reduced import forbidden_shifts
from search_cyclic17_vertex_degree_sat import verify_relaxation
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    allowed_shifts,
    translate,
    zero_positions,
)


def build_model(golf):
    zeros = zero_positions(golf)
    forbidden = forbidden_shifts(zeros)
    model = cp_model.CpModel()
    domains = {}
    choose = {}

    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            domain = tuple(
                allowed_shifts((i, j), orbit_index, zeros)
            )
            domains[i, j, orbit_index] = domain
            literals = []
            for shift in domain:
                literal = model.NewBoolVar(
                    f"x_{i}_{j}_{orbit_index}_{shift}"
                )
                choose[i, j, orbit_index, shift] = literal
                literals.append(literal)
            model.AddExactlyOne(literals)

    cross_exactly_one = 0
    for fixed_point in SQUARES:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in POINTS:
                if shift in forbidden[fixed_point, orbit_index]:
                    continue
                literals = []
                for other in SQUARES:
                    if other == fixed_point:
                        continue
                    i, j = sorted((fixed_point, other))
                    literal = choose.get(
                        (i, j, orbit_index, shift)
                    )
                    if literal is not None:
                        literals.append(literal)
                assert literals
                model.AddExactlyOne(literals)
                cross_exactly_one += 1

    deviations = []
    degree_literal_memberships = 0
    for i, j in FIXED_PAIRS:
        for point in POINTS:
            literals = []
            for orbit_index, representative in enumerate(
                REPRESENTATIVES
            ):
                for shift in domains[i, j, orbit_index]:
                    if point in translate(representative, shift):
                        literals.append(
                            choose[i, j, orbit_index, shift]
                        )
            target = 8 if point == 0 else 7
            deviation = model.NewIntVar(
                0, 33, f"degree_dev_{i}_{j}_{point}"
            )
            model.AddAbsEquality(
                deviation, sum(literals) - target
            )
            deviations.append(deviation)
            degree_literal_memberships += len(literals)

    model.Minimize(sum(deviations))
    stats = {
        "primary_boolean_variables": len(choose),
        "phase_exactly_one": len(FIXED_PAIRS)
        * len(REPRESENTATIVES),
        "cross_exactly_one": cross_exactly_one,
        "degree_deviation_variables": len(deviations),
        "degree_literal_memberships": degree_literal_memberships,
        "edge_position_collision_constraints": 0,
    }
    assert stats["primary_boolean_variables"] == 47880
    assert stats["phase_exactly_one"] == 4200
    assert stats["cross_exactly_one"] == 8400
    assert stats["degree_deviation_variables"] == 1785
    assert stats["degree_literal_memberships"] == 143640
    return model, choose, domains, stats


def add_hints(model, choose, domains, source: Path) -> int:
    payload = json.loads(source.read_text(encoding="utf-8"))
    if set(payload) != {f"{i},{j}" for i, j in FIXED_PAIRS}:
        raise ValueError("phase hint must contain all 105 fixed pairs")
    hinted = 0
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        if not isinstance(phases, list) or len(phases) != 40:
            raise ValueError(f"wrong phase hint for {i},{j}")
        for orbit_index, phase in enumerate(phases):
            selected = (-phase) % 17
            if selected not in domains[i, j, orbit_index]:
                raise ValueError(
                    f"hint violates phase domain at {i},{j},{orbit_index}"
                )
            for shift in domains[i, j, orbit_index]:
                model.AddHint(
                    choose[i, j, orbit_index, shift],
                    int(shift == selected),
                )
                hinted += 1
    return hinted


def phases_from_solver(solver, choose, domains):
    answer = {}
    for i, j in FIXED_PAIRS:
        phases = []
        for orbit_index in range(len(REPRESENTATIVES)):
            selected = [
                shift for shift in domains[i, j, orbit_index]
                if solver.Value(
                    choose[i, j, orbit_index, shift]
                )
            ]
            assert len(selected) == 1
            phases.append((-selected[0]) % 17)
        answer[f"{i},{j}"] = phases
    return answer


def write_phases(path: Path, phases) -> str:
    encoded = (
        json.dumps(phases, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=1200.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--lns-only", action="store_true")
    parser.add_argument("--diversify-lns", action="store_true")
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    model, choose, domains, stats = build_model(
        construct_golf17()
    )
    hinted = (
        add_hints(model, choose, domains, args.hint)
        if args.hint is not None
        else 0
    )
    if args.audit_only:
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "counts": stats,
                    "hinted_primary_booleans": hinted,
                    "scope": "soft vertex-degree relaxation",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.use_lns_only = args.lns_only
    solver.parameters.diversify_lns_params = args.diversify_lns
    if hinted:
        solver.parameters.repair_hint = True
        solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    report = {
        "status": solver.StatusName(status),
        "counts": stats,
        "hinted_primary_booleans": hinted,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
        "portable_positive_lower_bound_proof": False,
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        objective = round(solver.ObjectiveValue())
        phases = phases_from_solver(solver, choose, domains)
        report["degree_l1"] = objective
        if args.output is not None:
            report["phase_sha256"] = write_phases(
                args.output, phases
            )
        if objective == 0:
            verify_relaxation(phases, domains)
            report.update(
                {
                    "status": "FEASIBLE_RELAXATION",
                    "semantic_relaxation_verifier": "PASS",
                }
            )
        else:
            report["semantic_relaxation_verifier"] = "NOT_RUN"
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
