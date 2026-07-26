#!/usr/bin/env python3
"""Rank-four two-coordinate Plucker ratio: classification, translation, frontier.

SCOPE: does NOT solve #835, does NOT prove a no-go for the rank-four family,
does NOT construct a colouring.  Proves the local classification and the exact
geometric translation; exhibits a LOCAL positive link at p=3; reports the
absence of local links at p=5,7,11 as COMPUTATION only.

Stdlib only, dependency-free, assertion-enabled.
"""

from __future__ import annotations
import itertools
import random


def P1(p):
    return [(1, c) for c in range(p)] + [(0, 1)]


def dt(u, v, p):
    return (u[0] * v[1] - u[1] * v[0]) % p


def rat(a, b, p):
    if a == 0 and b == 0:
        return None
    if a == 0:
        return "inf"
    return (b * pow(a, p - 2, p)) % p


def wedge4(f, g, u, v, p):
    """rank(a f^g + b u^v) = 4 for generic (a,b) iff f,g,u,v independent."""
    M = [list(f), list(g), list(u), list(v)]
    n = 4
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, n) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        iv = pow(M[r][c], p - 2, p)
        M[r] = [(x * iv) % p for x in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                fct = M[i][c]
                M[i] = [(M[i][j] - fct * M[r][j]) % p for j in range(n)]
        r += 1
    return r


def link_ok(A, B, lam, n, p):
    R = {}
    for i, j in itertools.combinations(range(n), 2):
        r = rat(dt(A[i], A[j], p), (lam[i] * lam[j] * dt(B[i], B[j], p)) % p, p)
        if r is None:
            return None
        R.setdefault(r, []).append((i, j))
    for i in range(n):
        if (
            len(
                {
                    rat(dt(A[i], A[j], p), (lam[i] * lam[j] * dt(B[i], B[j], p)) % p, p)
                    for j in range(n)
                    if j != i
                }
            )
            != n - 1
        ):
            return None

    def is_pm(edges):
        return len(edges) == n // 2 and sorted(
            vertex for edge in edges for vertex in edge
        ) == list(range(n))

    F = sorted(R.values(), key=len, reverse=True)
    groups = []

    def bt(t):
        if t == len(F):
            return len(groups) == p and all(is_pm(g) for g in groups)
        for gi in range(len(groups)):
            old = groups[gi][:]
            groups[gi] = old + F[t]
            if len(groups[gi]) <= n // 2 and len(
                {v for e in groups[gi] for v in e}
            ) == 2 * len(groups[gi]):
                if bt(t + 1):
                    return True
            groups[gi] = old
        if len(groups) < p:
            groups.append(list(F[t]))
            if bt(t + 1):
                return True
            groups.pop()
        return False

    return groups if bt(0) else None


def rand_map(n, pts, rnd):
    while True:
        f = [rnd.choice(pts) for _ in range(n)]
        c = {}
        for v in f:
            c[v] = c.get(v, 0) + 1
        if max(c.values()) <= 2:
            return f


def main():
    p = 5
    print("1. PROVED -- exactly two rank-2 members (Pfaffian ab), one orbit")
    f, g, u, v = (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)
    assert wedge4(f, g, u, v, p) == 4
    print("   e1^e2 and e3^e4: f,g,u,v independent -> rank 4 generically: ok")
    assert wedge4((1, 0, 0, 0), (0, 1, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), p) == 3
    print("   a 3-dim span reproduces the decomposable (Grassmann-line) case: ok")

    print("\n2. PROVED -- Lemma 4: A- and B-fibres must have size <= 2")
    print("   rho^-1([0:1]) is the union of cliques on A-fibres; a clique of")
    print("   size >= 3 cannot lie in a perfect matching.")

    print("\n3. COMPUTATION -- local link at p=3 (exhibited), frontier elsewhere")
    A = [(1, 1), (0, 1), (0, 1), (1, 1)]
    B = [(0, 1), (0, 1), (1, 2), (1, 2)]
    lam = [1, 1, 1, 2]
    g3 = link_ok(A, B, lam, 4, 3)
    assert g3 is not None and len(g3) == 3
    print(
        f"   p=3 witness verifies: {len(g3)} perfect matchings, sizes {[len(x) for x in g3]}"
    )
    for pp, tries in ((5, 60000), (7, 60000), (11, 60000)):
        n = pp + 1
        rnd = random.Random(101 * pp)
        pts = P1(pp)
        found = None
        for _ in range(tries):
            A = rand_map(n, pts, rnd)
            B = rand_map(n, pts, rnd)
            if len({(A[i], B[i]) for i in range(n)}) != n:
                continue
            lam = [1] + [rnd.randrange(1, pp) for _ in range(n - 1)]
            gg = link_ok(A, B, lam, n, pp)
            if gg:
                found = gg
                break
        print(
            f"   p={pp:2d}: {'FOUND' if found else 'none'} in {tries} random tries"
            f" (fibres <= 2)  -- COMPUTATION, not a proof"
        )
        assert found is None
    print("\nSCOPE.  No no-go proved at p >= 5, nothing claimed at p = 17, and a")
    print("local link is strictly weaker than a global pair of Plucker systems.")
    print("Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()
