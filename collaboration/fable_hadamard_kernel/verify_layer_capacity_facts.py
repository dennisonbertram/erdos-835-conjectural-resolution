#!/usr/bin/env python3
"""Exact facts for the k=16 Hadamard-kernel shadow at the derived layers.

(1) Wilson diagonal entries of W_{4,5}(21) and W_{3,4}(20) are coprime
    to 17, so both inclusion matrices have FULL rank mod 17; hence
    ker M_D has dimension >= (#nonzero-class columns) - full rank
    >> 15 for every possible member D.  The modular inclusion-matrix
    rank therefore gives NO universal capacity bound (determination (c):
    negative, proved).
(2) Adjacent-star overlap before deleting D at the LS(4,5,21) layer:
    two 4-stars with |B cap B'| = 3 share exactly the single block
    B cup B'.  After deletion they share it iff B cup B' is not in D.
    The underlying overlap count is verified by direct enumeration.
Deterministic, stdlib only.
"""

from math import comb
from itertools import combinations

# (1) Wilson diagonal + rank bookkeeping
for t, kk, v, bD in ((4, 5, 21, 1197), (3, 4, 20, 285)):
    diag = [comb(kk - j, t - j) for j in range(t + 1)]
    assert all(d % 17 for d in diag), diag
    full = comb(v, t)
    cols = comb(v, kk) - bD
    print(
        f"W_{{{t},{kk}}}({v}): diag {diag} all coprime to 17 -> "
        f"rank_17 = {full} (full); columns after deleting any member "
        f"= {cols}; ker M_D >= {cols - full} >> 15"
    )

# (2) adjacent-star overlap (exact, small enumeration on a window)
V = range(9)  # local window suffices: containment is local
B = (0, 1, 2, 3)
Bp = (0, 1, 2, 4)
shared = [c for c in combinations(V, 5) if set(B) <= set(c) and set(Bp) <= set(c)]
assert shared == [(0, 1, 2, 3, 4)]
print(
    "adjacent 4-stars (|cap| = 3) share one block before deletion; "
    "after deletion they share it iff the union is not in D: verified"
)
print("ALL CHECKS PASSED")
