#!/usr/bin/env python3
"""Independent audit of the exact C17-invariant single-matching attack."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

from verify_cyclic_cnf_audit import (
    build_quotient,
    construct_link,
    shift_block,
    validate_link,
)


PHASE_VARIABLES = 3_876
ALLOWED_ROWS = 2_964
GROUPS = 1_140
Q_GROUPS = 228
TC_GROUPS = 912
MODULUS = 17
LABELS = 13


def read_exact_matrix(
    path: Path,
) -> tuple[dict[int, tuple[int, ...]], tuple[tuple[int, ...], ...]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != "p exact 1140 2964":
        raise AssertionError("unexpected exact-cover matrix header")
    rows: dict[int, tuple[int, ...]] = {}
    columns: list[list[int]] = [[] for _ in range(GROUPS)]
    for line in lines[1:]:
        values = tuple(map(int, line.split()))
        if len(values) != 6:
            raise AssertionError("matrix row does not have degree five")
        label, covered = values[0], values[1:]
        if label in rows or label not in range(1, PHASE_VARIABLES + 1):
            raise AssertionError("invalid or duplicate matrix row label")
        if len(set(covered)) != 5 or any(
            column not in range(GROUPS) for column in covered
        ):
            raise AssertionError("invalid exact-cover columns")
        rows[label] = covered
        for column in covered:
            columns[column].append(label)
    if len(rows) != ALLOWED_ROWS:
        raise AssertionError("wrong exact-cover row count")
    if {len(column) for column in columns} != {13}:
        raise AssertionError("each exact-cover column should contain thirteen rows")
    if {sum(label in column for column in columns) for label in rows} != {5}:
        raise AssertionError("each allowed row should occur in five columns")
    return rows, tuple(tuple(sorted(column)) for column in columns)


def diagonal_cell_representative(
    cell: tuple[tuple[int, int, int, int], int],
) -> tuple[tuple[int, int, int, int], int]:
    quad, colour = cell
    return min(
        (shift_block(quad, amount), (colour + amount) % MODULUS)
        for amount in range(MODULUS)
    )


def diagonal_tc_representative(
    item: tuple[tuple[int, int, int], int],
) -> tuple[tuple[int, int, int], int]:
    triple, colour = item
    return min(
        (shift_block(triple, amount), (colour + amount) % MODULUS)
        for amount in range(MODULUS)
    )


def compare_matrix_to_quotient(
    matrix_columns: tuple[tuple[int, ...], ...],
) -> tuple[
    dict[tuple[tuple[int, int, int, int], int], int],
    tuple[tuple[tuple[int, int, int, int], int], ...],
    tuple[tuple[int, ...], ...],
    dict[tuple[int, int, int], int],
]:
    link = construct_link()
    validate_link(link)
    cells, groups = build_quotient(link)
    block_representatives = tuple(sorted({quad for quad, _colour in cells}))
    if len(block_representatives) != Q_GROUPS:
        raise AssertionError("wrong independent block-orbit count")
    block_number = {
        representative: number
        for number, representative in enumerate(block_representatives)
    }
    label_for_cell = {
        cell: MODULUS * block_number[cell[0]] + cell[1] + 1 for cell in cells
    }
    reconstructed = tuple(
        tuple(sorted(label_for_cell[cells[cell]] for cell in group))
        for group in groups
    )
    if reconstructed != matrix_columns:
        raise AssertionError(
            "canonical exact-cover matrix differs from independent quotient"
        )
    return label_for_cell, cells, groups, link


def audit_matrix_row_bridge(
    rows: dict[int, tuple[int, ...]],
    label_for_cell: dict[tuple[tuple[int, int, int, int], int], int],
    cells: tuple[tuple[tuple[int, int, int, int], int], ...],
    groups: tuple[tuple[int, ...], ...],
) -> None:
    matrix_label = {
        tuple(sorted(columns)): label for label, columns in rows.items()
    }
    if len(matrix_label) != ALLOWED_ROWS:
        raise AssertionError("matrix incidence signatures are not unique")
    incidence: list[list[int]] = [[] for _ in cells]
    for group_number, group in enumerate(groups):
        for cell in group:
            incidence[cell].append(group_number)
    for cell_number, cell in enumerate(cells):
        signature = tuple(sorted(incidence[cell_number]))
        if matrix_label.get(signature) != label_for_cell[cell]:
            raise AssertionError("cell-index to matrix-row bridge changes a row label")


def parse_dimacs(path: Path) -> tuple[int, tuple[tuple[int, ...], ...], str]:
    content = path.read_bytes()
    lines = content.decode("ascii").splitlines()
    header = lines[0].split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise AssertionError("invalid DIMACS header")
    variables, declared = map(int, header[2:])
    clauses = []
    for line in lines[1:]:
        values = tuple(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise AssertionError("invalid DIMACS clause")
        clause = values[:-1]
        if any(abs(literal) not in range(1, variables + 1) for literal in clause):
            raise AssertionError("DIMACS literal outside declared range")
        clauses.append(clause)
    if len(clauses) != declared:
        raise AssertionError("DIMACS clause count mismatch")
    return variables, tuple(clauses), hashlib.sha256(content).hexdigest()


def audit_cover_cnf(
    cnf_path: Path,
    map_path: Path,
    matrix_columns: tuple[tuple[int, ...], ...],
) -> tuple[str, str, Counter[int]]:
    variables, clauses, digest = parse_dimacs(cnf_path)
    if (variables, len(clauses)) != (PHASE_VARIABLES, 33_060):
        raise AssertionError("wrong cover-CNF dimensions")
    lengths = Counter(map(len, clauses))
    if lengths != Counter({2: 31_008, 1: 912, 16: 912, 17: 228}):
        raise AssertionError(f"unexpected cover-CNF clause census: {lengths}")

    offset = 0
    for orbit in range(Q_GROUPS):
        phase_variables = tuple(
            MODULUS * orbit + colour + 1 for colour in range(MODULUS)
        )
        if clauses[offset] != phase_variables:
            raise AssertionError("wrong block-orbit at-least-one clause")
        offset += 1
        expected_pairs = tuple(
            (-left, -right) for left, right in combinations(phase_variables, 2)
        )
        if clauses[offset : offset + len(expected_pairs)] != expected_pairs:
            raise AssertionError("wrong block-orbit pairwise clauses")
        offset += len(expected_pairs)
    tail = clauses[offset:]
    units = {-clause[0] for clause in tail if len(clause) == 1}
    coverage = [clause for clause in tail if len(clause) == 16]
    allowed = set().union(*map(set, matrix_columns[:Q_GROUPS]))
    if units != set(range(1, PHASE_VARIABLES + 1)) - allowed:
        raise AssertionError("unit clauses are not exactly the 912 forbidden phases")
    reduced_coverage = Counter(
        frozenset(literal for literal in clause if literal not in units)
        for clause in coverage
    )
    expected_tc = Counter(
        frozenset(group) for group in matrix_columns[Q_GROUPS:]
    )
    if reduced_coverage != expected_tc:
        raise AssertionError("coverage clauses do not reduce to the 912 TC groups")

    mapping = json.loads(map_path.read_text(encoding="ascii"))
    if mapping.get("encoding") != "cover":
        raise AssertionError("map does not identify the cover encoding")
    if mapping.get("cnf_sha256") != digest:
        raise AssertionError("map CNF digest mismatch")
    map_digest = hashlib.sha256(map_path.read_bytes()).hexdigest()
    return digest, map_digest, lengths


def independent_formula_labels(
    link: dict[tuple[int, int, int], int],
    cells: tuple[tuple[tuple[int, int, int, int], int], ...],
    blend: int,
    multiplier: int,
) -> tuple[int, ...]:
    labels = []
    for quad, colour in cells:
        finite = [point for point in quad if point < MODULUS]
        point_mean = sum(finite) * pow(len(finite), -1, MODULUS) % MODULUS
        face_colours = {link[face] for face in combinations(quad, 3)}
        face_mean = sum(face_colours) * pow(4, -1, MODULUS) % MODULUS
        anchor = (blend * point_mean + (1 - blend) * face_mean) % MODULUS
        ordered = sorted(
            set(range(MODULUS)) - face_colours,
            key=lambda value: multiplier * (value - anchor) % MODULUS,
        )
        labels.append(ordered.index(colour))
    return tuple(labels)


def collision_score(
    labels: tuple[int, ...],
    groups: tuple[tuple[int, ...], ...],
) -> int:
    score = 0
    for group in groups:
        counts = Counter(labels[cell] for cell in group)
        score += sum(count * (count - 1) // 2 for count in counts.values())
    return score


def audit_formula_screen(
    link: dict[tuple[int, int, int], int],
    cells: tuple[tuple[tuple[int, int, int, int], int], ...],
    groups: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int, int], tuple[int, int, int, int], int, int]:
    target = set(range(LABELS))
    best_fan: tuple[int, int, int] | None = None
    best_matching: tuple[int, int, int, int] | None = None
    fan_digests = set()
    matching_digests = set()
    for blend in range(MODULUS):
        for multiplier in range(1, MODULUS):
            labels = independent_formula_labels(
                link, cells, blend, multiplier
            )
            if any(
                {labels[cell] for cell in group} != target
                for group in groups[:Q_GROUPS]
            ):
                raise AssertionError("formula is not Q-rainbow")
            fan_digests.add(hashlib.sha256(bytes(labels)).digest())
            candidate = (
                collision_score(labels, groups[Q_GROUPS:]),
                blend,
                multiplier,
            )
            if best_fan is None or candidate < best_fan:
                best_fan = candidate
            for label in range(LABELS):
                selected = tuple(
                    int(value == label) for value in labels
                )
                matching_digests.add(hashlib.sha256(bytes(selected)).digest())
                score = 0
                for group in groups[Q_GROUPS:]:
                    count = sum(selected[cell] for cell in group)
                    score += count * (count - 1) // 2
                match_candidate = score, blend, multiplier, label
                if best_matching is None or match_candidate < best_matching:
                    best_matching = match_candidate
    if best_fan != (4_098, 1, 2):
        raise AssertionError(f"unexpected formula-screen optimum {best_fan}")
    if best_matching != (237, 1, 8, 12):
        raise AssertionError(f"unexpected matching-screen optimum {best_matching}")
    if len(fan_digests) != 272 or len(matching_digests) != 3_536:
        raise AssertionError("formula screen contains duplicate candidates")
    return best_fan, best_matching, len(fan_digests), len(matching_digests)


def audit_structural_delimiters(
    label_for_cell: dict[tuple[tuple[int, int, int, int], int], int],
    cells: tuple[tuple[tuple[int, int, int, int], int], ...],
    groups: tuple[tuple[int, ...], ...],
    link: dict[tuple[int, int, int], int],
) -> None:
    cell_number = {cell: number for number, cell in enumerate(cells)}
    witness_cells = (
        ((0, 1, 2, 3), 0),
        ((0, 1, 2, 6), 0),
        ((0, 1, 3, 6), 0),
    )
    witness_indices = tuple(
        cell_number[diagonal_cell_representative(cell)] for cell in witness_cells
    )
    tc_items = (
        ((0, 1, 2), 0),
        ((0, 1, 3), 0),
        ((0, 1, 6), 0),
    )
    all_tc = (
        (triple, colour)
        for triple in combinations(range(19), 3)
        for colour in range(MODULUS)
        if colour != link[triple]
    )
    tc_representatives = tuple(
        sorted({diagonal_tc_representative(item) for item in all_tc})
    )
    tc_number = {
        item: Q_GROUPS + number
        for number, item in enumerate(tc_representatives)
    }
    matrix = tuple(
        tuple(
            int(cell in groups[tc_number[diagonal_tc_representative(item)]])
            for cell in witness_indices
        )
        for item in tc_items
    )
    if matrix != ((1, 1, 0), (1, 0, 1), (0, 1, 1)):
        raise AssertionError("strong odd-cycle witness does not descend to quotient")

    odd_hole = (
        ((0, 1, 2, 3), 0),
        ((0, 1, 2, 4), 0),
        ((0, 1, 4, 6), 0),
        ((0, 1, 6, 8), 0),
        ((0, 1, 3, 8), 0),
    )
    hole_indices = tuple(
        cell_number[diagonal_cell_representative(cell)] for cell in odd_hole
    )
    group_sets = tuple(set(group) for group in groups)
    for left, right in combinations(range(5), 2):
        adjacent = any(
            hole_indices[left] in group and hole_indices[right] in group
            for group in group_sets
        )
        distance = min(right - left, 5 - (right - left))
        if adjacent != (distance == 1):
            raise AssertionError("displayed odd hole is not induced in quotient")
    if len(set(label_for_cell.values())) != ALLOWED_ROWS:
        raise AssertionError("cell-to-phase map is not injective")


def audit_direct_cnf(
    path: Path,
    matrix_columns: tuple[tuple[int, ...], ...],
) -> str:
    variables, clauses, digest = parse_dimacs(path)
    if (variables, len(clauses)) != (PHASE_VARIABLES, 90_060):
        raise AssertionError("wrong direct exact-cover CNF dimensions")
    position = 0
    for group in matrix_columns:
        if clauses[position] != group:
            raise AssertionError("direct CNF has wrong group coverage clause")
        position += 1
        expected = tuple(
            (-left, -right) for left, right in combinations(group, 2)
        )
        if clauses[position : position + len(expected)] != expected:
            raise AssertionError("direct CNF has wrong group AMO clauses")
        position += len(expected)
    if position != len(clauses):
        raise AssertionError("direct CNF has trailing clauses")
    return digest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--cover-cnf", type=Path, required=True)
    parser.add_argument("--cover-map", type=Path, required=True)
    parser.add_argument("--direct-cnf", type=Path)
    args = parser.parse_args()

    rows, matrix_columns = read_exact_matrix(args.matrix)
    label_for_cell, cells, groups, link = compare_matrix_to_quotient(
        matrix_columns
    )
    audit_matrix_row_bridge(rows, label_for_cell, cells, groups)
    cover_digest, map_digest, lengths = audit_cover_cnf(
        args.cover_cnf, args.cover_map, matrix_columns
    )
    best_fan, best_matching, fan_count, matching_count = audit_formula_screen(
        link, cells, groups
    )
    audit_structural_delimiters(
        label_for_cell, cells, groups, link
    )
    direct_digest = (
        audit_direct_cnf(args.direct_cnf, matrix_columns)
        if args.direct_cnf is not None
        else "NOT_CHECKED"
    )

    print("invariant matching attack audit: PASS")
    print(
        f"exact_matrix_rows={len(rows)} columns={len(matrix_columns)} "
        "row_degree=5 column_size=13"
    )
    print("identity=pre-existing C17-equivariant LS(3,4,20) exact-cover instance")
    print("full_cell_index_to_matrix_row_bijection=PASS")
    print(f"cover_cnf_sha256={cover_digest}")
    print(f"cover_map_sha256={map_digest}")
    print(
        "cover_clause_lengths="
        + ",".join(f"{length}:{count}" for length, count in sorted(lengths.items()))
    )
    print("cover_encoding_auxiliaries=0 forbidden_phase_units=912")
    print(
        f"formulae={fan_count} best_fan={best_fan} "
        f"matching_candidates={matching_count} best_matching={best_matching}"
    )
    print("strong_odd_cycle_and_induced_C5_descend_to_quotient=PASS")
    print(f"direct_exact_cover_cnf_sha256={direct_digest}")
    print("scope=no matching found; every UNKNOWN remains inconclusive")


if __name__ == "__main__":
    main()
