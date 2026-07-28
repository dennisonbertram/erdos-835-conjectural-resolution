"""Write a compact exact CNF for a totally blocked exceptional seven-prefix.

This is an independent encoding of the same mathematical search as
``write_r0_full_blocking_cnf.py``.  The main simplification is to represent
each remaining complement directly by its thirteen membership bits.  For a
vertex v the residual row identity

    omissions(v) = degree_F(v) - 2

is encoded as the single positive-literal cardinality equation

    omissions(v) + unused_incident_edges(v) = 10.

For a complement triple T, exact cardinality three means that the three
membership literals indexed by T are simultaneously true exactly when that
row equals T.  This lets every perfect-matching blocking clause be gated by
those three literals without 286 one-hot choice variables per row.

SAT is exactly a seven-matching prefix that blocks all seven remaining
size-ten supports.  A replay-checked UNSAT proof establishes the exceptional
r=0 eighth-matching lemma.  No Tutte-core catalogue is assumed.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path


N = 13
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRIPLES = tuple(combinations(VERTICES, 3))


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Return all perfect matchings as tuples of global K_13 edge indices."""
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        edge = EDGE_INDEX[tuple(sorted((first, second)))]
        for tail in perfect_matchings(rest):
            result.append((edge, *tail))
    return tuple(result)


class Writer:
    """Streaming DIMACS writer with a small auditable cardinality encoding."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.body_path = path.with_suffix(path.suffix + ".body")
        self.handle = self.body_path.open("w", encoding="ascii")
        self.variables = 0
        self.clauses = 0

    def variable(self) -> int:
        self.variables += 1
        return self.variables

    def variables_block(self, count: int) -> list[int]:
        return [self.variable() for _ in range(count)]

    def add(self, clause: list[int] | tuple[int, ...]) -> None:
        self.handle.write(" ".join(map(str, clause)))
        self.handle.write(" 0\n")
        self.clauses += 1

    def exactly_one(self, literals: list[int]) -> None:
        self.add(literals)
        for left, right in combinations(literals, 2):
            self.add([-left, -right])

    def at_most_one(self, literals: list[int]) -> None:
        for left, right in combinations(literals, 2):
            self.add([-left, -right])

    def exactly(self, literals: list[int], target: int) -> None:
        """Encode an exact count using a deterministic unary-state automaton.

        State s[i,j] means that exactly j of the first i signed literals are
        true.  Every layer is one-hot.  The transition clauses force the next
        state for both truth values of the next literal; trying to increment
        past ``target`` is forbidden.  Finally s[n,target] is asserted.
        """
        if not 0 <= target <= len(literals):
            self.add([])
            return

        states = [
            self.variables_block(target + 1)
            for _ in range(len(literals) + 1)
        ]
        self.add([states[0][0]])
        for count in range(1, target + 1):
            self.add([-states[0][count]])

        for index, literal in enumerate(literals, start=1):
            current = states[index]
            previous = states[index - 1]
            self.exactly_one(current)
            for count, previous_state in enumerate(previous):
                # If the literal is false, the count is unchanged.
                self.add([-previous_state, literal, current[count]])
                # If the literal is true, the count increases by one.
                if count < target:
                    self.add(
                        [-previous_state, -literal, current[count + 1]]
                    )
                else:
                    self.add([-previous_state, -literal])

        self.add([states[-1][target]])

    def lex_not_greater(self, left: list[int], right: list[int]) -> None:
        """Encode the bit-vector relation left <=_lex right."""
        if len(left) != len(right):
            raise ValueError("lexicographic vectors must have equal length")

        prefix_equal = self.variable()
        self.add([prefix_equal])
        for left_bit, right_bit in zip(reversed(left), reversed(right)):
            # Under an equal higher prefix, 1 > 0 is forbidden.
            self.add([-prefix_equal, -left_bit, right_bit])

            next_equal = self.variable()
            # next_equal iff prefix_equal and the current bits are equal.
            self.add([-next_equal, prefix_equal])
            self.add([-next_equal, -left_bit, right_bit])
            self.add([-next_equal, left_bit, -right_bit])
            self.add(
                [-prefix_equal, -left_bit, -right_bit, next_equal]
            )
            self.add(
                [-prefix_equal, left_bit, right_bit, next_equal]
            )
            prefix_equal = next_equal

    def finish(self) -> None:
        self.handle.close()
        with self.path.open("w", encoding="ascii") as output:
            output.write(f"p cnf {self.variables} {self.clauses}\n")
            with self.body_path.open("r", encoding="ascii") as body:
                while chunk := body.read(1024 * 1024):
                    output.write(chunk)
        self.body_path.unlink()


def build(path: Path) -> None:
    writer = Writer(path)

    f = writer.variables_block(len(EDGES))
    x = [writer.variables_block(len(EDGES)) for _ in range(7)]
    triples = [writer.variables_block(N) for _ in range(7)]
    fives = [writer.variables_block(N) for _ in range(3)]

    incident = [
        [index for index, edge in enumerate(EDGES) if vertex in edge]
        for vertex in VERTICES
    ]

    # Seven edge-disjoint matchings of sizes 4,4,4,4,5,5,5.
    for colour in range(7):
        writer.exactly(x[colour], 4 if colour < 4 else 5)
        for vertex in VERTICES:
            writer.at_most_one(
                [x[colour][edge] for edge in incident[vertex]]
            )
    for edge in range(len(EDGES)):
        writer.at_most_one([x[colour][edge] for colour in range(7)])
        for colour in range(7):
            writer.add([-x[colour][edge], f[edge]])
        writer.add([-f[edge], *[x[colour][edge] for colour in range(7)]])

    # Every four-edge matching is isomorphic to this one.
    canonical = {
        EDGE_INDEX[(0, 1)],
        EDGE_INDEX[(2, 3)],
        EDGE_INDEX[(4, 5)],
        EDGE_INDEX[(6, 7)],
    }
    for edge in range(len(EDGES)):
        writer.add([x[0][edge] if edge in canonical else -x[0][edge]])

    # Once the first four-edge matching is canonical, the other three
    # four-edge colours remain exchangeable.  The three five-edge colours
    # are exchangeable as well.
    for colour in range(1, 3):
        writer.lex_not_greater(x[colour], x[colour + 1])
    for colour in range(4, 6):
        writer.lex_not_greater(x[colour], x[colour + 1])

    # Seven complement triples and three complement five-sets.  Sorting each
    # exchangeable family removes row permutations without losing solutions.
    for triple in triples:
        writer.exactly(triple, 3)
    for five in fives:
        writer.exactly(five, 5)
    for row in range(6):
        writer.lex_not_greater(triples[row], triples[row + 1])
    for row in range(2):
        writer.lex_not_greater(fives[row], fives[row + 1])

    # omissions(v) = degree_F(v)-2, rewritten with positive signed literals.
    for vertex in VERTICES:
        omissions = [
            *[triples[row][vertex] for row in range(7)],
            *[fives[row][vertex] for row in range(3)],
        ]
        unused_incident = [-f[edge] for edge in incident[vertex]]
        writer.exactly([*omissions, *unused_incident], 10)

    # If a row is exactly T, every perfect matching of V-T must meet F.
    for row in range(7):
        for triple in TRIPLES:
            support = tuple(
                vertex for vertex in VERTICES if vertex not in triple
            )
            gate = [-triples[row][vertex] for vertex in triple]
            for matching in perfect_matchings(support):
                writer.add([*gate, *[f[edge] for edge in matching]])

    writer.finish()
    print(
        f"WROTE {path} variables={writer.variables} "
        f"clauses={writer.clauses}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
