#!/usr/bin/env python3
"""Exact checks for algebraic_construction_no_go.md."""

from itertools import combinations
from math import comb


P = 17
N = 32


def verify_product_sum_lemma():
    """Check all 31*32 fixed-size sumsets and the Fourier error bound."""

    for deleted in range(1, N):
        allowed = [value for value in range(N) if value not in (0, deleted)]
        reachable = [set() for _ in range(16)]
        reachable[0].add(0)
        for value in allowed:
            for size in range(14, -1, -1):
                for old_sum in reachable[size]:
                    reachable[size + 1].add((old_sum + value) % N)
        assert reachable[15] == set(range(N))

    bounds = {}
    for order in (2, 4, 8, 16, 32):
        bounds[order] = sum(
            comb(32 // order, index) * (16 - order * index)
            for index in range(15 // order + 1)
        )
    assert bounds == {2: 102960, 4: 560, 8: 48, 16: 16, 32: 16}

    character_counts = {2: 1, 4: 2, 8: 4, 16: 8, 32: 16}
    error_bound = sum(
        character_counts[order] * bound for order, bound in bounds.items()
    )
    assert error_bound == 104656
    assert comb(30, 15) == 155117520
    assert (comb(30, 15) - error_bound) // 32 == 4844152
    assert comb(30, 15) > error_bound


def add(left, right):
    """Add in F_17[beta]/(beta^2-3), encoded as a+17*b."""

    return ((left % P + right % P) % P) + P * (
        (left // P + right // P) % P
    )


def neg(value):
    return ((-(value % P)) % P) + P * ((-(value // P)) % P)


def sub(left, right):
    return add(left, neg(right))


def mul(left, right):
    left_real, left_beta = left % P, left // P
    right_real, right_beta = right % P, right // P
    real = (left_real * right_real + 3 * left_beta * right_beta) % P
    beta = (left_real * right_beta + left_beta * right_real) % P
    return real + P * beta


def power(value, exponent):
    result = 1
    while exponent:
        if exponent & 1:
            result = mul(result, value)
        value = mul(value, value)
        exponent >>= 1
    return result


def verify_vandermonde_trace_obstruction():
    beta = P
    assert power(beta, 32) == 1
    assert power(beta, 16) != 1
    roots = [power(beta, exponent) for exponent in range(32)]
    assert len(set(roots)) == 32

    inside_exponents = {
        6,
        7,
        8,
        9,
        10,
        13,
        15,
        16,
        18,
        19,
        20,
        25,
        28,
        30,
        31,
    }
    outside_exponents = [
        exponent for exponent in range(32) if exponent not in inside_exponents
    ]

    local_factors = []
    for outside in outside_exponents:
        factor = 1
        for inside in inside_exponents:
            factor = mul(factor, sub(roots[outside], roots[inside]))
        local_factors.append(factor)

    coordinates = [(value % P, value // P) for value in local_factors]
    assert coordinates == [
        (10, 4),
        (4, 3),
        (16, 11),
        (3, 1),
        (0, 8),
        (0, 9),
        (15, 4),
        (1, 4),
        (9, 5),
        (8, 11),
        (0, 15),
        (10, 0),
        (2, 12),
        (6, 6),
        (16, 2),
        (14, 11),
        (5, 8),
    ]

    sum_a_squared = sum(a * a for a, _ in coordinates) % P
    sum_ab = sum(a * b for a, b in coordinates) % P
    sum_b_squared = sum(b * b for _, b in coordinates) % P
    assert (sum_a_squared, sum_ab, sum_b_squared) == (9, 0, 10)

    squares = {value * value % P for value in range(P)}
    assert 5 not in squares

    # Enumerate every projective trace direction as an independent check of
    # the anisotropic quadratic-form proof.
    directions = [(1, slope) for slope in range(P)] + [(0, 1)]
    for real, beta_coefficient in directions:
        values = [
            (real * a + 3 * beta_coefficient * b) % P
            for a, b in coordinates
        ]
        square_sum = sum(value * value for value in values) % P
        predicted = (
            9 * real * real + 5 * beta_coefficient * beta_coefficient
        ) % P
        assert square_sum == predicted
        assert square_sum != 0

    assert sum(value * value for value in range(P)) % P == 0


def rank_mod_17(matrix):
    work = [row[:] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(work))
                if work[candidate][column] % P
            ),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column] % P, -1, P)
        work[row] = [value * inverse % P for value in work[row]]
        for other in range(len(work)):
            if other == row:
                continue
            factor = work[other][column] % P
            if factor:
                work[other] = [
                    (left - factor * right) % P
                    for left, right in zip(work[other], work[row])
                ]
        row += 1
        if row == len(work):
            break
    return row


def verify_determinant_link_obstruction():
    """Audit the finite-field facts in the ordered 14-column-link proof."""

    assert sum(range(P)) % P == 0
    assert sum(pow(value, 8, P) for value in range(P)) % P == 0
    assert pow(P - 1, 8, P) == 1
    assert P - 1 != 1

    # For every possible set of nine finite slopes, the evaluation matrix
    # ((t_f-t_e)^8) is nonsingular.  This independently checks the shifted
    # eighth-power/Vandermonde step used to deduce a_f^8+b_f^8=0.
    for slopes in combinations(range(P), 9):
        shifted_eighth_powers = [
            [pow(right - left, 8, P) for right in slopes]
            for left in slopes
        ]
        assert rank_mod_17(shifted_eighth_powers) == 9

    # At a zero centred partial sum Q_i, the next vector is the parallel
    # mate.  Avoiding a third parallel vector forces the displayed ratio.
    for mate_ratio in range(1, P):
        q_after_pair = (-2 * (1 + mate_ratio)) % P
        if q_after_pair == 0:
            assert mate_ratio == P - 1
            assert pow(mate_ratio, 8, P) != P - 1


def main():
    verify_product_sum_lemma()
    verify_vandermonde_trace_obstruction()
    verify_determinant_link_obstruction()
    print("algebraic construction no-go checks passed")


if __name__ == "__main__":
    main()
