#!/usr/bin/env python3
"""Generate 105 independently exact cyclic prescribed-link slices.

The companion C++ Algorithm-X binary is run once for each golf-square pair.
Each successful result chooses one translate from every moving-triple orbit
and exactly decomposes that pair's residual K_17 graph.  The output uses the
phase convention expected by the joint cyclic search scripts.

The 105 solves are independent.  Therefore the resulting file is a row-exact
search seed, not a radius-five certificate: its orbit-wise K_15 edge colours
will generally conflict and must be repaired before the shared-N condition
holds.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
from itertools import combinations
from pathlib import Path


P = 17
PAIRS = tuple(combinations(range(15), 2))


def solve_pair(
    binary: Path,
    pair: tuple[int, int],
    *,
    seconds: float,
    nodes: int,
    retries: int,
    seed: int,
) -> tuple[tuple[int, int], list[int], dict[str, object]]:
    i, j = pair
    last = None
    for attempt in range(retries):
        command = [
            str(binary),
            "--pair",
            f"{i},{j}",
            "--seconds",
            str(seconds),
            "--nodes",
            str(nodes),
            "--seed",
            str(seed + 1_000_003 * attempt),
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        if not completed.stdout.strip():
            raise RuntimeError(
                f"slice solver produced no output for {i},{j}: "
                f"{completed.stderr}"
            )
        last = json.loads(completed.stdout)
        if last.get("status") != "SAT":
            continue
        shifts = last.get("selected_shifts")
        if (
            not isinstance(shifts, list)
            or len(shifts) != 40
            or not all(
                isinstance(shift, int) and 0 <= shift < P
                for shift in shifts
            )
        ):
            raise ValueError(f"invalid solver payload for {i},{j}")
        phases = [(-shift) % P for shift in shifts]
        return pair, phases, last
    raise RuntimeError(
        f"no exact slice found for {i},{j} after {retries} attempts; "
        f"last result={last}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seconds", type=float, default=30.0)
    parser.add_argument("--nodes", type=int, default=1_000_000_000)
    parser.add_argument("--retries", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()

    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    phases: dict[str, list[int]] = {}
    statistics: dict[str, dict[str, object]] = {}
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.workers
    ) as executor:
        futures = {
            executor.submit(
                solve_pair,
                args.binary,
                pair,
                seconds=args.seconds,
                nodes=args.nodes,
                retries=args.retries,
                seed=args.seed + 10_007 * index,
            ): pair
            for index, pair in enumerate(PAIRS)
        }
        completed_count = 0
        for future in concurrent.futures.as_completed(futures):
            pair, pair_phases, stats = future.result()
            key = f"{pair[0]},{pair[1]}"
            phases[key] = pair_phases
            statistics[key] = {
                field: stats[field]
                for field in ("rows", "nodes", "seconds", "status")
            }
            completed_count += 1
            print(
                json.dumps(
                    {
                        "status": "SLICE",
                        "pair": list(pair),
                        "completed": completed_count,
                        "total": len(PAIRS),
                        "nodes": stats["nodes"],
                        "seconds": stats["seconds"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    if set(phases) != {f"{i},{j}" for i, j in PAIRS}:
        raise AssertionError("generator did not complete every fixed pair")
    args.output.write_text(
        json.dumps(phases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "DONE",
                "slices": len(phases),
                "scope": (
                    "105 independently exact slices; shared-N constraints "
                    "not claimed"
                ),
                "total_nodes": sum(
                    int(stats["nodes"]) for stats in statistics.values()
                ),
                "total_solver_seconds": sum(
                    float(stats["seconds"]) for stats in statistics.values()
                ),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
