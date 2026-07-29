#!/usr/bin/env python3
"""Standard-library checks for evidence/constructive_no_go.md."""

from collections import Counter
from itertools import combinations
from math import comb


GF16_MODULUS = 0b10011


def xor(values):
    total = 0
    for value in values:
        total ^= value
    return total


def gf16_mul(left, right):
    product = 0
    while right:
        if right & 1:
            product ^= left
        right >>= 1
        left <<= 1
        if left & 0b10000:
            left ^= GF16_MODULUS
    return product


def gf16_inv(value):
    assert value
    result = 1
    for _ in range(14):
        result = gf16_mul(result, value)
    assert gf16_mul(result, value) == 1
    return result


def gf16_product(values):
    result = 1
    for value in values:
        result = gf16_mul(result, value)
    return result


def pair_statistics(first, second):
    ratio = gf16_mul(gf16_product(first), gf16_inv(gf16_product(second)))
    return ratio, len(set(first) & set(second)) % 2


def verify_k16_numeric_counts():
    block_count = comb(32, 16) // 17
    assert block_count == 35_357_670
    assert block_count % 4 == 2

    central = comb(30, 15)
    character_coefficient = 2 * comb(14, 7)
    assert central == 155_117_520
    assert character_coefficient == 6_864
    assert (central + 15 * character_coefficient) // 32 == 4_850_640
    assert (central - character_coefficient) // 32 == 4_847_208
    assert (central + 15 * character_coefficient) % 32 == 0
    assert (central - character_coefficient) % 32 == 0


def verify_small_fourier_analogue():
    """Exhaustively check the F_2^3 count quoted in the note."""

    space = range(8)
    for x in space:
        for y in space:
            if x == y:
                continue
            remaining = [z for z in space if z not in (x, y)]
            counts = Counter(xor(subset) for subset in combinations(remaining, 3))
            assert set(counts) == set(space)
            for target in space:
                expected = 4 if target in (x, y) else 2
                assert counts[target] == expected


def verify_character_coefficient_directly():
    """Check both signs in the nontrivial-character coefficient."""

    plus_removed = sum(
        (-1) ** j * comb(14, 15 - j) * comb(16, j)
        for j in range(16)
        if 0 <= 15 - j <= 14
    )
    minus_removed = sum(
        (-1) ** j * comb(16, 15 - j) * comb(14, j)
        for j in range(15)
        if 0 <= 15 - j <= 16
    )
    assert plus_removed == 6_864
    assert minus_removed == -6_864


def verify_prime_cycle_collisions():
    """Check the consecutive-block collisions in Theorem 5."""

    first = frozenset(range(16))
    shifted = frozenset(range(1, 17))
    assert len(first) == len(shifted) == 16
    assert len(first & shifted) == 15
    assert first ^ shifted == {0, 16}

    derived_first = frozenset(range(4))
    derived_shifted = frozenset(range(1, 5))
    assert len(derived_first) == len(derived_shifted) == 4
    assert len(derived_first & derived_shifted) == 3
    assert derived_first ^ derived_shifted == {0, 4}


def verify_affine_line_projective_collision():
    """Check an explicit coordinate instance of Theorem 6."""

    # In the bit representation of F_16, H={0,...,7} is a
    # three-dimensional F_2-subspace.  Take r=8, h=1, q=10.
    subspace = set(range(8))
    r, h, q = 8, 1, 10
    assert r not in subspace
    assert h in subspace and h
    assert q not in subspace
    assert q not in (r, r ^ h)

    first_layer = (subspace - {0}) | {r}
    second_layer = subspace
    changed_layer = (first_layer - {h}) | {q}
    assert len(first_layer) == len(second_layer) == len(changed_layer) == 8
    assert xor(first_layer) == r
    assert xor(second_layer) == 0
    assert xor(changed_layer) == (r ^ h ^ q) != 0


def verify_reduced_rational_function_collision():
    """Check the vertical edge used in Theorem 7."""

    labels = set(range(1, 16))
    chosen_label = 1
    first_layer = {chosen_label}
    second_layer = labels - {chosen_label}
    assert len(first_layer) + len(second_layer) == 15

    changed_first_layer = set()
    changed_second_layer = set(labels)
    assert len(changed_first_layer) + len(changed_second_layer) == 15

    # The encoded numerator/denominator root sets are both {a} before
    # the exchange and both empty afterwards, so both reduced quotients
    # are the constant function one and both polynomial differences vanish.
    first_a = first_layer
    first_c = labels - second_layer
    changed_a = changed_first_layer
    changed_c = labels - changed_second_layer
    assert first_a == first_c == {chosen_label}
    assert changed_a == changed_c == set()


def verify_product_ratio_parity_edges():
    """Check all edge constructions in Theorem 8."""

    nonunits = set(range(2, 16))

    # Same-parity edges force injectivity on the fourteen nonunit ratios.
    for a, b in combinations(sorted(nonunits), 2):
        even_first = ({a}, {1})
        even_second = ({b}, {1})
        assert pair_statistics(*even_first) == (a, 0)
        assert pair_statistics(*even_second) == (b, 0)

        t = next(value for value in range(1, 16) if value not in (1, a, b))
        odd_first = ({t, a}, {t, 1})
        odd_second = ({t, b}, {t, 1})
        assert pair_statistics(*odd_first) == (a, 1)
        assert pair_statistics(*odd_second) == (b, 1)

    # Cross-parity edges make the two fourteen-element images disjoint.
    for a in sorted(nonunits):
        for b in sorted(nonunits):
            if a == b:
                w = next(
                    value
                    for value in range(1, 16)
                    if value not in (1, gf16_inv(a))
                )
                first = ({1, gf16_mul(a, w)}, {1, w})
                second = ({gf16_mul(a, w)}, {w})
            else:
                d = gf16_mul(b, gf16_inv(a))
                forbidden = {
                    1,
                    d,
                    gf16_inv(a),
                    gf16_mul(gf16_inv(a), d),
                }
                w = next(
                    value for value in range(1, 16) if value not in forbidden
                )
                first = ({1, gf16_mul(a, w)}, {1, w})
                second = ({d, gf16_mul(a, w)}, {1, w})
            assert pair_statistics(*first) == (a, 1)
            assert pair_statistics(*second) == (b, 0)


if __name__ == "__main__":
    verify_k16_numeric_counts()
    verify_small_fourier_analogue()
    verify_character_coefficient_directly()
    verify_prime_cycle_collisions()
    verify_affine_line_projective_collision()
    verify_reduced_rational_function_collision()
    verify_product_ratio_parity_edges()
    print("constructive no-go evidence: all checks passed")
