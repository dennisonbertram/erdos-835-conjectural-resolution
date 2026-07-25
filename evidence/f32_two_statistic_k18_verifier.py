#!/usr/bin/env python3
"""Verify an explicit actual-edge K18 in the (e1, e8+e1^8) quotient.

This is a certificate checker, not a search.  All finite-field arithmetic,
all elementary symmetric coefficients, and all 153 Johnson-graph edges are
recomputed directly from the embedded 17-subsets.
"""

from itertools import combinations


MODULUS = 0b100101  # X^5 + X^2 + 1

# The first seventeen quotient vertices are (a, 1), in this order.  They are
# realized by deleting a from BASE_ROOTS.  The eighteenth is EXTERNAL_STATE.
BASE_ROOTS = (
    0, 1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23, 24, 26, 28, 30,
)
EXTERNAL_STATE = (29, 27)

# Row i is a 17-set, encoded as a 32-bit characteristic mask, with two
# deletions whose statistics are (BASE_ROOTS[i], 1) and EXTERNAL_STATE.
EXTENSION_WITNESS_MASKS = (
    2031344421,
    2746287807,
    3516397638,
    2787818318,
    1635163064,
    3871419836,
    3880068826,
    764258591,
    21756349,
    3509571678,
    700097723,
    3969021235,
    3454195298,
    1862479197,
    21756349,
    4149293654,
    1122617591,
)
EXTENSION_DELETIONS = (
    (9, 20),
    (1, 29),
    (24, 6),
    (17, 9),
    (4, 30),
    (5, 16),
    (16, 7),
    (11, 26),
    (22, 5),
    (14, 2),
    (21, 27),
    (23, 31),
    (6, 12),
    (29, 24),
    (2, 5),
    (28, 29),
    (7, 4),
)


def multiply(left: int, right: int) -> int:
    """Polynomial multiplication followed by direct long-division."""

    raw = 0
    for bit in range(5):
        if right >> bit & 1:
            raw ^= left << bit
    for degree in range(8, 4, -1):
        if raw >> degree & 1:
            raw ^= MODULUS << (degree - 5)
    assert raw < 32
    return raw


def power(value: int, exponent: int) -> int:
    answer = 1
    while exponent:
        if exponent & 1:
            answer = multiply(answer, value)
        value = multiply(value, value)
        exponent >>= 1
    return answer


def trace(value: int) -> int:
    answer = 0
    current = value
    for _ in range(5):
        answer ^= current
        current = multiply(current, current)
    assert answer in (0, 1)
    return answer


def statistic(points: frozenset[int]) -> tuple[int, int]:
    """Compute (e_1, e_8 + e_1^8) from the definition."""

    assert len(points) == 16
    coefficients = [1] + [0] * 8
    for point in sorted(points):
        for degree in range(8, 0, -1):
            coefficients[degree] ^= multiply(
                point, coefficients[degree - 1]
            )
    first = coefficients[1]
    return first, coefficients[8] ^ power(first, 8)


def points_from_mask(mask: int) -> frozenset[int]:
    assert 0 <= mask < 1 << 32
    points = frozenset(point for point in range(32) if mask >> point & 1)
    assert len(points) == 17
    return points


def deletion_realizations(
    roots: frozenset[int],
) -> dict[tuple[int, int], frozenset[int]]:
    """Map every deletion statistic to its 16-set realization."""

    answer = {}
    for deleted in roots:
        subset = roots - {deleted}
        state = statistic(subset)
        assert state not in answer
        answer[state] = subset
    assert len(answer) == 17
    return answer


def main() -> None:
    # Sanity-check that the chosen polynomial really gives a field of order 32:
    # every nonzero element has the expected multiplicative inverse.
    for value in range(1, 32):
        assert multiply(value, power(value, 30)) == 1

    base_set = frozenset(BASE_ROOTS)
    assert len(base_set) == 17
    assert base_set == {0} | {x for x in range(1, 32) if trace(x) == 1}
    base_realizations = deletion_realizations(base_set)
    base_states = tuple((parameter, 1) for parameter in BASE_ROOTS)
    assert set(base_realizations) == set(base_states)

    verified_edges = set()

    # Any two different deletions from one 17-set share exactly fifteen points.
    for left, right in combinations(base_states, 2):
        left_set = base_realizations[left]
        right_set = base_realizations[right]
        assert len(left_set & right_set) == 15
        verified_edges.add(frozenset((left, right)))

    assert len(EXTENSION_WITNESS_MASKS) == len(base_states)
    assert len(EXTENSION_DELETIONS) == len(base_states)
    rows = zip(
        base_states, EXTENSION_WITNESS_MASKS, EXTENSION_DELETIONS
    )
    for base_state, mask, (base_deleted, external_deleted) in rows:
        roots = points_from_mask(mask)
        assert base_deleted in roots
        assert external_deleted in roots
        assert statistic(roots - {base_deleted}) == base_state
        assert statistic(roots - {external_deleted}) == EXTERNAL_STATE
        realizations = deletion_realizations(roots)
        assert base_state in realizations
        assert EXTERNAL_STATE in realizations
        left_set = realizations[base_state]
        right_set = realizations[EXTERNAL_STATE]
        assert left_set != right_set
        assert len(left_set & right_set) == 15
        verified_edges.add(frozenset((base_state, EXTERNAL_STATE)))

    clique_states = set(base_states) | {EXTERNAL_STATE}
    assert len(clique_states) == 18
    assert len(verified_edges) == 18 * 17 // 2
    for left, right in combinations(clique_states, 2):
        assert frozenset((left, right)) in verified_edges

    print("F_32 two-statistic actual-edge K18 certificate: PASS")
    print("quotient vertices:", len(clique_states))
    print("Johnson edges checked:", len(verified_edges))
    print("base 17-set:", BASE_ROOTS)
    print("external quotient state:", EXTERNAL_STATE)
    print("consequence: no 17-colouring can depend only on (e1, e8+e1^8)")


if __name__ == "__main__":
    main()
