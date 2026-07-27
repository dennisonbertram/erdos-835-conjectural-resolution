#!/usr/bin/env python3
"""Exact audit of general H2 rigidity under a hypothetical O_k -> K_{k+1} cover.

This verifier uses only the Python standard library.  The finite scans are
regression checks; the all-parameter arguments are proved in README.md.
"""

from fractions import Fraction
from math import comb


CHECKS = 0


def check(condition, message):
    """Raise on a failed exact check and count successful checks."""
    global CHECKS
    if not condition:
        raise AssertionError(message)
    CHECKS += 1


def theta(k, module):
    """Odd-graph eigenvalue at Johnson harmonic degree ``module``."""
    return (-1) ** module * (k - module)


def eberlein(k, relation, module):
    """Johnson distance-``relation`` eigenvalue on harmonic ``module``."""
    return sum(
        (-1) ** (relation - term)
        * comb(k - 1 - term, relation - term)
        * comb(k - 1 - module, term)
        * comb(k + term - module, term)
        for term in range(relation + 1)
    )


def h_certificate(value):
    """The quartic support certificate, evaluated exactly."""
    return Fraction(
        (5 * value - 6) * (value + 3) * (value - 2) * (value + 1),
        5,
    )


def h2_weights(k):
    """Forced four-point spectral measure, keyed by module index."""
    return {
        2: Fraction(1, k + 1),
        k - 3: Fraction(2 * k - 3, 5 * (k + 1)),
        k - 2: Fraction(4, 15),
        k - 1: Fraction(1, 3),
    }


def moments(k, top):
    """Moments of the forced H2 measure through ``top``."""
    weights = h2_weights(k)
    return [
        sum(weight * theta(k, module) ** power for module, weight in weights.items())
        for power in range(top + 1)
    ]


def relation_valency(k, intersection):
    """Formal fibre intersection number n_s from design binomial inversion."""
    sign = (-1) ** (intersection + 1)
    numerator = comb(k - 1, intersection) * (comb(k, intersection + 1) + sign * k)
    return Fraction(numerator, k + 1)


def kernel_numerator(k, intersection):
    """Numerator F_s of the normalized degree-two Johnson kernel."""
    s = intersection
    return 2 * (2 * k - 3) * s * (s - 1) - 4 * (k - 2) ** 2 * s + (k - 1) * (k - 2) ** 2


def normalized_h2_kernel(k, intersection):
    """Degree-two projector kernel at intersection s, divided by its diagonal."""
    denominator = k * (k - 1) * (k - 2)
    return Fraction(kernel_numerator(k, intersection), denominator)


def spectral_scalar(k, intersection):
    """A_s eigenvalue on H2 from the four global spectral weights."""
    relation = k - 1 - intersection
    return sum(
        weight * eberlein(k, relation, module)
        for module, weight in h2_weights(k).items()
    )


def closed_scalar(k, intersection):
    """A_s eigenvalue on H2 from n_s times the normalized kernel."""
    return relation_valency(k, intersection) * normalized_h2_kernel(k, intersection)


def is_prime(value):
    """Deterministic trial-division primality test for the scan range."""
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def audit_symbolic_family(k):
    """Audit the exact formulas at one even parameter k."""
    check(k >= 6 and k % 2 == 0, f"invalid control parameter k={k}")
    support = {2, k - 3, k - 2, k - 1}
    weights = h2_weights(k)

    check(set(weights) == support, f"support indices failed at k={k}")
    check(
        {theta(k, module) for module in support} == {k - 2, -3, 2, -1},
        f"support spectral points failed at k={k}",
    )
    check(sum(weights.values()) == 1, f"weights do not sum to one at k={k}")
    check(
        all(weight > 0 for weight in weights.values()),
        f"nonpositive weight at k={k}",
    )

    spectrum = [theta(k, module) for module in range(k)]
    check(
        all(h_certificate(value) >= 0 for value in spectrum),
        f"quartic sign failed at k={k}",
    )
    check(
        {value for value in spectrum if h_certificate(value) == 0} == {-3, 2, -1},
        f"quartic zero set failed at k={k}",
    )

    mm = moments(k, 4)
    expected_m3 = (k - 2) * (k - 5)
    expected_m4 = k**3 - 9 * k**2 + 33 * k - 28
    check(mm[:3] == [1, 0, k], f"moments 0..2 failed at k={k}")
    check(mm[3] == expected_m3, f"third moment failed at k={k}")
    check(mm[4] == expected_m4, f"fourth moment failed at k={k}")

    pair_counts = [comb(k - 2, 2), Fraction(k - 2, 2), 0]
    pair_coefficient = pair_counts[0] - 2 * pair_counts[1]
    check(
        pair_coefficient == Fraction((k - 2) * (k - 5), 2),
        f"pair-incidence coefficient failed at k={k}",
    )
    check(
        [
            pair_counts[0]
            + (pair_counts[1] - pair_counts[0]) * membership
            + pair_coefficient * (membership == 2)
            for membership in range(3)
        ]
        == pair_counts,
        f"pair-incidence interpolation failed at k={k}",
    )

    lower = (
        Fraction(h_certificate(k - 2), k + 1)
        - Fraction(4, 5) * expected_m3
        + Fraction(37, 5) * k
        - Fraction(36, 5)
    )
    check(lower == expected_m4, f"quartic lower bound failed at k={k}")

    full_distance_two_valency = comb(k - 1, 2) * comb(k, 2)
    distance_two_eigenvalue = eberlein(k, 2, 2)
    polynomial = k**3 - 11 * k**2 + 34 * k - 28
    check(
        distance_two_eigenvalue == Fraction((k - 1) * polynomial, 4),
        f"distance-two Eberlein value failed at k={k}",
    )
    average_relation_scalar = (
        relation_valency(k, k - 3) * distance_two_eigenvalue / full_distance_two_valency
    )
    check(
        average_relation_scalar == Fraction(polynomial, 4),
        f"average A_(k-3) scalar failed at k={k}",
    )
    check(
        k * (2 * k - 1) + 4 * average_relation_scalar == expected_m4,
        f"average fourth-moment equality failed at k={k}",
    )

    valencies = {}
    scalars = {}
    for intersection in range(k):
        valency = relation_valency(k, intersection)
        from_spectrum = spectral_scalar(k, intersection)
        from_kernel = closed_scalar(k, intersection)
        check(
            from_spectrum == from_kernel,
            f"scalar formulas disagree at k={k}, s={intersection}",
        )
        check(
            abs(normalized_h2_kernel(k, intersection)) <= 1,
            f"projector-kernel Perron bound failed at k={k}, s={intersection}",
        )
        valencies[intersection] = valency
        scalars[intersection] = from_spectrum

    fibre_size = Fraction(comb(2 * k - 1, k - 1), k + 1)
    check(sum(valencies.values()) == fibre_size, f"valency sum failed at k={k}")
    check(
        (valencies[0], valencies[k - 2], valencies[k - 1]) == (0, 0, 1),
        f"design-forced boundary valencies failed at k={k}",
    )
    check(sum(scalars.values()) == 0, f"full scalar sum failed at k={k}")
    check(
        sum(scalars[s] for s in range(1, k - 2)) == -1,
        f"nontrivial scalar sum failed at k={k}",
    )
    check(
        (scalars[0], scalars[k - 2], scalars[k - 1]) == (0, 0, 1),
        f"boundary scalars failed at k={k}",
    )
    check(
        scalars[1] == Fraction((k - 2) * (k - 5), 2),
        f"R eigenvalue failed at k={k}",
    )
    return valencies, scalars


def audit_prime_range(limit):
    """Finite search of elementary arithmetic conditions at prime k+1."""
    prime_count = 0
    relation_count = 0
    largest = None

    for prime in range(7, limit + 1, 2):
        if not is_prime(prime):
            continue
        prime_count += 1
        largest = prime
        k = prime - 1
        denominator = k * (k - 1) * (k - 2)
        dimension = (2 * k - 1) * (k - 2)
        fibre_size = comb(2 * k - 1, k - 1) // prime

        choose_k_minus_one_s = 1
        choose_k_s_plus_one = k
        valency_sum = 0
        scalar_sum = 0

        for intersection in range(k):
            relation_count += 1
            s = intersection
            sign = (-1) ** (s + 1)
            bracket = choose_k_s_plus_one + sign * k

            check(
                bracket % prime == 0,
                f"prime binomial congruence failed at p={prime}, s={s}",
            )
            quotient = bracket // prime
            valency = choose_k_minus_one_s * quotient
            check(valency >= 0, f"negative valency at p={prime}, s={s}")

            numerator = valency * kernel_numerator(k, s)
            check(
                numerator % denominator == 0,
                f"nonintegral scalar at p={prime}, s={s}",
            )
            scalar = numerator // denominator
            check(abs(scalar) <= valency, f"Perron failure at p={prime}, s={s}")

            first_congruence = kernel_numerator(k, s) + 2 * s * (s + 1)
            second_congruence = kernel_numerator(k, s) - 2 * s * (s - 1)
            third_congruence = kernel_numerator(k, s) + 2 * (s + 1) * (3 * s + 2)
            check(
                first_congruence % (k - 1) == 0,
                f"mod k-1 identity failed at p={prime}, s={s}",
            )
            check(
                second_congruence % (2 * (k - 2)) == 0,
                f"mod 2(k-2) identity failed at p={prime}, s={s}",
            )
            check(
                third_congruence % (2 * k) == 0,
                f"mod 2k identity failed at p={prime}, s={s}",
            )
            check(
                valency * (s + 1) % k == 0,
                f"k | n_s(s+1) failed at p={prime}, s={s}",
            )

            residual_square_budget = (
                fibre_size * valency - valency**2 - dimension * scalar**2
            )
            check(
                residual_square_budget >= 0,
                f"negative H2 residual square budget at p={prime}, s={s}",
            )

            valency_sum += valency
            scalar_sum += scalar

            if s + 1 < k:
                choose_k_minus_one_s = choose_k_minus_one_s * (k - 1 - s) // (s + 1)
                choose_k_s_plus_one = choose_k_s_plus_one * (k - s - 1) // (s + 2)

        check(valency_sum == fibre_size, f"prime valency sum failed at p={prime}")
        check(scalar_sum == 0, f"prime scalar sum failed at p={prime}")

        for module in (2, k - 3, k - 2, k - 1):
            global_dimension = comb(2 * k - 1, module) - comb(2 * k - 1, module - 1)
            check(
                global_dimension >= dimension,
                f"global eigenspace too small at p={prime}, module={module}",
            )

    return prime_count, relation_count, largest


def audit_controls(results):
    """Check the explicit k=6 and k=16 tables."""
    _, scalars6 = results[6]
    check(
        [scalars6[s] for s in (1, 2, 3)] == [2, -2, -1],
        "k=6 scalar control failed",
    )

    _, scalars16 = results[16]
    expected16 = [
        77,
        1488,
        13689,
        52000,
        75933,
        -24024,
        -162591,
        -108108,
        42185,
        73216,
        30537,
        5148,
        449,
    ]
    check(
        [scalars16[s] for s in range(1, 14)] == expected16,
        "k=16 scalar control failed",
    )
    check(moments(6, 4)[4] == 62, "k=6 fourth-moment control failed")
    check(moments(16, 4)[4] == 2292, "k=16 fourth-moment control failed")


def main():
    """Run exact family checks and the explicitly bounded prime scan."""
    family_results = {k: audit_symbolic_family(k) for k in range(6, 202, 2)}
    audit_controls(family_results)
    prime_count, relation_count, largest = audit_prime_range(2003)

    print(f"ALL {CHECKS:,} EXACT CHECKS PASSED")
    print("[theorem regression] every even k=6..200")
    print(
        "[finite prime scan] "
        f"{prime_count} primes p=k+1 through p={largest}; "
        f"{relation_count:,} relation instances"
    )
    print("[controls] k=6 Witt values and the full k=16 scalar table")
    print("Scope: these are necessary conditions; problem #835 remains open.")


if __name__ == "__main__":
    main()
