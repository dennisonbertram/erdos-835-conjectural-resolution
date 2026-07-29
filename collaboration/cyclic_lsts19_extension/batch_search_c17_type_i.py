#!/usr/bin/env python3
"""Portfolio a compiled witness solver across the 1,326 type-(i) branches.

Timeout and process-local exhaustion are recorded as search telemetry only.
Any SAT candidate must pass the independent semantic verifier.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--branches", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--worker-index", type=int, required=True)
    parser.add_argument("--worker-count", type=int, required=True)
    parser.add_argument("--seconds-per-branch", type=float, default=1.0)
    parser.add_argument("--seed-base", type=int, default=835)
    args = parser.parse_args()
    if not 0 <= args.worker_index < args.worker_count:
        raise ValueError("worker index must lie in [0, worker count)")
    if args.summary.exists():
        raise FileExistsError(f"refusing stale summary path: {args.summary}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    branches = [
        tuple(map(int, line.split()))
        for line in args.branches.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    if len(branches) != 1_326 or any(len(branch) != 8 for branch in branches):
        raise AssertionError("branch file does not contain 1,326 eight-row branches")

    with args.summary.open("x", encoding="utf-8") as stream:
        for index, branch in enumerate(branches):
            if index % args.worker_count != args.worker_index:
                continue
            model = args.output_dir / f"branch_{index:04d}.model"
            if model.exists():
                raise FileExistsError(f"refusing stale model path: {model}")
            command = [
                str(args.solver),
                str(args.matrix),
                str(model),
                str(args.seconds_per_branch),
                str(args.seed_base + index),
                *map(str, branch),
            ]
            started = time.monotonic()
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=args.seconds_per_branch + 30,
            )
            elapsed = time.monotonic() - started
            status = {
                0: "SAT_CANDIDATE",
                2: "UNKNOWN_TIMEOUT",
                3: "EXHAUSTED_WITHOUT_CERTIFICATE",
            }.get(result.returncode, "ERROR")
            record = {
                "branch_index": index,
                "elapsed_seconds": round(elapsed, 6),
                "exit_code": result.returncode,
                "model": str(model) if model.exists() else None,
                "rows": branch,
                "status": status,
                "stdout": result.stdout.strip(),
                "stderr_tail": result.stderr.strip().splitlines()[-1:]
                if result.stderr.strip()
                else [],
            }
            stream.write(json.dumps(record, sort_keys=True) + "\n")
            stream.flush()
            print(
                f"worker={args.worker_index} branch={index} status={status} "
                f"elapsed={elapsed:.3f}",
                flush=True,
            )
            if status == "SAT_CANDIDATE":
                return
            if status == "ERROR":
                raise RuntimeError(f"solver failed on branch {index}: {record}")


if __name__ == "__main__":
    main()
