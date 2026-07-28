#!/usr/bin/env python3
"""Search drivers for class-B first-lift counterexamples.

A search driver produces candidates only.  Nothing printed here is evidence
by itself: every UNSAT verdict is re-decided by two independent complete
solvers in verify_classB.py, and every SAT witness is re-checked from the
definition.  Node budgets are used to *steer* the search, never as evidence.

Usage:
  python3 search.py random   SEED N_INSTANCES
  python3 search.py anneal   SEED N_RESTARTS STEPS
  python3 search.py twins    SEED                 (exhaustive, see below)
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter

from classb import (check_class_B, cut_certificates, mvec, m_profiles,
                    profile, random_class_B, random_move, solve_dfs,
                    solve_sat, supports, check_completion)

N, Q = 13, 17
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certificates")


def report(tag, forb):
    """Store a candidate infeasible instance."""
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "candidate_%s_%d.json" % (tag, int(time.time() * 1000) % 10**9))
    json.dump({"n": N, "q": Q, "forb": forb}, open(path, "w"))
    print("!!! CANDIDATE INFEASIBLE INSTANCE written to", path, flush=True)
    return path


# ---------------------------------------------------------------------------
# hardness proxy: failure rate of randomised greedy-with-propagation
# ---------------------------------------------------------------------------
def greedy_once(n, q, forb, rng):
    """One randomised most-constrained-first greedy pass with full unit
    propagation and NO backtracking.  Returns True on success."""
    FULL = (1 << q) - 1
    avail = [FULL & ~forb[a] for a in range(n)]
    open_ = [((1 << n) - 1) ^ (1 << a) for a in range(n)]
    left = n * (n - 1) // 2
    while left:
        best = None
        forced = []
        for a in range(n):
            om = open_[a]
            while om:
                lb = om & -om
                om ^= lb
                b = lb.bit_length() - 1
                if b < a:
                    continue
                m = avail[a] & avail[b]
                if m == 0:
                    return False
                cnt = bin(m).count("1")
                if cnt == 1:
                    forced.append((a, b, m.bit_length() - 1))
                elif best is None or cnt < best[0]:
                    best = (cnt, a, b, m)
        for a in range(n):
            m = avail[a]
            while m:
                lb = m & -m
                m ^= lb
                c = lb.bit_length() - 1
                cand = 0
                om = open_[a]
                while om:
                    l2 = om & -om
                    om ^= l2
                    b = l2.bit_length() - 1
                    if (avail[b] >> c) & 1:
                        cand |= l2
                if cand == 0:
                    return False
                cnt = bin(cand).count("1")
                if cnt == 1:
                    forced.append((a, cand.bit_length() - 1, c))
                elif best is None or cnt < best[0]:
                    best = (cnt, a, c, cand, 'v')
        if forced:
            for (a, b, c) in forced:
                if not ((open_[a] >> b) & 1):
                    continue
                if not ((avail[a] >> c) & 1) or not ((avail[b] >> c) & 1):
                    return False
                lb = 1 << c
                avail[a] ^= lb
                avail[b] ^= lb
                open_[a] &= ~(1 << b)
                open_[b] &= ~(1 << a)
                left -= 1
            continue
        if best is None:
            return left == 0
        if len(best) == 4:
            _, a, b, m = best
            bits = [i for i in range(q) if (m >> i) & 1]
            c = rng.choice(bits)
        else:
            _, a, c, cand, _ = best
            bs = [i for i in range(n) if (cand >> i) & 1]
            b = rng.choice(bs)
        lb = 1 << c
        avail[a] ^= lb
        avail[b] ^= lb
        open_[a] &= ~(1 << b)
        open_[b] &= ~(1 << a)
        left -= 1
    return True


def hardness(n, q, forb, rng, trials=24):
    """Number of failed randomised greedy passes out of `trials`."""
    return sum(0 if greedy_once(n, q, forb, rng) else 1 for _ in range(trials))


# ---------------------------------------------------------------------------
def run_random(seed, count):
    rng = random.Random(seed)
    stats = Counter()
    t0 = time.time()
    done = 0
    while done < count:
        prof = rng.choice(m_profiles(N))
        forb = random_class_B(N, Q, rng, prof)
        if forb is None:
            continue
        for _ in range(rng.randrange(0, 600)):
            nf = random_move(N, Q, forb, rng)
            if nf:
                forb = nf
        try:
            check_class_B(N, Q, forb)
        except AssertionError:
            continue
        done += 1
        stats[profile(N, Q, forb)] += 1
        st, sols, nodes = solve_dfs(N, Q, forb, node_budget=5_000_000)
        stats[st] += 1
        if st == "UNSAT":
            report("random", forb)
        elif st == "BUDGET":
            report("budget", forb)
        elif st == "SAT":
            check_completion(N, Q, forb, sols[0])
    print("seed=%d random: %d instances  %s  %.1fs"
          % (seed, count, dict(stats), time.time() - t0), flush=True)
    return stats


def run_anneal(seed, restarts, steps):
    rng = random.Random(seed)
    best_overall = (-1, None)
    stats = Counter()
    for r in range(restarts):
        prof = rng.choice(m_profiles(N))
        forb = random_class_B(N, Q, rng, prof)
        if forb is None:
            continue
        cur = hardness(N, Q, forb, rng)
        T0, T1 = 4.0, 0.15
        for s in range(steps):
            T = T0 * (T1 / T0) ** (s / max(1, steps - 1))
            nf = random_move(N, Q, forb, rng)
            if nf is None:
                continue
            try:
                check_class_B(N, Q, nf)
            except AssertionError:
                continue
            h = hardness(N, Q, nf, rng)
            if h >= cur or rng.random() < pow(2.718281828, (h - cur) / T):
                forb, cur = nf, h
            if cur >= 24:
                st, sols, nodes = solve_dfs(N, Q, forb, node_budget=20_000_000)
                stats[st] += 1
                if st == "UNSAT":
                    report("anneal", forb)
                    return stats
                if st == "BUDGET":
                    report("budget", forb)
                if st == "SAT":
                    check_completion(N, Q, forb, sols[0])
            if cur > best_overall[0]:
                best_overall = (cur, list(forb))
        stats["restart"] += 1
        stats["best%d" % cur] += 1
    print("seed=%d anneal: best hardness %d/24  %s"
          % (seed, best_overall[0], dict(stats)), flush=True)
    if best_overall[1]:
        st, sols, nodes = solve_dfs(N, Q, best_overall[1], node_budget=50_000_000)
        print("   hardest instance verdict:", st, nodes, flush=True)
        if st == "UNSAT":
            report("anneal_best", best_overall[1])
    return stats


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "random":
        run_random(int(sys.argv[2]), int(sys.argv[3]))
    elif mode == "anneal":
        run_anneal(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else:
        raise SystemExit("unknown mode " + mode)
