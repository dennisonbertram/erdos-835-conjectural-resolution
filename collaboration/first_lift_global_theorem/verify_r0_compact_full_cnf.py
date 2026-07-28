#!/usr/bin/env python3
"""Independently audit the compact exceptional-profile full CNF.

The small exhaustive tests check that the custom signed-cardinality and
lexicographic encodings have exactly their documented projections.  The
optional DIMACS scan checks structural integrity.  If CaDiCaL returns a SAT
witness, ``--witness`` validates the mathematical object directly, without
trusting any auxiliary CNF variables.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory

import write_r0_compact_full_cnf as compact


def read_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = -1
    clauses: list[tuple[int, ...]] = []
    with path.open("r", encoding="ascii") as handle:
        for line in handle:
            if line.startswith("c") or not line.strip():
                continue
            if line.startswith("p"):
                _, kind, variable_text, clause_text = line.split()
                assert kind == "cnf"
                variables = int(variable_text)
                expected_clauses = int(clause_text)
                continue
            values = tuple(map(int, line.split()))
            assert values[-1] == 0
            clauses.append(values[:-1])
    assert variables >= 0
    assert len(clauses) == expected_clauses
    assert all(abs(literal) <= variables for clause in clauses for literal in clause)
    return variables, clauses


def clauses_hold(
    clauses: list[tuple[int, ...]],
    assignment: dict[int, bool],
) -> bool:
    return all(
        any(assignment[abs(literal)] == (literal > 0) for literal in clause)
        for clause in clauses
    )


def projected_satisfiable(
    variables: int,
    clauses: list[tuple[int, ...]],
    primary: dict[int, bool],
) -> bool:
    auxiliary = [
        variable for variable in range(1, variables + 1) if variable not in primary
    ]
    for values in product((False, True), repeat=len(auxiliary)):
        assignment = dict(primary)
        assignment.update(zip(auxiliary, values))
        if clauses_hold(clauses, assignment):
            return True
    return False


def audit_cardinality_projection() -> None:
    with TemporaryDirectory(prefix="r0-compact-card-") as directory:
        path = Path(directory) / "card.cnf"
        writer = compact.Writer(path)
        a, b, c = writer.variables_block(3)
        writer.exactly([a, -b, c], 2)
        writer.finish()
        variables, clauses = read_cnf(path)

    for av, bv, cv in product((False, True), repeat=3):
        primary = {a: av, b: bv, c: cv}
        observed = projected_satisfiable(variables, clauses, primary)
        expected = sum((av, not bv, cv)) == 2
        assert observed == expected, (primary, observed, expected)
    print("PASS signed exact-cardinality projection")


def audit_gated_cardinality_projection() -> None:
    with TemporaryDirectory(prefix="r0-compact-gated-card-") as directory:
        path = Path(directory) / "gated-card.cnf"
        writer = compact.Writer(path)
        gate, a, b = writer.variables_block(3)
        writer.exactly([a, b], 1, gate=gate)
        writer.finish()
        variables, clauses = read_cnf(path)

    for gate_value, av, bv in product((False, True), repeat=3):
        primary = {gate: gate_value, a: av, b: bv}
        observed = projected_satisfiable(variables, clauses, primary)
        expected = not gate_value or sum((av, bv)) == 1
        assert observed == expected, (primary, observed, expected)
    print("PASS gated exact-cardinality projection")


def audit_lex_projection() -> None:
    with TemporaryDirectory(prefix="r0-compact-lex-") as directory:
        path = Path(directory) / "lex.cnf"
        writer = compact.Writer(path)
        left = writer.variables_block(3)
        right = writer.variables_block(3)
        writer.lex_not_greater(left, right)
        writer.finish()
        variables, clauses = read_cnf(path)

    for left_values in product((False, True), repeat=3):
        for right_values in product((False, True), repeat=3):
            primary = {
                **dict(zip(left, left_values)),
                **dict(zip(right, right_values)),
            }
            observed = projected_satisfiable(variables, clauses, primary)
            left_number = sum(value << index for index, value in enumerate(left_values))
            right_number = sum(
                value << index for index, value in enumerate(right_values)
            )
            expected = left_number <= right_number
            assert observed == expected, (primary, observed, expected)
    print("PASS lexicographic projection")


def audit_matching_enumeration() -> None:
    assert len(compact.TRIPLES) == 286
    for triple in compact.TRIPLES:
        support = tuple(vertex for vertex in compact.VERTICES if vertex not in triple)
        matchings = compact.perfect_matchings(support)
        assert len(matchings) == 945
        assert len(set(matchings)) == 945
        for matching in matchings:
            assert len(matching) == 5
            endpoints = [
                vertex
                for edge_index in matching
                for vertex in compact.EDGES[edge_index]
            ]
            assert len(set(endpoints)) == 10
            assert set(endpoints) == set(support)
    print("PASS 286 supports each have exactly 945 enumerated perfect matchings")


def scan_dimacs(path: Path) -> None:
    digest = hashlib.sha256()
    header_variables = -1
    header_clauses = -1
    observed_clauses = 0
    with path.open("rb") as handle:
        for raw_line in handle:
            digest.update(raw_line)
            line = raw_line.strip()
            if not line or line.startswith(b"c"):
                continue
            if line.startswith(b"p"):
                _, kind, variables, clauses = line.split()
                assert kind == b"cnf"
                header_variables = int(variables)
                header_clauses = int(clauses)
                continue
            values = tuple(map(int, line.split()))
            assert values[-1] == 0
            assert all(0 < abs(literal) <= header_variables for literal in values[:-1])
            observed_clauses += 1
    assert observed_clauses == header_clauses
    print(
        "PASS DIMACS",
        f"variables={header_variables}",
        f"clauses={header_clauses}",
        f"sha256={digest.hexdigest()}",
    )


def positive_witness(path: Path) -> set[int]:
    positive: set[int] = set()
    saw_sat = False
    for token in path.read_text(encoding="ascii").split():
        if token in {"SATISFIABLE", "SAT"}:
            saw_sat = True
        elif token.lstrip("-").isdigit() and int(token) > 0:
            positive.add(int(token))
    assert saw_sat
    return positive


def audit_witness(path: Path) -> None:
    positive = positive_witness(path)
    cursor = 1
    f = list(range(cursor, cursor + len(compact.EDGES)))
    cursor += len(compact.EDGES)
    x = []
    for _ in range(7):
        x.append(list(range(cursor, cursor + len(compact.EDGES))))
        cursor += len(compact.EDGES)
    triples = []
    for _ in range(7):
        triples.append(list(range(cursor, cursor + compact.N)))
        cursor += compact.N
    fives = []
    for _ in range(3):
        fives.append(list(range(cursor, cursor + compact.N)))
        cursor += compact.N

    selected_matchings: list[set[int]] = []
    selected_union: set[int] = set()
    for colour in range(7):
        matching = {
            edge for edge, variable in enumerate(x[colour]) if variable in positive
        }
        assert len(matching) == (4 if colour < 4 else 5)
        endpoints = [
            vertex
            for edge in matching
            for vertex in compact.EDGES[edge]
        ]
        assert len(endpoints) == len(set(endpoints))
        assert selected_union.isdisjoint(matching)
        selected_union.update(matching)
        selected_matchings.append(matching)
    assert selected_union == {
        edge for edge, variable in enumerate(f) if variable in positive
    }

    canonical = {
        compact.EDGE_INDEX[(0, 1)],
        compact.EDGE_INDEX[(2, 3)],
        compact.EDGE_INDEX[(4, 5)],
        compact.EDGE_INDEX[(6, 7)],
    }
    assert selected_matchings[0] == canonical

    complement_triples = [
        tuple(vertex for vertex, variable in enumerate(row) if variable in positive)
        for row in triples
    ]
    complement_fives = [
        tuple(vertex for vertex, variable in enumerate(row) if variable in positive)
        for row in fives
    ]
    assert all(len(row) == 3 for row in complement_triples)
    assert all(len(row) == 5 for row in complement_fives)

    def bit_number(row: tuple[int, ...]) -> int:
        return sum(1 << vertex for vertex in row)

    assert list(map(bit_number, complement_triples)) == sorted(
        map(bit_number, complement_triples)
    )
    assert list(map(bit_number, complement_fives)) == sorted(
        map(bit_number, complement_fives)
    )

    for vertex in compact.VERTICES:
        degree = sum(vertex in compact.EDGES[edge] for edge in selected_union)
        omissions = sum(vertex in row for row in complement_triples)
        omissions += sum(vertex in row for row in complement_fives)
        assert omissions == degree - 2

    for triple in complement_triples:
        support = tuple(
            vertex for vertex in compact.VERTICES if vertex not in triple
        )
        assert all(
            not selected_union.isdisjoint(matching)
            for matching in compact.perfect_matchings(support)
        )
    print("PASS SAT witness is a direct totally blocked seven-prefix")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--witness", type=Path)
    args = parser.parse_args()

    audit_cardinality_projection()
    audit_gated_cardinality_projection()
    audit_lex_projection()
    audit_matching_enumeration()
    if args.cnf:
        scan_dimacs(args.cnf)
    if args.witness:
        audit_witness(args.witness)
    print(
        "SCOPE: encoding audit only; terminal SAT or replay-checked UNSAT "
        "is required for the eighth-matching lemma"
    )


if __name__ == "__main__":
    main()
