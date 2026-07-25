#!/usr/bin/env python3
"""Exact rank-four sign search on a fixed one-factorization of K_10.

For each unordered edge ij, the standard round-robin one-factorization gives
a magnitude in {1,...,9}.  This script chooses its sign and asks that every
principal 6-Pfaffian of the resulting 10x10 alternating matrix vanish modulo
19.  Over a field of odd characteristic this is equivalent to rank at most 4.

The scope is deliberately exact and narrow: UNSAT rules out this fixed
one-factorization, not all one-factorizations of K_10.  SAT gives a genuine
half-link which the paired-doubling lemma lifts to the full p=19 ordered link.
"""

from __future__ import annotations

import argparse
import itertools
from functools import lru_cache

from ortools.sat.python import cp_model


P = 19
N = 10
INFINITY = 9


def standard_factorization() -> dict[tuple[int, int], int]:
    """Return edge -> colour 1..9 for the round-robin factorization of K_10."""

    answer: dict[tuple[int, int], int] = {}
    for residue in range(9):
        pairs = [(INFINITY, residue)]
        pairs.extend(
            ((residue + offset) % 9, (residue - offset) % 9)
            for offset in range(1, 5)
        )
        for left, right in pairs:
            edge = tuple(sorted((left, right)))
            assert edge not in answer
            answer[edge] = residue + 1
    assert len(answer) == N * (N - 1) // 2
    return answer


@lru_cache(maxsize=None)
def pfaffian_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[int, tuple[tuple[int, int], ...]], ...]:
    """Expansion terms (sign, matching) of a principal Pfaffian."""

    if not vertices:
        return ((1, ()),)
    first = vertices[0]
    answer: list[tuple[int, tuple[tuple[int, int], ...]]] = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        expansion_sign = 1 if position % 2 == 1 else -1
        edge = tuple(sorted((first, second)))
        for sub_sign, sub_matching in pfaffian_matchings(remainder):
            answer.append(
                (expansion_sign * sub_sign, (edge,) + sub_matching)
            )
    return tuple(answer)


def symmetric_residue(value: int) -> int:
    value %= P
    return value if value <= P // 2 else value - P


def matrix_rank_mod(matrix: list[list[int]], p: int) -> int:
    work = [[value % p for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, p)
        work[rank] = [(inverse * value) % p for value in work[rank]]
        for row in range(rows):
            if row != rank and work[row][column]:
                multiplier = work[row][column]
                work[row] = [
                    (left - multiplier * right) % p
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
    return rank


def check_half_link(matrix: list[list[int]]) -> None:
    assert all(matrix[i][i] == 0 for i in range(N))
    assert all(
        matrix[i][j] % P == -matrix[j][i] % P
        for i in range(N)
        for j in range(N)
    )
    target = list(range(1, 10))
    for row in range(N):
        classes = sorted(
            min(matrix[row][column] % P, -matrix[row][column] % P)
            for column in range(N)
            if column != row
        )
        assert classes == target
    assert matrix_rank_mod(matrix, P) <= 4


def solve(seconds: float, workers: int, seed: int) -> int:
    magnitudes = standard_factorization()
    model = cp_model.CpModel()
    sign_bits = {
        edge: model.new_bool_var(f"negative_{edge[0]}_{edge[1]}")
        for edge in sorted(magnitudes)
    }

    # Vertex switching A_ij -> epsilon_i epsilon_j A_ij preserves rank and all
    # sign classes.  Fix the star at vertex 0 positive.
    for other in range(1, N):
        model.add(sign_bits[(0, other)] == 0)

    for subset in itertools.combinations(range(N), 6):
        constant = 0
        weighted_parities = []
        for term_index, (term_sign, matching) in enumerate(
            pfaffian_matchings(subset)
        ):
            coefficient = term_sign
            for edge in matching:
                coefficient *= magnitudes[edge]
            coefficient = symmetric_residue(coefficient)
            constant += coefficient

            parity = model.new_bool_var(
                "odd_" + "_".join(map(str, subset)) + f"_{term_index}"
            )
            # parity = XOR of the three edge-sign bits.
            model.add_bool_xor(
                [*(sign_bits[edge] for edge in matching), parity.negated()]
            )
            weighted_parities.append((-2 * coefficient, parity))

        quotient = model.new_int_var(-16, 16, "q_" + "_".join(map(str, subset)))
        model.add(
            constant
            + sum(coefficient * parity
                  for coefficient, parity in weighted_parities)
            == P * quotient
        )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.log_search_progress = True
    status = solver.solve(model)
    print("status:", solver.status_name(status))
    print("conflicts:", solver.num_conflicts)
    print("branches:", solver.num_branches)
    print("wall_seconds:", solver.wall_time)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return 1

    matrix = [[0] * N for _ in range(N)]
    for (left, right), magnitude in magnitudes.items():
        value = -magnitude if solver.value(sign_bits[(left, right)]) else magnitude
        matrix[left][right] = value % P
        matrix[right][left] = -value % P
    check_half_link(matrix)
    print("A = [")
    for row in matrix:
        print("  [" + ", ".join(map(str, row)) + "],")
    print("]")
    print("rank:", matrix_rank_mod(matrix, P))
    print("half-link exact verification: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=190835)
    args = parser.parse_args()
    return solve(args.seconds, args.workers, args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
