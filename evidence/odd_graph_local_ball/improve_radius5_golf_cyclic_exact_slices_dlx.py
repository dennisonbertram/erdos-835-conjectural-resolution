#!/usr/bin/env python3
"""Glue exact cyclic slices with weighted bit-parallel Algorithm X.

Every coordinate move re-solves one fixed-pair slice exactly using the
companion C++ exact-cover solver.  Row exactness is therefore invariant.
The row weights count collisions with the thirteen other incident golf-pair
edges at each endpoint, orbit by orbit.  A zero global collision count is
exactly the shared-N proper-edge-colouring condition.

Any positive collision count is only a search seed.  A zero-collision output
must still be passed through the independent joint semantic verifier before
it is called a radius-five layer.
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


def load_state(path: Path) -> State:
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = {f"{i},{j}" for i, j in FIXED_PAIRS}
    if set(payload) != expected:
        raise ValueError("seed must contain all 105 fixed-pair slices")
    state = {}
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        if (
            not isinstance(phases, list)
            or len(phases) != len(ORBITS)
            or not all(
                isinstance(phase, int) and 0 <= phase < P
                for phase in phases
            )
        ):
            raise ValueError(f"invalid phase list for {i},{j}")
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


def incident_pair(first: int, second: int) -> tuple[int, int]:
    return min(first, second), max(first, second)


def cross_metrics(state: State) -> tuple[int, int, int]:
    distinct = 0
    collision_pairs = 0
    conflict_free = 0
    for fixed_point in FIXED:
        for orbit in ORBITS:
            counts = collections.Counter(
                state[incident_pair(fixed_point, other)][orbit]
                for other in FIXED
                if other != fixed_point
            )
            distinct += len(counts)
            collision_pairs += sum(
                multiplicity * (multiplicity - 1) // 2
                for multiplicity in counts.values()
            )
            conflict_free += len(counts) == 14
    return distinct, collision_pairs, conflict_free


def pair_pressure(
    state: State,
    fixed_pair: tuple[int, int],
) -> int:
    i, j = fixed_pair
    return sum(
        sum(
            multiplicity * (multiplicity - 1) // 2
            for multiplicity in collections.Counter(
                state[incident_pair(endpoint, other)][orbit]
                for other in FIXED
                if other != endpoint
            ).values()
        )
        for endpoint in fixed_pair
        for orbit in ORBITS
    )


def weight_table(
    state: State,
    fixed_pair: tuple[int, int],
) -> list[list[int]]:
    i, j = fixed_pair
    answer = []
    for orbit in ORBITS:
        other_i = collections.Counter(
            state[incident_pair(i, other)][orbit]
            for other in FIXED
            if other not in fixed_pair
        )
        other_j = collections.Counter(
            state[incident_pair(j, other)][orbit]
            for other in FIXED
            if other not in fixed_pair
        )
        answer.append(
            [
                other_i[(-shift) % P] + other_j[(-shift) % P]
                for shift in range(P)
            ]
        )
    return answer


def solve_pair(
    binary: Path,
    state: State,
    fixed_pair: tuple[int, int],
    *,
    seconds: float,
    nodes: int,
    seed: int,
    optimize_weight: bool,
) -> tuple[str, int, list[int] | None]:
    table = weight_table(state, fixed_pair)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="cyclic17-slice-weights-",
        suffix=".txt",
    ) as weights:
        for row in table:
            weights.write(" ".join(map(str, row)) + "\n")
        weights.flush()
        command = [
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
            weights.name,
        ]
        if optimize_weight:
            command.append("--optimize-weight")
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    if not completed.stdout.strip():
        raise RuntimeError(
            f"weighted exact-cover solver produced no output: "
            f"{completed.stderr}"
        )
    result = json.loads(completed.stdout)
    if result.get("status") != "SAT":
        return str(result.get("status")), -1, None
    shifts = result.get("selected_shifts")
    if (
        not isinstance(shifts, list)
        or len(shifts) != len(ORBITS)
        or not all(
            isinstance(shift, int) and 0 <= shift < P
            for shift in shifts
        )
    ):
        raise ValueError("weighted exact-cover solver returned bad shifts")
    return (
        str(result["status"]),
        int(result["weight"]),
        [(-shift) % P for shift in shifts],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sweeps", type=int, default=5)
    parser.add_argument("--seconds-per-pair", type=float, default=3.0)
    parser.add_argument("--nodes", type=int, default=1_000_000_000)
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--optimize-weight", action="store_true")
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--accept-equal", action="store_true")
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    state = load_state(args.source)
    rng = random.Random(args.seed)
    distinct, collisions, conflict_free = cross_metrics(state)
    print(
        json.dumps(
            {
                "status": "START",
                "distinct_phase_slots": distinct,
                "collision_pairs": collisions,
                "conflict_free_groups": conflict_free,
                "target_distinct_phase_slots": 8400,
                "all_105_slices_exact": True,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    if args.audit_only:
        sha = write_state(args.output, state)
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "phase_sha256": sha,
                    "scope": "105 exact slices; cross collisions reported",
                },
                sort_keys=True,
            )
        )
        return

    for sweep in range(args.sweeps):
        order = list(FIXED_PAIRS)
        rng.shuffle(order)
        order.sort(key=lambda pair: -pair_pressure(state, pair))
        accepted = 0
        for step, fixed_pair in enumerate(order):
            old_phases = state[fixed_pair]
            old_metrics = (distinct, collisions, conflict_free)
            best_phases = None
            best_metrics = old_metrics
            best_weight = -1
            best_status = "UNKNOWN"
            for _ in range(args.attempts):
                status, weight, phases = solve_pair(
                    args.binary,
                    state,
                    fixed_pair,
                    seconds=args.seconds_per_pair,
                    nodes=args.nodes,
                    seed=rng.randrange(1, 2**63),
                    optimize_weight=args.optimize_weight,
                )
                if phases is None:
                    continue
                state[fixed_pair] = phases
                metrics = cross_metrics(state)
                state[fixed_pair] = old_phases
                # Collision pairs are the exact weighted local objective.
                # Distinct slots and conflict-free groups are secondary.
                quality = (-metrics[1], metrics[0], metrics[2])
                old_quality = (
                    -best_metrics[1],
                    best_metrics[0],
                    best_metrics[2],
                )
                if quality > old_quality or (
                    args.accept_equal
                    and quality == old_quality
                    and phases != old_phases
                    and best_phases is None
                ):
                    best_phases = phases
                    best_metrics = metrics
                    best_weight = weight
                    best_status = status
            changed = best_phases is not None and best_phases != old_phases
            improves = best_metrics[1] < collisions
            equal = best_metrics[1] == collisions
            if not changed or not (
                improves or (args.accept_equal and equal)
            ):
                continue
            state[fixed_pair] = best_phases
            distinct, collisions, conflict_free = best_metrics
            accepted += 1
            sha = write_state(args.output, state)
            print(
                json.dumps(
                    {
                        "status": best_status,
                        "sweep": sweep,
                        "step": step,
                        "pair": list(fixed_pair),
                        "weighted_local_cost": best_weight,
                        "distinct_phase_slots": distinct,
                        "collision_pairs": collisions,
                        "conflict_free_groups": conflict_free,
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
                            "status": "CROSS_COMPATIBLE_EXACT_SLICES",
                            "phase_sha256": sha,
                            "semantic_joint_verifier": "REQUIRED",
                            "scope": (
                                "candidate fixed-Wallis C17 layer only; "
                                "not full problem 835"
                            ),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
                return
        print(
            json.dumps(
                {
                    "status": "SWEEP",
                    "sweep": sweep,
                    "accepted": accepted,
                    "distinct_phase_slots": distinct,
                    "collision_pairs": collisions,
                    "conflict_free_groups": conflict_free,
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
                "status": "NO_JOINT_WITNESS",
                "distinct_phase_slots": distinct,
                "collision_pairs": collisions,
                "conflict_free_groups": conflict_free,
                "phase_sha256": sha,
                "mathematical_status": "heuristic only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
