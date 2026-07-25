#!/usr/bin/env python3
"""Search for a Z_17-equivariant LS(4,5,21) with phase variables.

This is equivalent to ``search_cyclic_ls_4_5_21.py``, but it stores one
F_17-valued phase for each orbit of five-sets and imposes an all-different
constraint on the seventeen extensions of one representative from every
orbit of four-sets.  Translation carries the remaining stars to these
constraints.

Requires OR-Tools.
"""

from __future__ import annotations

import argparse

from ortools.sat.python import cp_model

from search_cyclic_ls_4_5_21 import (
    AFFINE_ANCHOR,
    MODULUS,
    POINTS,
    canonical,
    orbit_representatives,
    verify_solution,
    witness_payload,
    write_json,
)


def build_model() -> tuple[
    cp_model.CpModel,
    tuple[tuple[int, ...], ...],
    dict[tuple[int, ...], cp_model.IntVar],
]:
    five_representatives = orbit_representatives(5)
    four_representatives = orbit_representatives(4)
    assert len(five_representatives) == 1197
    assert len(four_representatives) == 353

    model = cp_model.CpModel()
    phases = {
        representative: model.new_int_var(
            0,
            MODULUS - 1,
            "phase_" + "_".join(map(str, representative)),
        )
        for representative in five_representatives
    }

    for star_number, four_set in enumerate(four_representatives):
        colours = []
        for point in POINTS:
            if point in four_set:
                continue
            five_set = tuple(sorted(four_set + (point,)))
            representative, shift = canonical(five_set)
            colour = model.new_int_var(
                0,
                MODULUS - 1,
                f"colour_{star_number}_{point}",
            )
            model.add_modulo_equality(
                colour,
                phases[representative] + shift,
                MODULUS,
            )
            colours.append(colour)
        assert len(colours) == MODULUS
        model.add_all_different(colours)

    anchor_representative, anchor_shift = canonical(AFFINE_ANCHOR)
    model.add(phases[anchor_representative] + anchor_shift == 0)
    return model, five_representatives, phases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--randomized", action="store_true")
    parser.add_argument("--output", help="write a verified witness as JSON")
    parser.add_argument("--log", action="store_true")
    args = parser.parse_args()

    model, representatives, phases = build_model()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.log_search_progress = args.log
    solver.parameters.random_seed = args.seed
    solver.parameters.randomize_search = args.randomized

    status = solver.solve(model)
    print(f"five-set phase variables: {len(representatives)}")
    print("four-set orbit constraints: 353")
    print(f"seed: {args.seed}")
    print(f"randomized search: {args.randomized}")
    print(f"status: {solver.status_name(status)}")
    print(f"wall time: {solver.wall_time:.3f} seconds")
    print(f"branches: {solver.num_branches}")
    print(f"conflicts: {solver.num_conflicts}")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        phase_values = {
            representative: solver.value(variable)
            for representative, variable in phases.items()
        }
        verify_solution(representatives, phase_values)
        print("verified: cyclic LS(4,5,21) found")
        if args.output:
            write_json(args.output, witness_payload(representatives, phase_values))
            print(f"verified witness written: {args.output}")


if __name__ == "__main__":
    main()
