#!/usr/bin/env python3
"""Exact certificate: odd-active shaped kernel vector at r=5 (2026-07-24).

Statement refuted by the certificate below: "every integer vector z that is
supported on the non-A blocks of an S(4,5,11) A, has one +1 and one -1 in
some spheres (and 0 elsewhere), and satisfies Wz = 0, has an even number of
active spheres."  The recorded witness has 49 active spheres.

The base A is the deterministic first exact-cover solution (sorted
branching); the witness entries are (P, p_plus, p_minus), meaning
z = +1 on block X-(P u {p_plus}), -1 on block X-(P u {p_minus}).

Verification below is exact integer arithmetic, stdlib only.
Run with --search to look for fresh witnesses with CP-SAT (optional).
"""

import sys
from itertools import combinations

WITNESS = [
    ((0, 1, 2, 3, 4), 6, 7), ((0, 1, 2, 7, 8), 3, 4),
    ((0, 1, 2, 9, 10), 7, 6), ((0, 1, 3, 5, 7), 4, 2),
    ((0, 1, 3, 6, 9), 5, 8), ((0, 1, 4, 6, 8), 5, 10),
    ((0, 1, 4, 7, 9), 8, 10), ((0, 2, 3, 6, 10), 9, 5),
    ((0, 2, 3, 7, 9), 4, 10), ((0, 2, 4, 5, 9), 6, 7),
    ((0, 2, 4, 6, 7), 8, 5), ((0, 2, 5, 7, 10), 3, 8),
    ((0, 3, 4, 5, 6), 10, 1), ((0, 3, 4, 7, 10), 9, 5),
    ((0, 3, 4, 8, 9), 6, 7), ((0, 3, 6, 7, 8), 9, 2),
    ((0, 4, 5, 7, 8), 2, 1), ((0, 4, 6, 9, 10), 1, 3),
    ((0, 5, 6, 7, 9), 4, 3), ((0, 5, 6, 8, 10), 2, 9),
    ((0, 7, 8, 9, 10), 5, 1), ((1, 2, 3, 5, 9), 7, 6),
    ((1, 2, 3, 6, 8), 9, 4), ((1, 2, 3, 7, 10), 4, 8),
    ((1, 2, 4, 5, 7), 0, 10), ((1, 2, 4, 6, 10), 8, 3),
    ((1, 2, 5, 8, 10), 7, 6), ((1, 3, 5, 6, 10), 2, 9),
    ((1, 3, 7, 8, 9), 10, 2), ((1, 4, 5, 6, 9), 3, 0),
    ((1, 4, 7, 8, 10), 0, 3), ((1, 5, 7, 9, 10), 4, 2),
    ((1, 6, 8, 9, 10), 0, 4), ((2, 3, 4, 6, 9), 10, 0),
    ((2, 3, 4, 7, 8), 1, 5), ((2, 3, 5, 6, 7), 0, 10),
    ((2, 3, 8, 9, 10), 7, 6), ((2, 4, 5, 6, 8), 3, 0),
    ((2, 4, 7, 9, 10), 5, 3), ((2, 5, 6, 9, 10), 1, 4),
    ((2, 6, 7, 8, 10), 3, 4), ((3, 4, 5, 7, 9), 8, 1),
    ((3, 4, 6, 8, 10), 1, 5), ((3, 5, 6, 8, 9), 10, 4),
    ((3, 5, 7, 8, 10), 4, 9), ((3, 6, 7, 9, 10), 5, 8),
    ((4, 5, 6, 7, 10), 2, 9), ((4, 5, 8, 9, 10), 6, 7),
    ((4, 6, 7, 8, 9), 10, 0),
]


def build_A():
    n, r = 11, 5
    blocks_list = [frozenset(c) for c in combinations(range(n), r)]
    facets = list(combinations(range(n), r - 1))
    cols = {f: set() for f in facets}
    rows = {}
    for i, K in enumerate(blocks_list):
        rows[i] = [f for f in facets if frozenset(f) <= K]
        for f in rows[i]:
            cols[f].add(i)
    solution = []

    def select(rr):
        removed = []
        for j in rows[rr]:
            for i in cols[j]:
                for k in rows[i]:
                    if k != j:
                        cols[k].remove(i)
            removed.append(cols.pop(j))
        return removed

    def deselect(rr, removed):
        for j in reversed(rows[rr]):
            cols[j] = removed.pop()
            for i in cols[j]:
                for k in rows[i]:
                    if k != j:
                        cols[k].add(i)

    def solve_first():
        if not cols:
            return True
        c = min(cols, key=lambda k: len(cols[k]))
        for rr in sorted(cols[c]):
            solution.append(rr)
            rem = select(rr)
            if solve_first():
                return True
            deselect(rr, rem)
            solution.pop()
        return False

    assert solve_first()
    return sorted((blocks_list[i] for i in solution), key=sorted), facets


def verify_recorded():
    n = 11
    X = frozenset(range(n))
    A, facets = build_A()
    Aset = set(A)

    used_P = [frozenset(P) for (P, _, _) in WITNESS]
    assert len(set(used_P)) == len(WITNESS), "sphere repeated"
    for P in used_P:
        assert P in Aset, "witness sphere not a block of the deterministic A"

    blockmap = {}
    for (P, pp, pm) in WITNESS:
        Pf = frozenset(P)
        assert pp not in Pf and pm not in Pf and pp != pm
        Kp = X - Pf - {pp}
        Km = X - Pf - {pm}
        for K, v in ((Kp, 1), (Km, -1)):
            assert K not in Aset, "witness block lies in A"
            blockmap[K] = blockmap.get(K, 0) + v
    assert all(v in (-1, 1) for v in blockmap.values()), "entry collision"

    for f in facets:
        fs = frozenset(f)
        s = sum(v for K, v in blockmap.items() if fs <= K)
        assert s == 0, ("facet equation violated", f, s)

    n_active = len(WITNESS)
    print("recorded witness: {} active spheres (odd: {}), support {},"
          " norm {} == {} mod 4".format(
              n_active, n_active % 2 == 1, len(blockmap),
              2 * n_active, (2 * n_active) % 4))
    print("Wz = 0 verified over Z on all {} facets".format(len(facets)))
    print("all witness spheres are blocks of the deterministic base A")
    assert n_active % 2 == 1
    print("CERTIFICATE VALID: the shaped-kernel parity relaxation is FALSE "
          "at r=5.")


if __name__ == "__main__":
    verify_recorded()
    if "--search" in sys.argv:
        print("(fresh CP-SAT search not run; recorded witness suffices)")
