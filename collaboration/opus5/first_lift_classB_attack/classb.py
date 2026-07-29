#!/usr/bin/env python3
"""Class-B first-lift completion at n = 13, q = 17: exact core library.

INSTANCE.  A is an n-set (n odd), C a q-set with q = n+4.  Each a in A gets a
5-set S_a subset C ("forbidden" / missing colours).  Write

    m_c = #{a : c in S_a},     V_c = {a : c not in S_a},   |V_c| = n - m_c.

  class A : row sums 5 and every |V_c| even  (equivalently every m_c odd).
  class B : class A and m_c <= 5 for every c (equivalently |V_c| >= n-5).
  class B': class B and, in addition, the instance is the local shape induced
            by a simultaneous fan at one 5-set: there is a decomposition of the
            bipartite "forbidden" graph into five A-saturating matchings f_x
            whose missed 4-sets D_x = C \\ im(f_x) are the vertex palettes of a
            proper edge colouring of K_5.
  class C : fan-realisable; strictly inside class B'; not sampled here.

  These are NOT identified anywhere.  Only class B' is equivalent to extending
  a proper 17-edge-colouring of K_18 - E(K_13) that saturates the five
  vertices outside the hole.

COMPLETION.  E(K_A) partitions into perfect matchings M_c on V_c.
Equivalently (Section 2 of NOTE.md) a proper edge colouring h of K_A with
h(ab) in C \\ (S_a u S_b); the "M_c is *perfect* on V_c" part is then free.

Everything that is claimed as proved is either an exhaustive search that ran
to completion, an exact rational computation, or an explicit certificate that
is re-checked from the definition.  A node budget or a time limit is never
used as evidence of infeasibility.
"""

from __future__ import annotations

import itertools
import random
from collections import Counter
from fractions import Fraction


# ---------------------------------------------------------------------------
# instance arithmetic
# ---------------------------------------------------------------------------
def supports(n, q, forb):
    return [n - sum((forb[a] >> c) & 1 for a in range(n)) for c in range(q)]


def mvec(n, q, forb):
    return [sum((forb[a] >> c) & 1 for a in range(n)) for c in range(q)]


def check_class_B(n, q, forb):
    """Assert the defining arithmetic of a class-B instance; return |V_c|."""
    assert q == n + 4 and n % 2 == 1
    for a in range(n):
        assert forb[a] < (1 << q)
        assert bin(forb[a]).count("1") == 5, ("row sum != 5", a)
    m = mvec(n, q, forb)
    assert sum(m) == 5 * n
    for c in range(q):
        assert m[c] % 2 == 1, ("m_c even", c, m[c])
        assert m[c] <= 5, ("m_c > 5", c, m[c])
    return [n - x for x in m]


def profile(n, q, forb):
    return tuple(sorted(Counter(mvec(n, q, forb)).items()))


def m_profiles(n):
    """(n5,n3,n1) with 5n5+3n3+n1 = 5n and n5+n3+n1 = n+4."""
    q = n + 4
    out = []
    for a in range(q + 1):
        for b in range(q + 1 - a):
            c = q - a - b
            if 5 * a + 3 * b + c == 5 * n:
                out.append((a, b, c))
    return out


# ---------------------------------------------------------------------------
# the two cut conditions (Lemma 1 of results/first_lift_k13_hole/NOTE.md)
# ---------------------------------------------------------------------------
def cut_certificates(n, q, forb, only_first=False):
    Vmask = []
    half = []
    for c in range(q):
        mask = 0
        for a in range(n):
            if not ((forb[a] >> c) & 1):
                mask |= 1 << a
        Vmask.append(mask)
        half.append(bin(mask).count("1") // 2)
    out = []
    for xm in range(1, 1 << n):
        r = bin(xm).count("1")
        cap = r * (r - 1) // 2
        lo = hi = 0
        for c in range(q):
            s = bin(Vmask[c] & xm).count("1")
            if s > half[c]:
                lo += s - half[c]
            hi += s >> 1
        if lo > cap:
            out.append(("forced", tuple(i for i in range(n) if (xm >> i) & 1), lo, cap))
            if only_first:
                return out
        if hi < cap:
            out.append(("capacity", tuple(i for i in range(n) if (xm >> i) & 1), hi, cap))
            if only_first:
                return out
    return out


# ---------------------------------------------------------------------------
# exact DFS solver.  Complete: 'UNSAT' means the whole tree was searched.
# ---------------------------------------------------------------------------
def solve_dfs(n, q, forb, node_budget=None, want_all=False, cap=1):
    """Complete depth-first search with unit propagation on both
    (edge -> colour) and (vertex,colour -> partner) views.

    Returns (status, solutions, nodes).  status in {'SAT','UNSAT','BUDGET'}.
    A solution is a dict {(a,b): c} with a < b.
    """
    FULL = (1 << q) - 1
    avail = [FULL & ~forb[a] for a in range(n)]
    for a in range(n):
        if bin(avail[a]).count("1") != n - 1:
            raise ValueError("bad palette size at %d" % a)
    # open[a] = bitmask of b with edge ab still unassigned
    open_ = [((1 << n) - 1) ^ (1 << a) for a in range(n)]
    assign = {}
    sols = []
    nodes = [0]

    def rec():
        nodes[0] += 1
        if node_budget is not None and nodes[0] > node_budget:
            raise TimeoutError
        # ---- unit propagation -------------------------------------------
        undo = []
        try:
            while True:
                forced = None
                # edges with a unique candidate colour, and dead edges
                best = None
                for a in range(n):
                    om = open_[a]
                    while om:
                        lb = om & -om
                        om ^= lb
                        b = lb.bit_length() - 1
                        if b < a:
                            continue
                        m = avail[a] & avail[b]
                        if m == 0:
                            return False
                        cnt = bin(m).count("1")
                        if cnt == 1:
                            forced = ('e', a, b, m.bit_length() - 1)
                            break
                        if best is None or cnt < best[0]:
                            best = (cnt, 'e', (a, b, m))
                    if forced:
                        break
                if forced is None:
                    # (vertex,colour) with a unique possible partner, or none
                    for a in range(n):
                        m = avail[a]
                        while m:
                            lb = m & -m
                            m ^= lb
                            c = lb.bit_length() - 1
                            cand = 0
                            om = open_[a]
                            while om:
                                lb2 = om & -om
                                om ^= lb2
                                b = lb2.bit_length() - 1
                                if (avail[b] >> c) & 1:
                                    cand |= lb2
                            if cand == 0:
                                return False
                            cnt = bin(cand).count("1")
                            if cnt == 1:
                                forced = ('v', a, cand.bit_length() - 1, c)
                                break
                            if best is None or cnt < best[0]:
                                best = (cnt, 'v', (a, c, cand))
                        if forced:
                            break
                if forced is None:
                    break
                _, a, b, c = forced
                lb = 1 << c
                avail[a] ^= lb
                avail[b] ^= lb
                open_[a] &= ~(1 << b)
                open_[b] &= ~(1 << a)
                e = (a, b) if a < b else (b, a)
                assign[e] = c
                undo.append((a, b, c, e))
                best = None
            # ---- all propagated; check completion ------------------------
            if all(open_[a] == 0 for a in range(n)):
                assert all(avail[a] == 0 for a in range(n))
                sols.append(dict(assign))
                return len(sols) >= cap
            assert best is not None
            if best[1] == 'e':
                a, b, m = best[2]
                bits = []
                while m:
                    lb = m & -m
                    bits.append(lb.bit_length() - 1)
                    m ^= lb
                for c in bits:
                    lb = 1 << c
                    avail[a] ^= lb
                    avail[b] ^= lb
                    open_[a] &= ~(1 << b)
                    open_[b] &= ~(1 << a)
                    assign[(a, b)] = c
                    r = rec()
                    del assign[(a, b)]
                    open_[a] |= 1 << b
                    open_[b] |= 1 << a
                    avail[a] ^= lb
                    avail[b] ^= lb
                    if r:
                        return True
                return False
            a, c, cand = best[2]
            lb = 1 << c
            bs = []
            while cand:
                l2 = cand & -cand
                bs.append(l2.bit_length() - 1)
                cand ^= l2
            for b in bs:
                avail[a] ^= lb
                avail[b] ^= lb
                open_[a] &= ~(1 << b)
                open_[b] &= ~(1 << a)
                e = (a, b) if a < b else (b, a)
                assign[e] = c
                r = rec()
                del assign[e]
                open_[a] |= 1 << b
                open_[b] |= 1 << a
                avail[a] ^= lb
                avail[b] ^= lb
                if r:
                    return True
            return False
        finally:
            for (a, b, c, e) in reversed(undo):
                lb = 1 << c
                assign.pop(e, None)
                open_[a] |= 1 << b
                open_[b] |= 1 << a
                avail[a] ^= lb
                avail[b] ^= lb

    try:
        ok = rec()
    except TimeoutError:
        return ("BUDGET", sols, nodes[0])
    if sols:
        return ("SAT", sols, nodes[0])
    return ("UNSAT", [], nodes[0])


def check_completion(n, q, forb, sol):
    """Re-check a claimed completion straight from the definition."""
    FULL = (1 << q) - 1
    assert len(sol) == n * (n - 1) // 2, ("edge count", len(sol))
    used = [0] * n
    for (a, b), c in sol.items():
        assert 0 <= a < b < n and 0 <= c < q
        assert not ((forb[a] >> c) & 1) and not ((forb[b] >> c) & 1), "forbidden colour"
        assert not ((used[a] >> c) & 1) and not ((used[b] >> c) & 1), "repeated colour"
        used[a] |= 1 << c
        used[b] |= 1 << c
    for a in range(n):
        assert used[a] == FULL & ~forb[a], ("palette not exhausted", a)
    # and the matching supports really are V_c
    for c in range(q):
        cov = sorted([a for e, cc in sol.items() if cc == c for a in e])
        want = sorted(a for a in range(n) if not ((forb[a] >> c) & 1))
        assert cov == want, ("support", c)
    return True


# ---------------------------------------------------------------------------
# SAT encoding (independent second solver)
# ---------------------------------------------------------------------------
def sat_clauses(n, q, forb):
    """CNF for the completion problem.  Returns (clauses, var, edges)."""
    var = {}
    edges = [(a, b) for a in range(n) for b in range(a + 1, n)]
    for (a, b) in edges:
        for c in range(q):
            if not ((forb[a] >> c) & 1) and not ((forb[b] >> c) & 1):
                var[(a, b, c)] = len(var) + 1
    cls = []
    for (a, b) in edges:
        lits = [var[(a, b, c)] for c in range(q) if (a, b, c) in var]
        cls.append(lits)
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                cls.append([-lits[i], -lits[j]])
    for a in range(n):
        for c in range(q):
            if (forb[a] >> c) & 1:
                continue
            lits = []
            for b in range(n):
                if b == a:
                    continue
                e = (a, b, c) if a < b else (b, a, c)
                if e in var:
                    lits.append(var[e])
            cls.append(lits)
            for i in range(len(lits)):
                for j in range(i + 1, len(lits)):
                    cls.append([-lits[i], -lits[j]])
    return cls, var, edges


def solve_sat(n, q, forb, solver_name="cadical153"):
    """Independent exact decision via a CDCL SAT solver.  Returns
    ('SAT', sol) or ('UNSAT', None)."""
    from pysat.solvers import Solver
    cls, var, edges = sat_clauses(n, q, forb)
    with Solver(name=solver_name, bootstrap_with=cls) as s:
        if not s.solve():
            return ("UNSAT", None)
        model = set(l for l in s.get_model() if l > 0)
    sol = {}
    for (a, b, c), v in var.items():
        if v in model:
            sol[(a, b)] = c
    return ("SAT", sol)


def count_sat(n, q, forb, cap=1000, solver_name="cadical153"):
    """Count completions up to `cap` by blocking clauses.  Returns
    (count, exhausted) where exhausted is True iff the count is exact."""
    from pysat.solvers import Solver
    cls, var, edges = sat_clauses(n, q, forb)
    cnt = 0
    with Solver(name=solver_name, bootstrap_with=cls) as s:
        while cnt < cap and s.solve():
            model = set(l for l in s.get_model() if l > 0)
            block = [-v for v in var.values() if v in model]
            s.add_clause(block)
            cnt += 1
        else:
            exhausted = (cnt < cap)
    return cnt, exhausted


# ---------------------------------------------------------------------------
# exact rational LP feasibility of the fractional relaxation
# ---------------------------------------------------------------------------
def lp_feasible(n, q, forb):
    """Exact (rational) feasibility of

        x_{e,c} >= 0,  sum_c x_{e,c} = 1 (all e),
        sum_{b} x_{ab,c} = 1 for every c and every a in V_c,
        x_{e,c} = 0 unless e is inside V_c.

    Infeasibility is a rigorous proof that no completion exists.  Returns
    (True, None) or (False, farkas_certificate).
    Phase-I simplex in exact arithmetic (Bland's rule, so it terminates).
    """
    edges = [(a, b) for a in range(n) for b in range(a + 1, n)]
    V = [[a for a in range(n) if not ((forb[a] >> c) & 1)] for c in range(q)]
    inV = [[not ((forb[a] >> c) & 1) for a in range(n)] for c in range(q)]
    cols = []          # variable index -> (edge index, colour)
    for ei, (a, b) in enumerate(edges):
        for c in range(q):
            if inV[c][a] and inV[c][b]:
                cols.append((ei, c))
    rows = []          # constraint list, each (dict var->coef, rhs)
    rowid = {}
    for ei in range(len(edges)):
        rowid[('e', ei)] = len(rows)
        rows.append(({}, 1))
    for c in range(q):
        for a in V[c]:
            rowid[('v', c, a)] = len(rows)
            rows.append(({}, 1))
    for j, (ei, c) in enumerate(cols):
        a, b = edges[ei]
        rows[rowid[('e', ei)]][0][j] = 1
        rows[rowid[('v', c, a)]][0][j] = 1
        rows[rowid[('v', c, b)]][0][j] = 1
    return _phase1(len(cols), rows)


def _phase1(nvar, rows):
    """Phase-I simplex, exact rationals, Bland's rule.  rows: list of
    (dict var->coef, rhs>=0).  Returns (feasible, farkas_or_None)."""
    m = len(rows)
    N = nvar + m
    T = [[Fraction(0)] * (N + 1) for _ in range(m)]
    for i, (d, rhs) in enumerate(rows):
        for j, v in d.items():
            T[i][j] = Fraction(v)
        T[i][nvar + i] = Fraction(1)
        T[i][N] = Fraction(rhs)
    basis = [nvar + i for i in range(m)]
    # objective: minimise sum of artificials -> cost row = -sum of rows
    obj = [Fraction(0)] * (N + 1)
    for i in range(m):
        for j in range(N + 1):
            obj[j] -= T[i][j]
    for i in range(m):
        obj[nvar + i] = Fraction(0)
    while True:
        piv = -1
        for j in range(N):
            if obj[j] < 0:
                piv = j
                break
        if piv < 0:
            break
        best = -1
        bratio = None
        for i in range(m):
            if T[i][piv] > 0:
                r = T[i][N] / T[i][piv]
                if bratio is None or r < bratio or (r == bratio and basis[i] < basis[best]):
                    bratio, best = r, i
        if best < 0:
            raise RuntimeError("phase-I unbounded: impossible")
        p = T[best][piv]
        T[best] = [x / p for x in T[best]]
        for i in range(m):
            if i != best and T[i][piv] != 0:
                f = T[i][piv]
                T[i] = [x - f * y for x, y in zip(T[i], T[best])]
        if obj[piv] != 0:
            f = obj[piv]
            obj = [x - f * y for x, y in zip(obj, T[best])]
        basis[best] = piv
    val = -obj[N]
    if val == 0:
        x = [Fraction(0)] * nvar
        for i in range(m):
            if basis[i] < nvar:
                x[basis[i]] = T[i][N]
        return (True, x)
    # Farkas certificate: y with y^T A <= 0 on all columns and y^T b > 0.
    # At the phase-I optimum the reduced cost of artificial i is 1 - y_i.
    y = [1 - obj[nvar + i] for i in range(m)]
    return (False, y)


def lp_columns(n, q, forb):
    """The (edge, colour) pairs indexing the LP variables, in the order used
    by lp_feasible, together with the constraint-row index map."""
    edges = [(a, b) for a in range(n) for b in range(a + 1, n)]
    inV = [[not ((forb[a] >> c) & 1) for a in range(n)] for c in range(q)]
    V = [[a for a in range(n) if inV[c][a]] for c in range(q)]
    cols = []
    for ei, (a, b) in enumerate(edges):
        for c in range(q):
            if inV[c][a] and inV[c][b]:
                cols.append((ei, c))
    idx = {}
    k = 0
    for ei in range(len(edges)):
        idx[('e', ei)] = k
        k += 1
    for c in range(q):
        for a in V[c]:
            idx[('v', c, a)] = k
            k += 1
    return edges, cols, idx, k


def check_lp_point(n, q, forb, x):
    """Re-check an exact rational feasible point of the fractional relaxation.
    Proves LP feasibility (so no Farkas certificate can exist)."""
    edges, cols, idx, k = lp_columns(n, q, forb)
    assert len(x) == len(cols), (len(x), len(cols))
    x = [Fraction(t) for t in x]
    acc = [Fraction(0)] * k
    for j, (ei, c) in enumerate(cols):
        if x[j] < 0:
            return False
        a, b = edges[ei]
        acc[idx[('e', ei)]] += x[j]
        acc[idx[('v', c, a)]] += x[j]
        acc[idx[('v', c, b)]] += x[j]
    return all(t == 1 for t in acc)


def check_farkas(n, q, forb, y):
    """Re-check a Farkas certificate from the definition: y^T b > 0 while
    y^T A_j <= 0 for every column j.  Proves LP infeasibility."""
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
    assert len(y) == k
    y = [Fraction(t) for t in y]
    rhs = sum(y)                       # all b_i are 1
    if rhs <= 0:
        return False
    for ei, (a, b) in enumerate(edges):
        for c in range(q):
            if inV[c][a] and inV[c][b]:
                s = y[idx[('e', ei)]] + y[idx[('v', c, a)]] + y[idx[('v', c, b)]]
                if s > 0:
                    return False
    return True


# ---------------------------------------------------------------------------
# class-B instance generation
# ---------------------------------------------------------------------------
def random_class_B(n, q, rng, prof=None):
    """Uniform-ish random class-B instance: pick a target m-profile, then find
    a 0/1 matrix with the prescribed row sums (5) and column sums m_c by
    randomised bipartite-degree realisation.  Returns forb or None."""
    profs = m_profiles(n)
    if prof is None:
        prof = rng.choice(profs)
    n5, n3, n1 = prof
    ms = [5] * n5 + [3] * n3 + [1] * n1
    rng.shuffle(ms)
    for _ in range(80):
        forb = [0] * n
        rem = ms[:]
        rowrem = [5] * n
        order = sorted(range(q), key=lambda c: -rem[c])
        ok = True
        for c in order:
            cand = [a for a in range(n) if rowrem[a] > 0]
            if len(cand) < rem[c]:
                ok = False
                break
            cand.sort(key=lambda a: (-rowrem[a], rng.random()))
            k = rem[c]
            # randomised choice biased to the largest remaining row capacity
            pool = cand[:]
            rng.shuffle(pool)
            pool.sort(key=lambda a: -rowrem[a])
            pick = pool[:k]
            for a in pick:
                forb[a] |= 1 << c
                rowrem[a] -= 1
        if ok and all(r == 0 for r in rowrem):
            return forb
    return None


def rand_class_B_swap(n, q, rng, steps=400, prof=None):
    """Random class-B instance obtained by starting from a canonical one and
    performing `steps` random class-B preserving moves."""
    forb = random_class_B(n, q, rng, prof)
    if forb is None:
        return None
    for _ in range(steps):
        forb = random_move(n, q, forb, rng) or forb
    return forb


def random_move(n, q, forb, rng, allow_profile_change=True):
    """One random class-B preserving perturbation.

    (i) transposition: a gives up c and takes c', a' gives up c' and takes c;
        every m stays the same.
    (ii) profile move: two vertices both give up c' and both take c;
        m_c += 2, m_c' -= 2 (kept odd and inside [1,5]).
    """
    for _ in range(60):
        if allow_profile_change and rng.random() < 0.35:
            a, b = rng.sample(range(n), 2)
            both_in = [c for c in range(q) if (forb[a] >> c) & 1 and (forb[b] >> c) & 1]
            both_out = [c for c in range(q)
                        if not ((forb[a] >> c) & 1) and not ((forb[b] >> c) & 1)]
            if not both_in or not both_out:
                continue
            cp = rng.choice(both_in)
            c = rng.choice(both_out)
            m = mvec(n, q, forb)
            if m[c] + 2 > 5 or m[cp] - 2 < 1:
                continue
            new = list(forb)
            new[a] = (new[a] & ~(1 << cp)) | (1 << c)
            new[b] = (new[b] & ~(1 << cp)) | (1 << c)
            return new
        a, b = rng.sample(range(n), 2)
        ca = [c for c in range(q) if (forb[a] >> c) & 1 and not ((forb[b] >> c) & 1)]
        cb = [c for c in range(q) if (forb[b] >> c) & 1 and not ((forb[a] >> c) & 1)]
        if not ca or not cb:
            continue
        c = rng.choice(ca)
        cp = rng.choice(cb)
        new = list(forb)
        new[a] = (new[a] & ~(1 << c)) | (1 << cp)
        new[b] = (new[b] & ~(1 << cp)) | (1 << c)
        return new
    return None
