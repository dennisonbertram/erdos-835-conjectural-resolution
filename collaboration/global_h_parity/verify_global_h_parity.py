#!/usr/bin/env python3
"""Independent global-H parity audit for the shared N-table.

Stdlib only.  No solver is used.  The script verifies:

* the one-factorization/Pfaffian sign identity through K_8;
* the no-hole two-sided link theorem on exact k=16 infinity layers;
* opposite H_infinity signs for cyclic and xor one-factorizations at k=16;
* the independent formula

      H = (-1)^C(k,2) Sigma(T) prod_x P(Psi^x)

  and its algebraic equality with the previously proved RHS(F), on all
  11,760 labelled k=6 chart/root controls and all 17 Wallis roots;
* two exact shared k=6 tables showing that matching-size profiles alone
  permit both link-sign products (these are deliberately not L/M-coherent).
"""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
FOLLOWUP = HERE.parent / "opus5" / "radius5_followup"
sys.path.insert(0, str(FOLLOWUP))

from verify_radius3_census_and_k6_obstruction import (  # noqa: E402
    all_sils,
    discordant_families,
    wallis_sils,
)


def ent(square, first, second):
    if first == second:
        return first
    return square[tuple(sorted((first, second)))]


def sign_sequence(values):
    inversions = sum(
        values[left] > values[right]
        for left in range(len(values))
        for right in range(left + 1, len(values))
    )
    return -1 if inversions % 2 else 1


def sign_map(domain, target, mapping):
    position = {value: index for index, value in enumerate(target)}
    assert set(mapping) == set(domain)
    assert set(mapping.values()) == set(target)
    return sign_sequence([position[mapping[value]] for value in domain])


def perfect_matchings(vertices, allowed_edges=None):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:]):
        edge = frozenset((first, second))
        if allowed_edges is not None and edge not in allowed_edges:
            continue
        rest = vertices[1 : index + 1] + vertices[index + 2 :]
        for tail in perfect_matchings(rest, allowed_edges):
            yield (edge,) + tail


def enumerate_one_factorizations(order):
    """Canonical enumeration: factor i-1 contains edge {0,i}."""

    edges = {frozenset(edge) for edge in combinations(range(order), 2)}

    def recurse(next_vertex, remaining):
        if next_vertex == order:
            yield ()
            return
        base = frozenset((0, next_vertex))
        if base not in remaining:
            return
        other_vertices = [
            vertex
            for vertex in range(1, order)
            if vertex != next_vertex
        ]
        for tail_matching in perfect_matchings(other_vertices, remaining - {base}):
            factor = frozenset((base,) + tail_matching)
            for tail in recurse(next_vertex + 1, remaining - factor):
                yield (factor,) + tail

    yield from recurse(1, edges)


def matching_mate(matching, vertex):
    edge = next(edge for edge in matching if vertex in edge)
    return next(other for other in edge if other != vertex)


def check_one_factorization(factors, vertices):
    vertices = tuple(vertices)
    expected_edges = {
        frozenset(edge) for edge in combinations(vertices, 2)
    }
    seen = set()
    for factor in factors:
        assert len(factor) == len(vertices) // 2
        assert {vertex for edge in factor for vertex in edge} == set(vertices)
        assert not (seen & set(factor))
        seen.update(factor)
    assert seen == expected_edges


def pfaffian_sign(matching, vertices):
    """Coefficient sign of an undirected matching in the ordered Pfaffian."""

    position = {vertex: index for index, vertex in enumerate(vertices)}
    ordered_edges = sorted(
        matching,
        key=lambda edge: min(position[vertex] for vertex in edge),
    )
    endpoint_sequence = []
    for edge in ordered_edges:
        endpoint_sequence.extend(
            sorted(position[vertex] for vertex in edge)
        )
    return sign_sequence(endpoint_sequence)


def row_sign_product(factors, vertices):
    """P(F): product of the vertex-row signs of a one-factorization."""

    vertices = tuple(vertices)
    product = 1
    for vertex in vertices:
        target = [other for other in vertices if other != vertex]
        mapping = {
            factor_index: matching_mate(factor, vertex)
            for factor_index, factor in enumerate(factors)
        }
        product *= sign_map(
            list(range(len(factors))),
            target,
            mapping,
        )
    return product


def of_constant(order):
    return (-1) ** comb(order // 2, 2)


def verify_of_identity():
    distributions = {}
    expected_counts = {4: 1, 6: 6, 8: 6240}
    for order in (4, 6, 8):
        distribution = Counter()
        count = 0
        for factors in enumerate_one_factorizations(order):
            count += 1
            p_value = row_sign_product(factors, range(order))
            q_value = 1
            for factor in factors:
                q_value *= pfaffian_sign(factor, range(order))
            assert p_value == of_constant(order) * q_value
            distribution[p_value] += 1
        assert count == expected_counts[order]
        distributions[order] = dict(sorted(distribution.items()))
    assert set(distributions[8]) == {-1, 1}
    print("[exact] OF identity P=c_n product(pf), distributions:", distributions)


def cyclic_one_factorization(order):
    assert order % 2 == 0
    infinity = order - 1
    factors = []
    for residue in range(order - 1):
        factor = {frozenset((infinity, residue))}
        for difference in range(1, order // 2):
            factor.add(
                frozenset(
                    (
                        (residue - difference) % (order - 1),
                        (residue + difference) % (order - 1),
                    )
                )
            )
        factors.append(frozenset(factor))
    check_one_factorization(factors, range(order))
    return tuple(factors)


def xor_one_factorization(order):
    assert order > 0 and order & (order - 1) == 0
    factors = []
    for difference in range(1, order):
        factor = {
            frozenset((vertex, vertex ^ difference))
            for vertex in range(order)
            if vertex < (vertex ^ difference)
        }
        factors.append(frozenset(factor))
    check_one_factorization(factors, range(order))
    return tuple(factors)


def edge_factor_map(factors):
    answer = {}
    for factor_index, factor in enumerate(factors):
        for edge in factor:
            assert edge not in answer
            answer[edge] = factor_index
    return answer


def infinity_regrouping_sign(factors, vertices):
    """The rho(Psi) order-regrouping sign of infinity_layer_theorem."""

    vertices = tuple(vertices)
    factor_indices = tuple(range(len(factors)))
    labels = edge_factor_map(factors)
    product = 1
    for missing_factor in factor_indices:
        excluded_mates = {
            vertex: matching_mate(
                factors[missing_factor],
                vertex,
            )
            for vertex in vertices
        }
        domain = [
            (vertex, other)
            for vertex in vertices
            for other in vertices
            if other not in (
                vertex,
                excluded_mates[vertex],
            )
        ]
        target = [
            (factor, vertex)
            for factor in factor_indices
            if factor != missing_factor
            for vertex in vertices
        ]
        mapping = {
            (vertex, other): (
                labels[frozenset((vertex, other))],
                vertex,
            )
            for vertex, other in domain
        }
        product *= sign_map(domain, target, mapping)
    return product


def infinity_layer_control(target_factors):
    """Build a full exact infinity layer and evaluate both link products."""

    order = len(target_factors) + 1
    assert order == 16
    source_factors = cyclic_one_factorization(order)
    source_label = edge_factor_map(source_factors)
    target_label = edge_factor_map(target_factors)
    star = order - 1
    indices = tuple(range(order - 1))
    finite = tuple(range(order))

    # Every source edge e selects one target perfect matching D_e.
    selected = {
        source_edge: target_factors[source_label[source_edge]]
        for source_edge in source_label
    }

    # Dual check: a target edge in factor h selects exactly source factor h.
    for target_edge in target_label:
        selected_source_edges = {
            source_edge
            for source_edge, matching in selected.items()
            if target_edge in matching
        }
        assert selected_source_edges == set(
            source_factors[target_label[target_edge]]
        )

    augmented_product = 1
    for source_vertex in range(order):
        source_domain = [
            other for other in range(order) if other != source_vertex
        ]
        for finite_vertex in finite:
            finite_target = [
                other for other in finite if other != finite_vertex
            ]
            mapping = {}
            for other_source in source_domain:
                source_edge = frozenset((source_vertex, other_source))
                mapping[other_source] = matching_mate(
                    selected[source_edge],
                    finite_vertex,
                )
            augmented_product *= sign_map(
                source_domain,
                finite_target,
                mapping,
            )
    assert augmented_product == 1

    h_infinity = 1
    for index in indices:
        for finite_vertex in finite:
            domain = [other for other in indices if other != index]
            missing_partner = matching_mate(
                target_factors[index],
                finite_vertex,
            )
            target = [
                other
                for other in finite
                if other not in (finite_vertex, missing_partner)
            ]
            mapping = {}
            for other_index in domain:
                source_edge = frozenset((index, other_index))
                mapping[other_index] = matching_mate(
                    selected[source_edge],
                    finite_vertex,
                )
            h_infinity *= sign_map(domain, target, mapping)

    # Check the exact dual forced matching after deleting the star.
    for finite_edge, missing_index in target_label.items():
        interior = {
            source_edge
            for source_edge, matching in selected.items()
            if star not in source_edge and finite_edge in matching
        }
        assert len(interior) == (order - 2) // 2
        assert {
            vertex for edge in interior for vertex in edge
        } == set(indices) - {missing_index}

    p_value = row_sign_product(target_factors, finite)
    rho_value = infinity_regrouping_sign(target_factors, finite)
    assert h_infinity == p_value
    assert h_infinity == rho_value
    return h_infinity


def verify_infinity_layers():
    xor_value = infinity_layer_control(xor_one_factorization(16))
    cyclic_value = infinity_layer_control(cyclic_one_factorization(16))
    assert (xor_value, cyclic_value) == (1, -1)
    print(
        "[exact] k=16 infinity layers: "
        f"H_inf(xor)={xor_value:+d}, H_inf(cyclic)={cyclic_value:+d}"
    )


def square_row_sign(square, row, colour_order):
    mapping = {
        column: ent(square, row, column)
        for column in colour_order
    }
    return sign_map(colour_order, colour_order, mapping)


def chart_quantities(family, colour_count, infinity, check_dummy=False):
    finite = [colour for colour in range(colour_count) if colour != infinity]
    indices = list(range(len(family)))
    k = len(finite)
    assert len(indices) == k - 1 and k % 2 == 0
    colour_order = finite + [infinity]
    finite_position = {
        colour: position for position, colour in enumerate(finite)
    }
    L = {
        (index, vertex): ent(family[index], infinity, vertex)
        for index in indices
        for vertex in finite
    }

    # The order-k Latin square T.
    row_product = 1
    for index in indices:
        row_product *= sign_map(
            finite,
            finite,
            {vertex: L[index, vertex] for vertex in finite},
        )
    column_product = 1
    t_rows = indices + ["*"]
    for vertex in finite:
        column_product *= sign_map(
            t_rows,
            finite,
            {
                **{index: L[index, vertex] for index in indices},
                "*": vertex,
            },
        )
    symbol_product = 1
    lambda_signs = {}
    for symbol in finite:
        mapping = {
            index: next(
                vertex
                for vertex in finite
                if L[index, vertex] == symbol
            )
            for index in indices
        }
        mapping["*"] = symbol
        lambda_signs[symbol] = sign_map(t_rows, finite, mapping)
        symbol_product *= lambda_signs[symbol]
    at_value = row_product * column_product
    fixed = (-1) ** comb(k, 2)
    assert at_value * symbol_product == fixed

    delta_product = 1
    for square in family:
        delta = 1
        for row in colour_order:
            delta *= square_row_sign(square, row, colour_order)
        delta_product *= delta

    psi_products = {}
    psi_factors_by_colour = {}
    for symbol in colour_order:
        factors = []
        for index, square in enumerate(family):
            factor = {
                frozenset(edge)
                for edge in combinations(finite, 2)
                if ent(square, edge[0], edge[1]) == symbol
            }
            if symbol != infinity:
                inverse = next(
                    vertex
                    for vertex in finite
                    if L[index, vertex] == symbol
                )
                factor.add(frozenset((symbol, inverse)))
            assert len(factor) == k // 2
            assert {
                vertex for edge in factor for vertex in edge
            } == set(finite)
            factors.append(frozenset(factor))
        check_one_factorization(factors, finite)
        psi_factors_by_colour[symbol] = tuple(factors)
        psi_products[symbol] = row_sign_product(factors, finite)

    product_psi = 1
    for value in psi_products.values():
        product_psi *= value
    assert product_psi == fixed * delta_product

    independent = fixed * symbol_product * product_psi
    flag_formula = fixed * at_value * delta_product
    assert independent == flag_formula

    if check_dummy:
        # The dummy-vertex Pfaffian identity (18), including every deletion
        # sign, and the replacement identity (19).
        dummy = ("dummy", infinity)
        for index, square in enumerate(family):
            near_product = 1
            augmented_product = 1
            augmented_factors = []
            delta = 1
            for row in colour_order:
                delta *= square_row_sign(square, row, colour_order)
            for symbol in colour_order:
                near_vertices = [
                    colour
                    for colour in colour_order
                    if colour != symbol
                ]
                near_factor = {
                    frozenset(edge)
                    for edge in combinations(colour_order, 2)
                    if ent(square, edge[0], edge[1]) == symbol
                }
                assert len(near_factor) == k // 2
                assert {
                    vertex
                    for edge in near_factor
                    for vertex in edge
                } == set(near_vertices)
                near_pfaffian = pfaffian_sign(
                    near_factor,
                    near_vertices,
                )
                near_product *= near_pfaffian

                augmented_factor = set(near_factor)
                augmented_factor.add(frozenset((symbol, dummy)))
                augmented_factor = frozenset(augmented_factor)
                augmented_factors.append(augmented_factor)
                augmented_pfaffian = pfaffian_sign(
                    augmented_factor,
                    colour_order + [dummy],
                )
                assert augmented_pfaffian == (
                    (-1)
                    ** (
                        k
                        - colour_order.index(symbol)
                    )
                    * near_pfaffian
                )
                augmented_product *= augmented_pfaffian

                if symbol == infinity:
                    assert (
                        near_factor
                        == psi_factors_by_colour[symbol][index]
                    )
                else:
                    inverse = next(
                        vertex
                        for vertex in finite
                        if L[index, vertex] == symbol
                    )
                    replacement_ratio = (
                        pfaffian_sign(
                            psi_factors_by_colour[symbol][index],
                            finite,
                        )
                        * near_pfaffian
                    )
                    expected_ratio = (-1) ** (
                        k
                        - 1
                        - finite_position[symbol]
                        + (
                            finite_position[inverse]
                            > finite_position[symbol]
                        )
                    )
                    assert replacement_ratio == expected_ratio

            assert delta == of_constant(k + 2) * near_product
            check_one_factorization(
                augmented_factors,
                colour_order + [dummy],
            )
            assert (
                row_sign_product(
                    augmented_factors,
                    colour_order + [dummy],
                )
                == of_constant(k + 2) * augmented_product
            )

        # Infinity cofactors.
        infinity_correction = 1
        infinity_factors = psi_factors_by_colour[infinity]
        for index in indices:
            for vertex in finite:
                mate = matching_mate(infinity_factors[index], vertex)
                target = [value for value in finite if value != vertex]
                infinity_correction *= (-1) ** (
                    (k - 2) + target.index(mate)
                )
        assert infinity_correction == 1

        # Finite-colour cofactors, evaluated directly flag by flag.
        for symbol in finite:
            inverse = {
                index: next(
                    vertex
                    for vertex in finite
                    if L[index, vertex] == symbol
                )
                for index in indices
            }
            inverse_index = {
                vertex: index for index, vertex in inverse.items()
            }
            direct = 1
            for index in indices:
                hole = inverse[index]

                # Empty flag u=a_i: j -> a_j and * -> x.
                domain = [other for other in indices if other != index] + ["*"]
                target = [vertex for vertex in finite if vertex != hole]
                mapping = {
                    **{
                        other: inverse[other]
                        for other in indices
                        if other != index
                    },
                    "*": symbol,
                }
                direct *= sign_map(domain, target, mapping)

                # Flag u=x: delete the last dummy and its image a_i.
                target_at_x = [
                    vertex for vertex in finite if vertex != symbol
                ]
                direct *= (-1) ** (
                    (k - 2) + target_at_x.index(hole)
                )

                # Generic flags: add j_u -> a_i and * -> M_i-x mate.
                for vertex in finite:
                    if vertex in (symbol, hole):
                        continue
                    omitted_index = inverse_index[vertex]
                    source_order = [
                        other for other in indices if other != index
                    ] + ["*"]
                    target_order = [
                        other for other in finite if other != vertex
                    ]
                    source_positions = (
                        source_order.index(omitted_index),
                        source_order.index("*"),
                    )
                    mate = next(
                        other
                        for other in finite
                        if other != vertex
                        and ent(
                            family[index],
                            vertex,
                            other,
                        )
                        == symbol
                    )
                    target_positions = (
                        target_order.index(hole),
                        target_order.index(mate),
                    )
                    orientation = (
                        1
                        if target_positions[0] < target_positions[1]
                        else -1
                    )
                    direct *= (
                        (-1)
                        ** (
                            sum(source_positions)
                            + sum(target_positions)
                        )
                        * orientation
                    )
            closed = (
                (-1)
                ** (
                    finite_position[symbol]
                    + 1
                    + (k - 2) // 2
                )
                * lambda_signs[symbol]
            )
            assert direct == closed

    return {
        "independent": independent,
        "flag_formula": flag_formula,
        "symbol": symbol_product,
        "delta": delta_product,
        "psi_product": product_psi,
        "psi_signs": tuple(psi_products[colour] for colour in colour_order),
    }


def verify_chart_controls():
    squares = all_sils(7)
    families = discordant_families(squares, 7, 5)
    distribution = Counter()
    for family_indices in families:
        family = [squares[index] for index in family_indices]
        for infinity in range(7):
            values = chart_quantities(family, 7, infinity)
            distribution[
                (
                    values["independent"],
                    values["flag_formula"],
                    values["symbol"],
                    values["psi_product"],
                )
            ] += 1
    assert sum(distribution.values()) == 11_760
    assert all(key[0] == key[1] for key in distribution)
    print("[exact] k=6 all chart/root controls:", dict(sorted(distribution.items())))

    # Directly audit every dummy cofactor on one representative of each
    # sign outcome.
    checked = set()
    for family_indices in families:
        family = [squares[index] for index in family_indices]
        for infinity in range(7):
            values = chart_quantities(
                family,
                7,
                infinity,
                check_dummy=True,
            )
            checked.add(values["independent"])
            if checked == {-1, 1}:
                break
        if checked == {-1, 1}:
            break
    assert checked == {-1, 1}

    wallis = wallis_sils()
    wallis_values = [
        chart_quantities(wallis, 17, infinity, check_dummy=True)
        for infinity in range(17)
    ]
    assert {
        (
            value["independent"],
            value["flag_formula"],
            value["symbol"],
            value["psi_product"],
        )
        for value in wallis_values
    } == {(1, 1, 1, 1)}
    assert {
        value["psi_signs"] for value in wallis_values
    } == {(1,) * 17}
    print("[exact] Wallis all 17 roots: G=F=Sigma=prod(Psi)=+1")


PROFILE_PLUS = (
    (6, 2, 0, 4, 5, 5, 1, 0, 4, 6, 3, 1, 2, 3, 6),
    (2, 6, 4, 0, 1, 1, 5, 6, 3, 0, 4, 2, 3, 6, 5),
    (0, 3, 6, 5, 4, 2, 3, 1, 6, 1, 6, 0, 4, 5, 2),
    (1, 5, 3, 6, 0, 3, 6, 4, 5, 4, 2, 6, 0, 2, 1),
    (1, 0, 3, 2, 6, 2, 6, 3, 5, 5, 6, 4, 4, 1, 0),
    (5, 4, 2, 6, 0, 6, 0, 4, 1, 3, 2, 5, 1, 6, 3),
    (4, 6, 1, 0, 2, 0, 3, 1, 6, 2, 5, 3, 6, 5, 4),
    (6, 1, 0, 3, 5, 4, 1, 5, 2, 2, 0, 6, 6, 3, 4),
    (0, 2, 6, 4, 3, 6, 4, 2, 1, 3, 1, 5, 5, 0, 6),
    (3, 0, 5, 1, 6, 1, 2, 6, 0, 6, 4, 2, 3, 4, 5),
)

PROFILE_MINUS = (
    (6, 2, 3, 5, 0, 0, 1, 4, 5, 6, 3, 1, 2, 4, 6),
    (2, 1, 0, 6, 5, 6, 4, 1, 3, 3, 2, 0, 5, 6, 4),
    (3, 0, 1, 4, 6, 1, 6, 2, 4, 5, 6, 2, 0, 3, 5),
    (0, 5, 6, 1, 3, 4, 3, 6, 1, 2, 0, 6, 4, 5, 2),
    (1, 0, 5, 4, 6, 3, 6, 0, 2, 2, 6, 4, 3, 1, 5),
    (0, 4, 6, 3, 2, 5, 3, 6, 1, 1, 2, 6, 4, 5, 0),
    (4, 6, 2, 0, 1, 2, 5, 1, 6, 3, 4, 5, 6, 0, 3),
    (5, 6, 3, 0, 4, 2, 1, 3, 6, 0, 4, 5, 6, 2, 1),
    (6, 3, 4, 2, 0, 1, 0, 4, 5, 6, 5, 2, 1, 3, 6),
    (1, 2, 0, 6, 5, 6, 2, 5, 0, 4, 1, 3, 3, 6, 4),
)


def verify_profile_table(table):
    k = 6
    indices = tuple(range(5))
    finite = tuple(range(6))
    infinity = 6
    index_edges = tuple(combinations(indices, 2))
    finite_edges = tuple(combinations(finite, 2))
    index_edge_position = {
        edge: position for position, edge in enumerate(index_edges)
    }
    finite_edge_position = {
        edge: position for position, edge in enumerate(finite_edges)
    }
    assert len(table) == len(index_edges)
    assert all(len(row) == len(finite_edges) for row in table)

    for row in table:
        for colour in range(7):
            selected = {
                finite_edges[position]
                for position, value in enumerate(row)
                if value == colour
            }
            expected = 3 if colour == infinity else 2
            assert len(selected) == expected
            assert len({vertex for edge in selected for vertex in edge}) == 2 * expected

    for finite_edge in finite_edges:
        column = [
            table[index_position][finite_edge_position[finite_edge]]
            for index_position in range(len(index_edges))
        ]
        for colour in range(7):
            selected = {
                index_edges[position]
                for position, value in enumerate(column)
                if value == colour
            }
            expected = 2 if colour in (*finite_edge, infinity) else 1
            assert len(selected) == expected
            assert len({index for edge in selected for index in edge}) == 2 * expected

    link_product = 1
    bad_exact_flags = 0
    for index in indices:
        for vertex in finite:
            sizes = []
            for colour in range(7):
                mapping = {}
                for other_index in indices:
                    if other_index == index:
                        continue
                    index_edge = tuple(sorted((index, other_index)))
                    hits = [
                        other_vertex
                        for other_vertex in finite
                        if other_vertex != vertex
                        and table[index_edge_position[index_edge]][
                            finite_edge_position[
                                tuple(sorted((vertex, other_vertex)))
                            ]
                        ]
                        == colour
                    ]
                    if hits:
                        assert len(hits) == 1
                        mapping[other_index] = hits[0]
                target = sorted(mapping.values())
                assert len(target) == len(set(target))
                sizes.append(len(mapping))
                if mapping:
                    link_product *= sign_map(
                        sorted(mapping),
                        target,
                        mapping,
                    )
            if not (
                sizes[infinity] == k - 2
                and sizes[vertex] == k - 2
                and sorted(sizes) == [0, 3, 3, 3, 3, 4, 4]
            ):
                bad_exact_flags += 1
    assert bad_exact_flags > 0
    return link_product, bad_exact_flags


def verify_profile_countermodels():
    plus = verify_profile_table(PROFILE_PLUS)
    minus = verify_profile_table(PROFILE_MINUS)
    assert plus[0] == 1 and minus[0] == -1
    print(
        "[exact] size-profile-only shared tables: "
        f"H={plus[0]:+d}/{minus[0]:+d}; "
        f"non-L/M-coherent flags={plus[1]}/{minus[1]}"
    )


def main():
    verify_of_identity()
    verify_infinity_layers()
    verify_chart_controls()
    verify_profile_countermodels()
    print("ALL GLOBAL-H PARITY AUDITS PASSED")
    print("SCOPE: structural identity/no-go only; no k=16 N-table is asserted.")


if __name__ == "__main__":
    main()
