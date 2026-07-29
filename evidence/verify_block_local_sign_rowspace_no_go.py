#!/usr/bin/env python3
"""Exact verifier for block_local_sign_rowspace_no_go.md."""

from itertools import combinations, permutations

from verify_fixed_base_parity import (
    GF2Space,
    block_vector,
    exact_cover,
    popcount,
    system_perms,
)


def inversion_parity(sequence):
    return sum(
        sequence[i] > sequence[j]
        for i in range(len(sequence))
        for j in range(i + 1, len(sequence))
    ) % 2


def build_instance(n, r):
    points = frozenset(range(n))
    blocks = [frozenset(item) for item in combinations(range(n), r)]
    facets = list(combinations(range(n), r - 1))
    facets_of = {
        index: [
            facet for facet in facets if frozenset(facet) <= block
        ]
        for index, block in enumerate(blocks)
    }

    def columns(allowed):
        result = {facet: set() for facet in facets}
        for index in allowed:
            for facet in facets_of[index]:
                result[facet].add(index)
        return result

    base_solution = exact_cover(
        columns(range(len(blocks))), facets_of, cap=1
    )[0]
    base = sorted((blocks[index] for index in base_solution), key=sorted)
    base_set = set(base)
    nonbase = [block for block in blocks if block not in base_set]
    nonbase_index = {block: index for index, block in enumerate(nonbase)}
    allowed = [
        index for index, block in enumerate(blocks)
        if block not in base_set
    ]
    mates = [
        frozenset(blocks[index] for index in solution)
        for solution in exact_cover(columns(allowed), facets_of)
    ]

    rowspace = GF2Space()
    rows = []
    for row_index, facet_tuple in enumerate(facets):
        facet = frozenset(facet_tuple)
        row = sum(
            1 << index
            for index, block in enumerate(nonbase)
            if facet <= block
        )
        rows.append(row)
        rowspace.add(row, 1 << row_index)

    return {
        "n": n,
        "r": r,
        "points": points,
        "blocks": blocks,
        "facets": facets,
        "base": base,
        "base_set": base_set,
        "nonbase": nonbase,
        "nonbase_index": nonbase_index,
        "mates": mates,
        "rowspace": rowspace,
        "rows": rows,
    }


def block_data(instance, block):
    points = instance["points"]
    base = instance["base"]

    encodings = []
    for sphere in base:
        remainder = points - sphere - block
        if len(remainder) == 1 and block == points - sphere - remainder:
            encodings.append((sphere, next(iter(remainder))))
    assert len(encodings) == 1
    mate_sphere, p = encodings[0]

    theta = {p: p}
    incidence = {p: (mate_sphere, "*")}
    for w in block:
        facet = block - {w}
        hits = [sphere for sphere in base if facet <= sphere]
        assert len(hits) == 1
        sphere = hits[0]
        difference = sphere - facet
        assert len(difference) == 1
        x = next(iter(difference))
        assert x != p
        assert x not in theta
        theta[x] = w
        incidence[w] = (sphere, x)

    assert set(theta) == set(points - block)
    assert set(theta.values()) == set(block | {p})
    assert len(set(incidence.values())) == instance["r"] + 1
    return p, theta, incidence


def theta_vector(instance, point_order):
    order = {point: index for index, point in enumerate(point_order)}
    vector = 0
    for index, block in enumerate(instance["nonbase"]):
        p, theta, _ = block_data(instance, block)
        domain = sorted(instance["points"] - block, key=order.get)
        codomain = sorted(block | {p}, key=order.get)
        position = {point: j for j, point in enumerate(codomain)}
        permutation = [position[theta[point]] for point in domain]
        if inversion_parity(permutation):
            vector |= 1 << index
    return vector


def mate_vector(instance, mate):
    return block_vector(mate, instance["nonbase_index"])


def assert_kernel_witness(instance, support, h):
    vector = sum(
        1 << instance["nonbase_index"][frozenset(block)]
        for block in support
    )
    assert all(popcount(row & vector) % 2 == 0
               for row in instance["rows"])
    assert popcount(vector & h) % 2 == 1
    return vector


def exact_mate_difference_dimension(instance):
    space = GF2Space()
    base_vector = mate_vector(instance, instance["mates"][0])
    for mate in instance["mates"][1:]:
        space.add(base_vector ^ mate_vector(instance, mate), 0)
    return space.dim


def exterior_lists(instance):
    e_position = {}
    f_position = {}
    index = 0
    for sphere in instance["base"]:
        for content in sorted(instance["points"] - sphere):
            e_position[(sphere, content)] = index
            index += 1
    index = 0
    for sphere in instance["base"]:
        for slot in sorted(sphere):
            f_position[(sphere, slot)] = index
            index += 1
        f_position[(sphere, "*")] = index
        index += 1

    result = {}
    for block in instance["nonbase"]:
        _, _, incidence = block_data(instance, block)
        contents = sorted(incidence)
        e_list = [
            e_position[(incidence[content][0], content)]
            for content in contents
        ]
        f_list = [
            f_position[incidence[content]]
            for content in contents
        ]
        assert inversion_parity(e_list) == inversion_parity(f_list)
        result[block] = (e_list, f_list)
    return result


def cross_parity(lists, left, right):
    left_e, left_f = lists[left]
    right_e, right_f = lists[right]
    return (
        sum(x > y for x in left_e for y in right_e)
        + sum(x > y for x in left_f for y in right_f)
    ) % 2


def verify_exterior_quadratic(instance):
    lists = exterior_lists(instance)
    nonzero_pair = None
    for mate in instance["mates"]:
        ordered = sorted(mate, key=lambda block: tuple(sorted(block)))
        bit = sum(
            inversion_parity(lists[block][0])
            + inversion_parity(lists[block][1])
            for block in ordered
        ) % 2
        bit ^= sum(
            cross_parity(lists, left, right)
            for left, right in combinations(ordered, 2)
        ) % 2
        sign = system_perms(
            instance["base"], mate, instance["n"]
        )[1]
        assert bit == (sign == -1)
        if nonzero_pair is None:
            nonzero_pair = next(
                (
                    (left, right)
                    for left, right in combinations(ordered, 2)
                    if cross_parity(lists, left, right)
                ),
                None,
            )
    assert nonzero_pair is not None
    return tuple(
        tuple(sorted(block)) for block in nonzero_pair
    )


def verify_r3():
    instance = build_instance(7, 3)
    assert len(instance["mates"]) == 8
    assert instance["rowspace"].dim == 15

    lex_h = theta_vector(instance, tuple(range(7)))
    assert popcount(lex_h) == 18
    assert instance["rowspace"].contains(lex_h)
    certificate = instance["rowspace"].certificate(lex_h)
    certificate_facets = [
        instance["facets"][index]
        for index in range(len(instance["facets"]))
        if (certificate >> index) & 1
    ]
    assert certificate_facets == [
        (0, 1), (0, 4), (1, 2), (1, 5),
        (2, 5), (3, 4), (3, 5), (4, 5),
    ]
    assert {
        popcount(lex_h & mate_vector(instance, mate)) % 2
        for mate in instance["mates"]
    } == {0}
    assert exact_mate_difference_dimension(instance) == 6

    swapped_order = (1, 0, 2, 3, 4, 5, 6)
    swapped_h = theta_vector(instance, swapped_order)
    assert popcount(swapped_h) == 18
    assert not instance["rowspace"].contains(swapped_h)
    swapped_support = list(combinations((0, 2, 3, 5), 3))
    assert_kernel_witness(instance, swapped_support, swapped_h)
    assert {
        popcount(swapped_h & mate_vector(instance, mate)) % 2
        for mate in instance["mates"]
    } == {0}

    membership_count = sum(
        instance["rowspace"].contains(theta_vector(instance, order))
        for order in permutations(range(7))
    )
    assert membership_count == 336

    pair = verify_exterior_quadratic(instance)
    assert pair == ((0, 1, 3), (0, 2, 5))
    return membership_count


def verify_r5():
    instance = build_instance(11, 5)
    assert len(instance["mates"]) == 144
    assert len(instance["nonbase"]) == 396
    assert instance["rowspace"].dim == 210

    lex_h = theta_vector(instance, tuple(range(11)))
    assert popcount(lex_h) == 198
    assert not instance["rowspace"].contains(lex_h)
    support = list(combinations((0, 1, 2, 4, 5, 8), 5))
    assert_kernel_witness(instance, support, lex_h)
    assert {
        popcount(lex_h & mate_vector(instance, mate)) % 2
        for mate in instance["mates"]
    } == {0}
    assert exact_mate_difference_dimension(instance) == 44

    pair = verify_exterior_quadratic(instance)
    assert pair == ((0, 1, 2, 3, 5), (0, 1, 2, 4, 7))


def main():
    membership_count = verify_r3()
    verify_r5()
    print("r=3 lex h in restricted facet rowspace: PASS")
    print("r=5 lex h nonmembership, weight-6 kernel witness: PASS")
    print("h constant on all 8 Fano and 144 Witt exact mates: PASS")
    print(
        "r=3 reference-order audit: "
        f"{membership_count}/5040 orders in rowspace; swap(0,1) OUT: PASS"
    )
    print("exterior sign is quadratic with nonzero crossing terms: PASS")
    print("BLOCK-LOCAL SIGN ROWSPACE ROUTE: NO-GO")


if __name__ == "__main__":
    main()
