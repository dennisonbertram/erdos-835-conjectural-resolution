#!/usr/bin/env python3
"""Certificate-oriented full-row cut-sufficiency search over all 16 orbits.

This isolated driver keeps the decision predicate and CEGIS implementation in
``search_counterexamples.py`` unchanged.  It replaces only the expensive
support-orbit discovery with an exact enumeration of the seven Venn-cell
sizes, and it always installs every potentially binding capacity cut before
solving.

An ``unsat`` result remains uncertified search output until the emitted CNF is
proved by an external proof-producing solver and checked independently.
"""

from __future__ import annotations

import argparse
import json
import time
from itertools import permutations, product
from pathlib import Path

import search_counterexamples as search


CELL_MASKS = tuple(range(1, 8))


def permuted_signature(
    signature: tuple[int, ...],
    order: tuple[int, int, int],
) -> tuple[int, ...]:
    """Relabel the three families in one seven-cell Venn signature."""
    result = [0] * 7
    for old_mask, count in zip(CELL_MASKS, signature):
        new_mask = sum(
            ((old_mask >> old_index) & 1) << new_index
            for new_index, old_index in enumerate(order)
        )
        result[new_mask - 1] = count
    return tuple(result)


def canonical_cell_signature(signature: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        permuted_signature(signature, order)
        for order in permutations(range(3))
    )


def representative_from_signature(
    signature: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    """Build a labelled representative whose first triple is {0,1,2}."""
    vertices_by_mask: dict[int, tuple[int, ...]] = {}
    next_vertex = 0
    # Allocate cells meeting the first triple first.  Their total is exactly
    # three, so that triple receives the fixed anchor labels 0,1,2.
    for mask in (1, 3, 5, 7, 2, 4, 6):
        count = signature[mask - 1]
        vertices_by_mask[mask] = tuple(
            range(next_vertex, next_vertex + count)
        )
        next_vertex += count
    if next_vertex > len(search.VERTICES):
        raise AssertionError("Venn signature uses too many vertices")
    triples = tuple(
        tuple(
            sorted(
                vertex
                for mask, vertices in vertices_by_mask.items()
                if mask & (1 << family)
                for vertex in vertices
            )
        )
        for family in range(3)
    )
    if triples[0] != (0, 1, 2):
        raise AssertionError("representative does not have the fixed anchor")
    if any(len(triple) != 3 for triple in triples):
        raise AssertionError("representative triple has the wrong size")
    if search.membership_signature(triples) != signature:
        raise AssertionError("representative has the wrong Venn signature")
    return triples


def support_orbits_fast(
) -> tuple[tuple[tuple[int, ...], tuple[tuple[int, ...], ...]], ...]:
    """Enumerate the 16 orbits from integer Venn-cell data.

    Every nonempty Venn cell has size at most three.  The three equations
    saying that each family has size three, together with total size at most
    thirteen, are complete.  Venn-cell sizes classify a three-set system up
    to vertex permutations; quotienting the six family permutations is
    therefore orbit-complete.
    """
    signatures = set()
    for candidate in product(range(4), repeat=7):
        if any(
            sum(
                candidate[mask - 1]
                for mask in CELL_MASKS
                if mask & (1 << family)
            )
            != 3
            for family in range(3)
        ):
            continue
        if sum(candidate) > len(search.VERTICES):
            continue
        signatures.add(canonical_cell_signature(candidate))
    result = tuple(
        (signature, representative_from_signature(signature))
        for signature in sorted(signatures)
    )
    if len(result) != 16:
        raise AssertionError(f"expected 16 support orbits, found {len(result)}")
    if any(
        search.canonical_signature(representative) != signature
        for signature, representative in result
    ):
        raise AssertionError("fast orbit representative failed canonical audit")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", default="all")
    parser.add_argument("--cut-batch", type=int, default=10_000)
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument(
        "--unsat-cnf-dir",
        type=Path,
        required=True,
        help="directory for exact accumulated DIMACS files of UNSAT orbits",
    )
    parser.add_argument("--jsonl", type=Path)
    args = parser.parse_args()
    if args.cut_batch <= 0:
        parser.error("--cut-batch must be positive")
    if args.max_rounds < 0:
        parser.error("--max-rounds must be nonnegative")

    orbit_start = time.monotonic()
    orbits = support_orbits_fast()
    orbit_seconds = time.monotonic() - orbit_start
    selected = search.parse_orbits(args.orbits, len(orbits))
    output = args.jsonl.open("a", encoding="utf-8") if args.jsonl else None
    try:
        print(
            json.dumps(
                {
                    "support_orbits": len(orbits),
                    "orbit_enumeration_seconds": round(orbit_seconds, 6),
                    "orbit_method": "integer_venn_cells",
                },
                sort_keys=True,
            ),
            flush=True,
        )
        for orbit_index in selected:
            signature, representative = orbits[orbit_index]
            result = search.solve_orbit(
                orbit_index,
                signature,
                representative,
                cut_batch=args.cut_batch,
                full_rows=True,
                max_rounds=args.max_rounds,
                require_cut_feasible=True,
                static_cut_feasible=True,
                unsat_cnf_dir=args.unsat_cnf_dir,
            )
            result.update(
                {
                    "proof_claimed": False,
                    "orbit_method": "integer_venn_cells",
                    "decision_scope": (
                        "full-row pairwise-compatible nonpackable "
                        "cut-feasible triple"
                    ),
                }
            )
            line = json.dumps(result, sort_keys=True)
            print(line, flush=True)
            if output:
                output.write(line + "\n")
                output.flush()
            if result["status"] == "counterexample":
                break
    finally:
        if output:
            output.close()


if __name__ == "__main__":
    main()
