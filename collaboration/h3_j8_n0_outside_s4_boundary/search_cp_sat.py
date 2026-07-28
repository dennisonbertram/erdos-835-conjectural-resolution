#!/usr/bin/env python3
"""Exact CP-SAT search for one-fixed-exterior/S4-symmetric N=0 branches."""

from __future__ import annotations

import argparse
import itertools
import math

from ortools.sat.python import cp_model


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


def build_model(reference_positive_value, reference_weight_two_value):
    model = cp_model.CpModel()
    keys = sorted({key(block) for block in itertools.combinations(V, 4)})
    d = {
        orbit: model.new_int_var(
            0,
            13,
            f"d_{'_'.join(map(str, orbit[0]))}"
            f"_f{'_'.join(map(str, orbit[1]))}_o{orbit[2]}",
        )
        for orbit in keys
    }

    def value(block):
        return d[key(block)]

    for triple in representatives(3):
        triple_set = set(triple)
        model.add(
            sum(
                value(block)
                for block in itertools.combinations(V, 4)
                if triple_set.issubset(block)
            )
            <= 13
        )

    for size, (modulus, sign, rhs) in RECURRENCE.items():
        for index, subset in enumerate(representatives(size)):
            total = sum(
                value(block) for block in itertools.combinations(subset, 4)
            )
            upper = (
                rhs // modulus
                if sign == 1
                else (rhs + 13 * math.comb(size, 4)) // modulus
            )
            count = model.new_int_var(0, upper, f"N_{size}_{index}")
            model.add(modulus * count + sign * total == rhs)

    positive, negative = cube_cells()
    model.add(sum(value(block) for block in negative) == 0)
    model.add(sum(value(block) for block in positive) == 60)

    reference_positive = (0, 2, 4, 6)
    if reference_positive_value is not None:
        model.add(value(reference_positive) == reference_positive_value)
    for block in positive:
        model.add(value(reference_positive) >= value(block))

    odd_points = {1, 3, 5, 7}
    weight_two = [
        block for block in positive if len(set(block) & odd_points) == 2
    ]
    reference_weight_two = (0, 2, 5, 7)
    if reference_weight_two_value is not None:
        model.add(value(reference_weight_two) == reference_weight_two_value)
    for block in weight_two:
        model.add(value(reference_weight_two) >= value(block))

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
    for block in crossing:
        model.add(value(reference_crossing) >= value(block))
    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--reference-positive", type=int, choices=range(8, 14))
    parser.add_argument("--reference-weight-two", type=int, choices=range(14))
    args = parser.parse_args()

    model = build_model(args.reference_positive, args.reference_weight_two)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = 835
    status = solver.solve(model)
    print(f"reference_positive: {args.reference_positive}")
    print(f"reference_weight_two: {args.reference_weight_two}")
    print(f"status: {solver.status_name(status)}")
    print(f"wall_seconds: {solver.wall_time}")
    print(f"branches: {solver.num_branches}")
    print("scope: only one-fixed-exterior/S4 symmetry; UNKNOWN proves nothing")


if __name__ == "__main__":
    main()
