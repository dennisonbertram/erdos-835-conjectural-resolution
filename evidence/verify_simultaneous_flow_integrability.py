#!/usr/bin/env python3
"""Exact checks for evidence/simultaneous_flow_integrability.md."""

from itertools import combinations
from math import comb

from verify_nilpotent_shift_obstruction import verify_negative_controls


def add_formal_term(expression, x, y, base, coefficient=1):
    """Add coefficient*a_xy(base), canonically using reversal."""
    if x > y:
        x, y = y, x
        coefficient = -coefficient
    key = (x, y, tuple(sorted(base)))
    new_value = expression.get(key, 0) + coefficient
    if new_value:
        expression[key] = new_value
    elif key in expression:
        del expression[key]


def formal_hexagon_cancellation(k):
    """Verify K_yz+K_zx+K_xy - same-base triangles = hexagon."""
    points = set(range(2 * k))
    C = set(range(k - 2))
    x, y, z = k - 2, k - 1, k
    expression = {}

    for left, right in ((y, z), (z, x), (x, y)):
        for w in points - C - {left, right}:
            add_formal_term(expression, left, right, C | {w})

    for w in points - C - {x, y, z}:
        base = C | {w}
        for left, right in ((y, z), (z, x), (x, y)):
            add_formal_term(expression, left, right, base, -1)

    expected = {}
    add_formal_term(expected, y, z, C | {x})
    add_formal_term(expected, z, x, C | {y})
    add_formal_term(expected, x, y, C | {z})
    assert expression == expected


def add_sparse_row_to_basis(row, basis, prime):
    """Incremental exact Gaussian elimination of a sparse modular row."""
    while row:
        pivot = max(row)
        coefficient = row[pivot] % prime
        old = basis.get(pivot)
        if old is None:
            inverse = pow(coefficient, -1, prime)
            basis[pivot] = {
                column: value * inverse % prime
                for column, value in row.items()
                if value % prime
            }
            return
        for column, value in old.items():
            new_value = (
                row.get(column, 0) - coefficient * value
            ) % prime
            if new_value:
                row[column] = new_value
            elif column in row:
                del row[column]


def johnson_triangle_ranks(n, r, prime):
    vertices = tuple(combinations(range(n), r))
    vertex_index = {
        frozenset(vertex): index for index, vertex in enumerate(vertices)
    }
    edges = []
    for left_index, left_tuple in enumerate(vertices):
        left = set(left_tuple)
        for removed in left_tuple:
            for added in set(range(n)) - left:
                right = frozenset((left - {removed}) | {added})
                right_index = vertex_index[right]
                if left_index < right_index:
                    edges.append((left_index, right_index))
    edge_index = {edge: index for index, edge in enumerate(edges)}

    adjacency = [[] for _ in vertices]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    stack = [0]
    while stack:
        for neighbor in adjacency[stack.pop()]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    assert len(seen) == len(vertices)

    basis = {}

    def add_triangle(indices):
        row = {}
        directed_edges = zip(indices, indices[1:] + indices[:1])
        for left, right in directed_edges:
            sign = 1
            if left > right:
                left, right = right, left
                sign = -1
            column = edge_index[(left, right)]
            row[column] = (row.get(column, 0) + sign) % prime
            if not row[column]:
                del row[column]
        add_sparse_row_to_basis(row, basis, prime)

    lower_count = 0
    for common_tuple in combinations(range(n), r - 1):
        common = set(common_tuple)
        for triple in combinations(set(range(n)) - common, 3):
            add_triangle([
                vertex_index[frozenset(common | {point})]
                for point in triple
            ])
            lower_count += 1
    lower_rank = len(basis)

    upper_count = 0
    for ambient_tuple in combinations(range(n), r + 1):
        ambient = set(ambient_tuple)
        for triple in combinations(ambient_tuple, 3):
            add_triangle([
                vertex_index[frozenset(ambient - {point})]
                for point in triple
            ])
            upper_count += 1

    cycle_dimension = len(edges) - len(vertices) + 1
    assert len(basis) == cycle_dimension
    return {
        "vertices": len(vertices),
        "edges": len(edges),
        "cycle_dimension": cycle_dimension,
        "lower_count": lower_count,
        "upper_count": upper_count,
        "lower_rank": lower_rank,
        "total_rank": len(basis),
    }


def rank_mod_p(matrix, prime):
    matrix = [[entry % prime for entry in row] for row in matrix]
    row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (candidate for candidate in range(row, len(matrix))
             if matrix[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column], -1, prime)
        matrix[row] = [value * inverse % prime for value in matrix[row]]
        for candidate in range(len(matrix)):
            if candidate == row or not matrix[candidate][column]:
                continue
            factor = matrix[candidate][column]
            matrix[candidate] = [
                (left - factor * right) % prime
                for left, right in zip(matrix[candidate], matrix[row])
            ]
        row += 1
    return row


def verify_rank_two_and_plucker(prime):
    h = tuple(range(prime))
    matrix = [
        [(h[x] - h[y]) % prime for y in range(prime)]
        for x in range(prime)
    ]
    assert rank_mod_p(matrix, prime) == 2
    for x, y, z, w in combinations(range(prime), 4):
        value = (
            matrix[x][y] * matrix[z][w]
            - matrix[x][z] * matrix[y][w]
            + matrix[x][w] * matrix[y][z]
        ) % prime
        assert value == 0


def verify_global_dimensions():
    expected = {
        4: (70, 56, 14),
        6: (924, 792, 132),
        16: (601_080_390, 565_722_720, 35_357_670),
    }
    for k, values in expected.items():
        prime = k + 1
        columns = comb(2 * k, k)
        rows = comb(2 * k, k - 1)
        factors = tuple(k - j for j in range(k))
        assert (columns, rows, columns - rows) == values
        assert all(factor % prime for factor in factors)
        assert columns - rows == columns // prime


def main():
    for k in (4, 6, 16):
        formal_hexagon_cancellation(k)
        verify_rank_two_and_plucker(k + 1)
    verify_global_dimensions()

    k4 = johnson_triangle_ranks(8, 3, 5)
    assert k4 == {
        "vertices": 56,
        "edges": 420,
        "cycle_dimension": 365,
        "lower_count": 560,
        "upper_count": 280,
        "lower_rank": 280,
        "total_rank": 365,
    }
    k6 = johnson_triangle_ranks(12, 5, 7)
    assert k6 == {
        "vertices": 792,
        "edges": 13_860,
        "cycle_dimension": 13_069,
        "lower_count": 27_720,
        "upper_count": 18_480,
        "lower_rank": 10_395,
        "total_rank": 13_069,
    }

    verify_negative_controls()

    print("formal kernel+triangle => cross-star hexagon (k=4,6,16): PASS")
    print("rank-two and Pluecker identities over F5, F7, F17: PASS")
    print(
        "J(8,3)/F5 triangle span: "
        f"{k4['total_rank']}={k4['cycle_dimension']}: PASS"
    )
    print(
        "J(12,5)/F7 triangle span: "
        f"{k6['total_rank']}={k6['cycle_dimension']}: PASS"
    )
    print("k=4 Fano and k=6 Witt negative controls: EXHAUSTIVE PASS")
    print("SIMULTANEOUS FLOW INTEGRABILITY AUDIT: PASS")


if __name__ == "__main__":
    main()
