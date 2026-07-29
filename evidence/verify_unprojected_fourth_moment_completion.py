#!/usr/bin/env python3
"""Exact checks for unprojected_fourth_moment_completion.md.

The script is deliberately self-contained and uses integer arithmetic only.
The general statements in the note are proofs; finite checks here cover the
model tensor and the k=2/k=4 controls.
"""

from itertools import combinations, product
from math import comb, prod


def gram_entry(left, right, p, n):
    return n * (p * int(left == right) - 1)


def beta_coefficients(left, right, p):
    """Coefficients of b_ab in the spanning family (q_0,...,q_{p-1})."""
    result = [0] * p
    result[left] -= 1
    result[right] -= 1
    if left == right:
        result[left] += p
    return tuple(result)


def coefficient_inner(left, right, p, n):
    return sum(
        left[a] * right[b] * gram_entry(a, b, p, n)
        for a in range(p)
        for b in range(p)
    )


def model_fourth(labels, p, n):
    assert n % p == 0
    d = n // p
    return d * sum(
        prod(
            p * int(colour == point) - 1
            for colour in labels
        )
        for point in range(p)
    )


def multiplication_partition(labels):
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return tuple(sorted(counts.values(), reverse=True))


def table_fourth(labels, p, n):
    pattern = multiplication_partition(labels)
    a = p * p - 3 * p + 3
    values = {
        (4,): n * (p - 1) * a,
        (3, 1): -n * a,
        (2, 2): n * (2 * p - 3),
        (2, 1, 1): n * (p - 3),
        (1, 1, 1, 1): -3 * n,
    }
    return values[pattern]


def check_model_tensor(p, n):
    # Exhaust every four-colour pattern.  Separately compute the p-point
    # model, the table, and the beta-plus-constant decomposition.
    for labels in product(range(p), repeat=4):
        a, b, c, d = labels
        direct = model_fourth(labels, p, n)
        table = table_fourth(labels, p, n)
        beta_part = coefficient_inner(
            beta_coefficients(a, b, p),
            beta_coefficients(c, d, p),
            p,
            n,
        )
        c_ab = p * int(a == b) - 1
        c_cd = p * int(c == d) - 1
        decomposed = beta_part + n * c_ab * c_cd
        assert direct == table == decomposed

    # Check the projected multiplication table directly in the model.
    chis = [
        tuple(p * int(a == point) - 1 for point in range(p))
        for a in range(p)
    ]
    for a in range(p):
        for b in range(p):
            pointwise = tuple(
                chis[a][point] * chis[b][point] for point in range(p)
            )
            mean = sum(pointwise) // p
            projected = tuple(value - mean for value in pointwise)
            coefficients = beta_coefficients(a, b, p)
            reduced = tuple(
                sum(coefficients[colour] * chis[colour][point]
                    for colour in range(p))
                for point in range(p)
            )
            assert projected == reduced


def check_design(points, blocks, system, strength):
    selected = [blocks[index] for index in range(len(blocks))
                if (system >> index) & 1]
    for subset in combinations(points, strength):
        assert sum(set(subset) <= set(block) for block in selected) == 1


def check_k2_true_control():
    p, k = 3, 2
    points = tuple(range(4))
    blocks = tuple(combinations(points, k))
    classes = (
        {(0, 1), (2, 3)},
        {(0, 2), (1, 3)},
        {(0, 3), (1, 2)},
    )
    q = tuple(
        tuple(p * int(block in colour_class) - 1 for block in blocks)
        for colour_class in classes
    )

    assert all(sum(q[a][index] for a in range(p)) == 0
               for index in range(len(blocks)))
    for a in range(p):
        # W q_a = 0, with W the point-edge incidence matrix.
        for point in points:
            assert sum(q[a][index] for index, block in enumerate(blocks)
                       if point in block) == 0
        for b in range(p):
            inner = sum(q[a][i] * q[b][i] for i in range(len(blocks)))
            assert inner == gram_entry(a, b, p, len(blocks))

            c_ab = p * int(a == b) - 1
            beta = tuple(
                (p * int(a == b) - 1) * q[a][i] - q[b][i]
                for i in range(len(blocks))
            )
            # This is the exact unprojected identity q_a q_b=b_ab+c_ab 1.
            assert all(
                q[a][i] * q[b][i] == beta[i] + c_ab
                for i in range(len(blocks))
            )

    for labels in product(range(p), repeat=4):
        direct = sum(
            q[labels[0]][i] * q[labels[1]][i]
            * q[labels[2]][i] * q[labels[3]][i]
            for i in range(len(blocks))
        )
        assert direct == table_fourth(labels, p, len(blocks))

    fourths = [sum(value ** 4 for value in vector) for vector in q]
    assert fourths == [36, 36, 36]
    assert sum(fourths) == 108


def enumerate_sqs8():
    """Generate every S(3,4,8) as an exact cover, without classification."""
    points = tuple(range(8))
    blocks = tuple(combinations(points, 4))
    triples = tuple(combinations(points, 3))
    block_triples = tuple(
        tuple(index for index, triple in enumerate(triples)
              if set(triple) <= set(block))
        for block in blocks
    )
    triple_blocks = tuple(
        tuple(index for index, block in enumerate(blocks)
              if set(triple) <= set(block))
        for triple in triples
    )
    full = (1 << len(triples)) - 1
    systems = set()

    def search(covered, selected):
        if covered == full:
            assert len(selected) == 14
            systems.add(sum(1 << index for index in selected))
            return

        best = None
        for triple_index in range(len(triples)):
            if (covered >> triple_index) & 1:
                continue
            viable = tuple(
                block_index
                for block_index in triple_blocks[triple_index]
                if all(not ((covered >> inner) & 1)
                       for inner in block_triples[block_index])
            )
            candidate = (len(viable), triple_index, viable)
            if best is None or candidate[:2] < best[:2]:
                best = candidate
        assert best is not None and best[0] > 0
        for block_index in best[2]:
            addition = sum(1 << inner for inner in block_triples[block_index])
            search(covered | addition, selected + (block_index,))

    search(0, ())
    result = tuple(sorted(systems))
    assert len(result) == 30
    for system in result:
        assert system.bit_count() == 14
        check_design(points, blocks, system, 3)
    return points, blocks, result


def check_k4_false_control():
    points, blocks, systems = enumerate_sqs8()
    adjacency = tuple(
        frozenset(
            right for right in range(len(systems))
            if left != right and not (systems[left] & systems[right])
        )
        for left in range(len(systems))
    )
    assert all(len(neighbours) == 8 for neighbours in adjacency)
    assert sum(map(len, adjacency)) // 2 == 120

    triangle_count = 0
    for left, middle, right in combinations(range(len(systems)), 3):
        if (middle in adjacency[left]
                and right in adjacency[left]
                and right in adjacency[middle]):
            triangle_count += 1
    assert triangle_count == 0
    assert any(adjacency)
    maximum_clique = 2

    # Every individual design reaches the one-colour equality.  The
    # impossibility lies in finding five mutually disjoint such designs.
    p = 5
    individual_fourths = []
    for system in systems:
        q = tuple(
            p * ((system >> index) & 1) - 1
            for index in range(len(blocks))
        )
        assert sum(q) == 0
        assert sum(value * value for value in q) == 280
        assert sum(value ** 3 for value in q) == 840
        individual_fourths.append(sum(value ** 4 for value in q))
    assert set(individual_fourths) == {3640}
    assert p * individual_fourths[0] == 18_200
    assert maximum_clique < p
    return len(systems), sum(map(len, adjacency)) // 2, maximum_clique


def check_target_arithmetic():
    k, p = 16, 17
    n = comb(2 * k, k)
    a = p * p - 3 * p + 3
    assert n == 601_080_390
    assert a == 241
    assert n * (p - 1) * a == 2_317_765_983_840
    assert p * n * (p - 1) * a == 39_402_021_725_280
    assert n * (p - 1) ** 2 == 153_876_579_840


def main():
    check_model_tensor(3, 6)
    check_model_tensor(5, 70)
    check_model_tensor(17, comb(32, 16))
    check_k2_true_control()
    systems, disjoint_edges, maximum_clique = check_k4_false_control()
    check_target_arithmetic()
    print("projected p-point model and fourth-moment decomposition: PASS")
    print("k=2 true control: aggregate fourth moment 108")
    print(
        "k=4 false control: "
        f"{systems} systems, {disjoint_edges} disjoint pairs, "
        f"maximum clique {maximum_clique}"
    )
    print("k=16 fourth-moment boundary arithmetic: PASS")
    print("PASS: unprojected fourth-moment completion verified")


if __name__ == "__main__":
    main()
