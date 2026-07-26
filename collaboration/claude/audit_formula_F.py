#!/usr/bin/env python3
r"""Exact sign-bookkeeping audit of candidate formula (F), pure stdlib.

Formula (F) (collaboration/flag_at_exact_formula_audit_prompt.md):
    prod_{i in A, u in V} AT(Q^{i,u})
      = (-1)^{k(k-1)/2} * AT(T) * prod_i delta(S_i)

Conventions (exact):
  V = 0..k-1, A = 0..k-2, C = V then infinity (inf := k, always last).
  Flag square Q^{i,u}: rows (A\{i} induced order, then m, then l),
  columns (V\{u} induced order, then *), symbols C\{L_i(u)} induced order.
  Sign of a bijection between ordered sets = sign of its permutation matrix.
  AT(X) = (product of row signs) * (product of column signs).

Tasks run in order; the run STOPS at the first failed assertion.
"""
import random
import sys
from itertools import permutations
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "evidence"))
from global_latin_audit import construct_golf17  # noqa: E402

rng = random.Random(835)


def perm_sign(perm):
    s = 1
    for a in range(len(perm)):
        for b in range(a + 1, len(perm)):
            if perm[a] > perm[b]:
                s = -s
    return s


def bij_sign(domain, mapping, target):
    """Sign of bijection mapping: domain -> target (both ordered lists)."""
    pos = {t: p for p, t in enumerate(target)}
    perm = [pos[mapping[d]] for d in domain]
    assert sorted(perm) == list(range(len(target))), "not a bijection"
    return perm_sign(perm)


def prod(xs):
    p = 1
    for x in xs:
        p *= x
    return p


# --------------------------------------------------------------------------
# TASK 1: cofactor lemma (C) and the deletion rule
# --------------------------------------------------------------------------
def check_pair(C, dom, img, a, b):
    """One lemma-(C) instance. C ambient ordered target, dom ends with '*'."""
    fa = {d: img[p] for p, d in enumerate(dom[:-1])}
    fb = dict(fa)
    fa["*"] = b
    fb["*"] = a
    sa = bij_sign(dom, fa, [c for c in C if c != a])
    sb = bij_sign(dom, fb, [c for c in C if c != b])
    want = (-1) ** (C.index(a) + C.index(b) + 1)
    assert sa * sb == want, ("lemma C fails", C, a, b, img, sa, sb, want)


def task1():
    n_random = n_exhaust = 0
    for n in range(5, 10):
        C = sorted(rng.sample(range(100), n))          # arbitrary labels
        dom = sorted(rng.sample(range(100), n - 2)) + ["*"]
        for a in C:
            for b in C:
                if a == b:
                    continue
                rest = [c for c in C if c not in (a, b)]
                for _ in range(200):                    # 200 random g
                    img = rest[:]
                    rng.shuffle(img)
                    check_pair(C, dom, img, a, b)
                    n_random += 1
                if n <= 8:                              # exhaustive upgrade
                    for img in permutations(rest):
                        check_pair(C, dom, list(img), a, b)
                        n_exhaust += 1
    # deletion rule: delete domain pos r and image pos s => factor (-1)^(r+s)
    n_del_rand = n_del_exh = 0
    for n in range(5, 9):
        for p in [list(q) for q in permutations(range(n))] if n <= 6 else []:
            s0 = perm_sign(p)
            for r in range(n):
                s = p[r]
                q = [x - (x > s) for idx, x in enumerate(p) if idx != r]
                assert perm_sign(q) == s0 * (-1) ** (r + s), ("del", n, p, r)
                n_del_exh += 1
        for _ in range(100):
            p = list(range(n))
            rng.shuffle(p)
            s0 = perm_sign(p)
            for r in range(n):
                s = p[r]
                q = [x - (x > s) for idx, x in enumerate(p) if idx != r]
                assert perm_sign(q) == s0 * (-1) ** (r + s), ("del", n, p, r)
                n_del_rand += 1
    print(f"[task1] lemma (C): {n_random} random + {n_exhaust} exhaustive "
          f"instances OK; deletion rule: {n_del_exh} exhaustive + "
          f"{n_del_rand} random deletions OK")


# --------------------------------------------------------------------------
# shared builders (parametric in k; inf := k)
# --------------------------------------------------------------------------
def symbols(L, i, u, k):
    return [c for c in range(k + 1) if c != L[i][u]]


def lrow_sign(L, i, u, k):
    dom = [v for v in range(k) if v != u] + ["*"]
    mp = {v: L[i][v] for v in range(k) if v != u}
    mp["*"] = k
    return bij_sign(dom, mp, symbols(L, i, u, k))


def mrow_sign(L, M, i, u, k):
    dom = [v for v in range(k) if v != u] + ["*"]
    mp = {v: M[i][u][v] for v in range(k) if v != u}
    mp["*"] = u
    return bij_sign(dom, mp, symbols(L, i, u, k))


def starcol_sign(L, i, u, k):
    dom = [j for j in range(k - 1) if j != i] + ["m", "l"]
    mp = {j: L[j][u] for j in range(k - 1) if j != i}
    mp["m"] = u
    mp["l"] = k
    return bij_sign(dom, mp, symbols(L, i, u, k))


def S_row_signs(L, M, i, k):
    """Row signs of S_i (order k+1 on C): S(u,u)=u, S(u,v)=M_i(uv),
    S(u,inf)=L_i(u), S(inf,u)=L_i(u), S(inf,inf)=inf."""
    C = list(range(k + 1))
    out = []
    for u in range(k):
        mp = {v: M[i][u][v] for v in range(k) if v != u}
        mp[u] = u
        mp[k] = L[i][u]
        out.append(bij_sign(C, mp, C))
    mp = {u: L[i][u] for u in range(k)}
    mp[k] = k
    out.append(bij_sign(C, mp, C))
    return out


def T_row_signs(L, k):
    """T: rows A then e (last), columns V, symbols V; T(i,u)=L_i(u), T(e,u)=u."""
    V = list(range(k))
    out = [bij_sign(V, {u: L[i][u] for u in V}, V) for i in range(k - 1)]
    out.append(bij_sign(V, {u: u for u in V}, V))     # row e = identity
    return out


def T_col_signs(L, k):
    rows = list(range(k - 1)) + ["e"]
    out = []
    for u in range(k):
        mp = {i: L[i][u] for i in range(k - 1)}
        mp["e"] = u
        out.append(bij_sign(rows, mp, list(range(k))))
    return out


def sanity_conditions_12(L, M, k):
    nc = set(range(k + 1))
    for u in range(k):
        assert {L[i][u] for i in range(k - 1)} == set(range(k)) - {u}, \
            ("cond 1 fails", u)
    for i in range(k - 1):
        assert sorted(L[i]) == list(range(k)), ("L not perm", i)
        assert all(L[i][u] != u for u in range(k)), ("L not derangement", i)
        for u in range(k):
            for v in range(k):
                if u != v:
                    assert M[i][u][v] == M[i][v][u], ("M not symmetric", i)
            pal = {M[i][u][v] for v in range(k) if v != u}
            assert pal == nc - {u, L[i][u]}, ("cond 2 fails", i, u)


def build_wallis():
    K = 16
    golf = construct_golf17()
    L = [[None] * K for _ in range(K - 1)]
    M = [[[None] * K for _ in range(K)] for _ in range(K - 1)]
    for i in range(K - 1):
        for u in range(K):
            for v in range(K):
                if v != u:
                    M[i][u][v] = golf[i][u][v]
            seen = {golf[i][u][v] for v in range(K) if v != u}
            L[i][u] = next(x for x in range(K + 1)
                           if x not in seen and x != u)
            assert L[i][u] == golf[i][u][16]          # cross-check
    # S_i as defined coincides with golf[i] (inf = 16): sanity
    for i in range(K - 1):
        for u in range(K):
            assert golf[i][u][u] == u
        assert golf[i][16][16] == 16
        assert all(golf[i][16][u] == L[i][u] for u in range(K))
    return L, M


# --------------------------------------------------------------------------
# TASK 2: items 3, 4, 5 on the Wallis k=16 chart
# --------------------------------------------------------------------------
def task2(L, M):
    K = 16
    sanity_conditions_12(L, M, K)
    sgnL = [perm_sign(L[i]) for i in range(K - 1)]

    # item 3: l-rows
    for i in range(K - 1):
        p = prod(lrow_sign(L, i, u, K) for u in range(K))
        mid = sgnL[i] ** K * (-1) ** (sum(range(K))
                                      + sum(L[i][u] for u in range(K)))
        assert p == mid, ("item 3 first equality fails", i, p, mid)
        assert p == 1, ("item 3 second equality fails", i, p)
    print("[task2] item 3: all 15 i PASS "
          "(prod_u sgn(l-row) == sgn(L_i)^16 * (-1)^{240} == +1)")

    # item 4: m-rows
    deltas = []
    for i in range(K - 1):
        p = prod(mrow_sign(L, M, i, u, K) for u in range(K))
        d = prod(S_row_signs(L, M, i, K))
        deltas.append(d)
        assert p == d * sgnL[i], ("item 4 fails", i, p, d, sgnL[i])
    print(f"[task2] item 4: all 15 i PASS (prod_u sgn(m-row) == "
          f"delta(S_i)*sgn(L_i)); deltas = {deltas}")

    # item 5: *-columns, product over ALL 240 flags
    tot = prod(starcol_sign(L, i, u, K)
               for i in range(K - 1) for u in range(K))
    CT = prod(T_col_signs(L, K))
    want = (-1) ** (K * (K - 1) // 2) * CT
    assert tot == want, ("item 5 fails", tot, CT, want)
    print(f"[task2] item 5: PASS over 240 flags "
          f"(prod sgn(*-col) = {tot} == (-1)^120 * C(T), C(T) = {CT})")
    return sgnL, deltas, CT


# --------------------------------------------------------------------------
# TASK 3: genuine k=2 control, structures enumerated from the definitions
# --------------------------------------------------------------------------
def flag_square_AT(L, M, N, i, u, k):
    rows = [j for j in range(k - 1) if j != i] + ["m", "l"]
    cols = [v for v in range(k) if v != u] + ["*"]
    syms = symbols(L, i, u, k)

    def entry(r, c):
        if r == "m":
            return u if c == "*" else M[i][u][c]
        if r == "l":
            return k if c == "*" else L[i][c]
        return L[r][u] if c == "*" else N[frozenset((u, c))][frozenset((i, r))]

    grid = {(r, c): entry(r, c) for r in rows for c in cols}
    for r in rows:                                     # Latin check
        assert sorted(grid[(r, c)] for c in cols) == sorted(syms)
    for c in cols:
        assert sorted(grid[(r, c)] for r in rows) == sorted(syms)
    rowsigns = [bij_sign(cols, {c: grid[(r, c)] for c in cols}, syms)
                for r in rows]
    colsigns = [bij_sign(rows, {r: grid[(r, c)] for r in rows}, syms)
                for c in cols]
    return prod(rowsigns) * prod(colsigns), grid, rows, cols, syms


def task3():
    k = 2
    # L: enumerate ALL charts (one index, i=0) satisfying conditions 1-2
    Lcands = [p for p in permutations(range(k))
              if all(p[u] != u for u in range(k))
              and all({p[u]} == set(range(k)) - {u} for u in range(k))]
    assert Lcands == [(1, 0)], Lcands                 # unique derangement
    L = [list(Lcands[0])]
    # M_0: colour of the single edge 01, forced by condition 2
    mc = [c for c in range(k + 1)
          if all({c} == set(range(k + 1)) - {u, L[0][u]} for u in range(k))]
    assert mc == [k], mc                              # forced = infinity
    M = [[[None, k], [k, None]]]
    sanity_conditions_12(L, M, k)
    # condition 3 on edge 01
    assert {M[0][0][1]} == set(range(k + 1)) - {0, 1}
    # condition 4: K_A has one vertex, no edges; required incident palette
    # C \ {M_0(01), L_0(0), L_0(1)} = C \ {inf,1,0} = {} -- vacuous, N empty.
    assert set(range(k + 1)) - {M[0][0][1], L[0][0], L[0][1]} == set()
    N = {}                                            # DEGENERATE: no edges

    AT0, g0, rows, cols0, _ = flag_square_AT(L, M, N, 0, 0, k)
    AT1, g1, _, cols1, _ = flag_square_AT(L, M, N, 0, 1, k)
    assert AT0 == 1 and AT1 == 1, (AT0, AT1)          # user-stated control
    LHS = AT0 * AT1

    ATT = prod(T_row_signs(L, k)) * prod(T_col_signs(L, k))
    d0 = prod(S_row_signs(L, M, 0, k))
    assert ATT == 1, ATT                              # user-stated control
    assert d0 == -1, d0                               # user-stated control
    RHS = (-1) ** (k * (k - 1) // 2) * ATT * d0
    assert RHS == 1 and LHS == RHS, (LHS, RHS)

    # item-partition cross-check: LHS == item1*item2*item3*item4*item5
    item1 = 1                                         # no j-rows: A\{0} empty
    assert rows == ["m", "l"]
    # item 2 = product of all existing-column signs (col 1 of Q^{0,0} and
    # col 0 of Q^{0,1}); lemma (C) predicts (-1)^{pos L(0)+pos L(1)+1}
    syms0 = symbols(L, 0, 0, k)
    syms1 = symbols(L, 0, 1, k)
    c10 = bij_sign(rows, {r: g0[(r, 1)] for r in rows}, syms0)
    c01 = bij_sign(rows, {r: g1[(r, 0)] for r in rows}, syms1)
    item2 = c10 * c01
    assert item2 == (-1) ** (L[0][0] + L[0][1] + 1) == 1, (c10, c01)
    item3 = prod(lrow_sign(L, 0, u, k) for u in range(k))
    item4 = prod(mrow_sign(L, M, 0, u, k) for u in range(k))
    item5 = prod(starcol_sign(L, 0, u, k) for u in range(k))
    assert item4 == d0 * perm_sign(L[0]), (item4, d0)       # item-4 identity
    assert item5 == (-1) ** (k * (k - 1) // 2) * prod(T_col_signs(L, k))
    assert item1 * item2 * item3 * item4 * item5 == LHS
    print(f"[task3] k=2 control PASS: AT(Q^{{0,0}})=AT(Q^{{0,1}})=+1, "
          f"AT(T)={ATT}, delta(S_0)={d0}, LHS={LHS} == RHS="
          f"(-1)^1*({ATT})*({d0})={RHS}; N degenerates to the empty "
          f"colouring (K_A has no edges) and condition 4 is vacuous; "
          f"item partition 1..5 = ({item1},{item2},{item3},{item4},{item5}) "
          f"multiplies to LHS")


# --------------------------------------------------------------------------
# TASK 4: items 1-2 parity arithmetic (k = 4,6,8,16) + formal assembly
# --------------------------------------------------------------------------
def synthetic_L(k):
    """Condition-1 chart: L_i(u) = u+i+1 mod k (cyclic; derangements,
    columns rainbow).  Only condition 1 + bijectivity feed items 1-2."""
    return [[(u + i + 1) % k for u in range(k)] for i in range(k - 1)]


def task4_parity(k, L, name):
    for u in range(k):                                 # condition 1
        assert {L[i][u] for i in range(k - 1)} == set(range(k)) - {u}
    for i in range(k - 1):
        assert sorted(L[i]) == list(range(k))
        assert all(L[i][u] != u for u in range(k))
    # item 1: rows j of Q^{i,u} paired with rows i of Q^{j,u} via (C) with
    # a=L_i(u), b=L_j(u):  factor (-1)^{pos a + pos b + 1} per pair {i,j}.
    tot1 = 0
    for u in range(k):
        e_u = sum(L[i][u] + L[j][u] + 1
                  for i in range(k - 1) for j in range(i + 1, k - 1))
        closed = (k - 2) * (k * (k - 1) // 2 - u) + (k - 1) * (k - 2) // 2
        assert e_u == closed, ("item1 closed form", k, u, e_u, closed)
        assert e_u % 2 == ((k - 1) * (k - 2) // 2) % 2
        tot1 += e_u
    assert tot1 % 2 == 0, ("item 1 total not +1", k, tot1)
    # item 2: columns v of Q^{i,u} paired with columns u of Q^{i,v} via (C)
    # with a=L_i(u), b=L_i(v):  factor (-1)^{pos a + pos b + 1} per {u,v}.
    tot2 = 0
    for i in range(k - 1):
        e_i = sum(L[i][u] + L[i][v] + 1
                  for u in range(k) for v in range(u + 1, k))
        closed = (k - 1) * (k * (k - 1) // 2) + k * (k - 1) // 2
        assert e_i == closed, ("item2 closed form", k, i, e_i, closed)
        assert e_i % 2 == 0
        tot2 += e_i
    assert tot2 % 2 == 0, ("item 2 total not +1", k, tot2)
    print(f"[task4] k={k} ({name}): item-1 exponent {tot1} (even => +1; "
          f"per-u parity == C(k-1,2) mod 2), item-2 exponent {tot2} "
          f"(even => +1; per-i exponent == k^2(k-1)/2, even)")


def task4_assembly(L, M, sgnL, deltas, CT):
    K = 16
    # numeric: [item3]*[item4]*[item5] must equal RHS(F) given R(T)=prod sgnL
    item3 = prod(prod(lrow_sign(L, i, u, K) for u in range(K))
                 for i in range(K - 1))
    item4 = prod(prod(mrow_sign(L, M, i, u, K) for u in range(K))
                 for i in range(K - 1))
    item5 = prod(starcol_sign(L, i, u, K)
                 for i in range(K - 1) for u in range(K))
    RT = prod(T_row_signs(L, K))
    ATT = RT * CT
    assert RT == prod(sgnL), (RT, prod(sgnL))          # row e contributes +1
    rhs = (-1) ** (K * (K - 1) // 2) * ATT * prod(deltas)
    lhs_135 = item3 * item4 * item5
    assert lhs_135 == rhs, (item3, item4, item5, rhs)
    print(f"[task4] assembly at k=16 (Wallis): item3={item3}, item4={item4} "
          f"(= prod delta * prod sgnL), item5={item5}; product = {lhs_135} "
          f"== RHS(F) = (-1)^120 * AT(T) * prod delta = {rhs}")
    print(f"[task4] values: R(T)={RT}, C(T)={CT}, AT(T)={ATT}, "
          f"prod_i delta(S_i)={prod(deltas)}, prod_i sgn(L_i)={prod(sgnL)}, "
          f"RHS(F) at k=16 = {rhs}")


def main():
    task1()
    Lw, Mw = build_wallis()
    sgnL, deltas, CT = task2(Lw, Mw)
    task3()
    for k in (4, 6, 8):
        task4_parity(k, synthetic_L(k), "synthetic cyclic, condition 1")
    task4_parity(16, Lw, "Wallis chart")
    task4_assembly(Lw, Mw, sgnL, deltas, CT)
    print("[ok] ALL TASKS PASS")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FIRST FAILURE: {e!r}")
        sys.exit(1)
