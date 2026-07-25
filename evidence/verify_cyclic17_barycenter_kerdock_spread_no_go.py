#!/usr/bin/env python3
"""Exact audit for cyclic17_barycenter_kerdock_spread_no_go.md."""

from itertools import combinations

P = 17


def inv(a: int) -> int:
    assert a % P
    return pow(a, -1, P)


def rhs_centered(A: tuple[int, ...]) -> frozenset[int]:
    t = len(A)
    s = sum(A) % P
    return frozenset(((a - s * inv(t)) * inv(t + 1)) % P for a in A)


def main() -> None:
    # Equation (3) minus equation (4), for every possible cyclic part.
    for t in range(1, 16):
        for A in combinations(range(P), t):
            s = sum(A) % P
            missing_from_cyclic = frozenset(
                ((s + a) * inv(t + 1) - s * inv(t)) % P for a in A
            )
            assert missing_from_cyclic == rhs_centered(A)

    one = rhs_centered((0, 1))
    two = rhs_centered((0, 2))
    assert one == frozenset({(-inv(6)) % P, inv(6) % P})
    assert two == frozenset({(-2 * inv(6)) % P, 2 * inv(6) % P})
    assert one != two
    print("PASS: cyclic-17 barycentre offset ansatz contradicts its t=2 stars")


if __name__ == "__main__":
    main()
