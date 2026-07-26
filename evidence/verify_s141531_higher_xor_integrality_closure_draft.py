#!/usr/bin/env python3
"""Verifier for evidence/s141531_higher_xor_integrality_closure_draft.md.

Deterministic, exact (integer / Fraction) arithmetic, standard library only.
DRAFT companion -- touches no other artifact.

This is the audit record of a REJECTED closure attempt.  What it checks:

  A. Theorem C itself (VALID, general, unconditional), on independent
     surrogates: for random subsets S of a small F_2^n the inverse transform of
     K_j(F(u)) equals the exact count of j-subsets of S with the given XOR, for
     EVERY j.
  B. Necessity of hypothesis (H): the witness F = (2,0,0,0) on F_2^2, where
     a_1(00) = 1/2 and a_2(00) = -1/2 is non-integral AND negative.
  C0. Lemma D's counting step: forced shape + (H) forces S to consist of
     15-sets, to be an S(14,15,31), and to equal A -- so (H) <=> design.
  C. THE COUNTERMODEL that rejects the closure.  Two spectra on F_2^3 with
     IDENTICAL weight-layer multisets and identical branch counts, differing
     only in the assignment inside layer 1: for one, (H) holds and a_1 is the
     0/1 indicator; for the other, (H) fails with a_1' = -1/2 somewhere and
     a_3' non-integral.  Hence no scalar identity computed from layer/branch
     data alone does not DETERMINE whether (H) holds -- which is what the
     withdrawn argument needed it to do.
  D. Claim (3)'s punctured-generating-function identity.  This is recorded as
     an internal consistency check ONLY: it is derived from the layer/branch
     formula, which already presupposes F = transform(1_A), so it does NOT
     establish b | j A_j independently.
  E. Consistency: the layer formula reproduces the recorded m_D, t_E, A_3..A_6.

NOT claimed: that the all-j arithmetic is closed, or that Theorem B is
subsumed.  Theorem B is non-circular (it uses only |F(u)| <= b/31, valid for
every branch assignment) and remains the only unconditional all-j result.
This rejected argument does not prove conditions (1), (2), or (3).  They were
subsequently closed by separate noncircular notes and verifiers.  Nothing here
bears on Erdos-Rosenfeld Problem #835.

Run:  python3 -B evidence/verify_s141531_higher_xor_integrality_closure_draft.py
"""

import itertools
import random
from fractions import Fraction
from math import comb

V, R = 31, 15
B_COUNT = comb(V, R) // (R + 2)
FAILURES = []


def check(label, cond, detail=""):
    print(f"  [{'ok  ' if cond else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(label)


def lam(i):
    return comb(V - i, R - 1 - i) // (R - i)


BASE = [sum(comb(m, i) * (-2) ** i * lam(i) for i in range(min(m, R - 1) + 1))
        for m in range(R + 1)]
F0 = BASE[R]
F1 = BASE[R] + (-2) ** R
GAP = F1 - F0
PHI = [BASE[w] if w <= R else -BASE[V - w] for w in range(V + 1)]


def krawtchouk(w, d, n=V):
    return sum((-1) ** i * comb(d, i) * comb(n - d, w - i) for i in range(w + 1))


def _bp(P, i):
    num, den = Fraction(1), 1
    for a in range(i):
        num *= (P - a)
    for a in range(1, i + 1):
        den *= a
    return num / den


def Kj(j, F, b):
    """[z^j] (1+z)^((b+F)/2) (1-z)^((b-F)/2) -- exact, any b and F of like parity."""
    P, Q = Fraction(b + F, 2), Fraction(b - F, 2)
    return sum((-1) ** (j - i) * _bp(P, i) * _bp(Q, j - i) for i in range(j + 1))


def F_at(d, e=0):
    if d == R:
        return PHI[d] + GAP * e
    if d == R + 1:
        return PHI[d] - GAP * e
    return PHI[d]


def Delta(j):
    return Kj(j, F1, B_COUNT) - Kj(j, F0, B_COUNT)


def a(j, d, e=0):
    """a_j on layer d, branch e, via the hierarchy note's Theorem A formula."""
    if j < 0:
        return 0
    S = sum(Kj(j, PHI[w], B_COUNT) * krawtchouk(w, d) for w in range(V + 1))
    val = Fraction(S + Delta(j) * F_at(d, e) * (1 + (-1) ** (j + d)), 2 ** 31)
    assert val.denominator == 1, (j, d, e, val)
    return int(val)


def A_of(j):
    tot = Fraction(0)
    for w in range(0, V + 1, 2):
        tot += (B_COUNT * Kj(j, -F1, B_COUNT)
                + (comb(V, w) - B_COUNT) * Kj(j, -F0, B_COUNT)
                if w == R + 1 else comb(V, w) * Kj(j, PHI[w], B_COUNT))
    val = tot / 2 ** 30
    assert val.denominator == 1, (j, val)
    return int(val)


# ------------------------------------------------------------------ A

def surrogate(n, S):
    """Brute-force test of Theorem C's chain on G = F_2^n with subset S."""
    G = 1 << n
    b = len(S)

    def Fhat(u):
        return sum((-1) ** bin(u & B).count("1") for B in S)

    ok = True
    for j in range(b + 1):
        direct = {}
        for Y in itertools.combinations(S, j):
            x = 0
            for y in Y:
                x ^= y
            direct[x] = direct.get(x, 0) + 1
        for D in range(G):
            tot = sum((-1) ** bin(u & D).count("1") * Kj(j, Fhat(u), b)
                      for u in range(G))
            val = tot / G
            if val != direct.get(D, 0):
                ok = False
    return ok


def main():
    print("A. Theorem C on independent surrogates (brute force, all j)")
    rng = random.Random(835)
    allok = True
    for n, size in ((3, 4), (3, 6), (4, 5), (4, 7)):
        pool = list(range(1 << n))
        S = sorted(rng.sample(pool, size))
        r = surrogate(n, S)
        allok &= r
        print(f"    n={n}, |S|={size}: inverse transform of K_j(F^) == "
              f"subset count for every j -> {r}")
    check("Theorem C's chain validated on all surrogates", allok)

    print()
    print("B. Necessity of hypothesis (H): witness F = (2,0,0,0) on F_2^2")
    Fw = [2, 0, 0, 0]
    bw = Fw[0]
    def aw(j, D):
        return Fraction(sum((-1) ** bin(u & D).count("1") * Kj(j, Fw[u], bw)
                            for u in range(4)), 4)
    check("a_1(00) = 1/2, so (H) fails", aw(1, 0) == Fraction(1, 2), f"{aw(1,0)}")
    check("a_2(00) = -1/2: non-integral AND negative",
          aw(2, 0) == Fraction(-1, 2), f"{aw(2,0)}")

    print()
    print("C0. Lemma D: forced shape + (H) => S is the design and S = A")
    check("identity C(s,14) - 15*C(s,15) = C(s,14)*(15-s), s = 0..31",
          all(comb(s, 14) - 15 * comb(s, 15) == comb(s, 14) * (15 - s)
              for s in range(32)))
    check("for ODD s the term C(s,14)*(15-s) is <= 0, zero exactly for s <= 13 "
          "and s = 15",
          all(comb(s, 14) * (15 - s) <= 0 for s in range(1, 32, 2))
          and all(comb(s, 14) * (15 - s) == 0 for s in list(range(1, 14, 2)) + [15])
          and all(comb(s, 14) * (15 - s) < 0 for s in range(17, 32, 2)))
    check("step (a) is load-bearing: s = 14 would give a POSITIVE term +1",
          comb(14, 14) * (15 - 14) == 1)
    check("15*b = C(31,14) and lambda_14 = 1 (the i=14 incidence count)",
          15 * B_COUNT == comb(31, 14)
          and comb(31 - 14, 15 - 1 - 14) // (15 - 14) == 1)

    print()
    print("C. COUNTERMODEL: layer-multiset/branch-count data does NOT determine (H)")
    n = 3
    Gn = 1 << n

    def dot(u, v):
        return bin(u & v).count("1") & 1

    def inv(Fv):
        return [Fraction(sum((-1) ** dot(u, D) * Fv[u] for u in range(Gn)), Gn)
                for D in range(Gn)]

    def layers(Fv):
        return {w: sorted(Fv[u] for u in range(Gn) if bin(u).count("1") == w)
                for w in range(n + 1)}

    Sset = [0, 3, 5]
    Fc = [sum((-1) ** dot(u, B) for B in Sset) for u in range(Gn)]
    Fp = Fc[:]
    Fp[1], Fp[2] = Fc[2], Fc[1]          # swap INSIDE weight layer 1
    check("the two spectra have identical weight-layer multisets",
          layers(Fc) == layers(Fp), f"{layers(Fc)}")
    a1c, a1p = inv(Fc), inv(Fp)
    check("self-consistent spectrum: a_1 is the 0/1 indicator of S",
          all(x in (0, 1) for x in a1c) and [i for i, x in enumerate(a1c) if x] == Sset)
    check("reassigned spectrum: (H) FAILS, a_1' takes the value -1/2",
          Fraction(-1, 2) in a1p, f"a_1' = {[str(x) for x in a1p]}")
    bq = Fp[0]
    a3p = [Fraction(sum((-1) ** dot(u, D) * Kj(3, Fp[u], bq) for u in range(Gn)), Gn)
           for D in range(Gn)]
    check("and a_3' is non-integral too",
          any(x.denominator != 1 for x in a3p),
          f"non-integral at {[D for D, x in enumerate(a3p) if x.denominator != 1]}")
    check("=> layer-multiset/branch-count data alone does not determine (H)", True)

    print()
    print("D. Claim (3) punctured identity -- INTERNAL CONSISTENCY ONLY")
    print("   (derived from the layer/branch formula, which presupposes")
    print("    F = transform(1_A); does NOT independently prove b | j*A_j)")
    okk = True
    for j in range(2, 10):
        Aj = A_of(j)
        kap = Fraction(j * Aj, B_COUNT)
        ap0 = sum((-1) ** m * (a(j - m, 0) if m % 2 == 0 else a(j - m, R, 1))
                  for m in range(j + 1))
        ap1 = sum((-1) ** m * (a(j - m, V) if m % 2 == 0 else a(j - m, R + 1, 1))
                  for m in range(j + 1))
        same = (kap.denominator == 1 and int(kap) == Aj - (ap0 + ap1))
        okk &= same
        print(f"    j={j}: b | j*A_j and kappa_j = A_j - A'_j -> {same}"
              f"   kappa_j = {int(kap)}")
    check("kappa_j identity reproduces j*A_j/b for j = 2..9 "
          "(consistency check, not a proof)", okk)

    print()
    print("E. Consistency with the recorded values")
    MD = {28: 235980, 26: 174800, 24: 165186, 22: 153216, 20: 147972,
          18: 144144, 14: 144144, 12: 147972, 10: 153216, 8: 165186,
          6: 174800, 4: 235980}
    check("j=2 reproduces m_D on every layer", all(a(2, d) == m for d, m in MD.items()))
    check("j=2 reproduces the |D|=16 split 157425 / 142590",
          (a(2, 16, 1), a(2, 16, 0)) == (157425, 142590))
    check("j=3 reproduces the |E|=15 split 858252625232 / 858106686794",
          (a(3, R, 1), a(3, R, 0)) == (858252625232, 858106686794))
    check("A_3 .. A_6 reproduce",
          [A_of(j) for j in (3, 4, 5, 6)] ==
          [927696866625, 3793226637448341180,
           13402303385620814734177080,
           39490202682224904419269612470360])

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
        raise SystemExit(1)
    print("All checks passed.")
    print()
    print("VERDICT: the closure attempt is REJECTED as circular.  Theorem C is")
    print("valid, but (H) is full Fourier self-consistency of the unknown block")
    print("indicator; Lemma D (part C0) proves that under the forced shape (H) is")
    print("EQUIVALENT to A being an S(14,15,31).  Theorem A reached its")
    print("layer/branch formula by")
    print("substituting F(D) for transform(1_A)(D), which presupposes exactly")
    print("that.  Part C shows layer/branch data cannot supply (H).")
    print()
    print("STANDS: Theorem C; Lemma D ((H) <=> design); the countermodel; and")
    print("Theorem B's")
    print("non-negativity for all j (non-circular, NOT subsumed).")
    print("NOT PROVED HERE: conditions (1)-(3); separate later notes close them.")
    print("This does NOT solve Erdos-Rosenfeld Problem #835.")


if __name__ == "__main__":
    main()
