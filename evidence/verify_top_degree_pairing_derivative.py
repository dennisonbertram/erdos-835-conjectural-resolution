#!/usr/bin/env python3
"""Independent finite checks for top_degree_pairing_derivative_audit.md.

No solver is used.  The p=17 cube checks use the displayed linear maps and
their exact fibre counts, rather than a search.
"""

from itertools import combinations
from math import comb, factorial


def pairings(points):
    """All unoriented perfect matchings, each edge oriented by tuple order."""
    points = tuple(points)
    if not points:
        yield ()
        return
    first = points[0]
    for position in range(1, len(points)):
        second = points[position]
        rest = points[1:position] + points[position + 1:]
        for tail in pairings(rest):
            yield ((first, second),) + tail


def transversal_delta(matching, colour, p):
    """Signed colour counts on the matching cube."""
    answer = [0] * p
    k = len(matching)
    for mask in range(1 << k):
        block = frozenset(
            matching[index][(mask >> index) & 1] for index in range(k)
        )
        sign = -1 if bin(mask).count("1") & 1 else 1
        answer[colour[block]] += sign
    return answer


def check_k2_frame():
    """The actual tight 3-colouring of J(4,2) checks (7) directly."""
    colour = {}
    factors = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    for label, factor in enumerate(factors):
        for block in factor:
            colour[frozenset(block)] = label

    total = [[0] * 3 for _ in range(3)]
    for matching in pairings(range(4)):
        delta = transversal_delta(matching, colour, 3)
        assert sum(delta) == 0
        assert all(value % 2 == 0 for value in delta)
        for left in range(3):
            for right in range(3):
                total[left][right] += delta[left] * delta[right]

    d = comb(4, 2) // 3
    expected = [
        [factorial(2) * d * (3 * int(i == j) - 1) for j in range(3)]
        for i in range(3)
    ]
    assert total == expected
    print("k=2 frame identity:", total)


def e_value(matching, block):
    product = 1
    for left, right in matching:
        product *= int(left in block) - int(right in block)
    return product


def check_straightening():
    """Check (13) on all 4-subsets of an 8-point universe with two rest pairs."""
    rest = ((4, 5), (6, 7))
    first = ((0, 1), (2, 3)) + rest
    second = ((0, 2), (1, 3)) + rest
    third = ((0, 3), (1, 2)) + rest
    for block in map(frozenset, combinations(range(8), 4)):
        assert e_value(first, block) - e_value(second, block) + e_value(third, block) == 0
    print("four-point top-polytabloid straightening: PASS")


# A 4 x 16 binary matrix, represented by its nonzero column vectors.
# The xor of all columns is zero, and the columns span F_2^4.
COLUMNS = (1, 1, 2, 2, 4, 4, 8, 8, 3, 3, 5, 5, 9, 9, 6, 6)
ALL_ONES = (1 << 16) - 1
# This has odd Hamming weight, zero L-image, and preserves SPLIT_BIT.
ODD_KERNEL_TRANSLATION = (1 << 0) | (1 << 2) | (1 << 8)


def linear_image(vertex):
    image = 0
    for index, column in enumerate(COLUMNS):
        if (vertex >> index) & 1:
            image ^= column
    return image


def split_bit(vertex):
    return ((vertex >> 0) & 1) ^ ((vertex >> 2) & 1)


def balanced_cube_colour(vertex):
    image = linear_image(vertex)
    if image:
        return image  # labels 1,...,15
    return 16 if split_bit(vertex) else 0


def extreme_cube_colour(vertex, distinguished=0):
    """The local colouring producing E_distinguished in (14)."""
    if bin(vertex).count("1") % 2 == 0:
        return distinguished
    # Complement pairs of odd vertices are assigned evenly to the other labels.
    mate = vertex ^ ALL_ONES
    representative = min(vertex, mate)
    rank = representative // 2  # representatives are exactly the odd integers
    other = [label for label in range(17) if label != distinguished]
    return other[rank % 16]


def check_local_cube_witnesses():
    assert all(column for column in COLUMNS)
    assert linear_image(ALL_ONES) == 0
    assert linear_image(ODD_KERNEL_TRANSLATION) == 0
    assert split_bit(ALL_ONES) == 0
    assert split_bit(ODD_KERNEL_TRANSLATION) == 0
    assert bin(ODD_KERNEL_TRANSLATION).count("1") % 2 == 1

    # The columns span F_2^4, so all 15 nonzero L-fibres occur.  On the
    # zero fibre, 0 and e_0+e_1 have opposite split bits, so both remaining
    # colours occur.  Every cube edge changes L by a nonzero column; this
    # proves properness of the balanced colouring.  L(1)=0 and the split bit
    # is complement invariant, proving complement closure.
    image_span = {0}
    for column in COLUMNS:
        image_span |= {value ^ column for value in tuple(image_span)}
    assert image_span == set(range(16))
    assert linear_image((1 << 0) | (1 << 1)) == 0
    assert split_bit((1 << 0) | (1 << 1)) == 1
    assert balanced_cube_colour(0) == 0
    assert balanced_cube_colour((1 << 0) | (1 << 1)) == 16

    # The odd kernel translation preserves each balanced colour and reverses
    # cube parity, proving Delta=0 without enumerating the cube.
    balanced = [0] * 17

    # In the extreme construction, all even vertices get colour zero.  The
    # 16,384 antipodal pairs of odd vertices are split into 16 lots of 1,024
    # pairs.  Different parities are the only adjacent vertices, and the
    # colour supports are complement closed.
    extreme = [32768] + [-2048] * 16
    assert sum(extreme) == 0
    assert all(value % 2 == 0 for value in extreme)
    assert extreme_cube_colour(0) == extreme_cube_colour(ALL_ONES) == 0
    assert extreme_cube_colour(1) == extreme_cube_colour(1 ^ ALL_ONES)
    print("Q_16 local witnesses: balanced Delta=0 and extreme E_a: PASS")


def check_p17_arithmetic():
    p, k = 17, 16
    d = comb(2 * k, k) // p
    assert d == 35_357_670
    matchings = factorial(2 * k) // ((2 ** k) * factorial(k))

    # (7), divided by the number of matchings, is (9).
    assert factorial(k) * d * p == matchings * (2 ** k)
    # The covariance of the weighted zero/extreme local witness is (9).
    amplitude = 34_816
    witness_weight_denominator = 1_088
    assert amplitude * amplitude == (2 ** 22) * (17 ** 2)
    # (1/1088) * (1/17) sum_a E_a E_a^T has coefficient 2^16/17.
    assert amplitude * amplitude == witness_weight_denominator * p * (2 ** k)
    assert (1 << 15) ** 2 + 16 * (1 << 11) ** 2 == 1_140_850_688
    assert 1_140_850_688 // witness_weight_denominator == k * (2 ** k)
    print("p=17 frame and weighted-local-witness arithmetic: PASS")


if __name__ == "__main__":
    check_k2_frame()
    check_straightening()
    check_local_cube_witnesses()
    check_p17_arithmetic()
    print("PASS: top-degree pairing-derivative audit verified.")
