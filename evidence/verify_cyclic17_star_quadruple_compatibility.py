#!/usr/bin/env python3
"""Independently verify centre-0 four-row compatibility certificates.

Default PASS requires all 1,001 outer quadruples.  With ``--allow-partial``,
every resolved record is still checked exactly and the unresolved complement
must be listed explicitly; the resulting status is PASS_PARTIAL, not a
complete width-four theorem.
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
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    encoded = args.certificate.read_bytes()
    payload = json.loads(encoded)
    if payload.get("schema") != (
        "cyclic17-centre0-quadruple-compatibility-v1"
    ):
        raise ValueError("wrong certificate schema")
    if payload.get("centre") != 0:
        raise ValueError("certificate centre is not zero")

    expected = set(itertools.combinations(range(1, 15), 4))
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError("records is not a list")
    seen = set()
    golf = construct_golf17()
    for record in records:
        quadruple = tuple(record.get("outers", []))
        if quadruple not in expected or quadruple in seen:
            raise ValueError("duplicate or invalid outer quadruple")
        rows = record.get("phase_rows")
        if not isinstance(rows, list) or len(rows) != 4:
            raise ValueError("quadruple record has wrong phase rows")
        for outer, phases in zip(quadruple, rows):
            verify_row(golf, 0, outer, phases)
        collisions = sum(
            sum(
                left == right
                for left, right in zip(rows[a], rows[b])
            )
            for a, b in itertools.combinations(range(4), 2)
        )
        if collisions != 0 or record.get("collision_count") != 0:
            raise ValueError("quadruple record has a phase collision")
        seen.add(quadruple)

    unknown_raw = payload.get("unknown_quadruples", [])
    if not isinstance(unknown_raw, list):
        raise ValueError("unknown_quadruples is not a list")
    unknown = {tuple(item) for item in unknown_raw}
    if len(unknown) != len(unknown_raw):
        raise ValueError("duplicate unknown quadruple")
    if any(item not in expected for item in unknown):
        raise ValueError("invalid unknown quadruple")
    if seen & unknown or seen | unknown != expected:
        raise ValueError("resolved and unknown lists do not partition target")
    if payload.get("resolved_quadruples") != len(seen):
        raise ValueError("resolved count is inconsistent")
    if payload.get("target_quadruples") != len(expected):
        raise ValueError("target count is inconsistent")
    if unknown and not args.allow_partial:
        raise ValueError(
            "certificate is partial; rerun with --allow-partial"
        )

    print(
        json.dumps(
            {
                "status": "PASS" if not unknown else "PASS_PARTIAL",
                "centre": 0,
                "verified_quadruple_subsystems": len(seen),
                "unknown_quadruple_subsystems": len(unknown),
                "verified_exact_rows": 4 * len(seen),
                "verified_pairwise_phase_collisions": 0,
                "certificate_sha256": hashlib.sha256(
                    encoded
                ).hexdigest(),
                "scope": (
                    "four-row subsystems only; "
                    "no fourteen-row star claim"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
