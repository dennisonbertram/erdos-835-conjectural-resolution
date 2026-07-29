#!/usr/bin/env python3
"""Deterministic verifier for the elementary p-rank / SNF audit of
S(14,15,31) and S(7,8,24)  (companion: s141531_prank_snf_audit.md).

Everything is exact integer arithmetic; numpy is used only for mod-p
integer Gaussian elimination (honest ranks).  No randomness, no network,
no files written.

Checks:
  1. Parameter tables (lambda integrality) for both designs.
  2. Eberlein eigenvalue machinery certified by the second-orthogonality
     identity, then the forced Gram spectra theta_j(i) for i <= t/2,
     asserted against the recorded tables (trace + row-sum identities).
  3. Sweep over ALL inclusion levels i <= t/2 and primes {2..31}:
     (a) spectral characteristic-polynomial lower bound <= Wilson p-rank
         upper bound
         of W_{i,k}(v)  (Wilson diagonal form, valid since v >= k+i);
     (b) Cauchy-Binet determinant test
         sum_j m_j v_p(theta_j) >= 2 sum_j m_j v_p(C(k-j,i-j)).
     Exhaustiveness: the primes dividing any Wilson diagonal entry are
     asserted to lie in the tested set, so an untested prime has
     full-rank upper bound and neither test can fire.
  4. Chain squeeze  W_{i,t} N_t = C(k-i,t-i) N_i:  for p | C(k-i,t-i),
     rank_p(N_t) <= C(v,t) - rank_p(W_{i,t}); recorded minima asserted,
     plus the vacuity inequality  C(v, floor(t/2)) < min upper bound.
  5. Honest mod-p ranks of the forced Grams (i <= 3), asserted against
     the recorded values, including the saturation equalities and the
     non-semisimple case (r=15, i=3, p=7): honest 464 > 434 = optimistic.
     The three 4495-dimensional eliminations run by default (~10 min);
     pass --fast to skip exactly those (all other checks still run).
  6. Explicit integral point-Gram factorizations
     N N^T = a I + c J = X X^T with X in Z^{v x (4v+4)} built from
     quaternion blocks -- the rectangular Gram-factorability test only.
  7. Scoped modular-intersection audit: the intra-block intersection
     distributions are computed; every level of the standard
     divisibility/rank contradiction family is exhausted; and the ordinary
     Ray-Chaudhuri-Wilson bound is checked with its exact slack.

Run:  python3 verify_s141531_prank_snf_audit.py          (~10 min)
      python3 verify_s141531_prank_snf_audit.py --fast   (~1 min)
"""
import sys
from math import comb
from itertools import combinations

import numpy as np

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
FAST = "--fast" in sys.argv

THETA = {
    (31, 15): {
        1: [128314125, 4562280],
        2: [419159475, 30834720, 1179900],
        3: [814229325, 93054780, 7385300, 305900],
        4: [1046866275, 165430720, 20451600, 1761984, 79534],
        5: [938302365, 192472280, 32995248, 4441668, 418418, 20748],
        6: [601475875, 153977824, 34370050, 6437200, 950950, 98800, 5434],
        7: [278397405, 86612526, 24208470, 5925150, 1222650, 200070,
            23166, 1430],
    },
    (24, 8): {
        1: [115368, 10032],
        2: [122892, 22344, 2280],
        3: [67032, 19152, 4104, 504],
    },
}
CHAIN = {(31, 15): {2: 145422675, 3: 195892564, 5: 240851988,
                    7: 259923345, 11: 265155555, 13: 265182091},
         (24, 8): {2: 245157, 3: 313974, 5: 344356, 7: 346081}}
HONEST = {
    (31, 15): {(1, 2): 1, (1, 3): 0, (1, 5): 0, (1, 7): 31,
               (2, 2): 1, (2, 3): 0, (2, 5): 0, (2, 7): 434,
               (3, 5): 0, (3, 7): 464, (3, 13): 4030},
    (24, 8): {(1, 2): 1, (1, 3): 0, (1, 5): 24, (1, 7): 24,
              (2, 2): 1, (2, 3): 0, (2, 5): 24, (2, 7): 252,
              (3, 2): 1, (3, 3): 0, (3, 7): 275},
}
QUAT = {(31, 15): ((2134, 88, 24, 2), (1997, 63, 4, 1)),
        (24, 8): ((100, 4, 4, 0), (66, 5, 2, 2))}


def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def mult(v, j):
    return comb(v, j) - (comb(v, j - 1) if j else 0)


def eberlein(v, i, m, j):
    return sum((-1) ** h * comb(j, h) * comb(i - j, m - h)
               * comb(v - i - j, m - h) for h in range(min(j, m) + 1))


def design(v, k):
    t = k - 1
    lam = []
    for s in range(t + 1):
        num, den = comb(v - s, t - s), k - s
        assert num % den == 0
        lam.append(num // den)
    return t, lam


def modp_rank(A, p):
    R = (A % p).astype(np.int64)
    n, m = R.shape
    r = 0
    for c in range(m):
        if r >= n:
            break
        nz = np.nonzero(R[r:, c])[0]
        if nz.size == 0:
            continue
        pr = r + int(nz[0])
        if pr != r:
            R[[r, pr]] = R[[pr, r]]
        R[r] = (R[r] * pow(int(R[r, c]), -1, p)) % p
        col = R[:, c].copy()
        col[r] = 0
        rows = np.nonzero(col)[0]
        if rows.size:
            R[rows] = (R[rows] - np.outer(col[rows], R[r])) % p
        r += 1
    return r


def gram(v, k, i, lam):
    sets = list(combinations(range(v), i))
    M = np.zeros((len(sets), v), dtype=np.int64)
    for a, S in enumerate(sets):
        M[a, list(S)] = 1
    inter = M @ M.T
    return np.array(lam, dtype=np.int64)[2 * i - inter]


def wilson_rank(v, top, i, p):
    """p-rank of W_{i,top}(v) by Wilson's diagonal form (v >= top + i)."""
    assert v >= top + i
    return sum(mult(v, j) for j in range(i + 1) if comb(top - j, i - j) % p)


def main():
    for (v, k) in ((31, 15), (24, 8)):
        t, lam = design(v, k)
        b = lam[0]
        print(f"===== S({t},{k},{v}), b = {b} =====")
        # -- spectra + sweep --
        wprimes = set()
        for i in range(1, t // 2 + 1):
            E = [[eberlein(v, i, m, j) for m in range(i + 1)]
                 for j in range(i + 1)]
            for a in range(i + 1):
                for c in range(i + 1):
                    s = sum(mult(v, j) * E[j][a] * E[j][c]
                            for j in range(i + 1))
                    want = comb(v, i) * comb(i, a) * comb(v - i, a) \
                        if a == c else 0
                    assert s == want
            theta = [sum(lam[i + m] * E[j][m] for m in range(i + 1))
                     for j in range(i + 1)]
            assert theta == THETA[(v, k)][i]
            assert sum(mult(v, j) * th for j, th in enumerate(theta)) \
                == comb(v, i) * lam[i]
            wdiag = [comb(k - j, i - j) for j in range(i + 1)]
            for d in wdiag:
                rest = d
                for p in PRIMES:
                    while rest % p == 0:
                        rest //= p
                        wprimes.add(p)
                assert rest == 1, "untested prime divides a Wilson entry"
            for p in PRIMES:
                OPT = sum(mult(v, j) for j in range(i + 1) if theta[j] % p)
                UPP = sum(mult(v, j) for j in range(i + 1) if wdiag[j] % p)
                assert OPT <= UPP, ("rank hit", v, k, i, p)
                detv = sum(mult(v, j) * vp(theta[j], p)
                           for j in range(i + 1))
                need = 2 * sum(mult(v, j) * vp(wdiag[j], p)
                               for j in range(i + 1))
                assert detv >= need, ("det hit", v, k, i, p)
        print(f"  [ok] spectra certified, i = 1..{t//2}; sweep over "
              f"{len(PRIMES)} primes: no rank hit, no determinant hit "
              f"(prime list provably exhaustive)")
        # -- chain squeeze --
        for p, rec in CHAIN[(v, k)].items():
            ubs = [comb(v, t) - wilson_rank(v, t, i, p)
                   for i in range(t) if comb(k - i, t - i) % p == 0]
            assert min(ubs) == rec
        vac = comb(v, t // 2)
        assert vac < min(CHAIN[(v, k)].values())
        print(f"  [ok] chain-squeeze minima reproduced; slack against the "
              f"audited Gram-rank lower bounds: "
              f"C({v},{t//2}) = {vac} < {min(CHAIN[(v, k)].values())}")
        # -- honest ranks --
        for (i, p), rec in sorted(HONEST[(v, k)].items()):
            if FAST and i == 3:
                print(f"  [skip --fast] honest rank i={i} p={p} "
                      f"(recorded {rec})")
                continue
            G = gram(v, k, i, lam)
            hr = modp_rank(G, p)
            ub = wilson_rank(v, k, i, p)
            assert hr == rec and hr <= ub, (v, k, i, p, hr, rec, ub)
            print(f"  [ok] honest rank_p(Gram_{i}) mod {p}: {hr} <= "
                  f"Wilson {ub}" + ("  (saturated)" if hr == ub else ""))
        # non-semisimple witness at r=15
        if (v, k) == (31, 15) and not FAST:
            th = THETA[(v, k)][3]
            opt7 = sum(mult(v, j) for j in range(4) if th[j] % 7)
            assert opt7 == 434 and HONEST[(v, k)][(3, 7)] == 464 > opt7
            print("  [ok] non-semisimple witness: honest 464 > optimistic "
                  "434 at (i=3, p=7)")
        # -- Gram factorization --
        a, c = lam[1] - lam[2], lam[2]
        qa, qc = QUAT[(v, k)]
        assert sum(x * x for x in qa) == a and sum(x * x for x in qc) == c
        w, x, y, z = qa
        Q = np.array([[w, x, y, z], [-x, w, -z, y],
                      [-y, z, w, -x], [-z, -y, x, w]], dtype=np.int64)
        assert (Q @ Q.T == a * np.eye(4, dtype=np.int64)).all()
        # each point gets its own 4 columns holding one norm-a vector;
        # disjoint supports give a*I, the shared first 4 columns give c*J
        X = np.zeros((v, 4 * v + 4), dtype=np.int64)
        X[:, :4] = np.array(qc, dtype=np.int64)
        for r_ in range(v):
            X[r_, 4 + 4 * r_: 8 + 4 * r_] = Q[0]
        GX = X @ X.T
        want = a * np.eye(v, dtype=np.int64) + c * np.ones((v, v),
                                                           dtype=np.int64)
        assert (GX == want).all()
        assert 4 * v + 4 <= b
        print(f"  [ok] integral factorization N N^T = {a} I + {c} J = "
              f"X X^T, X in Z^({v}x{4*v+4}), {4*v+4} <= b")
        # -- scoped modular-intersection audit --
        rhs = [comb(k, i) * (lam[i] - 1) for i in range(t)]
        n = [0] * t
        for j in range(t - 1, -1, -1):
            n[j] = rhs[j] - sum(comb(i2, j) * n[i2]
                                for i2 in range(j + 1, t))
        assert sum(n) == b - 1
        if (v, k) == (31, 15):
            assert n[0] == 0 and n[13] > 0 and all(n[j] > 0
                                                   for j in range(1, 14))
        else:
            assert all(n[j] > 0 for j in range(0, 7))
        realized = [j for j in range(t) if n[j] > 0]
        s_cls = len(realized)
        # (i) Divisibility-contradiction family: at level i it needs
        # p | C(j,i) for every realized j, p not dividing C(k,i), and
        # b > C(v,i).  Exhaust every 0 <= i <= k:
        #   * i in the realized interval: j=i gives C(i,i)=1;
        #   * i below the interval: only i=0 can occur, and C(j,0)=1;
        #   * i above the interval: the row-dimension inequality is slack.
        assert all(i in realized for i in range(min(realized),
                                                max(realized) + 1))
        below = list(range(0, min(realized)))
        assert all(any(comb(j, i) == 1 for j in realized) for i in below)
        above = list(range(max(realized) + 1, k + 1))
        assert all(b <= comb(v, i) for i in above)
        if (v, k) == (31, 15):
            assert above == [14, 15]
            assert [comb(v, i) for i in above] == [265182525, 300540195]
        else:
            assert above == [7, 8]
            assert [comb(v, i) for i in above] == [346104, 735471]
        # (ii) bound-form Ray-Chaudhuri-Wilson: b <= C(v, s) holds with slack
        assert b <= comb(v, s_cls)
        print(f"  [ok] full intersection spectrum ({s_cls} classes) -> all "
              f"levels i=0..{k} of the scoped divisibility/rank family are "
              f"harmless; RW bound is slack: b = {b} <= C({v},{s_cls}) = "
              f"{comb(v, s_cls)}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
