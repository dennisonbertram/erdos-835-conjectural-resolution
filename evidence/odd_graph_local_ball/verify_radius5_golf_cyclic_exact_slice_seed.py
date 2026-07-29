#!/usr/bin/env python3
"""Independently verify a 105-slice cyclic exact-cover seed.

This checks every selected translate directly against the Wallis golf table:
each of the 105 fixed-point pairs must select one triple from every cyclic
orbit and decompose exactly the 120 edges outside its two zero one-factors.
It also reports, but does not require away, collisions in the 600 shared-N
proper-edge-colouring groups.  Thus PASS certifies all slices separately,
not a joint radius-five layer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parents[1]
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from global_latin_audit import construct_golf17


P = 17
POINTS = tuple(range(P))
SQUARES = tuple(range(15))
FIXED_PAIRS = tuple(combinations(SQUARES, 2))
MOVING_EDGES = tuple(combinations(POINTS, 2))
MOVING_TRIPLES = tuple(combinations(POINTS, 3))
LINK_LEFT, LINK_RIGHT = 17, 18
ALL_LSTS_POINTS = tuple(range(19))
ALL_LSTS_TRIPLES = set(combinations(ALL_LSTS_POINTS, 3))


def translate(
    subset: tuple[int, ...],
    amount: int,
) -> tuple[int, ...]:
    return tuple(sorted((value + amount) % P for value in subset))


def triple_representatives() -> list[tuple[int, int, int]]:
    answer = []
    unseen = set(MOVING_TRIPLES)
    while unseen:
        seed = min(unseen)
        representative = min(
            translate(seed, shift) for shift in POINTS
        )
        answer.append(representative)
        for shift in POINTS:
            unseen.discard(translate(representative, shift))
    if len(answer) != 40:
        raise AssertionError("wrong number of cyclic triple orbits")
    return answer


REPRESENTATIVES = triple_representatives()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()

    raw = args.source.read_bytes()
    payload = json.loads(raw)
    expected = {f"{i},{j}" for i, j in FIXED_PAIRS}
    if set(payload) != expected:
        raise ValueError("seed does not contain all 105 fixed pairs")

    golf = construct_golf17()
    shifts: dict[tuple[int, int, int], int] = {}
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        if (
            not isinstance(phases, list)
            or len(phases) != len(REPRESENTATIVES)
            or not all(
                isinstance(phase, int) and 0 <= phase < P
                for phase in phases
            )
        ):
            raise ValueError(f"invalid phase list for {i},{j}")
        for orbit_index, phase in enumerate(phases):
            shifts[i, j, orbit_index] = (-phase) % P

    for i, j in FIXED_PAIRS:
        forbidden = {
            edge
            for edge in MOVING_EDGES
            if golf[i][edge[0]][edge[1]] == 0
            or golf[j][edge[0]][edge[1]] == 0
        }
        if len(forbidden) != 16:
            raise AssertionError(f"zero one-factors overlap at {i},{j}")
        counts: Counter[tuple[int, int]] = Counter()
        degrees = [0] * P
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            triple = translate(
                representative,
                shifts[i, j, orbit_index],
            )
            for vertex in triple:
                degrees[vertex] += 1
            counts.update(combinations(triple, 2))
        residual = set(MOVING_EDGES) - forbidden
        if set(counts) != residual:
            raise AssertionError(
                f"selected triples have wrong residual support at {i},{j}"
            )
        if any(counts[edge] != 1 for edge in residual):
            raise AssertionError(
                f"selected triples repeat a residual edge at {i},{j}"
            )
        if degrees != [8] + [7] * 16:
            raise AssertionError(
                f"selected triples have wrong vertex degrees at {i},{j}"
            )

        # Reconstruct all seventeen translated colour classes directly.
        # This checks the phase/sign convention as well as the colour-zero
        # exact cover: every class must be an STS(19), and together they
        # must partition all triples on the nineteen points.
        partition: set[tuple[int, int, int]] = set()
        for colour in POINTS:
            blocks = {
                tuple(sorted((LINK_LEFT, LINK_RIGHT, colour)))
            }
            blocks.update(
                tuple(sorted((LINK_LEFT, x, y)))
                for x, y in MOVING_EDGES
                if golf[i][x][y] == colour
            )
            blocks.update(
                tuple(sorted((LINK_RIGHT, x, y)))
                for x, y in MOVING_EDGES
                if golf[j][x][y] == colour
            )
            blocks.update(
                translate(
                    representative,
                    (shifts[i, j, orbit_index] + colour) % P,
                )
                for orbit_index, representative in enumerate(REPRESENTATIVES)
            )
            if len(blocks) != 57:
                raise AssertionError(
                    f"wrong STS block count at {i},{j}, colour {colour}"
                )
            pair_counts: Counter[tuple[int, int]] = Counter()
            for block in blocks:
                pair_counts.update(combinations(block, 2))
            if (
                set(pair_counts) != set(combinations(ALL_LSTS_POINTS, 2))
                or set(pair_counts.values()) != {1}
            ):
                raise AssertionError(
                    f"not an STS(19) at {i},{j}, colour {colour}"
                )
            if not partition.isdisjoint(blocks):
                raise AssertionError(
                    f"colour classes overlap at {i},{j}, colour {colour}"
                )
            partition.update(blocks)
        if partition != ALL_LSTS_TRIPLES:
            raise AssertionError(
                f"colour classes do not partition triples at {i},{j}"
            )

    collision_pairs = 0
    distinct_phase_slots = 0
    conflict_free_groups = 0
    for orbit_index in range(len(REPRESENTATIVES)):
        for fixed_point in SQUARES:
            incident = [
                shifts[
                    min(fixed_point, other),
                    max(fixed_point, other),
                    orbit_index,
                ]
                for other in SQUARES
                if other != fixed_point
            ]
            counts = Counter(incident)
            collision_pairs += sum(
                multiplicity * (multiplicity - 1) // 2
                for multiplicity in counts.values()
            )
            distinct_phase_slots += len(counts)
            conflict_free_groups += len(counts) == len(incident)

    print(
        json.dumps(
            {
                "status": "PASS",
                "scope": (
                    "105 independently exact prescribed-link slices; "
                    "shared-N collisions reported, not accepted"
                ),
                "slices": len(FIXED_PAIRS),
                "selected_triples_per_slice": len(REPRESENTATIVES),
                "residual_edges_per_slice": 120,
                "reconstructed_sts19_classes": len(FIXED_PAIRS) * P,
                "shared_n_groups": 600,
                "shared_n_conflict_free_groups": conflict_free_groups,
                "shared_n_collision_pairs": collision_pairs,
                "shared_n_distinct_phase_slots": distinct_phase_slots,
                "shared_n_required_distinct_phase_slots": 600 * 14,
                "sha256": hashlib.sha256(raw).hexdigest(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
