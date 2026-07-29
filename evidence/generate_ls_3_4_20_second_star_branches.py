#!/usr/bin/env python3
"""Generate the lossless second-star symmetry branches for LS(3,4,20).

The parent CNF fixes the colours on the extensions of {0,1,2}.  Identify
colour i with point i+3 and put Q={3,...,19}.  In every parent model the
blocks {0,1,3,r}, r in Q\\{3}, define a derangement of the other sixteen
points.  The residual diagonal Sym(Q\\{3}) action conjugates this
derangement.  Hence its 55 possible cycle types are lossless orbit
representatives.

This script emits a compact cube file and a manifest containing the exact
positive primary literals for all 55 representatives.  It also records the
SHA-256 of the deterministic CNF obtained by appending each cube as unit
clauses to the exact parent CNF.  The companion materializer writes such a
branch CNF on demand.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Iterator


POINTS = 20
COLOURS = 17
ROOT = (0, 1, 2)
PAIR = (0, 1)
Q = tuple(range(3, POINTS))
ROW_POINT = 3
ROW_DOMAIN = tuple(range(4, POINTS))
SCHEMA = "ls-3-4-20-second-star-branches-v1"
BLOCKS = tuple(combinations(range(POINTS), 4))
BLOCK_INDEX = {block: index for index, block in enumerate(BLOCKS)}


def primary(block: tuple[int, ...], colour: int) -> int:
    return COLOURS * BLOCK_INDEX[block] + colour + 1


def partitions_minimum(
    total: int, minimum: int = 2, lower: int | None = None
) -> Iterator[tuple[int, ...]]:
    """Yield nondecreasing partitions with every part at least ``minimum``."""

    if lower is None:
        lower = minimum
    if total == 0:
        yield ()
        return
    for part in range(lower, total + 1):
        remainder = total - part
        if remainder and remainder < part:
            continue
        for tail in partitions_minimum(remainder, minimum, part):
            yield (part,) + tail


def canonical_permutation(cycle_type: tuple[int, ...]) -> dict[int, int]:
    """Put the cycles on consecutive entries of ROW_DOMAIN."""

    if sum(cycle_type) != len(ROW_DOMAIN) or any(part < 2 for part in cycle_type):
        raise ValueError("cycle type must partition 16 with parts at least two")
    result: dict[int, int] = {}
    offset = 0
    for length in cycle_type:
        cycle = ROW_DOMAIN[offset : offset + length]
        for index, point in enumerate(cycle):
            result[point] = cycle[(index + 1) % length]
        offset += length
    if set(result) != set(ROW_DOMAIN):
        raise AssertionError("canonical cycles do not cover the row domain")
    return result


def centralizer_order(cycle_type: tuple[int, ...]) -> int:
    multiplicities = Counter(cycle_type)
    result = 1
    for length, count in multiplicities.items():
        result *= length**count * math.factorial(count)
    return result


def cube_bytes(
    parent_sha256: str, branches: list[dict[str, object]]
) -> bytes:
    lines = [
        f"c {SCHEMA}\n",
        f"c parent_cnf_sha256 {parent_sha256}\n",
        (
            "c WLOG orbit representatives under the residual diagonal "
            "point-colour symmetry; not a literal partition of labelled models\n"
        ),
    ]
    for branch in branches:
        cycle_type = ",".join(str(part) for part in branch["cycle_type"])
        lines.append(
            f"c branch {int(branch['id']):02d} cycle_type {cycle_type}\n"
        )
        lines.append(
            "a "
            + " ".join(str(literal) for literal in branch["assumptions"])
            + " 0\n"
        )
    return "".join(lines).encode("ascii")


def branch_digest(
    parent_body: bytes,
    variables: int,
    parent_clauses: int,
    assumptions: list[int],
) -> str:
    digest = hashlib.sha256()
    digest.update(
        f"p cnf {variables} {parent_clauses + len(assumptions)}\n".encode("ascii")
    )
    digest.update(parent_body)
    for literal in assumptions:
        digest.update(f"{literal} 0\n".encode("ascii"))
    return digest.hexdigest()


def parse_header(parent_bytes: bytes) -> tuple[int, int, bytes]:
    header, separator, body = parent_bytes.partition(b"\n")
    if not separator:
        raise ValueError("parent CNF has no complete header line")
    fields = header.split()
    if len(fields) != 4 or fields[:2] != [b"p", b"cnf"]:
        raise ValueError("parent CNF does not start with a DIMACS header")
    return int(fields[2]), int(fields[3]), body


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-cnf", type=Path, required=True)
    parser.add_argument("--parent-manifest", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--cubes", type=Path, required=True)
    args = parser.parse_args()

    parent_bytes = args.parent_cnf.read_bytes()
    parent_sha256 = hashlib.sha256(parent_bytes).hexdigest()
    variables, parent_clauses, parent_body = parse_header(parent_bytes)
    if (variables, parent_clauses) != (159_885, 251_957):
        raise AssertionError("unexpected parent CNF dimensions")

    parent_manifest = json.loads(args.parent_manifest.read_text(encoding="utf-8"))
    if parent_manifest.get("cnf_sha256") != parent_sha256:
        raise AssertionError("parent manifest does not authenticate parent CNF")

    cycle_types = list(partitions_minimum(len(ROW_DOMAIN)))
    if len(cycle_types) != 55:
        raise AssertionError(f"expected 55 cycle types, found {len(cycle_types)}")

    branches: list[dict[str, object]] = []
    for branch_id, cycle_type in enumerate(cycle_types):
        permutation = canonical_permutation(cycle_type)
        units = []
        assumptions = []
        for point in ROW_DOMAIN:
            image = permutation[point]
            block = tuple(sorted(PAIR + (ROW_POINT, point)))
            colour = image - Q[0]
            literal = primary(block, colour)
            assumptions.append(literal)
            units.append(
                {
                    "point": point,
                    "image_point": image,
                    "block_index": BLOCK_INDEX[block],
                    "block": list(block),
                    "colour": colour,
                    "colour_point": image,
                    "literal": literal,
                }
            )
        z_value = centralizer_order(cycle_type)
        branches.append(
            {
                "id": branch_id,
                "cycle_type": list(cycle_type),
                "canonical_row_images": [
                    permutation[point] for point in ROW_DOMAIN
                ],
                "assumptions": assumptions,
                "units": units,
                "centralizer_order_in_sym16": z_value,
                "derangement_conjugacy_class_size": (
                    math.factorial(len(ROW_DOMAIN)) // z_value
                ),
                "geometric_branch_stabilizer_order": 2 * z_value,
                "branch_cnf_variables": variables,
                "branch_cnf_clauses": parent_clauses + len(assumptions),
                "branch_cnf_sha256": branch_digest(
                    parent_body,
                    variables,
                    parent_clauses,
                    assumptions,
                ),
            }
        )

    cubes = cube_bytes(parent_sha256, branches)
    payload: dict[str, object] = {
        "schema": SCHEMA,
        "parent": {
            "path": str(args.parent_cnf),
            "sha256": parent_sha256,
            "variables": variables,
            "clauses": parent_clauses,
        },
        "normalization": {
            "root_triple": list(ROOT),
            "root_extension_points": list(Q),
            "colour_point_rule": "colour c is identified with point c+3",
            "second_star_pair": list(PAIR),
            "second_star_row_point": ROW_POINT,
            "second_star_row_domain": list(ROW_DOMAIN),
            "residual_semantic_group": "Sym({0,1,2}) x diagonal Sym(Q)",
            "canonicalizing_subgroup": "diagonal Sym(Q\\{3})",
        },
        "branch_count": len(branches),
        "cube_literal_count_per_branch": len(ROW_DOMAIN),
        "cubes_sha256": hashlib.sha256(cubes).hexdigest(),
        "derangement_count": sum(
            int(branch["derangement_conjugacy_class_size"])
            for branch in branches
        ),
        "branches": branches,
    }
    canonical = (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    payload["manifest_sha256_without_self"] = hashlib.sha256(canonical).hexdigest()

    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.cubes.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    args.cubes.write_bytes(cubes)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "parent_cnf_sha256": parent_sha256,
                "branch_count": len(branches),
                "derangement_count": payload["derangement_count"],
                "cubes_sha256": payload["cubes_sha256"],
                "manifest_sha256_without_self": payload[
                    "manifest_sha256_without_self"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
