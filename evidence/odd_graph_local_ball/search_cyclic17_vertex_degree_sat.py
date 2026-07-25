#!/usr/bin/env python3
"""SAT relaxation for forced vertex degrees in the cyclic Wallis ansatz.

Keep exactly:

* one allowed phase for each of 4,200 fixed-pair/triple-orbit cells;
* the 10,200 phase-collision constraints making every orbit a proper
  list edge-colouring of K_15; and
* the 1,785 necessary selected-triple vertex-degree equations.

For each fixed pair, its forty selected triples must contain moving point
zero eight times and every other moving point seven times.  This follows
from the desired residual graph degrees 16 and 14 after deleting the two
zero one-factors.

The 12,600 edge-position collision constraints are deliberately omitted.
Thus SAT is only a degree-correct seed, while a proof-logged UNSAT result
would exclude the complete fixed-Wallis, C17-equivariant joint layer.
The PySAT status alone is diagnostic; use deterministic DIMACS plus an
independently checked proof before making an UNSAT claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
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
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    allowed_shifts,
    translate,
    zero_positions,
)


def build_cnf(golf, encoding: int = EncType.seqcounter):
    zeros = zero_positions(golf)
    domains = {}
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            domains[i, j, orbit_index] = tuple(
                allowed_shifts((i, j), orbit_index, zeros)
            )

    pool = IDPool()
    variable = {}
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in domains[i, j, orbit_index]:
                key = i, j, orbit_index, shift
                variable[key] = pool.id(key)
    primary_variables = pool.top
    assert primary_variables == 47880

    clauses: list[list[int]] = []
    phase_exactly_one = 0
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            clauses.extend(
                CardEnc.equals(
                    lits=[
                        variable[i, j, orbit_index, shift]
                        for shift in domains[i, j, orbit_index]
                    ],
                    bound=1,
                    vpool=pool,
                    encoding=encoding,
                ).clauses
            )
            phase_exactly_one += 1

    degree_groups: dict[
        tuple[int, int, int], list[int]
    ] = defaultdict(list)
    for i, j in FIXED_PAIRS:
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            for shift in domains[i, j, orbit_index]:
                literal = variable[i, j, orbit_index, shift]
                for moving_point in translate(representative, shift):
                    degree_groups[i, j, moving_point].append(literal)

    vertex_degree_equalities = 0
    degree_literal_memberships = 0
    for i, j in FIXED_PAIRS:
        for moving_point in POINTS:
            literals = degree_groups[i, j, moving_point]
            target = 8 if moving_point == 0 else 7
            assert len(literals) >= target
            degree_literal_memberships += len(literals)
            clauses.extend(
                CardEnc.equals(
                    lits=literals,
                    bound=target,
                    vpool=pool,
                    encoding=encoding,
                ).clauses
            )
            vertex_degree_equalities += 1
    assert degree_literal_memberships == primary_variables * 3

    cross_groups: dict[tuple[int, int, int], list[int]] = defaultdict(list)
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in domains[i, j, orbit_index]:
                literal = variable[i, j, orbit_index, shift]
                cross_groups[i, orbit_index, shift].append(literal)
                cross_groups[j, orbit_index, shift].append(literal)

    cross_at_most_one = 0
    for fixed_point in SQUARES:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in POINTS:
                literals = cross_groups.get(
                    (fixed_point, orbit_index, shift), []
                )
                if len(literals) > 1:
                    clauses.extend(
                        CardEnc.atmost(
                            lits=literals,
                            bound=1,
                            vpool=pool,
                            encoding=encoding,
                        ).clauses
                    )
                cross_at_most_one += 1

    stats = {
        "primary_variables": primary_variables,
        "total_variables": pool.top,
        "clauses": len(clauses),
        "phase_exactly_one": phase_exactly_one,
        "vertex_degree_equalities": vertex_degree_equalities,
        "degree_literal_memberships": degree_literal_memberships,
        "cross_at_most_one": cross_at_most_one,
        "edge_position_collision_constraints": 0,
    }
    assert stats["phase_exactly_one"] == 4200
    assert stats["vertex_degree_equalities"] == 1785
    assert stats["degree_literal_memberships"] == 143640
    assert stats["cross_at_most_one"] == 10200
    return clauses, variable, domains, stats


def preferred_literals(source, variable, domains):
    payload = json.loads(source.read_text(encoding="utf-8"))
    if set(payload) != {f"{i},{j}" for i, j in FIXED_PAIRS}:
        raise ValueError("phase hint must contain all 105 fixed pairs")
    answer = []
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
            answer.extend(
                variable[i, j, orbit_index, shift]
                if shift == selected
                else -variable[i, j, orbit_index, shift]
                for shift in domains[i, j, orbit_index]
            )
    return answer


def phases_from_model(positive, variable, domains):
    answer = {}
    for i, j in FIXED_PAIRS:
        phases = []
        for orbit_index in range(len(REPRESENTATIVES)):
            selected = [
                shift for shift in domains[i, j, orbit_index]
                if variable[i, j, orbit_index, shift] in positive
            ]
            assert len(selected) == 1
            phases.append((-selected[0]) % P)
        answer[f"{i},{j}"] = phases
    return answer


def verify_relaxation(phases, domains):
    selected = {}
    for i, j in FIXED_PAIRS:
        for orbit_index, phase in enumerate(phases[f"{i},{j}"]):
            shift = (-phase) % P
            assert shift in domains[i, j, orbit_index]
            selected[i, j, orbit_index] = shift

    for fixed_point in SQUARES:
        for orbit_index in range(len(REPRESENTATIVES)):
            values = {
                selected[
                    min(fixed_point, other),
                    max(fixed_point, other),
                    orbit_index,
                ]
                for other in SQUARES
                if other != fixed_point
            }
            assert len(values) == 14

    for i, j in FIXED_PAIRS:
        degrees = Counter()
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            degrees.update(
                translate(
                    representative,
                    selected[i, j, orbit_index],
                )
            )
        assert degrees[0] == 8
        assert all(degrees[moving_point] == 7 for moving_point in POINTS[1:])


def read_competition_solution(path: Path) -> set[int]:
    status = None
    literals = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("s "):
            status = line[2:].strip()
        elif line.startswith("v "):
            literals.extend(map(int, line[2:].split()))
    if status != "SATISFIABLE":
        raise ValueError(f"solution status is {status!r}, not SATISFIABLE")
    return {literal for literal in literals if literal > 0}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", default="maplechrono")
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dimacs", type=Path)
    parser.add_argument("--verify-solution", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    clauses, variable, domains, stats = build_cnf(construct_golf17())
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
                    "scope": "vertex-degree relaxation",
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
                "scope": (
                    "phase lists + cross permutations + vertex degrees; "
                    "edge-position collision constraints omitted"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
