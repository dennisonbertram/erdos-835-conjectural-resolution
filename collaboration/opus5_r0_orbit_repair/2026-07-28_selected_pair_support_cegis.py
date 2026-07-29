#!/usr/bin/env python3
"""One-CNF selected-pair support relaxation for support orbits 4 through 15.

For each support orbit, choose the omitted-row pair with maximum
intersection, exactly as in the compatible-pair orbit classifier.  The SAT
formula existentially chooses two edge-disjoint perfect matchings for that
pair.  It does not fix their isomorphism type.

The model retains only consequences required for a sound outer relaxation:

* exactly 27 deleted edges;
* selected-row multiplicity plus one <= deleted degree <= five;
* every three-support capacity cut;
* one explicit compatible-pair witness for the selected pair; and
* the implied fact that this selected pair blocks every third-family
  matching; and
* CEGIS clauses excluding prescribed simultaneous triples.

Full remaining-row realizability, the six prefix layers, and compatibility
of the other two pairs are deliberately omitted.  Therefore UNSAT is sound
for the full target, while SAT is only a relaxed obstruction candidate.
"""

from __future__ import annotations

import argparse
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


SEARCH = load_module("selected_pair_search", SEARCH_PATH)
CLASSIFIER = load_module("selected_pair_classifier", CLASSIFIER_PATH)

VERTICES = SEARCH.VERTICES
EDGES = SEARCH.EDGES
EDGE_INDEX = SEARCH.EDGE_INDEX
PAIR_SLOTS = (0, 1)

assert VERTICES == CLASSIFIER.VERTICES
assert EDGES == CLASSIFIER.EDGES


def orbit_data(
    orbit: int,
) -> tuple[
    tuple[int, ...],
    tuple[frozenset[int], ...],
    tuple[int, int],
]:
    signatures = CLASSIFIER.venn_signatures()
    if not 4 <= orbit < len(signatures):
        raise ValueError("orbit must lie in 4..15")
    signature = signatures[orbit]
    rows = CLASSIFIER.representative(signature)
    pair = CLASSIFIER.maximum_intersection_pair(rows)
    return signature, rows, pair


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
    """Return every positive capacity cut in deletion upper-bound form."""
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
                for edge_index, edge in enumerate(EDGES)
                if edge[0] in vertex_set and edge[1] in vertex_set
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
    """Upper bound on deletions inside U from explicit base constraints."""
    size = len(vertices)
    vertex_set = frozenset(vertices)
    outside = tuple(vertex for vertex in VERTICES if vertex not in vertex_set)
    outside_lower_sum = sum(degree_lower[vertex] for vertex in outside)
    outside_edge_capacity = len(outside) * (len(outside) - 1) // 2

    # If L is the sum of degrees outside U, then the number of deleted edges
    # not internal to U is both at least ceil(L/2) and at least
    # L-C(|V-U|,2).  Use the selected-multiplicity lower bound for L.
    minimum_not_internal = max(
        (outside_lower_sum + 1) // 2,
        outside_lower_sum - outside_edge_capacity,
        0,
    )
    return min(
        size * (size - 1) // 2,
        5 * size // 2,
        27,
        27 - minimum_not_internal,
    )


def membership_cells(
    rows: tuple[frozenset[int], ...],
) -> tuple[tuple[int, ...], ...]:
    cells: dict[tuple[bool, ...], list[int]] = {}
    for vertex in VERTICES:
        pattern = tuple(vertex in row for row in rows)
        cells.setdefault(pattern, []).append(vertex)
    return tuple(
        tuple(cell)
        for _, cell in sorted(cells.items())
    )


def build_instance(orbit: int) -> dict[str, object]:
    signature, rows, selected_pair = orbit_data(orbit)
    supports = tuple(frozenset(VERTICES) - row for row in rows)
    families = tuple(
        SEARCH.perfect_matchings(tuple(sorted(support)))
        for support in supports
    )
    masks = SEARCH.matching_masks(families)
    multiplicity = selected_multiplicity(rows)
    degree_lower = tuple(value + 1 for value in multiplicity)
    all_cuts = all_capacity_cuts(supports)
    encoded_cuts = tuple(
        cut
        for cut in all_cuts
        if cut[2] < automatic_internal_upper(cut[0], degree_lower)
    )

    cnf = SEARCH.Cnf()

    def deleted(edge_index: int) -> int:
        return cnf.variable(("deleted", edge_index))

    def pair_edge(slot: int, edge_index: int) -> int:
        return cnf.variable(("pair_edge", slot, edge_index))

    cnf.cardinality(
        ("deleted_total",),
        [deleted(edge_index) for edge_index in range(len(EDGES))],
        lower=27,
        upper=27,
    )
    for vertex in VERTICES:
        incident = [
            deleted(edge_index)
            for edge_index, edge in enumerate(EDGES)
            if vertex in edge
        ]
        cnf.cardinality(
            ("deleted_degree", vertex),
            incident,
            lower=degree_lower[vertex],
            upper=5,
        )

    for vertices, internal_edges, upper_deleted in encoded_cuts:
        cnf.cardinality(
            ("capacity_cut", vertices),
            [deleted(edge_index) for edge_index in internal_edges],
            upper=upper_deleted,
        )

    for slot, family_index in enumerate(selected_pair):
        support = supports[family_index]
        for edge_index, edge in enumerate(EDGES):
            if edge[0] not in support or edge[1] not in support:
                continue
            literal = pair_edge(slot, edge_index)
            cnf.add(-literal, -deleted(edge_index))
        for vertex in sorted(support):
            incident = [
                pair_edge(slot, edge_index)
                for edge_index, edge in enumerate(EDGES)
                if vertex in edge
                and edge[0] in support
                and edge[1] in support
            ]
            cnf.cardinality(
                ("pair_vertex", slot, vertex),
                incident,
                lower=1,
                upper=1,
            )

    common_support = supports[selected_pair[0]] & supports[selected_pair[1]]
    for edge in combinations(sorted(common_support), 2):
        edge_index = EDGE_INDEX[edge]
        cnf.add(
            -pair_edge(0, edge_index),
            -pair_edge(1, edge_index),
        )

    # Under the sought no-triple condition, the existentially selected
    # compatible pair cannot extend to any matching from the third family.
    # For each such matching N, require either a deleted edge of N or an edge
    # shared by N and one of the selected witnesses.  This is an implied
    # condition, not a fixed-pair restriction: both witnesses remain SAT
    # variables ranging over all compatible pairs on the selected supports.
    third_family, = tuple(
        family_index
        for family_index in range(3)
        if family_index not in selected_pair
    )
    eligible_by_slot = tuple(
        frozenset(
            edge_index
            for edge_index, edge in enumerate(EDGES)
            if edge[0] in supports[family_index]
            and edge[1] in supports[family_index]
        )
        for family_index in selected_pair
    )
    pair_nonextension_clauses = 0
    for matching in families[third_family]:
        clause = [deleted(edge_index) for edge_index in matching]
        clause.extend(
            pair_edge(slot, edge_index)
            for slot in PAIR_SLOTS
            for edge_index in matching
            if edge_index in eligible_by_slot[slot]
        )
        cnf.add(*clause)
        pair_nonextension_clauses += 1

    # Within a full three-row membership cell, every vertex permutation
    # preserves all supports and constraints.  A globally lexicographically
    # least D-vector in each orbit satisfies all adjacent-generator
    # inequalities below (the inequalities need not force a unique or global
    # minimum).  Applying the same vertex permutation to the existential
    # pair witnesses gives witnesses for that D, so it is sound to constrain
    # only D here.
    deleted_vector = [deleted(edge_index) for edge_index in range(len(EDGES))]
    cells = membership_cells(rows)
    symmetry_generators = 0
    for cell_index, cell in enumerate(cells):
        for swap_index, (left_vertex, right_vertex) in enumerate(
            zip(cell, cell[1:])
        ):

            def swapped(vertex: int) -> int:
                if vertex == left_vertex:
                    return right_vertex
                if vertex == right_vertex:
                    return left_vertex
                return vertex

            swapped_vector = [
                deleted(
                    EDGE_INDEX[
                        tuple(sorted((swapped(edge[0]), swapped(edge[1]))))
                    ]
                )
                for edge in EDGES
            ]
            SEARCH.lexicographic_leq(
                cnf,
                ("deleted_cell_swap", cell_index, swap_index),
                deleted_vector,
                swapped_vector,
            )
            symmetry_generators += 1

    return {
        "orbit": orbit,
        "signature": signature,
        "rows": rows,
        "supports": supports,
        "selected_pair": selected_pair,
        "pair_intersection": len(rows[selected_pair[0]] & rows[selected_pair[1]]),
        "third_family": third_family,
        "pair_nonextension_clauses": pair_nonextension_clauses,
        "multiplicity": multiplicity,
        "degree_lower": degree_lower,
        "all_cuts": all_cuts,
        "encoded_cuts": encoded_cuts,
        "cut_size_inventory": Counter(len(cut[0]) for cut in encoded_cuts),
        "membership_cells": cells,
        "symmetry_generators": symmetry_generators,
        "cnf": cnf,
        "deleted": deleted,
        "pair_edge": pair_edge,
        "families": families,
        "masks": masks,
    }


def available_matching_indices(
    masks: tuple[tuple[int, ...], ...],
    deleted_mask: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            index
            for index, matching_mask in enumerate(family)
            if not matching_mask & deleted_mask
        )
        for family in masks
    )


def new_triple_unions(
    families: tuple[tuple[tuple[int, ...], ...], ...],
    masks: tuple[tuple[int, ...], ...],
    available: tuple[tuple[int, ...], ...],
    learned: set[tuple[int, ...]],
    limit: int,
) -> tuple[tuple[int, ...], ...]:
    """Enumerate up to limit new available prescribed-triple unions."""
    result = set()
    for left in available[0]:
        left_mask = masks[0][left]
        for middle in available[1]:
            middle_mask = masks[1][middle]
            if left_mask & middle_mask:
                continue
            union_mask = left_mask | middle_mask
            for right in available[2]:
                if union_mask & masks[2][right]:
                    continue
                union = tuple(sorted({
                    edge_index
                    for family, matching_index in enumerate(
                        (left, middle, right)
                    )
                    for edge_index in families[family][matching_index]
                }))
                assert len(union) == 15
                if union in learned:
                    continue
                result.add(union)
                if len(result) >= limit:
                    return tuple(sorted(result))
    return tuple(sorted(result))


def extract_deleted(context: dict[str, object], model: set[int]) -> frozenset[int]:
    deleted = context["deleted"]
    return frozenset(
        edge_index
        for edge_index in range(len(EDGES))
        if deleted(edge_index) in model
    )


def extract_pair_witnesses(
    context: dict[str, object],
    model: set[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    pair_edge = context["pair_edge"]
    selected_pair = context["selected_pair"]
    supports = context["supports"]
    result = []
    for slot, family_index in enumerate(selected_pair):
        support = supports[family_index]
        matching = tuple(
            edge_index
            for edge_index, edge in enumerate(EDGES)
            if edge[0] in support
            and edge[1] in support
            and pair_edge(slot, edge_index) in model
        )
        result.append(matching)
    return tuple(result)


def verify_relaxed_model(
    context: dict[str, object],
    deleted_set: frozenset[int],
    witnesses: tuple[tuple[int, ...], tuple[int, ...]],
) -> None:
    assert len(deleted_set) == 27
    degree_lower = context["degree_lower"]
    for vertex in VERTICES:
        degree = sum(
            edge_index in deleted_set
            for edge_index, edge in enumerate(EDGES)
            if vertex in edge
        )
        assert degree_lower[vertex] <= degree <= 5

    for vertices, internal_edges, upper_deleted in context["all_cuts"]:
        assert sum(
            edge_index in deleted_set for edge_index in internal_edges
        ) <= upper_deleted, vertices

    selected_pair = context["selected_pair"]
    supports = context["supports"]
    used = set()
    for slot, matching in enumerate(witnesses):
        assert len(matching) == 5
        assert deleted_set.isdisjoint(matching)
        endpoints = [
            vertex
            for edge_index in matching
            for vertex in EDGES[edge_index]
        ]
        assert len(endpoints) == len(set(endpoints)) == 10
        assert set(endpoints) == set(supports[selected_pair[slot]])
        assert used.isdisjoint(matching)
        used.update(matching)

    third_family = context["third_family"]
    for matching in context["families"][third_family]:
        assert (
            not deleted_set.isdisjoint(matching)
            or not used.isdisjoint(matching)
        )


def solve_orbit(
    orbit: int,
    *,
    cut_batch: int,
    max_rounds: int,
    progress_every: int,
) -> dict[str, object]:
    start = time.monotonic()
    context = build_instance(orbit)
    cnf = context["cnf"]
    learned: set[tuple[int, ...]] = set()
    rounds = 0
    initial_clauses = len(cnf.clauses)

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
            witnesses = extract_pair_witnesses(context, model)
            verify_relaxed_model(context, deleted_set, witnesses)
            deleted_mask = sum(1 << edge_index for edge_index in deleted_set)
            available = available_matching_indices(
                context["masks"],
                deleted_mask,
            )
            unions = new_triple_unions(
                context["families"],
                context["masks"],
                available,
                learned,
                cut_batch,
            )
            if not unions:
                # Because the current model satisfies every previously
                # learned union clause, no learned union can be available.
                # Exhaustion therefore proves that this D has no prescribed
                # simultaneous triple.
                assert next(
                    SEARCH.disjoint_triples(
                        context["masks"],
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
                    "pair_witnesses": [
                        [EDGES[index] for index in matching]
                        for matching in witnesses
                    ],
                    "available_matching_counts": list(map(len, available)),
                }
                break

            for union in unions:
                clause = tuple(
                    context["deleted"](edge_index) for edge_index in union
                )
                cnf.add(*clause)
                solver.add_clause(clause)
            learned.update(unions)

            if progress_every and rounds % progress_every == 0:
                print(json.dumps({
                    "status": "progress",
                    "orbit": orbit,
                    "rounds": rounds,
                    "learned_unions": len(learned),
                    "available_matching_counts": list(map(len, available)),
                    "elapsed_seconds": round(time.monotonic() - start, 3),
                }, sort_keys=True), flush=True)
        else:
            status = "round-limit"
            details = {}

    return {
        "status": status,
        "orbit": orbit,
        "signature": context["signature"],
        "rows": [sorted(row) for row in context["rows"]],
        "selected_pair": context["selected_pair"],
        "pair_intersection": context["pair_intersection"],
        "rounds": rounds,
        "learned_unions": len(learned),
        "variables": cnf.top,
        "initial_clauses": initial_clauses,
        "final_clauses": len(cnf.clauses),
        "positive_capacity_cuts": len(context["all_cuts"]),
        "encoded_capacity_cuts": len(context["encoded_cuts"]),
        "encoded_cut_size_inventory": dict(
            sorted(context["cut_size_inventory"].items())
        ),
        "symmetry_generators": context["symmetry_generators"],
        "pair_nonextension_clauses": context["pair_nonextension_clauses"],
        "membership_cells": context["membership_cells"],
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "decision_scope": (
            "selected-pair support relaxation; full rows, prefix layers, "
            "and other pair compatibilities omitted"
        ),
        "proof_claimed": False,
        **details,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", nargs="+", type=int, default=(4,))
    parser.add_argument("--cut-batch", type=int, default=10_000)
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--jsonl", type=Path)
    args = parser.parse_args()
    if any(not 4 <= orbit <= 15 for orbit in args.orbits):
        parser.error("orbits must lie in 4..15")
    if args.cut_batch <= 0:
        parser.error("--cut-batch must be positive")
    if args.max_rounds < 0 or args.progress_every < 0:
        parser.error("round counts must be nonnegative")

    output = None
    if args.jsonl:
        args.jsonl.parent.mkdir(parents=True, exist_ok=True)
        output = args.jsonl.open("a", encoding="utf-8")
    try:
        for orbit in args.orbits:
            result = solve_orbit(
                orbit,
                cut_batch=args.cut_batch,
                max_rounds=args.max_rounds,
                progress_every=args.progress_every,
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
