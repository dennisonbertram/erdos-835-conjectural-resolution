#!/usr/bin/env python3
"""Check the Pfaffian congruence used in the p=19 rank frontier.

For an n-by-r matrix U and an invertible alternating r-by-r matrix J,

    Pf((U J U^T)[S]) = det(U[S]) Pf(J)                 (|S| = r).

The theorem is the standard congruence identity
Pf(P A P^T) = det(P) Pf(A).  This dependency-free program independently
checks the arithmetic on every r-subset of r+2 rows for deterministic
full-rank examples over F_3, F_7, F_11, and F_19.
"""

from __future__ import annotations

from itertools import combinations
from random import Random


def determinant(matrix: list[list[int]], prime: int) -> int:
    work = [[value % prime for value in row] for row in matrix]
    answer = 1
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer = answer * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] * inverse % prime
            for entry in range(column, len(work)):
                work[row][entry] = (
                    work[row][entry] - multiplier * work[column][entry]
                ) % prime
    return answer % prime


def pfaffian(matrix: list[list[int]], prime: int) -> int:
    """Pfaffian elimination for an even alternating matrix."""

    size = len(matrix)
    assert size % 2 == 0
    work = [[value % prime for value in row] for row in matrix]
    answer = 1
    for left in range(0, size, 2):
        mate = next(
            (right for right in range(left + 1, size) if work[left][right]),
            None,
        )
        if mate is None:
            return 0
        if mate != left + 1:
            for row in range(size):
                work[row][left + 1], work[row][mate] = (
                    work[row][mate],
                    work[row][left + 1],
                )
            work[left + 1], work[mate] = work[mate], work[left + 1]
            answer = -answer

        pivot = work[left][left + 1]
        answer = answer * pivot % prime
        inverse = pow(pivot, -1, prime)
        for row in range(left + 2, size):
            for column in range(row + 1, size):
                correction = (
                    work[left][row] * work[left + 1][column]
                    - work[left][column] * work[left + 1][row]
                )
                value = (work[row][column] - correction * inverse) % prime
                work[row][column] = value
                work[column][row] = -value % prime
    return answer % prime


def random_invertible_alternating(
    size: int, prime: int, random: Random
) -> list[list[int]]:
    while True:
        matrix = [[0] * size for _ in range(size)]
        for row in range(size):
            for column in range(row + 1, size):
                value = random.randrange(prime)
                matrix[row][column] = value
                matrix[column][row] = -value % prime
        if pfaffian(matrix, prime):
            return matrix


def alternating_gram(
    rows: list[list[int]], form: list[list[int]], prime: int
) -> list[list[int]]:
    size = len(rows)
    rank = len(form)
    answer = [[0] * size for _ in range(size)]
    for left in range(size):
        for right in range(left + 1, size):
            value = sum(
                rows[left][i] * form[i][j] * rows[right][j]
                for i in range(rank)
                for j in range(rank)
            ) % prime
            answer[left][right] = value
            answer[right][left] = -value % prime
    return answer


def principal(
    matrix: list[list[int]], indices: tuple[int, ...]
) -> list[list[int]]:
    return [[matrix[row][column] for column in indices] for row in indices]


def check_prime(prime: int) -> int:
    rank = prime - 1
    total = 0
    for trial in range(4):
        random = Random(10_000 * prime + trial)
        form = random_invertible_alternating(rank, prime, random)
        form_pfaffian = pfaffian(form, prime)

        # The identity block makes U full column rank; the last two rows
        # exercise nontrivial and sometimes singular maximal minors.
        rows = [
            [int(row == column) for column in range(rank)]
            for row in range(rank)
        ]
        rows.extend(
            [[random.randrange(prime) for _ in range(rank)] for _ in range(2)]
        )
        gram = alternating_gram(rows, form, prime)

        for indices in combinations(range(rank + 2), rank):
            row_minor = [rows[index] for index in indices]
            expected = determinant(row_minor, prime) * form_pfaffian % prime
            actual = pfaffian(principal(gram, indices), prime)
            assert actual == expected, (
                prime,
                trial,
                indices,
                actual,
                expected,
            )
            total += 1
    return total


def main() -> None:
    totals = {prime: check_prime(prime) for prime in (3, 7, 11, 19)}
    assert totals == {3: 24, 7: 112, 11: 264, 19: 760}
    print("checked principal congruences:", totals)
    print("rank-factor Pfaffian identity: PASS")


if __name__ == "__main__":
    main()
