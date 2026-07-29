#!/usr/bin/env python3
"""Deterministic verifier for collaboration/opus5/first_lift_classB_attack/NOTE.md.

Every claim in NOTE.md that is stated as proved is re-checked here from its
definition.  The exact-arithmetic parts use only the standard library
(fractions.Fraction); scipy and python-sat are used, when present, only for
*additional independent* cross-checks and never for a claim on their own.

Run:  cd collaboration/opus5/first_lift_classB_attack && python3 -B verify_classB.py
"""

from __future__ import annotations

import itertools
import json
import os
import random
import sys
from collections import Counter
from fractions import Fraction

from classb import (check_class_B, check_completion, check_farkas,
                    check_lp_point, cut_certificates, lp_feasible, m_profiles,
                    mvec, random_class_B, random_move, solve_dfs, supports)
from conditions import bc_margin, bc_min, bc_violations, rho_max, vertex_hall

HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "certificates")
OLD = os.path.join(HERE, "..", "first_lift_k13_hole", "certificates")

try:
    from classb import solve_sat
    import pysat                                            # noqa: F401
    HAVE_SAT = True
except Exception:                                           # pragma: no cover
    HAVE_SAT = False

FAIL = []


def c_solver_verdict(forb):
    """Second complete solver: the C engine cbsearch<n>, if it is built."""
    import subprocess
    n = len(forb)
    exe = os.path.join(HERE, "cbsearch%d" % n)
    if not os.path.exists(exe):
        return "SKIPPED (cbsearch%d not built)" % n
    out = subprocess.run([exe, "check", "1", "1", ",".join(map(str, forb))],
                         capture_output=True, text=True).stdout.split()
    return "%s in %s nodes" % (out[1], out[-1])


def section(t):
    print()
    print(t)
    print("-" * len(t))


def ok(msg):
    print("  PASS  " + msg)


# ---------------------------------------------------------------------------
def s1_arithmetic():
    section("1. class-B arithmetic at n = 13 (and the general n)")
    p13 = m_profiles(13)
    assert p13 == [(7, 10, 0), (8, 8, 1), (9, 6, 2), (10, 4, 3), (11, 2, 4),
                   (12, 0, 5)], p13
    for (n5, n3, n1) in p13:
        assert n5 + n3 + n1 == 17 and 5 * n5 + 3 * n3 + n1 == 65
        assert n3 == 24 - 2 * n5 and n1 == n5 - 7
        assert 8 * n5 + 10 * n3 + 12 * n1 == 156
        assert 4 * n5 + 5 * n3 + 6 * n1 == 78
    ok("six m-profiles at n=13; |V_c| in {8,10,12}; sum |V_c| = 156; "
       "sum |V_c|/2 = 78 = C(13,2)")
    for n in range(3, 20, 2):
        for (n5, n3, n1) in m_profiles(n):
            assert 2 * n5 + n3 == 2 * n - 2 and n1 == n5 - n + 6
    ok("general n: 2n5 + n3 = 2n-2 and n1 = n5 - n + 6")


# ---------------------------------------------------------------------------
def s2_bc_specialisations():
    section("2. (BC) contains the two Lemma-1 cuts and vertex Hall")
    rng = random.Random(20260727)
    tested = 0
    for n in (7, 9, 11, 13):
        q = n + 4
        for _ in range(60):
            forb = random_class_B(n, q, rng)
            if forb is None:
                continue
            for _ in range(200):
                nf = random_move(n, q, forb, rng)
                if nf:
                    forb = nf
            try:
                check_class_B(n, q, forb)
            except AssertionError:
                continue
            V = [[a for a in range(n) if not ((forb[a] >> c) & 1)] for c in range(q)]
            full = set(range(n))
            for _ in range(20):
                x = rng.randrange(1, n)
                X = set(rng.sample(range(n), x))
                W = full - X
                # (BC) with W = complement of X  <=>  forced-inside at X
                tot = 0
                for c in range(q):
                    sX = len(set(V[c]) & X)
                    sW = len(set(V[c]) & W)
                    tot += rho_max(sX, sW, 0)
                forced = sum(max(0, len(set(V[c]) & X) - len(V[c]) // 2)
                             for c in range(q))
                assert (tot < x * (n - x)) == (forced > x * (x - 1) // 2), \
                    "(BC) with W = A\\X is not the forced-inside cut"
                tested += 1
            # (BC) with |X| = 1 <=> Hall at that vertex, on the Hall side
            for a in range(n):
                cols = [c for c in range(q) if not ((forb[a] >> c) & 1)]
                for _ in range(10):
                    W = set(rng.sample([b for b in range(n) if b != a],
                                       rng.randrange(1, n - 1)))
                    tot = sum(rho_max(1, len(set(V[c]) & W),
                                      len(V[c]) - 1 - len(set(V[c]) & W))
                              for c in cols)
                    hall = len([c for c in cols if set(V[c]) & W])
                    assert tot == hall
                    tested += 1
    ok("%d random (instance, X, W) checks: (BC) with W = A\\X is exactly the "
       "forced-inside cut, and (BC) with |X| = 1 is exactly the Hall count"
       % tested)


def s3_bc_necessity():
    section("3. (BC) is necessary: no completable instance violates it")
    rng = random.Random(4242)
    tab = Counter()
    for n in (5, 7, 9):
        q = n + 4
        drawn = 0
        while drawn < 400:
            forb = random_class_B(n, q, rng)
            if forb is None:
                continue
            for _ in range(150):
                nf = random_move(n, q, forb, rng)
                if nf:
                    forb = nf
            try:
                check_class_B(n, q, forb)
            except AssertionError:
                continue
            drawn += 1
            st, sols, _ = solve_dfs(n, q, forb, node_budget=10 ** 8)
            assert st in ("SAT", "UNSAT")
            viol = bool(bc_violations(n, q, forb))
            if st == "SAT":
                check_completion(n, q, forb, sols[0])
                assert not viol, "a completable instance violates (BC)"
            tab[(n, st, "BC-violated" if viol else "BC-clean")] += 1
    for k in sorted(tab):
        print("      %-28s %d" % (str(k), tab[k]))
    ok("1200 instances at n=5,7,9: SAT never violates (BC); the "
       "(UNSAT, BC-clean) cells are non-empty, so (BC) is not sufficient")


def s4_bc_theorem():
    section("4. THEOREM: (BC) cannot fire at n = 13 (exact DP)")
    fires = []
    for n in range(3, 18, 2):
        m, x, w, prof = bc_margin(n)
        print("      n=%2d (k=%2d): worst (BC) margin %+d at |X|=%d |W|=%d "
              "profile %s" % (n, n + 3, m, x, w, prof))
        if m > 0:
            fires.append(n)
    assert fires == [5, 7, 9, 11], fires
    ok("a (BC) condition can be violated for n in {5,7,9,11} (k in "
       "{8,10,12,14}) and for NO n in {3,13,15,17}")
    # soundness control: the DP optimum must really be a lower bound for the
    # sum of rho^max over every ACTUAL instance and every disjoint pair X, W.
    rng = random.Random(818)
    ctl = 0
    for _ in range(8):
        forb = random_class_B(13, 17, rng)
        for _ in range(300):
            nf = random_move(13, 17, forb, rng)
            if nf:
                forb = nf
        check_class_B(13, 17, forb)
        V = [set(a for a in range(13) if not ((forb[a] >> c) & 1)) for c in range(17)]
        prof = tuple(Counter(mvec(13, 17, forb))[v] for v in (5, 3, 1))
        for _ in range(60):
            k = rng.randrange(2, 13)
            S = rng.sample(range(13), k)
            cut = rng.randrange(1, k)
            X, W = set(S[:cut]), set(S[cut:])
            tot = 0
            for c in range(17):
                sX, sW = len(V[c] & X), len(V[c] & W)
                tot += rho_max(sX, sW, len(V[c]) - sX - sW)
            lo = bc_min(13, len(X), len(W), prof)
            assert tot >= lo, ("DP optimum is not a lower bound", tot, lo)
            assert tot >= len(X) * len(W), "an actual instance violates (BC)"
            ctl += 1
    ok("%d (instance, X, W) controls at n=13: the DP optimum really is a lower "
       "bound for the actual sum of rho^max, and (BC) holds in every case" % ctl)
    b = bc_margin(13)
    assert b[0] == 0
    ok("at n = 13 the worst margin is exactly 0, attained at |X|=1 (an "
       "identity, not a violation): (BC) holds for every class-B instance")


def s5_hall_lemma():
    section("5. Lemma: vertex Hall holds whenever n >= 2r+1 (here r = 5)")
    # the closed-form argument of NOTE.md section 4, re-run as an exact search
    # over the relaxation it uses.
    r = 5
    bad = []
    for n in range(3, 22, 2):
        q = n + r - 1
        found = False
        # a Hall violation needs d > w, |V_c| <= w+1 for the d colours, and
        # d*(n-1-w) <= r*(n-1-w)
        for w in range(0, n):
            for d in range(w + 1, q - r + 1):
                if n - r > w + 1:
                    continue                       # |V_c| >= n-r forces w >= n-r-1
                if w == n - 1:
                    continue                       # d <= n-1 colours available
                if d * (n - 1 - w) <= r * (n - 1 - w):
                    found = True
        if found:
            bad.append(n)
    assert all(n <= 2 * r for n in bad), bad
    print("      the relaxation admits a Hall violation only for n in %s" % bad)
    ok("no vertex-Hall violation is possible for n >= 2r+1 = 11")
    rng = random.Random(7)
    for n in (11, 13):
        q = n + 4
        for _ in range(300):
            forb = random_class_B(n, q, rng)
            if forb is None:
                continue
            for _ in range(200):
                nf = random_move(n, q, forb, rng)
                if nf:
                    forb = nf
            try:
                check_class_B(n, q, forb)
            except AssertionError:
                continue
            assert not vertex_hall(n, q, forb)
    ok("600 random instances at n = 11, 13: no vertex-Hall violation (control)")


# ---------------------------------------------------------------------------
def check_extension_witness(n, q, forb, arr, parts, colours):
    """Re-check, from the definition, that (arr, parts, colours) exhibits the
    instance as a proper q-edge-colouring of K_{n+5} - E(K_n) that saturates
    the five vertices outside the hole (i.e. that it is in class B')."""
    P = list(range(5))
    pairs5 = [(x, y) for x in range(5) for y in range(x + 1, 5)]
    flat = [p for part in parts for p in part]
    assert sorted(tuple(p) for p in flat) == sorted(pairs5), "not a partition of E(K_5)"
    for part in parts:
        assert 1 <= len(part) <= 2
        if len(part) == 2:
            assert not (set(part[0]) & set(part[1])), "part is not a matching"
    assert len(set(colours)) == len(colours) == len(parts)
    colour_of_pair = {}
    for col, part in zip(colours, parts):
        for pr in part:
            colour_of_pair[tuple(sorted(pr))] = col
    # the partial colouring of K_{n+5} minus the hole
    seenP = [set() for _ in range(5)]
    seenA = [set() for _ in range(n)]
    for x in range(5):
        for a in range(n):
            c = arr[a][x]
            assert c not in seenP[x] and c not in seenA[a], "not proper"
            seenP[x].add(c)
            seenA[a].add(c)
    for (x, y) in pairs5:
        c = colour_of_pair[(x, y)]
        assert c not in seenP[x] and c not in seenP[y], "not proper on K_5"
        seenP[x].add(c)
        seenP[y].add(c)
    for x in range(5):
        assert len(seenP[x]) == q, "vertex of P not saturated"
    for a in range(n):
        m = 0
        for c in seenA[a]:
            m |= 1 << c
        assert m == forb[a], ("missing set at a does not match S_a", a)
    return True


def s6_old_certificates():
    section("6. re-verification of the four stored counterexamples "
            "(k = 8,10,12,14)")
    for name in ("counterexample_n05", "counterexample_n07",
                 "counterexample_n09", "counterexample_n11"):
        d = json.loads(open(os.path.join(OLD, name + ".json")).read())
        n, q, forb = d["n"], d["q"], d["forb"]
        v = check_class_B(n, q, forb)
        parts = [tuple(tuple(p) for p in part) for part in d["parts"]]
        assert check_extension_witness(n, q, forb, d["arr"], parts, d["colours"])
        if n <= 9:
            st, _, nodes = solve_dfs(n, q, forb, node_budget=10 ** 9)
            assert st == "UNSAT", st
            how = "python DFS, %d nodes" % nodes
        else:
            # the python DFS needs ~1.5e7 nodes here; use the C engine as the
            # second complete solver instead (both are exhaustive searches)
            how = c_solver_verdict(forb)
            if how.startswith("SKIPPED"):
                assert HAVE_SAT, "no second complete solver available"
                assert solve_sat(n, q, forb)[0] == "UNSAT"
                how = "CDCL only (%s)" % how
            else:
                assert how.startswith("UNSAT"), how
                how = "C DFS, " + how
        extra = ""
        if HAVE_SAT:
            assert solve_sat(n, q, forb)[0] == "UNSAT"
            extra = " (CDCL SAT solver agrees)"
        bc = bc_violations(n, q, forb) if n <= 9 else bc_violations(n, q, forb, xmax=6)
        assert bc, "no (BC) certificate"
        print("      %-20s n=%2d k=%2d supports %s" %
              (name, n, n + 3, sorted(Counter(v).items())))
        print("        exhaustive search UNSAT (%s)%s; violates (BC) at "
              "X=%s W=%s (%d < %d)"
              % (how, extra, bc[0][0], bc[0][1], bc[0][2], bc[0][3]))
    ok("all four are class-B, are witnessed as class-B' by an explicit proper "
       "colouring of K_{n+5} - E(K_n) saturating the 5 outside vertices, have "
       "no completion, and every one of them violates (BC)")


def s7_new_certificates():
    section("7. new certificates: (BC) is not sufficient, and neither is the LP")
    for name in ("n07_BCclean_LPinfeasible.json", "n07_BCclean_LPfeasible.json",
                 "n09_BCclean.json"):
        d = json.loads(open(os.path.join(CERTS, name)).read())
        n, q, forb = d["n"], d["q"], d["forb"]
        check_class_B(n, q, forb)
        assert not cut_certificates(n, q, forb), "violates a Lemma-1 cut"
        assert not vertex_hall(n, q, forb), "violates vertex Hall"
        assert not bc_violations(n, q, forb), "violates (BC)"
        st, _, nodes = solve_dfs(n, q, forb, node_budget=10 ** 9)
        assert st == "UNSAT", st
        if HAVE_SAT:
            assert solve_sat(n, q, forb)[0] == "UNSAT"
        line = "      %-32s n=%2d supports %s" % (
            name, n, sorted(Counter(supports(n, q, forb)).items()))
        if d["lp_feasible"]:
            x = [Fraction(a, b) for a, b in d["lp_point"]]
            assert check_lp_point(n, q, forb, x), "stored LP point is not feasible"
            print(line)
            print("        (BC)-clean, exhaustive UNSAT in %d nodes, and the "
                  "fractional relaxation IS feasible (exact rational point "
                  "re-checked)" % nodes)
        else:
            y = [Fraction(a, b) for a, b in d["farkas"]]
            assert check_farkas(n, q, forb, y), "stored Farkas certificate fails"
            print(line)
            print("        (BC)-clean, exhaustive UNSAT in %d nodes, "
                  "fractional relaxation infeasible (exact Farkas re-checked)"
                  % nodes)
    ok("(BC) is not sufficient at n = 7 or n = 9, and at n = 7 there is an "
       "instance whose obstruction is invisible even to the fractional "
       "relaxation")


# ---------------------------------------------------------------------------
def s8_solver_crosscheck():
    section("8. solver cross-validation")

    def brute(n, q, forb):
        FULLC = (1 << q) - 1
        edges = [(a, b) for a in range(n) for b in range(a + 1, n)]
        av = [FULLC & ~forb[a] for a in range(n)]

        def rec(i):
            if i == len(edges):
                return all(av[a] == 0 for a in range(n))
            a, b = edges[i]
            m = av[a] & av[b]
            while m:
                lb = m & -m
                m ^= lb
                av[a] ^= lb
                av[b] ^= lb
                if rec(i + 1):
                    return True
                av[a] ^= lb
                av[b] ^= lb
            return False
        return rec(0)

    rng = random.Random(31337)
    n, q = 7, 11
    agree = sat = unsat = 0
    while agree < 500:
        forb = random_class_B(n, q, rng)
        if forb is None:
            continue
        for _ in range(120):
            nf = random_move(n, q, forb, rng)
            if nf:
                forb = nf
        try:
            check_class_B(n, q, forb)
        except AssertionError:
            continue
        st, sols, _ = solve_dfs(n, q, forb, node_budget=10 ** 8)
        b = brute(n, q, forb)
        assert (st == "SAT") == b, ("solvers disagree", forb)
        if HAVE_SAT:
            assert (solve_sat(n, q, forb)[0] == "SAT") == b
        if st == "SAT":
            check_completion(n, q, forb, sols[0])
            sat += 1
        else:
            unsat += 1
        agree += 1
    ok("500 instances at n=7: DFS, an independent fixed-order brute force%s "
       "all agree (%d SAT, %d UNSAT); every SAT witness re-checked"
       % (", and a CDCL SAT solver" if HAVE_SAT else "", sat, unsat))


# ---------------------------------------------------------------------------
def gen_family(NR, NC, rowsum, sizes):
    """The twin5 generator, in Python, for arbitrary small parameters.
    Yields column-mask tuples satisfying (C) and (R) of NOTE.md section 6."""
    cap = [rowsum] * NR
    blockid = [0] * NR
    cols = []

    def val(m):
        v = 0
        for i in range(NR):
            if (m >> i) & 1:
                v |= 1 << (NR - 1 - i)
        return v

    def feasible(left):
        T = sum(cap)
        if T > max(sizes) * left or T < min(sizes) * left:
            return False
        # exact reachability of T as a sum of `left` values from `sizes`
        reach = {0}
        for _ in range(left):
            reach = set(t + s for t in reach for s in sizes if t + s <= T)
        if T not in reach:
            return False
        return max(cap) <= left

    def rec(j, prev):
        if j == NC:
            if all(c == 0 for c in cap):
                yield tuple(cols)
            return
        if not feasible(NC - j):
            return
        for m in range(1 << NR):
            k = bin(m).count("1")
            if k not in sizes:
                continue
            if val(m) > prev:
                continue
            if any(((m >> i) & 1) and cap[i] == 0 for i in range(NR)):
                continue
            bad = False
            for i in range(NR - 1):
                if blockid[i] == blockid[i + 1] and not ((m >> i) & 1) and ((m >> (i + 1)) & 1):
                    bad = True
                    break
            if bad:
                continue
            old = list(blockid)
            for i in range(NR):
                if (m >> i) & 1:
                    cap[i] -= 1
            nb, cur, curbit = 0, -1, -1
            for i in range(NR):
                bit = (m >> i) & 1
                if old[i] != cur or bit != curbit:
                    nb += 1
                    cur, curbit = old[i], bit
                blockid[i] = nb
            cols.append(m)
            yield from rec(j + 1, val(m))
            cols.pop()
            for i in range(NR):
                blockid[i] = old[i]
                if (m >> i) & 1:
                    cap[i] += 1
    yield from rec(0, (1 << NR) - 1 if False else 10 ** 9)


def s9_generator_completeness():
    section("9. the twin5 enumeration scheme is complete (unit test)")
    # small analogue: 4 x 5 matrices, row sums 3, column sizes in {1,3}
    NR, NC, RS, SZ = 4, 6, 3, (1, 3)
    gen = set()
    for cols in gen_family(NR, NC, RS, SZ):
        gen.add(tuple(sorted(cols)))
    # brute force over ALL labelled matrices, reduced modulo S_NR x S_NC
    allm = []
    for cols in itertools.product([m for m in range(1 << NR)
                                   if bin(m).count("1") in SZ], repeat=NC):
        if all(sum((m >> i) & 1 for m in cols) == RS for i in range(NR)):
            allm.append(cols)
    orbits = set()
    for cols in allm:
        best = None
        for perm in itertools.permutations(range(NR)):
            mapped = tuple(sorted(sum(((m >> i) & 1) << perm[i] for i in range(NR))
                                  for m in cols))
            if best is None or mapped < best:
                best = mapped
        orbits.add(best)
    genorb = set()
    for cols in gen:
        best = None
        for perm in itertools.permutations(range(NR)):
            mapped = tuple(sorted(sum(((m >> i) & 1) << perm[i] for i in range(NR))
                                  for m in cols))
            if best is None or mapped < best:
                best = mapped
        genorb.add(best)
    assert orbits and genorb == orbits, (len(genorb), len(orbits))
    ok("on the 4x6 analogue: %d labelled matrices fall into %d orbits, and the "
       "generator produces a representative of every one of them"
       % (len(allm), len(orbits)))
    # a second, larger analogue
    NR, NC, RS, SZ = 5, 5, 3, (3,)
    gen = set()
    for cols in gen_family(NR, NC, RS, SZ):
        gen.add(tuple(sorted(cols)))
    allm = []
    for cols in itertools.product([m for m in range(1 << NR)
                                   if bin(m).count("1") in SZ], repeat=NC):
        if all(sum((m >> i) & 1 for m in cols) == RS for i in range(NR)):
            allm.append(cols)
    orbits, genorb = set(), set()
    for src, dst in ((allm, orbits), (gen, genorb)):
        for cols in src:
            best = None
            for perm in itertools.permutations(range(NR)):
                mapped = tuple(sorted(sum(((m >> i) & 1) << perm[i] for i in range(NR))
                                      for m in cols))
                if best is None or mapped < best:
                    best = mapped
            dst.add(best)
    assert orbits and genorb == orbits, (len(genorb), len(orbits))
    ok("on the 5x5 analogue: %d labelled matrices, %d orbits, all generated"
       % (len(allm), len(orbits)))


def s9b_generator_vs_C():
    section("9b. the python and C enumerators agree (exhaustive small pairs)")
    for (n, r, sizes, want, unsat) in ((5, 5, (5, 3, 1), 248, 185),
                                       (7, 3, (3, 1), 1535, 2)):
        q = n + r - 1
        cnt = 0
        bad = 0
        for cols in gen_family(n, q, r, sizes):
            forb = [0] * n
            for i in range(n):
                f = 0
                for j, m in enumerate(cols):
                    if (m >> i) & 1:
                        f |= 1 << j
                forb[i] = f
            st, sols, _ = solve_dfs(n, q, forb, node_budget=10 ** 8)
            if st == "UNSAT":
                bad += 1
            else:
                check_completion(n, q, forb, sols[0])
            cnt += 1
        assert cnt == want, (cnt, want)
        assert bad == unsat, (bad, unsat)
        print("      Pi(%d,%d): %d representatives, %d with no completion "
              "(matches exh.c exactly)" % (n, r, cnt, bad))
    ok("the independent python implementation of the Lemma-G scheme reproduces "
       "the C enumerator's counts and verdicts on two complete parameter pairs")


def s10_twin5_slice():
    section("10. twin5 exhaustive family: deterministic re-check of a slice")
    path = os.path.join(HERE, "twin5_slice.json")
    if not os.path.exists(path):
        print("      (twin5_slice.json absent; skipping)")
        return
    d = json.loads(open(path).read())
    cnt = 0
    for cols in d["slice"]:
        forb = [0] * 13
        for i in range(8):
            f = 0
            for j, m in enumerate(cols):
                if (m >> i) & 1:
                    f |= 1 << j
            forb[i] = f
        for i in range(8, 13):
            forb[i] = 0x1F000
        check_class_B(13, 17, forb)
        st, sols, _ = solve_dfs(13, 17, forb, node_budget=10 ** 8)
        assert st == "SAT", st
        check_completion(13, 17, forb, sols[0])
        cnt += 1
    ok("%d stored twin5 instances re-decided in Python and every completion "
       "re-checked from the definition" % cnt)


def s11_parity():
    section("11. Lemma BP (the parity refinement) and the (9,4) counterexample")
    # --- Lemma BP arithmetic: at most r colours can be forbidden by all of a
    #     non-empty set, so at most 3r colours can be parity-constrained.
    for r in range(2, 9):
        for n in range(r + 2, 3 * r + 6):
            q = n + r - 1
            can_fire = (q <= 3 * r)
            assert can_fire == (n <= 2 * r + 1)
    ok("q <= 3r is equivalent to n <= 2r+1, so for n >= 2r+2 fewer than q "
       "colours can be parity-constrained (Lemma BP)")
    # --- exhaustive control at n = 13: every disjoint pair X, W with a
    #     non-empty rest has a colour of unconstrained parity.
    rng = random.Random(555)
    checked = 0
    for _ in range(6):
        forb = random_class_B(13, 17, rng)
        for _ in range(300):
            nf = random_move(13, 17, forb, rng)
            if nf:
                forb = nf
        check_class_B(13, 17, forb)
        V = [set(a for a in range(13) if not ((forb[a] >> c) & 1)) for c in range(17)]
        for xm in range(1, 1 << 13):
            rest = ((1 << 13) - 1) & ~xm
            sub = rest
            while sub:
                wm = sub
                sub = (sub - 1) & rest
                if (xm | wm) == (1 << 13) - 1:
                    continue                       # Z empty: parity automatic
                X = set(i for i in range(13) if (xm >> i) & 1)
                W = set(i for i in range(13) if (wm >> i) & 1)
                free = False
                for c in range(17):
                    sX = len(V[c] & X)
                    sW = len(V[c] & W)
                    z = len(V[c]) - sX - sW
                    if z >= 1 and min(sX, sW) >= 1:
                        free = True
                        break
                assert free, "Lemma BP fails"
                checked += 1
    ok("%d (X,W) pairs on 6 random n=13 instances: every one has a colour of "
       "unconstrained parity, so the parity refinement never applies" % checked)
    # --- the (9,4) certificate
    d = json.loads(open(os.path.join(CERTS, "n09r04_parity.json")).read())
    n, q, r, forb = d["n"], d["q"], d["r"], d["forb"]
    for a in range(n):
        assert bin(forb[a]).count("1") == r
    for c in range(q):
        m = sum((forb[a] >> c) & 1 for a in range(n))
        assert m <= r and (n - m) % 2 == 0
    X, W = set(d["X"]), set(d["W"])
    V = [set(a for a in range(n) if not ((forb[a] >> c) & 1)) for c in range(q)]
    par = 0
    for c in range(q):
        sX, sW = len(V[c] & X), len(V[c] & W)
        z = len(V[c]) - sX - sW
        assert not (z >= 1 and min(sX, sW) >= 1), "a colour has free parity"
        if z == 0:
            par += sX
    assert (par - len(X) * len(W)) % 2 == 1, "no parity violation"
    st, _, nodes = solve_dfs(n, q, forb, node_budget=10 ** 9)
    assert st == "UNSAT", st
    if HAVE_SAT:
        assert solve_sat(n, q, forb)[0] == "UNSAT"
    x = [Fraction(a, b) for a, b in d["lp_point"]]
    assert check_lp_point(n, q, forb, x), "stored LP point not feasible"
    print("      Pi(9,4): |X||W| = %d is odd while every colour forces an even "
          "contribution (total parity %d)" % (len(X) * len(W), par % 2))
    print("      exhaustive UNSAT in %d nodes; CDCL agrees; and the fractional "
          "relaxation is feasible with an exact rational point" % nodes)
    ok("a class-B-type instance with NO completion whose obstruction is pure "
       "parity and is invisible to the tested fractional relaxation")
    # --- the infinite family
    for s in (3, 7, 11):
        r = (3 * s - 1) // 2
        n = 3 * s
        q = n + r - 1
        assert 3 * r == q
        forb = [0] * n
        for (i, j), lo in (((0, 1), 0), ((0, 2), r), ((1, 2), 2 * r)):
            k = 3 - i - j
            for a in range(k * s, (k + 1) * s):
                for c in range(lo, lo + r):
                    forb[a] |= 1 << c
        for a in range(n):
            assert bin(forb[a]).count("1") == r
        Vv = [set(a for a in range(n) if not ((forb[a] >> c) & 1)) for c in range(q)]
        for c in range(q):
            assert n - len(Vv[c]) <= r and len(Vv[c]) % 2 == 0
        X = set(range(s))
        W = set(range(s, 2 * s))
        par = 0
        for c in range(q):
            sX, sW = len(Vv[c] & X), len(Vv[c] & W)
            z = len(Vv[c]) - sX - sW
            assert not (z >= 1 and min(sX, sW) >= 1)
            if z == 0:
                par += sX
        assert (par - s * s) % 2 == 1
        print("      s=%2d: Pi(%d,%d), q=%d, mu = n-r = %d, parity violated"
              % (s, n, r, q, n - r))
    ok("the family Pi(3s, (3s-1)/2) with s = 3 (mod 4) has no completion for "
       "every such s, and its minimum support n-r = (3s+1)/2 is unbounded: "
       "the minimum support size does NOT govern the phenomenon")


def s12_partition():
    section("12. the amalgamation condition (PART)")
    from conditions import partition_feasible, random_partitions
    d = json.loads(open(os.path.join(CERTS, "n09r04_parity.json")).read())
    assert not partition_feasible(d["n"], d["q"], d["forb"],
                                  [d["X"], d["W"], d["Z"]])
    ok("(PART) with the three groups already refutes the Pi(9,4) instance")
    rng = random.Random(97)
    tested = 0
    for _ in range(4):
        forb = random_class_B(13, 17, rng)
        for _ in range(300):
            nf = random_move(13, 17, forb, rng)
            if nf:
                forb = nf
        check_class_B(13, 17, forb)
        st, sols, _ = solve_dfs(13, 17, forb, node_budget=10 ** 8)
        assert st == "SAT"
        check_completion(13, 17, forb, sols[0])
        for P in random_partitions(13, 3, rng, 4):
            assert partition_feasible(13, 17, forb, P)
            tested += 1
    ok("%d (instance, 3-partition) pairs at n = 13: (PART) is satisfied by "
       "every completable instance, as it must be" % tested)
    # Theorem BP3: the mod-2 layer of (PART) at k = 3 never fires
    chk = 0
    for _ in range(4):
        forb = random_class_B(13, 17, rng)
        for _ in range(300):
            nf = random_move(13, 17, forb, rng)
            if nf:
                forb = nf
        check_class_B(13, 17, forb)
        V = [set(a for a in range(13) if not ((forb[a] >> c) & 1)) for c in range(17)]
        for P in random_partitions(13, 3, rng, 40):
            p = [len(x) for x in P]
            assert (p[0] * p[1]) % 2 == (p[0] * p[2]) % 2 == (p[1] * p[2]) % 2
            free = 0
            for c in range(17):
                if all(len(V[c] & set(P[i])) > 0 for i in range(3)):
                    free += 1
            assert free >= 1, "no colour with a free parity class"
            chk += 1
    ok("%d 3-partitions at n = 13: the three targets always agree mod 2 and at "
       "least one colour has a free parity class, so the mod-2 layer of (PART) "
       "never fires (Theorem BP3)" % chk)

    # (PART) is not sufficient: an exhaustive scan over ALL partitions into
    # 2 and 3 parts of the n = 7 instance whose obstruction is purely integral
    def all_partitions(n, k):
        def rec(i, parts):
            if i == n:
                if len(parts) == k:
                    yield [list(p) for p in parts]
                return
            for j in range(len(parts)):
                parts[j].append(i)
                yield from rec(i + 1, parts)
                parts[j].pop()
            if len(parts) < k:
                parts.append([i])
                yield from rec(i + 1, parts)
                parts.pop()
        yield from rec(0, [])

    d = json.loads(open(os.path.join(CERTS, "n07_BCclean_LPfeasible.json")).read())
    n, q, forb = d["n"], d["q"], d["forb"]
    tot = 0
    for k in (2, 3, 4):
        for P in all_partitions(n, k):
            assert partition_feasible(n, q, forb, P), "unexpected (PART) violation"
            tot += 1
    d2 = json.loads(open(os.path.join(CERTS, "n07_BCclean_LPinfeasible.json")).read())
    hits = sum(0 if partition_feasible(d2["n"], d2["q"], d2["forb"], P) else 1
               for P in all_partitions(d2["n"], 3))
    assert hits > 0
    ok("(PART) is NOT sufficient: all %d partitions into 2,3,4 parts of the "
       "purely-integral n=7 certificate are satisfiable, yet it has no "
       "completion; the LP-infeasible n=7 certificate does violate (PART) at "
       "k=3 (%d partitions)" % (tot, hits))


def main():
    print("Verifier for collaboration/opus5/first_lift_classB_attack/NOTE.md")
    print("=" * 52)
    print("python-sat available: %s" % HAVE_SAT)
    s1_arithmetic()
    s2_bc_specialisations()
    s3_bc_necessity()
    s4_bc_theorem()
    s5_hall_lemma()
    s6_old_certificates()
    s7_new_certificates()
    s8_solver_crosscheck()
    s9_generator_completeness()
    s9b_generator_vs_C()
    s10_twin5_slice()
    s11_parity()
    s12_partition()
    section("scope")
    print("Proved here: (BC) and (BP) are necessary; (BC) contains both Lemma-1")
    print("cuts and vertex Hall; (BC) can fire exactly for k in {8,10,12,14} and")
    print("never at k = 16; vertex Hall never fires for n >= 2r+1; (BP) never")
    print("fires for n >= 2r+2, in particular never at (13,5); an infinite")
    print("family of instances with unbounded minimum support has no completion;")
    print("(BC), (BP), (PART) and the fractional relaxation are each NOT")
    print("sufficient.  NOT proved here: that every class-B or class-B' instance")
    print("completes at n = 13, that a simultaneous fan or an LS(3,4,20) exists,")
    print("or anything about Erdos-Rosenfeld Problem #835, which remains open.")


if __name__ == "__main__":
    main()
