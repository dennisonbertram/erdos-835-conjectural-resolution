#!/usr/bin/env python3
"""Fix the audited cyclic LS(2,3,19) as one point link of LS(3,4,20).

The canonical unrestricted parent CNF already fixes the colour permutation on
the star of the triple {0,1,2}.  We map cyclic-link points 0,...,18 to parent
points 1,...,19 and relabel its seventeen colours so that its pair {0,1}
agrees with those existing units.  The remaining 952 point-link assignments
are then appended as unit clauses.

This is a construction ansatz.  UNSAT excludes only this fixed derived large
set; SAT supplies a complete LS(3,4,20) model that still requires independent
semantic verification.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))

from evidence.verify_defect_cross_link_lsts19 import (  # noqa: E402
    canonical,
    construct_lsts19,
    verify_large_set,
)


PARENT = REPO / "evidence" / "ls_3_4_20_generic_cnf" / "instance.cnf"
PARENT_SHA256 = "f855ff1dcd09c420d8d086a9bd759c7906b7685b0e40eb0149eb42768424625f"
POINTS = tuple(range(20))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
BLOCK_INDEX = {block: index for index, block in enumerate(BLOCKS)}
COLOURS = 17
PARENT_VARIABLES = 159_885
PARENT_CLAUSES = 251_957
LINK_BLOCKS = 969
PARENT_ROOT_UNITS = 17
NEW_UNITS = LINK_BLOCKS - PARENT_ROOT_UNITS
AUGMENTED_CLAUSES = PARENT_CLAUSES + NEW_UNITS


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def primary_variable(block: tuple[int, int, int, int], colour: int) -> int:
    if block not in BLOCK_INDEX or colour not in range(COLOURS):
        raise ValueError("invalid primary variable")
    return COLOURS * BLOCK_INDEX[block] + colour + 1


def fixed_link_units() -> tuple[int, ...]:
    colouring = construct_lsts19()
    verify_large_set(colouring)

    # On cyclic-link pair {0,1}, third points 2,...,18 receive all colours.
    # Relabel so the corresponding parent blocks {0,1,2,z+1} have parent
    # colours 0,...,16 in increasing fourth-point order, as the parent fixes.
    colour_map = {
        colouring[canonical((0, 1, third))]: third - 2 for third in range(2, 19)
    }
    if set(colour_map) != set(range(COLOURS)):
        raise AssertionError("link pair does not see every old colour")
    if set(colour_map.values()) != set(range(COLOURS)):
        raise AssertionError("derived colour relabelling is not bijective")

    units = []
    for triple, old_colour in sorted(colouring.items()):
        parent_block = tuple(sorted((0,) + tuple(value + 1 for value in triple)))
        units.append(primary_variable(parent_block, colour_map[old_colour]))
    if len(units) != LINK_BLOCKS or len(set(units)) != LINK_BLOCKS:
        raise AssertionError("fixed point link does not have 969 distinct units")
    return tuple(sorted(units))


def parent_unit_literals(lines: list[str]) -> set[int]:
    units = {
        int(fields[0])
        for line in lines
        if len(fields := line.split()) == 2 and fields[1] == "0"
    }
    if len(units) != PARENT_ROOT_UNITS:
        raise AssertionError(f"parent has {len(units)} unit clauses, expected 17")
    return units


def write_augmented_cnf(output: Path) -> tuple[str, str]:
    if sha256(PARENT) != PARENT_SHA256:
        raise AssertionError("canonical parent CNF hash mismatch")
    lines = PARENT.read_text(encoding="ascii").splitlines()
    if lines[0] != f"p cnf {PARENT_VARIABLES} {PARENT_CLAUSES}":
        raise AssertionError("canonical parent CNF header mismatch")

    fixed = set(fixed_link_units())
    existing = parent_unit_literals(lines[1:])
    if not existing <= fixed:
        raise AssertionError("fixed cyclic link conflicts with parent root units")
    added = sorted(fixed - existing)
    if len(added) != NEW_UNITS:
        raise AssertionError(f"expected 952 new units, found {len(added)}")

    lines[0] = f"p cnf {PARENT_VARIABLES} {AUGMENTED_CLAUSES}"
    content = ("\n".join(lines) + "\n").encode("ascii")
    content += b"".join(f"{literal} 0\n".encode("ascii") for literal in added)
    output.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest()

    unit_digest = hashlib.sha256()
    for literal in sorted(fixed):
        unit_digest.update(literal.to_bytes(4, "big"))
    return digest, unit_digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    args = parser.parse_args()
    digest, unit_digest = write_augmented_cnf(args.cnf)
    print(
        f"variables={PARENT_VARIABLES} clauses={AUGMENTED_CLAUSES} "
        f"fixed_link_units={LINK_BLOCKS} appended_units={NEW_UNITS}"
    )
    print(f"fixed-link unit SHA-256: {unit_digest}")
    print(f"augmented CNF SHA-256: {digest}")
    print(
        "scope: SAT constructs LS(3,4,20); UNSAT excludes only this fixed "
        "cyclic LS(2,3,19) point link"
    )


if __name__ == "__main__":
    main()
