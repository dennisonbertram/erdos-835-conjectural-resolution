#!/usr/bin/env python3
"""Ambient 4-cell system for a hypothetical S(r-1, r, 2r+1).

Point set partition: I (m), S1 (m+1), S2 (m+1), W (m+1), m=(r-1)/2,
B1=I∪S1 and B2=I∪S2 blocks with B1∩B2=I.  Variables M(a,al,be,ga)>=0 on
{0<=a<=m, 0<=al,be,ga<=m+1, a+al+be+ga=r}.

All accepted results are EXACT (fractions.Fraction) and verified against the
original equations.  numpy is used ONLY for modular *integer* elimination as a
search accelerator (no floating point anywhere); every candidate produced that
way is then verified exactly over Q, and the exact verification is the
deliverable.
"""
import sys, time
from fractions import Fraction as F
from math import comb, gcd, isqrt
import numpy as np

HERE = __file__.rsplit("/", 1)[0] or "."
sys.path.insert(0, HERE)
from verify_derived_closure_lp import (rref, parametrize, fourier_motzkin,
                                       backsub, solve_transpose,
                                       verify_combo, verify_point)

# The exact transcript is printed to stdout.  Pass "--results <path>" to also
# write it to a file; the default verifier run leaves the worktree untouched.
RESULTS_PATH = None
if "--results" in sys.argv:
    RESULTS_PATH = sys.argv[sys.argv.index("--results") + 1]
OUT = []
def log(s=""):
    s = str(s)
    OUT.append(s)
    print(s, flush=True)

def flush_results():
    if RESULTS_PATH is None:
        return
    with open(RESULTS_PATH, "w") as fh:
        fh.write("\n".join(OUT) + "\n")

def lcm(a, b):
    return a // gcd(a, b) * b

def lam(r, s):
    return F(comb(2 * r + 1 - s, r - 1 - s), r - s)

# ----------------------------------------------------------------------
def build(r):
    m = (r - 1) // 2
    grid = [(a, al, be, ga)
            for a in range(m + 1) for al in range(m + 2)
            for be in range(m + 2) for ga in range(m + 2)
            if a + al + be + ga == r]
    idx = {c: i for i, c in enumerate(grid)}
    mom = []
    for p in range(m + 1):
        for i in range(m + 2):
            for j in range(m + 2):
                for l in range(m + 2):
                    s = p + i + j + l
                    if s > r - 1:
                        continue
                    coeffs = {}
                    for c in grid:
                        a, al, be, ga = c
                        w = comb(a, p) * comb(al, i) * comb(be, j) * comb(ga, l)
                        if w:
                            coeffs[idx[c]] = F(w)
                    rhs = (lam(r, s) * comb(m, p) * comb(m + 1, i)
                           * comb(m + 1, j) * comb(m + 1, l))
                    mom.append((("moment", p, i, j, l), coeffs, rhs))
    B1 = (m, m + 1, 0, 0)
    B2 = (m, 0, m + 1, 0)
    zc = (m, 0, 0, m + 1)
    forced = {B1: F(1), B2: F(1)}
    for c in grid:
        a, al, be, ga = c
        if (c != B1 and a + al >= r - 1) or (c != B2 and a + be >= r - 1):
            assert c not in (B1, B2, zc)
            assert forced.get(c, F(0)) == 0
            forced[c] = F(0)
    for_eqs = [(("forced", c), {idx[c]: F(1)}, forced[c])
               for c in sorted(forced)]
    return grid, idx, mom, for_eqs, zc, B1, B2

def check_hypergeom(r, grid, idx, mom):
    """Exact check: M̄(c) = b*C(m,a)C(m+1,al)C(m+1,be)C(m+1,ga)/C(v,r)
    satisfies every moment equation (pure-integer verification)."""
    m = (r - 1) // 2
    v = 2 * r + 1
    b = lam(r, 0)
    Cvr = comb(v, r)
    w = [comb(m, c[0]) * comb(m + 1, c[1]) * comb(m + 1, c[2])
         * comb(m + 1, c[3]) for c in grid]
    for name, coeffs, rhs in mom:
        ssum = sum(int(cf) * w[i] for i, cf in coeffs.items())
        assert b * ssum == rhs * Cvr, f"hypergeom check failed at {name}"
    log(f"  [check] hypergeometric point satisfies all {len(mom)} moment "
        f"equations exactly (moment-matrix build validated).")

# ------------------------- modular machinery ---------------------------
def gen_primes(n, start=33_554_467):
    ps = []
    c = start
    while len(ps) < n:
        if all(c % q for q in range(2, isqrt(c) + 1)):
            ps.append(c)
        c += 2
    return ps

PRIMES = gen_primes(60)

def modp_rref(Mint, ncoef, p):
    """RREF mod p over the first ncoef columns.  Returns (R_top, pivcols,
    consistent) where consistent means all zero-coefficient rows have zero
    in the remaining (rhs) columns."""
    R = (Mint % p).astype(np.int64)
    nr = R.shape[0]
    r0 = 0
    pivcols = []
    for col in range(ncoef):
        if r0 >= nr:
            break
        nz = np.nonzero(R[r0:, col])[0]
        if nz.size == 0:
            continue
        pr = r0 + int(nz[0])
        if pr != r0:
            R[[r0, pr]] = R[[pr, r0]]
        inv = pow(int(R[r0, col]), -1, p)
        R[r0] = (R[r0] * inv) % p
        colv = R[:, col].copy()
        colv[r0] = 0
        rows = np.nonzero(colv)[0]
        if rows.size:
            R[rows] = (R[rows] - np.outer(colv[rows], R[r0])) % p
        pivcols.append(col)
        r0 += 1
    consistent = not np.any(R[r0:, ncoef:])
    return R[:r0], pivcols, consistent

def crt(res, primes):
    X, Pm = 0, 1
    for r_, p_ in zip(res, primes):
        t = ((int(r_) - X) * pow(Pm % p_, -1, p_)) % p_
        X += Pm * t
        Pm *= p_
    return X, Pm

def ratrec(c, P):
    c %= P
    if c == 0:
        return F(0)
    a0, a1 = P, c
    b0, b1 = 0, 1
    bnd = isqrt(P // 2)
    while a1 > bnd:
        q = a0 // a1
        a0, a1 = a1, a0 - q * a1
        b0, b1 = b1, b0 - q * b1
    if b1 == 0 or abs(b1) > bnd:
        return None
    num, den = (a1, b1) if b1 > 0 else (-a1, -b1)
    if den == 0 or gcd(den, P) != 1 or (num - c * den) % P != 0:
        return None
    g = gcd(abs(num), den)
    return F(num // g, den // g)

def reconstruct_vec(percol, primes):
    """percol: list over primes of int arrays; -> list of Fractions or None."""
    out = []
    n = len(percol[0])
    for i in range(n):
        X, P = crt([v[i] for v in percol], primes)
        f = ratrec(X, P)
        if f is None:
            return None
        out.append(f)
    return out

def int_rows(eqs, nv):
    """(list of (list[(cell,intcoef)], Fraction rhs, int rowscale), np matrix)."""
    rows = []
    mat = np.zeros((len(eqs), nv + 1), dtype=np.int64)
    for e, (name, coeffs, rhs) in enumerate(eqs):
        dl = rhs.denominator
        for c in coeffs.values():
            dl = lcm(dl, c.denominator)
        ent = []
        for i, c in coeffs.items():
            ic = c * dl
            assert ic.denominator == 1
            mat[e, i] = int(ic)
            ent.append((i, int(ic)))
        ir = rhs * dl
        assert ir.denominator == 1
        mat[e, nv] = int(ir)
        rows.append((ent, rhs, dl))
    assert np.abs(mat).max() < 2**62
    return rows, mat

def verify_solution(sprows, x):
    """Exact: every (scaled-integer) equation satisfied by rational vector x."""
    dl = 1
    for v in x:
        dl = lcm(dl, v.denominator)
    X = [int(v * dl) for v in x]
    for ent, rhs, sc in sprows:
        s = sum(ic * X[i] for i, ic in ent)
        rr = rhs * sc * dl
        if rr.denominator != 1 or s != int(rr):
            return False
    return True

def verify_kernel_vec(sprows, k):
    dl = 1
    for v in k:
        dl = lcm(dl, v.denominator)
    K = [int(v * dl) for v in k]
    return all(sum(ic * K[i] for i, ic in ent) == 0 for ent, _, _ in sprows)

def exact_affine_solution(eqs, nv, tag):
    """Consistency + exact particular solution + exact kernel basis of eqs.
    mod-p search, exact verification.  Returns dict or {'consistent': False}."""
    sprows, Mint = int_rows(eqs, nv)
    t0 = time.monotonic()
    ref_piv = None
    used, x0s, kerss = [], [], []
    incons_votes = 0
    pi = 0
    batch = 3
    while pi < len(PRIMES):
        for _ in range(batch):
            if pi >= len(PRIMES):
                break
            p = PRIMES[pi]; pi += 1
            R, piv, cons = modp_rref(Mint, nv, p)
            if not cons:
                incons_votes += 1
                log(f"    [modp] p={p}: inconsistent mod p "
                    f"({incons_votes} votes)")
                if incons_votes >= 3:
                    return {"consistent": False, "sprows": sprows,
                            "Mint": Mint}
                continue
            if ref_piv is None:
                ref_piv = piv
            if piv != ref_piv:
                log(f"    [modp] p={p}: pivot mismatch, dropping prime")
                continue
            pivset = set(piv)
            free = [c for c in range(nv) if c not in pivset]
            x0 = np.zeros(nv, dtype=np.int64)
            x0[piv] = R[:, nv]
            kers = []
            for f in free:
                k = np.zeros(nv, dtype=np.int64)
                k[f] = 1
                k[piv] = (-R[:, f]) % p
                kers.append(k)
            used.append(p); x0s.append(x0); kerss.append(kers)
        if not used:
            continue
        x0 = reconstruct_vec(x0s, used)
        if x0 is not None and verify_solution(sprows, x0):
            free = [c for c in range(nv) if c not in set(ref_piv)]
            kernel = []
            ok = True
            for fi in range(len(free)):
                k = reconstruct_vec([ks[fi] for ks in kerss], used)
                if k is None or not verify_kernel_vec(sprows, k):
                    ok = False
                    break
                kernel.append(k)
            if ok:
                log(f"    [exact] particular solution and {len(kernel)} kernel"
                    f" vectors reconstructed from primes {used} and verified"
                    f" EXACTLY against all {len(eqs)} equations"
                    f" ({time.monotonic()-t0:.1f}s)")
                return {"consistent": True, "x0": x0, "kernel": kernel,
                        "pivcols": ref_piv, "free": free, "rank": len(ref_piv),
                        "sprows": sprows, "Mint": Mint, "primes": used}
        batch = max(3, len(used))          # double the prime count and retry
        log(f"    [modp] reconstruction not yet verified with {len(used)} "
            f"primes; adding more")
    raise RuntimeError("rational reconstruction failed with 60 primes")

def exact_transpose_solve(eqs, nv, target, extra_row=None, tag=""):
    """Find exact y (len(eqs)[+0]) with sum_e y_e*coeffs_e[v] = target[v] for
    all v, plus optional extra equation sum_e extra_row[0][e]*y_e = extra_row[1].
    mod-p + CRT + exact verification.  Returns y (list of Fractions)."""
    ne = len(eqs)
    nrow = nv + (1 if extra_row else 0)
    # object dtype: target denominators can exceed int64 after row scaling
    Mint = np.zeros((nrow, ne + 1), dtype=object)
    scales = []
    for v in range(nv):
        dl = target[v].denominator
        scales.append(dl)
        Mint[v, ne] = int(target[v] * dl)
    for e, (_, coeffs, _) in enumerate(eqs):
        for v, c in coeffs.items():
            ic = c * scales[v]
            assert ic.denominator == 1
            Mint[v, e] = int(ic)
    if extra_row:
        coefv, rhsv = extra_row
        dl = rhsv.denominator
        for c in coefv:
            dl = lcm(dl, c.denominator)
        for e in range(ne):
            ic = coefv[e] * dl
            assert ic.denominator == 1
            Mint[nv, e] = int(ic)
        Mint[nv, ne] = int(rhsv * dl)
    ref_piv = None
    used, ys = [], []
    pi = 0
    while pi < len(PRIMES):
        p = PRIMES[pi]; pi += 1
        R, piv, cons = modp_rref(Mint, ne, p)
        if not cons:
            raise RuntimeError(f"transpose system inconsistent mod {p} ({tag})")
        if ref_piv is None:
            ref_piv = piv
        if piv != ref_piv:
            continue
        y = np.zeros(ne, dtype=np.int64)
        y[piv] = R[:, ne]
        used.append(p); ys.append(y)
        if len(used) < 2:
            continue
        cand = reconstruct_vec(ys, used)
        if cand is None:
            continue
        # exact verification
        acc = [F(0)] * nv
        for e, (_, coeffs, _) in enumerate(eqs):
            ye = cand[e]
            if ye == 0:
                continue
            for v, c in coeffs.items():
                acc[v] += ye * c
        if all(acc[v] == target[v] for v in range(nv)):
            if extra_row:
                s = sum(cand[e] * extra_row[0][e] for e in range(ne))
                if s != extra_row[1]:
                    continue
            return cand
    raise RuntimeError(f"transpose reconstruction failed ({tag})")

# ------------------------ exact LP (dual simplex form) ------------------
def simplex_feasibility(exprs, params):
    """Exact feasibility of {t in R^d : const_v + lin_v.t >= 0 for all v}.
    Solves the dual LP  min c^T mu  s.t. L^T mu = 0, sum mu + s = 1, mu,s >= 0
    (10-ish rows only) with Bland's rule, exact Fractions.
    Feasible  <=> optimum 0  -> returns ('FEASIBLE', {param: value}).
    Infeasible <=> optimum < 0 -> returns ('INFEASIBLE', {v: mu_v}, value),
    where sum_v mu_v * expr_v == value < 0 identically (asserted)."""
    nv = len(exprs)
    d = len(params)
    pmap = {p: j for j, p in enumerate(params)}
    consts = [e[0] for e in exprs]
    # columns: 0..nv-1 = mu_v, nv = slack, nv+1..nv+d = artificials, last = rhs
    slackc = nv
    artc = nv + 1
    ncols = nv + 1 + d + 1
    T = []
    for j in range(d):                       # rows j<d :  sum_v L[v][j] mu_v = 0
        row = [F(0)] * ncols
        for v in range(nv):
            cf = exprs[v][1].get(params[j], F(0))
            row[v] = cf
        row[artc + j] = F(1)
        T.append(row)
    row = [F(1)] * nv + [F(1)] + [F(0)] * d + [F(1)]   # sum mu + s = 1
    T.append(row)
    nrows = d + 1
    basis = [artc + j for j in range(d)] + [slackc]
    cost = [consts[v] for v in range(nv)] + [F(0)] * (1 + d)

    def do_pivot(i, e):
        piv = T[i][e]
        T[i] = [x / piv for x in T[i]]
        for ii in range(nrows):
            if ii != i and T[ii][e] != 0:
                f = T[ii][e]
                T[ii] = [a - f * b for a, b in zip(T[ii], T[i])]
        basis[i] = e

    # drive artificials out immediately (all their rows have rhs 0)
    for j in range(d):
        i = basis.index(artc + j) if (artc + j) in basis else None
        if i is None:
            continue
        e = next((c for c in range(nv + 1) if T[i][c] != 0), None)
        assert e is not None, "dependent parameter direction (unexpected)"
        do_pivot(i, e)
    assert all(b <= nv for b in basis)

    it = 0
    while True:
        it += 1
        assert it < 200000, "simplex iteration cap"
        y = [sum(cost[basis[i]] * T[i][c] for i in range(nrows))
             for c in range(ncols)]          # c_B^T * tableau
        enter = None
        basset = set(basis)
        for c in range(nv + 1):              # Bland: min index, no artificials
            if c in basset:
                continue
            if cost[c] - y[c] < 0:
                enter = c
                break
        if enter is None:
            break
        best = None
        for i in range(nrows):
            if T[i][enter] > 0:
                ratio = T[i][-1] / T[i][enter]
                if best is None or ratio < best[0] or \
                   (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        assert best is not None, "unbounded (impossible: sum mu <= 1)"
        do_pivot(best[1], enter)
    val = sum(cost[basis[i]] * T[i][-1] for i in range(nrows))
    if val < 0:
        mu = {}
        for i in range(nrows):
            if basis[i] < nv and T[i][-1] != 0:
                mu[basis[i]] = T[i][-1]
        assert all(x > 0 for x in mu.values())
        tot_c = sum(m * consts[v] for v, m in mu.items())
        assert tot_c == val < 0
        for p in params:                     # identically zero in each param
            assert sum(m * exprs[v][1].get(p, F(0))
                       for v, m in mu.items()) == 0
        return ("INFEASIBLE", mu, val)
    # feasible: recover t from simplex multipliers (art cols track B^{-1})
    cB = [cost[basis[i]] for i in range(nrows)]
    tdual = [sum(cB[i] * T[i][artc + j] for i in range(nrows))
             for j in range(d)]
    for sgn in (-1, 1):
        assign = {params[j]: sgn * tdual[j] for j in range(d)}
        ok = all(exprs[v][0] + sum(cf * assign[q]
                                   for q, cf in exprs[v][1].items()) >= 0
                 for v in range(nv))
        if ok:
            return ("FEASIBLE", assign)
    raise RuntimeError("dual recovery failed exact verification")

def try_integral(exprs, params, assign, sprows_all, grid):
    """Quick lattice probe: integer parameter vectors in a +/-1 box around
    t* (all expr coefficients must be integral so integer t => integral M).
    Returns exact integral point (verified) or None (logs 'untested'/'not
    found')."""
    from math import floor
    nv = len(exprs)
    d = len(params)
    for c0, lin in exprs:
        if c0.denominator != 1 or any(cf.denominator != 1
                                      for cf in lin.values()):
            log("      integrality: parametrization not integral -> untested")
            return None
    if d == 0:
        x = [e[0] for e in exprs]
        log("      integrality: solution unique and INTEGRAL")
        return x
    K = np.zeros((nv, d), dtype=np.int64)
    cvec = np.array([int(e[0]) for e in exprs], dtype=np.int64)
    for v in range(nv):
        for j, p in enumerate(params):
            K[v, j] = int(exprs[v][1].get(p, F(0)))
    base = np.array([floor(assign[p]) for p in params], dtype=np.int64)
    offs = np.array(np.meshgrid(*[[-1, 0, 1, 2]] * d)).reshape(d, -1).T
    cand = base[None, :] + offs                      # (4^d, d) integer grid
    tvec = None
    for lo in range(0, len(cand), 8192):             # chunked: memory bound
        chunk = cand[lo:lo + 8192]
        vals = chunk @ K.T + cvec[None, :]
        feas = np.nonzero(np.all(vals >= 0, axis=1))[0]
        if feas.size:
            tvec = chunk[int(feas[0])]
            break
    if tvec is None:
        log(f"      integrality: no integral point in the {len(cand)}-point "
            f"lattice window around t* (window only; not exhaustive)")
        return None
    x = [F(int(cvec[v]) + int(sum(K[v, j] * tvec[j] for j in range(d))))
         for v in range(nv)]
    assert verify_solution(sprows_all, x)
    assert all(t >= 0 for t in x)
    log(f"      integrality: INTEGRAL feasible point found and exactly "
        f"verified (params {[int(t) for t in tvec]}); nonzero cells:")
    for v in range(nv):
        if x[v] != 0:
            log(f"        M{grid[v]} = {x[v]}")
    return x

# --------------------------- small exact path --------------------------
def run_small(r, zval):
    grid, idx, mom, for_eqs, zc, B1, B2 = build(r)
    eqs = mom + for_eqs + [(("case", zval), {idx[zc]: F(1)}, F(zval))]
    nv = len(grid)
    res = rref(eqs, nv)
    log(f"  CASE Z{zval} [small exact path]: vars={nv}, eqs={len(eqs)}, "
        f"rank={res['rank']}")
    if not res["consistent"]:
        u = res["cert"]
        combo, crhs = verify_combo(eqs, u, nv)
        assert all(c == 0 for c in combo) and crhs == res["badrhs"] != 0
        log(f"    INFEASIBLE (equality stage).  Certificate multipliers "
            f"(nonzero) giving 0 = {crhs}:")
        for e, (name, _, _) in enumerate(eqs):
            if u[e] != 0:
                log(f"      u[{name}] = {u[e]}")
        log(f"    VERIFIED exactly: combined LHS coefficients all 0, "
            f"combined RHS = {crhs} != 0.")
        return {"verdict": "INFEASIBLE (equality stage)", "dim": None}
    dim = nv - res["rank"]
    exprs, free = parametrize(res, nv)
    log(f"    equality system consistent; affine dim = {dim}; "
        f"free vars = {[grid[f] for f in free]}")
    fm = fourier_motzkin(exprs, free)
    if fm[0] == "INFEASIBLE":
        _, cert, c0, _ = fm
        m = [cert.get(v, F(0)) for v in range(nv)]
        assert all(x >= 0 for x in m)
        y = solve_transpose(eqs, nv, m)
        assert y is not None
        combo, crhs = verify_combo(eqs, y, nv)
        assert combo == m and crhs == c0 < 0
        log(f"    INFEASIBLE (inequality stage).  Farkas certificate:")
        log(f"      inequality multipliers m>=0 (nonzero): " +
            ", ".join(f"m[M{grid[v]}]={m[v]}" for v in range(nv) if m[v] != 0))
        log(f"      equation multipliers y (nonzero):")
        for e, (name, _, _) in enumerate(eqs):
            if y[e] != 0:
                log(f"        y[{name}] = {y[e]}")
        log(f"      VERIFIED exactly from original equations: sum_e y_e*LHS_e "
            f"= m componentwise (all {nv} cells), m >= 0, and sum_e y_e*RHS_e "
            f"= {crhs} < 0.  So sum m*M = {crhs} < 0: impossible with M >= 0.")
        return {"verdict": "INFEASIBLE (inequality stage)", "dim": dim}
    _, stages = fm
    assign = backsub(stages)
    x = [exprs[v][0] + sum(c * assign[q] for q, c in exprs[v][1].items())
         for v in range(nv)]
    verify_point(eqs, x, grid)
    log(f"    FEASIBLE.  Exact point (nonzero cells): " +
        ", ".join(f"M{grid[v]}={x[v]}" for v in range(nv) if x[v] != 0))
    log(f"    Point verified against every original equality and M >= 0.")
    return {"verdict": "FEASIBLE", "dim": dim,
            "point": {grid[v]: x[v] for v in range(nv)}}

# ---------------------------- big path ---------------------------------
def run_big(r):
    t_start = time.monotonic()
    grid, idx, mom, for_eqs, zc, B1, B2 = build(r)
    nv = len(grid)
    lams = [lam(r, s) for s in range(r)]
    nonint = [s for s, x in enumerate(lams) if x.denominator != 1]
    log(f"  grid cells = {nv}, moment eqs = {len(mom)}, forced eqs = "
        f"{len(for_eqs)}; lambda non-integral at s in {nonint} "
        f"({'all integral' if not nonint else 'FLAG'})")
    check_hypergeom(r, grid, idx, mom)
    t_build = time.monotonic()
    log(f"  [time] build+hypergeom check: {t_build - t_start:.1f}s")
    E = mom + for_eqs
    sol = exact_affine_solution(E, nv, f"r={r} E")
    t_solve = time.monotonic()
    log(f"  [time] equality solve (moments+forced): {t_solve - t_build:.1f}s")
    results = {}
    if not sol["consistent"]:
        # exact left-null certificate: u with u^T A = 0, u^T rhs = 1
        sprows = sol["sprows"]
        target = [F(0)] * nv
        rhsvec = [rhs for (_, _, rhs) in E]
        u = exact_transpose_solve(E, nv, target, extra_row=(rhsvec, F(1)),
                                  tag="left-null")
        log("  moments+forced system INCONSISTENT over Q.  Exact left-null "
            "certificate u (nonzero entries):")
        for e, (name, _, _) in enumerate(E):
            if u[e] != 0:
                log(f"    u[{name}] = {u[e]}")
        log("  VERIFIED exactly: sum_e u_e*LHS_e = 0 for every cell and "
            "sum_e u_e*RHS_e = 1, so 0 = 1: both cases INFEASIBLE "
            "(equality stage).")
        for zval in (0, 1):
            results[zval] = {"verdict": "INFEASIBLE (equality stage)",
                             "dim": None}
        return results
    x0, kernel = sol["x0"], sol["kernel"]
    d = len(kernel)
    zi = idx[zc]
    kz = [k[zi] for k in kernel]
    log(f"  rank(moments+forced) = {sol['rank']} (certified: {d} exact "
        f"verified kernel vectors + nonzero {sol['rank']}x{sol['rank']} "
        f"minor mod p={sol['primes'][0]}); affine dim = {d}")
    log(f"  kernel z-coordinates (z = M{zc}): {[str(v) for v in kz]}")
    log(f"  particular-solution z value x0[z] = {x0[zi]}")
    z_fixed = all(v == 0 for v in kz)
    if z_fixed:
        log(f"  z is DETERMINED by the equalities alone: z = {x0[zi]}")
    else:
        log(f"  z is NOT determined by the equalities alone.")
    for zval in (0, 1):
        log(f"  CASE Z{zval}: z = {zval}")
        A_all = E + [(("case", zval), {zi: F(1)}, F(zval))]
        sprows_all, _ = int_rows(A_all, nv)
        if z_fixed:
            if x0[zi] == zval:
                exprs = [(x0[v], {i2: kernel[i2][v] for i2 in range(d)
                                  if kernel[i2][v] != 0}) for v in range(nv)]
                params = list(range(d))
                dim_case = d
            else:
                # certificate: y with A_E^T y = e_z, then y on E and -1 on case
                ez = [F(0)] * nv
                ez[zi] = F(1)
                y = exact_transpose_solve(E, nv, ez, tag="z-fixed")
                yr = sum(y[e] * E[e][2] for e in range(len(E)))
                assert yr == x0[zi]
                log(f"    INFEASIBLE (equality stage).  Certificate: "
                    f"multipliers y on moments+forced (nonzero below) and "
                    f"-1 on the case equation give LHS == 0 and RHS = "
                    f"{yr} - {zval} = {yr - zval} != 0.")
                for e, (name, _, _) in enumerate(E):
                    if y[e] != 0:
                        log(f"      y[{name}] = {y[e]}")
                log(f"    VERIFIED exactly: sum_e y_e*LHS_e = e_z "
                    f"componentwise, minus the case row leaves 0; RHS "
                    f"difference = {yr - zval} != 0.")
                results[zval] = {"verdict": "INFEASIBLE (equality stage)",
                                 "dim": None}
                continue
        else:
            i_star = next(i for i in range(d) if kz[i] != 0)
            others = [i for i in range(d) if i != i_star]
            # t_{i*} = (zval - x0z - sum_{i in others} kz_i t_i)/kz_{i*}
            c_star = (F(zval) - x0[zi]) / kz[i_star]
            lin_star = {i2: -kz[i2] / kz[i_star] for i2 in others}
            exprs = []
            for v in range(nv):
                const = x0[v] + kernel[i_star][v] * c_star
                lin = {}
                for i2 in others:
                    cf = kernel[i2][v] + kernel[i_star][v] * lin_star.get(i2, F(0))
                    if cf != 0:
                        lin[i2] = cf
                exprs.append((const, lin))
            params = others
            dim_case = d - 1
        log(f"    affine dim within case = {dim_case}")
        t_fm0 = time.monotonic()
        assign_override = None
        if dim_case > 6:
            sx = simplex_feasibility(exprs, list(params))
            method = "exact simplex (Bland)"
            if sx[0] == "INFEASIBLE":
                fm = ("INFEASIBLE", sx[1], sx[2], None)
            else:
                fm = ("FEASIBLE", None)
                assign_override = sx[1]
        else:
            fm = fourier_motzkin(exprs, list(params))
            method = "exact Fourier-Motzkin"
            assign_override = None
        t_fm = time.monotonic() - t_fm0
        log(f"    decision method: {method} ({t_fm:.1f}s)")
        if fm[0] == "INFEASIBLE":
            cert, c0 = fm[1], fm[2]
            m = [cert.get(v, F(0)) for v in range(nv)]
            assert all(x >= 0 for x in m)
            y = exact_transpose_solve(A_all, nv, m, tag=f"farkas Z{zval}")
            crhs = sum(y[e] * A_all[e][2] for e in range(len(A_all)))
            assert crhs == c0 < 0
            log(f"    INFEASIBLE (inequality stage).  [FM {t_fm:.1f}s]  "
                f"Farkas certificate:")
            log(f"      inequality multipliers m >= 0 (nonzero): " +
                ", ".join(f"m[M{grid[v]}]={m[v]}"
                          for v in range(nv) if m[v] != 0))
            log(f"      equation multipliers y (nonzero):")
            for e, (name, _, _) in enumerate(A_all):
                if y[e] != 0:
                    log(f"        y[{name}] = {y[e]}")
            log(f"      VERIFIED exactly against the original system: "
                f"sum_e y_e*LHS_e = m componentwise (all {nv} cells, checked "
                f"in the transpose solve), m >= 0, sum_e y_e*RHS_e = {crhs} "
                f"< 0.  Hence sum_v m_v*M_v = {crhs} < 0: impossible with "
                f"M >= 0.")
            results[zval] = {"verdict": "INFEASIBLE (inequality stage)",
                             "dim": dim_case}
        else:
            if assign_override is not None:
                assign = assign_override
            else:
                assign = backsub(fm[1])
            x = [exprs[v][0] + sum(c * assign[q]
                                   for q, c in exprs[v][1].items())
                 for v in range(nv)]
            assert verify_solution(sprows_all, x)
            assert all(t >= 0 for t in x)
            log(f"    FEASIBLE.  Exact point verified against ALL original "
                f"equations (moments, forced, case) and M >= 0: VERIFIED.")
            log(f"      parameter values t*: "
                f"{[(q, str(assign[q])) for q in sorted(assign)]}")
            binding = [grid[v] for v in range(nv) if x[v] == 0]
            log(f"      binding (zero) cells ({len(binding)}): {binding}")
            log(f"      nonzero cells ({sum(1 for t in x if t != 0)}):")
            for v in range(nv):
                if x[v] != 0:
                    log(f"        M{grid[v]} = {x[v]}")
            xi = try_integral(exprs, params, assign, sprows_all, grid)
            results[zval] = {"verdict": "FEASIBLE", "dim": dim_case,
                             "point": x, "integral": xi}
        flush_results()
    return results

# ------------------------------- main ----------------------------------
def main():
    summary = {}
    t0 = time.monotonic()
    log("=" * 78)
    log("r = 5  (S(4,5,11) ambient; machinery control)")
    lams5 = [lam(5, s) for s in range(5)]
    log(f"  lambda_s: {[str(x) for x in lams5]}")
    r5 = {z: run_small(5, z) for z in (0, 1)}
    summary[5] = r5
    if not r5[0]["verdict"].startswith("INFEASIBLE"):
        log("!!! CONTROL FAILURE: r=5 CASE Z0 must be INFEASIBLE.  STOPPING.")
        flush_results()
        return 1
    log(f"  CONTROL r=5 (Z0 INFEASIBLE): PASS")
    log(f"  [time] r=5 small path: {time.monotonic()-t0:.1f}s")
    flush_results()

    log("=" * 78)
    log("r = 5  cross-check through the big (mod-p accelerated) path")
    t1 = time.monotonic()
    r5big = run_big(5)
    for z in (0, 1):
        if r5big[z]["verdict"].split(" ")[0] != r5[z]["verdict"].split(" ")[0]:
            log(f"!!! CONTROL FAILURE: big-path r=5 Z{z} verdict "
                f"{r5big[z]['verdict']} != small-path {r5[z]['verdict']}. "
                f"STOPPING.")
            flush_results()
            return 1
    log(f"  CONTROL r=5 big-path agreement: PASS")
    log(f"  [time] r=5 big path: {time.monotonic()-t1:.1f}s")
    flush_results()

    log("=" * 78)
    log("r = 15  (main event)")
    t2 = time.monotonic()
    lams15 = [lam(15, s) for s in range(15)]
    log(f"  lambda_s: {[str(x) for x in lams15]}")
    summary[15] = run_big(15)
    log(f"  [time] r=15 total: {time.monotonic()-t2:.1f}s")
    flush_results()

    log("=" * 78)
    log("r = 9")
    t3 = time.monotonic()
    lams9 = [lam(9, s) for s in range(9)]
    log(f"  lambda_s: {[str(x) for x in lams9]}")
    summary[9] = run_big(9)
    log(f"  [time] r=9 total: {time.monotonic()-t3:.1f}s")
    flush_results()

    log("=" * 78)
    log("SUMMARY (ambient 4-cell system)")
    log(f"{'r':>3} {'Z0 verdict':>36} {'Z1 verdict':>36}")
    for r in sorted(summary):
        log(f"{r:>3} {summary[r][0]['verdict']:>36} "
            f"{summary[r][1]['verdict']:>36}")
    flush_results()
    return 0

if __name__ == "__main__":
    sys.exit(main())
