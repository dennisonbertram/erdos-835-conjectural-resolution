#!/usr/bin/env python3
"""Exact feasibility of the two-disjoint-blocks intersection system for a
hypothetical Steiner system S(k-1, k, 3k).  All arithmetic is exact
(fractions.Fraction); no floats anywhere.

Variables: N(alpha,beta) on G = {(a,b): a,b>=0, a+b<=k}.
Equalities:
  moment(i,j), i+j<=k-1:  sum C(a,i)C(b,j) N(a,b) = lambda_{i+j} C(k,i) C(k,j)
  forced: N(k,0)=1, N(0,k)=1, N(k-1,0)=N(k-1,1)=N(1,k-1)=N(0,k-1)=0
  case:   N(0,0) = z  (z = 0 or 1)
Inequalities: N(a,b) >= 0 on all grid points.
"""
from fractions import Fraction as F
from math import comb, gcd
from functools import reduce
import sys

OUT = []
def log(s=""):
    s = str(s)
    OUT.append(s)
    print(s, flush=True)

def lcm(a, b):
    return a // gcd(a, b) * b

def lam(k, i):
    return F(comb(3 * k - i, k - 1 - i), k - i)

# ----------------------------------------------------------------------
def build(k, zval):
    grid = [(a, b) for a in range(k + 1) for b in range(k + 1 - a)]
    idx = {p: n for n, p in enumerate(grid)}
    eqs = []  # (name, {varindex: Fraction}, rhs)
    momkeys = []
    for i in range(k):
        for j in range(k - i):
            coeffs = {}
            for (a, b) in grid:
                c = comb(a, i) * comb(b, j)
                if c:
                    coeffs[idx[(a, b)]] = F(c)
            rhs = lam(k, i + j) * comb(k, i) * comb(k, j)
            eqs.append((("moment", i, j), coeffs, rhs))
            momkeys.append((i, j))
    forced = {}
    def force(p, val):
        if p in forced:
            assert forced[p] == F(val), f"conflicting forced value at {p}"
        else:
            forced[p] = F(val)
    force((k, 0), 1); force((0, k), 1)
    force((k - 1, 0), 0); force((k - 1, 1), 0)
    force((1, k - 1), 0); force((0, k - 1), 0)
    for p in sorted(forced):
        eqs.append((("forced", p), {idx[p]: F(1)}, forced[p]))
    eqs.append((("case", zval), {idx[(0, 0)]: F(1)}, F(zval)))
    return grid, idx, eqs, momkeys, forced

# ----------------------------------------------------------------------
def rref(eqs, nvars):
    """Exact RREF of [A | rhs | I] with multiplier tracking."""
    m = len(eqs)
    rows = []
    for e, (_, coeffs, rhs) in enumerate(eqs):
        vec = [F(0)] * nvars
        for j, c in coeffs.items():
            vec[j] = c
        mult = [F(0)] * m
        mult[e] = F(1)
        rows.append([vec, rhs, mult])
    r = 0
    pivots = []
    for col in range(nvars):
        piv = None
        for rr in range(r, m):
            if rows[rr][0][col] != 0:
                piv = rr
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][0][col]
        rows[r][0] = [c / pv for c in rows[r][0]]
        rows[r][1] = rows[r][1] / pv
        rows[r][2] = [c / pv for c in rows[r][2]]
        for rr in range(m):
            if rr != r and rows[rr][0][col] != 0:
                f = rows[rr][0][col]
                rows[rr][0] = [a - f * b for a, b in zip(rows[rr][0], rows[r][0])]
                rows[rr][1] = rows[rr][1] - f * rows[r][1]
                rows[rr][2] = [a - f * b for a, b in zip(rows[rr][2], rows[r][2])]
        pivots.append((r, col))
        r += 1
    for rr in range(r, m):
        if rows[rr][1] != 0:
            return {"consistent": False, "rank": r,
                    "cert": rows[rr][2], "badrhs": rows[rr][1]}
    return {"consistent": True, "rank": r, "rows": rows[:r], "pivots": pivots}

# ----------------------------------------------------------------------
def parametrize(res, nvars):
    """exprs[v] = (const, {freecol: coeff}) so N_v = const + sum coeff*t_f."""
    pivcols = {c for _, c in res["pivots"]}
    free = [c for c in range(nvars) if c not in pivcols]
    exprs = [None] * nvars
    for f in free:
        exprs[f] = (F(0), {f: F(1)})
    for rr, c in res["pivots"]:
        vec, rhs, _ = res["rows"][rr]
        lin = {f: -vec[f] for f in free if vec[f] != 0}
        exprs[c] = (rhs, lin)
    return exprs, free

# ----------------------------------------------------------------------
def normalize(c0, lin, cert):
    """Scale (positively) so the linear part has integer coefficients with
    gcd 1 (canonical direction); constant-only ineqs scaled by |c0|."""
    nz = [e for e in lin.values() if e != 0] or ([c0] if c0 != 0 else [])
    if not nz:
        return c0, lin, cert
    gn = reduce(gcd, [abs(e.numerator) for e in nz])
    gl = reduce(lcm, [e.denominator for e in nz])
    g = F(gn, gl)          # positive; dividing keeps inequality direction
    return (c0 / g, {q: c / g for q, c in lin.items()},
            {v: c / g for v, c in cert.items()})

def dedup(ineqs):
    """Exact pruning: among ineqs sharing the same normalized direction,
    only the one with the smallest constant binds; drop trivially true
    constants; keep negative constants (infeasibility witnesses)."""
    best = {}
    for c0, lin, cert in ineqs:
        if not lin:
            if c0 >= 0:
                continue                       # trivially true
            key = ("const",)
        else:
            key = tuple(sorted(lin.items()))
        if key not in best or c0 < best[key][0]:
            best[key] = (c0, lin, cert)
    return list(best.values())

def fourier_motzkin(exprs, params):
    """Ineqs: expr_v >= 0.  Returns ('INFEASIBLE', cert, c0, stages) or
    ('FEASIBLE', stages).  cert: {var: mult>=0} with
    sum mult_v * expr_v == c0 < 0 identically."""
    ineqs = []
    for v, (c0, lin) in enumerate(exprs):
        lin = {q: c for q, c in lin.items() if c != 0}
        ineqs.append(normalize(c0, lin, {v: F(1)}))
    ineqs = dedup(ineqs)
    stages = []
    remaining = list(params)
    while True:
        for c0, lin, cert in ineqs:
            if not lin and c0 < 0:
                return ("INFEASIBLE", cert, c0, stages)
        if not remaining:
            return ("FEASIBLE", stages)
        def cost(p):
            pos = sum(1 for _, lin, _ in ineqs if lin.get(p, 0) > 0)
            neg = sum(1 for _, lin, _ in ineqs if lin.get(p, 0) < 0)
            return pos * neg
        p = min(remaining, key=cost)
        remaining.remove(p)
        stages.append((p, [(c0, dict(lin)) for c0, lin, _ in ineqs]))
        P  = [q for q in ineqs if q[1].get(p, 0) > 0]
        Ng = [q for q in ineqs if q[1].get(p, 0) < 0]
        Z  = [q for q in ineqs if q[1].get(p, 0) == 0]
        sys.stderr.write(f"      [FM] elim param {p}: pos={len(P)} neg={len(Ng)} "
                         f"zero={len(Z)}, {len(remaining)} params left\n")
        sys.stderr.flush()
        new = list(Z)
        for (c1, l1, t1) in P:
            for (c2, l2, t2) in Ng:
                a, b = l1[p], -l2[p]              # a>0, b>0
                cc = b * c1 + a * c2              # b*ineq1 + a*ineq2
                lin = {}
                for q in set(l1) | set(l2):
                    if q == p:
                        continue
                    val = b * l1.get(q, F(0)) + a * l2.get(q, F(0))
                    if val != 0:
                        lin[q] = val
                cert = {}
                for v in set(t1) | set(t2):
                    cert[v] = b * t1.get(v, F(0)) + a * t2.get(v, F(0))
                new.append(normalize(cc, lin, cert))
        ineqs = dedup(new)

def backsub(stages):
    """Pick exact rational parameter values satisfying all stage systems."""
    assign = {}
    for p, snap in reversed(stages):
        lo, hi = None, None
        for c0, lin in snap:
            cp = lin.get(p, F(0))
            if cp == 0:
                continue
            R = c0 + sum(coef * assign[q] for q, coef in lin.items() if q != p)
            bound = -R / cp
            if cp > 0:
                lo = bound if lo is None else max(lo, bound)
            else:
                hi = bound if hi is None else min(hi, bound)
        assert lo is None or hi is None or lo <= hi, "FM back-substitution broke"
        if lo is not None and hi is not None:
            assign[p] = (lo + hi) / 2
        elif lo is not None:
            assign[p] = lo
        elif hi is not None:
            assign[p] = hi
        else:
            assign[p] = F(0)
    return assign

# ----------------------------------------------------------------------
def solve_transpose(eqs, nvars, m):
    """Solve A^T y = m exactly (y over equations). Returns y or None."""
    ne = len(eqs)
    rows = []
    for v in range(nvars):
        vec = [F(0)] * ne
        for e, (_, coeffs, _) in enumerate(eqs):
            c = coeffs.get(v)
            if c:
                vec[e] = c
        rows.append([vec, m[v]])
    r = 0
    piv = []
    for col in range(ne):
        p = None
        for rr in range(r, nvars):
            if rows[rr][0][col] != 0:
                p = rr
                break
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][0][col]
        rows[r][0] = [c / pv for c in rows[r][0]]
        rows[r][1] = rows[r][1] / pv
        for rr in range(nvars):
            if rr != r and rows[rr][0][col] != 0:
                f = rows[rr][0][col]
                rows[rr][0] = [a - f * b for a, b in zip(rows[rr][0], rows[r][0])]
                rows[rr][1] = rows[rr][1] - f * rows[r][1]
        piv.append((r, col))
        r += 1
    for rr in range(r, nvars):
        if rows[rr][1] != 0:
            return None
    y = [F(0)] * ne
    for rr, col in piv:
        y[col] = rows[rr][1]
    return y

# ----------------------------------------------------------------------
def print_multipliers(eqs, y, label):
    log(f"    {label} (nonzero only):")
    for e, (name, _, _) in enumerate(eqs):
        if y[e] != 0:
            log(f"      y[{name}] = {y[e]}")

def print_poly(eqs, y, k, grid, forced, zcase_pt=(0, 0)):
    """P(a,b) = sum over moment eqs y_{ij} C(a,i)C(b,j); print values."""
    cij = {}
    for e, (name, _, _) in enumerate(eqs):
        if name[0] == "moment" and y[e] != 0:
            cij[(name[1], name[2])] = y[e]
    log("    Polynomial form  P(a,b) = sum c_ij * C(a,i)*C(b,j), c_ij (nonzero):")
    for (i, j), c in sorted(cij.items()):
        log(f"      c[{i},{j}] = {c}")
    log("    P at every grid point (a,b): value   [tags: F=forced point, Z=case point]:")
    special = set(forced) | {zcase_pt}
    for (a, b) in grid:
        val = sum(c * comb(a, i) * comb(b, j) for (i, j), c in cij.items())
        tag = ""
        if (a, b) in forced:
            tag += " F"
        if (a, b) == zcase_pt:
            tag += " Z"
        log(f"      P({a},{b}) = {val}{tag}")
    momrhs = sum(y[e] * rhs for e, (name, _, rhs) in enumerate(eqs)
                 if name[0] == "moment")
    log(f"    sum over moment eqs of c_ij * RHS_ij = {momrhs}")
    return cij

def verify_combo(eqs, y, nvars):
    """Return (combo_coeff_vector, combo_rhs) for sum_e y_e * eq_e."""
    combo = [F(0)] * nvars
    rhs = F(0)
    for e, (_, coeffs, r) in enumerate(eqs):
        if y[e] == 0:
            continue
        for v, c in coeffs.items():
            combo[v] += y[e] * c
        rhs += y[e] * r
    return combo, rhs

def verify_point(eqs, N, grid):
    for name, coeffs, rhs in eqs:
        s = sum(c * N[v] for v, c in coeffs.items())
        assert s == rhs, f"point violates {name}: {s} != {rhs}"
    for v, x in enumerate(N):
        assert x >= 0, f"point negative at {grid[v]}: {x}"

# ----------------------------------------------------------------------
def run_case(k, zval):
    grid, idx, eqs, momkeys, forced = build(k, zval)
    nvars = len(grid)
    res = rref(eqs, nvars)
    info = {"nvars": nvars, "neqs": len(eqs), "rank": res["rank"]}
    log(f"  CASE Z{zval}: N(0,0) = {zval}")
    log(f"    variables = {nvars}, equations = {len(eqs)}, rank = {res['rank']}")
    if not res["consistent"]:
        info["verdict"] = "INFEASIBLE (equality stage)"
        info["dim"] = None
        log("    EQUALITY SYSTEM INCONSISTENT.  Certificate multipliers u_e with")
        log("    sum_e u_e * (LHS_e) = 0 identically and sum_e u_e * RHS_e != 0:")
        u = res["cert"]
        print_multipliers(eqs, u, "equality-inconsistency multipliers")
        combo, crhs = verify_combo(eqs, u, nvars)
        assert all(c == 0 for c in combo), "cert LHS combo not zero"
        assert crhs == res["badrhs"] and crhs != 0
        log(f"    VERIFIED from original constraints: combined LHS coefficient of every")
        log(f"    N(a,b) is exactly 0; combined RHS = {crhs} != 0.  So 0 = {crhs}: contradiction.")
        print_poly(eqs, u, k, grid, forced)
        return info
    dim = nvars - res["rank"]
    info["dim"] = dim
    log(f"    equality system CONSISTENT; affine solution dimension = {dim}")
    exprs, free = parametrize(res, nvars)
    if free:
        log(f"    free parameters correspond to variables: "
            f"{[grid[f] for f in free]}")
    fm = fourier_motzkin(exprs, free)
    if fm[0] == "INFEASIBLE":
        _, cert, c0, _ = fm
        info["verdict"] = "INFEASIBLE (inequality stage)"
        log("    NONNEGATIVITY INFEASIBLE.  Farkas certificate:")
        assert all(c >= 0 for c in cert.values()), "cert has negative multiplier"
        # internal identity check in the parameters
        tot_c = sum(cert.get(v, F(0)) * exprs[v][0] for v in range(nvars))
        tot_lin = {}
        for v, mv in cert.items():
            for q, c in exprs[v][1].items():
                tot_lin[q] = tot_lin.get(q, F(0)) + mv * c
        assert all(c == 0 for c in tot_lin.values()) and tot_c == c0 < 0
        m = [cert.get(v, F(0)) for v in range(nvars)]
        y = solve_transpose(eqs, nvars, m)
        assert y is not None, "could not lift Farkas cert to equation multipliers"
        combo, crhs = verify_combo(eqs, y, nvars)
        assert combo == m, "A^T y != m"
        assert crhs == c0, f"y^T rhs = {crhs} != {c0}"
        log(f"    Inequality multipliers m_v >= 0 (nonzero only), on N(a,b) >= 0:")
        for v in range(nvars):
            if m[v] != 0:
                log(f"      m[N{grid[v]}] = {m[v]}")
        print_multipliers(eqs, y, "equation multipliers y_e (free sign)")
        log(f"    VERIFIED from ORIGINAL constraints: sum_e y_e * (LHS coeff of N(a,b))")
        log(f"    equals m_(a,b) for every grid point (checked all {nvars}), all m >= 0,")
        log(f"    and sum_e y_e * RHS_e = {crhs} < 0.")
        log(f"    Hence any solution of the equalities satisfies")
        log(f"    sum m_(a,b) * N(a,b) = {crhs} < 0, impossible with N >= 0.")
        cij = print_poly(eqs, y, k, grid, forced)
        # sign check of P away from forced/case points
        bad = []
        for (a, b) in grid:
            if (a, b) in forced or (a, b) == (0, 0):
                continue
            val = sum(c * comb(a, i) * comb(b, j) for (i, j), c in cij.items())
            if val < 0:
                bad.append((a, b, val))
        if bad:
            log(f"    NOTE: P < 0 at non-forced points {bad} (forced-eq multipliers"
                f" absorb the difference; full certificate m_v >= 0 still exact).")
        else:
            log("    Check: P(a,b) >= 0 at every grid point outside the forced/case set.")
        info["cert"] = (m, y, crhs)
        return info
    # FEASIBLE
    _, stages = fm
    assign = backsub(stages)
    N = [exprs[v][0] + sum(c * assign[q] for q, c in exprs[v][1].items())
         for v in range(nvars)]
    verify_point(eqs, N, grid)
    info["verdict"] = "FEASIBLE"
    info["point"] = {grid[v]: N[v] for v in range(nvars)}
    log("    FEASIBLE.  One exact feasible point (nonzero entries):")
    for v in range(nvars):
        if N[v] != 0:
            log(f"      N{grid[v]} = {N[v]}")
    zeros = [grid[v] for v in range(nvars) if N[v] == 0]
    log(f"      all other entries zero: {zeros}")
    log("    Point VERIFIED against every original equality and N >= 0.")
    if free:
        log("    General solution: N = point_0 + sum_f t_f * D_f with the")
        log("    particular solution below and direction basis D_f "
            "(one per free parameter):")
        log("      particular solution (t = 0): nonzero entries:")
        for v in range(nvars):
            if exprs[v][0] != 0:
                log(f"        N{grid[v]} = {exprs[v][0]}")
        for f in free:
            log(f"      direction for parameter t[{grid[f]}] (nonzero entries):")
            for v in range(nvars):
                c = exprs[v][1].get(f, F(0))
                if c != 0:
                    log(f"        D[N{grid[v]}] = {c}")
        log(f"      chosen parameter values: "
            f"{[(grid[f], assign[f]) for f in free]}")
        log("    (nonnegativity bounds on the parameters were resolved by exact")
        log("     Fourier-Motzkin; the point above satisfies them.)")
    else:
        log("    Solution is UNIQUE (affine dimension 0).")
        info["unique"] = True
    return info

# ----------------------------------------------------------------------
def main():
    results = {}
    control_fail = []
    for k in [2, 3, 4, 5, 6, 7, 8]:
        log("=" * 78)
        log(f"k = {k}   (v = {3*k}, hypothetical S({k-1},{k},{3*k}))")
        lams = [lam(k, i) for i in range(k)]
        log(f"  lambda_i, i=0..{k-1}: {[str(x) for x in lams]}")
        nonint = [i for i, x in enumerate(lams) if x.denominator != 1]
        if nonint:
            log(f"  FLAG: lambda_i NON-INTEGRAL for i in {nonint} "
                f"-> no design exists; LP still run as instructed.")
        else:
            log("  all lambda_i integral.")
        results[k] = {"lams": lams, "nonint": nonint}
        for zval in (0, 1):
            results[k][zval] = run_case(k, zval)
        # ---------------- controls ----------------
        if k == 2:
            ok = (lams[0] == 3 and lams[1] == 1
                  and results[2][0]["verdict"].startswith("INFEASIBLE")
                  and results[2][1]["verdict"] == "FEASIBLE"
                  and results[2][1].get("unique")
                  and results[2][1]["point"] == {(a, b): (F(1) if (a, b) in
                        [(2, 0), (0, 2), (0, 0)] else F(0))
                        for a in range(3) for b in range(3 - a)})
            log(f"  CONTROL k=2: {'PASS' if ok else 'FAIL'}")
            if not ok:
                control_fail.append(2)
        if k == 3:
            expected = {(a, b): F(0) for a in range(4) for b in range(4 - a)}
            expected[(3, 0)] = expected[(0, 3)] = expected[(0, 0)] = F(1)
            expected[(1, 1)] = F(9)
            ok = (lams[0] == 12 and lams[1] == 4 and lams[2] == 1
                  and results[3][0]["verdict"].startswith("INFEASIBLE")
                  and results[3][1]["verdict"] == "FEASIBLE"
                  and results[3][1].get("unique")
                  and results[3][1]["point"] == expected)
            log(f"  CONTROL k=3: {'PASS' if ok else 'FAIL'}")
            if not ok:
                control_fail.append(3)
        if k == 8:
            exp = [43263, 14421, 4389, 1197, 285, 57, 9, 1]
            ok = lams == [F(x) for x in exp]
            log(f"  CONTROL k=8 lambdas: {'PASS' if ok else 'FAIL'}")
            if not ok:
                control_fail.append(8)
        if control_fail:
            log("!!! CONTROL FAILURE — stopping as instructed.")
            break
    log("=" * 78)
    log("SUMMARY TABLE  (verdicts; dim = affine dimension of equality solution set)")
    log(f"{'k':>2} {'nonintegral λ':>14} {'Z0 verdict':>32} {'Z1 verdict':>32} {'dim Z0':>7} {'dim Z1':>7}")
    for k in sorted(results):
        r = results[k]
        if 0 not in r:
            continue
        log(f"{k:>2} {str(r['nonint']):>14} {r[0]['verdict']:>32} "
            f"{r[1]['verdict']:>32} {str(r[0]['dim']):>7} {str(r[1]['dim']):>7}")
    if control_fail:
        log(f"CONTROL FAILURES at k = {control_fail}")
    if RESULTS_PATH is not None:
        with open(RESULTS_PATH, "w") as fh:
            fh.write("\n".join(OUT) + "\n")
    return 1 if control_fail else 0

# No result file by default: stdout is the record.  Pass
# "--results <path>" to also write the log to a file.
RESULTS_PATH = None
if "--results" in sys.argv:
    RESULTS_PATH = sys.argv[sys.argv.index("--results") + 1]

if __name__ == "__main__":
    sys.exit(main())
