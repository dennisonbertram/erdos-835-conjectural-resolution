#!/usr/bin/env python3
"""Complete CP-SAT search for a large set LS(3,4,20).

There is one 17-valued variable per 4-subset.  The 17 extensions of every
3-subset are constrained all-different.  The extension star of {0,1,2} is
fixed in lexicographic order, which removes only global colour symmetry.

FEASIBLE produces a complete certificate.  INFEASIBLE is an exact solver
result but should be backed by the deterministic CNF and a checked proof
before being treated as a portable theorem.  UNKNOWN proves nothing.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from ortools.sat.python import cp_model


POINTS = 20
COLOURS = 17
BLOCKS = tuple(itertools.combinations(range(POINTS), 4))
BLOCK_INDEX = {block: index for index, block in enumerate(BLOCKS)}
SCHEMA = "ls-3-4-20-full-cpsat-v1"


def verify(colours: list[int]) -> None:
    if len(colours) != len(BLOCKS) or not all(0 <= colour < COLOURS for colour in colours):
        raise AssertionError("invalid colour vector")
    for triple in itertools.combinations(range(POINTS), 3):
        star = [
            colours[BLOCK_INDEX[tuple(sorted(triple + (point,)))]]
            for point in range(POINTS)
            if point not in triple
        ]
        if sorted(star) != list(range(COLOURS)):
            raise AssertionError(f"non-rainbow triple star {triple}")


def load_normalized_partial(path: Path) -> list[int]:
    """Load a proper partial colouring and normalize its root-star palette."""

    raw = []
    with path.open(encoding="utf-8") as stream:
        for expected, line in zip(BLOCKS, stream):
            fields = [int(field) for field in line.split()]
            if len(fields) != 5 or tuple(fields[:4]) != expected:
                raise ValueError(f"unexpected partial-certificate row at {expected}")
            if not -1 <= fields[4] < COLOURS:
                raise ValueError(f"invalid partial colour at {expected}")
            raw.append(fields[4])
    if len(raw) != len(BLOCKS):
        raise ValueError(f"partial certificate has {len(raw)} rows")

    for triple in itertools.combinations(range(POINTS), 3):
        assigned = [
            raw[BLOCK_INDEX[tuple(sorted(triple + (point,)))]]
            for point in range(POINTS)
            if point not in triple
        ]
        assigned = [colour for colour in assigned if colour >= 0]
        if len(assigned) != len(set(assigned)):
            raise ValueError(f"partial certificate conflicts at {triple}")

    root = (0, 1, 2)
    root_colours = [
        raw[BLOCK_INDEX[tuple(sorted(root + (point,)))]]
        for point in range(3, POINTS)
    ]
    if sorted(root_colours) != list(range(COLOURS)):
        raise ValueError("partial certificate must fully colour the root star")
    relabel = {old: new for new, old in enumerate(root_colours)}
    return [relabel[colour] if colour >= 0 else -1 for colour in raw]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=21_600)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument(
        "--hint",
        type=Path,
        help="Proper partial 4,845-row certificate used as a repair hint",
    )
    parser.add_argument("--log", action="store_true")
    args = parser.parse_args()

    model = cp_model.CpModel()
    colour = [
        model.NewIntVar(0, COLOURS - 1, f"c_{block}")
        for block in range(len(BLOCKS))
    ]
    triple_count = 0
    for triple in itertools.combinations(range(POINTS), 3):
        star = [
            colour[BLOCK_INDEX[tuple(sorted(triple + (point,)))]]
            for point in range(POINTS)
            if point not in triple
        ]
        model.AddAllDifferent(star)
        triple_count += 1
    if triple_count != 1_140:
        raise AssertionError("wrong triple count")

    root = (0, 1, 2)
    for assigned, point in enumerate(range(3, POINTS)):
        model.Add(
            colour[BLOCK_INDEX[tuple(sorted(root + (point,)))]] == assigned
        )

    partial = None
    if args.hint is not None:
        partial = load_normalized_partial(args.hint)
        for variable, assigned in zip(colour, partial):
            if assigned >= 0:
                model.AddHint(variable, assigned)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = args.log
    if partial is not None:
        solver.parameters.repair_hint = True
        solver.parameters.hint_conflict_limit = 1_000_000
    status = solver.Solve(model)
    result: dict[str, object] = {
        "schema": SCHEMA,
        "status": solver.StatusName(status),
        "blocks": len(BLOCKS),
        "triple_stars": triple_count,
        "symmetry_units": COLOURS,
        "hint": str(args.hint) if args.hint is not None else None,
        "hint_assigned_blocks": (
            sum(assigned >= 0 for assigned in partial)
            if partial is not None
            else 0
        ),
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        values = [solver.Value(variable) for variable in colour]
        verify(values)
        result["certificate_verified"] = True
        if args.certificate is not None:
            args.certificate.parent.mkdir(parents=True, exist_ok=True)
            with args.certificate.open("w", encoding="utf-8") as stream:
                for block, assigned in zip(BLOCKS, values):
                    stream.write("{} {} {} {} {}\n".format(*block, assigned))
            result["certificate"] = str(args.certificate)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
