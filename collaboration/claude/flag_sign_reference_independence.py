#!/usr/bin/env python3
"""COMPUTATION companion to flag_sign_reference_independence.md.

Checks, on the audited k=16 Wallis chart (conditions 1-2 data only,
which is all the lemma uses), for 200 random global relabellings tau:
  (a) per-i identity:   prod_u R_tau(i,u) == prod_v eps_tau({v, L_i(v)})
  (b) global identity:  prod_{i,u} R_tau(i,u) == +1
where R_tau(i,u) = prod over generic finite x != u, L_i(u) of
eps_tau({L_i^{-1}(x), mate of u in the x-class of M_i}).
Deterministic seed; exits nonzero on failure.
"""
import random
import sys
sys.path.insert(0, __file__.rsplit("/", 3)[0] + "/evidence")
from global_latin_audit import construct_golf17  # noqa: E402

K = 16
golf = construct_golf17()
L = [[None] * K for _ in range(15)]
for i in range(15):
    for u in range(K):
        seen = {golf[i][u][v] for v in range(K) if v != u}
        L[i][u] = next(x for x in range(K + 1) if x not in seen and x != u)
Linv = [[None] * (K + 1) for _ in range(15)]
for i in range(15):
    for u in range(K):
        Linv[i][L[i][u]] = u
mate = [[[None] * (K + 1) for _ in range(K)] for _ in range(15)]
for i in range(15):
    for u in range(K):
        for v in range(K):
            if v != u:
                mate[i][u][golf[i][u][v]] = v   # mate of u in colour-class

rng = random.Random(835)
for trial in range(200):
    tau = list(range(K))
    rng.shuffle(tau)

    def eps(a, b):
        return -1 if (a < b) != (tau[a] < tau[b]) else 1

    total = 1
    for i in range(15):
        prod_u = 1
        for u in range(K):
            r = 1
            for x in range(K):
                if x in (u, L[i][u]):
                    continue
                r *= eps(Linv[i][x], mate[i][u][x])
            prod_u *= r
        rhs = 1
        for v in range(K):
            rhs *= eps(v, L[i][v])
        assert prod_u == rhs, (trial, i)
        total *= prod_u
    assert total == 1, trial
print("[ok] per-i and global cancellation identities hold on the Wallis "
      "chart for 200 random relabellings")
