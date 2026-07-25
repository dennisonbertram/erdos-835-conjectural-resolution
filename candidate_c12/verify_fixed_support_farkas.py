#!/usr/bin/env python3
"""Exact solver-free verifier for fixed-support C(12,6,4) Farkas proofs.

Given one of the two A=45 z1/z3 relaxation witnesses and its named rational
certificate, verify:

  c_B = sum_{Q subset B} w_Q >= 0  for every 6-subset B,
  sum_Q (1 + z_Q) w_Q < 0.

If nonnegative block variables x_B had the prescribed quadruple degrees, then
the left identity summed over B would be both nonnegative and equal to the
negative second quantity, a contradiction.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


V = tuple(range(12))
QUADS = tuple(itertools.combinations(V, 4))
BLOCKS = tuple(itertools.combinations(V, 6))


# Each entry is representative, expected orbit size, expected quadruple
# degree, exact weight.  Unlisted quadruple orbits receive weight zero.
CERTIFICATES = {
    "split": {
        "automorphisms": 32,
        "rhs": Fraction(-24),
        "weights": (
            ((0, 1, 2, 8), 32, 1, Fraction(1, 8)),
            ((0, 1, 2, 10), 32, 2, Fraction(-1, 8)),
            ((0, 1, 6, 7), 4, 2, Fraction(1, 2)),
            ((0, 1, 6, 8), 16, 1, Fraction(-1, 2)),
            ((0, 1, 6, 9), 16, 1, Fraction(7, 8)),
            ((0, 1, 6, 10), 8, 1, Fraction(-1, 4)),
            ((0, 1, 6, 11), 8, 1, Fraction(-1, 8)),
            ((0, 1, 8, 9), 2, 4, Fraction(-1)),
            ((0, 2, 3, 4), 32, 1, Fraction(1, 8)),
            ((0, 2, 3, 6), 8, 1, Fraction(3, 8)),
            ((0, 2, 3, 7), 8, 1, Fraction(-5, 8)),
            ((0, 2, 3, 10), 8, 2, Fraction(5, 8)),
            ((0, 2, 3, 11), 8, 2, Fraction(-3, 8)),
            ((0, 2, 4, 6), 16, 1, Fraction(1, 2)),
            ((0, 2, 4, 8), 8, 4, Fraction(-1)),
            ((0, 2, 5, 6), 16, 1, Fraction(-1, 2)),
            ((0, 2, 5, 8), 8, 1, Fraction(1)),
            ((0, 2, 6, 8), 32, 1, Fraction(1, 16)),
            ((0, 2, 6, 9), 32, 1, Fraction(-1, 8)),
            ((0, 2, 7, 8), 32, 1, Fraction(1, 8)),
            ((0, 2, 7, 9), 32, 1, Fraction(3, 8)),
            ((0, 6, 8, 10), 8, 1, Fraction(1)),
            ((0, 6, 8, 11), 2, 1, Fraction(-1, 2)),
            ((0, 6, 9, 10), 4, 4, Fraction(-1)),
            ((0, 7, 8, 10), 2, 1, Fraction(-1)),
            ((2, 3, 4, 5), 1, 4, Fraction(-1)),
        ),
    },
    "collapsed": {
        "automorphisms": 192,
        "rhs": Fraction(-16),
        "weights": (
            ((0, 1, 2, 3), 12, 2, Fraction(-1, 9)),
            ((0, 1, 2, 4), 96, 1, Fraction(7, 72)),
            ((0, 1, 2, 6), 48, 2, Fraction(1, 36)),
            ((0, 1, 2, 8), 24, 1, Fraction(1, 9)),
            ((0, 1, 2, 9), 24, 1, Fraction(1, 9)),
            ((0, 1, 2, 10), 48, 1, Fraction(1, 36)),
            ((0, 1, 4, 5), 3, 4, Fraction(-1)),
            ((0, 2, 4, 6), 192, 1, Fraction(1, 12)),
            ((0, 2, 4, 8), 24, 1, Fraction(1)),
            ((0, 2, 4, 9), 12, 4, Fraction(-1)),
            ((0, 2, 5, 8), 12, 1, Fraction(-1)),
        ),
    },
}


def matching_group():
    for pair_perm in itertools.permutations(range(6)):
        for flips in itertools.product(range(2), repeat=6):
            perm = [0] * 12
            for old_pair in range(6):
                new_pair = pair_perm[old_pair]
                for old_side in range(2):
                    perm[2 * old_pair + old_side] = (
                        2 * new_pair + (old_side ^ flips[old_pair])
                    )
            yield tuple(perm)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=sorted(CERTIFICATES))
    ap.add_argument("witness", type=Path)
    args = ap.parse_args()

    data = json.loads(args.witness.read_text())
    z = {
        tuple(item["quad"]): int(item["value"])
        for item in data["defect"]
    }
    degree = {q: 1 + z.get(q, 0) for q in QUADS}
    assert Counter(z.values()) == {1: 60, 3: 15}

    automorphisms = []
    for perm in matching_group():
        image = {
            tuple(sorted(perm[v] for v in q)): value
            for q, value in z.items()
        }
        if image == z:
            automorphisms.append(perm)

    certificate = CERTIFICATES[args.kind]
    assert len(automorphisms) == certificate["automorphisms"]
    weights = {q: Fraction(0) for q in QUADS}
    weighted = set()
    for rep, expected_size, expected_degree, value in certificate["weights"]:
        orbit = {
            tuple(sorted(perm[v] for v in rep))
            for perm in automorphisms
        }
        assert len(orbit) == expected_size
        assert all(degree[q] == expected_degree for q in orbit)
        assert not (weighted & orbit)
        weighted.update(orbit)
        for q in orbit:
            weights[q] = value

    coefficient_histogram = Counter()
    for block in BLOCKS:
        bs = set(block)
        coefficient = sum(
            weights[q] for q in QUADS if set(q) <= bs
        )
        assert coefficient >= 0
        coefficient_histogram[coefficient] += 1

    rhs = sum(degree[q] * weights[q] for q in QUADS)
    assert rhs == certificate["rhs"]
    print("VERIFIED", args.kind)
    print("automorphisms", len(automorphisms))
    print("weighted_quads", len(weighted))
    print("block_coefficient_histogram")
    for value, count in sorted(coefficient_histogram.items()):
        print(value, count)
    print("degree_weighted_rhs", rhs)
    print("CONTRADICTION: nonnegative block sum equals negative rhs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
