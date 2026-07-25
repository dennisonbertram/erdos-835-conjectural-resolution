#!/usr/bin/env python3
"""Independent algebra checks used in the five-statistic K18 search.

This verifier does not repeat the MITM search and is not a global-exhaustion
certificate.  It checks only search provenance:

* the 992 one-exchange ratios have unique ordered-pair labels;
* two such ratios are adjacent exactly when their labels share an endpoint;
* inversion through degree eight contains an e6 term, so complementation does
  not descend to this five-statistic quotient and cannot reduce star families
  to top families;
* Burnside's lemma gives exactly 6,778 semilinear prefix orbits.

The actual theorem is instead certified directly, without any exhaustion, by
``f32_five_statistic_k18_verifier.py``.
"""

from itertools import combinations


MODULUS = 0b100101  # X^5 + X^2 + 1.


def multiply(left: int, right: int) -> int:
    raw = 0
    for bit in range(5):
        if right >> bit & 1:
            raw ^= left << bit
    for degree in range(8, 4, -1):
        if raw >> degree & 1:
            raw ^= MODULUS << (degree - 5)
    assert 0 <= raw < 32
    return raw


PRODUCT = tuple(
    tuple(multiply(left, right) for right in range(32))
    for left in range(32)
)


def power(value: int, exponent: int) -> int:
    answer = 1
    while exponent:
        if exponent & 1:
            answer = PRODUCT[answer][value]
        value = PRODUCT[value][value]
        exponent >>= 1
    return answer


def unit_multiply(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    assert len(left) == len(right) == 5
    answer = []
    for degree in range(5):
        value = 0
        for left_degree in range(degree + 1):
            value ^= PRODUCT[left[left_degree]][
                right[degree - left_degree]
            ]
        answer.append(value)
    return tuple(answer)


def unit_inverse(unit: tuple[int, ...]) -> tuple[int, ...]:
    answer = [1]
    for degree in range(1, 5):
        value = 0
        for left_degree in range(1, degree + 1):
            value ^= PRODUCT[unit[left_degree]][
                answer[degree - left_degree]
            ]
        answer.append(value)
    assert unit_multiply(unit, tuple(answer)) == (1, 0, 0, 0, 0)
    return tuple(answer)


def exchange_ratio(numerator: int, denominator: int) -> tuple[int, ...]:
    assert numerator != denominator
    linear_numerator = (1, numerator, 0, 0, 0)
    linear_denominator = (1, denominator, 0, 0, 0)
    return unit_multiply(
        linear_numerator, unit_inverse(linear_denominator)
    )


def verify_rook_graph() -> None:
    labels = tuple(
        (numerator, denominator)
        for numerator in range(32)
        for denominator in range(32)
        if numerator != denominator
    )
    ratios = {
        exchange_ratio(numerator, denominator):
        (numerator, denominator)
        for numerator, denominator in labels
    }
    assert len(labels) == len(ratios) == 32 * 31

    for left_label, right_label in combinations(labels, 2):
        left = exchange_ratio(*left_label)
        right = exchange_ratio(*right_label)
        quotient = unit_multiply(left, unit_inverse(right))
        algebraically_adjacent = quotient in ratios
        shares_endpoint = (
            left_label[0] == right_label[0]
            or left_label[1] == right_label[1]
        )
        assert algebraically_adjacent == shares_endpoint


Monomial = tuple[int, ...]
Polynomial = frozenset[Monomial]
ZERO_MONOMIAL = (0,) * 8


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    return frozenset(set(left) ^ set(right))


def polynomial_multiply(
    left: Polynomial, right: Polynomial
) -> Polynomial:
    answer: set[Monomial] = set()
    for left_monomial in left:
        for right_monomial in right:
            product = tuple(
                x + y for x, y in zip(left_monomial, right_monomial)
            )
            if product in answer:
                answer.remove(product)
            else:
                answer.add(product)
    return frozenset(answer)


def variable(index: int) -> Polynomial:
    exponents = [0] * 8
    exponents[index - 1] = 1
    return frozenset((tuple(exponents),))


def pure_power(index: int, exponent: int) -> Monomial:
    answer = [0] * 8
    answer[index - 1] = exponent
    return tuple(answer)


def verify_complementation_warning() -> None:
    elementary = [frozenset((ZERO_MONOMIAL,))]
    elementary.extend(variable(index) for index in range(1, 9))
    inverse = [frozenset((ZERO_MONOMIAL,))]
    for degree in range(1, 9):
        coefficient: Polynomial = frozenset()
        for index in range(1, degree + 1):
            coefficient = polynomial_add(
                coefficient,
                polynomial_multiply(
                    elementary[index], inverse[degree - index]
                ),
            )
        inverse.append(coefficient)

    assert inverse[1] == frozenset((pure_power(1, 1),))
    assert inverse[2] == frozenset((
        pure_power(1, 2), pure_power(2, 1)
    ))
    assert inverse[3] == frozenset((
        pure_power(1, 3), pure_power(3, 1)
    ))
    e1_squared_e2 = (2, 1, 0, 0, 0, 0, 0, 0)
    assert inverse[4] == frozenset((
        pure_power(1, 4),
        e1_squared_e2,
        pure_power(2, 2),
        pure_power(4, 1),
    ))
    assert inverse[8] == frozenset((
        pure_power(1, 8),
        (6, 1, 0, 0, 0, 0, 0, 0),
        (4, 2, 0, 0, 0, 0, 0, 0),
        (4, 0, 0, 1, 0, 0, 0, 0),
        (2, 0, 0, 0, 0, 1, 0, 0),
        pure_power(2, 4),
        (0, 2, 0, 1, 0, 0, 0, 0),
        (0, 1, 2, 0, 0, 0, 0, 0),
        pure_power(4, 2),
        pure_power(8, 1),
    ))


def frobenius(value: int, exponent: int) -> int:
    for _ in range(exponent):
        value = PRODUCT[value][value]
    return value


def verify_orbit_count() -> None:
    fixed_sum = 0
    for exponent in range(5):
        for scale in range(1, 32):
            fixed_product = 1
            for degree in range(1, 5):
                scale_power = power(scale, degree)
                fixed = sum(
                    value
                    == PRODUCT[scale_power][
                        frobenius(value, exponent)
                    ]
                    for value in range(32)
                )
                fixed_product *= fixed
            fixed_sum += fixed_product
    assert fixed_sum % (5 * 31) == 0
    assert fixed_sum // (5 * 31) == 6778


def main() -> None:
    for value in range(1, 32):
        assert power(value, 31) == 1
    verify_rook_graph()
    verify_complementation_warning()
    verify_orbit_count()
    print("F_32 five-statistic search-provenance checks: PASS")
    print("exchange ratios checked:", 32 * 31)
    print("ratio pairs checked:", (32 * 31) * (32 * 31 - 1) // 2)
    print("inverse e8 missing-coordinate audit: e6 term present")
    print("semilinear prefix orbits:", 6778)
    print("scope: not a global exhaustion certificate")


if __name__ == "__main__":
    main()
