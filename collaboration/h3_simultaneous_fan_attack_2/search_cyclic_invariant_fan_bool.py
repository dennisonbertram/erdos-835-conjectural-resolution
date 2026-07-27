#!/usr/bin/env python3
"""Search the C17-invariant fan with an exactly-one Boolean CP-SAT model.

This formulation exposes the same 38,532 primary variables as the direct CNF.
Every cell has exactly one fan label, and every group contains every label
exactly once.  OR-Tools 9.15's optional violation-local-search workers are
designed for constraints including exactly-one.  A returned assignment is
checked semantically before any certificate is written.  UNKNOWN has no
mathematical status.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ortools.sat.python import cp_model

from verify_fan_kernel_reduction import (
    CERTIFICATE,
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


LABELS = 13


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--violation-ls-workers", type=int, default=1)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--log-progress", action="store_true")
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    args = parser.parse_args()

    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)

    model = cp_model.CpModel()
    labels = [
        [model.new_bool_var(f"x_{cell}_{label}") for label in range(LABELS)]
        for cell in range(len(cells))
    ]
    for cell_labels in labels:
        model.add_exactly_one(cell_labels)
    for group in groups:
        for label in range(LABELS):
            model.add_exactly_one(labels[cell][label] for cell in group)

    for label, cell in enumerate(groups[0]):
        model.add(labels[cell][label] == 1)

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
        print("scope=UNKNOWN or INFEASIBLE is not a portable UNSAT certificate")
        return

    values = []
    for cell, cell_labels in enumerate(labels):
        selected = [
            label
            for label, variable in enumerate(cell_labels)
            if solver.boolean_value(variable)
        ]
        if len(selected) != 1:
            raise AssertionError(f"solver assignment is not one-hot at cell {cell}")
        values.append(selected[0])
    target = set(range(LABELS))
    if any({values[cell] for cell in group} != target for group in groups):
        raise AssertionError("solver assignment failed semantic group check")
    args.certificate.write_text(
        "".join(f"{value}\n" for value in values),
        encoding="ascii",
    )
    print(f"certificate={args.certificate}")
    print(f"orbit_cells={len(cells)}")
    print("semantic_verification=PASS")


if __name__ == "__main__":
    main()
