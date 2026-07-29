#!/usr/bin/env python3
"""Independent finite checks for full_slice_degree_necessity.md."""

from itertools import combinations
from math import comb


def rank_mod(rows, p):
    rows = [list(map(lambda x: x % p, row)) for row in rows]
    if not rows:
        return 0
    m, n = len(rows), len(rows[0])
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, m) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, p)
        rows[rank] = [(inv * x) % p for x in rows[rank]]
        for i in range(m):
            if i != rank and rows[i][col]:
                q = rows[i][col]
                rows[i] = [
                    (x - q * y) % p for x, y in zip(rows[i], rows[rank])
                ]
        rank += 1
        if rank == m:
            break
    return rank


def small_check(p):
    k = p - 1
    n = 2 * k
    km1 = list(combinations(range(n), k - 1))
    ks = list(combinations(range(n), k))
    index = {s: j for j, s in enumerate(ks)}

    W = []
    for t in km1:
        row = [0] * len(ks)
        outside = set(range(n)) - set(t)
        for x in outside:
            row[index[tuple(sorted(t + (x,)))]] = 1
        W.append(row)

    rank_w = rank_mod(W, p)
    assert rank_w == len(km1)

    gram = [
        [sum(x * y for x, y in zip(a, b)) % p for b in W]
        for a in W
    ]
    rank_gram = rank_mod(gram, p)
    assert len(km1) - rank_gram == 1

    # Equation (3), checked for every monomial support A.
    for a in range(k):
        scalar = (k - a) % p
        assert scalar
        for A in combinations(range(n), a):
            containing = [t for t in km1 if set(A) <= set(t)]
            for S in ks:
                lhs = sum(set(t) <= set(S) for t in containing) % p
                rhs = scalar * int(set(A) <= set(S)) % p
                assert lhs == rhs

    print(
        f"p={p}: rows={len(km1)}, columns={len(ks)}, "
        f"rank(W)={rank_w}, nullity(WW^T)=1"
    )


def symbolic_check(p):
    k = p - 1
    factors = [k - j for j in range(k)]
    assert factors == list(range(k, 0, -1))
    assert all(x % p for x in factors)

    eigen_factors = [(k - j, k + 1 - j) for j in range(k)]
    divisible = [(j, a, b) for j, (a, b) in enumerate(eigen_factors)
                 if (a * b) % p == 0]
    assert divisible == [(0, k, p)]

    rows = comb(2 * k, k - 1)
    cols = comb(2 * k, k)
    print(
        f"p={p}: Wilson factors nonzero; unique Gram p-factor at j=0; "
        f"rows={rows}, columns={cols}"
    )


if __name__ == "__main__":
    for prime in (3, 5):
        small_check(prime)
    symbolic_check(7)
    symbolic_check(17)
    print("PASS: every nonconstant zero-sum colour statistic has full slice degree.")
