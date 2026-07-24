#!/usr/bin/env python3
"""Search for a Z_17-equivariant LS(4,5,21).

The point set is Z_17 together with four fixed points.  Translation by one
is required to add one to the colour.  A colour phase is therefore needed
only for each orbit of five-subsets.  Every four-subset must have its 17
extensions in all 17 colours.

This is a deliberately restricted search: UNSAT rules out any LS(4,5,21)
admitting an automorphism of order 17, not an arbitrary LS(4,5,21).

Requires OR-Tools (`python3 -m pip install ortools`).
"""

from __future__ import annotations

import argparse
from itertools import combinations

from ortools.sat.python import cp_model


MODULUS = 17
POINTS = tuple(range(21))
AFFINE_ANCHOR = (0, 17, 18, 19, 20)


def translate(subset: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            (point + amount) % MODULUS if point < MODULUS else point
            for point in subset
        )
    )


def canonical(
    subset: tuple[int, ...],
) -> tuple[tuple[int, ...], int]:
    """Return (orbit representative, shift from representative to subset)."""
    representative, shift_from_subset = min(
        (translate(subset, amount), amount)
        for amount in range(MODULUS)
    )
    return representative, (-shift_from_subset) % MODULUS


def orbit_representatives(size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        sorted(
            {
                canonical(tuple(subset))[0]
                for subset in combinations(POINTS, size)
            }
        )
    )


def build_model(
    require_reflection: bool = False,
) -> tuple[
    cp_model.CpModel,
    tuple[tuple[int, ...], ...],
    dict[tuple[int, ...], cp_model.IntVar],
]:
    five_representatives = orbit_representatives(5)

    assert len(five_representatives) == 1197

    model = cp_model.CpModel()
    block_variables = {
        block: model.new_bool_var(
            "block_" + "_".join(map(str, block))
        )
        for block in combinations(POINTS, 5)
    }

    # Choose exactly one zero-colour block from every translation orbit.
    for representative in five_representatives:
        orbit = [
            translate(representative, amount)
            for amount in range(MODULUS)
        ]
        assert len(set(orbit)) == MODULUS
        model.add_exactly_one(block_variables[block] for block in orbit)

    # The chosen zero-colour blocks must form an S(4,5,21).
    for four_set in combinations(POINTS, 4):
        extensions = []
        for point in POINTS:
            if point in four_set:
                continue
            five_set = tuple(sorted(four_set + (point,)))
            extensions.append(block_variables[five_set])
        assert len(extensions) == MODULUS
        model.add_exactly_one(extensions)

    # Global translation of the selected design is immaterial.  Do not also
    # fix this phase when a reflection with prescribed centre zero is imposed:
    # translating the design conjugates the centre of that reflection.
    if not require_reflection:
        # Every S(4,5,21) has exactly one block through all four fixed
        # points.  Translation moves its cyclic point to zero.  This anchor
        # retains the full multiplier and fixed-point permutation symmetries.
        assert translate(AFFINE_ANCHOR, 0) == AFFINE_ANCHOR
        model.add(block_variables[AFFINE_ANCHOR] == 1)

    if require_reflection:
        for block, variable in block_variables.items():
            reflected = tuple(
                sorted(
                    (-point) % MODULUS
                    if point < MODULUS
                    else point
                    for point in block
                )
            )
            model.add(variable == block_variables[reflected])

    return model, five_representatives, block_variables


def verify_solution(
    representatives: tuple[tuple[int, ...], ...],
    phase_values: dict[tuple[int, ...], int],
) -> None:
    assert set(representatives) == set(phase_values)
    for four_set in combinations(POINTS, 4):
        colours = []
        for point in POINTS:
            if point in four_set:
                continue
            five_set = tuple(sorted(four_set + (point,)))
            representative, shift = canonical(five_set)
            colours.append(
                (phase_values[representative] + shift) % MODULUS
            )
        assert set(colours) == set(range(MODULUS))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--log", action="store_true")
    parser.add_argument(
        "--reflection",
        action="store_true",
        help="also require invariance under x -> -x on Z_17",
    )
    args = parser.parse_args()

    model, representatives, block_variables = build_model(args.reflection)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.log_search_progress = args.log

    status = solver.solve(model)
    status_name = solver.status_name(status)
    print(f"five-set orbits: {len(representatives)}")
    print("five-set choices: 20349")
    print("four-set exact-cover constraints: 5985")
    print(f"reflection required: {args.reflection}")
    print(f"status: {status_name}")
    print(f"wall time: {solver.wall_time:.3f} seconds")
    print(f"branches: {solver.num_branches}")
    print(f"conflicts: {solver.num_conflicts}")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected_blocks = tuple(
            block
            for block, variable in block_variables.items()
            if solver.value(variable)
        )
        assert len(selected_blocks) == 1197

        phase_values = {}
        for block in selected_blocks:
            representative, shift = canonical(block)
            assert representative not in phase_values
            phase_values[representative] = (-shift) % MODULUS

        verify_solution(representatives, phase_values)
        print("verified: cyclic LS(4,5,21) found")
        for representative in representatives:
            print(
                " ".join(map(str, representative)),
                phase_values[representative],
            )


if __name__ == "__main__":
    main()
