#!/usr/bin/env python3
"""Random-restart exact-cover search for an explicit LS(3,4,20).

The monolithic colour models in ``search_ls_3_4_20.py`` ask CP-SAT to find
all seventeen Steiner quadruple systems simultaneously.  This companion
search fixes Phelps' cyclic SQS(20) as the first class and then repeatedly
finds one exact-cover mate among the unused blocks.  A failed late stage
restarts from the fixed first class.

This is only a search heuristic: failure or timeout proves nothing.  A
reported solution is independently checked by ``verify_solution`` before
being written.
"""

from __future__ import annotations

import argparse
import time
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model

from search_ls_3_4_20 import (
    POINTS,
    phelps_cyclic_sqs20,
    verify_solution,
)


Block = tuple[int, int, int, int]
Triple = tuple[int, int, int]


def find_one_sqs(
    remaining: set[Block],
    *,
    seconds: float,
    workers: int,
    seed: int,
) -> set[Block] | None:
    """Find one SQS(20) contained in ``remaining``, if CP-SAT does so."""

    blocks = tuple(sorted(remaining))
    through: dict[Triple, list[int]] = {
        triple: [] for triple in combinations(POINTS, 3)
    }
    for index, block in enumerate(blocks):
        for triple in combinations(block, 3):
            through[triple].append(index)

    if any(not candidates for candidates in through.values()):
        return None

    model = cp_model.CpModel()
    chosen = [model.new_bool_var(f"x_{index}") for index in range(len(blocks))]
    for candidates in through.values():
        model.add_exactly_one(chosen[index] for index in candidates)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.randomize_search = True
    solver.parameters.search_branching = cp_model.RANDOMIZED_SEARCH
    solver.parameters.stop_after_first_solution = True
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    result = {
        block for block, variable in zip(blocks, chosen) if solver.value(variable)
    }
    if len(result) != 285:
        raise AssertionError(f"SQS candidate has {len(result)} blocks, not 285")
    for triple in combinations(POINTS, 3):
        if sum(set(triple).issubset(block) for block in result) != 1:
            raise AssertionError(f"SQS candidate fails at triple {triple}")
    return result


def try_restart(
    restart: int,
    *,
    seconds: float,
    workers: int,
    base_seed: int,
) -> list[set[Block]] | None:
    all_blocks = set(combinations(POINTS, 4))
    systems = [phelps_cyclic_sqs20()]
    remaining = all_blocks - systems[0]

    # Sixteen residual systems are required.  If fifteen are found, the
    # remaining 285 blocks must be the last system, which we verify exactly.
    for stage in range(1, 16):
        seed = base_seed + restart * 10_000 + stage
        started = time.monotonic()
        system = find_one_sqs(
            remaining,
            seconds=seconds,
            workers=workers,
            seed=seed,
        )
        elapsed = time.monotonic() - started
        if system is None:
            print(
                f"restart {restart}: stage {stage}/15 failed "
                f"after {elapsed:.3f}s",
                flush=True,
            )
            return None
        systems.append(system)
        remaining -= system
        print(
            f"restart {restart}: stage {stage}/15 found; "
            f"{len(remaining)} blocks remain; {elapsed:.3f}s",
            flush=True,
        )

    if len(remaining) != 285:
        raise AssertionError(f"last residual has {len(remaining)} blocks")
    for triple in combinations(POINTS, 3):
        if sum(set(triple).issubset(block) for block in remaining) != 1:
            print(
                f"restart {restart}: last residual fails at {triple}",
                flush=True,
            )
            return None
    systems.append(remaining)
    return systems


def normalized_values(systems: list[set[Block]]) -> dict[Block, int]:
    """Colour the systems so the extensions of 012 have labels 0,...,16."""

    by_extension: dict[int, set[Block]] = {}
    for system in systems:
        extensions = [
            point
            for point in range(3, 20)
            if (0, 1, 2, point) in system
        ]
        if len(extensions) != 1:
            raise AssertionError(f"reference triple has extensions {extensions}")
        by_extension[extensions[0]] = system
    if set(by_extension) != set(range(3, 20)):
        raise AssertionError("reference extensions do not partition 3,...,19")

    values: dict[Block, int] = {}
    for point, system in by_extension.items():
        label = point - 3
        for block in system:
            if block in values:
                raise AssertionError(f"block repeated: {block}")
            values[block] = label
    verify_solution(values)
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-seconds", type=float, default=10.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--restarts", type=int, default=100)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--solution", type=Path)
    args = parser.parse_args()

    for restart in range(args.restarts):
        systems = try_restart(
            restart,
            seconds=args.class_seconds,
            workers=args.workers,
            base_seed=args.seed,
        )
        if systems is None:
            continue
        values = normalized_values(systems)
        print("verified: LS(3,4,20) found", flush=True)
        if args.solution:
            args.solution.write_text(
                "".join(
                    "{} {} {} {} {}\n".format(*block, values[block])
                    for block in sorted(values)
                ),
                encoding="utf-8",
            )
            print(f"certificate: {args.solution}", flush=True)
        return
    print("no solution found within the random-restart budget", flush=True)


if __name__ == "__main__":
    main()
