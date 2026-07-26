#!/usr/bin/env python3
"""Exact audit of triangle triples and the dimension-two third moment.

This verifier uses only the Python standard library.  It establishes two
conditional consequences of a hypothetical S(14,15,31):

1. the dual of the 30-dimensional even point code has weight-three words,
   so a common-zero shortening does *not* inherit dual distance four;
2. the (0,9,9,13) shortening's relaxed third-moment problem forces a
   positive, explicitly bounded number of weight-three dual words.

The result is a route closure and structural theorem, not a nonexistence
proof for S(14,15,31).
"""

from collections import Counter, defaultdict
from itertools import product
from math import comb


V = 31
T = 14
K = 15
BLOCKS = comb(V, T) // K
EVEN_DIMENSION = 30
EVEN_SIZE = 1 << EVEN_DIMENSION

H_COUNTS = (0, 9, 9, 13)
H_ORDER = 4
SHORT_DIMENSION = 28
SHORT_SIZE = 1 << SHORT_DIMENSION
MIDDLE_FOURIER_JUMP = 1 << K
MIDDLE_WEIGHT_STEP = MIDDLE_FOURIER_JUMP // (2 * H_ORDER)

LAMBDA = tuple(
    comb(V - level, T - level) // (K - level)
    for level in range(T + 1)
)


def fourier(size: int, internal_middle: bool = False) -> int:
    """Return sum_B (-1)^|B cap S| for a set S of the given type."""
    if size > K:
        return -fourier(V - size, internal_middle)
    answer = sum(
        (-2) ** level * comb(size, level) * LAMBDA[level]
        for level in range(min(size, T) + 1)
    )
    if size == K and internal_middle:
        answer += (-2) ** K
    return answer


def code_weight(size: int, internal_middle: bool = False) -> int:
    numerator = BLOCKS - fourier(size, internal_middle)
    assert numerator % 2 == 0
    return numerator // 2


def krawtchouk(length: int, weight: int, degree: int) -> int:
    return sum(
        (-1) ** index
        * comb(weight, index)
        * comb(length - weight, degree - index)
        for index in range(degree + 1)
        if index <= weight and degree - index <= length - weight
    )


def macwilliams(
    distribution: Counter[int], length: int, dimension: int, degree: int
) -> int:
    numerator = sum(
        multiplicity * krawtchouk(length, weight, degree)
        for weight, multiplicity in distribution.items()
    )
    denominator = 1 << dimension
    assert numerator % denominator == 0
    return numerator // denominator


def even_code_distribution() -> Counter[int]:
    distribution: Counter[int] = Counter()
    for size in range(0, V + 1, 2):
        if size == K + 1:
            distribution[code_weight(size, True)] += BLOCKS
            distribution[code_weight(size, False)] += (
                comb(V, size) - BLOCKS
            )
        else:
            distribution[code_weight(size)] += comb(V, size)
    assert sum(distribution.values()) == EVEN_SIZE
    return distribution


def fixed_block_intersections() -> tuple[int, ...]:
    """Intersection distribution with one fixed design block."""
    extended_lambda = LAMBDA + (1,)
    counts = [0] * (K + 1)
    for level in range(K, -1, -1):
        rhs = comb(K, level) * extended_lambda[level]
        rhs -= sum(
            comb(size, level) * counts[size]
            for size in range(level + 1, K + 1)
        )
        counts[level] = rhs
    assert sum(counts) == BLOCKS
    return tuple(counts)


def punctured_distribution(
    intersections: tuple[int, ...],
) -> Counter[int]:
    """Weight distribution after puncturing at one fixed block."""
    joint: Counter[tuple[int, int]] = Counter()

    for size in range(0, V + 1, 2):
        total_by_bit = [
            sum(
                comb(K, inside) * comb(V - K, size - inside)
                for inside in range(
                    max(0, size - (V - K)), min(K, size) + 1
                )
                if inside % 2 == bit
            )
            for bit in (0, 1)
        ]

        if size == K + 1:
            internal_by_bit = [
                sum(
                    intersections[meeting]
                    for meeting in range(K + 1)
                    if (K - meeting) % 2 == bit
                )
                for bit in (0, 1)
            ]
            for bit in (0, 1):
                internal = internal_by_bit[bit]
                external = total_by_bit[bit] - internal
                if internal:
                    joint[(code_weight(size, True), bit)] += internal
                if external:
                    joint[(code_weight(size, False), bit)] += external
        else:
            weight = code_weight(size)
            for bit in (0, 1):
                if total_by_bit[bit]:
                    joint[(weight, bit)] += total_by_bit[bit]

    assert sum(joint.values()) == EVEN_SIZE
    punctured: Counter[int] = Counter()
    for (weight, coordinate), multiplicity in joint.items():
        punctured[weight - coordinate] += multiplicity
    return punctured


def dot(left: int, right: int) -> int:
    return bin(left & right).count("1") & 1  # int.bit_count needs py>=3.10


def shortening_types() -> tuple[int, dict[tuple[int, int], int]]:
    """Enumerate E/H cosets by external weight and middle capacity."""
    weights_h = tuple(
        sum(
            H_COUNTS[column]
            for column in range(H_ORDER)
            if dot(word, column)
        )
        for word in range(H_ORDER)
    )
    assert sorted(weights_h) == [0, 18, 22, 22]
    base_sum = sum(fourier(weight) for weight in weights_h)
    assert base_sum % H_ORDER == 0
    length = base_sum // H_ORDER

    types: defaultdict[tuple[int, int], int] = defaultdict(int)
    for profile in product(*(range(count + 1) for count in H_COUNTS)):
        if sum(profile) & 1:
            continue
        multiplicity = 1
        for count, selected in zip(H_COUNTS, profile):
            multiplicity *= comb(count, selected)
        translated_weights = tuple(
            sum(
                H_COUNTS[column] - profile[column]
                if dot(word, column)
                else profile[column]
                for column in range(H_ORDER)
            )
            for word in range(H_ORDER)
        )
        translated_sum = sum(fourier(weight) for weight in translated_weights)
        numerator = base_sum - translated_sum
        assert numerator % (2 * H_ORDER) == 0
        base_weight = numerator // (2 * H_ORDER)
        capacity = translated_weights.count(K + 1)
        types[(base_weight, capacity)] += multiplicity

    for key in tuple(types):
        assert types[key] % H_ORDER == 0
        types[key] //= H_ORDER
    assert sum(types.values()) == SHORT_SIZE
    return length, dict(sorted(types.items()))


def third_moment_bounds() -> tuple[int, int, int, int, int]:
    """Verify static LP dual certificates with exact integer arithmetic."""
    length, types = shortening_types()
    assert length == 4_419_003
    assert len(types) == 57

    # For the upper certificate,
    #   s^3 <= lambda_type + alpha*t + beta*s^2.
    upper_alpha = 188_441_387_008
    upper_beta = -10_953
    upper = (
        upper_alpha * BLOCKS
        + upper_beta * SHORT_SIZE * length
    )

    # For the lower certificate,
    #   s^3 >= lambda_type + alpha*t + beta*s^2.
    lower_alpha = 1_007_554_486_272
    lower_beta = -28_961
    lower = (
        lower_alpha * BLOCKS
        + lower_beta * SHORT_SIZE * length
    )

    for (base_weight, capacity), multiplicity in types.items():
        upper_residuals = []
        lower_residuals = []
        for internal in range(capacity + 1):
            weight = base_weight - MIDDLE_WEIGHT_STEP * internal
            centered = 2 * weight - length
            upper_residuals.append(
                centered**3
                - upper_alpha * internal
                - upper_beta * centered**2
            )
            lower_residuals.append(
                centered**3
                - lower_alpha * internal
                - lower_beta * centered**2
            )
        upper += multiplicity * max(upper_residuals)
        lower += multiplicity * min(lower_residuals)

    assert lower == -96_749_968_713_628_778_496
    assert upper == -92_587_049_516_424_757_248
    assert lower <= upper < 0

    moment_factor = 6 * SHORT_SIZE
    minimum_triangles = (-upper + moment_factor - 1) // moment_factor
    maximum_triangles = (-lower) // moment_factor
    assert minimum_triangles == 57_485_606_222
    assert maximum_triangles == 60_070_286_637
    return (
        length,
        lower,
        upper,
        minimum_triangles,
        maximum_triangles,
    )


def main() -> None:
    assert BLOCKS == 17_678_835
    assert LAMBDA == (
        17_678_835,
        8_554_275,
        3_991_995,
        1_789_515,
        766_935,
        312_455,
        120_175,
        43_263,
        14_421,
        4_389,
        1_197,
        285,
        57,
        9,
        1,
    )

    distribution = even_code_distribution()
    dual = tuple(
        macwilliams(distribution, BLOCKS, EVEN_DIMENSION, degree)
        for degree in range(5)
    )
    assert dual == (
        1,
        0,
        0,
        927_696_866_625,
        3_793_226_637_448_341_180,
    )

    intersections = fixed_block_intersections()
    assert intersections == (
        0,
        120,
        3_360,
        49_140,
        349_440,
        1_417_416,
        3_363_360,
        4_877_730,
        4_324_320,
        2_362_360,
        768_768,
        147_420,
        14_560,
        840,
        0,
        1,
    )

    punctured = punctured_distribution(intersections)
    punctured_dual_3 = macwilliams(
        punctured, BLOCKS - 1, EVEN_DIMENSION, 3
    )
    assert punctured_dual_3 == 927_696_709_200

    triangles = dual[3]
    triangles_through_block = triangles - punctured_dual_3
    closing_partners = 2 * triangles_through_block
    nonclosing_partners = intersections[7] - closing_partners
    assert triangles_through_block == 157_425
    assert closing_partners == 314_850
    assert nonclosing_partners == 4_562_880
    assert 3 * triangles == BLOCKS * triangles_through_block

    all_pairs_would_give = BLOCKS * intersections[7] // 6
    assert all_pairs_would_give == 14_372_097_307_425
    assert triangles < all_pairs_would_give

    (
        shortened_length,
        lower_moment,
        upper_moment,
        minimum_short_triangles,
        maximum_short_triangles,
    ) = third_moment_bounds()

    print(f"blocks={BLOCKS}")
    print(f"even_code_dual_A3={triangles}")
    print(f"triangles_through_each_block={triangles_through_block}")
    print(f"intersection_7_partners={intersections[7]}")
    print(f"closing_partners={closing_partners}")
    print(f"nonclosing_partners={nonclosing_partners}")
    print(f"shortened_length={shortened_length}")
    print(f"shortened_third_moment_interval=[{lower_moment},{upper_moment}]")
    print(
        "shortened_dual_A3_interval="
        f"[{minimum_short_triangles},{maximum_short_triangles}]"
    )
    print("S(14,15,31) triangle/third-moment audit: PASS")


if __name__ == "__main__":
    main()
