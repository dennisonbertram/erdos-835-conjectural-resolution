#!/usr/bin/env python3
"""Generate a deterministic exhaustive primary-variable cube partition.

Each leaf is a conjunction of positive one-hot primary literals.  It is
not a symmetry restriction: every colour choice is retained at every
split, so the leaves are a disjoint, exhaustive partition of all parent
models.  The companion verifier checks that claim without importing this
generator.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from generate_radius4_generic_sinz_cnf import ball, primary, symmetry_units


SCHEMA = "odd-graph-o16-primary-cube-partition-v1"
COLORS = 17


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-cnf-sha256", required=True, help="SHA-256 of the exact CNF being partitioned")
    parser.add_argument("--depth", type=int, default=1, help="number of free vertex rows to split; 1..3")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.depth < 1 or args.depth > 3:
        parser.error("--depth must be in 1..3 (17, 289, or 4913 leaves)")
    if len(args.parent_cnf_sha256) != 64 or any(item not in "0123456789abcdef" for item in args.parent_cnf_sha256):
        parser.error("--parent-cnf-sha256 must be 64 lowercase hexadecimal characters")

    vertices, distances, position = ball()
    fixed = {vertex for vertex, _ in symmetry_units(vertices, distances, position)}
    split_vertices = [vertex for vertex in range(len(vertices)) if vertex not in fixed][: args.depth]
    assert split_vertices == list(range(32, 32 + args.depth))
    leaves = []
    for leaf_id, colours in enumerate(itertools.product(range(COLORS), repeat=args.depth)):
        assumptions = [primary(vertex, colour) for vertex, colour in zip(split_vertices, colours)]
        leaves.append({"id": leaf_id, "colours": list(colours), "assumptions": assumptions})
    payload = {
        "schema": SCHEMA,
        "parent_cnf_sha256": args.parent_cnf_sha256,
        "colour_count": COLORS,
        "depth": args.depth,
        "split_vertex_positions": split_vertices,
        "leaf_count": len(leaves),
        "leaves": leaves,
    }
    canonical = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    payload["sha256_without_hash"] = hashlib.sha256(canonical).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in payload if key != "leaves"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
