#!/usr/bin/env python3
"""Exact finite checks for local_one_factorization_sign_audit.md.

This program is stdlib-only.  It enumerates unordered one-factorizations of
K_4, K_6, and K_8, checks the flag/Pfaffian sign identity on every one, and
checks the parity arithmetic and scalar formal countermodel used in the note.
"""

from itertools import combinations
from math import comb


def parity_of_permutation(values):
    return sum(
        values[i] > values[j]
        for i in range(len(values))
        for j in range(i + 1, len(values))
    ) & 1


def matching_pfaffian_bit(matching):
    """0 for +1 and 1 for -1, in the natural vertex order."""
    edges = sorted(tuple(sorted(edge)) for edge in matching)
    flattened = [vertex for edge in edges for vertex in edge]
    return parity_of_permutation(flattened)


def factorization_bit(factors):
    return sum(matching_pfaffian_bit(matching) for matching in factors) & 1


def star_product_bit(factors, n):
    """Parity of the product of all factor-to-mate star permutations."""
    result = 0
    for vertex in range(n):
        codomain = [other for other in range(n) if other != vertex]
        position = {other: index for index, other in enumerate(codomain)}
        images = []
        for matching in factors:
            edge = next(edge for edge in matching if vertex in edge)
            mate = edge[0] if edge[1] == vertex else edge[1]
            images.append(position[mate])
        result ^= parity_of_permutation(images)
    return result


def verify_factorization(factors, n):
    expected = set(combinations(range(n), 2))
    seen = set()
    assert len(factors) == n - 1
    for matching in factors:
        vertices = []
        for edge in matching:
            ordered = tuple(sorted(edge))
            assert ordered in expected
            assert ordered not in seen
            seen.add(ordered)
            vertices.extend(ordered)
        assert sorted(vertices) == list(range(n))
    assert seen == expected


def enumerate_one_factorizations(n):
    """Yield every unordered one-factorization exactly once.

    At each stage the least uncovered edge chooses the next factor.  Hence an
    unordered set of factors has one and only one recursive history.
    """
    edges = list(combinations(range(n), 2))
    full_mask = (1 << len(edges)) - 1
    edge_index = {edge: index for index, edge in enumerate(edges)}

    matchings = []

    def extend_matching(remaining, chosen):
        if not remaining:
            mask = sum(1 << edge_index[edge] for edge in chosen)
            matchings.append((mask, tuple(chosen)))
            return
        first = min(remaining)
        for other in sorted(remaining - {first}):
            extend_matching(remaining - {first, other}, chosen + [(first, other)])

    extend_matching(set(range(n)), [])
    by_edge = [[] for _ in edges]
    for matching in matchings:
        for index in range(len(edges)):
            if matching[0] & (1 << index):
                by_edge[index].append(matching)

    chosen = []

    def search(used_mask):
        if used_mask == full_mask:
            factors = tuple(matching for _, matching in chosen)
            verify_factorization(factors, n)
            yield factors
            return
        least = next(index for index in range(len(edges)) if not (used_mask >> index) & 1)
        for mask, matching in by_edge[least]:
            if not (mask & used_mask):
                chosen.append((mask, matching))
                yield from search(used_mask | mask)
                chosen.pop()

    yield from search(0)


def binom_bit(n, r):
    return comb(n, r) & 1


def verify_sts(blocks, n):
    pair_count = {pair: 0 for pair in combinations(range(n), 2)}
    for block in blocks:
        assert len(block) == 3
        for pair in combinations(sorted(block), 2):
            pair_count[pair] += 1
    assert set(pair_count.values()) == {1}


def sts_link_product_bit(blocks, n):
    verify_sts(blocks, n)
    result = 0
    for vertex in range(n):
        matching = []
        for block in blocks:
            if vertex in block:
                edge = tuple(sorted(other for other in block if other != vertex))
                matching.append(edge)
        assert len(matching) == (n - 1) // 2
        assert sorted(vertex for edge in matching for vertex in edge) == [
            other for other in range(n) if other != vertex
        ]
        result ^= matching_pfaffian_bit(matching)
    return result


def fano_sts():
    # Nonzero vectors of F_2^3; a line is {a,b,a+b}.
    return sorted(
        {
            tuple(sorted((a - 1, b - 1, (a ^ b) - 1)))
            for a in range(1, 8)
            for b in range(a + 1, 8)
        }
    )


def affine_plane_sts_9():
    # The twelve affine lines of AG(2,3).
    directions = [(1, 0), (0, 1), (1, 1), (1, 2)]
    lines = set()
    for x in range(3):
        for y in range(3):
            for dx, dy in directions:
                line = tuple(
                    sorted(
                        ((x + t * dx) % 3) * 3 + ((y + t * dy) % 3)
                        for t in range(3)
                    )
                )
                lines.add(line)
    return sorted(lines)


def local_constants(p):
    # a is the flag-transposition constant, h the STS-link constant.
    a = binom_bit((p + 1) // 2, 2)
    h = binom_bit(p + 2, 4)
    return a, h


def main():
    expected_counts = {4: 1, 6: 6, 8: 6240}
    distributions = {}
    for n in (4, 6, 8):
        counts = [0, 0]
        a = binom_bit(n // 2, 2)
        for factors in enumerate_one_factorizations(n):
            pf_bit = factorization_bit(factors)
            star_bit = star_product_bit(factors, n)
            assert pf_bit == (a ^ star_bit)
            counts[star_bit] += 1
        assert sum(counts) == expected_counts[n]
        distributions[n] = counts

    # Exact local controls.  Bit 0 is +1 and bit 1 is -1.
    assert distributions[4] == [1, 0]
    assert distributions[6] == [0, 6]
    assert distributions[8] == [5280, 960]

    # Small exact checks of the universal STS link product in (5).
    assert sts_link_product_bit(fano_sts(), 7) == binom_bit(7, 4) == 1
    assert sts_link_product_bit(affine_plane_sts_9(), 9) == binom_bit(9, 4) == 0

    # At p=5, fixing one point leaves seven K6 links.  Each has negative
    # star-product sign, while every pinned star is counted p-3=2 times.
    forced_local_product = (comb(7, 1) * 1) & 1
    assert (5 - 3) % 2 == 0
    forced_global_product = 0
    assert forced_local_product == 1
    assert forced_global_product == 0
    assert forced_local_product != forced_global_product

    # At p=7, K8 admits both star-product signs; and the two scalar bases
    # are already positive.
    assert distributions[8][0] and distributions[8][1]
    assert local_constants(7) == (0, 0)

    # The p=17 fixed-point products have the exact cardinalities below.
    assert comb(31, 13) == 206253075
    assert comb(31, 12) == 141120525
    assert local_constants(17) == (0, 0)

    # Scalar formal countermodel: give every matching sign the bit b=a=h,
    # and every star sign +1.  It satisfies every displayed flag identity
    # and every one-step STS-link identity for every tested odd p.
    for p in range(3, 100, 2):
        a, h = local_constants(p)
        assert a == h
        b = a
        assert (p * b) & 1 == a
        assert ((p + 2) * b) & 1 == h

    print("K4 one-factorizations: 1; star-product signs (+,-): (1, 0)")
    print("K6 one-factorizations: 6; star-product signs (+,-): (0, 6)")
    print("K8 one-factorizations: 6240; star-product signs (+,-): (5280, 960)")
    print("STS(7) and STS(9) universal link-Pfaffian signs: -1, +1")
    print("p=5 pinned-star control: contradiction reproduced")
    print("p=7 local signs are non-rigid; scalar bases are +1")
    print("p=17: C(31,13)=206253075, C(31,12)=141120525; bases are +1")
    print("all odd p < 100: scalar formal sign countermodel verified")
    print("local one-factorization sign audit: PASS")


if __name__ == "__main__":
    main()
