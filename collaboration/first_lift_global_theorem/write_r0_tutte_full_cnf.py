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

SAT is therefore a directly checkable seven-prefix blocking all seven
remaining size-ten supports. Checked UNSAT, together with the independently
verified exhaustive barrier catalogue, proves the exceptional r=0
eighth-matching lemma.
"""

from __future__ import annotations

import argparse
from itertools import combinations
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


def require_four_distinct_cores(
    writer: compact.Writer,
    descriptors: list[list[int]],
) -> dict[tuple[int, int], int]:
    """Forbid seven rows from using at most three distinct sorted cores."""
    different: dict[tuple[int, int], int] = {}
    for left, right in combinations(range(7), 2):
        assert len(descriptors[left]) == len(descriptors[right])
        difference_bits = []
        for left_bit, right_bit in zip(
            descriptors[left], descriptors[right]
        ):
            xor = writer.variable()
            difference_bits.append(xor)
            # xor iff left_bit and right_bit differ.
            writer.add([-xor, left_bit, right_bit])
            writer.add([-xor, -left_bit, -right_bit])
            writer.add([-left_bit, right_bit, xor])
            writer.add([left_bit, -right_bit, xor])
        pair_different = writer.variable()
        writer.add([-pair_different, *difference_bits])
        different[left, right] = pair_different

    # If there are at least four equivalence classes, then outside every
    # three chosen representatives is a row different from all three.
    for representatives in combinations(range(7), 3):
        witnesses = []
        for row in range(7):
            if row in representatives:
                continue
            witness = writer.variable()
            witnesses.append(witness)
            for representative in representatives:
                pair = tuple(sorted((row, representative)))
                writer.add([-witness, different[pair]])
        writer.add(witnesses)
    return different


def require_five_cores_if_barrier_b(
    writer: compact.Writer,
    barrier_choices_by_row: list[list[int]],
    different: dict[tuple[int, int], int],
) -> None:
    """If any row has a 3311 core, require at least five core classes."""
    b_choices = [choices[1] for choices in barrier_choices_by_row]
    has_b = writer.variable()
    for choice in b_choices:
        writer.add([-choice, has_b])
    writer.add([-has_b, *b_choices])

    require_five_distinct_cores(writer, different, gate=has_b)


def require_five_distinct_cores(
    writer: compact.Writer,
    different: dict[tuple[int, int], int],
    gate: int | None = None,
) -> None:
    """Require five core classes, optionally conditional on ``gate``."""
    for representatives in combinations(range(7), 4):
        witnesses = []
        for row in range(7):
            if row in representatives:
                continue
            witness = writer.variable()
            witnesses.append(witness)
            for representative in representatives:
                pair = tuple(sorted((row, representative)))
                writer.add([-witness, different[pair]])
        writer.add(witnesses if gate is None else [-gate, *witnesses])


def require_six_distinct_cores(
    writer: compact.Writer,
    different: dict[tuple[int, int], int],
    gate: int,
) -> None:
    """Conditionally require at least six core equivalence classes."""
    for representatives in combinations(range(7), 5):
        witnesses = []
        for row in range(7):
            if row in representatives:
                continue
            witness = writer.variable()
            witnesses.append(witness)
            for representative in representatives:
                pair = tuple(sorted((row, representative)))
                writer.add([-witness, different[pair]])
        writer.add([-gate, *witnesses])


def require_six_cores_if_two_b_rows(
    writer: compact.Writer,
    barrier_choices_by_row: list[list[int]],
    different: dict[tuple[int, int], int],
) -> None:
    """If at least two rows have 3311 cores, require six core classes."""
    b_choices = [choices[1] for choices in barrier_choices_by_row]
    at_least_two_b = writer.variable()
    for pair in combinations(b_choices, 2):
        writer.add([-pair[0], -pair[1], at_least_two_b])
    require_six_distinct_cores(
        writer, different, gate=at_least_two_b
    )


def require_six_cores_if_barrier_b(
    writer: compact.Writer,
    barrier_choices_by_row: list[list[int]],
    different: dict[tuple[int, int], int],
) -> None:
    """If any row has a 3311 core, require six core classes."""
    b_choices = [choices[1] for choices in barrier_choices_by_row]
    has_b = writer.variable()
    for choice in b_choices:
        writer.add([-choice, has_b])
    writer.add([-has_b, *b_choices])
    require_six_distinct_cores(writer, different, gate=has_b)


def build(
    path: Path,
    surviving_only: bool = False,
    require_four_cores: bool = False,
    require_five_cores: bool = False,
    exclude_all_k6: bool = False,
    b_needs_five_cores: bool = False,
    high_b_needs_six_cores: bool = False,
    b_needs_six_cores: bool = False,
    type_counts: tuple[int, ...] | None = None,
) -> None:
    if require_four_cores and not surviving_only:
        raise ValueError("--require-four-cores requires --surviving-only")
    if require_five_cores and not require_four_cores:
        raise ValueError(
            "--require-five-cores requires --require-four-cores"
        )
    if exclude_all_k6 and not surviving_only:
        raise ValueError("--exclude-all-k6 requires --surviving-only")
    if b_needs_five_cores and not require_four_cores:
        raise ValueError(
            "--b-needs-five-cores requires --require-four-cores"
        )
    if high_b_needs_six_cores and not require_five_cores:
        raise ValueError(
            "--high-b-needs-six-cores requires --require-five-cores"
        )
    if b_needs_six_cores and not require_five_cores:
        raise ValueError(
            "--b-needs-six-cores requires --require-five-cores"
        )
    writer = compact.Writer(path)
    barriers = BARRIERS[3:] if surviving_only else BARRIERS
    if type_counts is not None:
        if len(type_counts) != len(barriers) or sum(type_counts) != 7:
            raise ValueError("type counts must match the barriers and sum to 7")

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
    core_descriptors = []
    barrier_choices_by_row = []
    for row in range(7):
        choices = writer.variables_block(len(barriers))
        barrier_choices_by_row.append(choices)
        writer.exactly_one(choices)
        descriptor = list(choices)

        for choice, (_, separator_size, block_sizes) in zip(
            choices, barriers
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
            descriptor.extend(
                variable for block in blocks for variable in block
            )
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
        core_descriptors.append(descriptor)

    if type_counts is not None:
        for barrier, count in enumerate(type_counts):
            writer.exactly(
                [
                    barrier_choices_by_row[row][barrier]
                    for row in range(7)
                ],
                count,
            )

    if exclude_all_k6:
        # The verified D^4 shape theorem plus the complement row identity
        # eliminate the type multiset (0,0,0,7).
        writer.add(
            [
                barrier_choices_by_row[row][barrier]
                for row in range(7)
                for barrier in range(len(barriers) - 1)
            ]
        )

    if require_four_cores:
        different = require_four_distinct_cores(
            writer, core_descriptors
        )
        if require_five_cores:
            require_five_distinct_cores(writer, different)
            if high_b_needs_six_cores:
                require_six_cores_if_two_b_rows(
                    writer, barrier_choices_by_row, different
                )
            if b_needs_six_cores:
                require_six_cores_if_barrier_b(
                    writer, barrier_choices_by_row, different
                )
        elif b_needs_five_cores:
            require_five_cores_if_barrier_b(
                writer, barrier_choices_by_row, different
            )

    writer.finish()
    print(
        f"WROTE {path} variables={writer.variables} "
        f"clauses={writer.clauses} "
        f"barriers={'surviving' if surviving_only else 'all'} "
        f"four_cores={require_four_cores} "
        f"five_cores={require_five_cores} "
        f"exclude_all_k6={exclude_all_k6} "
        f"b_needs_five_cores={b_needs_five_cores} "
        f"high_b_needs_six_cores={high_b_needs_six_cores} "
        f"b_needs_six_cores={b_needs_six_cores} "
        f"type_counts={type_counts}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--surviving-only",
        action="store_true",
        help=(
            "Use the prior row-sum theorem eliminating 37, 55, and 333 "
            "from a total obstruction"
        ),
    )
    parser.add_argument(
        "--require-four-cores",
        action="store_true",
        help=(
            "Use the prior three-core capacity theorem that a total "
            "obstruction needs at least four distinct surviving cores"
        ),
    )
    parser.add_argument(
        "--type-counts",
        help=(
            "Comma-separated row counts in barrier order; with "
            "--surviving-only the order is 5111,3311,31111,6"
        ),
    )
    parser.add_argument(
        "--require-five-cores",
        action="store_true",
        help=(
            "Use the prior exact four-core-family theorem that a total "
            "obstruction needs at least five distinct surviving cores"
        ),
    )
    parser.add_argument(
        "--exclude-all-k6",
        action="store_true",
        help=(
            "Use the prior D^4 shape and row-identity theorem excluding "
            "seven K6 obstruction rows"
        ),
    )
    parser.add_argument(
        "--b-needs-five-cores",
        action="store_true",
        help=(
            "Use the prior four-core capacity theorem: if any row uses "
            "K3311, at least five distinct cores are required"
        ),
    )
    parser.add_argument(
        "--high-b-needs-six-cores",
        action="store_true",
        help=(
            "Use the exact five-core high-B theorem: at least two "
            "K3311 rows require at least six distinct cores"
        ),
    )
    parser.add_argument(
        "--b-needs-six-cores",
        action="store_true",
        help=(
            "Use the exact five-core B theorem: any K3311 row "
            "requires at least six distinct cores"
        ),
    )
    args = parser.parse_args()
    type_counts = (
        tuple(map(int, args.type_counts.split(",")))
        if args.type_counts
        else None
    )
    build(
        args.output,
        surviving_only=args.surviving_only,
        require_four_cores=args.require_four_cores,
        require_five_cores=args.require_five_cores,
        exclude_all_k6=args.exclude_all_k6,
        b_needs_five_cores=args.b_needs_five_cores,
        high_b_needs_six_cores=args.high_b_needs_six_cores,
        b_needs_six_cores=args.b_needs_six_cores,
        type_counts=type_counts,
    )


if __name__ == "__main__":
    main()
