#!/usr/bin/env python3
"""Search one C17-invariant matching with a MIP branch-and-cut backend.

The model has one binary variable per quotient cell and one equality for each
of the 1,140 exact-cover groups.  A returned assignment is checked
combinatorially before a certificate is written.  Timeout and backend-local
infeasibility without an independently checkable proof have no mathematical
status.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ortools.linear_solver import pywraplp

from search_cyclic_invariant_matching_local import verify_matching
from verify_fan_kernel_reduction import (
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


STATUS_NAMES = {
    pywraplp.Solver.OPTIMAL: "OPTIMAL",
    pywraplp.Solver.FEASIBLE: "FEASIBLE",
    pywraplp.Solver.INFEASIBLE: "INFEASIBLE",
    pywraplp.Solver.UNBOUNDED: "UNBOUNDED",
    pywraplp.Solver.ABNORMAL: "ABNORMAL",
    pywraplp.Solver.MODEL_INVALID: "MODEL_INVALID",
    pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=("SCIP", "HIGHS", "CBC"), default="SCIP")
    parser.add_argument("--seconds", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--log-progress", action="store_true")
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).with_name("cyclic_invariant_matching.txt"),
    )
    args = parser.parse_args()

    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    solver = pywraplp.Solver.CreateSolver(args.backend)
    if solver is None:
        raise RuntimeError(f"backend {args.backend} is unavailable")
    solver.SetTimeLimit(round(args.seconds * 1000))
    if args.workers:
        result = solver.SetNumThreads(args.workers)
        if not result:
            raise RuntimeError(f"backend {args.backend} rejected worker count")
    if args.log_progress:
        solver.EnableOutput()

    selected = [
        solver.BoolVar(f"selected_{cell}") for cell in range(len(cells))
    ]
    for group_number, group in enumerate(groups):
        constraint = solver.Constraint(1, 1, f"group_{group_number}")
        for cell in group:
            constraint.SetCoefficient(selected[cell], 1)

    status = solver.Solve()
    print(f"backend={args.backend}")
    print(f"status={STATUS_NAMES.get(status, f'UNKNOWN_CODE_{status}')}")
    print(f"variables={solver.NumVariables()}")
    print(f"constraints={solver.NumConstraints()}")
    print(f"wall_time={solver.WallTime() / 1000:.6f}")
    print(f"nodes={solver.nodes()}")
    if status not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        print("certificate=NONE")
        print(
            "scope=timeout or backend-local infeasibility is not a portable "
            "UNSAT certificate"
        )
        return

    chosen = [
        cell
        for cell, variable in enumerate(selected)
        if variable.solution_value() > 0.5
    ]
    verify_matching(chosen, groups)
    args.certificate.write_text(
        "".join(f"{cell}\n" for cell in chosen),
        encoding="ascii",
    )
    print(f"certificate={args.certificate}")
    print(f"selected_orbit_cells={len(chosen)}")
    print("semantic_verification=PASS")
    print("scope=one invariant LS(3,4,20) only; not a 13-fan or #835 solution")


if __name__ == "__main__":
    main()
