#!/usr/bin/env python3
"""Machine controls for the adjacency-rigidity theorems in PROOF.md §6
and their k=2 / k=4 controls (§7), plus k=16 cross-checks against the
actual K18 witnesses.

Checks:
  A. Completion identity (Lemma 1) and deletion identity (Lemma 6),
     exhaustively over F_4 and F_8 (all subsets), and over F_32 on the
     three certificate masks and their completions.
  B. Theorem R1/R2 control at k=4: for every actual edge of J(8,4)
     (every 5-set R over F_8, every deletion pair), the determined
     witness data (rho_1, u, v, rho_2..rho_4) reconstruct R's prefix
     exactly and the pair conditions C3, C4 hold.  Also: C3 or C4 fails
     for at least one NON-adjacent pair of distinct-e1 states, so the
     conditions are not vacuous.
  C. k=2 control over F_4: R1's determined (rho_1, u, v) match every
     actual edge of J(4,2); there are no C_j conditions (j>=3), i.e. the
     machinery yields no false obstruction where a tight colouring exists.
  D. k=16: for each of the 153 K18 pairs, with R = B_i ∪ {x,y} the actual
     witness, the determined data of R1 equal the true (rho, u, v), the
     conditions C3, C4 hold, and the two linear lambda tail equations of
     Theorem R2 hold with R's actual (rho_5..rho_8).
"""

from itertools import combinations

FIELDS = {4: (7, 2), 8: (11, 3), 32: (37, 5)}  # q -> (reduction, degree)


def mul(q, a, b):
    red, deg = FIELDS[q]
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a >> deg & 1:
            a ^= red
        b >>= 1
    return r


def epoly(q, elems, deg=None):
    if deg is None:
        deg = len(elems)
    e = [0] * (deg + 1)
    e[0] = 1
    for z in elems:
        for j in range(deg, 0, -1):
            e[j] ^= mul(q, z, e[j - 1])
    return e


def gpow(q, a, n):
    r = 1
    while n:
        if n & 1:
            r = mul(q, r, a)
        a = mul(q, a, a)
        n >>= 1
    return r


def ginv(q, a):
    return gpow(q, a, q - 2)


def delete(q, rho, x, j):
    """e_j(R \\ {x}) via Lemma 6."""
    acc = 0
    for i in range(j + 1):
        c = rho[j - i] if j - i < len(rho) else 0
        acc ^= mul(q, c, gpow(q, x, i))
    return acc


def check_identities():
    for q in (4, 8):
        for msk in range(1 << q):
            elems = [z for z in range(q) if msk >> z & 1]
            e = epoly(q, elems, len(elems) + 1)
            for p in range(q):
                if p in elems:
                    f = epoly(q, [z for z in elems if z != p])
                    for j in range(len(elems)):
                        assert (f[j] if j < len(f) else 0) == delete(q, e, p, j)
                else:
                    f = epoly(q, elems + [p])
                    for j in range(1, len(elems) + 2):
                        want = e[j] if j < len(e) else 0
                        prev = e[j - 1] if j - 1 < len(e) else 0
                        got = f[j] if j < len(f) else 0
                        assert got == want ^ mul(q, p, prev)
    q = 32
    for B in MASKS:
        elems = [z for z in range(32) if B >> z & 1]
        e = epoly(q, elems, 16)
        for p in range(32):
            if p in elems:
                continue
            f = epoly(q, elems + [p], 16)
            for j in range(1, 17):
                assert f[j] == e[j] ^ mul(q, p, e[j - 1])
    print("A. completion/deletion identities: PASS")


def determined_clean(q, A, B, m):
    """Theorem R1: (rho_0..rho_m, u, v) from two m-prefix states
    A, B = [e1..em].  Returns None if the states share e1.
    rho_j = e_j(A) + sum_{i=1..j} rho_{j-i} u^i, solved recursively."""
    s = A[0] ^ B[0]
    if s == 0:
        return None
    t = mul(q, A[1] ^ B[1], ginv(q, s))
    rho = [1, t ^ s]
    u = B[0] ^ t
    v = A[0] ^ t
    for j in range(2, m + 1):
        acc = A[j - 1]
        for i in range(1, j + 1):
            acc ^= mul(q, rho[j - i], gpow(q, u, i))
        rho.append(acc)
    return rho, u, v


def pair_conditions(q, A, B, m):
    """C_j, 3<=j<=m, of Theorem R2.  Returns list of booleans."""
    det = determined_clean(q, A, B, m)
    if det is None:
        return None
    rho, u, v = det
    out = []
    for j in range(3, m + 1):
        acc = 0
        for i in range(j + 1):
            acc ^= mul(q, rho[j - i] if j - i < len(rho) else 0,
                       gpow(q, v, i))
        out.append(acc == B[j - 1])
    return out


def check_k4():
    q, k = 8, 4
    stats = {}
    for S in combinations(range(8), 4):
        stats[S] = epoly(q, list(S))[1:5]
    checked = 0
    for R in combinations(range(8), 5):
        rho = epoly(q, list(R))
        for u, v in combinations(R, 2):
            SA = tuple(z for z in R if z != u)
            SB = tuple(z for z in R if z != v)
            A, B = stats[SA], stats[SB]
            det = determined_clean(q, A, B, 4)
            assert det is not None, "adjacent states share e1"
            drho, du, dv = det
            assert (du, dv) == (u, v)
            assert drho[1:5] == rho[1:5]
            assert all(pair_conditions(q, A, B, 4))
            checked += 1
    assert checked == 56 * 10
    fails = 0
    allsets = list(stats)
    for SA, SB in combinations(allsets, 2):
        if len(set(SA) & set(SB)) == 3:
            continue
        pc = pair_conditions(q, stats[SA], stats[SB], 4)
        if pc is not None and not all(pc):
            fails += 1
    assert fails > 0
    print(f"B. k=4 control: R1/R2 hold on all {checked} actual edges of "
          f"J(8,4); C3/C4 fail for {fails} non-adjacent prefix pairs "
          f"(conditions are not vacuous)")


def check_k2():
    q = 4
    stats = {S: epoly(q, list(S))[1:3] for S in combinations(range(4), 2)}
    checked = 0
    for R in combinations(range(4), 3):
        rho = epoly(q, list(R))
        for u, v in combinations(R, 2):
            SA = tuple(z for z in R if z != u)
            SB = tuple(z for z in R if z != v)
            det = determined_clean(q, stats[SA], stats[SB], 2)
            assert det is not None
            drho, du, dv = det
            assert (du, dv) == (u, v) and drho[1:3] == rho[1:3]
            checked += 1
    print(f"C. k=2 control: R1 reconstructs all {checked} actual edges of "
          f"J(4,2); no C_j exist, no false obstruction where the tight "
          f"3-colouring exists")


CLAIM = [(31, 31), (26, 28), (25, 4), (24, 9), (23, 14), (22, 3),
         (19, 0), (17, 21), (16, 24), (13, 22), (12, 27), (11, 13),
         (10, 0), (9, 24), (6, 31), (2, 17), (1, 9), (0, 4)]
MASKS = [0x7975CD00, 0x149693B9, 0xFA3041BA]


def check_k16():
    q = 32
    lam = dict(CLAIM)
    xs = [x for x, _ in CLAIM]
    outside = [{x for x in xs if not (B >> x & 1)} for B in MASKS]
    checked = 0
    for x, y in combinations(xs, 2):
        A = [1 ^ x, x, 0, 0]
        B = [1 ^ y, y, 0, 0]
        assert all(pair_conditions(q, A, B, 4)), (x, y)
        det = determined_clean(q, A, B, 4)
        drho, du, dv = det
        assert (du, dv) == (y, x)
        wit = next(i for i in range(3)
                   if x in outside[i] and y in outside[i])
        Relems = [z for z in range(32) if MASKS[wit] >> z & 1] + [x, y]
        rho = epoly(q, Relems, 9)
        assert drho[1:5] == rho[1:5]
        for state, dp in ((A + [lam[x]], du), (B + [lam[y]], dv)):
            tail = 0
            for i in range(9):
                tail ^= mul(q, rho[8 - i], gpow(q, dp, i))
            assert state[4] ^ gpow(q, state[0], 8) == tail
        checked += 1
    assert checked == 153
    print(f"D. k=16: R1/R2 + lambda tail equations verified against the "
          f"actual witness 17-sets on all {checked} K18 pairs")


if __name__ == "__main__":
    check_identities()
    check_k2()
    check_k4()
    check_k16()
    print("PASS: all rigidity controls hold")
