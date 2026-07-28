#!/usr/bin/env python3
"""Generate the local CNF which negates the r=1 K7 WW switch lemma."""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path


V = tuple(range(13))
U = tuple(range(7))
W = tuple(range(7, 13))
S = tuple(range(7, 12))
EDGES = tuple(combinations(V, 2))
CORE_EDGES = tuple(combinations(U, 2))
WW_EDGES = tuple(combinations(W, 2))


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
            self.add(state(n, lower))
        if upper is not None and upper < n:
            self.add(-state(n, upper + 1))

    def text(self) -> str:
        comments = (
            "local K7 WW-switch lemma, negated",
            "U=0..6 W=7..12 S=7..11",
            "D has maximum degree five; M0 and M1 are disjoint five-edge matchings",
        )
        lines = [*(f"c {comment}" for comment in comments)]
        lines.append(f"p cnf {self.top} {len(self.clauses)}")
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return "\n".join(lines) + "\n"


def build() -> Cnf:
    cnf = Cnf()

    def d(edge):
        return cnf.variable(("D", edge))

    def m(colour, edge):
        return cnf.variable(("M", colour, edge))

    def selected(edge):
        return cnf.variable(("selected", edge))

    def bad(core_edge, separator_vertex):
        return cnf.variable(("bad", core_edge, separator_vertex))

    def good(core_edge):
        return cnf.variable(("good", core_edge))

    # Each old colour is a five-edge matching, hence a perfect matching on
    # the complement of the three vertices it misses.
    for colour in range(2):
        cnf.cardinality(
            ("matching_size", colour),
            [m(colour, edge) for edge in EDGES],
            lower=5,
            upper=5,
        )
        for vertex in V:
            cnf.cardinality(
                ("matching_vertex", colour, vertex),
                [m(colour, edge) for edge in EDGES if vertex in edge],
                upper=1,
            )

    # Only the local prefix fact Delta(D)<=5 is retained.
    for vertex in V:
        cnf.cardinality(
            ("D_degree", vertex),
            [d(edge) for edge in EDGES if vertex in edge],
            upper=5,
        )

    # D, M0, M1 are edge-disjoint, and selected is exactly their union.
    for edge in EDGES:
        literals = [d(edge), m(0, edge), m(1, edge)]
        cnf.cardinality(("edge_disjoint", edge), literals, upper=1)
        for literal in literals:
            cnf.add(-literal, selected(edge))
        cnf.add(-selected(edge), *literals)

    # The terminal core is saturated.
    for edge in CORE_EDGES:
        cnf.add(selected(edge))

    # Exclude the all-bad equality A_s=U.  The all-bad case has a separate
    # direct construction.
    for separator_vertex in S:
        cnf.cardinality(
            ("proper_star", separator_vertex),
            [
                selected(tuple(sorted((u, separator_vertex))))
                for u in U
            ],
            upper=6,
        )

    # At least one old colour owns an edge entirely in W.
    cnf.add(*(m(colour, edge) for colour in range(2) for edge in WW_EDGES))

    # bad(e,s) iff all five vertices of U-V(e) miss s in the residual
    # bipartite graph.  good(e) iff no s witnesses this Hall obstruction.
    for core_edge in CORE_EDGES:
        bad_literals = []
        for separator_vertex in S:
            literal = bad(core_edge, separator_vertex)
            bad_literals.append(literal)
            required = [
                selected(tuple(sorted((u, separator_vertex))))
                for u in U
                if u not in core_edge
            ]
            for required_literal in required:
                cnf.add(-literal, required_literal)
            cnf.add(literal, *(-required_literal for required_literal in required))

        good_literal = good(core_edge)
        for bad_literal in bad_literals:
            cnf.add(-good_literal, -bad_literal)
        cnf.add(good_literal, *bad_literals)

    # Negate every good two-switch.  If colour i owns uv and pq and uv is
    # Hall-good, then each orientation must consume a selected cross edge.
    for colour in range(2):
        for core_edge in CORE_EDGES:
            u, v = core_edge
            for ww_edge in WW_EDGES:
                p, q = ww_edge
                for first, second in ((p, q), (q, p)):
                    cnf.add(
                        -m(colour, core_edge),
                        -m(colour, ww_edge),
                        -good(core_edge),
                        selected(tuple(sorted((u, first)))),
                        selected(tuple(sorted((v, second)))),
                    )

    return cnf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cnf = build()
    args.output.write_text(cnf.text(), encoding="ascii")
    print("variables", cnf.top, "clauses", len(cnf.clauses))


if __name__ == "__main__":
    main()
