#!/usr/bin/env python3
"""LP-margin annealing for the general two-parameter family Pi(n, r).

Maximises the chance of driving phi* below 0; phi* < 0 certifies that the
fractional relaxation is infeasible, hence that no completion exists.  Float
LP only: any hit is re-proved exactly elsewhere.

usage: python3 lphunt.py N R SEED RESTARTS STEPS
"""
import random
import sys

from general import profiles, random_instance, random_move, check_instance
from lpmargin import phi

n, r, seed, restarts, steps = (int(x) for x in sys.argv[1:6])
q = n + r - 1
rng = random.Random(seed)
best = (1e9, None)
out = "logs/lphunt_%d_%d_%d.txt" % (n, r, seed)
for rr in range(restarts):
    forb = random_instance(n, r, rng)
    if forb is None:
        break
    cur = phi(n, q, forb)
    if cur is None:
        continue
    for s in range(steps):
        T = 0.20 * (0.002 / 0.20) ** (s / max(1, steps - 1))
        nf = random_move(n, r, forb, rng)
        if nf is None:
            continue
        try:
            check_instance(n, r, nf)
        except AssertionError:
            continue
        v = phi(n, q, nf)
        if v is None:
            v = -1.0
        if v <= cur or rng.random() < pow(2.718281828, (cur - v) / T):
            forb, cur = nf, v
        if cur < best[0]:
            best = (cur, list(forb))
            if cur < -1e-9:
                print("LP-INFEASIBLE n=%d r=%d phi*=%.6g %s" % (n, r, cur, forb), flush=True)
                open(out, "a").write("LPCAND %d %d %.6g %s\n" % (n, r, cur, forb))
print("n=%d r=%d mu=%d seed=%d restarts=%d steps=%d best phi* = %.6g" %
      (n, r, n - r, seed, restarts, steps, best[0]), flush=True)
print("best instance:", best[1], flush=True)
