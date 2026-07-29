#!/usr/bin/env python3
"""Exact arithmetic audit for the strengthened Schreier-spectrum theorem.

This is a standard-library verifier.  It checks the design normalisations,
the point and pair modules, the reduced Odd-spectrum sign polynomials and
their extremal measures, the two-step intersection algebra, and the k=6
and k=16 numerical conclusions.  The companion README contains the proofs.
"""

from __future__ import annotations

from fractions import Fraction
from math import ceil, comb


def exact_div(numerator: int, denominator: int) -> int:
    if denominator == 0 or numerator % denominator:
        raise AssertionError(f"nonintegral quotient {numerator}/{denominator}")
    return numerator // denominator


def lambda_s(k: int, s: int) -> int:
    """Number of design blocks through a fixed s-set."""

    v = 2 * k - 1
    r = k - 1
    t = k - 2
    if not 0 <= s <= t:
        raise ValueError("lambda_s is requested only through the design strength")
    return exact_div(comb(v - s, t - s), comb(r - s, t - s))


def odd_spectrum(k: int) -> tuple[int, ...]:
    return tuple((-1) ** j * (k - j) for j in range(1, k))


def q_minus(k: int, theta: int) -> int:
    return (theta + k - 3) * (theta - 2) * (theta + 1)


def q_plus(k: int, theta: int) -> int:
    return (k - 4 - theta) * (theta + 3) * (theta + 1)


def moments(
    support: tuple[int, ...], weights: tuple[Fraction, ...], degrees: tuple[int, ...]
) -> tuple[Fraction, ...]:
    return tuple(
        sum(weight * theta**degree for theta, weight in zip(support, weights))
        for degree in degrees
    )


def verify_design_gram(k: int) -> None:
    """Audit full point/pair rank and the 1/(k+1) design scaling."""

    v = 2 * k - 1
    r = k - 1

    # Products of pair-incidence functions have degree at most four.
    for s in range(5):
        observed = lambda_s(k, s)
        uniform = comb(v - s, r - s)
        if observed * (k + 1) != uniform:
            raise AssertionError("wrong fibre-to-complete-design scaling")

    lam1, lam2, lam3, lam4 = (lambda_s(k, s) for s in range(1, 5))

    # Point Gram: diagonal lambda_1, off-diagonal lambda_2.
    point_constant = lam1 + (v - 1) * lam2
    point_difference = lam1 - lam2
    if point_constant <= 0 or point_difference <= 0:
        raise AssertionError("point-incidence matrix is not full rank")
    if point_constant != r * lam1:
        raise AssertionError("wrong constant eigenvalue of the point Gram")

    # Pair Gram is a linear combination of I, the triangular graph T(v),
    # and J.  T(v) has eigenvalues 2(v-2), v-4, -2.
    pair_constant = lam2 - lam4 + 2 * (v - 2) * (lam3 - lam4) + comb(v, 2) * lam4
    pair_point = lam2 - lam4 + (v - 4) * (lam3 - lam4)
    pair_harmonic = lam2 - lam4 - 2 * (lam3 - lam4)
    if min(pair_constant, pair_point, pair_harmonic) <= 0:
        raise AssertionError("pair-incidence matrix is not full rank")
    if pair_constant != comb(r, 2) * lam2:
        raise AssertionError("wrong constant eigenvalue of the pair Gram")

    m1 = v - 1
    m2 = comb(v, 2) - v
    if (m1, m2) != (2 * k - 2, (2 * k - 1) * (k - 2)):
        raise AssertionError("wrong Johnson harmonic dimensions")

    # Trace of the compressed global idempotent equals scalar times rank.
    if Fraction(m1, k + 1) != Fraction(1, k + 1) * m1:
        raise AssertionError("degree-one idempotent normalisation failed")
    if Fraction(m2, k + 1) != Fraction(1, k + 1) * m2:
        raise AssertionError("degree-two idempotent normalisation failed")

    print(
        f"[gram] k={k}: point Gram eigenvalues "
        f"{point_constant}, {point_difference}; pair Gram eigenvalues "
        f"{pair_constant}, {pair_point}, {pair_harmonic}"
    )


def verify_modules_and_sign_polynomials(k: int) -> None:
    if k < 6 or k % 2:
        raise ValueError("the pair-module theorem is scoped to even k >= 6")

    v = 2 * k - 1
    r = k - 1
    n = exact_div(comb(v, r), k + 1)
    degree = comb(k, 2)
    mu1 = Fraction(-k * k + 4 * k - 2, 2)
    mu2 = Fraction((k - 2) * (k - 5), 2)
    lower = Fraction(-k * k + 6 * k - 6, 2)
    upper = Fraction(k * k - 5 * k - 12, 2)
    h1 = 2 * k - 2
    h2 = (2 * k - 1) * (k - 2)
    if 1 + h1 + h2 > n:
        raise AssertionError("forced modules exceed the fibre")

    # Point-column action.  For p in B, the p-labelled factor contributes
    # k/2 neighbours; for p outside B, the missing edge must avoid p.
    point_out = comb(k - 1, 2)
    point_in = k // 2
    point_mu = point_in - point_out
    if point_mu != mu1:
        raise AssertionError("point-incidence module eigenvalue is wrong")

    # Pair-column action.  Values are indexed by |S cap B| = 0,1,2.
    f0 = comb(k - 2, 2)
    f1 = (k - 2) // 2
    f2 = 0
    linear = f1 - f0
    quadratic = Fraction((k - 2) * (k - 5), 2)
    recovered = (
        Fraction(f0),
        Fraction(f0 + linear),
        Fraction(f0 + 2 * linear) + quadratic,
    )
    if recovered != (Fraction(f0), Fraction(f1), Fraction(f2)):
        raise AssertionError("pair-incidence quotient action is wrong")
    if quadratic != mu2:
        raise AssertionError("pair-module eigenvalue is wrong")

    # Delete theta_1=-(k-1) and theta_2=k-2.
    reduced = tuple(theta for j, theta in enumerate((k,) + odd_spectrum(k)) if j >= 3)
    expected = tuple((-1) ** j * (k - j) for j in range(3, k))
    if reduced != expected:
        raise AssertionError("wrong reduced Odd support")
    if any(q_minus(k, theta) < 0 for theta in reduced):
        raise AssertionError("reduced lower sign polynomial is negative")
    if any(q_plus(k, theta) < 0 for theta in reduced):
        raise AssertionError("reduced upper sign polynomial is negative")

    # Equality measure for the reduced lower endpoint:
    # support {-(k-3), 2, -1}.
    lower_support = (-(k - 3), 2, -1)
    lower_weights = (
        Fraction(k - 2, (k - 4) * (k - 1)),
        Fraction(2 * k - 3, 3 * (k - 1)),
        Fraction(k - 6, 3 * (k - 4)),
    )
    if moments(lower_support, lower_weights, (0, 1, 2, 3)) != (
        Fraction(1),
        Fraction(0),
        Fraction(k),
        2 * lower,
    ):
        raise AssertionError("reduced lower equality measure is wrong")

    # Equality measure for the reduced upper endpoint:
    # support {k-4, -3, -1}.
    upper_support = (k - 4, -3, -1)
    upper_weights = (
        Fraction(k + 3, (k - 3) * (k - 1)),
        Fraction(2, k - 1),
        Fraction(k - 6, k - 3),
    )
    if moments(upper_support, upper_weights, (0, 1, 2, 3)) != (
        Fraction(1),
        Fraction(0),
        Fraction(k),
        2 * upper,
    ):
        raise AssertionError("reduced upper equality measure is wrong")

    # Original lower endpoint: its theta_1 weight and trace budget force
    # exact multiplicity dim(H_1).
    old_support = (-(k - 1), 2, -1)
    old_weights = (
        Fraction(1, k + 1),
        Fraction(2 * k - 1, 3 * (k + 1)),
        Fraction(1, 3),
    )
    if moments(old_support, old_weights, (0, 1, 2, 3)) != (
        Fraction(1),
        Fraction(0),
        Fraction(k),
        2 * mu1,
    ):
        raise AssertionError("old lower endpoint weights are wrong")
    compressed_trace = Fraction(h1, k + 1)
    if compressed_trace / old_weights[0] != h1:
        raise AssertionError("endpoint idempotent budget does not give exact rank")

    # Fourth Odd compression:
    # iota^* A^4 iota = k(2k-1)I + 4 A_{k-3}.
    old_fourth = moments(old_support, old_weights, (4,))[0]
    point_high_relation = Fraction(old_fourth - k * (2 * k - 1), 4)
    expected_point_high = Fraction((k - 2) * (k * k - 5 * k + 2), 4)
    if point_high_relation != expected_point_high:
        raise AssertionError("fourth compression misses the point module")
    high_lower = Fraction(-k * (k - 1), 4)
    high_upper = Fraction(k * (k * k - 4 * k + 2), 4)
    if not high_lower <= point_high_relation <= high_upper:
        raise AssertionError("point module violates fourth-moment PSD interval")

    print(
        f"[spectrum] k={k}: n={n}, modules "
        f"{degree}^1, {mu1}^{h1}, {mu2}^{h2}; "
        f"orthogonal interval=[{lower},{upper}]; "
        f"A_(k-3) nonprincipal interval=[{high_lower},{high_upper}]"
    )


def verify_two_step_algebra(k: int) -> None:
    degree = comb(k, 2)
    high_degree = exact_div(k * (k - 1) * (k - 2), 4)
    low_degree = exact_div(k * (k - 1) * (k - 2) * (k - 3) * (k - 4), 36)
    high_per_centre = exact_div(5 * (k - 2), 2)
    low_per_centre = exact_div((k - 2) * (k - 4), 2)
    high_row_sum = degree * high_per_centre
    low_row_sum = degree * low_per_centre
    if high_row_sum != 5 * high_degree:
        raise AssertionError("five-common-neighbour saturation failed")
    if Fraction(low_row_sum, low_degree) != Fraction(9, k - 3):
        raise AssertionError("wrong average on the low intersection relation")
    if high_row_sum + low_row_sum != degree * (degree - 1):
        raise AssertionError("two-step off-diagonal walk count failed")

    odd_girth_bound = 2 * ceil(Fraction(k - 2, 3)) + 1
    print(
        f"[R^2] k={k}: d={degree}, deg(A_{{k-3}})={high_degree}, "
        f"common=5; deg(A_{{k-4}})={low_degree}, "
        f"weighted row={low_row_sum}, entries<=3; "
        f"odd girth>={odd_girth_bound}"
    )


def verify_witt_control() -> None:
    n = exact_div(comb(11, 5), 7)
    dimensions = (1, 10, 44, 11)
    eigenvalues = (15, -7, 2, -3)
    if n != 66 or sum(dimensions) != n:
        raise AssertionError("wrong Witt module dimensions")
    if sum(m * theta for m, theta in zip(dimensions, eigenvalues)) != 0:
        raise AssertionError("Witt first trace failed")
    if sum(m * theta**2 for m, theta in zip(dimensions, eigenvalues)) != n * 15:
        raise AssertionError("Witt second trace failed")
    if sum(m * theta**3 for m, theta in zip(dimensions, eigenvalues)) != 0:
        raise AssertionError("Witt third trace failed")
    print("[control] k=6 forced modules recover 15^1, (-7)^10, 2^44, (-3)^11")


def verify_k16() -> None:
    k = 16
    n = exact_div(comb(31, 15), 17)
    if n != 17_678_835:
        raise AssertionError("wrong k=16 fibre size")
    kspace = n - (1 + 30 + 434)
    if kspace != 17_678_370:
        raise AssertionError("wrong residual dimension")

    high_degree = 840
    low_degree = 14_560
    q_row = 10_080
    if (
        exact_div(k * (k - 1) * (k - 2), 4) != high_degree
        or exact_div(k * (k - 1) * (k - 2) * (k - 3) * (k - 4), 36) != low_degree
        or comb(k, 2) * exact_div((k - 2) * (k - 4), 2) != q_row
    ):
        raise AssertionError("wrong k=16 intersection arithmetic")

    c4_min = 2_100 * n
    c4_max = 4_620 * n
    if (c4_min, c4_max) != (37_125_553_500, 81_676_217_700):
        raise AssertionError("wrong four-cycle range")
    trace4_min = n * (120 * 239 + 8 * 2_100)
    trace4_max = n * (120 * 239 + 8 * 4_620)
    if (trace4_min // n, trace4_max // n) != (45_480, 65_640):
        raise AssertionError("wrong fourth-trace range")

    # Exact traces forced on the residual K-space by odd girth.
    residual_odd = {
        power: 30 * 97**power - 434 * 77**power - 120**power
        for power in (1, 3, 5, 7, 9)
    }
    residual_second = n * 120 - 120**2 - 30 * 97**2 - 434 * 77**2
    if residual_odd[1] != -30_628 or residual_second != 2_118_590_344:
        raise AssertionError("wrong residual low moments")

    print(
        "[exact] k=16: 120^1, (-97)^30, 77^434, "
        "residual dimension 17,678,370 in [-83,82]"
    )
    print(
        "[exact] k=16: R^2=120I+5A_13+Q, "
        "deg(A_13)=840, supp(Q) in A_12, "
        "Q entries 0..3, Q row sum 10,080"
    )
    print(
        "[exact] k=16: four-cycle range "
        "37,125,553,500..81,676,217,700; "
        f"residual odd traces={residual_odd}"
    )


def main() -> None:
    for k in (6, 16):
        verify_design_gram(k)
        verify_modules_and_sign_polynomials(k)
        verify_two_step_algebra(k)
    verify_witt_control()
    verify_k16()
    print("ALL SCHREIER-SPECTRUM OBSTRUCTION AUDITS PASSED")
    print("SCOPE: stronger necessary theorem only; no contradiction for k=16")


if __name__ == "__main__":
    main()
