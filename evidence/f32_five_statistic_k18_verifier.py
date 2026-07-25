#!/usr/bin/env python3
"""Verify an actual-edge K18 in the five-statistic F_32 quotient.

For a 16-set S define

    sigma(S) = (e1(S), e2(S), e3(S), e4(S), e8(S) + e1(S)^8).

The certificate consists of eighteen quotient states and three 15-set
bases.  For every pair of states, at least one base excludes both of their
parameters.  Adding the two parameters separately to that base gives two
16-sets with intersection size fifteen and with the two claimed states.
"""

from itertools import combinations


MODULUS = 0b100101  # X^5 + X^2 + 1.

# Each pair is (added field element, lambda).
PARAMETER_LAMBDA = (
    (31, 31),
    (26, 28),
    (25, 4),
    (24, 9),
    (23, 14),
    (22, 3),
    (19, 0),
    (17, 21),
    (16, 24),
    (13, 22),
    (12, 27),
    (11, 13),
    (10, 0),
    (9, 24),
    (6, 31),
    (2, 17),
    (1, 9),
    (0, 4),
)

# Characteristic masks of three 15-subsets of F_32.
BASE_MASKS = (
    0x7975CD00,
    0x149693B9,
    0xFA3041BA,
)


def multiply(left: int, right: int) -> int:
    """Polynomial multiplication followed by direct long division."""

    raw = 0
    for bit in range(5):
        if right >> bit & 1:
            raw ^= left << bit
    for degree in range(8, 4, -1):
        if raw >> degree & 1:
            raw ^= MODULUS << (degree - 5)
    assert 0 <= raw < 32
    return raw


def power(value: int, exponent: int) -> int:
    answer = 1
    while exponent:
        if exponent & 1:
            answer = multiply(answer, value)
        value = multiply(value, value)
        exponent >>= 1
    return answer


def coefficients(points: frozenset[int]) -> tuple[int, ...]:
    answer = [1] + [0] * 8
    for point in sorted(points):
        for degree in range(8, 0, -1):
            answer[degree] ^= multiply(
                point, answer[degree - 1]
            )
    return tuple(answer)


def statistic(
    points: frozenset[int],
) -> tuple[int, int, int, int, int]:
    assert len(points) == 16
    elementary = coefficients(points)
    first = elementary[1]
    return (
        first,
        elementary[2],
        elementary[3],
        elementary[4],
        elementary[8] ^ power(first, 8),
    )


def points_from_mask(mask: int) -> frozenset[int]:
    assert 0 <= mask < 1 << 32
    points = frozenset(
        point for point in range(32) if mask >> point & 1
    )
    assert len(points) == 15
    return points


def claimed_state(parameter: int, lam: int) -> tuple[int, ...]:
    # Every base has prefix 1 + t.  Adding parameter x multiplies it
    # by 1+x*t, giving (e1,e2,e3,e4)=(1+x,x,0,0).
    return (1 ^ parameter, parameter, 0, 0, lam)


def main() -> None:
    for value in range(1, 32):
        assert power(value, 31) == 1

    bases = tuple(points_from_mask(mask) for mask in BASE_MASKS)
    for base in bases:
        assert coefficients(base)[:5] == (1, 1, 0, 0, 0)

    states = tuple(
        claimed_state(parameter, lam)
        for parameter, lam in PARAMETER_LAMBDA
    )
    assert len(states) == len(set(states)) == 18
    parameters = tuple(
        parameter for parameter, _ in PARAMETER_LAMBDA
    )
    assert len(parameters) == len(set(parameters)) == 18

    # First verify every available base realizes exactly the same state
    # for a given parameter.
    realizations = {}
    for index, ((parameter, _), state) in enumerate(
        zip(PARAMETER_LAMBDA, states)
    ):
        usable = []
        for base_index, base in enumerate(bases):
            if parameter in base:
                continue
            half_set = base | {parameter}
            assert len(half_set) == 16
            assert statistic(half_set) == state
            usable.append(base_index)
        assert usable
        realizations[index] = tuple(usable)

    # Then verify all 153 actual Johnson edges.
    edge_witnesses = {}
    for left, right in combinations(range(18), 2):
        left_parameter = parameters[left]
        right_parameter = parameters[right]
        usable = [
            base_index
            for base_index, base in enumerate(bases)
            if left_parameter not in base
            and right_parameter not in base
        ]
        assert usable
        base_index = usable[0]
        base = bases[base_index]
        left_half = base | {left_parameter}
        right_half = base | {right_parameter}
        assert len(left_half & right_half) == 15
        assert statistic(left_half) == states[left]
        assert statistic(right_half) == states[right]
        edge_witnesses[(left, right)] = base_index

    assert len(edge_witnesses) == 18 * 17 // 2
    usage = tuple(
        sum(base_index == chosen
            for chosen in edge_witnesses.values())
        for base_index in range(3)
    )
    print("F_32 five-statistic actual-edge K18 certificate: PASS")
    print("quotient vertices:", len(states))
    print("Johnson edges checked:", len(edge_witnesses))
    print("15-set base masks:", tuple(hex(mask) for mask in BASE_MASKS))
    print("first-witness usage by base:", usage)
    print(
        "consequence: every colouring depending only on "
        "(e1,e2,e3,e4,e8+e1^8) needs at least 18 colours"
    )


if __name__ == "__main__":
    main()
