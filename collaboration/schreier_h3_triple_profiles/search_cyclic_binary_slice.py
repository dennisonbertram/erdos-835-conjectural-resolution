#!/usr/bin/env python3
"""Probe a cyclic zero-one intersection-12 slice with CP-SAT.

This is a search, not a verifier.  UNKNOWN is a nonverdict.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations

from ortools.sat.python import cp_model


B_POINTS = tuple(range(15))
OUTSIDE_POINTS = tuple(range(16))
INFINITY = 15
A_TRIPLES = tuple(combinations(B_POINTS, 3))
U_TRIPLES = tuple(combinations(OUTSIDE_POINTS, 3))
A_INDEX = {triple: index for index, triple in enumerate(A_TRIPLES)}
U_INDEX = {triple: index for index, triple in enumerate(U_TRIPLES)}


def factorization() -> tuple[dict[int, set[tuple[int, int]]], dict]:
    factors: dict[int, set[tuple[int, int]]] = {
        a: set() for a in B_POINTS
    }
    for a in B_POINTS:
        factors[a].add(tuple(sorted((INFINITY, a))))
        for difference in range(1, 8):
            factors[a].add(
                tuple(
                    sorted(
                        (
                            (a + difference) % 15,
                            (a - difference) % 15,
                        )
                    )
                )
            )
    edge_colour = {
        edge: colour
        for colour, matching in factors.items()
        for edge in matching
    }
    assert len(edge_colour) == 120
    return factors, edge_colour


def translate_point(point: int, shift: int) -> int:
    return INFINITY if point == INFINITY else (point + shift) % 15


def translate_set(values: tuple[int, ...], shift: int) -> tuple[int, ...]:
    return tuple(sorted(translate_point(value, shift) for value in values))


def canonical_pair(
    a_triple: tuple[int, int, int],
    u_triple: tuple[int, int, int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return min(
        (
            translate_set(a_triple, shift),
            translate_set(u_triple, shift),
        )
        for shift in B_POINTS
    )


def orbit_representatives(items, translate):
    representatives = {}
    for item in items:
        canonical = min(translate(item, shift) for shift in B_POINTS)
        representatives.setdefault(canonical, item)
    return tuple(representatives.values())


def make_pair_orbits() -> tuple[list[list[int]], int]:
    orbit_by_canonical = {}
    pair_orbit = [[0] * len(U_TRIPLES) for _ in A_TRIPLES]
    for a_index, a_triple in enumerate(A_TRIPLES):
        for u_index, u_triple in enumerate(U_TRIPLES):
            canonical = canonical_pair(a_triple, u_triple)
            orbit_by_canonical.setdefault(
                canonical, len(orbit_by_canonical)
            )
            pair_orbit[a_index][u_index] = orbit_by_canonical[canonical]
    return pair_orbit, len(orbit_by_canonical)


def build_model(include_q: bool):
    factors, edge_colour = factorization()
    pair_orbit, orbit_count = make_pair_orbits()
    q_values = [
        [
            len(
                set(a_triple)
                & {
                    edge_colour[edge]
                    for edge in combinations(u_triple, 2)
                }
            )
            for u_triple in U_TRIPLES
        ]
        for a_triple in A_TRIPLES
    ]

    row_representatives = orbit_representatives(
        A_TRIPLES,
        lambda triple, shift: translate_set(triple, shift),
    )
    column_representatives = orbit_representatives(
        U_TRIPLES,
        lambda triple, shift: translate_set(triple, shift),
    )
    factor_edge_representatives = orbit_representatives(
        tuple(
            (a, edge)
            for a in B_POINTS
            for edge in combinations(OUTSIDE_POINTS, 2)
        ),
        lambda item, shift: (
            (item[0] + shift) % 15,
            translate_set(item[1], shift),
        ),
    )
    pair_point_representatives = orbit_representatives(
        tuple(
            (pair, point)
            for pair in combinations(B_POINTS, 2)
            for point in OUTSIDE_POINTS
        ),
        lambda item, shift: (
            translate_set(item[0], shift),
            translate_point(item[1], shift),
        ),
    )

    model = cp_model.CpModel()
    variables = [
        model.new_bool_var(f"x_{orbit}") for orbit in range(orbit_count)
    ]

    def add_counter(counter: Counter, right_hand_side: int) -> None:
        model.add(
            sum(
                coefficient * variables[orbit]
                for orbit, coefficient in counter.items()
            )
            == right_hand_side
        )

    for a_triple in row_representatives:
        add_counter(Counter(pair_orbit[A_INDEX[a_triple]]), 32)
    for u_triple in column_representatives:
        u_index = U_INDEX[u_triple]
        add_counter(
            Counter(
                pair_orbit[a_index][u_index]
                for a_index in range(len(A_TRIPLES))
            ),
            26,
        )
    for a, edge in factor_edge_representatives:
        add_counter(
            Counter(
                pair_orbit[a_index][u_index]
                for a_index, a_triple in enumerate(A_TRIPLES)
                if a in a_triple
                for u_index, u_triple in enumerate(U_TRIPLES)
                if set(edge) <= set(u_triple)
            ),
            84 if edge in factors[a] else 72,
        )
    for pair, point in pair_point_representatives:
        add_counter(
            Counter(
                pair_orbit[a_index][u_index]
                for a_index, a_triple in enumerate(A_TRIPLES)
                if set(pair) <= set(a_triple)
                for u_index, u_triple in enumerate(U_TRIPLES)
                if point in u_triple
            ),
            78,
        )

    if include_q:
        edge_representatives = orbit_representatives(
            tuple(combinations(OUTSIDE_POINTS, 2)),
            lambda edge, shift: translate_set(edge, shift),
        )
        cross_representatives = orbit_representatives(
            tuple(
                (a, point)
                for a in B_POINTS
                for point in OUTSIDE_POINTS
            ),
            lambda item, shift: (
                (item[0] + shift) % 15,
                translate_point(item[1], shift),
            ),
        )
        inside_pair_representatives = orbit_representatives(
            tuple(combinations(B_POINTS, 2)),
            lambda pair, shift: translate_set(pair, shift),
        )
        for edge in edge_representatives:
            counter = Counter()
            for a_index in range(len(A_TRIPLES)):
                for u_index, u_triple in enumerate(U_TRIPLES):
                    q_value = q_values[a_index][u_index]
                    if set(edge) <= set(u_triple) and q_value:
                        counter[pair_orbit[a_index][u_index]] += q_value
            add_counter(counter, 252)
        for a, point in cross_representatives:
            counter = Counter()
            for a_index, a_triple in enumerate(A_TRIPLES):
                if a in a_triple:
                    continue
                for u_index, u_triple in enumerate(U_TRIPLES):
                    q_value = q_values[a_index][u_index]
                    if point in u_triple and q_value:
                        counter[pair_orbit[a_index][u_index]] += q_value
            add_counter(counter, 1512)
        for pair in inside_pair_representatives:
            counter = Counter()
            for a_index, a_triple in enumerate(A_TRIPLES):
                if set(pair) & set(a_triple):
                    continue
                for u_index in range(len(U_TRIPLES)):
                    q_value = q_values[a_index][u_index]
                    if q_value:
                        counter[pair_orbit[a_index][u_index]] += q_value
            add_counter(counter, 6336)

    metadata = {
        "factors": factors,
        "pair_orbit": pair_orbit,
        "q_values": q_values,
    }
    return model, variables, metadata


def verify_solution(values: list[int], metadata: dict, include_q: bool) -> None:
    factors = metadata["factors"]
    pair_orbit = metadata["pair_orbit"]
    q_values = metadata["q_values"]

    def selected(a_index: int, u_index: int) -> int:
        return values[pair_orbit[a_index][u_index]]

    assert all(
        sum(selected(a_index, u_index) for u_index in range(len(U_TRIPLES)))
        == 32
        for a_index in range(len(A_TRIPLES))
    )
    assert all(
        sum(selected(a_index, u_index) for a_index in range(len(A_TRIPLES)))
        == 26
        for u_index in range(len(U_TRIPLES))
    )
    for a in B_POINTS:
        for edge in combinations(OUTSIDE_POINTS, 2):
            observed = sum(
                selected(a_index, u_index)
                for a_index, a_triple in enumerate(A_TRIPLES)
                if a in a_triple
                for u_index, u_triple in enumerate(U_TRIPLES)
                if set(edge) <= set(u_triple)
            )
            assert observed == (84 if edge in factors[a] else 72)
    for pair in combinations(B_POINTS, 2):
        for point in OUTSIDE_POINTS:
            observed = sum(
                selected(a_index, u_index)
                for a_index, a_triple in enumerate(A_TRIPLES)
                if set(pair) <= set(a_triple)
                for u_index, u_triple in enumerate(U_TRIPLES)
                if point in u_triple
            )
            assert observed == 78

    if include_q:
        for edge in combinations(OUTSIDE_POINTS, 2):
            observed = sum(
                selected(a_index, u_index) * q_values[a_index][u_index]
                for a_index in range(len(A_TRIPLES))
                for u_index, u_triple in enumerate(U_TRIPLES)
                if set(edge) <= set(u_triple)
            )
            assert observed == 252
        for a in B_POINTS:
            for point in OUTSIDE_POINTS:
                observed = sum(
                    selected(a_index, u_index) * q_values[a_index][u_index]
                    for a_index, a_triple in enumerate(A_TRIPLES)
                    if a not in a_triple
                    for u_index, u_triple in enumerate(U_TRIPLES)
                    if point in u_triple
                )
                assert observed == 1512
        for pair in combinations(B_POINTS, 2):
            observed = sum(
                selected(a_index, u_index) * q_values[a_index][u_index]
                for a_index, a_triple in enumerate(A_TRIPLES)
                if not (set(pair) & set(a_triple))
                for u_index in range(len(U_TRIPLES))
            )
            assert observed == 6336

    state_counts = Counter()
    for a_index in range(len(A_TRIPLES)):
        for u_index in range(len(U_TRIPLES)):
            if selected(a_index, u_index):
                state_counts[q_values[a_index][u_index]] += 1
    assert sum(state_counts.values()) == 14_560
    print(f"q_states={dict(sorted(state_counts.items()))}")
    print(
        "tau="
        + str(
            sum(
                q * (q - 1) // 2 * count
                for q, count in state_counts.items()
            )
        )
    )
    print("independent_solution_check=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--include-q", action="store_true")
    args = parser.parse_args()

    model, variables, metadata = build_model(args.include_q)
    print(
        f"variables={len(variables)} constraints={len(model.proto.constraints)} "
        f"include_q={args.include_q}"
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    status = solver.solve(model)
    print(
        f"status={solver.status_name(status)} wall={solver.wall_time:.6f} "
        f"branches={solver.num_branches} conflicts={solver.num_conflicts}"
    )
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = [solver.value(variable) for variable in variables]
        verify_solution(values, metadata, args.include_q)
    else:
        print("NONVERDICT: only SAT or UNSAT would resolve this cyclic slice")


if __name__ == "__main__":
    main()
