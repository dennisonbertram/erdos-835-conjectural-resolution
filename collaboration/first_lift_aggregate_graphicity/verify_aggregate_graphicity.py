#!/usr/bin/env python3
"""Exhaust the relaxed aggregate degree sequences in NOTE.md."""

from __future__ import annotations

import itertools


N_VERTICES = 13
N_COLOURS = 17
FORBIDDEN_PER_VERTEX = 5


def erdos_gallai_margin(degrees: tuple[int, ...]) -> int:
    """Minimum RHS-LHS over the Erdős--Gallai inequalities.

    The caller supplies a nonincreasing sequence with even sum.
    Nonnegative return value is equivalent to graphicality.
    """
    assert tuple(sorted(degrees, reverse=True)) == degrees
    assert sum(degrees) % 2 == 0
    best = None
    for k in range(1, len(degrees) + 1):
        left = sum(degrees[:k])
        right = k * (k - 1) + sum(min(degree, k) for degree in degrees[k:])
        margin = right - left
        best = margin if best is None else min(best, margin)
    assert best is not None
    return best


def havel_hakimi(degrees: tuple[int, ...]) -> bool:
    """Independent constructive graphicality check."""
    remaining = list(degrees)
    while remaining:
        remaining.sort(reverse=True)
        degree = remaining.pop(0)
        if degree < 0 or degree > len(remaining):
            return False
        for index in range(degree):
            remaining[index] -= 1
            if remaining[index] < 0:
                return False
    return True


def relaxed_b_sequences(r: int):
    """All sorted b-sequences satisfying (3)--(4) of NOTE.md."""
    lower_entry = max(0, r - (N_VERTICES - 1))
    upper_entry = min(FORBIDDEN_PER_VERTEX, r)
    lower_sum = max(r, FORBIDDEN_PER_VERTEX * r - 20)
    upper_sum = min(FORBIDDEN_PER_VERTEX * r, r + 48)

    for values in itertools.combinations_with_replacement(
        range(lower_entry, upper_entry + 1),
        N_VERTICES,
    ):
        total = sum(values)
        if not lower_sum <= total <= upper_sum:
            continue
        if (total - r) % 2:
            continue
        yield values


def main() -> int:
    grand_total = 0
    global_margin = None
    global_witness = None

    for r in range(N_COLOURS + 1):
        count = 0
        local_margin = None
        local_witness = None
        for forbidden_counts in relaxed_b_sequences(r):
            degrees = tuple(r - value for value in forbidden_counts)
            assert all(0 <= degree <= N_VERTICES - 1 for degree in degrees)
            assert sum(degrees) % 2 == 0
            margin = erdos_gallai_margin(degrees)
            assert margin >= 0, (r, forbidden_counts, degrees, margin)
            assert havel_hakimi(degrees), (r, forbidden_counts, degrees)
            count += 1
            if local_margin is None or margin < local_margin:
                local_margin = margin
                local_witness = degrees

        assert count > 0
        print(
            f"r={r:2d} relaxed_sequences={count:5d} "
            f"minimum_EG_margin={local_margin:2d} witness={local_witness}"
        )
        grand_total += count
        if global_margin is None or local_margin < global_margin:
            global_margin = local_margin
            global_witness = (r, local_witness)

    assert grand_total == 18_032
    print(f"total relaxed sequences checked: {grand_total}")
    print(
        "minimum Erdős-Gallai margin:",
        global_margin,
        "at",
        global_witness,
    )
    print("aggregate graphicality over the full relaxation: PASS")
    print("scope: necessary aggregate test only; simultaneous packing remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
