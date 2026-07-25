#!/usr/bin/env python3
"""Append one auditable cube as units to an exact parent DIMACS CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-cnf", type=Path, required=True)
    parser.add_argument("--cubes", type=Path, required=True)
    parser.add_argument("--cube-id", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    parent_bytes = args.parent_cnf.read_bytes()
    parent_hash = hashlib.sha256(parent_bytes).hexdigest()
    cubes = json.loads(args.cubes.read_text(encoding="utf-8"))
    if cubes.get("parent_cnf_sha256") != parent_hash:
        raise ValueError("cube manifest is for a different parent CNF")
    leaves = cubes.get("leaves")
    if not isinstance(leaves, list) or not 0 <= args.cube_id < len(leaves):
        raise ValueError("cube id is outside manifest")
    leaf = leaves[args.cube_id]
    if leaf.get("id") != args.cube_id or not all(isinstance(item, int) and item > 0 for item in leaf.get("assumptions", [])):
        raise ValueError("invalid cube entry")
    header, separator, body = parent_bytes.partition(b"\n")
    fields = header.split()
    if not separator or len(fields) != 4 or fields[:2] != [b"p", b"cnf"]:
        raise ValueError("parent does not begin with a DIMACS header")
    variables, clauses = int(fields[2]), int(fields[3])
    if any(item > variables for item in leaf["assumptions"]):
        raise ValueError("cube literal outside parent variable range")
    new_header = f"p cnf {variables} {clauses + len(leaf['assumptions'])}\n".encode("ascii")
    unit_bytes = b"".join(f"{item} 0\n".encode("ascii") for item in leaf["assumptions"])
    output_bytes = new_header + body + unit_bytes
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output_bytes)
    print(json.dumps({
        "cube_id": args.cube_id, "assumptions": leaf["assumptions"], "parent_cnf_sha256": parent_hash,
        "cube_cnf_sha256": hashlib.sha256(output_bytes).hexdigest(), "variables": variables,
        "clauses": clauses + len(leaf["assumptions"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
