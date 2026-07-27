#!/usr/bin/env python3
"""Verify a scalable manifest of compressed EH point-link DRAT proofs."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from certify_point_links import (
    SCHEMA,
    file_sha256,
    load_recon,
    normalized_transcript_sha256,
    valid_sha256,
)


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_seed.txt"
SOURCE_SHA256 = "b1ea090d3e3b88366c87e95660c1c82a406d2c3b100cc1d39bcc2c7e8fde47f9"
POINTS = tuple(range(20))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
TRIPLES = tuple(itertools.combinations(POINTS, 3))
N_COLOURS = 5


def independently_load_source() -> tuple[frozenset[tuple[int, ...]], ...]:
    """Authenticate and reconstruct the EH systems without generator imports."""

    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise AssertionError("authenticated EH source hash mismatch")
    lines = raw.decode("ascii").splitlines()
    if len(lines) != len(BLOCKS):
        raise AssertionError("EH source does not contain C(20,4) rows")

    owner: dict[tuple[int, ...], int] = {}
    for expected, line in zip(BLOCKS, lines):
        fields = tuple(map(int, line.split()))
        if len(fields) != 5 or fields[:4] != expected:
            raise AssertionError(f"malformed EH source row at {expected}")
        owner[expected] = fields[4]
    if Counter(owner.values()) != Counter({label: 285 for label in range(17)}):
        raise AssertionError("EH source label census mismatch")

    systems = tuple(
        frozenset(block for block, label in owner.items() if label == number)
        for number in range(15)
    )
    if set(map(len, systems)) != {285} or len(set().union(*systems)) != 15 * 285:
        raise AssertionError("EH systems are not fifteen disjoint 285-block classes")
    for number, system in enumerate(systems):
        covered = Counter(
            triple for block in system for triple in itertools.combinations(block, 3)
        )
        if set(covered) != set(TRIPLES) or set(covered.values()) != {1}:
            raise AssertionError(f"EH class {number} is not an SQS(20)")
    return systems


def independent_cnf_bytes(
    systems: tuple[frozenset[tuple[int, ...]], ...],
    drop: tuple[int, int, int],
    point: int,
) -> bytes:
    """Reconstruct the exact semantic DIMACS independently of its generator."""

    if (
        drop != tuple(sorted(drop))
        or len(set(drop)) != 3
        or not set(drop) <= set(range(15))
    ):
        raise AssertionError(f"invalid drop triple {drop}")
    if point not in POINTS:
        raise AssertionError(f"invalid point {point}")

    retained = set().union(
        *(system for number, system in enumerate(systems) if number not in drop)
    )
    derived = tuple(
        tuple(value for value in block if value != point)
        for block in BLOCKS
        if point in block and block not in retained
    )
    if not len(derived) == len(set(derived)) == 285:
        raise AssertionError("independent derived leave has wrong size")

    pair_rows_lists: dict[tuple[int, int], list[int]] = defaultdict(list)
    for row, triple in enumerate(derived):
        for pair in itertools.combinations(triple, 2):
            pair_rows_lists[pair].append(row)
    pair_rows = {pair: tuple(rows) for pair, rows in pair_rows_lists.items()}
    other_points = tuple(value for value in POINTS if value != point)
    if set(pair_rows) != set(itertools.combinations(other_points, 2)):
        raise AssertionError("independent derived leave misses a point pair")
    if set(map(len, pair_rows.values())) != {5}:
        raise AssertionError("independent derived leave is not five-fold")

    adjacency = [set() for _ in derived]
    for rows in pair_rows.values():
        for left, right in itertools.combinations(rows, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
    if set(map(len, adjacency)) != {12}:
        raise AssertionError("independent leave graph is not 12-regular")

    def variable(row: int, colour: int) -> int:
        return N_COLOURS * row + colour + 1

    clauses: list[tuple[int, ...]] = []
    for row in range(len(derived)):
        clauses.append(tuple(variable(row, colour) for colour in range(N_COLOURS)))
        clauses.extend(
            (-variable(row, left), -variable(row, right))
            for left, right in itertools.combinations(range(N_COLOURS), 2)
        )
    for rows in pair_rows.values():
        for colour in range(N_COLOURS):
            clauses.append(tuple(variable(row, colour) for row in rows))
            clauses.extend(
                (-variable(left, colour), -variable(right, colour))
                for left, right in itertools.combinations(rows, 2)
            )
    root_rows = pair_rows[min(pair_rows)]
    clauses.extend((variable(row, colour),) for colour, row in enumerate(root_rows))
    if len(clauses) != 12_545:
        raise AssertionError("independent semantic CNF has wrong clause count")
    text = [f"p cnf {len(derived) * N_COLOURS} {len(clauses)}\n"]
    text.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(text).encode("ascii")


def load_jsonl(path: Path) -> list[dict[str, object]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    keys = [(tuple(row["drop"]), int(row["point"])) for row in rows]
    if len(keys) != len(set(keys)):
        raise AssertionError(f"{path} contains duplicate cases")
    return rows


def streamed_gzip_digest(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    byte_count = 0
    with gzip.open(path, "rb") as proof:
        while chunk := proof.read(1 << 20):
            digest.update(chunk)
            byte_count += len(chunk)
    return byte_count, digest.hexdigest()


def replay(checker: str, cnf: Path, proof_gz: Path) -> tuple[str, int]:
    process = subprocess.Popen(
        [checker, str(cnf), "-i"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert process.stdin is not None
    with gzip.open(proof_gz, "rb") as proof:
        while chunk := proof.read(1 << 20):
            process.stdin.write(chunk)
    process.stdin.close()
    assert process.stdout is not None
    transcript = process.stdout.read().decode("utf-8", errors="replace")
    return_code = process.wait()
    if return_code != 0 or "s VERIFIED" not in transcript:
        raise AssertionError(
            f"DRAT replay failed ({return_code}) for {proof_gz}\n{transcript}"
        )
    return transcript, return_code


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recon", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--base-dir", type=Path, default=HERE)
    parser.add_argument("--drat-trim")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--expected-recon-rows", type=int)
    args = parser.parse_args()

    if args.require_complete and args.drat_trim is None:
        raise SystemExit("--require-complete requires --drat-trim")
    if args.require_complete and args.limit is not None:
        raise SystemExit("--require-complete is incompatible with --limit")
    recon_rows = load_recon(args.recon, args.expected_recon_rows)
    manifest_rows = load_jsonl(args.manifest)
    recon = {(tuple(row["drop"]), int(row["point"])): row for row in recon_rows}
    manifest = {(tuple(row["drop"]), int(row["point"])): row for row in manifest_rows}
    unsat_recon = {
        key for key, row in recon.items() if row["status"] == "UNSAT_RECONNAISSANCE"
    }
    if not set(manifest) <= unsat_recon:
        raise AssertionError("manifest contains a case not marked UNSAT in recon")
    if args.require_complete and set(manifest) != unsat_recon:
        missing = sorted(unsat_recon - set(manifest))
        raise AssertionError(f"manifest is missing {len(missing)} UNSAT cases")

    base = args.base_dir.resolve()
    referenced_paths: set[Path] = set()
    for key, row in manifest.items():
        if row.get("schema") != SCHEMA or row.get("status") != "UNSAT_CERTIFIED":
            raise AssertionError(f"{key}: bad schema or status")
        for field in (
            "cnf_sha256",
            "raw_proof_sha256",
            "trimmed_proof_sha256",
            "compressed_proof_sha256",
            "first_check_normalized_sha256",
            "replay_normalized_sha256",
        ):
            if not valid_sha256(row.get(field)):
                raise AssertionError(f"{key}: invalid hash field {field}")
        proof = (base / str(row["compressed_proof_path"])).resolve()
        try:
            proof.relative_to(base)
        except ValueError as error:
            raise AssertionError(
                f"{key}: proof path escapes the certificate base directory"
            ) from error
        referenced_paths.add(proof)
    scanned_paths = {
        proof
        for directory in {path.parent for path in referenced_paths}
        for proof in directory.glob("*.trimmed.drat.gz")
    }
    if scanned_paths != referenced_paths:
        missing_files = referenced_paths - scanned_paths
        orphan_files = scanned_paths - referenced_paths
        raise AssertionError(
            "certificate file/manifest mismatch: "
            f"missing={sorted(path.name for path in missing_files)} "
            f"orphan={sorted(path.name for path in orphan_files)}"
        )

    systems = independently_load_source()
    print(
        "[ok] authenticated source and fifteen SQS(20)s reconstructed "
        "independently of the CNF generator"
    )
    rows_to_check = sorted(manifest_rows, key=lambda row: (row["drop"], row["point"]))
    if args.limit is not None:
        rows_to_check = rows_to_check[: args.limit]

    bundle_digest = hashlib.sha256()
    total_compressed_bytes = 0
    for index, row in enumerate(rows_to_check, 1):
        drop = tuple(map(int, row["drop"]))
        point = int(row["point"])
        key = (drop, point)
        if row["cnf_sha256"] != recon[key]["cnf_sha256"]:
            raise AssertionError(f"{key}: manifest/recon CNF hash mismatch")
        if row["cnf_variables"] != 1_425 or row["cnf_clauses"] != 12_545:
            raise AssertionError(f"{key}: wrong CNF dimensions")

        proof = (base / str(row["compressed_proof_path"])).resolve()
        if proof.stat().st_size != row["compressed_proof_bytes"]:
            raise AssertionError(f"{key}: compressed proof byte count mismatch")
        if file_sha256(proof) != row["compressed_proof_sha256"]:
            raise AssertionError(f"{key}: compressed proof hash mismatch")
        raw_bytes, raw_digest = streamed_gzip_digest(proof)
        if raw_bytes != row["trimmed_proof_bytes"]:
            raise AssertionError(f"{key}: trimmed proof byte count mismatch")
        if raw_digest != row["trimmed_proof_sha256"]:
            raise AssertionError(f"{key}: trimmed proof hash mismatch")

        expected_cnf = independent_cnf_bytes(systems, drop, point)
        with tempfile.TemporaryDirectory(prefix="verify-eh-point-link-") as raw_temp:
            cnf = Path(raw_temp) / "instance.cnf"
            cnf.write_bytes(expected_cnf)
            cnf_digest = hashlib.sha256(expected_cnf).hexdigest()
            if cnf_digest != row["cnf_sha256"]:
                raise AssertionError(f"{key}: independent semantic CNF hash mismatch")
            if args.drat_trim is not None:
                transcript, return_code = replay(args.drat_trim, cnf, proof)
                if return_code != 0:
                    raise AssertionError(f"{key}: checker returned {return_code}")
                if (
                    normalized_transcript_sha256(transcript)
                    != row["replay_normalized_sha256"]
                ):
                    raise AssertionError(f"{key}: replay transcript hash mismatch")

        total_compressed_bytes += proof.stat().st_size
        bundle_digest.update(bytes(drop))
        bundle_digest.update(point.to_bytes(1, "big"))
        bundle_digest.update(bytes.fromhex(str(row["cnf_sha256"])))
        bundle_digest.update(bytes.fromhex(str(row["compressed_proof_sha256"])))
        if index % 25 == 0 or index == len(rows_to_check):
            print(f"[ok] verified {index}/{len(rows_to_check)} manifest rows")

    print("[ok] every checked CNF was independently reconstructed byte-for-byte")
    census = Counter(str(row["status"]) for row in recon_rows)
    print(f"[exact] recon census: {dict(sorted(census.items()))}")
    print(f"[exact] manifest rows: {len(manifest_rows)}")
    print(f"[exact] checked rows: {len(rows_to_check)}")
    print(f"[exact] compressed proof bytes checked: {total_compressed_bytes}")
    print(f"[exact] certificate bundle digest: {bundle_digest.hexdigest()}")
    print(f"[exact] manifest SHA-256: {file_sha256(args.manifest)}")
    if args.require_complete:
        print("[ok] every UNSAT reconnaissance row has a certificate")
    print("status: PASS")


if __name__ == "__main__":
    main()
