#!/usr/bin/env python3
"""Verify the bounded layer-scan manifest and all recorded prefix CNFs."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CYCLIC = REPO / "collaboration" / "cyclic_lsts19_extension"
sys.path[:0] = [str(CYCLIC), str(REPO)]

from generate_c17_equivariant_cnf import orbit_representatives  # noqa: E402
from search_c17_equivariant_exact_cover import build_exact_cover  # noqa: E402


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def finite_cnf(
    prefix: tuple[int, ...],
    columns: dict[int, set[int]],
    rows: dict[int, tuple[int, ...]],
    blocks: tuple[tuple[int, ...], ...],
    triples: tuple[tuple[int, ...], ...],
) -> tuple[bytes, int, int]:
    covered_list = [column for row in prefix for column in rows[row]]
    assert len(covered_list) == len(set(covered_list)) == 440
    covered = set(covered_list)
    qcols = {
        index for index, block in enumerate(blocks)
        if 17 not in block and 18 not in block
    }
    stars = {
        index for index, triple in enumerate(triples)
        if 17 not in triple and 18 not in triple
    }
    demands = {
        column for column in range(228, 1140)
        if (column - 228) // 16 in stars
    }
    assert len(covered & demands) == 80
    targets = qcols | (demands - covered)
    assert len(targets) == 700
    candidates = sorted(
        row
        for qcol in qcols
        for row in columns[qcol]
        if not (set(rows[row]) & covered)
    )
    variable = {row: index + 1 for index, row in enumerate(candidates)}
    clauses: list[tuple[int, ...]] = []
    for column in sorted(targets):
        options = tuple(
            variable[row] for row in candidates if column in rows[row]
        )
        assert options
        clauses.append(options)
        clauses.extend(
            (-left, -right) for left, right in combinations(options, 2)
        )
    lines = [f"p cnf {len(candidates)} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return (
        ("\n".join(lines) + "\n").encode("ascii"),
        len(candidates),
        len(clauses),
    )


def main() -> None:
    emit = None
    if len(sys.argv) == 3 and sys.argv[1] == "--emit-finite-cnfs":
        emit = Path(sys.argv[2])
        emit.mkdir(parents=True, exist_ok=True)
    elif len(sys.argv) != 1:
        raise SystemExit(
            "usage: verify_scan_telemetry.py "
            "[--emit-finite-cnfs OUTPUT_DIRECTORY]"
        )

    manifest_path = HERE / "scan_manifest.csv"
    prefixes_path = HERE / "compatible_prefixes.json"
    receipt = json.loads((HERE / "RUN_RECEIPT.json").read_text())
    assert sha256(manifest_path.read_bytes()) == receipt["scan_manifest_sha256"]
    assert sha256(prefixes_path.read_bytes()) == receipt[
        "compatible_prefixes_sha256"
    ]

    with manifest_path.open(newline="") as handle:
        manifest = list(csv.DictReader(handle))
    assert len(manifest) == 2652
    keys = {
        (int(row["branch"]), int(row["fixed_point"])) for row in manifest
    }
    assert keys == {
        (branch, fixed)
        for branch in range(1326)
        for fixed in (17, 18)
    }
    counts = Counter(row["status"] for row in manifest)
    assert counts == Counter({"UNKNOWN": 2485, "SAT": 167})
    assert all(
        len(row["witness_sha256"]) == 64
        and set(row["witness_sha256"]) <= set("0123456789abcdef")
        for row in manifest
    )
    assert receipt["status_counts"] == dict(counts)
    assert receipt["full_exact_covers_found"] == 0

    columns, rows = build_exact_cover()
    blocks = orbit_representatives(4)
    triples = orbit_representatives(3)
    branches = [
        tuple(map(int, line.split()))
        for line in (
            CYCLIC / "c17_type_i_branches.txt"
        ).read_text().splitlines()
    ]
    assert len(branches) == 1326
    q_both = {
        index for index, block in enumerate(blocks)
        if 17 in block and 18 in block
    }
    q_left = {
        index for index, block in enumerate(blocks)
        if 17 in block and 18 not in block
    }
    q_infinity = {
        index for index, block in enumerate(blocks)
        if 18 in block and 17 not in block
    }
    q_finite = {
        index for index, block in enumerate(blocks)
        if 17 not in block and 18 not in block
    }
    assert tuple(map(len, (q_both, q_left, q_infinity, q_finite))) == (
        8, 40, 40, 140
    )

    prefix_data = json.loads(prefixes_path.read_text())
    records = prefix_data["prefixes"]
    assert len(records) == 19
    assert len({record["id"] for record in records}) == 19
    for record in records:
        branch_index = record["mixed_branch_index"]
        mixed = tuple(record["mixed_rows"])
        left = tuple(record["left_rows"])
        infinity = tuple(record["infinity_rows"])
        assert mixed == branches[branch_index]
        assert (len(mixed), len(left), len(infinity)) == (8, 40, 40)
        assert all((row - 1) // 17 in q_both for row in mixed)
        assert all((row - 1) // 17 in q_left for row in left)
        assert all((row - 1) // 17 in q_infinity for row in infinity)
        content, variables, clauses = finite_cnf(
            mixed + left + infinity,
            columns,
            rows,
            blocks,
            triples,
        )
        finite = record["finite_completion"]
        assert finite["status"] == "UNSATISFIABLE_TELEMETRY"
        assert finite["target_columns"] == 700
        assert finite["variables"] == variables
        assert finite["clauses"] == clauses
        assert finite["cnf_sha256"] == sha256(content)
        if emit is not None:
            (emit / f'{record["id"]}.cnf').write_bytes(content)

    assert receipt["compatible_prefixes"] == 19
    assert receipt["finite_status_counts"] == {
        "UNSATISFIABLE_TELEMETRY": 19
    }
    print("1,326 branches x 2 layers represented exactly once: PASS")
    print("layer status census SAT=167, UNKNOWN=2,485: PASS")
    print("manifest and compatible-prefix digests: PASS")
    print("19 compatible 88-row prefixes reconstructed: PASS")
    print("19 finite-stage CNF hashes reconstructed: PASS")
    print("full exact covers found: 0")
    print(
        "scope: bounded telemetry only; every timeout is UNKNOWN and "
        "no global UNSAT conclusion is made"
    )


if __name__ == "__main__":
    main()
