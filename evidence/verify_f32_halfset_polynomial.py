#!/usr/bin/env python3
"""Verify the F_32 half-set-polynomial 17-value no-go."""

from collections import defaultdict


MODULUS = 0b100101  # x^5 + x^2 + 1


def multiply(left, right):
    out = 0
    while right:
        if right & 1:
            out ^= left
        right >>= 1
        left <<= 1
        if left & 32:
            left ^= MODULUS
    return out & 31


def power(value, exponent):
    out = 1
    while exponent:
        if exponent & 1:
            out = multiply(out, value)
        value = multiply(value, value)
        exponent >>= 1
    return out


def inverse(value):
    assert value
    return power(value, 30)


def trace(value):
    out = 0
    conjugate = value
    for _ in range(5):
        out ^= conjugate
        conjugate = multiply(conjugate, conjugate)
    assert out in (0, 1)
    return out


def subset_sum(subset):
    out = 0
    for value in subset:
        out ^= value
    return out


def elementary_two(subset):
    values = sorted(subset)
    out = 0
    for i, left in enumerate(values):
        for right in values[i + 1 :]:
            out ^= multiply(left, right)
    return out


def candidate_colour(subset):
    first = subset_sum(subset)
    if first == 0:
        return None
    second = elementary_two(subset)
    first_squared = multiply(first, first)
    z = multiply(second, inverse(first_squared))
    colour = multiply(z, z) ^ z ^ 1
    assert trace(colour) == 1
    return colour


def main():
    trace_one = {value for value in range(32) if trace(value) == 1}
    assert len(trace_one) == 16

    base = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 23}
    assert len(base) == 15
    assert subset_sum(base) == 11
    assert 11 in base

    cells = defaultdict(list)
    for extension in range(32):
        if extension not in base:
            cells[candidate_colour(base | {extension})].append(extension)

    assert None not in cells
    assert sum(len(cell) for cell in cells.values()) == 17
    assert len(cells) == 13 < 17
    assert cells[8] == [25, 28]
    assert cells[14] == [13, 15]
    assert all(colour in trace_one for colour in cells)

    print("F_32 half-set candidate: REJECTED")
    print("base xor = 11 belongs to the base, so infinity is absent")
    print("17 extensions use only {} distinct trace-one values".format(len(cells)))
    print("explicit collisions: 25/28 -> 8 and 13/15 -> 14")


if __name__ == "__main__":
    main()
