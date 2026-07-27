#!/usr/bin/env python3
"""Audit the arithmetic and finite classification in Theorem 3.

The theorem itself is a symbolic argument.  This checker verifies its
recurrence coefficients, divisibility bound, and every integer
potential-level case allowed by the elementary nonnegativity, degree, and
triangle-parity constraints.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction


def audit_recurrence() -> None:
    """Check the coefficient of every edge defect in (19)."""

    alpha = {2: Fraction(0)}
    beta = {2: Fraction(1)}
    for size in range(3, 12):
        alpha[size] = (
            Fraction(math.comb(15, size - 2), size - 1)
            - Fraction(size, size - 1) * alpha[size - 1]
        )
        beta[size] = -Fraction(size - 2, size - 1) * beta[size - 1]
        assert beta[size] == Fraction((-1) ** (size - 2), size - 1)

    modulus = math.lcm(*range(2, 11))
    assert modulus == 2520
    assert modulus > 30
    print(
        "j=10 recurrence:",
        "edge coefficients verified for s=3..11;",
        "lcm(2..10)=2520>30: PASS",
    )


def edge_weight(k: int, high_a: bool, high_b: bool) -> int:
    return k + int(high_a) + int(high_b)


def admissible_type(high_count: int, k: int) -> bool:
    """Test exactly the elementary constraints used after (25)."""

    high = set(range(high_count))
    weights = {
        (a, b): edge_weight(k, a in high, b in high)
        for a, b in itertools.combinations(range(13), 2)
    }
    if min(weights.values()) < 0:
        return False

    for a in range(13):
        degree = sum(
            weights[tuple(sorted((a, b)))] for b in range(13) if b != a
        )
        if degree > 15:
            return False

    # Equation (26) forces every triangle edge sum to be odd.
    return all(
        (
            weights[(a, b)]
            + weights[(a, c)]
            + weights[(b, c)]
        )
        % 2
        == 1
        for a, b, c in itertools.combinations(range(13), 3)
    )


def audit_potential_classification() -> None:
    """Enumerate all translated one-level and two-level cases."""

    one_level = [
        k
        for k in range(-3, 4)
        if admissible_type(high_count=0, k=k)
    ]
    assert one_level == [1]

    two_level = [
        (high_count, k)
        for high_count in range(1, 13)
        for k in range(-3, 4)
        if admissible_type(high_count=high_count, k=k)
    ]
    assert two_level == [(12, -1)]
    print(
        "potential classification:",
        "only all-one K13 and one deleted-star K13 survive: PASS",
    )


def audit_global_count() -> None:
    """Check the final equations h_a+h_b=2."""

    # Three pair equations already force any three h-values to one.
    for h0 in range(18):
        for h1 in range(18):
            for h2 in range(18):
                if h0 + h1 == h0 + h2 == h1 + h2 == 2:
                    assert (h0, h1, h2) == (1, 1, 1)

    h = [1] * 13
    full_colors = 17 - sum(h)
    assert full_colors == 4
    assert all(
        full_colors + sum(
            1 for center in range(13) if center not in {a, b}
        )
        == 15
        for a, b in itertools.combinations(range(13), 2)
    )
    print(
        "global color count:",
        "13 uniquely centered deleted stars and 4 full colors: PASS",
    )


def main() -> int:
    audit_recurrence()
    audit_potential_classification()
    audit_global_count()
    print(
        "scope:",
        "j=10 -> j=11 top-properness is audited conditionally;",
        "the lower tower and #835 are not constructed",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
