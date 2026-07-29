#!/usr/bin/env python3
"""Improve a cyclic radius-five phase seed by exact Kempe switches.

Every state maintained by this heuristic satisfies:

* the static zero-leave restrictions in all 105 prescribed-link slices; and
* the 600 orbit-wise K_15 edge-colouring constraints that become shared N.

A move swaps two phase colours on one connected alternating component of one
orbit's properly edge-coloured K_15.  It is accepted only when every swapped
edge still belongs to its exact list.  Thus the heuristic never relaxes those
constraints.  Its objective is the number of residual colour-zero edges
covered at least once.  The maximum 12,600 is equivalent to exact radius-five
feasibility and is checked through the canonical semantic verifier.

Any score below 12,600 is only a search seed, not mathematical evidence.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parents[1]
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))
from convert_cyclic17_r3_to_radius5 import convert
from global_latin_audit import construct_golf17


P = 17
POINTS = tuple(range(P))
SQUARES = tuple(range(15))
FIXED_PAIRS = tuple(combinations(SQUARES, 2))
MOVING_PAIRS = tuple(combinations(POINTS, 2))
MOVING_TRIPLES = tuple(combinations(POINTS, 3))


def translate(subset: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return tuple(sorted((x + amount) % P for x in subset))


def triple_representatives() -> list[tuple[int, int, int]]:
    representatives = []
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


def load_state(source: Path):
    payload = json.loads(source.read_text(encoding="utf-8"))
    assert set(payload) == {f"{i},{j}" for i, j in FIXED_PAIRS}
    state = {}
    for i, j in FIXED_PAIRS:
        phases = payload[f"{i},{j}"]
        assert (
            isinstance(phases, list)
            and len(phases) == 40
            and all(isinstance(value, int) and 0 <= value < P for value in phases)
        )
        for orbit_index, phase in enumerate(phases):
            state[i, j, orbit_index] = (-phase) % P
    return state


def dump_phases(state) -> dict[str, list[int]]:
    return {
        f"{i},{j}": [
            (-state[i, j, orbit_index]) % P
            for orbit_index in range(len(REPRESENTATIVES))
        ]
        for i, j in FIXED_PAIRS
    }


def make_domains(golf):
    domains = {}
    for i, j in FIXED_PAIRS:
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            domains[i, j, orbit_index] = {
                shift
                for shift in POINTS
                if all(
                    golf[i][x][y] != 0 and golf[j][x][y] != 0
                    for x, y in combinations(
                        translate(representative, shift), 2
                    )
                )
            }
    return domains


def make_coverage(state):
    coverage = {}
    for i, j in FIXED_PAIRS:
        counts = Counter()
        for orbit_index, representative in enumerate(REPRESENTATIVES):
            triple = translate(
                representative, state[i, j, orbit_index]
            )
            counts.update(combinations(triple, 2))
        coverage[i, j] = counts
    return coverage


def audit_state(state, domains, coverage) -> tuple[int, int]:
    for key, value in state.items():
        assert value in domains[key]
    for orbit_index in range(len(REPRESENTATIVES)):
        for fixed_point in SQUARES:
            values = {
                state[
                    min(fixed_point, other),
                    max(fixed_point, other),
                    orbit_index,
                ]
                for other in SQUARES
                if other != fixed_point
            }
            assert len(values) == 14
    objective = sum(
        sum(value > 0 for value in coverage[fixed_pair].values())
        for fixed_pair in FIXED_PAIRS
    )
    exact_slices = sum(
        len(coverage[fixed_pair]) == 120
        and set(coverage[fixed_pair].values()) == {1}
        for fixed_pair in FIXED_PAIRS
    )
    return objective, exact_slices


def components_for_colours(state, orbit_index: int, first: int, second: int):
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


def move_delta(state, coverage, orbit_index, first, second, component):
    representative = REPRESENTATIVES[orbit_index]
    delta = 0
    for fixed_pair in component:
        old = state[fixed_pair + (orbit_index,)]
        new = second if old == first else first
        old_edges = set(combinations(translate(representative, old), 2))
        new_edges = set(combinations(translate(representative, new), 2))
        counts = coverage[fixed_pair]
        delta += sum(
            (
                counts[edge]
                - int(edge in old_edges)
                + int(edge in new_edges)
                > 0
            )
            - (counts[edge] > 0)
            for edge in old_edges | new_edges
        )
    return delta


def apply_move(state, coverage, orbit_index, first, second, component):
    representative = REPRESENTATIVES[orbit_index]
    for fixed_pair in component:
        key = fixed_pair + (orbit_index,)
        old = state[key]
        new = second if old == first else first
        old_edges = tuple(combinations(translate(representative, old), 2))
        new_edges = tuple(combinations(translate(representative, new), 2))
        counts = coverage[fixed_pair]
        for edge in old_edges:
            counts[edge] -= 1
            if counts[edge] == 0:
                del counts[edge]
        counts.update(new_edges)
        state[key] = new


def valid_moves(state, domains, coverage):
    for orbit_index in range(len(REPRESENTATIVES)):
        for first, second in combinations(POINTS, 2):
            for component in components_for_colours(
                state, orbit_index, first, second
            ):
                if not all(
                    (
                        second
                        if state[fixed_pair + (orbit_index,)] == first
                        else first
                    )
                    in domains[fixed_pair + (orbit_index,)]
                    for fixed_pair in component
                ):
                    continue
                yield (
                    move_delta(
                        state,
                        coverage,
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--greedy-steps", type=int, default=500)
    parser.add_argument(
        "--restarts",
        type=int,
        default=0,
        help="iterated local-search restarts after the first greedy climb",
    )
    parser.add_argument("--perturbations", type=int, default=12)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument(
        "--certificate",
        type=Path,
        help="write canonical full certificate only if objective reaches 12600",
    )
    args = parser.parse_args()

    random.seed(args.seed)
    golf = construct_golf17()
    state = load_state(args.source)
    domains = make_domains(golf)
    coverage = make_coverage(state)
    objective, exact_slices = audit_state(state, domains, coverage)
    print(
        f"initial objective={objective}/12600 exact_slices={exact_slices}",
        flush=True,
    )

    accepted = 0
    for step in range(args.greedy_steps):
        moves = list(valid_moves(state, domains, coverage))
        best_delta = max((move[0] for move in moves), default=0)
        if best_delta <= 0:
            print(f"greedy local optimum after {accepted} switches", flush=True)
            break
        candidates = [move for move in moves if move[0] == best_delta]
        delta, orbit_index, first, second, component = random.choice(candidates)
        apply_move(
            state,
            coverage,
            orbit_index,
            first,
            second,
            component,
        )
        objective += delta
        accepted += 1
        if accepted % 10 == 0 or objective == 12600:
            _, exact_slices = audit_state(state, domains, coverage)
            print(
                f"switches={accepted} objective={objective}/12600 "
                f"exact_slices={exact_slices}",
                flush=True,
            )
        if objective == 12600:
            break

    best_state = dict(state)
    best_coverage = {
        fixed_pair: Counter(counts)
        for fixed_pair, counts in coverage.items()
    }
    best_objective = objective

    for restart in range(1, args.restarts + 1):
        state = dict(best_state)
        coverage = {
            fixed_pair: Counter(counts)
            for fixed_pair, counts in best_coverage.items()
        }
        objective = best_objective

        # Move through a few flat or mildly downhill alternating components.
        # Every move still preserves the exact hard constraints.
        for _ in range(args.perturbations):
            moves = list(valid_moves(state, domains, coverage))
            if not moves:
                break
            threshold = max(-3, max(move[0] for move in moves) - 2)
            candidates = [move for move in moves if move[0] >= threshold]
            delta, orbit_index, first, second, component = random.choice(candidates)
            apply_move(
                state,
                coverage,
                orbit_index,
                first,
                second,
                component,
            )
            objective += delta

        # Greedily climb to the next Kempe local optimum.
        for _ in range(args.greedy_steps):
            moves = list(valid_moves(state, domains, coverage))
            best_delta = max((move[0] for move in moves), default=0)
            if best_delta <= 0:
                break
            candidates = [move for move in moves if move[0] == best_delta]
            delta, orbit_index, first, second, component = random.choice(candidates)
            apply_move(
                state,
                coverage,
                orbit_index,
                first,
                second,
                component,
            )
            objective += delta
            if objective == 12600:
                break

        if objective > best_objective:
            best_objective = objective
            best_state = dict(state)
            best_coverage = {
                fixed_pair: Counter(counts)
                for fixed_pair, counts in coverage.items()
            }
            print(
                f"restart={restart} new_best={best_objective}/12600",
                flush=True,
            )
        elif restart % 5 == 0:
            print(
                f"restart={restart} local={objective}/12600 "
                f"best={best_objective}/12600",
                flush=True,
            )
        if best_objective == 12600:
            break

    state = best_state
    coverage = best_coverage
    objective = best_objective

    objective_check, exact_slices = audit_state(state, domains, coverage)
    assert objective_check == objective
    phases = dump_phases(state)
    args.output.write_text(
        json.dumps(phases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"final objective={objective}/12600 exact_slices={exact_slices}",
        flush=True,
    )
    print(f"wrote {args.output}", flush=True)
    if objective == 12600:
        payload = convert(phases)
        if args.certificate is not None:
            args.certificate.write_text(
                json.dumps(payload, sort_keys=True, separators=(",", ":"))
                + "\n",
                encoding="utf-8",
            )
            print(f"wrote {args.certificate}", flush=True)
        print("FULL SEMANTIC RADIUS-FIVE VERIFICATION: PASS", flush=True)
    else:
        print("scope: heuristic seed only; no radius-five certificate", flush=True)


if __name__ == "__main__":
    main()
