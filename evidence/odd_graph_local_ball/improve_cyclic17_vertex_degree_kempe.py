#!/usr/bin/env python3
"""Kempe local search for the cyclic Wallis vertex-degree relaxation.

A move swaps two phase colours on one alternating component of one
moving-triple orbit's properly edge-coloured K_15.  It is accepted only when
all swapped phase values remain in their exact zero-factor lists.  Therefore
every state preserves all phase domains and cross constraints.  The objective
is the total L1 deviation from degree 8 at moving point 0 and degree 7 at
every other moving point.

Degree L1 zero is only a witness for the necessary degree relaxation.  This
script omits residual-edge collision constraints and does not solve the full
radius-five quotient or Erdos--Rosenfeld problem 835.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path


BALL = Path(__file__).resolve().parent
EVIDENCE = BALL.parent
for directory in (str(BALL), str(EVIDENCE)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from global_latin_audit import construct_golf17
from improve_radius5_golf_cyclic_slice_lns import (
    audit_static,
    domains_for_seed,
    dump_phases,
    load_state,
)
from search_cyclic17_vertex_degree_sat import verify_relaxation
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    POINTS,
    REPRESENTATIVES,
    translate,
)


def make_degrees(state):
    answer = {fixed_pair: [0] * P for fixed_pair in FIXED_PAIRS}
    for fixed_pair in FIXED_PAIRS:
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            triple = translate(
                representative,
                state[fixed_pair + (orbit_index,)],
            )
            for point in triple:
                answer[fixed_pair][point] += 1
    return answer


def degree_l1(degrees) -> int:
    return sum(
        abs(value - (8 if point == 0 else 7))
        for values in degrees.values()
        for point, value in enumerate(values)
    )


def components_for_colours(
    state, orbit_index: int, first: int, second: int
):
    edges = [
        fixed_pair
        for fixed_pair in FIXED_PAIRS
        if state[fixed_pair + (orbit_index,)] in (first, second)
    ]
    incident = defaultdict(list)
    for edge in edges:
        for vertex in edge:
            incident[vertex].append(edge)
    unseen = set(edges)
    while unseen:
        seed = unseen.pop()
        component = [seed]
        stack = [seed]
        while stack:
            edge = stack.pop()
            for vertex in edge:
                for other in incident[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.append(other)
                        stack.append(other)
        yield tuple(component)


def move_delta(
    state,
    degrees,
    orbit_index,
    first,
    second,
    component,
) -> int:
    representative = REPRESENTATIVES[orbit_index]
    delta = 0
    for fixed_pair in component:
        old_shift = state[fixed_pair + (orbit_index,)]
        new_shift = second if old_shift == first else first
        old_triple = set(translate(representative, old_shift))
        new_triple = set(translate(representative, new_shift))
        values = degrees[fixed_pair]
        for point in old_triple | new_triple:
            old_deviation = abs(
                values[point] - (8 if point == 0 else 7)
            )
            new_value = (
                values[point]
                - int(point in old_triple)
                + int(point in new_triple)
            )
            new_deviation = abs(
                new_value - (8 if point == 0 else 7)
            )
            delta += new_deviation - old_deviation
    return delta


def apply_move(
    state,
    degrees,
    orbit_index,
    first,
    second,
    component,
) -> None:
    representative = REPRESENTATIVES[orbit_index]
    for fixed_pair in component:
        key = fixed_pair + (orbit_index,)
        old_shift = state[key]
        new_shift = second if old_shift == first else first
        old_triple = translate(representative, old_shift)
        new_triple = translate(representative, new_shift)
        values = degrees[fixed_pair]
        for point in old_triple:
            values[point] -= 1
        for point in new_triple:
            values[point] += 1
        state[key] = new_shift


def valid_moves(state, domains, degrees):
    for orbit_index in range(len(REPRESENTATIVES)):
        for first, second in combinations(POINTS, 2):
            for component in components_for_colours(
                state, orbit_index, first, second
            ):
                if not all(
                    (
                        second
                        if state[
                            fixed_pair + (orbit_index,)
                        ]
                        == first
                        else first
                    )
                    in domains[fixed_pair + (orbit_index,)]
                    for fixed_pair in component
                ):
                    continue
                yield (
                    move_delta(
                        state,
                        degrees,
                        orbit_index,
                        first,
                        second,
                        component,
                    ),
                    orbit_index,
                    first,
                    second,
                    component,
                )


def audit_degrees(state, degrees) -> int:
    rebuilt = make_degrees(state)
    assert rebuilt == degrees
    assert all(sum(values) == 120 for values in degrees.values())
    return degree_l1(degrees)


def write_seed(path: Path, state) -> str:
    encoded = (
        json.dumps(dump_phases(state), indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.write_bytes(encoded)
    return hashlib.sha256(encoded).hexdigest()


def greedy_climb(
    state,
    domains,
    degrees,
    objective,
    *,
    steps: int,
    rng: random.Random,
):
    accepted = 0
    for _ in range(steps):
        moves = list(valid_moves(state, domains, degrees))
        best_delta = min(
            (move[0] for move in moves), default=0
        )
        if best_delta >= 0:
            break
        candidates = [
            move for move in moves if move[0] == best_delta
        ]
        (
            delta,
            orbit_index,
            first,
            second,
            component,
        ) = rng.choice(candidates)
        apply_move(
            state,
            degrees,
            orbit_index,
            first,
            second,
            component,
        )
        objective += delta
        accepted += 1
        if objective == 0:
            break
    return objective, accepted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--greedy-steps", type=int, default=500)
    parser.add_argument("--restarts", type=int, default=30)
    parser.add_argument("--perturbations", type=int, default=12)
    parser.add_argument("--uphill", type=int, default=4)
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    domains = domains_for_seed(construct_golf17())
    state = load_state(args.source)
    audit_static(state, domains)
    degrees = make_degrees(state)
    objective = audit_degrees(state, degrees)
    initial = objective
    print(
        json.dumps(
            {"status": "START", "degree_l1": objective},
            sort_keys=True,
        ),
        flush=True,
    )

    objective, accepted = greedy_climb(
        state,
        domains,
        degrees,
        objective,
        steps=args.greedy_steps,
        rng=rng,
    )
    best_state = dict(state)
    best_degrees = {
        fixed_pair: values[:]
        for fixed_pair, values in degrees.items()
    }
    best = objective
    print(
        json.dumps(
            {
                "status": "GREEDY",
                "accepted": accepted,
                "degree_l1": best,
            },
            sort_keys=True,
        ),
        flush=True,
    )

    for restart in range(1, args.restarts + 1):
        state = dict(best_state)
        degrees = {
            fixed_pair: values[:]
            for fixed_pair, values in best_degrees.items()
        }
        objective = best
        for _ in range(args.perturbations):
            moves = list(valid_moves(state, domains, degrees))
            if not moves:
                break
            minimum = min(move[0] for move in moves)
            candidates = [
                move
                for move in moves
                if move[0] <= max(args.uphill, minimum + 4)
            ]
            (
                delta,
                orbit_index,
                first,
                second,
                component,
            ) = rng.choice(candidates)
            apply_move(
                state,
                degrees,
                orbit_index,
                first,
                second,
                component,
            )
            objective += delta

        objective, _ = greedy_climb(
            state,
            domains,
            degrees,
            objective,
            steps=args.greedy_steps,
            rng=rng,
        )
        if objective < best:
            audit_static(state, domains)
            assert audit_degrees(state, degrees) == objective
            best = objective
            best_state = dict(state)
            best_degrees = {
                fixed_pair: values[:]
                for fixed_pair, values in degrees.items()
            }
            sha = write_seed(args.output, best_state)
            print(
                json.dumps(
                    {
                        "status": "IMPROVED",
                        "restart": restart,
                        "degree_l1": best,
                        "phase_sha256": sha,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        elif restart % 5 == 0:
            print(
                json.dumps(
                    {
                        "status": "RESTART",
                        "restart": restart,
                        "local_degree_l1": objective,
                        "best_degree_l1": best,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        if best == 0:
            break

    audit_static(best_state, domains)
    assert audit_degrees(best_state, best_degrees) == best
    sha = write_seed(args.output, best_state)
    report = {
        "status": "DONE",
        "initial_degree_l1": initial,
        "degree_l1": best,
        "phase_sha256": sha,
        "semantic_relaxation_verifier": "NOT_RUN",
    }
    if best == 0:
        phases = dump_phases(best_state)
        verify_relaxation(
            phases,
            {
                key: tuple(value)
                for key, value in domains.items()
            },
        )
        report.update(
            {
                "status": "FEASIBLE_RELAXATION",
                "semantic_relaxation_verifier": "PASS",
            }
        )
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
