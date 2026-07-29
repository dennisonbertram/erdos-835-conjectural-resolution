#!/usr/bin/env python3
"""Generate, solve, and replay the 119 exact surviving-row-type branches."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
GLOBAL = HERE.parent
sys.path.insert(0, str(GLOBAL))

import verify_r0_compact_full_cnf as compact_audit  # noqa: E402
import write_r0_tutte_full_cnf as tutte  # noqa: E402


TYPE_NAMES = ("5111", "3311", "31111", "6")
PREREQUISITE_COMMITS = (
    "2b83717",  # row-sum elimination of 37, 55, 333
    "856478f",  # every total obstruction needs at least five cores
    "f1d277c",  # all-K6 branch excluded
    "34ec83d",  # exactly-five covers contain no 3311 core
)


def partition() -> list[dict[str, object]]:
    branches = []
    index = 0
    for a in range(8):
        for b in range(8 - a):
            for c in range(8 - a - b):
                d = 7 - a - b - c
                counts = (a, b, c, d)
                if counts == (0, 0, 0, 7):
                    continue
                branch_id = f"a{a}_b{b}_c{c}_d{d}"
                branches.append(
                    {
                        "index": index,
                        "id": branch_id,
                        "counts": dict(zip(TYPE_NAMES, counts)),
                        "count_tuple": counts,
                        "seed": 83600 + index,
                        "scope_class": (
                            "B_PRESENT_NEEDS_SIX_CORES"
                            if b
                            else "B_FREE_NEEDS_FIVE_CORES"
                        ),
                    }
                )
                index += 1
    assert len(branches) == 119
    assert len({branch["count_tuple"] for branch in branches}) == 119
    return branches


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def dimacs_header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        for line in handle:
            if line.startswith("p cnf "):
                _, _, variables, clauses = line.split()
                return int(variables), int(clauses)
    raise ValueError(f"missing DIMACS header: {path}")


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def active_cadical_processes() -> int:
    result = subprocess.run(
        ["pgrep", "-f", "/opt/homebrew/bin/cadical"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 1:
        return 0
    if result.returncode != 0:
        raise SystemExit(
            "REFUSED: unable to inspect active CaDiCaL processes: "
            f"{result.stderr.strip()}"
        )
    return len([line for line in result.stdout.splitlines() if line.strip()])


def replay_unsat(
    drat_trim: Path,
    cnf_path: Path,
    proof_path: Path,
    log_path: Path,
) -> bool:
    result = subprocess.run(
        [str(drat_trim), str(cnf_path), str(proof_path), "-i"],
        check=False,
        capture_output=True,
        text=True,
    )
    log_path.write_text(result.stdout + result.stderr, encoding="utf-8")
    return result.returncode == 0 and "VERIFIED" in result.stdout


def generate_branch(
    branch: dict[str, object],
    output_dir: Path,
) -> dict[str, object]:
    branch_id = str(branch["id"])
    counts = tuple(branch["count_tuple"])
    cnf_path = output_dir / f"{branch_id}.cnf"
    tutte.build(
        cnf_path,
        surviving_only=True,
        require_four_cores=True,
        require_five_cores=True,
        exclude_all_k6=True,
        b_needs_six_cores=True,
        type_counts=counts,
    )
    variables, clauses = dimacs_header(cnf_path)
    return {
        "schema_version": 1,
        "branch": branch_id,
        "index": branch["index"],
        "type_counts": branch["counts"],
        "seed": branch["seed"],
        "prerequisite_commits": PREREQUISITE_COMMITS,
        "cnf": cnf_path.name,
        "cnf_variables": variables,
        "cnf_clauses": clauses,
        "cnf_sha256": sha256(cnf_path),
        "status": "GENERATED_NONTERMINAL",
    }


def solve_branch(
    branch: dict[str, object],
    receipt: dict[str, object],
    output_dir: Path,
    cadical: Path,
    seconds: int,
    drat_trim: Path | None,
) -> dict[str, object]:
    branch_id = str(branch["id"])
    cnf_path = output_dir / str(receipt["cnf"])
    witness_path = output_dir / f"{branch_id}.witness"
    proof_path = output_dir / f"{branch_id}.drat"
    command = [
        str(cadical),
        "-q",
        "--checkproof=3",
        "--shuffle=true",
        f"--seed={branch['seed']}",
        "-t",
        str(seconds),
        "-w",
        str(witness_path),
        str(cnf_path),
        str(proof_path),
    ]
    result = subprocess.run(command, check=False)
    receipt["solver_returncode"] = result.returncode
    receipt["solve_seconds_cap"] = seconds
    receipt["witness"] = witness_path.name
    receipt["proof"] = proof_path.name

    if result.returncode == 10:
        compact_audit.audit_witness(witness_path)
        receipt["status"] = "VERIFIED_SAT_WITNESS"
    elif result.returncode == 20:
        if drat_trim is None:
            receipt["status"] = "UNSAT_AWAITING_REPLAY_NONTERMINAL"
        else:
            replay_log = output_dir / f"{branch_id}.drat-trim.log"
            verified = replay_unsat(
                drat_trim, cnf_path, proof_path, replay_log
            )
            receipt["replay_log"] = replay_log.name
            receipt["status"] = (
                "VERIFIED_UNSAT" if verified
                else "UNSAT_REPLAY_FAILED_NONTERMINAL"
            )
    else:
        receipt["status"] = "UNKNOWN_NONTERMINAL"
    return receipt


def select_branches(
    requested: list[str],
    branches: list[dict[str, object]],
) -> list[dict[str, object]]:
    if requested == ["all"]:
        return branches
    by_id = {str(branch["id"]): branch for branch in branches}
    unknown = [branch_id for branch_id in requested if branch_id not in by_id]
    if unknown:
        raise ValueError(f"unknown branch ids: {unknown}")
    return [by_id[branch_id] for branch_id in requested]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--branch", action="append", default=[])
    parser.add_argument("--solve-seconds", type=int)
    parser.add_argument(
        "--cadical",
        type=Path,
        default=Path("/opt/homebrew/bin/cadical"),
    )
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--allow-concurrent", action="store_true")
    args = parser.parse_args()

    branches = partition()
    public_partition = [
        {
            key: value
            for key, value in branch.items()
            if key != "count_tuple"
        }
        for branch in branches
    ]
    if args.list:
        print(
            json.dumps(
                {
                    "schema_version": 1,
                    "branch_count": len(branches),
                    "b_free_branch_count": 35,
                    "b_present_branch_count": 84,
                    "excluded_branch": "a0_b0_c0_d7",
                    "type_order": TYPE_NAMES,
                    "prerequisite_commits": PREREQUISITE_COMMITS,
                    "branches": public_partition,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    if not args.output_dir or not args.branch:
        parser.error("--output-dir and at least one --branch are required")
    if args.solve_seconds is not None and args.solve_seconds <= 0:
        parser.error("--solve-seconds must be positive")
    if (
        args.solve_seconds is not None
        and not args.allow_concurrent
        and active_cadical_processes()
    ):
        raise SystemExit(
            "REFUSED: another CaDiCaL process is active; omit solving or "
            "use --allow-concurrent explicitly"
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        args.output_dir / "partition.json",
        {
            "schema_version": 1,
            "branch_count": len(branches),
            "b_free_branch_count": 35,
            "b_present_branch_count": 84,
            "excluded_branch": "a0_b0_c0_d7",
            "type_order": TYPE_NAMES,
            "prerequisite_commits": PREREQUISITE_COMMITS,
            "branches": public_partition,
        },
    )
    selected = select_branches(args.branch, branches)
    for branch in selected:
        receipt = generate_branch(branch, args.output_dir)
        if args.solve_seconds is not None:
            receipt = solve_branch(
                branch,
                receipt,
                args.output_dir,
                args.cadical,
                args.solve_seconds,
                args.drat_trim,
            )
        write_json(
            args.output_dir / f"{branch['id']}.receipt.json",
            receipt,
        )
        print(
            f"{branch['id']} {receipt['status']} "
            f"sha256={receipt['cnf_sha256']}",
            flush=True,
        )


if __name__ == "__main__":
    main()
