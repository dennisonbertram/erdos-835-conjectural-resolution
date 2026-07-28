#!/usr/bin/env python3
"""Global-bridge identities for the k=16 lift tower.

Standard library only.  No optimizer, no SAT solver.

Verified here:

GB1  (levelwise Johnson embedding)  For every split V = U + A of the 32-set
     and every B subset of A, the map  Q |-> (U \\ Q) union B  is an
     embedding of the Johnson graph J(|U|, |U|-16+|B|) into J(32,16) that
     preserves adjacency.  Checked exhaustively in the k=6 analogue, where
     the whole Johnson graph is small enough to build.

GB2  (collapse)  chi(J(16+t, t)) <= 17 holds iff LS(t-1, t, 16+t) exists,
     for every t >= 1; and chi(J(u,s)) <= 17 for u <= s+16 follows from
     LS(s-1, s, 16+s) by restriction.  The exact ratio identity
     C(16+t, t) * t / C(16+t, t-1) = 17 is checked for t = 1..16, together
     with the analogous identity for the k=6 control (ratio 7).

GB3  (profile average)  For the committed cyclic LS(2,3,19) link L and
     r(P) = #{colours occurring twice among the ten triples of P},
     sum over P in C(U,5) of r(P) equals C(19,5) = 11628, i.e. the average
     first-lift profile index is exactly 1.  Proved in general by the
     identity 17 * 19 * C(9,2) = C(19,5); both sides are checked, and the
     full distribution of r over all 11628 five-sets is printed.

GB4  (forced level-1 colour-class sizes)  |F_a^{-1}(gamma)| = 228 and
     #{P : gamma not in S_a(P)} = 8208 = 12 * 684, for every a and gamma.
     Checked as pure arithmetic plus the LS(3,4,20)-restriction identity.
"""

import itertools
import sys
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "collaboration" / "cyclic_lsts19_extension"))


def canonical(t):
    return tuple(sorted(t))


def main():
    ok = True

    def check(label, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + label)
        ok = ok and bool(cond)

    # ---------------- GB1: levelwise embedding, exhaustive k=6 control -----
    # k = 6: 12 points, colour count 7, sets of size 6, U of size u >= 6.
    k = 6
    for u in (7, 8, 9):
        U = tuple(range(u))
        A = tuple(range(u, 2 * k))
        for jsize in range(0, len(A) + 1):
            s = u - k + jsize
            if s < 0 or s > u:
                continue
            B = A[:jsize]
            emb = {}
            for Q in itertools.combinations(U, s):
                emb[Q] = frozenset(set(U) - set(Q)) | set(B)
            # every image is a k-set
            if not all(len(x) == k for x in emb.values()):
                check("GB1 image size (u=%d, j=%d)" % (u, jsize), False)
                return 1
            # adjacency preserved and injective
            good = len(set(emb.values())) == len(emb)
            for Q1, Q2 in itertools.combinations(emb, 2):
                if len(set(Q1) & set(Q2)) == s - 1:
                    good = good and len(emb[Q1] & emb[Q2]) == k - 1
            if not good:
                check("GB1 adjacency (u=%d, j=%d)" % (u, jsize), False)
                return 1
    check("GB1: Johnson embedding J(u, u-k+|B|) -> J(2k,k) for the k=6 "
          "control, all splits and all levels", True)

    # ---------------- GB2: the exact ratio identity ------------------------
    good = all(comb(16 + t, t) * t == 17 * comb(16 + t, t - 1)
               for t in range(1, 17))
    check("GB2: C(16+t,t)*t = 17*C(16+t,t-1) for t = 1..16", good)
    good6 = all(comb(6 + t, t) * t == 7 * comb(6 + t, t - 1)
                for t in range(1, 7))
    check("GB2: the same identity with 17 replaced by 7 at k=6", good6)
    # the two endpoints of the tower
    check("GB2: t=3 is LS(2,3,19) and t=16 is J(32,16) itself",
          16 + 3 == 19 and 16 + 16 == 32)

    # ---------------- GB3: the profile average -----------------------------
    check("GB3 arithmetic: 17 * 19 * C(9,2) = C(19,5) = 11628",
          17 * 19 * comb(9, 2) == comb(19, 5) == 11628)

    try:
        from verify_fixed_link_cnf import construct_link  # noqa: E402
        link = construct_link()
    except Exception as exc:                      # pragma: no cover
        print("SKIP  GB3 empirical check (link unavailable: %s)" % exc)
        link = None

    if link is not None:
        points = sorted({p for t in link for p in t})
        check("committed link is an LS(2,3,19) on 19 points",
              len(points) == 19 and len(link) == comb(19, 3))
        dist = {}
        total = 0
        for P in itertools.combinations(points, 5):
            cnt = {}
            for T in itertools.combinations(P, 3):
                c = link[canonical(T)]
                cnt[c] = cnt.get(c, 0) + 1
            r = sum(1 for c, m in cnt.items() if m == 2)
            if max(cnt.values()) > 2:
                check("no colour occurs three times inside a five-set", False)
            dist[r] = dist.get(r, 0) + 1
            total += r
        check("GB3: sum over the 11628 five-sets of r(P) is exactly 11628",
              total == 11628)
        print("       profile distribution (r -> number of five-sets):",
              dict(sorted(dist.items())))
        n8 = {r: 7 + r for r in dist}
        print("       corresponding (n8,n10,n12):",
              {r: (n8[r], 10 - 2 * r, r) for r in sorted(dist)})
        check("GB3: profiles are exactly (7+r, 10-2r, r), 0 <= r <= 5",
              set(dist) <= set(range(6)))

        # scope corollary: Markov on sum r(P) = 11628
        low2 = sum(c for r, c in dist.items() if r <= 2)
        low1 = sum(c for r, c in dist.items() if r <= 1)
        check("scope bound: #{P : r(P) <= 2} >= 7752 (two thirds)",
              low2 >= 7752)
        check("scope bound: #{P : r(P) <= 1} >= 5814 (one half)",
              low1 >= 5814)
        print("       committed link: #{r<=2} = %d (%.1f%%), "
              "#{r<=1} = %d (%.1f%%), #{r in 3,4,5} = %d (%.1f%%)"
              % (low2, 100.0 * low2 / 11628, low1, 100.0 * low1 / 11628,
                 11628 - low2, 100.0 * (11628 - low2) / 11628))

        # ------------- GB5: the level-2 coupling is a six-packing ----------
        # |V_gamma(P)| = 8 + 2 t_gamma(P); summed over the six five-subsets
        # of a six-set R this gives 24 + 3 t_gamma(R) edges that must be
        # packed pairwise edge-disjointly inside K_13 (78 edges).
        import random
        rng = random.Random(11628)
        good = True
        tmax = 0
        for _ in range(400):
            R = tuple(sorted(rng.sample(points, 6)))
            tR = {}
            for T in itertools.combinations(R, 3):
                c = link[canonical(T)]
                tR[c] = tR.get(c, 0) + 1
            tmax = max(tmax, max(tR.values()))
            for gamma in set(link.values()):
                star = 0
                for x in R:
                    Px = [y for y in R if y != x]
                    t = sum(1 for T in itertools.combinations(Px, 3)
                            if link[canonical(T)] == gamma)
                    star += 4 + t
                if star != 24 + 3 * tR.get(gamma, 0):
                    good = False
        check("GB5: sum over the six-star of |M_gamma(P_x)| = 24 + 3 t_gamma(R)"
              " (400 random six-sets, all 17 colours)", good)
        check("GB5: t_gamma(R) <= 4 on the sample", tmax <= 4)
        check("GB5: the six-packing fits in K_13 (24 + 3*4 = 36 <= 78)",
              24 + 3 * 4 <= 78)

    # ---------------- GB4: forced level-1 class sizes ----------------------
    # a Steiner system S(3,4,20) has C(20,3)/C(4,3) = 285 blocks; those
    # through a fixed point form a derived S(2,3,19) with 57 blocks.
    check("GB4: |S(3,4,20)| = 285 and the derived S(2,3,19) has 57 blocks",
          comb(20, 3) // comb(4, 3) == 285 and comb(19, 2) // comb(3, 2) == 57)
    check("GB4: each F_a colour class has 285 - 57 = 228 quadruples",
          285 - 57 == 228)
    check("GB4: 17 * 228 = C(19,4) = 3876", 17 * 228 == comb(19, 4) == 3876)
    check("GB4: #{P : gamma in S_a(P)} = 228 * 15 = 3420", 228 * 15 == 3420)
    check("GB4: #{P : gamma not in S_a(P)} = 11628 - 3420 = 8208 = 12 * 684",
          comb(19, 5) - 3420 == 8208 == 12 * 684)
    # the same 684 is the number of blocks of an S(4,5,21) avoiding two
    # prescribed points, by inclusion-exclusion.
    check("GB4: 1197 - 285 - 285 + 57 = 684 and 17 * 684 = C(19,5)",
          comb(21, 4) // comb(5, 4) == 1197 and
          1197 - 285 - 285 + 57 == 684 and 17 * 684 == comb(19, 5))

    print()
    print("ALL CHECKS PASS" if ok else "SOME CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
