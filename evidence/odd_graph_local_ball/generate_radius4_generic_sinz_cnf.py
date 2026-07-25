#!/usr/bin/env python3
"""Emit the complete, symmetry-normalized radius-4 O_16 cover CNF.

The model has one primary variable x(v,c) for every vertex of the
radius-4 ball and every colour.  A Sinz sequential counter gives each
vertex exactly one colour.  At every centre through radius 3, one
at-least-one clause for each colour is enough: with 17 vertices that
already have one colour, these 17 clauses force every colour exactly
once.  Thus this is equisatisfiable with the generic local-cover model,
not a finite-field or other construction ansatz.

The generator deliberately uses only the Python standard library and a
fixed DIMACS order.  ``verify_radius4_generic_sinz_cnf.py`` rederives
the graph, clauses, hashes, and counts without importing this module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path
from typing import Iterator


POINT_COUNT = 31
SUBSET_SIZE = 15
COLOR_COUNT = 17
RADIUS = 4
FULL_MASK = (1 << POINT_COUNT) - 1
ROOT = (1 << SUBSET_SIZE) - 1
SCHEMA = "odd-graph-o16-radius4-generic-sinz-v1"


def neighbours(vertex: int) -> Iterator[int]:
    """Yield the 16 disjoint 15-subsets in ascending omitted-bit order."""

    complement = FULL_MASK ^ vertex
    remaining = complement
    while remaining:
        omitted_bit = remaining & -remaining
        remaining ^= omitted_bit
        yield complement ^ omitted_bit


def ball() -> tuple[list[int], list[int], dict[int, int]]:
    """Breadth-first radius-4 ball in a fixed, independently reproducible order."""

    vertices = [ROOT]
    distances = [0]
    position = {ROOT: 0}
    queue = deque([ROOT])
    while queue:
        vertex = queue.popleft()
        distance = distances[position[vertex]]
        if distance == RADIUS:
            continue
        for adjacent in neighbours(vertex):
            if adjacent not in position:
                position[adjacent] = len(vertices)
                vertices.append(adjacent)
                distances.append(distance + 1)
                queue.append(adjacent)
    return vertices, distances, position


def primary(vertex_position: int, colour: int) -> int:
    return vertex_position * COLOR_COUNT + colour + 1


def auxiliary(vertex_position: int, counter_position: int, primary_count: int) -> int:
    """Sinz state s_1..s_16; counter_position is zero-based."""

    return primary_count + vertex_position * (COLOR_COUNT - 1) + counter_position + 1


def symmetry_units(vertices: list[int], distances: list[int], position: dict[int, int]) -> list[tuple[int, int]]:
    """The 17 + 15 normalizations used by the generic model, as (v, colour)."""

    units = [(position[ROOT], 0)]
    root_neighbours = list(neighbours(ROOT))
    for colour, vertex in enumerate(root_neighbours, start=1):
        units.append((position[vertex], colour))
    first_branch = [vertex for vertex in neighbours(root_neighbours[0]) if vertex != ROOT]
    assert len(first_branch) == 15
    assert all(distances[position[vertex]] == 2 for vertex in first_branch)
    for colour, vertex in enumerate(first_branch, start=2):
        units.append((position[vertex], colour))
    assert len(units) == 32
    assert len({vertex for vertex, _ in units}) == 32
    return units


def dimensions(vertices: list[int], distances: list[int]) -> dict[str, int]:
    primary_count = len(vertices) * COLOR_COUNT
    auxiliary_count = len(vertices) * (COLOR_COUNT - 1)
    constrained_centres = sum(distance < RADIUS for distance in distances)
    vertex_alo_clauses = len(vertices)
    # Sinz AMO with n=17: 3n-4 = 47 clauses per vertex.
    vertex_amo_clauses = len(vertices) * (3 * COLOR_COUNT - 4)
    neighbourhood_alo_clauses = constrained_centres * COLOR_COUNT
    symmetry_clause_count = 32
    return {
        "primary_variables": primary_count,
        "auxiliary_variables": auxiliary_count,
        "variables": primary_count + auxiliary_count,
        "vertices": len(vertices),
        "constrained_centres": constrained_centres,
        "vertex_alo_clauses": vertex_alo_clauses,
        "vertex_amo_clauses": vertex_amo_clauses,
        "neighbourhood_alo_clauses": neighbourhood_alo_clauses,
        "symmetry_unit_clauses": symmetry_clause_count,
        "clauses": vertex_alo_clauses
        + vertex_amo_clauses
        + neighbourhood_alo_clauses
        + symmetry_clause_count,
    }


def clause_lines(
    vertices: list[int], distances: list[int], position: dict[int, int], stats: dict[str, int]
) -> Iterator[str]:
    """Return every DIMACS clause, excluding header, in its canonical order."""

    primary_count = stats["primary_variables"]
    for vertex_position in range(len(vertices)):
        yield " ".join(str(primary(vertex_position, colour)) for colour in range(COLOR_COUNT)) + " 0\n"
        yield f"{-primary(vertex_position, 0)} {auxiliary(vertex_position, 0, primary_count)} 0\n"
        for item in range(1, COLOR_COUNT - 1):
            previous = auxiliary(vertex_position, item - 1, primary_count)
            current = auxiliary(vertex_position, item, primary_count)
            yield f"{-primary(vertex_position, item)} {current} 0\n"
            yield f"{-previous} {current} 0\n"
            yield f"{-primary(vertex_position, item)} {-previous} 0\n"
        yield f"{-primary(vertex_position, COLOR_COUNT - 1)} {-auxiliary(vertex_position, COLOR_COUNT - 2, primary_count)} 0\n"

    for centre_position, vertex in enumerate(vertices):
        if distances[centre_position] >= RADIUS:
            continue
        closed_positions = [centre_position] + [position[item] for item in neighbours(vertex)]
        assert len(closed_positions) == COLOR_COUNT
        for colour in range(COLOR_COUNT):
            yield " ".join(str(primary(item, colour)) for item in closed_positions) + " 0\n"

    for vertex_position, colour in symmetry_units(vertices, distances, position):
        yield f"{primary(vertex_position, colour)} 0\n"


def canonical_map(vertices: list[int], distances: list[int], stats: dict[str, int]) -> bytes:
    payload = {
        "schema": SCHEMA,
        "constants": {"point_count": POINT_COUNT, "subset_size": SUBSET_SIZE, "colours": COLOR_COUNT, "radius": RADIUS},
        "variable_layout": {
            "primary": "x(v,c) = 17*v+c+1 for 0<=v<14657, 0<=c<17",
            "sinz_auxiliary": "s(v,i) = 249169+16*v+i+1 for 0<=v<14657, 0<=i<16",
        },
        "vertices": [{"position": i, "mask": vertex, "distance": distances[i]} for i, vertex in enumerate(vertices)],
        "counts": stats,
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_cnf(path: Path, vertices: list[int], distances: list[int], position: dict[int, int], stats: dict[str, int]) -> str:
    digest = hashlib.sha256()
    clause_count = 0
    with path.open("wb") as stream:
        header = f"p cnf {stats['variables']} {stats['clauses']}\n".encode("ascii")
        stream.write(header)
        digest.update(header)
        for line in clause_lines(vertices, distances, position, stats):
            encoded = line.encode("ascii")
            stream.write(encoded)
            digest.update(encoded)
            clause_count += 1
    assert clause_count == stats["clauses"]
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnf", type=Path, required=True, help="DIMACS CNF output path")
    parser.add_argument("--map", type=Path, required=True, help="canonical vertex/variable-map JSON output")
    parser.add_argument("--manifest", type=Path, required=True, help="deterministic metadata JSON output")
    args = parser.parse_args()

    vertices, distances, position = ball()
    stats = dimensions(vertices, distances)
    assert [sum(item == layer for item in distances) for layer in range(5)] == [1, 16, 240, 1800, 12600]
    assert stats["vertices"] == 14657
    assert stats["constrained_centres"] == 2057
    assert stats["primary_variables"] == 249169
    assert stats["variables"] == 483681
    assert stats["clauses"] == 738537
    map_bytes = canonical_map(vertices, distances, stats)

    for output in (args.cnf, args.map, args.manifest):
        output.parent.mkdir(parents=True, exist_ok=True)
    cnf_sha256 = write_cnf(args.cnf, vertices, distances, position, stats)
    args.map.write_bytes(map_bytes)
    manifest = {
        "schema": SCHEMA,
        "cnf_sha256": cnf_sha256,
        "map_sha256": hashlib.sha256(map_bytes).hexdigest(),
        "counts": stats,
        "layer_sizes": [sum(item == layer for item in distances) for layer in range(5)],
        "symmetry_units": [
            {"vertex_position": item, "mask": vertices[item], "colour": colour}
            for item, colour in symmetry_units(vertices, distances, position)
        ],
    }
    args.manifest.write_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
