#!/usr/bin/env python3
"""Reconstruct and verify the portable k=6 fan UNSAT certificate.

The checker uses only the Python standard library.  It reconstructs the exact
CNF from the mathematical incidence structure, validates the committed DRAT
file's digest, and checks every proof addition by reverse unit propagation
(RUP).  The certificate contains no RAT-only step.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path

from search_k6_fan import build_cnf, build_control


HERE = Path(__file__).resolve().parent
PROOF = HERE / "k6_fan.drat"
EXPECTED_CNF_SHA256 = "693e66c10202be59ab8eba2af350b6d9d2ca0d8a438a4c98c5929804e4112a6b"
EXPECTED_PROOF_SHA256 = (
    "45c46fa6da412ff716bf8825e5e2daa125c9dfbf927affd377157d3b4807ffb9"
)


Clause = tuple[int, ...]


def canonical(clause: Clause) -> Clause:
    """Canonicalize a clause because DIMACS literal order is immaterial."""
    return tuple(sorted(clause))


def serialize_cnf(nvars: int, clauses: list[Clause]) -> bytes:
    """Serialize the exact DIMACS instance used to produce the certificate."""
    lines = [f"p cnf {nvars} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def parse_proof(payload: bytes) -> list[tuple[bool, Clause]]:
    """Parse ASCII DRAT as (is_deletion, clause) operations."""
    operations: list[tuple[bool, Clause]] = []
    for line_number, raw in enumerate(payload.decode("ascii").splitlines(), 1):
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        deletion = fields[0] == "d"
        if deletion:
            fields = fields[1:]
        integers = tuple(map(int, fields))
        if not integers or integers[-1] != 0 or 0 in integers[:-1]:
            raise AssertionError(f"malformed proof line {line_number}")
        operations.append((deletion, integers[:-1]))
    return operations


def assign_literal(assignments: list[int], literal: int) -> bool:
    """Assign a literal true; return False exactly on an immediate conflict."""
    variable = abs(literal)
    value = 1 if literal > 0 else -1
    old = assignments[variable]
    if old == -value:
        return False
    assignments[variable] = value
    return True


def rup(clauses: list[Clause], candidate: Clause, nvars: int) -> bool:
    """Check that negating candidate and unit propagating yields conflict."""
    assignments = [0] * (nvars + 1)
    for literal in candidate:
        if not assign_literal(assignments, -literal):
            return True

    while True:
        changed = False
        for clause in clauses:
            unit = 0
            satisfied = False
            multiple_unassigned = False
            for literal in clause:
                value = assignments[abs(literal)]
                if value == (1 if literal > 0 else -1):
                    satisfied = True
                    break
                if value == 0:
                    if unit:
                        multiple_unassigned = True
                    else:
                        unit = literal
            if satisfied or multiple_unassigned:
                continue
            if unit == 0:
                return True
            if not assign_literal(assignments, unit):
                return True
            changed = True
        if not changed:
            return False


def verify_rup_proof(
    original: list[Clause],
    operations: list[tuple[bool, Clause]],
    nvars: int,
) -> tuple[int, int]:
    """Verify all RUP additions and exact DRAT deletions through the empty clause."""
    active = [canonical(clause) for clause in original]
    multiplicities = Counter(active)
    additions = 0
    deletions = 0
    found_empty = False

    for step, (deletion, raw_clause) in enumerate(operations, 1):
        clause = canonical(raw_clause)
        if deletion:
            if multiplicities[clause] == 0:
                raise AssertionError(f"step {step}: deletion target is absent")
            active.remove(clause)
            multiplicities[clause] -= 1
            deletions += 1
            continue

        if found_empty:
            raise AssertionError("proof contains additions after the empty clause")
        if not rup(active, clause, nvars):
            raise AssertionError(f"step {step}: clause is not RUP")
        active.append(clause)
        multiplicities[clause] += 1
        additions += 1
        if not clause:
            found_empty = True

    if not found_empty:
        raise AssertionError("proof never derives the empty clause")
    return additions, deletions


def main() -> None:
    cells, groups = build_control()
    if len(cells) != 378 or len(groups) != 630:
        raise AssertionError("unexpected control dimensions")
    if any(len(group) != 3 for group in groups):
        raise AssertionError("a constraint group is not a triple")
    if any(len(set(group)) != 3 for group in groups):
        raise AssertionError("a constraint group repeats a cell")

    clauses = build_cnf(len(cells), groups)
    nvars = 3 * len(cells)
    cnf_payload = serialize_cnf(nvars, clauses)
    cnf_digest = hashlib.sha256(cnf_payload).hexdigest()
    if cnf_digest != EXPECTED_CNF_SHA256:
        raise AssertionError(f"CNF digest mismatch: {cnf_digest}")

    proof_payload = PROOF.read_bytes()
    proof_digest = hashlib.sha256(proof_payload).hexdigest()
    if proof_digest != EXPECTED_PROOF_SHA256:
        raise AssertionError(f"proof digest mismatch: {proof_digest}")
    operations = parse_proof(proof_payload)
    additions, deletions = verify_rup_proof(clauses, operations, nvars)

    print("k=6 fan structure: PASS")
    print(f"cells: {len(cells)}")
    print(f"groups: {len(groups)}")
    print(f"variables: {nvars}")
    print(f"clauses: {len(clauses)}")
    print(f"cnf_sha256: {cnf_digest}")
    print(f"proof_sha256: {proof_digest}")
    print(f"RUP additions: {additions}")
    print(f"deletions: {deletions}")
    print("empty-clause derivation: PASS")
    print("certified result: this fixed LS(2,3,9) admits no simultaneous 3-fan")
    print("scope: this is a small control, not a result for k=16 or #835")


if __name__ == "__main__":
    main()
