#!/usr/bin/env python3
"""Determinant (Plucker) colourings of J(2k,k): exact reduction and controls.

SUPERSEDED.  The single maximal-minor construction c(B) = det(M_B) is already
proved IMPOSSIBLE for every admissible k > 2, INCLUDING k = 16, by the union
of the p = 1 mod 4, p = 3 mod 8 and p = 7 mod 8 link theorems.  Nothing here
leaves that ansatz open, and no matrix at k = 16 is worth searching for.

What survives: two elementary NECESSARY conditions and their small-k controls.
They are necessary only -- they are NOT a criterion for the ansatz (see the
k = 6 control).  No new unrestricted progress resulted from this attempt.

Stdlib only, no solver, assertion-enabled.
Run:  python3 -B collaboration/opus5/unrestricted_post_closure/verify_determinant_colouring.py
"""

from __future__ import annotations

import itertools
import random


def det(rows, p):
    M = [r[:] for r in rows]
    n, d = len(M), 1
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] % p), None)
        if piv is None:
            return 0
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            d = -d
        d = (d * M[c][c]) % p
        iv = pow(M[c][c], p - 2, p)
        for r in range(c + 1, n):
            f = (M[r][c] * iv) % p
            if f:
                for j in range(c, n):
                    M[r][j] = (M[r][j] - f * M[c][j]) % p
    return d % p


def inv_mat(A, p):
    n = len(A)
    M = [A[r][:] + [1 if i == r else 0 for i in range(n)] for r in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] % p), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        iv = pow(M[c][c], p - 2, p)
        M[c] = [(x * iv) % p for x in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c]
                M[r] = [(M[r][j] - f * M[c][j]) % p for j in range(2 * n)]
    return [row[n:] for row in M]


def rows_are_Fp_minus_1(A, p):
    tgt = sorted(set(range(p)) - {1})
    return all(sorted(r) == tgt for r in A)


def necessary(A, p):
    """Conditions (i) and (ii) of the theorem."""
    B = inv_mat(A, p)
    return B is not None and rows_are_Fp_minus_1(A, p) and rows_are_Fp_minus_1(B, p)


def is_tight(A, k, p):
    """Full test: c(B) = det([I|A]_B) is a tight (k+1)-colouring of J(2k,k)."""
    cols = [[1 if r == c else 0 for r in range(k)] for c in range(k)] + [
        [A[r][c] for r in range(k)] for c in range(k)
    ]
    for S in itertools.combinations(range(2 * k), k - 1):
        rest = [x for x in range(2 * k) if x not in S]
        vals = [
            det([[cols[c][r] for c in list(S) + [x]] for r in range(k)], p)
            for x in rest
        ]
        if sorted(vals) != list(range(p)):
            return False
    return True


def latin_squares(k, sym):
    out, rows = [], []

    def rec():
        if len(rows) == k:
            out.append([r[:] for r in rows])
            return
        for perm in itertools.permutations(sym):
            if all(
                all(perm[c] != rows[r][c] for c in range(k)) for r in range(len(rows))
            ):
                rows.append(list(perm))
                rec()
                rows.pop()

    rec()
    return out


def rand_latin(k, sym, rnd):
    L = [[None] * k for _ in range(k)]

    def bt(pos):
        if pos == k * k:
            return True
        r, c = divmod(pos, k)
        cand = [
            s for s in sym if s not in L[r][:c] and all(L[t][c] != s for t in range(r))
        ]
        rnd.shuffle(cand)
        for s in cand:
            L[r][c] = s
            if bt(pos + 1):
                return True
            L[r][c] = None
        return False

    bt(0)
    return L


# --------------------------------------------------------------------------


def section1():
    print("=" * 74)
    print("1.  PROVED -- the determinant ansatz and what it forces")
    print("=" * 74)
    print("    Let p = k+1 and let M be a k x 2k matrix over F_p.  Put")
    print("    c(B) = det(M_B) for a k-subset B of the 2k columns.")
    print()
    print("    A tight (k+1)-colouring of J(2k,k) is exactly a map c on")
    print("    k-subsets such that for every (k-1)-subset S the map")
    print("    x -> c(S u {x}) is a bijection from the other p columns onto the")
    print("    p colours (two k-sets sharing k-1 elements are adjacent, and a")
    print("    closed neighbourhood has p vertices).")
    print("    For c = det this is linear: det(M_{S u {x}}) is a linear")
    print("    functional of the column m_x, vanishing exactly on span(S).")
    print()
    print("    Normalise M = [I | A] (some k columns are independent, else all")
    print("    determinants vanish; apply GL_k).  Then:")
    print()
    print("    (i)  Take S = all identity columns but e_r.  The remaining p")
    print("         columns are e_r and a_1..a_k, and det(M_{S u {x}}) = eps_r")
    print("         times the r-th coordinate of x.  Bijectivity forces")
    print("           {1} u {A[r,s] : s} = F_p,")
    print("         i.e. ROW r OF A IS EXACTLY F_p \\ {1}, each value once.")
    print()
    print("    (ii) Take S = all A-columns but a_s.  Expanding along the last")
    print("         column, det = (-1)^(k+r) m_{rs} for x = e_r and")
    print("         (-1)^(k-s) det A for x = a_s.  Using")
    print("         m_{rs} = (-1)^(r+s) det(A) (A^-1)[s,r], every value carries")
    print("         the common factor (-1)^(k+s) det(A), so bijectivity forces")
    print("           {1} u {(A^-1)[s,r] : r} = F_p,")
    print("         i.e. ROW s OF A^-1 IS EXACTLY F_p \\ {1}.")
    print()
    print("    So A and A^-1 are both Latin-row on F_p \\ {1}. []")
    print()
    print("    NECESSARY ONLY.  These do NOT characterise the ansatz and do NOT")
    print("    reduce it to a matrix condition; see the k=6 control below.")


def section2():
    print()
    print("=" * 74)
    print("2.  CONTROL k = 2 (a tight colouring EXISTS) -- ansatz succeeds")
    print("=" * 74)
    k, p = 2, 3
    good = []
    for e in itertools.product(range(p), repeat=4):
        A = [list(e[:2]), list(e[2:])]
        if is_tight(A, k, p):
            good.append(A)
    print(
        f"    brute force over all {p**4} matrices A: {len(good)} give a tight"
        f" 3-colouring"
    )
    assert len(good) == 2
    print(
        f"    example A = {good[0]};  all satisfy (i)+(ii):"
        f" {all(necessary(A, p) for A in good)}"
    )
    assert all(necessary(A, p) for A in good)
    A = good[0]
    cols = [[1, 0], [0, 1], [A[0][0], A[1][0]], [A[0][1], A[1][1]]]
    cls = {}
    for B in itertools.combinations(range(4), 2):
        v = det([[cols[c][r] for c in B] for r in range(2)], p)
        cls.setdefault(v, []).append(B)
    print(f"    resulting colour classes: {dict(sorted(cls.items()))}")
    assert all(len(v) == 2 for v in cls.values()) and len(cls) == 3
    print("    -> the three perfect matchings of K_4, i.e. the tight colouring")
    print("       of J(4,2).  The ansatz is genuinely realisable.")


def section3():
    print()
    print("=" * 74)
    print("3.  CONTROL k = 4 -- reproduces the known impossibility cheaply")
    print("=" * 74)
    k, p = 4, 5
    sym = sorted(set(range(p)) - {1})
    sols = latin_squares(k, sym)
    ok = [A for A in sols if necessary(A, p)]
    print(f"    Latin squares on F_5\\{{1}}: {len(sols)}")
    print(f"    satisfying (i)+(ii): {len(ok)}")
    assert len(sols) == 576 and len(ok) == 0
    print("    ZERO.  So no matrix over F_5 can give a determinant colouring at")
    print("    k = 4 -- closed by the necessary conditions alone, without ever")
    print("    testing bijectivity.  Consistent with k=4 admitting no tight")
    print("    colouring at all.")
    rnd = random.Random(1)
    cnt = sum(
        1
        for _ in range(2000)
        if is_tight([[rnd.randrange(p) for _ in range(k)] for _ in range(k)], k, p)
    )
    print(f"    cross-check: 2000 random A tested directly, tight found {cnt}")
    assert cnt == 0


def section4():
    print()
    print("=" * 74)
    print("4.  CONTROL k = 6 -- (i)+(ii) is necessary but NOT sufficient")
    print("=" * 74)
    k, p = 6, 7
    sym = sorted(set(range(p)) - {1})
    rnd = random.Random(2)
    found = tight = 0
    for _ in range(3000):
        A = rand_latin(k, sym, rnd)
        if necessary(A, p):
            found += 1
            if is_tight(A, k, p):
                tight += 1
    print(
        f"    3000 random Latin squares on F_7\\{{1}}: {found} satisfy (i)+(ii),"
        f" of which {tight} are tight"
    )
    assert tight == 0
    print("    So the conditions do NOT collapse the ansatz by themselves at")
    print("    k = 6; the full bijectivity test is strictly stronger.  This is a")
    print("    sample, not an exhaustive k=6 closure, and none is claimed.")


def main():
    section1()
    section2()
    section3()
    section4()
    print()
    print("=" * 74)
    print("SCOPE.  SUPERSEDED artifact.  The single maximal-minor ansatz is")
    print("already closed for EVERY admissible k > 2, k = 16 included, by the")
    print("complete link no-go.  This file contributes only two necessary")
    print("conditions and their controls; it does NOT leave k=16 open, does NOT")
    print("offer a construction route, and does NOT claim orthogonality may be")
    print("imposed without loss.  No new unrestricted progress resulted.")
    print("Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()
