#!/usr/bin/env python3
"""Independent semantic audit for the orbit-7 fixed-pair certificates."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
LOCAL_SEARCH = HERE / "search_counterexamples.py"
LOCAL_CLASSIFIER = HERE / "remaining_pair_orbit_classifier.py"
SEARCH_PATH = (
    LOCAL_SEARCH
    if LOCAL_SEARCH.exists()
    else HERE.parent / "r0_three_family_helly_gate" / "search_counterexamples.py"
)
CLASSIFIER_PATH = (
    LOCAL_CLASSIFIER
    if LOCAL_CLASSIFIER.exists()
    else HERE / "2026-07-28_remaining_pair_orbit_classifier.py"
)
DEFAULT_RESULTS = HERE / "2026-07-28_orbit7_fixed_pair_results.jsonl"
DEFAULT_CNF_DIR = HERE / "2026-07-28_orbit7_fixed_pair_raw"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SEARCH = load_module("orbit7_verify_search", SEARCH_PATH)
CLASSIFIER = load_module("orbit7_verify_classifier", CLASSIFIER_PATH)
VERTICES = SEARCH.VERTICES
EDGES = SEARCH.EDGES

assert VERTICES == CLASSIFIER.VERTICES
assert EDGES == CLASSIFIER.EDGES


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


def orbit7_data() -> tuple[
    tuple[int, ...],
    tuple[frozenset[int], ...],
    tuple[int, int],
]:
    signature = CLASSIFIER.venn_signatures()[7]
    rows = CLASSIFIER.representative(signature)
    selected_pair = CLASSIFIER.maximum_intersection_pair(rows)
    assert signature == (0, 1, 2, 2, 1, 0, 0)
    assert rows == (
        frozenset((0, 1, 2)),
        frozenset((0, 1, 3)),
        frozenset((2, 4, 5)),
    )
    assert selected_pair == (0, 1)
    return signature, rows, selected_pair


def independent_pair_catalogue() -> tuple[dict[str, object], ...]:
    """Reconstruct all representatives without importing the fallback."""
    signature, rows, selected_pair = orbit7_data()
    vertex_masks = CLASSIFIER.vertex_masks(rows)
    supports = {
        family: tuple(sorted(set(VERTICES) - rows[family]))
        for family in selected_pair
    }
    families = {
        family: CLASSIFIER.perfect_matchings(supports[family])
        for family in selected_pair
    }
    family_masks = {
        family: tuple(map(CLASSIFIER.matching_mask, matchings))
        for family, matchings in families.items()
    }
    symmetries = CLASSIFIER.row_symmetries(signature, selected_pair)
    left_family, right_family = selected_pair
    representatives: dict[
        tuple,
        tuple[tuple[int, ...], tuple[int, ...]],
    ] = {}
    labelled_pairs = 0
    for left_index, left_mask in enumerate(family_masks[left_family]):
        for right_index, right_mask in enumerate(
            family_masks[right_family]
        ):
            if left_mask & right_mask:
                continue
            labelled_pairs += 1
            left = families[left_family][left_index]
            right = families[right_family][right_index]
            invariant = CLASSIFIER.pair_invariant(
                CLASSIFIER.decompose_pair(
                    left,
                    right,
                    selected_pair,
                    vertex_masks,
                ),
                symmetries,
            )
            representatives.setdefault(invariant, (left, right))
    assert labelled_pairs == 570_780
    assert len(representatives) == 76
    return tuple(
        {
            "case": f"orbit7_pair_{case_index:03d}",
            "case_index": case_index,
            "invariant": invariant,
            "left": pair[0],
            "right": pair[1],
        }
        for case_index, (invariant, pair) in enumerate(
            sorted(representatives.items())
        )
    )


def all_capacity_cuts(
    supports: tuple[frozenset[int], ...],
) -> tuple[tuple[tuple[int, ...], tuple[int, ...], int], ...]:
    result = []
    for size in range(len(VERTICES) + 1):
        for vertices in combinations(VERTICES, size):
            vertex_set = frozenset(vertices)
            required = sum(
                max(0, len(support & vertex_set) - 5)
                for support in supports
            )
            if not required:
                continue
            internal_edges = tuple(
                edge_index
                for edge_index, endpoints in enumerate(EDGES)
                if endpoints[0] in vertex_set
                and endpoints[1] in vertex_set
            )
            result.append((
                vertices,
                internal_edges,
                len(internal_edges) - required,
            ))
    return tuple(result)


def automatic_internal_upper(
    vertices: tuple[int, ...],
    degree_lower: tuple[int, ...],
) -> int:
    vertex_set = frozenset(vertices)
    outside = tuple(
        vertex for vertex in VERTICES if vertex not in vertex_set
    )
    outside_lower_sum = sum(
        degree_lower[vertex] for vertex in outside
    )
    outside_capacity = len(outside) * (len(outside) - 1) // 2
    minimum_not_internal = max(
        (outside_lower_sum + 1) // 2,
        outside_lower_sum - outside_capacity,
        0,
    )
    return min(
        len(vertices) * (len(vertices) - 1) // 2,
        5 * len(vertices) // 2,
        27,
        27 - minimum_not_internal,
    )


def build_static_case(
    case: dict[str, object],
) -> dict[str, object]:
    """Independently reconstruct the pre-CEGIS formula for one case."""
    signature, rows, selected_pair = orbit7_data()
    supports = tuple(frozenset(VERTICES) - row for row in rows)
    multiplicity = tuple(
        sum(vertex in row for row in rows)
        for vertex in VERTICES
    )
    degree_lower = tuple(value + 1 for value in multiplicity)
    all_cuts = all_capacity_cuts(supports)
    encoded_cuts = tuple(
        cut
        for cut in all_cuts
        if cut[2] < automatic_internal_upper(cut[0], degree_lower)
    )
    families = tuple(
        SEARCH.perfect_matchings(tuple(sorted(support)))
        for support in supports
    )

    left = tuple(case["left"])
    right = tuple(case["right"])
    fixed_edges = frozenset((*left, *right))
    assert len(fixed_edges) == 10
    assert frozenset(left).isdisjoint(right)
    assert tuple(
        frozenset(
            vertex
            for edge_index in matching
            for vertex in EDGES[edge_index]
        )
        for matching in (left, right)
    ) == tuple(supports[index] for index in selected_pair)

    cnf = SEARCH.Cnf()

    def deleted(edge_index: int) -> int:
        return cnf.variable(("deleted", edge_index))

    cnf.cardinality(
        ("deleted_total",),
        [deleted(edge_index) for edge_index in range(len(EDGES))],
        lower=27,
        upper=27,
    )
    for vertex in VERTICES:
        cnf.cardinality(
            ("deleted_degree", vertex),
            [
                deleted(edge_index)
                for edge_index, endpoints in enumerate(EDGES)
                if vertex in endpoints
            ],
            lower=degree_lower[vertex],
            upper=5,
        )
    for vertices, internal_edges, upper_deleted in encoded_cuts:
        cnf.cardinality(
            ("capacity_cut", vertices),
            [deleted(edge_index) for edge_index in internal_edges],
            upper=upper_deleted,
        )
    for edge_index in fixed_edges:
        cnf.add(-deleted(edge_index))

    third_family, = tuple(
        family
        for family in range(3)
        if family not in selected_pair
    )
    possible_thirds = tuple(
        matching
        for matching in families[third_family]
        if fixed_edges.isdisjoint(matching)
    )
    for matching in possible_thirds:
        cnf.add(*(deleted(edge_index) for edge_index in matching))

    return {
        **case,
        "signature": signature,
        "rows": rows,
        "selected_pair": selected_pair,
        "third_family": third_family,
        "supports": supports,
        "degree_lower": degree_lower,
        "all_cuts": all_cuts,
        "encoded_cuts": encoded_cuts,
        "families": families,
        "fixed_edges": fixed_edges,
        "possible_thirds": possible_thirds,
        "cnf": cnf,
    }


def audit_support_and_cuts() -> dict[str, object]:
    signature, rows, selected_pair = orbit7_data()
    supports = tuple(frozenset(VERTICES) - row for row in rows)
    degree_lower = tuple(
        1 + sum(vertex in row for row in rows)
        for vertex in VERTICES
    )
    cuts = all_capacity_cuts(supports)
    encoded = tuple(
        cut
        for cut in cuts
        if cut[2] < automatic_internal_upper(cut[0], degree_lower)
    )
    encoded_sizes = Counter(len(cut[0]) for cut in encoded)
    assert degree_lower == (
        3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1,
    )
    assert len(cuts) == 4_215
    assert len(encoded) == 540
    assert encoded_sizes == {6: 518, 7: 22}
    return {
        "signature": signature,
        "rows": [sorted(row) for row in rows],
        "selected_pair": selected_pair,
        "degree_lower": degree_lower,
        "positive_cuts": len(cuts),
        "encoded_nonautomatic_cuts": len(encoded),
        "automatic_cuts": len(cuts) - len(encoded),
        "encoded_cut_sizes": dict(sorted(encoded_sizes.items())),
    }


def audit_classifier_action() -> dict[str, object]:
    signature, _, _ = orbit7_data()
    result = CLASSIFIER.classify_orbit(
        7,
        signature,
        verify_generators=True,
    )
    assert result["disjoint_matching_pairs"] == 570_780
    assert result["canonical_pair_orbits"] == 76
    assert result["generator_orbits"] == 76
    assert result["action_generators"] == 7
    return result


def audit_case(
    result: dict[str, object],
    representative: dict[str, object],
    cnf_dir: Path,
) -> dict[str, object]:
    assert result["status"] == "unsat"
    assert result["proof_claimed"] is False
    assert result["orbit"] == 7
    assert result["case"] == representative["case"]
    assert result["case_index"] == representative["case_index"]
    assert result["invariant"] == json.loads(
        json.dumps(representative["invariant"])
    )
    assert result["vertex_symmetry"] is False
    assert result["signature"] == [0, 1, 2, 2, 1, 0, 0]
    assert result["rows"] == [[0, 1, 2], [0, 1, 3], [2, 4, 5]]
    assert result["selected_pair"] == [0, 1]
    assert result["third_family"] == 2
    assert result["pair_intersection"] == 2
    assert result["canonical_pair_types"] == 76
    assert result["compatible_labelled_pairs"] == 570_780
    assert result["positive_capacity_cuts"] == 4_215
    assert result["encoded_capacity_cuts"] == 540
    assert result["encoded_cut_size_inventory"] == {"6": 518, "7": 22}
    assert result["variables"] == 69_525
    assert result["rounds"] > 0
    assert result["left_matching"] == [
        list(EDGES[index]) for index in representative["left"]
    ]
    assert result["right_matching"] == [
        list(EDGES[index]) for index in representative["right"]
    ]

    context = build_static_case(representative)
    base = context["cnf"]
    assert not any(key[0] == "lex_equal" for key in base.variables)
    assert len(base.clauses) == result["initial_clauses"]
    assert len(context["possible_thirds"]) == result[
        "fixed_pair_third_extensions"
    ]
    independently_possible = tuple(
        matching
        for matching in context["families"][context["third_family"]]
        if context["fixed_edges"].isdisjoint(matching)
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
            assert union == tuple(sorted(union))
            assert len(set(union)) == 15
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
            assert all(
                literal > 0 and literal in reverse_deleted
                for literal in clause
            )
            assert tuple(
                reverse_deleted[literal] for literal in clause
            ) == union
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
        "fixed_pair_third_extensions": len(
            context["possible_thirds"]
        ),
        "semantic_clause_audit": "pass",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results",
        type=Path,
        default=DEFAULT_RESULTS,
    )
    parser.add_argument(
        "--cnf-dir",
        type=Path,
        default=DEFAULT_CNF_DIR,
    )
    parser.add_argument(
        "--skip-action-audit",
        action="store_true",
    )
    args = parser.parse_args()

    results = tuple(
        json.loads(line)
        for line in args.results.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    )
    assert len(results) == 76
    assert tuple(
        result["case_index"] for result in results
    ) == tuple(range(76))
    representatives = independent_pair_catalogue()
    assert len(representatives) == 76

    support = audit_support_and_cuts()
    classifier_action = (
        None
        if args.skip_action_audit
        else audit_classifier_action()
    )
    cases = [
        audit_case(result, representatives[index], args.cnf_dir)
        for index, result in enumerate(results)
    ]
    learned_clauses = sum(
        case["learned_clauses"] for case in cases
    )
    assert learned_clauses == 9_386_110
    print(json.dumps({
        "status": "pass",
        "support_and_cuts": support,
        "compatible_labelled_pairs": 570_780,
        "canonical_pair_types": len(representatives),
        "classifier_action_audit": classifier_action,
        "learned_clauses": learned_clauses,
        "cases": cases,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
