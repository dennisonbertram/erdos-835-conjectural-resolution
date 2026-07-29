#!/usr/bin/env python3
"""Extract a scoped infeasible core from two cyclic projection states.

The left state is row exact and the right state is cross compatible.  For
every phase cell on which they agree, this script creates an assumption that
fixes the joint compact model to that value.  If the assumptions are jointly
inconsistent, CP-SAT returns a sufficient subset.  The script then rebuilds
the exact model with only that subset fixed as hard equalities and verifies
that the scoped subproblem is infeasible again.

This is diagnostic only.  Such a core says that a particular set of seed
values cannot all extend to a joint layer.  It is not an obstruction to the
unconditioned fixed-Wallis C17 ansatz, much less to Erdos-Rosenfeld #835.
"""

from __future__ import annotations

import argparse
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
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    REPRESENTATIVES,
    build_model,
    load_phase_payload,
)


Cell = tuple[int, int, int, int]


def agreement_cells(left: Path, right: Path) -> list[Cell]:
    left_payload = load_phase_payload(left)
    right_payload = load_phase_payload(right)
    answer = []
    for i, j in FIXED_PAIRS:
        key = f"{i},{j}"
        for orbit_index in range(len(REPRESENTATIVES)):
            phase = left_payload[key][orbit_index]
            if phase == right_payload[key][orbit_index]:
                answer.append((i, j, orbit_index, phase))
    return answer


def solve_with_assumptions(
    cells: list[Cell],
    *,
    seconds: float,
) -> tuple[str, list[Cell], dict[str, int]]:
    model, selected, _ = build_model(construct_golf17())
    by_index = {}
    assumptions = []
    for i, j, orbit_index, phase in cells:
        literal = model.NewBoolVar(f"keep_{i}_{j}_{orbit_index}_{phase}")
        model.Add(
            selected[i, j, orbit_index] == (-phase) % P
        ).OnlyEnforceIf(literal)
        by_index[literal.Index()] = (i, j, orbit_index, phase)
        assumptions.append(literal)
    model.AddAssumptions(assumptions)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    status = solver.Solve(model)
    core = []
    if status == cp_model.INFEASIBLE:
        for index in solver.SufficientAssumptionsForInfeasibility():
            if index not in by_index:
                raise AssertionError(f"unknown assumption literal {index}")
            core.append(by_index[index])
    return solver.StatusName(status), core, {
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
        "wall_time_milliseconds": round(1000 * solver.WallTime()),
    }


def verify_hard_core(
    core: list[Cell],
    *,
    seconds: float,
) -> tuple[str, dict[str, int]]:
    model, selected, _ = build_model(construct_golf17())
    for i, j, orbit_index, phase in core:
        model.Add(selected[i, j, orbit_index] == (-phase) % P)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    status = solver.Solve(model)
    return solver.StatusName(status), {
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
        "wall_time_milliseconds": round(1000 * solver.WallTime()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    cells = agreement_cells(args.left, args.right)
    status, core, assumption_stats = solve_with_assumptions(
        cells,
        seconds=args.seconds,
    )
    report: dict[str, object] = {
        "status": status,
        "agreement_cells": len(cells),
        "assumption_solve": assumption_stats,
        "scope": "conditioned seed values only; not an ansatz obstruction",
    }
    if status == "INFEASIBLE":
        hard_status, hard_stats = verify_hard_core(
            core,
            seconds=args.seconds,
        )
        report.update(
            {
                "sufficient_core_cells": len(core),
                "hard_core_status": hard_status,
                "hard_core_solve": hard_stats,
                "core": [
                    {
                        "fixed_pair": [i, j],
                        "orbit": orbit_index,
                        "phase": phase,
                    }
                    for i, j, orbit_index, phase in core
                ],
            }
        )
    if args.output is not None:
        args.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
