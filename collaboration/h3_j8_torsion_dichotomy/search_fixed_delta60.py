#!/usr/bin/env python3
"""Exact CP-SAT model for the unresolved fixed-Delta=60 j=8 branch.

A FEASIBLE result is only a recurrence/local-capacity countermodel, not a
tower or colouring.  UNKNOWN has no mathematical force.
"""

from __future__ import annotations

import argparse
import itertools
import math

from ortools.sat.python import cp_model


V = tuple(range(13))
FOUR_SETS = tuple(itertools.combinations(V, 4))
INDEX = {q: i for i, q in enumerate(FOUR_SETS)}


def independent_original_sets(size: int, prime: int) -> list[tuple[int, ...]]:
    """Select original incidence rows forming a row-space basis over F_p."""
    pivots: dict[int, dict[int, int]] = {}
    selected: list[tuple[int, ...]] = []
    for s in itertools.combinations(V, size):
        row = {INDEX[q]: 1 for q in itertools.combinations(s, 4)}
        while row:
            pivot = min(row)
            lead = row[pivot]
            if pivot not in pivots:
                inverse = pow(lead, -1, prime)
                row = {
                    column: (value * inverse) % prime
                    for column, value in row.items()
                    if value % prime
                }
                pivots[pivot] = row
                selected.append(s)
                break
            base = pivots[pivot]
            for column, value in base.items():
                new_value = (row.get(column, 0) - lead * value) % prime
                if new_value:
                    row[column] = new_value
                else:
                    row.pop(column, None)
    return selected


def build_model() -> tuple[
    cp_model.CpModel,
    dict[tuple[int, ...], cp_model.IntVar],
    list[tuple[int, ...]],
    list[tuple[int, ...]],
]:
    model = cp_model.CpModel()
    e = {
        q: model.NewIntVar(-1, 12, f"e_{'_'.join(map(str, q))}")
        for q in FOUR_SETS
    }

    for triple in itertools.combinations(V, 3):
        model.Add(
            sum(e[q] for q in FOUR_SETS if set(triple).issubset(q)) <= 3
        )

    # Recurrence nonnegativity at size 5:
    # 2*N_S + sum_{Q subset S} d_Q = 13, with d=e+1.
    # The parity constraints alone are not sufficient.
    for s in itertools.combinations(V, 5):
        model.Add(sum(e[q] for q in itertools.combinations(s, 4)) <= 8)

    constraint_sets: list[tuple[tuple[int, ...], int]] = []
    for size, prime in ((5, 2), (6, 3), (8, 5), (10, 7)):
        basis = independent_original_sets(size, prime)
        constraint_sets.extend((s, prime) for s in basis)

    # The non-field rings must retain their full row sets.
    constraint_sets.extend((s, 4) for s in itertools.combinations(V, 7))
    constraint_sets.extend((s, 8) for s in itertools.combinations(V, 11))

    for s, modulus in constraint_sets:
        terms = [e[q] for q in itertools.combinations(s, 4)]
        lower = -len(terms)
        upper = 12 * len(terms)
        quotient = model.NewIntVar(
            math.floor(lower / modulus) - 1,
            math.ceil(upper / modulus) + 1,
            f"k_{modulus}_{'_'.join(map(str, s))}",
        )
        model.Add(sum(terms) == modulus * quotient)

    # The q=6 rows are implied modulo 2 by M5 and modulo 3 by M6.
    pairs = ((0, 1), (2, 3), (4, 5), (6, 7))
    positive: list[tuple[int, ...]] = []
    negative: list[tuple[int, ...]] = []
    for bits in itertools.product((0, 1), repeat=4):
        q = tuple(sorted(pairs[i][bits[i]] for i in range(4)))
        (positive if sum(bits) % 2 == 0 else negative).append(q)
    model.Add(
        sum(e[q] for q in positive) - sum(e[q] for q in negative) == 60
    )
    # Solver-free Q4 neighborhood argument from NOTE.md.
    model.Add(sum(e[q] + 1 for q in negative) <= 20)

    # The sign-preserving cube group is transitive on positive cells.
    reference_positive = (0, 2, 4, 6)
    for q in positive:
        model.Add(e[reference_positive] >= e[q])
    # Its stabilizer permutes the four coordinate directions.
    adjacent_negative = [
        (1, 2, 4, 6),
        (0, 3, 4, 6),
        (0, 2, 5, 6),
        (0, 2, 4, 7),
    ]
    for first, second in zip(adjacent_negative, adjacent_negative[1:]):
        model.Add(e[first] >= e[second])

    # The exterior S5 action permits this ordering without loss.
    for first, second in zip(range(8, 12), range(9, 13)):
        model.Add(e[(0, 2, 4, first)] >= e[(0, 2, 4, second)])

    model.AddDecisionStrategy(
        [e[q] for q in positive],
        cp_model.CHOOSE_FIRST,
        cp_model.SELECT_MAX_VALUE,
    )
    model.AddDecisionStrategy(
        [e[q] for q in negative],
        cp_model.CHOOSE_FIRST,
        cp_model.SELECT_MIN_VALUE,
    )
    return model, e, positive, negative


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()

    model, e, positive, negative = build_model()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.randomize_search = True
    status = solver.Solve(model)

    print("status:", solver.StatusName(status))
    print("wall_seconds:", solver.WallTime())
    print("branches:", solver.NumBranches())
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = {q: solver.Value(variable) for q, variable in e.items()}
        delta = (
            sum(values[q] for q in positive)
            - sum(values[q] for q in negative)
        )
        assert delta == 60
        print("delta:", delta)
        print(
            "nonzero:",
            {str(q): value for q, value in values.items() if value},
        )
        print("scope: recurrence/local-capacity countermodel only")
    else:
        print("scope: UNKNOWN proves nothing; INFEASIBLE would eliminate this model")


if __name__ == "__main__":
    main()
