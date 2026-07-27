#!/usr/bin/env python3
"""Generate, trim, replay, and package DRAT proofs from a recon receipt.

The process is intentionally sequential by default because other long-running
solvers may share the host.  Each manifest row is appended only after:

1. the semantic CNF is regenerated and matched to the reconnaissance hash;
2. CaDiCaL returns UNSAT and emits a binary DRAT proof;
3. drat-trim verifies that proof while extracting its binary core lemmas;
4. drat-trim independently replays the trimmed proof against the full CNF;
5. the trimmed proof is deterministically gzip-compressed and hashed.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

from point_link_cnf import build_instance, clauses_for, load_source, write_cnf


SCHEMA = "eh-point-link-drat-v1"
RECON_SCHEMA = "eh-point-link-recon-v1"
HEX_DIGITS = frozenset("0123456789abcdef")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def command_version(command: str, argument: str = "--version") -> str:
    completed = subprocess.run(
        [command, argument],
        check=False,
        capture_output=True,
        text=True,
    )
    return (completed.stdout + completed.stderr).strip().splitlines()[0]


def normalized_transcript_sha256(transcript: str) -> str:
    """Hash stable checker content while excluding elapsed-time reporting."""

    lines = [
        line.strip()
        for line in transcript.replace("\r", "\n").splitlines()
        if line.strip()
        and "verification time:" not in line
        and "reading proof from stdin" not in line
        and "turning on binary mode checking" not in line
    ]
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


def valid_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX_DIGITS


def load_recon(path: Path, expected_rows: int | None = None) -> list[dict[str, object]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    if expected_rows is not None and len(rows) != expected_rows:
        raise AssertionError(
            f"recon receipt has {len(rows)} rows, expected {expected_rows}"
        )
    allowed_statuses = {
        "UNSAT_RECONNAISSANCE",
        "SAT_VERIFIED",
        "UNKNOWN",
    }
    for row in rows:
        if row.get("schema") != RECON_SCHEMA:
            raise AssertionError("recon row has an unknown schema")
        drop = tuple(row.get("drop", ()))
        if (
            len(drop) != 3
            or drop != tuple(sorted(drop))
            or len(set(drop)) != 3
            or not set(drop) <= set(range(15))
        ):
            raise AssertionError(f"recon row has invalid drop {drop}")
        point = row.get("point")
        if not isinstance(point, int) or point not in range(20):
            raise AssertionError(f"recon row has invalid point {point}")
        status = row.get("status")
        if status not in allowed_statuses:
            raise AssertionError(f"recon row has invalid status {status}")
        return_code = row.get("cadical_returncode")
        if status == "UNSAT_RECONNAISSANCE" and return_code != 20:
            raise AssertionError("UNSAT recon row lacks return code 20")
        if status == "SAT_VERIFIED" and return_code != 10:
            raise AssertionError("SAT recon row lacks return code 10")
        if status == "UNKNOWN" and return_code in {10, 20}:
            raise AssertionError("UNKNOWN recon row has a decisive return code")
        if not valid_sha256(row.get("cnf_sha256")):
            raise AssertionError("recon row has an invalid CNF hash")
        if row.get("cnf_variables") != 1_425 or row.get("cnf_clauses") != 12_545:
            raise AssertionError("recon row has incorrect CNF dimensions")
        colour_hash = row.get("colour_sha256")
        if status == "SAT_VERIFIED":
            if not valid_sha256(colour_hash):
                raise AssertionError("SAT recon row has no verified colour hash")
        elif colour_hash is not None:
            raise AssertionError("non-SAT recon row has a colour hash")
        elapsed = row.get("elapsed_seconds")
        if not isinstance(elapsed, (int, float)) or elapsed < 0:
            raise AssertionError("recon row has an invalid elapsed time")
    keys = [(tuple(row["drop"]), int(row["point"])) for row in rows]
    if len(keys) != len(set(keys)):
        raise AssertionError("recon receipt contains duplicate cases")
    return sorted(rows, key=lambda row: (row["drop"], row["point"]))


def load_completed(path: Path) -> dict[tuple[tuple[int, ...], int], dict[str, object]]:
    if not path.exists():
        return {}
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    result: dict[tuple[tuple[int, ...], int], dict[str, object]] = {}
    for row in rows:
        key = (tuple(row["drop"]), int(row["point"]))
        if key in result:
            raise AssertionError("certificate manifest contains duplicate cases")
        result[key] = row
    return result


def deterministic_gzip(source: Path, target: Path) -> None:
    with source.open("rb") as incoming, target.open("wb") as outgoing:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            compresslevel=9,
            fileobj=outgoing,
            mtime=0,
        ) as compressed:
            while chunk := incoming.read(1 << 20):
                compressed.write(chunk)


def streamed_gzip_digest(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    byte_count = 0
    with gzip.open(path, "rb") as proof:
        while chunk := proof.read(1 << 20):
            digest.update(chunk)
            byte_count += len(chunk)
    return byte_count, digest.hexdigest()


def replay_gzip(checker: str, cnf: Path, proof_gz: Path) -> tuple[str, float]:
    started = time.perf_counter()
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
    elapsed = time.perf_counter() - started
    if return_code != 0 or "s VERIFIED" not in transcript:
        raise AssertionError(
            f"saved DRAT replay failed ({return_code}) for {proof_gz}\n{transcript}"
        )
    return transcript, elapsed


def checked_run(command: list[str], expected_text: str) -> tuple[str, float]:
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    elapsed = time.perf_counter() - started
    transcript = completed.stdout + completed.stderr
    if completed.returncode != 0 or expected_text not in transcript:
        raise AssertionError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{transcript}"
        )
    return transcript, elapsed


def certify_one(
    systems: tuple[frozenset[tuple[int, ...]], ...],
    recon: dict[str, object],
    certificate_dir: Path,
    cadical: str,
    drat_trim: str,
    seconds: int,
    cadical_version: str,
    checker_id: str,
) -> dict[str, object]:
    drop = tuple(map(int, recon["drop"]))
    if len(drop) != 3:
        raise AssertionError("malformed drop triple")
    point = int(recon["point"])
    stem = f"drop_{drop[0]}_{drop[1]}_{drop[2]}_point_{point}"
    destination = certificate_dir / f"{stem}.trimmed.drat.gz"

    with tempfile.TemporaryDirectory(prefix=f"{stem}-") as raw_temp:
        temp = Path(raw_temp)
        cnf = temp / f"{stem}.cnf"
        raw_proof = temp / f"{stem}.raw.drat"
        trimmed_proof = temp / f"{stem}.trimmed.drat"

        triples, by_pair = build_instance(systems, drop, point)
        cnf_digest = write_cnf(cnf, triples, clauses_for(triples, by_pair))
        if cnf_digest != recon["cnf_sha256"]:
            raise AssertionError(
                f"{stem}: regenerated CNF {cnf_digest} != recon hash "
                f"{recon['cnf_sha256']}"
            )

        started = time.perf_counter()
        solver = subprocess.run(
            [
                cadical,
                "-q",
                "-t",
                str(seconds),
                str(cnf),
                str(raw_proof),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        solver_elapsed = time.perf_counter() - started
        solver_transcript = solver.stdout + solver.stderr
        if solver.returncode != 20:
            raise AssertionError(
                f"{stem}: certificate run did not return UNSAT (code "
                f"{solver.returncode})\n{solver_transcript}"
            )

        first_transcript, first_elapsed = checked_run(
            [
                drat_trim,
                str(cnf),
                str(raw_proof),
                "-l",
                str(trimmed_proof),
                "-C",
            ],
            "s VERIFIED",
        )
        replay_transcript, replay_elapsed = checked_run(
            [drat_trim, str(cnf), str(trimmed_proof), "-i"],
            "s VERIFIED",
        )

        certificate_dir.mkdir(parents=True, exist_ok=True)
        temporary_destination = destination.with_name(
            f".{destination.name}.tmp-{os.getpid()}"
        )
        deterministic_gzip(trimmed_proof, temporary_destination)
        os.replace(temporary_destination, destination)
        row: dict[str, object] = {
            "schema": SCHEMA,
            "drop": list(drop),
            "point": point,
            "status": "UNSAT_CERTIFIED",
            "source_recon_status": recon["status"],
            "cnf_sha256": cnf_digest,
            "cnf_variables": 1_425,
            "cnf_clauses": 12_545,
            "cadical_version": cadical_version,
            "cadical_seconds": round(solver_elapsed, 6),
            "raw_proof_bytes": raw_proof.stat().st_size,
            "raw_proof_sha256": file_sha256(raw_proof),
            "checker_id": checker_id,
            "first_check_seconds": round(first_elapsed, 6),
            "first_check_normalized_sha256": normalized_transcript_sha256(
                first_transcript
            ),
            "trimmed_proof_bytes": trimmed_proof.stat().st_size,
            "trimmed_proof_sha256": file_sha256(trimmed_proof),
            "replay_seconds": round(replay_elapsed, 6),
            "replay_normalized_sha256": normalized_transcript_sha256(replay_transcript),
            "compressed_proof_path": destination.relative_to(
                certificate_dir.parent
            ).as_posix(),
            "compressed_proof_bytes": destination.stat().st_size,
            "compressed_proof_sha256": file_sha256(destination),
        }
    return row


def audit_completed(
    completed: dict[tuple[tuple[int, ...], int], dict[str, object]],
    recon: dict[tuple[tuple[int, ...], int], dict[str, object]],
    systems: tuple[frozenset[tuple[int, ...]], ...],
    certificate_dir: Path,
    drat_trim: str,
) -> None:
    """Fully validate every saved row before resume skips it."""

    expected_paths: set[Path] = set()
    for key, row in sorted(completed.items()):
        drop, point = key
        if key not in recon or recon[key]["status"] != "UNSAT_RECONNAISSANCE":
            raise AssertionError(f"saved certificate {key} lacks an UNSAT recon row")
        if row.get("schema") != SCHEMA or row.get("status") != "UNSAT_CERTIFIED":
            raise AssertionError(f"saved certificate {key} has bad schema/status")
        if row.get("cnf_sha256") != recon[key]["cnf_sha256"]:
            raise AssertionError(f"saved certificate {key} has wrong CNF hash")
        if row.get("cnf_variables") != 1_425 or row.get("cnf_clauses") != 12_545:
            raise AssertionError(f"saved certificate {key} has wrong CNF dimensions")

        stem = f"drop_{drop[0]}_{drop[1]}_{drop[2]}_point_{point}"
        proof = certificate_dir / f"{stem}.trimmed.drat.gz"
        recorded = certificate_dir.parent / str(row["compressed_proof_path"])
        if proof.resolve() != recorded.resolve():
            raise AssertionError(f"saved certificate {key} has wrong proof path")
        expected_paths.add(proof.resolve())
        if not proof.is_file():
            raise AssertionError(f"saved certificate {key} is missing its proof")
        if proof.stat().st_size != row.get("compressed_proof_bytes"):
            raise AssertionError(f"saved certificate {key} has wrong gzip size")
        if file_sha256(proof) != row.get("compressed_proof_sha256"):
            raise AssertionError(f"saved certificate {key} has wrong gzip hash")
        raw_bytes, raw_hash = streamed_gzip_digest(proof)
        if raw_bytes != row.get("trimmed_proof_bytes"):
            raise AssertionError(f"saved certificate {key} has wrong raw size")
        if raw_hash != row.get("trimmed_proof_sha256"):
            raise AssertionError(f"saved certificate {key} has wrong raw hash")

        triples, by_pair = build_instance(systems, drop, point)
        with tempfile.TemporaryDirectory(prefix="audit-eh-point-link-") as raw_temp:
            cnf = Path(raw_temp) / "instance.cnf"
            digest = write_cnf(cnf, triples, clauses_for(triples, by_pair))
            if digest != row["cnf_sha256"]:
                raise AssertionError(f"saved certificate {key} fails CNF rebuild")
            transcript, _ = replay_gzip(drat_trim, cnf, proof)
            if normalized_transcript_sha256(transcript) != row.get(
                "replay_normalized_sha256"
            ):
                raise AssertionError(
                    f"saved certificate {key} has wrong replay summary"
                )

    actual_paths = {
        path.resolve() for path in certificate_dir.glob("*.trimmed.drat.gz")
    }
    unexpected = actual_paths - expected_paths
    if unexpected:
        names = ", ".join(sorted(path.name for path in unexpected))
        raise AssertionError(f"orphan completed proof files: {names}")


def append_row(path: Path, row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_bytes() if path.exists() else b""
    added = (json.dumps(row, sort_keys=True) + "\n").encode("ascii")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("wb") as output:
        output.write(existing)
        output.write(added)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recon", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--certificate-dir", type=Path, required=True)
    parser.add_argument("--cadical", default="cadical")
    parser.add_argument("--drat-trim", required=True)
    parser.add_argument("--checker-id", required=True)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--expected-recon-rows", type=int)
    args = parser.parse_args()

    recon_rows = load_recon(args.recon, args.expected_recon_rows)
    recon = {(tuple(row["drop"]), int(row["point"])): row for row in recon_rows}
    candidates = [row for row in recon_rows if row["status"] == "UNSAT_RECONNAISSANCE"]
    completed = load_completed(args.manifest)
    _, systems = load_source()
    audit_completed(
        completed,
        recon,
        systems,
        args.certificate_dir,
        args.drat_trim,
    )
    pending = [
        row
        for row in candidates
        if (tuple(row["drop"]), int(row["point"])) not in completed
    ]
    if args.limit is not None:
        pending = pending[: args.limit]

    cadical_version = command_version(args.cadical)
    for index, recon in enumerate(pending, 1):
        row = certify_one(
            systems,
            recon,
            args.certificate_dir,
            args.cadical,
            args.drat_trim,
            args.seconds,
            cadical_version,
            args.checker_id,
        )
        append_row(args.manifest, row)
        print(
            json.dumps(
                {
                    "progress": f"{index}/{len(pending)}",
                    "drop": row["drop"],
                    "point": row["point"],
                    "compressed_proof_bytes": row["compressed_proof_bytes"],
                    "status": row["status"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    final = load_completed(args.manifest)
    manifest_digest = file_sha256(args.manifest) if args.manifest.exists() else None
    print(
        json.dumps(
            {
                "recon_unsat": len(candidates),
                "manifest_certificates": len(final),
                "remaining": len(candidates) - len(final),
                "manifest_sha256": manifest_digest,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
