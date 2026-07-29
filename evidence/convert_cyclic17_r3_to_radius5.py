#!/usr/bin/env python3
"""Convert a joint cyclic phase witness to the canonical radius-5 payload."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parent
BALL = EVIDENCE / "odd_graph_local_ball"
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))
if str(BALL) not in sys.path:
    sys.path.insert(0, str(BALL))

from global_latin_audit import construct_golf17
from verify_radius5_golf_joint import SCHEMA, golf_sha256, verify_payload


P = 17
MOVING = tuple(range(P))
FINITE = tuple(range(16))
FIXED = tuple(range(15))
UVS = tuple(combinations(FINITE, 2))
IJS = tuple(combinations(FIXED, 2))
FINITE_TRIPLES = tuple(combinations(FINITE, 3))
MOVING_TRIPLES = tuple(combinations(MOVING, 3))


def translate(subset: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return tuple(sorted((x + amount) % P for x in subset))


def make_triple_lookup():
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
            lookup[triple] = (orbit_index, shift)
            unseen.discard(triple)
    assert len(representatives) == 40 and len(lookup) == 680
    return lookup


TRIPLE_LOOKUP = make_triple_lookup()


def triple_colour(triple: tuple[int, int, int], phases: list[int]) -> int:
    orbit_index, shift = TRIPLE_LOOKUP[triple]
    return (phases[orbit_index] + shift) % P


def convert(phases_by_pair: dict[str, list[int]]) -> dict[str, object]:
    assert set(phases_by_pair) == {f"{i},{j}" for i, j in IJS}
    assert all(
        len(phases) == 40
        and all(isinstance(value, int) and 0 <= value < P for value in phases)
        for phases in phases_by_pair.values()
    )

    def phases(i: int, j: int) -> list[int]:
        return phases_by_pair[f"{i},{j}"]

    n_values = [
        triple_colour(tuple(sorted((u, v, 16))), phases(i, j))
        for u, v in UVS
        for i, j in IJS
    ]
    p_values = [
        triple_colour((u, v, w), phases(i, j))
        for i, j in IJS
        for u, v, w in FINITE_TRIPLES
    ]
    stats = {
        "n_variables": 12600,
        "p_variables": 58800,
        "integer_variables": 71400,
        "n_domain_values": 143640,
        "p_domain_values": 670320,
        "n_all_different": 1800,
        "p_all_different": 12600,
        "n_p_not_equal": 176400,
        "constraints": 190800,
    }
    golf = construct_golf17()
    payload: dict[str, object] = {
        "schema": SCHEMA,
        "golf_sha256": golf_sha256(golf),
        "counts": stats,
        "n_order": "uv-major then ij-major, lexicographic combinations",
        "n_values": n_values,
        "p_order": "ij-major then uvw-major, lexicographic combinations",
        "p_values": p_values,
    }
    canonical = (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    payload["sha256_without_hash"] = hashlib.sha256(canonical).hexdigest()
    verify_payload(payload, semantic_ball=True)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phases", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    payload = convert(json.loads(args.phases.read_text()))
    args.output.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    )
    print(
        "PASS: converted phases and independently verified the complete "
        "73,457-vertex radius-5 ball"
    )
    print(f"sha256_without_hash: {payload['sha256_without_hash']}")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
