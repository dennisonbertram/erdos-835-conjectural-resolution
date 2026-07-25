#!/usr/bin/env python3
"""Generate collision-free certificates for all two-row centre-star systems.

For each pair of outer rows at one fixed centre, keep one independently exact
row from the source and solve the other weighted residual exact-cover problem
with unit cost on matching phases.  Cost zero is a concrete collision-free
two-row witness and needs no optimality claim.

Completing all 91 pairs only rules out a two-row obstruction.  The witnesses
may use different row decompositions for different pairs, so this does not
glue fourteen rows, prove a star, or solve Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations
from pathlib import Path


P = 17
ORBITS = 40
OUTERS = tuple(range(1, 15))


def load_source(path: Path) -> dict[tuple[int, int], list[int]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    answer = {}
    for key, phases in payload.items():
        first, second = map(int, key.split(","))
        if (
            not isinstance(phases, list)
            or len(phases) != ORBITS
            or not all(
                isinstance(value, int) and 0 <= value < P
                for value in phases
            )
        ):
            raise ValueError(f"invalid source row {key}")
        answer[first, second] = phases
    expected = {
        (first, second)
        for first in range(15)
        for second in range(first + 1, 15)
    }
    if set(answer) != expected:
        raise ValueError("source does not contain all 105 rows")
    return answer


def solve_against(
    binary: Path,
    fixed_portable,
    centre: int,
    fixed_outer: int,
    solved_outer: int,
    *,
    seconds: float,
    nodes: int,
    seed: int,
) -> dict[str, object] | None:
    solved_pair = tuple(sorted((centre, solved_outer)))
    fixed_shifts = [(-phase) % P for phase in fixed_portable]
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="cyclic17-pairwise-",
        suffix=".weights",
    ) as stream:
        for orbit in range(ORBITS):
            stream.write(
                " ".join(
                    str(int(shift == fixed_shifts[orbit]))
                    for shift in range(P)
                )
                + "\n"
            )
        stream.flush()
        completed = subprocess.run(
            [
                str(binary),
                "--pair",
                f"{solved_pair[0]},{solved_pair[1]}",
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
        return None
    result = json.loads(completed.stdout)
    if result.get("status") != "SAT" or result.get("weight") != 0:
        return None
    selected_shifts = result.get("selected_shifts")
    if (
        not isinstance(selected_shifts, list)
        or len(selected_shifts) != ORBITS
        or not all(
            isinstance(value, int) and 0 <= value < P
            for value in selected_shifts
        )
    ):
        raise ValueError("row solver returned invalid shifts")
    solved_portable = [(-shift) % P for shift in selected_shifts]
    if any(
        left == right
        for left, right in zip(fixed_portable, solved_portable)
    ):
        raise AssertionError("reported zero-cost rows collide")
    return {
        "outer_a": fixed_outer,
        "outer_b": solved_outer,
        "phases_a": fixed_portable,
        "phases_b": solved_portable,
        "solver_optimal": bool(result.get("optimal")),
        "solver_timed_out": bool(result.get("timed_out")),
        "collision_count": 0,
        "source": "weighted_exact_row_solver",
    }


def load_pool(path: Path, centre: int):
    payload = json.loads(path.read_text(encoding="utf-8"))
    answer = {}
    for outer in OUTERS:
        key = f"{min(centre, outer)},{max(centre, outer)}"
        rows = payload.get(key)
        if not isinstance(rows, list):
            raise ValueError(f"pool omits {key}")
        candidates = []
        for row in rows:
            candidate = tuple(row)
            if (
                len(candidate) != ORBITS
                or not all(
                    isinstance(value, int) and 0 <= value < P
                    for value in candidate
                )
            ):
                raise ValueError(f"invalid pool row for {key}")
            if candidate not in candidates:
                candidates.append(candidate)
        answer[outer] = candidates
    return answer


def pool_record(first, second, phases_first, phases_second):
    return {
        "outer_a": first,
        "outer_b": second,
        "phases_a": list(phases_first),
        "phases_b": list(phases_second),
        "solver_optimal": False,
        "solver_timed_out": False,
        "collision_count": 0,
        "source": "existing_exact_row_pool",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--centre", type=int, default=0)
    parser.add_argument("--seconds", type=float, default=5.0)
    parser.add_argument("--nodes", type=int, default=1_000_000_000)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument(
        "--pool-source",
        type=Path,
        help="optional exact-row pools used before weighted pricing",
    )
    args = parser.parse_args()
    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    if args.centre != 0:
        parser.error("the current portable certificate schema fixes centre 0")

    source_bytes = args.source.read_bytes()
    source = load_source(args.source)
    candidates = {
        outer: [tuple(source[tuple(sorted((args.centre, outer)))])]
        for outer in OUTERS
    }
    if args.pool_source is not None:
        pool = load_pool(args.pool_source, args.centre)
        for outer in OUTERS:
            for candidate in pool[outer]:
                if candidate not in candidates[outer]:
                    candidates[outer].append(candidate)

    def solve_pair(outers):
        first, second = outers
        for first_row in candidates[first]:
            for second_row in candidates[second]:
                if all(
                    left != right
                    for left, right in zip(first_row, second_row)
                ):
                    return outers, pool_record(
                        first,
                        second,
                        first_row,
                        second_row,
                    )
        local_rng = random.Random(
            args.seed * 10_000 + first * 100 + second
        )
        orientations = (
            (first, second),
            (second, first),
        )
        for attempt in range(args.attempts):
            for fixed, solved in orientations:
                for fixed_row in candidates[fixed]:
                    result = solve_against(
                        args.binary,
                        fixed_row,
                        args.centre,
                        fixed,
                        solved,
                        seconds=args.seconds,
                        nodes=args.nodes,
                        seed=local_rng.randrange(1, 2**63),
                    )
                    if result is not None:
                        return outers, result
        return outers, None

    records = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(solve_pair, outers)
            for outers in combinations(OUTERS, 2)
        ]
        for future in as_completed(futures):
            outers, result = future.result()
            if result is not None:
                records[outers] = result
            print(
                json.dumps(
                    {
                        "status": (
                            "PAIR_WITNESS"
                            if result is not None
                            else "PAIR_UNRESOLVED"
                        ),
                        "outers": list(outers),
                        "completed": len(records),
                        "target": 91,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    payload = {
        "schema": "cyclic17-centre0-pairwise-compatibility-v1",
        "centre": args.centre,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "records": [
            records[outers]
            for outers in combinations(OUTERS, 2)
            if outers in records
        ],
        "resolved_pairs": len(records),
        "target_pairs": 91,
        "scope": "all two-row subsystems only; no 14-row star claim",
    }
    encoded = (
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    args.output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "status": (
                    "COMPLETE_PAIRWISE_CERTIFICATE"
                    if len(records) == 91
                    else "INCOMPLETE_PAIRWISE_SEARCH"
                ),
                "resolved_pairs": len(records),
                "target_pairs": 91,
                "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
                "scope": "two-row subsystems only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
