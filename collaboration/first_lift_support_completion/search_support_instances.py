#!/usr/bin/env python3
"""Exploratory exact search for K13 prescribed-support completions.

This script deliberately distinguishes arbitrary degree-compatible support
matrices from support matrices known to arise from a five-row partial
one-factorization.  It currently searches only the former class.

An INFEASIBLE completion result is a candidate counterexample and must be
converted to a proof-producing CNF before being cited as a theorem.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from ortools.sat.python import cp_model


N_VERTICES = 13
N_COLOURS = 17


def support_sizes(q):
    """Return the possible (8,10,12)-support histogram indexed by q=n_12."""

    return [8] * (q + 7) + [10] * (10 - 2 * q) + [12] * q


def random_support_matrix(q, rng, seconds):
    sizes = support_sizes(q)
    assert len(sizes) == N_COLOURS and sum(sizes) == 156
    model = cp_model.CpModel()
    support = {
        (a, colour): model.new_bool_var(f"s_{a}_{colour}")
        for a in range(N_VERTICES)
        for colour in range(N_COLOURS)
    }
    for a in range(N_VERTICES):
        model.add(sum(support[a, c] for c in range(N_COLOURS)) == 12)
    for c, size in enumerate(sizes):
        model.add(sum(support[a, c] for a in range(N_VERTICES)) == size)

    # A fresh random linear objective samples vertices of the support
    # polytope rather than repeatedly returning the same canonical matrix.
    weights = {
        key: rng.randrange(-1_000_000, 1_000_001)
        for key in support
    }
    model.maximize(sum(weights[key] * var for key, var in support.items()))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = rng.randrange(1, 2**31)
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, solver.status_name(status)
    supports = [
        [a for a in range(N_VERTICES) if solver.value(support[a, c])]
        for c in range(N_COLOURS)
    ]
    return supports, solver.status_name(status)


def completion_status(supports, seconds):
    model = cp_model.CpModel()
    edges = [
        (a, b)
        for a in range(N_VERTICES)
        for b in range(a + 1, N_VERTICES)
    ]
    allowed = {
        (a, b, c): model.new_bool_var(f"x_{a}_{b}_{c}")
        for a, b in edges
        for c in range(N_COLOURS)
        if a in supports[c] and b in supports[c]
    }
    for a, b in edges:
        variables = [
            allowed[a, b, c]
            for c in range(N_COLOURS)
            if (a, b, c) in allowed
        ]
        if not variables:
            return "INFEASIBLE", None
        model.add(sum(variables) == 1)
    for c, vertices in enumerate(supports):
        for a in vertices:
            model.add(
                sum(
                    allowed[min(a, b), max(a, b), c]
                    for b in vertices
                    if b != a
                )
                == 1
            )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.status_name(status), None
    colouring = {
        f"{a}-{b}": c
        for a, b in edges
        for c in range(N_COLOURS)
        if (a, b, c) in allowed and solver.value(allowed[a, b, c])
    }
    assert len(colouring) == 78
    return solver.status_name(status), colouring


def partial_factorization_status(supports, seconds):
    """Test realization by a proper colouring of K18-K13."""

    P = range(5)
    A = range(N_VERTICES)
    missing = {
        (a, c)
        for a in A
        for c in range(N_COLOURS)
        if a not in supports[c]
    }
    model = cp_model.CpModel()
    cross = {
        (p, a, c): model.new_bool_var(f"z_{p}_{a}_{c}")
        for a, c in missing
        for p in P
    }
    internal_edges = tuple(
        (p, q) for p in P for q in P if p < q
    )
    internal = {
        (p, q, c): model.new_bool_var(f"y_{p}_{q}_{c}")
        for p, q in internal_edges
        for c in range(N_COLOURS)
    }
    for a, c in missing:
        model.add(sum(cross[p, a, c] for p in P) == 1)
    for p in P:
        for a in A:
            model.add(
                sum(
                    cross[p, a, c]
                    for c in range(N_COLOURS)
                    if (a, c) in missing
                )
                == 1
            )
    for p, q in internal_edges:
        model.add(
            sum(internal[p, q, c] for c in range(N_COLOURS)) == 1
        )
    for p in P:
        for c in range(N_COLOURS):
            model.add(
                sum(
                    cross[p, a, c]
                    for a in A
                    if (a, c) in missing
                )
                + sum(
                    internal[min(p, q), max(p, q), c]
                    for q in P
                    if q != p
                )
                == 1
            )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    status = solver.solve(model)
    return solver.status_name(status)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--support-seconds", type=float, default=1.0)
    parser.add_argument("--completion-seconds", type=float, default=5.0)
    parser.add_argument(
        "--test-partial",
        action="store_true",
        help="also test realization by a proper K18-K13 colouring",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    counts = {}
    for sample in range(args.samples):
        q = sample % 6
        supports, support_status = random_support_matrix(
            q, rng, args.support_seconds
        )
        if supports is None:
            key = f"SUPPORT_{support_status}"
            counts[key] = counts.get(key, 0) + 1
            continue
        status, colouring = completion_status(
            supports, args.completion_seconds
        )
        counts[status] = counts.get(status, 0) + 1
        if args.test_partial:
            partial = partial_factorization_status(
                supports, args.completion_seconds
            )
            partial_key = f"PARTIAL_{partial}"
            counts[partial_key] = counts.get(partial_key, 0) + 1
            if partial == "INFEASIBLE":
                print(
                    f"NON_PARTIAL sample={sample} q={q} "
                    f"supports={supports}"
                )
                print(f"counts={counts}")
                return 3
        if status == "INFEASIBLE":
            certificate = {
                "scope": "arbitrary even support matrix, not fan-realizable",
                "seed": args.seed,
                "sample": sample,
                "q": q,
                "support_sizes": support_sizes(q),
                "supports": supports,
            }
            if args.output:
                args.output.write_text(
                    json.dumps(certificate, indent=2) + "\n",
                    encoding="utf-8",
                )
            print(json.dumps(certificate, sort_keys=True))
            print(f"counts={counts}")
            return 2
        if status == "UNKNOWN":
            print(
                f"sample={sample} q={q} completion=UNKNOWN; "
                "not counted as a counterexample"
            )
    print(
        f"scope=arbitrary-even-supports samples={args.samples} "
        f"seed={args.seed} counts={counts}"
    )
    print("no universal theorem or fan-realizable conclusion is claimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
