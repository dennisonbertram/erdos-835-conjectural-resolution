#!/usr/bin/env python3
"""Emit a compact CNF for compatibility of stored phase-row families.

Each input file is a concatenation of 40-byte rows.  The CNF selects exactly
one row per family and requires every selected pair to disagree in all forty
coordinates.  For each unordered family pair it uses a one-direction support
encoding: selecting a row on the source side forces the selected row on the
other side to belong to its complete compatibility list.
"""

import sys
from pathlib import Path


def sequential_amo(literals, next_variable, clauses):
    if len(literals) <= 1:
        return next_variable
    auxiliaries = list(
        range(next_variable, next_variable + len(literals) - 1)
    )
    next_variable += len(literals) - 1
    clauses.append((-literals[0], auxiliaries[0]))
    for index in range(1, len(literals) - 1):
        clauses.append((-literals[index], auxiliaries[index]))
        clauses.append((-auxiliaries[index - 1], auxiliaries[index]))
        clauses.append((-literals[index], -auxiliaries[index - 1]))
    clauses.append((-literals[-1], -auxiliaries[-1]))
    return next_variable


def main():
    if len(sys.argv) < 4:
        raise SystemExit(
            f"usage: {sys.argv[0]} OUTPUT.cnf FAMILY.bin FAMILY.bin ..."
        )
    output = Path(sys.argv[1])
    families = []
    for argument in sys.argv[2:]:
        raw = Path(argument).read_bytes()
        assert raw and len(raw) % 40 == 0
        rows = [
            raw[offset : offset + 40]
            for offset in range(0, len(raw), 40)
        ]
        assert len(set(rows)) == len(rows)
        assert all(all(phase <= 16 for phase in row) for row in rows)
        families.append(rows)

    row_variables = []
    next_variable = 1
    for family in families:
        variables = list(
            range(next_variable, next_variable + len(family))
        )
        row_variables.append(variables)
        next_variable += len(family)
    primary_variables = next_variable - 1

    clauses = []
    for variables in row_variables:
        clauses.append(tuple(variables))
        next_variable = sequential_amo(
            variables, next_variable, clauses
        )

    support_clauses = 0
    support_literals = 0
    for left in range(len(families)):
        for right in range(left + 1, len(families)):
            if len(families[left]) <= len(families[right]):
                source, target = left, right
            else:
                source, target = right, left
            target_rows = families[target]
            target_variables = row_variables[target]
            for source_row, source_variable in zip(
                families[source], row_variables[source]
            ):
                supported = [
                    variable
                    for target_row, variable in zip(
                        target_rows, target_variables
                    )
                    if all(
                        left_phase != right_phase
                        for left_phase, right_phase in zip(
                            source_row, target_row
                        )
                    )
                ]
                clause = tuple([-source_variable, *supported])
                clauses.append(clause)
                support_clauses += 1
                support_literals += len(clause)

    variable_count = next_variable - 1
    with output.open("w", encoding="ascii") as stream:
        stream.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")

    print(
        f"families={len(families)} rows={primary_variables} "
        f"vars={variable_count} clauses={len(clauses)} "
        f"support_clauses={support_clauses} "
        f"support_literals={support_literals} file={output}"
    )


if __name__ == "__main__":
    main()
