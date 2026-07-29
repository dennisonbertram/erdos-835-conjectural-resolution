#!/usr/bin/env python3
"""Exact CP-SAT completion search above an Etzion--Hartman subsystem.

Removing r of the verified fifteen systems leaves 15-r fixed systems and
q=r+2 unused extensions of every triple.  A completion to a large set is
therefore exactly a proper q-colouring of the residual graph, or equivalently
an all-different assignment on those q extensions of every triple.

UNSAT only rules out completion of the chosen fixed subsystem.  It is not a
universal nonexistence result for LS(3,4,20).
"""

from __future__ import annotations

import argparse
import itertools
from collections import defaultdict
from pathlib import Path

from ortools.sat.python import cp_model

from generate_eh_15_seed import BASE_SQS10, etzion_hartman_systems


def dls10_systems() -> list[set[tuple[int, ...]]]:
    """The verified ten-system doubling construction used by the C++ search."""
    n = 5
    latin = [[0] * 10 for _ in range(10)]
    for i in range(10):
        for j in range(10):
            if i < n and j < n:
                latin[i][j] = (i - j) % n
            elif i < n:
                latin[i][j] = n + (i + (j - n)) % n
            elif j < n:
                latin[i][j] = n + ((i - n) + j - 1) % n
            else:
                latin[i][j] = ((i - n) - (j - n)) % n

    systems = []
    for alpha in latin:
        inverse = [0] * 10
        for x, image in enumerate(alpha):
            inverse[image] = x
        system: set[tuple[int, ...]] = set()
        for base in BASE_SQS10:
            for singled in range(4):
                first = [10 + alpha[base[singled]]]
                second = [inverse[base[singled]]]
                for j in range(4):
                    if j == singled:
                        continue
                    first.append(base[j])
                    second.append(10 + base[j])
                system.add(tuple(sorted(first)))
                system.add(tuple(sorted(second)))
        for x in range(10):
            for y in range(x + 1, 10):
                system.add(tuple(sorted((x, y, 10 + alpha[x], 10 + alpha[y]))))
        assert len(system) == 285
        systems.append(system)

    used: set[tuple[int, ...]] = set()
    for system in systems:
        cover = defaultdict(int)
        for block in system:
            for triple in itertools.combinations(block, 3):
                cover[triple] += 1
        assert len(cover) == 1140
        assert set(cover.values()) == {1}
        assert not (used & system)
        used |= system
    return systems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--remove",
        type=int,
        nargs="+",
        default=(),
        metavar="C",
    )
    parser.add_argument(
        "--dls10",
        action="store_true",
        help="fix the ten-system doubling core (and do not use --remove)",
    )
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evidence/ls_3_4_20_witness.txt"),
    )
    parser.add_argument("--log", action="store_true")
    args = parser.parse_args()

    removed = tuple(sorted(args.remove))
    if args.dls10:
        if removed:
            parser.error("--dls10 does not accept --remove")
        systems = dls10_systems()
    else:
        if (
            len(set(removed)) != len(removed)
            or len(removed) < 1
            or len(removed) > 14
            or removed[0] < 0
            or removed[-1] >= 15
        ):
            parser.error(
                "--remove must name 1--14 distinct colours in 0,...,14"
            )
        systems = etzion_hartman_systems()
    kept = [
        system for colour, system in enumerate(systems)
        if colour not in removed
    ]
    q = 17 - len(kept)
    used = set().union(*kept)
    all_blocks = list(itertools.combinations(range(20), 4))
    residual = [block for block in all_blocks if block not in used]
    assert len(kept) == len(systems) - len(removed)
    assert len(residual) == q * 285
    index = {block: r for r, block in enumerate(residual)}

    by_triple: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for r, block in enumerate(residual):
        for triple in itertools.combinations(block, 3):
            by_triple[triple].append(r)
    assert len(by_triple) == 1140
    assert all(len(rows) == q for rows in by_triple.values())

    model = cp_model.CpModel()
    colour = [
        model.new_int_var(0, q - 1, f"c_{r}")
        for r in range(len(residual))
    ]
    for rows in by_triple.values():
        model.add_all_different([colour[r] for r in rows])

    # Quotient the global S_q colour symmetry using the lexicographically
    # first triple-star.
    reference = by_triple[(0, 1, 2)]
    for value, r in enumerate(reference):
        model.add(colour[r] == value)

    # The removed systems form exact colour classes and are useful search
    # hints.  The other two extensions receive arbitrary opposite
    # hints; hints need not satisfy every all-different constraint.
    removed_owner = {
        block: value
        for value, original_colour in enumerate(removed)
        for block in systems[original_colour]
    }
    for r, block in enumerate(residual):
        if block in removed_owner:
            model.add_hint(colour[r], removed_owner[block])
        else:
            hinted = (
                len(removed) + (sum(block) & 1)
                if len(removed) + 2 == q
                else sum(block) % q
            )
            model.add_hint(colour[r], hinted)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = args.log
    status = solver.solve(model)
    status_name = solver.status_name(status)
    print(
        f"remove={removed} status={status_name} "
        f"wall={solver.wall_time:.3f}s "
        f"conflicts={solver.num_conflicts} branches={solver.num_branches}"
    )

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise SystemExit(1)

    owner = {
        block: kept_colour
        for kept_colour, system in enumerate(kept)
        for block in system
    }
    for r, block in enumerate(residual):
        owner[block] = len(kept) + solver.value(colour[r])
    assert len(owner) == 4845

    # Internal check, deliberately separate from the output parser/verifier.
    for triple in itertools.combinations(range(20), 3):
        star = [
            owner[tuple(sorted(triple + (x,)))]
            for x in range(20)
            if x not in triple
        ]
        assert sorted(star) == list(range(17))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for block in all_blocks:
            handle.write("{} {} {} {} {}\n".format(*block, owner[block]))
    print(f"FOUND and internally verified; wrote {args.output}")


if __name__ == "__main__":
    main()
