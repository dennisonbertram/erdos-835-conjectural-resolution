#!/usr/bin/env python3
"""The full shared-N sign: layer regrouping, two-sided synthetic models, and
the root-colour coupling test.

Stdlib only, no solver.  Labels: PROVED / COMPUTATION / OPEN.

H_observed(L,M,N)  the actual partial-fiber sign product.  Exists ONLY on a
                   genuine radius-5 structure.
H_required(L,M)    the value (H) forces IF the chart extends.  Computable from
                   radius-3 data; defined even for charts that never extend.
These are never used interchangeably below.

Run:  python3 -B collaboration/opus5/full_n_sign/verify_full_n_sign.py
"""
from __future__ import annotations

import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "radius5_followup"))

from verify_radius3_census_and_k6_obstruction import (  # noqa: E402
    all_sils, discordant_families, wallis_sils)
from verify_formula_F import analyse  # noqa: E402


def sgn_map(dom, tgt, f):
    ti = {x: t for t, x in enumerate(tgt)}
    s = [ti[f[d]] for d in dom]
    r, seen = 1, [False] * len(s)
    for a in range(len(s)):
        if seen[a]:
            continue
        L, b = 0, a
        while not seen[b]:
            seen[b] = True
            L += 1
            b = s[b]
        if L % 2 == 0:
            r = -r
    return r


def onefac(k):
    """The standard 1-factorization of K_k (k even), classes 0..k-2."""
    cls = {}
    for c in range(k - 1):
        M = [frozenset((c, k - 1))]
        for t in range(1, k // 2):
            M.append(frozenset(((c + t) % (k - 1), (c - t) % (k - 1))))
        cls[c] = M
    return cls


def section1():
    print("=" * 74)
    print("1.  PROVED -- the layer regrouping")
    print("=" * 74)
    print("    H_observed = prod_x H_x with H_x = prod_{i,u} sgn Phi_{i,u,x}.")
    print("    Phi_{i,u,x} sends j to the column v with N_uv(ij) = x, i.e.")
    print("      Phi_{i,u,x}(j) = the D_x^{ij}-partner of u,")
    print("    where D_x^{ij} = {uv : N_uv(ij) = x} is the forced trace")
    print("    matching.  That is the per-ij reading.  Dually, the set")
    print("    {ij : N_uv(ij) = x} is the x-class of the edge colouring N_uv of")
    print("    K_A, a matching with the holes prescribed by condition 4.  So one")
    print("    colour layer is a set of incidences (ij, uv) in E(K_A) x E(K_V)")
    print("    that is a matching with prescribed holes in EACH direction.")


def section2():
    print()
    print("=" * 74)
    print("2.  PROVED -- the infinity layer is a self-contained two-sided object")
    print("=" * 74)
    print("    For x = infinity the holes vanish on one side and are a single")
    print("    point on the other:")
    print("      * D_inf^{ij} is a PERFECT matching of V (radius5_minimal_trace);")
    print("      * by condition 3, {M_i(uv) : i in A} = C\\{u,v}, so exactly one")
    print("        index Psi(uv) has M_i(uv) = infinity, and the infinity-class")
    print("        of N_uv is a perfect matching of A \\ {Psi(uv)}.")
    print("    For fixed i, {uv : M_i(uv) = infinity} is the infinity-class of")
    print("    M_i, a perfect matching of V.  So Psi is a ONE-FACTORIZATION of")
    print("    K_V indexed by A.  Counting checks:")
    k = 16
    assert (k - 1) * (k - 2) // 2 * (k // 2) == k * (k - 1) // 2 * ((k - 2) // 2)
    print("      sum_ij |D| = C(k-1,2)*k/2 = sum_uv (k-2)/2 = C(k,2)*(k-2)/2 ok")
    print("    Phi_{i,u,inf} : A\\{i} -> V\\{u, w} with w the Psi_i-partner of u,")
    print("    is a bijection.  Well defined since D_inf^{ij} is perfect;")
    print("    never hits w because uw lies in the class of Psi(uw) = i, whose")
    print("    A-matching avoids i; injective because two j, j' with the same")
    print("    partner v would put the adjacent edges ij, ij' in the A-matching")
    print("    of uv. []")


def infinity_layer_models(k, limit=500):
    A, V = list(range(k - 1)), list(range(k))
    cls = onefac(k)
    Psi = {e: c for c, M in cls.items() for e in M}
    EA = [frozenset(e) for e in itertools.combinations(A, 2)]
    EV = [frozenset(e) for e in itertools.combinations(V, 2)]
    allpm = []

    def pms(free, acc):
        if not free:
            allpm.append(list(acc))
            return
        a = min(free)
        for b in sorted(free - {a}):
            acc.append(frozenset((a, b)))
            pms(free - {a, b}, acc)
            acc.pop()

    pms(frozenset(V), [])
    sols, D = [], {}

    def rec(t):
        if len(sols) >= limit:
            return
        if t == len(EA):
            for uv in EV:
                S = [e for e in EA if uv in D[e]]
                cov = [p for e in S for p in e]
                if sorted(cov) != sorted(p for p in A if p != Psi[uv]):
                    return
            sols.append(dict(D))
            return
        for Mm in allpm:
            D[EA[t]] = Mm
            ok = True
            for uv in EV:
                S = [e for e in EA[:t + 1] if uv in D[e]]
                cov = [p for e in S for p in e]
                if len(cov) != len(set(cov)) or Psi[uv] in cov:
                    ok = False
                    break
            if ok:
                rec(t + 1)
            del D[EA[t]]

    rec(0)
    return sols, Psi, A, V


def H_inf(D, Psi, A, V):
    H = 1
    for i in A:
        cls_i = [e for e in Psi if Psi[e] == i]
        for u in V:
            w = [b for b in V if frozenset((u, b)) in cls_i][0]
            dom = [j for j in A if j != i]
            tgt = [v for v in V if v not in (u, w)]
            f = {}
            for j in dom:
                Mm = D[frozenset((i, j))]
                f[j] = [b for b in V if frozenset((u, b)) in Mm and b != u][0]
            H *= sgn_map(dom, tgt, f)
    return H


def section3():
    print()
    print("=" * 74)
    print("3.  COMPUTATION -- smallest EXACT jointly compatible synthetic models")
    print("=" * 74)
    print("    SATISFIED by these models, exactly and completely:")
    print("      * Psi is a one-factorization of K_V indexed by A;")
    print("      * every D^{ij} is a perfect matching of V (the per-ij side);")
    print("      * every {ij : uv in D^{ij}} is a perfect matching of")
    print("        A \\ {Psi(uv)} (the per-uv side).")
    print("    OMITTED, and therefore NOT claimed:")
    print("      * conditions 1, 2, 4 for a full chart (no L; M enters only")
    print("        through its infinity-class Psi);")
    print("      * the other k colour layers;")
    print("      * any radius-4 or radius-5 object.  These are models of the")
    print("        infinity-layer two-sided constraints ALONE.")
    print("      * only the STANDARD Psi is used; other one-factorizations of")
    print("        K_V are untested.")
    print()
    out = {}
    for k in (4, 6):
        sols, Psi, A, V = infinity_layer_models(k)
        Hs = {}
        for D in sols:
            h = H_inf(D, Psi, A, V)
            Hs[h] = Hs.get(h, 0) + 1
        out[k] = (len(sols), Hs)
        print(f"    k={k}: exact two-sided infinity-layer models = {len(sols)};"
              f"  H_inf values -> {Hs}")
    assert out[4] == (1, {1: 1}) and out[6] == (7, {-1: 7})
    print()
    print("    READING.  At both parameters the two-sided layer structure does")
    print("    NOT leave both signs possible: every model gives the SAME H_inf.")
    print("    So this is the opposite of a countermodel -- it is evidence that")
    print("    a layer CAN be sign-forced.  The forced value is k-dependent")
    print("    (+1 at k=4, -1 at k=6), so it is not a universal constant.")
    print("    This is a COMPUTATION on one Psi at two parameters, not a")
    print("    theorem, and it covers one layer of k+1.")


def section4():
    print()
    print("=" * 74)
    print("4.  COMPUTATION -- root-colour coupling (task 4)")
    print("=" * 74)
    n = 7
    sq = all_sils(n)
    fams = discordant_families(sq, n, n - 2)
    pat = {}
    for fi in fams:
        F = [sq[j] for j in fi]
        vals = tuple(analyse(F, n, INF)["rhs"] for INF in range(n))
        key = (len(set(vals)), sum(1 for v in vals if v == -1))
        pat[key] = pat.get(key, 0) + 1
    print(f"    k=6, all {len(fams)} charts: (#distinct H_required over the 7")
    print(f"    root colours, #roots giving -1) -> {dict(sorted(pat.items()))}")
    assert pat == {(2, 4): 1680}
    W = wallis_sils()
    vals16 = {analyse(W, 17, INF)["rhs"] for INF in range(17)}
    print(f"    k=16 Wallis: H_required over all 17 root colours -> {vals16}")
    assert vals16 == {1}
    print()
    print("    So the root colour DOES move H_required at k=6 -- in every one")
    print("    of the 1680 charts, 4 of the 7 roots give -1 and 3 give +1 --")
    print("    while for Wallis at k=16 it is constant +1.")
    print()
    print("    NO CONTRADICTION FOLLOWS.  Different root colours give DIFFERENT")
    print("    charts (L,M), each with its own N and its own H_observed.  There")
    print("    is no compatibility requirement forcing one value across roots,")
    print("    so the k=6 variation is not a coupling obstruction.  The test is")
    print("    negative: root-colour choice does not couple the sign equations")
    print("    tightly enough to exclude anything.")



def AT_square(rows, V):
    R = 1
    for r in rows:
        R *= sgn_map(V, V, r)
    C = 1
    for u in V:
        C *= sgn_map(range(len(rows)), V, {t: rows[t][u] for t in range(len(rows))})
    return R * C


def L_completion(D, Psi, A, V, i):
    """Theta_i completed by row e = identity and row f = Psi_i."""
    Psi_i = {}
    for e in [x for x in Psi if Psi[x] == i]:
        a, b = tuple(e)
        Psi_i[a] = b
        Psi_i[b] = a
    rows = []
    for j in A:
        if j == i:
            continue
        al = {}
        for e in D[frozenset((i, j))]:
            a, b = tuple(e)
            al[a] = b
            al[b] = a
        rows.append(al)
    rows.append({u: u for u in V})
    rows.append(Psi_i)
    for u in V:                      # it really is a Latin square
        assert sorted(r[u] for r in rows) == sorted(V)
    return rows


def section5():
    print()
    print("=" * 74)
    print("5.  PROVED -- closed formula  H_inf = prod_i AT(L^(i))")
    print("=" * 74)
    print("    Theta_i (rows A\\{i}, columns V, entry P(i,j,u)) has every row a")
    print("    fixed-point-free involution and every column u equal to")
    print("    V\\{u, Psi_i(u)}, so adjoining e = identity and f = Psi_i")
    print("    completes it to a k x k LATIN SQUARE L^(i).")
    print("    Deleting f then e from column u gives")
    print("      sgn Phi_{i,u} = (-1)^(1+pos(u)+pos(Psi_i u)+[Psi_i u < u]) sgn(col u),")
    print("    and summing the exponent over u gives k(k-1) + k/2 = k/2 mod 2,")
    print("    so prod_u sgn Phi_{i,u} = (-1)^(k/2) C(L^(i)).  Every row but e is")
    print("    a fixed-point-free involution, so R(L^(i)) = (-1)^((k/2)(k-1)).")
    print("    Multiplying over i the constant is (-1)^(k^2(k-1)/2), and")
    print("    k^2(k-1)/2 = (k/2)k(k-1) is even.  Hence H_inf = prod_i AT. []")
    print("    k even => each AT is reference-independent, so H_inf is INTRINSIC.")
    for k in (4, 6):
        sols, Psi, A, V = infinity_layer_models(k)
        ok = True
        vals = set()
        for D in sols:
            p = 1
            for i in A:
                p *= AT_square(L_completion(D, Psi, A, V, i), V)
            ok &= (p == H_inf(D, Psi, A, V))
            vals.add(p)
        print(f"    k={k}: {len(sols)} models; formula matches direct definition:"
              f" {ok}; H_inf values {vals}")
        assert ok
    print()
    print("    SUPERSEDED (see section 6): the (-1)^(k/2) reading below is FALSE.")
    print("    on k.  Fits k = 4 (+1), 6 (-1), 8 (+1).  At k = 16 it would be +1.")
    print()
    print("    RECORDED ERROR.  The intended k=8 test of BOTH parity classes of")
    print("    one-factorizations of K_8 was not achieved: the classifier used")
    print("    was the product of factor signs, but every factor of K_8 is 4")
    print("    transpositions, hence even, so that product is identically +1 and")
    print("    separates nothing.  Both parity classes at k=8 remain UNTESTED.")



def sts_projective():
    return {frozenset((a, b)): a ^ b
            for a in range(1, 16) for b in range(1, 16) if a < b}


def sts_bose():
    def q(x, y):
        return (3 * (x + y)) % 5
    pts = [(x, i) for x in range(5) for i in range(3)]
    idx = {p: t for t, p in enumerate(pts)}
    tri = [{(x, 0), (x, 1), (x, 2)} for x in range(5)]
    for i in range(3):
        for x in range(5):
            for y in range(x + 1, 5):
                tri.append({(x, i), (y, i), (q(x, y), (i + 1) % 3)})
    m = {}
    for T in tri:
        T = list(T)
        for a, b in itertools.combinations(T, 2):
            c = [z for z in T if z not in (a, b)][0]
            m[frozenset((idx[a] + 1, idx[b] + 1))] = idx[c] + 1
    return m


def H_from_sts(Psi_cls, m, k):
    """D^{ij} = Psi_{m(ij)}; two-sided by the STS link property."""
    V, A = list(range(k)), list(range(1, k))
    Psi = {e: c for c, M in Psi_cls.items() for e in M}
    inv = {}
    for c, M in Psi_cls.items():
        d = {}
        for e in M:
            a, b = tuple(e)
            d[a] = b
            d[b] = a
        inv[c] = d
    for uv in [frozenset(e) for e in itertools.combinations(V, 2)]:
        cov = [p for e in m if m[e] == Psi[uv] for p in e]
        assert sorted(cov) == sorted(x for x in A if x != Psi[uv])
    P = 1
    for i in A:
        rows = [inv[m[frozenset((i, j))]] for j in A if j != i]
        rows.append({u: u for u in V})
        rows.append(inv[i])
        for u in V:
            assert sorted(r[u] for r in rows) == sorted(V)
        P *= AT_square(rows, V)
    return P


def section6():
    print()
    print("=" * 74)
    print("6.  RETRACTION -- H_inf = (-1)^(k/2) is FALSE")
    print("=" * 74)
    print("    Any Steiner triple system m on A gives a two-sided family via")
    print("    D^{ij} = Psi_{m(ij)}: the set {ij : uv in D^{ij}} is the LINK of")
    print("    Psi(uv) in m, and a link of an STS point is a perfect matching of")
    print("    the remaining points.  Checked below for both STS(15).")
    xor = {c: [frozenset((u, u ^ c)) for u in range(16) if u < (u ^ c)]
           for c in range(1, 16)}
    rr0 = onefac(16)
    rr = {c + 1: rr0[c] for c in range(15)}
    out = {}
    for pn, pc in (("XOR", xor), ("round-robin", rr)):
        for sn, mm in (("projective", sts_projective()), ("Bose", sts_bose())):
            h = H_from_sts(pc, mm, 16)
            out[(pn, sn)] = h
            print(f"    Psi={pn:12s} STS={sn:11s} -> H_inf = {h:+d}")
    assert out[("XOR", "projective")] == out[("XOR", "Bose")] == 1
    assert out[("round-robin", "projective")] == out[("round-robin", "Bose")] == -1
    print("    (-1)^(16/2) = +1, so the round-robin rows REFUTE the conjecture.")
    print("    H_inf is constant in D (both STS agree per Psi) and varies with")
    print("    Psi.  This Opus pass left rho unidentified; the subsequent")
    print("    independent global-H proof establishes H_inf = rho(Psi) = P(Psi).")
    print("    The proved formula H_inf = prod_i AT(L^(i)) is unaffected.")
    print("    NOTE: K_4 and K_6 have a UNIQUE one-factorization up to")
    print("    isomorphism, so those parameters could never have exhibited")
    print("    Psi-dependence -- the earlier two-point fit was structurally")
    print("    incapable of refutation.  The k=8 evidence is withdrawn.")


def main():
    section1()
    section2()
    section3()
    section4()
    section5()
    section6()
    print()
    print("=" * 74)
    print("SUBSEQUENT STATUS.  collaboration/global_h_parity proves every")
    print("finite layer formula and shows that their total is identically the")
    print("existing flag formula F(L,M).  Thus this sign route supplies no new")
    print("single-root obstruction.  No k=16 chart is excluded here.")
    print("Erdos-Rosenfeld #835 remains OPEN -- no unrestricted theorem, no")
    print("construction.")


if __name__ == "__main__":
    main()
