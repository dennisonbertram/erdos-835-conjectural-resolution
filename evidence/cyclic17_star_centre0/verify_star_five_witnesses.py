#!/usr/bin/env python3
"""Verify all complete centre-0 families and every five-family witness."""

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

P = 17
ORBITS = 40
FIRST_HALF = (
    (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
    (5, 1, 7, 8, 9, 16, 14, 4, 13, 15, 10, 6, 11, 3, 12),
    (9, 10, 12, 2, 15, 13, 16, 14, 4, 7, 5, 8, 1, 11, 6),
    (14, 12, 2, 13, 3, 8, 9, 16, 7, 5, 1, 15, 6, 10, 11),
    (16, 11, 13, 15, 1, 3, 6, 10, 2, 14, 4, 7, 8, 12, 9),
    (13, 15, 16, 1, 14, 11, 4, 7, 12, 8, 9, 3, 10, 5, 2),
    (15, 4, 1, 14, 11, 2, 10, 3, 5, 6, 13, 16, 12, 9, 8),
    (12, 13, 14, 11, 10, 9, 2, 6, 16, 3, 15, 1, 7, 4, 5),
)


def translate(triple, shift):
    return tuple(sorted((point + shift) % P for point in triple))


def representatives():
    unseen = set(combinations(range(P), 3))
    result = []
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in range(P))
        result.append(representative)
        for shift in range(P):
            unseen.discard(translate(representative, shift))
    assert len(result) == ORBITS
    return result


def normalized_edge(position, difference):
    return tuple(sorted((position, (position + difference) % P)))


def zero_factor(square):
    result = {
        normalized_edge(
            (-FIRST_HALF[difference - 1][square]) % P, difference
        )
        for difference in range(1, 9)
    }
    assert len(result) == 8
    return result


def load_families(directory):
    reps = representatives()
    all_edges = set(combinations(range(P), 2))
    families = {}
    for outer in range(2, 15):
        path = directory / f"sols_0_{outer}.bin"
        raw = path.read_bytes()
        assert raw and len(raw) % ORBITS == 0
        rows = [
            raw[offset : offset + ORBITS]
            for offset in range(0, len(raw), ORBITS)
        ]
        assert len(set(rows)) == len(rows)
        residual = all_edges - zero_factor(0) - zero_factor(outer)
        assert len(residual) == 120
        for row in rows:
            assert all(phase <= 16 for phase in row)
            edges = []
            for orbit, phase in enumerate(row):
                triple = translate(reps[orbit], (-phase) % P)
                edges.extend(combinations(triple, 2))
            assert len(edges) == 120
            assert len(set(edges)) == 120
            assert set(edges) == residual
        families[outer] = rows
    return families


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("family_directory", type=Path)
    parser.add_argument("witnesses", type=Path)
    args = parser.parse_args()

    families = load_families(args.family_directory)
    records = [
        json.loads(line)
        for line in args.witnesses.read_text(encoding="ascii").splitlines()
        if line
    ]
    expected = list(combinations(range(2, 15), 5))
    assert len(records) == len(expected) == 1287
    seen = set()
    for record in records:
        selected_families = tuple(record["families"])
        selected_rows = tuple(record["rows"])
        assert selected_families in expected
        assert selected_families not in seen
        seen.add(selected_families)
        assert len(selected_rows) == 5
        rows = []
        for family, row_index in zip(selected_families, selected_rows):
            assert 0 <= row_index < len(families[family])
            rows.append(families[family][row_index])
        for left, right in combinations(rows, 2):
            assert all(a != b for a, b in zip(left, right))
    assert seen == set(expected)

    print(
        json.dumps(
            {
                "status": "PASS",
                "family_sizes": {
                    str(key): len(value)
                    for key, value in families.items()
                },
                "stored_rows_semantically_checked": sum(
                    map(len, families.values())
                ),
                "five_family_witnesses_checked": len(records),
                "witness_sha256": hashlib.sha256(
                    args.witnesses.read_bytes()
                ).hexdigest(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
