#!/usr/bin/env python3
"""Minimize invariant-matching defects with a MIP backend.

Quadruple-orbit equations remain exact.  Continuous under/over variables
linearize the L1 deviation of every triple-colour count from one.  Objective
zero is exactly an invariant matching and is checked semantically before a
certificate is written.  A positive incumbent or backend-local optimum has no
portable nonexistence status.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ortools.linear_solver import pywraplp

from search_cyclic_invariant_matching_local import QUAD_GROUPS, verify_matching
from search_cyclic_invariant_matching_mip import STATUS_NAMES
from verify_fan_kernel_reduction import (
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


def load_hint(path: Path, groups: tuple[tuple[int, ...], ...]) -> set[int]:
    cells = [
        int(line)
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    hinted = set(cells)
    if len(cells) != QUAD_GROUPS or len(hinted) != QUAD_GROUPS:
        raise ValueError(
            f"hint must contain {QUAD_GROUPS} distinct orbit-cell indices"
        )
    if any(len(hinted & set(group)) != 1 for group in groups[:QUAD_GROUPS]):
        raise ValueError("hint is not a one-per-Q-group transversal")
    return hinted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=("SCIP", "HIGHS", "CBC"), default="SCIP")
    parser.add_argument("--seconds", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--log-progress", action="store_true")
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--best-effort", type=Path)
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).with_name("cyclic_invariant_matching.txt"),
    )
    args = parser.parse_args()
    if args.hint is not None and args.backend != "SCIP":
        raise ValueError("warm-start hints are enabled only for the SCIP backend")

    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    solver = pywraplp.Solver.CreateSolver(args.backend)
    if solver is None:
        raise RuntimeError(f"backend {args.backend} is unavailable")
    solver.SetTimeLimit(round(args.seconds * 1000))
    if args.workers and not solver.SetNumThreads(args.workers):
        raise RuntimeError(f"backend {args.backend} rejected worker count")
    if args.log_progress:
        solver.EnableOutput()

    selected = [
        solver.BoolVar(f"selected_{cell}") for cell in range(len(cells))
    ]
    for group_number, group in enumerate(groups[:QUAD_GROUPS]):
        constraint = solver.Constraint(1, 1, f"quad_group_{group_number}")
        for cell in group:
            constraint.SetCoefficient(selected[cell], 1)

    under = []
    over = []
    objective = solver.Objective()
    objective.SetMinimization()
    for index, group in enumerate(groups[QUAD_GROUPS:]):
        below = solver.NumVar(0, 1, f"under_{index}")
        above = solver.NumVar(0, len(group) - 1, f"over_{index}")
        under.append(below)
        over.append(above)
        constraint = solver.Constraint(1, 1, f"tc_group_{index}")
        for cell in group:
            constraint.SetCoefficient(selected[cell], 1)
        constraint.SetCoefficient(below, 1)
        constraint.SetCoefficient(above, -1)
        objective.SetCoefficient(below, 1)
        objective.SetCoefficient(above, 1)

    if args.hint is not None:
        hinted = load_hint(args.hint, groups)
        hint_variables = list(selected)
        hint_values = [int(cell in hinted) for cell in range(len(cells))]
        for group, below, above in zip(
            groups[QUAD_GROUPS:], under, over
        ):
            count = len(hinted & set(group))
            hint_variables.extend((below, above))
            hint_values.extend((max(1 - count, 0), max(count - 1, 0)))
        solver.SetHint(hint_variables, hint_values)

    status = solver.Solve()
    print(f"backend={args.backend}")
    print(f"status={STATUS_NAMES.get(status, f'UNKNOWN_CODE_{status}')}")
    print(f"variables={solver.NumVariables()}")
    print(f"constraints={solver.NumConstraints()}")
    print(f"wall_time={solver.WallTime() / 1000:.6f}")
    print(f"nodes={solver.nodes()}")
    if status not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        print("certificate=NONE")
        print("scope=no feasible soft assignment was returned before timeout")
        return

    chosen = [
        cell
        for cell, variable in enumerate(selected)
        if variable.solution_value() > 0.5
    ]
    chosen_set = set(chosen)
    if len(chosen) != QUAD_GROUPS or any(
        len(chosen_set & set(group)) != 1
        for group in groups[:QUAD_GROUPS]
    ):
        raise AssertionError("MIP incumbent is not a Q-transversal")
    counts = [
        len(chosen_set & set(group)) for group in groups[QUAD_GROUPS:]
    ]
    defect = sum(abs(count - 1) for count in counts)
    print(f"reported_objective={objective.Value():.6f}")
    print(f"semantic_l1_defect={defect}")
    if defect:
        if args.best_effort is not None:
            args.best_effort.write_text(
                "".join(f"{cell}\n" for cell in chosen),
                encoding="ascii",
            )
            print(f"best_effort={args.best_effort}")
        print("certificate=NONE")
        print("scope=positive defect has no matching/nonexistence status")
        return

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
