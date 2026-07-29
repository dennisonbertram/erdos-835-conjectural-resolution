#!/usr/bin/env python3
"""Finite controls for maximal_minor_p7mod8_closure.md.

The proof in the note is symbolic.  This dependency-free script verifies
the exact field identities, the Vandermonde annihilators, the quadratic
character count used at the first new prime p=23, and the genuine p=7
ordered-link exception.
"""

from __future__ import print_function

from itertools import combinations


def legendre(value, prime):
    value %= prime
    if value == 0:
        return 0
    return 1 if pow(value, (prime - 1) // 2, prime) == 1 else -1


def inverse(value, prime):
    return pow(value % prime, prime - 2, prime)


def determinant(left, right, prime):
    return (left[0] * right[1] - left[1] * right[0]) % prime


def ordered_link_rows(vectors, prime):
    rows = []
    for i in range(len(vectors)):
        labels = []
        for j in range(len(vectors)):
            if i == j:
                continue
            left = vectors[min(i, j)]
            right = vectors[max(i, j)]
            labels.append(determinant(left, right, prime))
        rows.append(tuple(sorted(labels)))
    return tuple(rows)


def check_p7_link():
    prime = 7
    vectors = (
        (1, 0), (6, 0),
        (3, 3), (4, 4),
        (3, 6), (4, 1),
        (3, 5), (4, 2),
    )
    expected = tuple(range(prime))
    rows = ordered_link_rows(vectors, prime)
    assert len(rows) == prime + 1
    assert all(row == expected for row in rows)

    # The four squared scales are 1,2,2,2 on slopes 0,1,2,4.
    slopes = (0, 1, 2, 4)
    scales = (1, 2, 2, 2)
    residues = tuple(sorted({x * x % prime for x in range(1, prime)}))
    for index, slope in enumerate(slopes):
        values = sorted(
            scales[other] * (slopes[other] - slope) ** 2 % prime
            for other in range(len(slopes))
            if other != index
        )
        assert tuple(values) == residues
    return vectors


def derivative(slopes, point, prime):
    answer = 1
    for other in slopes:
        if other != point:
            answer = answer * (point - other) % prime
    return answer


def check_vandermonde_annihilators():
    prime = 23
    size = (prime + 1) // 2
    slopes = tuple(range(size))
    derivatives = tuple(
        derivative(slopes, point, prime) for point in slopes
    )
    inverse_derivatives = tuple(
        inverse(value, prime) for value in derivatives
    )

    # Constant numerator: moments 0 through m-2 vanish.
    for exponent in range(size - 1):
        assert sum(
            weight * pow(point, exponent, prime)
            for point, weight in zip(slopes, inverse_derivatives)
        ) % prime == 0

    # Every numerator of degree at most two annihilates moments 0 through
    # m-4, exactly as used by the next-to-top moment.
    for coefficients in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (3, 5, 7)):
        weights = tuple(
            (
                coefficients[0]
                + coefficients[1] * point
                + coefficients[2] * point * point
            )
            * inverse_derivatives[index]
            % prime
            for index, point in enumerate(slopes)
        )
        for exponent in range(size - 3):
            assert sum(
                weight * pow(point, exponent, prime)
                for point, weight in zip(slopes, weights)
            ) % prime == 0

    q = (prime - 7) // 8
    top = 2 * q + 1
    assert 2 * top == size - 2
    assert 2 * (top - 1) == size - 4
    return slopes


def quadratic_character_census(prime):
    """Classify the maximum same-character nonzero fibres of quadratics."""
    half = (prime - 1) // 2
    nonsquare_discriminant_max = 0
    square_discriminant_max = 0
    repeated_root_max = 0
    linear_max = 0

    for a in range(1, prime):
        for b in range(prime):
            for c in range(prime):
                discriminant = (b * b - 4 * a * c) % prime
                counts = {
                    1: 0,
                    -1: 0,
                }
                for x in range(prime):
                    character = legendre(a * x * x + b * x + c, prime)
                    if character:
                        counts[character] += 1
                maximum = max(counts.values())
                if discriminant == 0:
                    repeated_root_max = max(repeated_root_max, maximum)
                elif legendre(discriminant, prime) == 1:
                    square_discriminant_max = max(
                        square_discriminant_max, maximum
                    )
                else:
                    nonsquare_discriminant_max = max(
                        nonsquare_discriminant_max, maximum
                    )

    for b in range(1, prime):
        for c in range(prime):
            counts = {1: 0, -1: 0}
            for x in range(prime):
                character = legendre(b * x + c, prime)
                if character:
                    counts[character] += 1
            linear_max = max(linear_max, max(counts.values()))

    assert linear_max == half
    assert square_discriminant_max == half
    assert nonsquare_discriminant_max == half + 1
    assert repeated_root_max == prime - 1
    return {
        "linear_max": linear_max,
        "square_discriminant_max": square_discriminant_max,
        "nonsquare_discriminant_max": nonsquare_discriminant_max,
        "repeated_root_max": repeated_root_max,
    }


def check_anisotropic_involution():
    prime = 23
    # The first nonsquare normal form R(x)=x^2-d.
    d = next(value for value in range(2, prime) if legendre(value, prime) == -1)
    slopes = tuple(
        value
        for value in range(prime)
        if legendre(value * value - d, prime) == -1
    )
    size = (prime + 1) // 2
    assert len(slopes) == size
    assert 0 not in slopes
    scale = d  # nonsquare / nonsquare makes every z_s a square
    squared_scales = {
        slope: scale * inverse(slope * slope - d, prime) % prime
        for slope in slopes
    }
    assert all(legendre(value, prime) == 1 for value in squared_scales.values())

    distinct_counts = []
    for middle in slopes:
        image = {}
        fixed = []
        for slope in slopes:
            denominator = (2 * middle * slope - middle * middle - d) % prime
            assert denominator != 0
            partner = (
                ((middle * middle + d) * slope - 2 * d * middle)
                * inverse(denominator, prime)
                % prime
            )
            assert partner in squared_scales
            partner_denominator = (
                2 * middle * partner - middle * middle - d
            ) % prime
            back = (
                ((middle * middle + d) * partner - 2 * d * middle)
                * inverse(partner_denominator, prime)
                % prime
            )
            assert back == slope
            assert legendre(partner * partner - d, prime) == -1
            row_value = (
                squared_scales[slope] * (slope - middle) ** 2 % prime
            )
            partner_value = (
                squared_scales[partner] * (partner - middle) ** 2 % prime
            )
            assert row_value == partner_value
            image[slope] = partner
            if partner == slope:
                fixed.append(slope)

        assert set(fixed) == {middle, d * inverse(middle, prime) % prime}
        nonzero_values = {
            squared_scales[slope] * (slope - middle) ** 2 % prime
            for slope in slopes
            if slope != middle
        }
        distinct_counts.append(len(nonzero_values))
        assert len(nonzero_values) == size // 2
    return {
        "d": d,
        "slopes": slopes,
        "distinct_nonzero_values_per_row": tuple(distinct_counts),
    }


def has_nontrivial_three_term_progression(subset, prime):
    values = set(subset)
    for middle in subset:
        for left in subset:
            if left == middle:
                continue
            right = (2 * middle - left) % prime
            if right in values and right != middle and right != left:
                return True
    return False


def check_small_half_set_controls():
    # Exhaustive controls for the elementary half-plus-one lemma.
    results = {}
    for prime in (7, 11, 13):
        size = (prime + 1) // 2
        examined = 0
        progression_free = 0
        for subset in combinations(range(prime), size):
            examined += 1
            if not has_nontrivial_three_term_progression(subset, prime):
                progression_free += 1
        assert progression_free == 0
        results[prime] = examined
    return results


def check_field_square_sums():
    for prime in (7, 23, 31, 47, 71, 79, 103, 127):
        assert prime % 8 == 7
        assert sum(x * x for x in range(prime)) % prime == 0
        size = (prime + 1) // 2
        assert (4 * size) % prime == 2


def main():
    vectors = check_p7_link()
    slopes = check_vandermonde_annihilators()
    census = quadratic_character_census(23)
    anisotropic = check_anisotropic_involution()
    half_set_controls = check_small_half_set_controls()
    check_field_square_sums()
    print("p7_ordered_link_vectors=", vectors)
    print("p23_vandermonde_control_slopes=", slopes)
    print("p23_quadratic_character_census=", census)
    print("p23_anisotropic_involution=", anisotropic)
    print("half_plus_one_subsets_exhausted=", half_set_controls)
    print("maximal-minor p=7 mod 8 closure audit: PASS")


if __name__ == "__main__":
    main()
