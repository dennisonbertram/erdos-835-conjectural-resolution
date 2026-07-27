#!/usr/bin/env python3
"""Exclude the support-12 cyclic quotient partition 2+1+1+1+1."""

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
EXPECTED = (
    (11528036, 1522695592, 4214, 536412),
    (11652420, 1578362072, 476, 64688),
    (11643564, 1580167740, 838, 112592),
    (11540424, 1550767128, 2482, 331704),
    (11606284, 1571015564, 2196, 293364),
    (11525488, 1539366204, 5756, 794484),
    (11545544, 1545906224, 3018, 389132),
    (11583684, 1567129684, 1420, 189348),
    (11617704, 1578007992, 682, 94804),
    (11413552, 1503071480, 8390, 1113916),
    (11445528, 1535365532, 7396, 1004152),
    (11100660, 1426871676, 25682, 3522292),
)
PATTERN = re.compile(
    r"NONE q (\d+):(\d+) configurations (\d+) first_moves (\d+) "
    r"second_moves (\d+) bounded_pairs (\d+) pair_probes (\d+) "
    r"full_hash_hits (\d+) exact_checks (\d+)\s*\Z"
)


def run_range(
    binary: Path, columns: Path, start: int, end: int
) -> tuple[int, ...]:
    completed = subprocess.run(
        (str(binary), str(columns), str(start), str(end)),
        check=True,
        capture_output=True,
        text=True,
        timeout=900,
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
    with tempfile.TemporaryDirectory(prefix="cyclic-support12-21111-") as tmp:
        work = Path(tmp)
        columns = work / "columns.txt"
        binary = work / "verify_case21111"
        support8.write_columns(columns)
        compiled = subprocess.run(
            (
                *compiler,
                "-O3",
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(HERE / "verify_case21111.cpp"),
                "-o",
                str(binary),
            ),
            capture_output=True,
            text=True,
            timeout=180,
        )
        if compiled.returncode:
            raise RuntimeError(compiled.stderr)
        with ThreadPoolExecutor(max_workers=12) as executor:
            results = list(
                executor.map(
                    lambda bounds: run_range(binary, columns, *bounds),
                    RANGES,
                )
            )
    for bounds, values, expected in zip(RANGES, results, EXPECTED):
        if values != (81510, *expected, 0, 0):
            raise AssertionError(f"wrong counters {bounds}: {values}")
        print(f"Q range {bounds[0]}:{bounds[1]}: NONE")
    totals = tuple(sum(row[index] for row in results) for index in range(7))
    expected_totals = (
        978120,
        138202888,
        18498726888,
        62550,
        8446888,
        0,
        0,
    )
    if totals != expected_totals:
        raise AssertionError(f"wrong totals: {totals}")
    print(f"aggregate counters: {totals}")
    print("case 2+1+1+1+1: NONE")
    print("support-12 partition 2+1+1+1+1 audit: PASS")
    print("scope: only support-12 partition 1^6 remains")


if __name__ == "__main__":
    main()
