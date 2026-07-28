#!/usr/bin/env python3
"""Exact CEGIS search for the r=0 three-family coordination gate.

This is a search program, not a proof certificate.  It searches each orbit of
three 10-vertex supports, allowing repeated supports.  Pairwise compatibility
is encoded using the certified r=0 two-family gate: for live families, it is
equivalent to the absence of an edge forced in both families.

Whenever a model admits three pairwise edge-disjoint perfect matchings, the
corresponding blocking clause is added and the SAT solver is resumed.  A model
with no such triple is an exact counterexample.  An UNSAT result is exact for
the accumulated finite CNF, but should be independently certified before it is
used as a proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from itertools import combinations, permutations
from pathlib import Path
from typing import Iterable

from pysat.solvers import Cadical195


VERTICES = tuple(range(13))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
PREFIX_SIZES = (4, 4, 4, 5, 5, 5)


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Return perfect matchings as sorted tuples of edge-bit indices."""
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


def membership_signature(triples: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    """Seven nonempty Venn-cell sizes, in binary membership-mask order."""
    triple_sets = tuple(frozenset(triple) for triple in triples)
    return tuple(
        sum(
            all(
                (vertex in triple_sets[index]) == bool(mask & (1 << index))
                for index in range(3)
            )
            for vertex in VERTICES
        )
        for mask in range(1, 8)
    )


def canonical_signature(triples: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return min(
        membership_signature(tuple(triples[index] for index in order))
        for order in permutations(range(3))
    )


def support_orbits() -> tuple[tuple[tuple[int, ...], tuple[tuple[int, ...], ...]], ...]:
    """Enumerate the 16 vertex- and family-permutation support orbits."""
    anchor = (0, 1, 2)
    triples = tuple(combinations(VERTICES, 3))
    examples: dict[tuple[int, ...], tuple[tuple[int, ...], ...]] = {}
    for second in triples:
        for third in triples:
            representative = (anchor, second, third)
            signature = canonical_signature(representative)
            examples.setdefault(signature, representative)
    return tuple(sorted(examples.items()))


class Cnf:
    """Small exact CNF builder with an exact unary cardinality counter."""

    def __init__(self) -> None:
        self.top = 0
        self.variables: dict[tuple, int] = {}
        self.clauses: list[tuple[int, ...]] = []
        self.true = self.variable(("constant", True))
        self.false = self.variable(("constant", False))
        self.add(self.true)
        self.add(-self.false)

    def variable(self, key: tuple) -> int:
        if key not in self.variables:
            self.top += 1
            self.variables[key] = self.top
        return self.variables[key]

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))

    def cardinality(
        self,
        tag: tuple,
        literals: list[int],
        *,
        lower: int | None = None,
        upper: int | None = None,
    ) -> None:
        count_literals = len(literals)
        if lower is not None and not 0 <= lower <= count_literals:
            raise ValueError("invalid lower bound")
        if upper is not None and not 0 <= upper <= count_literals:
            raise ValueError("invalid upper bound")
        if lower is not None and upper is not None and lower > upper:
            raise ValueError("inconsistent bounds")

        largest = 0
        if lower:
            largest = max(largest, lower)
        if upper is not None and upper < count_literals:
            largest = max(largest, upper + 1)
        if not largest:
            return

        def state(prefix: int, count: int) -> int:
            if count == 0:
                return self.true
            if prefix == 0 or count > prefix:
                return self.false
            return self.variable(("counter", tag, prefix, count))

        for prefix, literal in enumerate(literals, start=1):
            for count in range(1, min(prefix, largest) + 1):
                current = state(prefix, count)
                old_same = state(prefix - 1, count)
                old_previous = state(prefix - 1, count - 1)
                self.add(-old_same, current)
                self.add(-old_previous, -literal, current)
                self.add(-current, old_same, old_previous)
                self.add(-current, old_same, literal)

        if lower:
            self.add(state(count_literals, lower))
        if upper is not None and upper < count_literals:
            self.add(-state(count_literals, upper + 1))


def lexicographic_leq(
    cnf: Cnf,
    tag: tuple,
    left: list[int],
    right: list[int],
) -> None:
    """Encode the bit vector ``left`` as lexicographically <= ``right``."""
    if len(left) != len(right):
        raise ValueError("lexicographic vectors have different lengths")
    prefix_equal = cnf.true
    for position, (left_bit, right_bit) in enumerate(zip(left, right)):
        cnf.add(-prefix_equal, -left_bit, right_bit)
        next_equal = cnf.variable(("lex_equal", tag, position))
        cnf.add(-next_equal, prefix_equal)
        cnf.add(-next_equal, -left_bit, right_bit)
        cnf.add(-next_equal, left_bit, -right_bit)
        cnf.add(-prefix_equal, -left_bit, -right_bit, next_equal)
        cnf.add(-prefix_equal, left_bit, right_bit, next_equal)
        prefix_equal = next_equal


def build_instance(
    omitted_triples: tuple[tuple[int, ...], ...],
    *,
    full_rows: bool,
    matching_constraints: bool = True,
    fixed_prefix_sizes: bool = True,
    vertex_symmetry: bool = True,
) -> tuple[Cnf, tuple[tuple[tuple[int, ...], ...], ...]]:
    supports = tuple(
        frozenset(VERTICES) - frozenset(triple) for triple in omitted_triples
    )
    families = (
        tuple(
            perfect_matchings(tuple(sorted(support))) for support in supports
        )
        if matching_constraints
        else ((), (), ())
    )
    cnf = Cnf()

    def colour_edge(colour: int, edge_index: int) -> int:
        return cnf.variable(("colour_edge", colour, edge_index))

    def deleted(edge_index: int) -> int:
        return cnf.variable(("deleted_edge", edge_index))

    def available(family: int, matching: int) -> int:
        return cnf.variable(("available_matching", family, matching))

    def remaining_row(row: int, vertex: int) -> int:
        return cnf.variable(("remaining_row", row, vertex))

    for colour, size in enumerate(PREFIX_SIZES):
        colour_edges = [
            colour_edge(colour, edge_index) for edge_index in range(len(EDGES))
        ]
        cnf.cardinality(
            ("colour_size", colour),
            colour_edges,
            lower=size if fixed_prefix_sizes else None,
            upper=size if fixed_prefix_sizes else len(VERTICES) // 2,
        )
        for vertex in VERTICES:
            cnf.cardinality(
                ("colour_vertex", colour, vertex),
                [
                    colour_edge(colour, edge_index)
                    for edge_index, edge in enumerate(EDGES)
                    if vertex in edge
                ],
                upper=1,
            )

    # The three size-four layers and the three size-five layers are unordered:
    # only their union is used by the matching families and capacity cuts.
    for left, right in ((0, 1), (1, 2), (3, 4), (4, 5)):
        lexicographic_leq(
            cnf,
            ("prefix", left, right),
            [
                colour_edge(left, edge_index)
                for edge_index in range(len(EDGES))
            ],
            [
                colour_edge(right, edge_index)
                for edge_index in range(len(EDGES))
            ],
        )

    for edge_index, edge in enumerate(EDGES):
        colours = [
            colour_edge(colour, edge_index) for colour in range(len(PREFIX_SIZES))
        ]
        cnf.cardinality(("edge_colour", edge), colours, upper=1)
        for literal in colours:
            cnf.add(-literal, deleted(edge_index))
        cnf.add(-deleted(edge_index), *colours)

    if not fixed_prefix_sizes:
        cnf.cardinality(
            ("deleted_edge_total",),
            [deleted(edge_index) for edge_index in range(len(EDGES))],
            lower=sum(PREFIX_SIZES),
            upper=sum(PREFIX_SIZES),
        )

    for vertex in VERTICES:
        cnf.cardinality(
            ("deleted_degree", vertex),
            [
                deleted(edge_index)
                for edge_index, edge in enumerate(EDGES)
                if vertex in edge
            ],
            lower=1,
            upper=5,
        )

    # Vertices with the same membership vector in the three fixed omitted
    # triples are interchangeable.  In every orbit choose a labelling whose
    # deleted-edge vector is lexicographically least.  Such a representative
    # is no larger than its image under every adjacent transposition inside a
    # membership cell, so the following generator constraints are
    # orbit-complete.  They do not assume that the remaining rows are
    # distinct.
    if vertex_symmetry:
        triple_sets = tuple(frozenset(triple) for triple in omitted_triples)
        membership_cells: dict[tuple[bool, ...], list[int]] = {}
        for vertex in VERTICES:
            pattern = tuple(vertex in triple for triple in triple_sets)
            membership_cells.setdefault(pattern, []).append(vertex)
        deleted_vector = [
            deleted(edge_index) for edge_index in range(len(EDGES))
        ]
        for cell_index, cell in enumerate(
            sorted(
                membership_cells.values(),
                key=lambda vertices: tuple(vertices),
            )
        ):
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
                            tuple(
                                sorted(
                                    (swapped(edge[0]), swapped(edge[1]))
                                )
                            )
                        ]
                    )
                    for edge in EDGES
                ]
                lexicographic_leq(
                    cnf,
                    ("deleted_vertex_swap", cell_index, swap_index),
                    deleted_vector,
                    swapped_vector,
                )

    if full_rows:
        # The eleven remaining complements are seven triples followed by four
        # five-sets.  The first three triples are the three support complements
        # whose coordination is being tested.
        remaining_sizes = (3,) * 7 + (5,) * 4
        for row, size in enumerate(remaining_sizes):
            row_literals = [
                remaining_row(row, vertex) for vertex in VERTICES
            ]
            cnf.cardinality(
                ("remaining_row_size", row),
                row_literals,
                lower=size,
                upper=size,
            )
        for row, triple in enumerate(omitted_triples):
            triple_set = frozenset(triple)
            for vertex in VERTICES:
                literal = remaining_row(row, vertex)
                cnf.add(literal if vertex in triple_set else -literal)

        # Rows 3..6 are the four unspecified triple occurrences, and rows
        # 7..10 are the four unspecified five-set occurrences.  Within each
        # group the row labels have no mathematical meaning: the only later
        # constraints use their column sums.  Sorting each group therefore
        # selects an orbit-complete representative and removes a 4! x 4!
        # permutation symmetry without identifying repeated occurrences.
        for left, right in (
            (3, 4),
            (4, 5),
            (5, 6),
            (7, 8),
            (8, 9),
            (9, 10),
        ):
            lexicographic_leq(
                cnf,
                ("remaining_row", left, right),
                [remaining_row(left, vertex) for vertex in VERTICES],
                [remaining_row(right, vertex) for vertex in VERTICES],
            )

        # d_D(v) + (11-rho(v)) = 12 is rho(v)=d_D(v)-1.  Together
        # with the row sizes, this is the exact remaining class-B inventory.
        for vertex in VERTICES:
            incident_deletions = [
                deleted(edge_index)
                for edge_index, edge in enumerate(EDGES)
                if vertex in edge
            ]
            absent_from_rows = [
                -remaining_row(row, vertex) for row in range(11)
            ]
            cnf.cardinality(
                ("class_b_column", vertex),
                incident_deletions + absent_from_rows,
                lower=12,
                upper=12,
            )

    if matching_constraints:
        for family_index, family in enumerate(families):
            for matching_index, matching in enumerate(family):
                literal = available(family_index, matching_index)
                deletions = [deleted(edge_index) for edge_index in matching]
                for edge_literal in deletions:
                    cnf.add(-literal, -edge_literal)
                cnf.add(literal, *deletions)
            cnf.add(
                *(
                    available(family_index, matching_index)
                    for matching_index in range(len(family))
                )
            )

        # The certified pair gate says that two live families fail to coordinate
        # iff some common-support edge is forced in both.  Exclude every such
        # edge.
        for left, right in combinations(range(3), 2):
            for edge in combinations(
                sorted(supports[left] & supports[right]), 2
            ):
                edge_index = EDGE_INDEX[edge]
                witnesses = [
                    available(left, matching_index)
                    for matching_index, matching in enumerate(families[left])
                    if edge_index not in matching
                ]
                witnesses.extend(
                    available(right, matching_index)
                    for matching_index, matching in enumerate(families[right])
                    if edge_index not in matching
                )
                cnf.add(*witnesses)

    return cnf, families


def matching_masks(
    families: tuple[tuple[tuple[int, ...], ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(sum(1 << edge_index for edge_index in matching) for matching in family)
        for family in families
    )


def cut_requirements(
    omitted_triples: tuple[tuple[int, ...], ...],
) -> tuple[tuple[tuple[int, ...], tuple[int, ...], int], ...]:
    """Return every nontrivial internal-edge capacity cut."""
    supports = tuple(
        frozenset(VERTICES) - frozenset(triple) for triple in omitted_triples
    )
    requirements = []
    for size in range(len(VERTICES) + 1):
        for vertices in combinations(VERTICES, size):
            vertex_set = frozenset(vertices)
            required = sum(
                max(0, len(support & vertex_set) - len(support) // 2)
                for support in supports
            )
            if not required:
                continue
            internal_edges = tuple(
                edge_index
                for edge_index, edge in enumerate(EDGES)
                if edge[0] in vertex_set and edge[1] in vertex_set
            )
            requirements.append((vertices, internal_edges, required))
    return tuple(requirements)


def violated_cut(
    requirements: tuple[tuple[tuple[int, ...], tuple[int, ...], int], ...],
    deleted_mask: int,
) -> tuple[tuple[int, ...], tuple[int, ...], int] | None:
    """Return one failed capacity cut, or ``None`` if every cut passes."""
    for vertices, internal_edges, required in requirements:
        available = sum(not deleted_mask & (1 << edge) for edge in internal_edges)
        if available < required:
            return vertices, internal_edges, required
    return None


def write_dimacs(path: Path, cnf: Cnf) -> str:
    """Write the exact accumulated CNF and return its SHA-256 digest."""
    path.parent.mkdir(parents=True, exist_ok=True)
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


def available_indices(
    masks: tuple[tuple[int, ...], ...], deleted_mask: int
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(index for index, mask in enumerate(family) if not mask & deleted_mask)
        for family in masks
    )


def disjoint_triples(
    masks: tuple[tuple[int, ...], ...],
    available: tuple[tuple[int, ...], ...],
    limit: int,
) -> Iterable[tuple[int, int, int]]:
    """Yield up to ``limit`` simultaneous triples for the current model."""
    found = 0
    for left in available[0]:
        left_mask = masks[0][left]
        for middle in available[1]:
            union = left_mask | masks[1][middle]
            if left_mask & masks[1][middle]:
                continue
            for right in available[2]:
                if not union & masks[2][right]:
                    yield (left, middle, right)
                    found += 1
                    if found >= limit:
                        return


def solve_orbit(
    orbit_index: int,
    signature: tuple[int, ...],
    omitted_triples: tuple[tuple[int, ...], ...],
    *,
    cut_batch: int,
    full_rows: bool,
    max_rounds: int,
    require_cut_feasible: bool = False,
    static_cut_feasible: bool = False,
    unsat_cnf_dir: Path | None = None,
) -> dict[str, object]:
    start = time.monotonic()
    cnf, families = build_instance(omitted_triples, full_rows=full_rows)
    masks = matching_masks(families)
    cuts = 0
    capacity_cuts = 0
    rounds = 0
    requirements = cut_requirements(omitted_triples)
    enforced_vertex_sets: set[tuple[int, ...]] = set()
    if static_cut_feasible:
        if not require_cut_feasible:
            raise ValueError("static cut feasibility requires cut feasibility")
        for vertices, internal_edges, required in requirements:
            # From d_D(v)<=5 and |D|=27, at most the displayed number of
            # edges can be deleted inside U.  Skip capacity inequalities that
            # are already automatic from these base constraints.
            maximum_deleted = min(
                len(internal_edges),
                5 * len(vertices) // 2,
                sum(PREFIX_SIZES),
            )
            minimum_available = len(internal_edges) - maximum_deleted
            if required <= minimum_available:
                continue
            cnf.cardinality(
                ("cut_feasible", vertices),
                [
                    -cnf.variable(("deleted_edge", edge_index))
                    for edge_index in internal_edges
                ],
                lower=required,
            )
            enforced_vertex_sets.add(vertices)
            capacity_cuts += 1
    initial_clauses = len(cnf.clauses)
    solver = Cadical195(bootstrap_with=cnf.clauses)
    result: dict[str, object]
    try:
        while max_rounds == 0 or rounds < max_rounds:
            rounds += 1
            satisfiable = solver.solve()
            if not satisfiable:
                result = {
                    "status": "unsat",
                    "rounds": rounds,
                    "cuts": cuts,
                }
                break
            model = set(literal for literal in solver.get_model() if literal > 0)
            deleted = tuple(
                edge_index
                for edge_index in range(len(EDGES))
                if cnf.variable(("deleted_edge", edge_index)) in model
            )
            deleted_mask = sum(1 << edge_index for edge_index in deleted)
            available = available_indices(masks, deleted_mask)
            violating = tuple(disjoint_triples(masks, available, cut_batch))
            if not violating:
                failed_cut = (
                    violated_cut(requirements, deleted_mask)
                    if require_cut_feasible
                    else None
                )
                if failed_cut is not None:
                    vertices, internal_edges, required = failed_cut
                    if vertices in enforced_vertex_sets:
                        raise AssertionError("an enforced capacity cut was violated")
                    enforced_vertex_sets.add(vertices)
                    old_clause_count = len(cnf.clauses)
                    cnf.cardinality(
                        ("cut_feasible", vertices),
                        [
                            -cnf.variable(("deleted_edge", edge_index))
                            for edge_index in internal_edges
                        ],
                        lower=required,
                    )
                    for clause in cnf.clauses[old_clause_count:]:
                        solver.add_clause(clause)
                    capacity_cuts += 1
                    continue
                selected_by_colour = []
                for colour in range(len(PREFIX_SIZES)):
                    selected_by_colour.append(
                        [
                            EDGES[edge_index]
                            for edge_index in range(len(EDGES))
                            if cnf.variable(("colour_edge", colour, edge_index)) in model
                        ]
                    )
                result = {
                    "status": "counterexample",
                    "rounds": rounds,
                    "cuts": cuts,
                    "available_counts": [len(indices) for indices in available],
                    "prefix": selected_by_colour,
                    "cut_feasible": require_cut_feasible,
                }
                if full_rows:
                    result["remaining_complements"] = [
                        [
                            vertex
                            for vertex in VERTICES
                            if cnf.variable(("remaining_row", row, vertex)) in model
                        ]
                        for row in range(11)
                    ]
                break
            for left, middle, right in violating:
                clause = (
                    -cnf.variable(("available_matching", 0, left)),
                    -cnf.variable(("available_matching", 1, middle)),
                    -cnf.variable(("available_matching", 2, right)),
                )
                solver.add_clause(clause)
                cnf.add(*clause)
            cuts += len(violating)
        else:
            result = {
                "status": "round-limit",
                "rounds": rounds,
                "cuts": cuts,
            }
    finally:
        solver.delete()

    if result["status"] == "unsat" and unsat_cnf_dir is not None:
        cnf_path = unsat_cnf_dir / f"orbit_{orbit_index}.cnf"
        result["cnf_sha256"] = write_dimacs(cnf_path, cnf)
        result["cnf_path"] = str(cnf_path)

    result.update(
        {
            "orbit": orbit_index,
            "signature": signature,
            "omitted_triples": omitted_triples,
            "variables": cnf.top,
            "initial_clauses": initial_clauses,
            "final_clauses": len(cnf.clauses),
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "full_rows": full_rows,
            "require_cut_feasible": require_cut_feasible,
            "static_cut_feasible": static_cut_feasible,
            "capacity_cuts": capacity_cuts,
        }
    )
    return result


def parse_orbits(specification: str, count: int) -> tuple[int, ...]:
    if specification == "all":
        return tuple(range(count))
    result = tuple(int(part) for part in specification.split(","))
    if any(index < 0 or index >= count for index in result):
        raise ValueError(f"orbit index must lie in 0..{count - 1}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", default="all")
    parser.add_argument("--cut-batch", type=int, default=10_000)
    parser.add_argument(
        "--relaxed-prefix-only",
        action="store_true",
        help="omit the exact eleven-row class-B completion constraints",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=0,
        help="zero means no round limit",
    )
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument(
        "--unsat-cnf-dir",
        type=Path,
        help="freeze the exact accumulated DIMACS CNF for every UNSAT orbit",
    )
    parser.add_argument(
        "--require-cut-feasible",
        action="store_true",
        help=(
            "search only for bad triples satisfying every internal-edge "
            "capacity cut"
        ),
    )
    parser.add_argument(
        "--static-cut-feasible",
        action="store_true",
        help=(
            "install every potentially binding capacity cut before solving; "
            "requires --require-cut-feasible"
        ),
    )
    args = parser.parse_args()
    if args.static_cut_feasible and not args.require_cut_feasible:
        parser.error("--static-cut-feasible requires --require-cut-feasible")

    orbits = support_orbits()
    print(f"support_orbits={len(orbits)}", flush=True)
    selected = parse_orbits(args.orbits, len(orbits))
    output = args.jsonl.open("a", encoding="utf-8") if args.jsonl else None
    try:
        for orbit_index in selected:
            signature, representative = orbits[orbit_index]
            result = solve_orbit(
                orbit_index,
                signature,
                representative,
                cut_batch=args.cut_batch,
                full_rows=not args.relaxed_prefix_only,
                max_rounds=args.max_rounds,
                require_cut_feasible=args.require_cut_feasible,
                static_cut_feasible=args.static_cut_feasible,
                unsat_cnf_dir=args.unsat_cnf_dir,
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
