#!/usr/bin/env python3
"""Search for a counterexample to the three-ten-set packing statement.

Statement under test (T3):

    Let D be the union of six matchings on 13 vertices with Delta(D) <= 5
    and |E(D)| <= 27, containing no K6 and no K_{5,5}.  Put H = K13 - D.
    Then for any three 10-subsets S1, S2, S3 there are pairwise
    edge-disjoint perfect matchings M_i inside H[S_i].

Deterministic pseudo-random driver (fixed seed).  This is search evidence,
not a proof.  Usage:  python3 search_three_ten_sets.py [rounds]
"""

import itertools
import random
import sys

N = 13
VERTS = tuple(range(N))
ALL_EDGES = frozenset(frozenset(e) for e in itertools.combinations(VERTS, 2))
SIXES = list(itertools.combinations(VERTS, 6))
TRIPLES = list(itertools.combinations(VERTS, 3))


def perfect_matchings(support, allowed):
    support = tuple(sorted(support))
    out = []

    def rec(rest, acc):
        if not rest:
            out.append(tuple(acc))
            return
        a = rest[0]
        for i in range(1, len(rest)):
            e = frozenset((a, rest[i]))
            if e in allowed:
                rec(rest[1:i] + rest[i + 1:], acc + [e])

    rec(support, [])
    return out


def has_k6(g):
    for c in SIXES:
        if all(frozenset(p) in g for p in itertools.combinations(c, 2)):
            return True
    return False


def has_k55(g):
    for a in itertools.combinations(VERTS, 5):
        rest = [x for x in VERTS if x not in a]
        for b in itertools.combinations(rest, 5):
            if all(frozenset((x, y)) in g for x in a for y in b):
                return True
    return False


def random_prefix(rng, profile):
    """Six complements covering all vertices, plus an edge-disjoint packing."""
    n5, n3 = profile
    for _ in range(400):
        comps = ([frozenset(rng.sample(VERTS, 5)) for _ in range(n5)] +
                 [frozenset(rng.sample(VERTS, 3)) for _ in range(n3)])
        if set().union(*comps) != set(VERTS):
            continue
        used = set()
        ms = []
        ok = True
        for c in comps:
            sup = sorted(set(VERTS) - c)
            opts = perfect_matchings(sup, ALL_EDGES - used)
            if not opts:
                ok = False
                break
            m = rng.choice(opts)
            ms.append(m)
            used |= set(m)
        if ok:
            return comps, ms, used
    return None


def three_pack(H, s1, s2, s3):
    for m1 in perfect_matchings(s1, H):
        H1 = H - set(m1)
        for m2 in perfect_matchings(s2, H1):
            H2 = H1 - set(m2)
            for m3 in perfect_matchings(s3, H2):
                return (m1, m2, m3)
    return None


def main():
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    rng = random.Random(20260728)
    tested = 0
    prefixes = 0
    fails = []
    # (n5, n3) six-prefix shapes actually used by the repository's covering
    # lemmas: r=0 uses 3+3, r=1 uses 4+2, r=2..5 use 4+2.
    shapes = [(3, 3), (4, 2)]
    for _ in range(rounds):
        shape = rng.choice(shapes)
        got = random_prefix(rng, shape)
        if got is None:
            continue
        comps, ms, D = got
        if max(sum(1 for e in D if v in e) for v in VERTS) > 5:
            continue
        if has_k6(D) or has_k55(D):
            continue
        prefixes += 1
        H = ALL_EDGES - D
        for _ in range(30):
            t1, t2, t3 = (frozenset(rng.choice(TRIPLES)) for _ in range(3))
            s1 = frozenset(VERTS) - t1
            s2 = frozenset(VERTS) - t2
            s3 = frozenset(VERTS) - t3
            tested += 1
            if three_pack(H, s1, s2, s3) is None:
                fails.append((sorted(map(sorted, D)),
                              sorted(t1), sorted(t2), sorted(t3)))
                break
        if fails:
            break
    print("core-free six-prefixes generated :", prefixes)
    print("ordered triples of 10-sets tested:", tested)
    print("counterexamples found            :", len(fails))
    if fails:
        d, a, b, c = fails[0]
        print("  D =", d)
        print("  triples =", a, b, c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
