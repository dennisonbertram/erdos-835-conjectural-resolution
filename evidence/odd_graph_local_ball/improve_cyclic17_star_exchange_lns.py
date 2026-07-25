#!/usr/bin/env python3
"""Exchange several exact rows while reducing one cyclic-17 star's collisions.

The source contains all 105 independently exact fixed-pair rows.  At one
chosen star centre, this program repeatedly re-solves a small set of incident
rows simultaneously.  Every changed row retains all eight exact residual-edge
permutations.  The CP-SAT objective is the exact number of phase-collision
pairs involving the exchanged rows; collisions among untouched rows are a
constant and are omitted.

This is a heuristic search.  Only collision count zero, followed by an
independent audit, is a one-star witness.  Even that would be only a necessary
local piece of the fixed-Wallis C17 ansatz, not a solution of ER #835.
"""

from __future__ import annotations

import argparse
import collections
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
from search_radius5_golf_cyclic_compact import (
    DIFFERENCES,
    P,
    POINTS,
    REPRESENTATIVE_EDGE_COORDINATES,
    REPRESENTATIVES,
    SQUARES,
    allowed_shifts,
    zero_positions,
)


FIXED_PAIRS = tuple(combinations(SQUARES, 2))
ORBITS = tuple(range(len(REPRESENTATIVES)))
State = dict[tuple[int, int], list[int]]


def incident_pair(first: int, second: int) -> tuple[int, int]:
    return min(first, second), max(first, second)


def load_state(path: Path) -> State:
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = {f"{i},{j}" for i, j in FIXED_PAIRS}
    if set(payload) != expected:
        raise ValueError("seed must contain all 105 fixed-pair rows")
    state = {}
    for pair in FIXED_PAIRS:
        values = payload[f"{pair[0]},{pair[1]}"]
        if (
            not isinstance(values, list)
            or len(values) != len(ORBITS)
            or not all(
                isinstance(value, int) and 0 <= value < P
                for value in values
            )
        ):
            raise ValueError(f"invalid phase row {pair}")
        # The portable JSON uses the historical canonical phase convention;
        # the compact model uses the actual translation shift.
        state[pair] = [(-value) % P for value in values]
    return state


def dump_state(state: State) -> dict[str, list[int]]:
    return {
        f"{pair[0]},{pair[1]}": [
            (-value) % P for value in state[pair]
        ]
        for pair in FIXED_PAIRS
    }


def write_state(path: Path, state: State) -> str:
    encoded = (
        json.dumps(dump_state(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def centre_metrics(state: State, centre: int) -> tuple[int, int, int]:
    distinct = 0
    collisions = 0
    exact = 0
    for orbit in ORBITS:
        counts = collections.Counter(
            state[incident_pair(centre, other)][orbit]
            for other in SQUARES
            if other != centre
        )
        distinct += len(counts)
        collisions += sum(
            multiplicity * (multiplicity - 1) // 2
            for multiplicity in counts.values()
        )
        exact += len(counts) == len(SQUARES) - 1
    return distinct, collisions, exact


def row_pressure(state: State, centre: int, pair: tuple[int, int]) -> int:
    return sum(
        state[pair][orbit]
        == state[incident_pair(centre, other)][orbit]
        for orbit in ORBITS
        for other in SQUARES
        if other not in pair
    )


def audit_row(
    state: State,
    pair: tuple[int, int],
    zeros,
) -> None:
    for difference in DIFFERENCES:
        positions = []
        for orbit, coordinates in enumerate(
            REPRESENTATIVE_EDGE_COORDINATES
        ):
            phase = state[pair][orbit]
            positions.extend(
                (phase + offset) % P
                for edge_difference, offset in coordinates
                if edge_difference == difference
            )
        expected = set(POINTS) - {
            zeros[pair[0], difference],
            zeros[pair[1], difference],
        }
        if len(positions) != 15 or set(positions) != expected:
            raise AssertionError(
                f"row {pair}, difference {difference} is not exact"
            )


def solve_exchange(
    state: State,
    centre: int,
    changed: list[tuple[int, int]],
    zeros,
    *,
    seconds: float,
    workers: int,
    seed: int,
) -> tuple[str, int | None, bool, dict[tuple[int, int], list[int]]]:
    model = cp_model.CpModel()
    phases = {}
    positions = collections.defaultdict(list)

    for pair in changed:
        for orbit, coordinates in enumerate(
            REPRESENTATIVE_EDGE_COORDINATES
        ):
            phase = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(
                    allowed_shifts(pair, orbit, zeros)
                ),
                f"phase_{pair[0]}_{pair[1]}_{orbit}",
            )
            phases[pair, orbit] = phase
            model.AddHint(phase, state[pair][orbit])
            for occurrence, (difference, offset) in enumerate(coordinates):
                residual = [
                    value
                    for value in POINTS
                    if value
                    not in {
                        zeros[pair[0], difference],
                        zeros[pair[1], difference],
                    }
                ]
                position = model.NewIntVarFromDomain(
                    cp_model.Domain.FromValues(residual),
                    f"pos_{pair[0]}_{pair[1]}_{orbit}_{occurrence}",
                )
                model.AddModuloEquality(position, phase + offset, P)
                positions[pair, difference].append(position)

    for pair in changed:
        for difference in DIFFERENCES:
            variables = positions[pair, difference]
            if len(variables) != 15:
                raise AssertionError("wrong edge-position multiplicity")
            model.AddAllDifferent(variables)
            model.Add(
                sum(variables)
                == sum(POINTS)
                - zeros[pair[0], difference]
                - zeros[pair[1], difference]
            )

    changed_set = set(changed)
    fixed = [
        incident_pair(centre, other)
        for other in SQUARES
        if other != centre
        and incident_pair(centre, other) not in changed_set
    ]
    objective_terms = []
    for pair in changed:
        for orbit in ORBITS:
            counts = collections.Counter(
                state[other][orbit] for other in fixed
            )
            cost_by_phase = [counts[value] for value in POINTS]
            cost = model.NewIntVar(
                min(cost_by_phase),
                max(cost_by_phase),
                f"fixed_cost_{pair[0]}_{pair[1]}_{orbit}",
            )
            model.AddElement(
                phases[pair, orbit],
                cost_by_phase,
                cost,
            )
            objective_terms.append(cost)

    for left, right in combinations(changed, 2):
        for orbit in ORBITS:
            equal = model.NewBoolVar(
                f"equal_{left[0]}_{left[1]}_"
                f"{right[0]}_{right[1]}_{orbit}"
            )
            model.Add(
                phases[left, orbit] == phases[right, orbit]
            ).OnlyEnforceIf(equal)
            model.Add(
                phases[left, orbit] != phases[right, orbit]
            ).OnlyEnforceIf(equal.Not())
            objective_terms.append(equal)

    objective = sum(objective_terms)
    model.Minimize(objective)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.StatusName(status), None, False, {}

    replacement = {
        pair: [
            solver.Value(phases[pair, orbit])
            for orbit in ORBITS
        ]
        for pair in changed
    }
    return (
        solver.StatusName(status),
        int(round(solver.ObjectiveValue())),
        status == cp_model.OPTIMAL,
        replacement,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--centre", type=int, required=True)
    parser.add_argument("--exchange-size", type=int, default=2)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--seconds-per-exchange", type=float, default=30.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument(
        "--random-pool",
        type=int,
        default=6,
        help="draw exchanged rows from this many highest-pressure rows",
    )
    args = parser.parse_args()

    if args.centre not in SQUARES:
        parser.error("--centre must lie in 0,...,14")
    if not 2 <= args.exchange_size <= len(SQUARES) - 1:
        parser.error("--exchange-size must lie in 2,...,14")
    if args.random_pool < args.exchange_size:
        parser.error("--random-pool must be at least --exchange-size")

    state = load_state(args.source)
    zeros = zero_positions(construct_golf17())
    for pair in FIXED_PAIRS:
        audit_row(state, pair, zeros)

    rng = random.Random(args.seed)
    incident = [
        incident_pair(args.centre, other)
        for other in SQUARES
        if other != args.centre
    ]
    distinct, collisions, exact = centre_metrics(state, args.centre)
    print(
        json.dumps(
            {
                "status": "START",
                "centre": args.centre,
                "exchange_size": args.exchange_size,
                "distinct": distinct,
                "collision_pairs": collisions,
                "exact_groups": exact,
            },
            sort_keys=True,
        ),
        flush=True,
    )

    for step in range(args.steps):
        ranked = list(incident)
        rng.shuffle(ranked)
        ranked.sort(
            key=lambda pair: -row_pressure(state, args.centre, pair)
        )
        pool = ranked[: min(args.random_pool, len(ranked))]
        changed = sorted(rng.sample(pool, args.exchange_size))
        old_rows = {pair: state[pair] for pair in changed}
        old_metrics = (distinct, collisions, exact)
        status, local_objective, optimal, replacement = solve_exchange(
            state,
            args.centre,
            changed,
            zeros,
            seconds=args.seconds_per_exchange,
            workers=args.workers,
            seed=rng.randrange(1, 2**31),
        )
        if replacement:
            for pair, row in replacement.items():
                state[pair] = row
                audit_row(state, pair, zeros)
        candidate_metrics = centre_metrics(state, args.centre)
        if candidate_metrics[1] >= collisions:
            for pair, row in old_rows.items():
                state[pair] = row
            accepted = False
        else:
            distinct, collisions, exact = candidate_metrics
            accepted = True
            sha = write_state(args.output, state)
        print(
            json.dumps(
                {
                    "status": "STEP",
                    "step": step,
                    "solver_status": status,
                    "local_objective": local_objective,
                    "local_optimum_proved": optimal,
                    "changed": [list(pair) for pair in changed],
                    "accepted": accepted,
                    "old_collision_pairs": old_metrics[1],
                    "collision_pairs": collisions,
                    "distinct": distinct,
                    "exact_groups": exact,
                    **({"phase_sha256": sha} if accepted else {}),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if collisions == 0:
            for pair in incident:
                audit_row(state, pair, zeros)
            sha = write_state(args.output, state)
            print(
                json.dumps(
                    {
                        "status": "STAR_WITNESS",
                        "centre": args.centre,
                        "verified_exact_rows": 14,
                        "verified_cross_groups": 40,
                        "phase_sha256": sha,
                        "independent_verifier": "REQUIRED",
                        "scope": "one fixed-Wallis C17 star only",
                    },
                    sort_keys=True,
                )
            )
            return

    sha = write_state(args.output, state)
    print(
        json.dumps(
            {
                "status": "NO_STAR_WITNESS",
                "centre": args.centre,
                "distinct": distinct,
                "collision_pairs": collisions,
                "exact_groups": exact,
                "phase_sha256": sha,
                "mathematical_status": "heuristic only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
