#!/usr/bin/env python3
r"""Check the F_32 seven-coefficient 32-clique certificate.

The certificate below is deliberately small and direct.  For every r in
F_32 it gives a 15-subset U_r of F_32 \ {0,1} with

    e_1(U_r) = ... = e_7(U_r) = r.

It then turns every ordered pair a != c into adjacent 16-sets whose first
seven elementary symmetric coefficients are respectively
(a,a^2,...,a^7) and (c,c^2,...,c^7).  Thus those 32 coefficient states
form a clique in the coefficient-transition graph.
"""


MODULUS = 0b100101  # X^5 + X^2 + 1


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
    answer = power(value, 30)
    assert multiply(value, answer) == 1
    return answer


def elementary_prefix(subset, length):
    """(e_1,...,e_length) in characteristic two."""

    values = [1] + [0] * length
    used = 0
    for point in subset:
        for degree in range(min(used + 1, length), 0, -1):
            values[degree] ^= multiply(point, values[degree - 1])
        used += 1
    return tuple(values[1:])


# A direct 32-row certificate.  Row r is U_r.  It was found by exact
# subset dynamic programming over F_32 \ {0,1}; the verifier needs no search.
DIAGONAL_WITNESSES = (
    (2, 4, 6, 8, 10, 12, 14, 17, 19, 21, 23, 25, 27, 29, 31),
    (3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23, 24, 26, 28, 30),
    (3, 4, 5, 8, 9, 12, 13, 18, 19, 22, 23, 26, 27, 30, 31),
    (2, 4, 5, 8, 9, 12, 13, 18, 19, 22, 23, 26, 27, 30, 31),
    (2, 3, 5, 8, 9, 10, 11, 20, 21, 22, 23, 28, 29, 30, 31),
    (2, 3, 4, 8, 9, 10, 11, 20, 21, 22, 23, 28, 29, 30, 31),
    (2, 3, 7, 8, 9, 10, 11, 20, 21, 22, 23, 28, 29, 30, 31),
    (2, 3, 6, 8, 9, 10, 11, 20, 21, 22, 23, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 9, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 8, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 11, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 10, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 13, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 12, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 15, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 14, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 17, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 16, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 19, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 18, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 21, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 20, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 23, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 4, 5, 6, 7, 22, 24, 25, 26, 27, 28, 29, 30, 31),
    (2, 3, 8, 9, 10, 11, 20, 21, 22, 23, 25, 28, 29, 30, 31),
    (2, 3, 8, 9, 10, 11, 20, 21, 22, 23, 24, 28, 29, 30, 31),
    (2, 3, 8, 9, 10, 11, 20, 21, 22, 23, 27, 28, 29, 30, 31),
    (2, 3, 8, 9, 10, 11, 20, 21, 22, 23, 26, 28, 29, 30, 31),
    (4, 5, 8, 9, 12, 13, 18, 19, 22, 23, 26, 27, 29, 30, 31),
    (4, 5, 8, 9, 12, 13, 18, 19, 22, 23, 26, 27, 28, 30, 31),
    (6, 7, 8, 9, 14, 15, 18, 19, 20, 21, 26, 27, 28, 29, 31),
    (6, 7, 8, 9, 14, 15, 18, 19, 20, 21, 26, 27, 28, 29, 30),
)


def powers(value):
    answer = []
    current = value
    for _ in range(7):
        answer.append(current)
        current = multiply(current, value)
    return tuple(answer)


def main():
    assert len(DIAGONAL_WITNESSES) == 32
    for value, subset in enumerate(DIAGONAL_WITNESSES):
        assert len(subset) == len(set(subset)) == 15
        assert set(subset).isdisjoint({0, 1})
        assert elementary_prefix(subset, 7) == (value,) * 7

    # For every two distinct proposed clique vertices v(a),v(c), construct
    # an edge between actual 16-sets with exactly those coefficient prefixes.
    checked_edges = 0
    for first in range(32):
        for second in range(first + 1, 32):
            difference = first ^ second
            ratio = multiply(first, inverse(difference))
            base = DIAGONAL_WITNESSES[ratio]
            common = {
                second ^ multiply(difference, point) for point in base
            }
            left = common | {second}
            right = common | {first}

            assert len(common) == 15
            assert len(left) == len(right) == 16
            assert len(left & right) == 15
            assert elementary_prefix(left, 7) == powers(first)
            assert elementary_prefix(right, 7) == powers(second)
            checked_edges += 1

    assert checked_edges == 32 * 31 // 2
    print("F_32 prefix certificate: PASS")
    print("32 coefficient states (a,a^2,...,a^7) form a clique")
    print("checked adjacent realizations:", checked_edges)


if __name__ == "__main__":
    main()
