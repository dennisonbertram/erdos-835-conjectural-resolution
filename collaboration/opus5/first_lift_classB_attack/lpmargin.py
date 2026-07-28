#!/usr/bin/env python3
"""LP margin phi* of a class-B instance, and an annealer that minimises it.

    phi*(S) = max { rho : A x = b, x_j >= rho for every allowed pair (e,c) }

where A x = b is the fractional relaxation of the completion problem
(see lp.py).  Substituting x = z + rho.1 with z >= 0 turns this into

    max rho   subject to   A z + rho s = b,  z >= 0,     s := A.1 .

phi* > 0  : the relaxation has a strict interior
phi* = 0  : feasible but every fractional solution touches a boundary
phi* < 0  : the relaxation is INFEASIBLE, hence no completion exists.

A negative phi* found in floating point is only a screen; classb.lp_feasible /
classb.check_farkas re-prove it in exact rational arithmetic.
"""

from __future__ import annotations

import random
import sys
import time
from collections import Counter

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, hstack

from classb import (check_class_B, m_profiles, random_class_B, random_move,
                    solve_dfs, supports, profile)


def phi(n, q, forb):
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
    for ei, (a, b) in enumerate(edges):
        for c in range(q):
            if inV[c][a] and inV[c][b]:
                for r in (idx[('e', ei)], idx[('v', c, a)], idx[('v', c, b)]):
                    rows.append(r)
                    cols.append(j)
                    vals.append(1.0)
                j += 1
    A = coo_matrix((vals, (rows, cols)), shape=(k, j)).tocsc()
    s = np.asarray(A.sum(axis=1)).ravel()
    M = hstack([A, coo_matrix(s.reshape(-1, 1))], format="csc")
    c_obj = np.zeros(j + 1)
    c_obj[-1] = -1.0                     # maximise rho
    bounds = [(0, None)] * j + [(None, None)]
    res = linprog(c_obj, A_eq=M, b_eq=np.ones(k), bounds=bounds, method="highs")
    if not res.success:
        return None                      # b not even in range(A): infeasible
    return -res.fun


# ---------------------------------------------------------------------------
def anneal(n, q, seed, restarts, steps, out):
    rng = random.Random(seed)
    best = (1e9, None)
    hist = Counter()
    for r in range(restarts):
        forb = random_class_B(n, q, rng, rng.choice(m_profiles(n)))
        if forb is None:
            continue
        cur = phi(n, q, forb)
        if cur is None:
            continue
        for s in range(steps):
            T = 0.20 * (0.002 / 0.20) ** (s / max(1, steps - 1))
            nf = random_move(n, q, forb, rng)
            if nf is None:
                continue
            try:
                check_class_B(n, q, nf)
            except AssertionError:
                continue
            v = phi(n, q, nf)
            if v is None:
                v = -1.0
            if v <= cur or rng.random() < pow(2.718281828, (cur - v) / T):
                forb, cur = nf, v
            if cur < best[0]:
                best = (cur, list(forb))
                if cur < -1e-9:
                    print("LP-INFEASIBLE CANDIDATE phi*=%.6g %s" % (cur, forb), flush=True)
                    with open(out, "a") as fh:
                        fh.write("LPCAND %.6g %s\n" % (cur, forb))
        hist[round(cur, 4)] += 1
    print("n=%d seed=%d restarts=%d steps=%d  best phi* = %.6g   forb=%s"
          % (n, seed, restarts, steps, best[0], best[1]), flush=True)
    return best


if __name__ == "__main__":
    n = int(sys.argv[1])
    seed = int(sys.argv[2])
    restarts = int(sys.argv[3])
    steps = int(sys.argv[4])
    anneal(n, n + 4, seed, restarts, steps, "logs/lpcand_n%d_%d.txt" % (n, seed))
