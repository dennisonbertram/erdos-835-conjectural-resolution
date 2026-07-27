#!/usr/bin/env python3
"""Reconnaissance sweep for derived EH point-links using CaDiCaL.

UNSAT rows from this program are *not* portable certificates.  A positive row
is exact because its model is decoded and checked as five STS(19)s.  Promote a
negative result only after generating and independently replaying a DRAT proof.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from point_link_cnf import (
    build_instance,
    clauses_for,
    decode_and_verify,
    load_source,
    parse_drop,
    parse_solver_model,
    write_cnf,
)


CONSTRUCTION_PACKS = (
    frozenset(range(0, 5)),
    frozenset(range(5, 10)),
    frozenset(range(10, 15)),
)

PORTABLY_EXCLUDED_DROPS = {
    (0, 1, 5),
    (0, 5, 10),
}


def excluded_by_ten_point(drop: tuple[int, int, int]) -> bool:
    return any(set(drop) <= pack for pack in CONSTRUCTION_PACKS)


def solve_one(
    systems: tuple[frozenset[tuple[int, ...]], ...],
    drop: tuple[int, int, int],
    point: int,
    cadical: str,
    seconds: int,
) -> dict[str, object]:
    triples, by_pair = build_instance(systems, drop, point)
    clauses = clauses_for(triples, by_pair)
    with tempfile.TemporaryDirectory(prefix="eh-point-link-") as raw_temp:
        temp = Path(raw_temp)
        cnf = temp / "instance.cnf"
        model = temp / "model.txt"
        cnf_sha256 = write_cnf(cnf, triples, clauses)
        started = time.perf_counter()
        completed = subprocess.run(
            [
                cadical,
                "-q",
                "-t",
                str(seconds),
                "-w",
                str(model),
                str(cnf),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        elapsed = time.perf_counter() - started
        transcript = completed.stdout + completed.stderr

        # SAT-competition return codes are 10 (SAT) and 20 (UNSAT).  Quiet
        # builds are allowed to suppress the textual status line.
        if completed.returncode == 20 or "s UNSATISFIABLE" in transcript:
            status = "UNSAT_RECONNAISSANCE"
            colour_sha256 = None
        elif completed.returncode == 10 or "s SATISFIABLE" in transcript:
            status = "SAT_VERIFIED"
            colours = decode_and_verify(triples, by_pair, parse_solver_model(model))
            colour_sha256 = hashlib.sha256(bytes(colours)).hexdigest()
        else:
            status = "UNKNOWN"
            colour_sha256 = None

    return {
        "drop": list(drop),
        "point": point,
        "status": status,
        "elapsed_seconds": round(elapsed, 6),
        "cadical_returncode": completed.returncode,
        "cnf_sha256": cnf_sha256,
        "colour_sha256": colour_sha256,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", type=parse_drop, action="append")
    parser.add_argument("--all-survivors", action="store_true")
    parser.add_argument(
        "--remaining-after-certificates",
        action="store_true",
        help="screen the 423 cases outside the 30 ten-point and two DRAT exclusions",
    )
    parser.add_argument("--point", type=int, action="append")
    parser.add_argument("--seconds", type=int, default=10)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--cadical", default="cadical")
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()

    if args.remaining_after_certificates:
        drops = [
            drop
            for drop in itertools.combinations(range(15), 3)
            if not excluded_by_ten_point(drop) and drop not in PORTABLY_EXCLUDED_DROPS
        ]
    elif args.all_survivors:
        drops = [
            drop
            for drop in itertools.combinations(range(15), 3)
            if not excluded_by_ten_point(drop)
        ]
    elif args.drop:
        drops = sorted(set(args.drop))
    else:
        raise SystemExit(
            "provide --drop, --all-survivors, or --remaining-after-certificates"
        )
    points = sorted(set(args.point if args.point is not None else [0]))
    if not set(points) <= set(range(20)):
        raise SystemExit("points must lie in 0,...,19")
    if args.jobs < 1:
        raise SystemExit("--jobs must be positive")

    _, systems = load_source()
    cases = [(drop, point) for drop in drops for point in points]
    rows: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                solve_one,
                systems,
                drop,
                point,
                args.cadical,
                args.seconds,
            ): (drop, point)
            for drop, point in cases
        }
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)

    rows.sort(key=lambda row: (row["drop"], row["point"]))
    args.results.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="ascii",
    )
    census: dict[str, int] = {}
    for row in rows:
        status = str(row["status"])
        census[status] = census.get(status, 0) + 1
    print(
        json.dumps(
            {
                "cases": len(rows),
                "census": census,
                "result_sha256": hashlib.sha256(args.results.read_bytes()).hexdigest(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
