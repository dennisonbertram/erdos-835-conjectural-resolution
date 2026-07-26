#!/usr/bin/env python3
"""Independent semantic check of a centre-0 star witness.

Deliberately does NOT import the SAT encoder.  Combinatorial data (Wallis
golf table, cyclic triple orbits, translate) is reused from the checked-in
independent slice verifier ``verify_radius5_golf_cyclic_exact_slice_seed``.

Checks, for witness rows j = 1..14 against centre 0:
  (a) each row is an exact residual decomposition: 40 triples, one per
      orbit, avoiding both zero one-factors M_0 and M_j, covering the 120
      residual edges exactly once (degrees 8,7,...,7);
  (b) for each orbit the 14 phases are distinct and each lies in the
      allowed set A_k(j) (translate avoids M_0 and M_j).
"""

import argparse
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

REPO_BALL = Path(
    "/Users/dennison/Documents/Math Problem/evidence/odd_graph_local_ball"
)
sys.path.insert(0, str(REPO_BALL))

from verify_radius5_golf_cyclic_exact_slice_seed import (  # noqa: E402
    MOVING_EDGES,
    P,
    REPRESENTATIVES,
    translate,
)
from global_latin_audit import construct_golf17  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("witness", type=Path)
    args = parser.parse_args()

    raw = args.witness.read_bytes()
    payload = json.loads(raw)
    centre = payload["centre"]
    rows = payload["rows"]
    outers = [s for s in range(15) if s != centre]
    assert sorted(map(int, rows)) == outers, "wrong outer row set"

    golf = construct_golf17()
    matchings = {
        square: {
            edge
            for edge in MOVING_EDGES
            if golf[square][edge[0]][edge[1]] == 0
        }
        for square in range(15)
    }
    for square, matching in matchings.items():
        assert len(matching) == 8, f"square {square} colour-0 not a matching"

    exact_rows = 0
    for j in outers:
        phases = rows[str(j)]
        assert len(phases) == 40, f"row {j} has {len(phases)} orbits"
        forbidden = matchings[centre] | matchings[j]
        assert len(forbidden) == 16, f"zero factors overlap at row {j}"
        residual = set(MOVING_EDGES) - forbidden
        assert len(residual) == 120
        counts: Counter = Counter()
        degrees = [0] * P
        for orbit_index, shift in enumerate(phases):
            assert isinstance(shift, int) and 0 <= shift < P
            triple = translate(REPRESENTATIVES[orbit_index], shift)
            edges = set(combinations(triple, 2))
            assert not edges & matchings[centre], (
                f"row {j} orbit {orbit_index} hits centre matching"
            )
            assert not edges & matchings[j], (
                f"row {j} orbit {orbit_index} hits row matching"
            )
            counts.update(edges)
            for vertex in triple:
                degrees[vertex] += 1
        assert set(counts) == residual, f"row {j} wrong residual support"
        assert set(counts.values()) == {1}, f"row {j} repeats an edge"
        assert sorted(degrees, reverse=True) == [8] + [7] * 16, (
            f"row {j} wrong degrees"
        )
        exact_rows += 1

    distinct_orbits = 0
    for orbit_index in range(40):
        column = [rows[str(j)][orbit_index] for j in outers]
        assert len(set(column)) == 14, (
            f"orbit {orbit_index} phase collision: {sorted(column)}"
        )
        distinct_orbits += 1

    print(
        json.dumps(
            {
                "status": "PASS",
                "centre": centre,
                "exact_rows": exact_rows,
                "distinct_orbit_columns": distinct_orbits,
                "witness_sha256": hashlib.sha256(raw).hexdigest(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
