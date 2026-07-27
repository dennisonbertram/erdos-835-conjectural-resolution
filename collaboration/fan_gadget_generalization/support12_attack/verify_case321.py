#!/usr/bin/env python3
"""Exclude the support-12 partition 3+2+1."""

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
    (91991144,4975484360,10546070,5216188),
    (93213240,5070110100,10737636,5279128),
    (93144560,5060666600,10723836,5283336),
    (92320888,5015361340,10621168,5230652),
    (92607640,5026412380,10650954,5243440),
    (92189120,4960795400,10501568,5224390),
    (92127260,4994311190,10574896,5221834),
    (92664168,5028585540,10646416,5245366),
    (92938600,5032347100,10664414,5266204),
    (91033016,4901476580,10393064,5152214),
    (91323500,4918460030,10426302,5168026),
    (88111636,4657412650,9866620,4985022),
)
PATTERN = re.compile(
    r"NONE q (\d+):(\d+) configs (\d+) single_probes (\d+) "
    r"double_probes (\d+) single_low (\d+) double_low (\d+) "
    r"single_hash (\d+) double_hash (\d+) exact_checks (\d+)\s*\Z"
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
    with tempfile.TemporaryDirectory(prefix="cyclic-support12-321-") as tmp:
        work = Path(tmp)
        columns = work / "columns.txt"
        binary = work / "verify_case321"
        support8.write_columns(columns)
        compiled = subprocess.run(
            (*compiler, "-O3", "-std=c++17", str(HERE / "verify_case321.cpp"),
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
        expected = (652080, *EXPECTED[index], 0, 0, 0)
        if values != expected:
            raise AssertionError(f"wrong counters {bounds}: {values}")
        print(f"Q range {bounds[0]}:{bounds[1]}: NONE")
    totals = tuple(sum(row[index] for row in results) for index in range(8))
    expected_totals = (
        7824960, 1103664772, 59641423270, 126352944, 62515800, 0, 0, 0,
    )
    if totals != expected_totals:
        raise AssertionError(f"wrong totals: {totals}")
    print(f"aggregate counters: {totals}")
    print("case 3+2+1: NONE")
    print("support-12 partition 3+2+1 audit: PASS")
    print("scope: three support-12 partitions remain unexplored")


if __name__ == "__main__":
    main()
