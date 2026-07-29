#!/usr/bin/env python3
"""Add the sound diagonal-S15 matching normalization to the pairwise CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterator

from generate_radius4_generic_sinz_cnf import ROOT, ball, primary, symmetry_units
from generate_radius4_generic_sinz_cnf import dimensions as sinz_dimensions
from generate_radius4_generic_pairwise_cnf import (
    SCHEMA as PAIRWISE_SCHEMA,
    all_clauses as pairwise_clauses,
    canonical_map as pairwise_map,
    dimensions as pairwise_dimensions,
)


SCHEMA = "odd-graph-o16-radius4-diagonal-matching-symbreak-v1"
COLOR_ONE = 1
N = 15


def partitions(total: int, ceiling: int | None = None) -> Iterator[tuple[int, ...]]:
    """Integer partitions in deterministic non-increasing order."""

    if total == 0:
        yield ()
        return
    if ceiling is None or ceiling > total:
        ceiling = total
    for first in range(ceiling, 0, -1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def representative(partition: tuple[int, ...]) -> tuple[int, ...]:
    """The standard contiguous-cycle permutation for one cycle partition."""

    image = [0] * N
    cursor = 0
    for length in partition:
        for offset in range(length):
            image[cursor + offset] = cursor + ((offset + 1) % length)
        cursor += length
    assert cursor == N
    return tuple(image)


PARTITIONS = tuple(partitions(N))
REPRESENTATIVES = tuple(representative(partition) for partition in PARTITIONS)
assert len(PARTITIONS) == 176 and len(set(REPRESENTATIVES)) == 176


def c_position(position: dict[int, int], row: int, column: int) -> int:
    """C_(u,i) for u the (row+1)-th non-special complement point."""

    mask = (ROOT ^ (1 << column)) | (1 << (15 + row + 1))
    return position[mask]


def symmetry_extension(position: dict[int, int], selector_start: int) -> Iterator[str]:
    """ALO over cycle types, then selector -> colour-1 matching literals."""

    selectors = [selector_start + item for item in range(len(REPRESENTATIVES))]
    yield " ".join(str(item) for item in selectors) + " 0\n"
    for item, permutation in enumerate(REPRESENTATIVES):
        selector = selectors[item]
        for row, column in enumerate(permutation):
            yield f"{-selector} {primary(c_position(position, row, column), COLOR_ONE)} 0\n"


def dimensions(vertices: list[int], distances: list[int]) -> dict[str, int]:
    stats = dict(pairwise_dimensions(vertices, distances))
    stats["diagonal_matching_selectors"] = len(REPRESENTATIVES)
    stats["diagonal_matching_clauses"] = 1 + len(REPRESENTATIVES) * N
    stats["variables"] += len(REPRESENTATIVES)
    stats["clauses"] += stats["diagonal_matching_clauses"]
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    vertices, distances, position = ball()
    sinz_stats = sinz_dimensions(vertices, distances)
    pairwise_stats = pairwise_dimensions(vertices, distances)
    stats = dimensions(vertices, distances)
    assert pairwise_stats["variables"] == 483681 and pairwise_stats["clauses"] == 5494321
    assert stats["variables"] == 483857 and stats["clauses"] == 5496962
    assert all(distances[c_position(position, row, column)] == 2 for row in range(N) for column in range(N))
    map_payload = json.loads(pairwise_map(vertices, distances, pairwise_stats))
    map_payload["schema"] = SCHEMA
    map_payload["counts"] = stats
    map_payload["diagonal_matching"] = {
        "special_colour": COLOR_ONE,
        "rows": "u=B_{row+1}, row=0..14",
        "columns": "i=A_column, column=0..14",
        "partitions": [list(partition) for partition in PARTITIONS],
        "representatives": [list(permutation) for permutation in REPRESENTATIVES],
        "selector_start": pairwise_stats["variables"] + 1,
    }
    map_bytes = (json.dumps(map_payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    for output in (args.cnf, args.map, args.manifest):
        output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    clauses = 0
    with args.cnf.open("wb") as stream:
        header = f"p cnf {stats['variables']} {stats['clauses']}\n".encode("ascii")
        stream.write(header)
        digest.update(header)
        for line in pairwise_clauses(vertices, distances, position, sinz_stats):
            encoded = line.encode("ascii")
            stream.write(encoded)
            digest.update(encoded)
            clauses += 1
        for line in symmetry_extension(position, pairwise_stats["variables"] + 1):
            encoded = line.encode("ascii")
            stream.write(encoded)
            digest.update(encoded)
            clauses += 1
    assert clauses == stats["clauses"]
    args.map.write_bytes(map_bytes)
    manifest = {
        "schema": SCHEMA, "parent_schema": PAIRWISE_SCHEMA,
        "cnf_sha256": digest.hexdigest(), "map_sha256": hashlib.sha256(map_bytes).hexdigest(),
        "counts": stats,
        "parent_dimensions": pairwise_stats,
        "layer_sizes": [sum(distance == level for distance in distances) for level in range(5)],
        "symmetry_units": [{"vertex_position": vertex, "mask": vertices[vertex], "colour": colour} for vertex, colour in symmetry_units(vertices, distances, position)],
        "diagonal_matching_partitions": [list(partition) for partition in PARTITIONS],
        "selector_start": pairwise_stats["variables"] + 1,
    }
    args.manifest.write_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({
        "schema": SCHEMA, "cnf_sha256": manifest["cnf_sha256"], "map_sha256": manifest["map_sha256"],
        "counts": stats, "selector_start": manifest["selector_start"], "conjugacy_classes": len(PARTITIONS),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
