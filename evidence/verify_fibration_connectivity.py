#!/usr/bin/env python3
"""Exact validator: fibration-graph connectivity + spectator census over
ALL unordered r=5 mate pairs (10,296) of a base S(4,5,11).

Facts checked/censused:
  - the split-(r+2)-set configuration graph on Delta u Delta is
    (r-1)-regular bipartite, SIMPLE, and CONNECTED for every pair;
  - #edges = (r-1) t;
  - spectator lemma: each split Z contains exactly (r+1)/2 - 2 = 1
    non-base A-block S, and w_B(S), w_C(S) are outside Z;
  - census of spectator membership in Delta (per-pair parity etc.).

Generic screen (PROVED, no computation): connectivity alone cannot
force t even.  For fixed d = r-1 and any t > d, take left and right
copies of Z/tZ and join x_L to (x+s)_R for s = 0,...,d-1.  This is a
simple d-regular bipartite graph; it is connected when d >= 2 because
the shifts 0 and 1 generate every vertex.  Odd t is allowed.  Hence
\{connected + (r-1)-regular bipartite\} does not imply parity, and any
symbolic invariant must use N1c/N3/N4 content.
Run: python3 verify_fibration_connectivity.py
"""
import sys
from itertools import combinations
from collections import Counter

sys.setrecursionlimit(100000)
HERE = __file__.rsplit("/", 1)[0] or "."
src = open(f"{HERE}/verify_H_identity.py").read().split("if __name__")[0]
ns = {}
exec(compile(src, "verify_H_identity.py", "exec"), ns)

V, R = 11, 5


def main():
    blocks = list(combinations(range(V), R))
    X0, Y0 = ns["cover_instance"](V, R - 1, blocks)
    A = ns["algox"](X0, Y0, cap=1)[0]
    rest = [x for x in blocks if x not in set(A)]
    X1, Y1 = ns["cover_instance"](V, R - 1, rest)
    mates = ns["algox"](X1, Y1, cap=None)
    ws = [ns["wmap"](A, M, V) for M in mates]
    Aset = [set(P) for P in A]

    t_census = Counter()
    specD_census = Counter()
    pairs = 0
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            wB, wC = ws[i], ws[j]
            delta = [P for P in A if wB[P] != wC[P]]
            t = len(delta)
            cfg = ns["x_configurations"](A, wB, wC, R)
            assert len(cfg) == (R - 1) * t
            adj = {}
            spec_in_delta = 0
            for Z, (P, Q) in cfg.items():
                Zs = set(Z)
                # spectator: the third A-block inside Z
                spect = [S for S, Ss in zip(A, Aset)
                         if Ss <= Zs and S != P and S != Q]
                assert len(spect) == 1
                S = spect[0]
                assert wB[S] not in Zs and wC[S] not in Zs
                if wB[S] != wC[S]:
                    spec_in_delta += 1
                adj.setdefault(("B", P), []).append(("C", Q))
                adj.setdefault(("C", Q), []).append(("B", P))
            # regularity + simplicity
            for node, nbrs in adj.items():
                assert len(nbrs) == R - 1
                assert len(set(nbrs)) == R - 1
            # connectivity
            start = next(iter(adj))
            comp = {start}
            stack = [start]
            while stack:
                u = stack.pop()
                for w2 in adj[u]:
                    if w2 not in comp:
                        comp.add(w2)
                        stack.append(w2)
            assert len(comp) == 2 * t, (len(comp), t)
            t_census[t] += 1
            specD_census[(t, spec_in_delta)] += 1
            pairs += 1
    print(f"pairs checked: {pairs} (expect 10296)")
    print(f"t census: {dict(sorted(t_census.items()))}")
    print("(t, #edges with spectator in Delta) census:")
    for k, c in sorted(specD_census.items()):
        print(f"    {k}: x{c}")
    print("ALL pairs: fibration graph simple, (r-1)-regular, CONNECTED; "
          "spectator lemma verified on every split 7-set")


if __name__ == "__main__":
    main()
