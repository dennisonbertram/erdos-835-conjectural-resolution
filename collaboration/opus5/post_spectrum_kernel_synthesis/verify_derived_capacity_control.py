#!/usr/bin/env python3
"""k=6 derived-layer control: one LS(2,3,9) exists and realises the forced
(p-2)-dimensional constant-Hadamard-product space.

This shows only that the DEGREE-TWO capacity bound cannot exclude that one
standalone derived large set.  It says nothing about higher-degree or
cross-layer compatibility obstructions.
Stdlib only, exact arithmetic over F_7.  Labels: EXACT COMPUTATION / PROVED.
"""

from __future__ import annotations
import itertools

P = 7  # p = k+1 with k = 6
N = 9  # the derived layer of a k=6 colouring is an LS(2,3,9)


def all_sts():
    out, blocks = [], []
    rem = {frozenset(p) for p in itertools.combinations(range(N), 2)}

    def rec():
        if not rem:
            out.append(list(blocks))
            return
        Pr = min(rem, key=lambda s: sorted(s))
        a, b = sorted(Pr)
        for c in range(N):
            if c in (a, b):
                continue
            B = frozenset((a, b, c))
            sub = [frozenset(x) for x in itertools.combinations(sorted(B), 2)]
            if any(s not in rem for s in sub):
                continue
            for s in sub:
                rem.discard(s)
            blocks.append(B)
            rec()
            blocks.pop()
            for s in sub:
                rem.add(s)

    rec()
    return out


def large_set(sts):
    sets = [frozenset(b) for b in sts]

    def rec(chosen, covered):
        if len(chosen) == P:
            return chosen
        for i in range(len(sets)):
            if i in chosen or (sets[i] & covered):
                continue
            r = rec(chosen + [i], covered | sets[i])
            if r:
                return r
        return None

    return rec([], frozenset()), sets


def rank_mod(rows, p):
    A = [r[:] for r in rows]
    m = len(A)
    nc = len(A[0]) if m else 0
    r = 0
    for c in range(nc):
        piv = next((i for i in range(r, m) if A[i][c] % p), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        iv = pow(A[r][c], p - 2, p)
        A[r] = [(x * iv) % p for x in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(nc)]
        r += 1
    return r


def main():
    print("=" * 74)
    print("k=6 DERIVED-LAYER CONTROL: LS(2,3,9)")
    print("=" * 74)
    sts = all_sts()
    print(f"  labelled STS(9): {len(sts)}, each with {len(sts[0])} blocks")
    LS, sets = large_set(sts)
    assert LS is not None
    tri = [frozenset(t) for t in itertools.combinations(range(N), 3)]
    cov = set().union(*[sets[i] for i in LS])
    assert len(cov) == len(tri) == 84 and sum(len(sets[i]) for i in LS) == 84
    print(
        f"  LS(2,3,9) FOUND: {P} disjoint systems partitioning all {len(tri)} triples"
    )
    print("  -> this standalone necessary derived large set exists")

    colour = {}
    for q, i in enumerate(LS):
        for B in sets[i]:
            colour[B] = q
    for Pr in itertools.combinations(range(N), 2):
        star = [B for B in tri if set(Pr) <= B]
        assert len(star) == N - 2 == P
        assert sorted(colour[B] for B in star) == list(range(P)), "star not rainbow"
    print(f"  every 2-star has exactly p = {P} triples and is rainbow: ok")

    D = [B for B in tri if colour[B] == 0]
    cols = [B for B in tri if colour[B] != 0]
    Y = [frozenset(p) for p in itertools.combinations(range(N), 2)]
    M = [[1 if Pr <= B else 0 for B in cols] for Pr in Y]
    print(
        f"  |D'|={len(D)}  M_D' is {len(Y)}x{len(cols)}; "
        f"rank_F7={rank_mod(M, P)}, nullity={len(cols) - rank_mod(M, P)}"
    )

    U = [[pow(colour[B], r, P) for B in cols] for r in range(1, P - 1)]
    assert rank_mod(U, P) == P - 2
    print(f"  U' = <g, g^2, ..., g^{P - 2}> has dimension {rank_mod(U, P)} = p-2: ok")
    for r, u in enumerate(U, start=1):
        img = [sum(M[i][j] * u[j] for j in range(len(cols))) % P for i in range(len(Y))]
        assert all(x == 0 for x in img), r
    print("  U' <= ker M_D': ok")
    bad = 0
    for r in range(1, P - 1):
        for s in range(1, P - 1):
            prod = [(U[r - 1][j] * U[s - 1][j]) % P for j in range(len(cols))]
            img = [
                sum(M[i][j] * prod[j] for j in range(len(cols))) % P
                for i in range(len(Y))
            ]
            want = (P - 1) % P if (r + s) == P - 1 else 0
            if len(set(img)) != 1 or img[0] != want:
                bad += 1
    assert bad == 0
    print("  M_D'(u_r o u_s) is constant, = -1 iff r+s = p-1: anti-diagonal Gram,")
    print("  NONDEGENERATE.  So the capacity at this derived layer is >= p-2 = 5.")

    print()
    print("=" * 74)
    print("CONSEQUENCE (PROVED)")
    print("=" * 74)
    print("  Logical implication, and nothing beyond it:")
    print("    a uniform degree-two capacity bound below p-2 at a derived layer")
    print("    implies, by the deleted-colour theorem, that no large set exists")
    print("    at that layer.")
    print()
    print("  At k=6: LS(2,3,9) exists, so no uniform degree-two capacity bound")
    print("  below 5 holds at that layer.  That is ALL this shows.  It does NOT")
    print("  show the descent 'cannot close' k=6, and it does NOT show that no")
    print("  higher-degree or cross-layer compatibility obstruction is visible")
    print("  there -- neither was tested.")
    print()
    print("  At k=16: a uniform degree-two capacity bound below 15 at the")
    print("  LS(4,5,21) layer would prove that no LS(4,5,21) exists.  Whether")
    print("  LS(4,5,21) exists is itself OPEN.  No comparison of difficulty")
    print("  between the two is claimed.")
    print()
    print("  Direction: capacity >= 15 does NOT imply the large set exists")
    print("  (degree two is only a relaxation of the full hierarchy).")
    print()
    print("k=16 is NOT settled.  Erdos-Rosenfeld #835 is NOT settled.")


if __name__ == "__main__":
    main()
