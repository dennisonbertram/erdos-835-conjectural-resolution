#!/usr/bin/env python3
"""Generate centre-0 compatibility witnesses for all 1,001 outer quadruples.

Rows retained by the complete width-three certificate (and optional exact-row
pool files) are viewed as vertices of a fourteen-partite compatibility graph.
Two rows are adjacent exactly when their forty phase slots are disjoint.  A
deterministic bitset backtracker searches for one four-clique for every outer
quadruple.

Every emitted record is a concrete witness, but this generator deliberately
does not make a theorem from a missing retained-pool clique.  Missing
quadruples are recorded as UNKNOWN.  Even a complete width-four certificate
concerns only the centre-0 necessary star of one fixed-Wallis cyclic ansatz;
it is not a fourteen-row star or a solution of Erdos--Rosenfeld problem 835.
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


def checked_row(raw, *, context: str) -> tuple[int, ...]:
    row = tuple(raw)
    if (
        len(row) != ORBITS
        or not all(
            isinstance(value, int) and 0 <= value < P
            for value in row
        )
    ):
        raise ValueError(f"invalid phase row in {context}")
    return row


def add_row(pools, outer: int, raw, *, context: str) -> None:
    if outer not in pools:
        raise ValueError(f"invalid outer {outer} in {context}")
    row = checked_row(raw, context=context)
    if row not in pools[outer]:
        pools[outer].append(row)


def load_width_three(path: Path, pools) -> bytes:
    encoded = path.read_bytes()
    payload = json.loads(encoded)
    if payload.get("schema") != (
        "cyclic17-centre0-triple-compatibility-v1"
    ):
        raise ValueError("wrong width-three certificate schema")
    if payload.get("centre") != 0:
        raise ValueError("width-three certificate has wrong centre")
    if payload.get("resolved_triples") != 364:
        raise ValueError("width-three certificate is incomplete")
    records = payload.get("records", [])
    if len(records) != 364:
        raise ValueError("width-three record count is not 364")
    witnesses = {}
    for record_index, record in enumerate(records):
        outers = record.get("outers", [])
        rows = record.get("phase_rows", [])
        if len(outers) != 3 or len(rows) != 3:
            raise ValueError("malformed width-three record")
        triple = tuple(outers)
        witnesses[triple] = {}
        for outer, row in zip(outers, rows):
            add_row(
                pools,
                outer,
                row,
                context=f"width-three record {record_index}",
            )
            witnesses[triple][outer] = checked_row(
                row,
                context=f"width-three record {record_index}",
            )
    if set(witnesses) != set(itertools.combinations(OUTERS, 3)):
        raise ValueError("width-three records do not cover all triples")
    return encoded, witnesses


def merge_pool(path: Path, pools) -> bytes:
    encoded = path.read_bytes()
    payload = json.loads(encoded)
    expected = {f"0,{outer}" for outer in OUTERS}
    if set(payload) != expected:
        raise ValueError(f"row pool {path} has the wrong keys")
    for outer in OUTERS:
        rows = payload[f"0,{outer}"]
        if not isinstance(rows, list):
            raise ValueError(f"row pool {path} omits outer {outer}")
        for row_index, row in enumerate(rows):
            add_row(
                pools,
                outer,
                row,
                context=f"{path} outer {outer} row {row_index}",
            )
    return encoded


def disjoint(first, second) -> bool:
    return all(left != right for left, right in zip(first, second))


def compatibility_masks(pools):
    masks = {}
    for left, right in itertools.combinations(OUTERS, 2):
        left_to_right = []
        right_to_left = [0] * len(pools[right])
        for left_index, left_row in enumerate(pools[left]):
            mask = 0
            for right_index, right_row in enumerate(pools[right]):
                if disjoint(left_row, right_row):
                    mask |= 1 << right_index
                    right_to_left[right_index] |= 1 << left_index
            left_to_right.append(mask)
        masks[left, right] = left_to_right
        masks[right, left] = right_to_left
    return masks


def iter_bits(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def popcount(mask: int) -> int:
    return bin(mask).count("1")


def find_cliques(subset, pools, masks, *, limit: int):
    available = {
        outer: (1 << len(pools[outer])) - 1
        for outer in subset
    }
    answers = []

    def recurse(remaining, candidates, selected):
        if len(answers) >= limit:
            return
        if not remaining:
            answers.append(dict(selected))
            return
        outer = min(
            remaining,
            key=lambda value: (
                popcount(candidates[value]),
                value,
            ),
        )
        candidate_mask = candidates[outer]
        if candidate_mask == 0:
            return
        next_remaining = tuple(
            value for value in remaining if value != outer
        )
        for row_index in iter_bits(candidate_mask):
            if len(answers) >= limit:
                return
            next_candidates = {}
            possible = True
            for other in next_remaining:
                allowed = (
                    candidates[other]
                    & masks[outer, other][row_index]
                )
                if allowed == 0:
                    possible = False
                    break
                next_candidates[other] = allowed
            if not possible:
                continue
            selected[outer] = row_index
            recurse(
                next_remaining,
                next_candidates,
                selected,
            )
            del selected[outer]

    recurse(tuple(subset), available, {})
    return answers


def find_clique(subset, pools, masks):
    answers = find_cliques(subset, pools, masks, limit=1)
    return answers[0] if answers else None


def solve_against_base(
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
        prefix="cyclic17-quadruple-",
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
        raise ValueError("row solver returned invalid shifts")
    portable = tuple((-shift) % P for shift in selected)
    if any(not disjoint(portable, row) for row in base_rows):
        raise AssertionError("zero-weight row has a collision")
    return portable


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("width_three_certificate", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--pool-source",
        type=Path,
        action="append",
        default=[],
        help="merge another retained exact-row pool",
    )
    parser.add_argument(
        "--binary",
        type=Path,
        help=(
            "weighted exact-row solver used to extend retained "
            "three-cliques"
        ),
    )
    parser.add_argument("--seconds", type=float, default=3.0)
    parser.add_argument("--nodes", type=int, default=1_000_000_000)
    parser.add_argument(
        "--base-limit",
        type=int,
        default=3,
        help="retained base triples tried per omitted outer",
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()
    if args.binary is not None and not args.binary.is_file():
        raise FileNotFoundError(args.binary)
    if args.base_limit <= 0:
        parser.error("--base-limit must be positive")

    pools = {outer: [] for outer in OUTERS}
    width_three_bytes, triple_witnesses = load_width_three(
        args.width_three_certificate,
        pools,
    )
    pool_hashes = []
    for path in args.pool_source:
        pool_bytes = merge_pool(path, pools)
        pool_hashes.append(
            {
                "path_name": path.name,
                "sha256": hashlib.sha256(pool_bytes).hexdigest(),
            }
        )
    if any(not pools[outer] for outer in OUTERS):
        raise ValueError("one or more outer-row pools are empty")

    masks = compatibility_masks(pools)
    quadruples = tuple(itertools.combinations(OUTERS, 4))
    records = {}
    unknown = []
    for completed, quadruple in enumerate(quadruples, start=1):
        selected = find_clique(quadruple, pools, masks)
        if selected is None:
            unknown.append(list(quadruple))
            status = "QUADRUPLE_UNKNOWN"
        else:
            rows = [
                pools[outer][selected[outer]]
                for outer in quadruple
            ]
            if not all(
                disjoint(rows[left], rows[right])
                for left, right in itertools.combinations(range(4), 2)
            ):
                raise AssertionError("backtracker returned a collision")
            records[quadruple] = {
                "outers": list(quadruple),
                "phase_rows": [list(row) for row in rows],
                "collision_count": 0,
                "source": "retained_exact_row_pool",
            }
            status = "QUADRUPLE_WITNESS"
        print(
            json.dumps(
                {
                    "status": status,
                    "outers": list(quadruple),
                    "completed": completed,
                    "resolved": len(records),
                    "target": len(quadruples),
                },
                sort_keys=True,
            ),
            flush=True,
        )

    if args.binary is not None and unknown:
        def solve_quadruple(quadruple):
            local_rng = random.Random(
                args.seed * 100_000_000
                + quadruple[0] * 1_000_000
                + quadruple[1] * 10_000
                + quadruple[2] * 100
                + quadruple[3]
            )
            bases = []
            seen_bases = set()
            for solved_outer in quadruple:
                base_outers = tuple(
                    outer
                    for outer in quadruple
                    if outer != solved_outer
                )
                preferred = triple_witnesses[base_outers]
                preferred_rows = tuple(
                    preferred[outer] for outer in base_outers
                )
                key = (solved_outer, preferred_rows)
                bases.append((solved_outer, base_outers, preferred_rows))
                seen_bases.add(key)
                for selected in find_cliques(
                    base_outers,
                    pools,
                    masks,
                    limit=args.base_limit,
                ):
                    rows = tuple(
                        pools[outer][selected[outer]]
                        for outer in base_outers
                    )
                    key = (solved_outer, rows)
                    if key not in seen_bases:
                        bases.append((solved_outer, base_outers, rows))
                        seen_bases.add(key)
            preferred_bases = bases[:4]
            remaining_bases = bases[4:]
            local_rng.shuffle(remaining_bases)
            bases = preferred_bases + remaining_bases
            for solved_outer, base_outers, base_rows in bases:
                solved_row = solve_against_base(
                    args.binary,
                    solved_outer,
                    base_rows,
                    seconds=args.seconds,
                    nodes=args.nodes,
                    seed=local_rng.randrange(1, 2**63),
                )
                if solved_row is None:
                    continue
                rows_by_outer = dict(zip(base_outers, base_rows))
                rows_by_outer[solved_outer] = solved_row
                rows = [rows_by_outer[outer] for outer in quadruple]
                return {
                    "outers": list(quadruple),
                    "phase_rows": [list(row) for row in rows],
                    "collision_count": 0,
                    "source": "weighted_exact_row_solver",
                }
            return None

        unresolved = [tuple(item) for item in unknown]
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(solve_quadruple, quadruple): quadruple
                for quadruple in unresolved
            }
            for completed, future in enumerate(
                as_completed(futures),
                start=1,
            ):
                quadruple = futures[future]
                record = future.result()
                if record is not None:
                    records[quadruple] = record
                print(
                    json.dumps(
                        {
                            "status": (
                                "QUADRUPLE_WITNESS"
                                if record is not None
                                else "QUADRUPLE_UNKNOWN"
                            ),
                            "stage": "weighted_extension",
                            "outers": list(quadruple),
                            "completed": completed,
                            "resolved": len(records),
                            "target": len(quadruples),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
        unknown = [
            list(quadruple)
            for quadruple in quadruples
            if quadruple not in records
        ]

    payload = {
        "schema": (
            "cyclic17-centre0-quadruple-compatibility-v1"
        ),
        "centre": 0,
        "width_three_certificate_sha256": hashlib.sha256(
            width_three_bytes
        ).hexdigest(),
        "pool_sources": pool_hashes,
        "pool_sizes": {
            str(outer): len(pools[outer]) for outer in OUTERS
        },
        "records": [
            records[quadruple]
            for quadruple in quadruples
            if quadruple in records
        ],
        "resolved_quadruples": len(records),
        "target_quadruples": len(quadruples),
        "unknown_quadruples": unknown,
        "scope": (
            "four-row subsystems only; "
            "no fourteen-row star claim"
        ),
    }
    encoded = (
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    args.output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "status": (
                    "COMPLETE_QUADRUPLE_CERTIFICATE"
                    if not unknown
                    else "INCOMPLETE_QUADRUPLE_SEARCH"
                ),
                "resolved_quadruples": len(records),
                "unknown_quadruples": len(unknown),
                "target_quadruples": len(quadruples),
                "certificate_sha256": hashlib.sha256(
                    encoded
                ).hexdigest(),
                "scope": "four-row subsystems only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
