#!/usr/bin/env python3
"""Verify the global averaging no-go for endpoint-only Griesmer searches.

The ambient group is the 30-dimensional group of even subsets of 31
points.  The artificial radial function F_plus replaces the unresolved
Fourier value of every 16-subset by its largest possible value.  Its
exact Fourier spectrum forces a large F_plus-sum on some nontrivial
coset of every proper subspace.  That coset is enough to prevent the
independent-endpoint shortened-code bounds from violating Griesmer.
"""

from __future__ import annotations

from math import comb


POINTS = 31
DESIGN_T = 14
BLOCK_SIZE = 15
BLOCKS = comb(POINTS, DESIGN_T) // BLOCK_SIZE
EVEN_GROUP_ORDER = 1 << (POINTS - 1)
MIDDLE_CORRECTION = 1 << BLOCK_SIZE


def parameters() -> tuple[int, ...]:
    return tuple(
        comb(POINTS - level, DESIGN_T - level)
        // (BLOCK_SIZE - level)
        for level in range(DESIGN_T + 1)
    )


LAMBDA = parameters()


def fourier_external(size: int) -> int:
    if size > BLOCK_SIZE:
        return -fourier_external(POINTS - size)
    return sum(
        (-2) ** level * comb(size, level) * LAMBDA[level]
        for level in range(min(size, DESIGN_T) + 1)
    )


FOURIER_MINUS = tuple(
    fourier_external(size) for size in range(POINTS + 1)
)
FOURIER_PLUS = tuple(
    value + (MIDDLE_CORRECTION if size == BLOCK_SIZE + 1 else 0)
    for size, value in enumerate(FOURIER_MINUS)
)


def krawtchouk(degree: int, character_weight: int) -> int:
    """K_degree(character_weight) for the 31-dimensional Hamming cube."""
    return sum(
        (-1) ** intersection
        * comb(character_weight, intersection)
        * comb(
            POINTS - character_weight,
            degree - intersection,
        )
        for intersection in range(
            max(0, degree - (POINTS - character_weight)),
            min(degree, character_weight) + 1,
        )
    )


def even_group_transform(
    values: tuple[int, ...],
) -> tuple[int, ...]:
    """Fourier transform, one value for each character weight 0,...,15.

    Characters indexed by a subset U and its complement agree on the
    even-subset group, so weights 0 through 15 give all character types.
    """
    return tuple(
        sum(
            values[size] * krawtchouk(size, character_weight)
            for size in range(0, POINTS + 1, 2)
        )
        for character_weight in range(BLOCK_SIZE + 1)
    )


def main() -> None:
    assert BLOCKS == 17_678_835
    assert comb(POINTS, BLOCK_SIZE + 1) == 17 * BLOCKS

    sum_minus = sum(
        comb(POINTS, size) * FOURIER_MINUS[size]
        for size in range(0, POINTS + 1, 2)
    )
    sum_plus = sum(
        comb(POINTS, size) * FOURIER_PLUS[size]
        for size in range(0, POINTS + 1, 2)
    )
    assert sum_minus == -MIDDLE_CORRECTION * BLOCKS
    assert sum_plus == (1 << 19) * BLOCKS
    assert sum_plus == 9_268_801_044_480

    transform = even_group_transform(FOURIER_PLUS)
    assert transform == (
        9_268_801_044_480,
        -298_993_582_080,
        -298_993_582_080,
        30_930_370_560,
        30_930_370_560,
        -5_727_846_400,
        -5_727_846_400,
        1_603_796_992,
        1_603_796_992,
        -627_572_736,
        -627_572_736,
        328_728_576,
        328_728_576,
        -224_919_552,
        -224_919_552,
        261_619_712,
    )
    nontrivial_maximum = max(transform[1:])
    assert nontrivial_maximum == 30_930_370_560

    # For a subspace H of size q and quotient size N, Fourier inversion
    # gives
    #   A_plus(H) <= (T + (N-1)R)/N.
    # Hence the average B_plus over the outside cosets is at least
    #   (T-R)/N = q * (T-R)/|E| = q * 137655/16.
    numerator = sum_plus - nontrivial_maximum
    assert numerator * 16 == EVEN_GROUP_ORDER * 137_655

    dimension_rows = []
    for subspace_dimension in range(POINTS - 1):
        maximum_image_dimension = (
            POINTS - 1 - subspace_dimension
        )
        # 137655/16 > k+1.  Thus some outside coset has
        # B_plus > q(k+1), the sufficient inequality in the proof.
        assert 137_655 > 16 * (maximum_image_dimension + 1)
        dimension_rows.append(
            (
                subspace_dimension,
                maximum_image_dimension,
                137_655 - 16 * (maximum_image_dimension + 1),
            )
        )

    print(f"blocks={BLOCKS}")
    print(f"sum_F_minus_over_even_subsets={sum_minus}")
    print(f"sum_F_plus_over_even_subsets={sum_plus}")
    print(f"F_plus_even_group_transform={transform}")
    print(f"nontrivial_transform_maximum={nontrivial_maximum}")
    print("outside_coset_average_per_H_word_lower=137655/16")
    print(
        "proper_subspace_dimensions_checked="
        f"{dimension_rows[0][0]}..{dimension_rows[-1][0]}"
    )
    print("endpoint-only shortening plus Griesmer: GLOBAL NO-GO PASS")


if __name__ == "__main__":
    main()
