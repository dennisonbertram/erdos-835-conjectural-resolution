#!/usr/bin/env python3
"""Two-orbit LNS for the cyclic fixed-golf radius-five phase search.

A neighborhood chooses two of the forty moving-triple orbits and reoptimizes
their 210 phase cells jointly.  The remaining thirty-eight orbits are fixed.
Each selected orbit is constrained to remain a proper list edge-colouring of
K_15, so every candidate preserves all static zero-factor restrictions and
all shared-N constraints.

Unlike one-orbit LNS, the local objective represents the union of the two
selected triples in each golf-pair slice.  This permits compensating moves
that temporarily exchange which orbit covers a residual edge.  Coverage is
the primary objective; optionally, exact-slice vertex-degree L1 is a strict
secondary tiebreak.  Only global coverage 12,600 is a certificate, and that
case is passed through the canonical full semantic verifier.
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
from improve_radius5_golf_cyclic_orbit_lns import degree_l1
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
    MOVING_EDGES,
    P,
    REPRESENTATIVES,
    SQUARES,
    translate,
)


def optimize_two_orbits(
    state: State,
    domains,
    selected_orbits: tuple[int, int],
    *,
    seconds: float,
    workers: int,
    seed: int,
    degree_tiebreak: bool,
) -> tuple[str, State | None]:
    selected_set = set(selected_orbits)
    model = cp_model.CpModel()
    choose: dict[
        tuple[int, int, int, int], cp_model.IntVar
    ] = {}

    base_coverage: dict[
        tuple[int, int], Counter[tuple[int, int]]
    ] = {}
    base_degrees: dict[tuple[int, int], list[int]] = {}
    for fixed_pair in FIXED_PAIRS:
        counts: Counter[tuple[int, int]] = Counter()
        degrees = [0] * P
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            if orbit_index in selected_set:
                continue
            triple = translate(
                representative,
                state[fixed_pair + (orbit_index,)],
            )
            counts.update(combinations(triple, 2))
            for vertex in triple:
                degrees[vertex] += 1
        base_coverage[fixed_pair] = counts
        base_degrees[fixed_pair] = degrees

    for orbit_index in selected_orbits:
        for i, j in FIXED_PAIRS:
            literals = []
            for shift in sorted(domains[i, j, orbit_index]):
                literal = model.NewBoolVar(
                    f"x_{orbit_index}_{i}_{j}_{shift}"
                )
                choose[orbit_index, i, j, shift] = literal
                literals.append(literal)
            model.AddExactlyOne(literals)
            model.AddHint(
                choose[
                    orbit_index,
                    i,
                    j,
                    state[i, j, orbit_index],
                ],
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
                    choose[orbit_index, i, j, shift]
                    for i, j in incident
                    if (orbit_index, i, j, shift) in choose
                ]
                if len(literals) > 1:
                    model.AddAtMostOne(literals)

    covered_terms = []
    for i, j in FIXED_PAIRS:
        base = base_coverage[i, j]
        for edge in MOVING_EDGES:
            if base[edge]:
                continue
            literals = []
            for orbit_index in selected_orbits:
                representative = REPRESENTATIVES[orbit_index]
                for shift in domains[i, j, orbit_index]:
                    if edge in combinations(
                        translate(representative, shift),
                        2,
                    ):
                        literals.append(
                            choose[orbit_index, i, j, shift]
                        )
            if not literals:
                continue
            covered = model.NewBoolVar(
                f"covered_{i}_{j}_{edge[0]}_{edge[1]}"
            )
            model.AddMaxEquality(covered, literals)
            covered_terms.append(covered)

    degree_terms = []
    if degree_tiebreak:
        for i, j in FIXED_PAIRS:
            for vertex in range(P):
                memberships = [
                    choose[orbit_index, i, j, shift]
                    for orbit_index in selected_orbits
                    for shift in domains[i, j, orbit_index]
                    if vertex in translate(
                        REPRESENTATIVES[orbit_index],
                        shift,
                    )
                ]
                deviation = model.NewIntVar(
                    0,
                    P,
                    f"degree_dev_{i}_{j}_{vertex}",
                )
                target = 8 if vertex == 0 else 7
                model.AddAbsEquality(
                    deviation,
                    base_degrees[i, j][vertex]
                    + sum(memberships)
                    - target,
                )
                degree_terms.append(deviation)

    if degree_tiebreak:
        model.Maximize(
            10_000 * sum(covered_terms) - sum(degree_terms)
        )
    else:
        model.Maximize(sum(covered_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 50_000
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.StatusName(status), None

    candidate = dict(state)
    for orbit_index in selected_orbits:
        for i, j in FIXED_PAIRS:
            selected = [
                shift
                for shift in domains[i, j, orbit_index]
                if solver.Value(choose[orbit_index, i, j, shift])
            ]
            if len(selected) != 1:
                raise AssertionError(
                    "two-orbit solver did not select one phase"
                )
            candidate[i, j, orbit_index] = selected[0]
    return solver.StatusName(status), candidate


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
    parser.add_argument("--neighborhoods", type=int, default=40)
    parser.add_argument("--seconds-per-neighborhood", type=float, default=10.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--accept-equal", action="store_true")
    parser.add_argument("--degree-tiebreak", action="store_true")
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    domains = domains_for_seed(construct_golf17())
    state = load_state(args.source)
    audit_static(state, domains)
    scores = slice_scores(state)
    initial = sum(scores.values())
    current_degree_l1 = degree_l1(state)
    print(
        json.dumps(
            {
                "status": "START",
                "global_coverage": initial,
                "degree_l1": current_degree_l1,
                "exact_slices": sum(score == 120 for score in scores.values()),
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

    neighborhoods = list(combinations(range(len(REPRESENTATIVES)), 2))
    rng.shuffle(neighborhoods)
    neighborhoods = neighborhoods[: args.neighborhoods]
    accepted = 0
    for step, selected_orbits in enumerate(neighborhoods):
        old_total = sum(scores.values())
        old_degree_l1 = current_degree_l1
        status, candidate = optimize_two_orbits(
            state,
            domains,
            selected_orbits,
            seconds=args.seconds_per_neighborhood,
            workers=args.workers,
            seed=rng.randrange(1, 2**31),
            degree_tiebreak=args.degree_tiebreak,
        )
        if candidate is None:
            continue
        audit_static(candidate, domains)
        candidate_scores = slice_scores(candidate)
        new_total = sum(candidate_scores.values())
        new_degree_l1 = degree_l1(candidate)
        changed = any(
            candidate[key] != state[key]
            for key in candidate
            if key[2] in selected_orbits
        )
        accept = new_total > old_total or (
            new_total == old_total
            and changed
            and (
                new_degree_l1 < old_degree_l1
                or args.accept_equal
            )
        )
        if not accept:
            continue
        state = candidate
        scores = candidate_scores
        current_degree_l1 = new_degree_l1
        accepted += 1
        print(
            json.dumps(
                {
                    "status": status,
                    "step": step,
                    "orbits": list(selected_orbits),
                    "old": old_total,
                    "new": new_total,
                    "old_degree_l1": old_degree_l1,
                    "degree_l1": new_degree_l1,
                    "exact_slices": sum(
                        score == 120 for score in scores.values()
                    ),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        write_seed(args.output, state)
        if new_total == len(FIXED_PAIRS) * 120:
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

    sha = write_seed(args.output, state)
    print(
        json.dumps(
            {
                "status": "DONE",
                "accepted": accepted,
                "initial_coverage": initial,
                "global_coverage": sum(scores.values()),
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
