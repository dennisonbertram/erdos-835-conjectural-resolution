#!/usr/bin/env python3
"""Exact finite checks used by determinant_link_p19.md.

This is deliberately dependency-free.  Its main loop exhausts the
``binom(19,10)=92378`` possible finite slope sets and verifies the
discriminant consequence used in the note: the product of the ten quadratic
characters of P'(t), where P(X)=prod_{s in T}(X-s), is always -1.  It also
checks directly that no set has constant character.  The proof itself does
not rely on this enumeration.
"""

from itertools import combinations
from math import comb, prod


P = 19
N = 10


def legendre(value: int, p: int) -> int:
    """Return 0, +1, or -1 for the quadratic character modulo p."""

    value %= p
    if value == 0:
        return 0
    return 1 if pow(value, (p - 1) // 2, p) == 1 else -1


def derivative_characters(slopes: tuple[int, ...], p: int) -> tuple[int, ...]:
    """Characters of P'(t) for P(X)=prod_{s in slopes}(X-s)."""

    answer = []
    for t in slopes:
        derivative = 1
        for s in slopes:
            if s != t:
                derivative = (derivative * (t - s)) % p
        answer.append(legendre(derivative, p))
    return tuple(answer)


def check_barycentric_identity() -> None:
    """A small exact control for the elementary barycentric lemma."""

    slopes = tuple(range(10))
    denominators = []
    for t in slopes:
        value = 1
        for s in slopes:
            if s != t:
                value = (value * (t - s)) % P
        denominators.append(value)
    weights = [pow(value, -1, P) for value in denominators]
    for exponent in range(9):
        assert sum(weight * pow(t, exponent, P) for weight, t in zip(weights, slopes)) % P == 0


def check_p3_link_control() -> None:
    """p=3 really has a determinant link, so no all-primes claim is made."""

    p = 3
    vectors = ((0, 1), (0, 2), (1, 0), (2, 0))
    for i in range(p + 1):
        labels = []
        for j in range(p + 1):
            if i == j:
                continue
            left, right = vectors[min(i, j)], vectors[max(i, j)]
            labels.append((left[0] * right[1] - left[1] * right[0]) % p)
        assert sorted(labels) == list(range(p))


def exhaust_p19() -> tuple[int, dict[int, int]]:
    """Check every slope set and return survivors and the plus-count histogram."""

    examined = 0
    constant_character_sets = 0
    plus_histogram: dict[int, int] = {}
    for slopes in combinations(range(P), N):
        examined += 1
        chars = derivative_characters(slopes, P)
        assert all(char in (-1, 1) for char in chars)
        # prod_t P'(t)=(-1)^binom(10,2) times a Vandermonde square, so
        # its character is chi(-1)=-1 in F_19.
        assert prod(chars) == -1
        plus_histogram[chars.count(1)] = plus_histogram.get(chars.count(1), 0) + 1
        if len(set(chars)) == 1:
            constant_character_sets += 1
    assert examined == comb(P, N) == 92378
    return constant_character_sets, plus_histogram


def check_small_control() -> None:
    """The p=7 analogue is not vacuous: its weaker condition has examples."""

    p = 7
    n = 4
    found = sum(
        len(set(derivative_characters(slopes, p))) == 1
        for slopes in combinations(range(p), n)
    )
    assert found == 14


def main() -> None:
    check_barycentric_identity()
    check_p3_link_control()
    check_small_control()
    survivors, histogram = exhaust_p19()
    assert survivors == 0
    print("p=19 subsets checked:", comb(P, N))
    print("number of +1 derivative characters:", sorted(histogram.items()))
    print("constant-character survivors:", survivors)
    print("determinant-link p=19 audit: PASS")


if __name__ == "__main__":
    main()
