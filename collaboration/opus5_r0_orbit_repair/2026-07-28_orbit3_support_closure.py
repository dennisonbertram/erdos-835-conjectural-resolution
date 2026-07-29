#!/usr/bin/env python3
"""Orbit-3 support-level prescribed-colour closure.

Selected omitted triples:

    R1 = 012, R2 = 014, R3 = 234.

The first two supports are pairwise compatible under the audited pair
theorem.  Their two fixed matchings form an alternating terminal path plus
even cycles.  A distinguished common vertex (3) is absent from the third
support.  Up to the exact support stabilizer, there are 16 pair types.

For each type this script asks whether a deleted graph can satisfy a sound
relaxation of the full source model and block every third matching.  UNSAT
proves extension for that type.  SAT is only a relaxed obstruction candidate.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations
from pathlib import Path

from pysat.solvers import Cadical195


VERTICES = tuple(range(13))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ROWS = (
    frozenset((0, 1, 2)),
    frozenset((0, 1, 4)),
    frozenset((2, 3, 4)),
)
SUPPORTS = tuple(frozenset(VERTICES) - row for row in ROWS)

END_LEFT = 4
END_RIGHT = 2
DISTINGUISHED = 3
ORDINARY = tuple(range(5, 13))


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


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def structural_vertices(distinguished_position: int) -> tuple[int, ...]:
    """Place vertex 3 at one structural W-position and fill the other eight."""
    result = []
    ordinary = iter(ORDINARY)
    for position in range(9):
        result.append(
            DISTINGUISHED
            if position == distinguished_position
            else next(ordinary)
        )
    return tuple(result)


def base_pair(
    shape: str,
    distinguished_position: int,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    """Return the two canonical matchings for one shape and X-position."""
    w = structural_vertices(distinguished_position)
    left = (
        edge(END_LEFT, w[0]),
        edge(w[1], w[2]),
        edge(w[3], w[4]),
        edge(w[5], w[6]),
        edge(w[7], w[8]),
    )
    right_by_shape = {
        "P10": (
            edge(w[0], w[1]),
            edge(w[2], w[3]),
            edge(w[4], w[5]),
            edge(w[6], w[7]),
            edge(w[8], END_RIGHT),
        ),
        "P6_C4": (
            edge(w[0], w[1]),
            edge(w[2], w[3]),
            edge(w[4], END_RIGHT),
            edge(w[6], w[7]),
            edge(w[8], w[5]),
        ),
        "P4_C6": (
            edge(w[0], w[1]),
            edge(w[2], END_RIGHT),
            edge(w[4], w[5]),
            edge(w[6], w[7]),
            edge(w[8], w[3]),
        ),
        "P2_C8": (
            edge(w[0], END_RIGHT),
            edge(w[2], w[3]),
            edge(w[4], w[5]),
            edge(w[6], w[7]),
            edge(w[8], w[1]),
        ),
        "P2_C4_C4": (
            edge(w[0], END_RIGHT),
            edge(w[2], w[3]),
            edge(w[4], w[1]),
            edge(w[6], w[7]),
            edge(w[8], w[5]),
        ),
    }
    return tuple(sorted(left)), tuple(sorted(right_by_shape[shape]))


def pair_invariant(
    pair: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
) -> tuple[object, ...]:
    """Complete orbit invariant under ordinary-core permutations and pair swap."""
    graph = {vertex: set() for vertex in (END_LEFT, END_RIGHT, DISTINGUISHED, *ORDINARY)}
    for matching in pair:
        for left, right in matching:
            graph[left].add(right)
            graph[right].add(left)

    unseen = set(graph)
    components = []
    while unseen:
        start = min(unseen)
        seen = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour in graph[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        components.append(frozenset(seen))
        unseen -= seen

    path = next(component for component in components if END_LEFT in component)
    assert END_RIGHT in path
    cycles = tuple(sorted(len(component) for component in components if component != path))

    def distance(start: int, target: int) -> int:
        frontier = {start}
        seen = {start}
        result = 0
        while target not in frontier:
            result += 1
            frontier = {
                neighbour
                for vertex in frontier
                for neighbour in graph[vertex]
                if neighbour not in seen
            }
            seen.update(frontier)
        return result

    containing = next(component for component in components if DISTINGUISHED in component)
    if containing == path:
        location = (
            "path",
            tuple(
                sorted(
                    (
                        distance(DISTINGUISHED, END_LEFT),
                        distance(DISTINGUISHED, END_RIGHT),
                    )
                )
            ),
        )
    else:
        location = ("cycle", len(containing))
    return (len(path) - 1, cycles, location)


SELECTED_POSITIONS = {
    "P10": (0, 1, 2, 3, 4),
    "P6_C4": (0, 1, 2, 5),
    "P4_C6": (0, 1, 3),
    "P2_C8": (0, 1),
    "P2_C4_C4": (0, 1),
}
PAIR_TYPES = {
    f"{shape}_X{position}": base_pair(shape, position)
    for shape, positions in SELECTED_POSITIONS.items()
    for position in positions
}


def audit_pair_orbits() -> None:
    """Check that the 16 selected representatives cover all 45 placements."""
    shapes = tuple(SELECTED_POSITIONS)
    all_invariants = {
        pair_invariant(base_pair(shape, position))
        for shape in shapes
        for position in range(9)
    }
    selected_invariants = {pair_invariant(pair) for pair in PAIR_TYPES.values()}
    assert len(PAIR_TYPES) == len(selected_invariants) == 16
    assert selected_invariants == all_invariants

    for left, right in PAIR_TYPES.values():
        assert len(left) == len(right) == 5
        assert set(left).isdisjoint(right)
        assert {
            vertex for endpoints in left for vertex in endpoints
        } == set(SUPPORTS[0])
        assert {
            vertex for endpoints in right for vertex in endpoints
        } == set(SUPPORTS[1])


def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
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


THIRD_MATCHINGS = perfect_matchings(tuple(sorted(SUPPORTS[2])))
FAMILIES = tuple(
    perfect_matchings(tuple(sorted(support))) for support in SUPPORTS
)
MATCHING_MASKS = tuple(
    tuple(sum(1 << index for index in matching) for matching in family)
    for family in FAMILIES
)


def cut_requirements() -> tuple[tuple[tuple[int, ...], tuple[int, ...], int], ...]:
    """Return every capacity cut not automatic from the degree cap."""
    requirements = []
    for size in (6, 7, 8):
        for vertices in combinations(VERTICES, size):
            vertex_set = frozenset(vertices)
            required = sum(
                max(0, len(support & vertex_set) - 5)
                for support in SUPPORTS
            )
            internal_edges = tuple(
                index
                for index, endpoints in enumerate(EDGES)
                if endpoints[0] in vertex_set and endpoints[1] in vertex_set
            )
            upper_deleted = len(internal_edges) - required
            maximum_deleted = min(
                len(internal_edges),
                5 * size // 2,
                27,
            )
            if upper_deleted < maximum_deleted:
                requirements.append((vertices, internal_edges, upper_deleted))
    return tuple(requirements)


CUT_REQUIREMENTS = cut_requirements()


def build_instance(
    pair_type: str,
) -> tuple[Cnf, tuple[tuple[int, ...], ...]]:
    cnf = Cnf()

    def deleted(edge_index: int) -> int:
        return cnf.variable(("deleted", edge_index))

    fixed_edges = frozenset(
        EDGE_INDEX[endpoints]
        for matching in PAIR_TYPES[pair_type]
        for endpoints in matching
    )
    assert len(fixed_edges) == 10
    for edge_index in fixed_edges:
        cnf.add(-deleted(edge_index))

    cnf.cardinality(
        ("deleted_total",),
        [deleted(index) for index in range(len(EDGES))],
        lower=27,
        upper=27,
    )

    selected_multiplicity = tuple(
        sum(vertex in row for row in ROWS) for vertex in VERTICES
    )
    for vertex in VERTICES:
        incident = [
            deleted(index)
            for index, endpoints in enumerate(EDGES)
            if vertex in endpoints
        ]
        cnf.cardinality(
            ("deleted_degree", vertex),
            incident,
            lower=selected_multiplicity[vertex] + 1,
            upper=5,
        )

    for vertices, internal_edges, upper_deleted in CUT_REQUIREMENTS:
        cnf.cardinality(
            ("capacity_cut", vertices),
            [deleted(index) for index in internal_edges],
            upper=upper_deleted,
        )

    possible_thirds = tuple(
        matching
        for matching in THIRD_MATCHINGS
        if fixed_edges.isdisjoint(matching)
    )
    for matching in possible_thirds:
        cnf.add(*(deleted(index) for index in matching))
    return cnf, possible_thirds


def deleted_set(cnf: Cnf, model: set[int]) -> frozenset[int]:
    return frozenset(
        index
        for index in range(len(EDGES))
        if cnf.variable(("deleted", index)) in model
    )


def verify_relaxed_model(
    pair_type: str,
    possible_thirds: tuple[tuple[int, ...], ...],
    deleted: frozenset[int],
) -> None:
    assert len(deleted) == 27
    selected_multiplicity = tuple(
        sum(vertex in row for row in ROWS) for vertex in VERTICES
    )
    for vertex in VERTICES:
        degree = sum(
            index in deleted
            for index, endpoints in enumerate(EDGES)
            if vertex in endpoints
        )
        assert selected_multiplicity[vertex] + 1 <= degree <= 5

    fixed_edges = frozenset(
        EDGE_INDEX[endpoints]
        for matching in PAIR_TYPES[pair_type]
        for endpoints in matching
    )
    assert deleted.isdisjoint(fixed_edges)
    for vertices, internal_edges, upper_deleted in CUT_REQUIREMENTS:
        assert sum(index in deleted for index in internal_edges) <= upper_deleted, vertices
    assert all(not deleted.isdisjoint(matching) for matching in possible_thirds)


def write_dimacs(path: Path, cnf: Cnf) -> str:
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


def available_indices(deleted_mask: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            index
            for index, matching_mask in enumerate(family)
            if not matching_mask & deleted_mask
        )
        for family in MATCHING_MASKS
    )


def disjoint_triple_unions(
    available: tuple[tuple[int, ...], ...],
    limit: int,
) -> tuple[tuple[int, ...], ...]:
    unions = set()
    for left in available[0]:
        left_mask = MATCHING_MASKS[0][left]
        for middle in available[1]:
            middle_mask = MATCHING_MASKS[1][middle]
            if left_mask & middle_mask:
                continue
            union = left_mask | middle_mask
            for right in available[2]:
                right_mask = MATCHING_MASKS[2][right]
                if union & right_mask:
                    continue
                full_union = union | right_mask
                unions.add(
                    tuple(
                        index
                        for index in range(len(EDGES))
                        if full_union & (1 << index)
                    )
                )
                if len(unions) >= limit:
                    return tuple(sorted(unions))
    return tuple(sorted(unions))


def solve_type(
    pair_type: str,
    output_dir: Path,
    cut_batch: int,
    max_rounds: int,
) -> dict[str, object]:
    cnf, possible_thirds = build_instance(pair_type)
    rounds = 0
    global_clauses = 0
    with Cadical195(bootstrap_with=cnf.clauses) as solver:
        while max_rounds == 0 or rounds < max_rounds:
            rounds += 1
            if not solver.solve():
                output_dir.mkdir(exist_ok=True)
                path = output_dir / f"{pair_type}.cnf"
                digest = write_dimacs(path, cnf)
                return {
                    "status": "unsat",
                    "pair_type": pair_type,
                    "rounds": rounds,
                    "variables": cnf.top,
                    "clauses": len(cnf.clauses),
                    "global_clauses": global_clauses,
                    "cuts": len(CUT_REQUIREMENTS),
                    "possible_thirds": len(possible_thirds),
                    "cnf": str(path),
                    "sha256": digest,
                }

            model = {literal for literal in solver.get_model() if literal > 0}
            deleted = deleted_set(cnf, model)
            verify_relaxed_model(pair_type, possible_thirds, deleted)
            deleted_mask = sum(1 << index for index in deleted)
            violating = disjoint_triple_unions(
                available_indices(deleted_mask),
                cut_batch,
            )
            if not violating:
                return {
                    "status": "sat_counterexample",
                    "pair_type": pair_type,
                    "rounds": rounds,
                    "variables": cnf.top,
                    "clauses": len(cnf.clauses),
                    "global_clauses": global_clauses,
                    "cuts": len(CUT_REQUIREMENTS),
                    "possible_thirds": len(possible_thirds),
                    "deleted": tuple(EDGES[index] for index in sorted(deleted)),
                }
            for union in violating:
                clause = tuple(cnf.variable(("deleted", index)) for index in union)
                cnf.add(*clause)
                solver.add_clause(clause)
            global_clauses += len(violating)
    return {
        "status": "round_limit",
        "pair_type": pair_type,
        "rounds": rounds,
        "variables": cnf.top,
        "clauses": len(cnf.clauses),
        "global_clauses": global_clauses,
        "cuts": len(CUT_REQUIREMENTS),
        "possible_thirds": len(possible_thirds),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--types",
        nargs="*",
        choices=tuple(PAIR_TYPES),
        default=tuple(PAIR_TYPES),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).with_name("2026-07-28_orbit3_support_closure_cnf"),
    )
    parser.add_argument("--cut-batch", type=int, default=10_000)
    parser.add_argument("--max-rounds", type=int, default=0)
    args = parser.parse_args()
    if args.cut_batch <= 0:
        parser.error("--cut-batch must be positive")
    if args.max_rounds < 0:
        parser.error("--max-rounds must be nonnegative")
    audit_pair_orbits()
    print(
        {
            "pair_orbits": len(PAIR_TYPES),
            "capacity_cuts": len(CUT_REQUIREMENTS),
            "third_matchings": len(THIRD_MATCHINGS),
        },
        flush=True,
    )
    for pair_type in args.types:
        print(
            solve_type(
                pair_type,
                args.output_dir,
                args.cut_batch,
                args.max_rounds,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
