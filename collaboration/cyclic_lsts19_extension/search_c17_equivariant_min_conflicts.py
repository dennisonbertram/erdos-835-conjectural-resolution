#!/usr/bin/env python3
"""Heuristic witness search for the exact C17-equivariant extension CSP.

Any emitted witness is checked by the independent semantic verifier.  Failure
to find one has no mathematical status.
"""

from __future__ import annotations

import argparse
import random
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from evidence.verify_defect_cross_link_lsts19 import (  # noqa: E402
    construct_lsts19,
)
from generate_c17_equivariant_cnf import (  # noqa: E402
    COLOURS,
    P,
    POINTS,
    canonical,
    orbit_representatives,
    representative_and_shift,
    variable,
)


def build_csp() -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[tuple[int, int], ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    link = construct_lsts19()
    blocks = orbit_representatives(4)
    triples = orbit_representatives(3)
    block_index = {block: index for index, block in enumerate(blocks)}
    stars = []
    domains = [set(COLOURS) for _ in blocks]
    affected: list[set[int]] = [set() for _ in blocks]

    for star_index, triple in enumerate(triples):
        entries = []
        for point in POINTS:
            if point not in triple:
                entries.append(
                    representative_and_shift(canonical(triple + (point,)), block_index)
                )
        stars.append(tuple(entries))
        forbidden = link[triple]
        for orbit, shift in entries:
            domains[orbit].discard((forbidden - shift) % P)
            affected[orbit].add(star_index)

    if any(len(domain) != 13 for domain in domains):
        raise AssertionError("every orbit must have exactly thirteen phases")
    return (
        blocks,
        tuple(stars),
        tuple(tuple(sorted(domain)) for domain in domains),
        tuple(tuple(sorted(indices)) for indices in affected),
    )


def star_penalty(
    assignment: list[int],
    entries: tuple[tuple[int, int], ...],
    changed_orbit: int = -1,
    changed_phase: int = -1,
) -> int:
    counts = [0] * P
    for orbit, shift in entries:
        phase = changed_phase if orbit == changed_orbit else assignment[orbit]
        counts[(phase + shift) % P] += 1
    return sum(count * (count - 1) // 2 for count in counts)


def conflicted_orbits(
    assignment: list[int], entries: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    by_colour: list[list[int]] = [[] for _ in COLOURS]
    for orbit, shift in entries:
        by_colour[(assignment[orbit] + shift) % P].append(orbit)
    return tuple(
        sorted({orbit for group in by_colour if len(group) > 1 for orbit in group})
    )


def write_model(path: Path, assignment: list[int]) -> None:
    literals = [variable(orbit, phase) for orbit, phase in enumerate(assignment)]
    path.write_text(
        "s SATISFIABLE\n" + "v " + " ".join(map(str, literals)) + " 0\n",
        encoding="ascii",
    )


def search(
    seconds: float,
    seed: int,
    noise: float,
    plateau: int,
    output: Path,
) -> bool:
    blocks, stars, domains, affected = build_csp()
    rng = random.Random(seed)
    deadline = time.monotonic() + seconds
    best_global = 10**9
    restarts = 0
    steps = 0

    while time.monotonic() < deadline:
        restarts += 1
        assignment = [rng.choice(domain) for domain in domains]
        penalties = [star_penalty(assignment, entries) for entries in stars]
        stagnant = 0

        while stagnant < plateau and time.monotonic() < deadline:
            steps += 1
            total = sum(penalties)
            if total < best_global:
                best_global = total
                print(
                    f"seed={seed} best={best_global} restart={restarts} steps={steps}",
                    file=sys.stderr,
                    flush=True,
                )
            if total == 0:
                # Direct local verification before emitting a theorem candidate.
                if any(star_penalty(assignment, entries) != 0 for entries in stars):
                    raise AssertionError("zero objective failed direct replay")
                if len(assignment) != len(blocks):
                    raise AssertionError("assignment has wrong orbit count")
                write_model(output, assignment)
                print(
                    f"SAT_CANDIDATE seed={seed} restarts={restarts} steps={steps}",
                    flush=True,
                )
                return True

            bad_stars = [index for index, penalty in enumerate(penalties) if penalty]
            star_index = rng.choice(bad_stars)
            choices = conflicted_orbits(assignment, stars[star_index])
            orbit = rng.choice(choices)
            current = assignment[orbit]
            old_local = sum(penalties[index] for index in affected[orbit])

            scored = []
            for phase in domains[orbit]:
                new_local = sum(
                    star_penalty(assignment, stars[index], orbit, phase)
                    for index in affected[orbit]
                )
                scored.append((new_local, phase))
            minimum = min(score for score, _ in scored)
            if rng.random() < noise:
                new_phase = rng.choice(domains[orbit])
            else:
                new_phase = rng.choice(
                    [phase for score, phase in scored if score == minimum]
                )

            assignment[orbit] = new_phase
            for index in affected[orbit]:
                penalties[index] = star_penalty(assignment, stars[index])
            new_local = sum(penalties[index] for index in affected[orbit])
            stagnant = 0 if new_local < old_local else stagnant + 1
            if new_phase == current:
                stagnant += 1

    print(
        f"UNKNOWN seed={seed} best={best_global} restarts={restarts} steps={steps}",
        flush=True,
    )
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--noise", type=float, default=0.04)
    parser.add_argument("--plateau", type=int, default=20_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 0 <= args.noise <= 1:
        raise ValueError("--noise must lie in [0,1]")
    found = search(
        args.seconds,
        args.seed,
        args.noise,
        args.plateau,
        args.output,
    )
    raise SystemExit(0 if found else 2)


if __name__ == "__main__":
    main()
