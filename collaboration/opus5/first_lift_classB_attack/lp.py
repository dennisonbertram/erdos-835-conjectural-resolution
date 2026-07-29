#!/usr/bin/env python3
"""Fractional relaxation of the class-B completion problem.

    x_{e,c} >= 0        for every edge e of K_A and colour c with e inside V_c
    sum_c x_{e,c} = 1                              (every edge gets one unit)
    sum_{b} x_{ab,c} = 1        for every colour c and every a in V_c

Every completion gives a 0/1 feasible point, so LP infeasibility is a
rigorous proof that no completion exists.  The screen below uses HiGHS
(floating point) and is therefore only a screen; every LP-infeasible verdict
that matters is re-proved exactly by rationalising the dual and checking the
Farkas inequalities in exact arithmetic (classb.check_farkas), or by the
exact rational phase-I simplex (classb.lp_feasible).
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

from classb import check_farkas, lp_feasible


def build(n, q, forb):
    edges = [(a, b) for a in range(n) for b in range(a + 1, n)]
    inV = [[not ((forb[a] >> c) & 1) for a in range(n)] for c in range(q)]
    V = [[a for a in range(n) if inV[c][a]] for c in range(q)]
    idx = {}
    k = 0
    for ei in range(len(edges)):
        idx[('e', ei)] = k
        k += 1
    for c in range(q):
        for a in V[c]:
            idx[('v', c, a)] = k
            k += 1
    rows, cols, vals = [], [], []
    j = 0
    colmap = []
    for ei, (a, b) in enumerate(edges):
        for c in range(q):
            if inV[c][a] and inV[c][b]:
                for r in (idx[('e', ei)], idx[('v', c, a)], idx[('v', c, b)]):
                    rows.append(r)
                    cols.append(j)
                    vals.append(1.0)
                colmap.append((ei, c))
                j += 1
    A = coo_matrix((vals, (rows, cols)), shape=(k, j)).tocsc()
    return A, k, j, edges, idx, colmap


def lp_infeasible_screen(n, q, forb):
    """Float screen.  Returns (feasible_bool, dual_y_or_None)."""
    A, m, nv, edges, idx, colmap = build(n, q, forb)
    b = np.ones(m)
    # phase I: min sum(s), A x + I s = b, x,s >= 0
    from scipy.sparse import hstack, identity
    M = hstack([A, identity(m, format="csc")], format="csc")
    cvec = np.concatenate([np.zeros(nv), np.ones(m)])
    res = linprog(cvec, A_eq=M, b_eq=b, bounds=(0, None), method="highs")
    if not res.success:
        return (None, None)
    if res.fun <= 1e-7:
        return (True, None)
    y = res.eqlin.marginals
    return (False, y)


def exact_farkas_from_float(n, q, forb, y, denom=(1, 2, 3, 4, 6, 8, 12, 24, 48, 120)):
    """Try to round the float dual to an exact Farkas certificate."""
    for d in denom:
        yy = [Fraction(int(round(t * d)), d) for t in y]
        if check_farkas(n, q, forb, yy):
            return yy
    return None


def prove_lp_infeasible(n, q, forb):
    """Rigorous: returns an exact Farkas certificate or None."""
    feas, y = lp_infeasible_screen(n, q, forb)
    if feas is True:
        return None
    if y is not None:
        cert = exact_farkas_from_float(n, q, forb, y)
        if cert is not None:
            return cert
    ok, y2 = lp_feasible(n, q, forb)          # exact rational fallback
    if ok:
        return None
    assert check_farkas(n, q, forb, y2)
    return y2
