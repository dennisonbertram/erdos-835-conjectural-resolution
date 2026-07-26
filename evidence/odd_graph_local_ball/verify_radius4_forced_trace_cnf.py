#!/usr/bin/env python3
"""Independent byte and semantic audit of the forced-trace CNF.

This verifier intentionally imports neither CNF generator.  It separately
reconstructs the canonical radius-4 odd-graph ball, parent CNF/map/manifest,
the 1,680 forced traces, the trace map, and every added Sinz clause.  It also
exhaustively checks the 15-input Sinz template's projection against direct
pairwise at-most-one over all 2^15 primary assignments.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path
from typing import Iterator


PARENT_SCHEMA = "odd-graph-o16-radius4-generic-sinz-v1"
SCHEMA = "odd-graph-o16-radius4-plus-radius5-forced-trace-sinz-v1"
PINNED_PARENT_CNF = "0e66e3d7f4e15bd155db737092b8387b10540fd0e5bbcb56127c650baf6c54dc"
PINNED_PARENT_MAP = "ba4c9455a31907d3af5d58a143eaf2ce0a48517e2a26122f320cb71fcc3393e6"
PINNED_PARENT_MANIFEST = "9c5fd2e89ea69d9dc607e2e7793962c35b9e7b45597977eb3c3e93445c88b4f2"

POINTS = 31
SUBSET = 15
COLOURS = 17
RADIUS = 4
UNIVERSE = (1 << POINTS) - 1
ROOT = (1 << SUBSET) - 1
PARENT_VARIABLES = 483_681
PARENT_CLAUSES = 738_537
TRACE_COUNT = 1_680
TRACE_SIZE = 15
TRACE_AUX_PER_AMO = 14
TRACE_CLAUSES_PER_AMO = 41
TRACE_AMO_COUNT = TRACE_COUNT * COLOURS
ADDED_VARIABLES = TRACE_AMO_COUNT * TRACE_AUX_PER_AMO
ADDED_CLAUSES = TRACE_AMO_COUNT * TRACE_CLAUSES_PER_AMO
TOTAL_VARIABLES = PARENT_VARIABLES + ADDED_VARIABLES
TOTAL_CLAUSES = PARENT_CLAUSES + ADDED_CLAUSES


def adjacent_masks(mask: int) -> Iterator[int]:
    available = UNIVERSE ^ mask
    while available:
        omitted = available & -available
        available ^= omitted
        yield (UNIVERSE ^ mask) ^ omitted


def audited_ball() -> tuple[list[int], list[int], dict[int, int]]:
    masks = [ROOT]
    levels = [0]
    location = {ROOT: 0}
    queue = deque([ROOT])
    while queue:
        here = queue.popleft()
        level = levels[location[here]]
        if level == RADIUS:
            continue
        for there in adjacent_masks(here):
            if there not in location:
                location[there] = len(masks)
                masks.append(there)
                levels.append(level + 1)
                queue.append(there)
    return masks, levels, location


def parent_counts(levels: list[int]) -> dict[str, int]:
    vertices = len(levels)
    centres = sum(level < RADIUS for level in levels)
    primary_variables = vertices * COLOURS
    auxiliary_variables = vertices * (COLOURS - 1)
    return {
        "primary_variables": primary_variables,
        "auxiliary_variables": auxiliary_variables,
        "variables": primary_variables + auxiliary_variables,
        "vertices": vertices,
        "constrained_centres": centres,
        "vertex_alo_clauses": vertices,
        "vertex_amo_clauses": vertices * (3 * COLOURS - 4),
        "neighbourhood_alo_clauses": centres * COLOURS,
        "symmetry_unit_clauses": 32,
        "clauses": (
            vertices
            + vertices * (3 * COLOURS - 4)
            + centres * COLOURS
            + 32
        ),
    }


def parent_primary(vertex: int, colour: int) -> int:
    return COLOURS * vertex + colour + 1


def parent_auxiliary(vertex: int, item: int, primary_count: int) -> int:
    return primary_count + (COLOURS - 1) * vertex + item + 1


def normal_form(
    masks: list[int], levels: list[int], location: dict[int, int]
) -> list[tuple[int, int]]:
    units = [(location[ROOT], 0)]
    first_layer = list(adjacent_masks(ROOT))
    units.extend((location[mask], colour) for colour, mask in enumerate(first_layer, 1))
    branch = [mask for mask in adjacent_masks(first_layer[0]) if mask != ROOT]
    if len(branch) != 15 or any(levels[location[mask]] != 2 for mask in branch):
        raise AssertionError("independent residual-symmetry reconstruction failed")
    units.extend((location[mask], colour) for colour, mask in enumerate(branch, 2))
    if len(units) != 32 or len({vertex for vertex, _ in units}) != 32:
        raise AssertionError("wrong independent normal form")
    return units


def expected_parent_lines(
    masks: list[int],
    levels: list[int],
    location: dict[int, int],
    counts: dict[str, int],
) -> Iterator[bytes]:
    yield f"p cnf {counts['variables']} {counts['clauses']}\n".encode("ascii")
    primary_count = counts["primary_variables"]
    for vertex in range(len(masks)):
        yield (
            " ".join(str(parent_primary(vertex, colour)) for colour in range(COLOURS))
            + " 0\n"
        ).encode("ascii")
        yield (
            f"{-parent_primary(vertex, 0)} "
            f"{parent_auxiliary(vertex, 0, primary_count)} 0\n"
        ).encode("ascii")
        for item in range(1, COLOURS - 1):
            previous = parent_auxiliary(vertex, item - 1, primary_count)
            current = parent_auxiliary(vertex, item, primary_count)
            yield f"{-parent_primary(vertex, item)} {current} 0\n".encode("ascii")
            yield f"{-previous} {current} 0\n".encode("ascii")
            yield f"{-parent_primary(vertex, item)} {-previous} 0\n".encode(
                "ascii"
            )
        yield (
            f"{-parent_primary(vertex, COLOURS - 1)} "
            f"{-parent_auxiliary(vertex, COLOURS - 2, primary_count)} 0\n"
        ).encode("ascii")
    for centre, mask in enumerate(masks):
        if levels[centre] == RADIUS:
            continue
        closed = [centre] + [location[item] for item in adjacent_masks(mask)]
        if len(closed) != COLOURS:
            raise AssertionError("closed neighbourhood does not have 17 vertices")
        for colour in range(COLOURS):
            yield (
                " ".join(str(parent_primary(vertex, colour)) for vertex in closed)
                + " 0\n"
            ).encode("ascii")
    for vertex, colour in normal_form(masks, levels, location):
        yield f"{parent_primary(vertex, colour)} 0\n".encode("ascii")


def canonical_parent_map(
    masks: list[int], levels: list[int], counts: dict[str, int]
) -> bytes:
    payload = {
        "schema": PARENT_SCHEMA,
        "constants": {
            "point_count": POINTS,
            "subset_size": SUBSET,
            "colours": COLOURS,
            "radius": RADIUS,
        },
        "variable_layout": {
            "primary": "x(v,c) = 17*v+c+1 for 0<=v<14657, 0<=c<17",
            "sinz_auxiliary": (
                "s(v,i) = 249169+16*v+i+1 for 0<=v<14657, 0<=i<16"
            ),
        },
        "vertices": [
            {"position": position, "mask": mask, "distance": levels[position]}
            for position, mask in enumerate(masks)
        ],
        "counts": counts,
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def canonical_parent_manifest(
    masks: list[int],
    levels: list[int],
    location: dict[int, int],
    counts: dict[str, int],
    map_digest: str,
) -> bytes:
    payload = {
        "schema": PARENT_SCHEMA,
        "cnf_sha256": PINNED_PARENT_CNF,
        "map_sha256": map_digest,
        "counts": counts,
        "layer_sizes": [
            sum(level == layer for level in levels) for layer in range(RADIUS + 1)
        ],
        "symmetry_units": [
            {
                "vertex_position": vertex,
                "mask": masks[vertex],
                "colour": colour,
            }
            for vertex, colour in normal_form(masks, levels, location)
        ],
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def verify_exact_file(
    path: Path, expected_lines: Iterator[bytes], label: str
) -> tuple[str, int]:
    digest = hashlib.sha256()
    line_count = 0
    with path.open("rb") as actual:
        for line_count, expected in enumerate(expected_lines, 1):
            observed = actual.readline()
            if observed != expected:
                raise AssertionError(
                    f"{label} differs at canonical line {line_count}"
                )
            digest.update(observed)
        if actual.read(1):
            raise AssertionError(f"{label} has trailing bytes")
    return digest.hexdigest(), line_count


def verify_exact_bytes(path: Path, expected: bytes, label: str) -> str:
    observed = path.read_bytes()
    if observed != expected:
        raise AssertionError(f"{label} differs from independent canonical bytes")
    return hashlib.sha256(observed).hexdigest()


def forced_traces(
    masks: list[int], levels: list[int], location: dict[int, int]
) -> list[dict[str, object]]:
    groups: list[dict[str, object]] = []
    incidence: Counter[int] = Counter()
    seen: set[tuple[int, ...]] = set()
    for fixed_pair in combinations(range(15), 2):
        base = ROOT ^ (1 << fixed_pair[0]) ^ (1 << fixed_pair[1])
        for pivot in range(16):
            positions = []
            for partner in range(16):
                if partner == pivot:
                    continue
                mask = base | (1 << (15 + pivot)) | (1 << (15 + partner))
                if mask not in location:
                    raise AssertionError("forced-trace mask is absent from radius four")
                position = location[mask]
                if masks[position] != mask or levels[position] != 4:
                    raise AssertionError("forced-trace position is not canonical sphere four")
                positions.append(position)
                incidence[position] += 1
            key = tuple(positions)
            if len(positions) != 15 or len(set(positions)) != 15 or key in seen:
                raise AssertionError("invalid or repeated forced-trace star")
            seen.add(key)
            groups.append(
                {
                    "trace": len(groups),
                    "fixed_points": list(fixed_pair),
                    "moving_pivot": pivot,
                    "vertex_positions": positions,
                }
            )
    sphere_four = {
        position for position, level in enumerate(levels) if level == RADIUS
    }
    if len(groups) != TRACE_COUNT:
        raise AssertionError("wrong number of forced traces")
    if set(incidence) != sphere_four or set(incidence.values()) != {2}:
        raise AssertionError("sphere-four trace incidence is not exactly two")
    return groups


def canonical_trace_map(groups: list[dict[str, object]]) -> bytes:
    payload = {
        "schema": SCHEMA,
        "parent_map_sha256": PINNED_PARENT_MAP,
        "ordering": {
            "fixed_points": "lexicographic combinations(range(15),2)",
            "moving_pivot": "ascending range(16)",
            "other_moving": "ascending range(16) excluding moving_pivot",
        },
        "variable_layout": {
            "parent_primary": "x(v,c)=17*v+c+1",
            "trace_sinz_auxiliary": (
                "a(t,c,i)=483681+((17*t+c)*14+i)+1 "
                "for 0<=t<1680, 0<=c<17, 0<=i<14"
            ),
        },
        "counts": {
            "trace_groups": TRACE_COUNT,
            "trace_size": TRACE_SIZE,
            "sphere4_vertices": 12_600,
            "incidences_per_sphere4_vertex": 2,
        },
        "groups": groups,
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def trace_auxiliary(trace: int, colour: int, item: int) -> int:
    return PARENT_VARIABLES + ((trace * COLOURS + colour) * 14 + item) + 1


def expected_trace_lines(groups: list[dict[str, object]]) -> Iterator[bytes]:
    for trace, group in enumerate(groups):
        positions = group["vertex_positions"]
        assert isinstance(positions, list) and len(positions) == TRACE_SIZE
        for colour in range(COLOURS):
            primaries = [parent_primary(int(vertex), colour) for vertex in positions]
            yield (
                f"{-primaries[0]} {trace_auxiliary(trace, colour, 0)} 0\n"
            ).encode("ascii")
            for item in range(1, TRACE_SIZE - 1):
                previous = trace_auxiliary(trace, colour, item - 1)
                current = trace_auxiliary(trace, colour, item)
                yield f"{-primaries[item]} {current} 0\n".encode("ascii")
                yield f"{-previous} {current} 0\n".encode("ascii")
                yield f"{-primaries[item]} {-previous} 0\n".encode("ascii")
            yield (
                f"{-primaries[-1]} {-trace_auxiliary(trace, colour, 13)} 0\n"
            ).encode("ascii")


def parse_clause(raw: bytes, variables: int) -> int:
    fields = raw.split()
    if not fields or fields[-1] != b"0":
        raise AssertionError("invalid or unterminated DIMACS clause")
    literals = [int(field) for field in fields[:-1]]
    if (
        not literals
        or any(literal == 0 or abs(literal) > variables for literal in literals)
        or len(set(literals)) != len(literals)
    ):
        raise AssertionError("invalid, repeated, or out-of-range DIMACS literal")
    return len(literals)


def verify_augmented_cnf(
    parent_path: Path,
    augmented_path: Path,
    trace_lines: Iterator[bytes],
) -> tuple[str, Counter[int], int]:
    digest = hashlib.sha256()
    lengths: Counter[int] = Counter()
    clauses = 0
    with parent_path.open("rb") as parent, augmented_path.open("rb") as augmented:
        if parent.readline() != b"p cnf 483681 738537\n":
            raise AssertionError("authenticated parent header changed")
        header = augmented.readline()
        expected_header = f"p cnf {TOTAL_VARIABLES} {TOTAL_CLAUSES}\n".encode(
            "ascii"
        )
        if header != expected_header:
            raise AssertionError("augmented DIMACS header is not canonical")
        digest.update(header)
        for parent_line in parent:
            actual = augmented.readline()
            if actual != parent_line:
                raise AssertionError(
                    f"augmented CNF differs in parent clause {clauses + 1}"
                )
            digest.update(actual)
            lengths[parse_clause(actual, TOTAL_VARIABLES)] += 1
            clauses += 1
        if clauses != PARENT_CLAUSES:
            raise AssertionError("wrong number of copied parent clauses")
        for expected in trace_lines:
            actual = augmented.readline()
            if actual != expected:
                raise AssertionError(
                    f"augmented CNF differs in trace clause "
                    f"{clauses - PARENT_CLAUSES + 1}"
                )
            digest.update(actual)
            lengths[parse_clause(actual, TOTAL_VARIABLES)] += 1
            clauses += 1
        if augmented.read(1):
            raise AssertionError("augmented CNF has trailing bytes")
    if clauses != TOTAL_CLAUSES:
        raise AssertionError(f"wrong augmented clause count: {clauses}")
    return digest.hexdigest(), lengths, clauses


def sinz_template() -> list[tuple[int, ...]]:
    # Primary variables are 1..15; auxiliaries are 16..29.
    clauses: list[tuple[int, ...]] = [(-1, 16)]
    for item in range(1, 14):
        primary = item + 1
        previous = 16 + item - 1
        current = 16 + item
        clauses.extend(
            [
                (-primary, current),
                (-previous, current),
                (-primary, -previous),
            ]
        )
    clauses.append((-15, -29))
    if len(clauses) != TRACE_CLAUSES_PER_AMO:
        raise AssertionError("wrong independent Sinz template size")
    return clauses


def auxiliary_2sat(clauses: list[tuple[int, ...]]) -> bool:
    variables = 14
    graph = [[] for _ in range(2 * variables)]
    reverse = [[] for _ in range(2 * variables)]

    def node(literal: int) -> int:
        variable = abs(literal) - 16
        return 2 * variable + (0 if literal > 0 else 1)

    def imply(source: int, target: int) -> None:
        graph[source].append(target)
        reverse[target].append(source)

    for clause in clauses:
        if not clause:
            return False
        first = node(clause[0])
        second = node(clause[-1])
        imply(first ^ 1, second)
        imply(second ^ 1, first)

    visited = [False] * (2 * variables)
    order: list[int] = []

    def visit(vertex: int) -> None:
        visited[vertex] = True
        for neighbour in graph[vertex]:
            if not visited[neighbour]:
                visit(neighbour)
        order.append(vertex)

    for vertex in range(2 * variables):
        if not visited[vertex]:
            visit(vertex)

    component = [-1] * (2 * variables)

    def assign(vertex: int, label: int) -> None:
        component[vertex] = label
        for neighbour in reverse[vertex]:
            if component[neighbour] == -1:
                assign(neighbour, label)

    for vertex in reversed(order):
        if component[vertex] == -1:
            assign(vertex, vertex)
    return all(component[2 * item] != component[2 * item + 1] for item in range(variables))


def audit_sinz_projection() -> int:
    template = sinz_template()
    checked = 0
    for assignment in range(1 << TRACE_SIZE):
        residual: list[tuple[int, ...]] = []
        for clause in template:
            kept: list[int] = []
            satisfied = False
            for literal in clause:
                if abs(literal) <= TRACE_SIZE:
                    value = bool(assignment & (1 << (abs(literal) - 1)))
                    if value == (literal > 0):
                        satisfied = True
                        break
                else:
                    kept.append(literal)
            if not satisfied:
                residual.append(tuple(kept))
        projected_sat = auxiliary_2sat(residual)
        # Keep the verifier runnable under the macOS system Python.
        direct_pairwise_sat = bin(assignment).count("1") <= 1
        if projected_sat != direct_pairwise_sat:
            raise AssertionError(
                f"Sinz projection differs from pairwise AMO at assignment {assignment}"
            )
        checked += 1
    return checked


def augmented_manifest(cnf_digest: str, trace_map_digest: str) -> dict[str, object]:
    return {
        "schema": SCHEMA,
        "scope": {
            "assumptions": (
                "complete unrestricted k=16 radius-4 ball plus the "
                "radius-5-forced trace consequence only"
            ),
            "excluded_ansatzes": [
                "Wallis",
                "cyclic",
                "finite-field",
                "Latin-square",
                "algebraic",
            ],
            "unsat_implication": "excludes k=16 only",
            "sat_implication": (
                "necessary local witness only; not a radius-5 extension "
                "and not a global colouring"
            ),
        },
        "parent": {
            "schema": PARENT_SCHEMA,
            "cnf_sha256": PINNED_PARENT_CNF,
            "map_sha256": PINNED_PARENT_MAP,
            "manifest_sha256": PINNED_PARENT_MANIFEST,
            "variables": PARENT_VARIABLES,
            "clauses": PARENT_CLAUSES,
        },
        "encoding": {
            "constraint": (
                "for every trace and colour, at most one of 15 parent "
                "one-hot primary literals"
            ),
            "method": "Sinz sequential AMO",
            "projection_equivalent_to": "pairwise disequality for each trace",
            "auxiliaries_per_amo": TRACE_AUX_PER_AMO,
            "clauses_per_amo": TRACE_CLAUSES_PER_AMO,
            "all_clauses_binary": True,
        },
        "counts": {
            "trace_groups": TRACE_COUNT,
            "trace_size": TRACE_SIZE,
            "trace_colours": COLOURS,
            "trace_amo_instances": TRACE_AMO_COUNT,
            "direct_pairwise_disequality_clauses": (
                TRACE_COUNT * COLOURS * (TRACE_SIZE * (TRACE_SIZE - 1) // 2)
            ),
            "trace_auxiliary_variables": ADDED_VARIABLES,
            "trace_sinz_clauses": ADDED_CLAUSES,
            "variables": TOTAL_VARIABLES,
            "clauses": TOTAL_CLAUSES,
            "clause_lengths": {
                "1": 32,
                "2": 688_879 + ADDED_CLAUSES,
                "17": 49_626,
            },
        },
        "cnf_sha256": cnf_digest,
        "trace_map_sha256": trace_map_digest,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-cnf", type=Path, required=True)
    parser.add_argument("--parent-map", type=Path, required=True)
    parser.add_argument("--parent-manifest", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--trace-map", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    masks, levels, location = audited_ball()
    layers = [
        sum(level == layer for level in levels) for layer in range(RADIUS + 1)
    ]
    if layers != [1, 16, 240, 1_800, 12_600]:
        raise AssertionError(f"wrong independently reconstructed layers: {layers}")
    counts = parent_counts(levels)
    if counts["variables"] != PARENT_VARIABLES or counts["clauses"] != PARENT_CLAUSES:
        raise AssertionError("wrong independently reconstructed parent dimensions")

    parent_digest, parent_lines = verify_exact_file(
        args.parent_cnf,
        expected_parent_lines(masks, levels, location, counts),
        "parent CNF",
    )
    if parent_digest != PINNED_PARENT_CNF or parent_lines != PARENT_CLAUSES + 1:
        raise AssertionError("parent CNF is not the independently audited artifact")

    parent_map_bytes = canonical_parent_map(masks, levels, counts)
    parent_map_digest = verify_exact_bytes(
        args.parent_map, parent_map_bytes, "parent map"
    )
    if parent_map_digest != PINNED_PARENT_MAP:
        raise AssertionError("independent parent-map digest disagrees with pin")
    parent_manifest_bytes = canonical_parent_manifest(
        masks, levels, location, counts, parent_map_digest
    )
    parent_manifest_digest = verify_exact_bytes(
        args.parent_manifest, parent_manifest_bytes, "parent manifest"
    )
    if parent_manifest_digest != PINNED_PARENT_MANIFEST:
        raise AssertionError("independent parent-manifest digest disagrees with pin")

    traces = forced_traces(masks, levels, location)
    trace_map_bytes = canonical_trace_map(traces)
    trace_map_digest = verify_exact_bytes(
        args.trace_map, trace_map_bytes, "forced-trace map"
    )
    cnf_digest, clause_lengths, clauses = verify_augmented_cnf(
        args.parent_cnf, args.cnf, expected_trace_lines(traces)
    )
    expected_lengths = Counter({1: 32, 2: 1_859_839, 17: 49_626})
    if clause_lengths != expected_lengths:
        raise AssertionError(
            f"wrong augmented clause-length distribution: {clause_lengths}"
        )

    expected_manifest = augmented_manifest(cnf_digest, trace_map_digest)
    expected_manifest_bytes = (
        json.dumps(expected_manifest, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    manifest_digest = verify_exact_bytes(
        args.manifest, expected_manifest_bytes, "augmented manifest"
    )
    projection_assignments = audit_sinz_projection()

    report = {
        "status": "PASS",
        "schema": SCHEMA,
        "scope": expected_manifest["scope"],
        "parent": {
            "authenticated": True,
            "cnf_sha256": parent_digest,
            "map_sha256": parent_map_digest,
            "manifest_sha256": parent_manifest_digest,
        },
        "cnf_sha256": cnf_digest,
        "trace_map_sha256": trace_map_digest,
        "manifest_sha256": manifest_digest,
        "layer_sizes": layers,
        "counts": expected_manifest["counts"],
        "parsed_clauses": clauses,
        "clause_lengths": {
            str(length): count for length, count in sorted(clause_lengths.items())
        },
        "trace_semantics": {
            "groups": len(traces),
            "group_size": TRACE_SIZE,
            "sphere4_vertices": 12_600,
            "incidences_per_sphere4_vertex": 2,
            "sinz_projection_assignments_checked": projection_assignments,
            "pairwise_disequality_equivalent": True,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
