#!/usr/bin/env python3
"""Heuristically glue a small centre-0 subset by exact row coordinates.

All states consist solely of independently exact prescribed-link rows.  A
coordinate move re-solves one row with weighted Algorithm X, using its phase
collision count against the other selected rows as the objective.  A
zero-collision state is independently checked and is a genuine witness for
the requested subsystem.  Failure or a positive local minimum is UNKNOWN.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from generate_cyclic17_star_quadruple_compatibility import (
    ORBITS,
    OUTERS,
    P,
    load_width_three,
    merge_pool,
)
from global_latin_audit import construct_golf17
from verify_cyclic17_star_pairwise_compatibility import verify_row


def parse_outers(text: str) -> tuple[int, ...]:
    try:
        values = tuple(sorted(set(map(int, text.split(",")))))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "outers must be comma-separated"
        ) from error
    if len(values) < 2 or any(value not in OUTERS for value in values):
        raise argparse.ArgumentTypeError(
            "choose at least two outers in 1,...,14"
        )
    return values


def collision(first, second) -> int:
    return sum(left == right for left, right in zip(first, second))


def objective(state, outers) -> int:
    return sum(
        collision(state[left], state[right])
        for left, right in itertools.combinations(outers, 2)
    )


def row_pressure(state, outer, outers) -> int:
    return sum(
        collision(state[outer], state[other])
        for other in outers
        if other != outer
    )


def solve_weighted(
    binary: Path,
    solved_outer: int,
    base_rows,
    *,
    seconds: float,
    nodes: int,
    seed: int,
):
    base_shifts = [
        [(-phase) % P for phase in row]
        for row in base_rows
    ]
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="cyclic17-subset-coordinate-",
        suffix=".weights",
    ) as stream:
        for orbit in range(ORBITS):
            stream.write(
                " ".join(
                    str(
                        sum(
                            shift == shifts[orbit]
                            for shifts in base_shifts
                        )
                    )
                    for shift in range(P)
                )
                + "\n"
            )
        stream.flush()
        completed = subprocess.run(
            [
                str(binary),
                "--pair",
                f"0,{solved_outer}",
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
        return None
    shifts = result.get("selected_shifts")
    if (
        not isinstance(shifts, list)
        or len(shifts) != ORBITS
    ):
        raise ValueError("row solver returned malformed shifts")
    phases = tuple((-shift) % P for shift in shifts)
    measured = sum(
        collision(phases, base_row) for base_row in base_rows
    )
    if measured != result.get("weight"):
        raise AssertionError("row solver weight disagrees with audit")
    return {
        "phases": phases,
        "weight": measured,
        "optimal": bool(result.get("optimal")),
        "nodes": result.get("nodes"),
    }


def finite_pool_best(pools, outers, *, seconds: float, workers: int):
    model = cp_model.CpModel()
    choice = {
        outer: model.NewIntVar(
            0,
            len(pools[outer]) - 1,
            f"choice_{outer}",
        )
        for outer in outers
    }
    costs = []
    for left, right in itertools.combinations(outers, 2):
        table = [
            (
                left_index,
                right_index,
                collision(left_row, right_row),
            )
            for left_index, left_row in enumerate(pools[left])
            for right_index, right_row in enumerate(pools[right])
        ]
        values = [entry[2] for entry in table]
        cost = model.NewIntVar(
            min(values),
            max(values),
            f"collision_{left}_{right}",
        )
        model.AddAllowedAssignments(
            [choice[left], choice[right], cost],
            table,
        )
        costs.append(cost)
    model.Minimize(sum(costs))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    return {
        outer: pools[outer][solver.Value(choice[outer])]
        for outer in outers
    }


def best_pool_state(
    pools,
    outers,
    triple_witnesses,
    rng,
    *,
    master_seconds,
    workers,
):
    candidates = []
    finite_master = finite_pool_best(
        pools,
        outers,
        seconds=master_seconds,
        workers=workers,
    )
    if finite_master is not None:
        candidates.append(finite_master)
    if len(outers) == 4:
        for omitted in outers:
            base_outers = tuple(
                outer for outer in outers if outer != omitted
            )
            base = triple_witnesses[base_outers]
            for row in pools[omitted]:
                state = dict(base)
                state[omitted] = row
                candidates.append(state)
    for _ in range(200):
        candidates.append(
            {
                outer: rng.choice(pools[outer])
                for outer in outers
            }
        )
    return min(candidates, key=lambda state: objective(state, outers))


def verify_state(state, outers):
    golf = construct_golf17()
    for outer in outers:
        verify_row(golf, 0, outer, list(state[outer]))
    score = objective(state, outers)
    if score != 0:
        raise ValueError("state is not collision-free")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("width_three_certificate", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--outers", type=parse_outers, required=True)
    parser.add_argument(
        "--pool-source",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument("--seconds-per-row", type=float, default=5.0)
    parser.add_argument("--pool-master-seconds", type=float, default=30.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--nodes", type=int, default=1_000_000_000)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--sweeps", type=int, default=10)
    parser.add_argument("--restarts", type=int, default=4)
    parser.add_argument("--accept-equal", action="store_true")
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()
    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)

    rng = random.Random(args.seed)
    pools = {outer: [] for outer in OUTERS}
    _, triple_witnesses = load_width_three(
        args.width_three_certificate,
        pools,
    )
    for path in args.pool_source:
        merge_pool(path, pools)

    best_state = best_pool_state(
        pools,
        args.outers,
        triple_witnesses,
        rng,
        master_seconds=args.pool_master_seconds,
        workers=args.workers,
    )
    best_score = objective(best_state, args.outers)
    print(
        json.dumps(
            {
                "status": "START",
                "outers": list(args.outers),
                "collision_pairs": best_score,
                "pool_sizes": {
                    str(outer): len(pools[outer])
                    for outer in args.outers
                },
            },
            sort_keys=True,
        ),
        flush=True,
    )

    visited = set()
    for restart in range(args.restarts):
        if restart == 0:
            state = dict(best_state)
        else:
            state = dict(best_state)
            changed = rng.sample(
                list(args.outers),
                k=min(
                    len(args.outers),
                    1 + rng.randrange(2),
                ),
            )
            for outer in changed:
                state[outer] = rng.choice(pools[outer])
        score = objective(state, args.outers)
        for sweep in range(args.sweeps):
            order = list(args.outers)
            rng.shuffle(order)
            order.sort(
                key=lambda outer: -row_pressure(
                    state,
                    outer,
                    args.outers,
                )
            )
            accepted = 0
            for outer in order:
                base_rows = [
                    state[other]
                    for other in args.outers
                    if other != outer
                ]
                base_score = sum(
                    collision(base_rows[left], base_rows[right])
                    for left, right in itertools.combinations(
                        range(len(base_rows)),
                        2,
                    )
                )
                best_move = None
                for _ in range(args.attempts):
                    result = solve_weighted(
                        args.binary,
                        outer,
                        base_rows,
                        seconds=args.seconds_per_row,
                        nodes=args.nodes,
                        seed=rng.randrange(1, 2**63),
                    )
                    if result is None:
                        continue
                    candidate_score = base_score + result["weight"]
                    key = (outer, result["phases"])
                    admissible = (
                        candidate_score < score
                        or (
                            args.accept_equal
                            and candidate_score == score
                            and key not in visited
                        )
                    )
                    if admissible and (
                        best_move is None
                        or candidate_score < best_move[0]
                    ):
                        best_move = (
                            candidate_score,
                            result["phases"],
                            result,
                        )
                if best_move is None:
                    continue
                score, phases, result = best_move
                state[outer] = phases
                visited.add((outer, phases))
                accepted += 1
                if phases not in pools[outer]:
                    pools[outer].append(phases)
                if score < best_score:
                    best_score = score
                    best_state = dict(state)
                    print(
                        json.dumps(
                            {
                                "status": "IMPROVEMENT",
                                "restart": restart,
                                "sweep": sweep,
                                "outer": outer,
                                "collision_pairs": score,
                                "row_weight_optimal": result[
                                    "optimal"
                                ],
                            },
                            sort_keys=True,
                        ),
                        flush=True,
                    )
                if score == 0:
                    verify_state(state, args.outers)
                    payload = {
                        "schema": (
                            "cyclic17-centre0-subset-witness-v1"
                        ),
                        "centre": 0,
                        "outers": list(args.outers),
                        "phase_rows": [
                            list(state[outer])
                            for outer in args.outers
                        ],
                        "collision_count": 0,
                        "scope": (
                            "selected centre-0 outer rows only"
                        ),
                    }
                    encoded = (
                        json.dumps(
                            payload,
                            indent=2,
                            sort_keys=True,
                        )
                        + "\n"
                    ).encode("utf-8")
                    args.output.write_bytes(encoded)
                    print(
                        json.dumps(
                            {
                                "status": "SUBSET_WITNESS",
                                "outers": list(args.outers),
                                "certificate_sha256": hashlib.sha256(
                                    encoded
                                ).hexdigest(),
                                "semantic_verifier": "PASS",
                            },
                            sort_keys=True,
                        )
                    )
                    return
            print(
                json.dumps(
                    {
                        "status": "SWEEP",
                        "restart": restart,
                        "sweep": sweep,
                        "accepted": accepted,
                        "collision_pairs": score,
                        "best_collision_pairs": best_score,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            if accepted == 0:
                break

    print(
        json.dumps(
            {
                "status": "UNKNOWN",
                "outers": list(args.outers),
                "best_collision_pairs": best_score,
                "mathematical_status": "heuristic only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
