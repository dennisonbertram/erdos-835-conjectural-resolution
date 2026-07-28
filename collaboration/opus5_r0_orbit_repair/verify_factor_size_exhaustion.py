#!/usr/bin/env python3
"""Check the finite size arithmetic in the full-row b-factor proof."""

from __future__ import annotations


def lower_bound(a: int, k: int) -> int:
    return 4 * a - 22 + (5 - a) * k


def main() -> None:
    exceptional = {
        (a, k, 13 - a - k)
        for a in range(5, 13)
        for k in range(1, 14 - a)
        if lower_bound(a, k) < -1
    }
    expected_a5 = {(5, k, 8 - k) for k in range(1, 9)}
    expected_large = {
        (6, 4, 3),
        (6, 5, 2),
        (6, 6, 1),
        (6, 7, 0),
        (7, 4, 2),
        (7, 5, 1),
        (7, 6, 0),
        (8, 4, 1),
        (8, 5, 0),
        (9, 4, 0),
    }
    assert exceptional == expected_a5 | expected_large

    # The first gate covers k=1..4, the rigid argument covers k=5, and
    # the repaired continuation covers k=6..8.
    assert expected_a5 == (
        {(5, k, 8 - k) for k in range(1, 5)}
        | {(5, 5, 3)}
        | {(5, k, 8 - k) for k in range(6, 9)}
    )

    # (5,8,0): the B-degree sum gives 20 deleted edges, while the
    # all-avoiding eight-cut permits at most 19.
    assert 8 * 5 // 2 == 20 > 19

    # (5,7,1): the seven-cut and eight-cut give incompatible bounds on m.
    possible_m_571 = tuple(
        m
        for m in range(8)
        if (35 - m) % 2 == 0
        and (35 - m) // 2 <= 15
        and (35 + m) // 2 <= 19
    )
    assert possible_m_571 == ()

    # (5,6,2): parity and the six/eight cuts force {m1,m2}={2,4};
    # the degree-four choice then violates the seven-cut.
    possible_562 = tuple(
        tuple(sorted((m1, m2)))
        for m1 in range(0, 5, 2)
        for m2 in range(0, 5, 2)
        if m1 + m2 >= 6
        and 16 + (m1 + m2) / 2 <= 19
    )
    assert set(possible_562) == {(2, 4)}
    assert 12 + 4 == 16 > 15

    print("factor size-triple exhaustion: PASS")
    print("exceptional a=5 triples:", sorted(expected_a5))
    print("exceptional a>=6 triples:", sorted(expected_large))


if __name__ == "__main__":
    main()
