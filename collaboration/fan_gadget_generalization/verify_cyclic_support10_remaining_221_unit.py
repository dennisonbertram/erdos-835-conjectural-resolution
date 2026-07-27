#!/usr/bin/env python3
"""Exclude the all-unit stratum of support-ten case 2+2+1."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
import tempfile

import verify_cyclic_support8 as support8


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_cyclic_support10_remaining_221_unit.cpp"
RANGES = ((0, 8892), (8892, 17784), (17784, 26676), (26676, 35568))
EXPECTED = (
    (593_693_808, 373_684, 331_046, 22_440),
    (586_017_736, 532_190, 475_900, 39_112),
    (590_042_240, 419_150, 376_000, 30_948),
    (558_685_796, 1_289_534, 1_146_058, 154_760),
)
PATTERN = re.compile(
    r"NONE singles (\d+):(\d+) unit_doubles 944478 "
    r"posting_hits (\d+) candidates (\d+) exact_lookups (\d+) "
    r"zero_threshold (\d+)\s*\Z"
)


def run_range(binary: Path, columns: Path, start: int, end: int) -> tuple[int, ...]:
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
        raise AssertionError("wrong reported range")
    return values[2:]


def main() -> None:
    compiler = support8.compiler_command()
    with tempfile.TemporaryDirectory(prefix="cyclic-support10-221-unit-") as tmp:
        work = Path(tmp)
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
            raise RuntimeError(compiled.stderr)
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(run_range, binary, columns, start, end)
                for start, end in RANGES
            ]
            results = [future.result() for future in futures]

    if tuple(results) != EXPECTED:
        raise AssertionError(f"unexpected counters: {results}")
    for bounds, counters in zip(RANGES, results):
        print(f"single range {bounds[0]}:{bounds[1]}: NONE; counters={counters}")
    totals = tuple(sum(values[index] for values in results) for index in range(4))
    if totals != (2_328_439_580, 2_614_558, 2_329_004, 247_260):
        raise AssertionError(f"wrong aggregate counters: {totals}")
    print(f"aggregate counters: {totals}")
    print("case 2+2+1 all-unit stratum: PASS")
    print("consequence: case 2+2+1 is fully excluded")
    print("remaining partitions: 2+1+1+1, 1+1+1+1+1")


if __name__ == "__main__":
    main()
