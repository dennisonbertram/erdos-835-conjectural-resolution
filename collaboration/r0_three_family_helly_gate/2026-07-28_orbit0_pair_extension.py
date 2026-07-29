#!/usr/bin/env python3
"""Exact finite SAT/CEGIS check for the orbit-0 cut-sufficiency gate.

Let H be the residual graph on the common ten-vertex support S and let
D[S] = K_10 - H.  The full-row setting gives |D[S]| <= 18 and
Delta(D[S]) <= 5.  This script asks, for each of the two possible cycle
types of the union of two edge-disjoint perfect matchings, whether all
internal-edge capacity cuts can hold while the graph has no triple of
edge-disjoint perfect matchings.  The fixed compatible pair is first
required not to extend; every remaining global triple is then excluded by
an exact CEGIS clause.

SAT after CEGIS gives a finite obstruction candidate.  UNSAT is exact for
the generated CNF, but a separately checkable proof certificate is still
needed before calling the result a theorem.
"""

from __future__ import annotations

import hashlib
from itertools import combinations
from pathlib import Path

from pysat.solvers import Cadical195

from search_counterexamples import Cnf


VERTICES = tuple(range(10))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
PAIR_TYPES = {
    "C10": (
        ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9)),
        ((0, 9), (1, 2), (3, 4), (5, 6), (7, 8)),
    ),
    "C4+C6": (
        ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9)),
        ((0, 3), (1, 2), (4, 9), (5, 6), (7, 8)),
    ),
}


def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    """Enumerate perfect matchings as tuples of local edge indices."""
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        edge_index = EDGE_INDEX[tuple(sorted((first, second)))]
        for tail in perfect_matchings(rest):
            result.append(tuple(sorted((edge_index, *tail))))
    return tuple(result)


def write_dimacs(path: Path, cnf: Cnf) -> str:
    """Write CNF and return its SHA-256 digest."""
    digest = hashlib.sha256()
    with path.open("w", encoding="ascii", newline="\n") as output:
        header = f"p cnf {cnf.top} {len(cnf.clauses)}\n"
        output.write(header)
        digest.update(header.encode("ascii"))
        for clause in cnf.clauses:
            line = " ".join(map(str, (*clause, 0))) + "\n"
            output.write(line)
            digest.update(line.encode("ascii"))
    return digest.hexdigest()


def build_instance(
    pair_type: str,
) -> tuple[Cnf, tuple[tuple[int, ...], ...]]:
    """Build the exact pair-nonextension instance for one union type."""
    cnf = Cnf()

    def deleted(edge_index: int) -> int:
        return cnf.variable(("deleted", edge_index))

    left, right = PAIR_TYPES[pair_type]
    fixed_edges = frozenset(
        EDGE_INDEX[tuple(sorted(edge))] for edge in (*left, *right)
    )
    for edge_index in fixed_edges:
        cnf.add(-deleted(edge_index))

    # Delta(D[S]) <= 5 follows from every prefix-deletion degree being <= 5.
    for vertex in VERTICES:
        cnf.cardinality(
            ("degree", vertex),
            [
                deleted(edge_index)
                for edge_index, edge in enumerate(EDGES)
                if vertex in edge
            ],
            upper=5,
        )

    # In orbit 0 the three omitted complements are a common triple T.
    # Their three occurrences force d_D(t) >= 4 for t in T.  Since |D|=27
    # and D[T] has at most three edges,
    #
    #   12 <= sum_{t in T} d_D(t)
    #      = |D[S,T]| + 2|D[T]|
    #      <= (27 - |D[S]|) + 3,
    #
    # hence |D[S]| <= 18.
    cnf.cardinality(
        ("total_deleted",),
        [deleted(edge_index) for edge_index in range(len(EDGES))],
        upper=18,
    )

    # For U subset S, the stated capacity inequality is
    # e_H(U) >= 3 max(0, |U|-5).
    for size in range(6, 11):
        required = 3 * (size - 5)
        for vertices in combinations(VERTICES, size):
            vertex_set = frozenset(vertices)
            internal_edges = [
                edge_index
                for edge_index, edge in enumerate(EDGES)
                if edge[0] in vertex_set and edge[1] in vertex_set
            ]
            cnf.cardinality(
                ("cut", vertices),
                [deleted(edge_index) for edge_index in internal_edges],
                upper=len(internal_edges) - required,
            )

    matchings = perfect_matchings(VERTICES)
    possible_thirds = tuple(
        matching
        for matching in matchings
        if fixed_edges.isdisjoint(matching)
    )
    # Every possible third matching must contain a deleted edge.
    for matching_index, matching in enumerate(possible_thirds):
        cnf.add(*(deleted(edge_index) for edge_index in matching))

    return cnf, possible_thirds


def verify_model(
    cnf: Cnf,
    possible_thirds: tuple[tuple[int, ...], ...],
    model: set[int],
) -> tuple[tuple[int, int], ...]:
    """Independently check every semantic condition on a SAT model."""
    deleted_indices = frozenset(
        edge_index
        for edge_index in range(len(EDGES))
        if cnf.variable(("deleted", edge_index)) in model
    )
    assert len(deleted_indices) <= 18
    assert all(
        sum(edge_index in deleted_indices for edge_index, edge in enumerate(EDGES)
            if vertex in edge)
        <= 5
        for vertex in VERTICES
    )
    for size in range(6, 11):
        required = 3 * (size - 5)
        for vertices in combinations(VERTICES, size):
            vertex_set = frozenset(vertices)
            available = sum(
                edge_index not in deleted_indices
                for edge_index, edge in enumerate(EDGES)
                if edge[0] in vertex_set and edge[1] in vertex_set
            )
            assert available >= required
    assert all(
        not deleted_indices.isdisjoint(matching)
        for matching in possible_thirds
    )
    return tuple(EDGES[index] for index in sorted(deleted_indices))


def disjoint_triples(
    matchings: tuple[tuple[int, ...], ...],
    deleted_indices: frozenset[int],
) -> tuple[tuple[int, ...], ...]:
    """Return distinct 15-edge unions of available disjoint triples."""
    available = tuple(
        frozenset(matching)
        for matching in matchings
        if deleted_indices.isdisjoint(matching)
    )
    unions = set()
    for left_index, left in enumerate(available):
        for middle_index in range(left_index + 1, len(available)):
            middle = available[middle_index]
            if not left.isdisjoint(middle):
                continue
            union = left | middle
            for right in available[middle_index + 1 :]:
                if union.isdisjoint(right):
                    unions.add(tuple(sorted(union | right)))
    return tuple(sorted(unions))


def main() -> None:
    output_dir = Path(__file__).with_name("2026-07-28_orbit0_pair_extension_cnf")
    output_dir.mkdir(exist_ok=True)
    all_unsat = True
    for pair_type in PAIR_TYPES:
        cnf, possible_thirds = build_instance(pair_type)
        matchings = perfect_matchings(VERTICES)
        rounds = 0
        global_cuts = 0
        with Cadical195(bootstrap_with=cnf.clauses) as solver:
            while True:
                rounds += 1
                satisfiable = solver.solve()
                if not satisfiable:
                    cnf_path = output_dir / f"{pair_type.replace('+', '_')}.cnf"
                    digest = write_dimacs(cnf_path, cnf)
                    print(
                        f"UNSAT {pair_type}: rounds={rounds} vars={cnf.top} "
                        f"clauses={len(cnf.clauses)} "
                        f"fixed_pair_thirds={len(possible_thirds)} "
                        f"global_cuts={global_cuts} sha256={digest}"
                    )
                    break
                model = {
                    literal for literal in solver.get_model() if literal > 0
                }
                deleted = verify_model(cnf, possible_thirds, model)
                deleted_indices = frozenset(EDGE_INDEX[edge] for edge in deleted)
                violating = disjoint_triples(matchings, deleted_indices)
                if not violating:
                    all_unsat = False
                    print(
                        f"SAT {pair_type}: rounds={rounds} "
                        f"fixed_pair_thirds={len(possible_thirds)} "
                        f"global_cuts={global_cuts} deleted={deleted}"
                    )
                    break
                for union in violating:
                    clause = tuple(
                        cnf.variable(("deleted", edge_index))
                        for edge_index in union
                    )
                    cnf.add(*clause)
                    solver.add_clause(clause)
                global_cuts += len(violating)
                print(
                    f"ROUND {pair_type} {rounds}: excluded "
                    f"{len(violating)} global triples "
                    f"(total {global_cuts})"
                )
    print(
        "RESULT orbit-0 support-level cut-sufficiency finite check: "
        + ("UNSAT in both union types" if all_unsat else "obstruction exists")
    )


if __name__ == "__main__":
    main()
