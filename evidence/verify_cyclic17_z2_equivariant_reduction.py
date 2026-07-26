#!/usr/bin/env python3
"""Verifier for Section 6 of `cyclic_layer_recursion_prime_census.md`:
the Z_2-equivariant reduction of the fixed-golf cyclic-17 radius-five boundary.

Stdlib only; no solver.  This file checks that the reduction is WELL DEFINED
and computes its exact size.  It does NOT search for a witness and makes no
feasibility claim -- see `search_cyclic17_z2_equivariant_radius5.py` for that.

Nothing here bears on Erdos-Rosenfeld #835, which remains open.

Run:  python3 -B evidence/verify_cyclic17_z2_equivariant_reduction.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from itertools import combinations

P = 17
HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(HERE, "cyclic17_symmetric_golf_design.json")


# ------------------------------------------------------------------ layer 1

def diff_class(e):
    x, y = tuple(e)
    d = (x - y) % P
    return min(d, P - d)


def load_design():
    with open(CERT, "rb") as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw.decode())
    assert data["prime"] == P
    design = tuple(frozenset(frozenset(e) for e in st) for st in data["starters"])
    return design, sha


def check_golf_design(design):
    assert len(design) == 15
    seen = set()
    for m in design:
        assert len(m) == 8
        assert sorted(x for e in m for x in e) == list(range(1, P))
        assert sorted(diff_class(e) for e in m) == list(range(1, 9))
        assert not (seen & m), "starters must be pairwise disjoint"
        seen |= set(m)
    assert len(seen) == 120, "must partition E(K_16)"
    return True


def multiplier_group(design):
    S = frozenset(design)
    return [m for m in range(1, P)
            if frozenset(frozenset(frozenset((m * x) % P for x in e) for e in st)
                         for st in design) == S]


# ------------------------------------------------------------------ layer 2

def triple_orbits():
    seen, reps = set(), []
    for t in combinations(range(P), 3):
        s = frozenset(t)
        if s in seen:
            continue
        for sh in range(P):
            seen.add(frozenset((v + sh) % P for v in s))
        reps.append(tuple(sorted(s)))
    return reps


def layer2_data(design, reps):
    owner = {}
    for i, m in enumerate(design):
        for e in m:
            owner[e] = i
    F = [[set() for _ in reps] for _ in range(15)]
    for q, T in enumerate(reps):
        for s in range(P):
            sh = tuple((v + s) % P for v in T)
            for e in (frozenset(x) for x in combinations(sh, 2)):
                if 0 not in e:
                    F[owner[e]][q].add(s)
    return F


def sigma_tau(design, reps):
    neg_st = lambda st: frozenset(frozenset((-x) % P for x in e) for e in st)
    idx = {st: i for i, st in enumerate(design)}
    sigma = [idx[neg_st(design[i])] for i in range(15)]
    rid = {}
    for q, T in enumerate(reps):
        for s in range(P):
            rid[frozenset((v + s) % P for v in T)] = (q, s)
    tau, a = [], []
    for q, T in enumerate(reps):
        q2, s = rid[frozenset((-v) % P for v in T)]
        tau.append(q2)
        a.append(s)
    return sigma, tau, a


# ------------------------------------------------------------------ checks

def main():
    design, sha = load_design()
    print("=" * 72)
    print("Z_2-equivariant reduction of the cyclic-17 radius-five boundary")
    print("=" * 72)
    print(f"  certificate  evidence/cyclic17_symmetric_golf_design.json")
    print(f"  SHA-256      {sha}")

    print("\n[1] the certificate is a golf design of Z_17 with multiplier {1,-1}")
    check_golf_design(design)
    mg = multiplier_group(design)
    assert mg == [1, 16], mg
    Pat = frozenset(frozenset((x, (-x) % P)) for x in range(1, 9))
    assert Pat in set(design) and design[0] == Pat
    print("    15 disjoint starters partitioning E(K_16): ok")
    print(f"    multiplier group = {mg}; patterned starter is member 0: ok")

    reps = triple_orbits()
    assert len(reps) == 40
    F = layer2_data(design, reps)
    assert all(len(F[i][q]) == 3 for i in range(15) for q in range(40))
    sigma, tau, a = sigma_tau(design, reps)

    print("\n[2] sigma and tau are involutions, and a_{tau q} = a_q")
    for i in range(15):
        assert sigma[sigma[i]] == i, i
    for q in range(40):
        assert tau[tau[q]] == q, q
        # -T_q = T_{tau q} + a_q; negating twice gives a_{tau q} = a_q, which is
        # exactly what makes Phi -> Phi' an involution rather than a 4-cycle.
        assert a[tau[q]] == a[q], (q, a[q], a[tau[q]])
    print("    sigma^2 = id on the 15 starters: ok")
    print("    tau^2 = id on the 40 triple orbits: ok")
    print("    a_{tau q} = a_q for all 40 orbits: ok")

    print("\n[3] cycle structure of sigma and tau")
    fix_s = [i for i in range(15) if sigma[i] == i]
    swaps = {frozenset((i, sigma[i])) for i in range(15) if sigma[i] != i}
    fix_t = [q for q in range(40) if tau[q] == q]
    assert fix_s == [0], fix_s
    assert len(swaps) == 7, len(swaps)
    assert len(fix_t) == 8, len(fix_t)
    print(f"    sigma: {len(fix_s)} fixed starter (the patterned one) "
          f"+ {len(swaps)} transpositions = 1 + 2*7 = 15: ok")
    print(f"    tau:   {len(fix_t)} fixed orbits of 40, "
          f"{(40 - len(fix_t)) // 2} transpositions: ok")

    print("\n[4] domain transport: the involution maps cell domains onto domains")
    dom = {}
    for (i, j) in combinations(range(15), 2):
        for q in range(40):
            dom[(i, j, q)] = frozenset(c for c in range(P)
                                       if c not in F[i][q] and c not in F[j][q])
    # s in F_i(q)  <=>  a_q - s in F_{sigma i}(tau q), because negating the
    # translate T_q + s gives T_{tau q} + (a_q - s) and negating M_i gives
    # M_{sigma i}.  Checked exhaustively here.
    for i in range(15):
        for q in range(40):
            got = {(a[q] - s) % P for s in F[i][q]}
            assert got == F[sigma[i]][tau[q]], (i, q)
    checked = 0
    for (i, j) in combinations(range(15), 2):
        si, sj = sorted((sigma[i], sigma[j]))
        for q in range(40):
            image = frozenset((a[q] - c) % P for c in dom[(i, j, q)])
            assert image == dom[(si, sj, tau[q])], (i, j, q)
            checked += 1
    assert checked == 4200
    print(f"    F_i(q) transports for all 15*40 = 600 pairs (i,q): ok")
    print(f"    domain of every one of the {checked} cells maps onto the "
          "domain of its image: ok")

    print("\n[5] cells fixed by the involution, and the forced values")
    fixed_cells = []
    for (i, j) in combinations(range(15), 2):
        if sorted((sigma[i], sigma[j])) != [i, j]:
            continue
        for q in fix_t:
            fixed_cells.append((i, j, q))
    # a sigma-fixed pair is {i, sigma i} with sigma i != i; there are 7 of them
    fixed_pairs = {frozenset((i, j)) for (i, j, q) in fixed_cells}
    assert fixed_pairs == swaps, "sigma-fixed pairs are exactly the 7 transpositions"
    assert len(fixed_cells) == 7 * 8 == 56, len(fixed_cells)
    inv2 = pow(2, P - 2, P)
    bad = []
    for (i, j, q) in fixed_cells:
        forced = (a[q] * inv2) % P          # 2*Phi = a_q  =>  Phi = a_q / 2
        if forced not in dom[(i, j, q)]:
            bad.append((i, j, q, forced))
    print(f"    sigma-fixed pairs = {len(fixed_pairs)}, tau-fixed orbits = "
          f"{len(fix_t)}  ->  {len(fixed_cells)} forced cells")
    print(f"    forced value a_q/2 outside its own domain: {len(bad)} cells")
    assert not bad, bad
    print("    => the reduction does not self-destruct on its fixed cells")

    print("\n[6] exact size of the reduced model")
    orbits = set()
    for (i, j) in combinations(range(15), 2):
        si, sj = sorted((sigma[i], sigma[j]))
        for q in range(40):
            orbits.add(frozenset({(i, j, q), (si, sj, tau[q])}))
    free2 = sum(1 for o in orbits if len(o) == 2)
    fixed1 = sum(1 for o in orbits if len(o) == 1)
    assert fixed1 == 56 and free2 == (4200 - 56) // 2
    assert fixed1 + 2 * free2 == 4200
    print(f"    4200 phase cells  ->  {len(orbits)} involution orbits")
    print(f"      {fixed1} singleton orbits (phase forced to a_q/2)")
    print(f"      {free2} paired orbits (one free phase each)")
    print(f"    free phases after the reduction: {free2} of 4200 "
          f"({100.0 * free2 / 4200:.1f}%)")

    print("\nAll structural checks passed.")
    print("No feasibility claim is made here, and #835 remains OPEN.")


if __name__ == "__main__":
    main()
