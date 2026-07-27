#!/usr/bin/env python3
"""Exclude every squarefree eight-cell trade in the cyclic C17 quotient.

The Python standard library reconstructs the quotient column file.  Three
C++17 programs, each using only the C++ standard library, exhaust the five
possible distributions of four positive cells over Q-groups:

    4, 3+1, 2+2, 2+1+1, 1+1+1+1.

The first three cases are compact subset/difference lookups.  The last two
use exact sparse meet-in-the-middle searches.  A C++17 compiler is required.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile

import verify_cyclic_small_trades as small


HERE = Path(__file__).resolve().parent
COLUMN_SHA256 = "8ccea7ad608b584d117ec8970c9bef485d79c5f328da364cb93d678ee35e8ff8"

SEARCHES = (
    (
        "verify_cyclic_support8_cases_compact.cpp",
        "\n".join(
            (
                "case 4: NONE",
                "four-subsets: 163020",
                "same-signature collisions: 0",
                "case 3+1: NONE",
                "triple-pair configurations: 7824960",
                "case 2+2: NONE",
                "double-pair configurations: 978120",
                "",
            )
        ),
    ),
    (
        "verify_cyclic_support8_case_211.cpp",
        "\n".join(
            (
                "case 2+1+1: NONE",
                "double-swap configurations: 978120",
                "exact residual lookups: 118592198",
                "",
            )
        ),
    ),
    (
        "verify_cyclic_support8_case_1111.cpp",
        "\n".join(
            (
                "case 1+1+1+1: NONE",
                "second-move hits: 1204296",
                "third-move hits: 101780540",
                "exact residual lookups: 92958652",
                "",
            )
        ),
    ),
)


def write_columns(path: Path) -> None:
    q_groups, tc_columns = small.build_columns()
    q_of_cell = [-1] * len(tc_columns)
    for q, group in enumerate(q_groups):
        for cell in group:
            if q_of_cell[cell] != -1:
                raise AssertionError("cell occurs in two Q-groups")
            q_of_cell[cell] = q

    lines = [str(len(tc_columns))]
    for cell, rows in enumerate(tc_columns):
        if q_of_cell[cell] == -1 or len(rows) != 4:
            raise AssertionError("wrong quotient column structure")
        local_rows = tuple(row - 228 for row in rows)
        if not all(0 <= row < 912 for row in local_rows):
            raise AssertionError("TC row outside the expected range")
        lines.append(
            " ".join(
                map(
                    str,
                    (q_of_cell[cell], *local_rows),
                )
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="ascii")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != COLUMN_SHA256:
        raise AssertionError(f"unexpected quotient-column SHA-256: {digest}")


def compiler_command() -> list[str]:
    configured = os.environ.get("CXX")
    if configured:
        command = shlex.split(configured)
        if not command:
            raise RuntimeError("CXX is empty")
        return command
    for candidate in ("clang++", "g++", "c++"):
        resolved = shutil.which(candidate)
        if resolved:
            return [resolved]
    raise RuntimeError("a C++17 compiler is required")


def main() -> None:
    compiler = compiler_command()
    with tempfile.TemporaryDirectory(prefix="cyclic-support8-") as temporary:
        work = Path(temporary)
        columns = work / "columns.txt"
        write_columns(columns)

        for source_name, expected in SEARCHES:
            source = HERE / source_name
            binary = work / source.stem
            compiled = subprocess.run(
                (
                    *compiler,
                    "-O3",
                    "-std=c++17",
                    "-Wall",
                    "-Wextra",
                    "-pedantic",
                    str(source),
                    "-o",
                    str(binary),
                ),
                capture_output=True,
                text=True,
                timeout=180,
            )
            if compiled.returncode:
                raise RuntimeError(
                    f"failed to compile {source_name}:\n{compiled.stderr}"
                )
            completed = subprocess.run(
                (str(binary), str(columns)),
                check=True,
                capture_output=True,
                text=True,
                timeout=900,
            )
            if completed.stdout != expected:
                raise AssertionError(
                    f"unexpected output from {source_name}:\n{completed.stdout}"
                )
            print(completed.stdout, end="")

    print("cyclic quotient support-eight audit: PASS")
    print("theorem: every nonzero squarefree quotient trade has support at least 10")
    print("scope: this does not construct or exclude an exact cover or fan")


if __name__ == "__main__":
    main()
