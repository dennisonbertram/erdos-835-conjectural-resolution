#!/usr/bin/env python3
"""Audit surface for PROOF.md Theorems 1, 2 and 3.

NOT RUN in the session that produced PROOF.md (no interpreter was available).
Every claim in PROOF.md is proved by hand there; this script only lets an
independent auditor re-derive the same formulas by brute force.

It does three things:

  (1) builds explicit Steiner systems S(t,t+1,v) -- and VERIFIES each one is
      really a Steiner system before using it, so the script validates its own
      inputs;
  (2) brute-forces the block-intersection distribution of each and compares it
      with the closed form (2.1) of PROOF.md;
  (3) checks Theorem 3 (integrality, nonnegativity, no-slack) symbolically for
      every prime p <= 61 and every rung 1 <= t <= p-2.

Standard library only.  Deterministic.  Prints ALL CHECKS PASS or FAIL lines.
"""

from itertools import combinations, product
from math import comb

FAILURES = []


def check(cond, label):
    if not cond:
        FAILURES.append(label)
        print("FAIL", label)


# --------------------------------------------------------------------------
# (1) explicit Steiner systems, each self-validated
# --------------------------------------------------------------------------

def is_steiner(blocks, t, v):
    """True iff `blocks` (frozensets of size t+1) is an S(t, t+1, v)."""
    cover = {}
    for b in blocks:
        if len(b) != t + 1:
            return False
        for sub in combinations(sorted(b), t):
            cover[sub] = cover.get(sub, 0) + 1
    if len(cover) != comb(v, t):
        return False
    return all(c == 1 for c in cover.values())


def s_1_2(v):
    """Perfect matching on [v], v even: an S(1,2,v)."""
    return [frozenset({2 * i, 2 * i + 1}) for i in range(v // 2)]


def s_2_3_7():
    """Fano plane: lines of PG(2,2) = {x, y, x^y} over the 7 nonzero vectors."""
    pts = list(range(1, 8))
    out = set()
    for x, y in combinations(pts, 2):
        out.add(frozenset({x, y, x ^ y}))
    return [frozenset({p - 1 for p in b}) for b in out]  # relabel to 0..6


def s_2_3_9():
    """AG(2,3): triples of F_3^2 summing to zero."""
    pts = [(a, b) for a in range(3) for b in range(3)]
    idx = {p: i for i, p in enumerate(pts)}
    out = set()
    for x, y, z in combinations(pts, 3):
        if (x[0] + y[0] + z[0]) % 3 == 0 and (x[1] + y[1] + z[1]) % 3 == 0:
            out.add(frozenset({idx[x], idx[y], idx[z]}))
    return list(out)


def s_3_4_8():
    """AG(3,2): 4-subsets of F_2^3 with zero XOR sum."""
    out = set()
    for q in combinations(range(8), 4):
        x = 0
        for a in q:
            x ^= a
        if x == 0:
            out.add(frozenset(q))
    return list(out)


def ternary_golay_hexads():
    """Supports of the weight-6 words of the extended ternary Golay [12,6,6].

    Generator G = [I_6 | B] with B the bordered Paley matrix over Z_5 mod 3.
    Returns the 132 hexads, which form an S(5,6,12).
    """
    core = [[0] * 5 for _ in range(5)]
    squares = {1, 4}  # quadratic residues mod 5
    for i in range(5):
        for j in range(5):
            d = (j - i) % 5
            core[i][j] = 0 if d == 0 else (1 if d in squares else 2)
    B = [[0] + [1] * 5]
    for i in range(5):
        B.append([1] + core[i])
    G = [[1 if j == i else 0 for j in range(6)] + B[i] for i in range(6)]

    hexads = set()
    for coeffs in product(range(3), repeat=6):
        word = [0] * 12
        for r, c in enumerate(coeffs):
            if c:
                for j in range(12):
                    word[j] = (word[j] + c * G[r][j]) % 3
        sup = frozenset(j for j in range(12) if word[j])
        if len(sup) == 6:
            hexads.add(sup)
    return list(hexads)


def derived(blocks, point):
    """Derived design at `point`: blocks through it, with the point removed."""
    return [frozenset(b - {point}) for b in blocks if point in b]


def relabel(blocks, ground):
    """Relabel a design on `ground` to 0..len(ground)-1."""
    idx = {p: i for i, p in enumerate(sorted(ground))}
    return [frozenset(idx[p] for p in b) for b in blocks]


# --------------------------------------------------------------------------
# (2) brute-force distribution vs the closed form
# --------------------------------------------------------------------------

def closed_form_same_class(K, q, i):
    """PROOF.md (2.1)."""
    num = comb(K, i) * (comb(q - 1, i) + (-1) ** i * (q - 1))
    return num / q


def closed_form_cross_class(K, q, i):
    """PROOF.md (3.1)."""
    num = comb(K, i) * (comb(q - 1, i) - (-1) ** i)
    return num / q


def audit_system(name, blocks, t, v):
    K, q = t + 1, v - t
    check(is_steiner(blocks, t, v), f"{name}: is an S({t},{t+1},{v})")
    n = comb(v, K) // q
    check(len(blocks) == n, f"{name}: block count {len(blocks)} == {n}")

    # the distribution must be independent of the chosen block: check them all
    ref = None
    for a0 in blocks:
        dist = [0] * (K + 1)
        for a in blocks:
            dist[K - len(a0 & a)] += 1
        if ref is None:
            ref = dist
        check(dist == ref, f"{name}: distribution independent of base block")
    for i in range(K + 1):
        want = closed_form_same_class(K, q, i)
        check(abs(ref[i] - want) < 1e-9, f"{name}: N_({i}) = {ref[i]} vs {want}")
    check(sum(ref) == n, f"{name}: row sum == |D|")
    print(f"  {name}: t={t} v={v} q={q} N={n} distribution={ref}")


def main():
    print("== (1)+(2) explicit systems, brute-force distributions ==")
    audit_system("S(1,2,8)", s_1_2(8), 1, 8)
    audit_system("S(1,2,12)", s_1_2(12), 1, 12)
    audit_system("S(2,3,7)", s_2_3_7(), 2, 7)
    audit_system("S(2,3,9)", s_2_3_9(), 2, 9)
    audit_system("S(3,4,8)", s_3_4_8(), 3, 8)

    hexads = ternary_golay_hexads()
    audit_system("S(5,6,12)", hexads, 5, 12)
    d11 = relabel(derived(hexads, 11), set(range(11)))
    audit_system("S(4,5,11)", d11, 4, 11)

    # complement-closure at the top rung (PROOF.md Corollary 4), checked on the
    # two available top-rung systems S(3,4,8) (k=4) and S(5,6,12) (k=6)
    print("== Corollary 4: complement-closure at the top rung ==")
    for name, blocks, k in (("S(3,4,8)", s_3_4_8(), 4), ("S(5,6,12)", hexads, 6)):
        bs = set(blocks)
        ground = frozenset(range(2 * k))
        check(all(ground - b in bs for b in bs), f"{name}: closed under complement")
        print(f"  {name}: complement-closed OK")

    # rung p-3 is an intersecting family: S(4,5,11) is the p=7 instance
    print("== Corollary 4: rung p-3 is an intersecting family ==")
    check(all(a & b for a, b in combinations(d11, 2)), "S(4,5,11): intersecting")
    print("  S(4,5,11): no two blocks disjoint OK")

    # cross-class distribution needs two disjoint systems of the same kind.
    # S(1,2,v) supplies them cheaply: any two disjoint 1-factors of K_v.
    print("== (2b) cross-class distribution, Theorem 2 ==")
    v = 8
    f1 = s_1_2(v)
    f2 = [frozenset({0, 2}), frozenset({1, 3}), frozenset({4, 6}), frozenset({5, 7})]
    check(is_steiner(f2, 1, v), "second 1-factor is an S(1,2,8)")
    check(not (set(f1) & set(f2)), "the two 1-factors are block-disjoint")
    K, q = 2, v - 1
    for a0 in f1:
        dist = [0] * (K + 1)
        for a in f2:
            dist[K - len(a0 & a)] += 1
        for i in range(K + 1):
            want = closed_form_cross_class(K, q, i)
            check(abs(dist[i] - want) < 1e-9, f"cross N^b_({i}) = {dist[i]} vs {want}")
    print("  S(1,2,8) cross-class distribution OK")

    # completeness identity (3.2)
    for (K, q) in ((2, 7), (3, 7), (4, 5), (6, 7), (5, 7), (16, 17)):
        for i in range(K + 1):
            lhs = closed_form_same_class(K, q, i) + (q - 1) * closed_form_cross_class(K, q, i)
            rhs = comb(K, i) * comb(q - 1, i)
            check(abs(lhs - rhs) < 1e-6, f"(3.2) at K={K} q={q} i={i}")
    print("  completeness identity (3.2) OK")

    # ------------------------------------------------------------------
    # (3) Theorem 3 over the whole tower, all primes p <= 61
    # ------------------------------------------------------------------
    print("== (3) Theorem 3: rung-uniform integrality / nonnegativity / no slack ==")
    primes = [p for p in range(5, 62)
              if all(p % d for d in range(2, int(p ** 0.5) + 1))]
    for p in primes:
        for t in range(1, p - 1):          # rungs t = 1 .. p-2
            K, q = t + 1, p
            for i in range(K + 1):
                a = comb(K, i) * (comb(q - 1, i) + (-1) ** i * (q - 1))
                b = comb(K, i) * (comb(q - 1, i) - (-1) ** i)
                check(a % q == 0, f"integrality N_({i}) p={p} t={t}")
                check(b % q == 0, f"integrality N^b_({i}) p={p} t={t}")
                check(a >= 0, f"nonnegativity N_({i}) p={p} t={t}")
                check(b >= 0, f"nonnegativity N^b_({i}) p={p} t={t}")
            # no slack: the shell inequality is exactly r <= p for every
            # 1 <= i <= min(K, p-2).  i = p-1 (top rung only) is degenerate:
            # beta = 0 there, the inequality reads 0 <= 0 and bounds nothing.
            for i in range(1, K + 1):
                beta = comb(q - 1, i) - (-1) ** i
                if beta == 0:
                    check(i == q - 1 and t == q - 2,
                          f"beta==0 only at i=p-1 top rung (p={p} t={t} i={i})")
                    nb = comb(K, i) * beta // q
                    check(nb == 0, f"degenerate shell has N^b=0 (p={p} t={t} i={i})")
                    continue
                check(beta > 0, f"beta>0 at p={p} t={t} i={i}")
                # largest r with N_(i) + (r-1) N^b_(i) <= v_i
                ni = comb(K, i) * (comb(q - 1, i) + (-1) ** i * (q - 1)) // q
                nb = comb(K, i) * beta // q
                vi = comb(K, i) * comb(q - 1, i)
                rmax = 1 + (vi - ni) // nb
                check(rmax == p, f"no-slack r<={rmax} != {p} at p={p} t={t} i={i}")
    print(f"  Theorem 3 verified for primes {primes[0]}..{primes[-1]}")

    # Corollary 4: D_t == 1 only at t=p-2, == 0 only at t=p-3
    print("== Corollary 4: D_t = 1 only at top rung, 0 only at rung p-3 ==")
    for p in primes:
        ones, zeros = [], []
        for t in range(1, p - 1):
            d = (comb(p - 1, t + 1) + (-1) ** (t + 1) * (p - 1)) // p
            if d == 1:
                ones.append(t)
            if d == 0:
                zeros.append(t)
        check(ones == [p - 2], f"D_t==1 exactly at t=p-2 for p={p} (got {ones})")
        check(zeros == [p - 3], f"D_t==0 exactly at t=p-3 for p={p} (got {zeros})")
    print("  Corollary 4 verified")

    # Corollary 5.3: C_k even for every k = p-1
    print("== Corollary 5.3: Catalan parity ==")
    for p in primes:
        k = p - 1
        ck = comb(2 * k, k) // (k + 1)
        check(ck % 2 == 0, f"C_{k} even (p={p})")
    print("  C_{p-1} even for all tested primes -> parity test is vacuous")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S)")
    else:
        print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
