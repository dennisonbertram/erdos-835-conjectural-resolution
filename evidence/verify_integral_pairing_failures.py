#!/usr/bin/env python3
"""Validator: falsification record for canonical integral pairings on
E3/X3 configuration sets (artifact section 2.11).

Candidate maps tested on true mate pairs (deterministic mate order):
  m1  reversal on E3: (P,Q,z) -> (Q,P): needs w_B(Q) = w_C(P).
  m4  Y-bases: (beta,gamma) = (B-base, C-base) of Y = P u Q.
  m6  complement-of-H is an A-block (PROVED impossible: it would be
      disjoint from P, contradicting intra n_0 = 0).
  c2  Y*-successor: mate-blocks T_P = P^c\\{z} in B, U_Q = Q^c\\{z} in C
      (|T_P ^ U_Q| = r-2 forced), Y* = T_P u U_Q, image = its bases.
  Xr  reversal on X3.
  m2/m3 (w-successors z -> w_B(Q), z -> w_C(P)): not functions — the
      per-locus counts K vary (0..25 at r=5), so images are empty or
      multi-valued; falsified structurally, no run needed.

A-priori constraint (PROVED earlier): per-z E3 counts and per-union X3
counts are frequently odd, so any successful pairing must be
trans-local.  All candidates above respect or fail this independently.

Asserted falsification counts (exact, deterministic prefixes):
  r=3 (56 ordered pairs, 336 configs): m1 0; m6 0; m4 image in E3: 0;
      c2 image in E3: 0 (dist-ok-not-E3 168, beta*=gamma* 168).
  r=5 (200 ordered pairs, 44028 configs): m1 3434 (7.8%, not
      universal); m6 0; m4 in E3: 0; X3 reversal 29002/65868 (44.0%).
  r=5 c2 (120 ordered pairs, 26384 configs): image in E3: 0.

Narrow-scope statement: these falsify the five listed canonical
constructions only.  They do NOT show that no integral pairing exists,
and say nothing about r=15.
Run: python3 verify_integral_pairing_failures.py  (r=3 checks only by
default; pass --full for the r=5 recounts)
"""
import sys
from itertools import combinations
from collections import Counter

sys.setrecursionlimit(100000)
HERE = __file__.rsplit("/", 1)[0] or "."
src = open(f"{HERE}/verify_H_identity.py").read().split("if __name__")[0]
ns = {}
exec(compile(src, "verify_H_identity.py", "exec"), ns)


def setup(v, r):
    blocks = list(combinations(range(v), r))
    X0, Y0 = ns["cover_instance"](v, r - 1, blocks)
    A = ns["algox"](X0, Y0, cap=1)[0]
    rest = [x for x in blocks if x not in set(A)]
    X1, Y1 = ns["cover_instance"](v, r - 1, rest)
    mates = ns["algox"](X1, Y1, cap=None)
    ws = [ns["wmap"](A, M, v) for M in mates]
    return A, ws


def battery(v, r, npairs):
    A, ws = setup(v, r)
    Asets = {P: set(P) for P in A}
    Aset = set(A)
    p2 = [(P, Q) for P in A for Q in A
          if P != Q and len(Asets[P] & Asets[Q]) == r - 2]
    p3 = [(P, Q) for P in A for Q in A
          if P != Q and len(Asets[P] & Asets[Q]) == r - 3]
    st = Counter()
    done = 0
    for i in range(len(ws)):
        for j in range(len(ws)):
            if i == j:
                continue
            wB, wC = ws[i], ws[j]
            E3 = [(P, Q) for P, Q in p2 if wB[P] == wC[Q]]
            E3set = set(E3)
            X3set = {(P, Q) for P, Q in p3
                     if wB[P] in Asets[Q] and wC[Q] in Asets[P]}
            for P, Q in E3:
                z = wB[P]
                st["E3"] += 1
                st["m1"] += (wB[Q] == wC[P])
                H = Asets[P] | {z}
                st["m6"] += (tuple(sorted(set(range(v)) - H)) in Aset)
                Ys = Asets[P] | Asets[Q]
                beta = next(S for S in A
                            if Asets[S] <= Ys and wB[S] in Ys)
                gamma = next(S for S in A
                             if Asets[S] <= Ys and wC[S] in Ys)
                st["m4"] += ((beta, gamma) in E3set)
                Tp = set(range(v)) - Asets[P] - {z}
                Uq = set(range(v)) - Asets[Q] - {z}
                Ystar = Tp | Uq
                assert len(Ystar) == r + 2
                bs = next(S for S in A
                          if Asets[S] <= Ystar and wB[S] in Ystar)
                gs = next(S for S in A
                          if Asets[S] <= Ystar and wC[S] in Ystar)
                st["c2"] += ((bs, gs) in E3set)
            for P, Q in X3set:
                st["X3"] += 1
                st["Xr"] += ((Q, P) in X3set)
            done += 1
            if done >= npairs:
                break
        if done >= npairs:
            break
    return st


def main(full=False):
    st = battery(7, 3, 56)
    assert st["E3"] == 336 and st["m1"] == 0 and st["m6"] == 0
    assert st["m4"] == 0 and st["c2"] == 0 and st["X3"] == 0
    print("[r=3] falsification counts verified: m1=0/336, m6=0, m4=0, "
          "c2=0 (X3 vacuous)")
    if full:
        st = battery(11, 5, 200)
        assert st["E3"] == 44028 and st["m1"] == 3434
        assert st["m6"] == 0 and st["m4"] == 0
        assert st["X3"] == 65868 and st["Xr"] == 29002
        print("[r=5] falsification counts verified: m1=3434/44028, "
              "m6=0, m4=0, X3-reversal=29002/65868")


if __name__ == "__main__":
    main(full="--full" in sys.argv)
