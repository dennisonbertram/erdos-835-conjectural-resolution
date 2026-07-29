#!/usr/bin/env python3
"""Exclude squarefree quotient trades on at most six cells.

A squarefree trade is a pair of disjoint cell sets P,N with

    B 1_P = B 1_N.

The verifier reconstructs the cyclic C17 quotient and exhausts supports two,
four, and six.  It uses the Q-group equations to reduce support six to three
oriented within-Q swaps.  Only the Python standard library is used.
"""

from __future__ import annotations

from collections import Counter, defaultdict

import verify_cyclic_linear_delimiter as base


def build_columns() -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    cells, groups = base.build_full_incidence()
    _equations, cell_index, group_keys = base.build_orbit_system(cells, groups)
    cell_reps = tuple(sorted(cell_index, key=cell_index.get))

    memberships: list[list[int]] = [[] for _ in cell_reps]
    for row, key in enumerate(group_keys):
        seen: set[int] = set()
        for cell in groups[key]:
            column = cell_index[base.cell_representative(cell)]
            if column not in seen:
                seen.add(column)
                memberships[column].append(row)

    q_groups: list[list[int]] = [[] for _ in range(228)]
    tc_columns: list[tuple[int, ...]] = []
    for column, rows in enumerate(memberships):
        q_rows = [row for row in rows if row < 228]
        if len(q_rows) != 1 or len(rows) != 5:
            raise AssertionError("wrong quotient column structure")
        q_groups[q_rows[0]].append(column)
        tc_columns.append(tuple(sorted(row for row in rows if row >= 228)))
    if any(len(group) != 13 for group in q_groups):
        raise AssertionError("wrong Q-group size")
    return tuple(tuple(group) for group in q_groups), tuple(tc_columns)


def verify_no_support_two(
    q_groups: tuple[tuple[int, ...], ...],
    tc_columns: tuple[tuple[int, ...], ...],
) -> None:
    for group in q_groups:
        signatures = [tc_columns[column] for column in group]
        if len(set(signatures)) != 13:
            raise AssertionError("found a two-cell trade")


def verify_no_support_four(
    q_groups: tuple[tuple[int, ...], ...],
    tc_columns: tuple[tuple[int, ...], ...],
) -> None:
    # Q-balance leaves two cases: 2+ versus 2- in one Q-group, or one
    # positive and one negative cell in each of two Q-groups.
    for group in q_groups:
        seen: dict[tuple[int, ...], tuple[int, int]] = {}
        for left_index, left in enumerate(group):
            for right in group[left_index + 1 :]:
                signature = tuple(sorted(tc_columns[left] + tc_columns[right]))
                old = seen.get(signature)
                if old is not None and not set(old) & {left, right}:
                    raise AssertionError("found a four-cell trade in one Q-group")
                seen[signature] = left, right

    for first_q, first_group in enumerate(q_groups):
        for second_group in q_groups[first_q + 1 :]:
            seen = {}
            for left in first_group:
                for right in second_group:
                    signature = tuple(sorted(tc_columns[left] + tc_columns[right]))
                    old = seen.get(signature)
                    if old is not None and set(old) != {left, right}:
                        difference = Counter(old)
                        difference.subtract((left, right))
                        if len(+difference) + len(-difference) == 4:
                            raise AssertionError(
                                "found a four-cell trade across two Q-groups"
                            )
                    seen[signature] = left, right


def verify_no_support_six(
    q_groups: tuple[tuple[int, ...], ...],
    tc_columns: tuple[tuple[int, ...], ...],
) -> tuple[int, int, int]:
    # Every 3+ versus 3- trade can pair positive and negative cells inside
    # their common Q-groups.  It is therefore a zero sum of three oriented
    # within-Q column differences.  Repeated Q-groups are allowed.
    moves: list[tuple[int, int, int, frozenset[int], frozenset[int]]] = []
    by_vector: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    positive_index: dict[int, list[int]] = defaultdict(list)
    negative_index: dict[int, list[int]] = defaultdict(list)
    support_histogram: Counter[int] = Counter()

    tc_sets = tuple(frozenset(column) for column in tc_columns)
    for q_group, columns in enumerate(q_groups):
        for positive in columns:
            for negative in columns:
                if positive == negative:
                    continue
                positive_rows = tc_sets[positive] - tc_sets[negative]
                negative_rows = tc_sets[negative] - tc_sets[positive]
                move = len(moves)
                moves.append(
                    (
                        q_group,
                        positive,
                        negative,
                        positive_rows,
                        negative_rows,
                    )
                )
                vector = (
                    tuple(sorted(positive_rows)),
                    tuple(sorted(negative_rows)),
                )
                if vector in by_vector:
                    raise AssertionError("duplicate swap vector gives a smaller trade")
                by_vector[vector] = move
                support_histogram[len(positive_rows) + len(negative_rows)] += 1
                for row in positive_rows:
                    positive_index[row].append(move)
                for row in negative_rows:
                    negative_index[row].append(move)

    if support_histogram != Counter({8: 34_910, 6: 658}):
        raise AssertionError(f"unexpected swap support census: {support_histogram}")

    algebraic_completion_hits = 0
    genuine_support_six = 0
    for first, (
        _first_q,
        first_positive,
        first_negative,
        first_positive_rows,
        first_negative_rows,
    ) in enumerate(moves):
        candidates: Counter[int] = Counter()
        for row in first_positive_rows:
            candidates.update(negative_index[row])
        for row in first_negative_rows:
            candidates.update(positive_index[row])

        for second, cancellation_count in candidates.items():
            if second <= first:
                continue
            (
                _second_q,
                second_positive,
                second_negative,
                second_positive_rows,
                second_negative_rows,
            ) = moves[second]

            # A third swap has coefficients only +/-1.  Same-sign overlap
            # would create an uncancellable coefficient +/-2.
            if (
                first_positive_rows & second_positive_rows
                or first_negative_rows & second_negative_rows
            ):
                continue
            residual_support = (
                len(first_positive_rows)
                + len(first_negative_rows)
                + len(second_positive_rows)
                + len(second_negative_rows)
                - 2 * cancellation_count
            )
            if residual_support not in (6, 8):
                continue

            residual_positive = (first_positive_rows | second_positive_rows) - (
                first_negative_rows | second_negative_rows
            )
            residual_negative = (first_negative_rows | second_negative_rows) - (
                first_positive_rows | second_positive_rows
            )
            third = by_vector.get(
                (
                    tuple(sorted(residual_negative)),
                    tuple(sorted(residual_positive)),
                )
            )
            if third is None:
                continue
            algebraic_completion_hits += 1

            cell_coefficients: dict[int, int] = defaultdict(int)
            for move in (first, second, third):
                _q_group, positive, negative, _positive_rows, _negative_rows = moves[
                    move
                ]
                cell_coefficients[positive] += 1
                cell_coefficients[negative] -= 1
            signed = {cell: value for cell, value in cell_coefficients.items() if value}
            if len(signed) == 6 and sorted(signed.values()) == [-1, -1, -1, 1, 1, 1]:
                genuine_support_six += 1

    if genuine_support_six:
        raise AssertionError("found a squarefree six-cell trade")
    return len(moves), algebraic_completion_hits, genuine_support_six


def main() -> None:
    q_groups, tc_columns = build_columns()
    verify_no_support_two(q_groups, tc_columns)
    verify_no_support_four(q_groups, tc_columns)
    moves, algebraic_completion_hits, genuine_support_six = verify_no_support_six(
        q_groups,
        tc_columns,
    )
    print("cyclic quotient small-trade audit: PASS")
    print("squarefree trade support 2: none")
    print("squarefree trade support 4: none")
    print("oriented within-Q swaps:", moves)
    print("algebraic zero-sum pair-completion hits:", algebraic_completion_hits)
    print("squarefree trade support 6:", genuine_support_six)
    print("theorem: every nonzero squarefree trade has support at least 8")
    print("scope: this does not construct or exclude an exact cover or fan")


if __name__ == "__main__":
    main()
