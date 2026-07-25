#!/usr/bin/env python3
"""Validator: the second-moment M2 identity, its decomposition, and the
reduction of Conjecture E to two evenness statements.

Definitions (pair of mates B, C of leg A; m = (r+1)/2, mu = (r+3)/2):
  M2 = #{ordered (P,Q), P != Q :
         |H_B(P) intersection H_C(Q)| = r-1}
  E3 = #{ordered (P,Q), |P intersection Q| = r-2 :
         w_B(P) = w_C(Q)}
  X3 = #{ordered (P,Q), |P intersection Q| = r-3 :
         w_B(P) in Q, w_C(Q) in P}

PROVED identities (checked exactly on every mate pair):
  (H-level law) every (r+1+k)-set contains exactly C(r+1+k, r+2)/k
      H-sets of one tiling; in particular every (r+3)-set contains
      exactly mu of each.
  (M2 value)  M2 = mu^2 C(2r+1, r+3) - b C(r,2) - t C(r,2)
  (M2 split)  M2 = 2 r b (m-1) - 2 (r-1) t + E3 + X3
  (congruence, r = 3 mod 4; C(r,2) odd)
      t = E3 + X3 + mu^2 C(2r+1,r+3) + b C(r,2)   (mod 2)

REDUCTION THEOREM (PROVED): at r = 15, all C(31,k) are odd (31 = 2^5-1,
Lucas), so mu^2 N3 + b C(15,2) is even; hence
      E3 even and X3 even  ==>  t even  ==>  Conjecture E
      ==> no LS(14,15,31) ==> chi(J(32,16)) >= 18.

FINITE-VERIFIED: E3 and X3 are even in every instance at r=3
(E3, X3) = (6, 0) and r=5 ((212,352), (220,320), (240,300));
localization is REFUTED: per-point counts K_z and per-Y X3 counts take
odd values freely — the evenness is global.

CONJECTURAL: evenness of E3 and X3 at r=15.
Run: python3 verify_M2_reduction.py
"""
import sys
from itertools import combinations
from collections import Counter
from math import comb

sys.setrecursionlimit(100000)
HERE = __file__.rsplit("/", 1)[0] or "."
src = open(f"{HERE}/verify_H_identity.py").read().split("if __name__")[0]
ns = {}
exec(compile(src, "verify_H_identity.py", "exec"), ns)


def run(v, r):
    m = (r + 1) // 2
    mu = (r + 3) // 2
    N3 = comb(2 * r + 1, r + 3)
    blocks = list(combinations(range(v), r))
    X0, Y0 = ns["cover_instance"](v, r - 1, blocks)
    A = ns["algox"](X0, Y0, cap=1)[0]
    b = len(A)
    rest = [x for x in blocks if x not in set(A)]
    X1, Y1 = ns["cover_instance"](v, r - 1, rest)
    mates = ns["algox"](X1, Y1, cap=None)
    ws = [ns["wmap"](A, M, v) for M in mates]
    Asets = {P: set(P) for P in A}
    # H-level law for k = 2 on a sample tiling
    w0 = ws[0]
    Hs = [set(P) | {w0[P]} for P in A]
    for Y in combinations(range(v), r + 3):
        Ys = set(Y)
        assert sum(1 for H in Hs if H <= Ys) == mu
    print(f"[r={r}] H-level law (k=2): every (r+3)-set has exactly "
          f"{mu} H-sets OK")
    p2 = [(P, S) for P in A for S in A
          if P != S and len(Asets[P] & Asets[S]) == r - 2]
    p3 = [(P, S) for P in A for S in A
          if P != S and len(Asets[P] & Asets[S]) == r - 3]
    species = Counter()
    odd_point_values = set()
    odd_union_values = set()
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            wB, wC = ws[i], ws[j]
            t = sum(1 for P in A if wB[P] != wC[P])
            M2 = 0
            for P in A:
                HB = Asets[P] | {wB[P]}
                for Q in A:
                    if Q == P:
                        continue
                    if len(HB & (Asets[Q] | {wC[Q]})) == r - 1:
                        M2 += 1
            assert M2 == mu * mu * N3 - b * comb(r, 2) - t * comb(r, 2)
            E3_by_point = Counter()
            for P, Q in p2:
                if wB[P] == wC[Q]:
                    E3_by_point[wB[P]] += 1
            E3 = sum(E3_by_point.values())
            X3_by_union = Counter()
            for P, Q in p3:
                if wB[P] in Asets[Q] and wC[Q] in Asets[P]:
                    X3_by_union[tuple(sorted(Asets[P] | Asets[Q]))] += 1
            X3 = sum(X3_by_union.values())
            assert M2 == 2 * r * b * (m - 1) - 2 * (r - 1) * t + E3 + X3
            if r % 4 == 3:
                assert t % 2 == (E3 + X3 + mu * mu * N3
                                 + b * comb(r, 2)) % 2
            # needed for the reduction: combined parity
            assert (E3 + X3) % 2 == 0
            # optional STRONGER conjecture (observed in all finite data)
            assert E3 % 2 == 0 and X3 % 2 == 0
            odd_point_values.update(
                value for value in E3_by_point.values() if value % 2
            )
            odd_union_values.update(
                value for value in X3_by_union.values() if value % 2
            )
            species[(t, E3, X3)] += 1
    print(f"[r={r}] M2 identities + evenness verified on "
          f"{sum(species.values())} pairs; species:")
    for k, c in sorted(species.items()):
        print(f"    (t, E3, X3) = {k}  x{c}")
    if r == 3:
        assert odd_point_values == {1}
        assert not odd_union_values
    if r == 5:
        assert {17, 19, 21, 25} <= odd_point_values
        assert {1, 3} <= odd_union_values
    print(f"[r={r}] odd localized E3 values={sorted(odd_point_values)}; "
          f"odd localized X3 values={sorted(odd_union_values)}")


if __name__ == "__main__":
    run(7, 3)
    run(11, 5)
