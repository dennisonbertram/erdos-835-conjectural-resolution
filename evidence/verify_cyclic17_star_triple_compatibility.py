#!/usr/bin/env python3
"""Independently verify centre-0 three-row compatibility certificates.

PASS for all 364 triples proves only that no obstruction is supported on at
most three outer rows.  Different triple records may use different rows, so
this is not a fourteen-row star and not a solution of Erdos--Rosenfeld 835.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent
BALL = EVIDENCE / "odd_graph_local_ball"
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from verify_cyclic17_star_pairwise_compatibility import verify_row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    encoded = args.certificate.read_bytes()
    payload = json.loads(encoded)
    if payload.get("schema") != (
        "cyclic17-centre0-triple-compatibility-v1"
    ):
        raise ValueError("wrong certificate schema")
    if payload.get("centre") != 0:
        raise ValueError("certificate centre is not zero")

    expected = set(itertools.combinations(range(1, 15), 3))
    if payload.get("resolved_triples") != len(expected):
        raise ValueError("certificate does not resolve all 364 triples")
    seen = set()
    golf = construct_golf17()
    for record in payload.get("records", []):
        triple = tuple(record.get("outers", []))
        if triple not in expected or triple in seen:
            raise ValueError("duplicate or invalid outer triple")
        rows = record.get("phase_rows")
        if not isinstance(rows, list) or len(rows) != 3:
            raise ValueError("triple record has wrong phase rows")
        for outer, phases in zip(triple, rows):
            verify_row(golf, 0, outer, phases)
        collisions = sum(
            sum(left == right for left, right in zip(rows[a], rows[b]))
            for a, b in itertools.combinations(range(3), 2)
        )
        if collisions != 0 or record.get("collision_count") != 0:
            raise ValueError("triple record has a phase collision")
        seen.add(triple)
    if seen != expected:
        raise ValueError("certificate omits outer triples")

    print(
        json.dumps(
            {
                "status": "PASS",
                "centre": 0,
                "verified_triple_subsystems": len(seen),
                "verified_exact_rows": 3 * len(seen),
                "verified_pairwise_phase_collisions": 0,
                "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
                "scope": (
                    "all three-row subsystems only; "
                    "no fourteen-row star claim"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
