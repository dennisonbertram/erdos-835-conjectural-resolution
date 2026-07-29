#!/usr/bin/env python3
"""Audit of the flag Latin-square construction and its parity identity.

Stdlib only, no solver.

  1  The construction Q^{(i,u)} is a Latin square of order k -- proof, with
     each of the four rainbow claims traced to the condition that supplies it,
     plus a concrete instantiation at k = 2.
  2  The parity identity rho*gamma*sigma = (-1)^(n(n-1)/2), verified
     exhaustively at n = 3, 4, 5.
  3  WHY THE ROUTE COLLAPSES: rho*gamma*sigma is constant over ALL Latin
     squares of a given order, so it is satisfied identically and cannot
     produce a contradiction.
  4  The refinement that does have content: for n EVEN the Alon-Tarsi sign
     rho*gamma is also reference-independent, and it is NOT constant.

Run:  python3 -B collaboration/opus5/radius5_followup/verify_flag_latin_square.py
"""
from __future__ import annotations

from itertools import permutations


def sgn(seq):
    s, seq = 1, list(seq)
    n = len(seq)
    seen = [False] * n
    for i in range(n):
        if seen[i]:
            continue
        L, j = 0, i
        while not seen[j]:
            seen[j] = True
            L += 1
            j = seq[j]
        if L % 2 == 0:
            s = -s
    return s


def all_latin(n):
    out, rows = [], []

    def rec():
        if len(rows) == n:
            out.append([r[:] for r in rows])
            return
        for p in permutations(range(n)):
            if all(all(p[c] != rows[r][c] for c in range(n))
                   for r in range(len(rows))):
                rows.append(list(p))
                rec()
                rows.pop()

    rec()
    return out


def reduced_latin(n):
    L = [[-1] * n for _ in range(n)]
    for c in range(n):
        L[0][c] = c
    for r in range(n):
        L[r][0] = r
    out = []
    cells = [(r, c) for r in range(1, n) for c in range(1, n)]

    def rec(t):
        if t == len(cells):
            out.append([row[:] for row in L])
            return
        r, c = cells[t]
        used = {L[r][j] for j in range(n) if L[r][j] >= 0}
        used |= {L[i][c] for i in range(n) if L[i][c] >= 0}
        for s in range(n):
            if s in used:
                continue
            L[r][c] = s
            rec(t + 1)
            L[r][c] = -1

    rec(0)
    return out


def three_signs(L, n):
    rho = 1
    for r in range(n):
        rho *= sgn(L[r])
    gam = 1
    for c in range(n):
        gam *= sgn([L[r][c] for r in range(n)])
    sig = 1
    for s in range(n):
        sig *= sgn([L[r].index(s) for r in range(n)])
    return rho, gam, sig


# --------------------------------------------------------------------------

def section1():
    print("=" * 74)
    print("1.  The flag construction IS a Latin square of order k -- CONFIRMED")
    print("=" * 74)
    print("    For a flag (i,u): rows (A\\{i}) u {m,l}, columns (V\\{u}) u {*},")
    print("    symbols C\\{L_i(u)}.  With |A| = k-1, |V| = k, |C| = k+1 the three")
    k = 16
    assert (k - 1 - 1) + 2 == k and (k - 1) + 1 == k and (k + 1) - 1 == k
    print(f"    sizes are {(k-1-1)+2}, {(k-1)+1}, {(k+1)-1} = k = {k}. ok")
    print()
    print("    Row m = {M_i(uv) : v != u} u {u}.  Condition 2 gives the colours")
    print("      on the edges at u as C\\{u, L_i(u)}; adding u yields C\\{L_i(u)}.")
    print("    Row l = {L_i(v) : v != u} u {inf}.  L_i is a derangement of V, so")
    print("      the values are V\\{L_i(u)}; adding inf yields C\\{L_i(u)}.")
    print("    Row j = {N_uv(ij) : v != u} u {L_j(u)}.  THIS is where the forced")
    print("      radius-5 trace enters: D_inf is a perfect matching of V, and")
    print("      D_x is a perfect matching of V\\{L_i^-1(x), L_j^-1(x)}.  Hence")
    print("      deg_{D_x}(u) = 1 except for x in {L_i(u), L_j(u)} where it is 0,")
    print("      so the row omits exactly those two and covers inf once:")
    print("      the values are C\\{L_i(u), L_j(u)}; adding L_j(u) gives")
    print("      C\\{L_i(u)}.")
    print("    Column v = {N_uv(ij) : j != i} u {M_i(uv)} u {L_i(v)}.  Condition")
    print("      4 gives the colours at i as C\\{M_i(uv), L_i(u), L_i(v)};")
    print("      adding the last two yields C\\{L_i(u)}.")
    print("    Column * = {L_j(u) : j != i} u {u} u {inf}.  Condition 1 makes")
    print("      j -> L_j(u) a bijection A -> V\\{u}, so off i the values are")
    print("      V\\{u, L_i(u)}; adding u and inf yields C\\{L_i(u)}.")
    print("    All four are rainbow onto the same 16-symbol set, so Q is a")
    print("    Latin square of order k. []")
    print()
    print("    CAVEAT ON TESTING.  No radius-5 object is known here at any k > 2:")
    print("    k=4 fails already at radius 3 and k=6 fails at radius 4 (see")
    print("    STATUS.md).  A k=16 radius-4 Wallis witness exists, but no")
    print("    radius-5 extension is known, so Q cannot yet be instantiated at")
    print("    k=16.  The one non-vacuous instantiation is k=2, done concretely.")
    # k = 2 instantiation: A = {a}, V = {u1,u2}, C = {u1,u2,inf}
    u1, u2, INF = 0, 1, 2
    L_a = {u1: u2, u2: u1}                    # derangement of V
    M_a = {(u1, u2): INF}                     # forced by condition 2
    assert set(M_a.values()) == {INF}
    sym = sorted({u1, u2, INF} - {L_a[u1]})   # C \ {L_i(u)} with u = u1
    Q = {("m", u2): M_a[(u1, u2)], ("m", "*"): u1,
         ("l", u2): L_a[u2], ("l", "*"): INF}
    for r in ("m", "l"):
        assert sorted(Q[(r, c)] for c in (u2, "*")) == sym
    for c in (u2, "*"):
        assert sorted(Q[(r, c)] for r in ("m", "l")) == sym
    print(f"    k=2 instantiation: symbols {sym}; all rows and columns rainbow: ok")


def section2():
    print()
    print("=" * 74)
    print("2.  The parity identity -- CONFIRMED")
    print("=" * 74)
    for n in (3, 4, 5):
        Ls = all_latin(n)
        vals = set()
        for L in Ls:
            rho, gam, sig = three_signs(L, n)
            vals.add(rho * gam * sig)
        pred = (-1) ** (n * (n - 1) // 2)
        print(f"    n={n}: {len(Ls):6d} Latin squares, rho*gamma*sigma in {vals},"
              f"  (-1)^(n(n-1)/2) = {pred}")
        assert vals == {pred}
    print(f"    At k = 16: (-1)^(16*15/2) = (-1)^120 = {(-1)**120}.")


def section3():
    print()
    print("=" * 74)
    print("3.  WHY THIS ROUTE COLLAPSES")
    print("=" * 74)
    print("    (a) At odd order, rho, gamma and sigma individually depend on")
    print("        reference orders.  At EVEN order each is reference-independent:")
    print("        a reference change multiplies every one of n constituent")
    print("        permutation signs, hence contributes sgn(alpha)^n = +1.")
    print("        In particular all three are intrinsic for the k=16 flags.")
    print("    (b) Nevertheless rho*gamma*sigma is CONSTANT over all Latin")
    print("        squares of a given")
    print("        order (section 2).  So every flag array of every candidate")
    print("        radius-5 ball has the same value, and so does every Latin")
    print("        square unrelated to the problem.")
    print("    (c) Therefore multiplying over the 15*16 = 240 flags gives")
    print(f"        ((-1)^120)^240 = 1 on the left and 1 on the right.  The")
    print("        identity is satisfied identically and constrains NOTHING")
    print("        about L, M, N.  No contradiction can arise from it.")
    print()
    print("    This is a proof that the proposed route is vacuous, not a")
    print("    failure to compute: the quantity carries no design information.")


def section4():
    print()
    print("=" * 74)
    print("4.  The refinement that DOES have content: Alon-Tarsi at even order")
    print("=" * 74)
    print("    For n EVEN, rho and gamma are each reference-independent (and so")
    print("    is their product): every reference change is repeated n times.")
    print("    Since k = 16 is even, AT(Q) = rho*gamma is a genuine per-flag")
    print("    invariant of the design data.  Unlike rho*gamma*sigma it is NOT")
    print("    constant:")
    for n in (4, 6):
        Ls = reduced_latin(n)
        d = {}
        for L in Ls:
            rho, gam, _ = three_signs(L, n)
            d[rho * gam] = d.get(rho * gam, 0) + 1
        print(f"      n={n}: {len(Ls):5d} reduced Latin squares, AT -> "
              f"{dict(sorted(d.items()))}")
    print("    (AT is relabelling-invariant at even n, so reduced squares")
    print("     already exhibit every attained value.)")
    print("    n = 4 being uniformly +1 is a small-order accident; from n = 6")
    print("    on both signs occur.  So the correct target is the product of")
    print("    AT(Q^{(i,u)}) over the 240 flags, NOT rho*gamma*sigma.")
    print()
    print("    FOLLOW-UP.  verify_formula_F.py now evaluates this global product")
    print("    symbolically from L,M data.  The result is a structural identity,")
    print("    not a contradiction; an independent value from the forced")
    print("    partial symbol fibers remains open.")


def main():
    section1()
    section2()
    section3()
    section4()
    print()
    print("=" * 74)
    print("SCOPE.  The construction is correct; the proposed parity identity is")
    print("correct but vacuous.  No sign contradiction was obtained, and no")
    print("construction.  Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()
