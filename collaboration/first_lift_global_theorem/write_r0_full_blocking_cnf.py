"""Write an exact CNF for a totally blocked exceptional seven-prefix.

The variables describe seven edge-disjoint matchings on K_13 (four of
size four and three of size five), their 31-edge union F, the seven
remaining three-point complements, and the three remaining five-point
complements.  The row identity is

    number of remaining complements containing v = degree_F(v) - 2.

For every chosen three-point complement C and every perfect matching M of
V\\C, the CNF requires M to meet F.  Thus SAT is exactly a counterexample
to the proposed eighth-matching lemma, while a checked UNSAT proof proves
that lemma for the exceptional r=0 profile.

This is an exploratory full model.  It deliberately does not encode Tutte
core types, so its correctness does not depend on the core catalogue.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


N = 13
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRIPLES = tuple(combinations(VERTICES, 3))


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:index] + vertices[index + 1 :]
        edge = EDGE_INDEX[tuple(sorted((first, second)))]
        for tail in perfect_matchings(rest):
            answer.append((edge, *tail))
    return tuple(answer)


class Writer:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.body_path = path.with_suffix(path.suffix + ".body")
        self.handle = self.body_path.open("w", encoding="ascii")
        self.clauses = 0

    def add(self, clause: list[int] | tuple[int, ...]) -> None:
        self.handle.write(" ".join(map(str, clause)))
        self.handle.write(" 0\n")
        self.clauses += 1

    def add_cardinality(
        self,
        literals: list[int],
        bound: int,
        kind: str,
        pool: IDPool,
        gate: int | None = None,
    ) -> None:
        if kind == "equals":
            encoded = CardEnc.equals(
                lits=literals,
                bound=bound,
                vpool=pool,
                encoding=EncType.seqcounter,
            )
        elif kind == "atmost":
            encoded = CardEnc.atmost(
                lits=literals,
                bound=bound,
                vpool=pool,
                encoding=EncType.seqcounter,
            )
        else:
            raise ValueError(kind)
        prefix = [] if gate is None else [-gate]
        for clause in encoded.clauses:
            self.add([*prefix, *clause])

    def finish(self, variables: int) -> None:
        self.handle.close()
        with self.path.open("w", encoding="ascii") as output:
            output.write(f"p cnf {variables} {self.clauses}\n")
            with self.body_path.open("r", encoding="ascii") as body:
                while chunk := body.read(1024 * 1024):
                    output.write(chunk)
        self.body_path.unlink()


def build(path: Path) -> None:
    pool = IDPool()
    writer = Writer(path)

    f = [pool.id(("f", edge)) for edge in range(len(EDGES))]
    x = [
        [pool.id(("x", colour, edge)) for edge in range(len(EDGES))]
        for colour in range(7)
    ]
    triple_choice = [
        [pool.id(("triple", row, index)) for index in range(len(TRIPLES))]
        for row in range(7)
    ]
    five = [
        [pool.id(("five", row, vertex)) for vertex in VERTICES]
        for row in range(3)
    ]
    degree_state = [
        {degree: pool.id(("degree", vertex, degree)) for degree in range(2, 8)}
        for vertex in VERTICES
    ]

    incident = [
        [index for index, edge in enumerate(EDGES) if vertex in edge]
        for vertex in VERTICES
    ]

    # The seven selected colours are edge-disjoint matchings of sizes
    # 4,4,4,4,5,5,5, and f is their union.
    for colour in range(7):
        writer.add_cardinality(
            x[colour],
            4 if colour < 4 else 5,
            "equals",
            pool,
        )
        for vertex in VERTICES:
            writer.add_cardinality(
                [x[colour][edge] for edge in incident[vertex]],
                1,
                "atmost",
                pool,
            )
    for edge in range(len(EDGES)):
        writer.add_cardinality(
            [x[colour][edge] for colour in range(7)],
            1,
            "atmost",
            pool,
        )
        for colour in range(7):
            writer.add([-x[colour][edge], f[edge]])
        writer.add([-f[edge], *[x[colour][edge] for colour in range(7)]])

    # Relabel K_13 so the first size-four matching is canonical.
    canonical = {
        EDGE_INDEX[(0, 1)],
        EDGE_INDEX[(2, 3)],
        EDGE_INDEX[(4, 5)],
        EDGE_INDEX[(6, 7)],
    }
    for edge in range(len(EDGES)):
        writer.add([x[0][edge] if edge in canonical else -x[0][edge]])

    # Each remaining ten-support has exactly one complement triple.  Sort the
    # seven one-hot choices to remove their S_7 row symmetry.
    for row in range(7):
        writer.add_cardinality(triple_choice[row], 1, "equals", pool)
    for row in range(6):
        for left in range(len(TRIPLES)):
            for right in range(left):
                writer.add(
                    [-triple_choice[row][left], -triple_choice[row + 1][right]]
                )

    # The three remaining size-eight supports have five-point complements.
    for row in range(3):
        writer.add_cardinality(five[row], 5, "equals", pool)

    # Conditional degree and complement-row equations.  A selected triple
    # contributes to a vertex exactly when its one-hot choice contains it.
    for vertex in VERTICES:
        writer.add_cardinality(
            list(degree_state[vertex].values()),
            1,
            "equals",
            pool,
        )
        containing_choices = [
            triple_choice[row][index]
            for row in range(7)
            for index, triple in enumerate(TRIPLES)
            if vertex in triple
        ]
        omissions = [
            *containing_choices,
            *[five[row][vertex] for row in range(3)],
        ]
        for degree, state in degree_state[vertex].items():
            writer.add_cardinality(
                [f[edge] for edge in incident[vertex]],
                degree,
                "equals",
                pool,
                gate=state,
            )
            writer.add_cardinality(
                omissions,
                degree - 2,
                "equals",
                pool,
                gate=state,
            )

    # Total blocking: every perfect matching of the ten-support contains an
    # already selected edge of F.
    for row in range(7):
        for triple_index, triple in enumerate(TRIPLES):
            support = tuple(vertex for vertex in VERTICES if vertex not in triple)
            choice = triple_choice[row][triple_index]
            for matching in perfect_matchings(support):
                writer.add([-choice, *[f[edge] for edge in matching]])

    writer.finish(pool.top)
    print(
        f"WROTE {path} variables={pool.top} clauses={writer.clauses}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
