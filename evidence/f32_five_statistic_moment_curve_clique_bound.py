#!/usr/bin/env python3
"""Exact clique bound after retaining e_4 in the F_32 moment-curve family.

For r in F_32, build the actual-edge quotient graph on the states

    (a, a^2, a^3, a^4 + r, lambda),  a,lambda in F_32,

where lambda=e_8+e_1^8.  Scaling identifies every nonzero r, so r=0 and
r=1 exhaust the family.  Half-set realizations and all one-point exchanges
are enumerated exactly by a meet-in-the-middle calculation.  A deterministic
branch-and-bound calculation then finds the exact maximum clique.
"""

from collections import defaultdict
from itertools import combinations


MODULUS = 0b100101  # X^5 + X^2 + 1
DEGREE = 8


def multiply(left: int, right: int) -> int:
    raw = 0
    for bit in range(5):
        if right >> bit & 1:
            raw ^= left << bit
    for degree in range(8, 4, -1):
        if raw >> degree & 1:
            raw ^= MODULUS << (degree - 5)
    assert 0 <= raw < 32
    return raw


PRODUCT = tuple(
    tuple(multiply(left, right) for right in range(32))
    for left in range(32)
)


def power(value: int, exponent: int) -> int:
    answer = 1
    while exponent:
        if exponent & 1:
            answer = PRODUCT[answer][value]
        value = PRODUCT[value][value]
        exponent >>= 1
    return answer


POWERS = tuple(
    tuple(power(value, exponent) for exponent in range(9))
    for value in range(32)
)


def trace(value: int) -> int:
    answer = 0
    current = value
    for _ in range(5):
        answer ^= current
        current = PRODUCT[current][current]
    assert answer in (0, 1)
    return answer


def subset_entries(
    points: range,
) -> list[tuple[int, tuple[int, ...], int]]:
    """Enumerate (size, coefficients through e_8, characteristic mask)."""

    answer = []
    coefficients = [1] + [0] * DEGREE

    def visit(index: int, mask: int, size: int) -> None:
        if index == len(points):
            answer.append((size, tuple(coefficients), mask))
            return

        visit(index + 1, mask, size)
        point = points[index]
        old = coefficients[:]
        for degree in range(DEGREE, 0, -1):
            coefficients[degree] ^= PRODUCT[point][
                coefficients[degree - 1]
            ]
        visit(index + 1, mask | (1 << point), size + 1)
        coefficients[:] = old

    visit(0, 0, 0)
    assert len(answer) == 1 << len(points)
    return answer


LEFT_ENTRIES = subset_entries(range(16))
RIGHT_ENTRIES = subset_entries(range(16, 32))
RIGHT_INDEX = defaultdict(list)
for size, coefficients, mask in RIGHT_ENTRIES:
    RIGHT_INDEX[(size,) + coefficients[1:5]].append((coefficients, mask))


def combined_coefficients(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    answer = []
    for degree in range(DEGREE + 1):
        value = 0
        for left_degree in range(degree + 1):
            value ^= PRODUCT[left[left_degree]][
                right[degree - left_degree]
            ]
        answer.append(value)
    return tuple(answer)


def needed_right_prefix(
    target: tuple[int, ...], left: tuple[int, ...]
) -> tuple[int, ...]:
    """Solve left(t)*right(t)=target(t) through degree four."""

    right = [1]
    for degree in range(1, 5):
        value = target[degree]
        for left_degree in range(1, degree + 1):
            value ^= PRODUCT[left[left_degree]][
                right[degree - left_degree]
            ]
        right.append(value)
    return tuple(right)


def encode(parameter: int, lam: int) -> int:
    return 32 * parameter + lam


def build_graph(
    offset: int,
) -> tuple[list[int], list[int], tuple[int, ...]]:
    """Return adjacency bitsets, realization counts, and per-a totals."""

    adjacency = [0] * 1024
    realization_counts = [0] * 1024
    totals = []

    for parameter in range(32):
        target = (
            1,
            parameter,
            POWERS[parameter][2],
            POWERS[parameter][3],
            POWERS[parameter][4] ^ offset,
        )
        total = 0
        for left_size, left_coefficients, left_mask in LEFT_ENTRIES:
            right_prefix = needed_right_prefix(target, left_coefficients)
            key = (16 - left_size,) + right_prefix[1:]
            for right_coefficients, right_mask in RIGHT_INDEX.get(key, ()):
                coefficients = combined_coefficients(
                    left_coefficients, right_coefficients
                )
                lam = coefficients[8] ^ POWERS[parameter][8]
                source = encode(parameter, lam)
                realization_counts[source] += 1
                total += 1
                subset_mask = left_mask | right_mask

                for removed in range(32):
                    if not (subset_mask >> removed & 1):
                        continue
                    quotient = [1]
                    for degree in range(1, DEGREE + 1):
                        quotient.append(
                            coefficients[degree]
                            ^ PRODUCT[removed][quotient[-1]]
                        )

                    for added in range(32):
                        if subset_mask >> added & 1:
                            continue
                        neighbor = [1]
                        for degree in range(1, DEGREE + 1):
                            neighbor.append(
                                quotient[degree]
                                ^ PRODUCT[added][quotient[degree - 1]]
                            )

                        other_parameter = neighbor[1]
                        if neighbor[2] != POWERS[other_parameter][2]:
                            continue
                        if neighbor[3] != POWERS[other_parameter][3]:
                            continue
                        if (
                            neighbor[4]
                            != POWERS[other_parameter][4] ^ offset
                        ):
                            continue

                        other_lam = (
                            neighbor[8] ^ POWERS[other_parameter][8]
                        )
                        target_vertex = encode(other_parameter, other_lam)
                        assert target_vertex != source
                        adjacency[source] |= 1 << target_vertex
                        adjacency[target_vertex] |= 1 << source
        totals.append(total)

    return adjacency, realization_counts, tuple(totals)


def is_clique(vertices: list[int], adjacency: list[int]) -> bool:
    for index, vertex in enumerate(vertices):
        for other in vertices[index + 1 :]:
            if not (adjacency[vertex] >> other & 1):
                return False
    return True


def greedy_coloring_order(
    candidates: int, adjacency: list[int]
) -> tuple[list[int], list[int]]:
    """Greedily partition candidates into independent colour classes."""

    order = []
    bounds = []
    colour = 0
    uncoloured = candidates
    while uncoloured:
        colour += 1
        available = uncoloured
        while available:
            bit = available & -available
            vertex = bit.bit_length() - 1
            order.append(vertex)
            bounds.append(colour)
            uncoloured ^= bit
            available ^= bit
            available &= ~adjacency[vertex]
    return order, bounds


def maximum_clique(
    adjacency: list[int], vertices: list[int], seed: list[int]
) -> tuple[list[int], int]:
    """Tomita-style exact branch and bound with greedy-colouring bounds."""

    assert is_clique(seed, adjacency)
    best = seed[:]
    nodes = 0

    def expand(size: int, candidates: int, chosen: list[int]) -> None:
        nonlocal best, nodes
        nodes += 1
        order, bounds = greedy_coloring_order(candidates, adjacency)
        for index in range(len(order) - 1, -1, -1):
            if size + bounds[index] <= len(best):
                return
            vertex = order[index]
            bit = 1 << vertex
            if not (candidates & bit):
                continue
            next_candidates = candidates & adjacency[vertex]
            if next_candidates:
                expand(size + 1, next_candidates, chosen + [vertex])
            elif size + 1 > len(best):
                best = chosen + [vertex]
            candidates ^= bit

    vertex_bits = sum(1 << vertex for vertex in vertices)
    expand(0, vertex_bits, [])
    assert is_clique(best, adjacency)
    return best, nodes


def brute_force_maximum(adjacency: list[int]) -> int:
    """Small independent reference used to test maximum_clique."""

    number = len(adjacency)
    best = 0
    for subset in range(1 << number):
        size = subset.bit_count()
        if size <= best:
            continue
        remaining = subset
        valid = True
        while remaining:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            others = subset ^ bit
            if adjacency[vertex] & others != others:
                valid = False
                break
            remaining ^= bit
        if valid:
            best = size
    return best


def self_test_maximum_clique() -> None:
    """Compare the exact solver to brute force on all graphs of order five."""

    edges = tuple(combinations(range(5), 2))
    for graph_code in range(1 << len(edges)):
        adjacency = [0] * 5
        for edge_index, (left, right) in enumerate(edges):
            if graph_code >> edge_index & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
        found, _ = maximum_clique(adjacency, list(range(5)), [])
        assert len(found) == brute_force_maximum(adjacency)


def main() -> None:
    for value in range(1, 32):
        assert PRODUCT[value][power(value, 30)] == 1
    self_test_maximum_clique()

    trace_parameters = [
        value
        for value in range(32)
        if value == 0 or trace(value) == 1
    ]
    zero_seed = [encode(value, 1) for value in trace_parameters]
    one_seed_pairs = (
        (0, 0),
        (1, 1),
        (2, 10),
        (11, 16),
        (22, 26),
        (13, 1),
        (14, 10),
        (24, 16),
        (26, 26),
        (5, 26),
        (7, 16),
        (9, 26),
        (17, 10),
        (18, 1),
        (20, 16),
        (29, 10),
        (30, 1),
    )
    one_seed = [encode(parameter, lam) for parameter, lam in one_seed_pairs]

    expected = {
        0: (1023, 45291),
        1: (1024, 71648),
    }
    for offset, seed in ((0, zero_seed), (1, one_seed)):
        adjacency, counts, totals = build_graph(offset)
        vertices = [
            vertex for vertex, count in enumerate(counts) if count > 0
        ]
        edge_count = sum(bits.bit_count() for bits in adjacency) // 2
        assert (len(vertices), edge_count) == expected[offset]
        maximum, nodes = maximum_clique(adjacency, vertices, seed)
        assert len(maximum) == 17
        print(
            f"r={offset}: realizable_vertices={len(vertices)}, "
            f"edges={edge_count}, maximum_clique=17, "
            f"branch_nodes={nodes}"
        )
        print(
            "  witness:",
            tuple((vertex // 32, vertex % 32) for vertex in maximum),
        )
        print("  half-set realization totals by a:", totals)

    print("F_32 five-statistic moment-curve clique bound: PASS")
    print("r=0 and r=1 exhaust all offsets up to nonzero scaling")
    print("consequence: this entire natural family has no K18")


if __name__ == "__main__":
    main()
