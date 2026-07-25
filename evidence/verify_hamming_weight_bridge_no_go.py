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


def local_coset_conflict(
    core: tuple[int, ...], added: int, syndrome: int
) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    """Return an overlapping weight-(|core|+1) support in the same coset.

    The exception is exactly the local escape C+added=C.  The note proves
    that this requires added=syndrome and a translation-periodic core.
    """
    cset = set(core)
    assert added not in cset and xorsum(core) == syndrome
    for y in core:
        face = (cset - {y}) | {added}
        new_point = added ^ y
        if new_point not in face:
            conflict = face | {new_point}
            assert len(conflict) == len(core) + 1
            assert xorsum(conflict) == syndrome
            assert conflict != cset | {added}
            return y, tuple(sorted(face)), tuple(sorted(conflict))
    raise AssertionError("local escape: core is translation-periodic")


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


def check_m4_coset_extension() -> None:
    """Exhaust the coset version in the small n=15 control."""
    labels = set(range(1, 16))
    low_by_syndrome = {h: [] for h in range(16)}
    high_by_syndrome = {h: set() for h in range(16)}
    for support in combinations(range(1, 16), 6):
        low_by_syndrome[xorsum(support)].append(support)
    for support in combinations(range(1, 16), 7):
        high_by_syndrome[xorsum(support)].add(frozenset(support))

    assert len(low_by_syndrome[0]) == 280
    assert len(high_by_syndrome[0]) == 435
    for h in range(1, 16):
        assert len(low_by_syndrome[h]) == 315
        assert len(high_by_syndrome[h]) == 400

        local_escapes = 0
        forced_conflicts = 0
        for core in low_by_syndrome[h]:
            cset = set(core)
            for added in labels - cset:
                try:
                    _, face, conflict = local_coset_conflict(core, added, h)
                except AssertionError as exc:
                    assert str(exc) == "local escape: core is translation-periodic"
                    assert added == h
                    assert {x ^ h for x in cset} == cset
                    local_escapes += 1
                    continue
                assert frozenset(conflict) in high_by_syndrome[h]
                assert set(face) <= cset | {added}
                assert set(face) <= set(conflict)
                forced_conflicts += 1
        # There are seven h-pairs away from {0,h}; choose any three.
        assert local_escapes == comb(7, 3) == 35
        assert forced_conflicts == 315 * 9 - 35


def check_m5_coset_arithmetic_and_periods() -> None:
    """Check exact coset counts and the 6,435 local escape candidates."""
    n = 31
    zero_counts = {14: 8_280_720, 15: 9_398_115}
    nonzero_counts = {}
    for weight, zero_count in zero_counts.items():
        remainder = comb(n, weight) - zero_count
        assert remainder % 31 == 0
        nonzero_counts[weight] = remainder // 31
    assert nonzero_counts == {14: 8_287_155, 15: 9_391_680}
    assert sum(nonzero_counts.values()) == 17_678_835

    h = 1
    unused = set(range(1, 32)) - {h}
    pairs = []
    while unused:
        x = min(unused)
        pair = {x, x ^ h}
        assert pair <= unused
        unused -= pair
        pairs.append(tuple(pair))
    assert len(pairs) == 15
    periodic_cores = 0
    for selected in combinations(pairs, 7):
        core = {x for pair in selected for x in pair}
        assert len(core) == 14
        assert xorsum(core) == h
        assert {x ^ h for x in core} == core
        periodic_cores += 1
    assert periodic_cores == comb(15, 7) == 6_435

    # A concrete h=1 coset core with no translation period, so it necessarily
    # creates an overlap for every possible one-point extension.
    aperiodic = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 16, 28)
    assert xorsum(aperiodic) == h
    assert all({x ^ shift for x in aperiodic} != set(aperiodic) for shift in range(1, 32))
    for added in set(range(1, 32)) - set(aperiodic):
        _, _, conflict = local_coset_conflict(aperiodic, added, h)
        assert xorsum(conflict) == h


def check_punctured_extended_identity() -> None:
    """Small exhaustive control for the shifted-label puncturing identity."""
    # With extended coordinates F_2^4, puncture at p and enumerate every
    # support on the remaining 15 coordinates.  The shifted Hamming syndrome
    # equals the extended-code syndrome after restoring p iff the support is
    # odd.
    for p in range(16):
        surviving = [x for x in range(16) if x != p]
        for mask in range(1 << len(surviving)):
            support = [x for i, x in enumerate(surviving) if mask & (1 << i)]
            shifted = xorsum(tuple(x ^ p for x in support))
            restored = xorsum(tuple(support)) ^ (p if len(support) & 1 else 0)
            assert shifted == restored


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
    check_m4_coset_extension()
    check_m5_coset_arithmetic_and_periods()
    check_punctured_extended_identity()
    check_m5_concrete_instance()
    print("PASS: Hamming support-preserving bridge obstruction verified")


if __name__ == "__main__":
    main()
