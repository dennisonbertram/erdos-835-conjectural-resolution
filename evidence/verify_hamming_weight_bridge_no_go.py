#!/usr/bin/env python3
"""Independent arithmetic and finite-control checks for the Hamming bridge no-go.

The all-m=5 obstruction is the elementary pairing proof in the companion
note.  This script checks its local mechanism exhaustively for m=4, verifies
the m=3 Fano positive control, and validates the exact Hamming enumerator
numbers used in the note.
"""

from __future__ import annotations

from itertools import combinations
from math import comb


def xorsum(values: tuple[int, ...] | set[int]) -> int:
    total = 0
    for value in values:
        total ^= value
    return total


def hamming_weight_count(m: int, weight: int) -> int:
    """MacWilliams enumerator for Ham(m,2), whose dual has weight 2^(m-1)."""
    n = (1 << m) - 1
    q = 1 << (m - 1)
    alternating = sum(
        (-1) ** j * comb(q, j) * comb(n - q, weight - j)
        for j in range(max(0, weight - (n - q)), min(q, weight) + 1)
    )
    numerator = comb(n, weight) + ((1 << m) - 1) * alternating
    assert numerator % (1 << m) == 0
    return numerator // (1 << m)


def codeword_supports(m: int, weight: int) -> list[tuple[int, ...]]:
    return [
        support
        for support in combinations(range(1, 1 << m), weight)
        if xorsum(support) == 0
    ]


def local_conflict(core: tuple[int, ...], added: int) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    """Return y,T,D where enlarged core and retained D share T.

    Raises if the impossible translation-invariance alternative occurred.
    """
    cset = set(core)
    assert added not in cset and xorsum(core) == 0
    for y in core:
        tset = (cset - {y}) | {added}
        syndrome = added ^ y
        if syndrome not in tset:
            dset = tset | {syndrome}
            assert len(tset) == len(core)
            assert len(dset) == len(core) + 1
            assert xorsum(dset) == 0
            assert dset != cset | {added}
            return y, tuple(sorted(tset)), tuple(sorted(dset))
    raise AssertionError("would force an impossible nonzero translation period")


def check_enumerator_counts() -> None:
    expected = {
        3: (0, 7, 7),
        4: (280, 435, 715),
        5: (8_280_720, 9_398_115, 17_678_835),
    }
    for m, (want_low, want_high, want_total) in expected.items():
        n = (1 << m) - 1
        k = 1 << (m - 1)
        low = hamming_weight_count(m, k - 2)
        high = hamming_weight_count(m, k - 1)
        assert (low, high, low + high) == (want_low, want_high, want_total)
        assert want_total == comb(n, k - 2) // (k - 1)


def check_fano_control() -> None:
    blocks = codeword_supports(3, 3)
    assert len(blocks) == 7
    pair_counts = {pair: 0 for pair in combinations(range(1, 8), 2)}
    for block in blocks:
        for pair in combinations(block, 2):
            pair_counts[pair] += 1
    assert set(pair_counts.values()) == {1}


def check_m4_all_local_enlargements() -> None:
    cores = codeword_supports(4, 6)
    retained = {frozenset(block) for block in codeword_supports(4, 7)}
    assert len(cores) == 280 and len(retained) == 435
    checks = 0
    for core in cores:
        cset = set(core)
        for added in set(range(1, 16)) - cset:
            _, face, conflict = local_conflict(core, added)
            enlarged = frozenset(cset | {added})
            assert frozenset(conflict) in retained
            assert set(face) <= enlarged and set(face) <= set(conflict)
            assert len(enlarged & set(conflict)) == 6
            checks += 1
    assert checks == 280 * 9


def check_m5_concrete_instance() -> None:
    # A 14-word of Ham(5,2); the general proof handles all 8,280,720 cores.
    core = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 28)
    assert len(core) == 14 and xorsum(core) == 0
    for added in set(range(1, 32)) - set(core):
        _, face, conflict = local_conflict(core, added)
        assert xorsum(conflict) == 0
        assert len(face) == 14 and len(conflict) == 15


def main() -> None:
    check_enumerator_counts()
    check_fano_control()
    check_m4_all_local_enlargements()
    check_m5_concrete_instance()
    print("PASS: Hamming support-preserving bridge obstruction verified")


if __name__ == "__main__":
    main()
