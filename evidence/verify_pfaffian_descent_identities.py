#!/usr/bin/env python3
"""Exact checks for the Schur-complement Pfaffian descent lemma."""

from itertools import combinations
from random import Random


def pfaffian(matrix, p):
    work = [row[:] for row in matrix]
    answer = 1
    for pivot in range(0, len(work), 2):
        mate = next((j for j in range(pivot + 1, len(work)) if work[pivot][j] % p), None)
        if mate is None:
            return 0
        if mate != pivot + 1:
            work[mate], work[pivot + 1] = work[pivot + 1], work[mate]
            for row in work:
                row[mate], row[pivot + 1] = row[pivot + 1], row[mate]
            answer = -answer
        edge = work[pivot][pivot + 1] % p
        answer = answer * edge % p
        inverse = pow(edge, -1, p)
        for i in range(pivot + 2, len(work)):
            for j in range(i + 1, len(work)):
                update = (
                    work[pivot][i] * work[pivot + 1][j]
                    - work[pivot][j] * work[pivot + 1][i]
                )
                work[i][j] = (work[i][j] - update * inverse) % p
                work[j][i] = -work[i][j] % p
    return answer % p


def principal(matrix, indices):
    return [[matrix[i][j] for j in indices] for i in indices]


def inverse(matrix, p):
    size = len(matrix)
    augmented = [
        [value % p for value in row] + [int(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column] % p)
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = pow(augmented[column][column], -1, p)
        augmented[column] = [scale * value % p for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                (x - scale * y) % p
                for x, y in zip(augmented[row], augmented[column])
            ]
    return [row[size:] for row in augmented]


def schur_descend(matrix, q, p):
    """Return the sign-normalized alternating Schur complement on U."""

    universe = list(range(len(matrix)))
    q = tuple(sorted(q))
    u = [i for i in universe if i not in q]
    if not q:
        return u, [row[:] for row in matrix]
    q_inverse = inverse(principal(matrix, q), p)
    # In block form [Q B; -B^T D], the Pfaffian complement is D+B^T Q^-1 B.
    result = [[0] * len(u) for _ in u]
    for i, left in enumerate(u):
        for j, right in enumerate(u):
            correction = sum(
                matrix[q[a]][left] * q_inverse[a][b] * matrix[q[b]][right]
                for a in range(len(q))
                for b in range(len(q))
            )
            result[i][j] = (matrix[left][right] + correction) % p
    # Reordering Q before a selected B gives prod_{b in B} s_b.
    signs = [(-1) ** sum(qpoint > point for qpoint in q) for point in u]
    for i in range(len(u)):
        for j in range(len(u)):
            result[i][j] = result[i][j] * signs[i] * signs[j] % p
    return u, result


def random_alternating(size, p, rng):
    matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            matrix[i][j] = rng.randrange(p)
            matrix[j][i] = -matrix[i][j] % p
    return matrix


def check_prime(p):
    rng = Random(1000 + p)
    n = 2 * p - 2
    qsize = p - 5
    for _ in range(12):
        matrix = random_alternating(n, p, rng)
        q = next(
            q for q in combinations(range(n), qsize)
            if pfaffian(principal(matrix, q), p)
        )
        qpf = pfaffian(principal(matrix, q), p)
        u, complement = schur_descend(matrix, q, p)
        assert len(u) == p + 3
        for b in combinations(range(len(u)), 4):
            original_indices = tuple(sorted(q + tuple(u[index] for index in b)))
            left = pfaffian(principal(matrix, original_indices), p)
            right = qpf * pfaffian(principal(complement, b), p) % p
            assert left == right
    print(f"p={p}: 12 random exact Schur/Pfaffian descents PASS")


if __name__ == "__main__":
    for prime in (5, 7, 11):
        check_prime(prime)
    print("sign-normalized 4-Pfaffian descent identity: VERIFIED")
