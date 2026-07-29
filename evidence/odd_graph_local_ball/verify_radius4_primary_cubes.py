#!/usr/bin/env python3
"""Independently verify a deterministic exhaustive primary-cube manifest."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path
from typing import Iterator


POINTS, SUBSET, COLORS, DEPTH = 31, 15, 17, 4
ALL = (1 << POINTS) - 1
ROOT = (1 << SUBSET) - 1
SCHEMA = "odd-graph-o16-primary-cube-partition-v1"


def neighbours(vertex: int) -> Iterator[int]:
    rest = ALL ^ vertex
    while rest:
        bit = rest & -rest
        rest ^= bit
        yield (ALL ^ vertex) ^ bit


def ball() -> tuple[list[int], list[int], dict[int, int]]:
    vertices, levels, lookup = [ROOT], [0], {ROOT: 0}
    queue = deque([ROOT])
    while queue:
        vertex = queue.popleft()
        if levels[lookup[vertex]] == DEPTH:
            continue
        for other in neighbours(vertex):
            if other not in lookup:
                lookup[other] = len(vertices)
                vertices.append(other)
                levels.append(levels[lookup[vertex]] + 1)
                queue.append(other)
    return vertices, levels, lookup


def primary(vertex: int, colour: int) -> int:
    return COLORS * vertex + colour + 1


def normalized_vertices(vertices: list[int], levels: list[int], lookup: dict[int, int]) -> set[int]:
    fixed = {lookup[ROOT]}
    root_neighbours = list(neighbours(ROOT))
    fixed.update(lookup[vertex] for vertex in root_neighbours)
    branch = [vertex for vertex in neighbours(root_neighbours[0]) if vertex != ROOT]
    assert len(branch) == 15 and all(levels[lookup[vertex]] == 2 for vertex in branch)
    fixed.update(lookup[vertex] for vertex in branch)
    assert len(fixed) == 32
    return fixed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--parent-cnf", type=Path, required=True)
    args = parser.parse_args()
    raw = args.manifest.read_bytes()
    payload = json.loads(raw)
    if payload.get("schema") != SCHEMA:
        raise AssertionError("wrong cube manifest schema")
    parent_hash = hashlib.sha256(args.parent_cnf.read_bytes()).hexdigest()
    if payload.get("parent_cnf_sha256") != parent_hash:
        raise AssertionError("manifest parent hash does not match supplied CNF")
    depth = payload.get("depth")
    if not isinstance(depth, int) or not 1 <= depth <= 3 or payload.get("colour_count") != COLORS:
        raise AssertionError("invalid cube depth or colour count")
    vertices, levels, lookup = ball()
    assert [sum(level == layer for level in levels) for layer in range(5)] == [1, 16, 240, 1800, 12600]
    fixed = normalized_vertices(vertices, levels, lookup)
    split_vertices = [vertex for vertex in range(len(vertices)) if vertex not in fixed][:depth]
    if payload.get("split_vertex_positions") != split_vertices:
        raise AssertionError("split vertices are not the canonical first free rows")
    leaves = payload.get("leaves")
    if payload.get("leaf_count") != COLORS ** depth or not isinstance(leaves, list) or len(leaves) != COLORS ** depth:
        raise AssertionError("leaf count is not exhaustive")
    for leaf_id, colours in enumerate(itertools.product(range(COLORS), repeat=depth)):
        expected = {"id": leaf_id, "colours": list(colours), "assumptions": [primary(vertex, colour) for vertex, colour in zip(split_vertices, colours)]}
        if leaves[leaf_id] != expected:
            raise AssertionError(f"leaf {leaf_id} is not the canonical complete cube")
    unhashed = dict(payload)
    recorded = unhashed.pop("sha256_without_hash", None)
    expected_hash = hashlib.sha256((json.dumps(unhashed, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")).hexdigest()
    if recorded != expected_hash:
        raise AssertionError("manifest self-hash mismatch")
    print(json.dumps({
        "status": "PASS", "schema": SCHEMA, "parent_cnf_sha256": parent_hash,
        "depth": depth, "split_vertex_positions": split_vertices,
        "leaf_count": COLORS ** depth, "manifest_sha256_without_hash": recorded,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
