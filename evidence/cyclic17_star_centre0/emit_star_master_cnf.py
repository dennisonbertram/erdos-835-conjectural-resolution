#!/usr/bin/env python3
"""Deterministic DIMACS CNF for the centre star master.

Variables 1..N: stored rows, family-major (family order as given, rows in
file order). ExactlyOne per family (ALO clause + sequential AMO).
AtMostOne per (orbit, phase) slot over its user rows (sequential AMO).
UNSAT == no star assembly from the complete families.
"""

import sys
from pathlib import Path


def sequential_amo(lits, next_aux, clauses):
    """Sinz sequential at-most-one. Returns next free aux var."""
    n = len(lits)
    if n <= 1:
        return next_aux
    s = [next_aux + i for i in range(n - 1)]
    next_aux += n - 1
    clauses.append((-lits[0], s[0]))
    for i in range(1, n - 1):
        clauses.append((-lits[i], s[i]))
        clauses.append((-s[i - 1], s[i]))
        clauses.append((-lits[i], -s[i - 1]))
    clauses.append((-lits[n - 1], -s[n - 2]))
    return next_aux


def main():
    out_path = sys.argv[1]
    family_files = sys.argv[2:]
    assert len(family_files) >= 2
    families = []
    for path in family_files:
        raw = Path(path).read_bytes()
        assert len(raw) % 40 == 0
        families.append([raw[k * 40:(k + 1) * 40] for k in range(len(raw) // 40)])

    var = 0
    fam_vars = []
    for fam in families:
        fam_vars.append([var + i + 1 for i in range(len(fam))])
        var += len(fam)
    n_rows = var

    slot_users = {}  # (orbit, phase) -> [vars]
    for f, fam in enumerate(families):
        for r, sol in enumerate(fam):
            v = fam_vars[f][r]
            for k in range(40):
                slot_users.setdefault((k, sol[k]), []).append(v)

    clauses = []
    next_aux = n_rows + 1
    for f in range(len(families)):
        clauses.append(tuple(fam_vars[f]))  # at least one
        next_aux = sequential_amo(fam_vars[f], next_aux, clauses)
    for key in sorted(slot_users):
        next_aux = sequential_amo(slot_users[key], next_aux, clauses)

    n_vars = next_aux - 1
    with open(out_path, "w") as out:
        out.write(f"p cnf {n_vars} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")
    print(f"rows={n_rows} vars={n_vars} clauses={len(clauses)} "
          f"slots={len(slot_users)} file={out_path}")


if __name__ == "__main__":
    main()
