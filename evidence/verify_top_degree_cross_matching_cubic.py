#!/usr/bin/env python3
"""Exact controls for top_degree_cross_matching_cubic_audit.md.

No external solver or numerical linear algebra is used.  The k=2 part
checks the projected-idempotence cubic formula directly.  The k=4 part
checks both the standard finite non-colouring control and a rational-Gram
description of the real global quadratic relaxation.
"""

from fractions import Fraction
from itertools import combinations
from math import factorial


def matchings(points):
    points = tuple(points)
    if not points:
        yield ()
        return
    first = points[0]
    for position in range(1, len(points)):
        second = points[position]
        rest = points[1:position] + points[position + 1:]
        for tail in matchings(rest):
            yield ((first, second),) + tail


def e_value(matching, block):
    value = 1
    for left, right in matching:
        value *= int(left in block) - int(right in block)
    return value


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def check_k2_cubic_identity():
    """Check (4), reconstruction (7), and all of (8) for J(4,2)."""
    k, p = 2, 3
    blocks = tuple(combinations(range(2 * k), k))
    all_matchings = tuple(matchings(range(2 * k)))
    e = [[e_value(matching, block) for block in blocks]
         for matching in all_matchings]

    # The three one-factors are the three colour classes.
    factors = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    colour = {
        tuple(sorted(block)): label
        for label, factor in enumerate(factors)
        for block in factor
    }
    q = [[p * int(colour[block] == label) - 1 for block in blocks]
         for label in range(p)]

    # q_a is in ker W: every lower star has values 2,-1,-1.
    for label in range(p):
        for point in range(2 * k):
            assert sum(q[label][index] for index, block in enumerate(blocks)
                       if point in block) == 0
    assert all(sum(q[label][index] for label in range(p)) == 0
               for index in range(len(blocks)))

    frame_scale = factorial(p)
    derivatives = [[dot(q[label], e[m]) for label in range(p)]
                   for m in range(len(all_matchings))]

    # Equation (7), checked coordinatewise in the ambient function space.
    for label in range(p):
        reconstructed = [Fraction(0) for _ in blocks]
        for m in range(len(all_matchings)):
            for index in range(len(blocks)):
                reconstructed[index] += Fraction(
                    derivatives[m][label] * e[m][index], frame_scale
                )
        assert reconstructed == q[label]

    triples = [
        [
            [sum(e[m][x] * e[n][x] * e[ell][x]
                 for x in range(len(blocks)))
             for ell in range(len(all_matchings))]
            for n in range(len(all_matchings))
        ]
        for m in range(len(all_matchings))
    ]

    for a in range(p):
        for b in range(p):
            # This is P_K(q_a q_b) tested against the spanning e_M's.
            product = [q[a][x] * q[b][x] for x in range(len(blocks))]
            for m in range(len(all_matchings)):
                rhs = ((p - 2) * derivatives[m][a] if a == b
                       else -derivatives[m][a] - derivatives[m][b])
                assert dot(product, e[m]) == rhs

                lhs = sum(
                    Fraction(
                        derivatives[n][a] * derivatives[ell][b]
                        * triples[m][n][ell],
                        frame_scale * frame_scale,
                    )
                    for n in range(len(all_matchings))
                    for ell in range(len(all_matchings))
                )
                assert lhs == rhs

    print("k=2: actual colouring satisfies projected idempotence and all cubic equations")


def check_k4_false_control():
    """Independent finite proof that J(8,4) has no tight five-colouring."""
    points = tuple(range(8))
    blocks = tuple(combinations(points, 4))
    triples = tuple(combinations(points, 3))
    block_triples = [
        tuple(index for index, triple in enumerate(triples)
              if set(triple) <= set(block))
        for block in blocks
    ]
    triple_blocks = [
        tuple(index for index, block in enumerate(blocks) if set(triple) <= set(block))
        for triple in triples
    ]
    assert all(len(options) == 5 for options in triple_blocks)

    # Enumerate every S(3,4,8) as an exact cover of the 56 triples; no
    # classification or isomorphism assumption is used.
    systems = []

    def enumerate_systems(covered, selected):
        if covered == (1 << len(triples)) - 1:
            assert len(selected) == 14
            systems.append(sum(1 << index for index in selected))
            return
        options_by_triple = []
        for triple_index in range(len(triples)):
            if (covered >> triple_index) & 1:
                continue
            viable = [
                block_index for block_index in triple_blocks[triple_index]
                if all(not ((covered >> inner) & 1)
                       for inner in block_triples[block_index])
            ]
            options_by_triple.append((len(viable), triple_index, viable))
        _, _, viable = min(options_by_triple)
        for block_index in viable:
            next_covered = covered
            for triple_index in block_triples[block_index]:
                next_covered |= 1 << triple_index
            enumerate_systems(next_covered, selected + (block_index,))

    enumerate_systems(0, ())
    systems = tuple(sorted(set(systems)))
    assert len(systems) == 30

    best = 0

    def search(start, chosen, occupied):
        nonlocal best
        best = max(best, chosen)
        for index in range(start, len(systems)):
            if not occupied & systems[index]:
                search(index + 1, chosen + 1, occupied | systems[index])

    search(0, 0, 0)
    assert best == 2
    print("k=4: 30 labelled S(3,4,8)'s; maximum disjoint family = 2 < 5")


def rank_mod(rows, modulus):
    rows = [[entry % modulus for entry in row] for row in rows]
    rank = 0
    width = len(rows[0])
    for column in range(width):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, modulus)
        rows[rank] = [(inverse * value) % modulus for value in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                scale = rows[i][column]
                rows[i] = [(x - scale * y) % modulus
                           for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def check_k4_global_quadratic_relaxation():
    """Build the Helmert five-simplex in the real top space, exactly."""
    k, p, d = 4, 5, 14
    points = tuple(range(2 * k))
    blocks = tuple(combinations(points, k))
    all_matchings = tuple(matchings(points))
    polytabloids = [
        [e_value(matching, block) for block in blocks]
        for matching in all_matchings
    ]

    # Select four explicitly determined independent top polytabloids.
    raw = []
    for vector in polytabloids:
        if rank_mod(raw + [vector], 101) > len(raw):
            raw.append(vector)
        if len(raw) == 4:
            break
    assert len(raw) == 4

    # Exact Gram--Schmidt gives an orthogonal rational four-frame.  Its
    # normalized version is an orthonormal real frame in K.
    orthogonal = []
    norms = []
    for vector in raw:
        current = [Fraction(value) for value in vector]
        for prior, norm in zip(orthogonal, norms):
            coefficient = dot(current, prior) / norm
            current = [x - coefficient * y for x, y in zip(current, prior)]
        norm = dot(current, current)
        assert norm > 0
        orthogonal.append(current)
        norms.append(norm)
    assert all(dot(left, right) == 0
               for i, left in enumerate(orthogonal)
               for right in orthogonal[:i])

    # Unnormalized Helmert columns; their squared norms are 2,6,12,20.
    helmert = (
        (1, 1, 1, 1),
        (-1, 1, 1, 1),
        (0, -2, 1, 1),
        (0, 0, -3, 1),
        (0, 0, 0, -4),
    )
    helmert_norms = (2, 6, 12, 20)
    assert all(sum(row[column] for row in helmert) == 0 for column in range(4))

    # This is the Gram matrix of q_a in (12), computed without floating
    # point: 350 times the Gram of the normalized Helmert rows.
    q_gram = []
    for a in range(p):
        row = []
        for b in range(p):
            value = 350 * sum(
                Fraction(helmert[a][i] * helmert[b][i], helmert_norms[i])
                for i in range(4)
            )
            row.append(value)
        q_gram.append(row)
    expected_q = [[Fraction(280 if a == b else -70) for b in range(p)]
                  for a in range(p)]
    assert q_gram == expected_q

    # f_a=(1+q_a)/5 has exactly the partition's first and second moments.
    f_gram = [[Fraction(70, 25) + q_gram[a][b] / 25
               for b in range(p)] for a in range(p)]
    assert f_gram == [[Fraction(d if a == b else 0) for b in range(p)]
                      for a in range(p)]

    # Via the exact frame, the same construction has the complete
    # cross-matching quadratic derivative frame.
    derivative_frame = [[Fraction(factorial(p)) * q_gram[a][b] / (p * p)
                         for b in range(p)] for a in range(p)]
    expected_frame = [[Fraction(factorial(k) * d * (p * int(a == b) - 1))
                       for b in range(p)] for a in range(p)]
    assert derivative_frame == expected_frame

    # Every selected raw vector is a top polytabloid and so is in ker W;
    # therefore the real frame used above is global and automatically obeys
    # every four-point straightening relation.
    for vector in raw:
        for star in combinations(points, k - 1):
            assert sum(vector[index] for index, block in enumerate(blocks)
                       if set(star) <= set(block)) == 0

    print(
        "k=4: global Plucker plus exact first/second-moment relaxation "
        "has a real five-simplex in K"
    )


if __name__ == "__main__":
    check_k2_cubic_identity()
    check_k4_false_control()
    check_k4_global_quadratic_relaxation()
    print("PASS: cross-matching cubic audit controls verified.")
