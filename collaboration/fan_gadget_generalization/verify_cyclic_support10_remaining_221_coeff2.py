#!/usr/bin/env python3
"""Exclude the coefficient-two stratum of support-ten case 2+2+1."""

from pathlib import Path
import subprocess
import tempfile

import verify_cyclic_support8 as support8


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_cyclic_support10_remaining_221_coeff2.cpp"
EXPECTED = (
    "NONE coeff2_double_swaps 33642 "
    "candidate_double_checks 234386020 "
    "exact_single_lookups 104226058\n"
)


def main() -> None:
    compiler = support8.compiler_command()
    with tempfile.TemporaryDirectory(prefix="cyclic-support10-221-") as temporary:
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
            raise RuntimeError(compiled.stderr)
        completed = subprocess.run(
            (str(binary), str(columns)),
            check=True,
            capture_output=True,
            text=True,
            timeout=900,
        )
        if completed.stdout != EXPECTED:
            raise AssertionError(f"unexpected output:\n{completed.stdout}")
        print(completed.stdout, end="")
    print("case 2+2+1 coefficient-two stratum: PASS")
    print("consequence: both double-swap vectors in any candidate are unit-valued")
    print("scope: the all-unit 2+2+1 stratum remains open")


if __name__ == "__main__":
    main()
