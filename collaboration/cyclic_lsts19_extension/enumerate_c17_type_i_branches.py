#!/usr/bin/env python3
"""Enumerate all valid type-(i) branches of the C17 exact-cover instance."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from generate_c17_equivariant_cnf import orbit_representatives
from search_c17_equivariant_exact_cover import build_exact_cover


def enumerate_branches() -> tuple[tuple[int, ...], ...]:
    columns, rows = build_exact_cover()
    representatives = orbit_representatives(4)
    type_i_orbits = [
        orbit
        for orbit, block in enumerate(representatives)
        if 17 in block and 18 in block
    ]
    if len(type_i_orbits) != 8:
        raise AssertionError("wrong type-(i) orbit count")
    options = {orbit: tuple(sorted(columns[orbit])) for orbit in type_i_orbits}
    branches = []

    def recurse(position: int, used: set[int], chosen: list[int]) -> None:
        if position == len(type_i_orbits):
            branches.append(tuple(chosen))
            return
        orbit = type_i_orbits[position]
        for row in options[orbit]:
            covered = set(rows[row])
            if covered & used:
                continue
            chosen.append(row)
            recurse(position + 1, used | covered, chosen)
            chosen.pop()

    recurse(0, set(), [])
    result = tuple(sorted(branches))
    if len(result) != 1_326 or len(set(result)) != 1_326:
        raise AssertionError("type-(i) branch census is not 1326")
    opus_branch = (1926, 3017, 3532, 3739, 3810, 3840, 3849, 3870)
    if opus_branch not in result:
        raise AssertionError("audited Opus witness is absent from the census")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    branches = enumerate_branches()
    content = (
        "\n".join(" ".join(map(str, branch)) for branch in branches) + "\n"
    ).encode("ascii")
    args.output.write_bytes(content)
    print(f"branches={len(branches)}")
    print(f"SHA-256: {hashlib.sha256(content).hexdigest()}")
    print(f"first: {' '.join(map(str, branches[0]))}")
    print(f"last: {' '.join(map(str, branches[-1]))}")
    opus_branch = (1926, 3017, 3532, 3739, 3810, 3840, 3849, 3870)
    print(f"Opus branch index: {branches.index(opus_branch)}")


if __name__ == "__main__":
    main()
