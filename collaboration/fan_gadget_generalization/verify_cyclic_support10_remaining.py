#!/usr/bin/env python3
"""Verify the support-ten 3+1+1 exclusion in four exact Q-ranges."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
import tempfile

import verify_cyclic_support8 as support8


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_cyclic_support10_remaining_311.cpp"
RANGES = ((0, 57), (57, 114), (114, 171), (171, 228))
EXPECTED_LOOKUPS = (220_203_366, 213_540_502, 214_422_052, 182_612_718)
RESULT = re.compile(r"NONE configurations (\d+) lookups (\d+)\s*\Z")


def run_range(binary: Path, columns: Path, start: int, end: int) -> tuple[int, int]:
    completed = subprocess.run(
        (str(binary), str(columns), str(start), str(end)),
        check=True,
        capture_output=True,
        text=True,
        timeout=900,
    )
    match = RESULT.fullmatch(completed.stdout)
    if match is None:
        raise AssertionError(f"unexpected range output:\n{completed.stdout}")
    return int(match.group(1)), int(match.group(2))


def main() -> None:
    compiler = support8.compiler_command()
    with tempfile.TemporaryDirectory(prefix="cyclic-support10-remaining-") as temporary:
        work = Path(temporary)
        columns = work / "columns.txt"
        binary = work / SOURCE.stem
        support8.write_columns(columns)
        compiled = subprocess.run(
            (
                *compiler,
                "-O3",
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(SOURCE),
                "-o",
                str(binary),
            ),
            capture_output=True,
            text=True,
            timeout=180,
        )
        if compiled.returncode:
            raise RuntimeError(f"failed to compile verifier:\n{compiled.stderr}")
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(run_range, binary, columns, start, end)
                for start, end in RANGES
            ]
            results = [future.result() for future in futures]

    for (start, end), (configurations, lookups), expected in zip(
        RANGES, results, EXPECTED_LOOKUPS
    ):
        if configurations != 1_956_240 or lookups != expected:
            raise AssertionError(
                f"unexpected range {start}:{end}: "
                f"{configurations} configurations, {lookups} lookups"
            )
        print(
            f"Q range {start}:{end}: NONE; "
            f"configurations={configurations}; lookups={lookups}"
        )
    total_configurations = sum(result[0] for result in results)
    total_lookups = sum(result[1] for result in results)
    if total_configurations != 7_824_960 or total_lookups != 830_778_638:
        raise AssertionError("wrong aggregate counters")
    print(f"aggregate configurations: {total_configurations}")
    print(f"aggregate exact residual lookups: {total_lookups}")
    print("case 3+1+1: NONE")
    print("cyclic quotient support-ten remaining audit: PASS")
    print("remaining partitions: 2+2+1, 2+1+1+1, 1+1+1+1+1")
    print("scope: support ten is not fully excluded")


if __name__ == "__main__":
    main()
