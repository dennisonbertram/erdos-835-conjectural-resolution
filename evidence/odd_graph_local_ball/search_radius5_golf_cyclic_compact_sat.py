#!/usr/bin/env python3
"""Compact SAT encoding of the cyclic fixed-golf radius-five ansatz.

This is an independent Boolean encoding of the eight-difference
AllDifferent reduction in ``search_radius5_golf_cyclic_compact.py``.
There is one primary literal only for an allowed phase value.  Exactly one
phase is chosen for each fixed-pair/triple-orbit cell.  Slice clauses forbid
two selected edge occurrences from landing at the same cyclic edge position,
and cross clauses forbid equal phases on incident edges of K_15.

Because every slice has exactly fifteen occurrences in each difference class
and its domains avoid the two forbidden positions, collision-freedom is
equivalent to exact residual-edge coverage.  SAT is expanded and checked on
the complete radius-five ball.  A bare UNSAT return is diagnostic only unless
accompanied by a portable proof log and independent proof checking.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Optional

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from convert_cyclic17_r3_to_radius5 import convert
from global_latin_audit import construct_golf17
from search_radius5_golf_cyclic_compact import (
    DIFFERENCES,
    FIXED_PAIRS,
    P,
    POINTS,
    REPRESENTATIVES,
    REPRESENTATIVE_EDGE_COORDINATES,
    SQUARES,
    allowed_shifts,
    zero_positions,
)


def build_cnf(
    golf,
    encoding: int = EncType.seqcounter,
    explicit_cover_clauses: bool = False,
):
    zeros = zero_positions(golf)
    domains: dict[tuple[int, int, int], tuple[int, ...]] = {}
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            domains[i, j, orbit_index] = tuple(
                allowed_shifts((i, j), orbit_index, zeros)
            )

    pool = IDPool()
    variable: dict[tuple[int, int, int, int], int] = {}
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in domains[i, j, orbit_index]:
                key = i, j, orbit_index, shift
                variable[key] = pool.id(key)
    primary_variables = pool.top
    assert primary_variables == sum(map(len, domains.values()))

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

    # For each fixed pair and difference, the 15 edge occurrences must land
    # at distinct positions.  Domains already remove both zero-factor
    # positions, so at-most-one is sufficient.
    slice_groups: dict[
        tuple[int, int, int, int], list[int]
    ] = defaultdict(list)
    for i, j in FIXED_PAIRS:
        for orbit_index, coordinates in enumerate(
            REPRESENTATIVE_EDGE_COORDINATES
        ):
            for shift in domains[i, j, orbit_index]:
                literal = variable[i, j, orbit_index, shift]
                for difference, offset in coordinates:
                    position = (offset + shift) % P
                    slice_groups[i, j, difference, position].append(literal)

    slice_at_most_one = 0
    slice_at_least_one = 0
    for i, j in FIXED_PAIRS:
        forbidden_by_difference = {
            difference: {zeros[i, difference], zeros[j, difference]}
            for difference in DIFFERENCES
        }
        for difference in DIFFERENCES:
            for position in POINTS:
                literals = slice_groups.get(
                    (i, j, difference, position), []
                )
                if position in forbidden_by_difference[difference]:
                    assert not literals
                    continue
                assert literals
                if explicit_cover_clauses:
                    clauses.append(literals)
                    slice_at_least_one += 1
                if len(literals) > 1:
                    clauses.extend(
                        CardEnc.atmost(
                            lits=literals,
                            bound=1,
                            vpool=pool,
                            encoding=encoding,
                        ).clauses
                    )
                slice_at_most_one += 1
    assert slice_at_most_one == len(FIXED_PAIRS) * len(DIFFERENCES) * 15

    cross_groups: dict[tuple[int, int, int], list[int]] = defaultdict(list)
    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            for shift in domains[i, j, orbit_index]:
                literal = variable[i, j, orbit_index, shift]
                cross_groups[i, orbit_index, shift].append(literal)
                cross_groups[j, orbit_index, shift].append(literal)

    cross_at_most_one = 0
    cross_at_least_one = 0
    for fixed_point in SQUARES:
        for orbit_index in range(len(REPRESENTATIVES)):
            allowed_phases = 0
            for shift in POINTS:
                literals = cross_groups.get(
                    (fixed_point, orbit_index, shift), []
                )
                if literals:
                    allowed_phases += 1
                    if explicit_cover_clauses:
                        clauses.append(literals)
                        cross_at_least_one += 1
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
            assert allowed_phases == 14
    assert cross_at_most_one == len(SQUARES) * len(REPRESENTATIVES) * P

    stats = {
        "primary_variables": primary_variables,
        "total_variables": pool.top,
        "clauses": len(clauses),
        "phase_exactly_one": phase_exactly_one,
        "slice_at_most_one": slice_at_most_one,
        "slice_at_least_one": slice_at_least_one,
        "cross_at_most_one": cross_at_most_one,
        "cross_at_least_one": cross_at_least_one,
        "explicit_cover_clauses": explicit_cover_clauses,
    }
    assert stats["primary_variables"] == 47880
    assert stats["phase_exactly_one"] == 4200
    assert stats["slice_at_most_one"] == 12600
    assert stats["cross_at_most_one"] == 10200
    assert stats["slice_at_least_one"] == (
        12600 if explicit_cover_clauses else 0
    )
    assert stats["cross_at_least_one"] == (
        8400 if explicit_cover_clauses else 0
    )
    return clauses, variable, domains, stats


def preferred_literals(
    source: Path,
    variable: dict[tuple[int, int, int, int], int],
    domains: dict[tuple[int, int, int], tuple[int, ...]],
) -> list[int]:
    payload = json.loads(source.read_text(encoding="utf-8"))
    if set(payload) != {f"{i},{j}" for i, j in FIXED_PAIRS}:
        raise ValueError("phase hint must contain all 105 fixed pairs")
    answer = []
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        if (
            not isinstance(phases, list)
            or len(phases) != len(REPRESENTATIVES)
        ):
            raise ValueError(f"wrong phase hint list for {i},{j}")
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


def phases_from_model(
    positive: set[int],
    variable: dict[tuple[int, int, int, int], int],
    domains: dict[tuple[int, int, int], tuple[int, ...]],
) -> dict[str, list[int]]:
    answer: dict[str, list[int]] = {}
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


def emit_verified_solution(
    positive: set[int],
    variable,
    domains,
    stats,
    phase_output: Optional[Path],
    certificate: Optional[Path],
    **extra,
) -> None:
    phases = phases_from_model(positive, variable, domains)
    encoded = (
        json.dumps(phases, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if phase_output is not None:
        phase_output.write_bytes(encoded)
    # ``convert`` reconstructs all N/P values and checks the complete
    # 73,457-vertex radius-five ball before returning its payload.
    payload = convert(phases)
    if certificate is not None:
        certificate.write_text(
            json.dumps(payload, sort_keys=True, separators=(",", ":"))
            + "\n",
            encoding="utf-8",
        )
    print(
        json.dumps(
            {
                "status": "FEASIBLE",
                "counts": stats,
                "phase_sha256": hashlib.sha256(encoded).hexdigest(),
                "certificate_sha256_without_hash": payload[
                    "sha256_without_hash"
                ],
                "semantic_ball_verified": True,
                **extra,
            },
            indent=2,
            sort_keys=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", default="maplechrono")
    parser.add_argument(
        "--cardinality-encoding",
        choices=("sequential", "pairwise"),
        default="sequential",
    )
    parser.add_argument("--hint", type=Path)
    parser.add_argument(
        "--explicit-cover-clauses",
        action="store_true",
        help=(
            "add the logically redundant at-least-one clause for every "
            "residual edge position and every allowed cross phase"
        ),
    )
    parser.add_argument("--dimacs", type=Path)
    parser.add_argument("--verify-solution", type=Path)
    parser.add_argument("--phase-output", type=Path)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    encoding = (
        EncType.seqcounter
        if args.cardinality_encoding == "sequential"
        else EncType.pairwise
    )
    clauses, variable, domains, stats = build_cnf(
        construct_golf17(),
        encoding,
        explicit_cover_clauses=args.explicit_cover_clauses,
    )
    stats["cardinality_encoding"] = args.cardinality_encoding
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
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if args.verify_solution is not None:
        emit_verified_solution(
            read_competition_solution(args.verify_solution),
            variable,
            domains,
            stats,
            args.phase_output,
            args.certificate,
            source=str(args.verify_solution),
        )
        return

    phase_hint_applied = False
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        if preferred:
            try:
                solver.set_phases(preferred)
                phase_hint_applied = True
            except NotImplementedError:
                # Kissat's PySAT wrapper does not expose phase preferences.
                # The hint is optional and never changes the formula.
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

    emit_verified_solution(
        positive,
        variable,
        domains,
        stats,
        args.phase_output,
        args.certificate,
        phase_hint_applied=phase_hint_applied,
    )


if __name__ == "__main__":
    main()
