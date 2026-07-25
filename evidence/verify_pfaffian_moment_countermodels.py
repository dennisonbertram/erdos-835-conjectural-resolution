#!/usr/bin/env python3
"""Exact p=17 countermodels for the low-degree 4-Pfaffian moments."""

from itertools import combinations


P = 17
N = 20


def matmul(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(N)) % P for j in range(N)]
        for i in range(N)
    ]


def rank(matrix):
    work = [row[:] for row in matrix]
    answer = 0
    for column in range(len(work[0])):
        pivot = next((r for r in range(answer, len(work)) if work[r][column] % P), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        scale = pow(work[answer][column], -1, P)
        work[answer] = [scale * value % P for value in work[answer]]
        for row in range(len(work)):
            if row != answer:
                scale = work[row][column]
                work[row] = [
                    (x - scale * y) % P for x, y in zip(work[row], work[answer])
                ]
        answer += 1
    return answer


def pf4(matrix, i, j, k, l):
    return (
        matrix[i][j] * matrix[k][l]
        - matrix[i][k] * matrix[j][l]
        + matrix[i][l] * matrix[j][k]
    ) % P


def check_low_moments(matrix):
    row_sums = [sum(row) % P for row in matrix]
    assert row_sums == [0] * N
    for i, j, k in combinations(range(N), 3):
        values = [pf4(matrix, i, j, k, u) for u in range(N)]
        assert sum(values) % P == 0
        assert sum(value * value for value in values) % P == 0


def rank_two_model():
    s = [0] * N
    t = [0] * N
    s[0], s[1] = 1, -1
    t[2], t[3] = 1, -1
    return [[(s[i] * t[j] - t[i] * s[j]) % P for j in range(N)] for i in range(N)]


def rank_four_square_zero_model():
    # Four disjoint isotropic sum-zero vectors: 1,-1,4,-4 has norm 34=0.
    columns = []
    for start in (0, 4, 8, 12):
        column = [0] * N
        column[start : start + 4] = [1, -1, 4, -4]
        columns.append([value % P for value in column])
    c = [[0] * 4 for _ in range(4)]
    c[0][1], c[1][0] = 1, -1
    c[2][3], c[3][2] = 1, -1
    return [
        [
            sum(columns[a][i] * c[a][b] * columns[b][j] for a in range(4) for b in range(4)) % P
            for j in range(N)
        ]
        for i in range(N)
    ]


if __name__ == "__main__":
    first = rank_two_model()
    check_low_moments(first)
    assert rank(first) == 2
    assert any(value for row in matmul(first, first) for value in row)
    assert all(pf4(first, *quadruple) == 0 for quadruple in combinations(range(N), 4))
    print("rank-2 model: A1=0 and degree-1/2 moments hold, but A^2 != 0")

    second = rank_four_square_zero_model()
    check_low_moments(second)
    assert rank(second) == 4
    assert all(value == 0 for row in matmul(second, second) for value in row)
    nonzero = sum(pf4(second, *quadruple) != 0 for quadruple in combinations(range(N), 4))
    assert nonzero > 0
    print(f"rank-4 model: A1=0, A^2=0, and {nonzero} nonzero 4-Pfaffians")
    print("low-degree star moments alone force neither A^2=0 nor rank<=2")
