#!/usr/bin/env python3
"""Audit + new corollaries for the deleted-colour Hadamard-kernel theorem.

Labels: PROVED / COMPUTATION / FAILED ATTACK.  Stdlib only, no solver.
"""

from __future__ import annotations
import itertools
from math import comb


def sqs8():
    """The unique S(3,4,8) = AG(3,2) planes, on F_2^3 labelled 0..7."""
    B = []
    for S in itertools.combinations(range(8), 4):
        x = 0
        for s in S:
            x ^= s
        if x == 0:
            B.append(frozenset(S))
    return B


def witt_s5612():
    """S(5,6,12) via the extended ternary Golay weight-6 supports."""
    # generator of the extended ternary Golay [12,6,6] code
    A = [
        [0, 1, 1, 1, 1, 1],
        [1, 0, 1, 2, 2, 1],
        [1, 1, 0, 1, 2, 2],
        [1, 2, 1, 0, 1, 2],
        [1, 2, 2, 1, 0, 1],
        [1, 1, 2, 2, 1, 0],
    ]
    G = [[1 if i == j else 0 for j in range(6)] + A[i] for i in range(6)]
    words = set()
    for co in itertools.product(range(3), repeat=6):
        w = tuple(sum(co[i] * G[i][j] for i in range(6)) % 3 for j in range(12))
        words.add(w)
    sup = [frozenset(j for j in range(12) if w[j]) for w in words]
    return [s for s in set(sup) if len(s) == 6]


def is_steiner(blocks, n, k):
    t = k - 1
    cnt = {}
    for B in blocks:
        for T in itertools.combinations(sorted(B), t):
            cnt[T] = cnt.get(T, 0) + 1
    return all(cnt.get(T, 0) == 1 for T in itertools.combinations(range(n), t))


def report(name, blocks, n, k):
    p = k + 1
    X = comb(n, k)
    Y = comb(n, k - 1)
    Dsz = len(blocks)
    print(f"  {name}: n={n} k={k} p={p}")
    assert is_steiner(blocks, n, k), "not a Steiner system"
    assert Dsz == X // p == Y // k, (Dsz, X // p, Y // k)
    assert X - Dsz == Y, "|X\\D| must equal |Y| (M_D square)"
    print(f"    |X|={X} |Y|={Y} |D|={Dsz}; |X\\D|=|Y| so M_D is SQUARE: ok")
    # exact average of D-blocks per (k+1)-set is 1
    num = Dsz * (n - k)
    den = comb(n, k + 1)
    assert num == den, (num, den)
    print(
        f"    sum over (k+1)-sets of #D-blocks inside = |D|*(n-k) = {num} = C(n,k+1): average exactly 1: ok"
    )
    # CLIQUE COROLLARY: every (k+1)-set must contain >= 1 D-block
    bad = [
        C
        for C in itertools.combinations(range(n), k + 1)
        if not any(
            frozenset(S) <= frozenset(C)
            for S in itertools.combinations(C, k)
            if frozenset(S) in set(map(frozenset, blocks))
        )
    ]
    print(
        f"    (k+1)-sets containing NO D-block: {len(bad)}  (any >0 would contradict dim U = p-2)"
    )
    assert not bad
    comp = [frozenset(range(n)) - frozenset(B) for B in blocks]
    print(f"    hence D^c is also an S({k - 1},{k},{n}): {is_steiner(comp, n, k)}")
    assert is_steiner(comp, n, k)


def rank_IJ(m, p):
    """rank of I + J_m over F_p."""
    M = [[(1 if i != j else 2) % p for j in range(m)] for i in range(m)]
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, m) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        iv = pow(M[r][c], p - 2, p)
        M[r] = [(x * iv) % p for x in M[r]]
        for i in range(m):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % p for j in range(m)]
        r += 1
    return r


def kerdim_stdlib(blocks, n, k, p):
    """dim ker M_D over F_p, pure stdlib (feasible at k = 2, 4)."""
    X = [frozenset(S) for S in itertools.combinations(range(n), k)]
    Y = [frozenset(S) for S in itertools.combinations(range(n), k - 1)]
    Dset = set(map(frozenset, blocks))
    cols = [S for S in X if S not in Dset]
    A = [[1 if B <= S else 0 for S in cols] for B in Y]
    rows, nc = len(A), len(cols)
    r = 0
    for c in range(nc):
        piv = next((i for i in range(r, rows) if A[i][c] % p), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        iv = pow(A[r][c], p - 2, p)
        A[r] = [(x * iv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(nc)]
        r += 1
    return nc - r


def section6():
    print()
    print("=" * 74)
    print("6.  COMPUTATION -- kernel dimensions, and a REFUTED guess")
    print("=" * 74)
    d2 = kerdim_stdlib([frozenset({0, 1}), frozenset({2, 3})], 4, 2, 3)
    d4 = kerdim_stdlib(sqs8(), 8, 4, 5)
    print(f"    dim ker M_D: k=2 -> {d2}, k=4 -> {d4}   (stdlib, exact)")
    assert (d2, d4) == (1, 7)
    print("    k=6 -> 77 (rank 715 of the 792x792 matrix over F_7), computed by")
    print("    the checked-in exact script verify_k6_kernel.py in this directory.")
    print()
    print("    REFUTED GUESS.  |D|/2 gives 1, 7, 66 for k = 2, 4, 6.  The first")
    print("    two match but k=6 gives 77, not 66, so dim ker M_D = |D|/2 is")
    print("    FALSE.  It is recorded here so it is not re-tried; in particular")
    print("    dim ker M_D at k = 16 is NOT determined by this work.")


def section7():
    print()
    print("=" * 74)
    print("7.  PROVED -- the descent to a derived large set is valid")
    print("=" * 74)
    n2, k2 = 21, 5
    rows_per = n2 - (k2 - 1)
    print(f"    For LS(4,5,21): a 4-set lies in {n2 - 4} = {rows_per} five-sets, and")
    print("    p = 17, so every row carries exactly p blocks: the theorem applies")
    print("    verbatim and yields U' of dimension p-2 = 15 inside ker M_D'.")
    assert rows_per == 17
    Xp = comb(21, 5)
    Yp = comb(21, 4)
    Dp = Xp // 17
    print(f"    |X'|={Xp} |Y'|={Yp} |D'|={Dp} |X'\\D'|={Xp - Dp}")
    assert Xp - Dp == 19152 and Yp == 5985
    print(f"    BUT M_D' is {Yp}x{Xp - Dp} -- WIDE, not square, so")
    print(f"    dim ker M_D' >= {Xp - Dp - Yp}.  The descent preserves the required")
    print("    15-dimensional structure, so it is LEGITIMATE.")
    print("    CORRECTED: a wide matrix does NOT show the descent is harder.  All")
    print("    that follows is that LINEAR nullity alone gives no bound there.")
    print("    The quadratic conditions -- in particular gluing the frames across")
    print("    overlapping 4-set stars -- may still make the derived layer the")
    print("    better place to work.  Nothing here settles that either way.")


def main():
    print("=" * 74)
    print("1.  AUDIT of the deleted-colour theorem -- SOUND")
    print("=" * 74)
    print("    Re-derived independently: power sums over a full star give (1);")
    print("    Newton + T^p - T - e_p having a root in F_p forces e_p = 0, so the")
    print("    converse holds.  u_r = g^r (1<=r<=p-2) are independent because a")
    print("    polynomial of degree <= p-2 vanishing on all of F_p* and at 0 is 0.")
    print("    M_D u_r = W(g^r) = 0, and M_D(u_r o u_s) = -1 iff (p-1)|(r+s);")
    print("    with 2 <= r+s <= 2p-4 that happens only at r+s = p-1, so b is the")
    print("    anti-diagonal(-1) form: NONDEGENERATE.  All counts check below.")
    print("    One wording imprecision: 'one (hence every) rho_B injective' -- the")
    print("    'hence every' is true a posteriori but is not needed as a hypothesis;")
    print("    the converse only uses surjectivity of a single rho_B.")

    print()
    print("=" * 74)
    print("2.  PROVED -- Wilson rank and the squareness of M_D")
    print("=" * 74)
    print("    rank_p W_{k-1,k}(2k) = sum_i [C(2k,i)-C(2k,i-1)] over i<=k-1 with")
    print("    p not dividing C(k-i,k-1-i) = k-i.  Since 1 <= k-i <= k < p, every")
    print("    i qualifies, and the sum telescopes to C(2k,k-1) = |Y|: FULL ROW RANK.")
    print("    |X\\D| = C(2k,k)(p-1)/p = C(2k,k-1) = |Y|, so M_D is square.")

    print()
    print("=" * 74)
    print("3.  PROVED -- frame reformulation")
    print("=" * 74)
    print("    b nondegenerate gives v_S in U with b(v_S,x) = x(S).  Then for every")
    print("    (k-1)-set B the deleted star satisfies b(x,y) = sum_S x(S)y(S), i.e.")
    print("    rho_B is an ISOMETRY onto H_0.  Transporting e_i -> e_i + 1 gives")
    print("      b(v_S,v_S) = 2,  b(v_S,v_S') = 1 for S,S' in a common star,")
    print("      sum over each deleted star of v_S = 0.")
    print("    Two k-sets lie in a common (k-1)-star iff |S n S'| = k-1, i.e. iff")
    print("    they are ADJACENT in the Johnson graph J(2k,k).")

    print()
    print("=" * 74)
    print("4.  Clique corollary -- PROVED but VACUOUS (see end of section)")
    print("=" * 74)
    for p in (3, 5, 7, 17):
        m = p
        r = rank_IJ(m, p)
        m2 = p - 1
        r2 = rank_IJ(m2, p)
        print(
            f"    p={p:2d}: rank(I+J_{p}) = {r} > p-2 = {p - 2} (forbidden);"
            f"  rank(I+J_{p - 1}) = {r2} = p-2 (allowed)"
        )
        assert r > p - 2 and r2 == p - 2
    print("    A clique of X\\D of size m has Gram I+J_m, whose rank must be <=")
    print("    dim U = p-2.  Maximal cliques of J(2k,k) have size k+1 = p and are")
    print("    of two kinds: the star of a (k-1)-set, and the k-subsets of a")
    print("    (k+1)-set.  Stars meet D in exactly one block (Steiner).  Hence")
    print("    EVERY (k+1)-set must contain at least one D-block; the exact count")
    print("    |D|(2k-k) = C(2k,k+1) then forces EXACTLY one, i.e. D^c is also an")
    print("    S(k-1,k,2k).  Verified on real zero classes:")
    report("k=2 (S(1,2,4))", [frozenset({0, 1}), frozenset({2, 3})], 4, 2)
    report("k=4 (S(3,4,8))", sqs8(), 8, 4)
    w = witt_s5612()
    assert len(w) == 132, len(w)
    report("k=6 (S(5,6,12) Witt)", w, 12, 6)
    print()
    print("    *** THIS COROLLARY IS VACUOUS -- CORRECTED ***")
    print("    The complement of a t-design is always a t-design, and for these")
    print("    parameters the constant is 1: the number of blocks of an")
    print("    S(k-1,k,2k) DISJOINT from a (k-1)-set is")
    print("      N = sum_j (-1)^j C(k-1,j) lambda_j,  lambda_j = C(2k-j,k-1-j)/(k-j),")
    print("    and N = 1 for every k (checked below).  So D^c is an S(k-1,k,2k)")
    print("    for EVERY such Steiner system, with no reference to a colouring.")
    print("    The clique argument therefore imposes NO constraint at all -- it")
    print("    is weaker even than complement-closure D = D^c, which is the")
    print("    genuine (Hoffman/E_k) fact.  It is NOT a new or stronger")
    print("    bi-Steiner condition and must not be cited as one.")
    for kk in (2, 4, 6, 10, 16, 22):
        N = sum(
            (-1) ** j * comb(kk - 1, j) * (comb(2 * kk - j, kk - 1 - j) // (kk - j))
            for j in range(kk)
        )
        print(f"      k={kk:3d}: N = {N}")
        assert N == 1

    print()
    print("=" * 74)
    print("5.  FAILED ATTACK -- no capacity bound below 15 at k=16")
    print("=" * 74)
    print("    The clique corollary caps cliques but is strictly weaker than what")
    print("    is needed: at k=4 it is satisfied (SQS(8) is complement-closed) yet")
    print("    the true capacity is 1, far below p-2 = 3.  So the collapse at k=4")
    print("    is NOT explained by cliques, and no clique-type argument can give")
    print("    the k=16 bound.")
    print("    Descent note: for a derived LS(4,5,21), |X'\\D'| = 19152 but")
    print(f"    |Y'| = {comb(21, 4)}, so M_D' is WIDE, with kernel of dimension at")
    print(f"    least {19152 - comb(21, 4)}.  Thus linear nullity alone gives no")
    print("    capacity bound there.  The quadratic frame-gluing constraints may")
    print("    still make descent useful; no inherited capacity bound was proved.")
    print()
    section6()
    section7()
    print()
    print("ALL CHECKS PASSED.  Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()
