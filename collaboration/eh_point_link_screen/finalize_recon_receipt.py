#!/usr/bin/env python3
"""Normalize and atomically seal the 423-case point-0 recon receipt."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from collections import Counter
from pathlib import Path

from certify_point_links import RECON_SCHEMA, load_recon
from screen_point_links import (
    PORTABLY_EXCLUDED_DROPS,
    excluded_by_ten_point,
)


RECEIPT_SCHEMA = "eh-point-link-recon-receipt-v1"


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("wb") as output:
        output.write(content)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def expected_keys() -> set[tuple[tuple[int, int, int], int]]:
    drops = {
        drop
        for drop in itertools.combinations(range(15), 3)
        if not excluded_by_ten_point(drop) and drop not in PORTABLY_EXCLUDED_DROPS
    }
    if len(drops) != 423:
        raise AssertionError("internal survivor census is not 423")
    return {(drop, 0) for drop in drops}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--seconds", type=int, required=True)
    parser.add_argument("--jobs", type=int, required=True)
    args = parser.parse_args()

    rows = [
        json.loads(line)
        for line in args.input.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    for row in rows:
        row["schema"] = RECON_SCHEMA
        row["cnf_variables"] = 1_425
        row["cnf_clauses"] = 12_545
    rows.sort(key=lambda row: (row["drop"], row["point"]))
    keys = {(tuple(row["drop"]), int(row["point"])) for row in rows}
    if keys != expected_keys() or len(rows) != 423:
        raise AssertionError(
            f"recon cases do not equal the intended 423-case set: rows={len(rows)}"
        )

    jsonl = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows).encode(
        "ascii"
    )
    atomic_write(args.output, jsonl)
    # Reparse with the strict consumer after the atomic write.
    audited = load_recon(args.output, expected_rows=423)

    census = Counter(str(row["status"]) for row in audited)
    elapsed = [float(row["elapsed_seconds"]) for row in audited]
    summary = {
        "schema": RECEIPT_SCHEMA,
        "row_schema": RECON_SCHEMA,
        "cases": len(audited),
        "expected_drop_cases": 423,
        "point": 0,
        "seconds_per_case": args.seconds,
        "jobs": args.jobs,
        "census": dict(sorted(census.items())),
        "total_solver_seconds": round(sum(elapsed), 6),
        "minimum_solver_seconds": min(elapsed),
        "maximum_solver_seconds": max(elapsed),
        "jsonl_path": args.output.name,
        "jsonl_sha256": hashlib.sha256(jsonl).hexdigest(),
    }
    atomic_write(
        args.summary,
        (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("ascii"),
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
