#!/usr/bin/env python3
"""Exact coefficient-eight boundary calculation over F_32.

This independently verifies the finite assertion used in
f32_prefix8_affine_boundary.md:

  for U subset F_32 minus {0,1}, |U|=15, e_1(U)=...=e_7(U)=0,

the set of possible e_8(U) is exactly the asserted 16-element set.

The two 15-point halves are exhaustively enumerated.  For each subset A of
the first half, the first seven coefficients required of its complement B
are E_A(t)^(-1) modulo t^8.  A dictionary over every subset B of the second
half gives all and only the matching 15-subsets U=A union B.  No SAT solver,
randomness, or precomputed witness list is used.
"""

MODULUS = 0b100101  # X^5 + X^2 + 1
MAX_DEGREE = 8


def multiply(left, right):
    answer = 0
    while right:
        if right & 1:
            answer ^= left
        right >>= 1
        left <<= 1
        if left & 32:
            left ^= MODULUS
    return answer & 31


PRODUCT = tuple(tuple(multiply(x, y) for y in range(32)) for x in range(32))


def multiply_series(left, right, degree):
    answer = [0] * (degree + 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            if i + j <= degree:
                answer[i + j] ^= PRODUCT[x][y]
    return tuple(answer)


def add_point(series, point):
    """Multiply a truncated E-series by 1 + point*t."""

    answer = list(series)
    for degree in range(MAX_DEGREE, 0, -1):
        answer[degree] ^= PRODUCT[point][answer[degree - 1]]
    return tuple(answer)


def inverse_prefix(series):
    """Return E(t)^(-1) modulo t^8 for E(0)=1."""

    answer = [1] + [0] * 7
    for degree in range(1, 8):
        value = 0
        for i in range(1, degree + 1):
            value ^= PRODUCT[series[i]][answer[degree - i]]
        answer[degree] = value
    return tuple(answer)


def enumerate_subsets(points):
    """Return (size, E-series, mask) for every subset of a 15-point half."""

    records = [(0, (1,) + (0,) * MAX_DEGREE, 0)] * (1 << len(points))
    for mask in range(1, 1 << len(points)):
        lowest_bit = mask & -mask
        point_index = lowest_bit.bit_length() - 1
        size, series, _ = records[mask ^ lowest_bit]
        records[mask] = (size + 1, add_point(series, points[point_index]), mask)
    return records


def main():
    # The field elements have the five-bit encodings 0,...,31.  Splitting
    # F \ {0,1} into these two 15-point sets is merely a partition; every
    # 15-subset is represented once as A union B.
    left_points = tuple(range(2, 17))
    right_points = tuple(range(17, 32))
    left = enumerate_subsets(left_points)
    right = enumerate_subsets(right_points)

    # Key only by coefficients through degree seven.  Multiple right-hand
    # subsets, if present, are retained, so this is an exhaustive count.
    right_index = {}
    for size, series, mask in right:
        right_index.setdefault((size, series[1:8]), []).append((series, mask))

    eighth_values = set()
    witnesses = []
    for left_size, left_series, left_mask in left:
        desired_right = inverse_prefix(left_series)
        for right_series, right_mask in right_index.get(
            (15 - left_size, desired_right[1:8]), ()
        ):
            product = multiply_series(left_series, right_series, MAX_DEGREE)
            assert product[:8] == (1,) + (0,) * 7
            eighth_values.add(product[8])
            witnesses.append((left_mask, right_mask, product[8]))

    expected = {
        1, 3, 5, 6, 7, 12, 17, 20,
        21, 22, 23, 24, 25, 26, 28, 29,
    }
    assert len(witnesses) == 16
    assert eighth_values == expected
    assert 0 not in eighth_values
    assert len(eighth_values) == 16 < 31

    # Directly reconstruct every printed witness as a final guard against
    # accidental collisions in the indexing representation.
    for left_mask, right_mask, eighth in witnesses:
        subset = {
            left_points[i] for i in range(15) if left_mask & (1 << i)
        } | {
            right_points[i] for i in range(15) if right_mask & (1 << i)
        }
        assert len(subset) == 15
        series = (1,) + (0,) * MAX_DEGREE
        for point in subset:
            series = add_point(series, point)
        assert series[1:8] == (0,) * 7
        assert series[8] == eighth

    print("F_32 coefficient-eight affine boundary: PASS")
    print("15-subsets with e_1=...=e_7=0:", len(witnesses))
    print("possible e_8 values:", sorted(eighth_values))


if __name__ == "__main__":
    main()
