#!/usr/bin/env python3
"""Verify the exact 132-row finite packing and omit-one CNF telemetry."""

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


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def make_omit_one_encoding(
    columns: dict[int, set[int]],
    rows: dict[int, tuple[int, ...]],
    qcols: tuple[int, ...],
    demands: tuple[int, ...],
) -> tuple[bytes, dict[int, bytes], dict[int, bytes], int, int]:
    """Precompute byte-exact clause blocks shared by all omit-one CNFs."""
    candidates = tuple(sorted(row for qcol in qcols for row in columns[qcol]))
    variable = {row: index + 1 for index, row in enumerate(candidates)}

    at_least_q: dict[int, tuple[int, ...]] = {}
    at_most_q: dict[int, list[tuple[int, int]]] = {}
    for qcol in qcols:
        options = tuple(variable[row] for row in sorted(columns[qcol]))
        at_least_q[qcol] = options
        at_most_q[qcol] = [
            (-left, -right) for left, right in combinations(options, 2)
        ]

    demand_clauses: list[tuple[int, ...]] = []
    for demand in demands:
        options = tuple(
            variable[row] for row in candidates if demand in rows[row]
        )
        demand_clauses.extend(
            (-left, -right) for left, right in combinations(options, 2)
        )

    def encode(clauses: list[tuple[int, ...]]) -> bytes:
        return b"".join(
            (" ".join(map(str, clause)) + " 0\n").encode("ascii")
            for clause in clauses
        )

    demand_blob = encode(demand_clauses)
    present_blocks: dict[int, bytes] = {}
    omitted_blocks: dict[int, bytes] = {}
    for qcol in qcols:
        present_blocks[qcol] = encode(
            at_most_q[qcol] + [at_least_q[qcol]]
        )
        omitted_blocks[qcol] = encode(
            at_most_q[qcol]
            + [(-value,) for value in at_least_q[qcol]]
        )
    variables = len(candidates)
    clauses = (
        len(demand_clauses)
        + sum(len(at_most_q[qcol]) + 1 for qcol in qcols)
        - 1
        + 13
    )
    header = f"p cnf {variables} {clauses}\n".encode("ascii")
    return header + demand_blob, present_blocks, omitted_blocks, variables, clauses


def omit_one_digest(
    omitted: int,
    common: bytes,
    present_blocks: dict[int, bytes],
    omitted_blocks: dict[int, bytes],
    qcols: tuple[int, ...],
) -> str:
    """Hash the byte-exact CNF without materializing 140 large strings."""
    digest = hashlib.sha256()
    digest.update(common)
    for qcol in qcols:
        digest.update(
            omitted_blocks[qcol] if qcol == omitted else present_blocks[qcol]
        )
    return digest.hexdigest()


def main() -> None:
    packing_path = HERE / "packing.json"
    manifest_path = HERE / "omit_one_manifest.csv"
    receipt_path = HERE / "RUN_RECEIPT.json"

    packing = json.loads(packing_path.read_text())
    receipt = json.loads(receipt_path.read_text())
    assert sha256(packing_path.read_bytes()) == receipt["packing_sha256"]
    assert sha256(manifest_path.read_bytes()) == receipt[
        "omit_one_manifest_sha256"
    ]

    columns, rows = build_exact_cover()
    blocks = orbit_representatives(4)
    triples = orbit_representatives(3)
    qcols = tuple(
        sorted(
            index
            for index, block in enumerate(blocks)
            if 17 not in block and 18 not in block
        )
    )
    stars = {
        index
        for index, triple in enumerate(triples)
        if 17 not in triple and 18 not in triple
    }
    demands = tuple(
        column
        for column in range(228, 1140)
        if (column - 228) // 16 in stars
    )
    assert (len(qcols), len(stars), len(demands)) == (140, 40, 640)

    selected = tuple(packing["selected_rows"])
    assert packing["schema"] == "erdos835-c17-finite-packing-v1"
    assert packing["claim"] == "alpha_finite >= 132"
    assert packing["size"] == len(selected) == 132
    assert len(set(selected)) == 132

    selected_qcols = []
    covered_demands = []
    covered_columns = []
    qcol_set = set(qcols)
    demand_set = set(demands)
    for row in selected:
        assert row in rows
        row_columns = rows[row]
        row_qcols = qcol_set & set(row_columns)
        row_demands = demand_set & set(row_columns)
        assert len(row_columns) == 5
        assert len(row_qcols) == 1
        assert len(row_demands) == 4
        selected_qcols.extend(row_qcols)
        covered_demands.extend(row_demands)
        covered_columns.extend(row_columns)

    assert len(selected_qcols) == len(set(selected_qcols)) == 132
    assert len(covered_demands) == len(set(covered_demands)) == 528
    assert len(covered_columns) == len(set(covered_columns)) == 660

    with manifest_path.open(newline="") as handle:
        manifest = list(csv.DictReader(handle))
    assert len(manifest) == 140
    assert {int(record["omitted_q"]) for record in manifest} == set(qcols)
    assert Counter(record["status"] for record in manifest) == Counter(
        {"UNKNOWN": 140}
    )

    common, present_blocks, omitted_blocks, variables, clauses = (
        make_omit_one_encoding(columns, rows, qcols, demands)
    )
    output_digest = sha256(b"c UNKNOWN\n")
    for record in manifest:
        omitted = int(record["omitted_q"])
        assert int(record["seed"]) == 13001 + omitted
        assert int(record["wall_limit_seconds"]) == 30
        assert int(record["variables"]) == variables == 1820
        assert int(record["clauses"]) == clauses == 48928
        assert record["cnf_sha256"] == omit_one_digest(
            omitted,
            common,
            present_blocks,
            omitted_blocks,
            qcols,
        )
        assert record["solver_output_sha256"] == output_digest

    assert receipt["alpha_finite_lower_bound"] == 132
    assert receipt["alpha_finite_upper_bound"] == 140
    assert receipt["upper_bound_kind"] == "TRIVIAL"
    assert receipt["omit_one_status_counts"] == {"UNKNOWN": 140}
    assert receipt["omit_one_runs"] == 140
    assert receipt["omit_one_wall_limit_seconds_each"] == 30

    print("finite quotient counts 140 Q, 40 stars, 640 demands: PASS")
    print("132 distinct finite Q rows reconstructed: PASS")
    print("528 finite demands collision-free: PASS")
    print("660 total covered columns pairwise distinct: PASS")
    print("alpha_finite >= 132: PROVED")
    print("140 omit-one CNF hashes reconstructed: PASS")
    print("omit-one bounded status census UNKNOWN=140: PASS")
    print("scope: alpha_finite >= 132 only; upper bound remains the trivial 140")


if __name__ == "__main__":
    main()
