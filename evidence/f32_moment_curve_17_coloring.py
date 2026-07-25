#!/usr/bin/env python3
"""Generate or verify exact 17-colourings of the two e4-boundary graphs.

This utility deliberately reuses the independently checked graph builder in
``f32_five_statistic_moment_curve_clique_bound.py``.  Its three modes are:

    cnf OFFSET OUTPUT.cnf
    extract OFFSET SOLVER_OUTPUT.txt OUTPUT.colors
    verify OFFSET INPUT.colors

The CNF uses one Boolean x[v,c] for every one of the 1024 possible vertices
and every colour c.  Unrealizable vertices are fixed false.  A known K17 is
fixed to all seventeen colours, removing global colour symmetry.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import f32_five_statistic_moment_curve_clique_bound as boundary


NUMBER_OF_VERTICES = 1024
NUMBER_OF_COLOURS = 17

ZERO_SEED_PAIRS = tuple(
    (value, 1)
    for value in range(32)
    if value == 0 or boundary.trace(value) == 1
)
ONE_SEED_PAIRS = (
    (0, 0),
    (1, 1),
    (2, 10),
    (11, 16),
    (22, 26),
    (13, 1),
    (14, 10),
    (24, 16),
    (26, 26),
    (5, 26),
    (7, 16),
    (9, 26),
    (17, 10),
    (18, 1),
    (20, 16),
    (29, 10),
    (30, 1),
)


def variable(vertex: int, colour: int) -> int:
    assert 0 <= vertex < NUMBER_OF_VERTICES
    assert 0 <= colour < NUMBER_OF_COLOURS
    return 1 + NUMBER_OF_COLOURS * vertex + colour


def graph(offset: int) -> tuple[list[int], list[int], list[int]]:
    adjacency, counts, _ = boundary.build_graph(offset)
    active = [vertex for vertex, count in enumerate(counts) if count]
    expected = {
        0: (1023, 45_291),
        1: (1024, 71_648),
    }
    edges = sum(bits.bit_count() for bits in adjacency) // 2
    assert (len(active), edges) == expected[offset]
    return adjacency, counts, active


def seed(offset: int) -> list[int]:
    pairs = ZERO_SEED_PAIRS if offset == 0 else ONE_SEED_PAIRS
    vertices = [
        boundary.encode(parameter, lam) for parameter, lam in pairs
    ]
    assert len(vertices) == 17
    return vertices


def generating_blocks(offset: int) -> list[tuple[int, ...]]:
    """Enumerate the 17-vertex quotient cliques from their 17-set bases."""

    target = (1, 0, 0, 0, offset)
    answer = []
    for left_size, left_coefficients, left_mask in boundary.LEFT_ENTRIES:
        right_size = 17 - left_size
        if not 1 <= right_size <= 16:
            continue
        right_prefix = boundary.needed_right_prefix(
            target, left_coefficients
        )
        key = (right_size,) + right_prefix[1:]
        for right_coefficients, right_mask in boundary.RIGHT_INDEX.get(
            key, ()
        ):
            rho = boundary.combined_coefficients(
                left_coefficients, right_coefficients
            )
            assert rho[:5] == target
            mask = left_mask | right_mask
            assert mask.bit_count() == 17
            vertices = []
            for point in range(32):
                if not (mask >> point & 1):
                    continue
                quotient = [1]
                for degree in range(1, 9):
                    quotient.append(
                        rho[degree]
                        ^ boundary.PRODUCT[point][quotient[-1]]
                    )
                first = quotient[1]
                lam = quotient[8] ^ boundary.POWERS[first][8]
                vertices.append(boundary.encode(point, lam))
            assert len(vertices) == 17
            answer.append(tuple(vertices))
    expected = {0: 341, 1: 562}
    assert len(answer) == expected[offset]
    return answer


def parity_transversal_test(offset: int) -> None:
    """Necessary GF(2) test for each seed-fixed colour class."""

    blocks = generating_blocks(offset)
    fixed_seed = seed(offset)
    outcomes = []
    for colour, selected_seed in enumerate(fixed_seed):
        rows = [
            sum(1 << vertex for vertex in block)
            | (1 << NUMBER_OF_VERTICES)
            for block in blocks
        ]
        for vertex in fixed_seed:
            rhs = int(vertex == selected_seed)
            rows.append((1 << vertex) | (rhs << NUMBER_OF_VERTICES))

        basis: dict[int, int] = {}
        inconsistent = False
        for row in rows:
            variables = row & ((1 << NUMBER_OF_VERTICES) - 1)
            while variables:
                pivot = variables.bit_length() - 1
                if pivot not in basis:
                    basis[pivot] = row
                    break
                row ^= basis[pivot]
                variables = row & ((1 << NUMBER_OF_VERTICES) - 1)
            else:
                if row >> NUMBER_OF_VERTICES & 1:
                    inconsistent = True
                    break
        outcomes.append((not inconsistent, len(basis)))
    print(
        f"offset={offset}: GF(2) exact-transversal necessary test "
        f"blocks={len(blocks)} outcomes={outcomes}"
    )


def clauses(offset: int) -> tuple[int, list[tuple[int, ...]]]:
    adjacency, counts, active = graph(offset)
    answer: list[tuple[int, ...]] = []

    for vertex in range(NUMBER_OF_VERTICES):
        if counts[vertex] == 0:
            for colour in range(NUMBER_OF_COLOURS):
                answer.append((-variable(vertex, colour),))
            continue
        answer.append(
            tuple(variable(vertex, colour)
                  for colour in range(NUMBER_OF_COLOURS))
        )
        for left_colour in range(NUMBER_OF_COLOURS):
            for right_colour in range(left_colour + 1, NUMBER_OF_COLOURS):
                answer.append(
                    (-variable(vertex, left_colour),
                     -variable(vertex, right_colour))
                )

    for left in active:
        later = adjacency[left] & ~((1 << (left + 1)) - 1)
        while later:
            bit = later & -later
            right = bit.bit_length() - 1
            later ^= bit
            for colour in range(NUMBER_OF_COLOURS):
                answer.append(
                    (-variable(left, colour), -variable(right, colour))
                )

    fixed = seed(offset)
    assert boundary.is_clique(fixed, adjacency)
    for colour, vertex in enumerate(fixed):
        answer.append((variable(vertex, colour),))

    return NUMBER_OF_VERTICES * NUMBER_OF_COLOURS, answer


def write_cnf(offset: int, output: Path) -> None:
    number_of_variables, generated = clauses(offset)
    with output.open("w", encoding="ascii") as stream:
        stream.write(
            f"p cnf {number_of_variables} {len(generated)}\n"
        )
        for clause in generated:
            stream.write(" ".join(map(str, clause)))
            stream.write(" 0\n")
    print(
        f"offset={offset}: variables={number_of_variables} "
        f"clauses={len(generated)} output={output}"
    )


def extract_colours(
    offset: int, solver_output: Path, output: Path
) -> None:
    assignments: dict[int, bool] = {}
    satisfiable = False
    for line in solver_output.read_text(encoding="ascii").splitlines():
        if line == "s SATISFIABLE":
            satisfiable = True
        if not line.startswith("v "):
            continue
        for literal_text in line.split()[1:]:
            literal = int(literal_text)
            if literal:
                assignments[abs(literal)] = literal > 0
    assert satisfiable

    _, counts, _ = graph(offset)
    colours = [-1] * NUMBER_OF_VERTICES
    for vertex in range(NUMBER_OF_VERTICES):
        selected = [
            colour
            for colour in range(NUMBER_OF_COLOURS)
            if assignments.get(variable(vertex, colour), False)
        ]
        if counts[vertex]:
            assert len(selected) == 1
            colours[vertex] = selected[0]
        else:
            assert not selected
    output.write_text(
        " ".join(map(str, colours)) + "\n", encoding="ascii"
    )
    verify_colours(offset, output)


def verify_colours(offset: int, input_path: Path) -> None:
    colours = tuple(
        map(int, input_path.read_text(encoding="ascii").split())
    )
    assert len(colours) == NUMBER_OF_VERTICES
    adjacency, counts, active = graph(offset)
    for vertex in range(NUMBER_OF_VERTICES):
        if counts[vertex]:
            assert 0 <= colours[vertex] < NUMBER_OF_COLOURS
        else:
            assert colours[vertex] == -1
    checked_edges = 0
    for left in active:
        later = adjacency[left] & ~((1 << (left + 1)) - 1)
        while later:
            bit = later & -later
            right = bit.bit_length() - 1
            later ^= bit
            assert colours[left] != colours[right]
            checked_edges += 1
    fixed = seed(offset)
    assert tuple(colours[vertex] for vertex in fixed) == tuple(range(17))
    print(
        f"offset={offset}: 17-colouring PASS "
        f"vertices={len(active)} edges={checked_edges}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    cnf_parser = subparsers.add_parser("cnf")
    cnf_parser.add_argument("offset", type=int, choices=(0, 1))
    cnf_parser.add_argument("output", type=Path)

    extract_parser = subparsers.add_parser("extract")
    extract_parser.add_argument("offset", type=int, choices=(0, 1))
    extract_parser.add_argument("solver_output", type=Path)
    extract_parser.add_argument("output", type=Path)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("offset", type=int, choices=(0, 1))
    verify_parser.add_argument("input", type=Path)

    parity_parser = subparsers.add_parser("parity")
    parity_parser.add_argument("offset", type=int, choices=(0, 1))

    arguments = parser.parse_args()
    if arguments.mode == "cnf":
        write_cnf(arguments.offset, arguments.output)
    elif arguments.mode == "extract":
        extract_colours(
            arguments.offset, arguments.solver_output, arguments.output
        )
    elif arguments.mode == "verify":
        verify_colours(arguments.offset, arguments.input)
    else:
        parity_transversal_test(arguments.offset)


if __name__ == "__main__":
    main()
