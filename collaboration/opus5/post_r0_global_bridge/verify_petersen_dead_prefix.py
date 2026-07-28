#!/usr/bin/env python3
"""Verifier for Theorem D of NOTE.md: a class-B' fourteen-prefix whose
residual is the Petersen graph.

NOT EXECUTED in the session that wrote it (no interpreter was available).
Every claim of NOTE.md is proved by hand there; this script is independent
audit surface only.

Standard library only.  Deterministic.  Prints one PASS/FAIL line per claim
and ends with ALL CHECKS PASS.
"""

import itertools
import sys

FAILURES = []


def check(name, cond):
    print(("PASS  " if cond else "FAIL  ") + name)
    if not cond:
        FAILURES.append(name)


# --------------------------------------------------------------- the ground set
Z5 = range(5)
E = [("e", i) for i in Z5]
F = [("f", i) for i in Z5]
V = E + F                      # the ten Petersen vertices
X, Y, Zt = ("t", 0), ("t", 1), ("t", 2)   # the three extra vertices x, y, z
A = [X, Y, Zt] + V             # |A| = 13


def ed(u, v):
    return (u, v) if u <= v else (v, u)


ALL = [ed(u, v) for u, v in itertools.combinations(A, 2)]


def e(i):
    return ("e", i % 5)


def f(i):
    return ("f", i % 5)


# ------------------------------------------------------------------- (5.1)-(5.2)
PET = ([ed(e(i), e(i + 2)) for i in Z5]
       + [ed(f(i), f(i + 1)) for i in Z5]
       + [ed(e(i), f(i + 2)) for i in Z5])

Q1 = [ed(e(i), f(i)) for i in Z5]
Q2 = [ed(e(i), f(i + 4)) for i in Z5]
Q3 = [ed(e(i), f(i + 3)) for i in Z5]
Q4 = [ed(e(i), f(i + 1)) for i in Z5]
RHO = [ed(e(i), e(i + 1)) for i in Z5] + [ed(f(i), f(i + 2)) for i in Z5]

Ei = [ed(e(i), e(i + 1)) for i in Z5]
Fi = [ed(f(i), f(i + 2)) for i in Z5]


def is_matching(edges):
    seen = set()
    for u, v in edges:
        if u in seen or v in seen:
            return False
        seen.add(u)
        seen.add(v)
    return True


def covered(edges):
    return {w for uv in edges for w in uv}


# --------------------------------------------------------------------- (5.3)
MA = [ed(Y, Zt)] + Q1
MB = [ed(X, Zt)] + Q2
MC = [ed(X, Y)] + Q3
MD = list(Q4)
N = [[ed(X, f(i)), ed(Y, f(i + 1)), ed(Zt, f(i + 2)), Ei[i]] for i in Z5]
NP = [[ed(X, e(i)), ed(Y, e(i + 1)), ed(Zt, e(i + 2)), Fi[i]] for i in Z5]

PREFIX = [MA, MB, MC, MD] + N + NP


# --------------------------------------------------------------------- (5.4)
def comp(m):
    return frozenset(A) - covered(m)


ROWS = [comp(m) for m in PREFIX] + [frozenset([X, Y, Zt])] * 3


def main():
    check("K_13 has 78 edges", len(ALL) == 78)
    check("Petersen has 15 edges, all distinct", len(PET) == 15 == len(set(PET)))
    check("Petersen is 3-regular",
          all(sum(1 for uv in PET if w in uv) == 3 for w in V))
    check("Petersen has girth >= 5 (no triangle, no 4-cycle)", girth_at_least_5())
    check("Petersen is not Hamiltonian", not has_hamilton_cycle())

    # (5.5)
    KV = [ed(u, v) for u, v in itertools.combinations(V, 2)]
    union = PET + Q1 + Q2 + Q3 + Q4 + RHO
    check("K_V = Pet + Q1..Q4 + Rho, disjointly",
          len(union) == len(set(union)) == 45 and set(union) == set(KV))
    for k, Q in enumerate([Q1, Q2, Q3, Q4], start=1):
        check("Q%d is a perfect matching of V" % k,
              is_matching(Q) and covered(Q) == set(V))
    check("Rho is a 2-factor of V",
          all(sum(1 for uv in RHO if w in uv) == 2 for w in V) and len(RHO) == 10)

    # prefix legitimacy
    flat = [uv for m in PREFIX for uv in m]
    check("prefix has 14 matchings", len(PREFIX) == 14)
    check("prefix edges pairwise disjoint, 63 of them",
          len(flat) == 63 == len(set(flat)))
    check("each prefix class is a matching", all(is_matching(m) for m in PREFIX))
    sizes = sorted(len(covered(m)) for m in PREFIX)
    check("prefix support sizes are 8^10 10^1 12^3",
          sizes == [8] * 10 + [10] + [12] * 3)

    residual = set(ALL) - set(flat)
    check("residual is exactly the Petersen graph", residual == set(PET))

    # class-B arithmetic
    check("17 rows", len(ROWS) == 17)
    check("every complement has odd size <= 5",
          all(len(b) in (1, 3, 5) for b in ROWS))
    check("every vertex lies in exactly five complements",
          all(sum(1 for b in ROWS if w in b) == 5 for w in A))
    prof = [sum(1 for b in ROWS if len(b) == k) for k in (5, 3, 1)]
    check("profile (n8,n10,n12) = (10,4,3), i.e. r = 3", prof == [10, 4, 3])
    check("sum of support sizes is 156",
          sum(13 - len(b) for b in ROWS) == 156)

    # the three unused colours
    check("three unused colours all have support V",
          all(frozenset(A) - ROWS[i] == frozenset(V) for i in (14, 15, 16)))

    # Lemma D1
    pms = list(perfect_matchings(V, set(PET)))
    check("Petersen has exactly six perfect matchings", len(pms) == 6)
    check("no two perfect matchings of Petersen are disjoint",
          all(set(a) & set(b) for a, b in itertools.combinations(pms, 2)))
    check("Petersen is not 3-edge-colourable (class 2)",
          not any(set(a) | set(b) | set(c) == set(PET)
                  for a, b, c in itertools.combinations(pms, 3)))

    # the prefix extends to exactly fifteen
    check("prefix extends by exactly one matching (to fifteen)",
          len(pms) > 0 and all(set(a) & set(b)
                               for a, b in itertools.combinations(pms, 2)))

    # Lemma D4 on Petersen: 3*(5 - nu(Pet - F)) <= |F| for every F
    check("Lemma D4 holds on Petersen for all 2^15 subsets F",
          capacity_ok())

    # class-B' point labelling of section 5.3 (the x,y,z part; the V part is
    # Koenig's theorem on a 5-regular bipartite graph and is checked here too)
    check("class-B' labelling of the x,y,z incidences", classbprime_xyz())
    check("class-B' labelling of the V incidences exists", classbprime_V())

    print()
    if FAILURES:
        print("FAILURES: %d" % len(FAILURES))
        return 1
    print("ALL CHECKS PASS")
    return 0


# ------------------------------------------------------------------- helpers
def girth_at_least_5():
    adj = {w: set() for w in V}
    for u, v in PET:
        adj[u].add(v)
        adj[v].add(u)
    for u, v in itertools.combinations(V, 2):
        common = adj[u] & adj[v]
        if v in adj[u] and common:
            return False                      # triangle
        if v not in adj[u] and len(common) > 1:
            return False                      # 4-cycle
    return True


def has_hamilton_cycle():
    adj = {w: set() for w in V}
    for u, v in PET:
        adj[u].add(v)
        adj[v].add(u)
    start = V[0]

    def rec(path, used):
        if len(path) == 10:
            return start in adj[path[-1]]
        for w in adj[path[-1]]:
            if w not in used:
                if rec(path + [w], used | {w}):
                    return True
        return False

    return rec([start], {start})


def max_matching_size(edges):
    """Maximum matching size of the graph with the given edge list."""
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    verts = sorted(adj, key=lambda w: (w[0], w[1]))

    def rec(i, used):
        while i < len(verts) and verts[i] in used:
            i += 1
        if i == len(verts):
            return 0
        v = verts[i]
        best = rec(i + 1, used)                       # leave v unmatched
        for w in adj[v]:
            if w not in used:
                best = max(best, 1 + rec(i + 1, used | {v, w}))
        return best

    return rec(0, frozenset())


def capacity_ok():
    edges = list(PET)
    n = len(edges)
    for mask in range(1 << n):
        keep = [edges[k] for k in range(n) if not (mask >> k) & 1]
        size = bin(mask).count("1")                   # |F|
        if 3 * (5 - max_matching_size(keep)) > size:
            return False
    return True


def perfect_matchings(vertices, allowed):
    vs = sorted(vertices)
    if not vs:
        yield ()
        return
    a = vs[0]
    for b in vs[1:]:
        if ed(a, b) in allowed:
            rest = [w for w in vs[1:] if w != b]
            for m in perfect_matchings(rest, allowed):
                yield (ed(a, b),) + m


def classbprime_xyz():
    P = [1, 2, 3, 4, 5]
    lam = {
        (X, "MA"): 1, (X, "MD"): 2, (X, "g1"): 3, (X, "g2"): 4, (X, "g3"): 5,
        (Y, "MB"): 2, (Y, "MD"): 1, (Y, "g1"): 4, (Y, "g2"): 5, (Y, "g3"): 3,
        (Zt, "MC"): 3, (Zt, "MD"): 5, (Zt, "g1"): 1, (Zt, "g2"): 2, (Zt, "g3"): 4,
    }
    for w in (X, Y, Zt):
        if sorted(v for (a, _), v in lam.items() if a == w) != P:
            return False
    used = {}
    for (a, c), p in lam.items():
        used.setdefault(c, []).append(p)
    for c, ps in used.items():
        if len(set(ps)) != len(ps):
            return False
    pairs = []
    unused = {c: [p for p in P if p not in used[c]] for c in used}
    fixed = {"MD": [(3, 4)], "g1": [(2, 5)], "g2": [(1, 3)], "g3": [(1, 2)],
             "MA": [(2, 3), (4, 5)], "MB": [(1, 4), (3, 5)],
             "MC": [(1, 5), (2, 4)]}
    for c, prs in fixed.items():
        flat = [p for pr in prs for p in pr]
        if sorted(flat) != sorted(unused[c]):
            return False
        pairs += [tuple(sorted(pr)) for pr in prs]
    return sorted(pairs) == sorted(
        tuple(sorted(pr)) for pr in itertools.combinations(P, 2))


def classbprime_V():
    """The V-side incidence graph is 5-regular bipartite; Koenig gives a proper
    5-edge-colouring.  Here we exhibit one by repeated Hall matchings."""
    rows = [i for i in range(len(ROWS)) if len(ROWS[i]) == 5]
    inc = {(w, i) for i in rows for w in ROWS[i]}
    if len(inc) != 50:
        return False
    if any(sum(1 for i in rows if w in ROWS[i]) != 5 for w in V):
        return False
    remaining = set(inc)
    for _ in range(5):
        m = bipartite_perfect_matching(V, rows, remaining)
        if m is None:
            return False
        remaining -= set(m.items())
    return not remaining


def bipartite_perfect_matching(left, right, edges):
    adj = {u: [v for v in right if (u, v) in edges] for u in left}
    match = {}
    rev = {}

    def aug(u, seen):
        for v in adj[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in rev or aug(rev[v], seen):
                match[u] = v
                rev[v] = u
                return True
        return False

    for u in left:
        if not aug(u, set()):
            return None
    return match


if __name__ == "__main__":
    sys.exit(main())
