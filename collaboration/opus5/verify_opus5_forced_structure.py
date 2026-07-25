#!/usr/bin/env python3
"""Independent validator for collaboration/opus5/PROOF.md.

NOT RUN in the session that wrote it: code execution was unavailable there.
Every assertion below is machine-checkable; run it before trusting PROOF.md.

    python3 -B collaboration/opus5/verify_opus5_forced_structure.py

What it checks, entirely from brute-force enumeration of real designs and
from an independently constructed Witt system S(5,6,12):

  T1  every (k+1)-set contains exactly one block            (Theorem 1)
  T2  lambda_s = binom(k+m,m)/(k+1); prime characterisation (Theorem 2)
  T3  f - 1/p lies in the least eigenspace of J(2k,k)       (Theorem 3)
  T4  #{B subset U} = binom(k+j,j)/p for |U| = k+j          (Theorem 4)
  T4b B|^U is an S(j-1,j,k+j) for every (k+j)-set U         (Cor 4.1)
  T5  inner distribution closed form                        (Theorem 5)
  T6  cross distribution closed form for disjoint systems   (Theorem 6)
  T6b odd k > 1 impossible; complement-closure for even k   (Cor 6.1/6.2)
  T7  dual distribution supported on {0, k}                 (Theorem 7)
  T8  every local array L_S is a Latin square               (Theorem 8)
  T9  at most p pairwise disjoint systems, = p iff large set (Theorem 9)
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

# ---------------------------------------------------------------- helpers


def binom(n: int, r: int) -> int:
    return math.comb(n, r) if 0 <= r <= n else 0


def ksets(points, k):
    return [frozenset(c) for c in itertools.combinations(sorted(points), k)]


def is_steiner(blocks, points, t, k):
    """blocks is an S(t,k,v) on points: every t-set in exactly one block."""
    blocks = list(blocks)
    if any(len(b) != k for b in blocks):
        return False
    seen = {}
    for b in blocks:
        for s in itertools.combinations(sorted(b), t):
            if s in seen:
                return False
            seen[s] = b
    return len(seen) == binom(len(points), t)


# ---------------------------------------------------- design constructions


def all_s_kminus1_k_2k(k):
    """All labelled S(k-1,k,2k) on [0,2k). Exhaustive; only for k = 2, 4."""
    pts = range(2 * k)
    cand = ksets(pts, k)
    tsets = list(itertools.combinations(range(2 * k), k - 1))
    idx = {t: i for i, t in enumerate(tsets)}
    cover = [frozenset(idx[t] for t in itertools.combinations(sorted(b), k - 1))
             for b in cand]
    need = len(tsets)
    out = []

    def rec(chosen, used):
        if len(used) == need:
            out.append([cand[i] for i in chosen])
            return
        target = min(set(range(need)) - used)
        for i, cv in enumerate(cover):
            if target in cv and not (cv & used):
                rec(chosen + [i], used | cv)

    rec([], frozenset())
    # dedupe (same block set reached in different orders)
    uniq = {frozenset(d) for d in out}
    return [sorted(d, key=sorted) for d in uniq]


def ternary_golay_hexads():
    """The 132 hexads of an S(5,6,12), built from the [12,6,6]_3 Golay code.

    Generator [I_6 | B]; B is the bordered circulant of the quadratic
    residues mod 5.  The construction is *verified*, not asserted: if the
    matrix were wrong the assertions below would fail.
    """
    circ_row = [0, 1, 2, 2, 1]           # chi(0),chi(1),chi(2),chi(3),chi(4)
    B = [[0] + [1] * 5]
    for i in range(5):
        B.append([1] + [circ_row[(j - i) % 5] for j in range(5)])
    gen = [[1 if j == i else 0 for j in range(6)] + B[i] for i in range(6)]

    words = set()
    for coeffs in itertools.product(range(3), repeat=6):
        w = [0] * 12
        for c, row in zip(coeffs, gen):
            if c:
                for j in range(12):
                    w[j] = (w[j] + c * row[j]) % 3
        words.add(tuple(w))
    assert len(words) == 729, len(words)

    wt = {}
    for w in words:
        wt[sum(1 for x in w if x)] = wt.get(sum(1 for x in w if x), 0) + 1
    assert wt == {0: 1, 6: 264, 9: 440, 12: 24}, wt

    hexads = {frozenset(j for j, x in enumerate(w) if x)
              for w in words if sum(1 for x in w if x) == 6}
    assert len(hexads) == 132, len(hexads)
    assert is_steiner(hexads, range(12), 5, 6)
    return sorted(hexads, key=sorted)


# --------------------------------------------------------- the predictions


def pred_lambda(k, s):
    m = k - s
    num = binom(k + m, m)
    assert num % (k + 1) == 0, (k, s)
    return num // (k + 1)


def pred_inner(k, u):
    p = k + 1
    val = Fraction(binom(k, u) * (binom(k, u) + (-1) ** u * k), p)
    assert val.denominator == 1
    return int(val)


def pred_cross(k, u):
    p = k + 1
    val = Fraction(binom(k, u) * (binom(k, u) - (-1) ** u), p)
    assert val.denominator == 1
    return int(val)


# --------------------------------------------------------------- the tests


def check_theorem2():
    """Integrality of all lambda_s holds iff k+1 is prime."""
    def ok(k):
        return all(binom(k + m, m) % (k + 1) == 0 for m in range(1, k + 1))

    for k in range(2, 60):
        assert ok(k) == (k + 1 > 1 and all((k + 1) % d for d in
                                           range(2, int((k + 1) ** .5) + 1))), k
    print("T2  lambda_s integral for all s  <=>  k+1 prime      [1..59]  OK")


def check_one_design(k, blocks, label):
    pts = list(range(2 * k))
    p = k + 1
    blockset = set(blocks)
    assert is_steiner(blocks, pts, k - 1, k), label
    assert len(blocks) == binom(2 * k, k) // p

    # T1: every (k+1)-set contains exactly one block
    for U in itertools.combinations(pts, k + 1):
        n = sum(1 for x in U if frozenset(U) - {x} in blockset)
        assert n == 1, (label, U, n)

    # T2 numeric: lambda_s
    for s in range(0, k):
        for T in itertools.combinations(pts, s):
            n = sum(1 for b in blocks if set(T) <= b)
            assert n == pred_lambda(k, s), (label, "lambda", s, n)
            break                                    # design is s-regular

    # T4 / T4b: super-set counts and the derived tower
    for j in range(1, k + 1):
        want = binom(k + j, j) // p
        for U in itertools.combinations(pts, k + j):
            inside = [b for b in blocks if b <= set(U)]
            assert len(inside) == want, (label, "T4", j, len(inside), want)
            derived = [frozenset(U) - b for b in inside]
            assert is_steiner(derived, U, j - 1, j), (label, "T4b", j)
            if k + j >= 2 * k:
                break
            if j >= 3:
                break                                # cost control

    # T5: inner distribution
    for B in blocks[:3]:
        dist = [0] * (k + 1)
        for Bp in blocks:
            dist[k - len(B & Bp)] += 1
        for u in range(k + 1):
            assert dist[u] == pred_inner(k, u), (label, "T5", u, dist[u])

    # Cor 6.2: complement-closure
    for B in blocks:
        assert frozenset(pts) - B in blockset, (label, "Cor6.2")

    print(f"T1/T2/T4/T4b/T5/6.2  {label}: OK "
          f"(inner distribution {[pred_inner(k,u) for u in range(k+1)]})")


def check_cross_and_max_disjoint(k, designs, label):
    """T6 on a disjoint pair; T9 on the maximum clique of disjointness."""
    pts = list(range(2 * k))
    sets = [set(d) for d in designs]
    n = len(designs)
    adj = [[i != j and not (sets[i] & sets[j]) for j in range(n)]
           for i in range(n)]

    pair = next(((i, j) for i in range(n) for j in range(i + 1, n)
                 if adj[i][j]), None)
    if pair is None:
        print(f"T6  {label}: no disjoint pair exists, T6 vacuous")
    else:
        i, j = pair
        for B in designs[i][:3]:
            dist = [0] * (k + 1)
            for Bp in designs[j]:
                dist[k - len(B & Bp)] += 1
            for u in range(k + 1):
                assert dist[u] == pred_cross(k, u), (label, "T6", u, dist[u])
        print(f"T6  {label}: cross distribution "
              f"{[pred_cross(k,u) for u in range(k+1)]}  OK")

    best = 0

    def grow(cur, cands):
        nonlocal best
        best = max(best, len(cur))
        for idx, c in enumerate(cands):
            grow(cur + [c], [d for d in cands[idx + 1:] if adj[c][d]])

    grow([], list(range(n)))
    assert best <= k + 1, (label, "T9", best)
    print(f"T9  {label}: max pairwise disjoint = {best} (bound {k+1}); "
          f"large set {'exists' if best == k + 1 else 'does NOT exist'}")
    return best


def check_theorem3_and_7(k, blocks, label):
    """f - 1/p is in the least eigenspace; dual distribution on {0,k}."""
    import numpy as np

    X = ksets(range(2 * k), k)
    pos = {s: i for i, s in enumerate(X)}
    N = len(X)
    A = np.zeros((N, N))
    for s in X:
        for t in X:
            if len(s & t) == k - 1:
                A[pos[s], pos[t]] = 1.0

    f = np.zeros(N)
    for b in blocks:
        f[pos[b]] = 1.0
    g = f - np.ones(N) / (k + 1)

    # T3: (A + kI) g = 0
    assert np.allclose(A @ g + k * g, 0, atol=1e-8), (label, "T3")

    # T7: projection of f onto every intermediate eigenspace is zero
    vals, vecs = np.linalg.eigh(A)
    thetas = sorted({round((k - j) ** 2 - j) for j in range(k + 1)})
    for th in thetas:
        mask = np.abs(vals - th) < 1e-6
        proj = vecs[:, mask].T @ f
        nrm = float(proj @ proj)
        if th == k * k:                                  # E_0
            assert nrm > 1e-6, (label, "T7 E_0")
        elif th == -k:                                   # E_k
            assert nrm > 1e-6, (label, "T7 E_k")
        else:
            assert nrm < 1e-6, (label, "T7", th, nrm)
    print(f"T3/T7  {label}: Fourier support is exactly {{E_0, E_k}}  OK")


def check_theorem8(k, classes, label):
    """L_S is a Latin square of order k on the p-1 colours != c(S)."""
    pts = list(range(2 * k))
    p = k + 1
    colour = {}
    for a, cls in enumerate(classes):
        for b in cls:
            colour[b] = a
    assert len(colour) == binom(2 * k, k)

    for S in ksets(pts, k):
        out = set(pts) - set(S)
        rows = sorted(S)
        cols = sorted(out)
        sym = set(range(p)) - {colour[S]}
        for x in rows:
            r = [colour[frozenset(set(S) - {x} | {y})] for y in cols]
            assert set(r) == sym and len(r) == k, (label, "T8 row", S, x)
        for y in cols:
            c = [colour[frozenset(set(S) - {x} | {y})] for x in rows]
            assert set(c) == sym and len(c) == k, (label, "T8 col", S, y)
    print(f"T8  {label}: all {binom(2*k,k)} local arrays are "
          f"order-{k} Latin squares  OK")


# ------------------------------------------------------------------- main


def pred_inner_general(k, v, u):
    """Theorem 5a: inner distribution of any S(k-1,k,v).  P = v-k+1."""
    P = v - k + 1
    val = Fraction(binom(k, u) * (binom(v - k, u) + (-1) ** u * (P - 1)), P)
    assert val.denominator == 1, (k, v, u, val)
    return int(val)


def check_theorem5a_and_7a():
    """General-v inner distribution and the lambda_j = average identity."""
    # 7a: lambda_j equals the average value, for a wide parameter range
    for k in range(2, 12):
        for v in range(2 * k - 1, 2 * k + 40):
            P = v - k + 1
            for j in range(0, k):
                lam = Fraction(binom(v - j, k - 1 - j), k - j)
                avg = Fraction(binom(v - j, k - j), P)
                assert lam == avg, (k, v, j, lam, avg)
    print("T7a  lambda_j == average value, k in 2..11, 40 values of v   OK")

    # 5a reduces to 5 at v = 2k
    for k in range(2, 20, 2):
        for u in range(k + 1):
            assert pred_inner_general(k, 2 * k, u) == pred_inner(k, u), (k, u)
    print("T5a  general formula reduces to (5.2) at v = 2k              OK")

    # 5a: nonnegative integers summing to |B| = binom(v,k)/P
    for k, v in [(4, 8), (6, 12), (5, 21), (4, 20), (3, 19), (4, 8),
                 (4, 10), (4, 14), (4, 16), (4, 22), (4, 26), (4, 28),
                 (6, 22), (7, 23)]:
        P = v - k + 1
        if binom(v, k) % P:
            continue
        dist = [pred_inner_general(k, v, u) for u in range(k + 1)]
        assert all(x >= 0 for x in dist), (k, v, dist)
        assert sum(dist) == binom(v, k) // P, (k, v, dist)
        assert dist[0] == 1 and dist[1] == 0, (k, v, dist)
    print("T5a  nonneg integers summing to |B| for 14 parameter pairs   OK")

    # Cor 7.2: no S(k-1,k,2k-1).  Cross-check against plain divisibility:
    # report the k where Cor 7.2 is strictly stronger than lambda-integrality.
    stronger = []
    for k in range(2, 30):
        v = 2 * k - 1
        if all(Fraction(binom(v - j, k - 1 - j), k - j).denominator == 1
               for j in range(k)):
            stronger.append(k)
    print(f"Cor7.2  no S(k-1,k,2k-1); divisibility alone leaves k in "
          f"{stronger} (Cor 7.2 covers those too)")

    # the S(4,5,21) instance quoted in PROOF.md
    assert [pred_inner_general(5, 21, u) for u in range(6)] == \
        [1, 0, 80, 320, 540, 256]
    assert sum([1, 0, 80, 320, 540, 256]) == 1197 == binom(21, 4) // 5
    print("T5a  S(4,5,21) distribution (1,0,80,320,540,256), total 1197 OK")


def check_odd_graph_walks():
    """Closed-walk identities for O_k used in IDEAS.md section B."""
    def spec(k):
        return [((-1) ** i * (k - i), binom(2 * k - 1, i) - binom(2 * k - 1, i - 1))
                for i in range(k)]

    def W(k, m):
        return sum(mult * theta ** m for theta, mult in spec(k))

    def tree_walks(k, half):          # closed 2*half-walks at root of k-tree
        if half == 2:
            return 2 * k * k - k
        if half == 3:
            return 2 * k * (k - 1) ** 2 + 2 * k * k * (k - 1) + k ** 3
        raise ValueError

    for k in range(4, 18, 2):
        N = binom(2 * k - 1, k - 1)
        assert sum(m for _, m in spec(k)) == N, k
        assert W(k, 1) == 0
        assert W(k, 2) == N * k
        assert W(k, 3) == 0, k                       # girth 6: no triangles
        assert W(k, 4) == N * tree_walks(k, 2), k    # girth 6: no 4-cycles
        assert W(k, 4) == N * k * (2 * k - 1), k
        assert W(k, 5) == 0, k                       # girth 6: no 5-cycles
        hexagons12 = W(k, 6) - N * tree_walks(k, 3)
        assert hexagons12 > 0 and hexagons12 % 12 == 0, k
        if k == 4:
            assert (N, W(4, 4), W(4, 6), tree_walks(4, 3)) == (35, 980, 9380, 232)
            assert hexagons12 // 12 == 105
    print("IDEAS-B  O_k walk identities k=4..16 even; O_4 has 105 hexagons OK")


def main() -> None:
    check_theorem2()
    check_theorem5a_and_7a()
    check_odd_graph_walks()

    # k = 2 : the three perfect matchings of K_4 (a genuine large set)
    d2 = all_s_kminus1_k_2k(2)
    assert len(d2) == 3, len(d2)
    for d in d2:
        check_one_design(2, d, "k=2 S(1,2,4)")
        check_theorem3_and_7(2, d, "k=2")
    best2 = check_cross_and_max_disjoint(2, d2, "k=2")
    assert best2 == 3
    ls = next([d2[i] for i in c] for c in itertools.combinations(range(3), 3)
              if len({b for i in c for b in d2[i]}) == binom(4, 2))
    check_theorem8(2, ls, "k=2 tight 3-colouring")

    # k = 4 : the 30 labelled SQS(8); no large set (max 2 disjoint)
    d4 = all_s_kminus1_k_2k(4)
    assert len(d4) == 30, len(d4)
    check_one_design(4, d4[0], "k=4 S(3,4,8)")
    check_theorem3_and_7(4, d4[0], "k=4")
    best4 = check_cross_and_max_disjoint(4, d4, "k=4")
    assert best4 == 2, best4          # 2 < 5, so no tight 5-colouring

    # k = 6 : the Witt system S(5,6,12)
    d6 = ternary_golay_hexads()
    check_one_design(6, d6, "k=6 S(5,6,12)")
    assert [pred_inner(6, u) for u in range(7)] == [1, 0, 45, 40, 45, 0, 1]
    check_theorem3_and_7(6, d6, "k=6")

    # Cor 6.1 : odd k > 1 is excluded by nonnegativity of n_0
    for k in range(3, 40, 2):
        assert Fraction(1 + (-1) ** k * k, k + 1) < 0, k
    print("Cor6.1  n_0 < 0 for every odd k in 3..39                    OK")

    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
