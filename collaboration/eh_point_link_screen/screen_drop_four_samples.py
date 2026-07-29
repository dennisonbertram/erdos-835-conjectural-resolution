#!/usr/bin/env python3
"""Run a structurally diverse point-0 sample of EH drop-four point-links.

SAT rows are mathematical witnesses: the returned assignment is decoded and
checked as six disjoint STS(19)s without trusting the CNF.  UNSAT rows remain
reconnaissance until a portable proof is generated and independently replayed.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path

from drop_four_point_link_cnf import (
    N_CLAUSES,
    N_VARIABLES,
    build_instance,
    clauses_for,
    decode_and_verify,
    parse_solver_model,
    write_cnf,
)
from point_link_cnf import BLOCKS, POINTS, load_source


SCHEMA = "eh-point-link-drop4-sample-v1"
RECEIPT_SCHEMA = "eh-point-link-drop4-sample-receipt-v1"
POINT = 0
CONSTRUCTION_PACKS = (
    frozenset(range(0, 5)),
    frozenset(range(5, 10)),
    frozenset(range(10, 15)),
)
SAMPLE_DROPS = (
    (0, 1, 2, 3),
    (0, 1, 2, 5),
    (0, 1, 5, 8),
    (0, 1, 5, 7),
    (0, 1, 5, 6),
    (0, 1, 5, 11),
    (0, 1, 5, 10),
    (0, 1, 9, 11),
    (0, 5, 9, 14),
)
EXPECTED_STRUCTURAL_CELLS = {
    ((4,), 144),
    ((3, 1), 24),
    ((2, 2), 4),
    ((2, 2), 16),
    ((2, 2), 17),
    ((2, 1, 1), 4),
    ((2, 1, 1), 29),
    ((2, 1, 1), 54),
    ((2, 1, 1), 104),
}


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("wb") as output:
        output.write(content)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def construction_pack_multiplicity(
    drop: tuple[int, int, int, int],
) -> tuple[int, ...]:
    return tuple(
        sorted(
            (len(set(drop) & pack) for pack in CONSTRUCTION_PACKS if set(drop) & pack),
            reverse=True,
        )
    )


def full_top_count(
    systems: tuple[frozenset[tuple[int, ...]], ...],
    drop: tuple[int, int, int, int],
) -> int:
    retained = set().union(
        *(system for number, system in enumerate(systems) if number not in drop)
    )
    leave = set(BLOCKS) - retained
    return sum(
        all(block in leave for block in itertools.combinations(top, 4))
        for top in itertools.combinations(POINTS, 5)
    )


def solver_version(cadical: str) -> str:
    completed = subprocess.run(
        [cadical, "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    lines = (completed.stdout + completed.stderr).strip().splitlines()
    if completed.returncode != 0 or not lines:
        raise AssertionError("could not determine CaDiCaL version")
    return lines[0]


def solve_one(
    systems: tuple[frozenset[tuple[int, ...]], ...],
    drop: tuple[int, int, int, int],
    cadical: str,
    seconds: int,
    cadical_version: str,
) -> dict[str, object]:
    triples, by_pair = build_instance(systems, drop, POINT)
    clauses = clauses_for(triples, by_pair)
    with tempfile.TemporaryDirectory(prefix="eh-drop4-point-link-") as raw_temp:
        temp = Path(raw_temp)
        cnf = temp / "instance.cnf"
        model = temp / "model.txt"
        cnf_sha256 = write_cnf(cnf, clauses)
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

        if completed.returncode == 20 or "s UNSATISFIABLE" in transcript:
            status = "UNSAT_RECONNAISSANCE"
            colours: tuple[int, ...] | None = None
        elif completed.returncode == 10 or "s SATISFIABLE" in transcript:
            status = "SAT_VERIFIED"
            colours = decode_and_verify(
                triples,
                by_pair,
                parse_solver_model(model),
            )
        else:
            status = "UNKNOWN"
            colours = None

    colour_sha256 = (
        hashlib.sha256(bytes(colours)).hexdigest() if colours is not None else None
    )
    return {
        "schema": SCHEMA,
        "drop": list(drop),
        "point": POINT,
        "construction_pack_multiplicity": list(construction_pack_multiplicity(drop)),
        "full_top_count": full_top_count(systems, drop),
        "status": status,
        "elapsed_seconds": round(elapsed, 6),
        "cadical_returncode": completed.returncode,
        "cadical_version": cadical_version,
        "cnf_sha256": cnf_sha256,
        "cnf_variables": N_VARIABLES,
        "cnf_clauses": N_CLAUSES,
        "colour_sha256": colour_sha256,
        "colours": list(colours) if colours is not None else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", default="cadical")
    parser.add_argument("--seconds", type=int, default=30)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.seconds <= 0:
        raise SystemExit("--seconds must be positive")

    _, systems = load_source()
    cells = {
        (construction_pack_multiplicity(drop), full_top_count(systems, drop))
        for drop in SAMPLE_DROPS
    }
    if cells != EXPECTED_STRUCTURAL_CELLS:
        raise AssertionError(
            f"sample does not cover the intended structural cells: {sorted(cells)}"
        )

    cadical_version = solver_version(args.cadical)
    rows: list[dict[str, object]] = []
    for index, drop in enumerate(SAMPLE_DROPS, 1):
        row = solve_one(
            systems,
            drop,
            args.cadical,
            args.seconds,
            cadical_version,
        )
        rows.append(row)
        print(
            json.dumps(
                {
                    "drop": row["drop"],
                    "elapsed_seconds": row["elapsed_seconds"],
                    "progress": f"{index}/{len(SAMPLE_DROPS)}",
                    "status": row["status"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    rows.sort(key=lambda row: row["drop"])
    results_content = "".join(
        json.dumps(row, sort_keys=True) + "\n" for row in rows
    ).encode("ascii")
    atomic_write(args.results, results_content)
    elapsed = [float(row["elapsed_seconds"]) for row in rows]
    census = Counter(str(row["status"]) for row in rows)
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "row_schema": SCHEMA,
        "cases": len(rows),
        "point": POINT,
        "seconds_per_case": args.seconds,
        "cadical_version": cadical_version,
        "census": dict(sorted(census.items())),
        "total_solver_seconds": round(sum(elapsed), 6),
        "minimum_solver_seconds": min(elapsed),
        "maximum_solver_seconds": max(elapsed),
        "structural_cells": [
            {
                "construction_pack_multiplicity": list(multiplicity),
                "full_top_count": tops,
            }
            for multiplicity, tops in sorted(EXPECTED_STRUCTURAL_CELLS)
        ],
        "results_path": args.results.name,
        "results_sha256": hashlib.sha256(results_content).hexdigest(),
    }
    receipt_content = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode(
        "ascii"
    )
    atomic_write(args.receipt, receipt_content)
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
