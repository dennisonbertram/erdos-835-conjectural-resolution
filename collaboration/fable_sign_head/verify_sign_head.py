#!/usr/bin/env python3
"""Deterministic stdlib verifier for the radius-5 sign head programme.

Companion to sign_head_note.md (same directory).  Pure stdlib.  Every part
stops at its first failed assertion.

Parts:
  A  machine-check of the assembly behind identity (H)
       A0  sign of a partial injection == parity of misordered cell pairs
       A1  cofactor lemma (C) and the deletion rule (brief re-verification)
       A2  shape-level identities (8), (9), (10), (6) on random Latin squares
           of even orders 4, 6, 8 with designated dummy lines m, l, *
       A3  the genuine k = 2 radius-5 structure, end to end:
           H, E, Sigma(Q), AT(Q), (10), (6), (7), (1), and (H) itself
  B  independent Wallis k = 16 recomputation: E (exact negative-pair count),
     RHS(F), required H
  C  complete labelled k = 6 radius-3 census: all discordant families, all
     root colours; E / RHS(F) / required-H distributions; per-uv (condition 4)
     feasibility;  k = 4 impossibility recheck
  D  the two butterfly regroupings of H (per-(u,i,{v,v'}) and
     per-(i,x,{j,j'})) agree with the per-flag inversion count on random
     tables
  E  re-verification of the stored falsification instances (written by
     gen_tables.py): constraint check + independent recomputation of the
     relaxed invariant Hhat on every stored table

Conventions (identical to collaboration/claude/audit_formula_F.py):
  V = 0..k-1, A = 0..k-2, infinity := k (always last in the colour order C).
  Flag square Q^{i,u}: rows (A\\{i} induced order, then m, then l), columns
  (V\\{u} induced order, then *), symbols C\\{L_i(u)} induced order.
  Sign of a bijection between ordered sets = sign of its permutation matrix.
"""
import json
import random
import sys
from itertools import combinations, permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent


# --------------------------------------------------------------------- basics
def perm_sign(perm):
    s = 1
    for a in range(len(perm)):
        for b in range(a + 1, len(perm)):
            if perm[a] > perm[b]:
                s = -s
    return s


def bij_sign(domain, mapping, target):
    pos = {t: p for p, t in enumerate(target)}
    perm = [pos[mapping[d]] for d in domain]
    assert sorted(perm) == list(range(len(target))), "not a bijection"
    return perm_sign(perm)


def pm_sign(cells):
    """Sign of a partial injection given as cells (r, c): the bijection from
    its hit rows (induced order) to its hit columns (induced order)."""
    cells = sorted(cells)
    rows = [r for r, _ in cells]
    cols = [c for _, c in cells]
    assert len(set(rows)) == len(cells) and len(set(cols)) == len(cells)
    order = sorted(cols)
    return perm_sign([order.index(c) for c in cols])


def inv_count(cells):
    """Misordered pairs of cells: (r-r')(c-c') < 0.  Defined for ANY cell
    set (rows or columns may repeat; equal coordinates contribute 0)."""
    n = 0
    cs = list(cells)
    for a in range(len(cs)):
        ra, ca = cs[a]
        for b in range(a + 1, len(cs)):
            rb, cb = cs[b]
            if (ra - rb) * (ca - cb) < 0:
                n += 1
    return n


def prod(xs):
    p = 1
    for x in xs:
        p *= x
    return p


def random_latin(n, rng):
    """Uniform-ish random Latin square of order n by randomized backtracking."""
    grid = [[None] * n for _ in range(n)]
    colused = [set() for _ in range(n)]

    def rec(r, c):
        if r == n:
            return True
        nr, nc = (r, c + 1) if c + 1 < n else (r + 1, 0)
        cand = [s for s in range(n)
                if s not in grid[r][:c] and s not in colused[c]]
        rng.shuffle(cand)
        for s in cand:
            grid[r][c] = s
            colused[c].add(s)
            if rec(nr, nc):
                return True
            colused[c].discard(s)
        grid[r][c] = None
        return False

    assert rec(0, 0)
    return grid


# ------------------------------------------------------------------- part A0
def part_a0():
    """pm_sign == (-1)^{inv_count} for every partial injection, exhaustively
    on rectangles up to 4x4 and all sizes of partial injections."""
    checked = 0
    for nr in range(1, 5):
        for nc in range(1, 5):
            for t in range(1, min(nr, nc) + 1):
                for rows in combinations(range(nr), t):
                    for cols in permutations(range(nc), t):
                        cells = list(zip(rows, cols))
                        assert pm_sign(cells) == (-1) ** inv_count(cells), \
                            ("A0", cells)
                        checked += 1
    print(f"[A0] sign(partial injection) == (-1)^misordered-pairs: "
          f"{checked} exhaustive instances OK")


# ------------------------------------------------------------------- part A1
def part_a1():
    rng = random.Random(835)
    nC = nD = 0
    for n in range(4, 9):
        C = list(range(n))
        for a in C:
            for b in C:
                if a == b:
                    continue
                rest = [c for c in C if c not in (a, b)]
                for _ in range(20):
                    img = rest[:]
                    rng.shuffle(img)
                    dom = list(range(n - 2)) + ["*"]
                    fa = {d: img[p] for p, d in enumerate(dom[:-1])}
                    fb = dict(fa)
                    fa["*"] = b
                    fb["*"] = a
                    sa = bij_sign(dom, fa, [c for c in C if c != a])
                    sb = bij_sign(dom, fb, [c for c in C if c != b])
                    assert sa * sb == (-1) ** (a + b + 1), ("A1-C", a, b)
                    nC += 1
        for _ in range(60):
            p = list(range(n))
            rng.shuffle(p)
            s0 = perm_sign(p)
            for r in range(n):
                s = p[r]
                q = [x - (x > s) for t, x in enumerate(p) if t != r]
                assert perm_sign(q) == s0 * (-1) ** (r + s), ("A1-del",)
                nD += 1
    print(f"[A1] lemma (C): {nC} instances OK; deletion rule: {nD} OK")


# ------------------------------------------------------------------- part A2
def flag_shape_checks(Q, n):
    """Q: n x n Latin square, rows 0..n-3 interior + m=n-2, l=n-1; columns
    0..n-2 interior + *=n-1; symbols 0..n-1 (natural order).  Returns
    (AT, Sigma, prod_eps, prod_sgnPhi) after checking (8), (9), (10), (6)."""
    m, ell, star = n - 2, n - 1, n - 1
    u_sym, inf_sym = Q[m][star], Q[ell][star]
    assert u_sym != inf_sym
    colof = [{Q[r][c]: c for c in range(n)} for r in range(n)]
    rowof_star = {Q[r][star]: r for r in range(n)}

    sigma = 1
    prod_eps = 1
    prod_phi = 1
    for x in range(n):
        pfull = [colof[r][x] for r in range(n)]        # row -> column
        s_c = perm_sign(pfull)
        cells = [(r, colof[r][x]) for r in range(n - 2)
                 if colof[r][x] != star]
        s_phi = pm_sign(cells)
        if x == inf_sym:
            w_inf = colof[m][x]
            assert colof[ell][x] == star
            assert s_c == (-1) ** (n - 2 - w_inf) * s_phi, ("(8) inf", x)
        elif x == u_sym:
            v0 = colof[ell][x]
            assert colof[m][x] == star
            assert s_c == (-1) ** (n - 1 - v0) * s_phi, ("(8) u", x)
        else:
            j_x = rowof_star[x]
            vM, vL = colof[m][x], colof[ell][x]
            assert j_x < n - 2 and vM != star and vL != star and vM != vL
            eps = 1 if vM < vL else -1
            assert s_c == (-1) ** (j_x + vM + vL) * eps * s_phi, ("(9)", x)
            prod_eps *= eps
        sigma *= s_c
        prod_phi *= s_phi
    km2 = n - 2
    rhs10 = (-1) ** (km2 * (km2 - 1) // 2 + 1) * prod_eps * prod_phi
    assert sigma == rhs10, ("(10)", sigma, rhs10)
    rows_sgn = prod(perm_sign([Q[r][c] for c in range(n)]) for r in range(n))
    # column sign: map rows -> symbols; symbols in natural order
    cols_sgn = prod(perm_sign([Q[r][c] for r in range(n)]) for c in range(n))
    AT = rows_sgn * cols_sgn
    assert AT * sigma == (-1) ** (n * (n - 1) // 2), ("(6)", AT, sigma)
    return AT, sigma, prod_eps, prod_phi


def part_a2():
    rng = random.Random(20260726)
    total = 0
    for n in (4, 6, 8):
        for _ in range(25):
            Q = random_latin(n, rng)
            flag_shape_checks(Q, n)
            total += 1
    print(f"[A2] shape identities (8), (9), (10), (6): {total} random Latin "
          f"squares of orders 4, 6, 8 OK (all symbols each)")


# ------------------------------------------------------------------- part A3
def part_a3():
    k = 2
    INF = k
    L = [[1, 0]]
    M = {(0, 1): INF}
    # conditions 1-3 for the unique k=2 structure; condition 4 is vacuous
    assert {L[0][u] for u in range(k)} == {1, 0}
    # flag squares
    ATs, Sigmas = [], []
    for u in range(k):
        i = 0
        v = 1 - u
        syms = [c for c in range(k + 1) if c != L[i][u]]
        # rows m, l ; columns v, *
        grid = {("m", v): M[(0, 1)], ("m", "*"): u,
                ("l", v): L[i][v], ("l", "*"): INF}
        rows, cols = ["m", "l"], [v, "*"]
        for r in rows:
            assert sorted(grid[(r, c)] for c in cols) == sorted(syms)
        for c in cols:
            assert sorted(grid[(r, c)] for r in rows) == sorted(syms)
        rs = prod(bij_sign(cols, {c: grid[(r, c)] for c in cols}, syms)
                  for r in rows)
        cs = prod(bij_sign(rows, {r: grid[(r, c)] for r in rows}, syms)
                  for c in cols)
        AT = rs * cs
        # symbol permutation product Sigma
        sig = 1
        for x in syms:
            mp = {r: next(c for c in cols if grid[(r, c)] == x) for r in rows}
            sig *= bij_sign(rows, mp, cols)
        assert AT * sig == (-1) ** (k * (k - 1) // 2), "(6) at k=2"
        ATs.append(AT)
        Sigmas.append(sig)
        # (10) at k=2: no interior rows, all fibers empty, no generic x;
        # fixed factor (-1)^{C(0,2)+1} = -1
        assert sig == (-1) ** (0 + 1) * 1 * 1, "(10) at k=2"
    # H and E from the definitions: empty products
    H = 1
    E = 1
    n_generic = sum(1 for u in range(k)
                    for x in range(k) if x not in (u, L[0][u]))
    assert n_generic == 0
    # RHS(F)
    T = {(0, 0): 1, (0, 1): 0, ("e", 0): 0, ("e", 1): 1}
    Trows = [0, "e"]
    ATT = prod(bij_sign([0, 1], {u: T[(r, u)] for u in (0, 1)}, [0, 1])
               for r in Trows) * \
        prod(bij_sign(Trows, {r: T[(r, u)] for r in Trows}, [0, 1])
             for u in (0, 1))
    S = {(0, 0): 0, (1, 1): 1, (0, 1): INF, (1, 0): INF,
         (0, INF): 1, (INF, 0): 1, (1, INF): 0, (INF, 1): 0,
         (INF, INF): INF}
    dS = prod(bij_sign(range(k + 1), {y: S[(q, y)] for y in range(k + 1)},
                       range(k + 1)) for q in range(k + 1))
    RHS = (-1) ** (k * (k - 1) // 2) * ATT * dS
    assert prod(Sigmas) == prod(ATs), "(7) at k=2"
    assert prod(ATs) == RHS, "(1) at k=2"
    assert prod(Sigmas) == E * H, "Sigma-product == E*H at k=2"
    assert H == E * RHS, "(H) at k=2"
    print(f"[A3] genuine k=2 end-to-end: AT(Q)={ATs}, Sigma(Q)={Sigmas}, "
          f"AT(T)={ATT}, delta(S)={dS}, E={E}, H={H}, RHS(F)={RHS}; "
          f"(6),(7),(1),(10),(H) all hold")


# ------------------------------------------------ chart utilities (any k)
def chart_from_sils(F, n, infp):
    """F: list of k-1 symmetric idempotent LS of order n = k+1 given as
    dicts on ordered pairs (x<y); infp: distinguished root colour.
    Returns (L, M, V) in CANONICAL labels 0..k-1 with infinity = k,
    where canonical labels sort the non-root colours increasingly."""
    k = n - 1
    Vraw = [c for c in range(n) if c != infp]
    lab = {c: t for t, c in enumerate(Vraw)}
    lab[infp] = k

    def ent(S, a, b):
        return S[(min(a, b), max(a, b))]

    L = [[None] * k for _ in F]
    M = [[[None] * k for _ in range(k)] for _ in F]
    for i, S in enumerate(F):
        for u in Vraw:
            L[i][lab[u]] = lab[ent(S, infp, u)]
            for v in Vraw:
                if v != u:
                    M[i][lab[u]][lab[v]] = lab[ent(S, u, v)]
    return L, M


def check_conditions_123(L, M, k):
    C = set(range(k + 1))
    for u in range(k):
        assert {L[i][u] for i in range(k - 1)} == set(range(k)) - {u}
    for i in range(k - 1):
        assert sorted(L[i]) == list(range(k))
        assert all(L[i][u] != u for u in range(k))
        for u in range(k):
            pal = {M[i][u][v] for v in range(k) if v != u}
            assert pal == C - {u, L[i][u]}
    for u in range(k):
        for v in range(u + 1, k):
            assert {M[i][u][v] for i in range(k - 1)} == C - {u, v}


def E_of_chart(L, M, k):
    """E(L,M) and the exact count of negative generic hole pairs."""
    neg = tot = 0
    for i in range(k - 1):
        Linv = [None] * (k + 1)
        for u in range(k):
            Linv[L[i][u]] = u
        mate = [[None] * (k + 1) for _ in range(k)]
        for u in range(k):
            for v in range(k):
                if v != u:
                    mate[u][M[i][u][v]] = v
        for u in range(k):
            for x in range(k):
                if x == u or x == L[i][u]:
                    continue
                vM, vL = mate[u][x], Linv[x]
                assert vM is not None and vL is not None
                assert vM != vL and vM != u and vL != u
                tot += 1
                if vM > vL:
                    neg += 1
    return (-1) ** neg, neg, tot


def RHS_of_chart(L, M, k):
    """(-1)^{k(k-1)/2} AT(T) prod_i delta(S_i), plus the pieces."""
    V = list(range(k))
    Trows = list(range(k - 1)) + ["e"]

    def Tval(r, u):
        return u if r == "e" else L[r][u]

    RT = prod(bij_sign(V, {u: Tval(r, u) for u in V}, V) for r in Trows)
    CT = prod(bij_sign(Trows, {r: Tval(r, u) for r in Trows}, V)
              for u in V)
    deltas = []
    Call = list(range(k + 1))
    for i in range(k - 1):
        d = 1
        for q in range(k + 1):
            if q == k:
                mp = {y: (L[i][y] if y < k else k) for y in Call}
            else:
                mp = {y: (q if y == q else (L[i][q] if y == k
                                            else M[i][q][y])) for y in Call}
            d *= bij_sign(Call, mp, Call)
        deltas.append(d)
    rhs = (-1) ** (k * (k - 1) // 2) * RT * CT * prod(deltas)
    return rhs, RT, CT, deltas


# ------------------------------------------------------------------- part B
FIRST_HALF_COLUMNS = (
    tuple(range(2, 17)),
    (5, 1, 7, 8, 9, 16, 14, 4, 13, 15, 10, 6, 11, 3, 12),
    (9, 10, 12, 2, 15, 13, 16, 14, 4, 7, 5, 8, 1, 11, 6),
    (14, 12, 2, 13, 3, 8, 9, 16, 7, 5, 1, 15, 6, 10, 11),
    (16, 11, 13, 15, 1, 3, 6, 10, 2, 14, 4, 7, 8, 12, 9),
    (13, 15, 16, 1, 14, 11, 4, 7, 12, 8, 9, 3, 10, 5, 2),
    (15, 4, 1, 14, 11, 2, 10, 3, 5, 6, 13, 16, 12, 9, 8),
    (12, 13, 14, 11, 10, 9, 2, 6, 16, 3, 15, 1, 7, 4, 5),
)


def wallis_sils():
    Q = 17
    out = []
    for sq in range(15):
        a = [0] + [FIRST_HALF_COLUMNS[j - 1][sq] for j in range(1, 9)]
        a.extend([-1] * 8)
        for j in range(9, 17):
            a[j] = (a[17 - j] + j) % Q
        assert sorted(a) == list(range(Q))
        Mch = set()
        for d in range(1, Q):
            y = (-a[d]) % Q
            x = (y + d) % Q
            if x != y:
                Mch.add(frozenset((x, y)))
        S = {}
        for c in range(Q):
            for e in Mch:
                x, y = tuple(e)
                p, q = sorted(((x + c) % Q, (y + c) % Q))
                S[(p, q)] = c
        out.append(S)
    return out


def part_b():
    k = 16
    F = wallis_sils()
    L, M = chart_from_sils(F, 17, 16)
    check_conditions_123(L, M, k)
    E, neg, tot = E_of_chart(L, M, k)
    rhs, RT, CT, deltas = RHS_of_chart(L, M, k)
    reqH = E * rhs
    print(f"[B] Wallis k=16: generic hole pairs = {tot}, negative = {neg}, "
          f"E = {E}")
    print(f"[B] R(T)={RT}, C(T)={CT}, AT(T)={RT*CT}, deltas={deltas}, "
          f"prod delta={prod(deltas)}, RHS(F)={rhs}, required H = {reqH}")
    assert tot == 3360 and neg == 1680 and E == 1
    assert rhs == 1 and reqH == 1
    return L, M


# ------------------------------------------------------------------ part B2
def E_lemma_steps(L, M, k):
    """Machine-check of every step of the E-lemma proof (E(L,M) = +1 for all
    even k, conditions 1-2 only):
      step 1 (sweep): for fixed i, x, v = L_i^{-1}(x), the mate involution of
        the x-class of M_i sweeps V\\{x,v}, so
        prod_{u in V\\{x,v}} eps(mate_x(u), v) = prod_{z in V\\{x,v}} eps(z, v);
      step 2 (per-i closed form):
        prod_x [per-(i,x)] = (-1)^{k(k-1)/2} prod_v eps(L_i(v), v);
      step 3 (global, condition 1):
        prod_{i,v} eps(L_i(v), v) = (-1)^{k(k-1)/2}, so
        E = (-1)^{k(k-1)/2 (k-1)} (-1)^{k(k-1)/2} = (-1)^{k^2(k-1)/2} = +1."""
    def eps(a, b):          # +1 iff a precedes b
        return 1 if a < b else -1

    E_direct, _, _ = E_of_chart(L, M, k)
    glob = 1
    for i in range(k - 1):
        Linv = [None] * (k + 1)
        for u in range(k):
            Linv[L[i][u]] = u
        mate = [[None] * (k + 1) for _ in range(k)]
        for u in range(k):
            for v in range(k):
                if v != u:
                    mate[u][M[i][u][v]] = v
        per_i = 1
        for x in range(k):
            v = Linv[x]
            supp = [u for u in range(k) if u not in (x, v)]
            assert sorted(mate[u][x] for u in supp) == supp   # involution sweep
            lhs = prod(eps(mate[u][x], v) for u in supp)
            rhs = prod(eps(z, v) for z in supp)
            assert lhs == rhs, ("E-lemma step 1", i, x)
            per_i *= lhs
        closed = (-1) ** (k * (k - 1) // 2) * \
            prod(eps(L[i][v], v) for v in range(k))
        assert per_i == closed, ("E-lemma step 2", i)
        glob *= prod(eps(L[i][v], v) for v in range(k))
    assert glob == (-1) ** (k * (k - 1) // 2), "E-lemma step 3"
    E_pred = (-1) ** (k * (k - 1) // 2 * k)
    assert E_pred == 1 and E_direct == 1, ("E-lemma total", E_direct)


def part_b2(Lw, Mw):
    E_lemma_steps(Lw, Mw, 16)
    print("[B2] E-lemma proof steps 1-3 verified on the Wallis k=16 chart; "
          "E = +1 as forced")


# ------------------------------------------------------------------- part C
def all_sils(n):
    edges = [(x, y) for x in range(n) for y in range(x + 1, n)]
    out, S = [], {}

    def rec(t):
        if t == len(edges):
            out.append(dict(S))
            return
        x, y = edges[t]
        ux = {S[e] for e in edges[:t] if x in e}
        uy = {S[e] for e in edges[:t] if y in e}
        for c in range(n):
            if c == x or c == y or c in ux or c in uy:
                continue
            S[(x, y)] = c
            rec(t + 1)
            del S[(x, y)]

    rec(0)
    return out


def _compat_bits(sq, n):
    edges = [(x, y) for x in range(n) for y in range(x + 1, n)]
    same = {e: [0] * n for e in edges}
    for a, S in enumerate(sq):
        for e in edges:
            same[e][S[e]] |= 1 << a
    full = (1 << len(sq)) - 1
    compat = []
    for S in sq:
        agree = 0
        for e in edges:
            agree |= same[e][S[e]]
        compat.append(full & ~agree)
    return compat


def _iter_bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def discordant_families(sq, n, need):
    compat = _compat_bits(sq, n)
    out = []

    def rec(cur, cand):
        if len(cur) == need:
            out.append(tuple(cur))
            return
        for v in _iter_bits(cand):
            rec(cur + [v], cand & compat[v] & ~((1 << (v + 1)) - 1))
            cand ^= 1 << v
            if len(cur) + bin(cand).count("1") < need:
                return

    rec([], (1 << len(sq)) - 1)
    return out


def max_discordant(sq, n):
    compat = _compat_bits(sq, n)
    best = 0

    def expand(cur, cand):
        nonlocal best
        if len(cur) > best:
            best = len(cur)
        for v in _iter_bits(cand):
            if len(cur) + bin(cand).count("1") <= best:
                return
            expand(cur + [v], cand & compat[v] & ~((1 << (v + 1)) - 1))
            cand ^= 1 << v

    expand([], (1 << len(sq)) - 1)
    return best


def cond4_edge_feasible(L, M, k, u, v):
    """Exhaustive: does a proper edge-colouring of K_{k-1} exist with the
    condition-4 palette C\\{M_i(uv), L_i(u), L_i(v)} at every index i?"""
    nA = k - 1
    holes = [{M[i][u][v], L[i][u], L[i][v]} for i in range(nA)]
    edges = [(a, b) for a in range(nA) for b in range(a + 1, nA)]
    used = [set() for _ in range(nA)]

    def rec(t):
        if t == len(edges):
            return True
        a, b = edges[t]
        for c in range(k + 1):
            if c in holes[a] or c in holes[b] or c in used[a] or c in used[b]:
                continue
            used[a].add(c)
            used[b].add(c)
            if rec(t + 1):
                return True
            used[a].discard(c)
            used[b].discard(c)
        return False

    return rec(0)


def part_c():
    # k = 4 impossibility recheck
    sq5 = all_sils(5)
    assert len(sq5) == 6 and max_discordant(sq5, 5) < 3
    print(f"[C] k=4: {len(sq5)} SILS(5), max discordant {max_discordant(sq5, 5)}"
          f" < 3 needed -> no radius-3 chart exists (recheck OK)")

    sq = all_sils(7)
    assert len(sq) == 6240
    fams = discordant_families(sq, 7, 5)
    assert len(fams) == 1680
    print(f"[C] k=6: SILS(7) = {len(sq)}, labelled discordant 5-families = "
          f"{len(fams)}")
    dist = {}
    negdist = {}
    peruv_ok = 0
    elemma_checked = 0
    k = 6
    for fam_idx, fi in enumerate(fams):
        F = [sq[t] for t in fi]
        for infp in range(7):
            L, M = chart_from_sils(F, 7, infp)
            check_conditions_123(L, M, k)
            if fam_idx < 5:                      # E-lemma steps on a sample
                E_lemma_steps(L, M, k)
                elemma_checked += 1
            E, neg, tot = E_of_chart(L, M, k)
            assert tot == (k - 1) * k * (k - 2)
            rhs, _, _, _ = RHS_of_chart(L, M, k)
            key = (E, rhs, E * rhs)
            dist[key] = dist.get(key, 0) + 1
            negdist[neg] = negdist.get(neg, 0) + 1
            if all(cond4_edge_feasible(L, M, k, u, v)
                   for u in range(k) for v in range(u + 1, k)):
                peruv_ok += 1
    ncharts = 7 * len(fams)
    print(f"[C] charts evaluated: {ncharts} (1680 families x 7 roots); "
          f"E-lemma proof steps re-verified on {elemma_checked} charts")
    print(f"[C] (E, RHS(F), required-H) distribution: {dist}")
    print(f"[C] negative-generic-pair count distribution: "
          f"{dict(sorted(negdist.items()))}")
    print(f"[C] charts whose per-uv layer (condition 4, all 15 edges) is "
          f"feasible: {peruv_ok}")
    out = {
        "n_sils7": len(sq), "n_families": len(fams), "n_charts": ncharts,
        "distribution": {str(kk): vv for kk, vv in sorted(dist.items())},
        "neg_pair_distribution": {str(kk): vv
                                  for kk, vv in sorted(negdist.items())},
        "per_uv_feasible_charts": peruv_ok,
    }
    (HERE / "k6_census.json").write_text(json.dumps(out, indent=1))
    return dist, peruv_ok


# ------------------------------------------------------------------- part D
def hhat_groupings(N, k):
    """N: dict[(u,v) sorted][(i,j) sorted] -> colour.  Returns the three
    independently computed butterfly counts (per-flag, per-(u,i,vv'),
    per-(i,x,jj'))."""
    A = range(k - 1)
    V = range(k)

    def nv(u, v, i, j):
        return N[(min(u, v), max(u, v))][(min(i, j), max(i, j))]

    g1 = 0
    for i in A:
        for u in V:
            fibers = {}
            for j in A:
                if j == i:
                    continue
                for v in V:
                    if v == u:
                        continue
                    fibers.setdefault(nv(u, v, i, j), []).append((j, v))
            for cells in fibers.values():
                g1 += inv_count(cells)
    g2 = 0
    for u in V:
        for i in A:
            for v in V:
                for vp in V:
                    if v >= vp or v == u or vp == u:
                        continue
                    for j in A:
                        if j == i:
                            continue
                        x = nv(u, v, i, j)
                        for jp in A:
                            if jp == i or jp == j:
                                continue
                            if nv(u, vp, i, jp) == x and jp < j:
                                g2 += 1
    g3 = 0
    for i in A:
        for j in A:
            for jp in A:
                if not (j < jp) or i in (j, jp):
                    continue
                for u in V:
                    for v in V:
                        if v == u:
                            continue
                        for vp in V:
                            if vp == u or vp == v:
                                continue
                            if (nv(u, v, i, j) == nv(u, vp, i, jp)
                                    and v > vp):
                                g3 += 1
    return g1, g2, g3


def part_d():
    rng = random.Random(66)
    k = 6
    for t in range(6):
        N = {}
        for u in range(k):
            for v in range(u + 1, k):
                N[(u, v)] = {}
                for i in range(k - 1):
                    for j in range(i + 1, k - 1):
                        N[(u, v)][(i, j)] = rng.randrange(k + 1)
        g1, g2, g3 = hhat_groupings(N, k)
        assert g1 == g2 == g3, ("D", t, g1, g2, g3)
    print("[D] butterfly regroupings: per-flag == per-(u,i,{v,v'}) == "
          "per-(i,x,{j,j'}) on 6 random k=6 tables OK")


# ------------------------------------------------------------------- part E
def fibers_of_flag(N, k, i, u):
    """Cell sets {x: [(j, v), ...]} of the partial fibers Phi_{i,u,x}."""
    fibers = {}
    for v in range(k):
        if v == u:
            continue
        key = (min(u, v), max(u, v))
        for (a, b), x in N[key].items():
            if i == a or i == b:
                j = b if i == a else a
                fibers.setdefault(x, []).append((j, v))
    return fibers


def hhat_of_table(N, k):
    """Relaxed invariant Hhat = (-1)^{total misordered cell pairs}.  Equals
    H = prod sgn Phi when every fiber is a partial matching (part A0)."""
    total = 0
    for i in range(k - 1):
        for u in range(k):
            for cells in fibers_of_flag(N, k, i, u).values():
                total += inv_count(cells)
    return (-1) ** total, total


def h_direct_of_table(N, k, L):
    """H = prod_{i,u,x} sgn Phi_{i,u,x}; requires every fiber to be a
    partial matching (raises otherwise).  Checks fiber sizes vs Lemma 3."""
    h = 1
    for i in range(k - 1):
        for u in range(k):
            fib = fibers_of_flag(N, k, i, u)
            assert L[i][u] not in fib          # empty class
            for x, cells in fib.items():
                want = (k - 2) if x in (u, k) else (k - 3)
                assert len(cells) == want, ("fiber size", i, u, x)
                h *= pm_sign(cells)
    return h


def load_json(name):
    p = HERE / name
    return json.loads(p.read_text()) if p.exists() else None


def decode_table(obj):
    N = {}
    for ek, row in obj.items():
        u, v = map(int, ek.split(","))
        N[(u, v)] = {}
        for pk, x in row.items():
            i, j = map(int, pk.split(","))
            N[(u, v)][(i, j)] = x
    return N


def verify_perij_table(N, L, k):
    """Check the per-ij trace constraints: for each pair {i,j} and colour x,
    the x-class is a perfect matching of its prescribed support."""
    Linv = []
    for i in range(k - 1):
        inv = [None] * (k + 1)
        for u in range(k):
            inv[L[i][u]] = u
        Linv.append(inv)
    for i in range(k - 1):
        for j in range(i + 1, k - 1):
            classes = {}
            for (u, v), row in N.items():
                classes.setdefault(row[(i, j)], []).append((u, v))
            for x in range(k + 1):
                cls = classes.get(x, [])
                if x == k:
                    supp = set(range(k))
                else:
                    supp = set(range(k)) - {Linv[i][x], Linv[j][x]}
                cover = [w for e in cls for w in e]
                assert sorted(cover) == sorted(supp), \
                    ("perij", i, j, x, cls, supp)


def verify_peruv_table(N, L, M, k):
    """Check condition 4 for every edge uv."""
    C = set(range(k + 1))
    for (u, v), row in N.items():
        for i in range(k - 1):
            vals = {row[(min(i, j), max(i, j))]
                    for j in range(k - 1) if j != i}
            assert vals == C - {M[i][u][v], L[i][u], L[i][v]}, \
                ("peruv", u, v, i)


def verify_perij_partial(N, L, k, pairs):
    """Trace constraints for a listed subset of index pairs only."""
    Linv = []
    for i in range(k - 1):
        inv = [None] * (k + 1)
        for u in range(k):
            inv[L[i][u]] = u
        Linv.append(inv)
    for i, j in pairs:
        classes = {}
        for (u, v), row in N.items():
            classes.setdefault(row[(i, j)], []).append((u, v))
        for x in range(k + 1):
            cls = classes.get(x, [])
            supp = set(range(k)) if x == k else \
                set(range(k)) - {Linv[i][x], Linv[j][x]}
            cover = [w for e in cls for w in e]
            assert sorted(cover) == sorted(supp), ("perij", i, j, x)


def part_e():
    reports = []
    for name in ("falsify_k6_perij.json", "falsify_k8_perij.json",
                 "falsify_k8_peruv.json", "falsify_k16_perij.json",
                 "falsify_k16_peruv.json",
                 "joint_k8_trace_cond4.json", "joint_k16_pairs1.json",
                 "joint_k16_pairs3.json", "joint_k16_partial.json"):
        obj = load_json(name)
        if obj is None:
            reports.append(f"[E] {name}: not present, skipped")
            continue
        if obj.get("status") == "INFEASIBLE" and not obj["instances"]:
            reports.append(f"[E] {name}: solver-INFEASIBLE record "
                           f"(no instances exist; nothing to re-verify)")
            continue
        k = obj["k"]
        L = obj["L"]
        M = obj.get("M")
        kind = obj["kind"]
        vals = []
        for inst in obj["instances"]:
            N = decode_table(inst["N"])
            if kind == "perij":
                verify_perij_table(N, L, k)
            if kind in ("peruv", "joint"):
                verify_peruv_table(N, L, M, k)
            if kind == "joint":
                if obj.get("pairs") is None:
                    verify_perij_table(N, L, k)
                else:
                    verify_perij_partial(N, L, k,
                                         [tuple(p) for p in obj["pairs"]])
            h, t = hhat_of_table(N, k)
            assert h == inst["Hhat"], (name, inst.get("tag"), h, inst["Hhat"])
            if kind == "joint" and obj.get("pairs") is None:
                hd = h_direct_of_table(N, k, L)
                assert hd == h, ("H_direct != Hhat", name, inst.get("tag"))
                assert hd == obj["H_required"], \
                    ("H != H_required on a two-sided table -- (H) violated!",
                     name, inst.get("tag"))
            vals.append(h)
        cnt = {1: vals.count(1), -1: vals.count(-1)}
        extra = ""
        if kind == "joint" and obj.get("pairs") is None and vals:
            extra = (f"; every instance is a genuine two-sided table and "
                     f"H_direct == Hhat == H_required = {obj['H_required']}")
        reports.append(f"[E] {name}: {len(vals)} instances re-verified, "
                       f"Hhat distribution {cnt}{extra}")
        if obj.get("counterexample"):
            a, b = obj["counterexample"]
            reports.append(f"[E]   counterexample pair: instances {a!r} vs "
                           f"{b!r} differ minimally and have opposite Hhat")
    for r in reports:
        print(r)


def main():
    part_a0()
    part_a1()
    part_a2()
    part_a3()
    Lw, Mw = part_b()
    part_b2(Lw, Mw)
    if "--skip-census" not in sys.argv:
        part_c()
    part_d()
    part_e()
    print("[ok] ALL PARTS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FIRST FAILURE: {e!r}")
        sys.exit(1)
