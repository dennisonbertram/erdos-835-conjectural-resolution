#!/usr/bin/env python3
"""Single-matching canonical CEGIS for prescribed-colour support orbits.

This implements the reduction proposed by Claude Opus 5 and independently
audited in ``2026-07-28_single_matching_orbit_audit.py``.  For a chosen
maximum-intersection pair of supports, one perfect matching is fixed up to
the pointwise three-row stabilizer; the compatible partner remains
existential in the CNF.

For each canonical first matching, the deletion graph D satisfies:

* |D| = 27;
* selected-row multiplicity plus one <= d_D(v) <= 5;
* every three-support capacity cut;
* availability of the fixed first matching;
* an existential edge-disjoint available partner matching; and
* absence of every prescribed simultaneous triple, enforced by sound
  static partner-extension clauses and exact global CEGIS.

UNSAT for every canonical first matching is sound for the corresponding
support orbit, assuming the selected support pair is compatible.  SAT with
no simultaneous triple is only a counterexample to this support relaxation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from collections import Counter
from pathlib import Path
from types import ModuleType

from pysat.solvers import Cadical195


HERE = Path(__file__).resolve().parent
FIXED_PATH = HERE / "2026-07-28_orbit4_fixed_pair_cegis.py"
AUDIT_PATH = HERE / "2026-07-28_single_matching_orbit_audit.py"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FIXED = load_module("single_matching_fixed_helpers", FIXED_PATH)
AUDIT = load_module("single_matching_count_audit", AUDIT_PATH)
SEARCH = FIXED.SEARCH
CLASSIFIER = FIXED.CLASSIFIER

VERTICES = FIXED.VERTICES
EDGES = FIXED.EDGES
EDGE_INDEX = SEARCH.EDGE_INDEX


def orbit_data(
    orbit: int,
) -> tuple[
    tuple[int, ...],
    tuple[frozenset[int], ...],
    tuple[int, int],
]:
    signatures = CLASSIFIER.venn_signatures()
    if not 0 <= orbit < len(signatures):
        raise ValueError(f"orbit must lie in 0..{len(signatures) - 1}")
    signature = signatures[orbit]
    rows = CLASSIFIER.representative(signature)
    selected_pair = CLASSIFIER.maximum_intersection_pair(rows)
    assert selected_pair == (0, 1)
    assert signature == AUDIT.VENN_SIGNATURES[orbit]
    return signature, rows, selected_pair


def matching_cell_invariant(
    matching: tuple[int, ...],
    masks: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            tuple(sorted((masks[left], masks[right])))
            for edge_index in matching
            for left, right in (EDGES[edge_index],)
        )
    )


def canonical_first_matchings(
    orbit: int,
) -> tuple[dict[str, object], ...]:
    """One deterministic matching for every pointwise-row-stabilizer orbit."""
    signature, rows, selected_pair = orbit_data(orbit)
    masks = CLASSIFIER.vertex_masks(rows)
    first_family = selected_pair[0]
    support = tuple(sorted(set(VERTICES) - rows[first_family]))
    matchings = CLASSIFIER.perfect_matchings(support)
    assert len(matchings) == 945

    representatives: dict[tuple[tuple[int, int], ...], tuple[int, ...]] = {}
    for matching in matchings:
        invariant = matching_cell_invariant(matching, masks)
        representatives.setdefault(invariant, matching)

    expected = AUDIT.OPUS_COUNTS[orbit]
    assert len(representatives) == expected
    degree_vector = tuple(
        sum(masks[vertex] == mask for vertex in support)
        for mask in (0, 2, 4, 6)
    )
    assert degree_vector == AUDIT.cell_degree_vector(signature)

    result = []
    for case_index, (invariant, matching) in enumerate(sorted(representatives.items())):
        result.append({
            "case": f"orbit{orbit}_single_{case_index:02d}",
            "case_index": case_index,
            "invariant": invariant,
            "first": matching,
        })
    return tuple(result)


def build_case(orbit: int, case: dict[str, object]) -> dict[str, object]:
    signature, rows, selected_pair = orbit_data(orbit)
    supports = tuple(frozenset(VERTICES) - row for row in rows)
    multiplicity = FIXED.selected_multiplicity(rows)
    degree_lower = tuple(value + 1 for value in multiplicity)
    all_cuts = FIXED.all_capacity_cuts(supports)
    encoded_cuts = tuple(
        cut
        for cut in all_cuts
        if cut[2] < FIXED.automatic_internal_upper(cut[0], degree_lower)
    )
    families = tuple(
        SEARCH.perfect_matchings(tuple(sorted(support)))
        for support in supports
    )
    family_masks = SEARCH.matching_masks(families)

    first = tuple(case["first"])
    first_edges = frozenset(first)
    assert len(first_edges) == 5
    assert frozenset(
        vertex
        for edge_index in first
        for vertex in EDGES[edge_index]
    ) == supports[selected_pair[0]]

    cnf = SEARCH.Cnf()

    def deleted(edge_index: int) -> int:
        return cnf.variable(("deleted", edge_index))

    def partner(edge_index: int) -> int:
        return cnf.variable(("partner", edge_index))

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
    for edge_index in first_edges:
        cnf.add(-deleted(edge_index))

    partner_family = selected_pair[1]
    partner_support = supports[partner_family]
    partner_edge_indices = tuple(
        edge_index
        for edge_index, (left, right) in enumerate(EDGES)
        if left in partner_support and right in partner_support
    )
    partner_edge_set = frozenset(partner_edge_indices)
    for edge_index in partner_edge_indices:
        cnf.add(-partner(edge_index), -deleted(edge_index))
        if edge_index in first_edges:
            cnf.add(-partner(edge_index))
    for vertex in sorted(partner_support):
        cnf.cardinality(
            ("partner_degree", vertex),
            [
                partner(edge_index)
                for edge_index in partner_edge_indices
                if vertex in EDGES[edge_index]
            ],
            lower=1,
            upper=1,
        )

    third_family = ({0, 1, 2} - set(selected_pair)).pop()
    relevant_thirds = tuple(
        matching
        for matching in families[third_family]
        if first_edges.isdisjoint(matching)
    )
    for matching in relevant_thirds:
        cnf.add(
            *(deleted(edge_index) for edge_index in matching),
            *(
                partner(edge_index)
                for edge_index in matching
                if edge_index in partner_edge_set
            ),
        )

    return {
        **case,
        "orbit": orbit,
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
        "family_masks": family_masks,
        "first_edges": first_edges,
        "partner_support": partner_support,
        "partner_edge_indices": partner_edge_indices,
        "partner_edge_set": partner_edge_set,
        "relevant_thirds": relevant_thirds,
        "cnf": cnf,
        "deleted": deleted,
        "partner": partner,
    }


def extract_deleted(context: dict[str, object], model: set[int]) -> frozenset[int]:
    deleted = context["deleted"]
    return frozenset(
        edge_index
        for edge_index in range(len(EDGES))
        if deleted(edge_index) in model
    )


def extract_partner(context: dict[str, object], model: set[int]) -> frozenset[int]:
    partner = context["partner"]
    return frozenset(
        edge_index
        for edge_index in context["partner_edge_indices"]
        if partner(edge_index) in model
    )


def verify_model(
    context: dict[str, object],
    deleted_set: frozenset[int],
    partner_set: frozenset[int],
) -> None:
    assert len(deleted_set) == 27
    for vertex in VERTICES:
        degree = sum(
            edge_index in deleted_set
            for edge_index, endpoints in enumerate(EDGES)
            if vertex in endpoints
        )
        assert context["degree_lower"][vertex] <= degree <= 5
    assert deleted_set.isdisjoint(context["first_edges"])
    assert deleted_set.isdisjoint(partner_set)
    assert context["first_edges"].isdisjoint(partner_set)

    partner_vertices = Counter(
        vertex
        for edge_index in partner_set
        for vertex in EDGES[edge_index]
    )
    assert set(partner_vertices) == set(context["partner_support"])
    assert all(multiplicity == 1 for multiplicity in partner_vertices.values())
    assert len(partner_set) == 5

    for vertices, internal_edges, upper_deleted in context["all_cuts"]:
        assert sum(
            edge_index in deleted_set for edge_index in internal_edges
        ) <= upper_deleted, vertices
    assert all(
        not (
            deleted_set.isdisjoint(matching)
            and partner_set.isdisjoint(matching)
        )
        for matching in context["relevant_thirds"]
    )


def new_triple_records(
    context: dict[str, object],
    available: tuple[tuple[int, ...], ...],
    limit: int,
) -> tuple[tuple[tuple[int, ...], tuple[int, int, int]], ...]:
    result: dict[tuple[int, ...], tuple[int, int, int]] = {}
    for matching_indices in SEARCH.disjoint_triples(
        context["family_masks"],
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
    orbit: int,
    case: dict[str, object],
    *,
    cut_batch: int,
    max_rounds: int,
    progress_every: int,
    output_dir: Path | None,
) -> dict[str, object]:
    start = time.monotonic()
    context = build_case(orbit, case)
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
                partner_set = extract_partner(context, model)
                verify_model(context, deleted_set, partner_set)
                deleted_mask = sum(1 << edge_index for edge_index in deleted_set)
                available = SEARCH.available_indices(
                    context["family_masks"],
                    deleted_mask,
                )
                records = new_triple_records(context, available, cut_batch)
                if not records:
                    assert next(
                        SEARCH.disjoint_triples(
                            context["family_masks"],
                            available,
                            1,
                        ),
                        None,
                    ) is None
                    status = "relaxed-counterexample"
                    details = {
                        "deleted_edges": [
                            EDGES[index] for index in sorted(deleted_set)
                        ],
                        "partner_edges": [
                            EDGES[index] for index in sorted(partner_set)
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
        "orbit": orbit,
        "signature": signature_as_list(context["signature"]),
        "invariant": context["invariant"],
        "first_matching": [EDGES[index] for index in context["first"]],
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
        "partner_extension_clauses": len(context["relevant_thirds"]),
        "vertex_symmetry": False,
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "decision_scope": (
            f"orbit{orbit} canonical-first-matching support relaxation; "
            "exact D size, degree bounds, all cuts, existential compatible "
            "partner, partner-extension blockers, and global triple CEGIS"
        ),
        "proof_claimed": False,
        **artifact_details,
        **details,
    }


def signature_as_list(value: tuple[int, ...]) -> list[int]:
    return list(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--cases", default="all")
    parser.add_argument("--cut-batch", type=int, default=10_000)
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if not 0 <= args.orbit < len(AUDIT.VENN_SIGNATURES):
        parser.error("--orbit must lie in 0..15")
    if args.cut_batch <= 0:
        parser.error("--cut-batch must be positive")
    if args.max_rounds < 0 or args.progress_every < 0:
        parser.error("round counts must be nonnegative")

    representatives = canonical_first_matchings(args.orbit)
    if args.cases == "all":
        selected = tuple(range(len(representatives)))
    else:
        selected = tuple(int(value) for value in args.cases.split(","))
        if any(not 0 <= index < len(representatives) for index in selected):
            parser.error(
                f"case indices must lie in 0..{len(representatives) - 1}"
            )

    output = None
    if args.jsonl:
        args.jsonl.parent.mkdir(parents=True, exist_ok=True)
        output = args.jsonl.open("a", encoding="utf-8")
    try:
        for case_index in selected:
            result = solve_case(
                args.orbit,
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
