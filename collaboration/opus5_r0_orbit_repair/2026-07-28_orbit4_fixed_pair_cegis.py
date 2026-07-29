#!/usr/bin/env python3
"""Fixed-compatible-pair support-relaxation CEGIS for support orbit 4.

This is an isolated contingency search.  It obtains the exact eleven
compatible-pair orbit representatives from the independently audited generic
classifier, then builds one CNF for each representative.  No vertex symmetry
clauses are used after the labelled pair is fixed.

For each case the deletion graph D satisfies:

* |D| = 27;
* selected-row multiplicity plus one <= d_D(v) <= 5;
* every three-support capacity cut (cuts implied by the base bounds are
  omitted from the encoding but checked semantically);
* every fixed-pair edge is available;
* every third matching extending the fixed pair is blocked; and
* every prescribed simultaneous triple is blocked by CEGIS.

UNSAT is sound for the corresponding fixed compatible-pair type.  SAT with
no simultaneous triple is only a counterexample to this relaxed model.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from collections import Counter
from itertools import combinations
from pathlib import Path
from types import ModuleType

from pysat.solvers import Cadical195


HERE = Path(__file__).resolve().parent
SEARCH_PATH = HERE.parent / "r0_three_family_helly_gate" / "search_counterexamples.py"
CLASSIFIER_PATH = HERE / "2026-07-28_remaining_pair_orbit_classifier.py"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SEARCH = load_module("orbit4_fixed_pair_search", SEARCH_PATH)
CLASSIFIER = load_module("orbit4_fixed_pair_classifier", CLASSIFIER_PATH)

VERTICES = SEARCH.VERTICES
EDGES = SEARCH.EDGES
EDGE_INDEX = SEARCH.EDGE_INDEX

assert VERTICES == CLASSIFIER.VERTICES
assert EDGES == CLASSIFIER.EDGES


def orbit4_data() -> tuple[
    tuple[int, ...],
    tuple[frozenset[int], ...],
    tuple[int, int],
]:
    signature = CLASSIFIER.venn_signatures()[4]
    rows = CLASSIFIER.representative(signature)
    selected_pair = CLASSIFIER.maximum_intersection_pair(rows)
    assert signature == (0, 0, 2, 2, 0, 0, 1)
    assert rows == (
        frozenset((0, 1, 2)),
        frozenset((0, 1, 2)),
        frozenset((2, 3, 4)),
    )
    assert selected_pair == (0, 1)
    return signature, rows, selected_pair


def canonical_pair_representatives() -> tuple[dict[str, object], ...]:
    """Return one deterministic labelled representative of each of 11 types."""
    _, rows, selected_pair = orbit4_data()
    masks = CLASSIFIER.vertex_masks(rows)
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
    symmetries = CLASSIFIER.row_symmetries(
        CLASSIFIER.venn_signatures()[4],
        selected_pair,
    )
    left_family, right_family = selected_pair
    representatives: dict[tuple, tuple[tuple[int, ...], tuple[int, ...]]] = {}
    labelled_pairs = 0
    for left_index, left_mask in enumerate(family_masks[left_family]):
        for right_index, right_mask in enumerate(family_masks[right_family]):
            if left_mask & right_mask:
                continue
            labelled_pairs += 1
            left = families[left_family][left_index]
            right = families[right_family][right_index]
            components = CLASSIFIER.decompose_pair(
                left,
                right,
                selected_pair,
                masks,
            )
            invariant = CLASSIFIER.pair_invariant(components, symmetries)
            representatives.setdefault(invariant, (left, right))

    assert labelled_pairs == 514_080
    assert len(representatives) == 11
    result = []
    for case_index, (invariant, pair) in enumerate(sorted(representatives.items())):
        left, right = pair
        assert frozenset(left).isdisjoint(right)
        result.append({
            "case": f"orbit4_pair_{case_index:02d}",
            "case_index": case_index,
            "invariant": invariant,
            "left": left,
            "right": right,
        })
    return tuple(result)


def selected_multiplicity(
    rows: tuple[frozenset[int], ...],
) -> tuple[int, ...]:
    return tuple(
        sum(vertex in row for row in rows)
        for vertex in VERTICES
    )


def all_capacity_cuts(
    supports: tuple[frozenset[int], ...],
) -> tuple[tuple[tuple[int, ...], tuple[int, ...], int], ...]:
    """Return all positive cuts in deletion upper-bound form."""
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
                if endpoints[0] in vertex_set and endpoints[1] in vertex_set
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
    """Upper bound on e_D(U) from the explicit base constraints."""
    vertex_set = frozenset(vertices)
    outside = tuple(vertex for vertex in VERTICES if vertex not in vertex_set)
    outside_lower_sum = sum(degree_lower[vertex] for vertex in outside)
    outside_edge_capacity = len(outside) * (len(outside) - 1) // 2
    minimum_not_internal = max(
        (outside_lower_sum + 1) // 2,
        outside_lower_sum - outside_edge_capacity,
        0,
    )
    return min(
        len(vertices) * (len(vertices) - 1) // 2,
        5 * len(vertices) // 2,
        27,
        27 - minimum_not_internal,
    )


def build_case(case: dict[str, object]) -> dict[str, object]:
    signature, rows, selected_pair = orbit4_data()
    supports = tuple(frozenset(VERTICES) - row for row in rows)
    multiplicity = selected_multiplicity(rows)
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
    masks = SEARCH.matching_masks(families)

    left = tuple(case["left"])
    right = tuple(case["right"])
    fixed_edges = frozenset((*left, *right))
    assert len(fixed_edges) == 10
    assert frozenset(left).isdisjoint(right)
    assert tuple(
        frozenset(vertex for edge_index in matching for vertex in EDGES[edge_index])
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

    possible_thirds = tuple(
        matching
        for matching in families[2]
        if fixed_edges.isdisjoint(matching)
    )
    for matching in possible_thirds:
        cnf.add(*(deleted(edge_index) for edge_index in matching))

    return {
        **case,
        "signature": signature,
        "rows": rows,
        "selected_pair": selected_pair,
        "supports": supports,
        "multiplicity": multiplicity,
        "degree_lower": degree_lower,
        "all_cuts": all_cuts,
        "encoded_cuts": encoded_cuts,
        "cut_size_inventory": Counter(len(cut[0]) for cut in encoded_cuts),
        "families": families,
        "masks": masks,
        "fixed_edges": fixed_edges,
        "possible_thirds": possible_thirds,
        "cnf": cnf,
        "deleted": deleted,
    }


def extract_deleted(context: dict[str, object], model: set[int]) -> frozenset[int]:
    deleted = context["deleted"]
    return frozenset(
        edge_index
        for edge_index in range(len(EDGES))
        if deleted(edge_index) in model
    )


def verify_model(context: dict[str, object], deleted_set: frozenset[int]) -> None:
    assert len(deleted_set) == 27
    for vertex in VERTICES:
        degree = sum(
            edge_index in deleted_set
            for edge_index, endpoints in enumerate(EDGES)
            if vertex in endpoints
        )
        assert context["degree_lower"][vertex] <= degree <= 5
    assert deleted_set.isdisjoint(context["fixed_edges"])
    for vertices, internal_edges, upper_deleted in context["all_cuts"]:
        assert sum(
            edge_index in deleted_set for edge_index in internal_edges
        ) <= upper_deleted, vertices
    assert all(
        not deleted_set.isdisjoint(matching)
        for matching in context["possible_thirds"]
    )


def new_triple_records(
    context: dict[str, object],
    available: tuple[tuple[int, ...], ...],
    limit: int,
) -> tuple[tuple[tuple[int, ...], tuple[int, int, int]], ...]:
    result: dict[tuple[int, ...], tuple[int, int, int]] = {}
    for matching_indices in SEARCH.disjoint_triples(
        context["masks"],
        available,
        limit,
    ):
        union = tuple(sorted({
            edge_index
            for family, matching_index in enumerate(matching_indices)
            for edge_index in context["families"][family][matching_index]
        }))
        assert len(union) == 15
        result.setdefault(union, matching_indices)
    return tuple(sorted(result.items()))


def solve_case(
    case: dict[str, object],
    *,
    cut_batch: int,
    max_rounds: int,
    progress_every: int,
    output_dir: Path | None,
) -> dict[str, object]:
    start = time.monotonic()
    context = build_case(case)
    cnf = context["cnf"]
    initial_clauses = len(cnf.clauses)
    learned_unions = 0
    rounds = 0
    learned_path = None
    learned_digest = hashlib.sha256()
    learned_output = None
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        learned_path = output_dir / f"{context['case']}.learned"
        learned_output = learned_path.open("w", encoding="ascii", newline="\n")

    try:
        with Cadical195(bootstrap_with=cnf.clauses) as solver:
            while max_rounds == 0 or rounds < max_rounds:
                rounds += 1
                if not solver.solve():
                    status = "unsat"
                    details: dict[str, object] = {}
                    break
                model = {
                    literal for literal in solver.get_model() if literal > 0
                }
                deleted_set = extract_deleted(context, model)
                verify_model(context, deleted_set)
                deleted_mask = sum(1 << edge_index for edge_index in deleted_set)
                available = SEARCH.available_indices(context["masks"], deleted_mask)
                records = new_triple_records(context, available, cut_batch)
                if not records:
                    assert next(
                        SEARCH.disjoint_triples(context["masks"], available, 1),
                        None,
                    ) is None
                    status = "relaxed-counterexample"
                    details = {
                        "deleted_edges": [
                            EDGES[index] for index in sorted(deleted_set)
                        ],
                        "available_matching_counts": list(map(len, available)),
                    }
                    break
                for union, matching_indices in records:
                    clause = tuple(
                        context["deleted"](edge_index) for edge_index in union
                    )
                    cnf.add(*clause)
                    solver.add_clause(clause)
                    if learned_output is not None:
                        line = " ".join(map(str, (*matching_indices, *union))) + "\n"
                        learned_output.write(line)
                        learned_digest.update(line.encode("ascii"))
                learned_unions += len(records)
                if progress_every and rounds % progress_every == 0:
                    print(json.dumps({
                        "status": "progress",
                        "case": context["case"],
                        "rounds": rounds,
                        "learned_unions": learned_unions,
                        "available_matching_counts": list(map(len, available)),
                        "elapsed_seconds": round(time.monotonic() - start, 3),
                    }, sort_keys=True), flush=True)
            else:
                status = "round-limit"
                details = {}
    finally:
        if learned_output is not None:
            learned_output.close()

    artifact_details = {}
    if output_dir is not None:
        cnf_path = output_dir / f"{context['case']}.cnf"
        cnf_sha256 = SEARCH.write_dimacs(cnf_path, cnf)
        artifact_details = {
            "cnf_path": str(cnf_path),
            "cnf_sha256": cnf_sha256,
            "learned_path": str(learned_path),
            "learned_sha256": learned_digest.hexdigest(),
        }

    return {
        "status": status,
        "case": context["case"],
        "case_index": context["case_index"],
        "invariant": context["invariant"],
        "left_matching": [EDGES[index] for index in context["left"]],
        "right_matching": [EDGES[index] for index in context["right"]],
        "rounds": rounds,
        "learned_unions": learned_unions,
        "variables": cnf.top,
        "initial_clauses": initial_clauses,
        "final_clauses": len(cnf.clauses),
        "positive_capacity_cuts": len(context["all_cuts"]),
        "encoded_capacity_cuts": len(context["encoded_cuts"]),
        "encoded_cut_size_inventory": dict(
            sorted(context["cut_size_inventory"].items())
        ),
        "fixed_pair_third_extensions": len(context["possible_thirds"]),
        "vertex_symmetry": False,
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "decision_scope": (
            "orbit4 fixed-compatible-pair support relaxation; exact D size, "
            "degree bounds, all cuts, fixed-pair extension blockers, and "
            "global simultaneous-triple CEGIS"
        ),
        "proof_claimed": False,
        **artifact_details,
        **details,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default="all")
    parser.add_argument("--cut-batch", type=int, default=10_000)
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.cut_batch <= 0:
        parser.error("--cut-batch must be positive")
    if args.max_rounds < 0 or args.progress_every < 0:
        parser.error("round counts must be nonnegative")

    representatives = canonical_pair_representatives()
    if args.cases == "all":
        selected = tuple(range(len(representatives)))
    else:
        selected = tuple(int(value) for value in args.cases.split(","))
        if any(not 0 <= index < len(representatives) for index in selected):
            parser.error("case indices must lie in 0..10")

    output = None
    if args.jsonl:
        args.jsonl.parent.mkdir(parents=True, exist_ok=True)
        output = args.jsonl.open("a", encoding="utf-8")
    try:
        for case_index in selected:
            result = solve_case(
                representatives[case_index],
                cut_batch=args.cut_batch,
                max_rounds=args.max_rounds,
                progress_every=args.progress_every,
                output_dir=args.output_dir,
            )
            line = json.dumps(result, sort_keys=True)
            print(line, flush=True)
            if output:
                output.write(line + "\n")
                output.flush()
    finally:
        if output:
            output.close()


if __name__ == "__main__":
    main()
