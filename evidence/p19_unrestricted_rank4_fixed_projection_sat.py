#!/usr/bin/env python3
"""Exact residual-coordinate SAT search for a fixed p=19 paired-link projection.

This is a construction search, not an unrestricted nonexistence certificate.
The first and third coordinates below come from a rank-four paired-link local
search.  The SAT instance ranges over all 19^2 choices of the remaining two
coordinates at each of vertices 2,...,9.  A satisfying assignment is decoded
and independently verified as a ten-vertex sign-class link, which then doubles
to a twenty-vertex ordered link.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


P = 19
N = 10
H = 9

# Only coordinates 0 and 2 are fixed.  Coordinates 1 and 3 are SAT variables.
PROJECTION = [
    (1, 0),
    (0, 1),
    (11, 9),
    (12, 5),
    (3, 8),
    (15, 13),
    (5, 2),
    (13, 4),
    (17, 3),
    (9, 12),
]


def sign_class(value: int) -> int:
    value %= P
    return min(value, P - value)


def pairing(left: tuple[int, int, int, int],
            right: tuple[int, int, int, int]) -> int:
    return (
        left[0] * right[2] - left[2] * right[0]
        + left[1] * right[3] - left[3] * right[1]
    ) % P


class Variables:
    def __init__(self) -> None:
        self.next_id = 1
        self.x: dict[tuple[int, int], int] = {}
        self.edge: dict[tuple[int, int, int], int] = {}
        self.aux: dict[tuple[int, int], int] = {}
        for vertex in range(2, N):
            for state in range(P * P):
                self.x[vertex, state] = self.fresh()
        for left in range(N):
            for right in range(left + 1, N):
                for value_class in range(1, H + 1):
                    self.edge[left, right, value_class] = self.fresh()
        for vertex in range(2, N):
            for index in range(P * P - 1):
                self.aux[vertex, index] = self.fresh()

    def fresh(self) -> int:
        answer = self.next_id
        self.next_id += 1
        return answer


def state_coordinates(vertex: int, state: int) -> tuple[int, int, int, int]:
    first, third = PROJECTION[vertex]
    return first, state // P, third, state % P


def fixed_coordinates(vertex: int) -> tuple[int, int, int, int]:
    first, third = PROJECTION[vertex]
    return first, 0, third, 0


def write_cnf(path: Path) -> Variables:
    variables = Variables()
    state_count = P * P
    variable_vertices = N - 2
    variable_edges = (N - 2) * (N - 3) // 2
    fixed_variable_edges = 2 * (N - 2)
    edge_count = N * (N - 1) // 2
    clauses = (
        variable_vertices * (1 + (3 * state_count - 4))
        + edge_count * (1 + H * (H - 1) // 2)
        + variable_edges * state_count * state_count
        + fixed_variable_edges * state_count
        + 1
        + N * H * ((N - 1) * (N - 2) // 2)
        + 1
    )

    with path.open("w", encoding="ascii") as output:
        output.write(f"p cnf {variables.next_id - 1} {clauses}\n")

        # Exactly one residual state per variable vertex, using Sinz's
        # sequential at-most-one encoding plus one at-least-one clause.
        for vertex in range(2, N):
            xs = [variables.x[vertex, state] for state in range(state_count)]
            ss = [variables.aux[vertex, index] for index in range(state_count - 1)]
            output.write(" ".join(map(str, xs)) + " 0\n")
            output.write(f"{-xs[0]} {ss[0]} 0\n")
            for index in range(1, state_count - 1):
                output.write(f"{-xs[index]} {ss[index]} 0\n")
                output.write(f"{-ss[index - 1]} {ss[index]} 0\n")
                output.write(f"{-xs[index]} {-ss[index - 1]} 0\n")
            output.write(f"{-xs[-1]} {-ss[-1]} 0\n")

        # The residual SL(2,19) action preserves every pairing and is
        # transitive on nonzero residual vectors.  This file searches the
        # nonzero branch and safely normalizes vertex 2 to (1,0).
        output.write(f"{variables.x[2, P]} 0\n")

        # Exactly one nonzero sign class on each edge.
        for left in range(N):
            for right in range(left + 1, N):
                edge_vars = [
                    variables.edge[left, right, value_class]
                    for value_class in range(1, H + 1)
                ]
                output.write(" ".join(map(str, edge_vars)) + " 0\n")
                for i, first in enumerate(edge_vars):
                    for second in edge_vars[i + 1:]:
                        output.write(f"{-first} {-second} 0\n")

        # Channel endpoint states to their exact edge sign class.  A zero
        # pairing is forbidden directly.
        for left in range(N):
            for right in range(left + 1, N):
                if left < 2 and right < 2:
                    value_class = sign_class(
                        pairing(fixed_coordinates(left), fixed_coordinates(right))
                    )
                    output.write(
                        f"{variables.edge[left, right, value_class]} 0\n"
                    )
                elif left < 2:
                    fixed = fixed_coordinates(left)
                    for state in range(state_count):
                        value_class = sign_class(
                            pairing(fixed, state_coordinates(right, state))
                        )
                        x = variables.x[right, state]
                        if value_class == 0:
                            output.write(f"{-x} 0\n")
                        else:
                            edge = variables.edge[left, right, value_class]
                            output.write(f"{-x} {edge} 0\n")
                else:
                    for left_state in range(state_count):
                        left_coordinates = state_coordinates(left, left_state)
                        x_left = variables.x[left, left_state]
                        for right_state in range(state_count):
                            value_class = sign_class(pairing(
                                left_coordinates,
                                state_coordinates(right, right_state),
                            ))
                            x_right = variables.x[right, right_state]
                            if value_class == 0:
                                output.write(f"{-x_left} {-x_right} 0\n")
                            else:
                                edge = variables.edge[left, right, value_class]
                                output.write(
                                    f"{-x_left} {-x_right} {edge} 0\n"
                                )

        # Each sign class occurs at most once at each vertex.  Since there
        # are nine incident edges and nine nonzero classes, this is exact.
        for vertex in range(N):
            incident = [
                (min(vertex, other), max(vertex, other))
                for other in range(N) if other != vertex
            ]
            for value_class in range(1, H + 1):
                edge_vars = [
                    variables.edge[left, right, value_class]
                    for left, right in incident
                ]
                for i, first in enumerate(edge_vars):
                    for second in edge_vars[i + 1:]:
                        output.write(f"{-first} {-second} 0\n")

    return variables


def decode_model(text: str, variables: Variables) -> list[tuple[int, int, int, int]]:
    positive: set[int] = set()
    for line in text.splitlines():
        if line.startswith("v "):
            positive.update(
                literal for literal in map(int, line.split()[1:])
                if literal > 0
            )
    vectors = [fixed_coordinates(0), fixed_coordinates(1)]
    for vertex in range(2, N):
        states = [
            state for state in range(P * P)
            if variables.x[vertex, state] in positive
        ]
        assert len(states) == 1, (vertex, states)
        vectors.append(state_coordinates(vertex, states[0]))
    return vectors


def rank(matrix: list[list[int]]) -> int:
    work = [[value % P for value in row] for row in matrix]
    answer = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(answer, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        inverse = pow(work[answer][column], -1, P)
        work[answer] = [value * inverse % P for value in work[answer]]
        for row in range(len(work)):
            if row != answer and work[row][column]:
                multiple = work[row][column]
                work[row] = [
                    (left - multiple * right) % P
                    for left, right in zip(work[row], work[answer])
                ]
        answer += 1
    return answer


def verify(vectors: list[tuple[int, int, int, int]]) -> None:
    matrix = [[0] * N for _ in range(N)]
    for left in range(N):
        for right in range(left + 1, N):
            matrix[left][right] = pairing(vectors[left], vectors[right])
            matrix[right][left] = -matrix[left][right] % P
    assert rank(matrix) <= 4
    target = list(range(1, H + 1))
    for row in matrix:
        assert sorted(sign_class(value) for value in row if value) == target
        assert all(value for index, value in enumerate(row) if row[index] != 0)
    print("SAT witness verified")
    print("vectors =", vectors)
    print("rank =", rank(matrix))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, default=Path("/private/tmp/p19-fixed.cnf"))
    parser.add_argument("--solver", default="/opt/homebrew/bin/cadical")
    parser.add_argument("--generate-only", action="store_true")
    args = parser.parse_args()
    variables = write_cnf(args.cnf)
    print(f"wrote {args.cnf}")
    if args.generate_only:
        return
    completed = subprocess.run(
        [args.solver, str(args.cnf)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(completed.stdout)
    if completed.returncode == 10:
        verify(decode_model(completed.stdout, variables))
    elif completed.returncode != 20:
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
