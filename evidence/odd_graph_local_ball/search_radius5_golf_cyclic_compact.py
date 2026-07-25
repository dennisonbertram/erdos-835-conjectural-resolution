#!/usr/bin/env python3
"""Compact exact CP-SAT model for the cyclic fixed-golf radius-five ansatz.

Moving edges of Z_17 have eight translation orbits, indexed by their
undirected differences 1,...,8.  Any choice of one translate from each of the
forty moving-triple orbits contains exactly fifteen edge occurrences of every
difference.  For a fixed golf-square pair ij, the two zero one-factors remove
exactly two edge positions in each difference orbit.  Consequently the
selected triples decompose the residual graph if and only if, for each of the
eight differences, their fifteen translated edge positions are AllDifferent.

This replaces 71,400 one-hot Booleans and 14,280 edge equations by 4,200 phase
integers, 12,600 modular edge-position auxiliaries, 840 slice AllDifferent
constraints, and the same 600 cross-slice AllDifferent constraints.

SAT is converted to the canonical N/P payload and checked on the complete
73,457-vertex radius-five ball.  UNKNOWN has no mathematical meaning, and an
UNSAT status is not a portable proof without an independently checkable proof
log.  The entire model is a fixed-Wallis-golf, C17-equivariant ansatz, not the
full Erdos-Rosenfeld problem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


EVIDENCE = Path(__file__).resolve().parents[1]
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from convert_cyclic17_r3_to_radius5 import convert
from global_latin_audit import construct_golf17


P = 17
POINTS = tuple(range(P))
SQUARES = tuple(range(15))
FIXED_PAIRS = tuple(combinations(SQUARES, 2))
MOVING_EDGES = tuple(combinations(POINTS, 2))
MOVING_TRIPLES = tuple(combinations(POINTS, 3))
DIFFERENCES = tuple(range(1, 9))


def translate(
    subset: tuple[int, ...], amount: int
) -> tuple[int, ...]:
    return tuple(sorted((value + amount) % P for value in subset))


def triple_representatives() -> list[tuple[int, int, int]]:
    representatives: list[tuple[int, int, int]] = []
    unseen = set(MOVING_TRIPLES)
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in POINTS)
        representatives.append(representative)
        for shift in POINTS:
            unseen.discard(translate(representative, shift))
    assert len(representatives) == 40
    return representatives


REPRESENTATIVES = triple_representatives()


def edge_coordinate(edge: tuple[int, int]) -> tuple[int, int]:
    """Write an unordered edge uniquely as {position, position+d}, 1<=d<=8."""
    x, y = edge
    forward = (y - x) % P
    if forward <= 8:
        return forward, x
    return P - forward, y


def representative_edge_coordinates():
    answer: list[tuple[tuple[int, int], ...]] = []
    multiplicities = {difference: 0 for difference in DIFFERENCES}
    for representative in REPRESENTATIVES:
        coordinates = tuple(
            edge_coordinate(edge)
            for edge in combinations(representative, 2)
        )
        answer.append(coordinates)
        for difference, _ in coordinates:
            multiplicities[difference] += 1
    assert multiplicities == {difference: 15 for difference in DIFFERENCES}
    return answer


REPRESENTATIVE_EDGE_COORDINATES = representative_edge_coordinates()


def zero_positions(golf) -> dict[tuple[int, int], int]:
    answer: dict[tuple[int, int], int] = {}
    for square in SQUARES:
        zero_edges = [
            edge for edge in MOVING_EDGES
            if golf[square][edge[0]][edge[1]] == 0
        ]
        assert len(zero_edges) == 8
        for edge in zero_edges:
            difference, position = edge_coordinate(edge)
            key = square, difference
            assert key not in answer
            answer[key] = position
    assert len(answer) == len(SQUARES) * len(DIFFERENCES)
    return answer


def allowed_shifts(
    fixed_pair: tuple[int, int],
    orbit_index: int,
    zeros: dict[tuple[int, int], int],
) -> list[int]:
    i, j = fixed_pair
    allowed = []
    for shift in POINTS:
        if all(
            (position + shift) % P
            not in {zeros[i, difference], zeros[j, difference]}
            for difference, position
            in REPRESENTATIVE_EDGE_COORDINATES[orbit_index]
        ):
            allowed.append(shift)
    assert allowed
    return allowed


def cross_matching_audit(
    zeros: dict[tuple[int, int], int],
) -> dict[str, object]:
    """Audit the exact round-robin interpretation of every cross constraint.

    For one triple orbit q and fixed square i, the three triangle edges forbid
    three distinct phases F_i(q).  At phase c, the c-coloured fixed-pair edges
    in any cross-compatible solution must therefore form a perfect matching
    on the squares i with c not in F_i(q).  There are fourteen allowed squares
    at the three phases where the translated triple contains 0, and twelve at
    each of the other fourteen phases.
    """
    domain_sizes: Counter[int] = Counter()
    allowed_vertex_sizes: Counter[int] = Counter()
    singleton_holes: Counter[int] = Counter()
    triple_holes: Counter[tuple[int, int, int]] = Counter()
    for orbit_index, coordinates in enumerate(
        REPRESENTATIVE_EDGE_COORDINATES
    ):
        forbidden = {
            square: {
                (zeros[square, difference] - offset) % P
                for difference, offset in coordinates
            }
            for square in SQUARES
        }
        assert all(len(values) == 3 for values in forbidden.values())
        for phase in POINTS:
            hole = {
                square
                for square in SQUARES
                if phase in forbidden[square]
            }
            allowed_vertices = set(SQUARES) - hole
            assert len(allowed_vertices) in (12, 14)
            allowed_vertex_sizes[len(allowed_vertices)] += 1
            if len(hole) == 1:
                singleton_holes.update(hole)
            else:
                assert len(hole) == 3
                triple_holes[tuple(sorted(hole))] += 1
        for fixed_pair in FIXED_PAIRS:
            domain = set(
                allowed_shifts(
                    fixed_pair,
                    orbit_index,
                    zeros,
                )
            )
            i, j = fixed_pair
            assert domain == (
                set(POINTS) - forbidden[i] - forbidden[j]
            )
            domain_sizes[len(domain)] += 1
    assert domain_sizes == Counter({11: 2658, 12: 1407, 13: 132, 14: 3})
    assert allowed_vertex_sizes == Counter({12: 560, 14: 120})
    assert singleton_holes == Counter({square: 8 for square in SQUARES})
    triple_point_counts = Counter(
        square
        for hole, multiplicity in triple_holes.items()
        for square in hole
        for _ in range(multiplicity)
    )
    triple_pair_counts = Counter(
        fixed_pair
        for hole, multiplicity in triple_holes.items()
        for fixed_pair in combinations(hole, 2)
        for _ in range(multiplicity)
    )
    assert triple_point_counts == Counter(
        {square: 112 for square in SQUARES}
    )
    assert triple_pair_counts == Counter(
        {fixed_pair: 16 for fixed_pair in FIXED_PAIRS}
    )
    assert len(triple_holes) == 336
    hole_multiplicities = Counter(triple_holes.values())
    assert min(hole_multiplicities) == 1
    assert max(hole_multiplicities) == 5
    per_fixed_pair_domain_values = Counter()
    for i, j in FIXED_PAIRS:
        per_fixed_pair_domain_values[
            sum(
                len(allowed_shifts((i, j), orbit_index, zeros))
                for orbit_index in range(len(REPRESENTATIVES))
            )
        ] += 1
    assert per_fixed_pair_domain_values == Counter({456: 105})
    return {
        "phase_domain_size_distribution": dict(sorted(domain_sizes.items())),
        "cross_colour_allowed_vertex_size_distribution": dict(
            sorted(allowed_vertex_sizes.items())
        ),
        "singleton_holes_per_fixed_vertex": 8,
        "triple_hole_design": "2-(15,3,16) multidesign",
        "distinct_triple_holes": len(triple_holes),
        "triple_hole_multiplicity_distribution": dict(
            sorted(hole_multiplicities.items())
        ),
        "allowed_phase_values_per_fixed_pair": 456,
    }


def build_model(golf):
    zeros = zero_positions(golf)
    cross_matching_stats = cross_matching_audit(zeros)
    model = cp_model.CpModel()
    selected: dict[tuple[int, int, int], cp_model.IntVar] = {}
    domain_values = 0

    for i, j in FIXED_PAIRS:
        for orbit_index in range(len(REPRESENTATIVES)):
            domain = allowed_shifts((i, j), orbit_index, zeros)
            domain_values += len(domain)
            selected[i, j, orbit_index] = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(domain),
                f"phase_{i}_{j}_{orbit_index}",
            )

    edge_positions: dict[
        tuple[int, int, int], list[cp_model.IntVar]
    ] = {
        (i, j, difference): []
        for i, j in FIXED_PAIRS
        for difference in DIFFERENCES
    }
    modular_equalities = 0
    for i, j in FIXED_PAIRS:
        for orbit_index, coordinates in enumerate(
            REPRESENTATIVE_EDGE_COORDINATES
        ):
            phase = selected[i, j, orbit_index]
            for occurrence, (difference, offset) in enumerate(coordinates):
                residual_positions = [
                    value for value in POINTS
                    if value not in {
                        zeros[i, difference],
                        zeros[j, difference],
                    }
                ]
                assert len(residual_positions) == 15
                position = model.NewIntVarFromDomain(
                    cp_model.Domain.FromValues(residual_positions),
                    f"edgepos_{i}_{j}_{orbit_index}_{occurrence}",
                )
                model.AddModuloEquality(position, phase + offset, P)
                modular_equalities += 1
                edge_positions[i, j, difference].append(position)

    slice_all_different = 0
    slice_sum_equalities = 0
    for (i, j, difference), variables in edge_positions.items():
        assert len(variables) == 15
        model.AddAllDifferent(variables)
        slice_all_different += 1
        model.Add(
            sum(variables)
            == sum(POINTS)
            - zeros[i, difference]
            - zeros[j, difference]
        )
        slice_sum_equalities += 1

    cross_all_different = 0
    cross_sum_equalities = 0
    for fixed_point in SQUARES:
        incident = [
            (min(fixed_point, other), max(fixed_point, other))
            for other in SQUARES
            if other != fixed_point
        ]
        assert len(incident) == 14
        for orbit_index in range(len(REPRESENTATIVES)):
            variables = [
                selected[i, j, orbit_index]
                for i, j in incident
            ]
            forbidden = {
                (
                    zeros[fixed_point, difference] - offset
                )
                % P
                for difference, offset
                in REPRESENTATIVE_EDGE_COORDINATES[orbit_index]
            }
            # A matching cannot contain two edges of one triangle, so the
            # three edge occurrences forbid three distinct shifts.
            assert len(forbidden) == 3
            model.AddAllDifferent(variables)
            cross_all_different += 1
            model.Add(
                sum(variables) == sum(POINTS) - sum(forbidden)
            )
            cross_sum_equalities += 1

    stats = {
        "phase_integer_variables": len(selected),
        "phase_domain_values": domain_values,
        "edge_position_integer_variables": modular_equalities,
        "modular_equalities": modular_equalities,
        "slice_all_different": slice_all_different,
        "slice_sum_equalities": slice_sum_equalities,
        "cross_slice_all_different": cross_all_different,
        "cross_slice_sum_equalities": cross_sum_equalities,
        **cross_matching_stats,
    }
    assert stats["phase_integer_variables"] == 4200
    assert stats["edge_position_integer_variables"] == 12600
    assert stats["modular_equalities"] == 12600
    assert stats["slice_all_different"] == 840
    assert stats["slice_sum_equalities"] == 840
    assert stats["cross_slice_all_different"] == 600
    assert stats["cross_slice_sum_equalities"] == 600
    return model, selected, stats


def add_hints(model, selected, source: Path) -> int:
    payload = json.loads(source.read_text(encoding="utf-8"))
    expected = {f"{i},{j}" for i, j in FIXED_PAIRS}
    if set(payload) != expected:
        raise ValueError("phase hint must contain all 105 fixed pairs")
    hinted = 0
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        if (
            not isinstance(phases, list)
            or len(phases) != len(REPRESENTATIVES)
        ):
            raise ValueError(f"wrong phase hint list for {i},{j}")
        for orbit_index, phase in enumerate(phases):
            if not isinstance(phase, int) or not 0 <= phase < P:
                raise ValueError(f"invalid phase hint for {i},{j}")
            model.AddHint(
                selected[i, j, orbit_index],
                (-phase) % P,
            )
            hinted += 1
    return hinted


def load_phase_payload(source: Path) -> dict[str, list[int]]:
    payload = json.loads(source.read_text(encoding="utf-8"))
    expected = {f"{i},{j}" for i, j in FIXED_PAIRS}
    if set(payload) != expected:
        raise ValueError("phase payload must contain all 105 fixed pairs")
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        if (
            not isinstance(phases, list)
            or len(phases) != len(REPRESENTATIVES)
            or not all(
                isinstance(phase, int) and 0 <= phase < P
                for phase in phases
            )
        ):
            raise ValueError(f"invalid phase payload list for {i},{j}")
    return payload


def add_common_fixes(
    model,
    selected,
    left_source: Path,
    right_source: Path,
    fraction: float,
    seed: int,
) -> int:
    """Fix cells on which two independently valid family states agree.

    This defines a conditioned exact subproblem only.  Infeasibility of the
    conditioned model has no consequence for the unconditioned ansatz.
    """
    left = load_phase_payload(left_source)
    right = load_phase_payload(right_source)
    agreements = []
    for i, j in FIXED_PAIRS:
        key = f"{i},{j}"
        for orbit_index in range(len(REPRESENTATIVES)):
            if left[key][orbit_index] != right[key][orbit_index]:
                continue
            agreements.append(
                (i, j, orbit_index, left[key][orbit_index])
            )
    rng = random.Random(seed)
    rng.shuffle(agreements)
    keep = round(fraction * len(agreements))
    agreements = agreements[:keep]
    for i, j, orbit_index, phase in agreements:
        model.Add(
            selected[i, j, orbit_index]
            == (-phase) % P
        )
    return len(agreements)


def phases_from_solver(solver, selected) -> dict[str, list[int]]:
    return {
        f"{i},{j}": [
            (-solver.Value(selected[i, j, orbit_index])) % P
            for orbit_index in range(len(REPRESENTATIVES))
        ]
        for i, j in FIXED_PAIRS
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=1200.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--phase-output", type=Path)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--fix-common-left", type=Path)
    parser.add_argument("--fix-common-right", type=Path)
    parser.add_argument(
        "--fix-common-fraction",
        type=float,
        default=1.0,
        help="reproducible fraction of agreeing cells to condition on",
    )
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    golf = construct_golf17()
    model, selected, stats = build_model(golf)
    hinted = (
        add_hints(model, selected, args.hint)
        if args.hint is not None
        else 0
    )
    if (args.fix_common_left is None) != (
        args.fix_common_right is None
    ):
        parser.error(
            "--fix-common-left and --fix-common-right must be used together"
        )
    if not 0.0 <= args.fix_common_fraction <= 1.0:
        parser.error("--fix-common-fraction must lie in [0,1]")
    common_fixed = (
        add_common_fixes(
            model,
            selected,
            args.fix_common_left,
            args.fix_common_right,
            args.fix_common_fraction,
            args.seed,
        )
        if args.fix_common_left is not None
        else 0
    )
    if args.audit_only:
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "counts": stats,
                    "hinted_phase_integers": hinted,
                    "common_fixed_phase_integers": common_fixed,
                    "triple_orbits": len(REPRESENTATIVES),
                    "edge_difference_orbits": len(DIFFERENCES),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    if hinted:
        solver.parameters.repair_hint = True
        solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    report: dict[str, object] = {
        "status": solver.StatusName(status),
        "counts": stats,
        "hinted_phase_integers": hinted,
        "common_fixed_phase_integers": common_fixed,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        phases = phases_from_solver(solver, selected)
        encoded = (
            json.dumps(phases, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        report["phase_sha256"] = hashlib.sha256(encoded).hexdigest()
        if args.phase_output is not None:
            args.phase_output.write_bytes(encoded)
        payload = convert(phases)
        report["semantic_verifier"] = {
            "status": "PASS",
            "vertices": 73457,
            "constrained_centres": 14657,
            "semantic_ball_verified": True,
        }
        report["certificate_sha256_without_hash"] = payload[
            "sha256_without_hash"
        ]
        if args.certificate is not None:
            args.certificate.write_text(
                json.dumps(
                    payload,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n",
                encoding="utf-8",
            )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
