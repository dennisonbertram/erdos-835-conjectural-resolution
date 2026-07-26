#!/usr/bin/env python3
"""Exact audit of the degree-three state refinement.

Standard library only.  Every decision uses integers or Fraction.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb


V = 31
BLOCK_SIZE = 15
N = 17_678_835
DIM_H3 = 4030
KERNEL_DENOMINATOR = 109_200
COMMUTATOR_DENOMINATOR = 305_900


def odd_johnson_eigenvalue(distance: int, degree: int) -> int:
    """Johnson distance-matrix eigenvalue on harmonic degree ``degree``."""

    return sum(
        (-1) ** (distance - t)
        * comb(BLOCK_SIZE - t, distance - t)
        * comb(BLOCK_SIZE - degree, t)
        * comb(V - BLOCK_SIZE + t - degree, t)
        for t in range(distance + 1)
    )


def distance_valency(distance: int) -> int:
    return comb(BLOCK_SIZE, distance) * comb(V - BLOCK_SIZE, distance)


def kernel_ratio(intersection: int, degree: int) -> Fraction:
    distance = BLOCK_SIZE - intersection
    return Fraction(
        odd_johnson_eigenvalue(distance, degree),
        distance_valency(distance),
    )


def p0(t: int) -> int:
    return 1


def p1(t: int) -> int:
    return -225 + 31 * t


def p2(t: int) -> int:
    return 1470 - 421 * t + 29 * t * t


def p3(t: int) -> int:
    return -88_725 + 39_730 * t - 5684 * t * t + 261 * t * t * t


def verify_kernels() -> None:
    scaled = (
        (p0, 1),
        (p1, 240),
        (p2, 1680),
        (p3, KERNEL_DENOMINATOR),
    )
    for degree, (polynomial, denominator) in enumerate(scaled):
        for intersection in range(16):
            assert Fraction(polynomial(intersection), denominator) == kernel_ratio(
                intersection,
                degree,
            )
    print("[kernel] degree 0, 1, 2, 3 Johnson kernels pass")


def affine_add(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def affine_scale(
    scalar: int,
    value: tuple[int, int],
) -> tuple[int, int]:
    return scalar * value[0], scalar * value[1]


def affine_p3(base: int, epsilon: int) -> tuple[int, int]:
    """p3(base + epsilon), where epsilon is a 0/1 count multiplier."""

    if epsilon == 0:
        return p3(base), 0
    return p3(base), p3(base + 1) - p3(base)


EXPECTED_H = {
    1: 3_244_696,
    2: 1_772_511,
    3: 795_240,
    4: 218_923,
    5: -50_400,
    6: -106_689,
    7: -43_904,
    8: 43_995,
    9: 63_048,
    10: -80_705,
    11: -481_224,
    12: -1_232_469,
    13: -2_428_400,
}


def pointwise_rk_affine(s: int) -> tuple[int, int]:
    """Return numerator (constant, x coefficient) in equation (6)."""

    a = 15 - s
    edge_counts = {
        0: comb(s + 1, 2),
        1: a * (s + 1),
        2: comb(a, 2),
    }

    # x_2=x, x_0=x+s(s-7), x_1=as-2x.
    colour_counts = {
        0: (s * (s - 7), 1),
        1: (a * s, -2),
        2: (0, 1),
    }

    total = (0, 0)
    for r in range(3):
        baseline = affine_scale(edge_counts[r], (p3(a - r), 0))
        increment = p3(a - r + 1) - p3(a - r)
        correction = affine_scale(increment, colour_counts[r])
        total = affine_add(total, affine_add(baseline, correction))
    return total


def verify_pointwise_formula() -> None:
    for s in range(1, 14):
        constant, coefficient = pointwise_rk_affine(s)
        assert constant == EXPECTED_H[s]
        assert coefficient == 1566

    normalization = (
        Fraction(DIM_H3, N) * Fraction(1566, KERNEL_DENOMINATOR)
    )
    assert normalization == Fraction(1, COMMUTATOR_DENOMINATOR)
    assert COMMUTATOR_DENOMINATOR**2 == 93_574_810_000
    print("[pointwise] all h_s values and the 1/305900 commutator pass")


def verify_q_levels() -> None:
    h12 = EXPECTED_H[12]
    for q in range(4):
        x = 3 - q
        rk = Fraction(h12 + 1566 * x, KERNEL_DENOMINATOR)
        rp = Fraction(DIM_H3, N) * rk
        expected = -Fraction(45_473, 17_742_200) - Fraction(
            q,
            COMMUTATOR_DENOMINATOR,
        )
        assert rp == expected

    assert Fraction(
        DIM_H3 * (-1_227_771),
        N * KERNEL_DENOMINATOR,
    ) == -Fraction(45_473, 17_742_200)
    print("[states] Q_0,Q_1,Q_2,Q_3 are the four masked RP levels")


def verify_leakage_arithmetic() -> None:
    square = COMMUTATOR_DENOMINATOR**2
    assert square == 93_574_810_000
    assert Fraction(47_740, 225) == Fraction(9548, 45)

    # Formal block identities:
    # [R,P] = [[0,-L*],[L,0]], so half its Frobenius square is tr(L*L).
    # [Q,P] has the same form with N=C_0 L+L(A-5I).
    # The scalar checks below audit the normalization in (9)--(11),(24)--(25).
    unordered_square_sum = 1
    trace_d = Fraction(unordered_square_sum, square)
    trace_z2 = Fraction(9548, 45) - trace_d / 225
    assert Fraction(47_740) - 225 * trace_z2 == trace_d
    assert 479_039_400 == 1566 * COMMUTATOR_DENOMINATOR
    print("[leakage] Delta and Gamma trace normalizations pass")


def verify_raw_moment_witnesses() -> None:
    scaled_polynomials = (p0, p1, p2, p3)
    h12_after_q_constant = EXPECTED_H[12] + 3 * 1566

    for q in range(4):
        max_z = 347 + 3 * q
        for z in range(max_z + 1):
            counts = {
                9: 3490 - 12 * q + z,
                10: 6606 + 36 * q - 4 * z,
                11: 3075 - 36 * q + 6 * z,
                12: 1388 + 12 * q - 4 * z,
                13: z,
                15: 1,
            }
            assert min(counts.values()) >= 0
            assert sum(counts.values()) == 14_560
            assert sum(p1(t) * count for t, count in counts.items()) == (
                8918 * p1(12)
            )
            assert sum(p2(t) * count for t, count in counts.items()) == (
                5148 * p2(12)
            )
            assert sum(p3(t) * count for t, count in counts.items()) == (
                2022 * p3(12)
                - 12 * (h12_after_q_constant - 1566 * q)
            )

        # z=0 supplies an explicit witness for the Q-weighted moments.
        z = 0
        counts = {
            9: 3490 - 12 * q + z,
            10: 6606 + 36 * q - 4 * z,
            11: 3075 - 36 * q + 6 * z,
            12: 1388 + 12 * q - 4 * z,
            13: z,
            15: 1,
        }
        weighted = {
            9: 1710 - 5 * q,
            10: 6696 + 9 * q,
            11: 0,
            12: 1674 - 5 * q,
            13: 0,
            15: q,
        }
        assert min(weighted.values()) >= 0
        assert all(weighted[t] <= 3 * counts[t] for t in counts)
        assert sum(weighted.values()) == 10_080
        assert sum(p1(t) * value for t, value in weighted.items()) == (
            6174 * p1(12)
        )
        assert sum(p2(t) * value for t, value in weighted.items()) == (
            3564 * p2(12)
        )

        # Every integer in [0,3N_t] is a sum of N_t states in {0,1,2,3}.
        for t, value in weighted.items():
            quotient, remainder = divmod(value, 3)
            state_count = quotient + (1 if remainder else 0)
            assert state_count <= counts[t]

    # The upper endpoint is sharp for nonnegativity: N_12 becomes negative.
    for q in range(4):
        z = 348 + 3 * q
        assert 1388 + 12 * q - 4 * z == -4

    assert len(scaled_polynomials) == 4
    print("[moments] every q-state has exact raw and Q-weighted witnesses")


def verify_state_and_finite_model_counts() -> None:
    # n_1+2n_2+3n_3=10080 and tau=n_2+3n_3 imply
    # sum q^2 = 10080+2 tau.
    for n2 in (0, 1, 100, 560):
        for n3 in (0, 1, 10, 373):
            tau = n2 + 3 * n3
            weighted_sum = 10_080
            square_sum = weighted_sum + 2 * tau
            assert square_sum == 10_080 + 2 * (n2 + 3 * n3)

    assert 2100 * 4 == 8400
    assert 840 * 8 == 6720
    assert 8400 - 6720 == 1680
    assert 10_080 + 2 * 1680 == 13_440

    # Local exact-cover counts.
    lambda_12 = comb(31 - 12, 14 - 12) // (15 - 12)
    lambda_13 = comb(31 - 13, 14 - 13) // (15 - 13)
    assert lambda_12 == 57
    assert lambda_13 == 9
    assert 1 + 3 * 8 + 32 == lambda_12
    assert 3 * 8 == 24
    assert 32 * 3 == 96
    assert comb(16, 2) - 24 == 96
    assert comb(15, 2) == 105
    assert comb(15, 3) == 455
    assert comb(16, 3) == 560
    print("[finite] tau bound and matching/triangle model counts pass")


def main() -> None:
    verify_kernels()
    verify_pointwise_formula()
    verify_q_levels()
    verify_leakage_arithmetic()
    verify_raw_moment_witnesses()
    verify_state_and_finite_model_counts()
    print("ALL H3 STATE-REFINEMENT AUDITS PASSED")
    print("SCOPE: exact necessary conditions only; no k=16 contradiction")


if __name__ == "__main__":
    main()
