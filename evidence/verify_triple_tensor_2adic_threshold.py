#!/usr/bin/env python3
"""Exact controls for triple_tensor_2adic_threshold_audit.md.

The tensor is computed directly from signed-support bitsets.  All
arithmetic is over Python integers; no numerical libraries or solvers are
used.
"""

from collections import Counter
from itertools import combinations
from math import comb, factorial


def perfect_matchings(points):
    points = tuple(points)
    if not points:
        yield ()
        return
    first = points[0]
    for position in range(1, len(points)):
        second = points[position]
        rest = points[1:position] + points[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def e_value(matching, block):
    block = set(block)
    value = 1
    for left, right in matching:
        value *= int(left in block) - int(right in block)
    return value


def signed_support(matching, blocks):
    positive = 0
    negative = 0
    values = []
    for index, block in enumerate(blocks):
        value = e_value(matching, block)
        values.append(value)
        if value == 1:
            positive |= 1 << index
        elif value == -1:
            negative |= 1 << index
    return positive, negative, tuple(values)


def direct_tensor(support_m, support_n, support_l):
    positive_m, negative_m, _ = support_m
    positive_n, negative_n, _ = support_n
    positive_l, negative_l, _ = support_l
    common = (
        (positive_m | negative_m)
        & (positive_n | negative_n)
        & (positive_l | negative_l)
    )
    negative_product = negative_m ^ negative_n ^ negative_l
    negative_common = common & negative_product
    positive_count = (common & ~negative_product).bit_count()
    negative_count = negative_common.bit_count()
    return positive_count - negative_count


def enumerate_sqs8():
    points = tuple(range(8))
    blocks = tuple(combinations(points, 4))
    triples = tuple(combinations(points, 3))
    block_triples = [
        tuple(
            index
            for index, triple in enumerate(triples)
            if set(triple) <= set(block)
        )
        for block in blocks
    ]
    triple_blocks = [
        tuple(
            index
            for index, block in enumerate(blocks)
            if set(triple) <= set(block)
        )
        for triple in triples
    ]
    full = (1 << len(triples)) - 1
    systems = []

    def search(covered, selected):
        if covered == full:
            assert len(selected) == 14
            systems.append(sum(1 << index for index in selected))
            return
        choices = []
        for triple_index in range(len(triples)):
            if (covered >> triple_index) & 1:
                continue
            viable = [
                block_index
                for block_index in triple_blocks[triple_index]
                if all(
                    not ((covered >> inner) & 1)
                    for inner in block_triples[block_index]
                )
            ]
            choices.append((len(viable), viable))
        _, viable = min(choices)
        for block_index in viable:
            next_covered = covered
            for triple_index in block_triples[block_index]:
                next_covered |= 1 << triple_index
            search(next_covered, selected + (block_index,))

    search(0, ())
    systems = tuple(sorted(set(systems)))
    assert len(systems) == 30
    return blocks, systems


def systems_for_parameter(k, matchings, blocks):
    if k == 2:
        block_index = {block: index for index, block in enumerate(blocks)}
        systems = []
        for matching in matchings:
            systems.append(
                sum(
                    1 << block_index[tuple(sorted(edge))]
                    for edge in matching
                )
            )
        assert len(set(systems)) == 3
        return tuple(systems)
    assert k == 4
    sqs_blocks, systems = enumerate_sqs8()
    assert sqs_blocks == blocks
    return systems


def check_exact_designs(k, blocks, systems):
    point_count = 2 * k
    facets = tuple(combinations(range(point_count), k - 1))
    blocks_through = [
        tuple(
            index
            for index, block in enumerate(blocks)
            if set(facet) <= set(block)
        )
        for facet in facets
    ]
    point_set = set(range(point_count))
    block_index = {block: index for index, block in enumerate(blocks)}
    for system in systems:
        assert all(
            sum((system >> index) & 1 for index in containing) == 1
            for containing in blocks_through
        )
        for index, block in enumerate(blocks):
            if not ((system >> index) & 1):
                continue
            complement = tuple(sorted(point_set - set(block)))
            assert (system >> block_index[complement]) & 1


def valuation_two(number):
    valuation = 0
    while number % 2 == 0:
        valuation += 1
        number //= 2
    return valuation, number


def has_disjoint_triangle(systems):
    for left, middle, right in combinations(range(len(systems)), 3):
        if (
            systems[left] & systems[middle] == 0
            and systems[left] & systems[right] == 0
            and systems[middle] & systems[right] == 0
        ):
            return True
    return False


def exhaust_parameter(k):
    p = k + 1
    blocks = tuple(combinations(range(2 * k), k))
    matchings = tuple(perfect_matchings(range(2 * k)))
    supports = tuple(signed_support(matching, blocks) for matching in matchings)
    e_vectors = tuple(support[2] for support in supports)
    systems = systems_for_parameter(k, matchings, blocks)
    check_exact_designs(k, blocks, systems)

    indicators = tuple(
        tuple((system >> index) & 1 for index in range(len(blocks)))
        for system in systems
    )
    deltas = tuple(
        tuple(
            sum(indicator[index] * e[index] for index in range(len(blocks)))
            for e in e_vectors
        )
        for indicator in indicators
    )
    assert all(value % 2 == 0 for row in deltas for value in row)
    half_deltas = tuple(
        tuple(value // 2 for value in row) for row in deltas
    )

    # Independently check the frame reconstruction E^T Delta =
    # k! (p f - 1) point by point.
    scale = factorial(k)
    for indicator, delta in zip(indicators, deltas):
        for block_index in range(len(blocks)):
            reconstructed = sum(
                delta[matching_index] * e_vectors[matching_index][block_index]
                for matching_index in range(len(matchings))
            )
            assert reconstructed == scale * (
                p * indicator[block_index] - 1
            )

    s, u = valuation_two(scale)
    forced_exponent = 2 * s - 2
    assert forced_exponent >= 0
    forced_power = 1 << forced_exponent

    disjoint_pair_count = sum(
        systems[left] & systems[right] == 0
        for left in range(len(systems))
        for right in range(len(systems))
    )
    disjoint_parities = Counter()
    overlap_cases = 0
    overlap_nonzero = 0
    overlap_odd = 0

    # For each outer matching build tau_{M,N,L}=T_{M,N,L}/2 directly
    # from the signed supports.  Matrix-vector multiplication then
    # exhausts every ordered pair of exact designs.
    for outer in range(len(matchings)):
        tau_rows = []
        for left in range(len(matchings)):
            row = []
            for right in range(len(matchings)):
                tensor = direct_tensor(
                    supports[outer], supports[left], supports[right]
                )
                assert tensor % 2 == 0
                row.append(tensor // 2)
            tau_rows.append(tuple(row))

        images = []
        for right_design in range(len(systems)):
            vector = half_deltas[right_design]
            images.append(
                tuple(
                    sum(row[index] * vector[index] for index in range(len(row)))
                    for row in tau_rows
                )
            )

        for left_design in range(len(systems)):
            left_vector = half_deltas[left_design]
            for right_design in range(len(systems)):
                a_value = sum(
                    left_vector[index] * images[right_design][index]
                    for index in range(len(matchings))
                )
                assert a_value % forced_power == 0
                quotient = a_value // forced_power

                overlap_derivative = sum(
                    indicators[left_design][index]
                    * indicators[right_design][index]
                    * e_vectors[outer][index]
                    for index in range(len(blocks))
                )
                assert overlap_derivative % 2 == 0
                omega = overlap_derivative // 2
                expected = p * u * u * (
                    p * omega
                    - half_deltas[left_design][outer]
                    - half_deltas[right_design][outer]
                )
                assert quotient == expected

                pretend_disjoint = -p * u * u * (
                    half_deltas[left_design][outer]
                    + half_deltas[right_design][outer]
                )
                assert quotient - pretend_disjoint == p * p * u * u * omega

                if systems[left_design] & systems[right_design] == 0:
                    assert omega == 0
                    assert quotient == pretend_disjoint
                    disjoint_parities[quotient & 1] += 1
                else:
                    overlap_cases += 1
                    overlap_nonzero += omega != 0
                    overlap_odd += omega & 1

    if k == 2:
        assert len(systems) == 3
        assert disjoint_pair_count == 6
        assert disjoint_parities == Counter({1: 12, 0: 6})
        assert overlap_cases == 9
        assert overlap_nonzero == overlap_odd == 6
        full = (1 << len(blocks)) - 1
        assert sum(systems) == full
    else:
        assert k == 4
        assert len(systems) == 30
        assert disjoint_pair_count == 240
        assert disjoint_parities == Counter({1: 13_440, 0: 11_760})
        assert overlap_cases == 69_300
        assert overlap_nonzero == 25_830
        assert overlap_odd == 21_840
        degrees = [
            sum(
                left != right and systems[left] & systems[right] == 0
                for right in range(len(systems))
            )
            for left in range(len(systems))
        ]
        assert set(degrees) == {8}
        assert not has_disjoint_triangle(systems)

    print(
        f"k={k}: {len(systems)} exact designs, {len(matchings)} matchings; "
        f"{disjoint_pair_count * len(matchings):,} disjoint-pair contractions; "
        f"quotient parity 0/1 = "
        f"{disjoint_parities[0]:,}/{disjoint_parities[1]:,}"
    )
    print(
        f"k={k}: {overlap_cases:,} overlapping-pair contractions; "
        f"omega nonzero/odd = {overlap_nonzero:,}/{overlap_odd:,}"
    )


def check_target():
    k, p = 16, 17
    s, u = valuation_two(factorial(k))
    assert s == 15
    assert u == 638_512_875
    assert 2 * s - 2 == 28
    assert p % 8 == 1
    assert u * u % 8 == 1

    # The exact large-set quotient coefficients in (14).
    self_coefficient = p * u * u * (p - 2)
    cross_coefficient = -p * u * u
    assert self_coefficient % 8 == 7
    assert cross_coefficient % 8 == 7

    # Symbolic binary colour-matrix check for every even-weight delta.
    for delta_mask in range(1 << p):
        if delta_mask.bit_count() % 2:
            continue
        rows = []
        for left in range(p):
            left_bit = (delta_mask >> left) & 1
            row = 0
            for right in range(p):
                right_bit = (delta_mask >> right) & 1
                value = (
                    left_bit
                    if left == right
                    else left_bit ^ right_bit
                )
                row |= value << right
            rows.append(row)
        full = (1 << p) - 1
        assert all((row & full).bit_count() % 2 == 0 for row in rows)
        for left, middle, right in combinations(range(p), 3):
            q_lm = (rows[left] >> middle) & 1
            q_lr = (rows[left] >> right) & 1
            q_mr = (rows[middle] >> right) & 1
            assert q_lm ^ q_lr ^ q_mr == 0

    print(
        "k=16: s=15, u=638512875, forced exponent=28; "
        "mod-2 colour matrices and triangle relations are consistent"
    )


if __name__ == "__main__":
    exhaust_parameter(2)
    exhaust_parameter(4)
    check_target()
    print("PASS: overlap-sensitive 2-adic threshold audit verified.")
