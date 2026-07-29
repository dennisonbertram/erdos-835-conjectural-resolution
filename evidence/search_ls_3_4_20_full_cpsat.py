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
SECOND_STAR_SCHEMA = "ls-3-4-20-second-star-branches-v1"


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


def cycles_of(permutation: dict[int, int]) -> list[tuple[int, ...]]:
    """Return directed cycles, each rotated to its least point."""

    unseen = set(permutation)
    cycles = []
    while unseen:
        start = min(unseen)
        cycle = []
        point = start
        while point in unseen:
            unseen.remove(point)
            cycle.append(point)
            point = permutation[point]
        if point != start:
            raise ValueError("second-star row is not a permutation")
        cycles.append(tuple(cycle))
    return sorted(cycles, key=lambda cycle: (len(cycle), cycle))


def conjugate_partial_to_branch(
    partial: list[int], branch: dict[str, object]
) -> tuple[list[int], dict[int, int]]:
    """Apply a diagonal point-colour relabelling to the branch representative."""

    domain = tuple(range(4, POINTS))
    source = {}
    for point in domain:
        assigned = partial[BLOCK_INDEX[(0, 1, 3, point)]]
        if assigned < 0:
            raise ValueError("partial must assign the complete second-star row")
        source[point] = assigned + 3
    units = branch["units"]
    target = {
        int(unit["point"]): int(unit["colour_point"])
        for unit in units
    }
    if set(source) != set(source.values()) or set(target) != set(target.values()):
        raise ValueError("second-star row is not a permutation of its domain")
    if any(source[point] == point for point in domain):
        raise ValueError("partial second-star row is not a derangement")

    source_cycles = cycles_of(source)
    target_cycles = cycles_of(target)
    if [len(cycle) for cycle in source_cycles] != [
        len(cycle) for cycle in target_cycles
    ]:
        raise ValueError("partial belongs to a different second-star branch")

    point_map = {0: 0, 1: 1, 2: 2, 3: 3}
    for source_cycle, target_cycle in zip(source_cycles, target_cycles):
        for old, new in zip(source_cycle, target_cycle):
            point_map[old] = new
    if set(point_map) != set(range(POINTS)):
        raise AssertionError("conjugating point map is incomplete")
    if set(point_map.values()) != set(range(POINTS)):
        raise AssertionError("conjugating point map is not bijective")
    for point in domain:
        if point_map[source[point]] != target[point_map[point]]:
            raise AssertionError("point map does not conjugate the row")

    transformed = [-1] * len(BLOCKS)
    for block, assigned in zip(BLOCKS, partial):
        new_block = tuple(sorted(point_map[point] for point in block))
        new_index = BLOCK_INDEX[new_block]
        if assigned >= 0:
            new_assigned = point_map[assigned + 3] - 3
            if transformed[new_index] >= 0:
                raise AssertionError("point relabelling collided on a block")
            transformed[new_index] = new_assigned
    return transformed, point_map


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
    parser.add_argument(
        "--second-star-manifest",
        type=Path,
        help="Verified 55-way second-star branch manifest",
    )
    parser.add_argument(
        "--second-star-branch-id",
        type=int,
        help="Fix one lossless second-star branch from the supplied manifest",
    )
    parser.add_argument(
        "--conjugate-hint-to-second-star",
        action="store_true",
        help=(
            "Diagonally relabel a normalized partial hint to the canonical "
            "representative of its selected second-star cycle type"
        ),
    )
    parser.add_argument("--log", action="store_true")
    args = parser.parse_args()
    if (args.second_star_manifest is None) != (
        args.second_star_branch_id is None
    ):
        parser.error(
            "--second-star-manifest and --second-star-branch-id "
            "must be supplied together"
        )
    if args.conjugate_hint_to_second_star and (
        args.hint is None or args.second_star_manifest is None
    ):
        parser.error(
            "--conjugate-hint-to-second-star requires both --hint and "
            "--second-star-manifest"
        )

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

    branch = None
    if args.second_star_manifest is not None:
        manifest = json.loads(
            args.second_star_manifest.read_text(encoding="utf-8")
        )
        if manifest.get("schema") != SECOND_STAR_SCHEMA:
            raise ValueError("wrong second-star manifest schema")
        branches = manifest.get("branches")
        branch_id = args.second_star_branch_id
        if (
            not isinstance(branches, list)
            or branch_id is None
            or not 0 <= branch_id < len(branches)
        ):
            raise ValueError("second-star branch id out of range")
        branch = branches[branch_id]
        if branch.get("id") != branch_id:
            raise ValueError("second-star branch ids are not canonical")
        units = branch.get("units")
        if not isinstance(units, list) or len(units) != 16:
            raise ValueError("second-star branch must contain 16 units")
        for unit in units:
            block = tuple(unit["block"])
            assigned = unit["colour"]
            if (
                block not in BLOCK_INDEX
                or not isinstance(assigned, int)
                or not 0 <= assigned < COLOURS
            ):
                raise ValueError("invalid second-star branch unit")
            model.Add(colour[BLOCK_INDEX[block]] == assigned)

    partial = None
    hint_point_map = None
    if args.hint is not None:
        partial = load_normalized_partial(args.hint)
        if args.conjugate_hint_to_second_star:
            if branch is None:
                raise AssertionError("missing selected branch")
            partial, hint_point_map = conjugate_partial_to_branch(
                partial, branch
            )
        if branch is not None:
            for unit in branch["units"]:
                assigned = partial[BLOCK_INDEX[tuple(unit["block"])]]
                if assigned >= 0 and assigned != unit["colour"]:
                    raise ValueError(
                        "normalized partial conflicts with second-star branch"
                    )
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
        "hint_conjugated_to_second_star": (
            args.conjugate_hint_to_second_star
        ),
        "hint_point_map": (
            [hint_point_map[point] for point in range(POINTS)]
            if hint_point_map is not None
            else None
        ),
        "second_star_manifest": (
            str(args.second_star_manifest)
            if args.second_star_manifest is not None
            else None
        ),
        "second_star_branch_id": (
            branch["id"] if branch is not None else None
        ),
        "second_star_cycle_type": (
            branch["cycle_type"] if branch is not None else None
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
