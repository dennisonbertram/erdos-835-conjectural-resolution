#!/usr/bin/env python3
"""Search matching-capacity inequalities over arbitrary target supports.

For an edge set F of K13 and a colour support V, every perfect matching on
V uses at least |V|/2 - nu(K[V] - F) edges of F.  Since the colour matchings
must be edge-disjoint, the sum of these deficiencies cannot exceed |F|.

The search maximizes that sum over all 13x17 support matrices with row sum
12 and column sizes 8, 10, or 12.  A strict violation is an exact
non-completability certificate for the broad arbitrary-support class.  It
does not by itself establish partial-factorization or fan realizability.
"""

from __future__ import annotations

import argparse
import functools
import itertools
import random

from ortools.sat.python import cp_model


N = 13
ALL_EDGES = tuple(itertools.combinations(range(N), 2))


def support_histogram(q):
    return {8: q + 7, 10: 10 - 2 * q, 12: q}


def cardinality(mask):
    return bin(mask).count("1")


def matching_deficiencies(forbidden):
    forbidden = {tuple(sorted(edge)) for edge in forbidden}

    @functools.cache
    def maximum_matching(mask):
        if mask == 0:
            return 0
        v_bit = mask & -mask
        v = v_bit.bit_length() - 1
        rest = mask ^ v_bit
        best = maximum_matching(rest)
        choices = rest
        while choices:
            u_bit = choices & -choices
            choices ^= u_bit
            u = u_bit.bit_length() - 1
            if (min(u, v), max(u, v)) not in forbidden:
                best = max(
                    best,
                    1 + maximum_matching(rest ^ u_bit),
                )
        return best

    deficiencies = {}
    for size in (8, 10, 12):
        for vertices in itertools.combinations(range(N), size):
            mask = sum(1 << vertex for vertex in vertices)
            deficiencies[mask] = size // 2 - maximum_matching(mask)
    return deficiencies


def maximize_violation(forbidden, q, seconds):
    deficiencies = matching_deficiencies(forbidden)
    histogram = support_histogram(q)
    model = cp_model.CpModel()
    choices = {}
    for mask, deficiency in deficiencies.items():
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
    objective = sum(
        deficiencies[mask] * variable
        for mask, variable in choices.items()
    )
    model.maximize(objective)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.status_name(status), None, None
    supports = [
        [vertex for vertex in range(N) if mask & (1 << vertex)]
        for mask, variable in choices.items()
        for _ in range(solver.value(variable))
    ]
    return solver.status_name(status), round(solver.objective_value), supports


def structured_edge_sets():
    yielded = set()

    def emit(name, edges):
        frozen = frozenset(tuple(sorted(edge)) for edge in edges)
        if frozen not in yielded:
            yielded.add(frozen)
            return name, frozen
        return None

    for size in range(1, N):
        result = emit(
            f"cut_{size}_{N-size}",
            (
                (a, b)
                for a in range(size)
                for b in range(size, N)
            ),
        )
        if result:
            yield result
    for size in range(2, N + 1):
        result = emit(
            f"clique_{size}",
            itertools.combinations(range(size), 2),
        )
        if result:
            yield result
    for size in range(1, N):
        result = emit(
            f"incident_{size}",
            (
                edge
                for edge in ALL_EDGES
                if edge[0] < size or edge[1] < size
            ),
        )
        if result:
            yield result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--random", type=int, default=100)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--seconds", type=float, default=2.0)
    parser.add_argument(
        "--case",
        action="append",
        help="only run structured cases with this exact name; repeatable",
    )
    parser.add_argument(
        "--q",
        type=int,
        action="append",
        choices=range(6),
        help="only run this support histogram q=n_12; repeatable",
    )
    args = parser.parse_args()
    rng = random.Random(args.seed)

    cases = list(structured_edge_sets())
    if args.case:
        wanted = set(args.case)
        cases = [case for case in cases if case[0] in wanted]
        missing = wanted - {name for name, _ in cases}
        if missing:
            parser.error(f"unknown structured cases: {sorted(missing)}")
    for index in range(args.random):
        probability = rng.uniform(0.05, 0.95)
        edges = frozenset(
            edge for edge in ALL_EDGES if rng.random() < probability
        )
        cases.append((f"random_{index}_p{probability:.3f}", edges))

    checked = 0
    status_counts = {}
    best_slack = None
    best_summary = None
    q_values = args.q if args.q is not None else range(6)
    for name, forbidden in cases:
        for q in q_values:
            status, demand, supports = maximize_violation(
                forbidden, q, args.seconds
            )
            checked += 1
            status_counts[status] = status_counts.get(status, 0) + 1
            if demand is None:
                print(f"name={name} q={q} status={status}")
                continue
            slack = len(forbidden) - demand
            if best_slack is None or slack < best_slack:
                best_slack = slack
                best_summary = (name, q, len(forbidden), demand, status)
                print(
                    f"best name={name} q={q} |F|={len(forbidden)} "
                    f"demand={demand} slack={slack} status={status}",
                    flush=True,
                )
            if demand > len(forbidden):
                print(
                    f"COUNTEREXAMPLE name={name} q={q} "
                    f"|F|={len(forbidden)} demand={demand}"
                )
                print(f"F={sorted(forbidden)}")
                print(f"supports={supports}")
                return 2
    print(
        f"checked={checked} statuses={status_counts} best={best_summary} "
        "no matching-capacity violation found"
    )
    print("this finite sample is not a universal completion theorem")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
