#!/usr/bin/env python3
"""Dependency-free verification of the j=8 torsion and rank reductions."""

from __future__ import annotations

from itertools import combinations, product


V = tuple(range(13))
FOUR_SETS = tuple(combinations(V, 4))
INDEX = {q: i for i, q in enumerate(FOUR_SETS)}


def rank_mod_prime(rows: list[tuple[int, ...]], prime: int) -> int:
    """Sparse deterministic row reduction over a prime field."""
    pivots: dict[int, dict[int, int]] = {}
    for support in rows:
        row = {column: 1 for column in support}
        while row:
            pivot = min(row)
            lead = row[pivot]
            if pivot not in pivots:
                inverse = pow(lead, -1, prime)
                row = {
                    column: (value * inverse) % prime
                    for column, value in row.items()
                    if value % prime
                }
                pivots[pivot] = row
                break
            base = pivots[pivot]
            for column, value in base.items():
                new_value = (row.get(column, 0) - lead * value) % prime
                if new_value:
                    row[column] = new_value
                else:
                    row.pop(column, None)
    return len(pivots)


def inclusion_rows(size: int) -> list[tuple[int, ...]]:
    return [
        tuple(INDEX[q] for q in combinations(s, 4))
        for s in combinations(V, size)
    ]


def audit_four_cube_extraction() -> None:
    pairs = ((0, 1), (2, 3), (4, 5), (6, 7))
    outside = (8, 9, 10, 11, 12)
    signed_transversals = {
        tuple(sorted(pairs[i][bit] for i, bit in enumerate(bits))):
        (-1) ** sum(bits)
        for bits in product((0, 1), repeat=4)
    }

    # Symmetry makes one canonical cube enough.  Exhaust all allowed filler
    # sizes and verify the alternating-difference coefficient of every Q.
    for modulus in range(2, 7):
        for filler in combinations(outside, modulus - 1):
            coefficients = {q: 0 for q in FOUR_SETS}
            for bits in product((0, 1), repeat=4):
                chosen = {pairs[i][bit] for i, bit in enumerate(bits)}
                s = chosen | set(filler)
                sign = (-1) ** sum(bits)
                for q in combinations(sorted(s), 4):
                    coefficients[q] += sign
            for q in FOUR_SETS:
                assert coefficients[q] == signed_transversals.get(q, 0)

    assert 60 % 2 == 0
    assert 60 % 3 == 0
    assert 60 % 4 == 0
    assert 60 % 5 == 0
    assert 60 % 6 == 0
    assert 8 * 12 - 8 * (-1) == 104
    assert [value for value in range(-104, 105) if value % 60 == 0] == [
        -60,
        0,
        60,
    ]


def audit_ranks() -> None:
    rows = {size: inclusion_rows(size) for size in (5, 6, 7, 8, 9, 10, 11)}

    rank_5_mod_2 = rank_mod_prime(rows[5], 2)
    rank_even_stack = rank_mod_prime(
        rows[5] + rows[7] + rows[9] + rows[11],
        2,
    )
    rank_6_mod_3 = rank_mod_prime(rows[6], 3)
    rank_three_stack = rank_mod_prime(rows[6] + rows[9], 3)
    rank_8_mod_5 = rank_mod_prime(rows[8], 5)
    rank_10_mod_7 = rank_mod_prime(rows[10], 7)

    assert rank_5_mod_2 == 495
    assert rank_even_stack == rank_5_mod_2
    assert rank_6_mod_3 == 441
    assert rank_three_stack == rank_6_mod_3
    assert rank_8_mod_5 == 429
    assert rank_10_mod_7 == 208

    print("rank M5 and even stack over F2: 495 = 495")
    print("rank M6 and [M6;M9] over F3: 441 = 441")
    print("rank M8 over F5: 429")
    print("rank M10 over F7: 208")


def audit_fixed_cube_local_structure() -> None:
    pairs = ((0, 1), (2, 3), (4, 5), (6, 7))
    signs: dict[tuple[int, ...], int] = {}
    for bits in product((0, 1), repeat=4):
        q = tuple(sorted(pairs[i][bit] for i, bit in enumerate(bits)))
        signs[q] = (-1) ** sum(bits)

    edges: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    degrees = {q: 0 for q in signs}
    for q, sign in signs.items():
        q_set = set(q)
        for other, other_sign in signs.items():
            if sign == 1 and other_sign == -1 and len(q_set & set(other)) == 3:
                edge = (q, other)
                edges.add(edge)
                degrees[q] += 1
                degrees[other] += 1

    assert len(edges) == 32
    assert set(degrees.values()) == {4}
    # From P-N=60 and P+N<=104, with N>=0.
    possible_n = [
        n
        for n in range(8 * 13 + 1)
        if 2 * n + 60 <= 104
    ]
    assert possible_n == list(range(23))

    negative_vertices = [
        bits for bits in product((0, 1), repeat=4) if sum(bits) % 2
    ]
    positive_vertices = [
        bits for bits in product((0, 1), repeat=4) if sum(bits) % 2 == 0
    ]

    def adjacent(first: tuple[int, ...], second: tuple[int, ...]) -> bool:
        return sum(a != b for a, b in zip(first, second)) == 1

    expansion = [0]
    for size in range(1, 9):
        smallest = 8
        for chosen in combinations(negative_vertices, size):
            neighborhood = {
                vertex
                for vertex in positive_vertices
                if any(adjacent(vertex, other) for other in chosen)
            }
            smallest = min(smallest, len(neighborhood))
        expansion.append(smallest)
    assert expansion == [0, 4, 6, 7, 7, 8, 8, 8, 8]

    def level_partitions(
        total: int,
        largest: int = 8,
    ) -> list[tuple[int, ...]]:
        if total == 0:
            return [()]
        answer = []
        for first in range(min(largest, total), 0, -1):
            for tail in level_partitions(total - first, first):
                answer.append((first, *tail))
        return answer

    minima = {}
    for total in (20, 21, 22):
        minima[total] = min(
            sum(expansion[size] for size in levels)
            for levels in level_partitions(total)
        )
    assert minima == {20: 23, 21: 24, 22: 24}
    # P=N+60 and P<=104-M require M<=44-N; totals 21 and 22 fail.
    assert minima[21] > 44 - 21
    assert minima[22] > 44 - 22

    # Coefficientwise inclusion-exclusion for the complement of every triple.
    for triple in combinations(V, 3):
        for q in FOUR_SETS:
            coefficient = 0
            for size in range(4):
                coefficient += (-1) ** size * sum(
                    set(u).issubset(q) for u in combinations(triple, size)
                )
            assert coefficient == int(set(q).isdisjoint(triple))

    for residue in range(7):
        allowed = [value for value in range(14) if value % 7 == residue]
        assert allowed == [residue, residue + 7]


def main() -> None:
    assert len(FOUR_SETS) == 715
    audit_four_cube_extraction()
    print("four-cube extraction, lcm, and 104 bound: PASS")
    audit_ranks()
    audit_fixed_cube_local_structure()
    print("fixed Delta=60 bound N<=20 and binary triple residues: PASS")
    print("PASS: q=6 is redundant and every cube coefficient is 0 or +/-60")
    print("scope: the Delta=60 branch, the full lift, and Problem #835 remain open")


if __name__ == "__main__":
    main()
