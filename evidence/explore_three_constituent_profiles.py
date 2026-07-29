#!/usr/bin/env python3
"""Test the two-fixed-nonblocks profile relaxation for three constituents.

This is exploratory: if A, B, C are pairwise block-disjoint
S(k-1,k,2k) systems, fix P in A and Q in B.  In the profile distribution
of C relative to P,Q, both distinguished profiles must have count zero.
The script tests exact nonnegative integral feasibility after imposing
complement closure.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from math import lcm
from pathlib import Path

from ortools.sat.python import cp_model

CLAUDE_WORK = Path(
    "/Users/dennison/.claude/jobs/243830f2/tmp/work/erdos835"
)
sys.path.insert(0, str(CLAUDE_WORK))

from triple_feasibility import build, nullspace, particular  # noqa: E402


def test(k: int, i: int) -> dict[str, object]:
    _, profiles, index, rows, rhs = build(k, i)
    nvars = len(profiles)
    solution, inconsistent = particular(rows, rhs, nvars)
    if inconsistent:
        return {"i": i, "status": "INCONSISTENT"}
    assert solution is not None
    kernel, rank = nullspace(rows, nvars)

    denominator = 1
    for value in solution:
        denominator = lcm(denominator, value.denominator)
    for vector in kernel:
        for value in vector:
            denominator = lcm(denominator, value.denominator)

    model = cp_model.CpModel()
    bound = 10**9
    parameters = [
        model.new_int_var(-bound, bound, f"t{j}")
        for j in range(len(kernel))
    ]
    counts = []
    for column in range(nvars):
        expression = int(solution[column] * denominator)
        expression += sum(
            int(kernel[j][column] * denominator) * parameters[j]
            for j in range(len(kernel))
        )
        count = model.new_int_var(0, bound, f"N{column}")
        model.add(expression == denominator * count)
        counts.append(count)

    # P has profile (i,k-i,0,0); Q has profile (i,0,k-i,0).
    model.add(counts[index[(i, k - i, 0, 0)]] == 0)
    model.add(counts[index[(i, 0, k - i, 0)]] == 0)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 120
    solver.parameters.num_search_workers = 8
    status = solver.solve(model)
    result: dict[str, object] = {
        "i": i,
        "profiles": nvars,
        "rank": rank,
        "dof": len(kernel),
        "status": solver.status_name(status),
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        witness = [solver.value(count) for count in counts]
        # Replay every original rational equation exactly.
        for row, target in zip(rows, rhs):
            actual = sum(
                coefficient * witness[column]
                for column, coefficient in row.items()
            )
            assert actual == target
        assert witness[index[(i, k - i, 0, 0)]] == 0
        assert witness[index[(i, 0, k - i, 0)]] == 0
        result["replay"] = "PASS"
    return result


def main() -> None:
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    selected = (
        [int(value) for value in sys.argv[2:]]
        if len(sys.argv) > 2
        else list(range(1, k))
    )
    for i in selected:
        result = test(k, i)
        print(
            f"i={i:2d}: profiles={result.get('profiles', '?'):>4} "
            f"rank={result.get('rank', '?'):>4} "
            f"dof={result.get('dof', '?'):>2} "
            f"status={result['status']} "
            f"replay={result.get('replay', '-')}",
            flush=True,
        )


if __name__ == "__main__":
    main()
