#!/usr/bin/env python3
"""Exactly replay the 302,743-neighborhood finite-packing search.

This exhausts a precisely delimited neighborhood of one score-10 assignment.
It is not a global search and cannot establish alpha_finite < 140.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CYCLIC = REPO / "collaboration" / "cyclic_lsts19_extension"
sys.path[:0] = [str(CYCLIC), str(REPO)]

from generate_c17_equivariant_cnf import orbit_representatives  # noqa: E402
from search_c17_equivariant_exact_cover import build_exact_cover  # noqa: E402


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def main() -> None:
    assignment_path = HERE / "near_assignment_score10.json"
    source_path = HERE / "verify_neighborhood_302743.py"
    receipt = json.loads((HERE / "RUN_RECEIPT.json").read_text())
    expected = receipt["neighborhood_302743"]
    assert sha256(assignment_path.read_bytes()) == expected[
        "near_assignment_sha256"
    ]
    assert sha256(source_path.read_bytes()) == expected["checker_sha256"]

    data = json.loads(assignment_path.read_text())
    selected = tuple(data["selected_rows"])
    assert data["score"] == 10
    assert data["size"] == len(selected) == 140
    assert len(set(selected)) == 140

    columns, rows = build_exact_cover()
    blocks = orbit_representatives(4)
    triples = orbit_representatives(3)
    qcols = tuple(
        sorted(
            index
            for index, block in enumerate(blocks)
            if 17 not in block and 18 not in block
        )
    )
    stars = {
        index
        for index, triple in enumerate(triples)
        if 17 not in triple and 18 not in triple
    }
    demands = {
        column
        for column in range(228, 1140)
        if (column - 228) // 16 in stars
    }
    assert (len(qcols), len(stars), len(demands)) == (140, 40, 640)
    row_demands = {
        row: frozenset(rows[row]) & demands
        for qcol in qcols
        for row in columns[qcol]
    }
    assert all(len(row_demands[row]) == 4 for row in row_demands)
    assert {(row - 1) // 17 for row in selected} == set(qcols)

    users: dict[int, list[int]] = {}
    for row in selected:
        for demand in row_demands[row]:
            users.setdefault(demand, []).append(row)
    score = sum(max(0, len(values) - 1) for values in users.values())
    conflict_edges = {
        tuple(sorted(pair))
        for values in users.values()
        if len(values) > 1
        for pair in combinations(values, 2)
    }
    bad = tuple(sorted({row for edge in conflict_edges for row in edge}))
    good = tuple(row for row in selected if row not in set(bad))
    assert (score, len(conflict_edges), len(bad), len(good)) == (
        expected["starting_score"],
        expected["conflict_edges"],
        expected["bad_rows"],
        expected["good_rows"],
    ) == (10, 10, 18, 122)

    completions = 0

    def extend(removed: frozenset[int]) -> tuple[int, ...] | None:
        fixed = tuple(row for row in selected if row not in removed)
        occupied: set[int] = set()
        for row in fixed:
            assert not (occupied & row_demands[row])
            occupied.update(row_demands[row])
        missing = set(qcols) - {(row - 1) // 17 for row in fixed}

        def dfs(
            todo: set[int], used: set[int], chosen: list[int]
        ) -> list[int] | None:
            if not todo:
                return list(chosen)
            best_q = -1
            best_options: list[int] | None = None
            for qcol in sorted(todo):
                choices = [
                    row
                    for row in sorted(columns[qcol])
                    if not (row_demands[row] & used)
                ]
                if not choices:
                    return None
                if best_options is None or len(choices) < len(best_options):
                    best_q, best_options = qcol, choices
            assert best_options is not None
            rest = set(todo)
            rest.remove(best_q)
            for row in best_options:
                result = dfs(
                    rest,
                    used | set(row_demands[row]),
                    chosen + [row],
                )
                if result is not None:
                    return result
            return None

        extension = dfs(missing, occupied, [])
        if extension is None:
            return None
        return fixed + tuple(extension)

    minimum_cover_size = None
    minimum_covers = []
    for size in range(len(bad) + 1):
        minimum_covers = [
            frozenset(choice)
            for choice in combinations(bad, size)
            if all(left in choice or right in choice for left, right in conflict_edges)
        ]
        if minimum_covers:
            minimum_cover_size = size
            break
    assert minimum_cover_size == expected["minimum_cover_size"] == 8
    assert len(minimum_covers) == expected["minimum_covers"] == 64
    for removed in minimum_covers:
        if extend(removed) is not None:
            completions += 1
    assert completions == 0

    family_counts: dict[str, int] = {}
    neighborhood_tests = 0
    all_bad = frozenset(bad)
    for size in (1, 2, 3):
        count = 0
        for extra in combinations(good, size):
            count += 1
            if extend(all_bad | frozenset(extra)) is not None:
                completions += 1
        assert count == math.comb(len(good), size)
        family_counts[str(size)] = count
        neighborhood_tests += count

    assert family_counts == expected["extra_good_subset_counts"] == {
        "1": 122,
        "2": 7381,
        "3": 295240,
    }
    assert neighborhood_tests == expected["neighborhoods_tested"] == 302743
    assert completions == expected["completions_found"] == 0
    assert receipt["alpha_finite_upper_bound"] == 140
    assert receipt["upper_bound_kind"] == "TRIVIAL"

    print("starting assignment score=10, conflict edges=10: PASS")
    print("bad rows=18, good rows=122: PASS")
    print("minimum vertex-cover size=8, covers=64: PASS")
    print("minimum-cover completions found=0: PASS")
    print("extra-good subset counts 122 + 7,381 + 295,240: PASS")
    print("defined neighborhoods tested=302,743: PASS")
    print("neighborhood completions found=0: PASS")
    print(
        "scope: exact local-neighborhood exhaustion only; "
        "no global upper bound below 140"
    )


if __name__ == "__main__":
    main()
