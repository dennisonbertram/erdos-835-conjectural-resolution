#!/usr/bin/env python3
"""Independently verify stored slice solutions against the Wallis golf table.

Reads a binary family file (40 phase bytes per solution, phase convention of
the seed JSON: phase = (-shift) % 17) for slice {i,j} and checks a random
sample (or all) with logic replicated from
evidence/odd_graph_local_ball/verify_radius5_golf_cyclic_exact_slice_seed.py:
one translate per orbit, avoids both zero one-factors, covers the 120
residual edges exactly once, degree vector (8,7,...,7) after rotating so the
common fixed point of the two matchings is vertex 0.
"""

import argparse
import json
import random
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVIDENCE))
from global_latin_audit import construct_golf17  # noqa: E402

P = 17
POINTS = tuple(range(P))
MOVING_EDGES = tuple(combinations(POINTS, 2))


def translate(subset, amount):
    return tuple(sorted((v + amount) % P for v in subset))


def triple_representatives():
    answer = []
    unseen = set(combinations(POINTS, 3))
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, s) for s in POINTS)
        answer.append(representative)
        for s in POINTS:
            unseen.discard(translate(representative, s))
    assert len(answer) == 40
    return answer


REPS = triple_representatives()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("family", type=Path)
    parser.add_argument("i", type=int)
    parser.add_argument("j", type=int)
    parser.add_argument("--sample", type=int, default=100)
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()

    raw = args.family.read_bytes()
    assert len(raw) % 40 == 0
    total = len(raw) // 40
    solutions = [raw[k * 40:(k + 1) * 40] for k in range(total)]
    # Distinctness of the whole family while we have it in hand.
    assert len(set(solutions)) == total, "duplicate solutions in family"

    golf = construct_golf17()
    forbidden = {
        e for e in MOVING_EDGES
        if golf[args.i][e[0]][e[1]] == 0 or golf[args.j][e[0]][e[1]] == 0
    }
    assert len(forbidden) == 16
    residual = set(MOVING_EDGES) - forbidden

    rng = random.Random(args.seed)
    sample_size = min(args.sample, total)
    checked = rng.sample(range(total), sample_size)
    for index in checked:
        phases = solutions[index]
        assert all(0 <= p < P for p in phases)
        shifts = [(-p) % P for p in phases]
        counts = Counter()
        degrees = [0] * P
        for orbit, rep in enumerate(REPS):
            triple = translate(rep, shifts[orbit])
            for v in triple:
                degrees[v] += 1
            counts.update(combinations(triple, 2))
        assert set(counts) == residual, f"wrong residual support, sol {index}"
        assert all(counts[e] == 1 for e in residual), f"repeat edge, sol {index}"
        assert degrees == [8] + [7] * 16, f"wrong degrees, sol {index}"

    print(json.dumps({
        "status": "PASS",
        "family": str(args.family),
        "pair": [args.i, args.j],
        "family_size": total,
        "all_distinct": True,
        "sample_verified": sample_size,
    }))


if __name__ == "__main__":
    main()
