#!/usr/bin/env python3
"""Boolean exact-cover formulation of the LS(3,4,20) search.

There is one Boolean variable x[B,c] for each 4-subset B and colour c.
Every block chooses exactly one colour, and for every triple T and colour c
exactly one of the seventeen extensions of T chooses c.  This is equivalent
to the integer/all-different model in ``search_ls_3_4_20.py`` but exposes
the exact-cover structure directly to CP-SAT.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model

from search_ls_3_4_20 import COLOURS, POINTS, verify_solution


def build_model() -> tuple[
    cp_model.CpModel,
    tuple[tuple[int, int, int, int], ...],
    dict[tuple[tuple[int, int, int, int], int], cp_model.IntVar],
]:
    blocks = tuple(combinations(POINTS, 4))
    model = cp_model.CpModel()
    selected = {
        (block, label): model.new_bool_var(
            "x_{}_{}".format("_".join(map(str, block)), label)
        )
        for block in blocks
        for label in COLOURS
    }
    assert len(selected) == 82_365

    for block in blocks:
        model.add_exactly_one(selected[block, label] for label in COLOURS)

    for triple in combinations(POINTS, 3):
        extensions = [
            tuple(sorted(triple + (point,)))
            for point in POINTS
            if point not in triple
        ]
        assert len(extensions) == 17
        for label in COLOURS:
            model.add_exactly_one(
                selected[block, label] for block in extensions
            )

    for point in range(3, 20):
        block = (0, 1, 2, point)
        model.add(selected[block, point - 3] == 1)

    return model, blocks, selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--log", action="store_true")
    parser.add_argument("--solution", type=Path)
    args = parser.parse_args()

    model, blocks, selected = build_model()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.log_search_progress = args.log
    solver.parameters.symmetry_level = 3

    status = solver.solve(model)
    print("Boolean block-colour variables: 82365")
    print("block exact-one constraints: 4845")
    print("triple-colour exact-one constraints: 19380")
    print("reference-star assignments: 17")
    print(f"status: {solver.status_name(status)}")
    print(f"wall time: {solver.wall_time:.3f} seconds")
    print(f"branches: {solver.num_branches}")
    print(f"conflicts: {solver.num_conflicts}")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = {}
        for block in blocks:
            labels = [
                label
                for label in COLOURS
                if solver.value(selected[block, label])
            ]
            assert len(labels) == 1
            values[block] = labels[0]
        verify_solution(values)
        print("verified: LS(3,4,20) found")
        if args.solution:
            args.solution.write_text(
                "".join(
                    "{} {} {} {} {}\\n".format(*block, values[block])
                    for block in blocks
                ),
                encoding="utf-8",
            )
            print(f"certificate: {args.solution}")


if __name__ == "__main__":
    main()
