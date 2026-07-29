#!/usr/bin/env python3
"""Exact audit for the degree-three Schreier support theorem."""

from __future__ import annotations

from fractions import Fraction
from math import ceil, comb


def multiplicity(v: int, j: int) -> int:
    return comb(v, j) - (comb(v, j - 1) if j else 0)


def valency(v: int, r: int, distance: int) -> int:
    return comb(r, distance) * comb(v - r, distance)


def johnson_eigenvalue(v: int, r: int, distance: int, j: int) -> int:
    return sum(
        (-1) ** (distance - t)
        * comb(r - t, distance - t)
        * comb(r - j, t)
        * comb(v - r + t - j, t)
        for t in range(distance + 1)
    )


def kernel_ratio(v: int, r: int, distance: int, j: int) -> Fraction:
    return Fraction(
        johnson_eigenvalue(v, r, distance, j),
        valency(v, r, distance),
    )


def design_lambda(s: int) -> int:
    numerator = comb(31 - s, 14 - s)
    denominator = 15 - s
    assert numerator % denominator == 0
    return numerator // denominator


def fibre_intersection_numbers() -> tuple[int, ...]:
    """Solve the fixed-block S(14,15,31) intersection equations."""

    counts = [0] * 16
    counts[15] = 1
    for r in range(14, -1, -1):
        rhs = comb(15, r) * design_lambda(r)
        counts[r] = rhs - sum(comb(s, r) * counts[s] for s in range(r + 1, 16))
    assert counts[0] == counts[14] == 0
    assert counts[1] == 120
    assert counts[12] == 14_560
    assert counts[13] == 840
    return tuple(counts)


def operator_pair(
    constant: Fraction | int, z_coefficient: Fraction | int
) -> tuple[Fraction, Fraction]:
    return Fraction(constant), Fraction(z_coefficient)


def add(*operators: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (
        sum((operator[0] for operator in operators), Fraction()),
        sum((operator[1] for operator in operators), Fraction()),
    )


def scale(
    scalar: Fraction | int, operator: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    return Fraction(scalar) * operator[0], Fraction(scalar) * operator[1]


def trim(polynomial: list[Fraction]) -> list[Fraction]:
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def subtract_scaled(
    left: list[Fraction],
    right: list[Fraction],
    scalar: Fraction,
    shift: int = 0,
) -> list[Fraction]:
    size = max(len(left), len(right) + shift)
    result = left + [Fraction()] * (size - len(left))
    for index, coefficient in enumerate(right):
        result[index + shift] -= scalar * coefficient
    return trim(result)


def odd_distance_polynomials(k: int) -> tuple[tuple[Fraction, ...], ...]:
    """Return D_d=p_d(A) from the Odd-graph distance recurrence."""

    def b(distance: int) -> int:
        quotient, parity = divmod(distance, 2)
        return k - quotient - parity

    def c(distance: int) -> int:
        quotient, parity = divmod(distance, 2)
        return quotient + parity

    polynomials: list[list[Fraction]] = [[Fraction(1)], [Fraction(0), Fraction(1)]]
    for distance in range(1, k - 1):
        times_a = [Fraction()] + polynomials[distance]
        numerator = subtract_scaled(
            times_a,
            polynomials[distance - 1],
            Fraction(b(distance - 1)),
        )
        denominator = c(distance + 1)
        polynomials.append([coefficient / denominator for coefficient in numerator])
    return tuple(tuple(polynomial) for polynomial in polynomials)


def reduce_mod_q3(polynomial: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    """Reduce a polynomial modulo t^5+11t^4-39t^3-155t^2+206t+312."""

    modulus = [
        Fraction(312),
        Fraction(206),
        Fraction(-155),
        Fraction(-39),
        Fraction(11),
        Fraction(1),
    ]
    result = list(polynomial)
    while len(result) > 5:
        lead = result[-1]
        shift = len(result) - len(modulus)
        result = subtract_scaled(result, modulus, lead, shift)
    return tuple(result + [Fraction()] * (5 - len(result)))


def verify_full_relation_module() -> None:
    """Every restricted distance relation is affine in R on H3."""

    polynomials = odd_distance_polynomials(16)
    assert len(polynomials) == 16
    coefficients: dict[int, tuple[Fraction, Fraction]] = {}
    for distance, polynomial in enumerate(polynomials):
        c0, _c1, c2, c3, c4 = reduce_mod_q3(polynomial)
        alpha = c0 + 16 * c2 + 1984 * c4
        beta = 2 * c3 + 4 * c4
        intersection = distance // 2 if distance % 2 else 15 - distance // 2
        coefficients[intersection] = (alpha, beta)

    expected = {
        0: (0, 0),
        1: (0, 1),
        2: (-1638, -12),
        3: (-2193, 66),
        4: (-26_100, -220),
        5: (35_442, 495),
        6: (-4026, -792),
        7: (72_765, 924),
        8: (-88_110, -792),
        9: (1694, 495),
        10: (-4884, -220),
        11: (14_655, 66),
        12: (2022, -12),
        13: (372, 1),
        14: (0, 0),
        15: (1, 0),
    }
    assert coefficients == expected
    print("[relations] every fibre relation has the audited affine R-action")


def verify_support_and_weights() -> dict[int, tuple[Fraction, Fraction]]:
    odd_spectrum = {j: (-1) ** j * (16 - j) for j in range(16)}
    assert {j: odd_spectrum[j] for j in (3, 12, 13, 14, 15)} == {
        3: -13,
        12: 4,
        13: -3,
        14: 2,
        15: -1,
    }

    def q3(theta: int) -> int:
        return (
            (theta + 13)
            * (theta - 4)
            * (theta + 3)
            * (theta - 2)
            * (theta + 1)
        )

    assert {j for j in range(16) if q3(odd_spectrum[j]) == 0} == {
        3,
        12,
        13,
        14,
        15,
    }
    assert (
        # Coefficients of
        # t^5 + 11t^4 - 39t^3 - 155t^2 + 206t + 312.
        q3(7)
        == 7**5 + 11 * 7**4 - 39 * 7**3 - 155 * 7**2 + 206 * 7 + 312
    )

    weights = {
        3: operator_pair(Fraction(1, 17), 0),
        12: operator_pair(Fraction(10, 119), Fraction(3, 7)),
        13: operator_pair(Fraction(9, 35), Fraction(-3, 7)),
        14: operator_pair(Fraction(3, 5), -1),
        15: operator_pair(0, 1),
    }
    for power, expected in {
        0: operator_pair(1, 0),
        1: operator_pair(0, 0),
        2: operator_pair(16, 0),
        3: operator_pair(-126, 30),
        4: operator_pair(1732, 60),
        5: operator_pair(-21_798, 510),
        6: operator_pair(284_500, 1380),
    }.items():
        observed = add(
            *(
                scale(odd_spectrum[j] ** power, weight)
                for j, weight in weights.items()
            )
        )
        assert observed == expected

    # Independent trace-zero sign certificate on the four removed residual
    # points.  The fixed -13 mass contributes the whole expectation.
    def g(theta: int) -> int:
        return (theta - 4) * (theta + 3) * (theta - 2) * (theta + 1)

    assert {theta: g(theta) for theta in (8, -7, 6, -5)} == {
        8: 2376,
        -7: 2376,
        6: 504,
        -5: 504,
    }
    assert all(g(theta) == 0 for theta in (4, -3, 2, -1))
    assert Fraction(g(-13), 17) == 1800
    print("[support] exact five-eigenspace support and operator weights pass")
    return weights


def verify_compressions_and_trace() -> None:
    v, r, j = 31, 15, 3
    dimension = multiplicity(v, j)
    assert dimension == 4030
    counts = fibre_intersection_numbers()

    # Average compression of a fibre intersection-s relation.
    def average_relation(s: int) -> Fraction:
        return counts[s] * kernel_ratio(v, r, r - s, j)

    averages = {
        1: Fraction(-299, 5),
        2: Fraction(-4602, 5),
        12: Fraction(13_698, 5),
        13: Fraction(1561, 5),
    }
    assert {s: average_relation(s) for s in averages} == averages

    z_average = Fraction(16, 75)
    compressions = {
        "R": operator_pair(-63, 15),
        "A13": operator_pair(309, 15),
        "A2": operator_pair(-882, -180),
        "A12": operator_pair(2778, -180),
    }
    assert {
        1: compressions["R"][0] + compressions["R"][1] * z_average,
        2: compressions["A2"][0] + compressions["A2"][1] * z_average,
        12: compressions["A12"][0] + compressions["A12"][1] * z_average,
        13: compressions["A13"][0] + compressions["A13"][1] * z_average,
    } == averages
    assert add(compressions["A13"], scale(-1, compressions["R"])) == (
        Fraction(372),
        Fraction(0),
    )

    # Restrictions of q3(A) and A q3(A).
    q3_restriction = add(
        scale(12, compressions["A2"]),
        scale(44, compressions["A13"]),
        scale(100, compressions["R"]),
        operator_pair(3288, 0),
    )
    aq3_restriction = add(
        scale(36, compressions["A12"]),
        scale(132, compressions["A2"]),
        scale(368, compressions["A13"]),
        scale(1648, compressions["R"]),
        operator_pair(6528, 0),
    )
    assert q3_restriction == aq3_restriction == operator_pair(0, 0)

    trace_z = Fraction(dimension) * z_average
    assert trace_z == Fraction(12_896, 15)
    trace_r = dimension * averages[1]
    assert trace_r == -240_994
    assert trace_r == -63 * dimension + 15 * trace_z

    # R^2 trace from R^2=120I+5A13+Q.  Q has row sum 10080 and
    # support only on intersection-12 pairs, where the P3 kernel is constant.
    q_average = 10_080 * kernel_ratio(v, r, 3, j)
    trace_r2 = dimension * (
        120 + 5 * averages[13] + q_average
    )
    assert q_average == Fraction(123_282, 65)
    assert trace_r2 == 14_417_914

    z2_lower = trace_z**2 / dimension
    z2_upper = Fraction(47_740, 225)
    assert z2_lower == Fraction(206_336, 1125)
    assert z2_upper == Fraction(9548, 45)
    variance_upper = z2_upper - z2_lower
    assert variance_upper == Fraction(3596, 125)
    rank_lower = ceil(trace_z**2 / z2_upper)
    assert rank_lower == 3484

    # If D=L*L is the R-leakage Gram, then
    # P3 Q P3 = 225 Z^2 - 1965 Z + 2304 I + D.
    # Its scalar polynomial is decreasing and positive on [0,3/5].
    def q_polynomial(z: Fraction) -> Fraction:
        return 225 * z * z - 1965 * z + 2304

    assert q_polynomial(Fraction(0)) == 2304
    assert q_polynomial(Fraction(3, 5)) == 1206
    assert 450 * Fraction(3, 5) - 1965 < 0
    print("[compression] exact Z trace, leakage, variance, and rank bounds pass")


def verify_formal_endpoint_witness() -> None:
    spectrum = {-61: 1914, -60: 396, -59: 720, -58: 1000}
    assert sum(spectrum.values()) == 4030
    assert sum(value * count for value, count in spectrum.items()) == -240_994
    assert (
        sum(value * value * count for value, count in spectrum.items())
        == 14_417_914
    )

    z_spectrum = {
        Fraction(value + 63, 15): count for value, count in spectrum.items()
    }
    assert min(z_spectrum) >= 0
    assert max(z_spectrum) <= Fraction(3, 5)
    assert sum(value * count for value, count in z_spectrum.items()) == Fraction(
        12_896, 15
    )
    assert sum(
        value * value * count for value, count in z_spectrum.items()
    ) == Fraction(9548, 45)
    print("[witness] compatible integral compressed-R moment spectrum passes")


def main() -> None:
    verify_support_and_weights()
    verify_full_relation_module()
    verify_compressions_and_trace()
    verify_formal_endpoint_witness()
    print("ALL DEGREE-THREE SCHREIER SUPPORT AUDITS PASSED")
    print("SCOPE: exact necessary conditions only; no k=16 contradiction")


if __name__ == "__main__":
    main()
