#!/usr/bin/env python3
"""Augment the canonical generic radius-4 O_16 CNF with forced traces.

The input CNF, map, and manifest must be the exact canonical artifacts emitted
by ``generate_radius4_generic_sinz_cnf.py``.  Their SHA-256 digests are pinned
below, so this program cannot silently augment a different parent instance.

For every unordered pair of root points {i,j} and every moving point u, radius
five forces the fifteen sphere-four colours N_uv(ij), v != u, to be pairwise
distinct.  In the parent's one-hot variables this is one at-most-one constraint
per trace and colour.  A canonical Sinz sequential encoding uses 14 auxiliary
variables and 41 binary clauses for each such 15-literal constraint.

No Wallis, cyclic, finite-field, Latin-square, or other construction assumption
is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Iterator


PARENT_SCHEMA = "odd-graph-o16-radius4-generic-sinz-v1"
SCHEMA = "odd-graph-o16-radius4-plus-radius5-forced-trace-sinz-v1"

PARENT_CNF_SHA256 = "0e66e3d7f4e15bd155db737092b8387b10540fd0e5bbcb56127c650baf6c54dc"
PARENT_MAP_SHA256 = "ba4c9455a31907d3af5d58a143eaf2ce0a48517e2a26122f320cb71fcc3393e6"
PARENT_MANIFEST_SHA256 = "9c5fd2e89ea69d9dc607e2e7793962c35b9e7b45597977eb3c3e93445c88b4f2"

ROOT = (1 << 15) - 1
COLOURS = 17
PARENT_VARIABLES = 483_681
PARENT_CLAUSES = 738_537
TRACE_GROUPS = 1_680
TRACE_SIZE = 15
TRACE_AUXILIARIES_PER_AMO = TRACE_SIZE - 1
TRACE_CLAUSES_PER_AMO = 3 * TRACE_SIZE - 4
TRACE_AMO_INSTANCES = TRACE_GROUPS * COLOURS
TRACE_AUXILIARY_VARIABLES = TRACE_AMO_INSTANCES * TRACE_AUXILIARIES_PER_AMO
TRACE_CLAUSES = TRACE_AMO_INSTANCES * TRACE_CLAUSES_PER_AMO
VARIABLES = PARENT_VARIABLES + TRACE_AUXILIARY_VARIABLES
CLAUSES = PARENT_CLAUSES + TRACE_CLAUSES

EXPECTED_PARENT_COUNTS = {
    "primary_variables": 249_169,
    "auxiliary_variables": 234_512,
    "variables": PARENT_VARIABLES,
    "vertices": 14_657,
    "constrained_centres": 2_057,
    "vertex_alo_clauses": 14_657,
    "vertex_amo_clauses": 688_879,
    "neighbourhood_alo_clauses": 34_969,
    "symmetry_unit_clauses": 32,
    "clauses": PARENT_CLAUSES,
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_digest(path: Path, expected: str, label: str) -> None:
    actual = sha256_file(path)
    if actual != expected:
        raise ValueError(
            f"{label} is not the pinned canonical artifact: "
            f"expected sha256 {expected}, got {actual}"
        )


def authenticate_parent(
    cnf_path: Path, map_path: Path, manifest_path: Path
) -> dict[str, object]:
    require_digest(cnf_path, PARENT_CNF_SHA256, "parent CNF")
    require_digest(map_path, PARENT_MAP_SHA256, "parent map")
    require_digest(manifest_path, PARENT_MANIFEST_SHA256, "parent manifest")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != PARENT_SCHEMA:
        raise ValueError("parent manifest has the wrong schema")
    if manifest.get("cnf_sha256") != PARENT_CNF_SHA256:
        raise ValueError("parent manifest does not bind the pinned CNF")
    if manifest.get("map_sha256") != PARENT_MAP_SHA256:
        raise ValueError("parent manifest does not bind the pinned map")
    if manifest.get("counts") != EXPECTED_PARENT_COUNTS:
        raise ValueError("parent manifest has unexpected dimensions")

    parent_map = json.loads(map_path.read_text(encoding="utf-8"))
    if parent_map.get("schema") != PARENT_SCHEMA:
        raise ValueError("parent map has the wrong schema")
    if parent_map.get("counts") != EXPECTED_PARENT_COUNTS:
        raise ValueError("parent map has unexpected dimensions")
    vertices = parent_map.get("vertices")
    if not isinstance(vertices, list) or len(vertices) != 14_657:
        raise ValueError("parent map does not contain the canonical 14,657 vertices")
    for position, entry in enumerate(vertices):
        if (
            not isinstance(entry, dict)
            or entry.get("position") != position
            or not isinstance(entry.get("mask"), int)
            or entry.get("distance") not in range(5)
        ):
            raise ValueError(f"invalid parent-map vertex entry at position {position}")

    with cnf_path.open("rb") as stream:
        if stream.readline() != b"p cnf 483681 738537\n":
            raise ValueError("pinned parent CNF has an unexpected DIMACS header")
    return parent_map


def trace_groups(parent_map: dict[str, object]) -> list[dict[str, object]]:
    vertices = parent_map["vertices"]
    assert isinstance(vertices, list)
    position_by_mask = {
        int(entry["mask"]): int(entry["position"])
        for entry in vertices
        if isinstance(entry, dict)
    }
    distance_by_position = [
        int(entry["distance"]) for entry in vertices if isinstance(entry, dict)
    ]

    groups: list[dict[str, object]] = []
    incidence: Counter[int] = Counter()
    for first_fixed, second_fixed in combinations(range(15), 2):
        fixed_mask = ROOT ^ (1 << first_fixed) ^ (1 << second_fixed)
        for moving_pivot in range(16):
            positions: list[int] = []
            for other_moving in range(16):
                if other_moving == moving_pivot:
                    continue
                mask = (
                    fixed_mask
                    | (1 << (15 + moving_pivot))
                    | (1 << (15 + other_moving))
                )
                try:
                    position = position_by_mask[mask]
                except KeyError as error:
                    raise ValueError(
                        "parent map is missing a forced-trace sphere-four vertex"
                    ) from error
                if distance_by_position[position] != 4:
                    raise ValueError("a forced-trace vertex is not in sphere four")
                positions.append(position)
                incidence[position] += 1
            if len(positions) != TRACE_SIZE or len(set(positions)) != TRACE_SIZE:
                raise AssertionError("a forced trace does not have 15 distinct vertices")
            groups.append(
                {
                    "trace": len(groups),
                    "fixed_points": [first_fixed, second_fixed],
                    "moving_pivot": moving_pivot,
                    "vertex_positions": positions,
                }
            )

    if len(groups) != TRACE_GROUPS:
        raise AssertionError(f"expected {TRACE_GROUPS} traces, got {len(groups)}")
    if len({tuple(group["vertex_positions"]) for group in groups}) != TRACE_GROUPS:
        raise AssertionError("forced-trace groups are not unique")
    sphere_four = {
        position
        for position, distance in enumerate(distance_by_position)
        if distance == 4
    }
    if set(incidence) != sphere_four or set(incidence.values()) != {2}:
        raise AssertionError(
            "forced traces must cover every sphere-four vertex exactly twice"
        )
    return groups


def trace_map_bytes(groups: list[dict[str, object]]) -> bytes:
    payload = {
        "schema": SCHEMA,
        "parent_map_sha256": PARENT_MAP_SHA256,
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
            "trace_groups": TRACE_GROUPS,
            "trace_size": TRACE_SIZE,
            "sphere4_vertices": 12_600,
            "incidences_per_sphere4_vertex": 2,
        },
        "groups": groups,
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def primary(vertex_position: int, colour: int) -> int:
    return COLOURS * vertex_position + colour + 1


def auxiliary(trace: int, colour: int, item: int) -> int:
    return (
        PARENT_VARIABLES
        + ((trace * COLOURS + colour) * TRACE_AUXILIARIES_PER_AMO + item)
        + 1
    )


def trace_clause_lines(groups: list[dict[str, object]]) -> Iterator[bytes]:
    """Emit canonical Sinz AMO clauses for every trace and colour."""

    for trace, group in enumerate(groups):
        positions = group["vertex_positions"]
        assert isinstance(positions, list) and len(positions) == TRACE_SIZE
        for colour in range(COLOURS):
            literals = [primary(int(position), colour) for position in positions]
            yield f"{-literals[0]} {auxiliary(trace, colour, 0)} 0\n".encode(
                "ascii"
            )
            for item in range(1, TRACE_SIZE - 1):
                previous = auxiliary(trace, colour, item - 1)
                current = auxiliary(trace, colour, item)
                yield f"{-literals[item]} {current} 0\n".encode("ascii")
                yield f"{-previous} {current} 0\n".encode("ascii")
                yield f"{-literals[item]} {-previous} 0\n".encode("ascii")
            yield (
                f"{-literals[TRACE_SIZE - 1]} "
                f"{-auxiliary(trace, colour, TRACE_SIZE - 2)} 0\n"
            ).encode("ascii")


def atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(content)
    temporary.replace(path)


def materialize_cnf(
    parent_path: Path, output_path: Path, groups: list[dict[str, object]]
) -> tuple[str, int]:
    if parent_path.resolve() == output_path.resolve():
        raise ValueError("output CNF must not overwrite the authenticated parent CNF")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    emitted_trace_clauses = 0
    with tempfile.NamedTemporaryFile(dir=output_path.parent, delete=False) as target:
        temporary = Path(target.name)
        header = f"p cnf {VARIABLES} {CLAUSES}\n".encode("ascii")
        target.write(header)
        digest.update(header)
        with parent_path.open("rb") as parent:
            parent_header = parent.readline()
            if parent_header != b"p cnf 483681 738537\n":
                raise ValueError("authenticated parent has an unexpected header")
            while chunk := parent.read(1024 * 1024):
                target.write(chunk)
                digest.update(chunk)
        for line in trace_clause_lines(groups):
            target.write(line)
            digest.update(line)
            emitted_trace_clauses += 1
    if emitted_trace_clauses != TRACE_CLAUSES:
        temporary.unlink(missing_ok=True)
        raise AssertionError(
            f"emitted {emitted_trace_clauses} trace clauses, expected {TRACE_CLAUSES}"
        )
    temporary.replace(output_path)
    return digest.hexdigest(), emitted_trace_clauses


def manifest_payload(cnf_sha256: str, trace_map_sha256: str) -> dict[str, object]:
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
            "cnf_sha256": PARENT_CNF_SHA256,
            "map_sha256": PARENT_MAP_SHA256,
            "manifest_sha256": PARENT_MANIFEST_SHA256,
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
            "auxiliaries_per_amo": TRACE_AUXILIARIES_PER_AMO,
            "clauses_per_amo": TRACE_CLAUSES_PER_AMO,
            "all_clauses_binary": True,
        },
        "counts": {
            "trace_groups": TRACE_GROUPS,
            "trace_size": TRACE_SIZE,
            "trace_colours": COLOURS,
            "trace_amo_instances": TRACE_AMO_INSTANCES,
            "direct_pairwise_disequality_clauses": (
                TRACE_GROUPS * COLOURS * (TRACE_SIZE * (TRACE_SIZE - 1) // 2)
            ),
            "trace_auxiliary_variables": TRACE_AUXILIARY_VARIABLES,
            "trace_sinz_clauses": TRACE_CLAUSES,
            "variables": VARIABLES,
            "clauses": CLAUSES,
            "clause_lengths": {
                "1": 32,
                "2": 688_879 + TRACE_CLAUSES,
                "17": 49_626,
            },
        },
        "cnf_sha256": cnf_sha256,
        "trace_map_sha256": trace_map_sha256,
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

    parent_map = authenticate_parent(
        args.parent_cnf, args.parent_map, args.parent_manifest
    )
    groups = trace_groups(parent_map)
    map_bytes = trace_map_bytes(groups)
    cnf_sha256, emitted = materialize_cnf(args.parent_cnf, args.cnf, groups)
    if emitted != TRACE_CLAUSES:
        raise AssertionError("wrong trace-clause count")
    atomic_write_bytes(args.trace_map, map_bytes)
    manifest = manifest_payload(cnf_sha256, hashlib.sha256(map_bytes).hexdigest())
    manifest_bytes = (
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    atomic_write_bytes(args.manifest, manifest_bytes)

    report = {
        "status": "MATERIALIZED",
        "schema": SCHEMA,
        "cnf_sha256": cnf_sha256,
        "trace_map_sha256": hashlib.sha256(map_bytes).hexdigest(),
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "counts": manifest["counts"],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
