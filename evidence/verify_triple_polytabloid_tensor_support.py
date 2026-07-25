#!/usr/bin/env python3
"""Exact controls for triple_polytabloid_tensor_support_audit.md.

Only Python integer arithmetic is used.  The direct tensor calculation
uses signed-support bitsets; the graph formula is evaluated separately
from the three-coloured union multigraph.
"""

from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
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
    positive_count = bin(common & ~negative_product).count("1")
    negative_count = bin(negative_common).count("1")
    return positive_count - negative_count


def graph_tensor(matching_m, matching_n, matching_l, point_count):
    """Evaluate the component formula, retaining parallel oriented edges."""
    oriented_edges = tuple(matching_m) + tuple(matching_n) + tuple(matching_l)
    adjacency = [[] for _ in range(point_count)]
    for edge_index, (left, right) in enumerate(oriented_edges):
        adjacency[left].append((right, edge_index))
        adjacency[right].append((left, edge_index))

    colour = [None] * point_count
    components = []
    for root in range(point_count):
        if colour[root] is not None:
            continue
        colour[root] = 0
        queue = deque([root])
        vertices = []
        bipartite = True
        while queue:
            vertex = queue.popleft()
            vertices.append(vertex)
            for neighbour, _ in adjacency[vertex]:
                required = 1 - colour[vertex]
                if colour[neighbour] is None:
                    colour[neighbour] = required
                    queue.append(neighbour)
                elif colour[neighbour] != required:
                    bipartite = False
        if not bipartite:
            return 0
        components.append(tuple(vertices))

    sign = 1
    for vertices in components:
        assert len(vertices) % 2 == 0
        half_size = len(vertices) // 2
        if half_size % 2:
            return 0
        vertex_set = set(vertices)
        for left, right in oriented_edges:
            if left not in vertex_set:
                continue
            assert right in vertex_set
            assert colour[left] != colour[right]
            sign *= 1 if colour[left] == 0 else -1
    return sign * (1 << len(components))


def reverse_first_edge(matching):
    first = matching[0]
    return ((first[1], first[0]),) + matching[1:]


def exhaust_tensor_formula(k):
    points = tuple(range(2 * k))
    blocks = tuple(combinations(points, k))
    matchings = tuple(perfect_matchings(points))
    supports = tuple(signed_support(matching, blocks) for matching in matchings)
    distribution = Counter()

    # The tensor and the component formula are symmetric in M,N,L.
    # Exhaust one representative of every permutation orbit and weight
    # its contribution to retain the complete ordered distribution.
    for m, n, ell in combinations_with_replacement(range(len(matchings)), 3):
        direct = direct_tensor(supports[m], supports[n], supports[ell])
        formula = graph_tensor(matchings[m], matchings[n], matchings[ell], 2 * k)
        assert direct == formula
        distinct = len({m, n, ell})
        multiplicity = 1 if distinct == 1 else 3 if distinct == 2 else 6
        distribution[direct] += multiplicity

    # Reversing one orientation multiplies the tensor by -1.
    reversed_matching = reverse_first_edge(matchings[0])
    reversed_support = signed_support(reversed_matching, blocks)
    for n in range(len(matchings)):
        for ell in range(len(matchings)):
            original = direct_tensor(supports[0], supports[n], supports[ell])
            changed_direct = direct_tensor(reversed_support, supports[n], supports[ell])
            changed_formula = graph_tensor(
                reversed_matching, matchings[n], matchings[ell], 2 * k
            )
            assert changed_direct == changed_formula == -original

    assert sum(distribution.values()) == len(matchings) ** 3
    assert all(value == 0 or value % 2 == 0 for value in distribution)
    print(
        f"k={k}: {len(matchings) ** 3:,} triples exhausted; "
        f"T distribution {dict(sorted(distribution.items()))}"
    )
    return blocks, matchings, supports


def enumerate_sqs8():
    points = tuple(range(8))
    blocks = tuple(combinations(points, 4))
    triples = tuple(combinations(points, 3))
    block_triples = [
        tuple(index for index, triple in enumerate(triples) if set(triple) <= set(block))
        for block in blocks
    ]
    triple_blocks = [
        tuple(index for index, block in enumerate(blocks) if set(triple) <= set(block))
        for triple in triples
    ]
    systems = []
    full = (1 << len(triples)) - 1

    def search(covered, selected):
        if covered == full:
            assert len(selected) == 14
            systems.append(sum(1 << index for index in selected))
            return
        candidates = []
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
            candidates.append((len(viable), viable))
        _, viable = min(candidates)
        for block_index in viable:
            next_covered = covered
            for triple_index in block_triples[block_index]:
                next_covered |= 1 << triple_index
            search(next_covered, selected + (block_index,))

    search(0, ())
    systems = tuple(sorted(set(systems)))
    assert len(systems) == 30
    return blocks, systems


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def k4_system_data(blocks, supports):
    sqs_blocks, systems = enumerate_sqs8()
    assert blocks == sqs_blocks
    indicators = tuple(
        tuple((system >> index) & 1 for index in range(len(blocks)))
        for system in systems
    )
    deltas = tuple(
        tuple(dot(indicator, support[2]) for support in supports)
        for indicator in indicators
    )
    assert all(value % 2 == 0 for delta in deltas for value in delta)
    return systems, indicators, deltas


def check_k4_contractions(blocks, matchings, supports):
    systems, _, deltas = k4_system_data(blocks, supports)
    system_a = systems[0]
    mate_index = next(
        index for index, system in enumerate(systems[1:], 1) if not system & system_a
    )

    k, p = 4, 5
    scale = factorial(k) ** 2
    for m in range(len(matchings)):
        self_sum = 0
        cross_sum = 0
        for n in range(len(matchings)):
            for ell in range(len(matchings)):
                tensor = direct_tensor(supports[m], supports[n], supports[ell])
                self_sum += deltas[0][n] * deltas[0][ell] * tensor
                cross_sum += deltas[0][n] * deltas[mate_index][ell] * tensor
        assert self_sum == p * scale * (p - 2) * deltas[0][m]
        assert cross_sum == -p * scale * (
            deltas[0][m] + deltas[mate_index][m]
        )
        assert self_sum % p == cross_sum % p == 0

    print(
        "k=4: all contractions verified for one S(3,4,8) and a disjoint mate"
    )


def gf2_rank(vectors):
    basis = {}
    for vector in vectors:
        work = vector
        while work:
            pivot = work.bit_length() - 1
            if pivot in basis:
                work ^= basis[pivot]
            else:
                basis[pivot] = work
                break
    return len(basis)


def gf2_in_span(vector, generators):
    basis = {}
    for generator in generators:
        work = generator
        while work:
            pivot = work.bit_length() - 1
            if pivot in basis:
                work ^= basis[pivot]
            else:
                basis[pivot] = work
                break
    work = vector
    while work:
        pivot = work.bit_length() - 1
        if pivot not in basis:
            return False
        work ^= basis[pivot]
    return True


def apply_binary_rows(rows, vector):
    image = 0
    for index, row in enumerate(rows):
        if bin(row & vector).count("1") % 2:
            image |= 1 << index
    return image


def connected_two_matching_union(matching_m, matching_n, point_count):
    adjacency = [[] for _ in range(point_count)]
    for left, right in tuple(matching_m) + tuple(matching_n):
        adjacency[left].append(right)
        adjacency[right].append(left)
    reached = {0}
    queue = [0]
    while queue:
        vertex = queue.pop()
        for neighbour in adjacency[vertex]:
            if neighbour not in reached:
                reached.add(neighbour)
                queue.append(neighbour)
    return len(reached) == point_count


def check_k4_hamilton_parity(blocks, matchings, supports):
    systems, _, deltas = k4_system_data(blocks, supports)
    point_set = set(range(8))

    representatives = []
    pair_index_by_block = {}
    for block_index, block in enumerate(blocks):
        complement = tuple(sorted(point_set - set(block)))
        complement_index = blocks.index(complement)
        if complement_index < block_index:
            continue
        pair_index = len(representatives)
        representatives.append(block)
        pair_index_by_block[block_index] = pair_index
        pair_index_by_block[complement_index] = pair_index
    assert len(representatives) == 35

    a_rows = []
    a_columns = [0] * len(representatives)
    for matching_index, matching in enumerate(matchings):
        row = 0
        for pair_index, block in enumerate(representatives):
            if e_value(matching, block):
                row |= 1 << pair_index
                a_columns[pair_index] |= 1 << matching_index
        a_rows.append(row)

    h_rows = []
    for matching_m in matchings:
        row = 0
        for index_n, matching_n in enumerate(matchings):
            if matching_m != matching_n and connected_two_matching_union(
                matching_m, matching_n, 8
            ):
                row |= 1 << index_n
        h_rows.append(row)

    # A A^T = H and A^T A = 0 over F_2.
    for index_m, row_m in enumerate(a_rows):
        reconstructed = 0
        for index_n, row_n in enumerate(a_rows):
            if bin(row_m & row_n).count("1") % 2:
                reconstructed |= 1 << index_n
        assert reconstructed == h_rows[index_m]
    assert all(
        bin(left & right).count("1") % 2 == 0
        for left in a_columns
        for right in a_columns
    )
    assert gf2_rank(a_rows) == 14
    assert gf2_rank(h_rows) == 8
    assert all(apply_binary_rows(h_rows, row) == 0 for row in a_columns)

    derivative_parities = []
    for system, delta in zip(systems, deltas):
        direct = sum(
            1 << index for index, value in enumerate(delta) if (value // 2) % 2
        )
        pair_indicator = 0
        for block_index in range(len(blocks)):
            if (system >> block_index) & 1:
                pair_indicator |= 1 << pair_index_by_block[block_index]
        from_incidence = apply_binary_rows(a_rows, pair_indicator)
        assert direct == from_incidence
        assert apply_binary_rows(h_rows, direct) == 0
        assert gf2_in_span(direct, h_rows)
        derivative_parities.append(direct)

    tensor_parity_matrices = []
    for m in range(len(matchings)):
        matrix_rows = []
        for n in range(len(matchings)):
            row = 0
            for ell in range(len(matchings)):
                tensor = direct_tensor(supports[m], supports[n], supports[ell])
                if abs(tensor) == 2:
                    row |= 1 << ell
            matrix_rows.append(row)
        assert all(
            ((matrix_rows[n] >> ell) & 1) == ((matrix_rows[ell] >> n) & 1)
            for n in range(len(matchings))
            for ell in range(len(matchings))
        )
        assert all(
            ((matrix_rows[n] >> n) & 1) == ((h_rows[m] >> n) & 1)
            for n in range(len(matchings))
        )
        tensor_parity_matrices.append(tuple(matrix_rows))

    for matrix_rows in tensor_parity_matrices:
        transformed = [
            apply_binary_rows(matrix_rows, right) for right in derivative_parities
        ]
        for left in derivative_parities:
            for image in transformed:
                assert bin(left & image).count("1") % 2 == 0

    print(
        "k=4 parity: AA^T=H, A^TA=0, ranks 14/8, "
        "and all 94,500 SQS-pair tensor bilinear equations pass"
    )


def check_target_arithmetic():
    k, p = 16, 17
    k_factorial = factorial(k)
    valuation_two = 0
    work = k_factorial
    while work % 2 == 0:
        valuation_two += 1
        work //= 2
    assert valuation_two == 15
    assert k_factorial % p == p - 1
    # k!^2 contributes 2^30 and every target Delta is even.
    assert 2 * k_factorial * k_factorial % (1 << 31) == 0
    print("k=16: v2(16!)=15, 16!=-1 mod 17, aggregate modulus audit closes")


def alternating_reciprocal_sum(k):
    return sum(Fraction((-1) ** r, comb(k, r)) for r in range(k + 1))


def check_hilbert_schmidt_residual():
    for k in (2, 4, 6, 16):
        p = k + 1
        reciprocal_sum = alternating_reciprocal_sum(k)
        assert reciprocal_sum == Fraction(2 * p, p + 1)
        scalar = reciprocal_sum / (p * p)
        assert scalar == Fraction(2, p * (p + 1))

    controls = {}
    for k in (2, 4, 16):
        p = k + 1
        vertex_count = comb(2 * k, k)
        residual = (p - 1) * (
            Fraction(2 * vertex_count, p * (p + 1)) - (p - 2)
        )
        controls[k] = residual
    assert controls[2] == 0
    assert controls[4] == Fraction(20, 3)
    assert controls[16] == 62_857_840
    # Off-diagonal residuals are -R/(p-1), so the resulting p by p
    # Gram matrix has one zero eigenvalue and p-1 positive eigenvalues.
    assert controls[16] / 16 == 3_928_615
    print(
        "Hilbert-Schmidt SOS: residuals k=2,4,16 are "
        f"{controls[2]}, {controls[4]}, {controls[16]} (all nonnegative)"
    )


if __name__ == "__main__":
    for parameter in (1, 2, 3):
        exhaust_tensor_formula(parameter)
    data = exhaust_tensor_formula(4)
    check_k4_contractions(*data)
    check_k4_hamilton_parity(*data)
    check_target_arithmetic()
    check_hilbert_schmidt_residual()
    print("PASS: triple-polytabloid support and modulus audit verified.")
