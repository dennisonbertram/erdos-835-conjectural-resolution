#!/usr/bin/env python3
"""Generate the six symmetry-reduced CNFs for the r=1 pair gate.

The generator is dependency-free.  Its only output is ordinary DIMACS CNF;
CaDiCaL and DRAT-trim are used separately to solve and certify the instances.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path


VERTICES = tuple(range(13))
EDGES = tuple(combinations(VERTICES, 2))
T0 = frozenset((10, 11, 12))
Y0 = frozenset(VERTICES) - T0
CASES = ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (3, 0))


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[frozenset, ...]:
    if not vertices:
        return (frozenset(),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(rest):
            result.append(frozenset((edge, *tail)))
    return tuple(result)


def support_pair(overlap: int) -> tuple[frozenset, frozenset]:
    common = tuple(sorted(T0))[:overlap]
    target_only = tuple(range(7, 10))[: 3 - overlap]
    t1 = frozenset((*common, *target_only))
    return Y0, frozenset(VERTICES) - t1


def canonical_matching(overlap: int, aa_edges: int) -> frozenset:
    _, y1 = support_pair(overlap)
    a = sorted(Y0 - y1)
    c = sorted(Y0 & y1)
    result = []
    for _ in range(aa_edges):
        result.append(tuple(sorted((a.pop(0), a.pop(0)))))
    while a:
        result.append(tuple(sorted((a.pop(0), c.pop(0)))))
    while c:
        result.append(tuple(sorted((c.pop(0), c.pop(0)))))
    return frozenset(result)


class Cnf:
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
        """Encode lower <= sum(literals) <= upper by an exact unary counter."""
        n = len(literals)
        if lower is not None and not 0 <= lower <= n:
            raise ValueError("invalid lower bound")
        if upper is not None and not 0 <= upper <= n:
            raise ValueError("invalid upper bound")
        if lower is not None and upper is not None and lower > upper:
            raise ValueError("inconsistent bounds")

        largest = 0
        if lower:
            largest = max(largest, lower)
        if upper is not None and upper < n:
            largest = max(largest, upper + 1)
        if not largest:
            return

        def state(prefix: int, count: int) -> int:
            if count == 0:
                return self.true
            if prefix == 0 or count > prefix:
                return self.false
            return self.variable(("counter", tag, prefix, count))

        # s(i,j) <-> [at least j of the first i literals are true].
        for prefix, literal in enumerate(literals, start=1):
            for count in range(1, min(prefix, largest) + 1):
                current = state(prefix, count)
                old_same = state(prefix - 1, count)
                old_previous = state(prefix - 1, count - 1)
                # current <-> old_same OR (old_previous AND literal)
                self.add(-old_same, current)
                self.add(-old_previous, -literal, current)
                self.add(-current, old_same, old_previous)
                self.add(-current, old_same, literal)

        if lower:
            self.add(state(n, lower))
        if upper is not None and upper < n:
            self.add(-state(n, upper + 1))

    def write(self, path: Path, comments: list[str]) -> None:
        with path.open("w", encoding="ascii", newline="\n") as stream:
            for comment in comments:
                stream.write(f"c {comment}\n")
            stream.write(f"p cnf {self.top} {len(self.clauses)}\n")
            for clause in self.clauses:
                stream.write(" ".join(map(str, clause)))
                stream.write(" 0\n")


def build_case(overlap: int, aa_edges: int) -> tuple[Cnf, dict[str, object]]:
    if (overlap, aa_edges) not in CASES:
        raise ValueError(f"not one of the six orbit cases: {(overlap, aa_edges)}")

    y0, y1 = support_pair(overlap)
    families = (
        perfect_matchings(tuple(sorted(y0))),
        perfect_matchings(tuple(sorted(y1))),
    )
    fixed = canonical_matching(overlap, aa_edges)
    fixed_index = families[0].index(fixed)
    cnf = Cnf()

    def x(colour: int, edge: tuple[int, int]) -> int:
        return cnf.variable(("colour_edge", colour, edge))

    def deleted(edge: tuple[int, int]) -> int:
        return cnf.variable(("deleted_edge", edge))

    def available(side: int, index: int) -> int:
        return cnf.variable(("available_matching", side, index))

    # D is the edge-disjoint union of four 4-matchings and two 5-matchings.
    for colour, size in enumerate((4, 4, 4, 4, 5, 5)):
        colour_edges = [x(colour, edge) for edge in EDGES]
        cnf.cardinality(
            ("colour_size", colour),
            colour_edges,
            lower=size,
            upper=size,
        )
        for vertex in VERTICES:
            cnf.cardinality(
                ("colour_vertex", colour, vertex),
                [x(colour, edge) for edge in EDGES if vertex in edge],
                upper=1,
            )

    # Different colours do not reuse an edge, and deleted(edge) is their union.
    for edge in EDGES:
        colours = [x(colour, edge) for colour in range(6)]
        cnf.cardinality(("edge_colour", edge), colours, upper=1)
        for literal in colours:
            cnf.add(-literal, deleted(edge))
        cnf.add(-deleted(edge), *colours)

    # Every vertex is covered, but no vertex occurs in all six prefix matchings.
    for vertex in VERTICES:
        cnf.cardinality(
            ("deleted_degree", vertex),
            [deleted(edge) for edge in EDGES if vertex in edge],
            lower=1,
            upper=5,
        )

    # A matching-availability variable is true exactly when none of its edges
    # belongs to D.
    for side, family in enumerate(families):
        for index, matching in enumerate(family):
            literal = available(side, index)
            matching_deletions = [deleted(edge) for edge in sorted(matching)]
            for edge_literal in matching_deletions:
                cnf.add(-literal, -edge_literal)
            cnf.add(literal, *matching_deletions)

    # The fixed orbit representative is available; the other support has some
    # available perfect matching.
    cnf.add(available(0, fixed_index))
    cnf.add(*(available(1, index) for index in range(len(families[1]))))

    # Negate the desired conclusion: no available pair is edge-disjoint.
    disjoint_pairs = 0
    for left_index, left in enumerate(families[0]):
        for right_index, right in enumerate(families[1]):
            if left.isdisjoint(right):
                disjoint_pairs += 1
                cnf.add(
                    -available(0, left_index),
                    -available(1, right_index),
                )

    # Also negate the alternative conclusion: no common-support edge is
    # forced in every available matching on both sides.
    common_support = y0 & y1
    for edge in combinations(sorted(common_support), 2):
        witnesses = []
        for side, family in enumerate(families):
            witnesses.extend(
                available(side, index)
                for index, matching in enumerate(family)
                if edge not in matching
            )
        cnf.add(*witnesses)

    metadata = {
        "overlap": overlap,
        "aa_edges": aa_edges,
        "fixed_matching": sorted(fixed),
        "variables": cnf.top,
        "clauses": len(cnf.clauses),
        "disjoint_pairs": disjoint_pairs,
        "perfect_matchings_per_side": len(families[0]),
    }
    return cnf, metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overlap", type=int, choices=range(4), required=True)
    parser.add_argument("--aa-edges", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cnf, metadata = build_case(args.overlap, args.aa_edges)
    cnf.write(
        args.output,
        [
            "r=1 cross-family gate, negated",
            f"overlap={args.overlap} aa_edges={args.aa_edges}",
            f"fixed_matching={metadata['fixed_matching']}",
        ],
    )
    print(
        " ".join(f"{key}={value}" for key, value in metadata.items()),
        flush=True,
    )


if __name__ == "__main__":
    main()
