#!/usr/bin/env python3
"""Disjointness-graph structure for odd-graph perfect-code families.

k=4: verify the 30 labelled Fanos' disjointness graph is a perfect matching.
k=6: build one S(4,5,11) by exact cover, then enumerate ALL S(4,5,11)s
block-disjoint from it (capped).  Count 1 would extend the Fano matching
phenomenon; a large count kills that conjecture.
"""
import sys, time
from itertools import combinations, permutations

sys.setrecursionlimit(100000)


def algox_solutions(X, Y, cap=None, deadline=None):
    """Yield exact-cover solutions (Algorithm X, dict-of-sets)."""
    solution = []
    out = []

    def select(r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for kk in Y[i]:
                    if kk != j:
                        X[kk].remove(i)
            cols.append(X.pop(j))
        return cols

    def deselect(r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for kk in Y[i]:
                    if kk != j:
                        X[kk].add(i)

    def solve():
        if cap is not None and len(out) >= cap:
            return
        if deadline is not None and time.time() > deadline:
            raise TimeoutError
        if not X:
            out.append(list(solution))
            return
        c = min(X, key=lambda c: len(X[c]))
        for r in sorted(X[c]):
            solution.append(r)
            cols = select(r)
            solve()
            deselect(r, cols)
            solution.pop()

    solve()
    return out


def steiner_cover_instance(v, t, blocks):
    Y = {b: [("t", s) for s in combinations(b, t)] for b in blocks}
    X = {}
    for r, cs in Y.items():
        for c in cs:
            X.setdefault(c, set()).add(r)
    return X, Y


def fano_matching_check():
    triples = list(combinations(range(7), 3))
    base = [b for b in triples
            if (1 << b[0] | 1 << b[1] | 1 << b[2]) and
            (b[0] + 1) ^ (b[1] + 1) ^ (b[2] + 1) == 0]
    # base via xor labels 1..7
    base = [b for b in triples if (b[0]+1) ^ (b[1]+1) ^ (b[2]+1) == 0]
    assert len(base) == 7
    fanos = set()
    for p in permutations(range(7)):
        fanos.add(frozenset(frozenset(p[x] for x in b) for b in base))
    fanos = list(fanos)
    assert len(fanos) == 30
    degs = []
    for f in fanos:
        d = sum(1 for g in fanos if g is not f and not (f & g))
        degs.append(d)
    print(f"[k=4] labelled Fanos: {len(fanos)}; disjointness degrees: "
          f"min={min(degs)} max={max(degs)} "
          f"({'perfect matching' if set(degs) == {1} else 'NOT a matching'})")


def s4511_mates(cap=2000, seconds=1200):
    v, t, ksz = 11, 4, 5
    blocks = list(combinations(range(v), ksz))
    X, Y = steiner_cover_instance(v, t, blocks)
    first = algox_solutions(X, Y, cap=1)[0]
    assert len(first) == 66
    cover = set()
    for b in first:
        for s in combinations(b, t):
            assert s not in cover
            cover.add(s)
    assert len(cover) == 330
    print(f"[k=6] built an S(4,5,11) (66 blocks)")
    used = set(first)
    rest = [b for b in blocks if b not in used]
    X2, Y2 = steiner_cover_instance(v, t, rest)
    t0 = time.time()
    try:
        sols = algox_solutions(X2, Y2, cap=cap,
                               deadline=time.time() + seconds)
        capped = len(sols) >= cap
        print(f"[k=6] disjoint mates found: {len(sols)}"
              f"{' (CAP reached)' if capped else ' (complete enumeration)'}"
              f"  [{time.time()-t0:.1f}s]")
    except TimeoutError:
        print(f"[k=6] enumeration timed out at {seconds}s "
              f"(found so far: partial)")


if __name__ == "__main__":
    fano_matching_check()
    s4511_mates()
