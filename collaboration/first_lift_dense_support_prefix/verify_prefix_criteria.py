#!/usr/bin/env python3
"""Check the finite order-18 arithmetic in NOTE.md.

This is not a substitute for the Dirac-theorem proof of the packing lemma.
It exhaustively checks the profile and ordering consequences used there.
"""

from __future__ import annotations

import itertools


def prefix_condition(sizes: tuple[int, ...]) -> bool:
    """Condition |V_i| >= 2i after nondecreasing ordering."""
    return all(size >= 2 * index for index, size in enumerate(sorted(sizes), 1))


def profiles() -> list[tuple[int, int, int]]:
    out = []
    # n_s is the number of colours with support size s.  There are seventeen
    # colours and 13*12 total support incidences.
    for n8 in range(18):
        for n10 in range(18 - n8):
            n12 = 17 - n8 - n10
            if 8 * n8 + 10 * n10 + 12 * n12 == 13 * 12:
                out.append((n8, n10, n12))
    return out


def main() -> int:
    got = profiles()
    expected = [(7 + q, 10 - 2 * q, q) for q in range(6)]
    assert got == expected

    palette = (8, 10, 12)
    for length in range(1, 5):
        assert all(
            prefix_condition(sizes)
            for sizes in itertools.combinations_with_replacement(palette, length)
        )

    for sizes in itertools.combinations_with_replacement(palette, 5):
        if max(sizes) >= 10:
            assert prefix_condition(sizes)

    for sizes in itertools.combinations_with_replacement(palette, 6):
        ordered = sorted(sizes)
        if ordered[-1] == 12 and ordered[-2] >= 10:
            assert prefix_condition(sizes)

    for q, (n8, n10, n12) in enumerate(got):
        full = [8] * n8 + [10] * n10 + [12] * n12
        assert any(
            prefix_condition(tuple(full[index] for index in choice))
            for choice in itertools.combinations(range(17), 5)
        )
        if q >= 1:
            assert any(
                prefix_condition(tuple(full[index] for index in choice))
                for choice in itertools.combinations(range(17), 6)
            )

    print("profiles:", got)
    print("all subfamilies of at most four satisfy the prefix condition: PASS")
    print("stated five- and six-colour criteria: PASS")
    print("every profile has a five-prefix; q>=1 has a six-prefix: PASS")
    print("scope: dense prefix only; seventeen-colour completion remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
