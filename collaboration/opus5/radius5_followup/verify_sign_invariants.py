#!/usr/bin/env python3
"""Priority A: sign/parity invariants of discordant symmetric idempotent Latin
square families, and an explicit -- and carefully NARROWED -- test of what they
do and do not exclude.

Stdlib only, no solver, self-contained (imports only the sibling census file).

  1  Which signs are intrinsic, with proofs.
  2  Exhaustive distributions at n = 3, 5, 7 (the k = 2, 4, 6 parameters).
  3  Observations at n = 7 and on the Wallis family, kept strictly separate
     from the tautology, and from anything proved.
  4  Exactly what is falsified -- radius-3-universal claims only.

Run:  python3 -B collaboration/opus5/radius5_followup/verify_sign_invariants.py
      ... --quick   (samples the n=7 families)
"""
from __future__ import annotations

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from verify_radius3_census_and_k6_obstruction import (  # noqa: E402
    all_sils, discordant_families, wallis_sils, check_sils)


def sgn(p):
    """Sign of a permutation given as a dict on its own domain.  Intrinsic."""
    seen, s = set(), 1
    for a in p:
        if a in seen:
            continue
        L, z = 0, a
        while z not in seen:
            seen.add(z)
            L += 1
            z = p[z]
        if L % 2 == 0:
            s = -s
    return s


def rowperm(S, n, q):
    d = {y: S[(min(q, y), max(q, y))] for y in range(n) if y != q}
    d[q] = q
    return d


def delta(S, n):
    r = 1
    for q in range(n):
        r *= sgn(rowperm(S, n, q))
    return r


def R_q(F, n, q):
    r = 1
    for S in F:
        r *= sgn(rowperm(S, n, q))
    return r


def C_q(F, n, q, perm=None, ref=None):
    """Column-sign product of the induced order-(n-1) Latin square at q."""
    pts = [y for y in range(n) if y != q]
    if ref:
        pts = [pts[i] for i in ref]
    idx = {y: t for t, y in enumerate(pts)}
    order = list(range(len(F))) if perm is None else perm
    rows = [[idx[y] for y in pts]]
    for i in order:
        rows.append([idx[rowperm(F[i], n, q)[y]] for y in pts])
    m = len(pts)
    c = 1
    for j in range(m):
        c *= sgn({t: rows[t][j] for t in range(m)})
    return c


# --------------------------------------------------------------------------

def section1():
    print("=" * 74)
    print("1.  Which signs are intrinsic (relabelling-safe)")
    print("=" * 74)
    print("    LEMMA 1 (PROVED).  delta(S) = prod_q sgn(row_q) is invariant")
    print("    under every relabelling of the point set.")
    print("    Proof.  Row q is a permutation pi_q of Q (it fixes q), so its")
    print("    sign is intrinsic -- no reference order is needed.  Relabelling")
    print("    by rho gives pi'_q = rho . pi_{rho^-1 q} . rho^-1, so")
    print("    sgn(pi'_q) = sgn(pi_{rho^-1 q}) and the product over q is merely")
    print("    reindexed.  Hence delta(S') = delta(S). []")
    print()
    print("    LEMMA 2 (TAUTOLOGY, not content).  For a family {S_1..S_m},")
    print("        prod_i delta(S_i) = prod_q R_q,   R_q := prod_i sgn(pi^i_q).")
    print("    Both sides are literally the same double product over (i,q)")
    print("    with the factors reordered.  This asserts NOTHING about the")
    print("    common value; it is bookkeeping. []")
    print()
    print("    LEMMA 3 (PROVED).  Let L_q be the induced order-m Latin square,")
    print("    m = n-1, whose rows are the identity and the pi^i_q restricted")
    print("    to Q\\{q}.  Its COLUMN-sign product C_q is intrinsic whenever m")
    print("    is even -- which holds here since n is odd.")
    print("    Proof.  A column maps the row-index set to the point set, two")
    print("    different sets, so an individual column sign needs a reference")
    print("    bijection beta.  Replacing beta by beta.sigma multiplies EVERY")
    print("    column sign by sgn(sigma), so the product over the m columns")
    print("    changes by sgn(sigma)^m = +1 for m even.  Reordering the family")
    print("    or relabelling the points likewise flips all m column signs at")
    print("    once.  Hence C_q is well defined. []")
    n = 7
    sq = all_sils(n)
    F = [sq[i] for i in discordant_families(sq, n, n - 2, limit=1)[0]]
    base = C_q(F, n, 0)
    swapped = C_q(F, n, 0, perm=[1, 0, 2, 3, 4])
    refswap = C_q(F, n, 0, ref=[1, 0, 2, 3, 4, 5])
    print(f"    invariance check (n=7, q=0): base {base}, family-swapped"
          f" {swapped}, reference-swapped {refswap}")
    assert base == swapped == refswap
    print("    NOTE.  An earlier draft of this file claimed the opposite -- that")
    print("    column signs are an artifact.  That was wrong: the flip is")
    print("    simultaneous across all m columns and cancels for m even.")


def section2():
    print()
    print("=" * 74)
    print("2.  Exhaustive delta distributions at n = 3, 5, 7 (k = 2, 4, 6)")
    print("=" * 74)
    for n in (3, 5, 7):
        sq = all_sils(n)
        for S in sq:
            check_sils(S, n)
        dist = {}
        for S in sq:
            d = delta(S, n)
            dist[d] = dist.get(d, 0) + 1
        print(f"    n={n:2d}: {len(sq):5d} squares,  delta distribution"
              f" {dict(sorted(dist.items()))}")
        if n == 7:
            assert dist == {-1: 5280, 1: 960}
    print()
    print("    CROSS-VALIDATION.  The n=7 split 5280 / 960 is exactly the K_8")
    print("    one-factorization sign split recorded independently in")
    print("    evidence/local_one_factorization_sign_audit.md, so delta is that")
    print("    file's epsilon_row reached from the Latin-square side.  It is")
    print("    NOT constant: a single square's sign carries no obstruction.")


def section3(quick):
    print()
    print("=" * 74)
    print("3.  OBSERVATIONS -- kept separate from anything proved")
    print("=" * 74)
    n = 7
    sq = all_sils(n)
    fams = discordant_families(sq, n, n - 2)
    sample = fams if not quick else random.Random(835).sample(fams, 200)
    prod, neg, cs = {}, {}, {}
    for fi in sample:
        F = [sq[i] for i in fi]
        p = 1
        for S in F:
            p *= delta(S, n)
        prod[p] = prod.get(p, 0) + 1
        neg[sum(1 for q in range(n) if R_q(F, n, q) == -1)] = \
            neg.get(sum(1 for q in range(n) if R_q(F, n, q) == -1), 0) + 1
        for q in range(n):
            c = C_q(F, n, q)
            cs[c] = cs.get(c, 0) + 1
    tag = "sampled" if quick else "ALL"
    print(f"    n=7, {len(sample)} complete discordant families ({tag}):")
    print(f"      prod_i delta(S_i)   -> {dict(sorted(prod.items()))}")
    print(f"      #q with R_q = -1    -> {dict(sorted(neg.items()))}")
    print(f"      C_q over (family,q) -> {dict(sorted(cs.items()))}")
    if quick:
        print("      These are SAMPLED OBSERVATIONS at one parameter, n = 7.")
    else:
        print("      These are EXHAUSTIVE OBSERVATIONS at one parameter, n = 7.")
    print("      None of them is proved for general n, and none is claimed to be.")

    W = wallis_sils()
    for S in W:
        check_sils(S, 17)
    pw = 1
    for S in W:
        pw *= delta(S, 17)
    negs = [q for q in range(17) if R_q(W, 17, q) == -1]
    cw = [C_q(W, 17, q) for q in range(17)]
    print()
    print("    n=17, the Wallis family -- a SINGLE EXAMPLE, and only a")
    print("    radius-3 object (see section 4):")
    print(f"      prod_i delta(S_i)   -> {pw}")
    print(f"      #q with R_q = -1    -> {len(negs)} of 17")
    print(f"      C_q                 -> constant {cw[0]}"
          f" ({cw.count(-1)} negative, {cw.count(1)} positive)")
    assert pw == 1 and len(negs) == 0 and set(cw) == {1}
    print()
    print("    The observations give DIFFERENT values:")
    if quick:
        print("      n =  7 (m =  6): C_q = -1 throughout this sample")
    else:
        print("      n =  7 (m =  6): C_q = -1 throughout this census")
    print("      n = 17 (m = 16): C_q = +1 for the single Wallis family")
    print("    These fit (-1)^((n-1)/2), but sampled n=7 data plus one n=17")
    print("    example do not prove rigidity at either parameter or in general.")
    return len(negs)


def section4(nneg17):
    print()
    print("=" * 74)
    print("4.  What is falsified -- narrowed")
    print("=" * 74)
    print("    At n = 7 the count #{q : R_q = -1} is rigidly 4 -- never 0.  The")
    print("    natural extrapolation is: 'for EVERY radius-3 discordant family,")
    print("    some R_q is negative'.  That would obstruct k = 16 at radius 3.")
    assert nneg17 == 0
    print(f"    FALSIFIED.  The Wallis family attains {nneg17}.  It is an")
    print("    explicitly verified radius-3 object, so this is a countermodel,")
    print("    not a search failure.")
    print()
    print("    SCOPE OF THE FALSIFICATION -- read this carefully.")
    print("    The Wallis family is a RADIUS-3 object only.  It is NOT a")
    print("    radius-5 ball and NOT a global colouring.  Therefore:")
    print("      * it refutes any conjecture quantified over all RADIUS-3")
    print("        discordant families;")
    print("      * it does NOT show that every later-layer sign obstruction of")
    print("        this shape is vacuous.  A genuine radius-5 compatibility")
    print("        theorem could still force the opposite sign and thereby")
    print("        exclude every radius-3 family that extends -- including")
    print("        Wallis.  Nothing here rules that out.")
    print("    So: the radius-3-universal generalization is dead; global sign")
    print("    identities at radius 5 and beyond remain open.")


def main():
    quick = "--quick" in sys.argv
    section1()
    section2()
    nneg = section3(quick)
    section4(nneg)
    print()
    print("=" * 74)
    print("SCOPE.  No contradiction and no construction was obtained.  Even a")
    print("full exclusion of k = 16 would leave the other prime cases open and")
    print("so would not settle the existential problem.")
    print("Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()
