#!/usr/bin/env python3
"""Exclude the support-12 cyclic quotient partition 1^6."""

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
    (236816, 24398272, 97616, 12408084),
    (279592, 30899764, 63896, 7533656),
    (280712, 30111328, 84962, 9389480),
    (245920, 23918804, 72232, 7492152),
    (156848, 11878520, 40106, 3966276),
    (162516, 14652144, 80236, 4630208),
    (166424, 11694224, 50704, 4192076),
    (198764, 14348004, 57424, 4455384),
    (144396, 8499400, 40510, 2825104),
    (103288, 5885248, 54208, 2158212),
    (106608, 5661440, 45794, 1778240),
    (68656, 2705904, 20798, 470644),
)
PATTERN = re.compile(
    r"NONE q (\d+):(\d+) outer (\d+) second_moves (\d+) "
    r"third_moves (\d+) fourth_moves (\d+) pair_probes (\d+) "
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
        timeout=1800,
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
    with tempfile.TemporaryDirectory(prefix="cyclic-support12-111111-") as tmp:
        work = Path(tmp)
        columns = work / "columns.txt"
        binary = work / "verify_case111111"
        support8.write_columns(columns)
        compiled = subprocess.run(
            (
                *compiler,
                "-O3",
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(HERE / "verify_case111111.cpp"),
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
        if values != (2964, *expected, 0, 0):
            raise AssertionError(f"wrong counters {bounds}: {values}")
        print(f"Q range {bounds[0]}:{bounds[1]}: NONE")
    totals = tuple(sum(row[index] for row in results) for index in range(7))
    expected_totals = (
        35568,
        2150540,
        184653052,
        708486,
        61299516,
        0,
        0,
    )
    if totals != expected_totals:
        raise AssertionError(f"wrong totals: {totals}")
    print(f"aggregate counters: {totals}")
    print("case 1+1+1+1+1+1: NONE")
    print("support-12 partition 1^6 audit: PASS")
    print("theorem: every nonzero squarefree quotient trade has support at least 14")


if __name__ == "__main__":
    main()
