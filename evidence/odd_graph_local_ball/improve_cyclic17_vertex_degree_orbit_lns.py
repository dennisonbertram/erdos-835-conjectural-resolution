#!/usr/bin/env python3
"""Degree-only full-orbit LNS for the cyclic Wallis phase model.

One move reoptimizes all 105 fixed-pair phases in one moving-triple orbit,
while the other 39 orbits remain fixed.  Every move preserves the phase
lists and all cross-orbit proper-edge-colouring constraints.  Its exact
linear objective is the total L1 deviation from the necessary per-slice
vertex degrees (8 at moving point 0 and 7 at all other moving points).

This is a seed search for the degree relaxation only.  It does not impose
residual-edge collision constraints and therefore cannot certify the full
radius-five quotient or Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
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


def optimize_orbit_for_degrees(
    state: State,
    domains,
    orbit_index: int,
    *,
    seconds: float,
    workers: int,
    seed: int,
) -> tuple[str, int, dict[tuple[int, int], int] | None]:
    model = cp_model.CpModel()
    choose = {}
    base_degrees = {}
    objective_terms = []

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
            final_l1 = sum(
                abs(
                    base_degrees[i, j][vertex]
                    + int(vertex in triple)
                    - (8 if vertex == 0 else 7)
                )
                for vertex in range(P)
            )
            if final_l1:
                objective_terms.append(-final_l1 * literal)
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
        return solver.StatusName(status), -1, None

    assignment = {}
    predicted_l1 = 0
    for i, j in FIXED_PAIRS:
        selected = [
            shift for shift in domains[i, j, orbit_index]
            if solver.Value(choose[i, j, shift])
        ]
        assert len(selected) == 1
        assignment[i, j] = selected[0]
        triple = translate(
            REPRESENTATIVES[orbit_index], selected[0]
        )
        predicted_l1 += sum(
            abs(
                base_degrees[i, j][vertex]
                + int(vertex in triple)
                - (8 if vertex == 0 else 7)
            )
            for vertex in range(P)
        )
    return solver.StatusName(status), predicted_l1, assignment


def write_seed(path: Path, state: State) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def audit_domains_only(state: State, domains) -> None:
    if set(state) != set(domains):
        raise ValueError("state has the wrong phase cells")
    for key, value in state.items():
        if value not in domains[key]:
            raise ValueError(f"phase violates zero-factor list at {key}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sweeps", type=int, default=4)
    parser.add_argument("--seconds-per-orbit", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--accept-equal", action="store_true")
    parser.add_argument(
        "--repair-cross",
        action="store_true",
        help=(
            "allow a domain-valid but cross-incompatible input; the first "
            "sweep replaces every orbit by a proper edge-colouring"
        ),
    )
    args = parser.parse_args()

    rng = random.Random(args.seed)
    golf = construct_golf17()
    domains = domains_for_seed(golf)
    state = load_state(args.source)
    if args.repair_cross:
        audit_domains_only(state, domains)
    else:
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

    for sweep in range(args.sweeps):
        order = list(range(len(REPRESENTATIVES)))
        rng.shuffle(order)
        accepted = 0
        for step, orbit_index in enumerate(order):
            status, predicted, assignment = optimize_orbit_for_degrees(
                state,
                domains,
                orbit_index,
                seconds=args.seconds_per_orbit,
                workers=args.workers,
                seed=rng.randrange(1, 2**31),
            )
            if assignment is None:
                if args.repair_cross and sweep == 0:
                    raise RuntimeError(
                        f"failed to repair orbit {orbit_index}: {status}"
                    )
                continue
            changed = any(
                assignment[i, j] != state[i, j, orbit_index]
                for i, j in FIXED_PAIRS
            )
            repairing = args.repair_cross and sweep == 0
            if not changed and not repairing:
                continue
            if not repairing and (
                predicted > current or (
                predicted == current and not args.accept_equal
                )
            ):
                continue
            old = current
            for (i, j), shift in assignment.items():
                state[i, j, orbit_index] = shift
            if not repairing:
                audit_static(state, domains)
            current = degree_l1(state)
            assert current == predicted
            accepted += 1
            write_seed(args.output, state)
            print(
                json.dumps(
                    {
                        "status": status,
                        "sweep": sweep,
                        "step": step,
                        "orbit": orbit_index,
                        "old_degree_l1": old,
                        "degree_l1": current,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            if current == 0 and not repairing:
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
        print(
            json.dumps(
                {
                    "status": "SWEEP",
                    "sweep": sweep,
                    "accepted": accepted,
                    "degree_l1": current,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if args.repair_cross and sweep == 0:
            audit_static(state, domains)
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
        if accepted == 0 and not args.accept_equal:
            break

    sha = write_seed(args.output, state)
    print(
        json.dumps(
            {
                "status": "DONE",
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
