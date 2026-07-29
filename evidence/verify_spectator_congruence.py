#!/usr/bin/env python3
"""Validator: spectator double-count identities I1-I4 and the
t-blindness congruence, on ALL mate pairs at r=3 and r=5.

Notation: m = (r+1)/2; ordered pairs (P,S) of distinct A-blocks with
|P intersection S| = r-2; Delta = disagreement set of a mate pair; U_B counts
[w_B(P) in S]; U^D restricts to P in Delta; U^DD to both in Delta;
Sigma_gamma = sum over P in Delta of the number of OTHER Delta-blocks
inside the crossed set Z_P = P u {w_B(P), w_C(P)}; Sigma_spec = number
of (split set, Delta-spectator) incidences.

PROVED identities checked exactly:
  I1: U_B = U_C = r b (m-1)
  I2: no mutual single-tiling arcs ([w_B(P) in S and w_B(S) in P] = 0)
  I3: U_B^D = r t (m-1)
  I4: U^DD = Sigma_gamma + (r-1) t + Sigma_spec, same value for B and C
  C : Sigma_spec == U^DD + Sigma_gamma (mod 2); the t-term (r-1)t is
      even for every odd r, so t is ABSENT from the congruence
      (t-blindness of first-moment spectator counts).

Run: python3 verify_spectator_congruence.py
"""
import sys
from itertools import combinations
from collections import Counter

sys.setrecursionlimit(100000)
HERE = __file__.rsplit("/", 1)[0] or "."
src = open(f"{HERE}/verify_H_identity.py").read().split("if __name__")[0]
ns = {}
exec(compile(src, "verify_H_identity.py", "exec"), ns)


def run(v, r):
    m = (r + 1) // 2
    blocks = list(combinations(range(v), r))
    X0, Y0 = ns["cover_instance"](v, r - 1, blocks)
    A = ns["algox"](X0, Y0, cap=1)[0]
    b = len(A)
    rest = [x for x in blocks if x not in set(A)]
    X1, Y1 = ns["cover_instance"](v, r - 1, rest)
    mates = ns["algox"](X1, Y1, cap=None)
    ws = [ns["wmap"](A, M, v) for M in mates]
    Asets = {P: set(P) for P in A}
    contained = {}
    for Z in combinations(range(v), r + 2):
        Zs = set(Z)
        contained[Z] = [P for P in A if Asets[P] <= Zs]
        assert len(contained[Z]) == m
    pairs_r2 = [(P, S) for P in A for S in A
                if P != S and len(set(P) & set(S)) == r - 2]
    split_candidates = []
    for P, Q in pairs_r2:
        Ps, Qs = Asets[P], Asets[Q]
        Z = tuple(sorted(Ps | Qs))
        spectators = tuple(
            S for S in contained[Z] if S != P and S != Q
        )
        assert len(spectators) == m - 2
        split_candidates.append(
            (P, Q, Qs - Ps, Ps - Qs, Z, spectators)
        )
    checked = 0
    species = Counter()
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            wB, wC = ws[i], ws[j]
            delta = {P for P in A if wB[P] != wC[P]}
            t = len(delta)
            UB = sum(1 for P, S in pairs_r2 if wB[P] in S)
            UC = sum(1 for P, S in pairs_r2 if wC[P] in S)
            assert UB == r * b * (m - 1) == UC
            assert not any(wB[P] in S and wB[S] in P for P, S in pairs_r2)
            UBd = sum(1 for P, S in pairs_r2
                      if P in delta and wB[P] in S)
            assert UBd == r * t * (m - 1)
            UBdd = sum(1 for P, S in pairs_r2
                       if P in delta and S in delta and wB[P] in S)
            UCdd = sum(1 for P, S in pairs_r2
                       if P in delta and S in delta and wC[P] in S)
            assert UBdd == UCdd
            Sg = 0
            for P in delta:
                Zp = set(P) | {wB[P], wC[P]}
                Sg += sum(1 for S in A
                          if S != P and set(S) <= Zp and S in delta)
            Sspec = UBdd - Sg - (r - 1) * t
            assert Sspec >= 0
            # Check that the residual in I4 is the claimed combinatorial
            # quantity, not merely a nonnegative number: for every split
            # (r+2)-set, enumerate its spectator A-blocks directly and count
            # those lying in Delta.
            configs = [
                item for item in split_candidates
                if wB[item[0]] in item[2] and wC[item[1]] in item[3]
            ]
            assert len(configs) == (r - 1) * t
            assert len({item[4] for item in configs}) == len(configs)
            actual_spec = 0
            for P, Q, _, _, Z, spectators in configs:
                Zs = set(Z)
                assert all(wB[S] not in Zs and wC[S] not in Zs
                           for S in spectators)
                actual_spec += sum(S in delta for S in spectators)
            assert Sspec == actual_spec
            assert Sspec % 2 == (UBdd + Sg) % 2
            species[(t, Sg, UBdd, Sspec)] += 1
            checked += 1
    print(f"[r={r}] I1-I4 + congruence verified on {checked} pairs")
    for k, c in sorted(species.items()):
        print(f"    (t, Sg, Udd, Sspec) = {k}  x{c}")


if __name__ == "__main__":
    run(7, 3)
    run(11, 5)
