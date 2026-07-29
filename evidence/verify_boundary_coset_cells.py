#!/usr/bin/env python3
"""Coset-cell calibration of D = block complements on real boundary Steiner
systems: r=3 (S(2,3,7), v=7) and r=5 (S(4,5,11), v=11).

Convention: F(U) = sum_{B in D} (-1)^{|B cap U|}  (sum over the complement
family D; note F_A(U) = (-1)^{|U|} F_D(U) since v-blocks complement).
"""
import sys
import time
from itertools import combinations
from math import comb
from collections import Counter, defaultdict

sys.setrecursionlimit(100000)


# ---- copied from evidence/verify_H_identity.py ----
def algox(X, Y, cap=None):
    solution, out = [], []

    def select(r_):
        cols = []
        for j in Y[r_]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    def deselect(r_, cols):
        for j in reversed(Y[r_]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

    def solve():
        if cap is not None and len(out) >= cap:
            return
        if not X:
            out.append(list(solution))
            return
        c = min(X, key=lambda c: len(X[c]))
        for r_ in sorted(X[c]):
            solution.append(r_)
            cols = select(r_)
            solve()
            deselect(r_, cols)
            solution.pop()

    solve()
    return out


def cover_instance(v, t, blocks):
    Y = {b: [("t", s) for s in combinations(b, t)] for b in blocks}
    X = {}
    for r_, cs in Y.items():
        for c in cs:
            X.setdefault(c, set()).add(r_)
    return X, Y
# ---- end copy ----


def popcount(x):
    return bin(x).count("1")


def mask(s):
    m = 0
    for i in s:
        m |= 1 << i
    return m


def analyze(v, r):
    t0 = time.time()
    blocks = list(combinations(range(v), r))
    X0, Y0 = cover_instance(v, r - 1, blocks)
    A = algox(X0, Y0, cap=1)[0]
    b = len(A)
    assert b == comb(v, r - 1) // r, (b, comb(v, r - 1) // r)
    full = (1 << v) - 1
    D = [full ^ mask(B) for B in A]
    Dset = set(D)
    assert all(popcount(d) == r + 1 for d in D)
    print(f"\n===== r={r}, v={v}: S({r-1},{r},{v}) built, b={b} blocks, "
          f"D = {b} ({r+1})-subsets  [{time.time()-t0:.1f}s cover]")

    # F over all 2^v subsets
    F = [0] * (1 << v)
    for U in range(1 << v):
        s = 0
        for d in D:
            s += 1 if popcount(d & U) % 2 == 0 else -1
        F[U] = s
    assert F[0] == b

    # ---- Part 1: F by |U| ----
    by_size = defaultdict(list)
    for U in range(1 << v):
        by_size[popcount(U)].append(U)
    print("\n[1] F(U) by |U| (F summed over D; F_A = (-1)^{|U|} F_D):")
    print(f"{'|U|':>4} {'#U':>6} {'min':>5} {'max':>5}  distinct values (count)")
    for k in range(v + 1):
        vals = Counter(F[U] for U in by_size[k])
        vs = sorted(vals)
        const = "CONST" if len(vs) == 1 else ""
        print(f"{k:>4} {len(by_size[k]):>6} {vs[0]:>5} {vs[-1]:>5}  "
              f"{ {val: vals[val] for val in vs} } {const}")
    for k in range(r):  # |U| <= r-1
        assert len(set(F[U] for U in by_size[k])) == 1, k
    # |U| = r+1 split by membership in D
    inD = sorted(set(F[U] for U in by_size[r + 1] if U in Dset))
    outD = sorted(set(F[U] for U in by_size[r + 1] if U not in Dset))
    print(f"    |U|={r+1}: F on U in D: {inD}; F on U not in D: {outD}")
    if len(inD) == 1 and len(outD) == 1:
        print(f"    affine in membership: values ({inD[0]}, {outD[0]}), "
              f"difference {inD[0]-outD[0]} (predicted +-2^{r} = {2**r})")

    # ---- Part 2: coset cells over all pairs of (r+1)-sets ----
    Us = by_size[r + 1]
    n = len(Us)
    npairs = n * (n - 1) // 2
    print(f"\n[2] coset cells over all {npairs} unordered pairs of "
          f"distinct ({r+1})-sets:")
    min_cell = None
    bad = 0
    xor_dist = defaultdict(Counter)  # |U1^U2| -> Counter of F(U1^U2)
    table = defaultdict(set)  # (F1,F2 sorted, |xor|) -> set of F(xor)
    table_n = Counter()
    t1 = time.time()
    for i in range(n):
        U1 = Us[i]
        F1 = F[U1]
        for j in range(i + 1, n):
            U2 = Us[j]
            F2 = F[U2]
            Ux = U1 ^ U2
            Fx = F[Ux]
            sx = popcount(Ux)
            xor_dist[sx][Fx] += 1
            key = (min(F1, F2), max(F1, F2), sx)
            table[key].add(Fx)
            table_n[key] += 1
            for s1 in (1, -1):
                for s2 in (1, -1):
                    num = b + s1 * F1 + s2 * F2 + s1 * s2 * Fx
                    if num % 4 != 0 or num < 0:
                        bad += 1
                    cell = num // 4
                    if min_cell is None or cell < min_cell:
                        min_cell = cell
    assert bad == 0
    assert min_cell == (0 if r == 3 else 4)
    print(f"    all 4*{npairs} = {4*npairs} cells nonneg integers: "
          f"{'YES' if bad == 0 else f'NO ({bad} bad)'}")
    print(f"    minimum cell value seen: {min_cell}")
    print(f"    F(U1 xor U2) distribution by |U1 xor U2| (value: #pairs):")
    for sx in sorted(xor_dist):
        d = xor_dist[sx]
        print(f"      |xor|={sx:>2}: { {val: d[val] for val in sorted(d)} }")
    print(f"    [{time.time()-t1:.1f}s pairs]")

    # ---- Part 3: is F(xor) determined by (F1, F2, |xor|)? ----
    multi = {k: v_ for k, v_ in table.items() if len(v_) > 1}
    in_value = inD[0]
    out_value = outD[0]
    assert multi == {
        (out_value, out_value, r + 1): {out_value, in_value}
    }
    print(f"\n[3] table (F(U1), F(U2), |U1 xor U2|) -> set of F(U1 xor U2):")
    print(f"    {len(table)} combos total; {len(multi)} have >1 observed "
          f"value -> F(xor) {'IS' if not multi else 'is NOT'} determined by "
          f"(F1, F2, |xor|)")
    rows = sorted(table.items())
    shown = rows[:30]
    print(f"    {'(F1,F2,|xor|)':>16} {'#pairs':>7}  observed F(xor) values")
    for (f1, f2, sx), vals in shown:
        print(f"    {str((f1, f2, sx)):>16} {table_n[(f1,f2,sx)]:>7}  "
              f"{sorted(vals)}")
    if len(rows) > 30:
        print(f"    ... ({len(rows)-30} more rows truncated)")
        if multi:
            mrows = sorted(multi.items())[:30]
            print(f"    non-singleton combos (up to 30):")
            for (f1, f2, sx), vals in mrows:
                print(f"    {str((f1, f2, sx)):>16} "
                      f"{table_n[(f1,f2,sx)]:>7}  {sorted(vals)}")
    print(f"    total elapsed r={r}: {time.time()-t0:.1f}s")

    triangle_pairs = 0
    mixed_pairs = 0
    for i, U1 in enumerate(Us):
        for U2 in Us[i + 1 :]:
            if popcount(U1 ^ U2) != r + 1:
                continue
            memberships = (U1 in Dset, U2 in Dset)
            if memberships == (True, True):
                triangle_pairs += 1
                assert (U1 ^ U2) in Dset
            elif memberships[0] != memberships[1]:
                mixed_pairs += 1
                assert (U1 ^ U2) not in Dset
    assert triangle_pairs == {3: 21, 5: 660}[r]
    assert mixed_pairs == {3: 84, 5: 11_880}[r]
    return {
        "r": r,
        "blocks": b,
        "triangle_pairs": triangle_pairs,
        "mixed_pairs": mixed_pairs,
        "minimum_cell": min_cell,
        "undetermined_table_entries": len(multi),
    }


if __name__ == "__main__":
    results = (analyze(7, 3), analyze(11, 5))
    print(f"\nboundary_results={results}")
    print("boundary coset-cell and finite triangle laws: PASS")
