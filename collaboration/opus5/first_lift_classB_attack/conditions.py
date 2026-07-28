#!/usr/bin/env python3
"""Necessary conditions for the class-B completion problem, and exact
dynamic programs proving whether they can fire at all for a given n.

Three families, in increasing strength:

  (F)  forced-inside      sum_c max(0, s_c - h_c)  <=  C(|X|,2)
  (C)  capacity           sum_c floor(s_c/2)       >=  C(|X|,2)
       [both from Lemma 1 of results/first_lift_k13_hole/NOTE.md]

  (BC) bipartite capacity, for DISJOINT X, W:
           |X|.|W|  <=  sum_c rho_c^max,
       where rho_c^max is the largest number of X-W edges a perfect matching
       on V_c can use.  (BC) with W = A \\ X is exactly (F); (BC) with
       |X| = 1 is exactly Hall's condition at a vertex for the choice of the
       partner of each colour.  (BC) with general disjoint X,W is strictly
       more general than either.

Each left-hand side is separable over colours once (m_c, d^X_c, d^W_c) is
fixed, and the only coupling is the two linear budgets, so the exact optimum
over the RELAXED set of integer profiles is a 2-dimensional knapsack DP.  The
relaxation contains every class-B instance, so "the optimum satisfies the
condition" is a proof for all of class B; the converse direction proves
nothing by itself.
"""

from __future__ import annotations

from classb import m_profiles


# ---------------------------------------------------------------------------
def rho_max(sX, sW, z):
    """Largest number of X-W edges in a perfect matching of V_c, where V_c
    meets X in sX vertices, W in sW vertices and the rest of A in z vertices
    (sX + sW + z = |V_c| is even).

    Every pairing inside V_c is allowed, so rho can be any value in
    [0, min(sX,sW)] except that when z = 0 the leftovers sX-rho and sW-rho
    must both be matched internally, forcing rho = sX = sW (mod 2).
    """
    hi = min(sX, sW)
    if z == 0 and ((sX - hi) % 2):
        hi -= 1
    return max(hi, 0)


def bc_min(n, x, w, prof):
    """Exact minimum of sum_c rho_c^max over the relaxation

        sum_c dX_c = 5x,  sum_c dW_c = 5w,
        max(0, m_c - (n-x)) <= dX_c <= min(m_c, x),
        max(0, m_c - (n-w)) <= dW_c <= min(m_c, w),
        dX_c + dW_c <= m_c,
        m_c - dX_c - dW_c <= n - x - w.

    Every class-B instance and every pair of disjoint X, W with |X|=x, |W|=w
    satisfies all of these, so the value returned is a valid lower bound for
    every instance.
    """
    INF = 10 ** 9
    bx, bw = 5 * x, 5 * w
    cur = [[INF] * (bw + 1) for _ in range(bx + 1)]
    cur[0][0] = 0
    for cnt, m in zip(prof, (5, 3, 1)):
        if not cnt:
            continue
        opts = []
        for dX in range(max(0, m - (n - x)), min(m, x) + 1):
            for dW in range(max(0, m - (n - w)), min(m, w) + 1):
                if dX + dW > m:
                    continue
                if m - dX - dW > n - x - w:
                    continue
                sX, sW = x - dX, w - dW
                z = (n - m) - sX - sW
                if z < 0:
                    continue
                opts.append((dX, dW, rho_max(sX, sW, z)))
        for _ in range(cnt):
            nxt = [[INF] * (bw + 1) for _ in range(bx + 1)]
            for i in range(bx + 1):
                rowi = cur[i]
                for j in range(bw + 1):
                    v = rowi[j]
                    if v == INF:
                        continue
                    for (dX, dW, r) in opts:
                        ii, jj = i + dX, j + dW
                        if ii <= bx and jj <= bw and v + r < nxt[ii][jj]:
                            nxt[ii][jj] = v + r
            cur = nxt
    return cur[bx][bw]


def bc_margin(n, verbose=False):
    """max over (x, w, profile) of  x*w - bc_min  ;  <= 0 proves (BC) never
    fires for any class-B instance with this n."""
    best = None
    for x in range(1, n):
        for w in range(1, n - x + 1):
            for prof in m_profiles(n):
                v = x * w - bc_min(n, x, w, prof)
                if best is None or v > best[0]:
                    best = (v, x, w, prof)
                if verbose and v > 0:
                    print("   (BC) can fire: x=%d w=%d prof=%s margin=%+d"
                          % (x, w, prof, v))
    return best


# ---------------------------------------------------------------------------
# instance-level checks
# ---------------------------------------------------------------------------
def bc_violations(n, q, forb, xmax=None):
    """All violated (BC) conditions of an actual instance (exponential; use
    only for small n or for a spot check)."""
    V = []
    for c in range(q):
        mask = 0
        for a in range(n):
            if not ((forb[a] >> c) & 1):
                mask |= 1 << a
        V.append(mask)
    out = []
    full = (1 << n) - 1
    for xm in range(1, 1 << n):
        rest = full & ~xm
        sub = rest
        while sub:
            wm = sub
            sub = (sub - 1) & rest
            x, w = bin(xm).count("1"), bin(wm).count("1")
            if xmax and (x > xmax or w > xmax):
                continue
            tot = 0
            for c in range(q):
                sX = bin(V[c] & xm).count("1")
                sW = bin(V[c] & wm).count("1")
                z = bin(V[c]).count("1") - sX - sW
                tot += rho_max(sX, sW, z)
            if tot < x * w:
                out.append((tuple(i for i in range(n) if (xm >> i) & 1),
                            tuple(i for i in range(n) if (wm >> i) & 1),
                            tot, x * w))
    return out


def vertex_hall(n, q, forb):
    """Hall's condition at each vertex: the bipartite graph between the 12
    colours available at a and the 12 other vertices (c ~ b iff b in V_c) must
    have a perfect matching.  Returns the list of violating (a, colour set)."""
    bad = []
    for a in range(n):
        cols = [c for c in range(q) if not ((forb[a] >> c) & 1)]
        adj = {}
        for c in cols:
            adj[c] = set(b for b in range(n) if b != a and not ((forb[b] >> c) & 1))
        matchR = {}

        def aug(u, seen):
            for v in adj[u]:
                if v in seen:
                    continue
                seen.add(v)
                if v not in matchR or aug(matchR[v], seen):
                    matchR[v] = u
                    return True
            return False

        for c in cols:
            if not aug(c, set()):
                bad.append((a, c))
    return bad


# ---------------------------------------------------------------------------
# (PART): the amalgamation / partition condition
# ---------------------------------------------------------------------------
def partition_feasible(n, q, forb, parts):
    """Necessary condition (PART).  Amalgamate A along the partition `parts`
    into k super-vertices.  For each colour c write v_i = |V_c cap P_i|; if the
    matchings exist then for every c there are integers rho_ij(c) >= 0
    (the number of M_c edges between P_i and P_j) with

        sum_{j != i} rho_ij(c) <= v_i   and   v_i - sum_j rho_ij(c) even,

    and, globally, sum_c rho_ij(c) = |P_i| |P_j| for all i < j.  (The counts of
    edges inside the parts are then automatic: they come out as C(|P_i|,2).)

    Returns True if such a choice exists, False if not.  False is a rigorous
    proof that no completion exists.  Exact DP over the k(k-1)/2 cross totals.
    """
    k = len(parts)
    idx = [(i, j) for i in range(k) for j in range(i + 1, k)]
    target = tuple(len(parts[i]) * len(parts[j]) for (i, j) in idx)
    V = [set(a for a in range(n) if not ((forb[a] >> c) & 1)) for c in range(q)]
    # per-colour option sets
    opts = []
    for c in range(q):
        v = [len(V[c] & set(P)) for P in parts]
        cur = []

        def rec(t, rho, rem):
            if t == len(idx):
                for i in range(k):
                    if rem[i] % 2:
                        return
                cur.append(tuple(rho))
                return
            i, j = idx[t]
            hi = min(rem[i], rem[j])
            for x in range(hi + 1):
                rem[i] -= x
                rem[j] -= x
                rho.append(x)
                rec(t + 1, rho, rem)
                rho.pop()
                rem[i] += x
                rem[j] += x
        rec(0, [], list(v))
        if not cur:
            return False
        opts.append(cur)
    reach = {tuple([0] * len(idx))}
    for c in range(q):
        nxt = set()
        for s in reach:
            for o in opts[c]:
                t = tuple(a + b for a, b in zip(s, o))
                if all(t[i] <= target[i] for i in range(len(idx))):
                    nxt.add(t)
        reach = nxt
        if not reach:
            return False
    return target in reach


def random_partitions(n, k, rng, count):
    out = []
    for _ in range(count):
        lab = [rng.randrange(k) for _ in range(n)]
        parts = [[a for a in range(n) if lab[a] == i] for i in range(k)]
        if all(parts):
            out.append(parts)
    return out
