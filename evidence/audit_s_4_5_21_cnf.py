#!/usr/bin/env python3
"""Independent structural audit for ``s_4_5_21_cnf.py``.

It checks each of the seven normalized S(4,5,21) cases against both the
direct combinatorial formulation and the CP-SAT formulation, then parses the
emitted DIMACS line by line.  It deliberately has no SAT solver dependency:
this is an encoding audit, not a search.
"""

from __future__ import annotations

import json
import tempfile
from collections import Counter
from itertools import combinations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from search_s_4_5_21_extension import (
    SECOND_LINK_CYCLE_TYPES,
    build_model,
)
from evidence.s_4_5_21_cnf import write_instance


POINTS = tuple(range(21))
ANCHOR = (0, 1, 2, 3, 4)
PAIRS = tuple((point, point + 1) for point in range(5, 21, 2))


def expected_fixed(cycles: tuple[int, ...]) -> set[tuple[int, ...]]:
    answer = {ANCHOR}
    answer |= {(0, 1, 2, left, right) for left, right in PAIRS}
    cursor = 0
    for length in cycles:
        indices = list(range(cursor, cursor + length))
        for index, next_index in zip(indices, indices[1:] + indices[:1]):
            answer.add(tuple(sorted((0, 1, 3, PAIRS[index][1], PAIRS[next_index][0]))))
        cursor += length
    assert len(answer) == 17
    return answer


def expected_blocks() -> list[tuple[int, ...]]:
    anchor = set(ANCHOR)
    return [
        block for block in combinations(POINTS, 5)
        if len(set(block) & anchor) <= 3 or block == ANCHOR
    ]


def expected_rows(blocks: list[tuple[int, ...]]) -> list[list[int]]:
    by_four = {four: [] for four in combinations(POINTS, 4)}
    for variable, block in enumerate(blocks, 1):
        for four in combinations(block, 4):
            by_four[four].append(variable)
    return list(by_four.values())


def read_clauses(path: Path) -> tuple[int, int, list[tuple[int, ...]]]:
    variables = clauses = None
    actual: list[tuple[int, ...]] = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line[0] == "c":
            continue
        if line.startswith("p "):
            _, kind, variables_text, clauses_text = line.split()
            assert kind == "cnf"
            variables, clauses = int(variables_text), int(clauses_text)
            continue
        literals = tuple(map(int, line.split()))
        assert literals[-1] == 0
        actual.append(literals[:-1])
    assert variables is not None and clauses is not None
    assert len(actual) == clauses
    return variables, clauses, actual


def audit_case(cycles: tuple[int, ...], directory: Path) -> None:
    cnf = directory / ("-".join(map(str, cycles)) + ".cnf")
    mapping = directory / ("-".join(map(str, cycles)) + ".json")
    write_instance(cycles, cnf, mapping)

    blocks = expected_blocks()
    rows = expected_rows(blocks)
    assert len(blocks) == 20269
    assert len(rows) == 5985
    assert {len(row) for row in rows} == {1, 15, 17}
    assert sum(len(row) for row in rows) == 5 * len(blocks)
    assert sum(len(row) == 1 for row in rows) == 5
    assert sum(len(row) == 15 for row in rows) == 160
    assert sum(len(row) == 17 for row in rows) == 5820

    fixed = expected_fixed(cycles)
    metadata = json.loads(mapping.read_text(encoding="utf-8"))
    assert [tuple(block) for block in metadata["variables"]] == blocks
    assert tuple(metadata["cycles"]) == cycles
    assert {tuple(block) for block in metadata["fixed"]} == fixed

    variables, clauses, actual = read_clauses(cnf)
    units = [blocks.index(block) + 1 for block in sorted(fixed)]
    expected_count = len(units) + sum(1 + len(row) * (len(row) - 1) // 2 for row in rows)
    assert variables == len(blocks)
    assert clauses == expected_count == metadata["clauses"] == 814322
    offset = 0
    assert actual[:len(units)] == [(unit,) for unit in units]
    offset += len(units)
    for row in rows:
        assert actual[offset] == tuple(row)
        offset += 1
        for left, right in combinations(row, 2):
            assert actual[offset] == (-left, -right)
            offset += 1
    assert offset == len(actual)

    # Cross-check every allowed variable, exact-one row, and normalization unit
    # against the independently implemented CP-SAT encoding.
    model, cp_variables, cp_fixed = build_model(False, True, cycles)
    assert not cp_fixed
    assert list(cp_variables) == blocks
    proto = model.Proto()
    cp_rows = Counter(
        tuple(sorted(literal + 1 for literal in constraint.exactly_one.literals))
        for constraint in proto.constraints
        if constraint.has_exactly_one()
    )
    assert cp_rows == Counter(tuple(row) for row in rows)
    cp_units = {
        constraint.linear.vars[0]
        for constraint in proto.constraints
        if constraint.has_linear()
        and list(constraint.linear.coeffs) == [1]
        and list(constraint.linear.domain) == [1, 1]
    }
    assert cp_units == {blocks.index(block) for block in fixed}
    assert sum(cp_rows.values()) == len(rows) and len(cp_units) == len(units)
    print(f"PASS {cycles}: {variables} variables, {clauses} clauses")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="s4521-cnf-audit-") as temporary:
        directory = Path(temporary)
        for cycles in SECOND_LINK_CYCLE_TYPES:
            audit_case(cycles, directory)
    print("CNF/CP-SAT structural equivalence: PASS")
    print("Decoder note: a genuine SAT model still requires a separate run of decode().")


if __name__ == "__main__":
    main()
