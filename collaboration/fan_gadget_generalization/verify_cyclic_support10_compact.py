#!/usr/bin/env python3
"""Exclude the one- and two-Q-group cases at squarefree support ten."""

from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile

import verify_cyclic_support8 as support8


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_cyclic_support10_compact.cpp"
EXPECTED = "\n".join(
    (
        "case 5: NONE",
        "five-subsets: 293436",
        "same-signature collisions: 0",
        "case 4+1: NONE",
        "four-pair configurations: 20540520",
        "unit-bounded four-pair vectors: 18091188",
        "case 3+2: NONE",
        "triple-pair configurations: 7824960",
        "double-bounded triple-pair vectors: 7824960",
        "consequence: any support-10 trade spans at least three Q-groups",
        "",
    )
)


def main() -> None:
    compiler = support8.compiler_command()
    with tempfile.TemporaryDirectory(prefix="cyclic-support10-") as temporary:
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
            raise RuntimeError(f"failed to compile verifier:\n{compiled.stderr}")
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

    print("cyclic quotient compact support-ten audit: PASS")
    print(
        "remaining partitions: 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1"
    )
    print("scope: support ten is not fully excluded")


if __name__ == "__main__":
    main()
