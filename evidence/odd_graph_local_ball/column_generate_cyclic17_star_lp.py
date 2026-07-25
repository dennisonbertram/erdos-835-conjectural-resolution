#!/usr/bin/env python3
"""Dual-price exact rows for the cyclic-17 centre-star set-packing LP.

Every generated column is an exact 40-triple row.  The LP objective and any
solver timeouts are diagnostic unless all fourteen weighted pricing problems
are proved optimal and the final dual is rationally certified.  In
particular, a finite-pool LP value below 14 is not itself a star obstruction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


P = 17
ORBITS = 40


def sorted_keys(payload) -> list[str]:
    return sorted(
        payload,
        key=lambda key: tuple(map(int, key.split(","))),
    )


def audit_pool(payload) -> list[str]:
    keys = sorted_keys(payload)
    if len(keys) != 14:
        raise ValueError("expected fourteen incident-pair pools")
    for key in keys:
        if not payload[key]:
            raise ValueError(f"empty pool {key}")
        unique = set()
        for candidate in payload[key]:
            row = tuple(candidate)
            if (
                len(row) != ORBITS
                or not all(
                    isinstance(phase, int) and 0 <= phase < P
                    for phase in row
                )
            ):
                raise ValueError(f"invalid row in pool {key}")
            if row in unique:
                raise ValueError(f"duplicate row in pool {key}")
            unique.add(row)
    return keys


def solve_pool_lp(payload, keys):
    rows = []
    columns = []
    data = []
    variable_meta = []
    variable = 0
    for label, key in enumerate(keys):
        for candidate_index, phases in enumerate(payload[key]):
            rows.append(label)
            columns.append(variable)
            data.append(1.0)
            for orbit, phase in enumerate(phases):
                rows.append(14 + orbit * P + phase)
                columns.append(variable)
                data.append(1.0)
            variable_meta.append((key, candidate_index))
            variable += 1
    constraint_count = 14 + ORBITS * P
    matrix = coo_matrix(
        (data, (rows, columns)),
        shape=(constraint_count, variable),
    ).tocsr()
    result = linprog(
        -np.ones(variable),
        A_ub=matrix,
        b_ub=np.ones(constraint_count),
        bounds=(0.0, None),
        method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    dual = -result.ineqlin.marginals
    slack = matrix.transpose().dot(dual) - 1.0
    if slack.min(initial=0.0) < -1e-7:
        raise AssertionError("floating pool dual is infeasible")
    return result, dual, variable_meta


def price_one(
    binary: Path,
    pair: str,
    portable_slot_dual,
    *,
    scale: int,
    seconds: float,
    seed: int,
    optimize: bool,
):
    # The exact-row binary indexes an actual translation shift.  Pool rows use
    # portable phase = -shift mod 17.
    weights = [
        str(
            int(
                round(
                    scale
                    * portable_slot_dual[orbit * P + ((-shift) % P)]
                )
            )
        )
        for orbit in range(ORBITS)
        for shift in range(P)
    ]
    with tempfile.NamedTemporaryFile(
        mode="w",
        prefix="cyclic17-star-lp-weights-",
        suffix=".txt",
        dir="/private/tmp",
        delete=True,
    ) as weight_file:
        weight_file.write(" ".join(weights))
        weight_file.write("\n")
        weight_file.flush()
        command = [
            str(binary),
            "--pair",
            pair,
            "--weights",
            weight_file.name,
            "--seconds",
            str(seconds),
            "--nodes",
            "1000000000",
            "--seed",
            str(seed),
        ]
        if optimize:
            command.append("--optimize-weight")
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    lines = [
        line
        for line in completed.stdout.splitlines()
        if line.strip().startswith("{")
    ]
    if not lines:
        raise RuntimeError(
            f"pricing {pair} produced no JSON: {completed.stderr}"
        )
    result = json.loads(lines[-1])
    if result.get("status") != "SAT":
        return pair, result, None
    phases = tuple((-shift) % P for shift in result["selected_shifts"])
    exact_float_weight = sum(
        portable_slot_dual[orbit * P + phase]
        for orbit, phase in enumerate(phases)
    )
    result["exact_float_slot_weight"] = float(exact_float_weight)
    return pair, result, phases


def write_pool(path: Path, payload) -> str:
    encoded = (
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("pool_source", type=Path)
    parser.add_argument("pool_output", type=Path)
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--seconds-per-price", type=float, default=5.0)
    parser.add_argument("--workers", type=int, default=7)
    parser.add_argument("--scale", type=int, default=1_000_000)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument(
        "--prove-prices",
        action="store_true",
        help=(
            "ask Algorithm X to prove each scaled-integer weight optimum; "
            "without this flag it stops at the first weight-guided exact row"
        ),
    )
    args = parser.parse_args()
    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    if args.scale <= 0:
        parser.error("--scale must be positive")

    payload = json.loads(args.pool_source.read_text(encoding="utf-8"))
    keys = audit_pool(payload)
    rng = random.Random(args.seed)
    for iteration in range(args.iterations):
        result, dual, _ = solve_pool_lp(payload, keys)
        label_dual = dual[:14]
        slot_dual = dual[14:]
        priced = []
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = [
                executor.submit(
                    price_one,
                    args.binary,
                    key,
                    slot_dual,
                    scale=args.scale,
                    seconds=args.seconds_per_price,
                    seed=rng.randrange(1, 2**63),
                    optimize=args.prove_prices,
                )
                for key in keys
            ]
            for future in as_completed(futures):
                priced.append(future.result())

        additions = 0
        violations = 0
        all_optimal = True
        price_summary = {}
        for pair, price_result, phases in priced:
            label = keys.index(pair)
            all_optimal &= bool(price_result.get("optimal"))
            if phases is None:
                price_summary[pair] = {
                    "status": price_result.get("status"),
                }
                continue
            reduced_left = (
                float(label_dual[label])
                + price_result["exact_float_slot_weight"]
            )
            if reduced_left < 1.0 - 1e-8:
                violations += 1
            candidate = list(phases)
            if candidate not in payload[pair]:
                payload[pair].append(candidate)
                additions += 1
            price_summary[pair] = {
                "dual_left": reduced_left,
                "optimal_integer_pricing": bool(
                    price_result.get("optimal")
                ),
                "timed_out": bool(price_result.get("timed_out")),
                "new": candidate == payload[pair][-1],
            }
        sha = write_pool(args.pool_output, payload)
        print(
            json.dumps(
                {
                    "status": "ITERATION",
                    "iteration": iteration,
                    "finite_pool_lp": float(-result.fun),
                    "columns": sum(len(payload[key]) for key in keys),
                    "additions": additions,
                    "violated_float_prices": violations,
                    "all_integer_prices_optimal": all_optimal,
                    "pool_sha256": sha,
                    "prices": price_summary,
                    "scope": (
                        "heuristic column generation unless all prices and "
                        "the final rational dual are certified"
                    ),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if additions == 0:
            break


if __name__ == "__main__":
    main()
