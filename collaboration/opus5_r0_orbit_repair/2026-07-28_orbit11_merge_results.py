#!/usr/bin/env python3
"""Deterministically merge and validate the four orbit-11 worker JSONLs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_INPUTS = tuple(
    HERE / f"2026-07-28_orbit11_fixed_pair_worker_{index}.jsonl"
    for index in range(4)
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inputs",
        type=Path,
        nargs="*",
        default=DEFAULT_INPUTS,
    )
    args = parser.parse_args()

    assert len(args.inputs) == 4
    rows: list[dict[str, object]] = []
    expected_ranges = (
        range(0, 24),
        range(24, 47),
        range(47, 70),
        range(70, 93),
    )
    for worker_index, path in enumerate(args.inputs):
        worker_rows = tuple(
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        assert len(worker_rows) == len(expected_ranges[worker_index])
        assert tuple(row["case_index"] for row in worker_rows) == tuple(
            expected_ranges[worker_index]
        )
        rows.extend(worker_rows)

    rows.sort(key=lambda row: row["case_index"])
    assert tuple(row["case_index"] for row in rows) == tuple(range(93))
    assert len({row["case"] for row in rows}) == 93
    assert all(row["status"] == "unsat" for row in rows)
    assert all(row["proof_claimed"] is False for row in rows)
    assert sum(row["learned_unions"] for row in rows) == 11_441_006
    assert sum(row["rounds"] for row in rows) == 1_705

    for row in rows:
        print(json.dumps(row, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
