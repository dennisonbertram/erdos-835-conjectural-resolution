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
import json
import os
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

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


def witness_payload(
    representatives: tuple[tuple[int, ...], ...],
    phase_values: dict[tuple[int, ...], int],
) -> dict[str, object]:
    """A stable, verifier-friendly encoding of a fully checked witness."""
    return {
        "model": "Z_17-equivariant LS(4,5,21)",
        "modulus": MODULUS,
        "representatives": [list(block) for block in representatives],
        "phases": [phase_values[block] for block in representatives],
    }


def write_json(path: str, payload: dict[str, object]) -> None:
    """Atomically write a final-run checkpoint or a verified witness."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    os.replace(temporary, target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="CP-SAT random seed; use one worker for a reproducible branch trace",
    )
    parser.add_argument(
        "--randomized",
        action="store_true",
        help="enable CP-SAT randomized search (otherwise the seed is only recorded)",
    )
    parser.add_argument(
        "--output",
        help="write a verified phase witness as JSON when a solution is found",
    )
    parser.add_argument(
        "--checkpoint",
        help="write final status/metrics, plus a witness if found; this is not a resumable solver state",
    )
    parser.add_argument(
        "--print-phases",
        action="store_true",
        help="also print all 1,197 phase values to stdout after verification",
    )
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
    solver.parameters.random_seed = args.seed
    solver.parameters.randomize_search = args.randomized

    status = solver.solve(model)
    status_name = solver.status_name(status)
    print(f"five-set orbits: {len(representatives)}")
    print("five-set choices: 20349")
    print("four-set exact-cover constraints: 5985")
    print(f"reflection required: {args.reflection}")
    print(f"seed: {args.seed}")
    print(f"randomized search: {args.randomized}")
    print(f"status: {status_name}")
    print(f"wall time: {solver.wall_time:.3f} seconds")
    print(f"branches: {solver.num_branches}")
    print(f"conflicts: {solver.num_conflicts}")

    verified_witness: dict[str, object] | None = None
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
        verified_witness = witness_payload(representatives, phase_values)
        if args.output:
            write_json(args.output, verified_witness)
            print(f"verified witness written: {args.output}")
        if args.print_phases:
            for representative in representatives:
                print(
                    " ".join(map(str, representative)),
                    phase_values[representative],
                )

    if args.checkpoint:
        checkpoint: dict[str, object] = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "configuration": {
                "seconds": args.seconds,
                "workers": args.workers,
                "seed": args.seed,
                "randomized": args.randomized,
                "reflection": args.reflection,
            },
            "result": {
                "status": status_name,
                "wall_time_seconds": solver.wall_time,
                "branches": solver.num_branches,
                "conflicts": solver.num_conflicts,
            },
        }
        if verified_witness is not None:
            checkpoint["verified_witness"] = verified_witness
        write_json(args.checkpoint, checkpoint)
        print(f"final-run checkpoint written: {args.checkpoint}")


if __name__ == "__main__":
    main()
