#!/usr/bin/env python3
"""Materialize one deterministic LS(3,4,20) second-star branch CNF.

By default this replaces the parent header and appends the branch's sixteen
positive assumptions as unit clauses.  With ``--star-pairwise-amo`` it also
adds the logically implied pairwise at-most-one clauses for every
(triple, colour) star.  The latter is a propagation strengthening only: the
parent's block exactly-one and star at-least-one constraints already imply it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


N = 20
Q = 17
FOURS = tuple(combinations(range(N), 4))
THREES = tuple(combinations(range(N), 3))
FOUR_INDEX = {block: index for index, block in enumerate(FOURS)}
SCHEMA = "ls-3-4-20-second-star-branches-v1"


def x(block: int, colour: int) -> int:
    return Q * block + colour + 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--branch-id", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--star-pairwise-amo",
        action="store_true",
        help="append all 2,635,680 implied star AMO binary clauses",
    )
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA:
        raise AssertionError("wrong branch manifest schema")
    branches = manifest.get("branches")
    if (
        not isinstance(branches, list)
        or args.branch_id < 0
        or args.branch_id >= len(branches)
    ):
        raise AssertionError("branch id out of range")
    branch = branches[args.branch_id]
    if branch.get("id") != args.branch_id:
        raise AssertionError("branch ids are not canonical")

    parent_bytes = args.parent_cnf.read_bytes()
    parent_hash = hashlib.sha256(parent_bytes).hexdigest()
    if manifest["parent"]["sha256"] != parent_hash:
        raise AssertionError("parent CNF hash mismatch")
    header, separator, body = parent_bytes.partition(b"\n")
    if not separator:
        raise AssertionError("parent CNF is missing its header newline")
    fields = header.split()
    if len(fields) != 4 or fields[:2] != [b"p", b"cnf"]:
        raise AssertionError("invalid parent CNF header")
    variables, clauses = int(fields[2]), int(fields[3])

    assumptions = branch["assumptions"]
    extra_amo = 0
    if args.star_pairwise_amo:
        extra_amo = len(THREES) * Q * (Q * (Q - 1) // 2)
        if extra_amo != 2_635_680:
            raise AssertionError("wrong implied star AMO count")
    output_clauses = clauses + extra_amo + len(assumptions)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    with args.output.open("wb") as stream:
        new_header = f"p cnf {variables} {output_clauses}\n".encode("ascii")
        stream.write(new_header)
        digest.update(new_header)
        stream.write(body)
        digest.update(body)

        if args.star_pairwise_amo:
            universe = set(range(N))
            for triple in THREES:
                extensions = [
                    FOUR_INDEX[tuple(sorted(triple + (point,)))]
                    for point in sorted(universe - set(triple))
                ]
                if len(extensions) != Q:
                    raise AssertionError("wrong triple-star size")
                for colour in range(Q):
                    for left, right in combinations(extensions, 2):
                        line = f"{-x(left, colour)} {-x(right, colour)} 0\n".encode(
                            "ascii"
                        )
                        stream.write(line)
                        digest.update(line)

        for literal in assumptions:
            line = f"{literal} 0\n".encode("ascii")
            stream.write(line)
            digest.update(line)

    result = {
        "schema": SCHEMA,
        "branch_id": args.branch_id,
        "cycle_type": branch["cycle_type"],
        "parent_cnf_sha256": parent_hash,
        "star_pairwise_amo": args.star_pairwise_amo,
        "variables": variables,
        "clauses": output_clauses,
        "output": str(args.output),
        "output_sha256": digest.hexdigest(),
    }
    if not args.star_pairwise_amo:
        if result["output_sha256"] != branch["branch_cnf_sha256"]:
            raise AssertionError("materialized branch hash disagrees with manifest")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
