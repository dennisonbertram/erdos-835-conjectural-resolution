#!/usr/bin/env python3
"""Exact standard-library audit for the degree-four Schreier frontier."""

from __future__ import annotations

from fractions import Fraction
from math import ceil, comb


Operator = tuple[Fraction, Fraction, Fraction]


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


def design_lambda(subset_size: int) -> int:
    numerator = comb(31 - subset_size, 14 - subset_size)
    denominator = 15 - subset_size
    assert numerator % denominator == 0
    return numerator // denominator


def fibre_intersection_numbers() -> tuple[int, ...]:
    counts = [0] * 16
    counts[15] = 1
    for r in range(14, -1, -1):
        rhs = comb(15, r) * design_lambda(r)
        counts[r] = rhs - sum(
            comb(s, r) * counts[s] for s in range(r + 1, 16)
        )
    expected = (
        0,
        120,
        3360,
        49_140,
        349_440,
        1_417_416,
        3_363_360,
        4_877_730,
        4_324_320,
        2_362_360,
        768_768,
        147_420,
        14_560,
        840,
        0,
        1,
    )
    assert tuple(counts) == expected
    return tuple(counts)


def operator(
    constant: Fraction | int,
    x_coefficient: Fraction | int = 0,
    y_coefficient: Fraction | int = 0,
) -> Operator:
    return (
        Fraction(constant),
        Fraction(x_coefficient),
        Fraction(y_coefficient),
    )


def add(*operators: Operator) -> Operator:
    return tuple(
        sum((entry[index] for entry in operators), Fraction())
        for index in range(3)
    )  # type: ignore[return-value]


def scale(scalar: Fraction | int, entry: Operator) -> Operator:
    return tuple(Fraction(scalar) * value for value in entry)  # type: ignore[return-value]


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
    """Return Odd-graph distance matrices D_d=p_d(A)."""

    def b(distance: int) -> int:
        quotient, parity = divmod(distance, 2)
        return k - quotient - parity

    def c(distance: int) -> int:
        quotient, parity = divmod(distance, 2)
        return quotient + parity

    polynomials: list[list[Fraction]] = [
        [Fraction(1)],
        [Fraction(0), Fraction(1)],
    ]
    for distance in range(1, k - 1):
        times_a = [Fraction()] + polynomials[distance]
        numerator = subtract_scaled(
            times_a,
            polynomials[distance - 1],
            Fraction(b(distance - 1)),
        )
        denominator = c(distance + 1)
        polynomials.append(
            [coefficient / denominator for coefficient in numerator]
        )
    return tuple(tuple(polynomial) for polynomial in polynomials)


def reduce_mod_q4(polynomial: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    """Reduce modulo q4=t^6-9t^5-59t^4+225t^3+706t^2-1008t-1440."""

    modulus = [
        Fraction(-1440),
        Fraction(-1008),
        Fraction(706),
        Fraction(225),
        Fraction(-59),
        Fraction(-9),
        Fraction(1),
    ]
    result = list(polynomial)
    while len(result) > 6:
        lead = result[-1]
        shift = len(result) - len(modulus)
        result = subtract_scaled(result, modulus, lead, shift)
    return tuple(result + [Fraction()] * (6 - len(result)))


def effect_trace_weight(
    a: int,
    j: int,
    counts: tuple[int, ...],
) -> Fraction:
    v, r = 31, 15
    vertex_count = comb(v, r)
    return Fraction(multiplicity(v, j), vertex_count) * sum(
        counts[s]
        * kernel_ratio(v, r, r - s, a)
        * kernel_ratio(v, r, r - s, j)
        for s in range(16)
    )


def verify_support_and_trace_weights() -> dict[int, Fraction]:
    spectrum = {j: (-1) ** j * (16 - j) for j in range(16)}
    support = (4, 11, 12, 13, 14, 15)

    def q4(theta: int) -> int:
        return (
            (theta - 12)
            * (theta + 5)
            * (theta - 4)
            * (theta + 3)
            * (theta - 2)
            * (theta + 1)
        )

    assert {j for j in range(16) if q4(spectrum[j]) == 0} == set(support)
    assert q4(7) == (
        7**6
        - 9 * 7**5
        - 59 * 7**4
        + 225 * 7**3
        + 706 * 7**2
        - 1008 * 7
        - 1440
    )

    counts = fibre_intersection_numbers()
    weights = {
        j: effect_trace_weight(4, j, counts)
        for j in range(16)
        if effect_trace_weight(4, j, counts)
    }
    expected = {
        4: Fraction(1, 17),
        11: Fraction(10, 119),
        12: Fraction(16, 175),
        13: Fraction(54, 175),
        14: Fraction(128, 525),
        15: Fraction(16, 75),
    }
    assert weights == expected
    assert sum(weights.values()) == 1

    moments = [
        sum(weight * spectrum[j] ** power for j, weight in weights.items())
        for power in range(7)
    ]
    assert moments == [
        Fraction(1),
        Fraction(0),
        Fraction(16),
        Fraction(452, 5),
        Fraction(6624, 5),
        Fraction(72_004, 5),
        Fraction(887_872, 5),
    ]
    print("[support] six-point support and exact trace weights pass")
    return weights


def verify_operator_cone_and_walks() -> None:
    weights = {
        4: operator(Fraction(1, 17)),
        11: operator(Fraction(-26, 153), Fraction(5, 9), Fraction(5, 9)),
        12: operator(Fraction(16, 63), Fraction(-5, 9), Fraction(-8, 63)),
        13: operator(Fraction(6, 7), -1, Fraction(-10, 7)),
        14: operator(0, 1, 0),
        15: operator(0, 0, 1),
    }
    spectrum = {j: (-1) ** j * (16 - j) for j in weights}
    expected_moments = {
        0: operator(1),
        1: operator(0),
        2: operator(16),
        3: operator(116, -70, -40),
        4: operator(1248, 140, 200),
        5: operator(15_220, -2030, -1520),
        6: operator(174_656, 5740, 7120),
    }
    for power, expected in expected_moments.items():
        observed = add(
            *(
                scale(spectrum[j] ** power, entry)
                for j, entry in weights.items()
            )
        )
        assert observed == expected

    compressions = {
        "R": operator(58, -35, -20),
        "A13": operator(188, 35, 50),
        "A2": operator(408, 350, 170),
        "A12": operator(1488, -350, -530),
    }
    assert add(
        compressions["A12"],
        scale(-3, compressions["A2"]),
        scale(8, compressions["A13"]),
        scale(-32, compressions["R"]),
        operator(88),
    ) == operator(0)
    assert add(
        compressions["A2"],
        compressions["A13"],
        scale(11, compressions["R"]),
        operator(-1234),
    ) == operator(0)
    assert add(
        compressions["A12"],
        compressions["R"],
        scale(11, compressions["A13"]),
        operator(-3614),
    ) == operator(0)

    dimension = multiplicity(31, 4)
    assert dimension == 26_970
    x_average = Fraction(128, 525)
    y_average = Fraction(16, 75)
    assert dimension * x_average == Fraction(230_144, 35)
    assert dimension * y_average == Fraction(28_768, 5)

    # The scalar point is strictly inside every endpoint PSD inequality.
    assert x_average > 0 and y_average > 0
    assert x_average + y_average - Fraction(26, 85) == Fraction(18, 119)
    assert 16 - 35 * x_average - 8 * y_average == Fraction(144, 25)
    assert 6 - 7 * x_average - 10 * y_average == Fraction(54, 25)

    expected_averages = {
        "R": Fraction(226, 5),
        "A13": Fraction(1036, 5),
        "A2": Fraction(2648, 5),
        "A12": Fraction(6448, 5),
    }
    for name, entry in compressions.items():
        observed = entry[0] + entry[1] * x_average + entry[2] * y_average
        assert observed == expected_averages[name]

    # Two independent rational, trace-zero diagonal perturbations fit inside
    # the strict cone, proving that the two-operator parametrization has
    # genuine local dimension.
    epsilon = Fraction(1, 1000)
    h_values = (1, -1, 0)
    k_values = (0, 1, -1)
    assert sum(h_values) == sum(k_values) == 0
    assert len(h_values) == len(k_values)
    for h_value, k_value in zip(h_values, k_values):
        x_value = x_average + epsilon * h_value
        y_value = y_average + epsilon * k_value
        assert x_value > 0 and y_value > 0
        assert x_value + y_value > Fraction(26, 85)
        assert 35 * x_value + 8 * y_value < 16
        assert 7 * x_value + 10 * y_value < 6

    print("[cone] exact two-operator PSD cone and restricted walks pass")


def verify_full_right_module() -> None:
    polynomials = odd_distance_polynomials(16)
    assert len(polynomials) == 16
    coefficients: dict[int, tuple[Fraction, Fraction, Fraction]] = {}
    for distance, polynomial in enumerate(polynomials):
        c0, _c1, c2, c3, c4, c5 = reduce_mod_q4(polynomial)
        # Restrict powers A^0,...,A^5 to the fibre.
        constant = c0 + 16 * c2 + 496 * c4
        r_coefficient = 2 * c3 + 178 * c5
        a13_coefficient = 4 * c4
        a2_coefficient = 12 * c5
        # Eliminate A2 via A2=1234 I-11 R-A13 on the right.
        reduced = (
            constant + 1234 * a2_coefficient,
            r_coefficient - 11 * a2_coefficient,
            a13_coefficient - a2_coefficient,
        )
        intersection = distance // 2 if distance % 2 else 15 - distance // 2
        coefficients[intersection] = reduced

    expected = {
        0: (0, 0, 0),
        1: (0, 1, 0),
        2: (1234, -11, -1),
        3: (-2535, 55, 11),
        4: (19_110, -165, -55),
        5: (-59_488, 330, 165),
        6: (84_084, -462, -330),
        7: (-99_099, 462, 462),
        8: (118_404, -330, -462),
        9: (-87_516, 165, 330),
        10: (31_746, -55, -165),
        11: (-9555, 11, 55),
        12: (3614, -1, -11),
        13: (0, 0, 1),
        14: (0, 0, 0),
        15: (1, 0, 0),
    }
    assert coefficients == expected
    print("[relations] all sixteen fibre relations reduce to three right maps")


def verify_quadratic_leakage() -> None:
    dimension = multiplicity(31, 4)
    psi_12 = kernel_ratio(31, 15, 3, 4)
    psi_13 = kernel_ratio(31, 15, 2, 4)
    assert psi_12 == Fraction(31, 350)
    assert psi_13 == Fraction(37, 150)
    trace_r2 = dimension * (120 + 4200 * psi_13 + 10_080 * psi_12)
    assert trace_r2 == 55_256_136

    scalar_r = Fraction(226, 5)
    leakage = trace_r2 - dimension * scalar_r**2
    assert leakage == Fraction(776_736, 5)
    assert leakage == dimension * Fraction(144, 25)
    assert leakage > 0
    print("[quadratic] R^2 trace and positive scalar-witness leakage pass")


def verify_rank_and_colour_coupling() -> None:
    counts = fibre_intersection_numbers()
    weights: dict[int, dict[int, Fraction]] = {}
    for a in range(8):
        weights[a] = {
            j: effect_trace_weight(a, j, counts)
            for j in range(16)
            if effect_trace_weight(a, j, counts)
        }
        expected_support = {a, *range(15 - a, 16)}
        assert set(weights[a]) == expected_support
        assert weights[a][a] == Fraction(1, 17)
        assert sum(weights[a].values()) == 1

    expected_a7 = {
        7: Fraction(1, 17),
        8: Fraction(1748, 284_427),
        9: Fraction(161, 16_731),
        10: Fraction(115, 1859),
        11: Fraction(9200, 117_117),
        12: Fraction(1840, 9009),
        13: Fraction(200, 1001),
        14: Fraction(200, 819),
        15: Fraction(16, 117),
    }
    assert weights[7] == expected_a7

    dimension_4 = multiplicity(31, 4)
    rank_need_4_11 = 17 * weights[4][11] * dimension_4
    assert rank_need_4_11 == Fraction(269_700, 7)
    assert ceil(rank_need_4_11) == 38_529
    assert ceil(rank_need_4_11) < multiplicity(31, 11)

    dimension_7 = multiplicity(31, 7)
    rank_need_7_8 = 17 * weights[7][8] * dimension_7
    assert rank_need_7_8 == Fraction(28_286_136, 143)
    assert ceil(rank_need_7_8) == 197_806
    assert ceil(rank_need_7_8) < multiplicity(31, 8)

    aggregate = {
        j: sum(
            17 * weights[a].get(j, Fraction()) * multiplicity(31, a)
            for a in range(8)
        )
        for j in range(8, 16)
    }
    expected_aggregate = {
        8: Fraction(28_286_136, 143),
        9: Fraction(66_000_984, 143),
        10: Fraction(29_774_880, 13),
        11: Fraction(49_624_800, 13),
        12: Fraction(645_122_400, 77),
        13: Fraction(744_372_000, 77),
        14: Fraction(10_788_000),
        15: Fraction(6_472_800),
    }
    assert aggregate == expected_aggregate
    expected_fill_fractions = {
        8: Fraction(1748, 46_475),
        9: Fraction(1748, 46_475),
        10: Fraction(16, 169),
        11: Fraction(16, 169),
        12: Fraction(80, 539),
        13: Fraction(80, 539),
        14: Fraction(80, 437),
        15: Fraction(80, 437),
    }
    assert {
        j: aggregate[j] / multiplicity(31, j) for j in aggregate
    } == expected_fill_fractions
    assert all(
        ceil(aggregate[j]) <= multiplicity(31, j) for j in aggregate
    )
    low_dimension = sum(multiplicity(31, a) for a in range(8))
    assert low_dimension == comb(31, 7) == 2_629_575
    assert sum(aggregate.values()) == 16 * low_dimension == 42_073_200

    # Explicit scalar a=4 regular-simplex coupling.
    alpha_squares = {
        j: Fraction(17, 16) * weights[4][j] for j in range(11, 16)
    }
    assert alpha_squares == {
        11: Fraction(5, 56),
        12: Fraction(17, 175),
        13: Fraction(459, 1400),
        14: Fraction(136, 525),
        15: Fraction(17, 75),
    }
    assert sum(alpha_squares.values()) == 1
    assert all(
        multiplicity(31, j) >= 16 * dimension_4 for j in range(11, 16)
    )

    # The a=7 diagonal-effect construction only needs these exact capacity
    # inequalities; factorization through E_j then gives a finite Naimark
    # relaxation witness.  Cyclic invariance is obtained by duplicating
    # every scalar slot on a real two-dimensional Fourier module, costing
    # at most two boundary dimensions beyond the desired trace.
    assert sum(
        17 * weights[7][j] * dimension_7 for j in range(8, 16)
    ) == 16 * dimension_7
    assert all(
        2 * ceil(
            Fraction(17, 2) * weights[7][j] * dimension_7
        )
        + 2
        <= multiplicity(31, j)
        for j in range(8, 16)
    )
    print("[coupling] 17-colour rank budgets and relaxation witnesses pass")


def main() -> None:
    verify_support_and_trace_weights()
    verify_operator_cone_and_walks()
    verify_full_right_module()
    verify_quadratic_leakage()
    verify_rank_and_colour_coupling()
    print(
        "PASS: H4 support/operator/rank relaxation is exact and feasible; "
        "this is not a cover."
    )


if __name__ == "__main__":
    main()
