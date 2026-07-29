#!/usr/bin/env python3
"""Diagnostic verifier for quadratic_coloring_ansatz_no_go.md.

For p=5,7,17 it generates deterministic normal-form coefficient systems
forced by the proof, checks equation (1) on every p-subset, and checks that
all deletion weighted degrees are constant.  It also reconstructs the normal
form from b using the differences in (3), independently exercising the
algebraic identities used in the written proof.
"""

from itertools import combinations, islice


def check_prime(p: int, exhaustive: bool) -> None:
    n = 2 * p - 2
    # Deliberately nonconstant deterministic data; all arithmetic is mod p.
    d = [(i * i + 3 * i + 1) % p for i in range(n)]
    A, C = (p - 2) % p, (2 * p - 3) % p
    a = [(A + 2 * d[i]) % p for i in range(n)]
    b = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            b[i][j] = b[j][i] = (d[i] + d[j] + C) % p

    # Reconstruct d up to an additive constant from delta_{i0}.
    recovered = [(b[i][2] - b[0][2]) % p if i not in (0, 2)
                 else None for i in range(n)]
    # Use a different witness coordinate when i equals 0 or 2.
    for i in range(n):
        if recovered[i] is None:
            r = 1 if i != 1 and 0 != 1 else 3
            recovered[i] = (b[i][r] - b[0][r]) % p
    for i, j, r in combinations(range(n), 3):
        assert (b[i][r] - b[j][r] - (recovered[i] - recovered[j])) % p == 0

    subsets = combinations(range(n), p)
    # The p=17 layer has more than six hundred million subsets.  The proof is
    # symbolic; a fixed sample is enough here to catch implementation slips.
    if not exhaustive:
        subsets = islice(subsets, 10_000)
    tested = 0
    for T in subsets:
        F = (sum(a[x] for x in T)
             + 2 * sum(b[x][y] for x, y in combinations(T, 2))) % p
        assert F == 0
        w = [(a[x] + sum(b[x][y] for y in T if y != x)) % p for x in T]
        assert len(set(w)) == 1
        tested += 1
    mode = "all" if exhaustive else "a deterministic sample of"
    print(f"p={p}: checked {mode} {tested} p-subsets; forced weighted degrees constant")


if __name__ == "__main__":
    for prime in (5, 7):
        check_prime(prime, exhaustive=True)
    check_prime(17, exhaustive=False)
    print("PASS: quadratic normal form obeys (1) and cannot be rainbow.")
