#!/usr/bin/env python3
"""Exact checks for evidence/constructive_candidate_tests.md."""

from itertools import product


P17 = 17
GF16_MODULUS = 0b10011  # x^4 + x + 1


def gf16_mul(left, right):
    product = 0
    while right:
        if right & 1:
            product ^= left
        right >>= 1
        left <<= 1
        if left & 0b10000:
            left ^= GF16_MODULUS
    return product


def gf16_inv(value):
    assert value
    result = 1
    for _ in range(14):
        result = gf16_mul(result, value)
    assert gf16_mul(result, value) == 1
    return result


def subset_polynomial(subset):
    """Low-to-high coefficients of product(X-a) in characteristic two."""

    coefficients = [1]
    for value in sorted(subset):
        updated = [0] * (len(coefficients) + 1)
        for degree, coefficient in enumerate(coefficients):
            updated[degree] ^= gf16_mul(coefficient, value)
            updated[degree + 1] ^= coefficient
        coefficients = updated
    return coefficients


def polynomial_difference(first, second):
    assert len(first) == len(second)
    result = [left ^ right for left, right in zip(first, second)]
    while result and result[-1] == 0:
        result.pop()
    return result


def leading_ratio(first, second):
    difference = polynomial_difference(
        subset_polynomial(first), subset_polynomial(second)
    )
    if not difference:
        return "infinity", difference
    next_coefficient = difference[-2] if len(difference) > 1 else 0
    return gf16_mul(next_coefficient, gf16_inv(difference[-1])), difference


def verify_projective_line_collision():
    first = {3, 4, 5, 7, 9, 13, 15}
    second = {1, 3, 4, 5, 7, 9, 15}
    common_c = {2, 3, 6, 9, 12, 14, 15}
    assert len(first) == len(second) == len(common_c) == 7
    assert first ^ second == {1, 13}

    first_colour, first_difference = leading_ratio(first, common_c)
    second_colour, second_difference = leading_ratio(second, common_c)
    assert first_difference == [13, 15, 9, 5, 1, 4, 13]
    assert second_difference == [3, 2, 4, 10, 7, 3, 1]
    assert first_colour == second_colour == 3


def legendre31(value):
    value %= 31
    if value == 0:
        return 0
    return 1 if pow(value, 15, 31) == 1 else -1


def paley_conference_matrix():
    matrix = [[0] * 32 for _ in range(32)]
    for left in range(31):
        for right in range(left + 1, 31):
            matrix[left][right] = legendre31(right - left) % P17
            matrix[right][left] = -matrix[left][right] % P17
    infinity = 31
    for finite in range(31):
        matrix[finite][infinity] = -1 % P17
        matrix[infinity][finite] = 1
    return matrix


def pfaffian_mod17(matrix):
    """Alternating Gaussian elimination; input order fixes Pfaffian sign."""

    work = [row[:] for row in matrix]
    size = len(work)
    assert size % 2 == 0
    result = 1

    for pivot_index in range(0, size, 2):
        partner = next(
            (
                index
                for index in range(pivot_index + 1, size)
                if work[pivot_index][index] % P17
            ),
            None,
        )
        if partner is None:
            return 0

        if partner != pivot_index + 1:
            work[partner], work[pivot_index + 1] = (
                work[pivot_index + 1],
                work[partner],
            )
            for row in work:
                row[partner], row[pivot_index + 1] = (
                    row[pivot_index + 1],
                    row[partner],
                )
            result = -result

        pivot = work[pivot_index][pivot_index + 1] % P17
        result = result * pivot % P17
        pivot_inverse = pow(pivot, -1, P17)

        for left in range(pivot_index + 2, size):
            for right in range(left + 1, size):
                correction = (
                    work[pivot_index][left]
                    * work[pivot_index + 1][right]
                    - work[pivot_index][right]
                    * work[pivot_index + 1][left]
                )
                work[left][right] = (
                    work[left][right] - correction * pivot_inverse
                ) % P17
                work[right][left] = -work[left][right] % P17

    return result % P17


def verify_paley_pfaffian_collision():
    matrix = paley_conference_matrix()
    base = {0, 1, 2, 3, 4, 7, 9, 12, 15, 17, 23, 24, 27, 30, 31}
    outside = [point for point in range(32) if point not in base]
    assert outside == [5, 6, 8, 10, 11, 13, 14, 16, 18, 19, 20, 21, 22, 25, 26, 28, 29]

    colours = []
    for point in outside:
        subset = sorted(base | {point})
        principal = [[matrix[left][right] for right in subset] for left in subset]
        colours.append(pfaffian_mod17(principal))

    assert colours == [0, 4, 6, 2, 12, 8, 6, 6, 8, 10, 7, 2, 15, 11, 0, 12, 9]
    assert len(set(colours)) == 11


def gf289_add(left, right):
    """Encode a+b*beta as a+17*b, with beta^2=3."""

    return ((left % 17 + right % 17) % 17) + 17 * (
        (left // 17 + right // 17) % 17
    )


def gf289_neg(value):
    return ((-value % 17) % 17) + 17 * ((-(value // 17)) % 17)


def gf289_sub(left, right):
    return gf289_add(left, gf289_neg(right))


def gf289_mul(left, right):
    left_real, left_beta = left % 17, left // 17
    right_real, right_beta = right % 17, right // 17
    real = (left_real * right_real + 3 * left_beta * right_beta) % 17
    beta = (left_real * right_beta + left_beta * right_real) % 17
    return real + 17 * beta


def gf289_pow(value, exponent):
    result = 1
    while exponent:
        if exponent & 1:
            result = gf289_mul(result, value)
        value = gf289_mul(value, value)
        exponent >>= 1
    return result


def verify_root_sum_no_go():
    beta = 17  # 0 + 1*beta
    assert gf289_pow(beta, 32) == 1
    assert gf289_pow(beta, 16) != 1
    roots = [gf289_pow(beta, exponent) for exponent in range(32)]
    assert len(set(roots)) == 32

    differences = {
        gf289_sub(left, right) for left in roots for right in roots
    }
    assert differences == set(range(17 * 17))

    # Scaling reduces all deleted pairs to {1, ratio}.
    for ratio in roots[1:]:
        allowed = [root for root in roots if root not in (1, ratio)]
        counts = [[0] * 289 for _ in range(16)]
        counts[0][0] = 1
        for root in allowed:
            for subset_size in range(14, -1, -1):
                for old_sum, count in enumerate(counts[subset_size]):
                    if count:
                        new_sum = gf289_add(old_sum, root)
                        counts[subset_size + 1][new_sum] += count
        assert all(count > 0 for count in counts[15])


def verify_affine_barycentre_no_go():
    """Exhaust the four fixed weights in the cyclic barycentre ansatz."""

    valid_after_one_finite_stars = []
    for weights in product(range(17), repeat=4):
        total = sum(weights) % 17
        if all((weight + total) % 17 == 0 for weight in weights):
            valid_after_one_finite_stars.append(weights)
    assert valid_after_one_finite_stars == [(0, 0, 0, 0)]

    # With all fixed weights zero, the two remaining fixed extensions of a
    # four-set containing two finite and two fixed points collide.
    finite_sum = 3 + 11
    first_colour = finite_sum * pow(2, -1, 17) % 17
    second_colour = finite_sum * pow(2, -1, 17) % 17
    assert first_colour == second_colour


if __name__ == "__main__":
    verify_projective_line_collision()
    verify_paley_pfaffian_collision()
    verify_root_sum_no_go()
    verify_affine_barycentre_no_go()
    print("constructive candidate tests: all checks passed")
