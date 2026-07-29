#!/usr/bin/env python3
"""Independent exact checks for the finite-layer/total-sign proof.

This script is evidence, not a substitute for the general proof in README.md.
It uses only the standard library and deliberately recomputes cofactors from
ordered subsets rather than importing either earlier sign verifier.
"""

from itertools import combinations
from math import comb
from random import Random


def sign_word(word):
    return -1 if sum(
        word[i] > word[j]
        for i in range(len(word))
        for j in range(i + 1, len(word))
    ) % 2 else 1


def sign_map(domain, target, mapping):
    positions = {value: index for index, value in enumerate(target)}
    assert set(mapping) == set(domain)
    assert set(mapping.values()) == set(target)
    return sign_word([positions[mapping[value]] for value in domain])


def cofactor(X, Y, old_domain, old_target, complement):
    """Sign(full extension) / sign(old map), for induced old orders."""

    old_domain = [value for value in X if value in old_domain]
    old_target = [value for value in Y if value in old_target]
    new_domain = [value for value in X if value not in old_domain]
    new_target = [value for value in Y if value not in old_target]
    identity_x = {value: value for value in X}
    identity_y = {value: value for value in Y}
    return (
        sign_map(old_domain + new_domain, X, identity_x)
        * sign_map(old_target + new_target, Y, identity_y)
        * sign_map(new_domain, new_target, complement)
    )


def random_matching(vertices, rng):
    vertices = list(vertices)
    rng.shuffle(vertices)
    return {
        vertices[index]: vertices[index ^ 1]
        for index in range(len(vertices))
    }


def verify_finite_cofactor_formula():
    rng = Random(835_2026)
    checked = 0
    for k in (2, 4, 6, 8, 10):
        V = list(range(k))
        A = list(range(k - 1))
        star = k - 1
        B = A + [star]
        for x in V:
            for _ in range(40):
                values = [value for value in V if value != x]
                rng.shuffle(values)
                a = dict(zip(A, values))
                inverse_a = {value: index for index, value in a.items()}
                lam = {**a, star: x}
                correction = 1

                for i in A:
                    # Empty old flag u=a_i: the full map is lambda without i.
                    X = [row for row in B if row != i]
                    u = a[i]
                    Y = [value for value in V if value != u]
                    gamma = {
                        row: lam[row]
                        for row in X
                    }
                    correction *= sign_map(X, Y, gamma)

                    # Nonempty flag u=x: add star -> a_i.
                    u = x
                    X = [row for row in B if row != i]
                    Y = [value for value in V if value != u]
                    old_domain = {row for row in A if row != i}
                    old_target = {
                        value for value in V
                        if value not in (u, a[i])
                    }
                    correction *= cofactor(
                        X, Y, old_domain, old_target, {star: a[i]}
                    )

                    # Generic flags.
                    U = [value for value in V if value not in (x, a[i])]
                    mate = random_matching(U, rng)
                    for u in U:
                        missing_row = inverse_a[u]
                        X = [row for row in B if row != i]
                        Y = [value for value in V if value != u]
                        old_domain = {
                            row for row in A
                            if row not in (i, missing_row)
                        }
                        old_target = {
                            value for value in V
                            if value not in (u, a[i], mate[u])
                        }
                        correction *= cofactor(
                            X,
                            Y,
                            old_domain,
                            old_target,
                            {missing_row: a[i], star: mate[u]},
                        )

                expected = (
                    (-1) ** (x + 1 + (k - 2) // 2)
                    * sign_map(B, V, lam)
                )
                assert correction == expected
                checked += 1
    print(f"[exact] finite cofactor formula: {checked:,} random instances PASS")


def pfaffian_sign(matching, vertices):
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    edges = sorted(
        (
            tuple(sorted((positions[left], positions[right])))
            for left, right in matching
            if positions[left] < positions[right]
        ),
        key=lambda edge: edge[0],
    )
    return sign_word([point for edge in edges for point in edge])


def standard_factorization(order):
    infinity = order - 1
    factors = []
    for colour in range(order - 1):
        factor = {(colour, infinity)}
        for offset in range(1, order // 2):
            left = (colour - offset) % (order - 1)
            right = (colour + offset) % (order - 1)
            factor.add(tuple(sorted((left, right))))
        factors.append(factor)
    expected = {
        tuple(edge)
        for edge in combinations(range(order), 2)
    }
    assert set().union(*factors) == expected
    assert sum(map(len, factors)) == len(expected)
    return factors


def matching_mate(matching, vertex):
    for left, right in matching:
        if left == vertex:
            return right
        if right == vertex:
            return left
    raise AssertionError(vertex)


def row_product(factors, vertices):
    vertices = list(vertices)
    return product(
        sign_map(
            list(range(len(factors))),
            [other for other in vertices if other != vertex],
            {
                index: matching_mate(factor, vertex)
                for index, factor in enumerate(factors)
            },
        )
        for vertex in vertices
    )


def product(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def relabel_factorization(factors, permutation):
    return [
        {
            tuple(sorted((permutation[left], permutation[right])))
            for left, right in factor
        }
        for factor in factors
    ]


def verify_one_factorization_sign():
    rng = Random(835)
    checked = 0
    for k in (2, 4, 6, 8, 10, 12):
        base = standard_factorization(k)
        for _ in range(100):
            permutation = list(range(k))
            rng.shuffle(permutation)
            factors = relabel_factorization(base, permutation)
            rng.shuffle(factors)
            lhs = row_product(factors, range(k))
            rhs = (
                (-1) ** comb(k // 2, 2)
                * product(pfaffian_sign(factor, range(k)) for factor in factors)
            )
            assert lhs == rhs
            checked += 1
    print(f"[exact] one-factorization sign: {checked:,} relabelings PASS")


def symmetric_idempotent_from_factorization(order):
    """Return S on C of size order-1, using the last point as dummy."""

    factors = standard_factorization(order)
    dummy = order - 1
    C = list(range(order - 1))
    labelled = {}
    for factor in factors:
        edge = next(edge for edge in factor if dummy in edge)
        colour = next(vertex for vertex in edge if vertex != dummy)
        labelled[colour] = factor - {edge}
    assert set(labelled) == set(C)

    square = {(u, u): u for u in C}
    for colour, matching in labelled.items():
        for left, right in matching:
            square[left, right] = colour
            square[right, left] = colour
    for u in C:
        assert set(square[u, v] for v in C) == set(C)
    return C, labelled, square


def verify_near_factor_identity():
    checked = 0
    for k in (2, 4, 6, 8, 10):
        C, near_factors, square = symmetric_idempotent_from_factorization(k + 2)
        delta = product(
            sign_map(C, C, {v: square[u, v] for v in C})
            for u in C
        )
        pf_product = product(
            pfaffian_sign(
                near_factors[colour],
                [vertex for vertex in C if vertex != colour],
            )
            for colour in C
        )
        assert delta == (-1) ** comb(k // 2 + 1, 2) * pf_product
        checked += 1
    print(f"[exact] symmetric-idempotent near-factor identity: {checked} orders PASS")


def verify_global_replacement_parity():
    """Check (21)-(22) on cyclic Latin families for several even k."""

    for k in (2, 4, 6, 8, 10, 12, 16):
        V = list(range(k))
        A = list(range(1, k))
        exponent = 0
        for shift in A:
            # L_shift(u)=u+shift mod k.
            inverse = {
                x: (x - shift) % k
                for x in V
            }
            for x in V:
                a = inverse[x]
                assert a != x
                exponent += k - 1 - x + (a > x)
        assert exponent % 2 == 0
    print("[exact] global Pfaffian replacement parity: cyclic k=2..16 PASS")


if __name__ == "__main__":
    verify_finite_cofactor_formula()
    verify_one_factorization_sign()
    verify_near_factor_identity()
    verify_global_replacement_parity()
    print("finite total identity audit: PASS")
