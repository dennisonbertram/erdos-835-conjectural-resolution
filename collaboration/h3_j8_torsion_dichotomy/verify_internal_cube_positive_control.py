#!/usr/bin/env python3
"""Semantic verifier for the 70-variable internal-cube positive control."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "internal_cube_positive_control.json"


def main() -> None:
    payload = json.loads(DATA.read_text())
    assert payload["schema"] == "j8-internal-cube-positive-control-v1"
    assert payload["vertices"] == 8

    vertices = tuple(range(8))
    four_sets = tuple(itertools.combinations(vertices, 4))
    values_list = payload["d_values"]
    assert len(four_sets) == len(values_list) == 70
    d = dict(zip(four_sets, values_list))
    assert all(isinstance(value, int) and 0 <= value <= 13 for value in d.values())

    triple_loads = {
        triple: sum(
            value for q, value in d.items() if set(triple).issubset(q)
        )
        for triple in itertools.combinations(vertices, 3)
    }
    assert len(triple_loads) == 56
    assert max(triple_loads.values()) <= 13
    print("70 coordinates and 56 internal triple capacities: PASS")

    # Since e=d-1, the d-sum residue is C(q+3,4) modulo q.
    for size, modulus, residue in ((5, 2, 1), (6, 3, 0), (7, 4, 3), (8, 5, 0)):
        for s in itertools.combinations(vertices, size):
            total = sum(d[q] for q in itertools.combinations(s, 4))
            assert total % modulus == residue
            if size == 5:
                assert total <= 13
        print(f"all internal size-{size} sums modulo {modulus}: PASS")
    print("all internal size-5 recurrence sums are at most 13: PASS")

    pairs = tuple(tuple(pair) for pair in payload["cube_pairs"])
    positive = []
    negative = []
    for bits in itertools.product((0, 1), repeat=4):
        q = tuple(sorted(pairs[i][bits[i]] for i in range(4)))
        (positive if sum(bits) % 2 == 0 else negative).append(q)
    positive_sum = sum(d[q] for q in positive)
    negative_sum = sum(d[q] for q in negative)
    assert positive_sum == 60
    assert negative_sum == 0
    assert positive_sum - negative_sum == 60
    print("oriented cube totals P=60, N=0, Delta=60: PASS")

    print("PASS: the internal 8-vertex necessary-condition projection is feasible")
    print("scope: no 13-vertex extension, tower, colouring, or #835 conclusion")


if __name__ == "__main__":
    main()
