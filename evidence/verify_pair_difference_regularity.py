#!/usr/bin/env python3
"""Validator: complete pair-difference regularity of S(14,15,31).

THEOREM.  In every hypothetical S(14,15,31), the number m_D of unordered
block pairs with B1 xor B2 = D depends only on |D|, refined at |D| = 16
by whether D^c is a block:
    |D|:   4      6      8      10     12     14     16int  16ext
    m_D:   235980 174800 165186 153216 147972 144144 157425 142590
    |D|:   18     20     22     24     26     28    (m_D = m_{32-|D|})
    m_D:   144144 147972 153216 165186 174800 235980
(|D| = 2 and 30 are empty: n_14 = n_0 = 0.)

Proof structure verified here:
 1. 3*A4 = sum_D C(m_D, 2) where A4 = #block 4-subsets with XOR = 0
    (weight-4 dual words of BOTH the full and even incidence codes; a
    4-subset splits into equal-difference pairs in exactly 3 ways and
    two equal-difference pairs cannot share a block).  A4 is FORCED:
    A4 = (2^{-31} sum_S F(S)^4 - b - 3b(b-1)) / 24
       = 3 793 226 637 448 341 180.
 2. The layer totals sum_{|D|=d} m_D = b*n_j/2 (d = 30-2j) are forced,
    the internal-16 values are forced individually (m_{B^c} = per-block
    triangle count 157425, from the punctured-enumerator theorem), and
    every layer average is an INTEGER.
 3. The uniform assignment already achieves sum_D C(m_D,2) = 3*A4
    EXACTLY (both sides 11 379 679 912 345 023 540).  C(m,2) is
    strictly convex, so any deviation from the uniform values strictly
    increases the sum: equality forces m_D uniform per class.  QED.

Consequences checked: the group-ring identity in Z[Z_2^31]
    A^2 = b*1 + 2*sum_d q_d K_d + 2*14835*xbar*A
(A = sum_B x^{1_B}, xbar = x^{1_X}, K_d = layer sums, 14835 =
157425-142590) holds at EVERY character: F(S)^2 = b + 2 sum_D m_D
(-1)^{|D cap S|} for all 32 size classes incl. both middle splits.
Equivalently (A - 14835*xbar)^2 = E with E forced.

Controls: the ACTUAL designs at r=3 and r=5 satisfy the same
regularity with middle split: r=3: |D|=4 internal 3, external 0;
r=5: |D|=4 all 3, |D|=6 internal 10 / external 0, |D|=8 all 3.
External middle value 0 <=> full triangle closure (true at r=3,5);
at r=15 the external value 142590 > 0 quantifies non-closure.
Run: python3 verify_pair_difference_regularity.py   (~15 s)
"""
import sys
from math import comb
from itertools import combinations
from collections import Counter

HERE = __file__.rsplit("/", 1)[0] or "."
V = 31
LAM = [comb(V - j, 14 - j) // (15 - j) for j in range(15)]
B = LAM[0]


def F_ext(s):
    if s <= 14:
        return sum((-2) ** j * comb(s, j) * LAM[j] for j in range(s + 1))
    if s == 15:
        return sum((-2) ** j * comb(15, j) * LAM[j] for j in range(15))
    return -F_ext(31 - s)


F15 = F_ext(15)


def F_classes(s):
    if s == 15:
        return [(F15 - 2 ** 15, B), (F15, comb(31, 15) - B)]
    if s == 16:
        return [(-F15 + 2 ** 15, B), (-F15, comb(31, 16) - B)]
    return [(F_ext(s), comb(31, s))]


def main():
    # 1. forced A4
    S4 = sum(c * f ** 4 for s in range(32) for f, c in F_classes(s))
    assert S4 % 2 ** 31 == 0
    A4, rem = divmod(S4 // 2 ** 31 - B - 3 * B * (B - 1), 24)
    assert rem == 0 and A4 == 3793226637448341180
    print("[ok] forced A4 =", A4)

    # 2. layer data
    rhs = [comb(15, i) * (LAM[i] - 1) for i in range(15)]
    n = [0] * 15
    for j in range(14, -1, -1):
        n[j] = rhs[j] - sum(comb(i, j) * n[i] for i in range(j + 1, 15))
    assert sum(n) == B - 1 and n[0] == 0 and n[14] == 0
    q = {}
    for j in range(1, 14):
        d = 30 - 2 * j
        if d == 16:
            continue
        tot = B * n[j] // 2
        assert (B * n[j]) % 2 == 0 and tot % comb(31, d) == 0
        q[d] = tot // comb(31, d)
    expect = {4: 235980, 6: 174800, 8: 165186, 10: 153216, 12: 147972,
              14: 144144, 18: 144144, 20: 147972, 22: 153216,
              24: 165186, 26: 174800, 28: 235980}
    assert q == expect
    P7 = B * n[7] // 2
    M_INT = 157425                      # forced per-block triangle count
    N_EXT = comb(31, 16) - B
    m_ext, rem = divmod(P7 - B * M_INT, N_EXT)
    assert rem == 0 and m_ext == 142590
    print("[ok] layer averages integral; q table + 16-split (157425/142590)")

    # 3. exact convexity equality
    tot = B * comb(M_INT, 2) + N_EXT * comb(m_ext, 2) + sum(
        comb(31, d) * comb(qd, 2) for d, qd in q.items())
    assert tot == 3 * A4 == 11379679912345023540
    print("[ok] uniform sum C(m,2) = 3*A4 exactly -> regularity forced")

    # 4. group-ring / character identity at every size class
    def K(d, s):
        return sum((-1) ** h * comb(s, h) * comb(31 - s, d - h)
                   for h in range(min(s, d) + 1))
    delta = M_INT - m_ext
    for s in range(32):
        for f, _ in F_classes(s):
            assert f * f == B + 2 * (sum(q[d] * K(d, s) for d in q)
                                     + m_ext * K(16, s)
                                     + delta * (-1) ** s * f), s
    print("[ok] F(S)^2 = b + 2 sum_D m_D chi_S(D) at all 32 classes")

    # 5. actual-design controls at r=3, r=5
    src = open(f"{HERE}/verify_H_identity.py").read().split("if __name__")[0]
    ns = {}
    exec(compile(src, "vhi", "exec"), ns)
    want = {(7, 3): {(4, True): {3: 7}, (4, False): {0: 28}},
            (11, 5): {(4, False): {3: 330}, (6, True): {10: 66},
                      (6, False): {0: 396}, (8, False): {3: 165}}}
    for (v, r), spec in want.items():
        blocks = list(combinations(range(v), r))
        X0, Y0 = ns["cover_instance"](v, r - 1, blocks)
        A = [frozenset(bb) for bb in ns["algox"](X0, Y0, cap=1)[0]]
        compl = {frozenset(range(v)) - bb for bb in A}
        m = Counter()
        for B1, B2 in combinations(A, 2):
            m[frozenset(B1 ^ B2)] += 1
        got = {}
        for d in range(2, v, 2):
            for internal in (True, False):
                cls = [D for D in map(frozenset, combinations(range(v), d))
                       if (D in compl) == internal] if d == r + 1 else (
                       [] if internal else
                       list(map(frozenset, combinations(range(v), d))))
                if not cls:
                    continue
                dist = Counter(m.get(D, 0) for D in cls)
                if set(dist) != {0} or (d, internal) in spec:
                    got[(d, internal)] = dict(dist)
        assert got == spec, (v, r, got)
        print(f"[ok] actual r={r}: layer-uniform with middle split, "
              f"external middle value 0 (= full closure)")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
