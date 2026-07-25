#!/usr/bin/env python3
"""Glue the fourteen exact rows at one fixed-Wallis star center.

Every coordinate move re-solves one complete prescribed-link row with the
bit-parallel Algorithm-X solver, so all 105 rows of the source remain exact.
The weight is only the phase-collision count against the other thirteen rows
at the selected star center.  The exact target is 40*14 = 560 distinct phase
slots (zero collision pairs), which is independently checked before a star
witness is reported.

Failure to hit the target is only heuristic.  A star witness is still only a
necessary local piece of the fixed-Wallis C17 radius-five ansatz.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import random
import subprocess
import tempfile
from itertools import combinations
from pathlib import Path


P = 17
FIXED = tuple(range(15))
FIXED_PAIRS = tuple(combinations(FIXED, 2))
ORBITS = tuple(range(40))
State = dict[tuple[int, int], list[int]]


def incident_pair(first: int, second: int) -> tuple[int, int]:
    return min(first, second), max(first, second)


def load_state(path: Path) -> State:
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = {f"{i},{j}" for i, j in FIXED_PAIRS}
    if set(payload) != expected:
        raise ValueError("seed must contain all 105 exact rows")
    state = {}
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        if (
            not isinstance(phases, list)
            or len(phases) != len(ORBITS)
            or not all(isinstance(value, int) and 0 <= value < P for value in phases)
        ):
            raise ValueError(f"invalid phase row {i},{j}")
        state[i, j] = list(phases)
    return state


def dump_state(state: State) -> dict[str, list[int]]:
    return {f"{i},{j}": state[i, j] for i, j in FIXED_PAIRS}


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
            for other in FIXED
            if other != centre
        )
        distinct += len(counts)
        collisions += sum(
            multiplicity * (multiplicity - 1) // 2
            for multiplicity in counts.values()
        )
        exact += len(counts) == 14
    return distinct, collisions, exact


def row_pressure(
    state: State,
    centre: int,
    fixed_pair: tuple[int, int],
) -> int:
    answer = 0
    for orbit in ORBITS:
        phase = state[fixed_pair][orbit]
        answer += sum(
            state[incident_pair(centre, other)][orbit] == phase
            for other in FIXED
            if other not in fixed_pair
        )
    return answer


def solve_row(
    binary: Path,
    state: State,
    centre: int,
    fixed_pair: tuple[int, int],
    *,
    seconds: float,
    nodes: int,
    seed: int,
) -> tuple[str, bool, int, list[int] | None]:
    weights = []
    for orbit in ORBITS:
        counts = collections.Counter(
            state[incident_pair(centre, other)][orbit]
            for other in FIXED
            if other not in fixed_pair
        )
        weights.append(
            [counts[(-shift) % P] for shift in range(P)]
        )
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="cyclic17-star-row-",
        suffix=".weights",
    ) as stream:
        for values in weights:
            stream.write(" ".join(map(str, values)) + "\n")
        stream.flush()
        completed = subprocess.run(
            [
                str(binary),
                "--pair",
                f"{fixed_pair[0]},{fixed_pair[1]}",
                "--seconds",
                str(seconds),
                "--nodes",
                str(nodes),
                "--seed",
                str(seed),
                "--weights",
                stream.name,
                "--optimize-weight",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    if not completed.stdout.strip():
        raise RuntimeError(
            f"row solver returned no JSON: {completed.stderr.strip()}"
        )
    result = json.loads(completed.stdout)
    if result.get("status") != "SAT":
        return str(result.get("status")), False, -1, None
    shifts = result["selected_shifts"]
    phases = [(-shift) % P for shift in shifts]
    return (
        "SAT",
        bool(result.get("optimal")),
        int(result["weight"]),
        phases,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--centre", type=int, required=True)
    parser.add_argument("--sweeps", type=int, default=10)
    parser.add_argument("--seconds-per-row", type=float, default=5.0)
    parser.add_argument("--nodes", type=int, default=1_000_000_000)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--accept-equal", action="store_true")
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()

    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    if args.centre not in FIXED:
        parser.error("--centre must lie in 0,...,14")
    state = load_state(args.source)
    rng = random.Random(args.seed)
    pairs = [
        incident_pair(args.centre, other)
        for other in FIXED
        if other != args.centre
    ]
    distinct, collisions, exact = centre_metrics(state, args.centre)
    print(
        json.dumps(
            {
                "status": "START",
                "centre": args.centre,
                "distinct": distinct,
                "target": 560,
                "collision_pairs": collisions,
                "exact_groups": exact,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    for sweep in range(args.sweeps):
        order = list(pairs)
        rng.shuffle(order)
        order.sort(
            key=lambda fixed_pair: -row_pressure(
                state,
                args.centre,
                fixed_pair,
            )
        )
        accepted = 0
        for step, fixed_pair in enumerate(order):
            old = state[fixed_pair]
            old_metrics = (distinct, collisions, exact)
            best = None
            best_metrics = old_metrics
            best_weight = -1
            best_optimal = False
            for _ in range(args.attempts):
                status, optimal, weight, phases = solve_row(
                    args.binary,
                    state,
                    args.centre,
                    fixed_pair,
                    seconds=args.seconds_per_row,
                    nodes=args.nodes,
                    seed=rng.randrange(1, 2**63),
                )
                if status != "SAT" or phases is None:
                    continue
                state[fixed_pair] = phases
                metrics = centre_metrics(state, args.centre)
                state[fixed_pair] = old
                quality = (-metrics[1], metrics[0], metrics[2])
                best_quality = (
                    -best_metrics[1],
                    best_metrics[0],
                    best_metrics[2],
                )
                if quality > best_quality:
                    best = phases
                    best_metrics = metrics
                    best_weight = weight
                    best_optimal = optimal
            if best is None or best == old:
                continue
            improves = best_metrics[1] < collisions
            equal = best_metrics[1] == collisions
            if not (improves or (args.accept_equal and equal)):
                continue
            state[fixed_pair] = best
            distinct, collisions, exact = best_metrics
            accepted += 1
            sha = write_state(args.output, state)
            print(
                json.dumps(
                    {
                        "status": "ACCEPTED",
                        "sweep": sweep,
                        "step": step,
                        "pair": list(fixed_pair),
                        "weighted_cost": best_weight,
                        "row_optimum_proved": best_optimal,
                        "distinct": distinct,
                        "collision_pairs": collisions,
                        "exact_groups": exact,
                        "phase_sha256": sha,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            if collisions == 0:
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
        print(
            json.dumps(
                {
                    "status": "SWEEP",
                    "sweep": sweep,
                    "accepted": accepted,
                    "distinct": distinct,
                    "collision_pairs": collisions,
                    "exact_groups": exact,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if accepted == 0 and not args.accept_equal:
            break
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
