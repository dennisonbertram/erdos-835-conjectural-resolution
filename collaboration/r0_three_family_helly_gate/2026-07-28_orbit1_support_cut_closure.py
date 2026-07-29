#!/usr/bin/env python3
"""Exact finite SAT/CEGIS check for orbit-1 support-level cut sufficiency.

The omitted triples are 012, 023, 123.  Vertex 2 lies outside every selected
support.  The other three special vertices 0, 1, 3 are relabelled here as
terminals 0, 1, 2, and the common nine-vertex core is 3,...,11.

Any compatible pair for the first two supports has an alternating
terminal-to-terminal path plus alternating even cycles.  On nine core
vertices its union has one of exactly five types:

    P10, P6+C4, P4+C6, P2+C8, P2+C4+C4.

For each canonical type this script asks whether the exact support cuts,
Delta(D) <= 5, and the full-row consequence |D[R]| <= 23 allow a graph with
no simultaneous triple.  Pair compatibility for the first two supports is
fixed explicitly.  Compatibility with the third support is deliberately not
assumed: UNSAT therefore proves a stronger statement.

SAT gives a support-level obstruction candidate that must still be checked
for the other pair compatibilities and exact full-row embeddability.  UNSAT is
exact for the generated CNF; frozen proof traces should be replayed before
promoting it to a computer-assisted theorem.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from itertools import combinations
from pathlib import Path

from pysat.solvers import Cadical195

from search_counterexamples import Cnf


VERTICES = tuple(range(12))
TERMINALS = (0, 1, 2)
CORE = tuple(range(3, 12))
SUPPORTS = (
    frozenset((TERMINALS[0], *CORE)),
    frozenset((TERMINALS[1], *CORE)),
    frozenset((TERMINALS[2], *CORE)),
)
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def edge(left: int, right: int) -> tuple[int, int]:
    """Return one normalized edge."""
    return tuple(sorted((left, right)))


W = CORE
PAIR_TYPES = {
    "P10": (
        (
            edge(0, W[0]),
            edge(W[1], W[2]),
            edge(W[3], W[4]),
            edge(W[5], W[6]),
            edge(W[7], W[8]),
        ),
        (
            edge(W[0], W[1]),
            edge(W[2], W[3]),
            edge(W[4], W[5]),
            edge(W[6], W[7]),
            edge(W[8], 1),
        ),
    ),
    "P6+C4": (
        (
            edge(0, W[0]),
            edge(W[1], W[2]),
            edge(W[3], W[4]),
            edge(W[5], W[6]),
            edge(W[7], W[8]),
        ),
        (
            edge(W[0], W[1]),
            edge(W[2], W[3]),
            edge(W[4], 1),
            edge(W[6], W[7]),
            edge(W[8], W[5]),
        ),
    ),
    "P4+C6": (
        (
            edge(0, W[0]),
            edge(W[1], W[2]),
            edge(W[3], W[4]),
            edge(W[5], W[6]),
            edge(W[7], W[8]),
        ),
        (
            edge(W[0], W[1]),
            edge(W[2], 1),
            edge(W[4], W[5]),
            edge(W[6], W[7]),
            edge(W[8], W[3]),
        ),
    ),
    "P2+C8": (
        (
            edge(0, W[0]),
            edge(W[1], W[2]),
            edge(W[3], W[4]),
            edge(W[5], W[6]),
            edge(W[7], W[8]),
        ),
        (
            edge(W[0], 1),
            edge(W[2], W[3]),
            edge(W[4], W[5]),
            edge(W[6], W[7]),
            edge(W[8], W[1]),
        ),
    ),
    "P2+C4+C4": (
        (
            edge(0, W[0]),
            edge(W[1], W[2]),
            edge(W[3], W[4]),
            edge(W[5], W[6]),
            edge(W[7], W[8]),
        ),
        (
            edge(W[0], 1),
            edge(W[2], W[3]),
            edge(W[4], W[1]),
            edge(W[6], W[7]),
            edge(W[8], W[5]),
        ),
    ),
}
EXPECTED_THIRDS = {
    "P10": 365,
    "P6+C4": 366,
    "P4+C6": 364,
    "P2+C8": 359,
    "P2+C4+C4": 361,
}


def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    """Enumerate perfect matchings as tuples of global edge indices."""
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        edge_index = EDGE_INDEX[edge(first, second)]
        for tail in perfect_matchings(rest):
            result.append(tuple(sorted((edge_index, *tail))))
    return tuple(result)


FAMILIES = tuple(
    perfect_matchings(tuple(sorted(support))) for support in SUPPORTS
)
assert tuple(map(len, FAMILIES)) == (945, 945, 945)


def cut_requirements() -> tuple[tuple[tuple[int, ...], tuple[int, ...], int], ...]:
    """Return every nonautomatic support cut for U contained in R."""
    requirements = []
    for size in range(len(VERTICES) + 1):
        for vertices in combinations(VERTICES, size):
            vertex_set = frozenset(vertices)
            required = sum(
                max(0, len(support & vertex_set) - 5)
                for support in SUPPORTS
            )
            if not required:
                continue
            internal_edges = tuple(
                edge_index
                for edge_index, endpoints in enumerate(EDGES)
                if endpoints[0] in vertex_set and endpoints[1] in vertex_set
            )
            upper_deleted = len(internal_edges) - required
            maximum_deleted = min(
                len(internal_edges),
                23,
                5 * len(vertices) // 2,
            )
            if upper_deleted >= maximum_deleted:
                continue
            requirements.append((vertices, internal_edges, upper_deleted))
    return tuple(requirements)


def build_instance(
    pair_type: str,
) -> tuple[Cnf, tuple[tuple[int, ...], ...]]:
    """Build one exact canonical-pair instance."""
    cnf = Cnf()

    def deleted(edge_index: int) -> int:
        return cnf.variable(("deleted", edge_index))

    left, right = PAIR_TYPES[pair_type]
    fixed_edges = frozenset(
        EDGE_INDEX[endpoints] for endpoints in (*left, *right)
    )
    assert len(fixed_edges) == 10
    assert tuple(
        frozenset(vertex for endpoints in matching for vertex in endpoints)
        for matching in (left, right)
    ) == SUPPORTS[:2]
    assert (
        frozenset(EDGE_INDEX[endpoints] for endpoints in left).isdisjoint(
            EDGE_INDEX[endpoints] for endpoints in right
        )
    )
    assert fixed_edges == frozenset(
        EDGE_INDEX[endpoints] for matching in (left, right)
        for endpoints in matching
    )
    for edge_index in fixed_edges:
        cnf.add(-deleted(edge_index))

    for vertex in VERTICES:
        cnf.cardinality(
            ("degree", vertex),
            [
                deleted(edge_index)
                for edge_index, endpoints in enumerate(EDGES)
                if vertex in endpoints
            ],
            upper=5,
        )

    # In the original 13-vertex instance, vertex 2 belongs to all three
    # omitted triples.  Thus rho(2) >= 3 and rho=d_D-1 imply d_D(2) >= 4.
    # Since the prefix union has 27 edges, deleting vertex 2 leaves at most
    # 23 deleted edges on R.
    cnf.cardinality(
        ("total_deleted",),
        [deleted(edge_index) for edge_index in range(len(EDGES))],
        upper=23,
    )

    requirements = cut_requirements()
    for vertices, internal_edges, upper_deleted in requirements:
        cnf.cardinality(
            ("cut", vertices),
            [deleted(edge_index) for edge_index in internal_edges],
            upper=upper_deleted,
        )

    possible_thirds = tuple(
        matching
        for matching in FAMILIES[2]
        if fixed_edges.isdisjoint(matching)
    )
    assert len(possible_thirds) == EXPECTED_THIRDS[pair_type]
    for matching in possible_thirds:
        cnf.add(*(deleted(edge_index) for edge_index in matching))

    return cnf, possible_thirds


def deleted_indices(cnf: Cnf, model: set[int]) -> frozenset[int]:
    """Extract the semantic deleted-edge set from a SAT model."""
    return frozenset(
        edge_index
        for edge_index in range(len(EDGES))
        if cnf.variable(("deleted", edge_index)) in model
    )


def verify_model(
    pair_type: str,
    possible_thirds: tuple[tuple[int, ...], ...],
    deleted_set: frozenset[int],
) -> None:
    """Independently check every semantic base condition."""
    assert len(deleted_set) <= 23
    assert all(
        sum(
            edge_index in deleted_set
            for edge_index, endpoints in enumerate(EDGES)
            if vertex in endpoints
        )
        <= 5
        for vertex in VERTICES
    )
    fixed_edges = frozenset(
        EDGE_INDEX[endpoints]
        for matching in PAIR_TYPES[pair_type]
        for endpoints in matching
    )
    assert deleted_set.isdisjoint(fixed_edges)
    for vertices, internal_edges, upper_deleted in cut_requirements():
        assert sum(edge_index in deleted_set for edge_index in internal_edges) <= (
            upper_deleted
        ), vertices
    assert all(
        not deleted_set.isdisjoint(matching)
        for matching in possible_thirds
    )


def disjoint_triple_unions(
    deleted_set: frozenset[int],
) -> tuple[tuple[int, ...], ...]:
    """Enumerate distinct available 15-edge triple unions."""
    available = tuple(
        tuple(
            frozenset(matching)
            for matching in family
            if deleted_set.isdisjoint(matching)
        )
        for family in FAMILIES
    )
    unions = set()
    for left in available[0]:
        for middle in available[1]:
            if not left.isdisjoint(middle):
                continue
            union = left | middle
            for right in available[2]:
                if union.isdisjoint(right):
                    unions.add(tuple(sorted(union | right)))
    return tuple(sorted(unions))


def write_dimacs(path: Path, cnf: Cnf) -> str:
    """Write the frozen CNF and return its SHA-256 digest."""
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


def solve_type(
    pair_type: str,
    *,
    output_dir: Path,
    max_rounds: int,
) -> dict[str, object]:
    """Run exact CEGIS for one canonical pair type."""
    cnf, possible_thirds = build_instance(pair_type)
    rounds = 0
    global_cuts = 0
    with Cadical195(bootstrap_with=cnf.clauses) as solver:
        while max_rounds == 0 or rounds < max_rounds:
            rounds += 1
            if not solver.solve():
                path = output_dir / f"{pair_type.replace('+', '_')}.cnf"
                digest = write_dimacs(path, cnf)
                return {
                    "status": "unsat",
                    "pair_type": pair_type,
                    "rounds": rounds,
                    "variables": cnf.top,
                    "clauses": len(cnf.clauses),
                    "possible_thirds": len(possible_thirds),
                    "global_cuts": global_cuts,
                    "sha256": digest,
                }
            model = {
                literal for literal in solver.get_model() if literal > 0
            }
            deleted_set = deleted_indices(cnf, model)
            verify_model(pair_type, possible_thirds, deleted_set)
            violating = disjoint_triple_unions(deleted_set)
            if not violating:
                return {
                    "status": "sat",
                    "pair_type": pair_type,
                    "rounds": rounds,
                    "variables": cnf.top,
                    "clauses": len(cnf.clauses),
                    "possible_thirds": len(possible_thirds),
                    "global_cuts": global_cuts,
                    "deleted": tuple(
                        EDGES[edge_index]
                        for edge_index in sorted(deleted_set)
                    ),
                    "family_sizes": tuple(
                        sum(
                            deleted_set.isdisjoint(matching)
                            for matching in family
                        )
                        for family in FAMILIES
                    ),
                }
            for union in violating:
                clause = tuple(
                    cnf.variable(("deleted", edge_index))
                    for edge_index in union
                )
                cnf.add(*clause)
                solver.add_clause(clause)
            global_cuts += len(violating)
        return {
            "status": "round_limit",
            "pair_type": pair_type,
            "rounds": rounds,
            "variables": cnf.top,
            "clauses": len(cnf.clauses),
            "possible_thirds": len(possible_thirds),
            "global_cuts": global_cuts,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--types",
        nargs="*",
        choices=tuple(PAIR_TYPES),
        default=tuple(PAIR_TYPES),
    )
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).with_name(
            "2026-07-28_orbit1_support_cut_closure_cnf"
        ),
    )
    args = parser.parse_args()
    requirements = cut_requirements()
    assert len(requirements) == 507
    assert Counter(map(lambda requirement: len(requirement[0]), requirements)) == {
        6: 462,
        7: 36,
        8: 9,
    }
    args.output_dir.mkdir(exist_ok=True)
    for pair_type in args.types:
        print(
            solve_type(
                pair_type,
                output_dir=args.output_dir,
                max_rounds=args.max_rounds,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
