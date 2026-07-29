#!/usr/bin/env python3
"""Independent validator for PROOF.md Theorem 1.3 and its corollaries.

NOT RUN when written (code execution was unavailable in that session).

Checks, from scratch:
  1. N_j = C(k,j)*(C(k,j) + (-1)^(k-j)*k) / (k+1)  against brute-force block
     intersection counts in S(3,4,8) (k=4) and S(5,6,12) (k=6);
  2. complement-closure of both systems (PROOF.md Theorem 2.1);
  3. the integrality sieve of Corollary 1.5 for even k <= 200, and whether it
     agrees with "k+1 is prime".

Stdlib only.  Exits nonzero on any failure.
"""
from itertools import combinations
from math import comb


# ---------------------------------------------------------------- predicted

def N_pred(k, j):
    """PROOF.md Theorem 1.3.  Valid for 0 <= j <= k-1."""
    num = comb(k, j) * (comb(k, j) + (-1) ** (k - j) * k)
    q, r = divmod(num, k + 1)
    if r:
        raise ValueError(f"non-integral N_{j} at k={k}")
    return q


# ---------------------------------------------------------------- systems

def steiner_3_4_8():
    """Blocks of AG(3,2): 4-subsets of F_2^3 with XOR 0."""
    return [frozenset(b) for b in combinations(range(8), 4)
            if b[0] ^ b[1] ^ b[2] ^ b[3] == 0]


def steiner_5_6_12():
    """The 132 hexads, as the PSL(2,11)-orbit of {inf} u QR(11).

    Points 0..10 are F_11, point 11 is infinity.
    """
    INF = 11

    def shift(x):
        return INF if x == INF else (x + 1) % 11

    def inv(x):
        if x == INF:
            return 0
        if x == 0:
            return INF
        return (-pow(x, 9, 11)) % 11      # -1/x, since x^9 = x^-1 mod 11

    base = frozenset({INF, 1, 3, 4, 5, 9})
    seen, frontier = {base}, [base]
    while frontier:
        nxt = []
        for blk in frontier:
            for g in (shift, inv):
                img = frozenset(g(x) for x in blk)
                if img not in seen:
                    seen.add(img)
                    nxt.append(img)
        frontier = nxt
    return sorted(seen, key=sorted)


def is_steiner(blocks, t, ksize, v):
    """Every t-subset of [v] lies in exactly one block."""
    if any(len(b) != ksize for b in blocks):
        return False
    count = {}
    for b in blocks:
        for s in combinations(sorted(b), t):
            count[s] = count.get(s, 0) + 1
    return len(count) == comb(v, t) and set(count.values()) == {1}


# ---------------------------------------------------------------- checks

def check_system(name, blocks, k, v):
    ok = True
    print(f"\n=== {name}: k={k}, v={v}, blocks={len(blocks)} ===")

    assert is_steiner(blocks, k - 1, k, v), f"{name} is not an S({k-1},{k},{v})"
    print(f"  valid S({k-1},{k},{v}): PASS")

    expected = comb(v, k) // (k + 1)
    print(f"  block count {len(blocks)} (expected {expected}): "
          f"{'PASS' if len(blocks) == expected else 'FAIL'}")
    ok &= len(blocks) == expected

    # complement closure
    universe = frozenset(range(v))
    closed = all(universe - b in set(blocks) for b in blocks)
    print(f"  complement-closed: {'PASS' if closed else 'FAIL'}")
    ok &= closed

    # intersection distribution, from every block
    pred = [N_pred(k, j) for j in range(k)]
    bad = 0
    for a0 in blocks:
        dist = [0] * (k + 1)
        for a in blocks:
            if a is not a0 and a != a0:
                dist[len(a0 & a)] += 1
        if dist[:k] != pred or dist[k] != 0:
            bad += 1
    print(f"  predicted N_j (j=0..{k-1}): {pred}")
    print(f"  blocks disagreeing with prediction: {bad} of {len(blocks)}"
          f"  -> {'PASS' if bad == 0 else 'FAIL'}")
    ok &= bad == 0
    return ok


def sieve(limit=200):
    print(f"\n=== integrality sieve, even k <= {limit} ===")

    def is_prime(n):
        if n < 2:
            return False
        d = 2
        while d * d <= n:
            if n % d == 0:
                return False
            d += 1
        return True

    passing, disagree = [], []
    for k in range(2, limit + 1, 2):
        good = all((comb(k, j) * (comb(k, j) + (-1) ** (k - j) * k)) % (k + 1) == 0
                   for j in range(k))
        if good:
            passing.append(k)
        if good != is_prime(k + 1):
            disagree.append(k)
    print(f"  k passing the sieve: {passing}")
    print(f"  k where sieve verdict != (k+1 prime): {disagree}")
    print("  (the paper claims only that primality IMPLIES the sieve; a "
          "nonempty disagreement list of composite k would be a new result)")
    for k in (8, 14, 20):
        witness = [j for j in range(k)
                   if (comb(k, j) * (comb(k, j) + (-1) ** (k - j) * k)) % (k + 1)]
        print(f"  k={k}: violating j = {witness} "
              f"-> {'PASS' if witness else 'FAIL (expected a violation)'}")
    return all(k not in passing for k in (8, 14, 20))


def main():
    ok = True
    ok &= check_system("S(3,4,8)", steiner_3_4_8(), 4, 8)
    ok &= check_system("S(5,6,12)", steiner_5_6_12(), 6, 12)
    ok &= sieve()
    print("\nOVERALL:", "PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
