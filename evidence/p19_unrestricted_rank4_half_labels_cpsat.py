#!/usr/bin/env python3
"""Exact sign-and-label search on the round-robin K_10 factorization.

Unlike ``p19_unrestricted_rank4_half_sign_cpsat.py``, this model also permits
an arbitrary bijection from the nine one-factors to the nine sign classes
{+/-1,...,+/-9}.  Thus INFEASIBLE excludes every labelling and every edge
signing of this one (unlabelled) factorization.  It still does not address the
other 395 isomorphism classes of one-factorizations of K_10.
"""

from __future__ import annotations

import argparse
import itertools

from ortools.sat.python import cp_model

from p19_unrestricted_rank4_half_sign_cpsat import (
    N,
    P,
    check_half_link,
    matrix_rank_mod,
    pfaffian_matchings,
    standard_factorization,
)


def solve(seconds: float, workers: int, seed: int) -> int:
    edge_classes = {
        edge: colour - 1
        for edge, colour in standard_factorization().items()
    }
    model = cp_model.CpModel()
    magnitudes = [
        model.new_int_var(1, 9, f"magnitude_{factor}")
        for factor in range(9)
    ]
    model.add_all_different(magnitudes)
    # Multiplying the whole alternating matrix by a nonzero field element
    # permutes the nine sign classes and preserves rank.  Normalize the class
    # of edge 01 to magnitude 1.
    model.add(magnitudes[edge_classes[(0, 1)]] == 1)

    sign_bits = {
        edge: model.new_bool_var(f"negative_{edge[0]}_{edge[1]}")
        for edge in sorted(edge_classes)
    }
    for other in range(1, N):
        model.add(sign_bits[(0, other)] == 0)

    product_cache: dict[tuple[int, int, int], cp_model.IntVar] = {}

    def magnitude_product(factors: tuple[int, int, int]) -> cp_model.IntVar:
        key = tuple(sorted(factors))
        if key in product_cache:
            return product_cache[key]
        first, second, third = key
        raw_pair = model.new_int_var(
            1, 81, "raw_pair_" + "_".join(map(str, key))
        )
        model.add_multiplication_equality(
            raw_pair, [magnitudes[first], magnitudes[second]]
        )
        raw_triple = model.new_int_var(
            1, 729, "raw_triple_" + "_".join(map(str, key))
        )
        model.add_multiplication_equality(
            raw_triple, [raw_pair, magnitudes[third]]
        )
        residue = model.new_int_var(
            1, 18, "product_mod19_" + "_".join(map(str, key))
        )
        model.add_modulo_equality(residue, raw_triple, P)
        product_cache[key] = residue
        return residue

    for subset in itertools.combinations(range(N), 6):
        signed_terms = []
        for term_index, (pfaffian_sign, matching) in enumerate(
            pfaffian_matchings(subset)
        ):
            parity = model.new_bool_var(
                "odd_" + "_".join(map(str, subset)) + f"_{term_index}"
            )
            model.add_bool_xor(
                [*(sign_bits[edge] for edge in matching), parity.negated()]
            )
            product = magnitude_product(
                tuple(edge_classes[edge] for edge in matching)
            )
            signed = model.new_int_var(
                -18, 18,
                "term_" + "_".join(map(str, subset)) + f"_{term_index}",
            )
            model.add(signed == pfaffian_sign * product).only_enforce_if(
                parity.negated()
            )
            model.add(signed == -pfaffian_sign * product).only_enforce_if(
                parity
            )
            signed_terms.append(signed)
        quotient = model.new_int_var(
            -15, 15, "q_" + "_".join(map(str, subset))
        )
        model.add(sum(signed_terms) == P * quotient)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.log_search_progress = True
    status = solver.solve(model)
    print("status:", solver.status_name(status))
    print("conflicts:", solver.num_conflicts)
    print("branches:", solver.num_branches)
    print("wall_seconds:", solver.wall_time)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return 1

    chosen_magnitudes = [solver.value(variable) for variable in magnitudes]
    matrix = [[0] * N for _ in range(N)]
    for (left, right), factor in edge_classes.items():
        magnitude = chosen_magnitudes[factor]
        value = -magnitude if solver.value(sign_bits[(left, right)]) else magnitude
        matrix[left][right] = value % P
        matrix[right][left] = -value % P
    check_half_link(matrix)
    print("factor magnitudes:", chosen_magnitudes)
    print("A = [")
    for row in matrix:
        print("  [" + ", ".join(map(str, row)) + "],")
    print("]")
    print("rank:", matrix_rank_mod(matrix, P))
    print("half-link exact verification: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=190835)
    args = parser.parse_args()
    return solve(args.seconds, args.workers, args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
