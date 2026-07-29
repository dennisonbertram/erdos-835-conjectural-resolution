#!/usr/bin/env python3
"""Exact checks for star_sign_gluing_audit.md (stdlib only)."""

from __future__ import annotations

import random
from itertools import combinations
from math import comb


OPPOSITE_K18 = [
    [(0, 1), (2, 4), (3, 13), (5, 12), (6, 15), (7, 14), (8, 11), (9, 16), (10, 17)],
    [(0, 2), (1, 15), (3, 6), (4, 11), (5, 17), (7, 16), (8, 14), (9, 13), (10, 12)],
    [(0, 3), (1, 14), (2, 6), (4, 12), (5, 9), (7, 17), (8, 15), (10, 11), (13, 16)],
    [(0, 4), (1, 2), (3, 15), (5, 11), (6, 7), (8, 13), (9, 12), (10, 14), (16, 17)],
    [(0, 5), (1, 13), (2, 8), (3, 17), (4, 6), (7, 15), (9, 10), (11, 14), (12, 16)],
    [(0, 6), (1, 8), (2, 14), (3, 11), (4, 9), (5, 7), (10, 13), (12, 17), (15, 16)],
    [(0, 7), (1, 4), (2, 13), (3, 16), (5, 8), (6, 11), (9, 17), (10, 15), (12, 14)],
    [(0, 8), (1, 5), (2, 7), (3, 9), (4, 14), (6, 10), (11, 16), (12, 15), (13, 17)],
    [(0, 9), (1, 10), (2, 15), (3, 14), (4, 5), (6, 12), (7, 13), (8, 16), (11, 17)],
    [(0, 10), (1, 12), (2, 3), (4, 15), (5, 16), (6, 13), (7, 11), (8, 17), (9, 14)],
    [(0, 11), (1, 16), (2, 12), (3, 8), (4, 10), (5, 13), (6, 14), (7, 9), (15, 17)],
    [(0, 12), (1, 9), (2, 11), (3, 5), (4, 16), (6, 8), (7, 10), (13, 15), (14, 17)],
    [(0, 13), (1, 11), (2, 5), (3, 4), (6, 17), (7, 12), (8, 10), (9, 15), (14, 16)],
    [(0, 14), (1, 6), (2, 17), (3, 12), (4, 7), (5, 15), (8, 9), (10, 16), (11, 13)],
    [(0, 15), (1, 7), (2, 16), (3, 10), (4, 17), (5, 6), (8, 12), (9, 11), (13, 14)],
    [(0, 16), (1, 17), (2, 10), (3, 7), (4, 8), (5, 14), (6, 9), (11, 15), (12, 13)],
    [(0, 17), (1, 3), (2, 9), (4, 13), (5, 10), (6, 16), (7, 8), (11, 12), (14, 15)],
]


def permutation_bit(values: list[int]) -> int:
    return sum(
        values[i] > values[j]
        for i in range(len(values))
        for j in range(i + 1, len(values))
    ) & 1


def matching_bit(matching: list[tuple[int, int]]) -> int:
    edges = [tuple(sorted(edge)) for edge in matching]
    result = 0
    for (a, b), (c, d) in combinations(edges, 2):
        if c < a:
            a, b, c, d = c, d, a, b
        result ^= a < c < b < d
    return int(result)


def verify_factorization(factors: list[list[tuple[int, int]]], n: int) -> None:
    expected = set(combinations(range(n), 2))
    seen = set()
    assert len(factors) == n - 1
    for matching in factors:
        assert len(matching) == n // 2
        vertices = []
        for edge in matching:
            edge = tuple(sorted(edge))
            assert edge in expected and edge not in seen
            seen.add(edge)
            vertices.extend(edge)
        assert sorted(vertices) == list(range(n))
    assert seen == expected


def star_vector(factors: list[list[tuple[int, int]]], n: int) -> int:
    result = 0
    for vertex in range(n):
        codomain = [x for x in range(n) if x != vertex]
        position = {x: i for i, x in enumerate(codomain)}
        images = []
        for matching in factors:
            edge = next(edge for edge in matching if vertex in edge)
            mate = edge[0] if edge[1] == vertex else edge[1]
            images.append(position[mate])
        result |= permutation_bit(images) << vertex
    return result


def factorization_bit(factors: list[list[tuple[int, int]]]) -> int:
    return sum(matching_bit(matching) for matching in factors) & 1


def cyclic_factorization(n: int) -> list[list[tuple[int, int]]]:
    modulus = n - 1
    infinity = modulus
    return [
        [(infinity, shift)]
        + [
            ((shift + offset) % modulus, (shift - offset) % modulus)
            for offset in range(1, (modulus + 1) // 2)
        ]
        for shift in range(modulus)
    ]


def relabel_and_normalize(
    factors: list[list[tuple[int, int]]],
    permutation: list[int],
) -> list[list[tuple[int, int]]]:
    n = len(permutation)
    relabelled = [
        [tuple(sorted((permutation[a], permutation[b]))) for a, b in matching]
        for matching in factors
    ]
    edge_colour = {
        edge: colour
        for colour, matching in enumerate(relabelled)
        for edge in matching
    }
    # Factor w-1 is normalized to contain the anchor edge {0,w}.
    return [relabelled[edge_colour[(0, w)]] for w in range(1, n)]


def affine_rank(vectors: list[int]) -> int:
    base = vectors[0]
    pivots = {}
    for vector in vectors[1:]:
        value = vector ^ base
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def main() -> None:
    # The flag-transposition constant is checked on two opposite-sign
    # K18 factorizations.
    cyclic = cyclic_factorization(18)
    for factors in (cyclic, OPPOSITE_K18):
        verify_factorization(factors, 18)
        left = factorization_bit(factors)
        right = (
            comb(9, 2) + bin(star_vector(factors, 18)).count("1")
        ) & 1
        assert left == right

    assert factorization_bit(cyclic) == 0
    assert factorization_bit(OPPOSITE_K18) == 1

    # Normalization fixes the star at vertex zero. Relabelled cyclic
    # factorizations span sixteen directions; one explicit factorization of
    # the opposite sign supplies the seventeenth.
    rng = random.Random(4)
    vectors = [star_vector(OPPOSITE_K18, 18)]
    for _ in range(5000):
        permutation = list(range(18))
        rng.shuffle(permutation)
        factors = relabel_and_normalize(cyclic, permutation)
        verify_factorization(factors, 18)
        vector = star_vector(factors, 18)
        assert not (vector & 1)
        vectors.append(vector)
    assert affine_rank(vectors) == 17

    r = 15
    m = (r + 3) // 2
    h_sts = comb(r + 4, 4) & 1
    g_system = h_sts * (comb(2 * r + 1, r - 3) & 1) & 1
    scalar_left = g_system * ((r + 2) & 1) & 1
    scalar_right = (comb(m, 2) & 1) * (
        comb(2 * r + 1, r - 2) & 1
    ) & 1
    assert h_sts == g_system == scalar_left == scalar_right == 0

    print("K18 cyclic factorization sign: +1")
    print("K18 explicit opposite factorization sign: -1")
    print("normalized K18 star-vector affine rank: 17 (maximum)")
    print("r=15 STS-link sign, system sign, and both scalar gluing sides: +1")
    print("star-sign gluing audit: PASS")


if __name__ == "__main__":
    main()
