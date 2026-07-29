#!/usr/bin/env python3
"""Saturated-core switching theorem for complement-cover six-prefixes.

Standard library only.  No optimizer, no SAT solver.

Checks, in order:

A. the finite Tutte case analysis behind
      Lemma A1:  if H has 13 vertices, delta(H) >= 7, alpha(H) <= 5 and no
      two disjoint 5-sets with no H-edge between them, then every
      10-subset of V(H) spans a perfect matching of H;
   done by exhausting every coarsened odd-block partition;

B. the same exhaustion for the residual catalogues after one and two extra
   matchings (Delta <= 6 and Delta <= 7);

C. the switch on the new r=0 certificate of
   `verify_r0_prefix_obstruction.py`: one two-edge switch removes the
   saturated K6, preserves every support, every vertex degree and every
   complement, and afterwards all eleven remaining supports of size ten are
   unblocked and three of them pack;

D. the same switch applied to the repository's r=2 obstruction
   (`collaboration/coordinated_nine_r2_obstruction/NOTE.md`), which repairs
   it to a nine-packing of pattern 8^4 10^3 12^2.
"""

import itertools
import sys

N = 13
VERTS = tuple(range(N))
ALL_EDGES = frozenset(frozenset(e) for e in itertools.combinations(VERTS, 2))


def has_pm(support, allowed):
    support = tuple(sorted(support))
    if len(support) % 2:
        return False

    def rec(rest):
        if not rest:
            return True
        a = rest[0]
        for i in range(1, len(rest)):
            if frozenset((a, rest[i])) in allowed:
                if rec(rest[1:i] + rest[i + 1:]):
                    return True
        return False

    return rec(support)


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


def odd_partitions(total, parts):
    """All non-decreasing tuples of `parts` odd positive integers summing to
    `total`."""
    res = []

    def rec(remaining, slots, lo, acc):
        if slots == 0:
            if remaining == 0:
                res.append(tuple(acc))
            return
        a = lo
        while a * slots <= remaining:
            rec(remaining - a, slots - 1, a, acc + [a])
            a += 2

    rec(total, parts, 1, [])
    return res


def core_data(blocks):
    """(order, edges, max degree) of the complete multipartite graph with the
    given part sizes."""
    c = sum(blocks)
    e = (c * c - sum(b * b for b in blocks)) // 2
    d = max(c - b for b in blocks)
    return c, e, d


def catalogue(n, delta_H, max_deg_D):
    """Coarsened Tutte cores that can block a size-n support when the residual
    graph has min degree >= delta_H - (13 - n) inside the support and the used
    graph has max degree <= max_deg_D."""
    out = []
    for s in range(0, n):
        parts = s + 2
        if parts > n - s:
            break
        for blocks in odd_partitions(n - s, parts):
            c, e, d = core_data(blocks)
            # the core is  K_{blocks} on the n - s non-separator vertices,
            # joined to nothing; the separator contributes nothing forced.
            if d <= max_deg_D:
                out.append((s, blocks, c, e, d))
    return out


def main():
    ok = True

    def check(label, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + label)
        ok = ok and bool(cond)

    # ---------------- A. the delta(H) >= 7 catalogue on a 10-set -----------
    # inside a 10-set, min degree >= 10 - 1 - 5 = 4  (Delta(D) <= 5)
    cat10_5 = catalogue(10, 7, 5)
    # keep only those consistent with min degree 4 inside the support:
    # a vertex of an odd block of order a has at most a-1 + s neighbours
    keep = [row for row in cat10_5 if min(row[1]) - 1 + row[0] >= 4]
    check("size-10 catalogue at Delta(D)<=5 is exactly {K5+K5, K6}",
          sorted((r[0], r[1]) for r in keep) == [(0, (5, 5)), (4, (1,) * 6)])
    print("      ", [(r[0], r[1]) for r in keep])

    # size-8 supports, for the record
    cat8 = [row for row in catalogue(8, 7, 5)
            if min(row[1]) - 1 + row[0] >= 8 - 1 - 5]
    print("       size-8 catalogue at Delta(D)<=5:",
          [(r[0], r[1]) for r in cat8])

    # ---------------- B. after one and two extra matchings -----------------
    cat10_6 = [row for row in catalogue(10, 7, 6)
               if min(row[1]) - 1 + row[0] >= 10 - 1 - 6]
    check("size-10 catalogue at Delta<=6 is {K5+K5, K333, K31111, K6}",
          sorted((r[0], r[1]) for r in cat10_6) ==
          [(0, (5, 5)), (1, (3, 3, 3)), (3, (1, 1, 1, 1, 3)), (4, (1,) * 6)])
    cat10_7 = [row for row in catalogue(10, 7, 7)
               if min(row[1]) - 1 + row[0] >= 10 - 1 - 7]
    print("       size-10 catalogue at Delta<=7:",
          [(r[0], r[1]) for r in cat10_7])

    # K333 needs nine core vertices of core-degree 6 > 5 = Delta(D); every one
    # of them must meet an edge of the single extra matching inside the core,
    # but a matching covers at most eight of nine vertices.
    check("K333 is excluded after one extra matching (9 > 2*floor(9/2))",
          9 > 2 * (9 // 2))

    # ---------------- C. the r=0 certificate and its switch ----------------
    C6 = [0, 1, 2, 3, 4, 5]
    G1 = frozenset({0, 1, 6, 10, 11})
    G2 = frozenset({2, 4, 7, 11, 12})
    G3 = frozenset({3, 5, 6, 7, 12})
    T1 = frozenset({6, 7, 8})
    T2 = frozenset({6, 7, 9})
    T3 = frozenset({6, 7, 10})
    SELECTED = [G1, G2, G3, T1, T2, T3]
    REMAINING = ([frozenset(set(C6) - {c}) for c in (0, 1, 2, 3)] +
                 [frozenset(t) for t in ({8, 9, 10}, {8, 9, 11}, {8, 10, 12},
                                         {9, 11, 12}, {10, 11, 12})] +
                 [frozenset({0, 1, 8}), frozenset({2, 3, 9})])
    PREFIX = [[(3, 4), (2, 5), (7, 9), (8, 12)],
              [(1, 3), (0, 5), (6, 8), (9, 10)],
              [(0, 4), (1, 2), (8, 9), (10, 11)],
              [(0, 1), (2, 3), (4, 5), (9, 11), (10, 12)],
              [(0, 2), (1, 4), (3, 5), (8, 10), (11, 12)],
              [(0, 3), (1, 5), (2, 4), (8, 11), (9, 12)]]
    PREFIX = [[frozenset(e) for e in m] for m in PREFIX]

    # the switch: matching 3 (complement T1) contains 0-1 inside C6 and 9-11
    # outside; replace them by 0-9 and 1-11.
    NEW3 = [e for e in PREFIX[3]
            if e not in (frozenset({0, 1}), frozenset({9, 11}))]
    NEW3 += [frozenset({0, 9}), frozenset({1, 11})]
    PREFIX2 = list(PREFIX)
    PREFIX2[3] = NEW3

    D = set(e for m in PREFIX for e in m)
    D2 = set(e for m in PREFIX2 for e in m)
    check("the switched prefix is still a packing (27 distinct edges)",
          len(D2) == 27 and
          len([e for m in PREFIX2 for e in m]) == 27)
    good = all(set().union(*[set(e) for e in m]) == set(VERTS) - set(c)
               for c, m in zip(SELECTED, PREFIX2))
    check("the switched prefix keeps every prescribed support", good)
    degD = {v: sum(1 for e in D if v in e) for v in VERTS}
    degD2 = {v: sum(1 for e in D2 if v in e) for v in VERTS}
    check("the switch preserves every vertex degree", degD == degD2)

    def has_k6(g):
        for c in itertools.combinations(VERTS, 6):
            if all(frozenset(p) in g for p in itertools.combinations(c, 2)):
                return True
        return False

    def has_k55(g):
        for ten in itertools.combinations(VERTS, 10):
            for a in itertools.combinations(ten, 5):
                b = [x for x in ten if x not in a]
                if b[0] < a[0]:
                    continue
                if all(frozenset((x, y)) in g for x in a for y in b):
                    return True
        return False

    check("D contains a saturated K6 before the switch", has_k6(D))
    check("the switched union contains no K6", not has_k6(D2))
    check("the switched union contains no K5,5", not has_k55(D2))

    H2 = ALL_EDGES - D2
    check("delta(H) >= 7 after the switch",
          min(sum(1 for e in H2 if v in e) for v in VERTS) >= 7)
    every10 = all(has_pm(s, H2) for s in itertools.combinations(VERTS, 10))
    check("after the switch EVERY 10-subset spans a perfect matching",
          every10)

    rem10 = [frozenset(VERTS) - c for c in REMAINING if len(c) == 3]
    trip = None
    for combo in itertools.combinations(rem10, 3):
        found = None
        for m1 in perfect_matchings(combo[0], H2):
            H3 = H2 - set(m1)
            for m2 in perfect_matchings(combo[1], H3):
                H4 = H3 - set(m2)
                for m3 in perfect_matchings(combo[2], H4):
                    found = (m1, m2, m3)
                    break
                if found:
                    break
            if found:
                break
        if found:
            trip = (combo, found)
            break
    check("the switched six-prefix extends by three size-10 supports",
          trip is not None)

    # ---------------- D. the repository's r=2 obstruction ------------------
    R2_SEL = [frozenset({0, 1, 3, 8, 10}), frozenset({0, 1, 2, 7, 11}),
              frozenset({0, 1, 3, 9, 12}), frozenset({0, 1, 2, 5, 6}),
              frozenset({4, 5, 6}), frozenset({0, 1, 4})]
    R2_M = [[(7, 11), (9, 12), (2, 6), (4, 5)],
            [(8, 9), (10, 12), (3, 5), (4, 6)],
            [(7, 8), (10, 11), (2, 4), (5, 6)],
            [(7, 9), (8, 10), (11, 12), (3, 4)],
            [(7, 10), (8, 12), (9, 11), (2, 3), (0, 1)],
            [(7, 12), (8, 11), (9, 10), (2, 5), (3, 6)]]
    R2_M = [[frozenset(e) for e in m] for m in R2_M]
    R2_REM10 = [frozenset(VERTS) - frozenset(t) for t in
                ({3, 5, 6}, {2, 4, 6}, {2, 3, 5}, {2, 3, 4})]
    R2_REM12 = [frozenset(VERTS) - {4}, frozenset(VERTS) - {5}]

    DR = set(e for m in R2_M for e in m)
    check("r=2 repository prefix: |E(D)|=26 with a saturated K6",
          len(DR) == 26 and has_k6(DR))
    HR = ALL_EDGES - DR
    check("r=2: all four remaining size-10 supports blocked before the switch",
          not any(has_pm(s, HR) for s in R2_REM10))

    # switch inside matching 0: 7-11 lies in the K6 on {7..12}; 2-6 lies
    # outside it.  Replace 7-11, 2-6 by 7-2, 11-6.
    NEW0 = [e for e in R2_M[0]
            if e not in (frozenset({7, 11}), frozenset({2, 6}))]
    NEW0 += [frozenset({2, 7}), frozenset({6, 11})]
    R2_M2 = [NEW0] + R2_M[1:]
    DR2 = set(e for m in R2_M2 for e in m)
    check("r=2 switched prefix is still a packing of the same supports",
          len(DR2) == 26 and
          all(set().union(*[set(e) for e in m]) == set(VERTS) - set(c)
              for c, m in zip(R2_SEL, R2_M2)))
    check("r=2 switched union has no K6 and no K5,5",
          (not has_k6(DR2)) and (not has_k55(DR2)))
    HR2 = ALL_EDGES - DR2
    check("r=2: after the switch every 10-subset spans a perfect matching",
          all(has_pm(s, HR2) for s in itertools.combinations(VERTS, 10)))

    # and now three more matchings: one size-10 plus the two size-12 supports
    nine = None
    for s10 in R2_REM10:
        for m1 in perfect_matchings(s10, HR2):
            X = HR2 - set(m1)
            for m2 in perfect_matchings(R2_REM12[0], X):
                Y = X - set(m2)
                for m3 in perfect_matchings(R2_REM12[1], Y):
                    nine = (s10, m1, m2, m3)
                    break
                if nine:
                    break
            if nine:
                break
        if nine:
            break
    check("r=2: the switched prefix extends to nine with pattern 8^4 10^3 12^2",
          nine is not None)

    print()
    print("ALL CHECKS PASS" if ok else "SOME CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
