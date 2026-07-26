#!/usr/bin/env python3
"""Exact cross-root audit for the individual layer-sign formulas.

This is a standard-library-only verifier.  It constructs the fifteen Wallis
SILS(17) squares from the published starter array and checks, without any
radius-five solver or N-table, all N-free claims made in README.md:

* every root/colour completion Psi is a one-factorization of K_16;
* P(Psi^{r,x}) is independent of the distinguished root r;
* the factorwise root switch has the stated two-edge form;
* the lambda and H_required transition formulas hold for every ordered
  (r,s,x), with r,s,x distinct;
* all scalar transition products around root cycles are identically +1.

No H_observed value is computed: no compatible Wallis radius-five N-table is
known.  H_required is the value forced by the proved layer theorem if such a
table exists.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations


Q = 17
COLOURS = tuple(range(Q))
INDICES = tuple(range(Q - 2))
STAR = "*"
INDEX_WITH_DUMMY = INDICES + (STAR,)

# Rows a_1,...,a_8 of Wallis's circulant golf array, transposed so that
# each column specifies one of the fifteen squares.
FIRST_HALF_COLUMNS = (
    tuple(range(2, 17)),
    (5, 1, 7, 8, 9, 16, 14, 4, 13, 15, 10, 6, 11, 3, 12),
    (9, 10, 12, 2, 15, 13, 16, 14, 4, 7, 5, 8, 1, 11, 6),
    (14, 12, 2, 13, 3, 8, 9, 16, 7, 5, 1, 15, 6, 10, 11),
    (16, 11, 13, 15, 1, 3, 6, 10, 2, 14, 4, 7, 8, 12, 9),
    (13, 15, 16, 1, 14, 11, 4, 7, 12, 8, 9, 3, 10, 5, 2),
    (15, 4, 1, 14, 11, 2, 10, 3, 5, 6, 13, 16, 12, 9, 8),
    (12, 13, 14, 11, 10, 9, 2, 6, 16, 3, 15, 1, 7, 4, 5),
)


def sign_sequence(values: list[int]) -> int:
    inversions = sum(
        values[left] > values[right]
        for left in range(len(values))
        for right in range(left + 1, len(values))
    )
    return -1 if inversions % 2 else 1


def sign_map(domain, target, mapping) -> int:
    domain = tuple(domain)
    target = tuple(target)
    assert set(mapping) == set(domain)
    assert set(mapping.values()) == set(target)
    position = {value: index for index, value in enumerate(target)}
    return sign_sequence([position[mapping[value]] for value in domain])


def construct_wallis() -> tuple[tuple[tuple[int, ...], ...], ...]:
    squares = []
    for square_index in INDICES:
        starter = [0] + [
            FIRST_HALF_COLUMNS[offset - 1][square_index] for offset in range(1, 9)
        ]
        starter.extend([-1] * 8)
        for offset in range(9, Q):
            starter[offset] = (starter[Q - offset] + offset) % Q
        assert sorted(starter) == list(COLOURS)
        square = tuple(
            tuple((starter[(left - right) % Q] + right) % Q for right in COLOURS)
            for left in COLOURS
        )
        squares.append(square)
    return tuple(squares)


def matching_mate(matching, vertex):
    edge = next(edge for edge in matching if vertex in edge)
    return next(other for other in edge if other != vertex)


def check_one_factorization(factors, vertices) -> None:
    vertices = tuple(vertices)
    all_edges = {frozenset(edge) for edge in combinations(vertices, 2)}
    seen = set()
    for matching in factors:
        assert len(matching) == len(vertices) // 2
        assert {vertex for edge in matching for vertex in edge} == set(vertices)
        assert not (seen & set(matching))
        seen.update(matching)
    assert seen == all_edges


def row_sign_product(factors, vertices) -> int:
    """P(F), with the fixed order of INDICES on the factors."""

    vertices = tuple(vertices)
    answer = 1
    for vertex in vertices:
        answer *= sign_map(
            INDICES,
            tuple(other for other in vertices if other != vertex),
            {index: matching_mate(factors[index], vertex) for index in INDICES},
        )
    return answer


def near_factor(square, colour):
    """The colour-class matching R_i^x on C minus {x}."""

    return frozenset(
        frozenset(edge)
        for edge in combinations(COLOURS, 2)
        if square[edge[0]][edge[1]] == colour
    )


def root_vertices(root):
    return tuple(colour for colour in COLOURS if colour != root)


def psi_factor(square, root, colour):
    """Psi_i^{r,x}, a perfect matching on C minus {r}."""

    factor = set(near_factor(square, colour))
    if colour != root:
        root_edge = next(edge for edge in factor if root in edge)
        mate = next(vertex for vertex in root_edge if vertex != root)
        factor.remove(root_edge)
        factor.add(frozenset((colour, mate)))
    return frozenset(factor)


def psi_family(squares, root, colour):
    factors = tuple(psi_factor(squares[index], root, colour) for index in INDICES)
    check_one_factorization(factors, root_vertices(root))
    return factors


def lambda_map(squares, root, colour):
    assert colour != root
    mapping = {}
    for index in INDICES:
        matching = near_factor(squares[index], colour)
        mapping[index] = matching_mate(matching, root)
    mapping[STAR] = colour
    assert set(mapping.values()) == set(root_vertices(root))
    return mapping


def swap_map(root, new_root):
    """The transposition (root new_root), restricted V_root -> V_new_root."""

    assert root != new_root
    return {
        vertex: (root if vertex == new_root else new_root if vertex == root else vertex)
        for vertex in root_vertices(root)
    }


def transport_matching(matching, mapping):
    return frozenset(
        frozenset((mapping[left], mapping[right]))
        for left, right in (tuple(edge) for edge in matching)
    )


def transition_theta(old_lambda, new_lambda, tau):
    """(lambda_x^s)^(-1) tau_rs lambda_x^r on A union {*}."""

    inverse_new = {value: key for key, value in new_lambda.items()}
    return {key: inverse_new[tau[old_lambda[key]]] for key in INDEX_WITH_DUMMY}


def required_h(p_value, root, colour, lam=None):
    """Layer value forced by (10)/(17) if a compatible N-table exists."""

    if colour == root:
        assert lam is None
        return p_value
    assert lam is not None
    vertices = root_vertices(root)
    lam_sign = sign_map(
        INDEX_WITH_DUMMY,
        vertices,
        lam,
    )
    k = len(vertices)
    exponent = vertices.index(colour) + 1 + (k - 2) // 2
    return (-1) ** exponent * lam_sign * p_value


def audit_wallis() -> None:
    squares = construct_wallis()

    # SILS and golf identities.
    for square in squares:
        for row in COLOURS:
            assert tuple(sorted(square[row])) == COLOURS
            assert square[row][row] == row
            for column in COLOURS:
                assert square[row][column] == square[column][row]
    for left, right in combinations(COLOURS, 2):
        assert {square[left][right] for square in squares} == set(COLOURS) - {
            left,
            right,
        }

    # Build every one-factorization and verify root-independence of P.
    psi_cache = {
        (root, colour): psi_family(squares, root, colour)
        for root in COLOURS
        for colour in COLOURS
    }
    lambda_cache = {
        (root, colour): lambda_map(squares, root, colour)
        for root in COLOURS
        for colour in COLOURS
        if colour != root
    }
    p_by_colour_and_root = {}
    for colour in COLOURS:
        values = {}
        for root in COLOURS:
            values[root] = row_sign_product(
                psi_cache[root, colour],
                root_vertices(root),
            )
        assert len(set(values.values())) == 1
        p_by_colour_and_root[colour] = values
    p_values = {colour: values[0] for colour, values in p_by_colour_and_root.items()}
    required = {}
    for colour in COLOURS:
        for root in COLOURS:
            required[colour, root] = required_h(
                p_values[colour],
                root,
                colour,
                (None if colour == root else lambda_cache[root, colour]),
            )

    switch_checks = 0
    theta_checks = 0
    h_transition_checks = 0
    crossing_h_checks = 0
    for root in COLOURS:
        for new_root in COLOURS:
            if root == new_root:
                continue
            tau = swap_map(root, new_root)
            epsilon = sign_map(
                root_vertices(root),
                root_vertices(new_root),
                tau,
            )
            for colour in COLOURS:
                old_factors = psi_cache[root, colour]
                new_factors = psi_cache[new_root, colour]
                transported = tuple(
                    transport_matching(matching, tau) for matching in old_factors
                )

                if colour in (root, new_root):
                    # The root layer becomes exactly the corresponding finite
                    # layer (or conversely) after swapping the two labels.
                    assert transported == new_factors
                    finite_root = new_root if colour == root else root
                    vertices = root_vertices(finite_root)
                    finite_coefficient = (-1) ** (
                        vertices.index(colour) + 1 + (len(vertices) - 2) // 2
                    ) * sign_map(
                        INDEX_WITH_DUMMY,
                        vertices,
                        lambda_cache[finite_root, colour],
                    )
                    assert (
                        required[colour, new_root] * required[colour, root]
                        == finite_coefficient
                    )
                    crossing_h_checks += 1
                else:
                    h_index = next(
                        index
                        for index, square in enumerate(squares)
                        if square[root][new_root] == colour
                    )
                    assert transported[h_index] == new_factors[h_index]
                    for index in INDICES:
                        if index == h_index:
                            continue
                        old_matching = transported[index]
                        new_matching = new_factors[index]
                        # Precisely two old edges and two new edges form the
                        # four-cycle switch described in the theorem.
                        removed = old_matching - new_matching
                        added = new_matching - old_matching
                        assert len(removed) == len(added) == 2
                        assert {vertex for edge in removed for vertex in edge} == {
                            vertex for edge in added for vertex in edge
                        }
                    switch_checks += 1

                    old_lambda = lambda_cache[root, colour]
                    new_lambda = lambda_cache[new_root, colour]
                    theta = transition_theta(old_lambda, new_lambda, tau)
                    h_index_from_theta = next(
                        index for index in INDICES if old_lambda[index] == new_root
                    )
                    assert h_index_from_theta == h_index
                    assert theta[STAR] == STAR
                    assert theta[h_index] == h_index
                    old_lambda_sign = sign_map(
                        INDEX_WITH_DUMMY,
                        root_vertices(root),
                        old_lambda,
                    )
                    new_lambda_sign = sign_map(
                        INDEX_WITH_DUMMY,
                        root_vertices(new_root),
                        new_lambda,
                    )
                    theta_sign = sign_map(
                        INDEX_WITH_DUMMY,
                        INDEX_WITH_DUMMY,
                        theta,
                    )
                    assert new_lambda_sign == epsilon * old_lambda_sign * theta_sign
                    theta_checks += 1

                    old_position = root_vertices(root).index(colour)
                    new_position = root_vertices(new_root).index(colour)
                    expected_ratio = (
                        (-1) ** (old_position + new_position) * epsilon * theta_sign
                    )
                    actual_ratio = required[colour, new_root] * required[colour, root]
                    assert actual_ratio == expected_ratio
                    h_transition_checks += 1

    # The compact kappa form covers transitions in which x is itself one
    # of the roots as well as the distinct-root formula above.
    kappa = {}
    for colour in COLOURS:
        for root in COLOURS:
            kappa[colour, root] = required[colour, root] * p_values[colour]
            assert required[colour, root] == (kappa[colour, root] * p_values[colour])

    cycle_checks = 0
    for colour in COLOURS:
        for first in COLOURS:
            for second in COLOURS:
                for third in COLOURS:
                    transition_12 = kappa[colour, second] * kappa[colour, first]
                    transition_23 = kappa[colour, third] * kappa[colour, second]
                    transition_31 = kappa[colour, first] * kappa[colour, third]
                    assert transition_12 * transition_23 * transition_31 == 1
                    cycle_checks += 1

    p_distribution = Counter(p_values.values())
    lambda_distribution = Counter()
    h_distribution_by_root = {}
    h_matrix_rows = []
    for root in COLOURS:
        row = tuple(required[colour, root] for colour in COLOURS)
        h_matrix_rows.append(row)
        h_distribution_by_root[root] = dict(sorted(Counter(row).items()))
        for colour in COLOURS:
            if colour != root:
                lambda_distribution[
                    sign_map(
                        INDEX_WITH_DUMMY,
                        root_vertices(root),
                        lambda_map(squares, root, colour),
                    )
                ] += 1

    # These fingerprints make accidental convention changes visible.
    assert p_distribution == Counter({1: 17})
    assert lambda_distribution == Counter({1: 136, -1: 136})
    assert set(
        tuple(sorted(distribution.items()))
        for distribution in h_distribution_by_root.values()
    ) == {((-1, 8), (1, 9))}
    assert {
        tuple(sorted(Counter(required[colour, root] for root in COLOURS).items()))
        for colour in COLOURS
    } == {((-1, 8), (1, 9))}
    assert all(row[root] == 1 for root, row in enumerate(h_matrix_rows))
    assert h_matrix_rows[16] == (
        1,
        -1,
        -1,
        -1,
        -1,
        -1,
        1,
        1,
        -1,
        -1,
        -1,
        1,
        1,
        1,
        1,
        1,
        1,
    )

    print("[exact] Wallis G(17): SILS and golf identities PASS")
    print(
        "[exact] 289 root/colour one-factorizations: P(Psi^{r,x}) is root-independent"
    )
    print(
        f"[exact] factor switches={switch_checks}, "
        f"lambda laws={theta_checks}, "
        f"third-colour H transitions={h_transition_checks}, "
        f"root-crossing H transitions={crossing_h_checks}"
    )
    print(f"[exact] scalar root-cycle products={cycle_checks}: all +1")
    print(
        "[exact] Wallis fingerprints: "
        f"P={dict(sorted(p_distribution.items()))}, "
        f"lambda={dict(sorted(lambda_distribution.items()))}"
    )
    print(
        "[exact] Wallis conditional layer targets: "
        "each root has 8 negative and 9 positive layers; "
        "the root layer is always +1"
    )
    print(f"[exact] root 16 target row: {h_matrix_rows[16]}")
    print(
        "[scope] no N-table and no H_observed was constructed; "
        "Erdos-Rosenfeld #835 remains open"
    )


if __name__ == "__main__":
    audit_wallis()
