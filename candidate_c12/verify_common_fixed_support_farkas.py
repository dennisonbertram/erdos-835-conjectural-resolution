#!/usr/bin/env python3
"""Verify one rational Farkas weight that excludes both aligned supports."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from verify_fixed_support_farkas import (
    BLOCKS,
    CERTIFICATES,
    QUADS,
    matching_group,
)


# This matching-preserving permutation swaps point-pairs {4,5} and {8,9}.
ALIGN = (0, 1, 2, 3, 8, 9, 6, 7, 4, 5, 10, 11)


def transform(mapping, perm):
    return {
        tuple(sorted(perm[v] for v in q)): value
        for q, value in mapping.items()
    }


def load_degree(path: Path):
    data = json.loads(path.read_text())
    z = {
        tuple(item["quad"]): int(item["value"])
        for item in data["defect"]
    }
    return z, {q: 1 + z.get(q, 0) for q in QUADS}


def expand_weight(kind: str, z):
    automorphisms = []
    for perm in matching_group():
        if transform(z, perm) == z:
            automorphisms.append(perm)
    assert len(automorphisms) == CERTIFICATES[kind]["automorphisms"]
    weight = {q: Fraction(0) for q in QUADS}
    for rep, expected_size, expected_degree, value in CERTIFICATES[kind][
        "weights"
    ]:
        orbit = {
            tuple(sorted(perm[v] for v in rep))
            for perm in automorphisms
        }
        assert len(orbit) == expected_size
        assert all(1 + z.get(q, 0) == expected_degree for q in orbit)
        for q in orbit:
            weight[q] = value
    return weight


def block_histogram(weight):
    answer = Counter()
    for block in BLOCKS:
        bs = set(block)
        coefficient = sum(
            weight[q] for q in QUADS if set(q) <= bs
        )
        assert coefficient >= 0
        answer[coefficient] += 1
    return answer


def pairing(degree, weight):
    return sum(degree[q] * weight[q] for q in QUADS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("split", type=Path)
    ap.add_argument("collapsed", type=Path)
    args = ap.parse_args()

    split_z, split_degree = load_degree(args.split)
    collapsed_z, _ = load_degree(args.collapsed)
    collapsed_z = transform(collapsed_z, ALIGN)
    collapsed_degree = {
        q: 1 + collapsed_z.get(q, 0) for q in QUADS
    }

    split_weight = expand_weight("split", split_z)
    collapsed_weight = transform(
        expand_weight(
            "collapsed",
            transform(collapsed_z, ALIGN),
        ),
        ALIGN,
    )
    # ALIGN is an involution, so the inner transform restores the stored
    # collapsed representative, and the outer transform aligns its weight.
    common_weight = {
        q: split_weight[q] + collapsed_weight[q] for q in QUADS
    }

    assert pairing(split_degree, split_weight) == -24
    assert pairing(split_degree, collapsed_weight) == 8
    assert pairing(collapsed_degree, split_weight) == 0
    assert pairing(collapsed_degree, collapsed_weight) == -16
    assert pairing(split_degree, common_weight) == -16
    assert pairing(collapsed_degree, common_weight) == -16

    histogram = block_histogram(common_weight)
    print("VERIFIED common certificate")
    print("alignment", " ".join(map(str, ALIGN)))
    print("split_pairing", pairing(split_degree, common_weight))
    print("collapsed_pairing", pairing(collapsed_degree, common_weight))
    print("block_coefficient_histogram")
    for value, count in sorted(histogram.items()):
        print(value, count)
    print("CONTRADICTION for both aligned supports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
