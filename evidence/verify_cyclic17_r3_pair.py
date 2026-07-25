#!/usr/bin/env python3
"""Stdlib-only semantic verifier for one cyclic-17 moving-triple slice."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

from global_latin_audit import construct_golf17


P = 17
MOVING = tuple(range(P))
MOVING_PAIRS = tuple(combinations(MOVING, 2))
MOVING_TRIPLES = tuple(combinations(MOVING, 3))


def translate(subset: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return tuple(sorted((x + amount) % P for x in subset))


def triple_orbit_table():
    representatives: list[tuple[int, int, int]] = []
    lookup: dict[tuple[int, int, int], tuple[int, int]] = {}
    unseen = set(MOVING_TRIPLES)
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in MOVING)
        orbit_index = len(representatives)
        representatives.append(representative)
        for shift in MOVING:
            triple = translate(representative, shift)
            assert triple not in lookup
            lookup[triple] = (orbit_index, shift)
            unseen.discard(triple)
    assert len(representatives) == 40
    assert len(lookup) == len(MOVING_TRIPLES)
    return representatives, lookup


TRIPLE_REPRESENTATIVES, TRIPLE_LOOKUP = triple_orbit_table()


def triple_colour(triple: tuple[int, int, int], phases: list[int]) -> int:
    orbit_index, shift = TRIPLE_LOOKUP[triple]
    return (phases[orbit_index] + shift) % P


def verify(path: Path, fixed_pair: tuple[int, int]) -> None:
    payload = json.loads(path.read_text())
    key = f"{fixed_pair[0]},{fixed_pair[1]}"
    phases = payload[key]
    assert len(phases) == 40
    assert all(isinstance(value, int) and 0 <= value < P for value in phases)

    golf = construct_golf17()
    i, j = fixed_pair

    # Directly verify every lower pair-star and translation equivariance.
    for pair in MOVING_PAIRS:
        colours = {golf[i][pair[0]][pair[1]], golf[j][pair[0]][pair[1]]}
        colours.update(
            triple_colour(tuple(sorted((*pair, z))), phases)
            for z in MOVING
            if z not in pair
        )
        assert colours == set(MOVING)
    for triple in MOVING_TRIPLES:
        for shift in MOVING:
            assert triple_colour(
                translate(triple, shift), phases
            ) == (triple_colour(triple, phases) + shift) % P

    # Reconstruct the claimed LS(2,3,19) and verify it from incidences.
    fixed_i, fixed_j = 17, 18
    all_points = tuple(range(19))
    all_triples = set(combinations(all_points, 3))
    partition: set[tuple[int, int, int]] = set()
    for colour in MOVING:
        blocks: set[tuple[int, int, int]] = {
            tuple(sorted((fixed_i, fixed_j, colour)))
        }
        blocks.update(
            tuple(sorted((fixed_i, x, y)))
            for x, y in MOVING_PAIRS
            if golf[i][x][y] == colour
        )
        blocks.update(
            tuple(sorted((fixed_j, x, y)))
            for x, y in MOVING_PAIRS
            if golf[j][x][y] == colour
        )
        blocks.update(
            triple
            for triple in MOVING_TRIPLES
            if triple_colour(triple, phases) == colour
        )
        assert len(blocks) == 57

        pair_counts = {pair: 0 for pair in combinations(all_points, 2)}
        for block in blocks:
            for pair in combinations(block, 2):
                pair_counts[pair] += 1
        assert set(pair_counts.values()) == {1}
        assert partition.isdisjoint(blocks)
        partition.update(blocks)
    assert partition == all_triples


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--fixed-pair", default="0,1")
    args = parser.parse_args()
    fixed_pair = tuple(sorted(map(int, args.fixed_pair.split(","))))
    assert (
        len(fixed_pair) == 2
        and 0 <= fixed_pair[0] < fixed_pair[1] < 15
    )
    verify(args.certificate, fixed_pair)
    print(
        "PASS: cyclic equivariance, all 136 moving-pair stars, and the "
        "reconstructed 17-system LS(2,3,19)"
    )


if __name__ == "__main__":
    main()
