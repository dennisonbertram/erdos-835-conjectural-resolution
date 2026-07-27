#!/usr/bin/env python3
"""Exclude the support-12 cyclic quotient partition 2+2+1+1."""

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
    (17285914800, 11898712488, 54964, 2198, 293260),
    (15982744800, 11248638984, 5184, 0, 0),
    (14343872400, 9800665368, 33912, 960, 126648),
    (12535261200, 8528085120, 31836, 310, 41176),
    (10786908000, 7433154168, 33220, 920, 126492),
    (9482878900, 6345199584, 12764, 214, 29916),
    (10967391600, 7364763024, 53284, 1376, 182092),
    (8983669200, 5907545220, 30484, 260, 34132),
    (7159812000, 4781923332, 7068, 248, 32736),
    (6033435100, 3699740860, 74228, 2308, 312476),
    (4743768700, 2860815764, 30516, 1274, 173892),
    (2494003600, 1357229336, 42764, 2364, 318144),
)
PATTERN = re.compile(
    r"NONE q (\d+):(\d+) outer (\d+) posting_hits (\d+) "
    r"touched (\d+) overlap_candidates (\d+) bounded_targets (\d+) "
    r"single_probes (\d+) fingerprint_hits (\d+) exact_checks (\d+)\s*\Z"
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
    with tempfile.TemporaryDirectory(prefix="cyclic-support12-2211-") as tmp:
        work = Path(tmp)
        columns = work / "columns.txt"
        binary = work / "verify_case2211"
        support8.write_columns(columns)
        compiled = subprocess.run(
            (
                *compiler,
                "-O3",
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(HERE / "verify_case2211.cpp"),
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
    totals = tuple(sum(row[index] for row in results) for index in range(8))
    expected_totals = (
        978120,
        120799660300,
        81226473248,
        410224,
        12432,
        1670964,
        0,
        0,
    )
    if totals != expected_totals:
        raise AssertionError(f"wrong totals: {totals}")
    print(f"aggregate counters: {totals}")
    print("case 2+2+1+1: NONE")
    print("support-12 partition 2+2+1+1 audit: PASS")
    print("scope: two support-12 partitions remain unexplored")


if __name__ == "__main__":
    main()
