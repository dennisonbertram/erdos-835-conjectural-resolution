#!/usr/bin/env python3
"""Search a cyclic-17 star by coordinating a growing pool of exact rows.

Each pool entry is a complete, independently checkable residual triangle
decomposition for one incident fixed-pair row.  A small CP-SAT master chooses
one entry per row and minimizes the exact number of cross-orbit phase
collision pairs.  Weighted Algorithm-X pricing then adds new exact rows
against the current master choice.  Retaining old rows lets several changes
be accepted together, unlike one-row coordinate descent.

This is heuristic column generation.  A zero-collision output is a one-star
witness after independent verification; failure to reach zero proves nothing.
Even a verified star is only a necessary local piece of the fixed-Wallis C17
radius-five ansatz and does not solve ER #835.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from improve_cyclic17_star_exact_rows import (
    FIXED,
    ORBITS,
    P,
    State,
    centre_metrics,
    incident_pair,
    load_state,
    solve_row,
    write_state,
)
from search_radius5_golf_cyclic_compact import (
    MOVING_EDGES,
    REPRESENTATIVES,
    translate,
)

GOLF = construct_golf17()


def audit_row(state: State, pair: tuple[int, int]) -> None:
    selected_edges = []
    for orbit, portable_phase in enumerate(state[pair]):
        triple = translate(
            REPRESENTATIVES[orbit],
            (-portable_phase) % P,
        )
        selected_edges.extend(combinations(triple, 2))
    if len(selected_edges) != 120 or len(set(selected_edges)) != 120:
        raise AssertionError(f"row {pair} is not an exact edge packing")
    uncovered = set(MOVING_EDGES) - set(selected_edges)
    expected_leave = {
        edge
        for edge in MOVING_EDGES
        if GOLF[pair[0]][edge[0]][edge[1]] == 0
        or GOLF[pair[1]][edge[0]][edge[1]] == 0
    }
    if uncovered != expected_leave:
        raise AssertionError(f"row {pair} has the wrong prescribed leave")


def master_solve(
    pools: dict[tuple[int, int], list[tuple[int, ...]]],
    pairs: list[tuple[int, int]],
    *,
    seconds: float,
    workers: int,
    seed: int,
    previous: dict[tuple[int, int], int] | None,
    incumbent: int | None,
) -> tuple[str, int | None, int | None, dict[tuple[int, int], int]]:
    model = cp_model.CpModel()
    choice = {}
    for pair in pairs:
        choice[pair] = model.NewIntVar(
            0,
            len(pools[pair]) - 1,
            f"choice_{pair[0]}_{pair[1]}",
        )
        if previous is not None and previous[pair] < len(pools[pair]):
            model.AddHint(choice[pair], previous[pair])

    collisions = []
    for left, right in combinations(pairs, 2):
        table = [
            (
                left_index,
                right_index,
                sum(
                    left_row[orbit] == right_row[orbit]
                    for orbit in ORBITS
                ),
            )
            for left_index, left_row in enumerate(pools[left])
            for right_index, right_row in enumerate(pools[right])
        ]
        costs = [entry[2] for entry in table]
        collision_cost = model.NewIntVar(
            min(costs),
            max(costs),
            f"collision_{left[0]}_{left[1]}_"
            f"{right[0]}_{right[1]}",
        )
        model.AddAllowedAssignments(
            [choice[left], choice[right], collision_cost],
            table,
        )
        collisions.append(collision_cost)
    total_collisions = sum(collisions)
    if incumbent is not None:
        # Every previous row is retained in its pool, so this bound is
        # feasible whenever ``previous`` is complete.  It prevents a
        # time-limited master solve from overwriting the best state with a
        # worse feasible incumbent.
        model.Add(total_collisions <= incumbent)
    model.Minimize(total_collisions)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.StatusName(status), None, None, {}
    selected = {pair: solver.Value(choice[pair]) for pair in pairs}
    return (
        solver.StatusName(status),
        int(round(solver.ObjectiveValue())),
        int(round(solver.BestObjectiveBound())),
        selected,
    )


def heuristic_master_solve(
    pools: dict[tuple[int, int], list[tuple[int, ...]]],
    pairs: list[tuple[int, int]],
    *,
    seconds: float,
    seed: int,
    previous: dict[tuple[int, int], int] | None,
    incumbent: int | None,
) -> tuple[str, int | None, int | None, dict[tuple[int, int], int]]:
    """Solve the 14-variable finite-pool master by exact-cost ILS.

    The returned objective is audited exactly, but this routine supplies no
    lower bound.  It is a faster witness-finding alternative to CP-SAT once
    the retained row pools become large.
    """

    rng = random.Random(seed)
    size = len(pairs)
    pair_cost = {}
    for left_index, left in enumerate(pairs):
        for right_index in range(left_index + 1, size):
            right = pairs[right_index]
            pair_cost[left_index, right_index] = [
                [
                    sum(
                        left_row[orbit] == right_row[orbit]
                        for orbit in ORBITS
                    )
                    for right_row in pools[right]
                ]
                for left_row in pools[left]
            ]

    def cost_at(
        left_index: int,
        left_choice: int,
        right_index: int,
        right_choice: int,
    ) -> int:
        if left_index < right_index:
            return pair_cost[left_index, right_index][left_choice][
                right_choice
            ]
        return pair_cost[right_index, left_index][right_choice][left_choice]

    def objective(selected: list[int]) -> int:
        return sum(
            cost_at(left, selected[left], right, selected[right])
            for left in range(size)
            for right in range(left + 1, size)
        )

    def single_descent(selected: list[int]) -> tuple[list[int], int]:
        current = objective(selected)
        while True:
            best_delta = 0
            best_moves = []
            order = list(range(size))
            rng.shuffle(order)
            for index in order:
                old = selected[index]
                old_cost = sum(
                    cost_at(index, old, other, selected[other])
                    for other in range(size)
                    if other != index
                )
                for candidate in range(len(pools[pairs[index]])):
                    if candidate == old:
                        continue
                    new_cost = sum(
                        cost_at(index, candidate, other, selected[other])
                        for other in range(size)
                        if other != index
                    )
                    delta = new_cost - old_cost
                    if delta < best_delta:
                        best_delta = delta
                        best_moves = [(index, candidate)]
                    elif delta == best_delta and delta < 0:
                        best_moves.append((index, candidate))
            if not best_moves:
                return selected, current
            index, candidate = rng.choice(best_moves)
            selected[index] = candidate
            current += best_delta

    def pair_improvement(
        selected: list[int],
        current: int,
    ) -> tuple[list[int], int, bool]:
        best_delta = 0
        best_moves = []
        for left in range(size):
            for right in range(left + 1, size):
                old_left = selected[left]
                old_right = selected[right]
                old_contribution = cost_at(
                    left,
                    old_left,
                    right,
                    old_right,
                ) + sum(
                    cost_at(left, old_left, other, selected[other])
                    + cost_at(right, old_right, other, selected[other])
                    for other in range(size)
                    if other not in (left, right)
                )
                for left_candidate in range(len(pools[pairs[left]])):
                    for right_candidate in range(
                        len(pools[pairs[right]])
                    ):
                        if (
                            left_candidate == old_left
                            and right_candidate == old_right
                        ):
                            continue
                        new_contribution = cost_at(
                            left,
                            left_candidate,
                            right,
                            right_candidate,
                        ) + sum(
                            cost_at(
                                left,
                                left_candidate,
                                other,
                                selected[other],
                            )
                            + cost_at(
                                right,
                                right_candidate,
                                other,
                                selected[other],
                            )
                            for other in range(size)
                            if other not in (left, right)
                        )
                        delta = new_contribution - old_contribution
                        if delta < best_delta:
                            best_delta = delta
                            best_moves = [
                                (
                                    left,
                                    left_candidate,
                                    right,
                                    right_candidate,
                                )
                            ]
                        elif delta == best_delta and delta < 0:
                            best_moves.append(
                                (
                                    left,
                                    left_candidate,
                                    right,
                                    right_candidate,
                                )
                            )
        if not best_moves:
            return selected, current, False
        left, left_candidate, right, right_candidate = rng.choice(
            best_moves
        )
        selected[left] = left_candidate
        selected[right] = right_candidate
        return selected, current + best_delta, True

    if previous is not None:
        best = [previous[pair] for pair in pairs]
    else:
        best = [0] * size
    best_objective = objective(best)
    if incumbent is not None and best_objective > incumbent:
        raise AssertionError("previous finite-pool choice exceeds incumbent")

    deadline = time.monotonic() + seconds
    temperature = 2.5
    current = list(best)
    current_objective = best_objective
    restarts = 0
    while time.monotonic() < deadline and best_objective:
        if restarts == 0:
            current = list(best)
        else:
            current = list(best)
            changes = 2 + rng.randrange(5)
            for _ in range(changes):
                index = rng.randrange(size)
                current[index] = rng.randrange(len(pools[pairs[index]]))
        current, current_objective = single_descent(current)
        if time.monotonic() < deadline:
            current, current_objective, improved_pair = pair_improvement(
                current,
                current_objective,
            )
            if improved_pair:
                current, current_objective = single_descent(current)
        if current_objective < best_objective:
            best = list(current)
            best_objective = current_objective

        # A short annealed walk escapes single-coordinate local minima before
        # the next exact-cost descent.
        for walk in range(500):
            if time.monotonic() >= deadline or best_objective == 0:
                break
            index = rng.randrange(size)
            old = current[index]
            candidate = rng.randrange(len(pools[pairs[index]]))
            if candidate == old:
                continue
            delta = sum(
                cost_at(index, candidate, other, current[other])
                - cost_at(index, old, other, current[other])
                for other in range(size)
                if other != index
            )
            local_temperature = max(
                0.15,
                temperature * (1.0 - walk / 600.0),
            )
            if delta <= 0 or rng.random() < math.exp(
                -delta / local_temperature
            ):
                current[index] = candidate
                current_objective += delta
                if current_objective < best_objective:
                    best = list(current)
                    best_objective = current_objective
        restarts += 1

    selected = {pair: best[index] for index, pair in enumerate(pairs)}
    return "HEURISTIC", best_objective, None, selected


def feasibility_master_solve(
    pools: dict[tuple[int, int], list[tuple[int, ...]]],
    pairs: list[tuple[int, int]],
    *,
    seconds: float,
    workers: int,
    seed: int,
    previous: dict[tuple[int, int], int] | None,
    incumbent: int | None,
) -> tuple[str, int | None, int | None, dict[tuple[int, int], int]]:
    """Test zero-collision feasibility in the finite exact-row pool."""

    del incumbent
    model = cp_model.CpModel()
    selected = {}
    slots: dict[tuple[int, int], list] = collections.defaultdict(list)
    for pair in pairs:
        literals = []
        for candidate_index, phases in enumerate(pools[pair]):
            literal = model.NewBoolVar(
                f"row_{pair[0]}_{pair[1]}_{candidate_index}"
            )
            selected[pair, candidate_index] = literal
            literals.append(literal)
            for orbit, phase in enumerate(phases):
                slots[orbit, phase].append(literal)
            if previous is not None:
                model.AddHint(
                    literal,
                    int(previous[pair] == candidate_index),
                )
        model.AddExactlyOne(literals)
    for literals in slots.values():
        model.AddAtMostOne(literals)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.StatusName(status), None, None, {}
    answer = {}
    for pair in pairs:
        chosen = [
            candidate_index
            for candidate_index in range(len(pools[pair]))
            if solver.BooleanValue(selected[pair, candidate_index])
        ]
        if len(chosen) != 1:
            raise AssertionError("finite-pool feasibility chose wrong row count")
        answer[pair] = chosen[0]
    return solver.StatusName(status), 0, 0, answer


def pool_sha256(
    pools: dict[tuple[int, int], list[tuple[int, ...]]],
) -> str:
    payload = {
        f"{pair[0]},{pair[1]}": [list(row) for row in candidates]
        for pair, candidates in sorted(pools.items())
    }
    return hashlib.sha256(
        (
            json.dumps(payload, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
    ).hexdigest()


def load_pools(
    path: Path,
    pairs: list[tuple[int, int]],
) -> dict[tuple[int, int], list[tuple[int, ...]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = {f"{pair[0]},{pair[1]}" for pair in pairs}
    if set(payload) != expected:
        raise ValueError("pool file has the wrong star rows")
    answer = {}
    for pair in pairs:
        rows = payload[f"{pair[0]},{pair[1]}"]
        candidates = []
        for row in rows:
            candidate = tuple(row)
            if (
                len(candidate) != len(ORBITS)
                or not all(
                    isinstance(value, int) and 0 <= value < P
                    for value in candidate
                )
            ):
                raise ValueError(f"invalid pool row for {pair}")
            if candidate not in candidates:
                candidates.append(candidate)
        if not candidates:
            raise ValueError(f"empty pool for {pair}")
        answer[pair] = candidates
    return answer


def write_pools(
    path: Path,
    pools: dict[tuple[int, int], list[tuple[int, ...]]],
) -> str:
    payload = {
        f"{pair[0]},{pair[1]}": [
            list(candidate) for candidate in candidates
        ]
        for pair, candidates in sorted(pools.items())
    }
    encoded = (
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--centre", type=int, required=True)
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--pricing-attempts", type=int, default=2)
    parser.add_argument("--seconds-per-row", type=float, default=2.0)
    parser.add_argument("--master-seconds", type=float, default=30.0)
    parser.add_argument(
        "--master-method",
        choices=("cp-sat", "heuristic", "feasibility"),
        default="cp-sat",
        help=(
            "finite-pool master: proof-capable CP-SAT optimization or "
            "faster exact-cost heuristic witness search"
        ),
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--pricing-workers",
        type=int,
        default=4,
        help="parallel weighted Algorithm-X row solves",
    )
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--pool-source", type=Path)
    parser.add_argument("--pool-output", type=Path)
    parser.add_argument(
        "--extra-pool-source",
        type=Path,
        action="append",
        default=[],
        help="union candidates from another retained-row pool",
    )
    parser.add_argument(
        "--pairwise-certificate",
        type=Path,
        action="append",
        default=[],
        help=(
            "add exact rows from a verified centre-star pairwise "
            "compatibility certificate"
        ),
    )
    parser.add_argument(
        "--subset-certificate",
        type=Path,
        action="append",
        default=[],
        help=(
            "add exact rows from records with parallel outers and "
            "phase_rows arrays, such as the width-three certificate"
        ),
    )
    parser.add_argument(
        "--extra-source",
        type=Path,
        action="append",
        default=[],
        help="add the fourteen star rows from another exact 105-row state",
    )
    args = parser.parse_args()

    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    if args.centre not in FIXED:
        parser.error("--centre must lie in 0,...,14")

    rng = random.Random(args.seed)
    state = load_state(args.source)
    pairs = [
        incident_pair(args.centre, other)
        for other in FIXED
        if other != args.centre
    ]
    for pair in pairs:
        audit_row(state, pair)
    pools = (
        load_pools(args.pool_source, pairs)
        if args.pool_source is not None
        else {pair: [] for pair in pairs}
    )
    for extra_pool_path in args.extra_pool_source:
        extra_pools = load_pools(extra_pool_path, pairs)
        for pair in pairs:
            for candidate in extra_pools[pair]:
                if candidate not in pools[pair]:
                    pools[pair].append(candidate)
    for certificate_path in args.pairwise_certificate:
        certificate = json.loads(
            certificate_path.read_text(encoding="utf-8")
        )
        if certificate.get("centre") != args.centre:
            raise ValueError("pairwise certificate has the wrong centre")
        for record in certificate.get("records", []):
            for outer_key, phase_key in (
                ("outer_a", "phases_a"),
                ("outer_b", "phases_b"),
            ):
                pair = incident_pair(args.centre, record[outer_key])
                candidate = tuple(record[phase_key])
                if len(candidate) != len(ORBITS):
                    raise ValueError("invalid pairwise certificate row")
                old = state[pair]
                state[pair] = list(candidate)
                audit_row(state, pair)
                state[pair] = old
                if candidate not in pools[pair]:
                    pools[pair].append(candidate)
    for certificate_path in args.subset_certificate:
        certificate = json.loads(
            certificate_path.read_text(encoding="utf-8")
        )
        if certificate.get("centre") != args.centre:
            raise ValueError("subset certificate has the wrong centre")
        for record in certificate.get("records", []):
            outers = record.get("outers", [])
            phase_rows = record.get("phase_rows", [])
            if len(outers) != len(phase_rows) or not outers:
                raise ValueError("invalid subset certificate record")
            for outer, phases in zip(outers, phase_rows):
                pair = incident_pair(args.centre, outer)
                candidate = tuple(phases)
                if len(candidate) != len(ORBITS):
                    raise ValueError("invalid subset certificate row")
                old = state[pair]
                state[pair] = list(candidate)
                audit_row(state, pair)
                state[pair] = old
                if candidate not in pools[pair]:
                    pools[pair].append(candidate)
    for extra_path in args.extra_source:
        extra = load_state(extra_path)
        for pair in pairs:
            candidate = tuple(extra[pair])
            old = state[pair]
            state[pair] = list(candidate)
            audit_row(state, pair)
            state[pair] = old
            if candidate not in pools[pair]:
                pools[pair].append(candidate)
    selected = {}
    for pair in pairs:
        current = tuple(state[pair])
        if current not in pools[pair]:
            pools[pair].append(current)
        selected[pair] = pools[pair].index(current)
        for candidate in pools[pair]:
            old = state[pair]
            state[pair] = list(candidate)
            audit_row(state, pair)
            state[pair] = old
    distinct, collision_count, exact = centre_metrics(
        state, args.centre
    )
    print(
        json.dumps(
            {
                "status": "START",
                "centre": args.centre,
                "collision_pairs": collision_count,
                "distinct": distinct,
                "exact_groups": exact,
            },
            sort_keys=True,
        ),
        flush=True,
    )

    for iteration in range(args.iterations):
        additions = 0
        with ThreadPoolExecutor(
            max_workers=args.pricing_workers
        ) as executor:
            futures = {
                executor.submit(
                    solve_row,
                    args.binary,
                    state,
                    args.centre,
                    pair,
                    seconds=args.seconds_per_row,
                    nodes=1_000_000_000,
                    seed=rng.randrange(1, 2**63),
                ): pair
                for pair in pairs
                for _ in range(args.pricing_attempts)
            }
            for future in as_completed(futures):
                pair = futures[future]
                status, _, _, phases = future.result()
                if status != "SAT" or phases is None:
                    continue
                candidate = tuple(phases)
                old = state[pair]
                state[pair] = list(candidate)
                audit_row(state, pair)
                state[pair] = old
                if candidate not in pools[pair]:
                    pools[pair].append(candidate)
                    additions += 1

        master = (
            {
                "cp-sat": master_solve,
                "heuristic": heuristic_master_solve,
                "feasibility": feasibility_master_solve,
            }[args.master_method]
        )
        master_kwargs = {
            "seconds": args.master_seconds,
            "seed": rng.randrange(1, 2**31),
            "previous": selected,
            "incumbent": collision_count,
        }
        if args.master_method in ("cp-sat", "feasibility"):
            master_kwargs["workers"] = args.workers
        status, objective, bound, selected_candidate = master(
            pools,
            pairs,
            **master_kwargs,
        )
        if selected_candidate:
            selected = selected_candidate
            for pair in pairs:
                state[pair] = list(pools[pair][selected[pair]])
                audit_row(state, pair)
        distinct, collision_count, exact = centre_metrics(
            state, args.centre
        )
        if objective is not None and objective != collision_count:
            raise AssertionError("master objective disagrees with audit")
        sha = write_state(args.output, state)
        pool_file_sha = (
            write_pools(args.pool_output, pools)
            if args.pool_output is not None
            else ""
        )
        print(
            json.dumps(
                {
                    "status": "ITERATION",
                    "iteration": iteration,
                    "solver_status": status,
                    "master_objective": objective,
                    "master_bound": bound,
                    "pool_additions": additions,
                    "pool_rows": sum(map(len, pools.values())),
                    "pool_sha256": pool_sha256(pools),
                    **(
                        {"pool_file_sha256": pool_file_sha}
                        if pool_file_sha
                        else {}
                    ),
                    "collision_pairs": collision_count,
                    "distinct": distinct,
                    "exact_groups": exact,
                    "phase_sha256": sha,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if collision_count == 0:
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
                "collision_pairs": collision_count,
                "distinct": distinct,
                "exact_groups": exact,
                "pool_rows": sum(map(len, pools.values())),
                "pool_sha256": pool_sha256(pools),
                "phase_sha256": sha,
                "mathematical_status": "heuristic only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
