#!/usr/bin/env python3
"""Decisive falsification test for the Disjointness-Parity conjecture
(IDEAS.md section A).

NOT RUN when written (code execution was unavailable in that session).

For each of
    S(2,3,7)   (Fano planes,      n=7,  30 systems expected)
    S(3,4,8)   (AG(3,2) planes,   n=8,  30 systems expected)
    S(4,5,11)  (M_11 pentads,     n=11, 5040 systems expected)
it:
  1. generates ALL labelled systems, as the S_n-orbit of one seed, by BFS
     under the adjacent transpositions (i, i+1), carrying a parity tag;
  2. reports whether any system is reachable with BOTH parities.  That would
     mean Aut(D) is not contained in A_n and would immediately kill the
     conjecture's mechanism for that case;
  3. counts block-disjoint pairs, split by same / different A_n-orbit.
     *** ONE same-orbit disjoint pair refutes the conjecture. ***
  4. reports whether the disjointness graph contains a triangle, i.e. whether
     three pairwise disjoint systems exist.  For the conjecture to be useful
     the answer must be NO for n = 7, 8, 11.

Stdlib only.  Exits nonzero if any structural self-check fails; the
conjecture verdict is printed, not asserted.
"""
from itertools import combinations
from math import comb, factorial

EXPECTED = {"S(2,3,7)": 30, "S(3,4,8)": 30, "S(4,5,11)": 5040}


# ---------------------------------------------------------------- seeds

def seed_fano():
    lines = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
             (1, 4, 6), (2, 3, 6), (2, 4, 5)]
    return 7, 2, 3, frozenset(frozenset(l) for l in lines)


def seed_sqs8():
    blocks = [b for b in combinations(range(8), 4)
              if b[0] ^ b[1] ^ b[2] ^ b[3] == 0]
    return 8, 3, 4, frozenset(frozenset(b) for b in blocks)


def seed_s4511():
    """Derived design of S(5,6,12) at the point 'infinity'.

    S(5,6,12) is built as the PSL(2,11)-orbit of {inf} u QR(11) on the
    projective line {0..10, inf}; deleting inf from the blocks through it
    leaves an S(4,5,11) on {0..10}.
    """
    INF = 11

    def shift(x):
        return INF if x == INF else (x + 1) % 11

    def inv(x):
        if x == INF:
            return 0
        if x == 0:
            return INF
        return (-pow(x, 9, 11)) % 11

    base = frozenset({INF, 1, 3, 4, 5, 9})
    seen, frontier = {base}, [base]
    while frontier:
        nxt = []
        for blk in frontier:
            for g in (shift, inv):
                img = frozenset(g(x) for x in blk)
                if img not in seen:
                    seen.add(img)
                    nxt.append(img)
        frontier = nxt
    assert len(seen) == 132, f"S(5,6,12) build gave {len(seen)} blocks"
    derived = frozenset(frozenset(b - {INF}) for b in seen if INF in b)
    return 11, 4, 5, derived


# ---------------------------------------------------------------- checks

def is_steiner(blocks, t, ksize, v):
    if any(len(b) != ksize for b in blocks):
        return False
    count = {}
    for b in blocks:
        for s in combinations(sorted(b), t):
            count[s] = count.get(s, 0) + 1
    return len(count) == comb(v, t) and set(count.values()) == {1}


def apply_perm(system, perm):
    return frozenset(frozenset(perm[x] for x in b) for b in system)


def orbit_with_parity(seed, n):
    """BFS over the S_n-orbit under adjacent transpositions.

    Returns (parity dict, aut_has_odd_element flag).
    """
    transps = []
    for i in range(n - 1):
        p = list(range(n))
        p[i], p[i + 1] = p[i + 1], p[i]
        transps.append(p)

    parity = {seed: 0}
    frontier = [seed]
    conflict = False
    while frontier:
        nxt = []
        for s in frontier:
            ps = parity[s]
            for p in transps:
                img = apply_perm(s, p)
                q = ps ^ 1
                if img not in parity:
                    parity[img] = q
                    nxt.append(img)
                elif parity[img] != q:
                    conflict = True
        frontier = nxt
    return parity, conflict


def run(name, seed_fn):
    n, t, ksize, seed = seed_fn()
    print(f"\n=== {name} ===")
    assert is_steiner(seed, t, ksize, n), f"{name}: seed is not a Steiner system"
    print(f"  seed valid S({t},{ksize},{n}) with {len(seed)} blocks: PASS")

    parity, conflict = orbit_with_parity(seed, n)
    total = len(parity)
    exp = EXPECTED[name]
    print(f"  labelled systems: {total} (expected {exp}) -> "
          f"{'PASS' if total == exp else 'FAIL'}")
    print(f"  |Aut| = {factorial(n)}/{total} = "
          f"{factorial(n) // total if total else 'n/a'}")

    if conflict:
        print("  AUT NOT IN A_n: some system is reachable with both parities.")
        print("  -> the sign-equivariant invariant CANNOT exist here; "
              "conjecture mechanism dead for this case.")
        return total == exp

    orb = [[], []]
    for s, q in parity.items():
        orb[q].append(s)
    print(f"  A_n-orbit sizes: ({len(orb[0])}, {len(orb[1])})")

    # bitmask encoding for fast disjointness
    allblocks = sorted(combinations(range(n), ksize))
    idx = {frozenset(b): i for i, b in enumerate(allblocks)}
    systems = list(parity.keys())
    tag = [parity[s] for s in systems]
    mask = []
    for s in systems:
        m = 0
        for b in s:
            m |= 1 << idx[b]
        mask.append(m)

    m_count = len(systems)
    nbrs = [set() for _ in range(m_count)]
    edges = []
    same = diff = 0
    for i in range(m_count):
        mi = mask[i]
        for j in range(i + 1, m_count):
            if mi & mask[j] == 0:
                nbrs[i].add(j)
                nbrs[j].add(i)
                edges.append((i, j))
                if tag[i] == tag[j]:
                    same += 1
                else:
                    diff += 1
    print(f"  block-disjoint pairs: {same + diff}  "
          f"(same A_n-orbit: {same}, different: {diff})")
    print("  CONJECTURE VERDICT: "
          + ("REFUTED for this case (a same-orbit disjoint pair exists)"
             if same else "consistent (every disjoint pair crosses orbits)"))

    triangle = None
    for i, j in edges:
        common = nbrs[i] & nbrs[j]
        if common:
            triangle = (i, j, min(common))
            break
    print(f"  three pairwise disjoint systems exist: "
          f"{'YES ' + str(triangle) if triangle else 'NO'}")
    return total == exp


def main():
    ok = True
    ok &= run("S(2,3,7)", seed_fano)
    ok &= run("S(3,4,8)", seed_sqs8)
    ok &= run("S(4,5,11)", seed_s4511)
    print("\nSTRUCTURAL SELF-CHECKS:", "PASS" if ok else "FAIL")
    print("The conjecture verdicts above are reported, not asserted.")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
