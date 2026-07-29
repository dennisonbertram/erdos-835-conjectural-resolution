#!/usr/bin/env python3
"""Search for an S(4,5,21), optionally above Phelps' cyclic SQS(20).

An S(4,5,21) is a collection of 5-subsets in which every 4-subset occurs
exactly once.  In ``--phelps-derived`` mode, point 20 is distinguished and
the derived S(3,4,20) is fixed to the cyclic Phelps system already used by
``search_ls_3_4_20.py``.  This restriction is useful for finding a witness,
but INFEASIBLE in that mode would not rule out an unrestricted S(4,5,21).

In unrestricted mode we use two lossless normalizations.  First fix the
block 01234.  The blocks through 012 then form a perfect matching on the
other 18 points, one of whose edges is 34; relabelling the remaining
sixteen points fixes its other eight edges.  After that normalization, the
matching through 013 is classified, under the stabilizer of the first
matching, by the half-lengths of the alternating cycles in the union of
the two matchings (equivalently, the numbers of first-matching edges in
those cycles).  The allowed partitions of eight have all parts at least
two.  Searching all seven such partitions is exhaustive; this is not an
automorphism assumption.

Requires OR-Tools.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model

from search_ls_3_4_20 import phelps_cyclic_sqs20


POINTS = tuple(range(21))
INFINITY = 20
ANCHOR = (0, 1, 2, 3, 4)
OUTSIDE_PAIRS = tuple((point, point + 1) for point in range(5, 21, 2))
SECOND_LINK_CYCLE_TYPES = (
    (8,),
    (6, 2),
    (5, 3),
    (4, 4),
    (4, 2, 2),
    (3, 3, 2),
    (2, 2, 2, 2),
)


def verify(blocks: set[tuple[int, ...]]) -> None:
    assert len(blocks) == 1197, len(blocks)
    counts = {four: 0 for four in combinations(POINTS, 4)}
    for block in blocks:
        assert len(block) == 5 and tuple(sorted(block)) == block
        for four in combinations(block, 4):
            counts[four] += 1
    failures = [four for four, count in counts.items() if count != 1]
    assert not failures, failures[:10]


def build_model(
    phelps_derived: bool,
    canonical_first_link: bool = True,
    second_link_cycles: tuple[int, ...] | None = None,
) -> tuple[
    cp_model.CpModel,
    dict[tuple[int, ...], cp_model.IntVar],
    set[tuple[int, ...]],
]:
    model = cp_model.CpModel()
    fixed: set[tuple[int, ...]] = set()

    if phelps_derived:
        fixed = {
            tuple(sorted(block + (INFINITY,)))
            for block in phelps_cyclic_sqs20()
        }
        assert len(fixed) == 285

        derived_blocks = {
            tuple(sorted(block[:-1]))
            for block in fixed
        }
        candidates = []
        for block in combinations(range(20), 5):
            if any(
                tuple(four) in derived_blocks
                for four in combinations(block, 4)
            ):
                continue
            candidates.append(block)
    else:
        candidates = [
            block
            for block in combinations(POINTS, 5)
            if len(set(block) & set(ANCHOR)) < 4 or block == ANCHOR
        ]

    variables = {
        block: model.new_bool_var("b_" + "_".join(map(str, block)))
        for block in candidates
    }

    fixed_four_sets = {
        four
        for block in fixed
        for four in combinations(block, 4)
    }

    extensions_by_four: dict[
        tuple[int, ...], list[cp_model.IntVar]
    ] = {}
    for block, variable in variables.items():
        for four in combinations(block, 4):
            extensions_by_four.setdefault(four, []).append(variable)

    for four in combinations(POINTS, 4):
        if four in fixed_four_sets:
            continue
        extensions = extensions_by_four.get(four, [])
        assert extensions, four
        model.add_exactly_one(extensions)

    if not phelps_derived:
        model.add(variables[ANCHOR] == 1)

        if canonical_first_link:
            for left, right in OUTSIDE_PAIRS:
                block = (0, 1, 2, left, right)
                model.add(variables[block] == 1)

        if second_link_cycles is not None:
            assert canonical_first_link
            assert tuple(sorted(second_link_cycles, reverse=True)) in (
                tuple(sorted(cycle_type, reverse=True))
                for cycle_type in SECOND_LINK_CYCLE_TYPES
            )
            assert sum(second_link_cycles) == len(OUTSIDE_PAIRS)
            assert all(length >= 2 for length in second_link_cycles)

            matching: list[tuple[int, int]] = []
            start = 0
            for length in second_link_cycles:
                indices = list(range(start, start + length))
                for current, following in zip(
                    indices, indices[1:] + indices[:1]
                ):
                    matching.append(
                        (
                            OUTSIDE_PAIRS[current][1],
                            OUTSIDE_PAIRS[following][0],
                        )
                    )
                start += length
            assert len(matching) == len(OUTSIDE_PAIRS)
            assert len({point for edge in matching for point in edge}) == 16
            for left, right in matching:
                block = tuple(sorted((0, 1, 3, left, right)))
                model.add(variables[block] == 1)

    return model, variables, fixed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=1800.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument("--log", action="store_true")
    parser.add_argument("--phelps-derived", action="store_true")
    parser.add_argument(
        "--no-canonical-first-link",
        action="store_true",
        help="disable the lossless first triple-link normalization",
    )
    parser.add_argument(
        "--second-link-cycles",
        help=(
            "comma-separated alternating half-cycle lengths, one of "
            "8; 6,2; 5,3; 4,4; 4,2,2; 3,3,2; 2,2,2,2"
        ),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    second_link_cycles = (
        tuple(int(item) for item in args.second_link_cycles.split(","))
        if args.second_link_cycles
        else None
    )
    if args.phelps_derived and (
        args.no_canonical_first_link or second_link_cycles is not None
    ):
        parser.error("triple-link normalizations are unrestricted-mode only")

    canonical_first_link = (
        not args.phelps_derived
        and not args.no_canonical_first_link
    )
    model, variables, fixed = build_model(
        args.phelps_derived,
        canonical_first_link,
        second_link_cycles,
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = args.log

    status = solver.solve(model)
    print(f"phelps derived: {args.phelps_derived}")
    print(f"canonical first link: {canonical_first_link}")
    print(f"second-link cycle type: {second_link_cycles}")
    print(f"active variables: {len(variables)}")
    print(f"fixed blocks: {len(fixed)}")
    print(f"status: {solver.status_name(status)}")
    print(f"wall time: {solver.wall_time:.3f} seconds")
    print(f"branches: {solver.num_branches}")
    print(f"conflicts: {solver.num_conflicts}")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected = fixed | {
            block
            for block, variable in variables.items()
            if solver.value(variable)
        }
        verify(selected)
        print("verified: S(4,5,21) found")
        text = "\n".join(" ".join(map(str, block)) for block in sorted(selected))
        if args.output:
            args.output.write_text(text + "\n", encoding="utf-8")
            print(f"witness: {args.output}")
        else:
            print(text)


if __name__ == "__main__":
    main()
