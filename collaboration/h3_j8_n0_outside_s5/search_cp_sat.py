#!/usr/bin/env python3
"""Exact CP-SAT search for the exterior-S5-symmetric N=0 model."""

from __future__ import annotations

import argparse
import math

from ortools.sat.python import cp_model

from model import (
    RECURRENCE,
    canonical_representatives,
    cube_cells,
    load_signature,
    orbit_key,
    orbit_keys,
    subset_signature,
)


def linear_form(
    variables: dict[tuple[tuple[int, ...], int], cp_model.IntVar],
    signature: tuple[tuple[tuple[tuple[int, ...], int], int], ...],
) -> cp_model.LinearExpr:
    return sum(coefficient * variables[key] for key, coefficient in signature)


def build_model() -> cp_model.CpModel:
    model = cp_model.CpModel()
    d = {
        key: model.new_int_var(
            0,
            13,
            f"d_{'_'.join(map(str, key[0]))}_o{key[1]}",
        )
        for key in orbit_keys()
    }

    for triple in canonical_representatives(3):
        model.add(linear_form(d, load_signature(triple)) <= 13)

    for size, (modulus, sign, rhs) in RECURRENCE.items():
        for index, subset in enumerate(canonical_representatives(size)):
            total = linear_form(d, subset_signature(subset))
            if sign == 1:
                upper = rhs // modulus
            else:
                upper = (rhs + 13 * math.comb(size, 4)) // modulus
            count = model.new_int_var(0, upper, f"N_{size}_{index}")
            model.add(modulus * count + sign * total == rhs)

    positive, negative = cube_cells()
    model.add(sum(d[orbit_key(block)] for block in negative) == 0)
    model.add(sum(d[orbit_key(block)] for block in positive) == 60)
    return model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    model = build_model()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = 835
    status = solver.solve(model)
    print(f"status: {solver.status_name(status)}")
    print(f"wall_seconds: {solver.wall_time}")
    print(f"branches: {solver.num_branches}")
    print("scope: UNSAT excludes only exterior-S5 symmetry; UNKNOWN proves nothing")


if __name__ == "__main__":
    main()
