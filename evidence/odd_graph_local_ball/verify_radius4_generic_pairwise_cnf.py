#!/usr/bin/env python3
"""Independently verify the generic radius-4 CNF with pairwise local AMOs.

This does not import either generator.  It reconstructs the ball and
the complete canonical DIMACS stream, including the redundant local
pairwise clauses, then checks both that stream's hash and the supplied
manifest/map.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path
from typing import Iterator


POINTS, SUBSET, COLORS, DEPTH = 31, 15, 17, 4
ALL = (1 << POINTS) - 1
ROOT = (1 << SUBSET) - 1
SCHEMA = "odd-graph-o16-radius4-generic-pairwise-v1"


def adjacent(vertex: int) -> Iterator[int]:
    complement = ALL ^ vertex
    while complement:
        bit = complement & -complement
        complement ^= bit
        yield (ALL ^ vertex) ^ bit


def reconstruct() -> tuple[list[int], list[int], dict[int, int]]:
    vertices, distance, lookup = [ROOT], [0], {ROOT: 0}
    queue = deque([ROOT])
    while queue:
        vertex = queue.popleft()
        level = distance[lookup[vertex]]
        if level == DEPTH:
            continue
        for other in adjacent(vertex):
            if other not in lookup:
                lookup[other] = len(vertices)
                vertices.append(other)
                distance.append(level + 1)
                queue.append(other)
    return vertices, distance, lookup


def x(vertex: int, colour: int) -> int:
    return COLORS * vertex + colour + 1


def sinz(vertex: int, item: int, primary_count: int) -> int:
    return primary_count + (COLORS - 1) * vertex + item + 1


def stats_for(distance: list[int]) -> dict[str, int]:
    vertices = len(distance)
    centres = sum(level < DEPTH for level in distance)
    primary_count = vertices * COLORS
    auxiliary_count = vertices * (COLORS - 1)
    vertex_alo = vertices
    vertex_amo = vertices * (3 * COLORS - 4)
    local_alo = centres * COLORS
    units = 32
    pairwise = centres * COLORS * (COLORS * (COLORS - 1) // 2)
    return {
        "primary_variables": primary_count,
        "auxiliary_variables": auxiliary_count,
        "variables": primary_count + auxiliary_count,
        "vertices": vertices,
        "constrained_centres": centres,
        "vertex_alo_clauses": vertex_alo,
        "vertex_amo_clauses": vertex_amo,
        "neighbourhood_alo_clauses": local_alo,
        "symmetry_unit_clauses": units,
        "local_pairwise_amo_clauses": pairwise,
        "clauses": vertex_alo + vertex_amo + local_alo + units + pairwise,
    }


def units(vertices: list[int], distance: list[int], lookup: dict[int, int]) -> list[tuple[int, int]]:
    result = [(lookup[ROOT], 0)]
    root_neighbours = list(adjacent(ROOT))
    result.extend((lookup[vertex], colour) for colour, vertex in enumerate(root_neighbours, 1))
    branch = [vertex for vertex in adjacent(root_neighbours[0]) if vertex != ROOT]
    assert len(branch) == 15 and all(distance[lookup[vertex]] == 2 for vertex in branch)
    result.extend((lookup[vertex], colour) for colour, vertex in enumerate(branch, 2))
    assert len(result) == 32 and len({vertex for vertex, _ in result}) == 32
    return result


def expected_stream(
    vertices: list[int], distance: list[int], lookup: dict[int, int], stats: dict[str, int]
) -> Iterator[bytes]:
    yield f"p cnf {stats['variables']} {stats['clauses']}\n".encode("ascii")
    primary_count = stats["primary_variables"]
    for vertex in range(len(vertices)):
        yield (" ".join(str(x(vertex, colour)) for colour in range(COLORS)) + " 0\n").encode("ascii")
        yield f"{-x(vertex, 0)} {sinz(vertex, 0, primary_count)} 0\n".encode("ascii")
        for colour in range(1, COLORS - 1):
            before, current = sinz(vertex, colour - 1, primary_count), sinz(vertex, colour, primary_count)
            yield f"{-x(vertex, colour)} {current} 0\n".encode("ascii")
            yield f"{-before} {current} 0\n".encode("ascii")
            yield f"{-x(vertex, colour)} {-before} 0\n".encode("ascii")
        yield f"{-x(vertex, COLORS - 1)} {-sinz(vertex, COLORS - 2, primary_count)} 0\n".encode("ascii")
    for centre, vertex in enumerate(vertices):
        if distance[centre] == DEPTH:
            continue
        closed = [centre] + [lookup[other] for other in adjacent(vertex)]
        for colour in range(COLORS):
            yield (" ".join(str(x(item, colour)) for item in closed) + " 0\n").encode("ascii")
    for vertex, colour in units(vertices, distance, lookup):
        yield f"{x(vertex, colour)} 0\n".encode("ascii")
    for centre, vertex in enumerate(vertices):
        if distance[centre] == DEPTH:
            continue
        closed = [centre] + [lookup[other] for other in adjacent(vertex)]
        for colour in range(COLORS):
            for left, right in combinations(closed, 2):
                yield f"{-x(left, colour)} {-x(right, colour)} 0\n".encode("ascii")


def parse(path: Path) -> tuple[int, int, int, Counter[int], str]:
    variables = clauses_in_header = None
    clauses = 0
    lengths: Counter[int] = Counter()
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for raw in stream:
            digest.update(raw)
            fields = raw.split()
            if not fields or fields[0] == b"c":
                raise ValueError("canonical DIMACS contains a blank/comment line")
            if fields[0] == b"p":
                if variables is not None or len(fields) != 4 or fields[1] != b"cnf":
                    raise ValueError("invalid DIMACS header")
                variables, clauses_in_header = int(fields[2]), int(fields[3])
                continue
            if variables is None or fields[-1] != b"0":
                raise ValueError("malformed DIMACS clause")
            literals = [int(field) for field in fields[:-1]]
            if not literals or any(literal == 0 or abs(literal) > variables for literal in literals):
                raise ValueError("literal outside header range")
            clauses += 1
            lengths[len(literals)] += 1
    if variables is None or clauses_in_header is None:
        raise ValueError("no DIMACS header")
    return variables, clauses_in_header, clauses, lengths, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    vertices, distance, lookup = reconstruct()
    layers = [sum(level == item for level in distance) for item in range(DEPTH + 1)]
    assert layers == [1, 16, 240, 1800, 12600]
    stats = stats_for(distance)
    assert stats["variables"] == 483681 and stats["clauses"] == 5494321
    assert stats["local_pairwise_amo_clauses"] == 4755784
    expected_hash = hashlib.sha256()
    expected_count = 0
    expected_lengths: Counter[int] = Counter()
    for line in expected_stream(vertices, distance, lookup, stats):
        expected_hash.update(line)
        if not line.startswith(b"p "):
            expected_count += 1
            expected_lengths[len(line.split()) - 1] += 1
    assert expected_count == stats["clauses"]
    actual_variables, header_clauses, actual_count, actual_lengths, actual_hash = parse(args.cnf)
    if (actual_variables, header_clauses, actual_count) != (stats["variables"], stats["clauses"], stats["clauses"]):
        raise AssertionError("header or clause count does not match independent dimensions")
    if actual_lengths != expected_lengths or actual_hash != expected_hash.hexdigest():
        raise AssertionError("CNF differs from independently reconstructed canonical pairwise instance")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA or manifest.get("counts") != stats:
        raise AssertionError("manifest schema/counts mismatch")
    if manifest.get("cnf_sha256") != actual_hash or manifest.get("layer_sizes") != layers:
        raise AssertionError("manifest hash/layers mismatch")
    expected_units = [{"vertex_position": vertex, "mask": vertices[vertex], "colour": colour} for vertex, colour in units(vertices, distance, lookup)]
    if manifest.get("symmetry_units") != expected_units:
        raise AssertionError("manifest units mismatch")
    map_bytes = args.map.read_bytes()
    if manifest.get("map_sha256") != hashlib.sha256(map_bytes).hexdigest():
        raise AssertionError("map hash mismatch")
    map_payload = json.loads(map_bytes)
    if map_payload.get("schema") != SCHEMA or map_payload.get("counts") != stats:
        raise AssertionError("map schema/counts mismatch")
    if map_payload.get("vertices") != [
        {"position": item, "mask": vertex, "distance": distance[item]} for item, vertex in enumerate(vertices)
    ]:
        raise AssertionError("map vertex table mismatch")
    print(json.dumps({
        "status": "PASS", "schema": SCHEMA, "cnf_sha256": actual_hash,
        "map_sha256": hashlib.sha256(map_bytes).hexdigest(), "counts": stats,
        "layer_sizes": layers, "symmetry_units": 32,
        "clause_lengths": {str(length): count for length, count in sorted(actual_lengths.items())},
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
