#!/usr/bin/env python3
"""Audit the bounded EH retain-11/drop-four reconnaissance sample."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

from drop_four_point_link_cnf import (
    N_CLAUSES,
    N_COLOURS,
    N_TRIPLES,
    N_VARIABLES,
    build_instance,
    clauses_for,
)
from point_link_cnf import load_source
from screen_drop_four_samples import (
    EXPECTED_STRUCTURAL_CELLS,
    POINT,
    RECEIPT_SCHEMA,
    SAMPLE_DROPS,
    SCHEMA,
    construction_pack_multiplicity,
    full_top_count,
)


def semantic_colour_check(
    triples: tuple[tuple[int, int, int], ...],
    by_pair: dict[tuple[int, int], tuple[int, ...]],
    colours: tuple[int, ...],
) -> None:
    if len(colours) != N_TRIPLES or not set(colours) <= set(range(N_COLOURS)):
        raise AssertionError("stored SAT colour vector has invalid shape")
    for pair, rows in by_pair.items():
        if {colours[row] for row in rows} != set(range(N_COLOURS)):
            raise AssertionError(f"stored SAT witness is not rainbow on pair {pair}")
    for colour in range(N_COLOURS):
        selected = [
            triples[row] for row, value in enumerate(colours) if value == colour
        ]
        if len(selected) != 57:
            raise AssertionError("stored SAT witness has a wrong colour-class size")
        covered = Counter(
            pair for triple in selected for pair in itertools.combinations(triple, 2)
        )
        if set(covered) != set(by_pair) or set(covered.values()) != {1}:
            raise AssertionError("stored SAT colour class is not an STS(19)")


def cnf_digest(clauses: list[tuple[int, ...]]) -> str:
    text = [f"p cnf {N_VARIABLES} {len(clauses)}\n"]
    text.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return hashlib.sha256("".join(text).encode("ascii")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    raw_results = args.results.read_bytes()
    rows = [
        json.loads(line)
        for line in raw_results.decode("ascii").splitlines()
        if line.strip()
    ]
    if len(rows) != len(SAMPLE_DROPS):
        raise AssertionError("sample results have the wrong row count")
    keys = [tuple(map(int, row["drop"])) for row in rows]
    if set(keys) != set(SAMPLE_DROPS) or len(keys) != len(set(keys)):
        raise AssertionError("sample result drops do not equal the intended set")

    _, systems = load_source()
    seen_cells: set[tuple[tuple[int, ...], int]] = set()
    for row in rows:
        drop = tuple(map(int, row["drop"]))
        if row.get("schema") != SCHEMA or row.get("point") != POINT:
            raise AssertionError(f"{drop}: bad schema or point")
        cell = (construction_pack_multiplicity(drop), full_top_count(systems, drop))
        if row.get("construction_pack_multiplicity") != list(cell[0]):
            raise AssertionError(f"{drop}: construction-pack multiplicity mismatch")
        if row.get("full_top_count") != cell[1]:
            raise AssertionError(f"{drop}: full-top count mismatch")
        seen_cells.add(cell)

        if (
            row.get("cnf_variables") != N_VARIABLES
            or row.get("cnf_clauses") != N_CLAUSES
        ):
            raise AssertionError(f"{drop}: wrong CNF dimensions")
        triples, by_pair = build_instance(systems, drop, POINT)
        if cnf_digest(clauses_for(triples, by_pair)) != row.get("cnf_sha256"):
            raise AssertionError(f"{drop}: regenerated CNF hash mismatch")

        status = row.get("status")
        return_code = row.get("cadical_returncode")
        colours_value = row.get("colours")
        colour_hash = row.get("colour_sha256")
        if status == "SAT_VERIFIED":
            if return_code != 10 or not isinstance(colours_value, list):
                raise AssertionError(f"{drop}: malformed SAT row")
            colours = tuple(map(int, colours_value))
            semantic_colour_check(triples, by_pair, colours)
            if hashlib.sha256(bytes(colours)).hexdigest() != colour_hash:
                raise AssertionError(f"{drop}: SAT colour hash mismatch")
        elif status == "UNSAT_RECONNAISSANCE":
            if (
                return_code != 20
                or colours_value is not None
                or colour_hash is not None
            ):
                raise AssertionError(f"{drop}: malformed UNSAT reconnaissance row")
        elif status == "UNKNOWN":
            if (
                return_code in {10, 20}
                or colours_value is not None
                or colour_hash is not None
            ):
                raise AssertionError(f"{drop}: malformed UNKNOWN row")
        else:
            raise AssertionError(f"{drop}: unknown status {status!r}")

        elapsed = row.get("elapsed_seconds")
        if not isinstance(elapsed, (int, float)) or elapsed < 0:
            raise AssertionError(f"{drop}: invalid elapsed time")

    if seen_cells != EXPECTED_STRUCTURAL_CELLS:
        raise AssertionError("sample does not cover the intended structural cells")

    receipt = json.loads(args.receipt.read_text(encoding="ascii"))
    elapsed = [float(row["elapsed_seconds"]) for row in rows]
    census = dict(sorted(Counter(str(row["status"]) for row in rows).items()))
    expected_receipt_fields = {
        "schema": RECEIPT_SCHEMA,
        "row_schema": SCHEMA,
        "cases": len(SAMPLE_DROPS),
        "point": POINT,
        "cadical_version": "3.0.1",
        "census": census,
        "total_solver_seconds": round(sum(elapsed), 6),
        "minimum_solver_seconds": min(elapsed),
        "maximum_solver_seconds": max(elapsed),
        "results_path": args.results.name,
        "results_sha256": hashlib.sha256(raw_results).hexdigest(),
    }
    for field, value in expected_receipt_fields.items():
        if receipt.get(field) != value:
            raise AssertionError(f"sample receipt field {field!r} mismatch")
    if receipt.get("seconds_per_case") != 30:
        raise AssertionError("sample receipt has an unexpected time bound")
    expected_cells_json = [
        {
            "construction_pack_multiplicity": list(multiplicity),
            "full_top_count": tops,
        }
        for multiplicity, tops in sorted(EXPECTED_STRUCTURAL_CELLS)
    ]
    if receipt.get("structural_cells") != expected_cells_json:
        raise AssertionError("sample receipt structural-cell list mismatch")

    print(f"[ok] audited {len(rows)} intended point-0 drop-four sample cases")
    print(f"[ok] structural cells: {len(seen_cells)}")
    print(f"[exact] status census: {census}")
    print(f"[exact] results SHA-256: {hashlib.sha256(raw_results).hexdigest()}")
    if census.get("SAT_VERIFIED", 0):
        print("[theorem] every SAT row stores six semantically verified STS(19)s")
    if census.get("UNSAT_RECONNAISSANCE", 0):
        print("[scope] UNSAT reconnaissance rows are not portable theorems")
    if census.get("UNKNOWN", 0):
        print("[scope] UNKNOWN rows carry no satisfiability conclusion")
    print("status: PASS")


if __name__ == "__main__":
    main()
