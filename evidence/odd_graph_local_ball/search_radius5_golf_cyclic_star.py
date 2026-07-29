#!/usr/bin/env python3
"""Solve one exact 14-row star in the cyclic Wallis radius-five quotient.

Fix one of the fifteen Wallis squares i.  The fourteen pair rows {i,j} must
each be an exact residual triangle decomposition, while for every one of the
forty moving-triple orbits their fourteen phases must be all different.  This
560-phase model imposes precisely those 14*8 row constraints and 40 cross
constraints.

Every full fixed-Wallis C17 layer restricts to a solution of every star.
Consequently a portable proof of infeasibility for even one star would exclude
that ansatz.  A star witness, however, is only a necessary local piece.  It
does not glue the other fourteen stars and does not solve Erdos-Rosenfeld
#835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from improve_radius5_golf_cyclic_slice_lns import (
    audit_static,
    domains_for_seed,
    dump_phases,
    load_state,
    slice_scores,
)
from search_radius5_golf_cyclic_alternating_projection import cross_distinct
from search_radius5_golf_cyclic_compact import (
    DIFFERENCES,
    FIXED_PAIRS,
    P,
    POINTS,
    REPRESENTATIVE_EDGE_COORDINATES,
    REPRESENTATIVES,
    SQUARES,
    allowed_shifts,
    zero_positions,
)


def incident_pair(first: int, second: int) -> tuple[int, int]:
    return min(first, second), max(first, second)


def build_star(
    centre: int,
    source,
    *,
    optimize_outer: bool,
    minimize_cross: bool = False,
):
    if optimize_outer and minimize_cross:
        raise ValueError("the two star objectives are mutually exclusive")
    zeros = zero_positions(construct_golf17())
    model = cp_model.CpModel()
    selected = {}
    pairs = [
        incident_pair(centre, other)
        for other in SQUARES
        if other != centre
    ]
    for fixed_pair in pairs:
        for orbit_index in range(len(REPRESENTATIVES)):
            domain = allowed_shifts(
                fixed_pair,
                orbit_index,
                zeros,
            )
            selected[fixed_pair + (orbit_index,)] = (
                model.NewIntVarFromDomain(
                    cp_model.Domain.FromValues(domain),
                    f"phase_{fixed_pair[0]}_{fixed_pair[1]}_"
                    f"{orbit_index}",
                )
            )
            if source is not None:
                model.AddHint(
                    selected[fixed_pair + (orbit_index,)],
                    source[fixed_pair + (orbit_index,)],
                )

    positions = defaultdict(list)
    modular_equalities = 0
    for fixed_pair in pairs:
        i, j = fixed_pair
        for orbit_index, coordinates in enumerate(
            REPRESENTATIVE_EDGE_COORDINATES
        ):
            phase = selected[fixed_pair + (orbit_index,)]
            for occurrence, (difference, offset) in enumerate(coordinates):
                residual = [
                    value
                    for value in POINTS
                    if value
                    not in {
                        zeros[i, difference],
                        zeros[j, difference],
                    }
                ]
                position = model.NewIntVarFromDomain(
                    cp_model.Domain.FromValues(residual),
                    f"pos_{i}_{j}_{orbit_index}_{occurrence}",
                )
                model.AddModuloEquality(position, phase + offset, P)
                positions[fixed_pair + (difference,)].append(position)
                modular_equalities += 1

    for fixed_pair in pairs:
        i, j = fixed_pair
        for difference in DIFFERENCES:
            variables = positions[fixed_pair + (difference,)]
            if len(variables) != 15:
                raise AssertionError("wrong star difference multiplicity")
            model.AddAllDifferent(variables)
            model.Add(
                sum(variables)
                == sum(POINTS)
                - zeros[i, difference]
                - zeros[j, difference]
            )

    cross_collision_literals = []
    for orbit_index, coordinates in enumerate(
        REPRESENTATIVE_EDGE_COORDINATES
    ):
        variables = [
            selected[fixed_pair + (orbit_index,)]
            for fixed_pair in pairs
        ]
        forbidden = {
            (zeros[centre, difference] - offset) % P
            for difference, offset in coordinates
        }
        if len(forbidden) != 3:
            raise AssertionError("wrong forbidden-phase set")
        if minimize_cross:
            for left, right in combinations(variables, 2):
                equal = model.NewBoolVar(
                    f"cross_equal_{orbit_index}_"
                    f"{len(cross_collision_literals)}"
                )
                model.Add(left == right).OnlyEnforceIf(equal)
                model.Add(left != right).OnlyEnforceIf(equal.Not())
                cross_collision_literals.append(equal)
        else:
            model.AddAllDifferent(variables)
            model.Add(
                sum(variables) == sum(POINTS) - sum(forbidden)
            )

    objective_terms = []
    if optimize_outer:
        if source is None:
            raise ValueError("--optimize-outer requires --source")
        for fixed_pair in pairs:
            outer = (
                fixed_pair[1]
                if fixed_pair[0] == centre
                else fixed_pair[0]
            )
            for orbit_index in range(len(REPRESENTATIVES)):
                phase = selected[fixed_pair + (orbit_index,)]
                other_values = {
                    source[
                        incident_pair(outer, other) + (orbit_index,)
                    ]
                    for other in SQUARES
                    if other not in fixed_pair
                }
                for value in sorted(
                    allowed_shifts(
                        fixed_pair,
                        orbit_index,
                        zeros,
                    )
                ):
                    if value in other_values:
                        continue
                    literal = model.NewBoolVar(
                        f"outer_new_{fixed_pair[0]}_{fixed_pair[1]}_"
                        f"{orbit_index}_{value}"
                    )
                    model.Add(phase == value).OnlyEnforceIf(literal)
                    model.Add(phase != value).OnlyEnforceIf(literal.Not())
                    objective_terms.append(literal)
        model.Maximize(sum(objective_terms))
    elif minimize_cross:
        model.Minimize(sum(cross_collision_literals))

    stats = {
        "centre": centre,
        "phase_integers": len(selected),
        "edge_position_integers": modular_equalities,
        "slice_all_different": len(pairs) * len(DIFFERENCES),
        "cross_all_different": (
            0 if minimize_cross else len(REPRESENTATIVES)
        ),
        "cross_collision_literals": len(cross_collision_literals),
        "outer_objective_literals": len(objective_terms),
    }
    if stats != {
        "centre": centre,
        "phase_integers": 560,
        "edge_position_integers": 1680,
        "slice_all_different": 112,
        "cross_all_different": 0 if minimize_cross else 40,
        "cross_collision_literals": 3640 if minimize_cross else 0,
        "outer_objective_literals": len(objective_terms),
    }:
        raise AssertionError("wrong star model counts")
    return model, selected, pairs, stats


def write_state(path: Path, state) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--centre", type=int, required=True)
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="complete 105-row exact seed used for hints and untouched rows",
    )
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--optimize-outer", action="store_true")
    parser.add_argument(
        "--minimize-cross",
        action="store_true",
        help="keep all rows exact but minimize star phase collisions",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    if args.centre not in SQUARES:
        parser.error("--centre must lie in 0,...,14")
    domains = domains_for_seed(construct_golf17())
    source = load_state(args.source) if args.source is not None else None
    if source is not None and set(slice_scores(source).values()) != {120}:
        raise ValueError("source must contain 105 exact pair rows")
    model, selected, pairs, stats = build_star(
        args.centre,
        source,
        optimize_outer=args.optimize_outer,
        minimize_cross=args.minimize_cross,
    )
    if args.audit_only:
        print(json.dumps({"status": "PASS", "counts": stats}, sort_keys=True))
        return

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    if source is not None:
        solver.parameters.repair_hint = True
        solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    report: dict[str, object] = {
        "status": solver.StatusName(status),
        "counts": stats,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        if source is None:
            state = {}
        else:
            state = dict(source)
        for fixed_pair in pairs:
            for orbit_index in range(len(REPRESENTATIVES)):
                state[fixed_pair + (orbit_index,)] = solver.Value(
                    selected[fixed_pair + (orbit_index,)]
                )
        for fixed_pair in pairs:
            if slice_scores(state)[fixed_pair] != 120:
                raise AssertionError("star output row is not exact")
        exact_cross_groups = 0
        collision_pairs = 0
        for orbit_index in range(len(REPRESENTATIVES)):
            values = [
                state[fixed_pair + (orbit_index,)]
                for fixed_pair in pairs
            ]
            counts = {
                value: values.count(value) for value in set(values)
            }
            exact_cross_groups += len(counts) == 14
            collision_pairs += sum(
                multiplicity * (multiplicity - 1) // 2
                for multiplicity in counts.values()
            )
        if not args.minimize_cross and exact_cross_groups != 40:
            raise AssertionError("star output cross group is not exact")
        report["verified_exact_rows"] = 14
        report["verified_cross_groups"] = exact_cross_groups
        report["star_collision_pairs"] = collision_pairs
        if args.minimize_cross:
            report["objective_value"] = solver.ObjectiveValue()
            report["best_objective_bound"] = solver.BestObjectiveBound()
        if source is not None:
            report["global_cross_distinct"] = cross_distinct(state)
            report["global_cross_target"] = 8400
            audit_static_candidate = False
            try:
                audit_static(state, domains)
                audit_static_candidate = True
            except ValueError:
                pass
            report["all_600_cross_groups_exact"] = audit_static_candidate
            if args.output is not None:
                report["phase_sha256"] = write_state(args.output, state)
        elif args.output is not None:
            partial = {
                f"{fixed_pair[0]},{fixed_pair[1]}": [
                    (-state[fixed_pair + (orbit_index,)]) % P
                    for orbit_index in range(len(REPRESENTATIVES))
                ]
                for fixed_pair in pairs
            }
            encoded = (
                json.dumps(partial, indent=2, sort_keys=True) + "\n"
            ).encode("utf-8")
            args.output.write_bytes(encoded)
            report["partial_sha256"] = hashlib.sha256(encoded).hexdigest()
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
