#!/usr/bin/env python3
"""Verify five complete support-12 Q-multiplicity partitions."""

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
EXPECTED_411 = (
    (241007804, 510402), (244684440, 518588),
    (244504260, 519064), (242342124, 511808),
    (242625220, 513308), (241969692, 511566),
    (241365300, 512174), (243243000, 515368),
    (243963720, 517338), (238355128, 503864),
    (239265288, 507988), (229940176, 487122),
)
PATTERN_411 = re.compile(
    r"NONE q (\d+):(\d+) configs (\d+) first (\d+) probes (\d+) "
    r"low_hits (\d+) hash_hits (\d+) exact_checks (\d+)\s*\Z"
)


def compile_source(compiler: list[str], source: Path, binary: Path) -> None:
    completed = subprocess.run(
        (*compiler, "-O3", "-std=c++17", str(source), "-o", str(binary)),
        capture_output=True, text=True, timeout=180,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr)


def run_411(binary: Path, columns: Path, start: int, end: int) -> tuple[int, ...]:
    completed = subprocess.run(
        (str(binary), str(columns), str(start), str(end)),
        check=True, capture_output=True, text=True, timeout=900,
    )
    match = PATTERN_411.fullmatch(completed.stdout)
    if match is None:
        raise AssertionError(f"unexpected case 4+1+1 output:\n{completed.stdout}")
    values = tuple(map(int, match.groups()))
    if values[:2] != (start, end):
        raise AssertionError("wrong Q range")
    return values[2:]


def main() -> None:
    compiler = support8.compiler_command()
    with tempfile.TemporaryDirectory(prefix="cyclic-support12-") as temporary:
        work = Path(temporary)
        columns = work / "columns.txt"
        support8.write_columns(columns)
        binaries = {}
        for stem in ("verify_cases6_51", "verify_cases42_33", "verify_case411"):
            binary = work / stem
            compile_source(compiler, HERE / f"{stem}.cpp", binary)
            binaries[stem] = binary

        first = subprocess.run(
            (str(binaries["verify_cases6_51"]), str(columns)),
            check=True, capture_output=True, text=True, timeout=900,
        ).stdout
        expected_first = (
            "NONE case6 subsets 391248 collisions 0 "
            "case51 configs 16432416 bounded 14211626\n"
        )
        if first != expected_first:
            raise AssertionError(f"unexpected cases 6/5+1 output:\n{first}")
        print(first, end="")

        second = subprocess.run(
            (str(binaries["verify_cases42_33"]), str(columns)),
            check=True, capture_output=True, text=True, timeout=900,
        ).stdout
        expected_second = (
            "NONE doubles 978120 case42 20540520 bounded 20540520 "
            "case33 7824960 vectors 7824960\n"
        )
        if second != expected_second:
            raise AssertionError(f"unexpected cases 4+2/3+3 output:\n{second}")
        print(second, end="")

        with ThreadPoolExecutor(max_workers=12) as executor:
            results = list(
                executor.map(
                    lambda bounds: run_411(
                        binaries["verify_case411"], columns, *bounds
                    ),
                    RANGES,
                )
            )

    for index, (bounds, values) in enumerate(zip(RANGES, results)):
        first_hits, low_hits = EXPECTED_411[index]
        expected = (1_711_710, first_hits, first_hits, low_hits, 0, 0)
        if values != expected:
            raise AssertionError(f"wrong case 4+1+1 counters {bounds}: {values}")
        print(f"case 4+1+1 Q range {bounds[0]}:{bounds[1]}: NONE")
    totals = tuple(sum(row[index] for row in results) for index in range(6))
    expected_totals = (20_540_520, 2_893_266_152, 2_893_266_152, 6_128_590, 0, 0)
    if totals != expected_totals:
        raise AssertionError(f"wrong case 4+1+1 totals: {totals}")
    print(f"case 4+1+1 aggregate counters: {totals}")
    print("support-12 partial audit: PASS")
    print("excluded complete partitions: 6, 5+1, 4+2, 3+3, 4+1+1")
    print("scope: six support-12 partitions remain unexplored")


if __name__ == "__main__":
    main()
