#!/usr/bin/env python3
"""Alternate the two exact constraint families of one cyclic-17 star.

The row projection solves the fourteen prescribed-link triangle decompositions
independently with weighted Algorithm X.  The cross projection solves each of
the forty centre/orbit groups as a minimum-Hamming list-constrained perfect
matching.  Both projected states are exact for their own family.

This is only a witness heuristic.  A nonzero Hamming gap proves nothing.
Equality, after independent verification, is a one-star witness and still not
the full radius-five layer or ER #835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from improve_radius5_golf_cyclic_slice_lns import (
    State,
    domains_for_seed,
    dump_phases,
    load_state,
    slice_scores,
)
from search_radius5_golf_cyclic_alternating_projection import (
    project_one_row,
)
from search_radius5_golf_cyclic_compact import (
    P,
    REPRESENTATIVES,
    SQUARES,
)


def incident_pair(first: int, second: int) -> tuple[int, int]:
    return min(first, second), max(first, second)


def star_pairs(centre: int) -> list[tuple[int, int]]:
    return [
        incident_pair(centre, other)
        for other in SQUARES
        if other != centre
    ]


def star_metrics(
    state: State,
    centre: int,
) -> tuple[int, int, int]:
    distinct = 0
    collisions = 0
    exact = 0
    pairs = star_pairs(centre)
    for orbit in range(len(REPRESENTATIVES)):
        counts = {}
        for pair in pairs:
            value = state[pair + (orbit,)]
            counts[value] = counts.get(value, 0) + 1
        distinct += len(counts)
        collisions += sum(
            multiplicity * (multiplicity - 1) // 2
            for multiplicity in counts.values()
        )
        exact += len(counts) == len(pairs)
    return distinct, collisions, exact


def star_hamming(
    left: State,
    right: State,
    centre: int,
) -> int:
    return sum(
        left[pair + (orbit,)] != right[pair + (orbit,)]
        for pair in star_pairs(centre)
        for orbit in range(len(REPRESENTATIVES))
    )


def write_state(path: Path, state: State) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def state_sha256(state: State) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def project_star_rows(
    binary: Path,
    target: State,
    fallback: State,
    centre: int,
    *,
    seconds: float,
    nodes: int,
    workers: int,
    seed: int,
) -> tuple[State, dict[str, int]]:
    rng = random.Random(seed)
    answer = dict(fallback)
    reports = []
    pairs = star_pairs(centre)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                project_one_row,
                binary,
                target,
                fallback,
                pair,
                seconds=seconds,
                nodes=nodes,
                seed=rng.randrange(1, 2**63),
            )
            for pair in pairs
        ]
        for future in as_completed(futures):
            pair, shifts, report = future.result()
            reports.append(report)
            for orbit, shift in enumerate(shifts):
                answer[pair + (orbit,)] = shift
    scores = slice_scores(answer)
    if any(scores[pair] != 120 for pair in pairs):
        raise AssertionError("star row projection produced an inexact row")
    return answer, {
        "hamming_to_target": star_hamming(answer, target, centre),
        "optimal_subproblems": sum(
            bool(report.get("optimal")) for report in reports
        ),
        "timed_out_subproblems": sum(
            bool(report.get("timed_out")) for report in reports
        ),
        "fallback_subproblems": sum(
            bool(report.get("used_fallback")) for report in reports
        ),
        "total_nodes": sum(int(report.get("nodes", 0)) for report in reports),
    }


def project_one_cross_group(
    target: State,
    domains,
    centre: int,
    orbit: int,
    *,
    rng: random.Random,
) -> dict[tuple[int, int], int]:
    pairs = star_pairs(centre)
    centre_allowed = sorted(
        set().union(
            *(domains[pair + (orbit,)] for pair in pairs)
        )
    )
    if len(centre_allowed) != len(pairs):
        raise AssertionError("wrong centre phase universe")
    phase_bit = {
        phase: 1 << index
        for index, phase in enumerate(centre_allowed)
    }

    # DP states map used phase masks to (Hamming cost, predecessor).
    layers: list[dict[int, tuple[int, int, int]]] = [{0: (0, -1, -1)}]
    for row_index, pair in enumerate(pairs):
        previous = layers[-1]
        current: dict[int, tuple[int, int, int]] = {}
        candidates = list(domains[pair + (orbit,)])
        rng.shuffle(candidates)
        candidates.sort(
            key=lambda phase: phase != target[pair + (orbit,)]
        )
        for mask, (cost, _, _) in previous.items():
            for phase in candidates:
                bit = phase_bit.get(phase)
                if bit is None or mask & bit:
                    continue
                next_mask = mask | bit
                next_cost = cost + (
                    phase != target[pair + (orbit,)]
                )
                old = current.get(next_mask)
                if old is None or next_cost < old[0]:
                    current[next_mask] = (next_cost, mask, phase)
        if not current:
            raise AssertionError(
                f"cross projection failed at row {row_index}"
            )
        layers.append(current)

    mask = (1 << len(centre_allowed)) - 1
    answer = {}
    for row_index in range(len(pairs), 0, -1):
        _, previous_mask, phase = layers[row_index][mask]
        answer[pairs[row_index - 1]] = phase
        mask = previous_mask
    return answer


def project_star_cross(
    target: State,
    domains,
    centre: int,
    *,
    seed: int,
) -> tuple[State, dict[str, int]]:
    rng = random.Random(seed)
    answer = dict(target)
    for orbit in range(len(REPRESENTATIVES)):
        assignment = project_one_cross_group(
            target,
            domains,
            centre,
            orbit,
            rng=rng,
        )
        for pair, phase in assignment.items():
            answer[pair + (orbit,)] = phase
    _, collisions, exact = star_metrics(answer, centre)
    if collisions != 0 or exact != len(REPRESENTATIVES):
        raise AssertionError("cross projection is not star exact")
    return answer, {
        "hamming_to_target": star_hamming(answer, target, centre)
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("cross_seed", type=Path)
    parser.add_argument("--row-fallback", type=Path, required=True)
    parser.add_argument("--centre", type=int, required=True)
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--row-seconds", type=float, default=3.0)
    parser.add_argument("--row-nodes", type=int, default=1_000_000_000)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--row-output", type=Path)
    parser.add_argument("--cross-output", type=Path)
    args = parser.parse_args()

    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    if args.centre not in SQUARES:
        parser.error("--centre must lie in 0,...,14")
    rng = random.Random(args.seed)
    domains = domains_for_seed(construct_golf17())
    cross = load_state(args.cross_seed)
    fallback = load_state(args.row_fallback)
    if any(
        slice_scores(fallback)[pair] != 120
        for pair in star_pairs(args.centre)
    ):
        raise ValueError("row fallback has an inexact star row")
    _, cross_collisions, cross_exact = star_metrics(
        cross, args.centre
    )
    if cross_collisions != 0 or cross_exact != 40:
        cross, _ = project_star_cross(
            cross,
            domains,
            args.centre,
            seed=rng.randrange(1, 2**63),
        )

    seen = set()
    for iteration in range(args.iterations):
        rows, row_report = project_star_rows(
            args.binary,
            cross,
            fallback,
            args.centre,
            seconds=args.row_seconds,
            nodes=args.row_nodes,
            workers=args.workers,
            seed=rng.randrange(1, 2**63),
        )
        row_sha = (
            write_state(args.row_output, rows)
            if args.row_output is not None
            else ""
        )
        cross, cross_report = project_star_cross(
            rows,
            domains,
            args.centre,
            seed=rng.randrange(1, 2**63),
        )
        cross_sha = (
            write_state(args.cross_output, cross)
            if args.cross_output is not None
            else ""
        )
        gap = star_hamming(rows, cross, args.centre)
        _, row_collisions, row_exact = star_metrics(
            rows, args.centre
        )
        fingerprint = tuple(
            rows[pair + (orbit,)]
            for pair in star_pairs(args.centre)
            for orbit in range(len(REPRESENTATIVES))
        )
        cycled = fingerprint in seen
        seen.add(fingerprint)
        print(
            json.dumps(
                {
                    "status": "ITERATION",
                    "iteration": iteration,
                    "row_cross_hamming": gap,
                    "row_collision_pairs": row_collisions,
                    "row_exact_cross_groups": row_exact,
                    "row_projection": row_report,
                    "cross_projection": cross_report,
                    **({"row_phase_sha256": row_sha} if row_sha else {}),
                    **(
                        {"cross_phase_sha256": cross_sha}
                        if cross_sha
                        else {}
                    ),
                    "cycled": cycled,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if gap == 0:
            sha = (
                write_state(args.row_output, rows)
                if args.row_output is not None
                else state_sha256(rows)
            )
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
        fallback = rows
    print(
        json.dumps(
            {
                "status": "NO_STAR_WITNESS",
                "centre": args.centre,
                "final_hamming_gap": star_hamming(
                    fallback, cross, args.centre
                ),
                "mathematical_status": "heuristic only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
