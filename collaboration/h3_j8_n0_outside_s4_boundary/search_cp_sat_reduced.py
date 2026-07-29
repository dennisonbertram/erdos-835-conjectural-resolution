#!/usr/bin/env python3
"""Exact rank-reduced CP-SAT search for one-fixed-exterior/S4 branches."""

from __future__ import annotations

import argparse
import itertools
import math
import time

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
    return (
        tuple(x for x in block if x in CUBE),
        tuple(x for x in block if x in FIXED),
        sum(x in SYMMETRIC for x in block),
    )


def representatives(size):
    for fixed_count in range(2):
        fixed_part = FIXED[:fixed_count]
        for symmetric_count in range(5):
            cube_count = size - fixed_count - symmetric_count
            if 0 <= cube_count <= 8:
                symmetric_part = SYMMETRIC[:symmetric_count]
                for cube_part in itertools.combinations(CUBE, cube_count):
                    yield tuple(
                        sorted((*cube_part, *fixed_part, *symmetric_part))
                    )


def cube_cells():
    positive = []
    negative = []
    for bits in itertools.product((0, 1), repeat=4):
        block = tuple(sorted(PAIRS[index][bits[index]] for index in range(4)))
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


def build_model(
    reference_positive_value,
    reference_weight_two_value,
    positive_values=None,
):
    model = cp_model.CpModel()
    keys = sorted({key(block) for block in itertools.combinations(V, 4)})
    key_index = {orbit: index for index, orbit in enumerate(keys)}
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

    rows5 = list(representatives(5))
    basis5 = independent_rows_mod_prime(rows5, key_index, 2)
    for index, subset in enumerate(rows5):
        total = sum(value(block) for block in itertools.combinations(subset, 4))
        model.add(total <= 13)
        if index in basis5:
            count = model.new_int_var(0, 6, f"N_5_{index}")
            model.add(2 * count + total == 13)

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
            upper = (
                rhs // modulus
                if sign == 1
                else (rhs + 13 * math.comb(size, 4)) // modulus
            )
            count = model.new_int_var(0, upper, f"N_{size}_{index}")
            total = sum(
                value(block) for block in itertools.combinations(subset, 4)
            )
            model.add(modulus * count + sign * total == rhs)

    positive, negative = cube_cells()
    model.add(sum(value(block) for block in negative) == 0)
    model.add(sum(value(block) for block in positive) == 60)
    if positive_values is not None:
        assert len(positive_values) == len(positive)
        for block, fixed_value in zip(positive, positive_values):
            model.add(value(block) == fixed_value)

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
    return model, len(keys), len(basis5), prime_bases, d


def m8_cube_cases():
    # Positive cube order:
    # 0000, 0011, 0101, 0110, 1001, 1010, 1100, 1111.
    # The first two values are the normalized maxima 8.  Deficits from 8
    # sum to four.  The crossing breaker makes the 0101 deficit no larger
    # than the other three crossing deficits.
    for deficits in itertools.product(range(5), repeat=6):
        if sum(deficits) != 4:
            continue
        crossing_reference, crossing_2, crossing_3, crossing_4, other, antipode = (
            deficits
        )
        if crossing_reference > min(crossing_2, crossing_3, crossing_4):
            continue
        yield (
            8,
            8,
            8 - crossing_reference,
            8 - crossing_2,
            8 - crossing_3,
            8 - crossing_4,
            8 - other,
            8 - antipode,
        )


def solve(model, seconds, workers):
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = 835
    status = solver.solve(model)
    return solver, status


def enumerate_m8(args):
    cases = tuple(m8_cube_cases())
    assert len(cases) == 71
    total_branches = 0
    started = time.monotonic()
    for index, values in enumerate(cases):
        model, _, _, _, d = build_model(8, 8, values)
        solver, status = solve(model, args.seconds, args.workers)
        total_branches += solver.num_branches
        status_name = solver.status_name(status)
        print(
            f"case={index:02d} values={','.join(map(str, values))} "
            f"status={status_name} wall={solver.wall_time} "
            f"branches={solver.num_branches}",
            flush=True,
        )
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            print("nonzero_d_orbits:")
            for orbit, variable in sorted(d.items()):
                if solver.value(variable):
                    print(f"  {orbit}: {solver.value(variable)}")
            print("aggregate_status: FEASIBLE")
            return
        if status != cp_model.INFEASIBLE:
            print("aggregate_status: UNKNOWN")
            print("scope: an UNKNOWN case proves nothing")
            return
    print("aggregate_status: INFEASIBLE_ALL_71")
    print(f"aggregate_wall_seconds: {time.monotonic() - started}")
    print(f"aggregate_branches: {total_branches}")
    print("scope: only one-fixed-exterior/S4 symmetry")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=1800)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--reference-positive", type=int, choices=range(8, 14))
    parser.add_argument("--reference-weight-two", type=int, choices=range(14))
    parser.add_argument(
        "--enumerate-m8-cube-cases",
        action="store_true",
        help="solve the 71 exact m=8,w=8 positive-cube patterns",
    )
    args = parser.parse_args()

    if args.enumerate_m8_cube_cases:
        enumerate_m8(args)
        return

    model, orbit_count, rank5, prime_bases, _ = build_model(
        args.reference_positive,
        args.reference_weight_two,
    )
    print(f"d_orbits: {orbit_count}")
    print(f"triple_orbits: {sum(1 for _ in representatives(3))}")
    print(f"size5_F2_rank: {rank5}")
    for size, (rows, basis) in prime_bases.items():
        print(f"size{size}_F{size - 3}_rank: {len(basis)} of {len(rows)}")
    print(f"reference_positive: {args.reference_positive}")
    print(f"reference_weight_two: {args.reference_weight_two}")

    solver, status = solve(model, args.seconds, args.workers)
    print(f"status: {solver.status_name(status)}")
    print(f"wall_seconds: {solver.wall_time}")
    print(f"branches: {solver.num_branches}")
    print("scope: only one-fixed-exterior/S4 symmetry; UNKNOWN proves nothing")


if __name__ == "__main__":
    main()
