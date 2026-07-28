#!/usr/bin/env python3
"""Search at (n,r) = (13,5) for a violation of the amalgamation condition
(PART) over random 3-partitions.  A violation would be a counterexample with
an exactly checkable certificate.  Driver only: any hit is re-proved."""
import random
import sys

from classb import check_class_B, random_class_B, random_move
from conditions import partition_feasible, random_partitions

seed = int(sys.argv[1]); ninst = int(sys.argv[2]); nparts = int(sys.argv[3])
rng = random.Random(seed)
n, q = 13, 17
tested = 0
for _ in range(ninst):
    forb = random_class_B(n, q, rng)
    if forb is None:
        continue
    for _ in range(rng.randrange(0, 600)):
        nf = random_move(n, q, forb, rng)
        if nf:
            forb = nf
    try:
        check_class_B(n, q, forb)
    except AssertionError:
        continue
    for P in random_partitions(n, 3, rng, nparts):
        if not partition_feasible(n, q, forb, P):
            print("PART VIOLATION", forb, P, flush=True)
        tested += 1
print("seed=%d: %d (instance, 3-partition) pairs tested, no (PART) violation"
      % (seed, tested), flush=True)
