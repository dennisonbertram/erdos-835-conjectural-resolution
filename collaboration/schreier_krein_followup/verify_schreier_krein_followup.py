#!/usr/bin/env python3
"""Exact audit for the Schreier--Krein follow-up."""

from __future__ import annotations

from fractions import Fraction
from math import comb


def multiplicity(v: int, j: int) -> int:
    return comb(v, j) - (comb(v, j - 1) if j else 0)


def valency(v: int, r: int, i: int) -> int:
    return comb(r, i) * comb(v - r, i)


def johnson_eigenvalue(v: int, r: int, i: int, j: int) -> int:
    """Eigenvalue of Johnson distance-i adjacency on harmonic degree j."""

    return sum(
        (-1) ** (i - t) * comb(r - t, i - t) * comb(r - j, t) * comb(v - r + t - j, t)
        for t in range(i + 1)
    )


def krein(v: int, r: int, a: int, b: int, c: int) -> Fraction:
    n_total = comb(v, r)
    ma = multiplicity(v, a)
    mb = multiplicity(v, b)
    return Fraction(ma * mb, n_total) * sum(
        Fraction(
            johnson_eigenvalue(v, r, i, a)
            * johnson_eigenvalue(v, r, i, b)
            * johnson_eigenvalue(v, r, i, c),
            valency(v, r, i) ** 2,
        )
        for i in range(r + 1)
    )


def moments(measure: dict[int, Fraction], top: int) -> tuple[Fraction, ...]:
    return tuple(
        sum(weight * theta**power for theta, weight in measure.items())
        for power in range(top + 1)
    )


def verify_krein_closure() -> None:
    expected_16 = {
        (1, 1): {
            0: Fraction(30),
            1: Fraction(1, 232),
            2: Fraction(465, 232),
        },
        (1, 2): {
            1: Fraction(6727, 232),
            2: Fraction(5, 522),
            3: Fraction(217, 72),
        },
        (2, 2): {
            0: Fraction(434),
            1: Fraction(217, 1566),
            2: Fraction(175739, 3132),
            3: Fraction(217, 6750),
            4: Fraction(81809, 13500),
        },
    }
    for pair, expected in expected_16.items():
        observed = {c: q for c in range(8) if (q := krein(31, 15, pair[0], pair[1], c))}
        assert observed == expected
        assert all(q > 0 for q in observed.values())

    observed_6 = {c: q for c in range(3) if (q := krein(11, 5, 1, 1, c))}
    assert observed_6 == {
        0: Fraction(10),
        1: Fraction(1, 27),
        2: Fraction(55, 27),
    }
    assert sum(multiplicity(11, j) for j in range(3)) == comb(11, 2) == 55
    print("[krein] exact H1/H2 products have positive Johnson coefficients")


def verify_h2_support() -> None:
    residual = (8, -7, 6, -5, 4, -3, 2, -1)

    def h(theta: int) -> Fraction:
        return Fraction(
            (5 * theta - 6) * (theta + 3) * (theta - 2) * (theta + 1),
            5,
        )

    assert all(h(theta) >= 0 for theta in residual)
    assert {theta for theta in residual if h(theta) == 0} == {-3, 2, -1}

    measure = {
        14: Fraction(1, 17),
        -3: Fraction(29, 85),
        2: Fraction(4, 15),
        -1: Fraction(1, 3),
    }
    observed = moments(measure, 10)
    assert observed[:4] == (1, 0, 16, 154)
    assert observed[4:7] == (2292, 31_562, 443_180)

    # The residual h-expectation is m4 - 2292.
    fixed_h = Fraction(1, 17) * h(14)
    residual_h_from_moments = (
        observed[4]
        + Fraction(4, 5) * observed[3]
        - Fraction(37, 5) * observed[2]
        + Fraction(36, 5)
        - fixed_h
    )
    assert residual_h_from_moments == 0

    control = {
        4: Fraction(1, 7),
        -3: Fraction(9, 35),
        2: Fraction(4, 15),
        -1: Fraction(1, 3),
    }
    assert moments(control, 3) == (1, 0, 6, 4)
    print("[support] H2 measure and k=6 Witt control verified exactly")


def verify_odd_walk_recurrence() -> None:
    """Expand the Odd distance-matrix recurrence through degree six."""

    k = 16

    def b(distance: int) -> int:
        quotient, parity = divmod(distance, 2)
        return k - quotient - parity

    def c(distance: int) -> int:
        quotient, parity = divmod(distance, 2)
        return quotient + parity

    coefficients = {0: 1}
    powers = {0: coefficients}
    for power in range(1, 7):
        next_coefficients: dict[int, int] = {}
        for distance, coefficient in coefficients.items():
            if distance:
                next_coefficients[distance - 1] = (
                    next_coefficients.get(distance - 1, 0)
                    + coefficient * b(distance - 1)
                )
            next_coefficients[distance + 1] = (
                next_coefficients.get(distance + 1, 0)
                + coefficient * c(distance + 1)
            )
        coefficients = next_coefficients
        powers[power] = coefficients

    assert powers[4] == {
        0: k * (2 * k - 1),
        2: 4 * k - 3,
        4: 4,
    }
    assert powers[5] == {
        1: 6 * k * k - 8 * k + 3,
        3: 12 * k - 14,
        5: 12,
    }
    assert powers[6] == {
        0: k * (6 * k * k - 8 * k + 3),
        2: 18 * k * k - 34 * k + 17,
        4: 36 * k - 52,
        6: 36,
    }
    print("[walks] Odd distance-matrix recurrence verified through degree six")


def verify_compressions_and_trace_budgets() -> None:
    k = 16
    v = 31
    r = 15
    degree = comb(k, 2)
    high_degree = 840
    low_degree = 14_560
    q_row = 10_080

    def kernel_ratio(i: int, j: int) -> Fraction:
        return Fraction(
            johnson_eigenvalue(v, r, i, j),
            valency(v, r, i),
        )

    high_h2 = high_degree * kernel_ratio(2, 2)
    low_h2 = low_degree * kernel_ratio(3, 2)
    assert (high_h2, low_h2) == (449, 5148)

    m4, m5, m6 = 2292, 31_562, 443_180
    assert m4 == k * (2 * k - 1) + 4 * high_h2
    intersection_two_h2 = Fraction(m5 - (12 * k - 14) * 77, 12)
    assert intersection_two_h2 == 1488
    assert m6 == (k * (6 * k * k - 8 * k + 3) + (36 * k - 52) * high_h2 + 36 * low_h2)
    q_h2 = 77**2 - degree - 5 * high_h2
    assert q_h2 == 3564
    assert 3 * low_h2 - q_h2 == 11_880

    expected = {
        0: (1, 120, 14_400, Fraction(0)),
        1: (30, -2_910, 282_270, Fraction(0)),
        2: (434, 33_418, 2_573_186, Fraction(0)),
        3: (4_030, -240_994, 14_417_914, Fraction(32_364, 5)),
        4: (26_970, 1_219_044, 55_256_136, Fraction(776_736, 5)),
        5: (138_446, -4_568_718, 152_547_714, Fraction(1_780_020)),
        6: (566_370, 13_026_510, 312_555_330, Fraction(12_945_600)),
        7: (1_893_294, -28_399_410, 492_984_630, Fraction(66_993_480)),
    }
    for j, wanted in expected.items():
        rank = multiplicity(v, j)
        trace_r = degree * rank * kernel_ratio(k - 2, j)
        trace_r2 = rank * (
            degree + 5 * high_degree * kernel_ratio(2, j) + q_row * kernel_ratio(3, j)
        )
        slack = trace_r2 - trace_r**2 / rank
        assert (rank, trace_r, trace_r2, slack) == wanted
        assert slack >= 0
    print("[moments] higher compressions and all harmonic trace budgets pass")


def main() -> None:
    verify_krein_closure()
    verify_h2_support()
    verify_odd_walk_recurrence()
    verify_compressions_and_trace_budgets()
    print("ALL SCHREIER--KREIN FOLLOW-UP AUDITS PASSED")
    print("SCOPE: exact necessary conditions only; no k=16 contradiction")


if __name__ == "__main__":
    main()
