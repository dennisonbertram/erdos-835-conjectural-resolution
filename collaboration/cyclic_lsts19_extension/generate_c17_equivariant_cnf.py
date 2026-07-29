#!/usr/bin/env python3
"""Generate the C17-equivariant fixed-link LS(3,4,20) extension CNF.

The audited cyclic LS(2,3,19) is covariant under simultaneous translation of
its seventeen finite points and colours.  This ansatz asks that the unknown
quadruples not containing the new point have the same covariance.

This is a restricted construction search.  SAT gives a complete LS(3,4,20);
UNSAT excludes only this C17-equivariant extension of this fixed point link.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
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


P = 17
FIXED = (17, 18)
POINTS = tuple(range(19))
COLOURS = tuple(range(P))
EXPECTED_BLOCK_ORBITS = 228
EXPECTED_TRIPLE_ORBITS = 57


def translate(values: tuple[int, ...], amount: int) -> tuple[int, ...]:
    """Translate finite points modulo 17 and fix points 17 and 18."""
    return canonical(
        tuple((value + amount) % P if value < P else value for value in values)
    )


def orbit_representatives(size: int) -> tuple[tuple[int, ...], ...]:
    unseen = set(itertools.combinations(POINTS, size))
    representatives = []
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in range(P))
        orbit = {translate(representative, shift) for shift in range(P)}
        if len(orbit) != P:
            raise AssertionError("a subset orbit is not free")
        representatives.append(representative)
        unseen -= orbit
    return tuple(sorted(representatives))


def representative_and_shift(
    values: tuple[int, ...],
    representative_index: dict[tuple[int, ...], int],
) -> tuple[int, int]:
    representative = min(translate(values, shift) for shift in range(P))
    shifts = [
        shift
        for shift in range(P)
        if translate(representative, shift) == canonical(values)
    ]
    if len(shifts) != 1:
        raise AssertionError("orbit shift is not unique")
    return representative_index[representative], shifts[0]


def variable(orbit: int, base_colour: int) -> int:
    return P * orbit + base_colour + 1


def build_instance(
    encoding: str,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
    list[tuple[int, ...]],
]:
    colouring = construct_lsts19()
    verify_large_set(colouring)
    for triple, colour in colouring.items():
        for shift in range(P):
            if colouring[translate(triple, shift)] != (colour + shift) % P:
                raise AssertionError("fixed point link is not C17-covariant")

    block_representatives = orbit_representatives(4)
    triple_representatives = orbit_representatives(3)
    if len(block_representatives) != EXPECTED_BLOCK_ORBITS:
        raise AssertionError("wrong quadruple-orbit count")
    if len(triple_representatives) != EXPECTED_TRIPLE_ORBITS:
        raise AssertionError("wrong triple-orbit count")
    block_index = {
        representative: index
        for index, representative in enumerate(block_representatives)
    }

    clauses: list[tuple[int, ...]] = []

    # Each quadruple orbit has one base colour.  The colour of its translate by
    # s is the base colour plus s modulo 17.
    for orbit in range(len(block_representatives)):
        clauses.append(tuple(variable(orbit, colour) for colour in COLOURS))
        for first, second in itertools.combinations(COLOURS, 2):
            clauses.append((-variable(orbit, first), -variable(orbit, second)))

    # For a triple representative T, its sixteen non-root extensions must use
    # all colours except the colour of the fixed root block {root} union T.
    # Pairwise distinctness plus the sixteen forbidden-colour clauses is exact.
    for triple in triple_representatives:
        forbidden = colouring[triple]
        extensions = []
        for point in POINTS:
            if point in triple:
                continue
            block = canonical(triple + (point,))
            extensions.append(representative_and_shift(block, block_index))
        if len(extensions) != 16 or len(set(extensions)) != 16:
            raise AssertionError("triple does not have sixteen distinct extensions")

        for orbit, shift in extensions:
            clauses.append((-variable(orbit, (forbidden - shift) % P),))

        if encoding == "pairwise":
            for (first_orbit, first_shift), (
                second_orbit,
                second_shift,
            ) in itertools.combinations(extensions, 2):
                if first_orbit == second_orbit:
                    if first_shift == second_shift:
                        raise AssertionError("duplicate extension in one triple star")
                    # The two translated copies always differ in colour.
                    continue
                for first_colour in COLOURS:
                    equal_second_colour = (
                        first_colour + first_shift - second_shift
                    ) % P
                    clauses.append(
                        (
                            -variable(first_orbit, first_colour),
                            -variable(second_orbit, equal_second_colour),
                        )
                    )
        elif encoding == "cover":
            # Sixteen slots and sixteen required colours: coverage forces a
            # bijection, so the pairwise clauses are unnecessary.
            for required in COLOURS:
                if required == forbidden:
                    continue
                clauses.append(
                    tuple(
                        variable(orbit, (required - shift) % P)
                        for orbit, shift in extensions
                    )
                )
        else:
            raise ValueError(f"unknown encoding: {encoding}")

    return block_representatives, triple_representatives, clauses


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def write_instance(cnf_path: Path, map_path: Path, encoding: str) -> tuple[str, str]:
    block_representatives, triple_representatives, clauses = build_instance(encoding)
    variables = P * len(block_representatives)
    lines = [f"p cnf {variables} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    cnf_content = ("\n".join(lines) + "\n").encode("ascii")
    cnf_path.write_bytes(cnf_content)

    mapping = {
        "schema": "erdos835-c17-equivariant-ls3420-v1",
        "finite_points": list(range(P)),
        "fixed_points": list(FIXED),
        "colour_modulus": P,
        "variable_rule": "1 + 17 * block_orbit_index + base_colour",
        "translate_rule": "finite points and colour add shift modulo 17",
        "encoding": encoding,
        "block_representatives": [list(block) for block in block_representatives],
        "triple_representatives": [list(triple) for triple in triple_representatives],
        "variables": variables,
        "clauses": len(clauses),
        "cnf_sha256": sha256_bytes(cnf_content),
        "scope": (
            "SAT constructs LS(3,4,20); UNSAT excludes only the C17-equivariant "
            "extension of this fixed cyclic LS(2,3,19)"
        ),
    }
    map_content = (json.dumps(mapping, indent=2, sort_keys=True) + "\n").encode("ascii")
    map_path.write_bytes(map_content)
    return sha256_bytes(cnf_content), sha256_bytes(map_content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument(
        "--encoding",
        choices=("pairwise", "cover"),
        default="pairwise",
        help="encode each star by pairwise inequality or required-colour coverage",
    )
    args = parser.parse_args()
    cnf_digest, map_digest = write_instance(args.cnf, args.map, args.encoding)
    header = args.cnf.read_text(encoding="ascii").splitlines()[0]
    print(header)
    print(
        f"block_orbits={EXPECTED_BLOCK_ORBITS} triple_orbits={EXPECTED_TRIPLE_ORBITS}"
    )
    print(f"cnf SHA-256: {cnf_digest}")
    print(f"map SHA-256: {map_digest}")
    print(f"encoding: {args.encoding}")
    print(
        "scope: SAT constructs LS(3,4,20); UNSAT excludes only this "
        "C17-equivariant fixed-link ansatz"
    )


if __name__ == "__main__":
    main()
