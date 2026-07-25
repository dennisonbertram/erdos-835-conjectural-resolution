#!/usr/bin/env python3
"""Exact verifier for the H-system counting identity.

For a leg A of S(r-1, r, 2r+1) and mates B, C (block-disjoint from A):
  H_X(P) = P u {w_X(P)}  (size r+1),  w_X(P) = gap of P u mate_X(P).

Claims verified here:
  (1) every (r+2)-set contains exactly one H_B(P);
  (2) C(2r+1, r+2) = b + (r-1) h + X(B,C),  h = |B ^ C|,
      X = #ordered pairs P != Q in A, |P ^ Q| = r-2,
          w_B(P) in Q minus P and w_C(Q) in P minus Q;
  (3) X = sum over (r-2)-sets R of #fix(c_R o b_R) in the link.
  (4) at r=3, test the canonical "other H-extension" involutions on
      X-configurations for a Klein-four action.

Families: r=3 (all mate pairs of a base Fano), r=5 (all 10296 pairs).
Run:  python3 verify_H_identity.py
"""
import sys
from itertools import combinations
from collections import Counter

sys.setrecursionlimit(100000)


def algox(X, Y, cap=None):
    solution, out = [], []

    def select(r_):
        cols = []
        for j in Y[r_]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    def deselect(r_, cols):
        for j in reversed(Y[r_]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

    def solve():
        if cap is not None and len(out) >= cap:
            return
        if not X:
            out.append(list(solution))
            return
        c = min(X, key=lambda c: len(X[c]))
        for r_ in sorted(X[c]):
            solution.append(r_)
            cols = select(r_)
            solve()
            deselect(r_, cols)
            solution.pop()

    solve()
    return out


def cover_instance(v, t, blocks):
    Y = {b: [("t", s) for s in combinations(b, t)] for b in blocks}
    X = {}
    for r_, cs in Y.items():
        for c in cs:
            X.setdefault(c, set()).add(r_)
    return X, Y


def wmap(A, M, v):
    Mset = set(map(tuple, M))
    w = {}
    for P in A:
        Pc = set(range(v)) - set(P)
        for x in Pc:
            if tuple(sorted(Pc - {x})) in Mset:
                w[P] = x
                break
        assert P in w
    return w


def x_configurations(A, wB, wC, r):
    """Return the X-configurations keyed by their (r+2)-set Y.

    The key is Y=P union Q.  H_B(P) and H_C(Q) are the unique H-sets
    they contain, so at most one X-configuration can have a given Y.
    """

    configurations = {}
    for P in A:
        Ps = set(P)
        for Q in A:
            if P == Q:
                continue
            Qs = set(Q)
            if len(Ps & Qs) != r - 2:
                continue
            if wB[P] not in Qs - Ps or wC[Q] not in Ps - Qs:
                continue
            Y = tuple(sorted(Ps | Qs))
            assert len(Y) == r + 2
            assert Y not in configurations
            configurations[Y] = (P, Q)
    return configurations


def verify_r3_klein(A, ws):
    """Test the only canonical fibre involutions available at r=3.

    For fixed P with wB(P) != wC(P), exactly r-1 X-configurations have
    first base P: they are the extensions of H_B(P) other than the
    same-base extension by wC(P).  At r=3 this fibre has size two, so
    "take the other extension" is a canonical fixed-point-free
    involution tau_B.  Define tau_C analogously by holding the second
    base Q fixed.  A canonical Klein-four proof would require tau_B and
    tau_C to commute.
    """

    checked = 0
    commute_count = 0
    orbit_sizes = Counter()
    product_cycle_types = Counter()
    generated_orbit_types = Counter()
    first_failure = None

    for wi, wB in enumerate(ws):
        for wj, wC in enumerate(ws):
            if wi == wj:
                continue
            configs = x_configurations(A, wB, wC, 3)
            assert len(configs) == 12

            by_first = {}
            by_second = {}
            for Y, (P, Q) in configs.items():
                by_first.setdefault(P, []).append(Y)
                by_second.setdefault(Q, []).append(Y)

            # Only disagreement bases occur, and every active fibre has
            # exactly r-1=2 configurations.
            disagreement = {P for P in A if wB[P] != wC[P]}
            assert set(by_first) == disagreement
            assert set(by_second) == disagreement
            assert all(len(fibre) == 2 for fibre in by_first.values())
            assert all(len(fibre) == 2 for fibre in by_second.values())

            tauB = {}
            tauC = {}
            for fibre in by_first.values():
                left, right = fibre
                tauB[left], tauB[right] = right, left
            for fibre in by_second.values():
                left, right = fibre
                tauC[left], tauC[right] = right, left

            assert all(tauB[tauB[Y]] == Y and tauB[Y] != Y for Y in configs)
            assert all(tauC[tauC[Y]] == Y and tauC[Y] != Y for Y in configs)

            commutes = all(
                tauB[tauC[Y]] == tauC[tauB[Y]] for Y in configs
            )

            product = {Y: tauB[tauC[Y]] for Y in configs}
            unseen_product = set(configs)
            cycle_lengths = []
            while unseen_product:
                seed = min(unseen_product)
                cycle = []
                current = seed
                while current not in cycle:
                    cycle.append(current)
                    unseen_product.discard(current)
                    current = product[current]
                assert current == seed
                cycle_lengths.append(len(cycle))
            product_cycle_types[tuple(sorted(cycle_lengths))] += 1

            unseen_group = set(configs)
            group_orbits = []
            while unseen_group:
                orbit = {min(unseen_group)}
                frontier = list(orbit)
                while frontier:
                    current = frontier.pop()
                    for image in (tauB[current], tauC[current]):
                        if image not in orbit:
                            orbit.add(image)
                            frontier.append(image)
                group_orbits.append(len(orbit))
                unseen_group -= orbit
            generated_orbit_types[tuple(sorted(group_orbits))] += 1

            checked += 1
            if commutes:
                commute_count += 1
                unseen = set(configs)
                while unseen:
                    seed = min(unseen)
                    orbit = {
                        seed,
                        tauB[seed],
                        tauC[seed],
                        tauB[tauC[seed]],
                    }
                    orbit_sizes[len(orbit)] += 1
                    unseen -= orbit
            elif first_failure is None:
                witness = next(
                    Y
                    for Y in configs
                    if tauB[tauC[Y]] != tauC[tauB[Y]]
                )
                first_failure = {
                    "mate_indices": (wi, wj),
                    "Y": witness,
                    "tauB_tauC": tauB[tauC[witness]],
                    "tauC_tauB": tauC[tauB[witness]],
                }

    print(
        "    (4) canonical r=3 fibre involutions: "
        f"{commute_count}/{checked} ordered mate pairs commute; "
        f"Klein orbit sizes {dict(orbit_sizes)}"
    )
    print(
        "        product cycle types: "
        f"{dict(product_cycle_types)}; generated-group orbit types: "
        f"{dict(generated_orbit_types)}"
    )
    if first_failure is not None:
        print(f"        first noncommuting witness: {first_failure}")
    return {
        "checked": checked,
        "commute_count": commute_count,
        "orbit_sizes": dict(orbit_sizes),
        "product_cycle_types": dict(product_cycle_types),
        "generated_orbit_types": dict(generated_orbit_types),
        "first_failure": first_failure,
    }


def verify_family(v, r):
    t = r - 1
    blocks = list(combinations(range(v), r))
    X0, Y0 = cover_instance(v, t, blocks)
    A = algox(X0, Y0, cap=1)[0]
    b = len(A)
    rest = [x for x in blocks if x not in set(A)]
    X1, Y1 = cover_instance(v, t, rest)
    mates = algox(X1, Y1, cap=None)
    ws = [wmap(A, M, v) for M in mates]
    print(f"[r={r}] b={b}, mates={len(mates)}")

    # (1) exactly-one H-covering, for a few mates
    for w in ws[:3]:
        Hs = [tuple(sorted(set(P) | {w[P]})) for P in A]
        cover = Counter()
        for Yset in combinations(range(v), r + 2):
            Ys = set(Yset)
            k = sum(1 for H in Hs if set(H) <= Ys)
            cover[k] += 1
        assert set(cover) == {1}, cover
    print(f"    (1) exactly-one H-covering: OK (3 mates, all "
          f"{sum(cover.values())} (r+2)-sets)")

    # precompute r-2 intersecting ordered pairs of A
    pairs = [(P, Q) for P in A for Q in A
             if P != Q and len(set(P) & set(Q)) == r - 2]

    lhs = 0
    from math import comb
    lhs = comb(v, r + 2)
    ok = 0
    Xvals = Counter()
    for wi in range(len(ws)):
        for wj in range(len(ws)):
            if wi == wj:
                continue
            wB, wC = ws[wi], ws[wj]
            h = sum(1 for P in A if wB[P] == wC[P])
            Xcnt = 0
            for P, Q in pairs:
                if wB[P] in set(Q) - set(P) and wC[Q] in set(P) - set(Q):
                    Xcnt += 1
            assert lhs == b + (r - 1) * h + Xcnt, (h, Xcnt)
            # fibre lemma: every disagreement base carries exactly r-1
            # X-configurations, so X = (r-1)(b-h) identically
            assert Xcnt == (r - 1) * (b - h), (h, Xcnt)
            ok += 1
            Xvals[(h, Xcnt)] += 1
    print(f"    (2) identity C({v},{r+2}) = b + (r-1)h + X: OK on {ok} "
          f"ordered mate pairs; (h, X) values: {dict(Xvals)}")

    # (3) link decomposition, one mate pair
    wB, wC = ws[0], ws[1]
    Xlink = 0
    for R in combinations(range(v), r - 2):
        Rs = set(R)
        link_blocks = [P for P in A if Rs <= set(P)]
        edges = [tuple(sorted(set(P) - Rs)) for P in link_blocks]
        epb = {}
        for P, e in zip(link_blocks, edges):
            epb[e] = P
        pt2e = {}
        for e in edges:
            for x in e:
                pt2e[x] = e
        for e in edges:
            P = epb[e]
            eB = pt2e.get(wB[P])
            if eB is None or eB == e:
                continue
            Q = epb[eB]
            if wC[Q] in e:
                Xlink += 1
    h = sum(1 for P in A if wB[P] == wC[P])
    assert Xlink == lhs - b - (r - 1) * h
    print(f"    (3) link decomposition X = sum #fix(c_R o b_R): OK "
          f"(X = {Xlink})")

    if r == 3:
        verify_r3_klein(A, ws)


if __name__ == "__main__":
    verify_family(7, 3)
    verify_family(11, 5)
