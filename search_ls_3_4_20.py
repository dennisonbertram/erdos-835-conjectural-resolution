#!/usr/bin/env python3
"""Direct CP-SAT search for a large set LS(3,4,20).

The variables are the colours of the 4-subsets of a 20-point set.  For
each 3-subset, its seventeen extensions are constrained to have all
different colours.  A fixed star removes all 17! colour permutations.

If ``--solution`` is supplied and a solution is found, the script writes a
plain text certificate with one line ``a b c d colour`` per 4-subset.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


POINTS = tuple(range(20))
COLOURS = tuple(range(17))
REFERENCE_TRIPLE = (0, 1, 2)
PHELPS_BASE_BLOCKS = (
    (19, 1, 0, 8),
    (19, 2, 0, 5),
    (19, 13, 0, 9),
    (0, 1, 2, 4),
    (0, 1, 6, 9),
    (0, 1, 10, 17),
    (0, 2, 6, 14),
    (0, 2, 9, 15),
    (0, 3, 4, 16),
    (0, 3, 5, 10),
    (0, 4, 5, 9),
    (0, 4, 7, 15),
    (0, 5, 6, 16),
    (0, 6, 11, 18),
    (0, 6, 8, 17),
)


def phelps_cyclic_sqs20() -> set[tuple[int, int, int, int]]:
    """Return Phelps' cyclic SQS(20), relabelled so 0123 is a block."""

    blocks = set()
    for base in PHELPS_BASE_BLOCKS:
        for shift in range(19):
            developed = tuple(
                sorted(
                    (point + shift) % 19 if point < 19 else point
                    for point in base
                )
            )
            # The published base system has 0124.  Swap point labels 3 and
            # 4 so its unique block through 012 agrees with our reference
            # star's colour-zero extension.
            relabelled = tuple(
                sorted(
                    4 if point == 3 else (3 if point == 4 else point)
                    for point in developed
                )
            )
            blocks.add(relabelled)
    assert len(blocks) == 285
    for triple in combinations(POINTS, 3):
        assert sum(set(triple).issubset(block) for block in blocks) == 1
    assert (0, 1, 2, 3) in blocks
    return blocks


def build_model(
    identity_second_star: bool = False,
    second_star_cycles: tuple[int, ...] | None = None,
    cyclic_pair_link: bool = False,
    phelps_class_zero: bool = False,
) -> tuple[
    cp_model.CpModel,
    dict[tuple[int, int, int, int], cp_model.IntVar],
]:
    model = cp_model.CpModel()
    colour = {
        block: model.new_int_var(
            0,
            16,
            "c_" + "_".join(map(str, block)),
        )
        for block in combinations(POINTS, 4)
    }
    assert len(colour) == 4845

    for triple in combinations(POINTS, 3):
        extensions = [
            colour[tuple(sorted(triple + (point,)))]
            for point in POINTS
            if point not in triple
        ]
        assert len(extensions) == 17
        model.add_all_different(extensions)

    # The extensions of one triple are necessarily rainbow.  Relabel the
    # colours so that adding points 3,...,19 gives colours 0,...,16.
    for point in range(3, 20):
        block = tuple(sorted(REFERENCE_TRIPLE + (point,)))
        model.add(colour[block] == point - 3)

    # After the first normalization, simultaneous permutations of the
    # outside points 4,...,19 and colours 1,...,16 act by conjugation on
    # the second star based at (0,1,3).  Requiring the identity is therefore
    # a deliberately restricted but strongly symmetry-broken subsearch,
    # useful for rapidly testing the simplest conjugacy class.
    if identity_second_star:
        for point in range(4, 20):
            block = (0, 1, 3, point)
            model.add(colour[block] == point - 3)

    if second_star_cycles is not None:
        assert sum(second_star_cycles) == 16
        assert all(length >= 2 for length in second_star_cycles)
        permutation = {}
        first = 1
        for length in second_star_cycles:
            cycle = list(range(first, first + length))
            for left, right in zip(cycle, cycle[1:] + cycle[:1]):
                permutation[left] = right
            first += length
        assert set(permutation) == set(range(1, 17))
        for point in range(4, 20):
            index = point - 3
            model.add(colour[(0, 1, 3, point)] == permutation[index])

    # The blocks through a fixed pair are a proper 17-edge-colouring of
    # K_18, hence a one-factorization.  This optional subsearch fixes that
    # link to the standard cyclic one-factorization on F_17 union {inf},
    # with point 2 as infinity and point x=3,...,19 labelled x-3.
    if cyclic_pair_link:
        inverse_two = pow(2, -1, 17)
        for left, right in combinations(range(3, 20), 2):
            left_label = left - 3
            right_label = right - 3
            factor = (left_label + right_label) * inverse_two % 17
            model.add(colour[(0, 1, left, right)] == factor)

    if phelps_class_zero:
        for block in phelps_cyclic_sqs20():
            model.add(colour[block] == 0)

    return model, colour


def verify_solution(
    values: dict[tuple[int, int, int, int], int],
) -> None:
    assert len(values) == 4845
    assert set(values.values()).issubset(COLOURS)
    for triple in combinations(POINTS, 3):
        star_colours = {
            values[tuple(sorted(triple + (point,)))]
            for point in POINTS
            if point not in triple
        }
        assert star_colours == set(COLOURS)

    expected_class_size = 4845 // 17
    assert expected_class_size == 285
    for label in COLOURS:
        blocks = [block for block, value in values.items() if value == label]
        assert len(blocks) == expected_class_size
        for triple in combinations(POINTS, 3):
            assert (
                sum(set(triple).issubset(block) for block in blocks) == 1
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--log", action="store_true")
    parser.add_argument("--solution", type=Path)
    parser.add_argument("--identity-second-star", action="store_true")
    parser.add_argument(
        "--second-star-cycles",
        help="comma-separated derangement cycle lengths summing to 16",
    )
    parser.add_argument("--cyclic-pair-link", action="store_true")
    parser.add_argument("--phelps-class-zero", action="store_true")
    args = parser.parse_args()

    second_star_cycles = (
        tuple(int(item) for item in args.second_star_cycles.split(","))
        if args.second_star_cycles
        else None
    )
    model, colour = build_model(
        args.identity_second_star,
        second_star_cycles,
        args.cyclic_pair_link,
        args.phelps_class_zero,
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.log_search_progress = args.log
    solver.parameters.symmetry_level = 3

    status = solver.solve(model)
    print("blocks / colour variables: 4845")
    print("triple-star all-different constraints: 1140")
    print("reference-star colour assignments: 17")
    print(f"identity second star: {args.identity_second_star}")
    print(f"second-star cycle type: {second_star_cycles}")
    print(f"cyclic pair link: {args.cyclic_pair_link}")
    print(f"Phelps cyclic class fixed as zero: {args.phelps_class_zero}")
    print(f"status: {solver.status_name(status)}")
    print(f"wall time: {solver.wall_time:.3f} seconds")
    print(f"branches: {solver.num_branches}")
    print(f"conflicts: {solver.num_conflicts}")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = {
            block: solver.value(variable)
            for block, variable in colour.items()
        }
        verify_solution(values)
        print("verified: LS(3,4,20) found")
        if args.solution:
            args.solution.write_text(
                "".join(
                    "{} {} {} {} {}\\n".format(*block, values[block])
                    for block in sorted(values)
                ),
                encoding="utf-8",
            )
            print(f"certificate: {args.solution}")


if __name__ == "__main__":
    main()
