#!/usr/bin/env python3
"""Decide Corollary F of NOTE.md: does the seventeen-row certificate instance
of Theorem D have a full 17-matching completion?

NOT EXECUTED in the session that wrote it (no interpreter was available).
Nothing in NOTE.md depends on its output; it decides only which branch of the
stated dichotomy holds.

Output is `COMPLETES` (with an explicit witness printed) or `NO COMPLETION`.
The search is a complete depth-first exact cover: it either exhibits a
completion or exhausts the whole space.

Standard library only.  Deterministic (no randomness, fixed tie-breaking).
"""

import itertools
import sys

Z5 = range(5)
E = [("e", i) for i in Z5]
F = [("f", i) for i in Z5]
V = E + F
X, Y, Zt = ("t", 0), ("t", 1), ("t", 2)
A = [X, Y, Zt] + V
IDX = {a: k for k, a in enumerate(A)}


def ed(u, v):
    return (u, v) if IDX[u] < IDX[v] else (v, u)


ALL = [ed(u, v) for u, v in itertools.combinations(A, 2)]


def e(i):
    return ("e", i % 5)


def f(i):
    return ("f", i % 5)


# ---- the seventeen prescribed complements, exactly as in NOTE.md (5.4) ----
ROWS = (
    [frozenset([X]), frozenset([Y]), frozenset([Zt])]
    + [frozenset([X, Y, Zt])] * 4
    + [frozenset([f(i + 3), f(i + 4), e(i + 2), e(i + 3), e(i + 4)]) for i in Z5]
    + [frozenset([e(i + 3), e(i + 4), f(i + 1), f(i + 3), f(i + 4)]) for i in Z5]
)
SUPPORTS = [tuple(sorted((set(A) - b), key=lambda a: IDX[a])) for b in ROWS]


def sanity():
    assert len(ROWS) == 17
    assert all(len(b) in (1, 3, 5) for b in ROWS)
    assert all(sum(1 for b in ROWS if a in b) == 5 for a in A)
    assert sum(len(s) for s in SUPPORTS) == 156
    assert sum(len(s) // 2 for s in SUPPORTS) == 78 == len(ALL)


def perfect_matchings(vertices, avail, cap=None, out=None):
    """All perfect matchings of `vertices` using only edges in the set `avail`."""
    res = [] if out is None else out
    vs = list(vertices)

    def rec(rem, acc):
        if cap is not None and len(res) >= cap:
            return
        if not rem:
            res.append(tuple(acc))
            return
        a = rem[0]
        for k in range(1, len(rem)):
            b = rem[k]
            uv = ed(a, b)
            if uv in avail:
                rec(rem[1:k] + rem[k + 1:], acc + [uv])

    rec(vs, [])
    return res


def has_pm(vertices, avail):
    return bool(perfect_matchings(vertices, avail, cap=1))


NODES = [0]


def solve(avail, assigned):
    NODES[0] += 1
    if len(assigned) == 17:
        return dict(assigned)

    best, best_c, best_n = None, None, None
    for cidx in range(17):
        if cidx in assigned:
            continue
        opts = perfect_matchings(SUPPORTS[cidx], avail, cap=400)
        n = len(opts)
        if n == 0:
            return None
        if best_n is None or n < best_n:
            best, best_c, best_n = opts, cidx, n
            if n == 1:
                break

    for m in best:
        nxt = avail - set(m)
        # cheap global prune: every unassigned colour must still be matchable
        ok = True
        for cidx in range(17):
            if cidx == best_c or cidx in assigned:
                continue
            if not has_pm(SUPPORTS[cidx], nxt):
                ok = False
                break
        if not ok:
            continue
        assigned[best_c] = m
        r = solve(nxt, assigned)
        if r is not None:
            return r
        del assigned[best_c]
    return None


def main():
    sanity()
    print("instance: 17 rows, profile (n8,n10,n12) =",
          tuple(sum(1 for s in SUPPORTS if len(s) == k) for k in (8, 10, 12)))
    sol = solve(frozenset(ALL), {})
    print("search nodes:", NODES[0])
    if sol is None:
        print("NO COMPLETION")
        return 1
    used = [uv for m in sol.values() for uv in m]
    assert len(used) == 78 == len(set(used))
    for cidx, m in sorted(sol.items()):
        cov = sorted({w for uv in m for w in uv}, key=lambda a: IDX[a])
        assert cov == list(SUPPORTS[cidx])
        print("  colour %2d  support %2d  %s" % (cidx, len(cov), sorted(m)))
    print("COMPLETES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
