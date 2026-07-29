#!/usr/bin/env python3
"""Deterministically merge and validate the four orbit-9 worker JSONLs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_INPUTS = tuple(
    HERE / f"2026-07-28_orbit9_fixed_pair_worker_{index}.jsonl"
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
    for worker_index, path in enumerate(args.inputs):
        worker_rows = tuple(
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        assert len(worker_rows) == (22 if worker_index < 3 else 21)
        assert tuple(row["case_index"] for row in worker_rows) == tuple(
            range(22 * worker_index, 22 * (worker_index + 1)) if worker_index < 3 else range(66, 87)
        )
        rows.extend(worker_rows)

    rows.sort(key=lambda row: row["case_index"])
    assert tuple(row["case_index"] for row in rows) == tuple(range(87))
    assert len({row["case"] for row in rows}) == 87
    assert all(row["status"] == "unsat" for row in rows)
    assert all(row["proof_claimed"] is False for row in rows)
    assert sum(row["learned_unions"] for row in rows) == 13_734_283
    assert sum(row["rounds"] for row in rows) == 3_423

    for row in rows:
        print(json.dumps(row, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
