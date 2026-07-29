#!/usr/bin/env python3
"""The two-parameter family, and the (BC) dynamic program for it.

Parameters (n, r):  |A| = n, |S_a| = r for every a, q = n + r - 1 colours,
m_c = #{a : c in S_a} <= r, and |V_c| = n - m_c even (so m_c = n mod 2).
The class-B question of the prompt is (n, r) = (13, 5).

mu := n - r is the minimum possible support |V_c|.  Peeling one vertex
(Proposition P of NOTE.md) maps (n, r) to (n-1, r+1), i.e. it lowers mu by 2
and keeps q fixed.
"""

from __future__ import annotations


def profiles(n, r):
    """All multiplicity profiles: the number of colours with m_c = v for each
    v in {r, r-2, ...} down to 1 or 2, with sum_c m_c = r n and q = n+r-1
    colours."""
    q = n + r - 1
    top = r if (r - n) % 2 == 0 else r - 1
    vals = [v for v in range(top, -1, -2)]   # m_c = 0 is legitimate when n is even
    out = []

    def rec(i, left_cols, left_sum, acc):
        if i == len(vals):
            if left_cols == 0 and left_sum == 0:
                out.append(tuple(acc))
            return
        v = vals[i]
        if i == len(vals) - 1:
            if v == 0:
                if left_sum == 0:
                    out.append(tuple(acc + [left_cols]))
            elif left_sum % v == 0 and left_sum // v == left_cols:
                out.append(tuple(acc + [left_cols]))
            return
        for k in range(left_cols + 1):
            if k * v > left_sum:
                break
            rec(i + 1, left_cols - k, left_sum - k * v, acc + [k])
    rec(0, q, r * n, [])
    return vals, out


def rho_max(sX, sW, z):
    hi = min(sX, sW)
    if z == 0 and ((sX - hi) % 2):
        hi -= 1
    return max(hi, 0)


def rho_min(sX, sW, z):
    return 1 if (z == 0 and (sX % 2)) else 0


def _dp(n, r, x, w, vals, prof, valfun, better, worst):
    bx, bw = r * x, r * w
    cur = [[worst] * (bw + 1) for _ in range(bx + 1)]
    cur[0][0] = 0
    for cnt, m in zip(prof, vals):
        if not cnt:
            continue
        opts = []
        for dX in range(max(0, m - (n - x)), min(m, x) + 1):
            for dW in range(max(0, m - (n - w)), min(m, w) + 1):
                if dX + dW > m or m - dX - dW > n - x - w:
                    continue
                sX, sW = x - dX, w - dW
                z = (n - m) - sX - sW
                if z < 0:
                    continue
                opts.append((dX, dW, valfun(sX, sW, z)))
        if not opts:
            return worst
        for _ in range(cnt):
            nxt = [[worst] * (bw + 1) for _ in range(bx + 1)]
            for i in range(bx + 1):
                rowi = cur[i]
                for j in range(bw + 1):
                    v = rowi[j]
                    if v == worst:
                        continue
                    for (dX, dW, val) in opts:
                        ii, jj = i + dX, j + dW
                        if ii <= bx and jj <= bw and better(v + val, nxt[ii][jj]):
                            nxt[ii][jj] = v + val
            cur = nxt
    return cur[bx][bw]


def bc_margin(n, r):
    """max over (x, w, profile) of the amount by which the upper (BC) bound or
    its lower companion can be violated.  <= 0 proves neither ever fires."""
    INF = 10 ** 9
    vals, profs = profiles(n, r)
    bestU = bestL = None
    for x in range(1, n):
        for w in range(1, n - x + 1):
            for prof in profs:
                u = _dp(n, r, x, w, vals, prof, rho_max,
                        lambda a, b: a < b, INF)
                if u < INF and (bestU is None or x * w - u > bestU[0]):
                    bestU = (x * w - u, x, w, prof)
                l = _dp(n, r, x, w, vals, prof, rho_min,
                        lambda a, b: a > b, -INF)
                if l > -INF and (bestL is None or l - x * w > bestL[0]):
                    bestL = (l - x * w, x, w, prof)
    return bestU, bestL


if __name__ == "__main__":
    print("(BC) worst margins; a positive margin means the condition CAN be")
    print("violated somewhere in the relaxation, <= 0 is a proof that it never")
    print("fires.  mu = n - r is the minimum support size.")
    print()
    print("%3s %3s %3s %4s | %8s %8s" % ("n", "r", "mu", "q", "upper", "lower"))
    rows = []
    for r in range(3, 11):
        for n in range(r + 1, 20):
            if n - r < 2 or n + r - 1 > 21:
                continue
            if not profiles(n, r)[1]:
                continue
            u, l = bc_margin(n, r)
            print("%3d %3d %3d %4d | %+8d %+8d" % (n, r, n - r, n + r - 1,
                                                   u[0], l[0]))


# ---------------------------------------------------------------------------
# instance generation for general (n, r)
# ---------------------------------------------------------------------------
def random_instance(n, r, rng, prof=None):
    vals, profs = profiles(n, r)
    if not profs:
        return None
    if prof is None:
        prof = rng.choice(profs)
    ms = []
    for cnt, v in zip(prof, vals):
        ms += [v] * cnt
    q = n + r - 1
    assert len(ms) == q
    rng.shuffle(ms)
    for _ in range(200):
        forb = [0] * n
        rowrem = [r] * n
        order = sorted(range(q), key=lambda c: -ms[c])
        ok = True
        for c in order:
            cand = [a for a in range(n) if rowrem[a] > 0]
            if len(cand) < ms[c]:
                ok = False
                break
            rng.shuffle(cand)
            cand.sort(key=lambda a: -rowrem[a])
            for a in cand[:ms[c]]:
                forb[a] |= 1 << c
                rowrem[a] -= 1
        if ok and all(t == 0 for t in rowrem):
            return forb
    return None


def check_instance(n, r, forb):
    q = n + r - 1
    for a in range(n):
        assert bin(forb[a]).count("1") == r, "row sum"
    for c in range(q):
        m = sum((forb[a] >> c) & 1 for a in range(n))
        assert m <= r and (n - m) % 2 == 0, ("column", c, m)
    return True


def random_move(n, r, forb, rng):
    q = n + r - 1

    def mc(f, c):
        return sum((f[a] >> c) & 1 for a in range(n))
    for _ in range(80):
        a, b = rng.sample(range(n), 2)
        if rng.random() < 0.35:
            both_in = [c for c in range(q) if (forb[a] >> c) & 1 and (forb[b] >> c) & 1]
            both_out = [c for c in range(q)
                        if not ((forb[a] >> c) & 1) and not ((forb[b] >> c) & 1)]
            if not both_in or not both_out:
                continue
            cp, c = rng.choice(both_in), rng.choice(both_out)
            if mc(forb, c) + 2 > r or mc(forb, cp) - 2 < 0:
                continue
            new = list(forb)
            new[a] = (new[a] & ~(1 << cp)) | (1 << c)
            new[b] = (new[b] & ~(1 << cp)) | (1 << c)
            return new
        ca = [c for c in range(q) if (forb[a] >> c) & 1 and not ((forb[b] >> c) & 1)]
        cb = [c for c in range(q) if (forb[b] >> c) & 1 and not ((forb[a] >> c) & 1)]
        if not ca or not cb:
            continue
        c, cp = rng.choice(ca), rng.choice(cb)
        new = list(forb)
        new[a] = (new[a] & ~(1 << c)) | (1 << cp)
        new[b] = (new[b] & ~(1 << cp)) | (1 << c)
        return new
    return None
