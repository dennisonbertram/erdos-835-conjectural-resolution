#!/usr/bin/env python3
"""Reproduce and audit the committed K7 WW-switch CNF/DRAT certificate."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import subprocess
import tempfile
from pathlib import Path

from generate_certificate import build


ROOT = Path(__file__).resolve().parent
CNF_GZ = ROOT / "certificate" / "k7_ww_switch.cnf.gz"
DRAT_GZ = ROOT / "certificate" / "k7_ww_switch.drat.gz"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()

    expected_cnf = build().text().encode("ascii")
    with gzip.open(CNF_GZ, "rb") as stream:
        committed_cnf = stream.read()
    assert committed_cnf == expected_cnf
    print("PASS exact CNF reconstruction", digest(committed_cnf))

    with gzip.open(DRAT_GZ, "rb") as stream:
        committed_drat = stream.read()
    assert committed_drat
    print("PASS DRAT payload", len(committed_drat), digest(committed_drat))

    if args.drat_trim:
        with tempfile.TemporaryDirectory(prefix="k7-ww-audit-") as directory:
            directory = Path(directory)
            cnf_path = directory / "instance.cnf"
            drat_path = directory / "proof.drat"
            cnf_path.write_bytes(committed_cnf)
            drat_path.write_bytes(committed_drat)
            result = subprocess.run(
                [str(args.drat_trim), str(cnf_path), str(drat_path)],
                check=False,
                text=True,
                capture_output=True,
            )
            output = result.stdout + result.stderr
            assert result.returncode == 0, output
            assert "s VERIFIED" in output, output
            print("PASS independent DRAT-trim verification")


if __name__ == "__main__":
    main()
