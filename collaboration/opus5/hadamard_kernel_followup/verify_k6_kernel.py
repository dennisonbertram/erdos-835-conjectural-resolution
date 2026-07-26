#!/usr/bin/env python3
"""Exact rank/nullity of M_D over F_7 for the Witt S(5,6,12) zero class (k=6).

Exact integer arithmetic mod 7 throughout (numpy int64 is used only as an
array container; no floating point is involved).  Requires numpy.

Run:  python3 -B collaboration/opus5/hadamard_kernel_followup/verify_k6_kernel.py
"""

from __future__ import annotations

import itertools
import os
import sys
from math import comb
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_frame_and_clique import witt_s5612, is_steiner


def rank_mod_p(A, p):
    A = A % p
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i, c] % p:
                piv = i
                break
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * pow(int(A[r, c]), p - 2, p)) % p
        nz = np.nonzero(A[:, c] % p)[0]
        for i in nz:
            if i != r:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
        if r == rows:
            break
    return r


def main():
    n, k, p = 12, 6, 7
    D = witt_s5612()
    assert len(D) == 132 and is_steiner(D, n, k)
    X = [frozenset(S) for S in itertools.combinations(range(n), k)]
    Y = [frozenset(S) for S in itertools.combinations(range(n), k - 1)]
    Dset = set(D)
    cols = [S for S in X if S not in Dset]
    assert len(cols) == len(Y) == comb(n, k - 1) == 792
    M = np.zeros((len(Y), len(cols)), dtype=np.int64)
    for r, B in enumerate(Y):
        for c, S in enumerate(cols):
            if B <= S:
                M[r, c] = 1
    rk = rank_mod_p(M.copy(), p)
    nul = len(cols) - rk
    print(f"k=6, p=7: Witt S(5,6,12), |D|={len(D)}, M_D is {len(Y)}x{len(cols)}")
    print(f"          rank over F_7 = {rk}, dim ker M_D = {nul}")
    assert (rk, nul) == (715, 77), (rk, nul)
    print(f"          |D|/2 = {len(D) // 2} != {nul}: the |D|/2 pattern is FALSE")
    print("EXACT k=6 KERNEL CHECK PASSED")


if __name__ == "__main__":
    main()
