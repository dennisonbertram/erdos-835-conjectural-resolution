#!/usr/bin/env python3
"""Sample five-saturated-vertex partial K18 one-factorizations.

Unlike search_support_instances.py, every generated instance is a genuine
proper 17-edge-colouring of K18-K13: the five vertices outside the hole are
saturated.  The cross edges are generated independently of any known full
one-factorization, so completion is not built in.

SAT samples are evidence only.  UNSAT must be certified independently before
being cited as a theorem, and neither outcome establishes fan realizability.
"""

from __future__ import annotations

import argparse
import itertools
import random

from ortools.sat.python import cp_model

from search_support_instances import completion_status


P_SIZE = 5
A_SIZE = 13
N_COLOURS = 17
P_EDGES = tuple(itertools.combinations(range(P_SIZE), 2))


def random_internal_colouring(q, rng, seconds):
    """Properly colour K5 with q double-edge colour classes."""

    sizes = [2] * q + [1] * (10 - 2 * q) + [0] * (7 + q)
    assert len(sizes) == N_COLOURS and sum(sizes) == 10
    model = cp_model.CpModel()
    x = {
        (edge, colour): model.new_bool_var(
            f"x_{edge[0]}_{edge[1]}_{colour}"
        )
        for edge in P_EDGES
        for colour in range(N_COLOURS)
    }
    for edge in P_EDGES:
        model.add(sum(x[edge, c] for c in range(N_COLOURS)) == 1)
    for colour, size in enumerate(sizes):
        model.add(sum(x[edge, colour] for edge in P_EDGES) == size)
    for vertex in range(P_SIZE):
        for colour in range(N_COLOURS):
            model.add(
                sum(
                    x[edge, colour]
                    for edge in P_EDGES
                    if vertex in edge
                )
                <= 1
            )
    weights = {
        key: rng.randrange(-1_000_000, 1_000_001)
        for key in x
    }
    model.maximize(sum(weights[key] * variable for key, variable in x.items()))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = rng.randrange(1, 2**31)
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, solver.status_name(status)
    return {
        edge: next(
            colour
            for colour in range(N_COLOURS)
            if solver.value(x[edge, colour])
        )
        for edge in P_EDGES
    }, solver.status_name(status)


def randomized_perfect_matching(columns, colours, allowed, rng):
    """Kuhn augmenting paths with randomized orders."""

    colour_to_column = {}

    def augment(column, seen):
        options = list(colours)
        rng.shuffle(options)
        for colour in options:
            if colour in seen or not allowed(column, colour):
                continue
            seen.add(colour)
            if (
                colour not in colour_to_column
                or augment(colour_to_column[colour], seen)
            ):
                colour_to_column[colour] = column
                return True
        return False

    order = list(columns)
    rng.shuffle(order)
    for column in order:
        if not augment(column, set()):
            return None
    return {
        column: colour
        for colour, column in colour_to_column.items()
    }


def random_cross_colouring(internal, rng, attempts):
    forbidden_at_p = {
        p: {
            colour
            for edge, colour in internal.items()
            if p in edge
        }
        for p in range(P_SIZE)
    }
    assert all(len(values) == 4 for values in forbidden_at_p.values())
    for _ in range(attempts):
        used_at_a = {a: set() for a in range(A_SIZE)}
        cross = {}
        rows = list(range(P_SIZE))
        rng.shuffle(rows)
        success = True
        for p in rows:
            available = [
                colour
                for colour in range(N_COLOURS)
                if colour not in forbidden_at_p[p]
            ]
            matching = randomized_perfect_matching(
                range(A_SIZE),
                available,
                lambda a, colour: colour not in used_at_a[a],
                rng,
            )
            if matching is None:
                success = False
                break
            for a, colour in matching.items():
                cross[p, a] = colour
                used_at_a[a].add(colour)
        if success:
            assert len(cross) == 65
            return cross
    return None


def supports_from_partial(internal, cross):
    supports = []
    for colour in range(N_COLOURS):
        missing_a = {
            a
            for p in range(P_SIZE)
            for a in range(A_SIZE)
            if cross[p, a] == colour
        }
        support = sorted(set(range(A_SIZE)) - missing_a)
        internal_count = sum(value == colour for value in internal.values())
        assert len(missing_a) == 5 - 2 * internal_count
        assert len(support) == 8 + 2 * internal_count
        supports.append(support)
    assert all(
        sum(a in support for support in supports) == 12
        for a in range(A_SIZE)
    )
    return supports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--internal-seconds", type=float, default=1.0)
    parser.add_argument("--cross-attempts", type=int, default=20)
    parser.add_argument("--completion-seconds", type=float, default=5.0)
    args = parser.parse_args()
    rng = random.Random(args.seed)

    counts = {}
    for sample in range(args.samples):
        q = sample % 6
        internal, status = random_internal_colouring(
            q, rng, args.internal_seconds
        )
        if internal is None:
            key = f"INTERNAL_{status}"
            counts[key] = counts.get(key, 0) + 1
            continue
        cross = random_cross_colouring(
            internal, rng, args.cross_attempts
        )
        if cross is None:
            counts["CROSS_FAILED"] = counts.get("CROSS_FAILED", 0) + 1
            continue
        supports = supports_from_partial(internal, cross)
        completion, _ = completion_status(
            supports, args.completion_seconds
        )
        counts[completion] = counts.get(completion, 0) + 1
        if completion == "INFEASIBLE":
            print(
                f"CANDIDATE sample={sample} q={q} "
                f"internal={internal} cross={cross} supports={supports}"
            )
            print(f"counts={counts}")
            return 2
        if completion == "UNKNOWN":
            print(
                f"sample={sample} q={q} completion=UNKNOWN; "
                "not counted as a counterexample"
            )
    print(
        f"scope=proper-K18-minus-K13 samples={args.samples} "
        f"seed={args.seed} counts={counts}"
    )
    print("no universal theorem or fan-realizable conclusion is claimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
