#!/usr/bin/env python3
"""Cross-compatible full-orbit LNS for the cyclic radius-five search.

For one of the forty moving-triple orbits, this move reoptimizes all 105
phases at once as a maximum-weight proper list edge-colouring of K_15.
All other thirty-nine orbits are fixed.  The weight of assigning a phase to
one golf pair is the number of its three moving edges not already covered by
the fixed orbits of that pair.  The local objective is therefore exactly the
resulting global distinct-edge coverage, up to an additive constant.

This strictly contains every two-colour Kempe move in that orbit and can jump
between edge-colourings that Kempe switching cannot connect monotonically.
Every accepted state still satisfies all zero-factor phase lists and all 600
shared-N constraints.  Only the score 12,600 is a radius-five witness; at that
score the complete canonical semantic verifier is run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
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

from convert_cyclic17_r3_to_radius5 import convert
from global_latin_audit import construct_golf17
from improve_radius5_golf_cyclic_slice_lns import (
    State,
    audit_static,
    domains_for_seed,
    dump_phases,
    load_state,
    slice_scores,
)
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    REPRESENTATIVES,
    SQUARES,
    translate,
)


def coverage_without_orbit(
    state: State,
    fixed_pair: tuple[int, int],
    omitted_orbit: int,
) -> Counter[tuple[int, int]]:
    counts: Counter[tuple[int, int]] = Counter()
    for orbit_index, representative in enumerate(REPRESENTATIVES):
        if orbit_index == omitted_orbit:
            continue
        triple = translate(
            representative,
            state[fixed_pair + (orbit_index,)],
        )
        counts.update(combinations(triple, 2))
    return counts


def degree_l1(state: State) -> int:
    answer = 0
    for fixed_pair in FIXED_PAIRS:
        degrees = [0] * P
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            triple = translate(
                representative,
                state[fixed_pair + (orbit_index,)],
            )
            for vertex in triple:
                degrees[vertex] += 1
        answer += sum(
            abs(degrees[vertex] - (8 if vertex == 0 else 7))
            for vertex in range(P)
        )
    return answer


def optimize_orbit(
    state: State,
    domains,
    orbit_index: int,
    *,
    seconds: float,
    workers: int,
    seed: int,
    degree_tiebreak: bool,
) -> tuple[
    str,
    int,
    int,
    dict[tuple[int, int], int] | None,
]:
    model = cp_model.CpModel()
    choose: dict[tuple[int, int, int], cp_model.IntVar] = {}
    base = {
        fixed_pair: coverage_without_orbit(
            state,
            fixed_pair,
            orbit_index,
        )
        for fixed_pair in FIXED_PAIRS
    }
    constant = sum(len(counts) for counts in base.values())
    objective_terms = []
    base_degrees = {}
    for fixed_pair in FIXED_PAIRS:
        degrees = [0] * P
        for other_orbit, representative in enumerate(REPRESENTATIVES):
            if other_orbit == orbit_index:
                continue
            triple = translate(
                representative,
                state[fixed_pair + (other_orbit,)],
            )
            for vertex in triple:
                degrees[vertex] += 1
        base_degrees[fixed_pair] = degrees

    for i, j in FIXED_PAIRS:
        literals = []
        for shift in sorted(domains[i, j, orbit_index]):
            literal = model.NewBoolVar(f"x_{i}_{j}_{shift}")
            choose[i, j, shift] = literal
            literals.append(literal)
            triple = translate(REPRESENTATIVES[orbit_index], shift)
            gain = sum(
                base[i, j][edge] == 0
                for edge in combinations(triple, 2)
            )
            final_degree_l1 = sum(
                abs(
                    base_degrees[i, j][vertex]
                    + int(vertex in triple)
                    - (8 if vertex == 0 else 7)
                )
                for vertex in range(P)
            )
            coefficient = (
                10_000 * gain - final_degree_l1
                if degree_tiebreak
                else gain
            )
            if coefficient:
                objective_terms.append(coefficient * literal)
        model.AddExactlyOne(literals)
        model.AddHint(
            choose[i, j, state[i, j, orbit_index]],
            1,
        )

    for fixed_point in SQUARES:
        incident = [
            (min(fixed_point, other), max(fixed_point, other))
            for other in SQUARES
            if other != fixed_point
        ]
        for shift in range(P):
            literals = [
                choose[i, j, shift]
                for i, j in incident
                if (i, j, shift) in choose
            ]
            if len(literals) > 1:
                model.AddAtMostOne(literals)

    model.Maximize(sum(objective_terms))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 50_000
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.StatusName(status), -1, -1, None
    assignment = {}
    for i, j in FIXED_PAIRS:
        selected = [
            shift
            for shift in domains[i, j, orbit_index]
            if solver.Value(choose[i, j, shift])
        ]
        if len(selected) != 1:
            raise AssertionError("orbit solver did not select one phase")
        assignment[i, j] = selected[0]
    predicted_gain = 0
    predicted_degree_l1 = 0
    for i, j in FIXED_PAIRS:
        triple = translate(
            REPRESENTATIVES[orbit_index],
            assignment[i, j],
        )
        predicted_gain += sum(
            base[i, j][edge] == 0
            for edge in combinations(triple, 2)
        )
        predicted_degree_l1 += sum(
            abs(
                base_degrees[i, j][vertex]
                + int(vertex in triple)
                - (8 if vertex == 0 else 7)
            )
            for vertex in range(P)
        )
    return (
        solver.StatusName(status),
        constant + predicted_gain,
        predicted_degree_l1,
        assignment,
    )


def write_seed(path: Path, state: State) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sweeps", type=int, default=3)
    parser.add_argument("--seconds-per-orbit", type=float, default=5.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--accept-equal", action="store_true")
    parser.add_argument(
        "--degree-tiebreak",
        action="store_true",
        help=(
            "lexicographically prefer lower forced vertex-degree L1 "
            "after maximizing coverage"
        ),
    )
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    golf = construct_golf17()
    domains = domains_for_seed(golf)
    state = load_state(args.source)
    audit_static(state, domains)
    scores = slice_scores(state)
    initial = sum(scores.values())
    initial_degree_l1 = degree_l1(state)
    current_degree_l1 = initial_degree_l1
    print(
        json.dumps(
            {
                "status": "START",
                "global_coverage": initial,
                "exact_slices": sum(score == 120 for score in scores.values()),
                "degree_l1": current_degree_l1,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    if args.audit_only:
        sha = write_seed(args.output, state)
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "phase_sha256": sha,
                    "scope": "static lists and shared-N constraints only",
                },
                sort_keys=True,
            )
        )
        return

    for sweep in range(args.sweeps):
        order = list(range(len(REPRESENTATIVES)))
        rng.shuffle(order)
        accepted = 0
        for step, orbit_index in enumerate(order):
            old_total = sum(scores.values())
            old_degree_l1 = current_degree_l1
            (
                status,
                predicted_total,
                predicted_degree_l1,
                assignment,
            ) = optimize_orbit(
                state,
                domains,
                orbit_index,
                seconds=args.seconds_per_orbit,
                workers=args.workers,
                seed=rng.randrange(1, 2**31),
                degree_tiebreak=args.degree_tiebreak,
            )
            if assignment is None:
                continue
            changed = any(
                assignment[i, j] != state[i, j, orbit_index]
                for i, j in FIXED_PAIRS
            )
            accept = predicted_total > old_total or (
                predicted_total == old_total
                and changed
                and (
                    predicted_degree_l1 < old_degree_l1
                    or args.accept_equal
                )
            )
            if not accept:
                continue
            for (i, j), shift in assignment.items():
                state[i, j, orbit_index] = shift
            audit_static(state, domains)
            scores = slice_scores(state)
            actual_total = sum(scores.values())
            if actual_total != predicted_total:
                raise AssertionError(
                    "orbit objective disagrees with global coverage"
                )
            current_degree_l1 = degree_l1(state)
            if current_degree_l1 != predicted_degree_l1:
                raise AssertionError(
                    "orbit objective disagrees with vertex-degree L1"
                )
            accepted += 1
            print(
                json.dumps(
                    {
                        "status": status,
                        "sweep": sweep,
                        "step": step,
                        "orbit": orbit_index,
                        "old": old_total,
                        "new": actual_total,
                        "old_degree_l1": old_degree_l1,
                        "degree_l1": current_degree_l1,
                        "exact_slices": sum(
                            score == 120 for score in scores.values()
                        ),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            write_seed(args.output, state)
            if actual_total == len(FIXED_PAIRS) * 120:
                phases = dump_phases(state)
                payload = convert(phases)
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
                print(
                    json.dumps(
                        {
                            "status": "SAT",
                            "semantic_verifier": "PASS",
                            "certificate_sha256_without_hash": payload[
                                "sha256_without_hash"
                            ],
                        },
                        sort_keys=True,
                    )
                )
                return
        print(
            json.dumps(
                {
                    "status": "SWEEP",
                    "sweep": sweep,
                    "accepted": accepted,
                    "global_coverage": sum(scores.values()),
                    "degree_l1": current_degree_l1,
                    "exact_slices": sum(
                        score == 120 for score in scores.values()
                    ),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if accepted == 0 and not args.accept_equal:
            break

    sha = write_seed(args.output, state)
    print(
        json.dumps(
            {
                "status": "DONE",
                "initial_coverage": initial,
                "global_coverage": sum(scores.values()),
                "initial_degree_l1": initial_degree_l1,
                "degree_l1": current_degree_l1,
                "exact_slices": sum(
                    score == 120 for score in scores.values()
                ),
                "phase_sha256": sha,
                "semantic_verifier": "NOT_RUN",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
