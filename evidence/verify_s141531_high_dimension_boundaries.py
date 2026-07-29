#!/usr/bin/env python3
"""Exact audit of two high-dimensional shortening boundaries.

This is a necessary-condition audit for a hypothetical S(14,15,31).
It does not prove existence or nonexistence of the design.

Only Python's standard library is used.  The two subspaces were found by
heuristic search, but every assertion about each frozen subspace is checked
exhaustively here.
"""

from __future__ import print_function

from collections import Counter, defaultdict
from hashlib import sha256
from math import comb, gcd


POINTS = 31
SUPPORT = 15
OUTSIDE = POINTS - SUPPORT
EVEN_DIMENSION = 30
BLOCKS = 17_678_835
MIDDLE_CORRECTION = 1 << 15

# External value at point-weight 16.  An actual complement of a block adds
# 2^15 to this Fourier value.
FOURIER_EXTERNAL = (
    17_678_835, 570_285, -570_285, -58_995, 58_995, 10_925,
    -10_925, -3_059, 3_059, 1_197, -1_197, -627, 627, 429,
    -429, 1_549, -1_549, 429, -429, -627, 627, 1_197, -1_197,
    -3_059, 3_059, 10_925, -10_925, -58_995, 58_995, 570_285,
    -570_285, -17_678_835,
)

M10_BASIS = (
    0x5, 0x35, 0x5C, 0xE4, 0x1FD,
    0x21C, 0x4E0, 0xA5C, 0x1015, 0x5341,
)
M12_BASIS = (
    0x3, 0x1B, 0x36, 0x7E, 0xA9, 0x1D0,
    0x291, 0x7CB, 0x80E, 0x1E11, 0x2844, 0x4B47,
)

EXPECTED_DIGEST = (
    "141e305903c70c68dd2d24c261cbebb27285a1db78a8e10de4032ca0a40278f7"
)


def popcount(value):
    return bin(value).count("1")


def binary_rank(rows, width=SUPPORT):
    pivots = [0] * width
    rank = 0
    for original in rows:
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivots[pivot]:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                rank += 1
                break
    return rank


def span(basis):
    words = [0]
    for row in basis:
        words += [word ^ row for word in words]
    assert len(set(words)) == 1 << len(basis)
    return tuple(sorted(words))


def ceil_div(numerator, denominator):
    return -((-numerator) // denominator)


def griesmer(distance, dimension):
    return sum(
        ceil_div(distance, 1 << power)
        for power in range(dimension)
    )


def coordinate_classes(subgroup):
    """Classes whose coordinate transpositions are weight-two words of H."""
    subgroup_set = set(subgroup)
    parent = list(range(SUPPORT))

    def find(value):
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def unite(left, right):
        left = find(left)
        right = find(right)
        if left != right:
            parent[right] = left

    for left in range(SUPPORT):
        for right in range(left + 1, SUPPORT):
            if (1 << left) ^ (1 << right) in subgroup_set:
                unite(left, right)

    root_to_index = {}
    classes = []
    coordinate_class = []
    for coordinate in range(SUPPORT):
        root = find(coordinate)
        if root not in root_to_index:
            root_to_index[root] = len(classes)
            classes.append([])
        index = root_to_index[root]
        classes[index].append(coordinate)
        coordinate_class.append(index)

    # Transitivity must make every class a complete set of weight-two words.
    for members in classes:
        for left in members:
            for right in members:
                if left != right:
                    assert (1 << left) ^ (1 << right) in subgroup_set
    return tuple(tuple(group) for group in classes), tuple(coordinate_class)


def hoffman_component_upper(class_sizes, signature):
    """Hoffman upper bound for a Cartesian product of Johnson graphs."""
    vertices = 1
    degree = 0
    least_absolute = 0
    for size, selected in zip(class_sizes, signature):
        vertices *= comb(size, selected)
        degree += selected * (size - selected)
        least_absolute += min(selected, size - selected)
    if degree == 0:
        return vertices, vertices, degree, least_absolute
    upper = (vertices * least_absolute) // (degree + least_absolute)
    return upper, vertices, degree, least_absolute


def analyze_frozen_subspace(basis, use_joint_bound):
    dimension = len(basis)
    assert binary_rank(basis) == dimension
    assert all(popcount(row) % 2 == 0 for row in basis)
    subgroup = span(basis)
    order = len(subgroup)
    assert order == 1 << dimension
    assert all(popcount(word) % 2 == 0 for word in subgroup)
    assert max(popcount(word) for word in subgroup) <= 14

    subgroup_sum = sum(
        FOURIER_EXTERNAL[popcount(word)] for word in subgroup
    )
    assert subgroup_sum % order == 0
    length = subgroup_sum // order
    correction_quantum = MIDDLE_CORRECTION // (2 * order)
    assert MIDDLE_CORRECTION == correction_quantum * 2 * order

    classes, coordinate_class = coordinate_classes(subgroup)
    class_sizes = tuple(len(group) for group in classes)

    seen = set()
    exact_enumerator = Counter()
    middle_profiles = Counter()
    safe_lower = None
    safe_witness = None
    exact_cap = None
    exact_cap_witness = None
    record_digest = sha256()
    quotient_words = 0

    for representative in range(1 << SUPPORT):
        if representative in seen:
            continue
        translated = tuple(representative ^ word for word in subgroup)
        assert not any(member in seen for member in translated)
        seen.update(translated)
        inside_counts = Counter(popcount(member) for member in translated)
        parity = popcount(representative) & 1

        for outside_size in range(parity, OUTSIDE + 1, 2):
            if representative == 0 and outside_size == 0:
                continue
            multiplicity = comb(OUTSIDE, outside_size)
            quotient_words += multiplicity
            translated_sum = sum(
                count * FOURIER_EXTERNAL[inside + outside_size]
                for inside, count in inside_counts.items()
            )
            numerator = subgroup_sum - translated_sum
            assert numerator % (2 * order) == 0
            base_weight = numerator // (2 * order)
            middle_inside_weight = 16 - outside_size
            middle_count = inside_counts[middle_inside_weight]

            independent_upper = middle_count
            component_summary = ()
            if use_joint_bound and middle_count:
                components = defaultdict(int)
                for member in translated:
                    if popcount(member) != middle_inside_weight:
                        continue
                    signature = [0] * len(classes)
                    for coordinate in range(SUPPORT):
                        if (member >> coordinate) & 1:
                            signature[coordinate_class[coordinate]] += 1
                    components[tuple(signature)] += 1

                independent_upper = 0
                summary_rows = []
                for signature in sorted(components):
                    observed = components[signature]
                    upper, vertices, degree, least_absolute = (
                        hoffman_component_upper(class_sizes, signature)
                    )
                    assert observed == vertices
                    independent_upper += upper
                    summary_rows.append(
                        (signature, observed, upper, degree, least_absolute)
                    )
                component_summary = tuple(summary_rows)

            lower = base_weight - correction_quantum * independent_upper
            if safe_lower is None or lower < safe_lower:
                safe_lower = lower
                safe_witness = (
                    representative,
                    outside_size,
                    base_weight,
                    middle_count,
                    independent_upper,
                    component_summary,
                )

            if middle_count == 0:
                exact_enumerator[base_weight] += multiplicity
                if exact_cap is None or base_weight < exact_cap:
                    exact_cap = base_weight
                    exact_cap_witness = (
                        representative, outside_size, base_weight
                    )
            else:
                middle_profiles[
                    (outside_size, base_weight, middle_count)
                ] += multiplicity

            record_digest.update(
                repr(
                    (
                        dimension,
                        representative,
                        outside_size,
                        multiplicity,
                        base_weight,
                        middle_count,
                        independent_upper,
                    )
                ).encode("ascii")
            )
            record_digest.update(b"\n")

    assert len(seen) == 1 << SUPPORT
    assert quotient_words == (1 << (EVEN_DIMENSION - dimension)) - 1
    assert safe_lower is not None and exact_cap is not None

    return {
        "basis": basis,
        "dimension": dimension,
        "order": order,
        "length": length,
        "image_dimension": EVEN_DIMENSION - dimension,
        "correction_quantum": correction_quantum,
        "classes": classes,
        "class_sizes": class_sizes,
        "safe_lower": safe_lower,
        "safe_witness": safe_witness,
        "exact_cap": exact_cap,
        "exact_cap_witness": exact_cap_witness,
        "exact_enumerator": exact_enumerator,
        "middle_profiles": middle_profiles,
        "record_digest": record_digest.hexdigest(),
    }


def verify_m10():
    result = analyze_frozen_subspace(M10_BASIS, use_joint_bound=False)
    assert result["length"] == 16_359
    assert result["image_dimension"] == 20
    assert result["correction_quantum"] == 16
    assert result["class_sizes"] == (3, 1, 3, 3, 4, 1)
    assert result["safe_lower"] == 1_640
    assert result["exact_cap"] == 8_024
    assert griesmer(8_024, 20) == 16_056
    assert result["length"] - griesmer(8_024, 20) == 303
    expected_enumerator = Counter(
        {
            8_024: 513,
            8_056: 57,
            8_212: 2_907,
            8_596: 171,
            8_628: 19,
            10_868: 3,
        }
    )
    assert result["exact_enumerator"] == expected_enumerator
    assert sum(expected_enumerator.values()) == 3_670

    exact_gcd = 0
    for weight in expected_enumerator:
        exact_gcd = gcd(exact_gcd, weight)
    assert exact_gcd == 4
    # Every uncertain word is base_weight - 16*t.  All bases are divisible
    # by four, so every actual word is divisible by four.
    assert all(
        base_weight % 4 == 0
        for (_, base_weight, _), _multiplicity
        in result["middle_profiles"].items()
    )

    return result


def verify_m12():
    result = analyze_frozen_subspace(M12_BASIS, use_joint_bound=True)
    assert result["length"] == 4_291
    assert result["image_dimension"] == 18
    assert result["correction_quantum"] == 4
    assert result["class_sizes"] == (3, 4, 4, 4)
    assert result["safe_lower"] == 556
    assert result["exact_cap"] == 2_188
    assert griesmer(2_188, 18) == 4_387
    assert result["length"] - griesmer(2_188, 18) == -96
    assert griesmer(556, 18) == 1_123
    assert result["length"] - griesmer(556, 18) == 3_168
    # Positivity is what proves that the restriction kernel is exactly H.
    assert result["safe_lower"] > 0
    return result


def main():
    m10 = verify_m10()
    m12 = verify_m12()
    combined = sha256()
    for result in (m10, m12):
        combined.update(result["record_digest"].encode("ascii"))
        combined.update(b"\n")
    digest = combined.hexdigest()
    assert digest == EXPECTED_DIGEST

    print(
        "m10=",
        {
            "basis": tuple(hex(row) for row in M10_BASIS),
            "length": m10["length"],
            "image_dimension": m10["image_dimension"],
            "safe_distance_lower": m10["safe_lower"],
            "exact_word_upper": m10["exact_cap"],
            "exact_enumerator": sorted(m10["exact_enumerator"].items()),
            "divisibility": 4,
            "griesmer_at_exact_upper": griesmer(m10["exact_cap"], 20),
            "slack": 303,
        },
    )
    print(
        "m12=",
        {
            "basis": tuple(hex(row) for row in M12_BASIS),
            "length": m12["length"],
            "image_dimension": m12["image_dimension"],
            "class_sizes": m12["class_sizes"],
            "joint_distance_lower": m12["safe_lower"],
            "joint_witness": m12["safe_witness"],
            "exact_word_upper": m12["exact_cap"],
            "exact_cap_witness": m12["exact_cap_witness"],
            "griesmer_at_joint_lower": griesmer(m12["safe_lower"], 18),
            "griesmer_at_exact_upper": griesmer(m12["exact_cap"], 18),
            "cap_slack": -96,
        },
    )
    print("combined_record_sha256=", digest)
    print("S(14,15,31) high-dimensional boundary audit: PASS")


if __name__ == "__main__":
    main()
