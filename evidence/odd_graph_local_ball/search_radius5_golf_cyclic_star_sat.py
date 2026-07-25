#!/usr/bin/env python3
"""Direct SAT encoding of one exact cyclic Wallis 14-row star.

This is the Boolean counterpart of ``search_radius5_golf_cyclic_star.py``.
It uses one primary literal for every allowed (pair row, triple orbit, shift)
choice and sequential-counter exactly-one constraints for:

* one shift in each of the 14*40 cells;
* one selected triple over each of the 14*120 residual moving edges; and
* one incident pair row at each of the 40*14 allowed centre phases.

The scope warning is the same as for the integer model: a star witness is
only a necessary local piece.  Solver ``INFEASIBLE`` is not a portable proof
unless a proof log is emitted and independently checked.
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
from improve_radius5_golf_cyclic_slice_lns import (
    audit_static,
    domains_for_seed,
    dump_phases,
    load_state,
    slice_scores,
)
from search_radius5_golf_cyclic_alternating_projection import cross_distinct
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    MOVING_EDGES,
    P,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    translate,
    zero_positions,
)


def incident_pair(first: int, second: int) -> tuple[int, int]:
    return min(first, second), max(first, second)


def build_cnf(centre: int):
    golf = construct_golf17()
    zeros = zero_positions(golf)
    domains = domains_for_seed(golf)
    pairs = [
        incident_pair(centre, other)
        for other in SQUARES
        if other != centre
    ]
    primary_keys = [
        (fixed_pair, orbit_index, shift)
        for fixed_pair in pairs
        for orbit_index in range(len(REPRESENTATIVES))
        for shift in sorted(domains[fixed_pair + (orbit_index,)])
    ]
    variable = {
        key: index
        for index, key in enumerate(primary_keys, start=1)
    }
    pool = IDPool(start_from=len(variable) + 1)
    clauses = []

    def exactly_one(literals):
        if not literals:
            raise AssertionError("empty exactly-one")
        clauses.extend(
            CardEnc.equals(
                lits=list(literals),
                bound=1,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )

    cell_constraints = 0
    for fixed_pair in pairs:
        for orbit_index in range(len(REPRESENTATIVES)):
            exactly_one(
                variable[fixed_pair, orbit_index, shift]
                for shift in domains[fixed_pair + (orbit_index,)]
            )
            cell_constraints += 1

    translated = {
        (orbit_index, shift): translate(representative, shift)
        for orbit_index, representative in enumerate(REPRESENTATIVES)
        for shift in POINTS
    }
    residual_constraints = 0
    for fixed_pair in pairs:
        i, j = fixed_pair
        leave = {
            edge
            for edge in MOVING_EDGES
            if golf[i][edge[0]][edge[1]] == 0
            or golf[j][edge[0]][edge[1]] == 0
        }
        if len(leave) != 16:
            raise AssertionError("wrong two-factor leave")
        for edge in MOVING_EDGES:
            if edge in leave:
                continue
            literals = []
            for orbit_index in range(len(REPRESENTATIVES)):
                for shift in domains[fixed_pair + (orbit_index,)]:
                    if set(edge) <= set(translated[orbit_index, shift]):
                        literals.append(
                            variable[fixed_pair, orbit_index, shift]
                        )
            exactly_one(literals)
            residual_constraints += 1

    cross_constraints = 0
    for orbit_index in range(len(REPRESENTATIVES)):
        forbidden = {
            shift
            for shift in POINTS
            if any(
                golf[centre][x][y] == 0
                for x, y in combinations(
                    translated[orbit_index, shift],
                    2,
                )
            )
        }
        if len(forbidden) != 3:
            raise AssertionError("wrong centre forbidden set")
        for shift in POINTS:
            if shift in forbidden:
                continue
            literals = [
                variable[fixed_pair, orbit_index, shift]
                for fixed_pair in pairs
                if (fixed_pair, orbit_index, shift) in variable
            ]
            exactly_one(literals)
            cross_constraints += 1

    stats = {
        "centre": centre,
        "primary_variables": len(variable),
        "total_variables": pool.top,
        "clauses": len(clauses),
        "cell_exactly_one": cell_constraints,
        "residual_edge_exactly_one": residual_constraints,
        "cross_phase_exactly_one": cross_constraints,
    }
    if (
        stats["cell_exactly_one"] != 560
        or stats["residual_edge_exactly_one"] != 1680
        or stats["cross_phase_exactly_one"] != 560
    ):
        raise AssertionError("wrong star SAT counts")
    return clauses, variable, domains, pairs, stats


def write_state(path: Path, state) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--centre", type=int, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--phase-hint",
        type=Path,
        help="optional separate cross-compatible polarity hint",
    )
    parser.add_argument("--solver", default="maplechrono")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--dimacs",
        type=Path,
        help="write the deterministic star CNF for an external solver",
    )
    parser.add_argument(
        "--polarity-hinted-dimacs",
        type=Path,
        help=(
            "write an equisatisfiable CNF with non-hint primary variables "
            "complemented, so the all-true phase equals the supplied hint"
        ),
    )
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    if args.centre not in SQUARES:
        parser.error("--centre must lie in 0,...,14")
    clauses, variable, domains, pairs, stats = build_cnf(args.centre)
    source = load_state(args.source)
    if set(slice_scores(source).values()) != {120}:
        raise ValueError("source must contain 105 exact rows")
    hint_state = (
        load_state(args.phase_hint)
        if args.phase_hint is not None
        else source
    )
    if args.phase_hint is not None:
        audit_static(hint_state, domains)
    if args.dimacs is not None:
        CNF(from_clauses=clauses).to_file(args.dimacs)
        encoded = args.dimacs.read_bytes()
        stats["dimacs_sha256"] = hashlib.sha256(encoded).hexdigest()
    if args.polarity_hinted_dimacs is not None:
        complemented = {
            literal
            for (fixed_pair, orbit_index, shift), literal
            in variable.items()
            if hint_state[fixed_pair + (orbit_index,)] != shift
        }
        hinted_clauses = [
            [
                -literal
                if abs(literal) in complemented
                else literal
                for literal in clause
            ]
            for clause in clauses
        ]
        CNF(from_clauses=hinted_clauses).to_file(
            args.polarity_hinted_dimacs
        )
        encoded = args.polarity_hinted_dimacs.read_bytes()
        stats["polarity_hinted_dimacs_sha256"] = hashlib.sha256(
            encoded
        ).hexdigest()
        stats["complemented_primary_variables"] = len(complemented)
    if args.audit_only:
        print(json.dumps({"status": "PASS", "counts": stats}, sort_keys=True))
        return

    preferred = []
    for (fixed_pair, orbit_index, shift), literal in variable.items():
        preferred.append(
            literal
            if hint_state[fixed_pair + (orbit_index,)] == shift
            else -literal
        )
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        try:
            solver.set_phases(preferred)
        except NotImplementedError:
            pass
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
        accumulator = solver.accum_stats()
    report: dict[str, object] = {
        "status": "SAT" if satisfiable else "INFEASIBLE",
        "counts": stats,
        "solver": args.solver,
        "solver_stats": accumulator,
    }
    if satisfiable:
        positive = {literal for literal in model if literal > 0}
        state = dict(source)
        for fixed_pair in pairs:
            for orbit_index in range(len(REPRESENTATIVES)):
                selected = [
                    shift
                    for shift in domains[fixed_pair + (orbit_index,)]
                    if variable[fixed_pair, orbit_index, shift] in positive
                ]
                if len(selected) != 1:
                    raise AssertionError("SAT star selected != 1 phase")
                state[fixed_pair + (orbit_index,)] = selected[0]
        scores = slice_scores(state)
        if any(scores[fixed_pair] != 120 for fixed_pair in pairs):
            raise AssertionError("SAT star has a nonexact pair row")
        for orbit_index in range(len(REPRESENTATIVES)):
            if len(
                {
                    state[fixed_pair + (orbit_index,)]
                    for fixed_pair in pairs
                }
            ) != 14:
                raise AssertionError("SAT star has a cross collision")
        report["verified_exact_rows"] = 14
        report["verified_cross_groups"] = 40
        report["global_cross_distinct"] = cross_distinct(state)
        report["global_cross_target"] = 8400
        if args.output is not None:
            report["phase_sha256"] = write_state(args.output, state)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
