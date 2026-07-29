#!/usr/bin/env python3
"""Search exact weighted matching obstructions for target K13 supports.

For nonnegative edge weights w, any completion must satisfy

    sum_c min{w(M): M perfect matching of K[V_c]} <= sum_e w(e).

For a fixed integer weight vector and histogram, this script maximizes the
left side over every support-admissible multiset by CP-SAT.  A strict
violation is an exact certificate that the printed support family has no
completion.  It does not establish partial-factorization or fan realization.
"""

from __future__ import annotations

import argparse
import functools
import itertools
import json
import random

from ortools.sat.python import cp_model


N = 13
ALL_EDGES = tuple(itertools.combinations(range(N), 2))


def cardinality(mask):
    return bin(mask).count("1")


def support_histogram(q):
    return {8: q + 7, 10: 10 - 2 * q, 12: q}


def minimum_matching_costs(weights):
    weights = {
        tuple(sorted(edge)): int(weight)
        for edge, weight in weights.items()
    }

    @functools.cache
    def minimum_perfect_matching(mask):
        if mask == 0:
            return 0
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        rest = mask ^ first_bit
        best = None
        choices = rest
        while choices:
            partner_bit = choices & -choices
            choices ^= partner_bit
            partner = partner_bit.bit_length() - 1
            value = (
                weights[tuple(sorted((first, partner)))]
                + minimum_perfect_matching(rest ^ partner_bit)
            )
            best = value if best is None else min(best, value)
        assert best is not None
        return best

    return {
        mask: minimum_perfect_matching(mask)
        for size in (8, 10, 12)
        for vertices in itertools.combinations(range(N), size)
        for mask in [sum(1 << vertex for vertex in vertices)]
    }


def maximize_weighted_demand(weights, q, seconds):
    costs = minimum_matching_costs(weights)
    histogram = support_histogram(q)
    model = cp_model.CpModel()
    choices = {}
    for mask in costs:
        size = cardinality(mask)
        if histogram[size]:
            choices[mask] = model.new_int_var(
                0, histogram[size], f"count_{mask}"
            )
    for size, count in histogram.items():
        model.add(
            sum(
                variable
                for mask, variable in choices.items()
                if cardinality(mask) == size
            )
            == count
        )
    for vertex in range(N):
        model.add(
            sum(
                variable
                for mask, variable in choices.items()
                if mask & (1 << vertex)
            )
            == 12
        )
    model.maximize(
        sum(costs[mask] * variable for mask, variable in choices.items())
    )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    status = solver.solve(model)
    status_name = solver.status_name(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return status_name, None, None
    supports = [
        [vertex for vertex in range(N) if mask & (1 << vertex)]
        for mask, variable in choices.items()
        for _ in range(solver.value(variable))
    ]
    return status_name, round(solver.objective_value), supports


def weight_cases(rng, count, maximum):
    # Deterministic structured controls.
    yield "uniform", {edge: 1 for edge in ALL_EDGES}
    for split in (1, 2, 3, 4, 5, 6):
        yield (
            f"two_level_cut_{split}",
            {
                edge: (
                    7
                    if (edge[0] < split) != (edge[1] < split)
                    else 1
                )
                for edge in ALL_EDGES
            },
        )
    for index in range(count):
        yield (
            f"random_{index}",
            {
                edge: rng.randrange(maximum + 1)
                for edge in ALL_EDGES
            },
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--random", type=int, default=100)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--max-weight", type=int, default=100)
    parser.add_argument("--seconds", type=float, default=3.0)
    parser.add_argument(
        "--q",
        type=int,
        action="append",
        choices=range(6),
        help="only run this histogram q=n_12; repeatable",
    )
    args = parser.parse_args()
    rng = random.Random(args.seed)
    q_values = args.q if args.q is not None else range(6)

    checked = 0
    statuses = {}
    best = None
    for name, weights in weight_cases(
        rng, args.random, args.max_weight
    ):
        capacity = sum(weights.values())
        for q in q_values:
            status, demand, supports = maximize_weighted_demand(
                weights, q, args.seconds
            )
            checked += 1
            statuses[status] = statuses.get(status, 0) + 1
            if demand is None:
                print(f"name={name} q={q} status={status}", flush=True)
                continue
            slack = capacity - demand
            if best is None or slack < best[0]:
                best = (slack, name, q, capacity, demand, status)
                print(
                    f"best name={name} q={q} sum_w={capacity} "
                    f"demand={demand} slack={slack} status={status}",
                    flush=True,
                )
            if demand > capacity:
                certificate = {
                    "scope": (
                        "arbitrary target support-admissible matrix; "
                        "not partial- or fan-realizable"
                    ),
                    "name": name,
                    "q": q,
                    "status": status,
                    "weights": [
                        [left, right, weights[left, right]]
                        for left, right in ALL_EDGES
                    ],
                    "sum_weights": capacity,
                    "minimum_matching_cost_sum": demand,
                    "supports": supports,
                }
                print("WEIGHTED_COUNTEREXAMPLE")
                print(json.dumps(certificate, sort_keys=True))
                return 2
    print(
        f"checked={checked} statuses={statuses} best={best}; "
        "no weighted violation found"
    )
    print("finite search only; no universal or fan conclusion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
