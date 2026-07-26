#!/usr/bin/env python3
"""Independent verifier for `cyclic_layer_recursion_prime_census.md`.

Stdlib only.  No solver is used anywhere in this file: every existence claim
is a witness that is checked here, and every non-existence claim is an
exhaustive search that terminates.

Run:  python3 -B evidence/verify_cyclic_layer_recursion_prime_census.py
      python3 -B evidence/verify_cyclic_layer_recursion_prime_census.py --quick

`--quick` skips the p=13 exhaustive slice census (section 5), which is the
only slow part.
"""
from __future__ import annotations

import sys
import time
from itertools import combinations

# --------------------------------------------------------------------------
# The two golf designs of Z_17 used in the note.
# --------------------------------------------------------------------------

# Wallis circulant golf array, exactly as in evidence/global_latin_audit.py.
FIRST_HALF_COLUMNS = (
    tuple(range(2, 17)),
    (5, 1, 7, 8, 9, 16, 14, 4, 13, 15, 10, 6, 11, 3, 12),
    (9, 10, 12, 2, 15, 13, 16, 14, 4, 7, 5, 8, 1, 11, 6),
    (14, 12, 2, 13, 3, 8, 9, 16, 7, 5, 1, 15, 6, 10, 11),
    (16, 11, 13, 15, 1, 3, 6, 10, 2, 14, 4, 7, 8, 12, 9),
    (13, 15, 16, 1, 14, 11, 4, 7, 12, 8, 9, 3, 10, 5, 2),
    (15, 4, 1, 14, 11, 2, 10, 3, 5, 6, 13, 16, 12, 9, 8),
    (12, 13, 14, 11, 10, 9, 2, 6, 16, 3, 15, 1, 7, 4, 5),
)

# A golf design of Z_17 invariant under x -> -x, found in this work.
# Starter 0 is the patterned starter P; starters 2t+1, 2t+2 are swapped by
# negation.  Theorem A says this is the largest multiplier group possible.
SYMMETRIC_GOLF_17 = (
    ((1, 16), (2, 15), (3, 14), (4, 13), (5, 12), (6, 11), (7, 10), (8, 9)),
    ((1, 2), (3, 12), (4, 9), (5, 16), (6, 10), (7, 14), (8, 11), (13, 15)),
    ((1, 12), (2, 4), (3, 10), (5, 14), (6, 9), (7, 11), (8, 13), (15, 16)),
    ((1, 15), (2, 12), (3, 5), (4, 8), (6, 14), (7, 13), (9, 10), (11, 16)),
    ((1, 6), (2, 16), (3, 11), (4, 10), (5, 15), (7, 8), (9, 13), (12, 14)),
    ((1, 9), (2, 6), (3, 4), (5, 11), (7, 12), (8, 15), (10, 13), (14, 16)),
    ((1, 3), (2, 9), (4, 7), (5, 10), (6, 12), (8, 16), (11, 15), (13, 14)),
    ((1, 10), (2, 14), (3, 16), (4, 15), (5, 8), (6, 13), (7, 9), (11, 12)),
    ((1, 14), (2, 13), (3, 15), (4, 11), (5, 6), (7, 16), (8, 10), (9, 12)),
    ((1, 8), (2, 7), (3, 6), (4, 12), (5, 9), (10, 16), (11, 13), (14, 15)),
    ((1, 7), (2, 3), (4, 6), (5, 13), (8, 12), (9, 16), (10, 15), (11, 14)),
    ((1, 13), (2, 5), (3, 9), (4, 14), (6, 8), (7, 15), (10, 11), (12, 16)),
    ((1, 5), (2, 10), (3, 13), (4, 16), (6, 7), (8, 14), (9, 11), (12, 15)),
    ((1, 11), (2, 8), (3, 7), (4, 5), (6, 15), (9, 14), (10, 12), (13, 16)),
    ((1, 4), (2, 11), (3, 8), (5, 7), (6, 16), (9, 15), (10, 14), (12, 13)),
)


def wallis_golf_17():
    """M_i = S_i^{-1}(0) for the fifteen Wallis squares."""
    out = []
    for square in range(15):
        a = [0] + [FIRST_HALF_COLUMNS[j - 1][square] for j in range(1, 9)]
        a.extend([-1] * 8)
        for j in range(9, 17):
            a[j] = (a[17 - j] + j) % 17
        assert sorted(a) == list(range(17))
        edges = set()
        for d in range(1, 17):
            y = (-a[d]) % 17
            x = (y + d) % 17
            if x != y:
                edges.add(frozenset((x, y)))
        out.append(frozenset(edges))
    return tuple(out)


def as_design(rows):
    return tuple(frozenset(frozenset(e) for e in row) for row in rows)


# --------------------------------------------------------------------------
# Layer 1: starters and golf designs
# --------------------------------------------------------------------------

def diff_class(p, e):
    x, y = tuple(e)
    d = (x - y) % p
    return min(d, p - d)


def is_starter(p, m):
    half = (p - 1) // 2
    if len(m) != half:
        return False
    pts = [x for e in m for x in e]
    if sorted(pts) != list(range(1, p)):
        return False
    return sorted(diff_class(p, e) for e in m) == list(range(1, half + 1))


def all_starters(p):
    """Exhaustive recursion on the least unmatched point."""
    out = []

    def rec(free, used, acc):
        if not free:
            out.append(frozenset(acc))
            return
        v = min(free)
        for w in free - {v}:
            d = diff_class(p, frozenset((v, w)))
            if d in used:
                continue
            rec(free - {v, w}, used | {d}, acc + [frozenset((v, w))])

    rec(frozenset(range(1, p)), frozenset(), [])
    return out


def all_starters_bruteforce(p):
    """Independent recount: filter every perfect matching of Z_p\\{0}."""
    out = []

    def rec(free, acc):
        if not free:
            m = frozenset(acc)
            if is_starter(p, m):
                out.append(m)
            return
        v = min(free)
        for w in free - {v}:
            rec(free - {v, w}, acc + [frozenset((v, w))])

    rec(frozenset(range(1, p)), [])
    return out


def _compat(S):
    n = len(S)
    c = [set() for _ in range(n)]
    for a in range(n):
        for b in range(a + 1, n):
            if not (S[a] & S[b]):
                c[a].add(b)
                c[b].add(a)
    return c


def max_disjoint_family(S):
    compat = _compat(S)
    best, best_sol = 0, ()

    def expand(cur, cand):
        nonlocal best, best_sol
        if len(cur) + len(cand) <= best:
            return
        if not cand:
            if len(cur) > best:
                best, best_sol = len(cur), tuple(cur)
            return
        for v in sorted(cand):
            expand(cur + [v], {w for w in cand if w > v and w in compat[v]})
            cand = cand - {v}
            if len(cur) + len(cand) <= best:
                return

    expand([], set(range(len(S))))
    return best, best_sol


def all_golf_designs(S, size):
    compat = _compat(S)
    out = []

    def rec(cur, cand):
        if len(cur) == size:
            out.append(tuple(cur))
            return
        if len(cur) + len(cand) < size:
            return
        for v in sorted(cand):
            rec(cur + [v], {w for w in cand if w > v and w in compat[v]})
            cand = cand - {v}
            if len(cur) + len(cand) < size:
                return

    rec([], set(range(len(S))))
    return out


def check_golf_design(p, design):
    """p-2 pairwise disjoint starters partitioning E(K_{p-1}) on Z_p\\{0}."""
    assert len(design) == p - 2, (len(design), p - 2)
    for m in design:
        assert is_starter(p, m)
    seen = set()
    for m in design:
        assert not (seen & m), "starters must be pairwise disjoint"
        seen |= set(m)
    assert len(seen) == (p - 1) * (p - 2) // 2, "must partition E(K_{p-1})"
    return True


def multiplier_group(p, design):
    S = frozenset(design)
    return [m for m in range(1, p)
            if frozenset(frozenset(frozenset((m * x) % p for x in e) for e in st)
                         for st in design) == S]


# --------------------------------------------------------------------------
# Layer 2: one prescribed-link cyclic slice
# --------------------------------------------------------------------------

def triple_orbits(p):
    seen, reps = set(), []
    for t in combinations(range(p), 3):
        s = frozenset(t)
        if s in seen:
            continue
        for sh in range(p):
            seen.add(frozenset((v + sh) % p for v in s))
        reps.append(tuple(sorted(s)))
    return reps


def slice_search(p, design, i, j, reps):
    """Exhaustive: one translate per triple orbit decomposing K_p-M_i-M_j.

    Returns a phase witness, or None.  The search is complete, so None is a
    proof that this prescribed-link cyclic slice does not exist.
    """
    forb = design[i] | design[j]
    residual = [frozenset(e) for e in combinations(range(p), 2)
                if frozenset(e) not in forb]
    eidx = {e: t for t, e in enumerate(residual)}
    m, nq = len(residual), len(reps)
    assert m == 3 * nq, (m, nq)
    opts = []
    for T in reps:
        row = []
        for c in range(p):
            sh = tuple((v + c) % p for v in T)
            es = [frozenset(x) for x in combinations(sh, 2)]
            if all(e in eidx for e in es):
                mask = 0
                for e in es:
                    mask |= 1 << eidx[e]
                row.append((c, mask))
        opts.append(row)
    by_edge = [[] for _ in range(m)]
    for q in range(nq):
        for oi, (_, mask) in enumerate(opts[q]):
            mm = mask
            while mm:
                b = (mm & -mm).bit_length() - 1
                by_edge[b].append((q, oi))
                mm &= mm - 1
    full = (1 << m) - 1
    chosen = [None] * nq

    def rec(cov, live):
        if cov == full:
            return True
        best = None
        mm = full & ~cov
        while mm:
            b = (mm & -mm).bit_length() - 1
            mm &= mm - 1
            cand = [(q, oi) for (q, oi) in by_edge[b]
                    if (live >> q) & 1 and not (opts[q][oi][1] & cov)]
            if best is None or len(cand) < len(best):
                best = cand
                if not cand:
                    return False
        for (q, oi) in best:
            c, mask = opts[q][oi]
            chosen[q] = c
            if rec(cov | mask, live & ~(1 << q)):
                return True
            chosen[q] = None
        return False

    return tuple(chosen) if rec(0, (1 << nq) - 1) else None


def verify_slice(p, design, i, j, phases, reps):
    forb = design[i] | design[j]
    residual = {frozenset(e) for e in combinations(range(p), 2)
                if frozenset(e) not in forb}
    got = []
    for q, T in enumerate(reps):
        sh = tuple((v + phases[q]) % p for v in T)
        got.extend(frozenset(x) for x in combinations(sh, 2))
    assert len(got) == len(set(got)) == len(residual) and set(got) == residual
    return True


def cycle_type(p, mi, mj):
    adj = {v: [] for v in range(1, p)}
    for e in list(mi) + list(mj):
        x, y = tuple(e)
        adj[x].append(y)
        adj[y].append(x)
    seen, out = set(), []
    for v in range(1, p):
        if v in seen:
            continue
        length, cur, prev = 0, v, None
        while cur not in seen:
            seen.add(cur)
            length += 1
            nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
            prev, cur = cur, nxt
        out.append(length)
    return tuple(sorted(out))


# --------------------------------------------------------------------------

def section1_layer1_object():
    print("=" * 74)
    print("1.  The two golf designs of Z_17 are genuine layer-1 objects")
    print("=" * 74)
    W = wallis_golf_17()
    G = as_design(SYMMETRIC_GOLF_17)
    for name, d in (("Wallis", W), ("(-1)-symmetric", G)):
        check_golf_design(17, d)
        print(f"    {name:16s} 15 disjoint starters partitioning "
              f"E(K_16): ok")
    return W, G


def section2_theorem_a(W, G):
    print()
    print("=" * 74)
    print("2.  Theorem A: multiplier rigidity at the Fermat prime 17")
    print("=" * 74)
    p = 17
    P = frozenset(frozenset((x, (-x) % p)) for x in range(1, 9))
    assert is_starter(p, P), "the patterned starter must be a starter"
    print("    patterned starter P = {{x,-x}} is a starter of Z_17: ok")

    # step (i): negation preserves difference class, so a (-1)-invariant
    # starter has -e = e for every edge, i.e. it equals P.
    for d in (W, G):
        for st in d:
            for e in st:
                ne = frozenset((-x) % p for x in e)
                assert diff_class(p, ne) == diff_class(p, e)
    print("    negation preserves difference class (checked on all 240 edges): ok")
    for pp in (5, 7, 11, 13):
        inv = [m for m in all_starters(pp)
               if frozenset(frozenset((-x) % pp for x in e) for e in m) == m]
        Pp = frozenset(frozenset((x, (-x) % pp))
                       for x in range(1, (pp - 1) // 2 + 1))
        assert inv == [Pp], (pp, inv)
    print("    for p = 5,7,11,13 the ONLY (-1)-invariant starter is P "
          "(exhaustive): ok")

    # step (ii): Z_17^* is cyclic of order 16, so every nontrivial subgroup
    # contains the unique involution -1 = 16.
    units = list(range(1, p))
    subgroups = set()
    for g in units:
        H, x = set(), 1
        while x not in H:
            H.add(x)
            x = (x * g) % p
        subgroups.add(frozenset(H))
    for H in subgroups:
        if len(H) > 1:
            assert 16 in H, H
    assert {len(H) for H in subgroups} == {1, 2, 4, 8, 16}
    print(f"    Z_17^* has {len(subgroups)} subgroups, orders "
          f"{sorted(len(H) for H in subgroups)};")
    print("    every nontrivial one contains -1 = 16: ok")

    # step (iii): the counting conclusion.
    #   H acts on the 15 starters of a golf design.  A starter with
    #   nontrivial stabiliser has -1 in its stabiliser, hence equals P.
    #   If P is in the design: 15 - 1 = 14 = |H| * t, and |H| is a power of
    #   two, so |H| divides 2.  If P is not in the design: 15 = |H| * t with
    #   15 odd, so |H| = 1.
    for size, has_P in ((15, False), (14, True)):
        for h in (1, 2, 4, 8, 16):
            if size % h == 0:
                assert h <= 2 or not has_P, (size, h)
    assert 15 % 4 and 15 % 2, "15 is odd"
    assert 14 % 4 == 2, "14 = 2 x 7 admits only |H| = 1 or 2"
    print("    counting: 15 odd => |H|=1 without P; 14 = 2x7 => |H| | 2 with P: ok")

    mw, mg = multiplier_group(17, W), multiplier_group(17, G)
    assert mw == [1], mw
    assert mg == [1, 16], mg
    assert P not in set(W) and P in set(G)
    print(f"    Wallis multiplier group = {mw} (P not a member) -- "
          "trivial, as Theorem A forces")
    print(f"    symmetric design multiplier group = {mg} (P is a member) -- "
          "attains the bound")


def section3_census():
    print()
    print("=" * 74)
    print("3.  Layer-1 census: is there a golf design of Z_p at all?")
    print("=" * 74)
    verdicts = {}
    for p in (3, 5, 7, 11, 13):
        S = all_starters(p)
        assert set(S) == set(all_starters_bruteforce(p)), p
        need = p - 2
        best, sol = max_disjoint_family(S)
        exists = best >= need
        if exists:
            check_golf_design(p, tuple(S[i] for i in sol[:need]))
        verdicts[p] = exists
        print(f"    p={p:3d}  k={p-1:3d}  starters={len(S):6d} (two independent "
              f"enumerations agree)")
        print(f"             max pairwise disjoint={best:3d}  need={need:3d}  "
              f"-> golf design {'EXISTS' if exists else 'IMPOSSIBLE'}")
    assert verdicts == {3: True, 5: False, 7: False, 11: False, 13: True}
    print()
    print("    => the cyclic ansatz is impossible at LAYER 1 for k = 4, 6, 10.")
    print("    => k = 2, where a tight colouring does exist, is NOT obstructed.")


def section4_p13(quick):
    print()
    print("=" * 74)
    print("4.  k=12: every golf design of Z_13, every prescribed-link slice")
    print("=" * 74)
    p = 13
    S = all_starters(p)
    fams = all_golf_designs(S, p - 2)
    print(f"    Z_13 has exactly {len(fams)} golf designs")
    assert len(fams) == 4
    designs = [tuple(S[i] for i in f) for f in fams]
    for d in designs:
        check_golf_design(p, d)

    def mul(m, d):
        return frozenset(frozenset(frozenset((m * x) % p for x in e) for e in st)
                         for st in d)

    orbit = {mul(m, designs[0]) for m in range(1, p)}
    assert {frozenset(d) for d in designs} <= orbit
    print(f"    all {len(fams)} lie in a single orbit under multiplication "
          "by Z_13^*")
    print(f"    multiplier group of design 0: {multiplier_group(p, designs[0])} "
          "(order 3 -- Theorem A does not apply, 13 is not a Fermat prime)")
    if quick:
        print("    [--quick] skipping the exhaustive slice census")
        return
    reps = triple_orbits(p)
    assert len(reps) == 22
    table = {}
    for t, d in enumerate(designs):
        good = bad = 0
        t0 = time.time()
        for (i, j) in combinations(range(p - 2), 2):
            ct = cycle_type(p, d[i], d[j])
            w = slice_search(p, d, i, j, reps)
            if w is None:
                bad += 1
            else:
                verify_slice(p, d, i, j, w, reps)
                good += 1
            table.setdefault(ct, [0, 0])[0 if w is None else 1] += 1
        print(f"    design {t}: {good:3d} slices feasible (witness verified), "
              f"{bad:3d} PROVED infeasible   ({time.time() - t0:.0f}s)")
        assert (good, bad) == (24, 31), (good, bad)
        sys.stdout.flush()
    print()
    print("    => for EVERY golf design of Z_13, 31 of the 55 prescribed-link")
    print("       slices do not exist.  Hence there is no C_13-equivariant")
    print("       tight 13-colouring of J(24,12).  The obstruction is already")
    print("       at a SINGLE slice -- it is not a coupling failure.")
    print()
    print("    refuted hypothesis: the cycle type of M_i u M_j does NOT decide")
    print("    slice feasibility (every type yields both outcomes):")
    for ct in sorted(table):
        inf, fea = table[ct]
        print(f"       {str(ct):18s} infeasible={inf:4d}  feasible={fea:4d}")
        assert inf > 0 and fea > 0, ct


def layer2_data(p, design):
    """F[i][q] = the 3 shifts s with (T_q + s) meeting M_i; B[q][c] = holes."""
    owner = {}
    for i, m in enumerate(design):
        for e in m:
            owner[e] = i
    reps = triple_orbits(p)
    n = len(design)
    F = [[set() for _ in reps] for _ in range(n)]
    B = [[set() for _ in range(p)] for _ in reps]
    for q, T in enumerate(reps):
        for s in range(p):
            sh = tuple((v + s) % p for v in T)
            for e in (frozenset(x) for x in combinations(sh, 2)):
                if 0 in e:
                    continue
                i = owner[e]
                F[i][q].add(s)
                B[q][s].add(i)
    return reps, F, B


def section5_crosscheck(W, G):
    """Reproduce the p=17 numbers documented in cyclic17_equivariant_reduction.md
    and cyclic17_vertex_degree_structure.md, from this independent code path."""
    print()
    print("=" * 74)
    print("5.  Cross-check against the recorded p=17 Wallis numbers")
    print("=" * 74)
    p = 17
    for name, d in (("Wallis", W), ("(-1)-symmetric", G)):
        reps, F, B = layer2_data(p, d)
        assert len(reps) == 40
        hist, total = {}, 0
        for (i, j) in combinations(range(15), 2):
            for q in range(40):
                sz = len([c for c in range(p)
                          if c not in F[i][q] and c not in F[j][q]])
                hist[sz] = hist.get(sz, 0) + 1
                total += sz
        bh = {}
        vt = {i: 0 for i in range(15)}
        pr = {}
        for q in range(40):
            for c in range(p):
                bh[len(B[q][c])] = bh.get(len(B[q][c]), 0) + 1
                if len(B[q][c]) == 3:
                    for i in B[q][c]:
                        vt[i] += 1
                    for a, b in combinations(sorted(B[q][c]), 2):
                        pr[(a, b)] = pr.get((a, b), 0) + 1
        assert all(len(F[i][q]) == 3 for i in range(15) for q in range(40))
        assert bh == {1: 120, 3: 560}, bh
        assert total == 47880 and total // 105 == 456
        assert set(vt.values()) == {112} and set(pr.values()) == {16}
        print(f"    {name:16s} |B_c(q)| histogram {bh}")
        print(f"    {'':16s} 47,880 phase literals, 456 per fixed pair,")
        print(f"    {'':16s} 2-(15,3,16) multidesign: 112 per square, 16 per pair")
        print(f"    {'':16s} phase-domain sizes {dict(sorted(hist.items()))}")
        if name == "Wallis":
            assert hist == {11: 2658, 12: 1407, 13: 132, 14: 3}, hist
            print(f"    {'':16s} -> matches the recorded distribution exactly")
    print()
    print("    The aggregate invariants are forced by the golf-design axioms and")
    print("    are design-independent; the fine domain-size distribution is not.")


def main():
    quick = "--quick" in sys.argv
    W, G = section1_layer1_object()
    section2_theorem_a(W, G)
    section3_census()
    section5_crosscheck(W, G)
    section4_p13(quick)
    print()
    print("All checks passed.")
    print("Nothing here resolves Erdos-Rosenfeld #835, which remains OPEN.")


if __name__ == "__main__":
    main()
