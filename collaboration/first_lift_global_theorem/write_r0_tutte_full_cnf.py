"""Write an exact Tutte-barrier CNF for the exceptional r=0 frontier.

This model has the same primary objects as the core-independent full model:
seven selected matchings, seven remaining complement triples, three remaining
complement five-sets, and the exact complement row sums.  Instead of listing
all 945 perfect matchings of each ten-support, it existentially chooses one of
the seven coarsened Tutte barriers classified in
``EIGHTH_MATCHING_CORE_CATALOGUE.md``.

For a chosen support V and separator S, the vertices of V-S are assigned to
s+2 odd blocks of the catalogue shape.  Every edge between distinct blocks is
required to lie in F.  This is equivalent to the residual graph on V having
no perfect matching.

SAT is therefore a directly checkable totally blocked seven-prefix.  Checked
UNSAT, together with the independently verified exhaustive barrier catalogue,
proves the exceptional r=0 eighth-matching lemma.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import write_r0_compact_full_cnf as compact


# (name, separator size, odd block sizes)
BARRIERS = (
    ("37", 0, (3, 7)),
    ("55", 0, (5, 5)),
    ("333", 1, (3, 3, 3)),
    ("5111", 2, (5, 1, 1, 1)),
    ("3311", 2, (3, 3, 1, 1)),
    ("31111", 3, (3, 1, 1, 1, 1)),
    ("6", 4, (1, 1, 1, 1, 1, 1)),
)


def build(path: Path) -> None:
    writer = compact.Writer(path)

    f = writer.variables_block(len(compact.EDGES))
    x = [writer.variables_block(len(compact.EDGES)) for _ in range(7)]
    triples = [writer.variables_block(compact.N) for _ in range(7)]
    fives = [writer.variables_block(compact.N) for _ in range(3)]

    incident = [
        [
            index
            for index, edge in enumerate(compact.EDGES)
            if vertex in edge
        ]
        for vertex in compact.VERTICES
    ]

    # Seven edge-disjoint matchings of sizes 4,4,4,4,5,5,5.
    for colour in range(7):
        writer.exactly(x[colour], 4 if colour < 4 else 5)
        for vertex in compact.VERTICES:
            writer.at_most_one(
                [x[colour][edge] for edge in incident[vertex]]
            )
    for edge in range(len(compact.EDGES)):
        writer.at_most_one([x[colour][edge] for colour in range(7)])
        for colour in range(7):
            writer.add([-x[colour][edge], f[edge]])
        writer.add([-f[edge], *[x[colour][edge] for colour in range(7)]])

    canonical = {
        compact.EDGE_INDEX[(0, 1)],
        compact.EDGE_INDEX[(2, 3)],
        compact.EDGE_INDEX[(4, 5)],
        compact.EDGE_INDEX[(6, 7)],
    }
    for edge in range(len(compact.EDGES)):
        writer.add([x[0][edge] if edge in canonical else -x[0][edge]])
    for colour in range(1, 3):
        writer.lex_not_greater(x[colour], x[colour + 1])
    for colour in range(4, 6):
        writer.lex_not_greater(x[colour], x[colour + 1])

    for triple in triples:
        writer.exactly(triple, 3)
    for five in fives:
        writer.exactly(five, 5)
    for row in range(6):
        writer.lex_not_greater(triples[row], triples[row + 1])
    for row in range(2):
        writer.lex_not_greater(fives[row], fives[row + 1])

    for vertex in compact.VERTICES:
        omissions = [
            *[triples[row][vertex] for row in range(7)],
            *[fives[row][vertex] for row in range(3)],
        ]
        unused_incident = [-f[edge] for edge in incident[vertex]]
        writer.exactly([*omissions, *unused_incident], 10)

    # Every remaining size-ten support chooses a coarsened Tutte barrier.
    for row in range(7):
        choices = writer.variables_block(len(BARRIERS))
        writer.exactly_one(choices)

        for choice, (_, separator_size, block_sizes) in zip(
            choices, BARRIERS
        ):
            # Group zero is the separator; the rest are the odd blocks.
            group_sizes = (separator_size, *block_sizes)
            groups = [
                writer.variables_block(compact.N) for _ in group_sizes
            ]

            for vertex in compact.VERTICES:
                roles = [group[vertex] for group in groups]
                writer.at_most_one(roles)
                for role in roles:
                    writer.add([-role, choice])
                    writer.add([-role, -triples[row][vertex]])
                # If this barrier is selected and v is not omitted, v has a
                # separator/block role.
                writer.add(
                    [-choice, triples[row][vertex], *roles]
                )

            for group, size in zip(groups, group_sizes):
                writer.exactly(group, size, gate=choice)

            blocks = groups[1:]
            # Blocks of the same size are exchangeable.  Sorting adjacent
            # equal-size blocks removes factors as large as 6! for K_6.
            for block in range(len(blocks) - 1):
                if block_sizes[block] == block_sizes[block + 1]:
                    writer.lex_not_greater(
                        blocks[block], blocks[block + 1]
                    )

            for edge, (left_vertex, right_vertex) in enumerate(
                compact.EDGES
            ):
                for left_block in range(len(blocks)):
                    for right_block in range(len(blocks)):
                        if left_block == right_block:
                            continue
                        writer.add(
                            [
                                -blocks[left_block][left_vertex],
                                -blocks[right_block][right_vertex],
                                f[edge],
                            ]
                        )

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
