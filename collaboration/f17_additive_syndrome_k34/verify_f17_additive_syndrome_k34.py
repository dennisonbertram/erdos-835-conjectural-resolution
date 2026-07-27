#!/usr/bin/env python3
"""Exact K34 certificate for the two-layer additive F_17^2 syndrome.

Standard library only.  The dynamic program constructs explicit adjacent
16-sets for every pair of quotient vertices in F_17 x {7, 8}; the audit then
checks those witnesses directly.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations

PRIME = 17
CORE_SIZE = 15
BLOCK_SIZE = 16
GROUND = tuple((value, layer) for layer in range(2) for value in range(1, PRIME))
STATE_COUNT = PRIME * PRIME
CLIQUE = frozenset((first, second) for second in (7, 8) for first in range(PRIME))


def state_index(state: tuple[int, int]) -> int:
    """Encode an F_17^2 state."""
    return state[0] + PRIME * state[1]


def decode_state(index: int) -> tuple[int, int]:
    """Decode an F_17^2 state."""
    return index % PRIME, index // PRIME


def add_states(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Add two states in F_17^2."""
    return (
        (left[0] + right[0]) % PRIME,
        (left[1] + right[1]) % PRIME,
    )


def syndrome(indices: frozenset[int]) -> tuple[int, int]:
    """Return the additive syndrome of a ground-index set."""
    return (
        sum(GROUND[index][0] for index in indices) % PRIME,
        sum(GROUND[index][1] for index in indices) % PRIME,
    )


def core_subset_sums(excluded: tuple[int, int]) -> list[int]:
    """Store one 15-subset mask at every reachable residual syndrome."""
    first, second = excluded
    tables = [[-1] * STATE_COUNT for _ in range(CORE_SIZE + 1)]
    tables[0][state_index((0, 0))] = 0
    processed = 0

    for point_index, point in enumerate(GROUND):
        if point_index in excluded:
            continue
        upper = min(processed, CORE_SIZE - 1)
        for size in range(upper, -1, -1):
            source = tables[size]
            target = tables[size + 1]
            for old_index, old_mask in enumerate(source):
                if old_mask < 0:
                    continue
                new_state = add_states(decode_state(old_index), point)
                new_index = state_index(new_state)
                if target[new_index] < 0:
                    target[new_index] = old_mask | (1 << point_index)
        processed += 1

    return tables[CORE_SIZE]


def mask_to_set(mask: int) -> frozenset[int]:
    """Decode a bit mask of ground indices."""
    return frozenset(index for index in range(len(GROUND)) if mask & (1 << index))


def canonical_pair(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Canonicalize an unordered syndrome pair."""
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def construct_witnesses() -> dict[
    tuple[tuple[int, int], tuple[int, int]],
    tuple[frozenset[int], frozenset[int]],
]:
    """Construct the first deterministic witness for every clique edge."""
    required = set(combinations(sorted(CLIQUE), 2))
    witnesses: dict[
        tuple[tuple[int, int], tuple[int, int]],
        tuple[frozenset[int], frozenset[int]],
    ] = {}

    for first, second in combinations(range(len(GROUND)), 2):
        residual = core_subset_sums((first, second))
        for residual_index, mask in enumerate(residual):
            if mask < 0:
                continue
            residual_state = decode_state(residual_index)
            left = add_states(residual_state, GROUND[first])
            right = add_states(residual_state, GROUND[second])
            pair = canonical_pair(left, right)
            if pair not in required or pair in witnesses:
                continue
            core = mask_to_set(mask)
            witnesses[pair] = (
                core | {first},
                core | {second},
            )
        if len(witnesses) == len(required):
            break

    assert set(witnesses) == required
    return witnesses


def verify_witnesses(
    witnesses: dict[
        tuple[tuple[int, int], tuple[int, int]],
        tuple[frozenset[int], frozenset[int]],
    ],
) -> str:
    """Independently audit all constructed Johnson edges and hash them."""
    required = set(combinations(sorted(CLIQUE), 2))
    assert len(GROUND) == 32
    assert len(set(GROUND)) == 32
    assert len(CLIQUE) == 34
    assert len(required) == 561
    assert set(witnesses) == required

    digest_rows = []
    for pair in sorted(witnesses):
        left_set, right_set = witnesses[pair]
        assert len(left_set) == BLOCK_SIZE
        assert len(right_set) == BLOCK_SIZE
        assert len(left_set ^ right_set) == 2
        assert len(left_set & right_set) == CORE_SIZE

        observed = canonical_pair(
            syndrome(left_set),
            syndrome(right_set),
        )
        assert observed == pair
        assert pair[0] in CLIQUE
        assert pair[1] in CLIQUE

        digest_rows.append(
            f"{pair[0]}|{pair[1]}|"
            f"{','.join(map(str, sorted(left_set)))}|"
            f"{','.join(map(str, sorted(right_set)))}"
        )

    return sha256("\n".join(digest_rows).encode()).hexdigest()


def main() -> None:
    """Build and audit the finite certificate."""
    witnesses = construct_witnesses()
    digest = verify_witnesses(witnesses)
    print("[PASS] 32 distinct labels in F_17^* x {0,1}")
    print("[PASS] Q = F_17 x {7,8} has 34 quotient vertices")
    print("[PASS] all C(34,2) = 561 pairs have explicit Johnson-edge witnesses")
    print("[PASS] every witness is a 15-set core plus one exchanged point")
    print("[PASS] every completed set has the requested additive syndrome")
    print(f"canonical witness SHA-256: {digest}")
    print("TWO-LAYER ADDITIVE SYNDROME QUOTIENT CONTAINS K_34")
    print("This excludes that construction family only; #835 remains open.")


if __name__ == "__main__":
    main()
