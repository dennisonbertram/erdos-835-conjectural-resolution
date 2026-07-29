#!/usr/bin/env python3
"""Independent semantic audit for the orbit-9 fixed-pair certificates.

This verifier deliberately does not import the fixed-pair CEGIS driver.  It
reconstructs the support orbit, the complete compatible-pair catalogue, the
action-orbit audit, every static CNF clause, and every learned triple clause.
"""

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
DEFAULT_RESULTS = HERE / "2026-07-28_orbit9_fixed_pair_results.jsonl"
DEFAULT_CNF_DIR = HERE / "2026-07-28_orbit9_fixed_pair_raw"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SEARCH = load_module("orbit9_verify_search", SEARCH_PATH)
CLASSIFIER = load_module("orbit9_verify_classifier", CLASSIFIER_PATH)
VERTICES = SEARCH.VERTICES
EDGES = SEARCH.EDGES
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}

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


def orbit9_data() -> tuple[
    tuple[int, ...],
    tuple[frozenset[int], ...],
    tuple[int, int],
]:
    signatures = CLASSIFIER.venn_signatures()
    assert len(signatures) == 16
    signature = signatures[9]
    rows = CLASSIFIER.representative(signature)
    selected_pair = CLASSIFIER.maximum_intersection_pair(rows)
    assert signature == (1, 1, 1, 1, 1, 1, 0)
    assert rows == (
        frozenset((0, 1, 2)),
        frozenset((1, 3, 5)),
        frozenset((2, 4, 5)),
    )
    assert selected_pair == (0, 1)
    assert tuple(
        len(rows[left] & rows[right])
        for left, right in combinations(range(3), 2)
    ) == (1, 1, 1)
    return signature, rows, selected_pair


def independent_pair_catalogue() -> tuple[dict[str, object], ...]:
    """Enumerate all labelled pairs and retain exact invariant representatives."""
    signature, rows, selected_pair = orbit9_data()
    masks = CLASSIFIER.vertex_masks(rows)
    supports = {
        family: tuple(sorted(set(VERTICES) - rows[family]))
        for family in selected_pair
    }
    families = {
        family: CLASSIFIER.perfect_matchings(supports[family])
        for family in selected_pair
    }
    assert all(len(family) == 945 for family in families.values())
    family_masks = {
        family: tuple(map(CLASSIFIER.matching_mask, matchings))
        for family, matchings in families.items()
    }
    symmetries = CLASSIFIER.row_symmetries(signature, selected_pair)
    assert len(symmetries) == 2

    left_family, right_family = selected_pair
    representatives: dict[
        tuple,
        tuple[tuple[int, ...], tuple[int, ...]],
    ] = {}
    labelled_pairs = 0
    for left_index, left_mask in enumerate(family_masks[left_family]):
        for right_index, right_mask in enumerate(family_masks[right_family]):
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
                    masks,
                ),
                symmetries,
            )
            representatives.setdefault(invariant, (left, right))

    assert labelled_pairs == 627_900
    assert len(representatives) == 87
    return tuple(
        {
            "case": f"orbit9_pair_{case_index:03d}",
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
    """Reconstruct the full pre-CEGIS formula without the fallback driver."""
    signature, rows, selected_pair = orbit9_data()
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
    signature, rows, selected_pair = orbit9_data()
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
        2, 3, 3, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1,
    )
    assert len(cuts) == 4_250
    assert len(encoded) == 575
    assert encoded_sizes == {6: 553, 7: 22}
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
    signature, _, _ = orbit9_data()
    result = CLASSIFIER.classify_orbit(
        9,
        signature,
        verify_generators=True,
    )
    assert result["signature"] == signature
    assert result["rows"] == ((0, 1, 2), (1, 3, 5), (2, 4, 5))
    assert result["pair"] == (0, 1)
    assert result["row_symmetries"] == 2
    assert result["disjoint_matching_pairs"] == 627_900
    assert result["canonical_pair_orbits"] == 87
    assert result["generator_orbits"] == 87
    assert result["action_generators"] == 7
    return result


def decode_matching(endpoints: list[list[int]]) -> tuple[int, ...]:
    return tuple(
        sorted(EDGE_INDEX[tuple(sorted(edge))] for edge in endpoints)
    )


def audit_case(
    result: dict[str, object],
    representative: dict[str, object],
    cnf_dir: Path,
) -> dict[str, object]:
    assert result["status"] == "unsat"
    assert result["orbit"] == 9
    assert result["case"] == representative["case"]
    assert result["case_index"] == representative["case_index"]
    assert result["signature"] == [1, 1, 1, 1, 1, 1, 0]
    assert result["rows"] == [[0, 1, 2], [1, 3, 5], [2, 4, 5]]
    assert result["selected_pair"] == [0, 1]
    assert result["third_family"] == 2
    assert result["pair_intersection"] == 1
    assert result["compatible_labelled_pairs"] == 627_900
    assert result["canonical_pair_types"] == 87
    assert result["positive_capacity_cuts"] == 4_250
    assert result["encoded_capacity_cuts"] == 575
    assert result["encoded_cut_size_inventory"] == {
        "6": 553,
        "7": 22,
    }
    assert result["variables"] == 73_760
    assert result["proof_claimed"] is False
    assert result["vertex_symmetry"] is False
    assert result["invariant"] == json.loads(
        json.dumps(representative["invariant"])
    )
    assert decode_matching(result["left_matching"]) == representative["left"]
    assert decode_matching(result["right_matching"]) == representative["right"]

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
        "fixed_pair_third_extensions": len(context["possible_thirds"]),
        "no_post_fixed_pair_symmetry": True,
        "semantic_clause_audit": "pass",
    }


def load_results(paths: tuple[Path, ...]) -> tuple[dict[str, object], ...]:
    results = []
    for path in paths:
        results.extend(
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    results.sort(key=lambda result: result["case_index"])
    assert len(results) == 87
    assert tuple(
        result["case_index"] for result in results
    ) == tuple(range(87))
    assert len({result["case"] for result in results}) == 87
    return tuple(results)


def write_results(
    path: Path,
    results: tuple[dict[str, object], ...],
) -> None:
    content = "".join(
        json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
        for result in results
    )
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results",
        type=Path,
        default=DEFAULT_RESULTS,
    )
    parser.add_argument(
        "--worker-results",
        nargs="+",
        type=Path,
    )
    parser.add_argument(
        "--write-merged-results",
        type=Path,
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
    parser.add_argument(
        "--write-audit",
        type=Path,
    )
    parser.add_argument(
        "--write-classifier-audit",
        type=Path,
    )
    args = parser.parse_args()

    result_paths = (
        tuple(args.worker_results)
        if args.worker_results
        else (args.results,)
    )
    results = load_results(result_paths)
    if args.write_merged_results:
        write_results(args.write_merged_results, results)

    representatives = independent_pair_catalogue()
    assert len(representatives) == 87
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
    assert learned_clauses == 13_734_283
    audit = {
        "status": "pass",
        "support_and_cuts": support,
        "compatible_labelled_pairs": 627_900,
        "canonical_pair_types": len(representatives),
        "classifier_action_audit": classifier_action,
        "learned_clauses": learned_clauses,
        "no_post_fixed_pair_symmetry": True,
        "cases": cases,
    }
    if args.write_audit:
        args.write_audit.write_text(
            json.dumps(audit, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.write_classifier_audit:
        assert classifier_action is not None
        classifier_audit = {
            **classifier_action,
            "status": "independent-classifier-action-audit-pass",
        }
        args.write_classifier_audit.write_text(
            json.dumps(classifier_audit, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
