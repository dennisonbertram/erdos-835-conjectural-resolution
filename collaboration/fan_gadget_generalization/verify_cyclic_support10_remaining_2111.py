#!/usr/bin/env python3
"""Exclude support-ten case 2+1+1+1 by exact fingerprint filtering."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
import tempfile

import verify_cyclic_support8 as support8


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_cyclic_support10_remaining_2111.cpp"
RANGES = tuple((start, start + 19) for start in range(0, 228, 19))
EXPECTED_FIRST = (
    11528036, 11652420, 11643564, 11540424, 11606284, 11524564,
    11545544, 11583684, 11617704, 11412942, 11444896, 11097384,
)
EXPECTED_PROBES = (
    1522695592, 1578362072, 1580167740, 1550767128, 1571015564,
    1539269256, 1545906224, 1567129684, 1578007992, 1503007220,
    1535298908, 1426526424,
)
EXPECTED_LOW = (
    3221636, 3339930, 3345444, 3289394, 3326200, 3262860,
    3275956, 3320838, 3339932, 3186024, 3251390, 3022138,
)
PATTERN = re.compile(
    r"NONE q (\d+):(\d+) configs (\d+) first (\d+) probes (\d+) "
    r"low_hits (\d+) hash_hits (\d+) exact_checks (\d+)\s*\Z"
)


def run_range(binary: Path, columns: Path, start: int, end: int) -> tuple[int, ...]:
    completed = subprocess.run(
        (str(binary), str(columns), str(start), str(end)),
        check=True, capture_output=True, text=True, timeout=900,
    )
    match = PATTERN.fullmatch(completed.stdout)
    if match is None:
        raise AssertionError(f"unexpected output:\n{completed.stdout}")
    values = tuple(map(int, match.groups()))
    if values[:2] != (start, end):
        raise AssertionError("wrong reported range")
    return values[2:]


def main() -> None:
    compiler = support8.compiler_command()
    with tempfile.TemporaryDirectory(prefix="cyclic-support10-2111-") as tmp:
        work = Path(tmp)
        columns = work / "columns.txt"
        binary = work / SOURCE.stem
        support8.write_columns(columns)
        compiled = subprocess.run(
            (*compiler, "-O3", "-std=c++17", str(SOURCE), "-o", str(binary)),
            capture_output=True, text=True, timeout=180,
        )
        if compiled.returncode:
            raise RuntimeError(compiled.stderr)
        with ThreadPoolExecutor(max_workers=12) as executor:
            results = list(
                executor.map(
                    lambda bounds: run_range(binary, columns, *bounds), RANGES
                )
            )

    for index, (bounds, values) in enumerate(zip(RANGES, results)):
        expected = (
            81510, EXPECTED_FIRST[index], EXPECTED_PROBES[index],
            EXPECTED_LOW[index], 0, 0,
        )
        if values != expected:
            raise AssertionError(f"wrong counters for {bounds}: {values}")
        print(f"Q range {bounds[0]}:{bounds[1]}: NONE; counters={values}")
    totals = tuple(sum(row[index] for row in results) for index in range(6))
    if totals != (978120, 138197446, 18498153804, 39181742, 0, 0):
        raise AssertionError(f"wrong totals: {totals}")
    print(f"aggregate counters: {totals}")
    print("case 2+1+1+1: NONE")
    print("cyclic quotient support-ten 2+1+1+1 audit: PASS")
    print("remaining partition: 1+1+1+1+1")


if __name__ == "__main__":
    main()
