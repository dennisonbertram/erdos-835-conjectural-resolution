#!/usr/bin/env python3
"""Search one multiplicatively free SIDLS on PG(1,16).

A solution is a symmetric idempotent Latin square S of order 17 such that

    S(rho*a, rho*b) != rho*S(a,b)

for every nonidentity rho in GF(16)^* and every off-diagonal cell {a,b}.
Its fifteen GF(16)^* twists would therefore be pairwise disjoint at every
off-diagonal cell, giving the complete L/M layer in radius4_reduction.md.

The optional ``frobenius`` variant also imposes

    S(a^2,b^2) = S(a,b)^2.

There are two equivalent encodings of multiplicative freeness:

* binary: one forbidden-assignment table for every rho and cell;
* orbit: after transporting each cell back to an orbit representative,
  the fifteen transported symbols must be all different.

Any positive result is independently checked before a witness is written.
An INFEASIBLE result concerns only this multiplicative-twist construction,
not the unrestricted radius-4 problem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time

from ortools.sat.python import cp_model


INF = 16
MODULUS = 0b10011  # x^4 + x + 1
POINTS = range(17)
CELLS = [(a, b) for a in POINTS for b in range(a + 1, 17)]


def multiply(a: int, b: int) -> int:
    """Multiply bit-vector representatives in GF(16)."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 0x10:
            a ^= MODULUS
    return result


def inverse(a: int) -> int:
    assert 1 <= a < 16
    result = 1
    for _ in range(14):
        result = multiply(result, a)
    return result


def act(rho: int, point: int) -> int:
    return INF if point == INF else multiply(rho, point)


def frobenius(point: int) -> int:
    return INF if point == INF else multiply(point, point)


def cell(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def free_cell_orbits() -> list[list[tuple[int, tuple[int, int]]]]:
    """The nine free length-15 orbits; {0,infinity} is the sole fixed cell."""
    seen: set[tuple[int, int]] = set()
    result = []
    for representative in CELLS:
        if representative in seen:
            continue
        orbit = [
            (rho, cell(act(rho, representative[0]),
                       act(rho, representative[1])))
            for rho in range(1, 16)
        ]
        distinct = {entry for _, entry in orbit}
        seen.update(distinct)
        if len(distinct) == 1:
            assert representative == (0, INF)
            continue
        assert len(distinct) == 15
        result.append(orbit)
    assert len(result) == 9
    return result


def build_model(
    encoding: str,
    impose_frobenius: bool,
) -> tuple[cp_model.CpModel, dict[tuple[int, int], cp_model.IntVar]]:
    model = cp_model.CpModel()
    value = {}
    for a, b in CELLS:
        allowed = [symbol for symbol in POINTS if symbol not in (a, b)]
        value[(a, b)] = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(allowed), f"S_{a}_{b}"
        )

    # Multiplicative conjugation transports any solution so that this holds.
    model.Add(value[(0, INF)] == 1)

    # Symmetry is built into unordered cells. These constraints make every row
    # Latin; its missing diagonal value is the row label.
    for a in POINTS:
        model.AddAllDifferent(
            [value[cell(a, b)] for b in POINTS if b != a]
        )

    if encoding == "binary":
        for rho in range(2, 16):
            for original in CELLS:
                transported = cell(
                    act(rho, original[0]), act(rho, original[1])
                )
                if transported == original:
                    assert original == (0, INF)
                    continue
                forbidden = [
                    (symbol, act(rho, symbol)) for symbol in POINTS
                ]
                model.AddForbiddenAssignments(
                    [value[original], value[transported]], forbidden
                )
    else:
        for orbit_index, orbit in enumerate(free_cell_orbits()):
            representative = dict(orbit)[1]
            common_domain = [
                symbol for symbol in POINTS
                if symbol not in representative
            ]
            transported_values = []
            for rho, transported_cell in orbit:
                back = model.NewIntVarFromDomain(
                    cp_model.Domain.FromValues(common_domain),
                    f"back_{orbit_index}_{rho}",
                )
                rho_inverse = inverse(rho)
                model.AddAllowedAssignments(
                    [value[transported_cell], back],
                    [
                        (symbol, act(rho_inverse, symbol))
                        for symbol in POINTS
                    ],
                )
                transported_values.append(back)
            model.AddAllDifferent(transported_values)

    if impose_frobenius:
        # Add the relation on every cell. Repetition around 2- and 4-cycles is
        # intentional and avoids relying on a fragile orbit-representative loop.
        for original in CELLS:
            image = cell(
                frobenius(original[0]), frobenius(original[1])
            )
            allowed = [
                (symbol, frobenius(symbol))
                for symbol in POINTS
                if symbol not in original
                and frobenius(symbol) not in image
            ]
            model.AddAllowedAssignments(
                [value[original], value[image]], allowed
            )

    return model, value


def verify(square: list[list[int]]) -> None:
    expected = set(POINTS)
    assert len(square) == 17 and all(len(row) == 17 for row in square)
    for a in POINTS:
        assert square[a][a] == a
        assert set(square[a]) == expected
        for b in POINTS:
            assert square[a][b] == square[b][a]
    for rho in range(2, 16):
        for a, b in CELLS:
            assert square[act(rho, a)][act(rho, b)] != act(
                rho, square[a][b]
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--encoding", choices=("binary", "orbit"), default="binary"
    )
    parser.add_argument("--frobenius", action="store_true")
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--certificate")
    args = parser.parse_args()

    model, value = build_model(args.encoding, args.frobenius)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    started = time.monotonic()
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    statistics = {
        "status": status_name,
        "wall_seconds": round(time.monotonic() - started, 3),
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "booleans": solver.NumBooleans(),
        "encoding": args.encoding,
        "frobenius": args.frobenius,
    }
    print(json.dumps(statistics, sort_keys=True))
    if status_name not in ("OPTIMAL", "FEASIBLE"):
        return 2 if status_name == "INFEASIBLE" else 3

    square = [[a if a == b else -1 for b in POINTS] for a in POINTS]
    for a, b in CELLS:
        square[a][b] = square[b][a] = solver.Value(value[(a, b)])
    verify(square)
    if args.frobenius:
        for a, b in CELLS:
            assert square[frobenius(a)][frobenius(b)] == frobenius(
                square[a][b]
            )

    payload = {
        "object": "multiplicatively free SIDLS on PG(1,16)",
        "field": "GF(16)=F2[x]/(x^4+x+1); infinity=16",
        "normalization": "S(0,infinity)=1",
        "statistics": statistics,
        "square": square,
    }
    canonical = json.dumps(payload, sort_keys=True).encode()
    payload["sha256_without_hash"] = hashlib.sha256(canonical).hexdigest()
    if args.certificate:
        with open(args.certificate, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
        print(f"verified certificate: {args.certificate}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
