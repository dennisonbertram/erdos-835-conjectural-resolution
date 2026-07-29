#!/usr/bin/env python3
"""Theorem F: the whole POINTWISE algebra of a tight colouring is forced.

Unrestricted -- no cyclic ansatz, no symmetry hypothesis, no golf design.

Context.  `collaboration/opus5/PROOF.md` Thm 7/7a shows every necessary
condition that is a LINEAR functional of the inner/dual distribution (slice
degree <= k-1) is automatically satisfied, and the exact rational five-point
certificate shows that particular LP relaxation is feasible.  Theorem F below
strengthens the first statement in a different direction: not just linear
functionals of low degree, but EVERY polynomial in the colour indicators
evaluated pointwise and summed, of EVERY order, is a constant determined by k
alone.  So no purely pointwise functional can ever obstruct, and any
obstruction must use the Johnson scheme operators nontrivially.

Also emits the explicit forced CENTRED moment tensors, which anyone building a
degree-k cubic obstruction needs as a baseline.

Verified exactly (Fraction arithmetic) against the real tight 3-colouring of
J(4,2) at k=2 -- a case where a tight colouring genuinely exists.

Stdlib only.  Run:
    python3 -B evidence/verify_pointwise_moment_exhaustion.py
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import comb


# ------------------------------------------------------------------ theory

def raw_moment(k, multiset):
    """sum_x prod_i f_{a_i}(x) for a tight (k+1)-colouring.

    The colour classes partition the vertex set, so the indicators are
    idempotent with pairwise disjoint supports:  f_a f_b = delta_{ab} f_a.
    Hence the product is f_a if every index equals a, and 0 otherwise.
    """
    N, p = comb(2 * k, k), k + 1
    if len(set(multiset)) == 1:
        return Fraction(N, p)
    return Fraction(0)


def centred_moment(k, multiset):
    """sum_x prod_i g_{a_i}(x) where g_a = f_a - 1/p.

    Expand the product and use raw_moment on each term.
    """
    N, p = comb(2 * k, k), k + 1
    m = len(multiset)
    total = Fraction(0)
    for pick in product((0, 1), repeat=m):        # 1 = take f, 0 = take -1/p
        coeff = Fraction((-1) ** (m - sum(pick)), p ** (m - sum(pick)))
        chosen = [multiset[i] for i in range(m) if pick[i]]
        if not chosen:
            total += coeff * N                     # sum_x 1 = N
        else:
            total += coeff * raw_moment(k, chosen)
    return total


# ------------------------------------------------- the k=2 control colouring

def tight_colouring_k2():
    """J(4,2): vertices are the 2-subsets of [4]; non-adjacency is disjointness,
    so the three complementary pairs are the three colour classes."""
    verts = [frozenset(s) for s in combinations(range(4), 2)]
    classes = []
    used = set()
    for v in verts:
        if v in used:
            continue
        comp = frozenset(set(range(4)) - v)
        classes.append((v, comp))
        used |= {v, comp}
    assert len(classes) == 3 and all(len(c) == 2 for c in classes)
    # every class must be independent: J(4,2) adjacency is |A cap B| = 1
    for a, b in classes:
        assert len(a & b) != 1
    # and they must partition the 6 vertices
    flat = [x for c in classes for x in c]
    assert sorted(map(sorted, flat)) == sorted(map(sorted, verts))
    return verts, classes


def empirical_moment(verts, classes, multiset, centred):
    p = len(classes)
    idx = {}
    for q, cls in enumerate(classes):
        for v in cls:
            idx[v] = q
    total = Fraction(0)
    for v in verts:
        prod = Fraction(1)
        for a in multiset:
            val = Fraction(1) if idx[v] == a else Fraction(0)
            if centred:
                val -= Fraction(1, p)
            prod *= val
        total += prod
    return total


# ------------------------------------------------------------------ main

def main():
    print("=" * 74)
    print("Theorem F (unrestricted).  Every pointwise moment is forced.")
    print("=" * 74)
    print("    Let c be ANY tight (k+1)-colouring of J(2k,k), with colour")
    print("    classes C_0..C_k and indicators f_q, N = C(2k,k), p = k+1.")
    print("    The classes partition the vertices, so f_a f_b = delta_ab f_a.")
    print("    Therefore for any multiset a_1..a_m of colours")
    print("        sum_x f_{a_1}(x)...f_{a_m}(x) = N/p if all a_i are equal,")
    print("                                      = 0   otherwise.")
    print("    []")
    print()
    print("    CONSEQUENCE.  Every polynomial functional of the indicators")
    print("    evaluated pointwise and summed -- of EVERY order, not just")
    print("    order <= k-1 -- is a constant depending only on k.  No such")
    print("    functional can separate a hypothetical tight colouring from an")
    print("    existing one, so no purely pointwise obstruction exists at any")
    print("    order.  Any obstruction must pair the indicators against the")
    print("    Johnson scheme operators (adjacency), not merely multiply them")
    print("    pointwise.  This is consistent with, and sharpens, the")
    print("    'full slice degree k plus third-order idempotence' frontier")
    print("    recorded in collaboration/opus5/PROOF.md.")

    print()
    print("=" * 74)
    print("Forced centred moments g_a = f_a - 1/p, at k = 16 (p = 17)")
    print("=" * 74)
    k = 16
    N, p = comb(2 * k, k), k + 1
    print(f"    N = C(32,16) = {N},  p = {p}")
    cases = [
        ("<g_a, g_a>", (0, 0), None),
        ("<g_a, g_b>, a != b", (0, 1), None),
        ("T_aaa", (0, 0, 0), None),
        ("T_aac, a != c", (0, 0, 1), None),
        ("T_abc all distinct", (0, 1, 2), None),
        ("Q_abcd all distinct", (0, 1, 2, 3), None),
    ]
    for label, ms, _ in cases:
        val = centred_moment(k, ms)
        num = val * Fraction(p ** len(ms), N)
        print(f"    {label:22s} = {str(val):>28s}"
              f"   = ({num}) * N / {p}^{len(ms)}")

    # the centred moments must sum to zero over all colour tuples, because
    # sum_a g_a = 0 identically
    for m in (2, 3, 4):
        tot = Fraction(0)
        for tup in product(range(p), repeat=m):
            tot += centred_moment(k, tup)
        assert tot == 0, (m, tot)
    print("    consistency: sum over all colour tuples vanishes for m=2,3,4"
          " (since sum_a g_a = 0): ok")

    print()
    print("=" * 74)
    print("Control: the genuine tight 3-colouring of J(4,2) (k=2)")
    print("=" * 74)
    verts, classes = tight_colouring_k2()
    print(f"    {len(verts)} vertices, {len(classes)} colour classes, "
          f"sizes {[len(c) for c in classes]}")
    checked = 0
    for m in range(1, 6):
        for tup in product(range(3), repeat=m):
            got_raw = empirical_moment(verts, classes, tup, centred=False)
            want_raw = raw_moment(2, tup)
            assert got_raw == want_raw, (tup, got_raw, want_raw)
            got_c = empirical_moment(verts, classes, tup, centred=True)
            want_c = centred_moment(2, tup)
            assert got_c == want_c, (tup, got_c, want_c)
            checked += 1
    print(f"    every raw and centred moment up to order 5 matches the closed"
          f" form: {checked} tuples, exact rational arithmetic: ok")

    print()
    print("SCOPE.  Theorem F is unrestricted -- it assumes no symmetry and no")
    print("ansatz -- but it is a NO-GO about a class of proof strategies, not")
    print("progress toward existence.  Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()
