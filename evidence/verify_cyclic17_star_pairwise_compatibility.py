#!/usr/bin/env python3
"""Independently verify all centre-0 two-row compatibility certificates.

Passing this verifier proves only that every pair of outer rows has some
collision-free pair of exact residual decompositions.  Different records may
use different decompositions, so the certificate is not a fourteen-row star
and is not a result for the unrestricted Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent
BALL = EVIDENCE / "odd_graph_local_ball"
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from search_radius5_golf_cyclic_compact import (
    MOVING_EDGES,
    P,
    REPRESENTATIVES,
    translate,
)


def verify_row(golf, centre: int, outer: int, phases) -> None:
    if (
        not isinstance(phases, list)
        or len(phases) != len(REPRESENTATIVES)
        or not all(
            isinstance(value, int) and 0 <= value < P
            for value in phases
        )
    ):
        raise ValueError("invalid phase row")
    selected_edges = []
    for orbit, portable_phase in enumerate(phases):
        triple = translate(
            REPRESENTATIVES[orbit],
            (-portable_phase) % P,
        )
        selected_edges.extend(combinations(triple, 2))
    if len(selected_edges) != 120 or len(set(selected_edges)) != 120:
        raise ValueError("row is not an exact residual edge packing")
    leave = set(MOVING_EDGES) - set(selected_edges)
    expected = {
        edge
        for edge in MOVING_EDGES
        if golf[centre][edge[0]][edge[1]] == 0
        or golf[outer][edge[0]][edge[1]] == 0
    }
    if leave != expected:
        raise ValueError("row has the wrong prescribed leave")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    encoded = args.certificate.read_bytes()
    payload = json.loads(encoded)
    if payload.get("schema") != (
        "cyclic17-centre0-pairwise-compatibility-v1"
    ):
        raise ValueError("wrong certificate schema")
    if payload.get("centre") != 0:
        raise ValueError("certificate centre is not zero")
    if payload.get("resolved_pairs") != 91:
        raise ValueError("certificate does not resolve all 91 pairs")

    expected_pairs = set(combinations(range(1, 15), 2))
    seen = set()
    golf = construct_golf17()
    for record in payload.get("records", []):
        first = record.get("outer_a")
        second = record.get("outer_b")
        pair = tuple(sorted((first, second)))
        if pair not in expected_pairs or pair in seen:
            raise ValueError("duplicate or invalid outer pair")
        phases_first = record.get("phases_a")
        phases_second = record.get("phases_b")
        verify_row(golf, 0, first, phases_first)
        verify_row(golf, 0, second, phases_second)
        collisions = sum(
            left == right
            for left, right in zip(phases_first, phases_second)
        )
        if collisions != 0 or record.get("collision_count") != 0:
            raise ValueError("pair certificate has a phase collision")
        seen.add(pair)
    if seen != expected_pairs:
        raise ValueError("certificate omits outer pairs")

    print(
        json.dumps(
            {
                "status": "PASS",
                "centre": 0,
                "verified_pair_subsystems": len(seen),
                "verified_exact_rows": 2 * len(seen),
                "verified_phase_collisions": 0,
                "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
                "scope": (
                    "all two-row subsystems only; "
                    "no fourteen-row star claim"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
