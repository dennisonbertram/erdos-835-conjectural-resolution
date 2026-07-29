#!/usr/bin/env python3
"""Verify a coherent 19-point model for adjacent defect links.

The certificate is one cyclic LS(2,3,19).  Its two prescribed links are
given by two Wallis starters; the forty integers select one translate from
each orbit of triples on Z_17.  Everything checked below is reconstructed
directly from those 74 small integers.

This is a local cross-link model, not an S(14,15,31) large set.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import comb


P = 17
FINITE = tuple(range(P))
LEFT = 17
INFINITY = 18
POINTS = tuple(range(19))
COLOURS = set(FINITE)

# The first two rows of the Wallis G(17) starter table.
STARTERS = (
    (0, 2, 5, 9, 14, 16, 13, 15, 12, 4, 8, 7, 11, 10, 6, 3, 1),
    (0, 3, 1, 10, 12, 11, 15, 4, 13, 5, 14, 9, 6, 8, 7, 16, 2),
)

# Portable phases for pair (0,1) in
# cyclic17_all_105_exact_slices_certificate.json.
PHASES = (
    7, 1, 9, 0, 5, 12, 15, 8, 13, 11,
    4, 16, 10, 14, 15, 14, 2, 10, 6, 9,
    11, 4, 8, 3, 12, 6, 5, 4, 11, 2,
    14, 0, 7, 8, 6, 1, 10, 5, 12, 6,
)


Triple = tuple[int, int, int]


def canonical(values: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    return tuple(sorted(values))


def translate(values: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return canonical(tuple((value + amount) % P for value in values))


def representatives() -> tuple[Triple, ...]:
    unseen = set(combinations(FINITE, 3))
    answer: list[Triple] = []
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in FINITE)
        answer.append(representative)
        for shift in FINITE:
            unseen.discard(translate(representative, shift))
    assert len(answer) == 40
    return tuple(answer)


def square(starter: tuple[int, ...], x: int, y: int) -> int:
    return (starter[(x - y) % P] + y) % P


def put(
    colouring: dict[Triple, int],
    raw_triple: tuple[int, int, int],
    colour: int,
) -> None:
    triple = canonical(raw_triple)
    assert triple not in colouring
    assert colour in COLOURS
    colouring[triple] = colour


def construct_lsts19() -> dict[Triple, int]:
    colouring: dict[Triple, int] = {}

    for x in FINITE:
        put(colouring, (LEFT, INFINITY, x), x)
    for x, y in combinations(FINITE, 2):
        put(colouring, (LEFT, x, y), square(STARTERS[0], x, y))
        put(colouring, (INFINITY, x, y), square(STARTERS[1], x, y))

    reps = representatives()
    assert len(PHASES) == len(reps)
    for orbit, representative in enumerate(reps):
        zero_shift = (-PHASES[orbit]) % P
        for colour in FINITE:
            triple = translate(representative, zero_shift + colour)
            put(colouring, triple, colour)

    assert len(colouring) == comb(19, 3) == 969
    assert set(colouring) == set(combinations(POINTS, 3))
    return colouring


def verify_large_set(colouring: dict[Triple, int]) -> None:
    block_counts = Counter(colouring.values())
    assert block_counts == Counter({colour: 57 for colour in FINITE})

    for pair in combinations(POINTS, 2):
        seen = {
            colouring[canonical(pair + (third,))]
            for third in POINTS
            if third not in pair
        }
        assert seen == COLOURS

    for colour in FINITE:
        pair_counts: Counter[tuple[int, int]] = Counter()
        for triple, value in colouring.items():
            if value == colour:
                pair_counts.update(combinations(triple, 2))
        assert pair_counts == Counter(
            {pair: 1 for pair in combinations(POINTS, 2)}
        )


def verify_link_factorizations_and_transport(
    colouring: dict[Triple, int],
) -> None:
    # Every point link is a one-factorization of K_18.
    for centre in POINTS:
        vertices = tuple(point for point in POINTS if point != centre)
        for vertex in vertices:
            row = {
                colouring[canonical((centre, vertex, other))]
                for other in vertices
                if other != vertex
            }
            assert row == COLOURS

    # Adjacent links agree on the exchanged-point star and are cellwise
    # disjoint everywhere else after the exchanged points are identified.
    for left, right in combinations(POINTS, 2):
        common = tuple(
            point for point in POINTS if point not in (left, right)
        )
        for vertex in common:
            common_star_colour = colouring[
                canonical((left, right, vertex))
            ]
            assert common_star_colour in COLOURS
        for x, y in combinations(common, 2):
            assert (
                colouring[canonical((left, x, y))]
                != colouring[canonical((right, x, y))]
            )


def permutation_sign(values: list[int]) -> int:
    inversions = sum(
        values[i] > values[j]
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )
    return -1 if inversions % 2 else 1


def normalized_link_row_sign(
    colouring: dict[Triple, int],
    centre: int,
) -> int:
    """Product of row signs after normalizing the infinity star."""
    assert centre != INFINITY
    vertices = [
        point for point in POINTS
        if point not in (centre, INFINITY)
    ]
    label = {
        point: colouring[canonical((centre, INFINITY, point))]
        for point in vertices
    }
    assert set(label.values()) == COLOURS
    point_of = {colour: point for point, colour in label.items()}

    answer = 1
    for row_colour in FINITE:
        x = point_of[row_colour]
        row = []
        for column_colour in FINITE:
            if column_colour == row_colour:
                row.append(row_colour)
            else:
                y = point_of[column_colour]
                row.append(colouring[canonical((centre, x, y))])
        assert set(row) == COLOURS
        answer *= permutation_sign(row)
    return answer


def raw_link_row_sign(
    colouring: dict[Triple, int],
    centre: int,
) -> int:
    """Product of the row signs in the unnormalized point link."""
    vertices = [
        point for point in POINTS
        if point != centre
    ]
    answer = 1
    for vertex in vertices:
        row = [
            colouring[canonical((centre, vertex, other))]
            for other in vertices
            if other != vertex
        ]
        assert set(row) == COLOURS
        answer *= permutation_sign(row)
    return answer


def defect_multiplicities(
    colouring: dict[Triple, int],
) -> tuple[Counter[int], tuple[int, tuple[int, int, int]], tuple[int, tuple[int, int, int]]]:
    distribution: Counter[int] = Counter()
    first_zero: tuple[int, tuple[int, int, int]] | None = None
    first_multiple: tuple[int, tuple[int, int, int]] | None = None
    colour_triples = tuple(combinations(FINITE, 3))

    for centre in POINTS:
        if centre == INFINITY:
            continue
        finite_vertices = tuple(
            point for point in POINTS
            if point not in (centre, INFINITY)
        )
        counts: Counter[tuple[int, int, int]] = Counter()
        for triangle in combinations(finite_vertices, 3):
            edge_colours = canonical(tuple(
                colouring[canonical((centre,) + edge)]
                for edge in combinations(triangle, 2)
            ))
            assert len(set(edge_colours)) == 3
            counts[edge_colours] += 1

        assert sum(counts.values()) == comb(17, 3) == 680
        for colours in colour_triples:
            multiplicity = counts[colours]
            distribution[multiplicity] += 1
            if multiplicity == 0 and first_zero is None:
                first_zero = (centre, colours)
            if multiplicity > 1 and first_multiple is None:
                first_multiple = (centre, colours)

    assert sum(distribution.values()) == 18 * comb(17, 3)
    assert sum(
        multiplicity * frequency
        for multiplicity, frequency in distribution.items()
    ) == 18 * comb(17, 3)
    assert distribution == Counter(
        {0: 4760, 1: 4267, 2: 2176, 3: 697, 4: 204, 5: 102, 6: 34}
    )
    assert first_zero is not None
    assert first_multiple is not None
    return distribution, first_zero, first_multiple


def triangles_with_colours(
    colouring: dict[Triple, int],
    centre: int,
    colours: tuple[int, int, int],
) -> list[Triple]:
    vertices = tuple(
        point for point in POINTS
        if point not in (centre, INFINITY)
    )
    answer = []
    for triangle in combinations(vertices, 3):
        edge_colours = canonical(tuple(
            colouring[canonical((centre,) + edge)]
            for edge in combinations(triangle, 2)
        ))
        if edge_colours == colours:
            answer.append(triangle)
    return answer


def main() -> None:
    colouring = construct_lsts19()
    verify_large_set(colouring)
    verify_link_factorizations_and_transport(colouring)
    signs = Counter(
        normalized_link_row_sign(colouring, centre)
        for centre in POINTS
        if centre != INFINITY
    )
    assert signs == Counter({-1: 17, 1: 1})
    normalized_product = 1
    for centre in POINTS:
        if centre != INFINITY:
            normalized_product *= normalized_link_row_sign(
                colouring, centre
            )
    raw_signs = {
        centre: raw_link_row_sign(colouring, centre)
        for centre in POINTS
    }
    raw_product = 1
    for sign in raw_signs.values():
        raw_product *= sign
    assert Counter(raw_signs.values()) == Counter({-1: 18, 1: 1})
    assert raw_product == 1
    assert normalized_product == raw_signs[INFINITY] == -1
    distribution, zero, multiple = defect_multiplicities(colouring)
    six_witness = triangles_with_colours(colouring, 0, (1, 12, 14))
    assert six_witness == [
        (1, 3, 15),
        (2, 5, 14),
        (3, 11, 15),
        (6, 12, 13),
        (7, 9, 16),
        (8, 12, 13),
    ]

    print("LS(2,3,19): PASS (17 STS classes, 969 triples)")
    print("19 coherent K18 links and all 171 pair transports: PASS")
    print(f"normalized link row-sign distribution: {dict(sorted(signs.items()))}")
    print(
        "raw point-link sign distribution/product: "
        f"{dict(sorted(Counter(raw_signs.values()).items()))}, {raw_product}"
    )
    print(
        "orientation boundary identity "
        f"product(normalized) = raw(infinity) = {normalized_product}"
    )
    print(
        "finite rainbow multiplicity distribution over 18 links: "
        f"{dict(sorted(distribution.items()))}"
    )
    print(f"first zero witness (centre, colours): {zero}")
    print(f"first multiple witness (centre, colours): {multiple}")
    print(
        "multiplicity-six witness (centre, colours, triangles): "
        f"{(0, (1, 12, 14), six_witness)}"
    )
    print("defect cross-link LS(2,3,19) audit: PASS")


if __name__ == "__main__":
    main()
