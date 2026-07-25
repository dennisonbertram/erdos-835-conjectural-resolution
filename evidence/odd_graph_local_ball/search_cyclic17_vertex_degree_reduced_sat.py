#!/usr/bin/env python3
"""Smaller proof-capable SAT encoding of the cyclic Wallis degree relaxation.

This formula is logically equivalent to
``search_cyclic17_vertex_degree_sat.py``.  It applies three exact reductions:

* cross constraints are encoded as 8,400 ``ExactlyOne`` constraints, since
  the fourteen incident pair-edges use all fourteen allowed shifts;
* only sixteen moving-point degrees on ninety fixed-pair edges are imposed,
  using the exact omitted-edge basis from
  ``search_cyclic17_vertex_degree_reduced.py``;
* a membership variable records whether one selected translated triple
  contains one moving point, so each degree cardinality has forty inputs
  rather than roughly eighty primary phase literals.

The full residual-edge collision constraints remain omitted.  SAT gives only
a degree-correct seed.  A checked UNSAT proof would exclude only the fixed
Wallis, C17-equivariant joint layer, not Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from search_cyclic17_vertex_degree_reduced import (
    ENFORCED_PAIRS,
    ENFORCED_POINTS,
    forbidden_shifts,
    verify_aggregate_identity,
)
from search_cyclic17_vertex_degree_sat import (
    phases_from_model,
    preferred_literals,
    read_competition_solution,
    verify_relaxation,
)
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    allowed_shifts,
    translate,
    zero_positions,
)


def add_cardinality(
    clauses,
    literals,
    *,
    bound: int,
    pool: IDPool,
    encoding: int,
) -> None:
    clauses.extend(
        CardEnc.equals(
            lits=literals,
            bound=bound,
            vpool=pool,
            encoding=encoding,
        ).clauses
    )


def build_cnf(golf, degree_encoding: int = EncType.kmtotalizer):
    zeros = zero_positions(golf)
    forbidden = forbidden_shifts(zeros)
    domains = {
        (i, j, orbit_index): tuple(
            allowed_shifts((i, j), orbit_index, zeros)
        )
        for i, j in FIXED_PAIRS
        for orbit_index in range(len(REPRESENTATIVES))
    }

    pool = IDPool()
    variable = {}
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in domains[i, j, orbit_index]:
                key = i, j, orbit_index, shift
                variable[key] = pool.id(("phase",) + key)
    primary_variables = pool.top
    assert primary_variables == 47880

    clauses = []
    phase_exactly_one = 0
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            add_cardinality(
                clauses,
                [
                    variable[i, j, orbit_index, shift]
                    for shift in domains[i, j, orbit_index]
                ],
                bound=1,
                pool=pool,
                encoding=EncType.seqcounter,
            )
            phase_exactly_one += 1

    cross_groups = defaultdict(list)
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in domains[i, j, orbit_index]:
                literal = variable[i, j, orbit_index, shift]
                cross_groups[i, orbit_index, shift].append(literal)
                cross_groups[j, orbit_index, shift].append(literal)

    cross_exactly_one = 0
    cross_literal_memberships = 0
    for fixed_point in SQUARES:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in POINTS:
                if shift in forbidden[fixed_point, orbit_index]:
                    assert not cross_groups.get(
                        (fixed_point, orbit_index, shift)
                    )
                    continue
                literals = cross_groups[
                    fixed_point, orbit_index, shift
                ]
                assert literals
                add_cardinality(
                    clauses,
                    literals,
                    bound=1,
                    pool=pool,
                    encoding=EncType.seqcounter,
                )
                cross_exactly_one += 1
                cross_literal_memberships += len(literals)

    membership = {}
    membership_link_clauses = 0
    membership_primary_literals = 0
    constant_zero_memberships = 0
    for i, j in ENFORCED_PAIRS:
        for moving_point in ENFORCED_POINTS:
            for orbit_index, representative in enumerate(
                REPRESENTATIVES
            ):
                source_literals = [
                    variable[i, j, orbit_index, shift]
                    for shift in domains[i, j, orbit_index]
                    if moving_point in translate(
                        representative, shift
                    )
                ]
                if not source_literals:
                    constant_zero_memberships += 1
                    continue
                member = pool.id(
                    (
                        "membership",
                        i,
                        j,
                        moving_point,
                        orbit_index,
                    )
                )
                membership[
                    i, j, moving_point, orbit_index
                ] = member
                # member iff at least one of the source phase literals.
                clauses.extend(
                    [-literal, member]
                    for literal in source_literals
                )
                clauses.append([-member] + source_literals)
                membership_link_clauses += len(source_literals) + 1
                membership_primary_literals += len(source_literals)

    membership_variables = len(membership)
    assert (
        membership_variables + constant_zero_memberships
        == 90 * 16 * 40
    )

    vertex_degree_equalities = 0
    for i, j in ENFORCED_PAIRS:
        for moving_point in ENFORCED_POINTS:
            degree_members = []
            for orbit_index in range(len(REPRESENTATIVES)):
                member = membership.get(
                    (i, j, moving_point, orbit_index)
                )
                if member is not None:
                    degree_members.append(member)
            add_cardinality(
                clauses,
                degree_members,
                bound=8 if moving_point == 0 else 7,
                pool=pool,
                encoding=degree_encoding,
            )
            vertex_degree_equalities += 1

    stats = {
        "primary_variables": primary_variables,
        "membership_variables": membership_variables,
        "constant_zero_memberships": constant_zero_memberships,
        "total_variables": pool.top,
        "clauses": len(clauses),
        "phase_exactly_one": phase_exactly_one,
        "cross_exactly_one": cross_exactly_one,
        "cross_literal_memberships": cross_literal_memberships,
        "vertex_degree_equalities": vertex_degree_equalities,
        "membership_link_clauses": membership_link_clauses,
        "membership_primary_literals": membership_primary_literals,
        "enforced_fixed_pairs": len(ENFORCED_PAIRS),
        "enforced_moving_points": len(ENFORCED_POINTS),
        "edge_position_collision_constraints": 0,
    }
    assert stats["phase_exactly_one"] == 4200
    assert stats["cross_exactly_one"] == 8400
    assert stats["vertex_degree_equalities"] == 1440
    return clauses, variable, domains, stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", default="maplechrono")
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dimacs", type=Path)
    parser.add_argument("--verify-solution", type=Path)
    parser.add_argument(
        "--degree-encoding",
        choices=("kmtotalizer", "sequential"),
        default="kmtotalizer",
    )
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    golf = construct_golf17()
    verify_aggregate_identity(golf)
    degree_encoding = (
        EncType.kmtotalizer
        if args.degree_encoding == "kmtotalizer"
        else EncType.seqcounter
    )
    clauses, variable, domains, stats = build_cnf(
        golf, degree_encoding
    )
    stats["degree_encoding"] = args.degree_encoding
    preferred = (
        preferred_literals(args.hint, variable, domains)
        if args.hint is not None
        else []
    )
    if args.dimacs is not None:
        CNF(from_clauses=clauses).to_file(args.dimacs)
        stats["dimacs_sha256"] = hashlib.sha256(
            args.dimacs.read_bytes()
        ).hexdigest()
    if args.audit_only:
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "counts": stats,
                    "hinted_primary_literals": len(preferred),
                    "aggregate_degree_identity": "PASS",
                    "prescribed_hole_multidesign": "PASS",
                    "scope": "exact vertex-degree relaxation",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    if args.verify_solution is not None:
        phases = phases_from_model(
            read_competition_solution(args.verify_solution),
            variable,
            domains,
        )
        verify_relaxation(phases, domains)
        encoded = (
            json.dumps(phases, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        if args.output is not None:
            args.output.write_bytes(encoded)
        print(
            json.dumps(
                {
                    "status": "FEASIBLE_RELAXATION",
                    "counts": stats,
                    "phase_sha256": hashlib.sha256(encoded).hexdigest(),
                    "semantic_relaxation_verifier": "PASS",
                    "source": str(args.verify_solution),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    phase_hint_applied = False
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        if preferred:
            try:
                solver.set_phases(preferred)
                phase_hint_applied = True
            except NotImplementedError:
                pass
        satisfiable = solver.solve()
        if not satisfiable:
            print(
                json.dumps(
                    {
                        "status": "INFEASIBLE",
                        "portable_proof": False,
                        "counts": stats,
                        "phase_hint_applied": phase_hint_applied,
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return
        positive = {
            literal for literal in solver.get_model()
            if literal > 0
        }

    phases = phases_from_model(positive, variable, domains)
    verify_relaxation(phases, domains)
    encoded = (
        json.dumps(phases, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if args.output is not None:
        args.output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "status": "FEASIBLE_RELAXATION",
                "counts": stats,
                "phase_hint_applied": phase_hint_applied,
                "phase_sha256": hashlib.sha256(encoded).hexdigest(),
                "semantic_relaxation_verifier": "PASS",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
