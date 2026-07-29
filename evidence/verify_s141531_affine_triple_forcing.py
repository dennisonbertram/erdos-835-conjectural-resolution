#!/usr/bin/env python3
"""Verify a forced affine triple in every hypothetical S(14,15,31).

The static rational dual certificate proves the following conditional
statement.  If B1 and B2 are blocks with |B1 cap B2| = 6, then at least
666 blocks B3 satisfy

    |B1 cap B3| = |B2 cap B3| = 4,
    B1 cap B2 cap B3 = empty,
    B1 union B2 union B3 = X.

The complements of B1, B2, B3 are the three weight-16 points in an affine
2-flat whose fourth point has weight 14.  This realizes, rather than merely
permits, all three unresolved middle-layer endpoints in the best
dimension-two common-zero shortening.

Only Python's standard library is needed.  No floating-point optimizer is
used by this verifier.
"""

from __future__ import annotations

import base64
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path
import zlib


POINTS = 31
DESIGN_T = 14
BLOCK_SIZE = 15
BLOCKS = comb(POINTS, DESIGN_T) // BLOCK_SIZE
MIDDLE_CORRECTION = 1 << BLOCK_SIZE
CAPACITIES = (6, 9, 9, 7)
FIRST = (6, 9, 0, 0)
SECOND = (6, 0, 9, 0)
TARGET = (0, 4, 4, 7)
DUAL_SHA256 = "dc904285cac5b121f09553a930fb213a764bf31e216780e463491db43047fdef"

LAMBDA = tuple(
    comb(POINTS - level, DESIGN_T - level) // (BLOCK_SIZE - level)
    for level in range(DESIGN_T + 1)
)


def bounded_compositions(total: int, capacities: tuple[int, ...]):
    for values in product(*(range(capacity + 1) for capacity in capacities)):
        if sum(values) == total:
            yield values


def coefficient(profile: tuple[int, ...], moment: tuple[int, ...]) -> int:
    answer = 1
    for present, selected in zip(profile, moment):
        if selected > present:
            return 0
        answer *= comb(present, selected)
    return answer


def forced_zero(profile: tuple[int, ...]) -> bool:
    """Steiner systems have no two distinct blocks sharing 14 points."""
    return (
        profile != FIRST and profile[0] + profile[1] >= DESIGN_T
    ) or (
        profile != SECOND and profile[0] + profile[2] >= DESIGN_T
    )


def live_profiles() -> tuple[tuple[int, ...], ...]:
    return tuple(
        profile
        for profile in bounded_compositions(BLOCK_SIZE, CAPACITIES)
        if profile not in (FIRST, SECOND) and not forced_zero(profile)
    )


def load_dual() -> dict[tuple[int, ...], Fraction]:
    path = Path(__file__).with_name("s141531_affine_triple_dual.b85")
    compressed = base64.b85decode(path.read_bytes().strip())
    raw = zlib.decompress(compressed)
    assert sha256(raw).hexdigest() == DUAL_SHA256
    records = json.loads(raw)
    assert len(records) == 396

    dual: dict[tuple[int, ...], Fraction] = {}
    for raw_moment, numerator, denominator in records:
        moment = tuple(raw_moment)
        assert len(moment) == 4
        assert sum(moment) == DESIGN_T
        assert all(
            0 <= selected <= capacity
            for selected, capacity in zip(moment, CAPACITIES)
        )
        assert denominator > 0
        assert moment not in dual
        dual[moment] = Fraction(numerator, denominator)
    return dual


def verify_dual() -> tuple[Fraction, Fraction]:
    """Check the exact LP-dual inequality N_TARGET >= 666."""
    dual = load_dual()
    facets = set(bounded_compositions(DESIGN_T, CAPACITIES))
    assert set(dual) <= facets
    assert len(facets) == 406

    objective = Fraction(0)
    for moment, multiplier in dual.items():
        # There is one design block through every actual 14-subset.  The
        # aggregate right side is the number of 14-subsets of this profile,
        # after removing the two fixed blocks.
        rhs = 1
        for capacity, selected in zip(CAPACITIES, moment):
            rhs *= comb(capacity, selected)
        rhs -= coefficient(FIRST, moment)
        rhs -= coefficient(SECOND, moment)
        assert rhs >= 0
        objective += multiplier * rhs
    assert objective == 666

    minimum_slack: Fraction | None = None
    for profile in live_profiles():
        dual_coefficient = sum(
            multiplier * coefficient(profile, moment)
            for moment, multiplier in dual.items()
        )
        primal_coefficient = Fraction(profile == TARGET)
        slack = primal_coefficient - dual_coefficient
        assert slack >= 0
        if minimum_slack is None or slack < minimum_slack:
            minimum_slack = slack
    assert minimum_slack == 0
    return objective, minimum_slack


def fixed_block_intersection_distribution() -> tuple[int, ...]:
    """Recover the exact intersection distribution about one fixed block."""
    distribution = [0] * (BLOCK_SIZE + 1)
    distribution[BLOCK_SIZE] = 1
    for intersection in range(DESIGN_T, -1, -1):
        moment = comb(BLOCK_SIZE, intersection) * LAMBDA[intersection]
        distribution[intersection] = moment - sum(
            comb(larger, intersection) * distribution[larger]
            for larger in range(intersection + 1, BLOCK_SIZE + 1)
        )
    answer = tuple(distribution)
    assert answer == (
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
    return answer


def fourier_external(size: int) -> int:
    if size > BLOCK_SIZE:
        return -fourier_external(POINTS - size)
    return sum(
        (-2) ** level * comb(size, level) * LAMBDA[level]
        for level in range(min(size, DESIGN_T) + 1)
    )


def fourier_upper(size: int) -> int:
    return fourier_external(size) + (
        MIDDLE_CORRECTION if size == BLOCK_SIZE + 1 else 0
    )


def dot(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def word_weights(counts: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(counts[value] for value in range(4) if dot(word, value))
        for word in range(4)
    )


def translated_weights(
    counts: tuple[int, ...], profile: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(
        sum(
            (
                counts[value] - profile[value]
                if dot(word, value)
                else profile[value]
            )
            for value in range(4)
        )
        for word in range(4)
    )


def ceil_div(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def griesmer(distance: int, dimension: int) -> int:
    return sum(
        ceil_div(distance, 1 << power) for power in range(dimension)
    )


def verify_shortening_endpoint_is_attained() -> dict[str, int]:
    """Check the exact best-profile shortening parameters."""
    counts = (0, 9, 9, 13)
    h_weights = word_weights(counts)
    assert h_weights == (0, 22, 22, 18)
    base_sum = sum(fourier_external(weight) for weight in h_weights)
    assert base_sum % 4 == 0
    length = base_sum // 4
    assert length == 4_419_003

    subgroup_profiles = {
        tuple(
            counts[value] if dot(word, value) else 0
            for value in range(4)
        )
        for word in range(4)
    }
    lower_distance: int | None = None
    lower_patterns: set[tuple[int, ...]] = set()
    for profile in product(*(range(count + 1) for count in counts)):
        if sum(profile) & 1 or profile in subgroup_profiles:
            continue
        weights = translated_weights(counts, profile)
        lower = ceil_div(
            base_sum - sum(fourier_upper(weight) for weight in weights),
            8,
        )
        if lower_distance is None or lower < lower_distance:
            lower_distance = lower
            lower_patterns = {weights}
        elif lower == lower_distance:
            lower_patterns.add(weights)
    assert lower_distance == 2_197_848
    assert (14, 16, 16, 16) in lower_patterns

    # The forced triple makes all three size-16 terms internal, so this safe
    # lower endpoint is an actual punctured word weight.
    actual_coset_sum = fourier_external(14) + 3 * fourier_upper(16)
    actual_weight = (base_sum - actual_coset_sum) // 8
    assert actual_weight == lower_distance

    original_minimum = 8_809_920
    removed = BLOCKS - length
    assert griesmer(original_minimum, 3) > removed
    image_dimension = 30 - 2
    assert griesmer(actual_weight, image_dimension) == 4_395_712
    assert length - griesmer(actual_weight, image_dimension) == 23_291
    return {
        "length": length,
        "dimension": image_dimension,
        "distance": actual_weight,
        "griesmer": griesmer(actual_weight, image_dimension),
        "slack": 23_291,
    }


def verify_affine_translation() -> dict[str, object]:
    """Construct a canonical set-theoretic instance of the profile map."""
    universe = (1 << POINTS) - 1
    intersection = sum(1 << point for point in range(0, 6))
    first_only = sum(1 << point for point in range(6, 15))
    second_only = sum(1 << point for point in range(15, 24))
    outside = sum(1 << point for point in range(24, 31))
    b1 = intersection | first_only
    b2 = intersection | second_only
    b3 = (
        outside
        | sum(1 << point for point in range(6, 10))
        | sum(1 << point for point in range(15, 19))
    )
    assert tuple(block.bit_count() for block in (b1, b2, b3)) == (15, 15, 15)
    assert (b1 & b2).bit_count() == 6
    assert (b1 & b3).bit_count() == 4
    assert (b2 & b3).bit_count() == 4
    assert b1 & b2 & b3 == 0
    assert b1 | b2 | b3 == universe

    d1, d2, d3 = (universe ^ block for block in (b1, b2, b3))
    q = d1 ^ d2 ^ d3
    h1 = d1 ^ d2
    h2 = d1 ^ d3
    assert tuple(value.bit_count() for value in (d1, d2, d3)) == (16, 16, 16)
    assert q.bit_count() == 14
    assert sorted(
        value.bit_count() for value in (h1, h2, h1 ^ h2)
    ) == [18, 22, 22]
    assert sorted(
        (q ^ value).bit_count() for value in (0, h1, h2, h1 ^ h2)
    ) == [14, 16, 16, 16]

    column_counts = [0] * 4
    q_profile = [0] * 4
    for point in range(POINTS):
        column = ((h1 >> point) & 1) | (((h2 >> point) & 1) << 1)
        column_counts[column] += 1
        q_profile[column] += (q >> point) & 1
    assert sorted(column_counts) == [0, 9, 9, 13]
    assert sorted(q_profile) == [0, 4, 4, 6]
    return {
        "subspace_nonzero_weights": (18, 22, 22),
        "coset_weights": (14, 16, 16, 16),
        "column_counts_up_to_GL2": (0, 9, 9, 13),
        "coset_profile_up_to_GL2": (0, 4, 4, 6),
    }


def main() -> None:
    assert BLOCKS == 17_678_835
    dual_objective, minimum_slack = verify_dual()
    distribution = fixed_block_intersection_distribution()
    affine = verify_affine_translation()
    shortening = verify_shortening_endpoint_is_attained()

    unordered_intersection_six_pairs = BLOCKS * distribution[6] // 2
    forced_affine_planes = unordered_intersection_six_pairs * int(
        dual_objective
    )
    assert forced_affine_planes == 19_800_275_399_704_800

    print(f"dual_sha256={DUAL_SHA256}")
    print(f"dual_entries=396 exact_objective={dual_objective}")
    print(f"minimum_dual_slack={minimum_slack}")
    print(f"partners_at_intersection_6_per_block={distribution[6]}")
    print(f"forced_profile_blocks_per_pair_at_least={dual_objective}")
    print(f"forced_affine_planes_at_least={forced_affine_planes}")
    print(f"affine_translation={affine}")
    print(f"shortened_code={shortening}")
    print("S(14,15,31) affine-triple forcing: PASS")


if __name__ == "__main__":
    main()
