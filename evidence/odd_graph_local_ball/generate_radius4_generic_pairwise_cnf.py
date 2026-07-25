#!/usr/bin/env python3
"""Emit the complete radius-4 CNF with redundant local pairwise AMO clauses.

This is the generic Sinz instance plus, for every constrained closed
neighbourhood and every colour, all pairwise negative clauses.  Those
clauses are logical consequences of the base formula, so the instance
has exactly the same primary-colour models.  They make the local
``exactly once per colour`` condition propagation-complete.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Iterator

from generate_radius4_generic_sinz_cnf import (
    COLOR_COUNT,
    RADIUS,
    SCHEMA as BASE_SCHEMA,
    ball,
    canonical_map as base_canonical_map,
    clause_lines as base_clause_lines,
    dimensions as base_dimensions,
    neighbours,
    primary,
    symmetry_units,
)


SCHEMA = "odd-graph-o16-radius4-generic-pairwise-v1"


def dimensions(vertices: list[int], distances: list[int]) -> dict[str, int]:
    stats = dict(base_dimensions(vertices, distances))
    local_pairwise = stats["constrained_centres"] * COLOR_COUNT * (COLOR_COUNT * (COLOR_COUNT - 1) // 2)
    stats["local_pairwise_amo_clauses"] = local_pairwise
    stats["clauses"] += local_pairwise
    return stats


def additional_clauses(
    vertices: list[int], distances: list[int], position: dict[int, int]
) -> Iterator[str]:
    """Canonical redundant pairwise AMO clauses for local colour classes."""

    for centre, vertex in enumerate(vertices):
        if distances[centre] >= RADIUS:
            continue
        closed = [centre] + [position[other] for other in neighbours(vertex)]
        assert len(closed) == COLOR_COUNT
        for colour in range(COLOR_COUNT):
            for left, right in combinations(closed, 2):
                yield f"{-primary(left, colour)} {-primary(right, colour)} 0\n"


def all_clauses(
    vertices: list[int], distances: list[int], position: dict[int, int], base_stats: dict[str, int]
) -> Iterator[str]:
    # The base stream needs its original header count only for its internal
    # variable layout; passing the base dimensions preserves its clauses.
    yield from base_clause_lines(vertices, distances, position, base_stats)
    yield from additional_clauses(vertices, distances, position)


def canonical_map(vertices: list[int], distances: list[int], stats: dict[str, int]) -> bytes:
    # Retain the full vertex table from the base map but identify this stronger
    # clause family explicitly.  It has the same variable numbering.
    base_stats = base_dimensions(vertices, distances)
    payload = json.loads(base_canonical_map(vertices, distances, base_stats))
    payload["schema"] = SCHEMA
    payload["counts"] = stats
    payload["augmentation"] = {
        "kind": "pairwise local colour AMO",
        "clauses_per_centre_colour": COLOR_COUNT * (COLOR_COUNT - 1) // 2,
        "logical_status": "entailed by base vertex exact-one plus local colour ALO",
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    vertices, distances, position = ball()
    base_stats = base_dimensions(vertices, distances)
    stats = dimensions(vertices, distances)
    assert stats["variables"] == 483681
    assert stats["local_pairwise_amo_clauses"] == 4755784
    assert stats["clauses"] == 5494321
    map_bytes = canonical_map(vertices, distances, stats)
    for output in (args.cnf, args.map, args.manifest):
        output.parent.mkdir(parents=True, exist_ok=True)

    digest = hashlib.sha256()
    clauses = 0
    with args.cnf.open("wb") as stream:
        header = f"p cnf {stats['variables']} {stats['clauses']}\n".encode("ascii")
        stream.write(header)
        digest.update(header)
        for clause in all_clauses(vertices, distances, position, base_stats):
            encoded = clause.encode("ascii")
            stream.write(encoded)
            digest.update(encoded)
            clauses += 1
    assert clauses == stats["clauses"]
    args.map.write_bytes(map_bytes)
    manifest = {
        "schema": SCHEMA,
        "base_schema": BASE_SCHEMA,
        "cnf_sha256": digest.hexdigest(),
        "map_sha256": hashlib.sha256(map_bytes).hexdigest(),
        "counts": stats,
        "layer_sizes": [sum(distance == layer for distance in distances) for layer in range(RADIUS + 1)],
        "symmetry_units": [
            {"vertex_position": vertex, "mask": vertices[vertex], "colour": colour}
            for vertex, colour in symmetry_units(vertices, distances, position)
        ],
    }
    args.manifest.write_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
