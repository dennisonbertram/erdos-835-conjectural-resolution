#!/usr/bin/env python3
"""Verify a non-mate isotropic line in the deleted k=6 Witt kernel.

This is a pure-stdlib witness checker.  It does not invoke the SAT solver
used to discover the witness and does not enumerate the full quadratic cone.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
WITNESS_PATH = HERE / "k6_lambda3_witness.json"
PRIME = 7


def canonical_witt_hexads() -> set[tuple[int, ...]]:
    """Build W_12 from the extended ternary Golay [12,6,6]_3 code."""
    matrix = [
        [0, 1, 1, 1, 1, 1],
        [1, 0, 1, 2, 2, 1],
        [1, 1, 0, 1, 2, 2],
        [1, 2, 1, 0, 1, 2],
        [1, 2, 2, 1, 0, 1],
        [1, 1, 2, 2, 1, 0],
    ]
    generator = [[int(i == j) for j in range(6)] + matrix[i] for i in range(6)]

    words: set[tuple[int, ...]] = set()
    for coefficients in product(range(3), repeat=6):
        word = tuple(
            sum(coefficients[i] * generator[i][j] for i in range(6)) % 3
            for j in range(12)
        )
        words.add(word)
    assert len(words) == 3**6
    assert Counter(sum(value != 0 for value in word) for word in words) == {
        0: 1,
        6: 264,
        9: 440,
        12: 24,
    }

    hexads = {
        tuple(index for index, value in enumerate(word) if value)
        for word in words
        if sum(value != 0 for value in word) == 6
    }
    # The two nonzero scalar multiples of a weight-six word have the same
    # support, leaving the 132 blocks of W_12.
    assert len(hexads) == 132
    return hexads


def verify_steiner_system(
    hexads: set[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    facets = list(combinations(range(12), 5))
    coverage = Counter(facet for block in hexads for facet in combinations(block, 5))
    assert len(facets) == 792
    assert set(coverage) == set(facets)
    assert set(coverage.values()) == {1}
    return facets


def load_witness() -> tuple[str, dict[str, object]]:
    payload = json.loads(WITNESS_PATH.read_text())
    assert payload["schema"] == "k6-deleted-witt-lambda3-bitset-v1"
    bits = payload["bits"]
    assert isinstance(bits, str)
    assert set(bits) <= {"0", "1"}
    assert sha256(bits.encode()).hexdigest() == payload["bits_sha256"]
    assert bits.count("1") == payload["selected_count"] == 396
    return bits, payload


def main() -> None:
    base = canonical_witt_hexads()
    facets = verify_steiner_system(base)
    all_hexads = list(combinations(range(12), 6))
    remaining = [block for block in all_hexads if block not in base]
    assert len(all_hexads) == 924
    assert len(remaining) == len(facets) == 792

    bits, payload = load_witness()
    assert len(bits) == len(remaining)
    selected = {block for bit, block in zip(bits, remaining) if bit == "1"}
    assert len(selected) == 396
    assert not (selected & base)

    selected_star_counts: Counter[int] = Counter()
    value_profiles: Counter[tuple[tuple[int, int], ...]] = Counter()
    linear_sums: Counter[int] = Counter()
    square_sums: Counter[int] = Counter()

    for facet in facets:
        facet_set = set(facet)
        star = [block for block in remaining if facet_set.issubset(block)]
        assert len(star) == 6
        selected_count = sum(block in selected for block in star)
        selected_star_counts[selected_count] += 1

        values = [6 if block in selected else 1 for block in star]
        value_profiles[tuple(sorted(Counter(values).items()))] += 1
        linear_sums[sum(values) % PRIME] += 1
        square_sums[sum(value * value for value in values) % PRIME] += 1

    # E is a simple 5-(12,6,3) subdesign inside the complement of W_12.
    assert selected_star_counts == {3: 792}

    # Thus x has three +1 and three -1 entries on every deleted star.
    assert value_profiles == {((1, 3), (6, 3)): 792}
    assert linear_sums == {0: 792}
    assert square_sums == {6: 792}

    # A scalar multiple of h_C=1+1_C for a Steiner mate C has local
    # multiplicities 5+1 on every deleted star.  The witness has 3+3, so its
    # projective line is not in the Steiner-mate sector.
    assert all(
        sorted(count for _, count in profile) == [3, 3] for profile in value_profiles
    )

    print("canonical W_12: 132 hexads; every 5-set covered exactly once")
    print("deleted matrix: 792 rows x 792 remaining hexads")
    print("witness E: 396 hexads; every deleted star meets E exactly 3 times")
    print("Mx = 0 and M(x^2) = 6*1 over F_7")
    print("local value multiplicity is 3+3, not the mate profile 5+1")
    print("witness SHA-256:", payload["bits_sha256"])
    print("K6 NON-MATE ISOTROPIC-LINE WITNESS: PASS")


if __name__ == "__main__":
    main()
