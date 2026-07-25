#!/usr/bin/env python3
"""Reduced exact CP-SAT model for the cyclic Wallis degree relaxation.

This is equivalent to ``search_cyclic17_vertex_degree_sat.py`` but uses two
exact redundancies.

First, for a fixed triple orbit and golf square, the fourteen incident
fixed-pair edges use every one of the fourteen allowed shifts exactly once.
We encode those constraints directly as ``ExactlyOne`` constraints.

Second, the degree equations need only be imposed for sixteen moving points
on ninety fixed-pair edges.  The seventeenth point follows because every
fixed-pair slice selects forty triples.  The omitted fifteen fixed-pair edges
are

    01, 12, 02, 03, 04, ..., 0,14.

Their unsigned incidence matrix is nonsingular: the twelve leaves first
force the star-edge deviations to zero, and the remaining triangle then
forces its three deviations to zero.  Cross-shift permutations force the
sum of the degree deviations on all edges incident with any fixed point to
be zero, so all omitted degree equations follow.

The edge-position collision constraints of the full radius-five quotient
remain omitted.  SAT is therefore only a degree-correct seed.  UNSAT would
exclude the fixed-Wallis, C17-equivariant joint layer only after a portable
proof; CP-SAT status alone is not such a proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    POINTS,
    REPRESENTATIVES,
    REPRESENTATIVE_EDGE_COORDINATES,
    SQUARES,
    allowed_shifts,
    translate,
    zero_positions,
)
from search_cyclic17_vertex_degree_sat import verify_relaxation


OMITTED_PAIRS = (
    (0, 1),
    (1, 2),
    (0, 2),
    *((0, fixed_point) for fixed_point in range(3, 15)),
)
OMITTED_PAIR_SET = frozenset(OMITTED_PAIRS)
ENFORCED_PAIRS = tuple(
    fixed_pair
    for fixed_pair in FIXED_PAIRS
    if fixed_pair not in OMITTED_PAIR_SET
)
ENFORCED_POINTS = POINTS[:-1]


def forbidden_shifts(zeros):
    return {
        (fixed_point, orbit_index): frozenset(
            (
                zeros[fixed_point, difference] - offset
            )
            % P
            for difference, offset
            in REPRESENTATIVE_EDGE_COORDINATES[orbit_index]
        )
        for fixed_point in SQUARES
        for orbit_index in range(len(REPRESENTATIVES))
    }


def build_model(golf, *, all_degrees: bool = False):
    zeros = zero_positions(golf)
    forbidden = forbidden_shifts(zeros)
    assert all(len(values) == 3 for values in forbidden.values())

    model = cp_model.CpModel()
    domains = {}
    choose = {}
    phase_exactly_one = 0
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            domain = tuple(
                allowed_shifts((i, j), orbit_index, zeros)
            )
            domains[i, j, orbit_index] = domain
            literals = []
            for shift in domain:
                literal = model.NewBoolVar(
                    f"x_{i}_{j}_{orbit_index}_{shift}"
                )
                choose[i, j, orbit_index, shift] = literal
                literals.append(literal)
            model.AddExactlyOne(literals)
            phase_exactly_one += 1

    # At a fixed point and orbit, the incident phases form a permutation of
    # the fourteen shifts not forbidden by that square's zero matching.
    cross_exactly_one = 0
    cross_literal_memberships = 0
    for fixed_point in SQUARES:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in POINTS:
                if shift in forbidden[fixed_point, orbit_index]:
                    continue
                literals = []
                for other in SQUARES:
                    if other == fixed_point:
                        continue
                    i, j = sorted((fixed_point, other))
                    literal = choose.get(
                        (i, j, orbit_index, shift)
                    )
                    if literal is not None:
                        literals.append(literal)
                assert literals
                model.AddExactlyOne(literals)
                cross_exactly_one += 1
                cross_literal_memberships += len(literals)

    degree_pairs = FIXED_PAIRS if all_degrees else ENFORCED_PAIRS
    degree_points = POINTS if all_degrees else ENFORCED_POINTS
    vertex_degree_equalities = 0
    degree_literal_memberships = 0
    for i, j in degree_pairs:
        for moving_point in degree_points:
            literals = []
            for orbit_index, representative in enumerate(
                REPRESENTATIVES
            ):
                for shift in domains[i, j, orbit_index]:
                    if moving_point in translate(
                        representative, shift
                    ):
                        literals.append(
                            choose[i, j, orbit_index, shift]
                        )
            model.Add(
                sum(literals)
                == (8 if moving_point == 0 else 7)
            )
            vertex_degree_equalities += 1
            degree_literal_memberships += len(literals)

    stats = {
        "primary_boolean_variables": len(choose),
        "phase_exactly_one": phase_exactly_one,
        "cross_exactly_one": cross_exactly_one,
        "cross_literal_memberships": cross_literal_memberships,
        "vertex_degree_equalities": vertex_degree_equalities,
        "degree_literal_memberships": degree_literal_memberships,
        "enforced_fixed_pairs": len(degree_pairs),
        "enforced_moving_points": len(degree_points),
        "omitted_pair_basis_size": (
            0 if all_degrees else len(OMITTED_PAIRS)
        ),
        "edge_position_collision_constraints": 0,
    }
    assert stats["primary_boolean_variables"] == 47880
    assert stats["phase_exactly_one"] == 4200
    assert stats["cross_exactly_one"] == 8400
    if not all_degrees:
        assert stats["vertex_degree_equalities"] == 1440
        assert stats["enforced_fixed_pairs"] == 90
        assert stats["enforced_moving_points"] == 16
        assert stats["omitted_pair_basis_size"] == 15
    return model, choose, domains, stats


def read_hint(source: Path):
    payload = json.loads(source.read_text(encoding="utf-8"))
    if set(payload) != {f"{i},{j}" for i, j in FIXED_PAIRS}:
        raise ValueError("phase hint must contain all 105 fixed pairs")
    return payload


def add_hints(model, choose, domains, source: Path) -> int:
    payload = read_hint(source)
    hinted = 0
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        if not isinstance(phases, list) or len(phases) != 40:
            raise ValueError(f"wrong phase hint for {i},{j}")
        for orbit_index, phase in enumerate(phases):
            selected = (-phase) % P
            if selected not in domains[i, j, orbit_index]:
                raise ValueError(
                    f"hint violates phase domain at {i},{j},{orbit_index}"
                )
            for shift in domains[i, j, orbit_index]:
                model.AddHint(
                    choose[i, j, orbit_index, shift],
                    int(shift == selected),
                )
                hinted += 1
    return hinted


def phases_from_solver(solver, choose, domains):
    answer = {}
    for i, j in FIXED_PAIRS:
        phases = []
        for orbit_index in range(len(REPRESENTATIVES)):
            selected = [
                shift for shift in domains[i, j, orbit_index]
                if solver.Value(
                    choose[i, j, orbit_index, shift]
                )
            ]
            assert len(selected) == 1
            phases.append((-selected[0]) % P)
        answer[f"{i},{j}"] = phases
    return answer


def verify_aggregate_identity(golf) -> None:
    """Check the exact identity used to omit fifteen fixed-pair equations."""
    zeros = zero_positions(golf)
    forbidden = forbidden_shifts(zeros)
    singleton_holes = Counter()
    triple_vertex_counts = Counter()
    triple_pair_counts = Counter()
    triple_holes = 0
    for orbit_index in range(len(REPRESENTATIVES)):
        for shift in POINTS:
            holes = tuple(
                fixed_point
                for fixed_point in SQUARES
                if shift in forbidden[fixed_point, orbit_index]
            )
            assert len(holes) in (1, 3)
            if len(holes) == 1:
                singleton_holes[holes[0]] += 1
            else:
                triple_holes += 1
                triple_vertex_counts.update(holes)
                triple_pair_counts.update(combinations(holes, 2))
    assert triple_holes == 560
    assert singleton_holes == Counter(
        {fixed_point: 8 for fixed_point in SQUARES}
    )
    assert triple_vertex_counts == Counter(
        {fixed_point: 112 for fixed_point in SQUARES}
    )
    assert triple_pair_counts == Counter(
        {fixed_pair: 16 for fixed_pair in FIXED_PAIRS}
    )

    target = [14 * (8 if point == 0 else 7) for point in POINTS]
    for fixed_point in SQUARES:
        aggregate = Counter()
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            forbidden = {
                (
                    zeros[fixed_point, difference] - offset
                )
                % P
                for difference, offset
                in REPRESENTATIVE_EDGE_COORDINATES[orbit_index]
            }
            for shift in POINTS:
                if shift not in forbidden:
                    aggregate.update(
                        translate(representative, shift)
                    )
        assert [aggregate[point] for point in POINTS] == target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=1200.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--all-degrees", action="store_true")
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    golf = construct_golf17()
    verify_aggregate_identity(golf)
    model, choose, domains, stats = build_model(
        golf, all_degrees=args.all_degrees
    )
    hinted = (
        add_hints(model, choose, domains, args.hint)
        if args.hint is not None
        else 0
    )
    if args.audit_only:
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "counts": stats,
                    "hinted_primary_booleans": hinted,
                    "aggregate_degree_identity": "PASS",
                    "prescribed_hole_multidesign": "PASS",
                    "scope": "exact vertex-degree relaxation",
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
    report = {
        "status": solver.StatusName(status),
        "counts": stats,
        "hinted_primary_booleans": hinted,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
        "portable_unsat_proof": False,
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        phases = phases_from_solver(solver, choose, domains)
        verify_relaxation(phases, domains)
        encoded = (
            json.dumps(phases, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        if args.output is not None:
            args.output.write_bytes(encoded)
        report.update(
            {
                "status": "FEASIBLE_RELAXATION",
                "phase_sha256": hashlib.sha256(encoded).hexdigest(),
                "semantic_relaxation_verifier": "PASS",
            }
        )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
