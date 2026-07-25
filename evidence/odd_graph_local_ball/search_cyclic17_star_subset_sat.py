#!/usr/bin/env python3
"""Proof-capable SAT model for a subset of one cyclic Wallis star.

For selected outer rows at centre 0, this encodes:

* one allowed phase in each row/orbit cell;
* exact coverage of every residual moving edge in each selected row; and
* pairwise-distinct phases among the selected rows in every orbit.

SAT is independently verified and proves compatibility only for the selected
rows.  Solver UNSAT is not treated as a theorem without an externally checked
proof.  Even a full fourteen-row star would remain only a necessary local
piece of the fixed-Wallis C17 ansatz, not a solution of Erdos--Rosenfeld 835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
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
from improve_radius5_golf_cyclic_slice_lns import domains_for_seed
from search_radius5_golf_cyclic_compact import (
    MOVING_EDGES,
    POINTS,
    REPRESENTATIVES,
    translate,
)


def parse_outers(text: str) -> tuple[int, ...]:
    try:
        values = tuple(sorted(set(map(int, text.split(",")))))
    except ValueError as error:
        raise argparse.ArgumentTypeError("outers must be comma-separated") from error
    if not values or any(not 1 <= value <= 14 for value in values):
        raise argparse.ArgumentTypeError("outers must lie in 1,...,14")
    return values


def build_cnf(outers):
    golf = construct_golf17()
    domains = domains_for_seed(golf)
    variable = {}
    for outer in outers:
        for orbit in range(len(REPRESENTATIVES)):
            for shift in domains[0, outer, orbit]:
                variable[outer, orbit, shift] = len(variable) + 1
    pool = IDPool(start_from=len(variable) + 1)
    clauses = []

    def exactly_one(literals):
        clauses.extend(
            CardEnc.equals(
                lits=list(literals),
                bound=1,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )

    cell_rows = 0
    for outer in outers:
        for orbit in range(len(REPRESENTATIVES)):
            exactly_one(
                variable[outer, orbit, shift]
                for shift in domains[0, outer, orbit]
            )
            cell_rows += 1

    translated = {
        (orbit, shift): translate(representative, shift)
        for orbit, representative in enumerate(REPRESENTATIVES)
        for shift in POINTS
    }
    residual_rows = 0
    for outer in outers:
        leave = {
            edge
            for edge in MOVING_EDGES
            if golf[0][edge[0]][edge[1]] == 0
            or golf[outer][edge[0]][edge[1]] == 0
        }
        assert len(leave) == 16
        for edge in MOVING_EDGES:
            if edge in leave:
                continue
            exactly_one(
                variable[outer, orbit, shift]
                for orbit in range(len(REPRESENTATIVES))
                for shift in domains[0, outer, orbit]
                if set(edge) <= set(translated[orbit, shift])
            )
            residual_rows += 1

    cross_binary_clauses = 0
    for orbit in range(len(REPRESENTATIVES)):
        for shift in POINTS:
            literals = [
                variable[outer, orbit, shift]
                for outer in outers
                if (outer, orbit, shift) in variable
            ]
            for left, right in combinations(literals, 2):
                clauses.append([-left, -right])
                cross_binary_clauses += 1

    stats = {
        "centre": 0,
        "outers": list(outers),
        "primary_variables": len(variable),
        "total_variables": pool.top,
        "clauses": len(clauses),
        "cell_exactly_one": cell_rows,
        "residual_edge_exactly_one": residual_rows,
        "cross_binary_clauses": cross_binary_clauses,
    }
    assert cell_rows == len(outers) * 40
    assert residual_rows == len(outers) * 120
    return clauses, variable, domains, stats


def phases_from_positive(positive, variable, domains, outers):
    answer = {}
    for outer in outers:
        phases = []
        for orbit in range(len(REPRESENTATIVES)):
            selected = [
                shift
                for shift in domains[0, outer, orbit]
                if variable[outer, orbit, shift] in positive
            ]
            if len(selected) != 1:
                raise ValueError("model selected != 1 phase")
            phases.append((-selected[0]) % 17)
        answer[str(outer)] = phases
    return answer


def verify_phases(phases, outers):
    golf = construct_golf17()
    for outer in outers:
        row = phases[str(outer)]
        selected_edges = []
        for orbit, portable_phase in enumerate(row):
            triple = translate(
                REPRESENTATIVES[orbit],
                (-portable_phase) % 17,
            )
            selected_edges.extend(combinations(triple, 2))
        if len(selected_edges) != 120 or len(set(selected_edges)) != 120:
            raise ValueError("row is not an exact residual decomposition")
        leave = set(MOVING_EDGES) - set(selected_edges)
        expected = {
            edge
            for edge in MOVING_EDGES
            if golf[0][edge[0]][edge[1]] == 0
            or golf[outer][edge[0]][edge[1]] == 0
        }
        if leave != expected:
            raise ValueError("row has wrong prescribed leave")
    for left, right in combinations(outers, 2):
        if any(
            first == second
            for first, second in zip(phases[str(left)], phases[str(right)])
        ):
            raise ValueError("selected rows have a phase collision")


def read_solution(path: Path) -> set[int]:
    status = None
    literals = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("s "):
            status = line[2:].strip()
        elif line.startswith("v "):
            literals.extend(map(int, line[2:].split()))
    if status != "SATISFIABLE":
        raise ValueError(f"solution status is {status!r}")
    return {literal for literal in literals if literal > 0}


def read_phase_hint(path: Path, variable, outers) -> list[int]:
    selected = {}
    for line_number, raw in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not raw.strip():
            continue
        fields = raw.split()
        if len(fields) != 3:
            raise ValueError(f"bad hint line {line_number}")
        outer, orbit, shift = map(int, fields)
        if outer not in outers or not 0 <= orbit < len(REPRESENTATIVES):
            raise ValueError(f"bad hint coordinate on line {line_number}")
        key = (outer, orbit, shift)
        if key not in variable:
            raise ValueError(f"forbidden hinted phase on line {line_number}")
        cell = (outer, orbit)
        if cell in selected:
            raise ValueError(f"duplicate hinted cell on line {line_number}")
        selected[cell] = variable[key]
    expected = {
        (outer, orbit)
        for outer in outers
        for orbit in range(len(REPRESENTATIVES))
    }
    if set(selected) != expected:
        raise ValueError("hint does not specify every selected cell")
    positives = set(selected.values())
    return [
        literal if literal in positives else -literal
        for literal in variable.values()
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outers", type=parse_outers, required=True)
    parser.add_argument("--solver", default="maplechrono")
    parser.add_argument("--dimacs", type=Path)
    parser.add_argument("--verify-solution", type=Path)
    parser.add_argument(
        "--phase-hint",
        type=Path,
        help="complete selected-row hint as 'outer orbit shift' lines",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    clauses, variable, domains, stats = build_cnf(args.outers)
    if args.dimacs is not None:
        CNF(from_clauses=clauses).to_file(args.dimacs)
        stats["dimacs_sha256"] = hashlib.sha256(
            args.dimacs.read_bytes()
        ).hexdigest()
    if args.audit_only:
        print(json.dumps({"status": "PASS", "counts": stats}, indent=2))
        return

    if args.verify_solution is not None:
        positive = read_solution(args.verify_solution)
        phases = phases_from_positive(
            positive, variable, domains, args.outers
        )
        verify_phases(phases, args.outers)
        encoded = (
            json.dumps(phases, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        if args.output is not None:
            args.output.write_bytes(encoded)
        print(
            json.dumps(
                {
                    "status": "SUBSET_WITNESS",
                    "counts": stats,
                    "phase_sha256": hashlib.sha256(encoded).hexdigest(),
                    "semantic_subset_verifier": "PASS",
                    "scope": "selected centre-0 outer rows only",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        if args.phase_hint is not None:
            solver.set_phases(
                read_phase_hint(
                    args.phase_hint,
                    variable,
                    args.outers,
                )
            )
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
        solver_stats = solver.accum_stats()
    if not satisfiable:
        print(
            json.dumps(
                {
                    "status": "INFEASIBLE",
                    "portable_proof": False,
                    "counts": stats,
                    "solver_stats": solver_stats,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    positive = {literal for literal in model if literal > 0}
    phases = phases_from_positive(
        positive, variable, domains, args.outers
    )
    verify_phases(phases, args.outers)
    encoded = (
        json.dumps(phases, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if args.output is not None:
        args.output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "status": "SUBSET_WITNESS",
                "counts": stats,
                "solver_stats": solver_stats,
                "phase_sha256": hashlib.sha256(encoded).hexdigest(),
                "semantic_subset_verifier": "PASS",
                "scope": "selected centre-0 outer rows only",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
