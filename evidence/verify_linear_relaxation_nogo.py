#!/usr/bin/env python3
"""Validator: rigorous no-go for the F2-linear-relaxation route to the
E3/X3 evenness statements (artifact section 2.10).

Setting: encode a tiling as x[z][P] = [w(P) = z] (z not in P).  ALL
constraints proved so far are linear-affine over F2:
  per-P parity, per-(r+2)-set tiling parity, per-point uniformity
  parity.  E3 and X3 are bilinear forms T_E, T_X in (x, y).

Checked facts (deterministic):
  r=3: kernel dim 7; T_E violates on the LINEAR terms (5/7 kernel
       generators k have T_E(k, g0) = 1); T_X is vacuous (no block
       pairs at distance 0); the full affine space has 128 elements of
       which exactly 8 are 0/1-fibre-legal, and those 8 are exactly
       the true tilings (0 pseudo-tilings); census of (legal, T_E)
       = {(True,0): 8, (False,1): 64, (False,0): 56}.
  r=5: kernel dim 132; linear terms clean for both forms, but the
       FULL kernel-pair check has 1583/8778 violations for T_E and
       1583/8778 for T_X.  The violation sets coincide exactly, so
       T_E + T_X has 0/8778 violations.

Conclusions (PROVED by these witnesses):
  - T_E is not constant on the r=3 F2-affine hull; neither T_E nor T_X
    is constant on the r=5 hull.  Thus no parameter-uniform proof can
    merely assert separate constancy on these affine relaxations.
  - The combined form behaves differently: it fails at r=3 but is
    constant on the full r=5 affine hull.  For true tilings this is
    the r=1 (mod 4) coefficient cancellation; it supplies no lift to
    r=15, where the combined parity is identically t.
  - At r=3, per-fibre exactly-one is sufficient to remove every
    countermodel.  At r=5 this checker does not isolate which of the
    omitted exact-cardinality constraints is decisive.
  - No inference about the enormous r=15 affine hull is made.  A
    parameter-specific identity there remains logically possible, but
    the r=5 cancellation is not evidence for one.
Run: python3 verify_linear_relaxation_nogo.py
"""
import sys
from itertools import combinations
from collections import Counter

sys.setrecursionlimit(100000)
HERE = __file__.rsplit("/", 1)[0] or "."
src = open(f"{HERE}/verify_H_identity.py").read().split("if __name__")[0]
ns = {}
exec(compile(src, "verify_H_identity.py", "exec"), ns)


def setup(v, r):
    blocks = list(combinations(range(v), r))
    X0, Y0 = ns["cover_instance"](v, r - 1, blocks)
    A = ns["algox"](X0, Y0, cap=1)[0]
    b = len(A)
    rest = [x for x in blocks if x not in set(A)]
    X1, Y1 = ns["cover_instance"](v, r - 1, rest)
    mates = ns["algox"](X1, Y1, cap=None)
    ws = [ns["wmap"](A, M, v) for M in mates]
    Asets = {P: set(P) for P in A}
    varidx = {}
    for P in A:
        for z in range(v):
            if z not in Asets[P]:
                varidx[(z, P)] = len(varidx)
    rows, rhs = [], []
    for P in A:
        m2 = 0
        for z in range(v):
            if z not in Asets[P]:
                m2 |= 1 << varidx[(z, P)]
        rows.append(m2)
        rhs.append(1)
    for Z in combinations(range(v), r + 2):
        Zs = set(Z)
        m2 = 0
        for P in A:
            if Asets[P] <= Zs:
                for z in Zs - Asets[P]:
                    m2 |= 1 << varidx[(z, P)]
        rows.append(m2)
        rhs.append(1)
    for z in range(v):
        m2 = 0
        for P in A:
            if z not in Asets[P]:
                m2 |= 1 << varidx[(z, P)]
        rows.append(m2)
        rhs.append((b // v) % 2)
    piv = {}
    for m2 in rows:
        cur = m2
        while cur:
            j = (cur & -cur).bit_length() - 1
            if j in piv:
                cur ^= piv[j]
            else:
                piv[j] = cur
                break
    for j in sorted(piv, reverse=True):
        for j2 in piv:
            if j2 != j and (piv[j2] >> j) & 1:
                piv[j2] ^= piv[j]
    K = []
    for fc in range(len(varidx)):
        if fc in piv:
            continue
        vec = 1 << fc
        for j, prow in piv.items():
            if (prow >> fc) & 1:
                vec |= 1 << j
        K.append(vec)
    return A, ws, Asets, varidx, K, rows, rhs


def forms(v, r, A, Asets, varidx):
    p2 = [(P, Q) for P in A for Q in A
          if P != Q and len(Asets[P] & Asets[Q]) == r - 2]
    p3 = [(P, Q) for P in A for Q in A
          if P != Q and len(Asets[P] & Asets[Q]) == r - 3]

    def TE(xv, yv):
        s = 0
        for P, Q in p2:
            for z in range(v):
                if z not in Asets[P] and z not in Asets[Q]:
                    if (xv >> varidx[(z, P)]) & 1 and \
                       (yv >> varidx[(z, Q)]) & 1:
                        s ^= 1
        return s

    def TX(xv, yv):
        s = 0
        for P, Q in p3:
            a1 = 0
            for z in Asets[Q] - Asets[P]:
                if (xv >> varidx[(z, P)]) & 1:
                    a1 ^= 1
            if a1:
                a2 = 0
                for z2 in Asets[P] - Asets[Q]:
                    if (yv >> varidx[(z2, Q)]) & 1:
                        a2 ^= 1
                s ^= a2
        return s

    return TE, TX


def encode(w, A, varidx):
    m2 = 0
    for P in A:
        m2 |= 1 << varidx[(w[P], P)]
    return m2


def satisfies_affine(vector, rows, rhs):
    return all(((row & vector).bit_count() & 1) == value
               for row, value in zip(rows, rhs))


def main():
    # r=3
    A, ws, Asets, varidx, K, rows, rhs = setup(7, 3)
    TE, TX = forms(7, 3, A, Asets, varidx)
    f0 = encode(ws[0], A, varidx)
    g0 = encode(ws[1], A, varidx)
    assert len(K) == 7
    assert satisfies_affine(f0, rows, rhs)
    assert satisfies_affine(g0, rows, rhs)
    assert TE(f0, g0) == 0 and TX(f0, g0) == 0
    lin_viol = sum(1 for k in K if TE(k, g0))
    assert lin_viol == 5, lin_viol
    assert all(TX(k, g0) == 0 for k in K)
    census = Counter()
    legal_tilings = pseudo = 0
    for msk in range(1 << 7):
        x = f0
        mm, i = msk, 0
        while mm:
            if mm & 1:
                x ^= K[i]
            mm >>= 1
            i += 1
        wx, legal = {}, True
        for P in A:
            zs = [z for z in range(7) if z not in Asets[P]
                  and (x >> varidx[(z, P)]) & 1]
            if len(zs) != 1:
                legal = False
                break
            wx[P] = zs[0]
        census[(legal, TE(x, g0))] += 1
        if legal:
            tiling = all(
                sum(1 for P in A if Asets[P] <= set(Z) and wx[P] in Z) == 1
                for Z in combinations(range(7), 5))
            if tiling:
                legal_tilings += 1
            else:
                pseudo += 1
    assert census == Counter({(False, 1): 64, (False, 0): 56,
                              (True, 0): 8}), census
    assert legal_tilings == 8 and pseudo == 0
    print("[r=3] no-go verified: 5/7 linear violations for T_E; affine "
          "census {(True,0):8,(False,1):64,(False,0):56}; the 8 legal "
          "solutions are exactly the true tilings")

    # r=5
    A, ws, Asets, varidx, K, rows, rhs = setup(11, 5)
    TE, TX = forms(11, 5, A, Asets, varidx)
    f0 = encode(ws[0], A, varidx)
    g0 = encode(ws[1], A, varidx)
    assert len(K) == 132
    assert satisfies_affine(f0, rows, rhs)
    assert satisfies_affine(g0, rows, rhs)
    assert TE(f0, g0) == 0 and TX(f0, g0) == 0
    assert all(TE(k, g0) == 0 and TE(f0, k) == 0 for k in K)
    assert all(TX(k, g0) == 0 and TX(f0, k) == 0 for k in K)
    vE = vX = vCombined = 0
    first_E = first_X = first_combined = None
    for a in range(len(K)):
        for b2 in range(a, len(K)):
            e_value = TE(K[a], K[b2])
            x_value = TX(K[a], K[b2])
            if e_value:
                vE += 1
                if first_E is None:
                    first_E = (a, b2)
            if x_value:
                vX += 1
                if first_X is None:
                    first_X = (a, b2)
            if e_value ^ x_value:
                vCombined += 1
                if first_combined is None:
                    first_combined = (a, b2)
    assert (vE, vX, vCombined) == (1583, 1583, 0), (
        vE, vX, vCombined
    )
    print("[r=5] no-go verified: linear terms clean; kernel-pair "
          "violations 1583/8778 for T_E and for T_X; "
          f"first witnesses T_E={first_E}, T_X={first_X}; "
          f"combined violations={vCombined}, first={first_combined}")


if __name__ == "__main__":
    main()
