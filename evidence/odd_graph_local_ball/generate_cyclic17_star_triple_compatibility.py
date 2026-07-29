#!/usr/bin/env python3
"""Generate exact compatibility certificates for all 364 outer triples.

Candidate exact rows are retained from the complete two-row certificate (and
optionally another row pool).  If a triple is not already represented by
three pairwise-disjoint retained rows, two disjoint rows are fixed and the
third residual exact-cover problem is solved with collision weight.

A zero-weight result is a concrete three-row witness even if optimization
times out.  Completing all triples rules out obstructions supported on at
most three outer rows; it does not glue fourteen rows, prove a star, or solve
Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


P = 17
ORBITS = 40
OUTERS = tuple(range(1, 15))


def disjoint(first, second) -> bool:
    return all(left != right for left, right in zip(first, second))


def load_pair_certificate(path: Path):
    encoded = path.read_bytes()
    payload = json.loads(encoded)
    if payload.get("schema") != (
        "cyclic17-centre0-pairwise-compatibility-v1"
    ):
        raise ValueError("wrong pair-certificate schema")
    if payload.get("resolved_pairs") != 91:
        raise ValueError("pair certificate is incomplete")
    pools = {outer: [] for outer in OUTERS}
    pair_rows = {}
    for record in payload["records"]:
        first = record["outer_a"]
        second = record["outer_b"]
        first_row = tuple(record["phases_a"])
        second_row = tuple(record["phases_b"])
        pair_rows[tuple(sorted((first, second)))] = {
            first: first_row,
            second: second_row,
        }
        for outer, row in ((first, first_row), (second, second_row)):
            if row not in pools[outer]:
                pools[outer].append(row)
    return encoded, pools, pair_rows


def merge_pool(path: Path, pools) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    for outer in OUTERS:
        key = f"0,{outer}"
        rows = payload.get(key)
        if not isinstance(rows, list):
            raise ValueError(f"pool omits {key}")
        for raw in rows:
            row = tuple(raw)
            if (
                len(row) != ORBITS
                or not all(
                    isinstance(value, int) and 0 <= value < P
                    for value in row
                )
            ):
                raise ValueError(f"invalid pool row for {key}")
            if row not in pools[outer]:
                pools[outer].append(row)


def record_for_rows(triple, rows, source):
    return {
        "outers": list(triple),
        "phase_rows": [list(rows[outer]) for outer in triple],
        "collision_count": 0,
        "source": source,
    }


def solve_third(
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
        prefix="cyclic17-triple-",
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
        return None
    result = json.loads(completed.stdout)
    if result.get("status") != "SAT" or result.get("weight") != 0:
        return None
    selected = result.get("selected_shifts")
    if (
        not isinstance(selected, list)
        or len(selected) != ORBITS
        or not all(
            isinstance(value, int) and 0 <= value < P
            for value in selected
        )
    ):
        raise ValueError("third-row solver returned invalid shifts")
    portable = tuple((-shift) % P for shift in selected)
    if any(not disjoint(portable, row) for row in base_rows):
        raise AssertionError("zero-cost third row has a collision")
    return portable


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("pair_certificate", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--pool-source", type=Path)
    parser.add_argument("--seconds", type=float, default=3.0)
    parser.add_argument("--nodes", type=int, default=1_000_000_000)
    parser.add_argument("--base-limit", type=int, default=3)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()
    if not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    if args.base_limit <= 0:
        parser.error("--base-limit must be positive")

    pair_bytes, pools, pair_rows = load_pair_certificate(
        args.pair_certificate
    )
    if args.pool_source is not None:
        merge_pool(args.pool_source, pools)

    def solve_triple(triple):
        # First use the retained master with no new row solve.
        for raw_rows in itertools.product(
            *(pools[outer] for outer in triple)
        ):
            if all(
                disjoint(raw_rows[left], raw_rows[right])
                for left, right in itertools.combinations(range(3), 2)
            ):
                rows = dict(zip(triple, raw_rows))
                return triple, record_for_rows(
                    triple, rows, "retained_exact_row_pool"
                )

        bases = []
        for solved_outer in triple:
            first, second = (
                outer for outer in triple if outer != solved_outer
            )
            preferred = pair_rows[tuple(sorted((first, second)))]
            bases.append(
                (
                    solved_outer,
                    preferred[first],
                    preferred[second],
                )
            )
            for first_row in pools[first]:
                for second_row in pools[second]:
                    if disjoint(first_row, second_row):
                        candidate = (
                            solved_outer,
                            first_row,
                            second_row,
                        )
                        if candidate not in bases:
                            bases.append(candidate)
        local_rng = random.Random(
            args.seed * 1_000_000
            + triple[0] * 10_000
            + triple[1] * 100
            + triple[2]
        )
        preferred_bases = bases[:3]
        remaining = bases[3:]
        local_rng.shuffle(remaining)
        bases = (preferred_bases + remaining)[: args.base_limit]
        for solved_outer, first_row, second_row in bases:
            third_row = solve_third(
                args.binary,
                solved_outer,
                (first_row, second_row),
                seconds=args.seconds,
                nodes=args.nodes,
                seed=local_rng.randrange(1, 2**63),
            )
            if third_row is None:
                continue
            fixed_outers = [
                outer for outer in triple if outer != solved_outer
            ]
            rows = {
                fixed_outers[0]: first_row,
                fixed_outers[1]: second_row,
                solved_outer: third_row,
            }
            return triple, record_for_rows(
                triple, rows, "weighted_exact_row_solver"
            )
        return triple, None

    records = {}
    triples = tuple(itertools.combinations(OUTERS, 3))
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(solve_triple, triple)
            for triple in triples
        ]
        for future in as_completed(futures):
            triple, record = future.result()
            if record is not None:
                records[triple] = record
            print(
                json.dumps(
                    {
                        "status": (
                            "TRIPLE_WITNESS"
                            if record is not None
                            else "TRIPLE_UNKNOWN"
                        ),
                        "outers": list(triple),
                        "completed": len(records),
                        "target": len(triples),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    payload = {
        "schema": "cyclic17-centre0-triple-compatibility-v1",
        "centre": 0,
        "pair_certificate_sha256": hashlib.sha256(
            pair_bytes
        ).hexdigest(),
        "records": [
            records[triple] for triple in triples if triple in records
        ],
        "resolved_triples": len(records),
        "target_triples": len(triples),
        "unknown_triples": [
            list(triple) for triple in triples if triple not in records
        ],
        "scope": "three-row subsystems only; no fourteen-row star claim",
    }
    encoded = (
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    args.output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "status": (
                    "COMPLETE_TRIPLE_CERTIFICATE"
                    if len(records) == len(triples)
                    else "INCOMPLETE_TRIPLE_SEARCH"
                ),
                "resolved_triples": len(records),
                "target_triples": len(triples),
                "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
                "scope": "three-row subsystems only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
