#!/usr/bin/env python3
"""Necessary-condition sweep for the S(7,8,24) tower:
  D1 S(7,8,24), D2 S(6,7,23), D3 S(5,6,22), D4 S(4,5,21).

STEP 1: forced pair-intersection distribution n_j per design (exact).
STEP 2: Delsarte dual distribution B in the Johnson scheme J(v,k), with the
        P/Q duality identity PQ = C(v,k) I verified exactly before use.
STEP 3: per (design, j with n_j>0): the forced two-block configuration LP
        (cells I,S1,S2,W) -- rank/affine dim, exact feasibility, and exact
        LP min/max of the closing cell M(j,0,0,k-j) and the inner-block cell
        M(0,0,0,k).

Exact rationals throughout; numpy only for modular integer elimination and
never as evidence -- every accepted result is verified exactly over Q.
"""
import sys, time
from fractions import Fraction as F
from math import comb
import numpy as np

HERE = __file__.rsplit("/", 1)[0] or "."
sys.path.insert(0, HERE)
import verify_ambient_moment_lp as amb
from verify_ambient_moment_lp import lcm

# No result file by default: stdout is the record.  Pass
# "--results <path>" to also write the log to a file.
RESULTS_PATH = None
if "--results" in sys.argv:
    RESULTS_PATH = sys.argv[sys.argv.index("--results") + 1]
OUT = []
def log(s=""):
    s = str(s)
    OUT.append(s)
    print(s, flush=True)
amb.log = log            # route imported machinery's logging into this file

def flush_results():
    if RESULTS_PATH is None:
        return
    with open(RESULTS_PATH, "w") as fh:
        fh.write("\n".join(OUT) + "\n")

DESIGNS = [("D1 S(7,8,24)", 8, 24, [43263, 14421, 4389, 1197, 285, 57, 9, 1]),
           ("D2 S(6,7,23)", 7, 23, [14421, 4389, 1197, 285, 57, 9, 1]),
           ("D3 S(5,6,22)", 6, 22, [4389, 1197, 285, 57, 9, 1]),
           ("D4 S(4,5,21)", 5, 21, [1197, 285, 57, 9, 1])]

def lams_of(v, k):
    t = k - 1
    return [F(comb(v - i, t - i), k - i) for i in range(t + 1)]

# ------------------------------ STEP 1 ---------------------------------
def pair_distribution(v, k):
    """n_j = #blocks (other than B0) meeting a fixed block B0 in j points,
    j = 0..t-1, from sum_j C(j,i) n_j = C(k,i)(lambda_i - 1), i=0..t-1
    (triangular; solved downward)."""
    t = k - 1
    lams = lams_of(v, k)
    n = [F(0)] * t
    for i in range(t - 1, -1, -1):
        rhs = comb(k, i) * (lams[i] - 1)
        n[i] = rhs - sum(comb(jj, i) * n[jj] for jj in range(i + 1, t))
    assert sum(n) == lams[0] - 1, "sum n_j != b-1"
    return n

# ------------------------------ STEP 2 ---------------------------------
def delsarte(v, k, njs):
    """Dual distribution B of the inner distribution a (a_0=1, a_{k-j}=n_j)
    in J(v,k).  The duality convention is validated by checking
    P Q == C(v,k) I exactly before use."""
    def Eb(i, m):        # Eberlein E_m(i)
        return sum((-1) ** h * comb(i, h) * comb(k - i, m - h)
                   * comb(v - k - i, m - h)
                   for h in range(0, min(i, m) + 1))
    K = k + 1
    P = [[F(Eb(i, m)) for m in range(K)] for i in range(K)]
    f = [comb(v, i) - (comb(v, i - 1) if i else 0) for i in range(K)]
    val = [comb(k, m) * comb(v - k, m) for m in range(K)]
    Y = comb(v, k)
    Q = [[F(f[m]) * P[m][i] / val[i] for m in range(K)] for i in range(K)]
    ok = all(sum(P[i][m] * Q[m][i2] for m in range(K)) ==
             (Y if i == i2 else 0) for i in range(K) for i2 in range(K))
    ok2 = all(sum(Q[i][m] * P[m][i2] for m in range(K)) ==
              (Y if i == i2 else 0) for i in range(K) for i2 in range(K))
    assert ok and ok2, "PQ = |Y| I duality identity FAILED -- stopping"
    b = lams_of(v, k)[0]
    a = [F(0)] * K
    a[0] = F(1)
    for j, nj in enumerate(njs):
        a[k - j] = nj
    B = [sum(a[i] * Q[i][m] for i in range(K)) / b for m in range(K)]
    return B

# --------------------- STEP 3: configuration LP -------------------------
def build_config(v, k, j):
    """Cells I(|I|=j), S1(k-j), S2(k-j), W(v-2k+j); B1=I∪S1, B2=I∪S2."""
    t = k - 1
    s1 = k - j
    w = v - 2 * k + j
    grid = [(a, al, be, ga)
            for a in range(j + 1) for al in range(s1 + 1)
            for be in range(s1 + 1) for ga in range(w + 1)
            if a + al + be + ga == k]
    idx = {c: i for i, c in enumerate(grid)}
    lams = lams_of(v, k)
    mom = []
    for p in range(min(j, t) + 1):
        for i in range(min(s1, t) + 1):
            for q in range(min(s1, t) + 1):
                for l in range(min(w, t) + 1):
                    s = p + i + q + l
                    if s > t:
                        continue
                    coeffs = {}
                    for c in grid:
                        a, al, be, ga = c
                        cf = (comb(a, p) * comb(al, i) * comb(be, q)
                              * comb(ga, l))
                        if cf:
                            coeffs[idx[c]] = F(cf)
                    rhs = (lams[s] * comb(j, p) * comb(s1, i) * comb(s1, q)
                           * comb(w, l))
                    mom.append((("moment", p, i, q, l), coeffs, rhs))
    B1 = (j, s1, 0, 0)
    B2 = (j, 0, s1, 0)
    forced = {B1: F(1), B2: F(1)}
    for c in grid:
        a, al, be, ga = c
        if (c != B1 and a + al >= t) or (c != B2 and a + be >= t):
            assert c not in (B1, B2)
            assert forced.get(c, F(0)) == 0
            forced[c] = F(0)
    for_eqs = [(("forced", c), {idx[c]: F(1)}, forced[c])
               for c in sorted(forced)]
    # exact hypergeometric sanity check of the moment matrix
    b = lams[0]
    Cvk = comb(v, k)
    wts = [comb(j, c[0]) * comb(s1, c[1]) * comb(s1, c[2]) * comb(w, c[3])
           for c in grid]
    for name, coeffs, rhs in mom:
        ssum = sum(int(cf) * wts[i] for i, cf in coeffs.items())
        assert b * ssum == rhs * Cvk, f"hypergeom check failed {name}"
    return grid, idx, mom, for_eqs

# ----------------------- exact LP optimizer -----------------------------
def pivot(T, basis, i, e):
    piv = T[i][e]
    T[i] = [x / piv for x in T[i]]
    for ii in range(len(T)):
        if ii != i and T[ii][e] != 0:
            fct = T[ii][e]
            T[ii] = [a - fct * bb for a, bb in zip(T[ii], T[i])]
    basis[i] = e

def core_simplex(T, basis, cost, barred):
    """Minimize cost over the tableau; Dantzig rule with Bland fallback
    (after 3000 iterations) for guaranteed termination.  Exact Fractions."""
    nrows = len(T)
    ncols = len(T[0]) - 1
    it = 0
    while True:
        it += 1
        assert it < 300000, "simplex iteration cap"
        y = [sum(cost[basis[i]] * T[i][c] for i in range(nrows))
             for c in range(ncols)]
        basset = set(basis)
        cands = [(cost[c] - y[c], c) for c in range(ncols)
                 if c not in basset and c not in barred and cost[c] - y[c] < 0]
        if not cands:
            return
        enter = min(cands)[1] if it <= 3000 else min(c for _, c in cands)
        best = None
        for i in range(nrows):
            if T[i][enter] > 0:
                ratio = T[i][-1] / T[i][enter]
                if (best is None or ratio < best[0]
                        or (ratio == best[0] and basis[i] < basis[best[1]])):
                    best = (ratio, i)
        assert best is not None, "unbounded LP (unexpected here)"
        pivot(T, basis, best[1], enter)

def lp_optimize(exprs, params, obj, sense):
    """Exact optimum of obj = (g0, {param: coeff}) over
    {t : const_v + lin_v.t >= 0 for all v}.  Solves the dual
    (rows = #params) with two-phase simplex; the optimal value is certified
    both by a verified primal point achieving it and by verified dual
    multipliers mu >= 0 with sum mu_v lin_v = g and g0 - sum mu_v const_v = V.
    Returns (V, primal_assign, mu)."""
    g0, glin = obj
    if sense == "max":
        V, assign, mu = lp_optimize(
            exprs, params, (-g0, {p: -c for p, c in glin.items()}), "min")
        return -V, assign, mu
    d = len(params)
    nv = len(exprs)
    if d == 0:
        return g0, {}, {}
    consts = [e[0] for e in exprs]
    g = [glin.get(p, F(0)) for p in params]
    art0 = nv
    T = []
    flip = []
    for jj in range(d):
        row = ([exprs[v][1].get(params[jj], F(0)) for v in range(nv)]
               + [F(0)] * d + [g[jj]])
        if g[jj] < 0:
            row = [-x for x in row]
            flip.append(-1)
        else:
            flip.append(1)
        row[art0 + jj] = F(1)
        T.append(row)
    basis = [art0 + jj for jj in range(d)]
    cost1 = [F(0)] * nv + [F(1)] * d + [F(0)]
    core_simplex(T, basis, cost1, barred=set())
    val1 = sum(cost1[basis[i]] * T[i][-1] for i in range(d))
    assert val1 == 0, "dual infeasible => primal unbounded (unexpected)"
    for i in range(d):
        if basis[i] >= art0:
            e = next((c for c in range(nv) if T[i][c] != 0), None)
            assert e is not None, "dependent parameter direction"
            pivot(T, basis, i, e)
    cost2 = list(consts) + [F(0)] * d + [F(0)]
    core_simplex(T, basis, cost2, barred=set(range(art0, art0 + d)))
    Wstar = sum(cost2[basis[i]] * T[i][-1] for i in range(d))
    V = g0 - Wstar
    mu = {basis[i]: T[i][-1] for i in range(d)
          if basis[i] < nv and T[i][-1] != 0}
    assert all(x >= 0 for x in mu.values())
    for jj in range(d):
        assert sum(m * exprs[v][1].get(params[jj], F(0))
                   for v, m in mu.items()) == g[jj], "dual eq check failed"
    assert g0 - sum(m * consts[v] for v, m in mu.items()) == V
    cB = [cost2[basis[i]] for i in range(d)]
    pi = [flip[jj] * sum(cB[i] * T[i][art0 + jj] for i in range(d))
          for jj in range(d)]
    for sgn in (1, -1):
        assign = {params[jj]: sgn * pi[jj] for jj in range(d)}
        vals = [exprs[v][0] + sum(cf * assign[q]
                                  for q, cf in exprs[v][1].items())
                for v in range(nv)]
        if all(x >= 0 for x in vals):
            objval = g0 + sum(g[jj] * assign[params[jj]] for jj in range(d))
            if objval == V:
                return V, assign, mu
    raise RuntimeError("primal recovery failed exact verification")

# ------------------------- per-config driver ----------------------------
def run_config(dname, v, k, j, nj):
    t0 = time.monotonic()
    t = k - 1
    grid, idx, mom, for_eqs = build_config(v, k, j)
    nv = len(grid)
    E = mom + for_eqs
    log(f"  ({dname}, j={j})  n_j={nj}: cells={nv}, moment eqs={len(mom)}, "
        f"forced eqs={len(for_eqs)} (hypergeom check passed)")
    sol = amb.exact_affine_solution(E, nv, f"{dname} j={j}")
    if not sol["consistent"]:
        rhsvec = [rhs for (_, _, rhs) in E]
        u = amb.exact_transpose_solve(E, nv, [F(0)] * nv,
                                      extra_row=(rhsvec, F(1)),
                                      tag=f"{dname} j={j} left-null")
        log(f"    *** INFEASIBLE (equality stage) *** -- MAJOR FLAG.  Exact "
            f"left-null certificate u (nonzero entries):")
        for e, (name, _, _) in enumerate(E):
            if u[e] != 0:
                log(f"      u[{name}] = {u[e]}")
        log("    VERIFIED exactly: sum u_e*LHS_e = 0 per cell, "
            "sum u_e*RHS_e = 1, so 0 = 1.")
        return {"verdict": "INFEASIBLE (equality)", "dim": None}
    x0, kernel = sol["x0"], sol["kernel"]
    d = len(kernel)
    log(f"    rank = {sol['rank']}, affine dim = {d}")
    exprs = [(x0[v2], {i2: kernel[i2][v2] for i2 in range(d)
                       if kernel[i2][v2] != 0}) for v2 in range(nv)]
    params = list(range(d))
    feas = amb.simplex_feasibility(exprs, params)
    if feas[0] == "INFEASIBLE":
        _, mu, c0 = feas
        m = [mu.get(v2, F(0)) for v2 in range(nv)]
        y = amb.exact_transpose_solve(E, nv, m, tag=f"{dname} j={j} farkas")
        crhs = sum(y[e] * E[e][2] for e in range(len(E)))
        assert crhs == c0 < 0
        log(f"    *** INFEASIBLE (inequality stage) *** -- MAJOR FLAG.  "
            f"Farkas certificate:")
        log(f"      m >= 0 (nonzero): " +
            ", ".join(f"m[M{grid[v2]}]={m[v2]}"
                      for v2 in range(nv) if m[v2] != 0))
        log(f"      equation multipliers y (nonzero):")
        for e, (name, _, _) in enumerate(E):
            if y[e] != 0:
                log(f"        y[{name}] = {y[e]}")
        log(f"      VERIFIED exactly: sum_e y_e*LHS_e = m per cell, m >= 0, "
            f"sum_e y_e*RHS_e = {crhs} < 0.")
        return {"verdict": "INFEASIBLE (inequality)", "dim": d}
    _, assign0 = feas
    x = [exprs[v2][0] + sum(cf * assign0[q]
                            for q, cf in exprs[v2][1].items())
         for v2 in range(nv)]
    assert amb.verify_solution(sol["sprows"], x)
    assert all(xx >= 0 for xx in x)
    log(f"    FEASIBLE; witness point verified exactly against all "
        f"{len(E)} equations and M >= 0 ({sum(1 for xx in x if xx != 0)} "
        f"nonzero cells).")
    # tracked cells
    close_cell = (j, k - j, 0, 0)  # placeholder replaced below
    close_cell = (j, 0, 0, k - j)
    incell = (0, 0, 0, k)
    tracked = [close_cell] + ([incell] if incell != close_cell else [])
    res = {"verdict": "FEASIBLE", "dim": d, "minmax": {}}
    for cell in tracked:
        ci = idx[cell]
        obj = (x0[ci], {i2: kernel[i2][ci] for i2 in range(d)
                        if kernel[i2][ci] != 0})
        vmin, amin, mumin = lp_optimize(exprs, params, obj, "min")
        vmax, amax, mumax = lp_optimize(exprs, params, obj, "max")
        res["minmax"][cell] = (vmin, vmax)
        log(f"    LP range of M{cell}: min = {vmin}, max = {vmax} "
            f"(both certified: verified achieving points + verified dual "
            f"multipliers)")
        if vmin > 0:
            # lift the lower bound to original-equation multipliers
            target = [F(1) if v2 == ci else F(0) for v2 in range(nv)]
            for v2, mv in mumin.items():
                target[v2] -= mv
            y = amb.exact_transpose_solve(E, nv, target,
                                          tag=f"{dname} j={j} bound {cell}")
            V2 = sum(y[e] * E[e][2] for e in range(len(E)))
            assert V2 == vmin
            log(f"      FORCED-POSITIVE: M{cell} >= {vmin} for EVERY "
                f"solution -- certified at original-equation level: "
                f"y with sum_e y_e*LHS_e = e_cell - m (m >= 0) and "
                f"sum_e y_e*RHS_e = {V2}; hence M(cell) = {V2} + "
                f"sum m_v M_v >= {V2} > 0.  ({sum(1 for ye in y if ye != 0)} "
                f"nonzero y entries; stored in results file context)")
            res.setdefault("forced_pos", []).append((cell, vmin))
    log(f"    [time] config: {time.monotonic()-t0:.1f}s")
    flush_results()
    return res

# ------------------------------- main ----------------------------------
def main():
    t_all = time.monotonic()
    sweep = {}
    for dname, k, v, lam_claim in DESIGNS:
        log("=" * 78)
        log(f"{dname}  (t={k-1}, k={k}, v={v})")
        lams = lams_of(v, k)
        if lams != [F(x) for x in lam_claim]:
            log(f"!!! lambda mismatch: formula gives "
                f"{[str(x) for x in lams]} vs claimed {lam_claim}.  STOP.")
            flush_results()
            return 1
        log(f"  lambdas verified: {[str(x) for x in lams]}")
        nonint = [i for i, x in enumerate(lams) if x.denominator != 1]
        if nonint:
            log(f"  FLAG: non-integral lambda at i in {nonint}")
        # STEP 1
        n = pair_distribution(v, k)
        log(f"  STEP 1 pair distribution n_j (j=0..{k-2}): "
            f"{[str(x) for x in n]}")
        bad = [(jj, x) for jj, x in enumerate(n)
               if x < 0 or x.denominator != 1]
        if bad:
            log(f"  *** NONEXISTENCE FLAG: negative/non-integral n_j at "
                f"{bad} ***")
        log(f"  check sum n_j = b-1 = {lams[0]-1}: PASS")
        # STEP 2
        B = delsarte(v, k, n)
        log(f"  STEP 2 Delsarte: PQ = C({v},{k}) I verified exactly.  "
            f"B vector (m=0..{k}): {[str(x) for x in B]}")
        zer = all(B[m] == 0 for m in range(1, k))
        neg = [(m, B[m]) for m in range(len(B)) if B[m] < 0]
        log(f"  B_1..B_{k-1} all zero: {zer};  negative entries: "
            f"{neg if neg else 'none'}")
        if neg:
            log(f"  *** NONEXISTENCE FLAG: negative B_m at {neg} ***")
        sweep[dname] = {"n": n, "B": B, "configs": {}}
        flush_results()
    # STEP 3
    log("=" * 78)
    log("STEP 3: forced two-block configuration LPs")
    for dname, k, v, _ in DESIGNS:
        n = sweep[dname]["n"]
        for j in range(k - 1):
            if n[j] == 0:
                log(f"  ({dname}, j={j}): n_j = 0 -> configuration not "
                    f"forced; SKIPPED")
                continue
            sweep[dname]["configs"][j] = run_config(dname, v, k, j, n[j])
    # summary
    log("=" * 78)
    log("SUMMARY")
    for dname, k, v, _ in DESIGNS:
        log(f"{dname}: n_j = {[str(x) for x in sweep[dname]['n']]}")
        log(f"  B = {[str(x) for x in sweep[dname]['B']]}")
        for j, r in sorted(sweep[dname]["configs"].items()):
            mm = "; ".join(f"M{c}: [{a}, {b}]"
                           for c, (a, b) in r.get("minmax", {}).items())
            fp = r.get("forced_pos")
            log(f"  j={j}: {r['verdict']}, dim={r['dim']}"
                + (f", {mm}" if mm else "")
                + (f", FORCED-POSITIVE: {fp}" if fp else ""))
    log(f"[time] total sweep: {time.monotonic()-t_all:.1f}s")
    flush_results()
    return 0

if __name__ == "__main__":
    sys.exit(main())
