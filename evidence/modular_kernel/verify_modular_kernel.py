#!/usr/bin/env python3
"""Exact small-prime checks for the modular inclusion-kernel attack."""

from __future__ import annotations

from itertools import combinations
from math import comb

import numpy as np


def inverse_mod(value: int, prime: int) -> int:
    return pow(int(value), -1, prime)


def rref_mod(matrix: np.ndarray, prime: int) -> tuple[np.ndarray, list[int]]:
    reduced = matrix.copy() % prime
    row_count, column_count = reduced.shape
    pivots: list[int] = []
    row = 0
    for column in range(column_count):
        candidates = np.flatnonzero(reduced[row:, column])
        if len(candidates) == 0:
            continue
        pivot_row = row + int(candidates[0])
        reduced[[row, pivot_row]] = reduced[[pivot_row, row]]
        reduced[row] *= inverse_mod(reduced[row, column], prime)
        reduced[row] %= prime
        for other_row in range(row_count):
            if other_row != row and reduced[other_row, column]:
                reduced[other_row] -= (
                    reduced[other_row, column] * reduced[row]
                )
                reduced[other_row] %= prime
        pivots.append(column)
        row += 1
        if row == row_count:
            break
    return reduced, pivots


def nullspace_mod(matrix: np.ndarray, prime: int) -> np.ndarray:
    reduced, pivots = rref_mod(matrix, prime)
    free_columns = [
        column for column in range(matrix.shape[1]) if column not in pivots
    ]
    basis = np.zeros((len(free_columns), matrix.shape[1]), dtype=np.int64)
    for basis_row, free_column in enumerate(free_columns):
        basis[basis_row, free_column] = 1
        for pivot_row, pivot_column in enumerate(pivots):
            basis[basis_row, pivot_column] = -reduced[pivot_row, free_column]
    return basis % prime


def row_rank_mod(rows, prime: int) -> int:
    basis: dict[int, np.ndarray] = {}
    for row in rows:
        vector = np.asarray(row, dtype=np.int64).copy() % prime
        while True:
            support = np.flatnonzero(vector)
            if len(support) == 0:
                break
            pivot = int(support[0])
            if pivot in basis:
                vector -= vector[pivot] * basis[pivot]
                vector %= prime
            else:
                vector *= inverse_mod(vector[pivot], prime)
                vector %= prime
                basis[pivot] = vector
                break
    return len(basis)


def inclusion_matrix(
    point_count: int, row_size: int, column_size: int
) -> tuple[np.ndarray, list[tuple[int, ...]]]:
    columns = list(combinations(range(point_count), column_size))
    column_index = {column: index for index, column in enumerate(columns)}
    rows = list(combinations(range(point_count), row_size))
    matrix = np.zeros((len(rows), len(columns)), dtype=np.int64)
    for row_index, row in enumerate(rows):
        row_set = set(row)
        for extension in combinations(
            [point for point in range(point_count) if point not in row_set],
            column_size - row_size,
        ):
            column = tuple(sorted(row + extension))
            matrix[row_index, column_index[column]] = 1
    return matrix, columns


def check_kernel_and_schur_square(prime: int) -> None:
    k = prime - 1
    point_count = 2 * k
    matrix, columns = inclusion_matrix(point_count, k - 1, k)
    kernel = nullspace_mod(matrix, prime)
    expected_dimension = comb(point_count, k) // prime
    assert len(kernel) == expected_dimension

    column_index = {column: index for index, column in enumerate(columns)}
    complements = np.array(
        [
            column_index[
                tuple(point for point in range(point_count) if point not in column)
            ]
            for column in columns
        ]
    )
    assert np.array_equal(kernel[:, complements], kernel)

    schur_rank = row_rank_mod(
        (
            kernel[left] * kernel[right] % prime
            for left in range(len(kernel))
            for right in range(left, len(kernel))
        ),
        prime,
    )
    assert schur_rank == len(columns) // 2
    print(
        f"p={prime}: N={len(columns)}, dim(K)={len(kernel)}, "
        f"dim(K*K)={schur_rank}"
    )


def local_k4_label(edge: tuple[int, int]) -> int:
    """Label K4 edges by its three one-factors, using 1,2,4 in F_7."""

    first, second = edge
    binary_labels = (0, 1, 2, 3)
    difference = binary_labels[first] ^ binary_labels[second]
    return {1: 1, 2: 2, 3: 4}[difference]


def tensor_counterexample_p7() -> None:
    prime = 7
    groups = (tuple(range(0, 4)), tuple(range(4, 8)), tuple(range(8, 12)))
    matrix, columns = inclusion_matrix(12, 5, 6)
    values = np.zeros(len(columns), dtype=np.int64)

    for column_index, column in enumerate(columns):
        column_set = set(column)
        intersections = [
            tuple(point - group[0] for point in group if point in column_set)
            for group in groups
        ]
        if all(len(intersection) == 2 for intersection in intersections):
            value = 1
            for intersection in intersections:
                value *= local_k4_label(intersection)
            values[column_index] = value % prime

    assert np.any(values != values[0])
    assert np.all(matrix @ values % prime == 0)
    assert np.all(matrix @ (values * values % prime) % prime == 0)
    counts = [int(np.count_nonzero(values == value)) for value in range(prime)]
    assert counts == [708, 72, 72, 0, 72, 0, 0]
    print(f"p=7 tensor counterexample counts: {counts}")


def main() -> None:
    # These exact ranks are small enough to recompute in a few seconds.
    for prime in (3, 5, 7):
        check_kernel_and_schur_square(prime)
    tensor_counterexample_p7()

    p17_dimension = comb(32, 16) // 17
    assert p17_dimension == 35_357_670
    print(f"p=17: predicted full-row-rank kernel dimension {p17_dimension}")
    print("modular-kernel evidence: all checks passed")


if __name__ == "__main__":
    main()
