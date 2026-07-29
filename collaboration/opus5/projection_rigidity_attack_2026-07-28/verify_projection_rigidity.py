#!/usr/bin/env python3
"""Verifier for the two-valued top-module projection attack on Erdos-Rosenfeld #835.

Standard library only (fractions, itertools, random).  Every check is exact
rational arithmetic; no floating point is used in any assertion.

Scope of what this file certifies (and nothing more):

  A. Theorem A1/A2 (automaticity).  For a partition of ANY N-set into q equal
     classes, P = (q R - J)/N satisfies every graph-free identity checked
     below.  This does not include top-module containment/AP=-P, which is the
     hard graph condition.  Checked on random partitions.
  B. Theorem A3 (converse, exhaustive at small size).  Every symmetric matrix
     with entries in {k/N, -1/N} and P^2 = P is (q R - J)/N for an
     equipartition into q classes of size N/q.  Checked exhaustively for
     (N,q) = (6,3); q=2 is outside the theorem's k=q-1>=2 hypothesis.
  C. Krein/Schur-support condition q^d_{dd} != 0 for the Johnson scheme
     J(2k-1, k-1).  Closed form evaluated exactly for k = 4,6,10,12,16 and
     cross-checked at k = 4 against a directly constructed primitive
     idempotent on 35 vertices.
  D. k = 4 control.  All 30 Fano planes are perfect codes of KG(7,3); the
     maximum number of pairwise disjoint ones is computed exactly.
  E. k = 6 control.  An S(4,5,11) is constructed (cyclic, 6 base blocks),
     verified to be a perfect code of KG(11,5), and shown to satisfy the
     design-quadrature and Krein-positivity conditions.
"""

from fractions import Fraction as F
from itertools import combinations, product
import random
import sys

FAILURES = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    if not cond:
        FAILURES.append(name)
    print(f"[{status}] {name}" + (f"  {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# A. Automaticity: the projection package holds for ANY equipartition.
# ---------------------------------------------------------------------------

def projection_from_partition(colour, q):
    """P = (q R - J)/N where R is the equivalence matrix of `colour`."""
    N = len(colour)
    return [[F(q * (1 if colour[u] == colour[v] else 0) - 1, N) for v in range(N)]
            for u in range(N)]


def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    Bt = list(zip(*B))
    return [[sum(A[i][t] * Bt[j][t] for t in range(m)) for j in range(p)] for i in range(n)]


def rank_exact(M):
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = F(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == rows:
            break
    return r


def check_automaticity(N, q, seed):
    """Every listed identity, for a RANDOM equipartition of an abstract N-set."""
    k = q - 1
    m = N // q
    rng = random.Random(seed)
    colour = [a for a in range(q) for _ in range(m)]
    rng.shuffle(colour)
    P = projection_from_partition(colour, q)
    tag = f"(N={N}, q={q}, seed={seed})"

    sym = all(P[u][v] == P[v][u] for u in range(N) for v in range(N))
    check(f"A.symmetric {tag}", sym)

    two_valued = all(P[u][v] in (F(k, N), F(-1, N)) for u in range(N) for v in range(N))
    check(f"A.two-valued {tag}", two_valued)

    P2 = matmul(P, P)
    check(f"A.idempotent P^2=P {tag}", P2 == P)

    tr = sum(P[u][u] for u in range(N))
    check(f"A.trace = k {tag}", tr == F(k), f"trace={tr}")
    check(f"A.rank = k {tag}", rank_exact(P) == k)

    rowsums = [sum(P[u]) for u in range(N)]
    check(f"A.P*1 = 0 {tag}", all(s == 0 for s in rowsums))

    # Schur square:  P o P = ((k-1)/N) P + (k/N^2) J
    schur_ok = all(P[u][v] * P[u][v] == F(k - 1, N) * P[u][v] + F(k, N * N)
                   for u in range(N) for v in range(N))
    check(f"A.Schur square identity {tag}", schur_ok)

    # Schur cube:  P o P o P = ((k^2-k+1)/N^2) P + (k(k-1)... ) J ; solve for beta
    alpha = F(k * k - k + 1, N * N)
    beta = F(k, N) ** 3 - alpha * F(k, N)
    cube_ok = all(P[u][v] ** 3 == alpha * P[u][v] + beta for u in range(N) for v in range(N))
    check(f"A.Schur cube in span(P,J) {tag}", cube_ok)

    # (N P + J)/q is a 0/1 equivalence-relation matrix
    R = [[(N * P[u][v] + 1) / q for v in range(N)] for u in range(N)]
    check(f"A.(NP+J)/q is 0/1 equivalence matrix {tag}",
          all(x in (F(0), F(1)) for row in R for x in row)
          and all(R[u][v] == (1 if colour[u] == colour[v] else 0)
                  for u in range(N) for v in range(N)))


# ---------------------------------------------------------------------------
# B. Exhaustive converse: two-valued + idempotent forces an equipartition.
# ---------------------------------------------------------------------------

def check_converse_exhaustive(N, q):
    """Enumerate every symmetric {k/N,-1/N}-matrix with P^2 = P.

    Theorem B needs k = q-1 >= 2 (its class-size step divides by k-1), so q = 2
    is excluded here: at q = 2 the diagonal equation degenerates and the
    statement is not claimed.
    """
    k = q - 1
    assert k >= 2, "Theorem B is stated for k >= 2"
    hi, lo = F(k, N), F(-1, N)
    pairs = list(combinations(range(N), 2))
    solutions = []
    for bits in product((0, 1), repeat=len(pairs)):
        P = [[hi if u == v else lo for v in range(N)] for u in range(N)]
        for (u, v), b in zip(pairs, bits):
            if b:
                P[u][v] = P[v][u] = hi
        if matmul(P, P) == P:
            solutions.append(P)

    # every solution must be the equivalence matrix of an equipartition into q
    # classes of size N/q
    ok = True
    for P in solutions:
        cls = {}
        for u in range(N):
            cls.setdefault(frozenset(v for v in range(N) if P[u][v] == hi), set()).add(u)
        parts = list(cls.keys())
        if len(parts) != q or any(len(p) != N // q for p in parts):
            ok = False
        if set().union(*parts) != set(range(N)) or sum(len(p) for p in parts) != N:
            ok = False
    expected = 1
    n_parts = N // q
    # number of partitions of N labelled points into q unordered blocks of size n_parts
    from math import factorial
    expected = factorial(N) // (factorial(n_parts) ** q * factorial(q))
    check(f"B.exhaustive converse (N={N}, q={q})",
          ok and len(solutions) == expected,
          f"{len(solutions)} solutions, expected {expected} equipartitions")


# ---------------------------------------------------------------------------
# C. Johnson scheme J(n,d): eigenmatrix and the Krein parameter q^d_{dd}.
# ---------------------------------------------------------------------------

def binom(n, r):
    if r < 0 or r > n:
        return 0
    num = 1
    for i in range(r):
        num = num * (n - i) // (i + 1)
    return num


def johnson_p(n, d):
    """p_i(j) = eigenvalue of the distance-i relation A_i of J(n,d) on V_j.

    Uses the standard intersection array b_i = (d-i)(n-d-i), c_i = i^2 and the
    three-term recurrence, so nothing is taken on faith beyond that array.
    """
    deg = d * (n - d)
    theta = [(d - j) * (n - d - j) - j for j in range(d + 1)]
    b = [(d - i) * (n - d - i) for i in range(d + 1)]
    c = [i * i for i in range(d + 1)]
    a = [deg - b[i] - c[i] for i in range(d + 1)]
    p = [[F(0)] * (d + 1) for _ in range(d + 1)]
    for j in range(d + 1):
        p[0][j] = F(1)
        if d >= 1:
            p[1][j] = F(theta[j])
        for i in range(1, d):
            p[i + 1][j] = ((F(theta[j] - a[i]) * p[i][j] - F(b[i - 1]) * p[i - 1][j])
                           / F(c[i + 1]))
    return p, theta


def krein_top(n, d):
    """q^d_{dd} = (m_d^2 / |X|) * sum_i p_i(d)^3 / v_i^2  (exact)."""
    X = binom(n, d)
    v = [binom(d, i) * binom(n - d, i) for i in range(d + 1)]
    m_d = binom(n, d) - binom(n, d - 1)
    p, _ = johnson_p(n, d)
    total = sum(p[i][d] ** 3 / F(v[i]) ** 2 for i in range(d + 1))
    return F(m_d) ** 2 / F(X) * total, m_d, v, p


def johnson_direct_check(n, d):
    """Independent construction of E_d on J(n,d) and direct q^d_{dd}; small n only."""
    verts = list(combinations(range(n), d))
    idx = {s: i for i, s in enumerate(verts)}
    X = len(verts)
    A1 = [[F(0)] * X for _ in range(X)]
    for s in verts:
        for t in verts:
            if len(set(s) & set(t)) == d - 1:
                A1[idx[s]][idx[t]] = F(1)
    _, theta = johnson_p(n, d)
    E = [[F(1) if i == j else F(0) for j in range(X)] for i in range(X)]
    for j in range(d):
        M = [[A1[i][l] - (F(theta[j]) if i == l else F(0)) for l in range(X)] for i in range(X)]
        E = matmul(E, M)
        s = F(1) / F(theta[d] - theta[j])
        E = [[x * s for x in row] for row in E]
    m_d = binom(n, d) - binom(n, d - 1)
    cube = sum(E[u][v] ** 3 for u in range(X) for v in range(X))
    return F(X) / F(m_d) * cube, E


# ---------------------------------------------------------------------------
# D/E. Odd-graph controls.
# ---------------------------------------------------------------------------

def kneser(n, r):
    verts = list(combinations(range(n), r))
    idx = {s: i for i, s in enumerate(verts)}
    nbr = [[] for _ in verts]
    for s in verts:
        rest = [x for x in range(n) if x not in s]
        for t in combinations(rest, r):
            nbr[idx[s]].append(idx[t])
    return verts, idx, nbr


def is_perfect_code(nbr, code):
    """Exactly one of {v} u N(v) lies in `code`, for every vertex v."""
    C = set(code)
    return all(((1 if v in C else 0) + sum(1 for w in nbr[v] if w in C)) == 1
               for v in range(len(nbr)))


def tau_cube(N, code, q):
    """sum_p y_p^3 for y = 1_C - (1/q) 1."""
    s = len(code)
    return s * (1 - F(1, q)) ** 3 + (N - s) * (F(-1, q)) ** 3


def all_fano_planes():
    triples = list(combinations(range(7), 3))
    pairs = list(combinations(range(7), 2))
    cover = {p: [t for t in triples if set(p) <= set(t)] for p in pairs}
    out = []

    def rec(chosen, used_pairs):
        if len(chosen) == 7:
            out.append(tuple(chosen))
            return
        p = next(p for p in pairs if p not in used_pairs)
        for t in cover[p]:
            tp = set(combinations(t, 2))
            if tp & used_pairs:
                continue
            rec(chosen + [t], used_pairs | tp)

    rec([], set())
    return out


def max_clique(adj, n):
    best = [0]
    order = sorted(range(n), key=lambda v: -len(adj[v]))

    def rec(cand, size):
        if size + len(cand) <= best[0]:
            return
        if not cand:
            best[0] = max(best[0], size)
            return
        for i, v in enumerate(cand):
            if size + len(cand) - i <= best[0]:
                return
            rec([u for u in cand[i + 1:] if u in adj[v]], size + 1)

    rec(order, 0)
    return best[0]


def cyclic_s4511():
    """Find 6 base 5-blocks mod 11 whose 4-subset orbits partition all 30 orbits."""
    def orb4(s):
        return min(tuple(sorted((x + t) % 11 for x in s)) for t in range(11))

    reps5 = sorted({min(tuple(sorted((x + t) % 11 for x in s)) for t in range(11))
                    for s in combinations(range(11), 5)})
    prof = {}
    for b in reps5:
        os_ = [orb4(c) for c in combinations(b, 4)]
        if len(set(os_)) == 5:
            prof[b] = frozenset(os_)
    keys = sorted(prof)
    sol = []

    def rec(start, chosen, covered):
        if sol:
            return
        if len(chosen) == 6:
            sol.append(list(chosen))
            return
        for i in range(start, len(keys)):
            b = keys[i]
            if prof[b] & covered:
                continue
            rec(i + 1, chosen + [b], covered | prof[b])
            if sol:
                return

    rec(0, [], frozenset())
    if not sol:
        return None
    return [tuple(sorted((x + t) % 11 for x in b)) for b in sol[0] for t in range(11)]


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("A. Automaticity of the projection package (graph-free)")
    print("=" * 72)
    for (N, q, seed) in [(12, 3, 1), (20, 5, 2), (35, 5, 3), (24, 3, 4)]:
        check_automaticity(N, q, seed)

    print()
    print("=" * 72)
    print("B. Exhaustive converse: two-valued + idempotent => equipartition")
    print("=" * 72)
    check_converse_exhaustive(6, 3)

    print()
    print("=" * 72)
    print("C. Krein/Schur-support condition q^d_dd != 0 for J(2k-1,k-1)")
    print("=" * 72)
    direct, _ = johnson_direct_check(7, 3)
    formula, m_d, _, _ = krein_top(7, 3)
    check("C.formula vs direct idempotent, J(7,3)", direct == formula,
          f"both = {formula}")
    for k in (4, 6, 10, 12, 16):
        n, d = 2 * k - 1, k - 1
        val, m_d, _, _ = krein_top(n, d)
        check(f"C.q^d_dd > 0 for J({n},{d})  [k={k}]", val > 0,
              f"q^d_dd = {val}  (~{float(val):.6g}), m_d = {m_d}")

    print()
    print("=" * 72)
    print("D. k = 4 control: KG(7,3), Fano planes, one code vs a partition")
    print("=" * 72)
    verts, idx, nbr = kneser(7, 3)
    N4, q4 = len(verts), 5
    check("D.|V(KG(7,3))| = 35 and 4-regular", N4 == 35 and all(len(x) == 4 for x in nbr))
    fanos = all_fano_planes()
    check("D.number of Fano planes = 30", len(fanos) == 30)
    codes = [[idx[t] for t in f] for f in fanos]
    check("D.every Fano plane is a perfect code of KG(7,3)",
          all(is_perfect_code(nbr, c) for c in codes))

    def top_module(c):
        C = set(c)
        return all(sum(1 for w in nbr[v] if w in C) == (0 if v in C else 1)
                   for v in range(N4))

    check("D.1_C - (1/5)1 lies in the (-1)-eigenspace", all(top_module(c) for c in codes))
    tau4 = tau_cube(N4, codes[0], q4)
    check("D.tau(y_C,y_C,y_C) = N(q-1)(q-2)/q^3",
          tau4 == F(N4 * (q4 - 1) * (q4 - 2), q4 ** 3), f"= {tau4}")
    adj = {i: {j for j in range(30) if j != i and not (set(codes[i]) & set(codes[j]))}
           for i in range(30)}
    mc = max_clique(adj, 30)
    check("D.max pairwise disjoint Fano planes < 5 (so no LS(2,3,7))", mc < 5,
          f"maximum = {mc}, a partition needs q = 5")

    print()
    print("=" * 72)
    print("E. k = 6 control: KG(11,5) and the Witt design S(4,5,11)")
    print("=" * 72)
    blocks = cyclic_s4511()
    check("E.cyclic S(4,5,11) found (66 blocks)", blocks is not None and len(blocks) == 66)
    if blocks:
        cnt = {}
        for b in blocks:
            for c in combinations(b, 4):
                cnt[c] = cnt.get(c, 0) + 1
        check("E.every 4-subset in exactly one block (lambda = 1)",
              len(cnt) == binom(11, 4) and set(cnt.values()) == {1})
        v6, i6, n6 = kneser(11, 5)
        N6, q6 = len(v6), 7
        check("E.|V(KG(11,5))| = 462 and 6-regular",
              N6 == 462 and all(len(x) == 6 for x in n6))
        code6 = [i6[b] for b in blocks]
        check("E.the Witt design is a perfect code of KG(11,5)", is_perfect_code(n6, code6))
        C6 = set(code6)
        check("E.1_C - (1/7)1 lies in the (-1)-eigenspace",
              all(sum(1 for w in n6[v] if w in C6) == (0 if v in C6 else 1)
                  for v in range(N6)))
        tau6 = tau_cube(N6, code6, q6)
        check("E.tau(y_C,y_C,y_C) = N(q-1)(q-2)/q^3 > 0",
              tau6 == F(N6 * (q6 - 1) * (q6 - 2), q6 ** 3) and tau6 > 0, f"= {tau6}")
        val, _, _, _ = krein_top(11, 5)
        check("E.hence q^d_dd > 0 for J(11,5): Krein layer cannot obstruct k=6",
              val > 0, f"q^d_dd = {val}")

    print()
    print("=" * 72)
    print(f"RESULT: {len(FAILURES)} failure(s)"
          + (": " + ", ".join(FAILURES) if FAILURES else ""))
    print("=" * 72)
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
