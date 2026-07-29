#!/usr/bin/env python3
"""Exact moment identities for principal 4-Pfaffian stars."""

from itertools import combinations
from random import Random


def random_alternating(size, p, rng):
    matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            matrix[i][j] = rng.randrange(p)
            matrix[j][i] = -matrix[i][j] % p
    return matrix


def pf4(matrix, i, j, k, l, p):
    return (
        matrix[i][j] * matrix[k][l]
        - matrix[i][k] * matrix[j][l]
        + matrix[i][l] * matrix[j][k]
    ) % p


def verify_prime(p):
    rng = Random(2000 + p)
    n = p + 3
    for _ in range(8):
        matrix = random_alternating(n, p, rng)
        row_sums = [sum(row) % p for row in matrix]
        gram = [
            [sum(matrix[i][u] * matrix[j][u] for u in range(n)) % p for j in range(n)]
            for i in range(n)
        ]
        for i, j, k in combinations(range(n), 3):
            values = [pf4(matrix, i, j, k, u, p) for u in range(n)]
            # Repeated-index terms are zero, so this is also the p-value star sum.
            first = sum(values) % p
            expected_first = (
                matrix[i][j] * row_sums[k]
                - matrix[i][k] * row_sums[j]
                + matrix[j][k] * row_sums[i]
            ) % p
            assert first == expected_first

            w = (matrix[j][k], -matrix[i][k] % p, matrix[i][j])
            triple = (i, j, k)
            second = sum(value * value for value in values) % p
            expected_second = sum(
                w[a] * gram[triple[a]][triple[b]] * w[b]
                for a in range(3)
                for b in range(3)
            ) % p
            assert second == expected_second
    print(f"p={p}: first- and second-moment 4-Pfaffian identities PASS")


if __name__ == "__main__":
    for prime in (5, 7, 11, 17):
        verify_prime(prime)
    print("principal 4-Pfaffian star moment identities: VERIFIED")
