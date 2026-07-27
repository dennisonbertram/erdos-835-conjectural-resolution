#!/usr/bin/env python3
"""First-lift K_{k-3}-hole completion: exact library.

Standard library only.  No search heuristics are used for any claim that is
stated as proved: every proved statement here is either an exact exhaustive
enumeration, an exact dynamic program over a stated relaxation, or an explicit
certificate that is re-checked from its definition.

Setting (Section 3 of collaboration/unrestricted_lift_tower/NOTE.md, written
for general even k; the note itself is the k=16 case).

    U  = k+3 points        A = k-3 points = n vertices of the hole
    C  = k+1 colours = q   P = a fixed 5-subset of U
    n  = k-3  (odd),  q = n+4

For a fixed P the level-1 tower law asks for a proper edge colouring
h_P of K_A in which the set of colours *missing* at a in A is exactly

    S_a(P) = { F_a(P \\ {x}) : x in P }        (|S_a| = 5)

equivalently, for each colour c a perfect matching M_c on

    V_c = { a in A : c not in S_a },   |V_c| = n - m_c,  m_c = #{a : c in S_a}

with the seventeen (in general q) matchings partitioning E(K_A).

Three nested instance classes are used throughout, and are kept strictly
apart:

  class A  ("arbitrary even support")
        any 0/1 matrix with row sums 5 and every |V_c| even.
  class B  ("column-bounded")
        class A and additionally m_c <= 5 for every colour.  By Koenig's
        theorem this is exactly the set of matrices that decompose into five
        A-saturating matchings, i.e. that admit *some* 13x5 array of the
        shape required by equation (8) of the note.
  class B' ("locally fan-consistent")
        class B and additionally the five missed-colour 4-sets D_x of such a
        decomposition are the face-colour sets of an actual proper colouring
        L of the ten triples of P.  This is exactly the local data that a
        simultaneous fan induces at the single five-set P.

  class C  ("simultaneous-fan realisable") is contained in class B', and is
        NOT sampled anywhere in this file: no simultaneous fan is known to
        exist, so class C is not known to be non-empty.
"""

from __future__ import annotations

import random
from collections import Counter

PAIRS5 = [(x, y) for x in range(5) for y in range(5) if x < y]


# --------------------------------------------------------------------------
# basic instance arithmetic
# --------------------------------------------------------------------------
def supports(n, q, forb):
    """|V_c| for every colour c."""
    return [n - sum((forb[a] >> c & 1) for a in range(n)) for c in range(q)]


def m_profile(n, q, forb):
    """Counter of m_c = n - |V_c| over the q colours."""
    return Counter(n - v for v in supports(n, q, forb))


def check_instance_shape(n, q, forb):
    """Assert the defining arithmetic of a class-A instance; return |V_c|."""
    assert q == n + 4, (n, q)
    assert n % 2 == 1
    for a in range(n):
        assert bin(forb[a]).count("1") == 5, ("row sum", a)
        assert forb[a] < (1 << q)
    v = supports(n, q, forb)
    assert sum(v) == n * (n - 1), (sum(v), n * (n - 1))
    assert sum(v) // 2 == n * (n - 1) // 2
    for c in range(q):
        assert v[c] % 2 == 0, ("odd support", c, v[c])
    return v


def in_class_B(n, q, forb):
    """m_c <= 5 for every colour (equivalently every |V_c| >= n-5)."""
    return all(n - v <= 5 for v in supports(n, q, forb))


# --------------------------------------------------------------------------
# the two cut conditions  (Lemma 1 of the NOTE)
# --------------------------------------------------------------------------
def cut_certificates(n, q, forb, only_first=False):
    """All violated cut conditions.

    For X subset of A, with s_c = |V_c cap X| and h_c = |V_c|/2:

        forced(X)   = sum_c max(0, s_c - h_c)  <=  C(|X|,2)
        capacity(X) = sum_c floor(s_c / 2)     >=  C(|X|,2)

    Both are necessary for a completion to exist (proof in NOTE.md Lemma 1).
    Returns a list of ('forced'|'capacity', X, value, C(|X|,2)).
    """
    Vmask = []
    half = []
    for c in range(q):
        mask = 0
        for a in range(n):
            if not (forb[a] >> c & 1):
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
            d = s - half[c]
            if d > 0:
                lo += d
            hi += s >> 1
        if lo > cap:
            out.append(("forced", tuple(i for i in range(n) if xm >> i & 1), lo, cap))
            if only_first:
                return out
        if hi < cap:
            out.append(("capacity", tuple(i for i in range(n) if xm >> i & 1), hi, cap))
            if only_first:
                return out
    return out


# --------------------------------------------------------------------------
# exact bound: can a cut condition fire at all, for a given n?
# --------------------------------------------------------------------------
def m_profiles(n):
    """All (n5,n3,n1) with 5*n5+3*n3+1*n1 = 5n and n5+n3+n1 = n+4.

    These are exactly the possible multiplicity profiles of a class-B
    instance: sum_c m_c = 5n because every row sum is 5, m_c is odd because
    |V_c| = n - m_c is even, and m_c <= 5 is the class-B condition.
    """
    q = n + 4
    out = []
    for a in range(q + 1):
        for b in range(q + 1 - a):
            c = q - a - b
            if 5 * a + 3 * b + c == 5 * n:
                out.append((a, b, c))
    return out


def _dp(n, x, prof, value, better, worst):
    """Exact optimum of sum_c value(m_c,d_c) over integer d-profiles with
    sum_c d_c = 5x and max(0, m_c-(n-x)) <= d_c <= min(m_c, x).

    d_c = #{a in X : c in S_a}; the stated box and the sum are exactly the
    constraints that hold for every class-B instance and every X with |X|=x,
    so this is a relaxation of the achievable d-profiles.  An optimum that
    satisfies a necessary condition therefore PROVES that no class-B instance
    violates it; an optimum that violates it proves nothing by itself.
    """
    budget = 5 * x
    cur = [worst] * (budget + 1)
    cur[0] = 0
    for cnt, m in zip(prof, (5, 3, 1)):
        if not cnt:
            continue
        lo = max(0, m - (n - x))
        hi = min(m, x)
        vals = [(d, value(m, d)) for d in range(lo, hi + 1)]
        for _ in range(cnt):
            nxt = [worst] * (budget + 1)
            for cost in range(budget + 1):
                if cur[cost] == worst:
                    continue
                base = cur[cost]
                for d, v in vals:
                    t = cost + d
                    if t <= budget:
                        cand = base + v
                        if better(cand, nxt[t]):
                            nxt[t] = cand
            cur = nxt
    return cur[budget]


def max_forced(n, x, prof):
    """Exact max of sum_c max(0, s_c - h_c) over the relaxation above."""
    return _dp(
        n,
        x,
        prof,
        lambda m, d: max(0, x - d - (n - m) // 2),
        lambda a, b: a > b,
        -(10**9),
    )


def min_capacity(n, x, prof):
    """Exact min of sum_c floor(s_c/2) over the relaxation above."""
    return _dp(n, x, prof, lambda m, d: (x - d) // 2, lambda a, b: a < b, 10**9)


def cut_margins(n):
    """max over (x, profile) of the amount by which each cut condition can be
    violated.  A value <= 0 is a proof that the condition never fires."""
    bestF = bestC = None
    for x in range(1, n + 1):
        cap = x * (x - 1) // 2
        for prof in m_profiles(n):
            f = max_forced(n, x, prof) - cap
            c = cap - min_capacity(n, x, prof)
            if bestF is None or f > bestF[0]:
                bestF = (f, x, prof)
            if bestC is None or c > bestC[0]:
                bestC = (c, x, prof)
    return bestF, bestC


# --------------------------------------------------------------------------
# exact completion solver (complete search; UNSAT is a proof)
# --------------------------------------------------------------------------
def solve(n, q, forb, node_budget=None):
    """Exact search.  Returns ('SAT', colouring, nodes) / ('UNSAT', None, nodes)
    / ('BUDGET', None, nodes).  Branching is on the item (open edge, or
    (vertex,colour) slot) with fewest candidates, so 'UNSAT' is exhaustive."""
    FULL = (1 << q) - 1
    avail = [FULL & ~forb[a] for a in range(n)]
    for a in range(n):
        if bin(avail[a]).count("1") != n - 1:
            raise ValueError(
                "palette at vertex %d has size %d, need %d"
                % (a, bin(avail[a]).count("1"), n - 1)
            )
    open_nbrs = [set(b for b in range(n) if b != a) for a in range(n)]
    assign = {}
    out = []
    nodes = [0]

    def rec():
        nodes[0] += 1
        if node_budget is not None and nodes[0] > node_budget:
            raise TimeoutError
        best = None
        any_open = False
        for a in range(n):
            for b in open_nbrs[a]:
                if b < a:
                    continue
                any_open = True
                m = avail[a] & avail[b]
                if m == 0:
                    return False
                cnt = bin(m).count("1")
                if best is None or cnt < best[0]:
                    best = (cnt, "e", (a, b, m))
                    if cnt == 1:
                        break
            if best is not None and best[0] == 1:
                break
        if not any_open:
            out.append(dict(assign))
            return True
        if best[0] > 1:
            for a in range(n):
                m = avail[a]
                while m:
                    lb = m & -m
                    c = lb.bit_length() - 1
                    m ^= lb
                    cnt = 0
                    for b in open_nbrs[a]:
                        if avail[b] >> c & 1:
                            cnt += 1
                            if cnt >= best[0]:
                                break
                    if cnt == 0:
                        return False
                    if cnt < best[0]:
                        best = (cnt, "v", (a, c))
                        if cnt == 1:
                            break
                if best[0] == 1:
                    break
        if best[1] == "e":
            a, b, m = best[2]
            bits = []
            while m:
                lb = m & -m
                bits.append(lb)
                m ^= lb
            for lb in bits:
                c = lb.bit_length() - 1
                avail[a] ^= lb
                avail[b] ^= lb
                open_nbrs[a].discard(b)
                open_nbrs[b].discard(a)
                assign[(a, b)] = c
                if rec():
                    return True
                del assign[(a, b)]
                open_nbrs[a].add(b)
                open_nbrs[b].add(a)
                avail[a] ^= lb
                avail[b] ^= lb
            return False
        a, c = best[2]
        lb = 1 << c
        for b in list(open_nbrs[a]):
            if not (avail[b] >> c & 1):
                continue
            avail[a] ^= lb
            avail[b] ^= lb
            open_nbrs[a].discard(b)
            open_nbrs[b].discard(a)
            e = (a, b) if a < b else (b, a)
            assign[e] = c
            if rec():
                return True
            del assign[e]
            open_nbrs[a].add(b)
            open_nbrs[b].add(a)
            avail[a] ^= lb
            avail[b] ^= lb
        return False

    try:
        ok = rec()
    except TimeoutError:
        return ("BUDGET", None, nodes[0])
    return ("SAT", out[0], nodes[0]) if ok else ("UNSAT", None, nodes[0])


def solve_randomised(n, q, forb, seed=0, restarts=400, cutoff=100_000):
    """Randomised-restart wrapper around the same complete search.

    Needed because the deterministic value ordering of solve() is pathological
    on some highly symmetric SATISFIABLE instances: it can exhaust a large node
    budget without finding a completion that random value ordering finds in a
    few dozen nodes.  A 'BUDGET' answer from solve() is therefore never
    evidence of infeasibility.  If any restart finishes without hitting the
    cutoff, its verdict is exhaustive and final.
    """
    rng = random.Random(seed)
    FULL = (1 << q) - 1
    for r in range(restarts):
        avail = [FULL & ~forb[a] for a in range(n)]
        open_nbrs = [set(b for b in range(n) if b != a) for a in range(n)]
        assign = {}
        nodes = [0]

        def rec():
            nodes[0] += 1
            if nodes[0] > cutoff:
                raise TimeoutError
            best = None
            any_open = False
            for a in range(n):
                for b in open_nbrs[a]:
                    if b < a:
                        continue
                    any_open = True
                    m = avail[a] & avail[b]
                    if m == 0:
                        return False
                    cnt = bin(m).count("1")
                    if best is None or cnt < best[0]:
                        best = (cnt, "e", (a, b, m))
                        if cnt == 1:
                            break
                if best is not None and best[0] == 1:
                    break
            if not any_open:
                return True
            if best[0] > 1:
                for a in range(n):
                    m = avail[a]
                    while m:
                        lb = m & -m
                        c = lb.bit_length() - 1
                        m ^= lb
                        cnt = 0
                        for b in open_nbrs[a]:
                            if avail[b] >> c & 1:
                                cnt += 1
                                if cnt >= best[0]:
                                    break
                        if cnt == 0:
                            return False
                        if cnt < best[0]:
                            best = (cnt, "v", (a, c))
                            if cnt == 1:
                                break
                    if best[0] == 1:
                        break
            if best[1] == "e":
                a, b, m = best[2]
                bits = []
                while m:
                    lb = m & -m
                    bits.append(lb)
                    m ^= lb
                rng.shuffle(bits)
                for lb in bits:
                    c = lb.bit_length() - 1
                    avail[a] ^= lb
                    avail[b] ^= lb
                    open_nbrs[a].discard(b)
                    open_nbrs[b].discard(a)
                    assign[(a, b)] = c
                    if rec():
                        return True
                    del assign[(a, b)]
                    open_nbrs[a].add(b)
                    open_nbrs[b].add(a)
                    avail[a] ^= lb
                    avail[b] ^= lb
                return False
            a, c = best[2]
            lb = 1 << c
            bs = [b for b in open_nbrs[a] if avail[b] >> c & 1]
            rng.shuffle(bs)
            for b in bs:
                avail[a] ^= lb
                avail[b] ^= lb
                open_nbrs[a].discard(b)
                open_nbrs[b].discard(a)
                e = (a, b) if a < b else (b, a)
                assign[e] = c
                if rec():
                    return True
                del assign[e]
                open_nbrs[a].add(b)
                open_nbrs[b].add(a)
                avail[a] ^= lb
                avail[b] ^= lb
            return False

        try:
            ok = rec()
        except TimeoutError:
            continue
        return ("SAT", dict(assign), r) if ok else ("UNSAT", None, r)
    return ("RESTARTS_EXHAUSTED", None, restarts)


def check_completion(n, q, forb, sol):
    """Re-check a claimed completion from the definition."""
    FULL = (1 << q) - 1
    assert len(sol) == n * (n - 1) // 2, len(sol)
    used = [0] * n
    for (a, b), c in sol.items():
        assert 0 <= a < b < n
        assert not (forb[a] >> c & 1) and not (forb[b] >> c & 1)
        assert not (used[a] >> c & 1) and not (used[b] >> c & 1)
        used[a] |= 1 << c
        used[b] |= 1 << c
    for a in range(n):
        assert used[a] == FULL & ~forb[a]
    return True


# --------------------------------------------------------------------------
# class-B' generation:  L on the ten triples of P  ->  D_x  ->  the array
# --------------------------------------------------------------------------
def link_partitions():
    """All partitions of E(K_5) into matchings (parts of size 1 or 2).

    Complementation T <-> P\\T turns the ten triples of P into the ten pairs
    of P; two triples of P meet in exactly one point iff their complementary
    pairs are disjoint.  So a proper colouring L of the ten triples (triples
    sharing a pair get different colours, forced because every colour class of
    an LS(2,3,|U|) is a partial Steiner system) is exactly such a partition.
    """
    seen = set()
    res = []

    def rec(rem, parts):
        if not rem:
            key = tuple(sorted(tuple(sorted(p)) for p in parts))
            if key not in seen:
                seen.add(key)
                res.append([tuple(p) for p in parts])
            return
        p = rem[0]
        rest = rem[1:]
        rec(rest, parts + [(p,)])
        for q in rest:
            if not (set(p) & set(q)):
                rec([r for r in rest if r != q], parts + [(p, q)])

    rec(list(PAIRS5), [])
    return res


def Dx_from_parts(parts, colours):
    """D_x = { L(T) : T a triple inside P\\{x} }, computed from the partition."""
    Dx = [set() for _ in range(5)]
    tvec = {}
    for col, part in zip(colours, parts):
        tvec[col] = len(part)
        for x, y in part:
            Dx[x].add(col)
            Dx[y].add(col)
    assert all(len(d) == 4 for d in Dx), [len(d) for d in Dx]
    return [frozenset(d) for d in Dx], tvec


def _aug(u, adj, seen, matchR, matchL, rng):
    cand = list(adj[u])
    if rng:
        rng.shuffle(cand)
    for v in cand:
        if seen[v]:
            continue
        seen[v] = True
        if matchR[v] == -1 or _aug(matchR[v], adj, seen, matchR, matchL, rng):
            matchR[v] = u
            matchL[u] = v
            return True
    return False


def perfect_matching(adj, nleft, nright, rng=None):
    matchR = [-1] * nright
    matchL = [-1] * nleft
    order = list(range(nleft))
    if rng:
        rng.shuffle(order)
    for u in order:
        if not _aug(u, adj, [False] * nright, matchR, matchL, rng):
            return None
    return matchL


def array_from_Dx(n, q, Dx, rng, tries=60):
    """Build the n x 5 array: column x is a bijection A -> C \\ D_x, rows
    all-distinct.  Returns (forb, array) or None."""
    for _ in range(tries):
        used = [0] * n
        arr = [[None] * 5 for _ in range(n)]
        order = list(range(5))
        rng.shuffle(order)
        ok = True
        for x in order:
            cols = sorted(set(range(q)) - set(Dx[x]))
            assert len(cols) == n
            adj = [
                [i for i, c in enumerate(cols) if not (used[a] >> c & 1)]
                for a in range(n)
            ]
            mm = perfect_matching(adj, n, len(cols), rng)
            if mm is None:
                ok = False
                break
            for a in range(n):
                c = cols[mm[a]]
                arr[a][x] = c
                used[a] |= 1 << c
        if ok:
            return used, arr
    return None


def check_class_Bprime(n, q, forb, arr, parts, colours):
    """Re-check, from the definitions, that (arr, parts, colours) witnesses
    membership of forb in class B'."""
    Dx, tvec = Dx_from_parts(parts, colours)
    # the partition really is a partition of E(K_5) into matchings
    flat = [p for part in parts for p in part]
    assert sorted(flat) == sorted(PAIRS5), "not a partition of E(K_5)"
    for part in parts:
        assert 1 <= len(part) <= 2
        if len(part) == 2:
            assert not (set(part[0]) & set(part[1])), "part is not a matching"
    assert len(set(colours)) == len(colours) == len(parts)
    # each column is a bijection onto C \ D_x
    for x in range(5):
        col = [arr[a][x] for a in range(n)]
        assert len(set(col)) == n
        assert set(col) == set(range(q)) - set(Dx[x]), "column %d image" % x
    # rows are 5 distinct colours and reproduce forb
    for a in range(n):
        assert len(set(arr[a])) == 5
        m = 0
        for c in arr[a]:
            m |= 1 << c
        assert m == forb[a], ("row %d" % a, m, forb[a])
    return True


def random_class_Bprime(n, q, rng, parts_pool):
    parts = rng.choice(parts_pool)
    colours = rng.sample(range(q), len(parts))
    Dx, tvec = Dx_from_parts(parts, colours)
    got = array_from_Dx(n, q, Dx, rng)
    if got is None:
        return None
    forb, arr = got
    return dict(forb=forb, arr=arr, parts=parts, colours=colours, Dx=Dx)


# --------------------------------------------------------------------------
# explicit counterexample family
# --------------------------------------------------------------------------
def counterexample_n11():
    """Closed-form class-B' counterexample at n=11 (k=14), with its witness.

    A = X (6) + Y (5).  Colours: four c's forbidden by every vertex of Y (so
    V_c = X, and each such colour must be a perfect matching on X: 3 edges),
    six g_j indexed by X with S_a = {g_i : i != a} for a in X (so
    V_{g_j} = Y + {j}), and five e_a with S_a = {c_0..c_3, e_a} for a in Y
    (so V_{e_a} = A - {a}).

        forced(X) = 4*3 + 5*1 = 17 > 15 = C(6,2)
        forced(Y) = 6*2       = 12 > 10 = C(5,2)

    Returns (n, q, forb, arr, parts, colours).
    """
    n, q = 11, 15
    X = list(range(6))
    Y = list(range(6, 11))
    CC = [0, 1, 2, 3]
    G = [4, 5, 6, 7, 8, 9]
    E = [10, 11, 12, 13, 14]
    forb = [0] * n
    for j, a in enumerate(X):
        for i, g in enumerate(G):
            if i != j:
                forb[a] |= 1 << g
    for i, a in enumerate(Y):
        for c in CC + [E[i]]:
            forb[a] |= 1 << c
    # ---- class-B' witness --------------------------------------------
    # L = the rotational near-one-factorisation of K_5:
    #     F_x = {{x+1,x+4},{x+2,x+3}} (mod 5) is a matching missing x,
    # and colour e_{Y[x]} carries F_x, so D_x = E \ {e_{Y[x]}}.
    parts = []
    for x in range(5):
        parts.append(
            (
                tuple(sorted(((x + 1) % 5, (x + 4) % 5))),
                tuple(sorted(((x + 2) % 5, (x + 3) % 5))),
            )
        )
    colours = E[:]
    arr = [[None] * 5 for _ in range(n)]
    for x in range(5):
        # Y block: vertex Y[x] takes its own e; Y[i] (i != x) takes the c
        # indexed by the nonzero shift (i-x) mod 5, a fixed-point-free
        # decomposition of the off-diagonal of a 5x5 array.
        arr[Y[x]][x] = E[x]
        for i in range(5):
            if i != x:
                arr[Y[i]][x] = CC[(i - x) % 5 - 1]
        # X block: shift by x+1 mod 6, fixed-point free, so row X[j] never
        # receives g_j and receives the other five g's once each.
        for j in range(6):
            arr[X[j]][x] = G[(j + x + 1) % 6]
    return n, q, forb, arr, parts, colours
