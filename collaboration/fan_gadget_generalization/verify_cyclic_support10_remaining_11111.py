#!/usr/bin/env python3
"""Exclude support-ten case 1+1+1+1+1 by exact fingerprint filtering."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
import tempfile

import verify_cyclic_support8 as support8


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_cyclic_support10_remaining_11111.cpp"
RANGES = tuple((start, start + 19) for start in range(0, 228, 19))
EXPECTED_SECOND = (
    236816, 279592, 280712, 245920, 156848, 162516,
    166424, 198764, 144396, 103288, 106608, 68656,
)
EXPECTED_THIRD = (
    24398190, 30899218, 30110240, 23917978, 11878148, 14649820,
    11694182, 14346506, 8498926, 5882822, 5659614, 2704880,
)
EXPECTED_PROBES = (
    2692308256, 3438393424, 3220216632, 2331811944, 1024916280,
    1384597288, 853583268, 1053650040, 562108596, 373554496,
    320073244, 105589460,
)
EXPECTED_LOW = (
    5701994, 7282840, 6823312, 4938316, 2171670, 2929352,
    1809426, 2233048, 1188888, 790910, 675762, 224388,
)
PATTERN = re.compile(
    r"NONE q (\d+):(\d+) second (\d+) third (\d+) probes (\d+) "
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
    with tempfile.TemporaryDirectory(prefix="cyclic-support10-11111-") as tmp:
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
            EXPECTED_SECOND[index], EXPECTED_THIRD[index],
            EXPECTED_PROBES[index], EXPECTED_LOW[index], 0, 0,
        )
        if values != expected:
            raise AssertionError(f"wrong counters for {bounds}: {values}")
        print(f"Q range {bounds[0]}:{bounds[1]}: NONE; counters={values}")
    totals = tuple(sum(row[index] for row in results) for index in range(6))
    if totals != (2150540, 184640524, 17360802928, 36769906, 0, 0):
        raise AssertionError(f"wrong totals: {totals}")
    print(f"aggregate counters: {totals}")
    print("case 1+1+1+1+1: NONE")
    print("cyclic quotient support-ten 1^5 audit: PASS")
    print("theorem: every nonzero squarefree quotient trade has support at least 12")


if __name__ == "__main__":
    main()
