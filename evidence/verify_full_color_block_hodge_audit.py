#!/usr/bin/env python3
"""Exact checks for full_color_block_hodge_audit.md."""

from fractions import Fraction
from math import comb


COLORS = 17
FIBRE_SIZE = 17_678_835


def matmul(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def add_scaled(left, right, scale):
    return [
        [
            left[i][j] + scale * right[i][j]
            for j in range(len(left[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def outer(left, right):
    return [[x * y for y in right] for x in left]


def verify_parameter_arithmetic():
    mu = 570_285
    b = FIBRE_SIZE
    n = comb(31, 15)
    rank_t = comb(30, 15)
    nullity_t = comb(30, 14)
    facets = comb(31, 14)

    assert b == facets // 15 == n // 17 == 31 * mu
    assert n == 300_540_195 == 527 * mu
    assert rank_t == 155_117_520 == 272 * mu
    assert nullity_t == 145_422_675 == 255 * mu
    assert facets == 265_182_525 == 465 * mu
    assert rank_t + nullity_t == n
    assert rank_t % 2 == 0
    assert nullity_t % 2 == 1
    assert rank_t // 2 == 136 * mu

    # Spectral trace compatibility.
    assert 16 * n == 31 * rank_t
    assert 496 * n == 31**2 * rank_t

    t_nullities = []
    gram_nullities = []
    for q in range(9, 18):
        lower_t = (31 * q - 272) * mu
        lower_gram = (31 * q - 255) * mu
        assert lower_t > 0 and lower_gram > 0
        assert lower_t % 2 == (q * b) % 2
        t_nullities.append(lower_t // mu)
        gram_nullities.append(lower_gram // mu)
    assert t_nullities == [7, 38, 69, 100, 131, 162, 193, 224, 255]
    assert gram_nullities == [24, 55, 86, 117, 148, 179, 210, 241, 272]


def verify_fusion_simplex():
    b = FIBRE_SIZE
    mu = 570_285
    n = 527 * mu
    d = 272 * mu

    frame_bound = Fraction(31, 16)
    pair_trace = Fraction(15 * b, 256)
    alpha = Fraction(b, d)
    assert alpha == Fraction(31, 272)

    assert 17 * b == frame_bound * d

    norm = Fraction(b) - alpha * b
    off_diagonal = pair_trace - alpha * b
    assert norm == Fraction(241 * b, 272)
    assert off_diagonal == Fraction(-241 * b, 4352)
    assert off_diagonal == -norm / 16

    # The 17-by-17 Gram matrix of the centred projections is a regular
    # simplex Gram: row sums zero and it is positive semidefinite.
    gram = [
        [norm if i == j else off_diagonal for j in range(17)]
        for i in range(17)
    ]
    assert all(sum(row) == 0 for row in gram)
    # On the sum-zero subspace the eigenvalue is norm-off_diagonal > 0.
    assert norm - off_diagonal == Fraction(17, 16) * norm > 0

    reflection_pair_trace = Fraction(n - 4 * b) + 4 * pair_trace
    assert reflection_pair_trace == Fraction(847 * b, 64)
    assert reflection_pair_trace > 0

    # Trace the tight-reflection sum in two independent ways.
    trace_by_colours = 17 * (n - 2 * b)
    trace_by_spectrum = 17 * (255 * mu) + Fraction(105, 8) * (272 * mu)
    assert trace_by_colours == trace_by_spectrum


def edge_indices():
    result = {}
    index = 0
    for left in range(COLORS):
        for right in range(left + 1, COLORS):
            result[left, right] = index
            index += 1
    assert index == 136
    return result


def verify_voltage_countermodel():
    modulus = FIBRE_SIZE
    indices = edge_indices()

    def voltage(left, right):
        if left < right:
            return pow(2, indices[left, right], modulus)
        return -pow(2, indices[right, left], modulus) % modulus

    # Every pair of base colours has fifteen distinct two-step lifts.
    for left in range(COLORS):
        for right in range(COLORS):
            if left == right:
                continue
            shifts = [
                (voltage(left, middle) + voltage(middle, right)) % modulus
                for middle in range(COLORS)
                if middle not in (left, right)
            ]
            assert len(shifts) == len(set(shifts)) == 15

    # No base triangle lifts to a triangle.
    for first in range(COLORS):
        for second in range(first + 1, COLORS):
            for third in range(second + 1, COLORS):
                cycle_voltage = (
                    voltage(first, second)
                    + voltage(second, third)
                    + voltage(third, first)
                ) % modulus
                assert cycle_voltage != 0

    # The sheet-constant restriction is the transitive skew tournament.
    skew = [
        [
            0 if i == j else (1 if i < j else -1)
            for j in range(COLORS)
        ]
        for i in range(COLORS)
    ]
    assert transpose(skew) == [[-value for value in row] for row in skew]
    ones = [1] * COLORS
    skew_ones = [
        sum(skew[i][j] * ones[j] for j in range(COLORS))
        for i in range(COLORS)
    ]
    assert skew_ones == list(range(16, -17, -2))
    norm_squared = sum(value * value for value in skew_ones)
    assert norm_squared == 1632
    assert 31 * COLORS - norm_squared == -1105

    skew_squared = matmul(skew, skew)
    skew_cubed = matmul(skew_squared, skew)
    cubic_error = add_scaled(skew_cubed, skew, 31)
    assert any(value != 0 for row in cubic_error for value in row)


def verify_full_small_control():
    """The r=1 full Hodge/block system is an exact positive control."""

    operator = [
        [0, 1, -1],
        [-1, 0, 1],
        [1, -1, 0],
    ]
    identity = [[int(i == j) for j in range(3)] for i in range(3)]
    all_ones = [[1] * 3 for _ in range(3)]

    assert transpose(operator) == [
        [-value for value in row] for row in operator
    ]
    squared = matmul(operator, operator)
    expected_squared = add_scaled(all_ones, identity, -3)
    assert squared == expected_squared
    cubed = matmul(squared, operator)
    assert cubed == [[-3 * value for value in row] for row in operator]

    projections = []
    for colour in range(3):
        column = [operator[row][colour] for row in range(3)]
        projection = [
            [Fraction(value, 2) for value in row]
            for row in outer(column, column)
        ]
        assert matmul(projection, projection) == projection
        assert trace(projection) == 1
        projections.append(projection)

    projection_sum = [
        [
            sum(projections[colour][i][j] for colour in range(3))
            for j in range(3)
        ]
        for i in range(3)
    ]
    expected_sum = [
        [Fraction(-squared[i][j], 2) for j in range(3)]
        for i in range(3)
    ]
    assert projection_sum == expected_sum

    for left in range(3):
        for right in range(left + 1, 3):
            assert trace(matmul(projections[left], projections[right])) == Fraction(
                1, 4
            )


def main():
    verify_parameter_arithmetic()
    verify_fusion_simplex()
    verify_voltage_countermodel()
    verify_full_small_control()
    print("full-colour block Hodge arithmetic: VERIFIED")
    print("majority-block Pfaffian nullity bounds: VERIFIED")
    print("projection fusion simplex and non-Clifford reflection trace: VERIFIED")
    print("17-colour actual-fibre voltage countermodel: VERIFIED")
    print("r=1 full Hodge/block positive control: VERIFIED")


if __name__ == "__main__":
    main()
