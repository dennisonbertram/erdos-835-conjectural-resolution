#!/usr/bin/env python3
"""Audit of the flag Alon-Tarsi programme.

Stdlib only, no solver.  Labels: PROVED / COMPUTATION / CONJECTURE / OPEN.

  1  PROVED + COMPUTATION -- the R_tau cancellation lemma (audited, corrected
     scope), verified on real radius-3 data at k = 6 and k = 16.
  2  PROVED + COMPUTATION -- the flag incidence multiplicities that govern any
     pairing argument.  The N-multiplicity is 4, not 2.
  3  FOLLOW-UP -- the product was subsequently evaluated by formula (F);
     the independent partial-symbol-fiber value remains open.

Run:  python3 -B collaboration/opus5/radius5_followup/verify_flag_at_product.py
"""
from __future__ import annotations

import os
import random
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from verify_radius3_census_and_k6_obstruction import (  # noqa: E402
    all_sils, discordant_families, wallis_sils, check_sils)


def ent(S, a, b):
    return S[(min(a, b), max(a, b))] if a != b else a


def eps(tau, a, b):
    """-1 exactly when tau reverses the relative order of a and b."""
    return 1 if (tau[a] - tau[b]) * (a - b) > 0 else -1


def R_tau(F, n, INF, i, u, tau):
    V = [c for c in range(n) if c != INF]
    S = F[i]
    L = {v: ent(S, INF, v) for v in V}
    Linv = {c: v for v, c in L.items()}
    r = 1
    for x in V:
        if x == u or x == L[u]:
            continue
        mate = [v for v in V if v != u and ent(S, u, v) == x]
        assert len(mate) == 1
        r *= eps(tau, Linv[x], mate[0])
    return r


def total_R(F, n, INF, tau):
    V = [c for c in range(n) if c != INF]
    p = 1
    for i in range(len(F)):
        for u in V:
            p *= R_tau(F, n, INF, i, u, tau)
    return p


# --------------------------------------------------------------------------

def section1():
    print("=" * 74)
    print("1.  The R_tau cancellation lemma -- AUDITED, CORRECT (PROVED)")
    print("=" * 74)
    print("    Setting.  For finite x in V the x-class of M_i is a perfect")
    print("    matching on V \\ {x, L_i^-1(x)} (radius4_reduction.md, cond. 2).")
    print("    So p_{i,x}(u), the mate of u in that class, is defined exactly")
    print("    when u is not x and not L_i^-1(x), i.e. exactly when x is not u")
    print("    and not L_i(u).  The product range in R_tau is therefore")
    print("    precisely the set of x for which the term exists: 14 of the 16")
    print("    values of V.  ok")
    print()
    print("    Step 1.  Put v = L_i^-1(x).  As x runs over V \\ {u, L_i(u)},")
    print("    v runs over V \\ {u, L_i^-1(u)}.  Hence")
    print("      R_tau(i,u) = prod_{v != u, L_i^-1(u)} eps_tau({v, m_v(u)}),")
    print("    where m_v = p_{i, L_i(v)} is the matching on V \\ {v, L_i(v)}.")
    print()
    print("    Step 2.  Fix v and vary u.  The term exists iff u is not v and")
    print("    not L_i(v) -- exactly the 14 points carrying the matching m_v.")
    print("    m_v is an involution of that set, hence a bijection of it, so as")
    print("    u runs over those 14 points m_v(u) does too, each exactly once:")
    print("      prod_u eps_tau({v, m_v(u)}) = prod_{z != v, L_i(v)} eps_tau({v,z}).")
    print("    This is the 'each endpoint occurs exactly once' step, and it is")
    print("    correct because m_v is a PERFECT matching on that 14-set.")
    print()
    print("    Step 3.  Over all ordered (v,z) with z != v every unordered pair")
    print("    occurs twice, so prod_v prod_{z != v} eps_tau = 1.  Removing the")
    print("    pair {v, L_i(v)} divides by eps_tau({v,L_i(v)}), and for signs")
    print("    division equals multiplication:")
    print("      prod_u R_tau(i,u) = prod_v eps_tau({v, L_i(v)}).")
    print()
    print("    Step 4.  Condition 1 says {L_i(v) : i in A} = V \\ {v} for each")
    print("    fixed v, a bijection A -> V\\{v}.  Hence")
    print("      prod_{i,u} R_tau = prod_v prod_{z != v} eps_tau({v,z}) = 1. []")
    print()
    print("    SCOPE CORRECTION.  The lemma covers only the GENERIC symbol")
    print("    fibers x in V \\ {u, L_i(u)} -- 14 of the 16 symbols of")
    print("    C \\ {L_i(u)}.  The two non-generic fibers, the symbol u and the")
    print("    symbol infinity, are NOT covered.  So the lemma establishes that")
    print("    the generic part of the flag symbol-sign product is globally")
    print("    reference-independent.  It does NOT determine its value, and it")
    print("    does not by itself handle the whole symbol-sign product.")

    print()
    print("    COMPUTATION -- verified on real radius-3 (L, M) data.  R_tau uses")
    print("    only L and M, never N, so it is testable even though no radius-4")
    print("    object exists at k = 6.")
    rnd = random.Random(835)
    n = 7
    sq = all_sils(n)
    fams = discordant_families(sq, n, n - 2)
    bad = tested = 0
    for t, fi in enumerate(fams):
        F = [sq[j] for j in fi]
        for INF in ([0] if t % 8 else range(n)):
            V = [c for c in range(n) if c != INF]
            tau = {v: r for v, r in zip(V, rnd.sample(range(len(V)), len(V)))}
            if total_R(F, n, INF, tau) != 1:
                bad += 1
            tested += 1
    print(f"      k=6  (all {len(fams)} radius-3 families): {tested} cases,"
          f" violations {bad}")
    assert bad == 0
    W = wallis_sils()
    for S in W:
        check_sils(S, 17)
    bad = 0
    for _ in range(40):
        INF = rnd.randrange(17)
        V = [c for c in range(17) if c != INF]
        tau = {v: r for v, r in zip(V, rnd.sample(range(len(V)), len(V)))}
        if total_R(W, 17, INF, tau) != 1:
            bad += 1
    print(f"      k=16 (Wallis): 40 random (infinity, tau) cases,"
          f" violations {bad}")
    assert bad == 0


def section2():
    print()
    print("=" * 74)
    print("2.  Flag incidence multiplicities (PROVED + COMPUTATION)")
    print("=" * 74)
    k = 16
    A, V = k - 1, k
    flags = A * V
    print(f"    flags (i,u): |A| x |V| = {A} x {V} = {flags}")
    print(f"    each Q has {A-1} existing rows, 2 dummy rows, {V-1} existing")
    print(f"    columns, 1 dummy column; order {A-1+2} = {V-1+1} = {k}. ok")
    assert A - 1 + 2 == k == V - 1 + 1
    ncells = flags * (A - 1) * (V - 1)
    nentries = (A * (A - 1) // 2) * (V * (V - 1) // 2)
    print(f"    N-carrying cells over all flags: {flags} x {A-1} x {V-1}"
          f" = {ncells:,}")
    print(f"    distinct N entries: C({A},2) x C({V},2) = {nentries:,}")
    print(f"    multiplicity = {ncells // nentries}")
    assert ncells == nentries * 4
    print("    PROVED.  The entry N_uv(ij) occupies cell (row j, col v) of")
    print("    Q^{i,u}; the four cells are obtained by choosing which of i,j is")
    print("    the flag index and which of u,v is the flag column.  So EVERY N")
    print("    entry appears in exactly FOUR flag arrays, not two.")
    print("    Any pairing argument that treats row j of Q^{i,u} with row i of")
    print("    Q^{j,u} handles only one of the two available pairings; the")
    print("    column pairing (col v of Q^{i,u} with col u of Q^{i,v}) is the")
    print("    other.  Together they cover each N entry 4 times, i.e. twice in")
    print("    row products and twice in column products.")
    print()
    print("    The two paired lines agree on all their N cells and differ only")
    print("    in the single dummy entry and in WHICH symbol is deleted:")
    print("      row j of Q^{i,u}: v -> N_uv(ij), * -> L_j(u), symbols C\\{L_i(u)}")
    print("      row i of Q^{j,u}: v -> N_uv(ij), * -> L_i(u), symbols C\\{L_j(u)}")
    print("    so their signs differ by a cofactor depending only on L, not N.")
    print("    That is the structural reason an N-free formula is plausible.")


def section3():
    print()
    print("=" * 74)
    print("3.  Follow-up: formula (F) is now proved; partial fibers remain OPEN")
    print("=" * 74)
    print("    The later symbolic cofactor audit proves")
    print("      prod_{i,u} AT(Q^{i,u})")
    print("        = (-1)^(k(k-1)/2) AT(T) prod_i delta(S_i).")
    print("    See verify_formula_F.py and")
    print("    evidence/odd_graph_local_ball/flag_at_exact_formula.md.")
    print("    The k=2 structure checks the genuine equality; all k=6")
    print("    radius-3 families and the Wallis k=16 chart check every L,M-only")
    print("    factor.  Those latter controls are not radius-5 witnesses.")
    print()
    print("    OPEN.  No independent value for the N-dependent partial-symbol")
    print("    fiber product is known.  Such a value could still conflict with")
    print("    formula (F); no conflict has been derived.")
    print()
    print("    WHAT WOULD NOT COUNT.  A universal Latin-square identity is not")
    print("    an obstruction (that is how rho*gamma*sigma failed).  A")
    print("    fixed-Wallis computation is not an unrestricted theorem.  Any")
    print("    claimed contradiction must be shown NOT to hold for every Latin")
    print("    square of order 16 of the relevant shape.")


def main():
    section1()
    section2()
    section3()
    print()
    print("=" * 74)
    print("SCOPE.  The R_tau lemma and multiplicity count are proved; formula")
    print("(F) evaluates the AT product, but no partial-fiber value is known.")
    print("No sign contradiction and")
    print("no construction was obtained.  The unrestricted existential problem")
    print("is untouched: Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()
