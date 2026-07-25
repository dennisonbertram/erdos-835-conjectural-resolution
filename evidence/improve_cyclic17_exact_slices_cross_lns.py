#!/usr/bin/env python3
"""Glue exact cyclic-17 slices by cross-compatibility coordinate descent.

The input must contain one independently valid exact-cover phase vector for
each of the 105 fixed pairs.  Every local move re-solves one complete
40-orbit slice, so all 105 residual triangle decompositions remain exact.
The objective is the number of distinct phases around each fixed vertex and
triple orbit.  Its maximum is 15*40*14 = 8,400, exactly the missing joint
cross-slice condition.

Any score below 8,400 is only a heuristic seed.  A score of 8,400 is passed
through the independent joint semantic verifier before it is reported.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model

from global_latin_audit import construct_golf17
from search_cyclic17_r3_extension import (
    FIXED,
    FIXED_PAIRS,
    MOVING_PAIRS,
    P,
    POINTS,
    TRIPLE_REPRESENTATIVES,
    translate,
    verify_certificate,
    verify_joint_compatibility,
    verify_single_fixed_pair,
)


State = dict[tuple[int, int], list[int]]


def load_state(path: Path) -> State:
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = {f"{i},{j}" for i, j in FIXED_PAIRS}
    if set(payload) != expected:
        raise ValueError("input must contain all 105 fixed-pair slices")
    verify_certificate(payload)
    return {
        (i, j): list(payload[f"{i},{j}"])
        for i, j in FIXED_PAIRS
    }


def dump_state(state: State) -> dict[str, list[int]]:
    return {
        f"{i},{j}": state[i, j]
        for i, j in FIXED_PAIRS
    }


def write_state(path: Path, state: State) -> str:
    encoded = (
        json.dumps(dump_state(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def incident_pair(fixed_point: int, other: int) -> tuple[int, int]:
    return min(fixed_point, other), max(fixed_point, other)


def cross_score(state: State) -> int:
    return sum(
        len(
            {
                state[incident_pair(fixed_point, other)][orbit_index]
                for other in FIXED
                if other != fixed_point
            }
        )
        for fixed_point in FIXED
        for orbit_index in range(len(TRIPLE_REPRESENTATIVES))
    )


def pair_pressure(state: State, fixed_pair: tuple[int, int]) -> int:
    """Return the local deficit in the 80 incident cross groups."""
    i, j = fixed_pair
    return sum(
        14
        - len(
            {
                state[incident_pair(endpoint, other)][orbit_index]
                for other in FIXED
                if other != endpoint
            }
        )
        for endpoint in (i, j)
        for orbit_index in range(len(TRIPLE_REPRESENTATIVES))
    )


def slice_domains_and_occurrences(golf, fixed_pair):
    i, j = fixed_pair
    leave = {
        pair
        for pair in MOVING_PAIRS
        if golf[i][pair[0]][pair[1]] == 0
        or golf[j][pair[0]][pair[1]] == 0
    }
    assert len(leave) == 16
    domains = {}
    occurrences = {edge: [] for edge in MOVING_PAIRS if edge not in leave}
    for orbit_index, representative in enumerate(TRIPLE_REPRESENTATIVES):
        values = []
        for shift in POINTS:
            triple = translate(representative, shift)
            edges = tuple(combinations(triple, 2))
            if any(edge in leave for edge in edges):
                continue
            values.append(shift)
            for edge in edges:
                occurrences[edge].append((orbit_index, shift))
        assert values
        domains[orbit_index] = tuple(values)
    assert len(occurrences) == 120
    assert all(values for values in occurrences.values())
    return domains, occurrences


def optimize_pair(
    state: State,
    golf,
    fixed_pair: tuple[int, int],
    *,
    seconds: float,
    seed: int,
    random_tiebreak: int,
) -> tuple[str, int, list[int] | None]:
    """Re-solve one exact slice while maximizing its cross contribution."""
    i, j = fixed_pair
    domains, occurrences = slice_domains_and_occurrences(golf, fixed_pair)
    model = cp_model.CpModel()
    choose = {}
    objective_terms = []
    rng = random.Random(seed)
    for orbit_index, shifts in domains.items():
        literals = []
        others_i = {
            state[incident_pair(i, other)][orbit_index]
            for other in FIXED
            if other not in fixed_pair
        }
        others_j = {
            state[incident_pair(j, other)][orbit_index]
            for other in FIXED
            if other not in fixed_pair
        }
        for shift in shifts:
            literal = model.NewBoolVar(f"x_{orbit_index}_{shift}")
            choose[orbit_index, shift] = literal
            literals.append(literal)
            phase = (-shift) % P
            cross_weight = (
                int(phase not in others_i)
                + int(phase not in others_j)
            )
            tie_weight = (
                rng.randrange(random_tiebreak + 1)
                if random_tiebreak
                else 0
            )
            objective_terms.append(
                (1000 * cross_weight + tie_weight) * literal
            )
            if phase == state[fixed_pair][orbit_index]:
                model.AddHint(literal, 1)
        model.AddExactlyOne(literals)

    for edge, values in occurrences.items():
        model.AddExactlyOne(
            [choose[orbit_index, shift] for orbit_index, shift in values]
        )

    model.Maximize(sum(objective_terms))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 10_000
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.StatusName(status), -1, None

    phases = []
    for orbit_index, shifts in domains.items():
        selected = [
            shift
            for shift in shifts
            if solver.Value(choose[orbit_index, shift])
        ]
        assert len(selected) == 1
        phases.append((-selected[0]) % P)
    certificate = {f"{i},{j}": phases}
    verify_single_fixed_pair(certificate, fixed_pair)
    return solver.StatusName(status), round(solver.ObjectiveValue()), phases


def optimize_two_incident_pairs(
    state: State,
    golf,
    centre: int,
    outer_left: int,
    outer_right: int,
    *,
    seconds: float,
    seed: int,
    random_tiebreak: int,
) -> tuple[str, tuple[list[int], list[int]] | None]:
    """Jointly re-solve two rows sharing one fixed vertex.

    The shared cross group is nonlinear in the two new phases: equal new
    phases contribute only one distinct value.  Explicit ``seen`` Booleans
    encode that OR exactly, allowing this move to escape one-row optima.
    """
    left_pair = incident_pair(centre, outer_left)
    right_pair = incident_pair(centre, outer_right)
    pairs = (left_pair, right_pair)
    domains_by_pair = {}
    occurrences_by_pair = {}
    for fixed_pair in pairs:
        domains, occurrences = slice_domains_and_occurrences(
            golf, fixed_pair
        )
        domains_by_pair[fixed_pair] = domains
        occurrences_by_pair[fixed_pair] = occurrences

    model = cp_model.CpModel()
    choose = {}
    rng = random.Random(seed)
    tie_terms = []
    outer_terms = []
    for fixed_pair, outer in (
        (left_pair, outer_left),
        (right_pair, outer_right),
    ):
        for orbit_index, shifts in domains_by_pair[fixed_pair].items():
            literals = []
            other_outer_phases = {
                state[incident_pair(outer, other)][orbit_index]
                for other in FIXED
                if other not in fixed_pair
            }
            for shift in shifts:
                literal = model.NewBoolVar(
                    f"x_{fixed_pair[0]}_{fixed_pair[1]}_"
                    f"{orbit_index}_{shift}"
                )
                choose[fixed_pair + (orbit_index, shift)] = literal
                literals.append(literal)
                phase = (-shift) % P
                if phase not in other_outer_phases:
                    outer_terms.append(literal)
                if random_tiebreak:
                    tie_terms.append(
                        rng.randrange(random_tiebreak + 1) * literal
                    )
                if phase == state[fixed_pair][orbit_index]:
                    model.AddHint(literal, 1)
            model.AddExactlyOne(literals)

        for values in occurrences_by_pair[fixed_pair].values():
            model.AddExactlyOne(
                [
                    choose[fixed_pair + (orbit_index, shift)]
                    for orbit_index, shift in values
                ]
            )

    shared_terms = []
    for orbit_index in range(len(TRIPLE_REPRESENTATIVES)):
        base = {
            state[incident_pair(centre, other)][orbit_index]
            for other in FIXED
            if other not in (centre, outer_left, outer_right)
        }
        for phase in POINTS:
            if phase in base:
                continue
            candidate_literals = []
            shift = (-phase) % P
            for fixed_pair in pairs:
                literal = choose.get(
                    fixed_pair + (orbit_index, shift)
                )
                if literal is not None:
                    candidate_literals.append(literal)
            if not candidate_literals:
                continue
            if len(candidate_literals) == 1:
                shared_terms.append(candidate_literals[0])
            else:
                seen = model.NewBoolVar(
                    f"seen_{centre}_{orbit_index}_{phase}"
                )
                model.AddMaxEquality(seen, candidate_literals)
                shared_terms.append(seen)

    model.Maximize(
        1000 * (sum(outer_terms) + sum(shared_terms))
        + sum(tie_terms)
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 20_000
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.StatusName(status), None

    answer = []
    for fixed_pair in pairs:
        phases = []
        for orbit_index, shifts in domains_by_pair[fixed_pair].items():
            selected = [
                shift
                for shift in shifts
                if solver.Value(
                    choose[fixed_pair + (orbit_index, shift)]
                )
            ]
            assert len(selected) == 1
            phases.append((-selected[0]) % P)
        verify_single_fixed_pair(
            {f"{fixed_pair[0]},{fixed_pair[1]}": phases},
            fixed_pair,
        )
        answer.append(phases)
    return solver.StatusName(status), (answer[0], answer[1])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sweeps", type=int, default=5)
    parser.add_argument("--seconds-per-pair", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument(
        "--random-tiebreak",
        type=int,
        default=10,
        help="secondary random coefficient below the 1000-point exact score",
    )
    parser.add_argument("--accept-equal", action="store_true")
    parser.add_argument(
        "--two-row-steps",
        type=int,
        default=0,
        help="after the one-row sweeps, try this many adjacent two-row moves",
    )
    parser.add_argument(
        "--seconds-per-two-row",
        type=float,
        default=5.0,
    )
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    state = load_state(args.source)
    golf = construct_golf17()
    rng = random.Random(args.seed)
    score = cross_score(state)
    print(
        json.dumps(
            {
                "status": "START",
                "cross_score": score,
                "target": 8400,
                "all_105_slices_exact": True,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    if args.audit_only:
        sha = write_state(args.output, state)
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "phase_sha256": sha,
                    "cross_score": score,
                    "scope": "105 exact slices; cross compatibility not assumed",
                },
                sort_keys=True,
            )
        )
        return

    for sweep in range(args.sweeps):
        order = list(FIXED_PAIRS)
        rng.shuffle(order)
        order.sort(key=lambda pair: -pair_pressure(state, pair))
        accepted = 0
        for step, fixed_pair in enumerate(order):
            old_phases = state[fixed_pair]
            old_score = score
            status, _, phases = optimize_pair(
                state,
                golf,
                fixed_pair,
                seconds=args.seconds_per_pair,
                seed=rng.randrange(1, 2**31),
                random_tiebreak=args.random_tiebreak,
            )
            if phases is None:
                continue
            state[fixed_pair] = phases
            candidate_score = cross_score(state)
            changed = phases != old_phases
            if candidate_score < old_score or (
                candidate_score == old_score
                and (not args.accept_equal or not changed)
            ):
                state[fixed_pair] = old_phases
                continue
            score = candidate_score
            accepted += 1
            sha = write_state(args.output, state)
            print(
                json.dumps(
                    {
                        "status": status,
                        "sweep": sweep,
                        "step": step,
                        "pair": list(fixed_pair),
                        "old_cross_score": old_score,
                        "cross_score": score,
                        "phase_sha256": sha,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            if score == 8400:
                payload = dump_state(state)
                verify_joint_compatibility(payload)
                print(
                    json.dumps(
                        {
                            "status": "FEASIBLE_JOINT_LAYER",
                            "cross_score": score,
                            "phase_sha256": sha,
                            "semantic_joint_verifier": "PASS",
                            "scope": (
                                "fixed-Wallis C17 layer |R|=2 only; "
                                "not full problem 835"
                            ),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
                return
        print(
            json.dumps(
                {
                    "status": "SWEEP",
                    "sweep": sweep,
                    "accepted": accepted,
                    "cross_score": score,
                    "target": 8400,
                },
                sort_keys=True,
            ),
            flush=True,
        )

    wedges = [
        (centre, outer_left, outer_right)
        for centre in FIXED
        for outer_left, outer_right in combinations(
            [other for other in FIXED if other != centre],
            2,
        )
    ]
    for step in range(args.two_row_steps):
        rng.shuffle(wedges)
        wedges.sort(
            key=lambda wedge: -(
                pair_pressure(
                    state,
                    incident_pair(wedge[0], wedge[1]),
                )
                + pair_pressure(
                    state,
                    incident_pair(wedge[0], wedge[2]),
                )
            )
        )
        # Randomize among the most pressured wedges to avoid repeatedly
        # solving the identical local optimum.
        centre, outer_left, outer_right = rng.choice(wedges[:50])
        left_pair = incident_pair(centre, outer_left)
        right_pair = incident_pair(centre, outer_right)
        old_left = state[left_pair]
        old_right = state[right_pair]
        old_score = score
        status, candidate = optimize_two_incident_pairs(
            state,
            golf,
            centre,
            outer_left,
            outer_right,
            seconds=args.seconds_per_two_row,
            seed=rng.randrange(1, 2**31),
            random_tiebreak=args.random_tiebreak,
        )
        if candidate is None:
            continue
        state[left_pair], state[right_pair] = candidate
        candidate_score = cross_score(state)
        changed = candidate != (old_left, old_right)
        if candidate_score < old_score or (
            candidate_score == old_score
            and (not args.accept_equal or not changed)
        ):
            state[left_pair] = old_left
            state[right_pair] = old_right
            continue
        score = candidate_score
        sha = write_state(args.output, state)
        print(
            json.dumps(
                {
                    "status": status,
                    "two_row_step": step,
                    "wedge": [centre, outer_left, outer_right],
                    "old_cross_score": old_score,
                    "cross_score": score,
                    "phase_sha256": sha,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if score == 8400:
            payload = dump_state(state)
            verify_joint_compatibility(payload)
            print(
                json.dumps(
                    {
                        "status": "FEASIBLE_JOINT_LAYER",
                        "cross_score": score,
                        "phase_sha256": sha,
                        "semantic_joint_verifier": "PASS",
                        "scope": (
                            "fixed-Wallis C17 layer |R|=2 only; "
                            "not full problem 835"
                        ),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            return

    sha = write_state(args.output, state)
    print(
        json.dumps(
            {
                "status": "NO_JOINT_WITNESS",
                "cross_score": score,
                "target": 8400,
                "phase_sha256": sha,
                "mathematical_status": "heuristic only",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
