#!/usr/bin/env python3
"""Independent semantic verifier for exported cyclic LS(4,5,21) witnesses."""

from __future__ import annotations

import argparse
import json
from itertools import combinations


P = 17
POINTS = tuple(range(21))


def translate(subset: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return tuple(sorted((point + amount) % P if point < P else point for point in subset))


def canonical(subset: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    representative, shift_from_subset = min(
        (translate(subset, amount), amount) for amount in range(P)
    )
    return representative, (-shift_from_subset) % P


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("witness")
    args = parser.parse_args()
    payload = json.loads(open(args.witness).read())
    assert payload["model"] == "Z_17-equivariant LS(4,5,21)"
    assert payload["modulus"] == P
    representatives = tuple(tuple(block) for block in payload["representatives"])
    phases = tuple(payload["phases"])
    assert len(representatives) == len(phases) == 1197
    phase_by_representative = dict(zip(representatives, phases))
    assert len(phase_by_representative) == 1197
    for block in representatives:
        assert canonical(block)[0] == block
    for four_set in combinations(POINTS, 4):
        colours = []
        for point in POINTS:
            if point in four_set:
                continue
            representative, shift = canonical(tuple(sorted((*four_set, point))))
            colours.append((phase_by_representative[representative] + shift) % P)
        assert set(colours) == set(range(P)), (four_set, colours)
    print("independent cyclic LS(4,5,21) semantic verification: PASS")


if __name__ == "__main__":
    main()
