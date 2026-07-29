#!/usr/bin/env python3
"""Independent semantic audit of the frozen orbit-3 CNF reductions.

For every frozen DIMACS file this verifier:

1. reconstructs the static relaxation and checks it is the exact CNF prefix;
2. decodes every later CEGIS clause as a set of 15 undeleted-edge variables;
3. independently checks that those 15 edges admit the prescribed partition
   into three pairwise edge-disjoint perfect matchings.

Thus every learned semantic clause is justified without trusting the CEGIS
search that produced it.  SAT unsatisfiability is checked separately by the
committed DRAT certificates.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
from itertools import combinations
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "2026-07-28_orbit3_support_closure.py"
DEFAULT_CNF_DIR = HERE / "2026-07-28_orbit3_support_closure_cnf"


def load_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("orbit3_generator", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def prescribed_union_checker(module: ModuleType):
    expected_degrees = tuple(
        sum(vertex in support for support in module.SUPPORTS)
        for vertex in module.VERTICES
    )
    expected_colours = tuple(
        sum(1 << colour for colour, support in enumerate(module.SUPPORTS) if vertex in support)
        for vertex in module.VERTICES
    )
    allowed_colours = tuple(
        sum(
            1 << colour
            for colour, support in enumerate(module.SUPPORTS)
            if endpoints[0] in support and endpoints[1] in support
        )
        for endpoints in module.EDGES
    )
    colour_counts = (0, 1, 1, 2, 1, 2, 2, 3)

    def valid(edge_indices: tuple[int, ...]) -> bool:
        if len(edge_indices) != 15 or len(set(edge_indices)) != 15:
            return False

        degrees = [0] * len(module.VERTICES)
        for edge_index in edge_indices:
            left, right = module.EDGES[edge_index]
            degrees[left] += 1
            degrees[right] += 1
        if tuple(degrees) != expected_degrees:
            return False

        used = [0] * len(module.VERTICES)

        def colour(remaining: tuple[int, ...]) -> bool:
            if not remaining:
                return tuple(used) == expected_colours

            best_position = -1
            best_options = 0
            best_count = 4
            for position, edge_index in enumerate(remaining):
                left, right = module.EDGES[edge_index]
                options = allowed_colours[edge_index] & ~(used[left] | used[right])
                count = colour_counts[options]
                if count == 0:
                    return False
                if count < best_count:
                    best_position = position
                    best_options = options
                    best_count = count
                    if count == 1:
                        break

            edge_index = remaining[best_position]
            left, right = module.EDGES[edge_index]
            tail = remaining[:best_position] + remaining[best_position + 1 :]
            options = best_options
            while options:
                bit = options & -options
                options -= bit
                used[left] |= bit
                used[right] |= bit
                if colour(tail):
                    return True
                used[left] ^= bit
                used[right] ^= bit
            return False

        return colour(edge_indices)

    return valid


def audit_generator(module: ModuleType) -> None:
    module.audit_pair_orbits()
    assert len(module.PAIR_TYPES) == 16
    assert len(module.CUT_REQUIREMENTS) == 555
    assert all(len(family) == 945 for family in module.FAMILIES)
    multiplicity = tuple(
        sum(vertex in row for row in module.ROWS)
        for vertex in module.VERTICES
    )
    assert sum(multiplicity) == 9
    for size in range(14):
        for vertices in combinations(module.VERTICES, size):
            vertex_set = frozenset(vertices)
            demand = sum(
                max(0, len(support & vertex_set) - 5)
                for support in module.SUPPORTS
            )
            if size <= 5:
                assert demand == 0
            if size >= 9:
                outside = set(module.VERTICES) - vertex_set
                outside_size = len(outside)
                internal_deleted_bound = (
                    27
                    - sum(multiplicity[vertex] + 1 for vertex in outside)
                    + outside_size * (outside_size - 1) // 2
                )
                cut_deleted_bound = size * (size - 1) // 2 - demand
                assert internal_deleted_bound <= cut_deleted_bound

    for support, family in zip(module.SUPPORTS, module.FAMILIES):
        for matching in family:
            endpoints = [
                vertex
                for edge_index in matching
                for vertex in module.EDGES[edge_index]
            ]
            assert len(matching) == 5
            assert len(endpoints) == len(set(endpoints)) == 10
            assert set(endpoints) == set(support)


def audit_cnf(
    module: ModuleType,
    pair_type: str,
    path: Path,
    valid_union,
) -> dict[str, object]:
    base, _ = module.build_instance(pair_type)
    variable_to_edge = {
        variable: key[1]
        for key, variable in base.variables.items()
        if key[0] == "deleted"
    }

    stored_path = path if path.exists() else Path(f"{path}.gz")
    if not stored_path.exists():
        raise FileNotFoundError(f"neither {path} nor {path}.gz exists")
    opener = gzip.open if stored_path.suffix == ".gz" else Path.open

    declared_variables = None
    declared_clauses = None
    clauses_seen = 0
    semantic_clauses = 0
    raw_digest = hashlib.sha256()
    with opener(stored_path, "rt", encoding="ascii", newline="") as source:
        for line_number, raw_line in enumerate(source, start=1):
            raw_digest.update(raw_line.encode("ascii"))
            line = raw_line.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p "):
                if declared_variables is not None:
                    raise AssertionError(f"{stored_path}:{line_number}: duplicate header")
                fields = line.split()
                assert fields[:2] == ["p", "cnf"], (stored_path, line_number, fields)
                declared_variables = int(fields[2])
                declared_clauses = int(fields[3])
                assert declared_variables == base.top
                continue

            assert declared_variables is not None, (
                f"{stored_path}:{line_number}: clause before header"
            )
            literals = tuple(map(int, line.split()))
            assert literals and literals[-1] == 0, (stored_path, line_number)
            assert 0 not in literals[:-1], (stored_path, line_number)
            clause = literals[:-1]

            if clauses_seen < len(base.clauses):
                assert clause == base.clauses[clauses_seen], (
                    stored_path,
                    line_number,
                    clauses_seen,
                )
            else:
                assert len(clause) == 15, (
                    stored_path,
                    line_number,
                    len(clause),
                )
                assert all(literal > 0 for literal in clause), (
                    stored_path,
                    line_number,
                )
                try:
                    edge_indices = tuple(variable_to_edge[literal] for literal in clause)
                except KeyError as error:
                    raise AssertionError(
                        f"{stored_path}:{line_number}: non-deleted variable {error.args[0]}"
                    ) from error
                assert valid_union(edge_indices), (
                    stored_path,
                    line_number,
                    tuple(module.EDGES[index] for index in edge_indices),
                )
                semantic_clauses += 1
            clauses_seen += 1

    assert declared_variables is not None and declared_clauses is not None
    assert clauses_seen == declared_clauses
    assert clauses_seen >= len(base.clauses)
    return {
        "pair_type": pair_type,
        "variables": declared_variables,
        "clauses": clauses_seen,
        "static_prefix": len(base.clauses),
        "semantic_clauses": semantic_clauses,
        "stored_file": str(stored_path),
        "stored_sha256": file_sha256(stored_path),
        "raw_sha256": raw_digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf-dir", type=Path, default=DEFAULT_CNF_DIR)
    parser.add_argument("--types", nargs="*", default=None)
    args = parser.parse_args()

    module = load_generator()
    audit_generator(module)
    valid_union = prescribed_union_checker(module)
    pair_types = tuple(args.types) if args.types else tuple(module.PAIR_TYPES)
    unknown = set(pair_types) - set(module.PAIR_TYPES)
    if unknown:
        parser.error(f"unknown pair types: {sorted(unknown)}")

    print(
        {
            "pair_orbits": len(module.PAIR_TYPES),
            "capacity_cuts": len(module.CUT_REQUIREMENTS),
            "matchings_per_support": tuple(map(len, module.FAMILIES)),
        },
        flush=True,
    )
    for pair_type in pair_types:
        print(
            audit_cnf(
                module,
                pair_type,
                args.cnf_dir / f"{pair_type}.cnf",
                valid_union,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
