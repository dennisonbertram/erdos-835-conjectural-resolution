#!/usr/bin/env python3
"""Exact audit for automatic j=9 -> j=10 top-properness.

The mathematical proof is in NOTE.md.  This standard-library-only checker:

1. checks the fixed-colour recurrence and its modular consequences;
2. proves the triple-pair inclusion image equals the octahedral kernel at
   n=13 by exact modular ranks;
3. checks the fractional-part arithmetic;
4. audits every numerical threshold in the integer-weight lemma.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction


N = 13
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
TRIPLES = tuple(itertools.combinations(VERTICES, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRIPLE_INDEX = {triple: index for index, triple in enumerate(TRIPLES)}


def modular_rank(rows: list[dict[int, int]], prime: int) -> int:
    """Exact sparse Gaussian rank over F_prime."""

    basis: dict[int, dict[int, int]] = {}
    for source in rows:
        row = {column: value % prime for column, value in source.items() if value % prime}
        while row:
            pivot = min(row)
            old = basis.get(pivot)
            if old is None:
                inverse = pow(row[pivot], prime - 2, prime)
                row = {
                    column: value * inverse % prime
                    for column, value in row.items()
                    if value * inverse % prime
                }
                basis[pivot] = row
                break
            factor = row[pivot]
            for column, value in old.items():
                updated = (row.get(column, 0) - factor * value) % prime
                if updated:
                    row[column] = updated
                else:
                    row.pop(column, None)
    return len(basis)


def pair_partitions(items: tuple[int, ...]):
    """Yield every partition of an even tuple into unordered pairs."""

    if not items:
        yield ()
        return
    first = items[0]
    for position in range(1, len(items)):
        second = items[position]
        rest = items[1:position] + items[position + 1 :]
        for tail in pair_partitions(rest):
            yield ((first, second),) + tail


def audit_recurrence() -> None:
    alpha = {3: Fraction(0)}
    beta = {3: Fraction(1)}
    for size in range(4, 11):
        alpha[size] = (
            Fraction(math.comb(14, size - 3), size - 2)
            - Fraction(size, size - 2) * alpha[size - 1]
        )
        beta[size] = -Fraction(size - 3, size - 2) * beta[size - 1]
        assert beta[size] == Fraction((-1) ** (size - 3), size - 2)

    assert alpha[4] == 7
    assert alpha[5] == Fraction(56, 3)
    assert alpha[6] == 63
    assert math.lcm(*range(2, 9)) == 840
    # An octahedron has four positive and four negative d-values in [0,14].
    assert 4 * 14 == 56 < 840
    print("recurrence: sizes 4..10 and lcm bound: PASS")


def audit_octahedral_kernel() -> None:
    inclusion_rows = [
        {EDGE_INDEX[edge]: 1 for edge in itertools.combinations(triple, 2)}
        for triple in TRIPLES
    ]

    octahedral_rows: list[dict[int, int]] = []
    relation_count = 0
    for six in itertools.combinations(VERTICES, 6):
        partitions = tuple(pair_partitions(six))
        assert len(partitions) == 15
        for partition in partitions:
            relation_count += 1
            row: dict[int, int] = {}
            edge_coefficients: dict[tuple[int, int], int] = {}
            for bits in itertools.product((0, 1), repeat=3):
                triple = tuple(
                    sorted(partition[index][bit] for index, bit in enumerate(bits))
                )
                coefficient = -1 if sum(bits) % 2 else 1
                column = TRIPLE_INDEX[triple]
                row[column] = row.get(column, 0) + coefficient
                for edge in itertools.combinations(triple, 2):
                    edge_coefficients[edge] = (
                        edge_coefficients.get(edge, 0) + coefficient
                    )
            assert len(row) == 8
            assert all(value == 0 for value in edge_coefficients.values())
            octahedral_rows.append(row)

    assert relation_count == math.comb(13, 6) * 15 == 25_740
    for prime in (1_000_003, 1_000_033):
        rank_w = modular_rank(inclusion_rows, prime)
        rank_o = modular_rank(octahedral_rows, prime)
        assert rank_w == math.comb(13, 2) == 78
        assert rank_o == math.comb(13, 3) - math.comb(13, 2) == 208
    print(
        "octahedral kernel:",
        "25,740 relations, ranks W=78 and O=208 over two primes: PASS",
    )


def audit_fractional_parts() -> None:
    # From 6 theta = 15 theta = 0 we get 3 theta = 0.  Check the three
    # possibilities, with 4 theta = 1/3 selecting theta = 1/3.
    candidates = [Fraction(k, 3) for k in range(3)]
    survivors = [
        theta
        for theta in candidates
        if (4 * theta - Fraction(1, 3)).denominator == 1
    ]
    assert survivors == [Fraction(1, 3)]

    # Each edge of an s-set occurs in s-2 triples.
    for size in (4, 5, 6):
        sample = tuple(range(size))
        counts = {edge: 0 for edge in itertools.combinations(sample, 2)}
        for triple in itertools.combinations(sample, 3):
            for edge in itertools.combinations(triple, 2):
                counts[edge] += 1
        assert set(counts.values()) == {size - 2}
    print("fractional parts: common residue theta=1/3 forced: PASS")


def audit_integer_lemma() -> None:
    # Global and vertex bounds.
    assert -math.comb(13, 3) // 11 == -26
    assert (3 * math.comb(13, 2)) // 33 == 7
    total_range = range(-26, 8)
    row_values = {
        row
        for total in total_range
        for row in range(-20, 21)
        if -66 - total <= 10 * row <= 18 - total
    }
    assert min(row_values) == -7
    assert max(row_values) == 4

    # Fixed-edge lower and upper sums with row values in [-7,4].
    possible_edge_values = {
        edge
        for row_a in range(-7, 5)
        for row_b in range(-7, 5)
        for edge in range(-10, 11)
        if -11 <= 9 * edge + row_a + row_b <= 3
    }
    assert possible_edge_values == {-2, -1, 0, 1}

    # A -2 edge forces row sum at least 7 across its endpoints; with each
    # row at most 4, both endpoints are at least 3.  A forced +1 cross-edge
    # would require the third row to be at most -9, below the row minimum.
    assert -4 + 11 == 7
    assert 7 - 4 == 3
    assert -6 - 3 == -9 < -7

    # First clique pass: 4k-28 <= -6 permits exactly k <= 5.
    first_pass = [k for k in range(13) if 4 * k - 28 <= -6]
    assert max(first_pass) == 5

    # With negative degrees <=5, a positive edge has p_a+p_b <=4.
    assert -6 + 2 * 5 == 4

    # Second clique pass: 2(k-1) <=4 permits exactly k <=3.
    second_pass = [k for k in range(13) if 2 * (k - 1) <= 4]
    assert max(second_pass) == 3

    # A positive-edge endpoint then has Z >= 1-3=-2, contradicting the
    # required endpoint sum <=-6.
    assert 1 - 3 == -2
    assert 2 * (-2) == -4 > -6
    print("integer-weight lemma: all numerical thresholds: PASS")


def main() -> int:
    assert len(EDGES) == 78
    assert len(TRIPLES) == 286
    audit_recurrence()
    audit_octahedral_kernel()
    audit_fractional_parts()
    audit_integer_lemma()
    print("PASS: automatic j=9 -> j=10 top-properness arithmetic and rank audit")
    print("scope: conditional high-lift theorem only; lower tower and #835 remain open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
