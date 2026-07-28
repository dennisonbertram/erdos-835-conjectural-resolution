#!/usr/bin/env python3
"""Exact Gurobi search for the exterior-S5-symmetric N=0 model."""

from __future__ import annotations

import argparse

import gurobipy as gp
from gurobipy import GRB

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
    variables: dict[tuple[tuple[int, ...], int], gp.Var],
    signature: tuple[tuple[tuple[tuple[int, ...], int], int], ...],
) -> gp.LinExpr:
    return gp.quicksum(
        coefficient * variables[key] for key, coefficient in signature
    )


def build_model() -> gp.Model:
    model = gp.Model("j8_n0_exterior_s5")
    d = {
        key: model.addVar(
            vtype=GRB.INTEGER,
            lb=0,
            ub=13,
            name=f"d_{'_'.join(map(str, key[0]))}_o{key[1]}",
        )
        for key in orbit_keys()
    }

    for index, triple in enumerate(canonical_representatives(3)):
        model.addConstr(
            linear_form(d, load_signature(triple)) <= 13,
            name=f"load_{index}",
        )

    for size, (modulus, sign, rhs) in RECURRENCE.items():
        for index, subset in enumerate(canonical_representatives(size)):
            count = model.addVar(
                vtype=GRB.INTEGER,
                lb=0,
                name=f"N_{size}_{index}",
            )
            model.addConstr(
                modulus * count
                + sign * linear_form(d, subset_signature(subset))
                == rhs,
                name=f"recurrence_{size}_{index}",
            )

    positive, negative = cube_cells()
    model.addConstr(
        gp.quicksum(d[orbit_key(block)] for block in negative) == 0,
        name="negative_cube_mass",
    )
    model.addConstr(
        gp.quicksum(d[orbit_key(block)] for block in positive) == 60,
        name="positive_cube_mass",
    )
    return model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--iis")
    args = parser.parse_args()

    model = build_model()
    model.Params.TimeLimit = args.seconds
    model.Params.Threads = args.threads
    model.optimize()
    names = {
        GRB.OPTIMAL: "OPTIMAL",
        GRB.INFEASIBLE: "INFEASIBLE",
        GRB.TIME_LIMIT: "TIME_LIMIT",
    }
    print(f"status: {names.get(model.Status, model.Status)}")
    print(f"runtime_seconds: {model.Runtime}")
    print(f"solution_count: {model.SolCount}")
    print(f"rows: {model.NumConstrs}")
    print(f"columns: {model.NumVars}")
    if model.Status == GRB.INFEASIBLE and args.iis:
        model.computeIIS()
        model.write(args.iis)
        print(f"iis: {args.iis}")
    print("scope: UNSAT excludes only exterior-S5 symmetry; TIME_LIMIT proves nothing")


if __name__ == "__main__":
    main()
