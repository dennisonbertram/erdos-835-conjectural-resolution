#!/usr/bin/env python3
"""Exclude the support-12 partition 2+2+2."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import verify_cyclic_support8 as support8  # noqa: E402


RANGES = tuple((start, start + 19) for start in range(0, 228, 19))
EXPECTED_PROBES = (
    341367840, 261047160, 225078480, 185775480, 142860960, 48684240,
    229253640, 153545040, 82775880, 91728120, 44880000, 16901280,
)
EXPECTED_LOW = (
    19348616, 14791888, 12746068, 10518150, 8091520, 2755418,
    12984280, 8698890, 4685784, 5198860, 2540750, 956540,
)
PATTERN = re.compile(
    r"NONE q (\d+):(\d+) outer (\d+) probes (\d+) low_hits (\d+) "
    r"hash_hits (\d+) exact_checks (\d+)\s*\Z"
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
        raise AssertionError("wrong range")
    return values[2:]


def main() -> None:
    compiler = support8.compiler_command()
    with tempfile.TemporaryDirectory(prefix="cyclic-support12-222-") as tmp:
        work = Path(tmp)
        columns = work / "columns.txt"
        binary = work / "verify_case222"
        support8.write_columns(columns)
        compiled = subprocess.run(
            (*compiler, "-O3", "-std=c++17", str(HERE / "verify_case222.cpp"),
             "-o", str(binary)),
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
        expected = (81510, EXPECTED_PROBES[index], EXPECTED_LOW[index], 0, 0)
        if values != expected:
            raise AssertionError(f"wrong counters {bounds}: {values}")
        print(f"Q range {bounds[0]}:{bounds[1]}: NONE")
    totals = tuple(sum(row[index] for row in results) for index in range(5))
    if totals != (978120, 1823898120, 103316764, 0, 0):
        raise AssertionError(f"wrong totals: {totals}")
    print(f"aggregate counters: {totals}")
    print("case 2+2+2: NONE")
    print("support-12 partition 2+2+2 audit: PASS")
    print("scope: five support-12 partitions remain unexplored")


if __name__ == "__main__":
    main()
