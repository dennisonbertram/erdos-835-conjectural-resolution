#!/usr/bin/env python3
"""Independent CP-SAT search for the cyclic prescribed-link radius-5 ansatz.

For every golf-square pair ij and every translation orbit of triples of
Z_17, ``selected[ij, orbit]`` records which translate has colour zero.
The per-slice constraints say that those forty triples decompose the
complement of the two prescribed zero-matchings.  The cross-slice
AllDifferent constraints make the resulting Q_ij values into the shared
N_uv list edge-colourings.

Any solution is expanded to all 12,600 N and 58,800 P values and passed to
``verify_radius5_golf_joint.py``.  This is a restricted, translation-
equivariant search for the fixed cyclic golf chart, not a global O_16 cover.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


EVIDENCE = Path(__file__).resolve().parents[1]
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))
from global_latin_audit import construct_golf17
from verify_radius5_golf_joint import (
    IJS,
    TRIPLES,
    UVS,
    golf_sha256,
    verify_payload,
)


P = 17
POINTS = tuple(range(P))
SQUARES = tuple(range(15))
MOVING_PAIRS = tuple(combinations(POINTS, 2))
MOVING_TRIPLES = tuple(combinations(POINTS, 3))


def translate(subset: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return tuple(sorted((x + amount) % P for x in subset))


def triple_orbits() -> tuple[
    list[tuple[int, int, int]],
    dict[tuple[int, int, int], tuple[int, int]],
]:
    representatives: list[tuple[int, int, int]] = []
    lookup: dict[tuple[int, int, int], tuple[int, int]] = {}
    unseen = set(MOVING_TRIPLES)
    while unseen:
        seed = min(unseen)
        orbit = [translate(seed, shift) for shift in POINTS]
        representative = min(orbit)
        orbit_index = len(representatives)
        representatives.append(representative)
        for shift in POINTS:
            triple = translate(representative, shift)
            assert triple not in lookup
            lookup[triple] = (orbit_index, shift)
            unseen.discard(triple)
    assert len(representatives) == 40
    assert len(lookup) == 680
    return representatives, lookup


REPRESENTATIVES, TRIPLE_LOOKUP = triple_orbits()


def build_model(golf, optimize_coverage: bool = False):
    model = cp_model.CpModel()
    selected = {}
    chosen = {}
    for i, j in IJS:
        for orbit_index in range(len(REPRESENTATIVES)):
            phase_choice = model.NewIntVar(
                0, P - 1, f"selected_{i}_{j}_{orbit_index}"
            )
            selected[i, j, orbit_index] = phase_choice
            literals = []
            for shift in POINTS:
                literal = model.NewBoolVar(
                    f"chosen_{i}_{j}_{orbit_index}_{shift}"
                )
                chosen[i, j, orbit_index, shift] = literal
                model.Add(phase_choice == shift).OnlyEnforceIf(literal)
                model.Add(phase_choice != shift).OnlyEnforceIf(literal.Not())
                literals.append(literal)
            model.AddExactlyOne(literals)

    triples_on_pair: dict[
        tuple[int, int], list[tuple[int, int]]
    ] = {pair: [] for pair in MOVING_PAIRS}
    for orbit_index, representative in enumerate(REPRESENTATIVES):
        for shift in POINTS:
            triple = translate(representative, shift)
            for pair in combinations(triple, 2):
                triples_on_pair[pair].append((orbit_index, shift))
    assert all(len(occurrences) == 15 for occurrences in triples_on_pair.values())

    edge_equations = 0
    coverage_literals = []
    for i, j in IJS:
        zero_leave = {
            pair
            for pair in MOVING_PAIRS
            if golf[i][pair[0]][pair[1]] == 0
            or golf[j][pair[0]][pair[1]] == 0
        }
        assert len(zero_leave) == 16
        for moving_pair, occurrences in triples_on_pair.items():
            literals = [
                chosen[i, j, orbit_index, shift]
                for orbit_index, shift in occurrences
            ]
            if moving_pair in zero_leave:
                model.Add(sum(literals) == 0)
            elif optimize_coverage:
                covered = model.NewBoolVar(
                    f"covered_{i}_{j}_{moving_pair[0]}_{moving_pair[1]}"
                )
                model.AddMaxEquality(covered, literals)
                coverage_literals.append(covered)
            else:
                model.Add(sum(literals) == 1)
            edge_equations += 1

    # In every exact colour-zero triangle decomposition the two prescribed
    # zero-matchings both miss vertex 0 and cover every other moving vertex.
    # The residual degrees are therefore 16 at 0 and 14 elsewhere, so the
    # selected triangles contain vertex 0 eight times and every other vertex
    # seven times.  These equations are redundant in the exact model but
    # materially tighten the max-coverage relaxation.
    vertex_degree_equations = 0
    for i, j in IJS:
        for vertex in POINTS:
            incident = []
            for orbit_index, representative in enumerate(REPRESENTATIVES):
                for shift in POINTS:
                    if vertex in translate(representative, shift):
                        incident.append(chosen[i, j, orbit_index, shift])
            assert len(incident) == 120
            model.Add(sum(incident) == (8 if vertex == 0 else 7))
            vertex_degree_equations += 1

    # The colour of a representative is minus its selected zero-translate.
    # Negation is a permutation of Z_17, so requiring selected shifts to be
    # distinct is exactly the shared-N edge-colouring condition.  Translation
    # covariance propagates it from one representative to its whole orbit.
    cross_all_different = 0
    for fixed_point in SQUARES:
        incident = [
            (min(fixed_point, other), max(fixed_point, other))
            for other in SQUARES
            if other != fixed_point
        ]
        for orbit_index in range(len(REPRESENTATIVES)):
            model.AddAllDifferent(
                [
                    selected[i, j, orbit_index]
                    for i, j in incident
                ]
            )
            cross_all_different += 1

    stats = {
        "phase_integer_variables": len(selected),
        "one_hot_boolean_variables": len(chosen),
        "phase_exactly_one": len(selected),
        "colour_zero_edge_equations": edge_equations,
        "cross_slice_all_different": cross_all_different,
        "forced_vertex_degree_equations": vertex_degree_equations,
    }
    assert stats == {
        "phase_integer_variables": 4200,
        "one_hot_boolean_variables": 71400,
        "phase_exactly_one": 4200,
        "colour_zero_edge_equations": 14280,
        "cross_slice_all_different": 600,
        "forced_vertex_degree_equations": 1785,
    }
    if optimize_coverage:
        assert len(coverage_literals) == len(IJS) * 120 == 12600
        model.Maximize(sum(coverage_literals))
    return model, selected, stats, coverage_literals


def add_phase_hints(
    model, selected, source: Path
) -> dict[tuple[int, int, int], int]:
    payload = json.loads(source.read_text(encoding="utf-8"))
    hinted_values = {}
    for key, phases in payload.items():
        i, j = map(int, key.split(","))
        if (i, j) not in IJS:
            continue
        if not isinstance(phases, list) or len(phases) != 40:
            raise ValueError(f"wrong phase list for {key}")
        for orbit_index, phase in enumerate(phases):
            if not isinstance(phase, int) or not 0 <= phase < P:
                raise ValueError(f"bad phase in {key}")
            value = (-phase) % P
            model.AddHint(selected[i, j, orbit_index], value)
            hinted_values[i, j, orbit_index] = value
    return hinted_values


def construct_orbit_hints(
    golf,
    seconds_per_orbit: float,
    seed: int,
    fixed_values: dict[tuple[int, int, int], int] | None = None,
):
    """Build a coherent cross-slice seed one triple orbit at a time.

    For one orbit, every fixed-pair phase has a static domain: selecting a
    translate whose triple meets either prescribed zero-matching is forbidden.
    The shared-N condition is then an exact list edge-colouring of K_15.
    These forty problems are independent and small.  Their solutions are only
    hints because they need not satisfy the per-slice edge covers jointly.
    """
    answer = {}
    solved = 0
    for orbit_index, representative in enumerate(REPRESENTATIVES):
        local = cp_model.CpModel()
        values = {}
        for i, j in IJS:
            domain = []
            for shift in POINTS:
                triple = translate(representative, shift)
                if all(
                    golf[i][x][y] != 0 and golf[j][x][y] != 0
                    for x, y in combinations(triple, 2)
                ):
                    domain.append(shift)
            assert domain
            values[i, j] = local.NewIntVarFromDomain(
                cp_model.Domain.FromValues(domain),
                f"orbit_hint_{orbit_index}_{i}_{j}",
            )
            if fixed_values is not None and (i, j, orbit_index) in fixed_values:
                local.Add(
                    values[i, j] == fixed_values[i, j, orbit_index]
                )
        for fixed_point in SQUARES:
            local.AddAllDifferent(
                [
                    values[
                        min(fixed_point, other),
                        max(fixed_point, other),
                    ]
                    for other in SQUARES
                    if other != fixed_point
                ]
            )
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = seconds_per_orbit
        solver.parameters.num_search_workers = 1
        solver.parameters.random_seed = seed + orbit_index
        status = solver.Solve(local)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        solved += 1
        for i, j in IJS:
            answer[i, j, orbit_index] = solver.Value(values[i, j])
    return answer, solved


def phases_from_solver(solver, selected) -> dict[str, list[int]]:
    return {
        f"{i},{j}": [
            (-solver.Value(selected[i, j, orbit_index])) % P
            for orbit_index in range(len(REPRESENTATIVES))
        ]
        for i, j in IJS
    }


def colour_from_phases(
    triple: tuple[int, int, int], phases: list[int]
) -> int:
    orbit_index, shift = TRIPLE_LOOKUP[tuple(sorted(triple))]
    return (phases[orbit_index] + shift) % P


def full_radius5_payload(phases, golf, stats):
    n_values = [
        colour_from_phases(
            (u, v, 16),
            phases[f"{i},{j}"],
        )
        for u, v in UVS
        for i, j in IJS
    ]
    p_values = [
        colour_from_phases(
            (u, v, w),
            phases[f"{i},{j}"],
        )
        for i, j in IJS
        for u, v, w in TRIPLES
    ]
    payload = {
        "schema": "odd-graph-o16-radius5-fixed-golf-joint-v1",
        "golf_sha256": golf_sha256(golf),
        "counts": {
            **stats,
            "n_variables": len(n_values),
            "p_variables": len(p_values),
        },
        "n_order": "uv-major then ij-major, lexicographic combinations",
        "n_values": n_values,
        "p_order": "ij-major then uvw-major, lexicographic combinations",
        "p_values": p_values,
    }
    canonical = (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    payload["sha256_without_hash"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--hint", type=Path)
    parser.add_argument(
        "--orbit-hint-seconds",
        type=float,
        default=0.0,
        help="solve each of 40 independent orbit list-edge-colourings as a hint",
    )
    parser.add_argument("--phase-output", type=Path)
    parser.add_argument(
        "--orbit-hint-output",
        type=Path,
        help="write the coherent 4200-value orbit seed before the joint solve",
    )
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument(
        "--optimize-coverage",
        action="store_true",
        help="maximize covered residual edges; objective 12600 is exact feasibility",
    )
    args = parser.parse_args()

    golf = construct_golf17()
    model, selected, stats, coverage_literals = build_model(
        golf, optimize_coverage=args.optimize_coverage
    )
    hinted_values = (
        add_phase_hints(model, selected, args.hint)
        if args.hint is not None
        else {}
    )
    orbit_hints = {}
    solved_hint_orbits = 0
    if args.orbit_hint_seconds > 0:
        orbit_hints, solved_hint_orbits = construct_orbit_hints(
            golf,
            args.orbit_hint_seconds,
            args.seed,
            fixed_values=hinted_values,
        )
        for key, value in orbit_hints.items():
            if key not in hinted_values:
                model.AddHint(selected[key], value)
                hinted_values[key] = value
    hinted = len(hinted_values)
    if args.orbit_hint_output is not None:
        if len(hinted_values) != len(IJS) * len(REPRESENTATIVES):
            raise ValueError(
                "--orbit-hint-output requires all 4200 phase hints"
            )
        seed_phases = {
            f"{i},{j}": [
                (-hinted_values[i, j, orbit_index]) % P
                for orbit_index in range(len(REPRESENTATIVES))
            ]
            for i, j in IJS
        }
        args.orbit_hint_output.write_text(
            json.dumps(seed_phases, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.audit_only:
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "counts": stats,
                    "hinted_phase_integers": hinted,
                    "solved_hint_orbits": solved_hint_orbits,
                    "triple_orbits": len(REPRESENTATIVES),
                    "coverage_objective_maximum": len(coverage_literals),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    if hinted:
        solver.parameters.repair_hint = True
        solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    result = {
        "status": solver.StatusName(status),
        "counts": stats,
        "hinted_phase_integers": hinted,
        "solved_hint_orbits": solved_hint_orbits,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    if args.optimize_coverage and status in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE,
    ):
        result["coverage_objective"] = int(round(solver.ObjectiveValue()))
        result["coverage_best_bound"] = int(round(solver.BestObjectiveBound()))
        result["coverage_objective_maximum"] = 12600
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        phases = phases_from_solver(solver, selected)
        if args.phase_output is not None:
            args.phase_output.write_text(
                json.dumps(phases, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        exact = (
            not args.optimize_coverage
            or int(round(solver.ObjectiveValue())) == 12600
        )
        if exact:
            payload = full_radius5_payload(phases, golf, stats)
            report = verify_payload(payload, semantic_ball=True)
            result["semantic_verifier"] = report
            result["certificate_sha256_without_hash"] = payload[
                "sha256_without_hash"
            ]
            if args.certificate is not None:
                args.certificate.write_text(
                    json.dumps(
                        payload,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                    + "\n",
                    encoding="utf-8",
                )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
