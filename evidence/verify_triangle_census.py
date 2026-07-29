#!/usr/bin/env python3
"""Validator: forced triangle-triple census for boundary Steiner systems
S(r-1, r, 2r+1), and the refutation of universal triangle closure at r=15.

THEOREM (census).  For any S(r-1,r,2r+1) A on X, |X| = 2r+1, r odd, let
T = #unordered triples {B1,B2,B3} of blocks with 1_B1+1_B2+1_B3 = 1_X
(equivalently: common 7-point... common m-point core I = Bi cap Bj,
m = (r-1)/2, partitioning X \\ I into three (m+1)-sets).  Then
    6 * 2^(2r+1) * T = sum over ALL subsets S of X of (-1)^{|S|} F(S)^3,
where F(S) = sum_B (-1)^{|B cap S|}.  Every F(S) is forced by the design
parameters except at |S| in {r, r+1}, where the split is determined by
|A| = b alone.  Hence T is forced by the parameters.
Proof: expand F^3 and sum the character over S first; the inner sum is
2^(2r+1) exactly when 1_B1+1_B2+1_B3 = 1_X (the 0 case is impossible for
odd r), and each unordered triple arises 6 times.

COROLLARY (closure test).  Each pair with |B1 cap B2| = m closes to at
most one triple (B3 is determined), so with P_m = forced number of such
pairs: universal triangle closure <=> 3T = P_m.  Values:
    r=3 :  3T = 21          = P_1  (closure holds - forced)
    r=5 :  3T = 660         = P_2  (closure holds - forced)
    r=15:  3T = 2783090599875 < P_7 = 43116291922275
so in EVERY hypothetical S(14,15,31) exactly 40,333,201,322,400 of the
7-intersecting pairs do NOT close: universal closure is REFUTED at r=15
(it could only hold vacuously), while T = 927,696,866,625 > 0 proves the
triples exist in forced number.  T equals A_3^perp of the even incidence
subcode C_0 (weight-3 dual words are exactly these triples; the full
31-dim code has A_3^perp = 0 for the trivial odd-parity reason, so the
even/full distinction is essential).

Controls in this file: (a) P_7 by two independent routes (intra pair
distribution inversion; per-7-set derived-design count with N0(8)=758);
(b) the forced census formula reproduces the ACTUAL triple counts of the
real designs at r=3 (Fano: 7) and r=5 (S(4,5,11): 220), where closure
is full; (c) the weight-1/2 analogues vanish identically.
Run: python3 verify_triangle_census.py   (~15 s; r=5 exact cover)
"""
import sys
from math import comb
from itertools import combinations

HERE = __file__.rsplit("/", 1)[0] or "."


def lam_vec(r):
    v = 2 * r + 1
    out = []
    for j in range(r):
        num, den = comb(v - j, r - 1 - j), (r - j)
        assert num % den == 0
        out.append(num // den)
    return out


def forced_moment(r, power):
    """sum over all S subset X of (-1)^{|S|} F(S)^power (forced)."""
    v = 2 * r + 1
    lam = lam_vec(r)
    b = lam[0]

    def F_ext(s):
        if s <= r - 1:
            return sum((-2) ** j * comb(s, j) * lam[j] for j in range(s + 1))
        if s == r:
            return sum((-2) ** j * comb(r, j) * lam[j] for j in range(r))
        return -F_ext(v - s)

    Fr = F_ext(r)
    tot = 0
    for s in range(v + 1):
        if s == r:
            tot += (-1) ** s * (b * (Fr - 2 ** r) ** power
                                + (comb(v, r) - b) * Fr ** power)
        elif s == r + 1:
            tot += (-1) ** s * (b * (-Fr + 2 ** r) ** power
                                + (comb(v, r + 1) - b) * (-Fr) ** power)
        else:
            tot += (-1) ** s * comb(v, s) * F_ext(s) ** power
    return tot


def census(r):
    q, rem = divmod(forced_moment(r, 3), 6 * 2 ** (2 * r + 1))
    assert rem == 0
    return q


def pair_count(r):
    """P_m: forced #pairs with |B1 cap B2| = (r-1)/2, via inversion of
    sum_j C(j,i) n_j = C(r,i)(lam_i - 1)."""
    v = 2 * r + 1
    lam = lam_vec(r)
    b = lam[0]
    rhs = [comb(r, i) * (lam[i] - 1) for i in range(r)]
    n = [0] * r
    for j in range(r - 1, -1, -1):
        n[j] = rhs[j] - sum(comb(i, j) * n[i] for i in range(j + 1, r))
    assert sum(n) == b - 1
    m = (r - 1) // 2
    num = b * n[m]
    assert num % 2 == 0
    return num // 2


def main():
    # weight-1/2 analogues vanish: no block B with 1_B in {0, 1_X}, and no
    # pair with B1 xor B2 = X (a block complement is never a block)
    for r in (3, 5, 15):
        assert forced_moment(r, 1) == 0
        assert forced_moment(r, 2) == 0
    print("[ok] signed power-1 and power-2 sums vanish identically")

    # r=15 headline numbers
    T15, P15 = census(15), pair_count(15)
    assert T15 == 927696866625
    assert P15 == 43116291922275
    assert P15 == comb(31, 7) * 43263 * 758 // 2  # derived-design route
    assert 3 * T15 == 2783090599875
    assert P15 - 3 * T15 == 40333201322400
    print("[ok] r=15: T =", T15, " P7 =", P15, "(two routes agree)")
    print("[ok] r=15: closing pairs 3T =", 3 * T15,
          "; non-closing =", P15 - 3 * T15, " => universal closure REFUTED")

    # small r: forced census matches parameters AND closure is forced full
    assert census(3) == 7 and pair_count(3) == 21
    assert census(5) == 220 and pair_count(5) == 660
    print("[ok] r=3: 3T = 21 = P1 ; r=5: 3T = 660 = P2 (closure forced)")

    # actual-design controls
    src = open(f"{HERE}/verify_H_identity.py").read().split("if __name__")[0]
    ns = {}
    exec(compile(src, "verify_H_identity.py", "exec"), ns)
    for v, r in ((7, 3), (11, 5)):
        blocks = list(combinations(range(v), r))
        X0, Y0 = ns["cover_instance"](v, r - 1, blocks)
        A = ns["algox"](X0, Y0, cap=1)[0]
        Aset, full = set(A), frozenset(range(v))
        m = (r - 1) // 2
        pairs = close = 0
        for B1, B2 in combinations(A, 2):
            if len(set(B1) & set(B2)) == m:
                pairs += 1
                if tuple(sorted(full - (set(B1) ^ set(B2)))) in Aset:
                    close += 1
        assert close % 3 == 0 and close // 3 == census(r) and pairs == close
        print(f"[ok] actual r={r}: triples = {close // 3} = forced census; "
              f"full closure {close}/{pairs}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
