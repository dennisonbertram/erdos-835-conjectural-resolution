#!/usr/bin/env python3
"""Verifier for evidence/triangle_closure_derived_reduction.md.

Checks, in exact integer arithmetic and with no third-party imports:

  1. The parameter table.  For an S(k-1,k,3k) the number N_0(k) of blocks
     disjoint from a fixed block is determined by the parameters; recompute it
     and record which k are arithmetically admissible.

  2. The reduction.  For an S(r-1,r,2r+1) and two blocks meeting in exactly
     m=(r-1)/2 points, the derived design at their intersection is an
     S(m,m+1,3m+3), the two block-differences are disjoint blocks of it, and
     (B1 xor B2)^complement is a block of the parent design if and only if the
     complement of their union inside the derived point set is a block of the
     derived design.  Checked constructively on the Fano plane (r=3) and on an
     S(4,5,11) built here by exact cover (r=5).

  3. The mechanism.  In those two derived designs every block is disjoint from
     exactly two others, matching N_0(2)=N_0(3)=2, and the injective map
     T -> B_T of the proof has image of size at most 2 whenever it avoids W.

  4. The negative control.  N_0 is NOT 2 at the next admissible parameters, so
     the mechanism that proves triangle closure at r=3,5 is absent from r=9 on.

Run:  python3 -B evidence/verify_triangle_closure_reduction.py
"""

from fractions import Fraction
from itertools import combinations
from math import comb

FAILURES = []


def check(label, cond, detail=""):
    status = "ok  " if cond else "FAIL"
    print(f"  [{status}] {label}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(label)


# --------------------------------------------------------------------------
# 1. Parameters of the derived family S(k-1, k, 3k)
# --------------------------------------------------------------------------

def lam(k, s):
    """Blocks of an S(k-1,k,3k) through a fixed s-set (s <= k)."""
    if s == k:
        return Fraction(1)
    return Fraction(comb(3 * k - s, k - 1 - s), k - s)


def admissible(k):
    """All lambda_s integral -- the arithmetic condition for S(k-1,k,3k)."""
    return all(lam(k, s).denominator == 1 for s in range(k))


def n0(k):
    """Blocks disjoint from a fixed block, by inclusion-exclusion over it."""
    total = sum((-1) ** j * comb(k, j) * lam(k, j) for j in range(k + 1))
    assert total.denominator == 1
    return int(total)


def parameter_table():
    print("1. Derived-family parameters  S(k-1, k, 3k)")
    rows = []
    for k in range(2, 13):
        r = 2 * k - 1                      # the parent parameter, m = k-1
        rows.append((k, 3 * k, r, admissible(k), n0(k) if admissible(k) else None))
    print("     k   v=3k   r=2k-1   admissible   N_0")
    for k, v, r, adm, val in rows:
        print(f"    {k:2d}  {v:5d}   {r:6d}   {str(adm):10s}   "
              f"{'-' if val is None else val}")
    got = {k: val for k, v, r, adm, val in rows if adm}
    check("N_0(2) = 2", got[2] == 2)
    check("N_0(3) = 2", got[3] == 2)
    check("N_0 = 2 only for k in {2,3}",
          [k for k, val in got.items() if val == 2] == [2, 3])
    check("N_0(5) = 22  (r=9)", got[5] == 22)
    check("N_0(8) = 758 (r=15)", got[8] == 758)
    check("N_0(9) = 2558 (r=17)", got[9] == 2558)
    check("k = 4, 7, 10, 12 inadmissible",
          all(not admissible(k) for k in (4, 7, 10, 12)))
    return got


# --------------------------------------------------------------------------
# 2. Designs used as instances
# --------------------------------------------------------------------------

FANO = [frozenset(b) for b in
        [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
         (1, 4, 6), (2, 3, 6), (2, 4, 5)]]


def exact_cover_steiner(v, k, t):
    """Build one S(t,k,v) by exact cover on the t-subsets.  Deterministic."""
    tsets = list(combinations(range(v), t))
    tidx = {s: i for i, s in enumerate(tsets)}
    cands = [(c, [tidx[s] for s in combinations(c, t)])
             for c in combinations(range(v), k)]
    cover = [[] for _ in tsets]
    for i, (_, ts) in enumerate(cands):
        for s in ts:
            cover[s].append(i)
    used = [False] * len(tsets)
    chosen = []

    def rec():
        best, best_n = -1, len(cands) + 1
        for s in range(len(tsets)):
            if used[s]:
                continue
            n = sum(1 for i in cover[s]
                    if not any(used[x] for x in cands[i][1]))
            if n < best_n:
                best_n, best = n, s
            if n == 0:
                return False
        if best == -1:
            return True
        for i in cover[best]:
            ts = cands[i][1]
            if any(used[x] for x in ts):
                continue
            for x in ts:
                used[x] = True
            chosen.append(cands[i][0])
            if rec():
                return True
            chosen.pop()
            for x in ts:
                used[x] = False
        return False

    if not rec():
        raise RuntimeError(f"no S({t},{k},{v}) found")
    return [frozenset(b) for b in chosen]


def is_steiner(blocks, points, t, k):
    seen = {}
    for b in blocks:
        if len(b) != k:
            return False
        for s in combinations(sorted(b), t):
            if s in seen:
                return False
            seen[s] = True
    return len(seen) == comb(len(points), t)


# --------------------------------------------------------------------------
# 3. The reduction, checked constructively
# --------------------------------------------------------------------------

def verify_instance(A, X, r, expected_pairs, expected_derived_blocks):
    m = (r - 1) // 2
    Aset = set(A)
    pairs = closed = 0
    derived_sizes = set()
    disjoint_counts = set()
    image_sizes = set()

    for B1, B2 in combinations(A, 2):
        I = B1 & B2
        if len(I) != m:
            continue
        pairs += 1
        S1, S2 = B1 - I, B2 - I
        W = X - (B1 | B2)
        K = I | W

        # -- part 1: set algebra -------------------------------------------
        if not (len(S1) == len(S2) == len(W) == m + 1 and len(K) == r
                and K == X - (B1 ^ B2) and not (S1 & S2) and not (I & W)):
            FAILURES.append("size/identity algebra")
            return

        # -- the derived design at I ---------------------------------------
        P = X - I
        AI = [b - I for b in A if I <= b]
        AIset = set(AI)
        derived_sizes.add(len(AI))
        if len(P) != 3 * m + 3 or not is_steiner(AI, P, m, m + 1):
            FAILURES.append("derived design is not S(m,m+1,3m+3)")
            return
        if S1 not in AIset or S2 not in AIset:
            FAILURES.append("S1,S2 not derived blocks")
            return

        # -- part 1 conclusion: the equivalence ----------------------------
        if (K in Aset) != (W in AIset):
            FAILURES.append("reduction equivalence")
            return
        if K in Aset:
            closed += 1

        # -- part 2: the counting mechanism --------------------------------
        # every block of A_I is disjoint from exactly N_0(m+1) others
        for b in AI:
            disjoint_counts.add(sum(1 for c in AI if c != b and not (b & c)))
        # the injective map T -> B_T on the m-subsets of W
        image = set()
        inside = False
        for T in combinations(sorted(W), m):
            Ts = frozenset(T)
            BT = next(b for b in AI if Ts <= b)
            if BT <= W:
                inside = True
            image.add(BT)
        if len(image) != m + 1 and not inside:
            FAILURES.append("T -> B_T not injective")
            return
        if not inside:
            image_sizes.add(len(image))

    check(f"r={r}: qualifying pairs", pairs == expected_pairs,
          f"{pairs} (expected {expected_pairs})")
    check(f"r={r}: triangle closure holds on every qualifying pair",
          closed == pairs, f"{closed}/{pairs}")
    check(f"r={r}: derived design block count",
          derived_sizes == {expected_derived_blocks},
          f"{sorted(derived_sizes)}")
    check(f"r={r}: every derived block disjoint from exactly N_0(m+1)={n0(m+1)}",
          disjoint_counts == {n0(m + 1)}, f"{sorted(disjoint_counts)}")
    check(f"r={r}: no pair needed the 'B_T avoids W' branch",
          not image_sizes,
          "branch never taken (some B_T always lies inside W)"
          if not image_sizes else f"image sizes {sorted(image_sizes)}")


# --------------------------------------------------------------------------

def main():
    print(__doc__.strip().splitlines()[0])
    print()
    parameter_table()

    print()
    print("2. Fano plane, r = 3 (m = 1)")
    X7 = frozenset(range(7))
    check("Fano is an S(2,3,7)", is_steiner(FANO, X7, 2, 3))
    verify_instance(FANO, X7, 3, expected_pairs=21, expected_derived_blocks=3)

    print()
    print("3. S(4,5,11) built by exact cover, r = 5 (m = 2)")
    A11 = exact_cover_steiner(11, 5, 4)
    X11 = frozenset(range(11))
    check("constructed design is an S(4,5,11)", is_steiner(A11, X11, 4, 5))
    check("block count is C(11,4)/C(5,4) = 66", len(A11) == 66)
    verify_instance(A11, X11, 5, expected_pairs=660, expected_derived_blocks=12)

    print()
    print("4. Negative control: the mechanism is absent beyond r = 5")
    check("r=9  derived design S(4,5,15) has N_0 = 22, not 2", n0(5) == 22)
    check("r=15 derived design S(7,8,24) has N_0 = 758, not 2", n0(8) == 758)
    check("758 is even (no immediate parity obstruction at r=15)",
          n0(8) % 2 == 0)

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
        raise SystemExit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
