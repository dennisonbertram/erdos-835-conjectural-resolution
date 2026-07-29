#!/usr/bin/env python3
"""Exact redundant verifier for collaboration/opus5/bcz_odd_graph_attack_2026-07-29.

Standard library only (math, fractions, itertools, random).  Exact integer /
rational arithmetic throughout; no floating point is used for any decision.

NOT EXECUTED BY ITS OPUS AUTHOR.  Python execution was refused by the permission
layer in the session that produced the original PROOF.md.  It was subsequently
executed by the independent root audit, which also added the closed form in
Theorem 11.4.  This script is a redundant check, not a dependency of any claim.

What it checks, part by part (and nothing else):

  A  Theorem 1 (intertwining B_pi^T S = S B_sigma) for every ordered pair of
     equitable partitions found on K3, C6, Q3, Petersen, and O_4 = KG(7,3).
     Equitable partitions are produced by 1-dimensional Weisfeiler-Leman
     refinement of assorted seeds, and each is re-verified to be equitable
     directly from the definition.

  B  k = 2 control.  O_2 = KG(3,1) = K_3, q = 3, tau = the three singletons is a
     genuine partition into perfect codes.  Checks B_tau = J_q - I_q, and checks
     Theorem 3 -- (B_pi + I) T = J and T 1 = 1 -- for every equitable pi of K3.

  C  Theorem 3 bookkeeping on O_4: the multiplicity of -1 in B_pi equals
     dim(U_pi ∩ V_{k-1}), computed independently as rank(Pi_{V_3} X_pi), and the
     affine solution space of (B_pi + I) T = J, T 1 = 1 has dimension
     eps_pi * (q - 1).

  D  Corollary 6.1 on O_4: every equitable partition with -1 not in spec(B_pi)
     has all cell sizes divisible by q = 5.

  E  Theorem 8 on O_4 against a real perfect code.  The cyclic Fano plane is
     checked to satisfy (A + I) 1_C = 1, and for every vertex M the exact
     distance distribution |P_j ∩ C| is compared with the closed form.

  F  Theorems 8.1 and 11 evaluated exactly for every even k <= 200 with k + 1
     prime: integrality and nonnegativity of alpha_j, the totals identities, and
     the two-colour condition (11.2)  0 <= x_i <= alpha_i(a)  in all three
     (eps_a, eps_a') cases.  Part F is the only genuinely new information this
     script can produce; PROOF.md Theorem 11.3 covers k = 4, 6, 10 by hand.

  G  Theorem 7 (Kummer divisibility) for every even k <= 80 with k + 1 prime.
     The range is smaller than in part F because the (m, j) double loop is
     quadratic in k.

Scope limits: it verifies no existence claim, tests nothing at k = 16 beyond the
closed-form arithmetic of parts F and G, and does not attempt to enumerate all
equitable partitions of any graph.

Expected runtime is dominated by part A on O_4 (pairwise 35x35 exact integer
matrix products over every pair of equitable partitions found) and by the
exact rational eliminations in part C; order of a minute, not seconds.
"""

import math
import random
from fractions import Fraction
from itertools import combinations

FAILURES = []


def check(cond, label):
    if not cond:
        FAILURES.append(label)
    return cond


# --------------------------------------------------------------------------
# graphs
# --------------------------------------------------------------------------

def kneser(n, r):
    """Kneser graph KG(n, r): r-subsets of [n], adjacent iff disjoint."""
    verts = [frozenset(c) for c in combinations(range(n), r)]
    index = {v: i for i, v in enumerate(verts)}
    adj = [[] for _ in verts]
    for i, S in enumerate(verts):
        for j in range(i + 1, len(verts)):
            if not (S & verts[j]):
                adj[i].append(j)
                adj[j].append(i)
    return verts, index, adj


def cycle(n):
    return [[(i - 1) % n, (i + 1) % n] for i in range(n)]


def hypercube(d):
    return [[u ^ (1 << b) for b in range(d)] for u in range(1 << d)]


# --------------------------------------------------------------------------
# equitable partitions
# --------------------------------------------------------------------------

def wl_refine(adj, initial):
    """1-dimensional Weisfeiler-Leman refinement.  The result is equitable."""
    colour = list(initial)
    while True:
        sig = [(colour[u], tuple(sorted(colour[w] for w in adj[u])))
               for u in range(len(adj))]
        order = sorted(set(sig))
        idx = {s: i for i, s in enumerate(order)}
        new = [idx[s] for s in sig]
        if len(set(new)) == len(set(colour)):
            return new
        colour = new


def cells_of(colour):
    groups = {}
    for u, c in enumerate(colour):
        groups.setdefault(c, []).append(u)
    return [tuple(groups[c]) for c in sorted(groups)]


def quotient(adj, cells):
    """Quotient matrix if the partition is equitable, else None."""
    where = {}
    for i, P in enumerate(cells):
        for u in P:
            where[u] = i
    m = len(cells)
    B = [[None] * m for _ in range(m)]
    for i, P in enumerate(cells):
        for u in P:
            cnt = [0] * m
            for w in adj[u]:
                cnt[where[w]] += 1
            for j in range(m):
                if B[i][j] is None:
                    B[i][j] = cnt[j]
                elif B[i][j] != cnt[j]:
                    return None
    return B


def equitable_partitions(adj, seed=0, extra_seeds=12):
    """A deterministic assortment of equitable partitions (never exhaustive)."""
    n = len(adj)
    rng = random.Random(seed)
    seeds = [[0] * n, list(range(n))]
    for u in range(n):
        s = [0] * n
        s[u] = 1
        seeds.append(s)
    for u, v in list(combinations(range(min(n, 6)), 2)):
        s = [0] * n
        s[u] = 1
        s[v] = 1
        seeds.append(s)
    for _ in range(extra_seeds):
        seeds.append([rng.randrange(2) for _ in range(n)])

    found, out = set(), []
    for s in seeds:
        cells = cells_of(wl_refine(adj, s))
        key = tuple(cells)
        if key in found:
            continue
        found.add(key)
        B = quotient(adj, cells)
        if check(B is not None, "WL output not equitable"):
            out.append((cells, B))
    return out


# --------------------------------------------------------------------------
# exact linear algebra over Q
# --------------------------------------------------------------------------

def rank_q(rows):
    """Exact rank of a matrix given as a list of rows of numbers."""
    M = [[Fraction(x) for x in row] for row in rows]
    if not M:
        return 0
    ncols, r = len(M[0]), 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][c]
        M[r] = [x / inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)]
            for i in range(n)]


def adjacency_matrix(adj):
    n = len(adj)
    A = [[0] * n for _ in range(n)]
    for u in range(n):
        for w in adj[u]:
            A[u][w] = 1
    return A


def shifted(A, t):
    return [[A[i][j] - (t if i == j else 0) for j in range(len(A))]
            for i in range(len(A))]


# --------------------------------------------------------------------------
# arithmetic helpers
# --------------------------------------------------------------------------

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True


def cell_size(k, j):
    """|P_j| for the distance partition of O_k from a vertex."""
    return math.comb(k - 1, j) * math.comb(k, k - 1 - j)


def alpha(k, j, eps):
    """PROOF.md Theorem 8.  Returns an exact integer; asserts divisibility."""
    q = k + 1
    num = math.comb(k - 1, j) * (math.comb(k, k - 1 - j)
                                 + (-1) ** (k - 1 - j) * (q * eps - 1))
    if num % q != 0:
        raise AssertionError(f"alpha not integral at k={k}, j={j}, eps={eps}")
    return num // q


def transport_x(k, eps_a, eps_b):
    """PROOF.md (11.1): x_i = sum_{t<=i} [ alpha_t(a) - alpha_{k-1-t}(a') ]."""
    xs, acc = [], 0
    for i in range(k):
        acc += alpha(k, i, eps_a) - alpha(k, k - 1 - i, eps_b)
        xs.append(acc)
    return xs


def transport_x_closed(k, i, eps_a, eps_b):
    """PROOF.md Theorem 11.4, equation (11.5)."""
    q = k + 1
    B = math.comb(k - 2, i) if i <= k - 2 else 0
    delta = eps_a + eps_b
    numerator = B * (
        (k - 1) * math.comb(k, i + 1)
        + k * (2 - q * delta) * ((-1) ** i)
    )
    denominator = q * k
    if numerator % denominator != 0:
        raise AssertionError(
            f"closed transport not integral at k={k}, i={i}, "
            f"eps=({eps_a},{eps_b})"
        )
    return numerator // denominator


def admissible_k(limit):
    return [k for k in range(2, limit + 1, 2) if is_prime(k + 1)]


# --------------------------------------------------------------------------
# A -- Theorem 1
# --------------------------------------------------------------------------

def part_A():
    graphs = {
        "K3": [[1, 2], [0, 2], [0, 1]],
        "C6": cycle(6),
        "Q3": hypercube(3),
        "Petersen": kneser(5, 2)[2],
        "O_4=KG(7,3)": kneser(7, 3)[2],
    }
    for name, adj in graphs.items():
        parts = equitable_partitions(adj)
        for cells_p, Bp in parts:
            for cells_s, Bs in parts:
                S = [[len(set(P) & set(Q)) for Q in cells_s] for P in cells_p]
                lhs = matmul([list(col) for col in zip(*Bp)], S)   # B_pi^T S
                rhs = matmul(S, Bs)
                check(lhs == rhs, f"A: intertwining failed on {name}")
        print(f"  A  {name}: {len(parts)} equitable partitions, "
              f"{len(parts) ** 2} ordered pairs checked")


# --------------------------------------------------------------------------
# B -- k = 2 control
# --------------------------------------------------------------------------

def part_B():
    q = 3
    verts, index, adj = kneser(3, 1)
    tau = [(i,) for i in range(3)]
    Bt = quotient(adj, tau)
    check(Bt == [[0, 1, 1], [1, 0, 1], [1, 1, 0]], "B: B_tau != J-I at k=2")
    for cells, Bp in equitable_partitions(adj):
        m = len(cells)
        T = [[Fraction(len(set(P) & set(C)), len(P)) for C in tau]
             for P in cells]
        BI = [[Bp[i][j] + (1 if i == j else 0) for j in range(m)]
              for i in range(m)]
        prod = matmul([[Fraction(x) for x in row] for row in BI], T)
        check(all(prod[i][a] == 1 for i in range(m) for a in range(q)),
              "B: (B_pi+I)T != J at k=2")
        check(all(sum(T[i]) == 1 for i in range(m)), "B: T not row stochastic")
    print("  B  k=2: perfect-code partition exists and satisfies Theorem 3")


# --------------------------------------------------------------------------
# C, D, E -- O_4
# --------------------------------------------------------------------------

def part_CDE():
    k, q = 4, 5
    verts, index, adj = kneser(7, 3)
    n = len(verts)
    A = adjacency_matrix(adj)

    # 30 * Pi_{V_3}, with V_3 the (-1)-eigenspace; spec(O_4) = {4, -3, 2, -1}
    P30 = matmul(matmul(shifted(A, 4), shifted(A, -3)), shifted(A, 2))
    denom = (-1 - 4) * (-1 + 3) * (-1 - 2)
    check(denom == 30, "C: projector denominator")
    # diagonal of Pi_{V_3} is m_3/N = 14/35 = 2/5, so 30*Pi has diagonal 12
    check(all(P30[i][i] == 12 for i in range(n)), "C: projector diagonal")

    parts = equitable_partitions(adj)
    for cells, Bp in parts:
        m = len(cells)
        BI = [[Bp[i][j] + (1 if i == j else 0) for j in range(m)]
              for i in range(m)]
        eps_alg = m - rank_q(BI)                       # multiplicity of -1

        Xp = [[1 if u in set(P) else 0 for P in cells] for u in range(n)]
        eps_geo = rank_q(matmul(P30, Xp))              # dim(U_pi ∩ V_3)
        check(eps_alg == eps_geo,
              f"C: eps mismatch {eps_alg} != {eps_geo} on O_4")

        # affine solution space of (B+I)T = J, T1 = 1 has dim eps*(q-1):
        # solve the homogeneous system in the mq unknowns Z_{ia} directly.
        # Restricted to small m so the exact elimination stays cheap.
        if m <= 12:
            rows = []
            for i in range(m):                     # (B+I) Z = 0
                for a in range(q):
                    row = [0] * (m * q)
                    for j in range(m):
                        row[j * q + a] = BI[i][j]
                    rows.append(row)
            for i in range(m):                     # Z 1_q = 0
                row = [0] * (m * q)
                for b in range(q):
                    row[i * q + b] = 1
                rows.append(row)
            nullity = m * q - rank_q(rows)
            check(nullity == eps_alg * (q - 1),
                  f"C: solution-space dim {nullity} != {eps_alg}*(q-1)")

        if eps_alg == 0:                                # Corollary 6.1
            for P in cells:
                check(len(P) % q == 0,
                      f"D: cell size {len(P)} not divisible by {q}")
    print(f"  C  O_4: {len(parts)} equitable partitions, "
          f"algebraic and geometric eps agree on all")
    print("  D  O_4: every eps=0 partition has all cell sizes divisible by 5")

    # E -- the cyclic Fano plane is a perfect code; check Theorem 8 at every M
    fano = [frozenset(((b + s) % 7 for b in (0, 1, 3))) for s in range(7)]
    C = set(index[b] for b in fano)
    check(len(C) == 7, "E: Fano plane size")
    for u in range(n):
        closed = 1 if u in C else 0
        closed += sum(1 for w in adj[u] if w in C)
        check(closed == 1, "E: (A+I)1_C != 1")
    for M in range(n):
        Mset = verts[M]
        eps = 1 if M in C else 0
        for j in range(k):
            observed = sum(1 for u in C if len(verts[u] & Mset) == j)
            check(observed == alpha(k, j, eps),
                  f"E: distance distribution mismatch at M={M}, j={j}")
        check(sum(cell_size(k, j) for j in range(k)) == n, "E: cell sizes")
    print("  E  O_4: Fano plane is a perfect code and matches Theorem 8 "
          f"at all {n} vertices")


# --------------------------------------------------------------------------
# F -- Theorems 8.1 and 11 for all admissible k <= 200
# --------------------------------------------------------------------------

def part_F(limit=200):
    violations = []
    for k in admissible_k(limit):
        q = k + 1
        N = math.comb(2 * k - 1, k - 1)
        try:
            a0 = [alpha(k, j, 0) for j in range(k)]
            a1 = [alpha(k, j, 1) for j in range(k)]
        except AssertionError as exc:
            FAILURES.append(f"F: {exc}")
            continue
        for a in (a0, a1):
            check(all(x >= 0 for x in a), f"F: negative alpha at k={k}")
            check(sum(a) * q == N, f"F: alpha total wrong at k={k}")
        check(all(a1[j] + (q - 1) * a0[j] == cell_size(k, j) for j in range(k)),
              f"F: colour sum wrong at k={k}")

        for ea, eb in ((0, 0), (1, 0), (0, 1)):
            xs = transport_x(k, ea, eb)
            bound = a1 if ea == 1 else a0
            for i, x in enumerate(xs):
                check(
                    x == transport_x_closed(k, i, ea, eb),
                    f"F: Theorem 11.4 closed form mismatch at "
                    f"k={k}, eps=({ea},{eb}), i={i}",
                )
                if not (0 <= x <= bound[i]):
                    violations.append((k, ea, eb, i, x, bound[i]))
    if violations:
        FAILURES.append(f"F: condition (11.2) VIOLATED: {violations[:10]}")
        print("  F  *** condition (11.2) violated ***")
        for v in violations[:10]:
            print("     k=%d (eps_a,eps_b)=(%d,%d) i=%d  x=%d  bound=%d" % v)
    else:
        ks = admissible_k(limit)
        print(f"  F  Theorems 8.1 and 11.3: no violation for the {len(ks)} "
              f"admissible k <= {limit} (k = {ks[0]}..{ks[-1]})")


# --------------------------------------------------------------------------
# G -- Theorem 7
# --------------------------------------------------------------------------

def part_G(limit=80):
    for k in admissible_k(limit):
        q = k + 1
        for m in range(0, k - 1):
            for j in range(0, m + 1):
                check(math.comb(2 * k - 1 - m, k - 1 - j) % q == 0,
                      f"G: Kummer divisibility failed at k={k}, m={m}, j={j}")
                check(cell_size_stab(k, m, j) % q == 0,
                      f"G: stabilizer cell size not divisible at k={k}")
    print(f"  G  Theorem 7 holds for all admissible k <= {limit}")


def cell_size_stab(k, m, j):
    return math.comb(m, j) * math.comb(2 * k - 1 - m, k - 1 - j)


# --------------------------------------------------------------------------

def main():
    print("Exact verifier for bcz_odd_graph_attack_2026-07-29")
    part_A()
    part_B()
    part_CDE()
    part_F()
    part_G()
    print()
    if FAILURES:
        print(f"RESULT: {len(FAILURES)} failure(s)")
        for f in FAILURES[:40]:
            print("  -", f)
    else:
        print("RESULT: 0 failure(s)")


if __name__ == "__main__":
    main()
