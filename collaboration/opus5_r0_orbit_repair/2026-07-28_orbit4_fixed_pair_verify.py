#!/usr/bin/env python3
"""Independent semantic audit for the orbit-4 fixed-pair certificates."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
GENERATOR_PATH = HERE / "2026-07-28_orbit4_fixed_pair_cegis.py"
DEFAULT_RESULTS = HERE / "2026-07-28_orbit4_fixed_pair_certificate_results.jsonl"
DEFAULT_CNF_DIR = HERE / "2026-07-28_orbit4_fixed_pair_cnf"


def load_generator():
    spec = importlib.util.spec_from_file_location("orbit4_fixed_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GEN = load_generator()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_clause(line: str) -> tuple[int, ...]:
    values = tuple(map(int, line.split()))
    assert values and values[-1] == 0
    return values[:-1]


def independent_automatic_upper(
    vertices: tuple[int, ...],
    degree_lower: tuple[int, ...],
) -> int:
    vertex_set = frozenset(vertices)
    outside = tuple(vertex for vertex in GEN.VERTICES if vertex not in vertex_set)
    lower_sum = sum(degree_lower[vertex] for vertex in outside)
    outside_capacity = len(outside) * (len(outside) - 1) // 2
    minimum_not_internal = max(
        (lower_sum + 1) // 2,
        lower_sum - outside_capacity,
        0,
    )
    return min(
        len(vertices) * (len(vertices) - 1) // 2,
        5 * len(vertices) // 2,
        27,
        27 - minimum_not_internal,
    )


def audit_support_and_cuts() -> dict[str, object]:
    signature, rows, selected_pair = GEN.orbit4_data()
    assert signature == (0, 0, 2, 2, 0, 0, 1)
    assert rows == (
        frozenset((0, 1, 2)),
        frozenset((0, 1, 2)),
        frozenset((2, 3, 4)),
    )
    assert selected_pair == (0, 1)
    supports = tuple(frozenset(GEN.VERTICES) - row for row in rows)
    multiplicity = tuple(
        sum(vertex in row for row in rows)
        for vertex in GEN.VERTICES
    )
    degree_lower = tuple(value + 1 for value in multiplicity)

    positive = 0
    encoded = 0
    automatic = 0
    encoded_sizes = Counter()
    for size in range(len(GEN.VERTICES) + 1):
        for vertices in combinations(GEN.VERTICES, size):
            vertex_set = frozenset(vertices)
            required = sum(
                max(0, len(support & vertex_set) - 5)
                for support in supports
            )
            if not required:
                continue
            positive += 1
            internal_count = size * (size - 1) // 2
            cut_upper = internal_count - required
            automatic_upper = independent_automatic_upper(vertices, degree_lower)
            if cut_upper < automatic_upper:
                encoded += 1
                encoded_sizes[size] += 1
            else:
                automatic += 1
    assert positive == 3_844
    assert encoded == 457
    assert encoded_sizes == {6: 392, 7: 64, 8: 1}
    assert positive == encoded + automatic
    return {
        "signature": signature,
        "rows": [sorted(row) for row in rows],
        "selected_pair": selected_pair,
        "degree_lower": degree_lower,
        "positive_cuts": positive,
        "encoded_nonautomatic_cuts": encoded,
        "automatic_cuts": automatic,
        "encoded_cut_sizes": dict(sorted(encoded_sizes.items())),
    }


def audit_case(
    result: dict[str, object],
    representative: dict[str, object],
    cnf_dir: Path,
) -> dict[str, object]:
    assert result["status"] == "unsat"
    assert result["case_index"] == representative["case_index"]
    assert result["case"] == representative["case"]
    assert result["vertex_symmetry"] is False

    context = GEN.build_case(representative)
    base = context["cnf"]
    assert not any(key[0] == "lex_equal" for key in base.variables)
    assert len(base.clauses) == result["initial_clauses"]
    assert len(context["possible_thirds"]) == result["fixed_pair_third_extensions"]

    fixed_edges = context["fixed_edges"]
    independently_possible = tuple(
        matching
        for matching in context["families"][2]
        if fixed_edges.isdisjoint(matching)
    )
    assert independently_possible == context["possible_thirds"]

    cnf_path = cnf_dir / f"{result['case']}.cnf"
    learned_path = cnf_dir / f"{result['case']}.learned"
    assert sha256(cnf_path) == result["cnf_sha256"]
    assert sha256(learned_path) == result["learned_sha256"]

    reverse_deleted = {
        variable: key[1]
        for key, variable in base.variables.items()
        if key[0] == "deleted"
    }
    learned_count = 0
    seen_unions: set[tuple[int, ...]] = set()
    with (
        cnf_path.open("r", encoding="ascii") as cnf_stream,
        learned_path.open("r", encoding="ascii") as learned_stream,
    ):
        header = cnf_stream.readline().split()
        assert header == [
            "p",
            "cnf",
            str(result["variables"]),
            str(result["final_clauses"]),
        ]
        for expected_clause in base.clauses:
            assert parse_clause(cnf_stream.readline()) == expected_clause

        for learned_line in learned_stream:
            values = tuple(map(int, learned_line.split()))
            assert len(values) == 18
            matching_indices = values[:3]
            union = values[3:]
            assert len(set(union)) == 15
            assert union == tuple(sorted(union))
            assert union not in seen_unions
            seen_unions.add(union)

            matchings = tuple(
                context["families"][family][matching_index]
                for family, matching_index in enumerate(matching_indices)
            )
            matching_sets = tuple(map(frozenset, matchings))
            assert matching_sets[0].isdisjoint(matching_sets[1])
            assert matching_sets[0].isdisjoint(matching_sets[2])
            assert matching_sets[1].isdisjoint(matching_sets[2])
            assert union == tuple(sorted(set().union(*matching_sets)))

            clause = parse_clause(cnf_stream.readline())
            assert len(clause) == 15
            assert all(literal > 0 and literal in reverse_deleted for literal in clause)
            assert tuple(reverse_deleted[literal] for literal in clause) == union
            learned_count += 1
        assert cnf_stream.readline() == ""

    assert learned_count == result["learned_unions"]
    assert len(base.clauses) + learned_count == result["final_clauses"]
    return {
        "case": result["case"],
        "cnf_sha256": result["cnf_sha256"],
        "learned_sha256": result["learned_sha256"],
        "base_clauses": len(base.clauses),
        "learned_clauses": learned_count,
        "fixed_pair_third_extensions": len(context["possible_thirds"]),
        "semantic_clause_audit": "pass",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--cnf-dir", type=Path, default=DEFAULT_CNF_DIR)
    args = parser.parse_args()

    results = tuple(
        json.loads(line)
        for line in args.results.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    assert len(results) == 11
    assert tuple(result["case_index"] for result in results) == tuple(range(11))
    representatives = GEN.canonical_pair_representatives()
    assert len(representatives) == 11

    support = audit_support_and_cuts()
    cases = [
        audit_case(result, representatives[index], args.cnf_dir)
        for index, result in enumerate(results)
    ]
    print(json.dumps({
        "status": "pass",
        "support_and_cuts": support,
        "canonical_pair_types": len(representatives),
        "cases": cases,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
