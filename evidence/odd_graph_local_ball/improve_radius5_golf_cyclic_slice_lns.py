#!/usr/bin/env python3
"""Cross-preserving slice LNS for the cyclic radius-five phase model.

The input is a complete 4,200-phase seed satisfying the static zero-factor
lists and all 600 orbit-wise proper edge-colouring constraints on K_15.
One move chooses a fixed-point pair ``ij`` and reoptimizes all forty phases
of that slice simultaneously.  For each triple orbit, phases already used
by the other thirteen edges at either endpoint are removed from the domain.
Consequently every accepted move preserves the shared-N constraints exactly.

The local CP-SAT objective is the number of distinct residual edges covered
by the forty selected triples.  A score of 120 is an exact prescribed-link
slice; a global score of 105*120=12,600 is an exact joint radius-five layer.
At that value the script invokes the canonical converter and complete
73,457-vertex semantic verifier.  Any smaller score is only a search seed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from convert_cyclic17_r3_to_radius5 import convert
from global_latin_audit import construct_golf17
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    MOVING_EDGES,
    P,
    POINTS,
    REPRESENTATIVES,
    SQUARES,
    allowed_shifts,
    translate,
    zero_positions,
)


State = dict[tuple[int, int, int], int]


def load_state(source: Path) -> State:
    payload = json.loads(source.read_text(encoding="utf-8"))
    expected = {f"{i},{j}" for i, j in FIXED_PAIRS}
    if set(payload) != expected:
        raise ValueError("phase seed must contain all 105 fixed pairs")
    state: State = {}
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        if (
            not isinstance(phases, list)
            or len(phases) != len(REPRESENTATIVES)
        ):
            raise ValueError(f"invalid phase list for {i},{j}")
        for orbit_index, phase in enumerate(phases):
            if not isinstance(phase, int) or not 0 <= phase < P:
                raise ValueError(f"invalid phase at {i},{j},{orbit_index}")
            state[i, j, orbit_index] = (-phase) % P
    return state


def dump_phases(state: State) -> dict[str, list[int]]:
    return {
        f"{i},{j}": [
            (-state[i, j, orbit_index]) % P
            for orbit_index in range(len(REPRESENTATIVES))
        ]
        for i, j in FIXED_PAIRS
    }


def domains_for_seed(golf):
    zeros = zero_positions(golf)
    return {
        (i, j, orbit_index): frozenset(
            allowed_shifts((i, j), orbit_index, zeros)
        )
        for i, j in FIXED_PAIRS
        for orbit_index in range(len(REPRESENTATIVES))
    }


def audit_static(state: State, domains) -> None:
    if set(state) != {
        (i, j, orbit_index)
        for i, j in FIXED_PAIRS
        for orbit_index in range(len(REPRESENTATIVES))
    }:
        raise ValueError("state has the wrong cells")
    for key, value in state.items():
        if value not in domains[key]:
            raise ValueError(f"phase violates zero-factor list at {key}")
    for orbit_index in range(len(REPRESENTATIVES)):
        for fixed_point in SQUARES:
            values = [
                state[
                    min(fixed_point, other),
                    max(fixed_point, other),
                    orbit_index,
                ]
                for other in SQUARES
                if other != fixed_point
            ]
            if len(set(values)) != len(values):
                raise ValueError(
                    "seed violates shared-N proper edge-colouring at "
                    f"{fixed_point},{orbit_index}"
                )


def selected_triple(
    state: State,
    fixed_pair: tuple[int, int],
    orbit_index: int,
) -> tuple[int, int, int]:
    return translate(
        REPRESENTATIVES[orbit_index],
        state[fixed_pair + (orbit_index,)],
    )


def slice_coverage(
    state: State,
    fixed_pair: tuple[int, int],
) -> set[tuple[int, int]]:
    return {
        edge
        for orbit_index in range(len(REPRESENTATIVES))
        for edge in combinations(
            selected_triple(state, fixed_pair, orbit_index),
            2,
        )
    }


def slice_scores(state: State) -> dict[tuple[int, int], int]:
    return {
        fixed_pair: len(slice_coverage(state, fixed_pair))
        for fixed_pair in FIXED_PAIRS
    }


def local_domains(
    state: State,
    domains,
    fixed_pair: tuple[int, int],
) -> dict[int, tuple[int, ...]]:
    i, j = fixed_pair
    answer = {}
    for orbit_index in range(len(REPRESENTATIVES)):
        blocked = {
            state[
                min(endpoint, other),
                max(endpoint, other),
                orbit_index,
            ]
            for endpoint in fixed_pair
            for other in SQUARES
            if other not in fixed_pair
        }
        values = tuple(
            sorted(domains[i, j, orbit_index] - blocked)
        )
        current = state[i, j, orbit_index]
        if current not in values:
            raise AssertionError("current cross-compatible phase was blocked")
        answer[orbit_index] = values
    return answer


def optimize_slice(
    state: State,
    domains,
    fixed_pair: tuple[int, int],
    *,
    seconds: float,
    seed: int,
    hard_degrees: bool,
) -> tuple[str, int, dict[int, int] | None]:
    local = local_domains(state, domains, fixed_pair)
    model = cp_model.CpModel()
    choose: dict[tuple[int, int], cp_model.IntVar] = {}
    for orbit_index, values in local.items():
        literals = []
        for shift in values:
            literal = model.NewBoolVar(
                f"x_{orbit_index}_{shift}"
            )
            choose[orbit_index, shift] = literal
            literals.append(literal)
        model.AddExactlyOne(literals)
        model.AddHint(
            choose[
                orbit_index,
                state[fixed_pair + (orbit_index,)],
            ],
            1,
        )

    if hard_degrees:
        for vertex in POINTS:
            literals = [
                choose[orbit_index, shift]
                for orbit_index, values in local.items()
                for shift in values
                if vertex in translate(
                    REPRESENTATIVES[orbit_index],
                    shift,
                )
            ]
            model.Add(sum(literals) == (8 if vertex == 0 else 7))

    covered = {}
    for edge in MOVING_EDGES:
        literals = [
            choose[orbit_index, shift]
            for orbit_index, values in local.items()
            for shift in values
            if edge in combinations(
                translate(REPRESENTATIVES[orbit_index], shift),
                2,
            )
        ]
        indicator = model.NewBoolVar(f"covered_{edge[0]}_{edge[1]}")
        if literals:
            model.AddMaxEquality(indicator, literals)
        else:
            model.Add(indicator == 0)
        covered[edge] = indicator
    model.Maximize(sum(covered.values()))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 10_000
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver.StatusName(status), -1, None
    assignment = {}
    for orbit_index, values in local.items():
        selected = [
            shift
            for shift in values
            if solver.Value(choose[orbit_index, shift])
        ]
        if len(selected) != 1:
            raise AssertionError("local solver did not select one phase")
        assignment[orbit_index] = selected[0]
    return (
        solver.StatusName(status),
        round(solver.ObjectiveValue()),
        assignment,
    )


def write_seed(path: Path, state: State) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--sweeps", type=int, default=3)
    parser.add_argument("--seconds-per-slice", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--hard-degrees", action="store_true")
    parser.add_argument("--accept-equal", action="store_true")
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    golf = construct_golf17()
    domains = domains_for_seed(golf)
    state = load_state(args.source)
    audit_static(state, domains)
    scores = slice_scores(state)
    initial = sum(scores.values())
    print(
        json.dumps(
            {
                "status": "START",
                "global_coverage": initial,
                "exact_slices": sum(score == 120 for score in scores.values()),
                "hard_degrees": args.hard_degrees,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    if args.audit_only:
        sha = write_seed(args.output, state)
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "phase_sha256": sha,
                    "scope": "static lists and shared-N constraints only",
                },
                sort_keys=True,
            )
        )
        return

    for sweep in range(args.sweeps):
        order = list(FIXED_PAIRS)
        rng.shuffle(order)
        order.sort(key=scores.__getitem__)
        accepted = 0
        for step, fixed_pair in enumerate(order):
            old_score = scores[fixed_pair]
            status, new_score, assignment = optimize_slice(
                state,
                domains,
                fixed_pair,
                seconds=args.seconds_per_slice,
                seed=rng.randrange(1, 2**31),
                hard_degrees=args.hard_degrees,
            )
            if assignment is None:
                continue
            accept = new_score > old_score or (
                args.accept_equal
                and new_score == old_score
                and any(
                    assignment[orbit_index]
                    != state[fixed_pair + (orbit_index,)]
                    for orbit_index in range(len(REPRESENTATIVES))
                )
            )
            if not accept:
                continue
            for orbit_index, shift in assignment.items():
                state[fixed_pair + (orbit_index,)] = shift
            audit_static(state, domains)
            actual = len(slice_coverage(state, fixed_pair))
            if actual != new_score:
                raise AssertionError("local objective disagrees with coverage")
            scores[fixed_pair] = actual
            accepted += 1
            total = sum(scores.values())
            print(
                json.dumps(
                    {
                        "status": status,
                        "sweep": sweep,
                        "step": step,
                        "pair": list(fixed_pair),
                        "old": old_score,
                        "new": new_score,
                        "global_coverage": total,
                        "exact_slices": sum(
                            score == 120 for score in scores.values()
                        ),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            write_seed(args.output, state)
            if total == len(FIXED_PAIRS) * 120:
                phases = dump_phases(state)
                payload = convert(phases)
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
                print(
                    json.dumps(
                        {
                            "status": "SAT",
                            "semantic_verifier": "PASS",
                            "certificate_sha256_without_hash": payload[
                                "sha256_without_hash"
                            ],
                        },
                        sort_keys=True,
                    )
                )
                return
        print(
            json.dumps(
                {
                    "status": "SWEEP",
                    "sweep": sweep,
                    "accepted": accepted,
                    "global_coverage": sum(scores.values()),
                    "exact_slices": sum(
                        score == 120 for score in scores.values()
                    ),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if accepted == 0 and not args.accept_equal:
            break

    sha = write_seed(args.output, state)
    print(
        json.dumps(
            {
                "status": "DONE",
                "initial_coverage": initial,
                "global_coverage": sum(scores.values()),
                "exact_slices": sum(
                    score == 120 for score in scores.values()
                ),
                "phase_sha256": sha,
                "semantic_verifier": "NOT_RUN",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
