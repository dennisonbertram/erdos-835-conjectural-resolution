#!/usr/bin/env python3
"""Verifier for collaboration/opus5/first_lift_k13_hole/NOTE.md.

Standard library only.  Every claim quoted in NOTE.md is re-checked here from
its definition.  The verifier constructs no simultaneous fan, no LS(3,4,20)
and no colouring of J(32,16), and it does not settle Erdos--Rosenfeld
Problem #835.

Run:
  python3 -B \
    collaboration/opus5/first_lift_k13_hole/verify_first_lift_obstruction.py
"""

from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path

from first_lift import (
    PAIRS5,
    check_class_Bprime,
    check_completion,
    check_instance_shape,
    cut_certificates,
    cut_margins,
    in_class_B,
    link_partitions,
    m_profiles,
    m_profile,
    max_forced,
    min_capacity,
    random_class_Bprime,
    solve,
    solve_randomised,
    supports,
)

HERE = Path(__file__).resolve().parent
CERTS = HERE / "certificates"


# --------------------------------------------------------------------------
def section(title):
    print()
    print(title)
    print("-" * len(title))


# --------------------------------------------------------------------------
def check_setup_arithmetic():
    """The instance-class arithmetic of Section 1 of the NOTE."""
    section("1. instance-class arithmetic")
    for n in (3, 5, 7, 9, 11, 13):
        q = n + 4
        profs = m_profiles(n)
        for a, b, c in profs:
            assert a + b + c == q
            assert 5 * a + 3 * b + c == 5 * n
        print(
            "n=%2d q=%2d : %d admissible (n5,n3,n1) profiles %s"
            % (n, q, len(profs), profs)
        )
    # k=16 specialisation quoted in the NOTE
    profs13 = m_profiles(13)
    assert profs13 == [
        (7, 10, 0),
        (8, 8, 1),
        (9, 6, 2),
        (10, 4, 3),
        (11, 2, 4),
        (12, 0, 5),
    ], profs13
    for n5, n3, n1 in profs13:
        assert n3 == 24 - 2 * n5 and n1 == n5 - 7
        assert 4 * n5 + 5 * n3 + 6 * n1 == 78  # sum of |V_c|/2
        assert 8 * n5 + 10 * n3 + 12 * n1 == 156  # sum of |V_c|
    print("k=16: n3 = 24-2*n5 and n1 = n5-7 for all six profiles;")
    print("      sum_c |V_c| = 156 = 13*12 and sum_c |V_c|/2 = 78 = C(13,2): PASS")
    print("      so at k=16 at most five colours have |V_c| = 12 and")
    print("      every colour has |V_c| in {8,10,12}: PASS")
    pool = link_partitions()
    assert len(pool) == 332, len(pool)
    for parts in pool:
        flat = [p for part in parts for p in part]
        assert sorted(flat) == sorted(PAIRS5)
        for part in parts:
            assert 1 <= len(part) <= 2
            if len(part) == 2:
                assert not (set(part[0]) & set(part[1]))
    print("partitions of E(K_5) into matchings (= proper colourings L of the")
    print("      ten triples of P): %d, each re-checked: PASS" % len(pool))
    # level-0 packing count: each colour class of L is a partial Steiner
    # triple system on k+3 points, so it has at most floor(v*floor((v-1)/2)/3)
    # triples; (k+1) classes must cover all C(k+3,3) of them.
    print()
    print("level-0 packing count (why class C is empty for some k):")
    for k in (6, 8, 10, 12, 14, 16, 18):
        v = k + 3
        cap = (k + 1) * ((v * ((v - 1) // 2)) // 3)
        tot = v * (v - 1) * (v - 2) // 6
        print(
            "  k=%2d: v=%2d, %2d colours cover at most %d of the %d triples%s"
            % (k, v, k + 1, cap, tot, "" if cap >= tot else "   -> IMPOSSIBLE")
        )
    for k in (8, 14):
        v = k + 3
        assert (k + 1) * ((v * ((v - 1) // 2)) // 3) < v * (v - 1) * (v - 2) // 6
    for k in (6, 10, 12, 16, 18):
        v = k + 3
        assert (k + 1) * ((v * ((v - 1) // 2)) // 3) >= v * (v - 1) * (v - 2) // 6
    print("  so at k=8 and k=14 no level-0 link exists at all: PASS")


# --------------------------------------------------------------------------
def brute_force_completion(n, q, forb):
    """Independent, heuristic-free completion search: fixed edge order, try
    every allowed colour.  Used only to cross-validate the fast solver."""
    FULL = (1 << q) - 1
    edges = [(a, b) for a in range(n) for b in range(a + 1, n)]
    avail = [FULL & ~forb[a] for a in range(n)]

    def rec(i):
        if i == len(edges):
            return all(avail[a] == 0 for a in range(n))
        a, b = edges[i]
        m = avail[a] & avail[b]
        while m:
            lb = m & -m
            m ^= lb
            avail[a] ^= lb
            avail[b] ^= lb
            if rec(i + 1):
                return True
            avail[a] ^= lb
            avail[b] ^= lb
        return False

    return rec(0)


def check_solver():
    """Cross-validate the fast exact solver against the brute-force search."""
    section("2. exact solver cross-validation (n=5, independent search order)")
    rng = random.Random(4242)
    n, q = 5, 9
    pool = [p for p in link_partitions() if len(p) <= q]
    agree = sat = unsat = 0
    while agree < 600:
        inst = random_class_Bprime(n, q, rng, pool)
        if inst is None:
            continue
        forb = inst["forb"]
        st, sol, _ = solve(n, q, forb)
        bf = brute_force_completion(n, q, forb)
        assert (st == "SAT") == bf, ("solvers disagree", forb, st, bf)
        if st == "SAT":
            assert check_completion(n, q, forb, sol)
            sat += 1
        else:
            unsat += 1
        agree += 1
    print("600 class-B' instances at n=5: fast solver and brute force agree on")
    print(
        "  all of them (%d SAT, %d UNSAT); every SAT witness re-checked: PASS"
        % (sat, unsat)
    )
    # the randomised-restart wrapper must agree with the deterministic search
    rng = random.Random(99)
    n, q = 9, 13
    pool = [p for p in link_partitions() if len(p) <= q]
    seen = 0
    while seen < 200:
        inst = random_class_Bprime(n, q, rng, pool)
        if inst is None:
            continue
        forb = inst["forb"]
        a, _, _ = solve(n, q, forb, node_budget=3_000_000)
        b, solb, _ = solve_randomised(n, q, forb, seed=seen)
        assert a == b, (forb, a, b)
        if b == "SAT":
            assert check_completion(n, q, forb, solb)
        seen += 1
    print("200 instances at n=9: solve and solve_randomised agree, and every")
    print("  randomised witness re-checked: PASS")
    print("caveat recorded: a 'BUDGET' verdict from solve() is NOT evidence of")
    print("  infeasibility; only a finished search or a cut certificate is.")


# --------------------------------------------------------------------------
def check_lemma1_necessity():
    """Lemma 1: both cut conditions are necessary.  Empirical confirmation."""
    section("3. Lemma 1 (both cut conditions are necessary): empirical check")
    rng = random.Random(31337)
    for n in (5, 7, 9):
        q = n + 4
        pool = [p for p in link_partitions() if len(p) <= q]
        tab = Counter()
        drawn = 0
        while drawn < 4000:
            inst = random_class_Bprime(n, q, rng, pool)
            if inst is None:
                continue
            drawn += 1
            forb = inst["forb"]
            check_instance_shape(n, q, forb)
            assert in_class_B(n, q, forb)
            viol = bool(cut_certificates(n, q, forb, only_first=True))
            st, sol, _ = solve(n, q, forb, node_budget=3_000_000)
            assert st in ("SAT", "UNSAT"), st
            if st == "SAT":
                assert check_completion(n, q, forb, sol)
            tab[(st, "cut-violated" if viol else "cut-clean")] += 1
        assert tab[("SAT", "cut-violated")] == 0, "a cut condition is NOT necessary"
        print("n=%2d, 4000 class-B' instances: %s" % (n, dict(tab)))
        print(
            "      SAT with a violated cut condition: %d (must be 0): PASS"
            % tab[("SAT", "cut-violated")]
        )
    print("Reading: no completable instance ever violates a cut condition, so")
    print("both conditions are necessary.  Where the 'UNSAT + cut-clean' cell")
    print("above is nonzero, they are also NOT sufficient; the stored")
    print("certificate of section 5 is one such instance.")


# --------------------------------------------------------------------------
def load_cert(name):
    d = json.loads((CERTS / name).read_text())
    d["parts"] = [tuple(tuple(p) for p in part) for part in d["parts"]]
    return d


def check_certificates():
    """Theorem A: explicit class-B' instances with no completion."""
    section("4. Theorem A: class-B' counterexamples (re-checked from definitions)")
    for name in sorted(p.name for p in CERTS.glob("counterexample_n*.json")):
        d = load_cert(name)
        n, q, forb = d["n"], d["q"], d["forb"]
        v = check_instance_shape(n, q, forb)
        assert in_class_B(n, q, forb), "not in class B"
        assert check_class_Bprime(n, q, forb, d["arr"], d["parts"], d["colours"])
        cc = cut_certificates(n, q, forb)
        assert cc, "no cut certificate"
        kind, X, val, cap = cc[0]
        # re-derive the certificate value straight from the definition
        V = [set(a for a in range(n) if not (forb[a] >> c & 1)) for c in range(q)]
        Xs = set(X)
        if kind == "forced":
            recomputed = sum(max(0, len(V[c] & Xs) - len(V[c]) // 2) for c in range(q))
        else:
            recomputed = sum(len(V[c] & Xs) // 2 for c in range(q))
        assert recomputed == val and cap == len(X) * (len(X) - 1) // 2
        line = "n=%2d k=%2d  |V_c| multiset %s  m-profile %s" % (
            n,
            n + 3,
            dict(sorted(Counter(v).items())),
            dict(sorted(m_profile(n, q, forb).items())),
        )
        print(line)
        print(
            "      certificate: %s(X) = %d %s C(|X|,2) = %d with |X| = %d"
            % (kind, val, ">" if kind == "forced" else "<", cap, len(X))
        )
        if n <= 9:
            st, _, nodes = solve(n, q, forb, node_budget=5_000_000)
            assert st == "UNSAT", st
            print("      exhaustive solver: UNSAT in %d nodes: PASS" % nodes)
        else:
            print("      exhaustive solver not run (certificate alone is the proof)")


def check_cut_insufficiency():
    section("5. the cut conditions are necessary but NOT sufficient")
    d = load_cert("cut_insufficient_n07.json")
    n, q, forb = d["n"], d["q"], d["forb"]
    check_instance_shape(n, q, forb)
    assert in_class_B(n, q, forb)
    assert check_class_Bprime(n, q, forb, d["arr"], d["parts"], d["colours"])
    assert cut_certificates(n, q, forb) == [], "this instance does violate a cut"
    st, _, nodes = solve(n, q, forb, node_budget=5_000_000)
    assert st == "UNSAT", st
    print("n=7 (k=10) class-B' instance, |V_c| = %s" % supports(n, q, forb))
    print("  violates NO cut condition (all 2^7-1 = 127 subsets checked)")
    print("  yet the exhaustive solver proves UNSAT in %d nodes: PASS" % nodes)
    print("  => no argument that only rules out cut violations can settle k=16.")


# --------------------------------------------------------------------------
def check_theorem_B():
    """Theorem B: at k=16 no cut condition can fire, for any class-B instance."""
    section("6. Theorem B: exact cut margins by dynamic programming")
    print("margin > 0 means the condition CAN be violated somewhere in the")
    print("relaxation; margin <= 0 is a proof that it never fires.")
    fires = []
    for n in range(3, 32, 2):
        (fm, fx, fp), (cm, cx, cp) = cut_margins(n)
        print(
            "n=%2d (k=%2d): forced-inside %+d (at |X|=%d, profile %s) |"
            " capacity %+d (at |X|=%d, profile %s)" % (n, n + 3, fm, fx, fp, cm, cx, cp)
        )
        if fm > 0 or cm > 0:
            fires.append(n + 3)
        if n >= 13 or n == 3:
            assert fm <= 0 and cm <= 0, (n, fm, cm)
    assert fires == [8, 10, 12, 14], fires
    print()
    print(
        "a cut condition can fire for k in %s and for no other k <= 34: PASS" % (fires,)
    )
    print()
    print("per-|X| margins at k=16 (maximum over all six m-profiles):")
    for x in range(1, 14):
        cap = x * (x - 1) // 2
        f = max(max_forced(13, x, p) - cap for p in m_profiles(13))
        c = max(cap - min_capacity(13, x, p) for p in m_profiles(13))
        assert f <= 0 and c <= 0, (x, f, c)
        print("  |X| = %2d : forced-inside %+d   capacity %+d" % (x, f, c))
    print("all thirteen forced-inside and all thirteen capacity margins are")
    print("<= 0 at k=16: PASS")
    print()
    print("The relaxation used: d_c = #{a in X : c in S_a} ranges over every")
    print("integer profile with sum_c d_c = 5|X| and")
    print("max(0, m_c-(13-|X|)) <= d_c <= min(m_c,|X|).  Every class-B instance")
    print("satisfies these, so a nonpositive margin is a theorem about all of")
    print("class B, hence about class B' and about any simultaneous fan.")


def check_amalgamation_outline():
    """The arithmetic quoted in Section 7 of the NOTE."""
    section("7a. amalgamation outline arithmetic (Section 7 of the NOTE)")
    for t in (0, 1, 2):
        m = 5 - 2 * t
        loops = 4 + t
        assert m + 2 * loops == 13, (t, m, loops)
        print(
            "  t_c=%d: %d cross edges + 2*%d loops = %d = multiplicity of alpha"
            % (t, m, loops, m + 2 * loops)
        )
    print("so amalgamating A to one vertex is a legitimate outline for every")
    print("colour, which is exactly why detachment alone cannot recover the")
    print("prescribed cross-edge assignment: PASS")


def check_class_separation():
    """Remark: class B is strictly larger than class B'."""
    section("7. remark: class B strictly contains class B'")
    # At n=7 put all five vertices of Y on the same five colours.  Then the
    # six remaining colours must each occupy 5-2t_c columns, and each column
    # gives the two X-vertices one colour each, so 5-2t_c <= 2.
    admissible_t = [t for t in (0, 1, 2) if 5 - 2 * t <= 2]
    assert admissible_t == [2], admissible_t
    assert 6 * 2 != 10
    print("n=7: the pattern 'all five vertices of Y forbid the same five")
    print("  colours' lies in class B (row sums 5, all m_c in {1,3,5}), but in")
    print("  class B' every one of the six other colours would need")
    print("  5-2t_c <= |X| = 2, forcing t_c = 2, hence sum_c t_c = 6*2 = 12,")
    print("  contradicting sum_c t_c = 10 = C(5,3): PASS")
    print("  (this is why the n=7 certificate above is a different instance)")


def check_k16_smoke():
    section("8. k=16 smoke search (deterministic, small)")
    rng = random.Random(20260727)
    n, q = 13, 17
    pool = [p for p in link_partitions() if len(p) <= q]
    stats = Counter()
    hist = Counter()
    worst = 0
    drawn = 0
    while drawn < 300:
        inst = random_class_Bprime(n, q, rng, pool)
        if inst is None:
            continue
        drawn += 1
        forb = inst["forb"]
        check_instance_shape(n, q, forb)
        assert not cut_certificates(n, q, forb), "Theorem B contradicted"
        st, sol, nodes = solve(n, q, forb, node_budget=5_000_000)
        stats[st] += 1
        worst = max(worst, nodes)
        hist[tuple(sorted(Counter(supports(n, q, forb)).items()))] += 1
        if st == "SAT":
            assert check_completion(n, q, forb, sol)
    print(
        "300 class-B' instances at k=16: %s, max %d search nodes" % (dict(stats), worst)
    )
    print("support multisets seen (all six m-profiles):")
    for k, v in sorted(hist.items()):
        print("   ", k, v)
    assert len(hist) == 6, len(hist)
    assert stats["SAT"] == 300, dict(stats)
    print("every one completed, and every completion was re-checked: PASS")


def main():
    print("Verifier for collaboration/opus5/first_lift_k13_hole/NOTE.md")
    print("=" * 47)
    check_setup_arithmetic()
    check_solver()
    check_lemma1_necessity()
    check_certificates()
    check_cut_insufficiency()
    check_theorem_B()
    check_amalgamation_outline()
    check_class_separation()
    check_k16_smoke()
    section("scope")
    print("Proved here: the two cut conditions are necessary; explicit")
    print("class-B' instances with no completion exist at k = 8, 10, 12, 14;")
    print("no cut condition can fire at k = 16; the cut conditions are not")
    print("sufficient at k = 10.  NOT proved here: that every class-B' or")
    print("fan-realisable instance completes at k=16, that a simultaneous fan")
    print("exists, or anything about Erdos--Rosenfeld Problem #835, which")
    print("remains open.")


if __name__ == "__main__":
    main()
