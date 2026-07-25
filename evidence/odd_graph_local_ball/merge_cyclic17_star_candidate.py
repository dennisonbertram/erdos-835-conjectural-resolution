#!/usr/bin/env python3
"""Merge and audit a 14-row star candidate into an exact 105-row state."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from improve_cyclic17_star_exact_rows import (
    FIXED,
    centre_metrics,
    incident_pair,
)
from search_cyclic17_star_row_pool import audit_row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=Path)
    parser.add_argument("star", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    state_payload = json.loads(args.base.read_text(encoding="utf-8"))
    state = {
        tuple(map(int, key.split(","))): list(phases)
        for key, phases in state_payload.items()
    }
    star_payload = json.loads(args.star.read_text(encoding="utf-8"))
    centre = star_payload["centre"]
    rows = star_payload["rows"]
    expected = {
        f"{incident_pair(centre, other)[0]},"
        f"{incident_pair(centre, other)[1]}"
        for other in FIXED
        if other != centre
    }
    if set(rows) != expected:
        raise ValueError("star candidate has the wrong incident rows")
    for key, phases in rows.items():
        pair = tuple(map(int, key.split(",")))
        state[pair] = list(phases)
        audit_row(state, pair)

    encoded = (
        json.dumps(
            {
                f"{pair[0]},{pair[1]}": phases
                for pair, phases in sorted(state.items())
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    args.output.write_bytes(encoded)
    distinct, collision_pairs, exact_groups = centre_metrics(
        state, centre
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "centre": centre,
                "collision_pairs": collision_pairs,
                "distinct": distinct,
                "exact_groups": exact_groups,
                "sha256": hashlib.sha256(encoded).hexdigest(),
                "scope": "one fixed-Wallis C17 star candidate only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
