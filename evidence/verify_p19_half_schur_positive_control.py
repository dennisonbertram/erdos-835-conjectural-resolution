#!/usr/bin/env python3
"""Independent planted positive control for the Schur sign search.

This does not construct a half-link.  It plants an arbitrary dense rank-four
alternating matrix, forgets every edge sign, and checks that the same
8-by-8^6 normalized sign enumeration used by the catalogue search recovers a
rank-four matrix with all planted edge magnitudes.
"""

from __future__ import annotations

from itertools import combinations

P = 19
N = 10


def sign_class(value: int) -> int:
    value %= P
    return min(value, P - value)


def inverse_matrix(matrix: list[list[int]]) -> list[list[int]] | None:
    n = len(matrix)
    left = [[entry % P for entry in row] for row in matrix]
    right = [[int(row == column) for column in range(n)] for row in range(n)]
    for column in range(n):
        pivot = next(
            (row for row in range(column, n) if left[row][column]),
            None,
        )
        if pivot is None:
            return None
        left[column], left[pivot] = left[pivot], left[column]
        right[column], right[pivot] = right[pivot], right[column]
        scale = pow(left[column][column], -1, P)
        left[column] = [(scale * value) % P for value in left[column]]
        right[column] = [(scale * value) % P for value in right[column]]
        for row in range(n):
            if row == column or not left[row][column]:
                continue
            multiplier = left[row][column]
            left[row] = [
                (value - multiplier * pivot_value) % P
                for value, pivot_value in zip(left[row], left[column])
            ]
            right[row] = [
                (value - multiplier * pivot_value) % P
                for value, pivot_value in zip(right[row], right[column])
            ]
    return right


def matrix_vector(
    matrix: list[list[int]],
    vector: list[int],
) -> list[int]:
    return [
        sum(left * right for left, right in zip(row, vector)) % P
        for row in matrix
    ]


def dot(left: list[int], right: list[int]) -> int:
    return sum(a * b for a, b in zip(left, right)) % P


def rank_mod(matrix: list[list[int]]) -> int:
    work = [[entry % P for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = pow(work[rank][column], -1, P)
        work[rank] = [(scale * value) % P for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                (value - multiplier * pivot_value) % P
                for value, pivot_value in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def schur_completion(
    h: list[list[int]],
    x: list[list[int]],
) -> list[list[int]] | None:
    """x is 4-by-6 and the result is the full 10-by-10 matrix."""
    h_inverse = inverse_matrix(h)
    if h_inverse is None:
        return None
    columns = [[x[row][column] for row in range(4)] for column in range(6)]
    transformed = [matrix_vector(h_inverse, column) for column in columns]
    result = [[0] * N for _ in range(N)]
    for row in range(4):
        for column in range(4):
            result[row][column] = h[row][column] % P
    for outside, column in enumerate(columns, start=4):
        for inside in range(4):
            result[inside][outside] = column[inside] % P
            result[outside][inside] = -column[inside] % P
    for left in range(6):
        for right in range(left + 1, 6):
            value = -dot(columns[left], transformed[right]) % P
            result[left + 4][right + 4] = value
            result[right + 4][left + 4] = -value % P
    return result


def dense_planted_matrix() -> tuple[int, list[list[int]]]:
    h = [
        [0, 1, 2, 3],
        [-1, 0, 4, 5],
        [-2, -4, 0, 6],
        [-3, -5, -6, 0],
    ]
    for seed in range(1, 10000):
        x = [
            [
                (seed + 2 * row + 3 * column + row * column) % P
                for column in range(6)
            ]
            for row in range(4)
        ]
        if any(value == 0 for row in x for value in row):
            continue
        matrix = schur_completion(h, x)
        assert matrix is not None
        if all(matrix[left][right] for left, right in combinations(range(N), 2)):
            assert rank_mod(matrix) == 4
            return seed, matrix
    raise RuntimeError("failed to make a dense planted control")


def normalize_switches(matrix: list[list[int]]) -> list[list[int]]:
    epsilon = [1] * N
    for vertex in range(1, 4):
        epsilon[vertex] = 1 if matrix[0][vertex] <= 9 else -1
    for vertex in range(4, N):
        switched = epsilon[0] * matrix[0][vertex] % P
        epsilon[vertex] = 1 if switched <= 9 else -1
    return [
        [
            epsilon[row] * epsilon[column] * matrix[row][column] % P
            for column in range(N)
        ]
        for row in range(N)
    ]


def recover_from_magnitudes(
    magnitudes: list[list[int]],
) -> tuple[int, list[int], list[list[int]]] | None:
    for anchor_pattern in range(8):
        h = [[0] * 4 for _ in range(4)]
        for left in range(4):
            for right in range(left + 1, 4):
                value = magnitudes[left][right]
                if left:
                    bit = 0 if (left, right) == (1, 2) else (
                        1 if (left, right) == (1, 3) else 2
                    )
                    if anchor_pattern & (1 << bit):
                        value = -value % P
                h[left][right] = value
                h[right][left] = -value % P
        h_inverse = inverse_matrix(h)
        if h_inverse is None:
            continue

        states: list[list[list[int]]] = []
        transformed: list[list[list[int]]] = []
        for vertex in range(4, N):
            vertex_states = []
            for state in range(8):
                vector = [magnitudes[inside][vertex] for inside in range(4)]
                for coordinate in range(1, 4):
                    if state & (1 << (coordinate - 1)):
                        vector[coordinate] = -vector[coordinate] % P
                vertex_states.append(vector)
            states.append(vertex_states)
            transformed.append(
                [matrix_vector(h_inverse, vector) for vector in vertex_states]
            )

        assignment = [-1] * 6

        def search(depth: int) -> bool:
            if depth == 6:
                return True
            for state in range(8):
                if all(
                    sign_class(
                        -dot(
                            states[earlier][assignment[earlier]],
                            transformed[depth][state],
                        )
                    )
                    == magnitudes[earlier + 4][depth + 4]
                    for earlier in range(depth)
                ):
                    assignment[depth] = state
                    if search(depth + 1):
                        return True
            return False

        if not search(0):
            continue
        x = [
            [states[column][assignment[column]][row] for column in range(6)]
            for row in range(4)
        ]
        recovered = schur_completion(h, x)
        assert recovered is not None
        return anchor_pattern, assignment, recovered
    return None


def main() -> None:
    seed, planted = dense_planted_matrix()
    planted = normalize_switches(planted)
    magnitudes = [
        [sign_class(planted[row][column]) for column in range(N)]
        for row in range(N)
    ]
    result = recover_from_magnitudes(magnitudes)
    assert result is not None
    anchor_pattern, assignment, recovered = result
    assert rank_mod(recovered) == 4
    assert all(
        sign_class(recovered[left][right]) == magnitudes[left][right]
        for left, right in combinations(range(N), 2)
    )
    print(f"planted_seed={seed}")
    print(f"recovered_anchor_pattern={anchor_pattern}")
    print("recovered_outside_states=" + ",".join(map(str, assignment)))
    print("recovered_rank=4")
    print("schur_sign_enumeration_positive_control=PASS")


if __name__ == "__main__":
    main()
