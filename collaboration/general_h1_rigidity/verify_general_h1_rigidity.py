#!/usr/bin/env python3
"""Exact audit of the general even-k H1 rigidity theorem.

The theorem gives necessary conditions for a hypothetical cover
O_k -> K_{k+1}.  The finite scans at the end are controls only; the
general proofs are in README.md.
"""

from fractions import Fraction
from math import comb


def choose(top: int, bottom: int) -> int:
    """Binomial coefficient with the usual zero-outside-range convention."""
    if bottom < 0 or bottom > top:
        return 0
    return comb(top, bottom)


def theta(k: int, module: int) -> int:
    """Odd-graph eigenvalue on global Johnson module ``module``."""
    return (-1) ** module * (k - module)


def eberlein(
    v: int,
    r: int,
    distance: int,
    module: int,
) -> int:
    """Johnson distance-relation eigenvalue."""
    return sum(
        (-1) ** (distance - index)
        * comb(r - index, distance - index)
        * comb(r - module, index)
        * comb(v - r + index - module, index)
        for index in range(distance + 1)
    )


def h1_measure(k: int) -> dict[int, Fraction]:
    """The three forced global Odd-eigenspace weights for even k."""
    return {
        1: Fraction(1, k + 1),
        k - 2: Fraction(2 * k - 1, 3 * (k + 1)),
        k - 1: Fraction(1, 3),
    }


def moments(k: int, top: int) -> list[Fraction]:
    weights = h1_measure(k)
    return [
        sum(weight * theta(k, module) ** power for module, weight in weights.items())
        for power in range(top + 1)
    ]


def p_distance_one(k: int, distance: int) -> int:
    """Johnson distance eigenvalue on the degree-one module."""
    return choose(k - 2, distance) * choose(k, distance) - choose(
        k - 1, distance
    ) * choose(k - 1, distance - 1)


def p_distance_top(k: int, distance: int) -> int:
    """Johnson distance eigenvalue on global module k-1."""
    return (-1) ** distance * choose(k - 1, distance)


def p_distance_next_to_top(k: int, distance: int) -> int:
    """Johnson distance eigenvalue on global module k-2."""
    return (-1) ** distance * (
        choose(k - 1, distance) - 3 * choose(k - 2, distance - 1)
    )


def relation_scalar_from_measure(k: int, distance: int) -> Fraction:
    """H1 scalar of the fibre relation at Johnson distance ``distance``."""
    weights = h1_measure(k)
    v, r = 2 * k - 1, k - 1
    return sum(
        weight * eberlein(v, r, distance, module) for module, weight in weights.items()
    )


def relation_scalar_closed(k: int, distance: int) -> Fraction:
    """Closed factored formula for the same scalar."""
    middle = k * (k - 1) - (2 * k - 1) * distance
    final = comb(k, distance) + (-1) ** distance * k
    return Fraction(
        choose(k - 1, distance) * middle * final,
        k * (k - 1) * (k + 1),
    )


def relation_scalar_integer_numerator(k: int, distance: int) -> int:
    """Integer N_d such that the relation scalar is N_d/(k+1)."""
    endpoint_part = (-1) ** distance * (
        k * choose(k - 1, distance) - (2 * k - 1) * choose(k - 2, distance - 1)
    )
    return p_distance_one(k, distance) + endpoint_part


def fibre_intersection_number(k: int, intersection: int) -> Fraction:
    """Forced row size of the fibre intersection relation."""
    return Fraction(
        comb(k - 1, intersection)
        * (comb(k, intersection + 1) + (-1) ** (intersection + 1) * k),
        k + 1,
    )


def steiner_index(k: int, incidence_degree: int) -> Fraction:
    """Index lambda_i of S(k-2,k-1,2k-1)."""
    v, r, strength = 2 * k - 1, k - 1, k - 2
    return Fraction(
        comb(v - incidence_degree, strength - incidence_degree),
        comb(r - incidence_degree, strength - incidence_degree),
    )


def factorisation(number: int) -> dict[int, int]:
    """Small exact trial-division factorisation used only by the audit."""
    result: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            result[divisor] = result.get(divisor, 0) + 1
            number //= divisor
        divisor += 1
    if number > 1:
        result[number] = result.get(number, 0) + 1
    return result


def has_only_extreme_base_p_digits(number: int, prime: int) -> bool:
    """Whether every base-p digit is 0 or p-1."""
    while number:
        digit = number % prime
        if digit not in (0, prime - 1):
            return False
        number //= prime
    return True


def scalar_integrality_criterion(k: int) -> bool:
    """The proved arithmetic criterion for all H1 scalars to be integral."""
    n = k + 1
    factors = factorisation(n)
    if any(exponent != 1 for exponent in factors.values()):
        return False
    return all(
        has_only_extreme_base_p_digits(n // prime - 1, prime) for prime in factors
    )


def all_scalars_integral(k: int) -> bool:
    return all(
        relation_scalar_closed(k, distance).denominator == 1 for distance in range(k)
    )


def is_prime(number: int) -> bool:
    factors = factorisation(number)
    return len(factors) == 1 and next(iter(factors.values())) == 1


def audit_one(k: int) -> dict[int, Fraction]:
    assert k >= 4 and k % 2 == 0
    weights = h1_measure(k)
    assert sum(weights.values()) == 1
    assert [theta(k, module) for module in weights] == [-(k - 1), 2, -1]

    def certificate(value: int) -> int:
        return (value - 2) * (value + 1)

    residual = [module for module in range(k) if module != 1]
    assert all(certificate(theta(k, module)) >= 0 for module in residual)
    assert {
        theta(k, module) for module in residual if certificate(theta(k, module)) == 0
    } == {2, -1}
    assert Fraction(certificate(-(k - 1)), k + 1) == k - 2

    mu1 = Fraction(-k * k + 4 * k - 2, 2)
    moment_list = moments(k, 3)
    assert moment_list[:3] == [1, 0, k]
    assert moment_list[3] == 2 * mu1

    scalars: dict[int, Fraction] = {}
    for distance in range(k):
        direct = relation_scalar_from_measure(k, distance)
        closed = relation_scalar_closed(k, distance)
        numerator = relation_scalar_integer_numerator(k, distance)
        assert direct == closed == Fraction(numerator, k + 1)
        assert Fraction(numerator).denominator == 1

        assert eberlein(2 * k - 1, k - 1, distance, 1) == p_distance_one(
            k,
            distance,
        )
        assert eberlein(2 * k - 1, k - 1, distance, k - 2) == p_distance_next_to_top(
            k, distance
        )
        assert eberlein(2 * k - 1, k - 1, distance, k - 1) == p_distance_top(
            k, distance
        )

        intersection = k - 1 - distance
        profile = fibre_intersection_number(k, intersection)
        multiplier = (2 * k - 1) * intersection - (k - 1) ** 2
        assert closed == profile * Fraction(multiplier, k * (k - 1))
        scalars[intersection] = closed

    # The forced intersection profile satisfies every design moment,
    # even as a rational formal profile at inadmissible parameters.
    profiles = {
        intersection: fibre_intersection_number(k, intersection)
        for intersection in range(k)
    }
    for incidence_degree in range(k - 1):
        left = sum(
            comb(intersection, incidence_degree) * count
            for intersection, count in profiles.items()
        )
        right = comb(k - 1, incidence_degree) * steiner_index(k, incidence_degree)
        assert left == right

    assert profiles[k - 1] == 1
    assert scalars[k - 1] == 1
    assert scalars[0] == 0
    assert scalars[k - 2] == 0
    assert scalars[1] == mu1
    assert sum(scalars[intersection] for intersection in range(k - 1)) == -1
    return scalars


def main() -> None:
    controls = {k: audit_one(k) for k in range(4, 82, 2)}
    assert controls[6][1] == -7
    assert controls[16][1] == -97
    assert controls[16][13] == 623
    assert controls[16][12] == 8918
    assert controls[16][2] == -2282

    # This checks the proved digit criterion against direct exact arithmetic.
    criterion_controls = {
        k: (all_scalars_integral(k), scalar_integrality_criterion(k))
        for k in range(4, 1002, 2)
    }
    assert all(direct == criterion for direct, criterion in criterion_controls.values())

    prime_cases = [
        k for k, (direct, _) in criterion_controls.items() if is_prime(k + 1) and direct
    ]
    composite_digit_survivors = [
        k
        for k, (direct, _) in criterion_controls.items()
        if not is_prime(k + 1) and direct
    ]
    assert not composite_digit_survivors

    # Prime parameters have integral fibre indices; a composite parameter
    # fails at the least-prime-divisor Lucas witness.  This is only a
    # finite control of the general proof in README.md.
    for k in range(4, 302, 2):
        indices_integral = all(
            steiner_index(k, incidence_degree).denominator == 1
            for incidence_degree in range(k - 1)
        )
        assert indices_integral == is_prime(k + 1)

    print("[exact] general even-k H1 support, weights, and relation formulas pass")
    print("[exact] fibre intersection profiles satisfy all design moments")
    print("[exact] direct scalar integrality agrees with the proved digit criterion")
    print(f"[control] prime k+1 cases through 1001: {len(prime_cases)}")
    print("[control] no composite digit-criterion survivor through k=1000")
    print("Scope: the scan is a control, not a proof that no survivor exists.")


if __name__ == "__main__":
    main()
