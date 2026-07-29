#!/usr/bin/env python3
"""Exhaustive small-field validation of the e4 edge-law algebra (PROOF.md).

The identities behind Theorems A/B are proved for k-sets over any
F_{2^m}, k >= 4.  This checker replays ALL of them exhaustively in
F_16 = F_2[beta]/(beta^4+beta+1) with k = 8:

  * every 9-set R (11,440 of them), every deletion:   (L0.1), (L0.2);
  * every adjacent pair of 8-sets (411,840 = 11,440 * 36 unordered
    pairs):                                            (L1.1), a != b;
  * every pair with both e2-hypotheses:                x = a, y = b,
                                                       defect identity (A.1);
  * every pair with all four hypotheses (Theorem A):   e1=e2=e3(R)=0 and
                                                       e4(S)+a^4 = e4(R) = e4(T)+b^4;
  * every R with e1=e2=e3(R)=0 (Theorem B):            all deletion states on
                                                       the refined curve with
                                                       lambda_R quartic labels;
  * bijection count: fully-on-curve adjacent pairs == 36 * |R-family|;
  * necessity of hypotheses: nonzero counts of (i) pairs where an e2
    hypothesis fails and x != a, (ii) pairs where both e2 hold, an e3
    fails, and h(S) != h(T).

Independent of the F_32 enumeration code: different field, different
loop structure, statistics recomputed from scratch at every step.
"""

from itertools import combinations

MOD16 = 0b10011  # beta^4 + beta + 1


def mul(left: int, right: int) -> int:
    raw = 0
    for bit in range(4):
        if right >> bit & 1:
            raw ^= left << bit
    for degree in range(6, 3, -1):
        if raw >> degree & 1:
            raw ^= MOD16 << (degree - 4)
    return raw


MUL = [[mul(a, b) for b in range(16)] for a in range(16)]
INV = [0] * 16
for a in range(1, 16):
    for b in range(1, 16):
        if MUL[a][b] == 1:
            INV[a] = b
            break


def fpow(a: int, e: int) -> int:
    r = 1
    while e:
        if e & 1:
            r = MUL[r][a]
        a = MUL[a][a]
        e >>= 1
    return r


def stats(points) -> list:
    """[e_0..e_8] of a subset of F_16, from the definition."""
    e = [1] + [0] * 8
    for p in points:
        for d in range(8, 0, -1):
            e[d] ^= MUL[p][e[d - 1]]
    return e


def main() -> None:
    n_r = n_del = n_pairs = 0
    n_e2_fail_xne_a = 0        # e2 hypothesis broken and x != a
    n_e3_fail_h_mismatch = 0   # both e2 hold, some e3 broken, h(S) != h(T)
    n_full_curve_pairs = 0
    curve_family = []          # 9-sets with e1=e2=e3=0

    for R in combinations(range(16), 9):
        n_r += 1
        Rset = set(R)
        eR = stats(R)

        # (L0.1)/(L0.2) for every deletion
        del_stats = {}
        for x in R:
            S = sorted(Rset - {x})
            eS = stats(S)
            del_stats[x] = eS
            for j in range(1, 9):
                assert eR[j] == eS[j] ^ MUL[x][eS[j - 1]], "L0.1"
            for m in range(0, 9):
                acc = 0
                for j in range(0, m + 1):
                    acc ^= MUL[eR[j]][fpow(x, m - j)]
                assert eS[m] == acc, "L0.2"
            n_del += 1

        if eR[1] == 0 and eR[2] == 0 and eR[3] == 0:
            curve_family.append(R)
            r = eR[4]
            # Theorem B part 1: every deletion state is on the refined curve
            for a in R:
                eS = del_stats[a]
                assert eS[1] == a
                assert eS[2] == fpow(a, 2)
                assert eS[3] == fpow(a, 3)
                assert eS[4] == fpow(a, 4) ^ r
                lam = MUL[r][a] ^ eR[5]
                lam = MUL[lam][a] ^ eR[6]
                lam = MUL[lam][a] ^ eR[7]
                lam = MUL[lam][a] ^ eR[8]
                assert eS[8] ^ fpow(a, 8) == lam, "lambda quartic"

        for x, y in combinations(R, 2):
            n_pairs += 1
            eS, eT = del_stats[x], del_stats[y]
            a, b = eS[1], eT[1]
            # Lemma 1.1
            assert a != b, "adjacent sets share e1"
            assert x ^ y == a ^ b, "x+y = a+b"
            # Lemma 1.2 (L1.1): deleted point from e1,e2 data
            num = eS[2] ^ eT[2] ^ MUL[b][a ^ b]
            assert x == MUL[num][INV[a ^ b]], "L1.1"

            e2S_curve = eS[2] == fpow(a, 2)
            e2T_curve = eT[2] == fpow(b, 2)
            if not (e2S_curve and e2T_curve):
                if x != a:
                    n_e2_fail_xne_a += 1
                continue
            # both e2 hypotheses: deleted points are the e1 values
            assert x == a and y == b, "Theorem A part 1"
            # defect identity (A.1) at both endpoints
            assert (eT[4] ^ fpow(b, 4)) ^ eR[4] == MUL[b][eT[3] ^ fpow(b, 3)]
            assert (eS[4] ^ fpow(a, 4)) ^ eR[4] == MUL[a][eS[3] ^ fpow(a, 3)]

            e3S_curve = eS[3] == fpow(a, 3)
            e3T_curve = eT[3] == fpow(b, 3)
            hS = eS[4] ^ fpow(a, 4)
            hT = eT[4] ^ fpow(b, 4)
            if e3S_curve and e3T_curve:
                n_full_curve_pairs += 1
                # Theorem A parts 2-3
                assert eR[1] == 0 and eR[2] == 0 and eR[3] == 0
                assert hS == eR[4] == hT
            elif hS != hT:
                n_e3_fail_h_mismatch += 1

    assert n_r == 11440 and n_del == 11440 * 9 and n_pairs == 11440 * 36
    # Theorem B part 3 (bijection of fully-on-curve edges with (R, pair)):
    assert n_full_curve_pairs == 36 * len(curve_family)
    # hypothesis necessity: dropped hypotheses really break the law
    assert n_e2_fail_xne_a > 0
    assert n_e3_fail_h_mismatch > 0

    print("F16 exhaustive edge-law validation: PASS")
    print("9-sets checked:", n_r, " deletions:", n_del,
          " adjacent pairs:", n_pairs)
    print("R-family (e1=e2=e3=0):", len(curve_family),
          " fully-on-curve pairs:", n_full_curve_pairs)
    print("counterexamples with an e2 hypothesis dropped (x != a):",
          n_e2_fail_xne_a)
    print("counterexamples with e3 dropped (h mismatch):",
          n_e3_fail_h_mismatch)


if __name__ == "__main__":
    main()
