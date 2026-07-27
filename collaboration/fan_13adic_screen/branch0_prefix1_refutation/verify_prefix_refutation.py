#!/usr/bin/env python3
"""Reconstruct and verify the branch-0 prefix and its finite-completion CNF."""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CYCLIC = REPO / "collaboration" / "cyclic_lsts19_extension"
sys.path[:0] = [str(CYCLIC), str(REPO)]

from generate_c17_equivariant_cnf import orbit_representatives  # noqa: E402
from search_c17_equivariant_exact_cover import build_exact_cover  # noqa: E402


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    record = json.loads((HERE / "prefix.json").read_text())
    columns, rows = build_exact_cover()
    blocks = orbit_representatives(4)
    triples = orbit_representatives(3)
    branches = [
        tuple(map(int, line.split()))
        for line in (
            CYCLIC / "c17_type_i_branches.txt"
        ).read_text().splitlines()
    ]

    mixed = tuple(record["mixed_rows"])
    left = tuple(record["left_rows"])
    infinity = tuple(record["infinity_rows"])
    assert record["mixed_branch_index"] == 0
    assert mixed == branches[0]
    assert (len(mixed), len(left), len(infinity)) == (8, 40, 40)

    q_both = {
        index for index, block in enumerate(blocks)
        if 17 in block and 18 in block
    }
    q_left = {
        index for index, block in enumerate(blocks)
        if 17 in block and 18 not in block
    }
    q_infinity = {
        index for index, block in enumerate(blocks)
        if 18 in block and 17 not in block
    }
    q_finite = {
        index for index, block in enumerate(blocks)
        if 17 not in block and 18 not in block
    }
    assert tuple(map(len, (q_both, q_left, q_infinity, q_finite))) == (
        8, 40, 40, 140
    )
    assert all((row - 1) // 17 in q_both for row in mixed)
    assert all((row - 1) // 17 in q_left for row in left)
    assert all((row - 1) // 17 in q_infinity for row in infinity)

    t_both = {
        index for index, triple in enumerate(triples)
        if 17 in triple and 18 in triple
    }
    t_left = {
        index for index, triple in enumerate(triples)
        if 17 in triple and 18 not in triple
    }
    t_infinity = {
        index for index, triple in enumerate(triples)
        if 18 in triple and 17 not in triple
    }
    t_finite = {
        index for index, triple in enumerate(triples)
        if 17 not in triple and 18 not in triple
    }
    assert tuple(map(len, (t_both, t_left, t_infinity, t_finite))) == (
        1, 8, 8, 40
    )

    prefix = mixed + left + infinity
    assert len(prefix) == len(set(prefix)) == 88
    assert all(row in rows for row in prefix)
    covered_list = [column for row in prefix for column in rows[row]]
    assert len(covered_list) == len(set(covered_list)) == 440
    covered = set(covered_list)

    finite_demands = {
        column for column in range(228, 1140)
        if (column - 228) // 16 in t_finite
    }
    precovered = covered & finite_demands
    assert len(finite_demands) == 640
    assert len(precovered) == 80
    targets = q_finite | (finite_demands - precovered)
    assert len(targets) == 700

    candidates = sorted(
        row
        for qcol in q_finite
        for row in columns[qcol]
        if not (set(rows[row]) & covered)
    )
    assert len(candidates) == 1016
    variable = {row: index + 1 for index, row in enumerate(candidates)}
    clauses: list[tuple[int, ...]] = []
    for column in sorted(targets):
        options = tuple(
            variable[row] for row in candidates if column in rows[row]
        )
        assert options
        clauses.append(options)
        clauses.extend(
            (-left_var, -right_var)
            for left_var, right_var in combinations(options, 2)
        )
    assert len(clauses) == 17046
    lines = [f"p cnf {len(candidates)} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    reconstructed = ("\n".join(lines) + "\n").encode("ascii")

    cnf = (HERE / "finite_completion.cnf").read_bytes()
    assert reconstructed == cnf
    expected = record["finite_completion"]
    assert sha256(cnf) == expected["cnf_sha256"]
    compressed = (HERE / "finite_completion.drat.gz").read_bytes()
    assert sha256(compressed) == expected["drat_gzip_sha256"]
    assert sha256(gzip.decompress(compressed)) == expected["drat_sha256"]

    print("8+40+40+140 orbit decomposition: PASS")
    print("explicit 88-row compatible prefix: PASS")
    print("finite target/candidate counts 700/1016: PASS")
    print("17,046-clause CNF byte reconstruction: PASS")
    print("CNF and compressed/uncompressed DRAT digests: PASS")
    print(
        "scope: one prefix-local refutation only; no full C17, "
        "LS(3,4,20), fan, or #835 conclusion"
    )


if __name__ == "__main__":
    main()
