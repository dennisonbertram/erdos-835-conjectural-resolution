#!/usr/bin/env python3
"""Exact rank-reduced Gurobi search for one-fixed-exterior/S4 branches."""

from __future__ import annotations

import argparse
import itertools

import gurobipy as gp
from gurobipy import GRB


V = tuple(range(13))
CUBE = tuple(range(8))
FIXED = (8,)
SYMMETRIC = tuple(range(9, 13))
PAIRS = ((0, 1), (2, 3), (4, 5), (6, 7))
RECURRENCE = {
    5: (2, 1, 13),
    6: (3, -1, 39),
    7: (4, 1, 195),
    8: (5, -1, 325),
    9: (6, 1, 702),
    10: (7, -1, 546),
    11: (8, 1, 858),
}


def key(block):
    cube_part = tuple(x for x in block if x in CUBE)
    fixed_part = tuple(x for x in block if x in FIXED)
    symmetric_count = sum(x in SYMMETRIC for x in block)
    return cube_part, fixed_part, symmetric_count


def representatives(size):
    for fixed_count in range(2):
        fixed_part = FIXED[:fixed_count]
        for symmetric_count in range(5):
            cube_count = size - fixed_count - symmetric_count
            if 0 <= cube_count <= 8:
                symmetric_part = SYMMETRIC[:symmetric_count]
                for cube_part in itertools.combinations(CUBE, cube_count):
                    yield tuple(sorted((*cube_part, *fixed_part, *symmetric_part)))


def cube_cells():
    positive = []
    negative = []
    for bits in itertools.product((0, 1), repeat=4):
        block = tuple(sorted(PAIRS[i][bits[i]] for i in range(4)))
        (positive if sum(bits) % 2 == 0 else negative).append(block)
    return positive, negative


def independent_rows_mod_prime(rows, key_index, prime):
    pivots = {}
    selected = set()
    for index, subset in enumerate(rows):
        row = {}
        for block in itertools.combinations(subset, 4):
            column = key_index[key(block)]
            coefficient = (row.get(column, 0) + 1) % prime
            if coefficient:
                row[column] = coefficient
            else:
                row.pop(column, None)
        while row:
            pivot = min(row)
            if pivot in pivots:
                multiplier = row[pivot]
                for column, coefficient in pivots[pivot].items():
                    value = (
                        row.get(column, 0) - multiplier * coefficient
                    ) % prime
                    if value:
                        row[column] = value
                    else:
                        row.pop(column, None)
            else:
                inverse = pow(row[pivot], -1, prime)
                pivots[pivot] = {
                    column: coefficient * inverse % prime
                    for column, coefficient in row.items()
                }
                selected.add(index)
                break
    return selected


def build_model(args):
    model = gp.Model("j8_n0_one_fixed_exterior_s4")
    model.Params.TimeLimit = args.seconds
    model.Params.Threads = args.threads
    model.Params.MIPFocus = 3
    model.Params.Heuristics = 0
    model.Params.Symmetry = 2

    keys = sorted({key(block) for block in itertools.combinations(V, 4)})
    key_index = {orbit: index for index, orbit in enumerate(keys)}
    d = {
        orbit: model.addVar(
            vtype=GRB.INTEGER,
            lb=0,
            ub=13,
            name=(
                f"d_{'_'.join(map(str, orbit[0]))}"
                f"_f{'_'.join(map(str, orbit[1]))}_o{orbit[2]}"
            ),
        )
        for orbit in keys
    }

    def value(block):
        return d[key(block)]

    for index, triple in enumerate(representatives(3)):
        triple_set = set(triple)
        model.addConstr(
            gp.quicksum(
                value(block)
                for block in itertools.combinations(V, 4)
                if triple_set.issubset(block)
            )
            <= 13,
            name=f"load_{index}",
        )

    rows5 = list(representatives(5))
    basis5 = independent_rows_mod_prime(rows5, key_index, 2)
    for index, subset in enumerate(rows5):
        total = gp.quicksum(
            value(block) for block in itertools.combinations(subset, 4)
        )
        if index in basis5:
            count = model.addVar(vtype=GRB.INTEGER, lb=0, name=f"N_5_{index}")
            model.addConstr(
                2 * count + total == 13,
                name=f"recurrence_5_{index}",
            )
        else:
            model.addConstr(total <= 13, name=f"size5_bound_{index}")

    prime_bases = {}
    for size, prime in ((6, 3), (8, 5), (10, 7)):
        rows = list(representatives(size))
        prime_bases[size] = (
            rows,
            independent_rows_mod_prime(rows, key_index, prime),
        )

    for size, (modulus, sign, rhs) in RECURRENCE.items():
        if size in (5, 9):
            continue
        rows = (
            prime_bases[size][0]
            if size in prime_bases
            else list(representatives(size))
        )
        selected = (
            prime_bases[size][1]
            if size in prime_bases
            else set(range(len(rows)))
        )
        for index, subset in enumerate(rows):
            if index not in selected:
                continue
            count = model.addVar(
                vtype=GRB.INTEGER,
                lb=0,
                name=f"N_{size}_{index}",
            )
            total = gp.quicksum(
                value(block) for block in itertools.combinations(subset, 4)
            )
            model.addConstr(
                modulus * count + sign * total == rhs,
                name=f"recurrence_{size}_{index}",
            )

    positive, negative = cube_cells()
    model.addConstr(
        gp.quicksum(value(block) for block in negative) == 0,
        name="negative_cube_mass",
    )
    model.addConstr(
        gp.quicksum(value(block) for block in positive) == 60,
        name="positive_cube_mass",
    )

    reference_positive = (0, 2, 4, 6)
    if args.reference_positive is not None:
        model.addConstr(
            value(reference_positive) == args.reference_positive,
            name="positive_max_value",
        )
    for index, block in enumerate(positive):
        if block != reference_positive:
            model.addConstr(
                value(reference_positive) >= value(block),
                name=f"positive_max_{index}",
            )

    odd_points = {1, 3, 5, 7}
    weight_two = [
        block for block in positive if len(set(block) & odd_points) == 2
    ]
    reference_weight_two = (0, 2, 5, 7)
    if args.reference_weight_two is not None:
        model.addConstr(
            value(reference_weight_two) == args.reference_weight_two,
            name="weight_two_max_value",
        )
    for index, block in enumerate(weight_two):
        if block != reference_weight_two:
            model.addConstr(
                value(reference_weight_two) >= value(block),
                name=f"weight_two_max_{index}",
            )

    reference_bits = {2, 3}
    crossing = []
    for block in weight_two:
        bits = {
            pair_index
            for pair_index, pair in enumerate(PAIRS)
            if pair[1] in block
        }
        if len(bits & reference_bits) == 1:
            crossing.append(block)
    reference_crossing = (0, 3, 4, 7)
    for index, block in enumerate(crossing):
        if block != reference_crossing:
            model.addConstr(
                value(reference_crossing) >= value(block),
                name=f"crossing_max_{index}",
            )
    return model, len(keys), len(basis5), prime_bases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=1800)
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--reference-positive", type=int, choices=range(8, 14))
    parser.add_argument("--reference-weight-two", type=int, choices=range(14))
    args = parser.parse_args()

    model, orbit_count, rank5, prime_bases = build_model(args)
    print(f"d_orbits: {orbit_count}")
    print(f"triple_orbits: {sum(1 for _ in representatives(3))}")
    print(f"size5_F2_rank: {rank5}")
    for size, (rows, basis) in prime_bases.items():
        print(f"size{size}_F{size - 3}_rank: {len(basis)} of {len(rows)}")
    print(f"reference_positive: {args.reference_positive}")
    print(f"reference_weight_two: {args.reference_weight_two}")
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
    print("scope: only one-fixed-exterior/S4 symmetry; TIME_LIMIT proves nothing")


if __name__ == "__main__":
    main()
