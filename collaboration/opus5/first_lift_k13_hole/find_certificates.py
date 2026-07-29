#!/usr/bin/env python3
"""Search for class-B' counterexample certificates and write them to JSON.

This file is a SEARCH driver: nothing it prints is a claim.  Every certificate
it writes is re-checked from the definitions by
verify_first_lift_obstruction.py, which is the only file whose output is
quoted as evidence.

Usage:  python3 -B find_certificates.py [seed]
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

from first_lift import (
    Dx_from_parts,
    check_class_Bprime,
    check_instance_shape,
    counterexample_n11,
    cut_certificates,
    in_class_B,
    link_partitions,
    perfect_matching,
    random_class_Bprime,
    solve,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "certificates"


def targeted_r5(n, rng, tries=4000):
    """A = X (n-5) + Y (5); every vertex of Y forbids the same five colours.

    Then V_c = X for those five colours, each of which must be a perfect
    matching on X, forcing 5*(n-5)/2 edges inside X while only C(n-5,2) exist.
    This is a violation exactly when 5*(n-5)/2 > (n-5)(n-6)/2, i.e. n < 11.
    """
    q = n + 4
    X = list(range(n - 5))
    Y = list(range(n - 5, n))
    CC = list(range(5))
    NON = list(range(5, q))
    pool = [p for p in link_partitions() if len(p) <= len(NON)]
    for _ in range(tries):
        parts = rng.choice(pool)
        colours = rng.sample(NON, len(parts))
        Dx, _ = Dx_from_parts(parts, colours)
        if any(set(d) & set(CC) for d in Dx):
            continue  # CC must stay usable
        # Y block: a 5x5 Latin square on CC (fixed-point-free shift design)
        arr = [[None] * 5 for _ in range(n)]
        perm = rng.sample(range(5), 5)
        for x in range(5):
            for i in range(5):
                arr[Y[i]][x] = CC[perm[(i - x) % 5]]
        # X block: column x is a bijection X -> (NON \ D_x); rows distinct
        ok = False
        for _try in range(40):
            used = [0] * n
            order = list(range(5))
            rng.shuffle(order)
            good = True
            for x in order:
                cols = sorted(set(NON) - set(Dx[x]))
                if len(cols) != len(X):
                    good = False
                    break
                adj = [
                    [i for i, c in enumerate(cols) if not (used[X[j]] >> c & 1)]
                    for j in range(len(X))
                ]
                mm = perfect_matching(adj, len(X), len(cols), rng)
                if mm is None:
                    good = False
                    break
                for j in range(len(X)):
                    c = cols[mm[j]]
                    arr[X[j]][x] = c
                    used[X[j]] |= 1 << c
            if good:
                ok = True
                break
        if not ok:
            continue
        forb = [0] * n
        for a in range(n):
            for c in arr[a]:
                forb[a] |= 1 << c
        if any(bin(forb[a]).count("1") != 5 for a in range(n)):
            continue
        try:
            check_instance_shape(n, q, forb)
            check_class_Bprime(n, q, forb, arr, parts, colours)
        except AssertionError:
            continue
        if not in_class_B(n, q, forb):
            continue
        if not cut_certificates(n, q, forb, only_first=True):
            continue
        return dict(
            n=n,
            q=q,
            forb=forb,
            arr=arr,
            parts=[list(map(list, p)) for p in parts],
            colours=list(colours),
            construction="r5",
        )
    return None


def random_unsat(n, rng, tries=200000):
    """Any class-B' instance the exact solver proves has no completion."""
    q = n + 4
    pool = [p for p in link_partitions() if len(p) <= q]
    for _ in range(tries):
        inst = random_class_Bprime(n, q, rng, pool)
        if inst is None:
            continue
        st, _, _ = solve(n, q, inst["forb"], node_budget=2_000_000)
        if st == "UNSAT":
            return dict(
                n=n,
                q=q,
                forb=inst["forb"],
                arr=inst["arr"],
                parts=[list(map(list, p)) for p in inst["parts"]],
                colours=list(inst["colours"]),
                construction="random",
            )
    return None


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20260727
    rng = random.Random(seed)
    OUT.mkdir(exist_ok=True)
    found = {}

    n, q, forb, arr, parts, colours = counterexample_n11()
    found[11] = dict(
        n=n,
        q=q,
        forb=forb,
        arr=arr,
        parts=[list(map(list, p)) for p in parts],
        colours=list(colours),
        construction="closed-form n=11",
    )

    for n in (7, 9):
        c = targeted_r5(n, rng)
        if c is None:
            # At n=7 the r5 pattern is in class B but provably not in class B':
            # every non-CC colour would have to appear in 5-2t_c <= |X| = 2
            # columns, forcing t_c = 2 for all six of them and sum_c t_c = 12,
            # contradicting sum_c t_c = 10.  Fall back to random search.
            print("n=%d: targeted r5 search found nothing; falling back" % n)
            c = random_unsat(n, rng)
        if c is None:
            print("n=%d: no class-B' counterexample found" % n)
        else:
            found[n] = c

    c = random_unsat(5, rng)
    if c is None:
        print("n=5: random search found no UNSAT class-B' instance")
    else:
        found[5] = c

    for n, cert in sorted(found.items()):
        cert["seed"] = seed
        path = OUT / ("counterexample_n%02d.json" % n)
        path.write_text(json.dumps(cert, indent=1, sort_keys=True) + "\n")
        print(
            "wrote",
            path.name,
            "cuts:",
            len(cut_certificates(cert["n"], cert["q"], cert["forb"])),
        )


if __name__ == "__main__":
    main()
