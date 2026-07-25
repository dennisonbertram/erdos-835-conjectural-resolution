#!/usr/bin/env python3
"""Audit that the symmetry CNF is the exact pairwise body plus valid WLOG tail."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


KNOWN_PARENT_SHA256 = "c6733572a4d62a1b6736e8332ae6ccebe63780969fed88957e78463240697a42"
PARENT_VARIABLES, PARENT_CLAUSES, SELECTORS = 483681, 5494321, 176
TOTAL_VARIABLES, TOTAL_CLAUSES = PARENT_VARIABLES + SELECTORS, PARENT_CLAUSES + 1 + SELECTORS * 15


def split_dimacs(data: bytes) -> tuple[bytes, bytes]:
    header, newline, body = data.partition(b"\n")
    fields = header.split()
    if not newline or len(fields) != 4 or fields[:2] != [b"p", b"cnf"]:
        raise ValueError("invalid DIMACS header")
    return header, body


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-cnf", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    parent = args.parent_cnf.read_bytes()
    parent_header, parent_body = split_dimacs(parent)
    if parent_header != f"p cnf {PARENT_VARIABLES} {PARENT_CLAUSES}".encode("ascii"):
        raise AssertionError("wrong pairwise parent dimensions")
    parent_hash = hashlib.sha256(parent).hexdigest()
    if parent_hash != KNOWN_PARENT_SHA256:
        raise AssertionError("parent is not the audited canonical pairwise CNF")
    current = args.cnf.read_bytes()
    current_header, current_body = split_dimacs(current)
    if current_header != f"p cnf {TOTAL_VARIABLES} {TOTAL_CLAUSES}".encode("ascii"):
        raise AssertionError("wrong symmetry-CNF dimensions")
    if not current_body.startswith(parent_body):
        raise AssertionError("symmetry CNF does not retain the exact canonical pairwise body")
    tail = current_body[len(parent_body):]
    map_payload = json.loads(args.map.read_text(encoding="utf-8"))
    matching = map_payload.get("diagonal_matching", {})
    representatives = matching.get("representatives")
    if map_payload.get("schema") != "odd-graph-o16-radius4-diagonal-matching-symbreak-v1" or not isinstance(representatives, list) or len(representatives) != SELECTORS:
        raise AssertionError("map lacks audited matching representatives")
    vertices = map_payload.get("vertices")
    if not isinstance(vertices, list) or len(vertices) != 14657:
        raise AssertionError("map lacks canonical vertex table")
    lookup = {item["mask"]: item["position"] for item in vertices}
    root = (1 << 15) - 1
    selector_start = PARENT_VARIABLES + 1
    expected = [" ".join(str(selector_start + item) for item in range(SELECTORS)) + " 0\n"]
    for item, permutation in enumerate(representatives):
        if not isinstance(permutation, list) or sorted(permutation) != list(range(15)):
            raise AssertionError("representative is not a permutation")
        for row, column in enumerate(permutation):
            mask = (root ^ (1 << column)) | (1 << (15 + row + 1))
            position = lookup[mask]
            literal = 17 * position + 2  # primary(position, colour 1)
            expected.append(f"{-(selector_start + item)} {literal} 0\n")
    expected_tail = "".join(expected).encode("ascii")
    if tail != expected_tail:
        raise AssertionError("symmetry tail is not the exact audited selector encoding")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    current_hash = hashlib.sha256(current).hexdigest()
    if manifest.get("cnf_sha256") != current_hash or manifest.get("map_sha256") != hashlib.sha256(args.map.read_bytes()).hexdigest():
        raise AssertionError("manifest hashes mismatch")
    if manifest.get("counts", {}).get("variables") != TOTAL_VARIABLES or manifest.get("counts", {}).get("clauses") != TOTAL_CLAUSES:
        raise AssertionError("manifest dimensions mismatch")
    print(json.dumps({
        "status": "PASS", "parent_cnf_sha256": parent_hash, "cnf_sha256": current_hash,
        "variables": TOTAL_VARIABLES, "clauses": TOTAL_CLAUSES,
        "selector_clauses": 1 + SELECTORS * 15,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
