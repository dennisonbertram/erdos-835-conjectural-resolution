#!/usr/bin/env python3
"""Exhaustive dimension-2 shortening audit for a hypothetical S(14,15,31).

This verifier classifies every two-dimensional subcode H of the even
point-incidence code by its four labelled column multiplicities.  This is
redundant under changes of basis in H, but exhaustive.  It then enumerates
every even point-subset profile outside H and applies a Fourier/Griesmer
lower bound to the corresponding punctured coset.

The dimension-2 search is exhaustive.  The two dimension-3 profiles at
the end were selected by a separate random search; their individual
coset audits are exhaustive, but their selection is not.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
from math import comb


POINTS = 31
DESIGN_T = 14
BLOCK_SIZE = 15
BLOCKS = comb(POINTS, DESIGN_T) // BLOCK_SIZE
EVEN_CODE_DIMENSION = 30
MIDDLE_CORRECTION = 1 << BLOCK_SIZE
EXPECTED_DIMENSION_TWO_SHA256 = (
    "f963ed6e72aa544385592c3c7379b8c99e3358960e626c54d42c986dd417a639"
)


def parameters() -> tuple[int, ...]:
    return tuple(
        comb(POINTS - level, DESIGN_T - level)
        // (BLOCK_SIZE - level)
        for level in range(DESIGN_T + 1)
    )


LAMBDA = parameters()


def fourier_external(size: int) -> int:
    """Forced Fourier value, using the external value at sizes 15 and 16."""
    if size > BLOCK_SIZE:
        # Every block has odd size.
        return -fourier_external(POINTS - size)
    return sum(
        (-2) ** level * comb(size, level) * LAMBDA[level]
        for level in range(min(size, DESIGN_T) + 1)
    )


FOURIER_LOWER = tuple(fourier_external(size) for size in range(POINTS + 1))
FOURIER_UPPER = tuple(
    value + (MIDDLE_CORRECTION if size == BLOCK_SIZE + 1 else 0)
    for size, value in enumerate(FOURIER_LOWER)
)


def griesmer(distance: int, dimension: int) -> int:
    return sum(
        (distance + (1 << power) - 1) // (1 << power)
        for power in range(dimension)
    )


def ceil_div(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def dot(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def binary_rank(vectors: set[int], dimension: int) -> int:
    pivots = [0] * dimension
    rank = 0
    for vector in vectors:
        row = vector
        while row:
            pivot = row.bit_length() - 1
            if pivots[pivot]:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                rank += 1
                break
    return rank


def maximum_kernel_dimension(removed_upper: int, minimum: int) -> int:
    return max(
        (
            dimension
            for dimension in range(EVEN_CODE_DIMENSION + 1)
            if griesmer(minimum, dimension) <= removed_upper
        ),
        default=0,
    )


def h_word_weights(counts: tuple[int, ...]) -> tuple[int, ...]:
    order = len(counts)
    return tuple(
        sum(counts[value] for value in range(order) if dot(word, value))
        for word in range(order)
    )


def h_profiles(counts: tuple[int, ...]) -> set[tuple[int, ...]]:
    order = len(counts)
    return {
        tuple(
            counts[value] if dot(word, value) else 0
            for value in range(order)
        )
        for word in range(order)
    }


def translated_weights(
    counts: tuple[int, ...], profile: tuple[int, ...]
) -> tuple[int, ...]:
    order = len(counts)
    return tuple(
        sum(
            (
                counts[value] - profile[value]
                if dot(word, value)
                else profile[value]
            )
            for value in range(order)
        )
        for word in range(order)
    )


def audit_fixed_profile(
    counts: tuple[int, ...],
    original_minimum: int,
) -> dict[str, object]:
    """Exhaustively audit all profile representatives for one fixed H."""
    dimension = (len(counts)).bit_length() - 1
    order = 1 << dimension
    assert len(counts) == order
    assert sum(counts) == POINTS
    assert all(
        sum(counts[value] for value in range(order) if dot(row, value))
        % 2
        == 0
        for row in (1 << bit for bit in range(dimension))
    )
    assert binary_rank(
        {value for value, count in enumerate(counts) if value and count},
        dimension,
    ) == dimension

    weights_h = h_word_weights(counts)
    base_lower = sum(FOURIER_LOWER[weight] for weight in weights_h)
    base_upper = sum(FOURIER_UPPER[weight] for weight in weights_h)
    length_lower = ceil_div(base_lower, order)
    length_upper = base_upper // order
    removed_upper = BLOCKS - length_lower
    kernel_upper = maximum_kernel_dimension(
        removed_upper, original_minimum
    )
    image_lower = EVEN_CODE_DIMENSION - kernel_upper
    subgroup_profiles = h_profiles(counts)

    representative_count = 0
    distance_lower: int | None = None
    lower_witness: tuple[tuple[int, ...], tuple[int, ...]] | None = None
    exact_word_upper: int | None = None
    exact_witness: tuple[tuple[int, ...], tuple[int, ...]] | None = None

    for profile in product(*(range(count + 1) for count in counts)):
        if sum(profile) & 1 or profile in subgroup_profiles:
            continue
        representative_count += 1
        weights = translated_weights(counts, profile)
        numerator_lower = base_lower - sum(
            FOURIER_UPPER[weight] for weight in weights
        )
        lower = ceil_div(numerator_lower, 2 * order)
        if distance_lower is None or lower < distance_lower:
            distance_lower = lower
            lower_witness = (profile, weights)

        # This is an actual word weight only when neither H nor its coset
        # touches the unresolved middle layer.
        if (
            BLOCK_SIZE + 1 not in weights_h
            and BLOCK_SIZE + 1 not in weights
        ):
            exact_numerator = base_lower - sum(
                FOURIER_LOWER[weight] for weight in weights
            )
            assert exact_numerator % (2 * order) == 0
            exact_weight = exact_numerator // (2 * order)
            if exact_word_upper is None or exact_weight < exact_word_upper:
                exact_word_upper = exact_weight
                exact_witness = (profile, weights)

    assert distance_lower is not None
    bound = griesmer(distance_lower, image_lower)
    return {
        "dimension": dimension,
        "counts": counts,
        "h_weights": weights_h,
        "length_bounds": (length_lower, length_upper),
        "removed_upper": removed_upper,
        "kernel_upper": kernel_upper,
        "image_lower": image_lower,
        "profile_representatives": representative_count,
        "distance_lower": distance_lower,
        "lower_witness": lower_witness,
        "exact_word_upper": exact_word_upper,
        "exact_witness": exact_witness,
        "griesmer": bound,
        "margin": bound - length_upper,
    }


def update_digest(digest: object, *values: object) -> None:
    digest.update(("|".join(map(repr, values)) + "\n").encode("ascii"))


def audit_all_dimension_two(original_minimum: int) -> dict[str, object]:
    """Classify and exhaust all dimension-2 column profiles."""
    digest = sha256()
    summaries: list[dict[str, object]] = []
    total_representatives = 0

    for count0 in range(POINTS + 1):
        for count1 in range(POINTS - count0 + 1):
            for count2 in range(POINTS - count0 - count1 + 1):
                count3 = POINTS - count0 - count1 - count2
                counts = (count0, count1, count2, count3)

                # Both generator rows must be even.
                if (count1 + count3) & 1 or (count2 + count3) & 1:
                    continue
                positive = {
                    value
                    for value in (1, 2, 3)
                    if counts[value] > 0
                }
                if binary_rank(positive, 2) != 2:
                    continue

                record = audit_fixed_profile(counts, original_minimum)
                summaries.append(record)
                total_representatives += int(
                    record["profile_representatives"]
                )
                update_digest(
                    digest,
                    counts,
                    record["h_weights"],
                    record["length_bounds"],
                    record["kernel_upper"],
                    record["image_lower"],
                    record["profile_representatives"],
                    record["distance_lower"],
                    record["lower_witness"],
                    record["exact_word_upper"],
                    record["exact_witness"],
                    record["griesmer"],
                    record["margin"],
                )

    best_margin = max(int(record["margin"]) for record in summaries)
    best_records = [
        record
        for record in summaries
        if int(record["margin"]) == best_margin
    ]
    contradictions = [
        record for record in summaries if int(record["margin"]) > 0
    ]
    return {
        "valid_h_profiles": len(summaries),
        "profile_representatives": total_representatives,
        "best_margin": best_margin,
        "best_records": best_records,
        "contradictions": contradictions,
        "enumeration_sha256": digest.hexdigest(),
    }


def original_even_code_minimum() -> int:
    candidates: list[int] = []
    for size in range(2, POINTS, 2):
        values = [FOURIER_LOWER[size]]
        if size == BLOCK_SIZE + 1:
            values.append(FOURIER_UPPER[size])
        candidates.extend((BLOCKS - value) // 2 for value in values)
    return min(candidates)


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
    original_minimum = original_even_code_minimum()
    assert original_minimum == 8_809_920

    result = audit_all_dimension_two(original_minimum)
    assert result["valid_h_profiles"] == 1_450
    assert result["profile_representatives"] == 1_567_276
    assert result["best_margin"] == -23_291
    assert len(result["best_records"]) == 24
    assert not result["contradictions"]
    assert result["enumeration_sha256"] == EXPECTED_DIMENSION_TWO_SHA256
    best = result["best_records"][0]
    assert best == {
        "dimension": 2,
        "counts": (0, 9, 9, 13),
        "h_weights": (0, 22, 22, 18),
        "length_bounds": (4_419_003, 4_419_003),
        "removed_upper": 13_259_832,
        "kernel_upper": 2,
        "image_lower": 28,
        "profile_representatives": 696,
        "distance_lower": 2_197_848,
        "lower_witness": ((0, 4, 4, 6), (14, 16, 16, 16)),
        "exact_word_upper": 2_201_720,
        "exact_witness": ((0, 0, 2, 12), (14, 12, 8, 28)),
        "griesmer": 4_395_712,
        "margin": -23_291,
    }
    print(
        "dimension_2_exhaustive=",
        {
            "valid_labelled_h_profiles": result["valid_h_profiles"],
            "profile_representatives": result["profile_representatives"],
            "tied_best_labelled_profiles": len(result["best_records"]),
            "best_record": best,
            "contradictions": len(result["contradictions"]),
            "enumeration_sha256": result["enumeration_sha256"],
        },
    )

    # These two profiles were selected by a separate seeded random search.
    # Their audits are exhaustive for the fixed profiles, but the pair is
    # not an exhaustive classification of dimension-3 subcodes.
    dimension_three = tuple(
        audit_fixed_profile(counts, original_minimum)
        for counts in (
            (10, 1, 2, 4, 6, 2, 1, 5),
            (1, 3, 5, 2, 3, 2, 4, 11),
        )
    )
    assert dimension_three[0]["distance_lower"] == 1_090_940
    assert dimension_three[0]["margin"] == -26_669
    assert dimension_three[1]["distance_lower"] == 1_093_188
    assert dimension_three[1]["margin"] == -23_291
    print("dimension_3_selected_nonexhaustive=", dimension_three)
    print("S(14,15,31) small-subcode shortening audit: PASS")


if __name__ == "__main__":
    main()
