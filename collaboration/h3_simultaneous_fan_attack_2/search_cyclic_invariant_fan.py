#!/usr/bin/env python3
"""Search the C17-invariant quotient for a simultaneous 13-fan.

This optional search helper uses OR-Tools.  Any SAT result is written as the
2,964-line certificate checked by the standard-library verifier.  UNKNOWN has
no mathematical status.
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--log-progress", action="store_true")
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    args = parser.parse_args()

    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)

    model = cp_model.CpModel()
    labels = [model.new_int_var(0, 12, f"x_{index}") for index in range(len(cells))]
    for group in groups:
        model.add_all_different(labels[cell] for cell in group)

    # The first group is a Q-group.  Global permutation of the thirteen fan
    # labels makes this normalization lossless inside the invariant ansatz.
    for label, cell in enumerate(groups[0]):
        model.add(labels[cell] == label)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = args.log_progress
    status = solver.solve(model)
    status_name = solver.status_name(status)
    print(f"status={status_name}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    print(f"wall_time={solver.wall_time:.6f}")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = [solver.value(label) for label in labels]
        target = set(range(13))
        if any({values[cell] for cell in group} != target for group in groups):
            raise AssertionError("solver assignment failed semantic group check")
        args.certificate.write_text(
            "".join(f"{value}\n" for value in values),
            encoding="ascii",
        )
        print(f"certificate={args.certificate}")
        print("semantic_verification=PASS")
    else:
        print("certificate=NONE")
        print("scope=UNKNOWN or INFEASIBLE is not a portable UNSAT certificate")


if __name__ == "__main__":
    main()
