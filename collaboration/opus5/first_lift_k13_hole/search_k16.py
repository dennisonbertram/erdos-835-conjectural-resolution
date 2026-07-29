#!/usr/bin/env python3
"""Search for a class-B' instance at k=16 (n=13, q=17) with no completion.

This is a SEARCH driver.  Nothing it prints is a proof of anything except the
literal counts it reports.  A negative result here is evidence, not a theorem.

Three strategies:
  random      uniform-ish over the 332 link partitions of E(K_5) and over the
              admissible 13x5 arrays;
  structured  the exact analogue of the closed-form n=11 counterexample:
              A = X (8) + Y (5) with every vertex of Y forbidding the same
              five colours, so five colours have V_c = X exactly;
  climb       hill-climbing on the exact solver's node count, i.e. towards
              the most constrained instances reachable by single-column
              transpositions inside class B';
  classb      the strictly larger class B: the five missed-colour four-sets
              D_x are arbitrary subject only to every colour lying in an even
              number of them, so no proper colouring L of the ten triples of P
              need exist.

Usage: python3 -B search_k16.py <mode> <trials> <seed>
"""

from __future__ import annotations

import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

from first_lift import (
    Dx_from_parts,
    array_from_Dx,
    check_class_Bprime,
    check_completion,
    check_instance_shape,
    cut_certificates,
    in_class_B,
    link_partitions,
    perfect_matching,
    random_class_Bprime,
    solve,
    solve_randomised,
    supports,
)

N, Q = 13, 17
HERE = Path(__file__).resolve().parent


def forb_from_arr(n, arr):
    forb = [0] * n
    for a in range(n):
        for c in arr[a]:
            forb[a] |= 1 << c
    return forb


def structured(rng, pool, tries=200):
    """A = X(8) + Y(5); all of Y forbids the same five colours CC."""
    X = list(range(8))
    Y = list(range(8, 13))
    CC = list(range(5))
    NON = list(range(5, Q))
    for _ in range(tries):
        parts = rng.choice(pool)
        colours = rng.sample(NON, len(parts))
        Dx, _ = Dx_from_parts(parts, colours)
        if any(set(d) & set(CC) for d in Dx):
            continue
        arr = [[None] * 5 for _ in range(N)]
        perm = rng.sample(range(5), 5)
        for x in range(5):
            for i in range(5):
                arr[Y[i]][x] = CC[perm[(i - x) % 5]]
        used = [0] * N
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
        if not good:
            continue
        forb = forb_from_arr(N, arr)
        if any(bin(f).count("1") != 5 for f in forb):
            continue
        try:
            check_instance_shape(N, Q, forb)
            check_class_Bprime(N, Q, forb, arr, parts, colours)
        except AssertionError:
            continue
        return dict(forb=forb, arr=arr, parts=parts, colours=colours)
    return None


def random_class_B(rng, tries=200):
    """Class B only: any five 4-sets D_x with every colour in an even number
    of them.  Equivalently row sums 5 and all column sums odd and <= 5, with
    NO demand that the D_x come from a proper colouring of the ten triples."""
    for _ in range(tries):
        n4 = rng.randint(0, 5)
        n2 = (20 - 4 * n4) // 2
        if n2 < 0 or n4 + n2 > Q:
            continue
        cols = list(range(Q))
        rng.shuffle(cols)
        Dx = [set() for _ in range(5)]
        for i in range(n4):
            for x in rng.sample(range(5), 4):
                Dx[x].add(cols[i])
        for i in range(n4, n4 + n2):
            for x in rng.sample(range(5), 2):
                Dx[x].add(cols[i])
        if any(len(d) != 4 for d in Dx):
            continue
        got = array_from_Dx(N, Q, [frozenset(d) for d in Dx], rng)
        if got is None:
            continue
        forb, arr = got
        if any(bin(f).count("1") != 5 for f in forb):
            continue
        try:
            check_instance_shape(N, Q, forb)
        except AssertionError:
            continue
        if not in_class_B(N, Q, forb):
            continue
        return dict(forb=forb, arr=arr, parts=[], colours=[])
    return None


def neighbours(inst, rng):
    """Swap two rows inside one column; stays a bijection onto C \\ D_x.
    Keeps class B' iff both rows keep five distinct entries."""
    arr = [row[:] for row in inst["arr"]]
    x = rng.randrange(5)
    a, b = rng.sample(range(N), 2)
    arr[a][x], arr[b][x] = arr[b][x], arr[a][x]
    if len(set(arr[a])) != 5 or len(set(arr[b])) != 5:
        return None
    forb = forb_from_arr(N, arr)
    out = dict(inst)
    out["arr"] = arr
    out["forb"] = forb
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "random"
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = random.Random(seed)
    pool = [p for p in link_partitions() if len(p) <= Q]

    stats = Counter()
    hist = Counter()
    worst_nodes = 0
    worst_inst = None
    t0 = time.time()
    tested = 0

    def test(inst):
        nonlocal worst_nodes, worst_inst, tested
        forb = inst["forb"]
        check_instance_shape(N, Q, forb)
        assert in_class_B(N, Q, forb)
        if mode == "structured":
            # these are highly symmetric and satisfiable-but-hard for the
            # deterministic value ordering; try randomised restarts first,
            # whose verdict is equally exhaustive when a restart finishes
            st, sol, _ = solve_randomised(N, Q, forb, seed=seed, cutoff=20_000)
            nodes = 0
            if st == "RESTARTS_EXHAUSTED":
                st, sol, nodes = solve(N, Q, forb, node_budget=5_000_000)
        else:
            st, sol, nodes = solve(N, Q, forb, node_budget=2_000_000)
        if st == "BUDGET":
            # deterministic value ordering can stall on satisfiable instances;
            # retry with randomised restarts before recording anything
            st2, sol2, _ = solve_randomised(N, Q, forb, seed=seed)
            stats["budget_then_" + st2] += 1
            if st2 == "SAT":
                st, sol = "SAT", sol2
            else:
                st = st2
        tested += 1
        stats[st] += 1
        hist[tuple(sorted(Counter(supports(N, Q, forb)).items()))] += 1
        if nodes > worst_nodes:
            worst_nodes, worst_inst = nodes, inst
        if tested % 2000 == 0:
            print(
                "  ... %d tested, %s, max nodes %d, %.1fs"
                % (tested, dict(stats), worst_nodes, time.time() - t0),
                flush=True,
            )
        if st == "SAT":
            assert check_completion(N, Q, forb, sol)
        else:
            cc = cut_certificates(N, Q, forb)
            print("NON-SAT at k=16:", st, "cuts:", cc[:2], "forb:", forb, flush=True)
            (HERE / "certificates").mkdir(exist_ok=True)
            (HERE / "certificates" / ("k16_non_sat_%d.json" % seed)).write_text(
                json.dumps(
                    {
                        "n": N,
                        "q": Q,
                        "forb": forb,
                        "arr": inst["arr"],
                        "parts": [list(map(list, p)) for p in inst["parts"]],
                        "colours": list(inst["colours"]),
                        "status": st,
                    },
                    indent=1,
                )
                + "\n"
            )
        return st, nodes

    if mode == "random":
        while tested < trials:
            inst = random_class_Bprime(N, Q, rng, pool)
            if inst is None:
                stats["genfail"] += 1
                continue
            test(inst)
    elif mode == "structured":
        while tested < trials:
            inst = structured(rng, pool)
            if inst is None:
                stats["genfail"] += 1
                continue
            test(inst)
    elif mode == "classb":
        while tested < trials:
            inst = random_class_B(rng)
            if inst is None:
                stats["genfail"] += 1
                continue
            test(inst)
    elif mode == "climb":
        cur = None
        while cur is None:
            cur = random_class_Bprime(N, Q, rng, pool)
        _, curnodes = test(cur)
        stalls = 0
        while tested < trials:
            nb = neighbours(cur, rng)
            if nb is None:
                continue
            st, nodes = test(nb)
            if nodes >= curnodes:
                cur, curnodes = nb, nodes
                stalls = 0
            else:
                stalls += 1
                if stalls > 400:
                    cur = None
                    while cur is None:
                        cur = random_class_Bprime(N, Q, rng, pool)
                    _, curnodes = test(cur)
                    stalls = 0
    else:
        raise SystemExit("unknown mode %r" % mode)

    print(
        "mode=%s trials=%d seed=%d tested=%d %s"
        % (mode, trials, seed, tested, dict(stats))
    )
    print("  support histograms observed (|V_c| multiset -> count):")
    for k, v in sorted(hist.items()):
        print("   ", k, v)
    print("  max solver nodes: %d   elapsed %.1fs" % (worst_nodes, time.time() - t0))


if __name__ == "__main__":
    main()
