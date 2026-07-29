#!/usr/bin/env python3
"""Degree-primary two/three-orbit LNS for the cyclic Wallis phase model.

Each neighborhood reoptimizes two or optionally three complete moving-triple
orbits while preserving their proper list edge-colourings of K_15.  The
objective is exactly the total L1 deviation from the necessary slice
degrees: 8 at moving point 0 and 7 at every other moving point.

This searches only the necessary vertex-degree relaxation.  It omits all
residual-edge collision constraints and cannot certify the full radius-five
quotient or Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from improve_radius5_golf_cyclic_orbit_lns import degree_l1
from improve_radius5_golf_cyclic_slice_lns import (
    State,
    audit_static,
    domains_for_seed,
    dump_phases,
    load_state,
)
from search_cyclic17_vertex_degree_sat import verify_relaxation
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    REPRESENTATIVES,
    SQUARES,
    translate,
)


def optimize_two_orbits_for_degrees(
    state: State,
    domains,
    selected_orbits: tuple[int, ...],
    *,
    seconds: float,
    workers: int,
    seed: int,
) -> tuple[str, State | None]:
    selected_set = set(selected_orbits)
    model = cp_model.CpModel()
    choose = {}
    base_degrees = {}

    for fixed_pair in FIXED_PAIRS:
        degrees = [0] * P
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            if orbit_index in selected_set:
                continue
            triple = translate(
                representative,
                state[fixed_pair + (orbit_index,)],
            )
            for vertex in triple:
                degrees[vertex] += 1
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

    deviations = []
    for i, j in FIXED_PAIRS:
        for vertex in range(P):
            memberships = [
                choose[orbit_index, i, j, shift]
                for orbit_index in selected_orbits
                for shift in domains[i, j, orbit_index]
                if vertex in translate(
                    REPRESENTATIVES[orbit_index], shift
                )
            ]
            deviation = model.NewIntVar(
                0, P, f"dev_{i}_{j}_{vertex}"
            )
            model.AddAbsEquality(
                deviation,
                base_degrees[i, j][vertex]
                + sum(memberships)
                - (8 if vertex == 0 else 7),
            )
            deviations.append(deviation)

    model.Minimize(sum(deviations))
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
                shift for shift in domains[i, j, orbit_index]
                if solver.Value(
                    choose[orbit_index, i, j, shift]
                )
            ]
            assert len(selected) == 1
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
    parser.add_argument(
        "--orbit-count",
        type=int,
        choices=(2, 3),
        default=2,
        help="number of complete triple orbits in each neighborhood",
    )
    parser.add_argument("--neighborhoods", type=int, default=80)
    parser.add_argument(
        "--seconds-per-neighborhood", type=float, default=5.0
    )
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--accept-equal", action="store_true")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    golf = construct_golf17()
    domains = domains_for_seed(golf)
    state = load_state(args.source)
    audit_static(state, domains)
    initial = degree_l1(state)
    current = initial
    print(
        json.dumps(
            {"status": "START", "degree_l1": current},
            sort_keys=True,
        ),
        flush=True,
    )

    neighborhoods = list(
        combinations(
            range(len(REPRESENTATIVES)), args.orbit_count
        )
    )
    rng.shuffle(neighborhoods)
    neighborhoods = neighborhoods[: args.neighborhoods]
    accepted = 0
    for step, selected_orbits in enumerate(neighborhoods):
        status, candidate = optimize_two_orbits_for_degrees(
            state,
            domains,
            selected_orbits,
            seconds=args.seconds_per_neighborhood,
            workers=args.workers,
            seed=rng.randrange(1, 2**31),
        )
        if candidate is None:
            continue
        audit_static(candidate, domains)
        new = degree_l1(candidate)
        changed = any(
            candidate[key] != state[key]
            for key in candidate
            if key[2] in selected_orbits
        )
        if not changed:
            continue
        if new > current or (
            new == current and not args.accept_equal
        ):
            continue
        old = current
        state = candidate
        current = new
        accepted += 1
        write_seed(args.output, state)
        print(
            json.dumps(
                {
                    "status": status,
                    "step": step,
                    "orbits": list(selected_orbits),
                    "old_degree_l1": old,
                    "degree_l1": current,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if current == 0:
            phases = dump_phases(state)
            verify_relaxation(
                phases,
                {
                    key: tuple(value)
                    for key, value in domains.items()
                },
            )
            sha = write_seed(args.output, state)
            print(
                json.dumps(
                    {
                        "status": "FEASIBLE_RELAXATION",
                        "phase_sha256": sha,
                        "semantic_relaxation_verifier": "PASS",
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
                "initial_degree_l1": initial,
                "degree_l1": current,
                "phase_sha256": sha,
                "semantic_relaxation_verifier": "NOT_RUN",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
