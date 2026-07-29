#!/usr/bin/env python3
"""Validate, merge, and receipt a partitioned type-(i) branch sweep."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branches", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--solver-source", type=Path, required=True)
    parser.add_argument("--summary", type=Path, action="append", required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--seconds-per-branch", type=float, required=True)
    parser.add_argument("--seed-base", type=int, required=True)
    args = parser.parse_args()
    if args.output_jsonl.exists() or args.receipt.exists():
        raise FileExistsError("refusing to overwrite an existing merged artifact")

    branches = [
        tuple(map(int, line.split()))
        for line in args.branches.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    if len(branches) != 1_326:
        raise AssertionError("branch census is not 1326")

    records = []
    for path in args.summary:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
    records.sort(key=lambda record: record["branch_index"])
    if [record["branch_index"] for record in records] != list(range(1_326)):
        raise AssertionError("summary files do not partition all branch indices")

    nodes = []
    for record in records:
        index = record["branch_index"]
        if tuple(record["rows"]) != branches[index]:
            raise AssertionError(f"branch rows mismatch at index {index}")
        if record["model"] is not None:
            raise AssertionError("a model exists and requires semantic verification")
        match = re.fullmatch(r"UNKNOWN timeout nodes=(\d+)", record["stdout"])
        if record["status"] != "UNKNOWN_TIMEOUT" or not match:
            raise AssertionError(f"unexpected branch status at index {index}")
        record["seed"] = args.seed_base + index
        nodes.append(int(match.group(1)))

    merged_content = (
        "\n".join(
            json.dumps(record, sort_keys=True, separators=(",", ":"))
            for record in records
        )
        + "\n"
    ).encode("utf-8")
    args.output_jsonl.write_bytes(merged_content)
    merged_digest = hashlib.sha256(merged_content).hexdigest()
    status_counts = Counter(record["status"] for record in records)
    receipt = {
        "branch_count": len(records),
        "branch_file_sha256": sha256(args.branches),
        "elapsed_seconds_max": max(record["elapsed_seconds"] for record in records),
        "elapsed_seconds_min": min(record["elapsed_seconds"] for record in records),
        "elapsed_seconds_total": round(
            sum(record["elapsed_seconds"] for record in records), 6
        ),
        "matrix_sha256": sha256(args.matrix),
        "merged_jsonl_sha256": merged_digest,
        "models_found": 0,
        "nodes_max": max(nodes),
        "nodes_min": min(nodes),
        "nodes_total": sum(nodes),
        "schema": "erdos835-c17-type-i-bounded-sweep-v1",
        "scope": (
            "bounded witness-search telemetry only; 1326 timeouts do not prove "
            "UNSAT for any branch or for the equivariant ansatz"
        ),
        "seconds_per_branch": args.seconds_per_branch,
        "seed_rule": f"{args.seed_base} + branch_index",
        "solver_source_sha256": sha256(args.solver_source),
        "source_summary_sha256": {path.name: sha256(path) for path in args.summary},
        "status_counts": dict(sorted(status_counts.items())),
    }
    receipt_content = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    args.receipt.write_bytes(receipt_content)
    print(f"merged records: {len(records)}")
    print(f"status counts: {dict(status_counts)}")
    print(f"nodes total: {sum(nodes)}")
    print(f"merged SHA-256: {merged_digest}")
    print(f"receipt SHA-256: {hashlib.sha256(receipt_content).hexdigest()}")
    print(f"scope: {receipt['scope']}")


if __name__ == "__main__":
    main()
