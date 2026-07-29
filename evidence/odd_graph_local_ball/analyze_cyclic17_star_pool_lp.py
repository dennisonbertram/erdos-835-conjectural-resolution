#!/usr/bin/env python3
"""Solve the finite retained-row set-packing LP for one cyclic-17 star.

This is diagnostic only: a bound below 14 applies only to the supplied
finite row pool.  A global obstruction would additionally require certified
weighted exact-row pricing for every one of the fourteen labels.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


P = 17
ORBITS = 40


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pool", type=Path)
    parser.add_argument("--include-solution", action="store_true")
    args = parser.parse_args()

    payload = json.loads(args.pool.read_text(encoding="utf-8"))
    keys = sorted(
        payload,
        key=lambda key: tuple(map(int, key.split(","))),
    )
    if len(keys) != 14:
        raise ValueError("expected fourteen incident-pair pools")

    # The first fourteen constraints choose at most one row for each label.
    # The remaining 40*17 constraints are phase slots; forbidden slots simply
    # receive no coefficients.
    rows = []
    columns = []
    data = []
    variable_meta = []
    variable = 0
    for label, key in enumerate(keys):
        if not payload[key]:
            raise ValueError(f"empty pool {key}")
        for candidate_index, phases in enumerate(payload[key]):
            if (
                len(phases) != ORBITS
                or not all(
                    isinstance(phase, int) and 0 <= phase < P
                    for phase in phases
                )
            ):
                raise ValueError(f"invalid row in pool {key}")
            rows.append(label)
            columns.append(variable)
            data.append(1.0)
            for orbit, phase in enumerate(phases):
                rows.append(14 + orbit * P + phase)
                columns.append(variable)
                data.append(1.0)
            variable_meta.append((key, candidate_index))
            variable += 1

    constraint_count = 14 + ORBITS * P
    matrix = coo_matrix(
        (data, (rows, columns)),
        shape=(constraint_count, variable),
    ).tocsr()
    result = linprog(
        -np.ones(variable),
        A_ub=matrix,
        b_ub=np.ones(constraint_count),
        bounds=(0.0, None),
        method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)

    positive = [
        {
            "pair": variable_meta[index][0],
            "candidate": variable_meta[index][1],
            "value": float(value),
        }
        for index, value in enumerate(result.x)
        if value > 1e-9
    ]
    dual = -result.ineqlin.marginals
    dual_slack = matrix.transpose().dot(dual) - 1.0
    if dual_slack.min(initial=0.0) < -1e-7:
        raise AssertionError("floating dual is not feasible for the pool")
    print(
        json.dumps(
            {
                "status": "OPTIMAL_FINITE_POOL_LP",
                "pool": str(args.pool),
                "variables": variable,
                "constraints": constraint_count,
                "objective": float(-result.fun),
                "positive_variables": len(positive),
                "minimum_pool_dual_slack": float(
                    dual_slack.min(initial=0.0)
                ),
                "label_dual_sum": float(dual[:14].sum()),
                "slot_dual_sum": float(dual[14:].sum()),
                "scope": (
                    "finite retained row pool only; not a global star bound"
                ),
                "pricing_required_for_global_bound": True,
                **(
                    {"positive_solution": positive}
                    if args.include_solution
                    else {}
                ),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
