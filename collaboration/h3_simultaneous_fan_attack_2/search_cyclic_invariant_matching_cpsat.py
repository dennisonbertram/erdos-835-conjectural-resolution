#!/usr/bin/env python3
"""Search exactly for one C17-invariant perfect matching with CP-SAT.

The model has one Boolean variable per quotient cell and one exactly-one
constraint for each of the 1,140 quotient groups.  A satisfying assignment is
semantically checked and written as 228 selected orbit-cell indices.  UNKNOWN
has no mathematical status, and INFEASIBLE is not treated as portable evidence
without an independently checked proof from a proof-producing solver.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ortools.sat.python import cp_model

from search_cyclic_invariant_matching_local import QUAD_GROUPS, verify_matching
from verify_fan_kernel_reduction import (
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--violation-ls-workers", type=int, default=1)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--log-progress", action="store_true")
    parser.add_argument(
        "--hint",
        type=Path,
        help="optional 228-line best-effort Q-transversal from local search",
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).with_name("cyclic_invariant_matching.txt"),
    )
    args = parser.parse_args()

    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    model = cp_model.CpModel()
    selected = [
        model.new_bool_var(f"selected_{cell}") for cell in range(len(cells))
    ]
    for group in groups:
        model.add_exactly_one(selected[cell] for cell in group)
    if args.hint is not None:
        hinted_cells = [
            int(line)
            for line in args.hint.read_text(encoding="ascii").splitlines()
            if line.strip()
        ]
        if (
            len(hinted_cells) != QUAD_GROUPS
            or len(set(hinted_cells)) != QUAD_GROUPS
        ):
            raise ValueError(
                f"hint must contain {QUAD_GROUPS} distinct orbit-cell indices"
            )
        hinted = set(hinted_cells)
        qgroups = groups[:QUAD_GROUPS]
        if any(len(hinted & set(group)) != 1 for group in qgroups):
            raise ValueError("hint is not a one-per-Q-group transversal")
        for cell, variable in enumerate(selected):
            model.add_hint(variable, int(cell in hinted))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_workers = args.workers
    solver.parameters.num_violation_ls = args.violation_ls_workers
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = args.log_progress
    status = solver.solve(model)
    print(f"status={solver.status_name(status)}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    print(f"wall_time={solver.wall_time:.6f}")
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("certificate=NONE")
        print("scope=UNKNOWN or unproved INFEASIBLE has no mathematical status")
        return

    chosen = [
        cell for cell, variable in enumerate(selected)
        if solver.boolean_value(variable)
    ]
    verify_matching(chosen, groups)
    args.certificate.write_text(
        "".join(f"{cell}\n" for cell in chosen),
        encoding="ascii",
    )
    print(f"certificate={args.certificate}")
    print(f"selected_orbit_cells={len(chosen)}")
    print("semantic_verification=PASS")
    print("scope=one invariant matching only; not a 13-fan or #835 solution")


if __name__ == "__main__":
    main()
