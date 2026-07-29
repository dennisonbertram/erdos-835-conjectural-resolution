#!/usr/bin/env python3
"""Exact arithmetic audit for the critical-group cover obstruction."""

from __future__ import annotations

import argparse
from collections import Counter
from math import comb


def is_prime(number: int) -> bool:
    """Return whether number is prime."""
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def valuation(number: int, prime: int) -> int:
    """Return the prime-adic valuation of a nonzero integer."""
    assert number
    exponent = 0
    while number % prime == 0:
        number //= prime
        exponent += 1
    return exponent


def factor_integer(number: int) -> Counter[int]:
    """Factor a positive integer by exact trial division."""
    assert number > 0
    factors: Counter[int] = Counter()
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            factors[divisor] += 1
            number //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if number > 1:
        factors[number] += 1
    return factors


def odd_graph_spectrum(k: int) -> list[tuple[int, int, int]]:
    """Return (index, Laplacian eigenvalue, multiplicity) for O_k."""
    ground_size = 2 * k - 1
    spectrum = []
    previous = 0
    for index in range(k):
        current = comb(ground_size, index)
        multiplicity = current - previous
        adjacency_eigenvalue = (-1) ** index * (k - index)
        laplacian_eigenvalue = k - adjacency_eigenvalue
        spectrum.append((index, laplacian_eigenvalue, multiplicity))
        previous = current
    return spectrum


def tree_factorization(k: int) -> Counter[int]:
    """Return the exact prime-exponent factorization of tau(O_k)."""
    vertex_count = comb(2 * k - 1, k - 1)
    factors: Counter[int] = Counter()
    for index, eigenvalue, multiplicity in odd_graph_spectrum(k):
        if index == 0:
            assert eigenvalue == 0
            continue
        for prime, exponent in factor_integer(eigenvalue).items():
            factors[prime] += exponent * multiplicity
    for prime, exponent in factor_integer(vertex_count).items():
        factors[prime] -= exponent
    assert all(exponent >= 0 for exponent in factors.values())
    return +factors


def verify_prime_case(prime: int) -> dict[str, int]:
    """Verify every formula used in the all-prime theorem."""
    assert prime >= 5 and is_prime(prime)
    k = prime - 1
    r = prime - 2
    ground_size = 2 * prime - 3
    vertex_count = comb(ground_size, r)
    assert valuation(vertex_count, prime) == 1
    sheets = vertex_count // prime
    assert sheets % prime != 0
    assert (2 * sheets + 1) % prime == 0

    top_multiplicity = vertex_count - comb(ground_size, r - 1)
    assert top_multiplicity == 2 * sheets

    spectrum = odd_graph_spectrum(k)
    divisible_indices = [
        index
        for index, eigenvalue, _multiplicity in spectrum[1:]
        if eigenvalue % prime == 0
    ]
    assert divisible_indices == [r]
    assert spectrum[r][1] == prime
    assert spectrum[r][2] == top_multiplicity

    tree_valuation = sum(
        multiplicity * valuation(eigenvalue, prime)
        for _index, eigenvalue, multiplicity in spectrum[1:]
    ) - valuation(vertex_count, prime)
    source_p_rank = 2 * sheets - 1
    target_p_rank = prime - 2
    quotient_valuation = tree_valuation - target_p_rank

    assert tree_valuation == source_p_rank
    assert source_p_rank >= target_p_rank
    assert quotient_valuation == 2 * sheets - prime + 1
    assert quotient_valuation >= 0
    assert top_multiplicity >= prime - 1

    # The Gram eigenvalues in the full-row-rank proof are all positive.
    for johnson_index in range(r):
        gram_eigenvalue = (r - johnson_index) * (r - johnson_index + 2)
        assert gram_eigenvalue > 0

    return {
        "p": prime,
        "k": k,
        "vertices": vertex_count,
        "sheets": sheets,
        "source_p_rank": source_p_rank,
        "target_p_rank": target_p_rank,
        "quotient_p_valuation": quotient_valuation,
    }


def verify_k16_factorization() -> Counter[int]:
    """Check the recorded complete factorization at k=16."""
    factors = tree_factorization(16)
    assert factors[17] == 35_357_669
    factors[17] -= 15
    factors = +factors
    expected = Counter(
        {
            2: 212_416_154,
            3: 97_750_066,
            5: 27_978_677,
            7: 99_249_600,
            17: 35_357_654,
            19: 65_132_549,
            23: 12_271_349,
            29: 4_029,
            31: 29,
        }
    )
    assert factors == expected
    return factors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-prime",
        type=int,
        default=101,
        help="verify every odd prime p with 5 <= p <= this bound",
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="print the exact row for every checked prime",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [
        verify_prime_case(prime)
        for prime in range(5, args.max_prime + 1, 2)
        if is_prime(prime)
    ]
    assert rows

    if args.show_all:
        for row in rows:
            print(row)

    k16 = verify_prime_case(17)
    assert k16 == {
        "p": 17,
        "k": 16,
        "vertices": 300_540_195,
        "sheets": 17_678_835,
        "source_p_rank": 35_357_669,
        "target_p_rank": 15,
        "quotient_p_valuation": 35_357_654,
    }
    factorization = verify_k16_factorization()

    print(f"ALL {len(rows)} PRIME CASES THROUGH {args.max_prime} PASSED")
    print(f"k=16 exact row: {k16}")
    print(f"k=16 tree-quotient factorization: {dict(factorization)}")
    print("CRITICAL-GROUP / TREE / SPECTRAL CONDITIONS ALL PASS")


if __name__ == "__main__":
    main()
