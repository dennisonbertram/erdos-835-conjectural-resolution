#!/usr/bin/env python3
"""Aggregate theorem gate for all 455 EH retain-twelve cases.

This orchestrates the independent ten-point, legacy DRAT, batch DRAT, and
three-pack verifiers, then checks that their exclusion routes partition all
C(15,3) drop triples with no overlap or gap.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

from certify_point_links import file_sha256, load_recon


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TEN_POINT_VERIFIER = (
    REPO
    / "collaboration"
    / "eh_core_symmetry_orbits"
    / "verify_eh_core_symmetry_orbits.py"
)
LEGACY_VERIFIER = HERE / "verify_point_link_certificate.py"
BATCH_VERIFIER = HERE / "verify_certificate_manifest.py"
LOWER_BOUND_VERIFIER = HERE / "verify_three_pack_lower_bound.py"
SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_seed.txt"

TEN_POINT_PACKS = (
    frozenset(range(0, 5)),
    frozenset(range(5, 10)),
    frozenset(range(10, 15)),
)
LEGACY_DROPS = {
    (0, 1, 5),
    (0, 5, 10),
}
RECEIPT_SCHEMA = "eh-point-link-all-455-gate-v2"
RECON_RECEIPT_SCHEMA = "eh-point-link-recon-receipt-v1"
EXPECTED_SOURCE_SHA256 = (
    "b1ea090d3e3b88366c87e95660c1c82a406d2c3b100cc1d39bcc2c7e8fde47f9"
)
EXPECTED_CHECKER_ID = "drat-trim@2e3b2dc0ecf938addbd779d42877b6ed69d9a985"


def run_gate(command: list[str], required_fragments: tuple[str, ...]) -> str:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    transcript = completed.stdout + completed.stderr
    print(transcript, end="")
    if completed.returncode != 0:
        raise AssertionError(
            f"gate command returned {completed.returncode}: {' '.join(command)}"
        )
    for fragment in required_fragments:
        if fragment not in transcript:
            raise AssertionError(
                f"gate command lacks {fragment!r}: {' '.join(command)}"
            )
    return transcript


def atomic_json(path: Path, value: dict[str, object]) -> None:
    content = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("ascii")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("wb") as output:
        output.write(content)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def transcript_value(transcript: str, prefix: str) -> str:
    matches = [
        line.removeprefix(prefix).strip()
        for line in transcript.splitlines()
        if line.startswith(prefix)
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"expected one transcript line beginning {prefix!r}, got {len(matches)}"
        )
    return matches[0]


def load_and_validate_recon_receipt(
    path: Path,
    recon_path: Path,
    recon_rows: list[dict[str, object]],
) -> dict[str, object]:
    receipt = json.loads(path.read_text(encoding="ascii"))
    census = dict(sorted(Counter(str(row["status"]) for row in recon_rows).items()))
    elapsed = [float(row["elapsed_seconds"]) for row in recon_rows]
    expected = {
        "schema": RECON_RECEIPT_SCHEMA,
        "row_schema": "eh-point-link-recon-v1",
        "cases": 423,
        "expected_drop_cases": 423,
        "point": 0,
        "census": census,
        "total_solver_seconds": round(sum(elapsed), 6),
        "minimum_solver_seconds": min(elapsed),
        "maximum_solver_seconds": max(elapsed),
        "jsonl_path": recon_path.name,
        "jsonl_sha256": file_sha256(recon_path),
    }
    for field, value in expected.items():
        if receipt.get(field) != value:
            raise AssertionError(
                f"recon summary field {field!r} is {receipt.get(field)!r}, "
                f"expected {value!r}"
            )
    for field in ("seconds_per_case", "jobs"):
        value = receipt.get(field)
        if not isinstance(value, int) or value <= 0:
            raise AssertionError(f"recon summary has invalid {field!r}")
    print("[ok] reconnaissance summary receipt matches all 423 committed rows")
    return receipt


def main() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit(
            "the aggregate gate requires Python 3.10+ because the existing "
            "ten-point verifier uses int.bit_count()"
        )
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-recon", type=Path, required=True)
    parser.add_argument("--batch-recon-receipt", type=Path)
    parser.add_argument("--batch-manifest", type=Path, required=True)
    parser.add_argument("--batch-base-dir", type=Path, required=True)
    parser.add_argument("--drat-trim", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    all_drops = set(itertools.combinations(range(15), 3))
    ten_point = {
        drop for drop in all_drops if any(set(drop) <= pack for pack in TEN_POINT_PACKS)
    }
    if len(ten_point) != 30:
        raise AssertionError("ten-point route does not contain 30 cases")

    recon_rows = load_recon(args.batch_recon, expected_rows=423)
    for row in recon_rows:
        if row["point"] != 0 or row["status"] != "UNSAT_RECONNAISSANCE":
            raise AssertionError(
                "every batch row must be a point-0 UNSAT reconnaissance case"
            )
    recon_receipt_path = args.batch_recon_receipt
    if recon_receipt_path is None:
        recon_receipt_path = args.batch_recon.with_name(
            f"{args.batch_recon.stem}_receipt.json"
        )
    recon_receipt = load_and_validate_recon_receipt(
        recon_receipt_path,
        args.batch_recon,
        recon_rows,
    )
    batch = {tuple(row["drop"]) for row in recon_rows}
    if len(batch) != 423:
        raise AssertionError("batch route does not contain 423 cases")
    routes = {
        "ten_point": ten_point,
        "legacy_drat": LEGACY_DROPS,
        "batch_drat": batch,
    }
    for left_name, right_name in itertools.combinations(routes, 2):
        overlap = routes[left_name] & routes[right_name]
        if overlap:
            raise AssertionError(
                f"coverage overlap between {left_name} and {right_name}: "
                f"{sorted(overlap)}"
            )
    covered = set().union(*routes.values())
    if covered != all_drops:
        raise AssertionError(
            f"coverage mismatch: missing={sorted(all_drops - covered)} "
            f"extra={sorted(covered - all_drops)}"
        )
    print("[ok] coverage routes partition all 455 drops as 30 + 2 + 423")

    python = sys.executable
    run_gate(
        [python, "-B", str(TEN_POINT_VERIFIER)],
        (
            "[scope] 30 of 455 EH drop-three repair cases are excluded",
            "status: PASS",
        ),
    )
    run_gate(
        [
            python,
            "-B",
            str(LEGACY_VERIFIER),
            "--drat-trim",
            args.drat_trim,
        ],
        (
            "(0, 1, 5) independent drat-trim replay returns s VERIFIED",
            "(0, 5, 10) independent drat-trim replay returns s VERIFIED",
            "status: PASS",
        ),
    )
    batch_transcript = run_gate(
        [
            python,
            "-B",
            str(BATCH_VERIFIER),
            "--recon",
            str(args.batch_recon),
            "--manifest",
            str(args.batch_manifest),
            "--base-dir",
            str(args.batch_base_dir),
            "--drat-trim",
            args.drat_trim,
            "--require-complete",
            "--expected-recon-rows",
            "423",
        ],
        (
            "[exact] recon census: {'UNSAT_RECONNAISSANCE': 423}",
            "[exact] manifest rows: 423",
            "[ok] every checked CNF was independently reconstructed byte-for-byte",
            "[ok] every UNSAT reconnaissance row has a certificate",
            "status: PASS",
        ),
    )
    lower_bound_transcript = run_gate(
        [python, "-B", str(LOWER_BOUND_VERIFIER)],
        (
            "all 455 point-0 leaves contain the three discarded STS(19)s",
            "status: PASS",
        ),
    )

    manifest_rows = [
        json.loads(line)
        for line in args.batch_manifest.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    if len(manifest_rows) != 423:
        raise AssertionError("batch manifest does not have 423 rows")
    manifest_keys = {(tuple(row["drop"]), int(row["point"])) for row in manifest_rows}
    if manifest_keys != {(drop, 0) for drop in batch}:
        raise AssertionError("batch manifest keys do not match batch recon keys")
    checker_ids = {str(row["checker_id"]) for row in manifest_rows}
    cadical_versions = {str(row["cadical_version"]) for row in manifest_rows}
    if checker_ids != {EXPECTED_CHECKER_ID}:
        raise AssertionError(f"unexpected checker IDs: {checker_ids}")
    if cadical_versions != {"3.0.1"}:
        raise AssertionError(f"unexpected CaDiCaL versions: {cadical_versions}")

    bundle_digest = hashlib.sha256()
    total_compressed_bytes = 0
    largest_compressed_bytes = 0
    for row in sorted(manifest_rows, key=lambda value: (value["drop"], value["point"])):
        drop = tuple(map(int, row["drop"]))
        point = int(row["point"])
        compressed_bytes = int(row["compressed_proof_bytes"])
        total_compressed_bytes += compressed_bytes
        largest_compressed_bytes = max(largest_compressed_bytes, compressed_bytes)
        bundle_digest.update(bytes(drop))
        bundle_digest.update(point.to_bytes(1, "big"))
        bundle_digest.update(bytes.fromhex(str(row["cnf_sha256"])))
        bundle_digest.update(bytes.fromhex(str(row["compressed_proof_sha256"])))
    bundle_digest_hex = bundle_digest.hexdigest()
    if (
        int(
            transcript_value(
                batch_transcript,
                "[exact] compressed proof bytes checked:",
            )
        )
        != total_compressed_bytes
    ):
        raise AssertionError("batch verifier compressed-byte total mismatch")
    if (
        transcript_value(
            batch_transcript,
            "[exact] certificate bundle digest:",
        )
        != bundle_digest_hex
    ):
        raise AssertionError("batch verifier bundle digest mismatch")
    canonical_three_pack_digest = transcript_value(
        lower_bound_transcript,
        "[exact] canonical three-pack digest:",
    )
    if len(canonical_three_pack_digest) != 64:
        raise AssertionError("canonical three-pack digest is malformed")
    if file_sha256(SOURCE) != EXPECTED_SOURCE_SHA256:
        raise AssertionError("authenticated EH seed hash mismatch")

    coverage_digest = hashlib.sha256()
    for route, drops in sorted(routes.items()):
        for drop in sorted(drops):
            coverage_digest.update(route.encode("ascii") + b"\0")
            coverage_digest.update(bytes(drop))
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "coverage": {route: len(drops) for route, drops in routes.items()},
        "coverage_total": len(covered),
        "coverage_digest": coverage_digest.hexdigest(),
        "batch_recon_sha256": file_sha256(args.batch_recon),
        "batch_recon_receipt_sha256": file_sha256(recon_receipt_path),
        "batch_manifest_sha256": file_sha256(args.batch_manifest),
        "batch_certificate_count": len(manifest_rows),
        "batch_compressed_proof_bytes": total_compressed_bytes,
        "batch_largest_compressed_proof_bytes": largest_compressed_bytes,
        "batch_certificate_bundle_digest": bundle_digest_hex,
        "batch_recon_summary": {
            "census": recon_receipt["census"],
            "maximum_solver_seconds": recon_receipt["maximum_solver_seconds"],
            "minimum_solver_seconds": recon_receipt["minimum_solver_seconds"],
            "total_solver_seconds": recon_receipt["total_solver_seconds"],
        },
        "canonical_three_pack_cases": 455,
        "canonical_three_pack_digest": canonical_three_pack_digest,
        "point_link_packing_number_exactly_three_cases": 425,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "solver_versions": sorted(cadical_versions),
        "checker_ids": sorted(checker_ids),
        "legacy_evidence_sha256": {
            "drop_0_1_5_point_0.cnf": file_sha256(HERE / "drop_0_1_5_point_0.cnf"),
            "drop_0_1_5_point_0.drat.gz": file_sha256(
                HERE / "drop_0_1_5_point_0.drat.gz"
            ),
            "drop_0_5_10_point_0.cnf": file_sha256(HERE / "drop_0_5_10_point_0.cnf"),
            "drop_0_5_10_point_0.drat.gz": file_sha256(
                HERE / "drop_0_5_10_point_0.drat.gz"
            ),
        },
        "all_independent_gates_passed": True,
        "theorem": (
            "Every twelve-system subfamily of the EH 15-core is excluded; "
            "therefore any LS(3,4,20) shares at most eleven EH systems."
        ),
        "scope": (
            "This is a theorem about overlap with the fixed EH core, not "
            "nonexistence of LS(3,4,20) and not a resolution of #835."
        ),
    }
    atomic_json(args.receipt, receipt)
    print("[theorem] every twelve-system subfamily of the EH 15-core is excluded")
    print("[theorem] any LS(3,4,20) shares at most 11 of the EH 15-core")
    print(
        "[theorem] the 425 point-link-certified leaves have STS(19) "
        "packing number exactly 3"
    )
    print(
        "[scope] The separate ten-point theorem does not determine the "
        "point-0 packing number in its other 30 cases."
    )
    print("[scope] This does not decide LS(3,4,20) or #835.")
    print(f"[exact] aggregate receipt SHA-256: {file_sha256(args.receipt)}")
    print("status: PASS")


if __name__ == "__main__":
    main()
