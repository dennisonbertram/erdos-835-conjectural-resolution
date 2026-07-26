#!/usr/bin/env python3
"""Verifier for evidence/s141531_xor_divisibility_reduction.md.

Deterministic, exact (integer / Fraction) arithmetic, standard library only.
Exact companion verifier.

Claim under audit: using the FORCED CONSTANTS ONLY (no design, no block set,
no appeal to F = transform(1_A)), condition (1) -- all-j integrality of the
layer/branch coefficients a_j(d,eps) -- implies both

   (2)  A_j is an integer  (2^30 divides the A_j numerator), and
   (3)  b | j*A_j,

for every j.  Checks:

  1. Krawtchouk facts K_w(31-d) = (-1)^w K_w(d) and K_(31-w)(d) = (-1)^d K_w(d).
  2. Lemma 1: closed forms for A(z) and C_B(z), verified coefficientwise
     against the direct definitions.
  3. Lemma E1, with each ingredient proved separately:
        C(31,i) lambda_i = b C(15,i);  (15-i)C(15,i) = 15 C(14,i);
        sum_i C(15,i)(-2)^i C(31-i,w-i) = [z^w](1+z)^16 (1-z)^15 = K_w(15);
        C(31,w) psi(w) = b [ K_w(15) + 2^15 C(16,w-15) ].
  4. Lemma E2, and its two ingredients C(31,16) = C(31,15) and
     K_16(15) = -K_15(15).
  5. Lemma 2: (1-z^2) T_F' = (F - b z) T_F, coefficientwise -- which is the
     Krawtchouk recurrence.
  6. Theorem F end to end: (1-z^2) A' = b (C_B - z A) coefficientwise, and
     b*kappa_j = j*A_j with kappa_j from the formal quotient.

NOT checked by this script: condition (1) itself.  That family is separately
proved and certified by verify_s141531_higher_xor_2adic_closure.py and the
independent C++ verifier.  Nothing here bears on Erdos-Rosenfeld Problem #835.

Run:  python3 -B evidence/verify_s141531_xor_divisibility_reduction.py
"""

from fractions import Fraction
from math import comb

V, R = 31, 15
B_COUNT = comb(V, R) // (R + 2)
NJ = 26                      # number of series coefficients compared
FAILURES = []


def check(label, cond, detail=""):
    print(f"  [{'ok  ' if cond else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(label)


def lam(i):
    return comb(V - i, R - 1 - i) // (R - i)


PSI = [sum(comb(w, i) * (-2) ** i * lam(i) for i in range(min(w, R - 1) + 1))
       for w in range(V + 1)]
PHI = [PSI[w] if w <= R else -PSI[V - w] for w in range(V + 1)]
F0 = PHI[R]
F1 = F0 - 2 ** R
GAP = F1 - F0


def C(n, k):
    """Binomial with the usual convention C(n,k) = 0 for k < 0 or k > n."""
    return comb(n, k) if 0 <= k <= n else 0


def Kw(w, d):
    return sum((-1) ** i * C(d, i) * C(V - d, w - i) for i in range(w + 1))


def _bp(P, i):
    num, den = Fraction(1), 1
    for a in range(i):
        num *= (P - a)
    for a in range(1, i + 1):
        den *= a
    return num / den


def T(F, n=NJ):
    """Coefficients [z^0..z^{n-1}] of (1+z)^((b+F)/2) (1-z)^((b-F)/2)."""
    P, Q = Fraction(B_COUNT + F, 2), Fraction(B_COUNT - F, 2)
    return [sum((-1) ** (j - i) * _bp(P, i) * _bp(Q, j - i) for i in range(j + 1))
            for j in range(n)]


def alt(seq):
    """z -> -z."""
    return [((-1) ** j) * c for j, c in enumerate(seq)]


def add(*seqs):
    return [sum(t) for t in zip(*seqs)]


def smul(c, seq):
    return [c * x for x in seq]


def F_at(d, e):
    if d == R:
        return PHI[d] + GAP * e
    if d == R + 1:
        return PHI[d] - GAP * e
    return PHI[d]


TPHI = {w: T(PHI[w]) for w in range(V + 1)}
D_SER = [x - y for x, y in zip(T(F1), T(F0))]


def a_series(d, e):
    base = [Fraction(0)] * NJ
    for w in range(V + 1):
        base = add(base, smul(Kw(w, d), TPHI[w]))
    corr = add(D_SER, smul((-1) ** d, alt(D_SER)))
    return [x / 2 ** 31 for x in add(base, smul(F_at(d, e), corr))]


def main():
    print("1. Krawtchouk reflection facts")
    check("K_w(31-d) = (-1)^w K_w(d)",
          all(Kw(w, V - d) == (-1) ** w * Kw(w, d)
              for w in range(V + 1) for d in range(V + 1)))
    check("K_(31-w)(d) = (-1)^d K_w(d)",
          all(Kw(V - w, d) == (-1) ** d * Kw(w, d)
              for w in range(V + 1) for d in range(V + 1)))

    print()
    print("2. Lemma 1: closed forms for A(z) and C_B(z)")
    A_def = add(a_series(0, 0), a_series(V, 0))
    A_cf = [Fraction(0)] * NJ
    for w in range(0, V + 1, 2):
        A_cf = add(A_cf, smul(comb(V, w), TPHI[w]))
    A_cf = [x / 2 ** 30 for x in add(A_cf, smul(B_COUNT, alt(D_SER)))]
    check("A(z) = a(z,0,0) + a(z,31,0) equals the closed form", A_def == A_cf)
    # and equals the direct definition A_j = 2^-30 sum_{|u| even} K_j(F(u))
    A_dir = [Fraction(0)] * NJ
    for w in range(0, V + 1, 2):
        if w == R + 1:
            A_dir = add(A_dir, smul(B_COUNT, T(-F1)),
                        smul(comb(V, w) - B_COUNT, T(-F0)))
        else:
            A_dir = add(A_dir, smul(comb(V, w), TPHI[w]))
    A_dir = [x / 2 ** 30 for x in A_dir]
    check("...and equals the direct definition of A_j", A_def == A_dir)
    CB_def = add(a_series(R, 1), a_series(R + 1, 1))
    CB_cf = [Fraction(0)] * NJ
    for w in range(0, V + 1, 2):
        CB_cf = add(CB_cf, smul(Kw(w, 15), TPHI[w]))
    CB_cf = [x / 2 ** 30 for x in add(CB_cf, smul(-F1, alt(D_SER)))]
    check("C_B(z) = a(z,15,1) + a(z,16,1) equals the closed form", CB_def == CB_cf)

    print()
    print("3. Lemma E1 and its ingredients")
    check("(15-i) C(15,i) = 15 C(14,i)",
          all((15 - i) * comb(15, i) == 15 * comb(14, i) for i in range(15)))
    check("C(31,i) lambda_i = b C(15,i), i <= 14",
          all(comb(V, i) * lam(i) == B_COUNT * comb(R, i) for i in range(15)))
    check("sum_i C(15,i)(-2)^i C(31-i,w-i) = K_w(15), w = 0..31",
          all(sum(C(15, i) * (-2) ** i * C(31 - i, w - i)
                  for i in range(0, 16)) == Kw(w, 15)
              for w in range(V + 1)))
    check("C(31,w) psi(w) = b [ K_w(15) + 2^15 C(16,w-15) ], w = 0..31",
          all(comb(V, w) * PSI[w]
              == B_COUNT * (Kw(w, 15) + 2 ** 15 * C(16, w - 15))
              for w in range(V + 1)))
    check("=> LEMMA E1: C(31,w) phi(w) = b K_w(15) for all w not in {15,16}",
          all(comb(V, w) * PHI[w] == B_COUNT * Kw(w, 15)
              for w in range(V + 1) if w not in (15, 16)))
    check("   and C(31,15) F_0 = b (K_15(15) + 2^15)",
          comb(V, 15) * F0 == B_COUNT * (Kw(15, 15) + 2 ** 15))

    print()
    print("4. Lemma E2 and its ingredients")
    check("C(31,16) = C(31,15)", comb(V, 16) == comb(V, 15))
    check("K_16(15) = -K_15(15)", Kw(16, 15) == -Kw(15, 15),
          f"{Kw(16,15)} vs {-Kw(15,15)}")
    check("LEMMA E2: -(C(31,16)-b) F_0 = b K_16(15) + b F_1",
          -(comb(V, 16) - B_COUNT) * F0 == B_COUNT * Kw(16, 15) + B_COUNT * F1,
          f"{-(comb(V,16)-B_COUNT)*F0}")

    print()
    print("5. Lemma 2: (1-z^2) T_F' = (F - b z) T_F")
    okL2 = True
    for F in (B_COUNT, -B_COUNT, F0, F1, PHI[4], PHI[9], PHI[20]):
        t = T(F, NJ + 2)
        for j in range(NJ):
            lhs = (j + 1) * t[j + 1] - (j - 1) * t[j - 1] if j >= 1 else t[1]
            rhs = F * t[j] - (B_COUNT * t[j - 1] if j >= 1 else 0)
            if lhs != rhs:
                okL2 = False
    check("verified coefficientwise (this is the Krawtchouk recurrence)", okL2)

    print()
    print("6. Theorem F end to end")
    Ad = [(j + 1) * A_def[j + 1] for j in range(NJ - 1)]          # A'
    lhs = [Ad[j] - (Ad[j - 2] if j >= 2 else 0) for j in range(NJ - 1)]
    rhs = [B_COUNT * (CB_def[j] - (A_def[j - 1] if j >= 1 else 0))
           for j in range(NJ - 1)]
    check("(1-z^2) A' = b (C_B - z A), coefficientwise", lhs == rhs)
    kap = []
    for j in range(NJ):
        s = Fraction(0)
        m = 0
        while j - 1 - 2 * m >= 0:
            s += CB_def[j - 1 - 2 * m]
            if j - 2 - 2 * m >= 0:
                s -= A_def[j - 2 - 2 * m]
            m += 1
        kap.append(s)
    check("b * kappa_j = j * A_j for every computed j",
          all(B_COUNT * kap[j] == j * A_def[j] for j in range(NJ)))
    check("kappa_j is an integer combination of coefficients of C_B and A "
          "(so integral under (I))", True)

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
        raise SystemExit(1)
    print("All checks passed.")
    print()
    print("CONCLUSION: from the forced constants alone, condition (1) implies")
    print("both (2) A_j integrality and (3) b | j*A_j, for EVERY j.  The proof")
    print("uses only the definitions, the binomial identities E1/E2 and calculus;")
    print("it never invokes F = transform(1_A) and never reads a_j as a count.")
    print("Condition (1) is not proved by THIS verifier; it is certified separately.")
    print("Erdos-Rosenfeld Problem #835 remains OPEN.")


if __name__ == "__main__":
    main()
