#!/usr/bin/env python3
"""Independently audit a generated generic radius-4 O_16 Sinz CNF.

This file intentionally does not import the generator.  It separately
reconstructs the odd-graph ball, normal-form symmetry assignments, and
the canonical DIMACS stream, then compares the independently generated
SHA-256 digest to the supplied file.  It also parses the DIMACS file to
check header, clause count, clause lengths, and literal bounds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from pathlib import Path
from typing import Iterator


NPOINTS = 31
K = 15
NCOLORS = 17
DEPTH = 4
UNIVERSE = (1 << NPOINTS) - 1
BASE = (1 << K) - 1
SCHEMA = "odd-graph-o16-radius4-generic-sinz-v1"


def disjoint_neighbours(mask: int) -> Iterator[int]:
    complement = UNIVERSE ^ mask
    while complement:
        bit = complement & -complement
        complement ^= bit
        yield (UNIVERSE ^ mask) ^ bit


def reconstruct_ball() -> tuple[list[int], list[int], dict[int, int]]:
    masks: list[int] = [BASE]
    levels: list[int] = [0]
    lookup = {BASE: 0}
    pending = deque([BASE])
    while pending:
        here = pending.popleft()
        level = levels[lookup[here]]
        if level == DEPTH:
            continue
        for there in disjoint_neighbours(here):
            if there not in lookup:
                lookup[there] = len(masks)
                masks.append(there)
                levels.append(level + 1)
                pending.append(there)
    return masks, levels, lookup


def x(vertex: int, colour: int) -> int:
    return NCOLORS * vertex + colour + 1


def s(vertex: int, index: int, primary_count: int) -> int:
    return primary_count + (NCOLORS - 1) * vertex + index + 1


def audited_dimensions(levels: list[int]) -> dict[str, int]:
    vertex_count = len(levels)
    centres = sum(level < DEPTH for level in levels)
    primary_count = vertex_count * NCOLORS
    auxiliary_count = vertex_count * (NCOLORS - 1)
    vertex_alo = vertex_count
    vertex_amo = vertex_count * (3 * NCOLORS - 4)
    local_alo = centres * NCOLORS
    units = 32
    return {
        "primary_variables": primary_count,
        "auxiliary_variables": auxiliary_count,
        "variables": primary_count + auxiliary_count,
        "vertices": vertex_count,
        "constrained_centres": centres,
        "vertex_alo_clauses": vertex_alo,
        "vertex_amo_clauses": vertex_amo,
        "neighbourhood_alo_clauses": local_alo,
        "symmetry_unit_clauses": units,
        "clauses": vertex_alo + vertex_amo + local_alo + units,
    }


def normal_form_units(masks: list[int], levels: list[int], lookup: dict[int, int]) -> list[tuple[int, int]]:
    fixed = [(lookup[BASE], 0)]
    first_layer = list(disjoint_neighbours(BASE))
    for colour, mask in enumerate(first_layer, 1):
        fixed.append((lookup[mask], colour))
    # Global colour relabelling fixes the closed root neighbourhood.
    assert [(vertex, colour) for vertex, colour in fixed[:17]] == [(i, i) for i in range(17)]
    branch = [mask for mask in disjoint_neighbours(first_layer[0]) if mask != BASE]
    assert len(branch) == 15
    assert all(levels[lookup[mask]] == 2 for mask in branch)
    for colour, mask in enumerate(branch, 2):
        fixed.append((lookup[mask], colour))
    # The remaining normalization is the free S_15 action on root points.
    assert len(fixed) == 32 and len({vertex for vertex, _ in fixed}) == 32
    return fixed


def expected_lines(masks: list[int], levels: list[int], lookup: dict[int, int], stats: dict[str, int]) -> Iterator[bytes]:
    yield f"p cnf {stats['variables']} {stats['clauses']}\n".encode("ascii")
    primary_count = stats["primary_variables"]
    for vertex in range(len(masks)):
        yield (" ".join(str(x(vertex, colour)) for colour in range(NCOLORS)) + " 0\n").encode("ascii")
        yield f"{-x(vertex, 0)} {s(vertex, 0, primary_count)} 0\n".encode("ascii")
        for colour in range(1, NCOLORS - 1):
            previous = s(vertex, colour - 1, primary_count)
            current = s(vertex, colour, primary_count)
            yield f"{-x(vertex, colour)} {current} 0\n".encode("ascii")
            yield f"{-previous} {current} 0\n".encode("ascii")
            yield f"{-x(vertex, colour)} {-previous} 0\n".encode("ascii")
        yield f"{-x(vertex, NCOLORS - 1)} {-s(vertex, NCOLORS - 2, primary_count)} 0\n".encode("ascii")
    for centre, mask in enumerate(masks):
        if levels[centre] == DEPTH:
            continue
        closed = [centre] + [lookup[neighbour] for neighbour in disjoint_neighbours(mask)]
        assert len(closed) == NCOLORS
        for colour in range(NCOLORS):
            yield (" ".join(str(x(vertex, colour)) for vertex in closed) + " 0\n").encode("ascii")
    for vertex, colour in normal_form_units(masks, levels, lookup):
        yield f"{x(vertex, colour)} 0\n".encode("ascii")


def parse_dimacs(path: Path) -> tuple[int, int, int, Counter[int], str]:
    header_variables = header_clauses = None
    clauses = 0
    lengths: Counter[int] = Counter()
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for raw in stream:
            digest.update(raw)
            if raw.startswith(b"c"):
                raise ValueError("canonical certificate must not contain DIMACS comments")
            fields = raw.split()
            if not fields:
                raise ValueError("blank DIMACS line")
            if fields[0] == b"p":
                if header_variables is not None or len(fields) != 4 or fields[1] != b"cnf":
                    raise ValueError("invalid or duplicate DIMACS header")
                header_variables, header_clauses = int(fields[2]), int(fields[3])
                continue
            if header_variables is None:
                raise ValueError("clause precedes DIMACS header")
            if fields[-1] != b"0":
                raise ValueError("unterminated DIMACS clause")
            literals = [int(item) for item in fields[:-1]]
            if not literals or any(item == 0 or abs(item) > header_variables for item in literals):
                raise ValueError("invalid DIMACS literal")
            clauses += 1
            lengths[len(literals)] += 1
    if header_variables is None or header_clauses is None:
        raise ValueError("missing DIMACS header")
    return header_variables, header_clauses, clauses, lengths, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    args = parser.parse_args()

    masks, levels, lookup = reconstruct_ball()
    layers = [sum(level == item for level in levels) for item in range(DEPTH + 1)]
    if layers != [1, 16, 240, 1800, 12600]:
        raise AssertionError(f"wrong ball layer sizes: {layers}")
    stats = audited_dimensions(levels)
    expected_stats = {
        "vertices": 14657, "constrained_centres": 2057, "primary_variables": 249169,
        "auxiliary_variables": 234512, "variables": 483681, "clauses": 738537,
        "vertex_alo_clauses": 14657, "vertex_amo_clauses": 688879,
        "neighbourhood_alo_clauses": 34969, "symmetry_unit_clauses": 32,
    }
    if stats != expected_stats:
        raise AssertionError(f"wrong model dimensions: {stats}")
    units = normal_form_units(masks, levels, lookup)
    expected_digest = hashlib.sha256()
    expected_clause_count = 0
    expected_lengths: Counter[int] = Counter()
    for line in expected_lines(masks, levels, lookup, stats):
        expected_digest.update(line)
        if not line.startswith(b"p "):
            expected_clause_count += 1
            expected_lengths[len(line.split()) - 1] += 1
    assert expected_clause_count == stats["clauses"]

    header_variables, header_clauses, actual_clauses, actual_lengths, actual_digest = parse_dimacs(args.cnf)
    if (header_variables, header_clauses, actual_clauses) != (stats["variables"], stats["clauses"], stats["clauses"]):
        raise AssertionError("DIMACS header or parsed clause count disagrees with audited dimensions")
    if actual_lengths != expected_lengths:
        raise AssertionError(f"DIMACS clause-length distribution differs: {actual_lengths}")
    if actual_digest != expected_digest.hexdigest():
        raise AssertionError("CNF SHA-256 differs from independently reconstructed canonical stream")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA or manifest.get("counts") != stats:
        raise AssertionError("manifest schema or dimensions disagree with audit")
    if manifest.get("cnf_sha256") != actual_digest or manifest.get("layer_sizes") != layers:
        raise AssertionError("manifest CNF hash or layer sizes disagree with audit")
    if manifest.get("symmetry_units") != [
        {"vertex_position": vertex, "mask": masks[vertex], "colour": colour} for vertex, colour in units
    ]:
        raise AssertionError("manifest symmetry WLOG assignments disagree with independent reconstruction")
    map_bytes = args.map.read_bytes()
    if manifest.get("map_sha256") != hashlib.sha256(map_bytes).hexdigest():
        raise AssertionError("manifest map hash disagrees with map file")
    parsed_map = json.loads(map_bytes)
    if parsed_map.get("schema") != SCHEMA or parsed_map.get("counts") != stats:
        raise AssertionError("map schema or dimensions disagree with audit")
    map_vertices = parsed_map.get("vertices")
    if map_vertices != [
        {"position": vertex, "mask": mask, "distance": levels[vertex]}
        for vertex, mask in enumerate(masks)
    ]:
        raise AssertionError("map vertices disagree with independent BFS reconstruction")

    report = {
        "status": "PASS",
        "schema": SCHEMA,
        "cnf_sha256": actual_digest,
        "map_sha256": hashlib.sha256(map_bytes).hexdigest(),
        "layer_sizes": layers,
        "counts": stats,
        "clause_lengths": {str(length): count for length, count in sorted(actual_lengths.items())},
        "symmetry_units": len(units),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
