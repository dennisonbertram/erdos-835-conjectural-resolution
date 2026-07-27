#!/usr/bin/env python3
"""Independently reconstruct and audit the fixed cyclic-link extension CNF."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "evidence" / "ls_3_4_20_generic_cnf" / "instance.cnf"
PARENT_SHA256 = "f855ff1dcd09c420d8d086a9bd759c7906b7685b0e40eb0149eb42768424625f"
EXPECTED_CNF_SHA256 = "a187094af93645080977a5f2fffcf40cdf2ca40086852390307269e263a3c65c"
EXPECTED_UNIT_SHA256 = (
    "fdf715ea0f53b1afa2c893381946e7361b08e7f92e575828d183e176d5981846"
)

P = 17
LEFT = 17
INFINITY = 18
LINK_POINTS = tuple(range(19))
PARENT_POINTS = tuple(range(20))
COLOURS = tuple(range(17))
BLOCKS = tuple(itertools.combinations(PARENT_POINTS, 4))
BLOCK_INDEX = {block: index for index, block in enumerate(BLOCKS)}
TRIPLES = tuple(itertools.combinations(PARENT_POINTS, 3))
PARENT_VARIABLES = 159_885
PARENT_CLAUSES = 251_957
AUGMENTED_CLAUSES = 252_909

STARTERS = (
    (0, 2, 5, 9, 14, 16, 13, 15, 12, 4, 8, 7, 11, 10, 6, 3, 1),
    (0, 3, 1, 10, 12, 11, 15, 4, 13, 5, 14, 9, 6, 8, 7, 16, 2),
)
PHASES = (
    7,
    1,
    9,
    0,
    5,
    12,
    15,
    8,
    13,
    11,
    4,
    16,
    10,
    14,
    15,
    14,
    2,
    10,
    6,
    9,
    11,
    4,
    8,
    3,
    12,
    6,
    5,
    4,
    11,
    2,
    14,
    0,
    7,
    8,
    6,
    1,
    10,
    5,
    12,
    6,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(values))


def translate(values: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return canonical(tuple((value + amount) % P for value in values))


def representatives() -> tuple[tuple[int, int, int], ...]:
    unseen = set(itertools.combinations(range(P), 3))
    result = []
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in range(P))
        result.append(representative)
        for shift in range(P):
            unseen.discard(translate(representative, shift))
    if len(result) != 40:
        raise AssertionError("cyclic triple orbit census is not 40")
    return tuple(result)


def square(starter: tuple[int, ...], x: int, y: int) -> int:
    return (starter[(x - y) % P] + y) % P


def construct_link() -> dict[tuple[int, int, int], int]:
    colouring: dict[tuple[int, int, int], int] = {}

    def put(raw: tuple[int, int, int], colour: int) -> None:
        triple = canonical(raw)
        if triple in colouring or colour not in COLOURS:
            raise AssertionError("invalid or duplicate cyclic link assignment")
        colouring[triple] = colour

    for x in range(P):
        put((LEFT, INFINITY, x), x)
    for x, y in itertools.combinations(range(P), 2):
        put((LEFT, x, y), square(STARTERS[0], x, y))
        put((INFINITY, x, y), square(STARTERS[1], x, y))
    for orbit, representative in enumerate(representatives()):
        zero_shift = (-PHASES[orbit]) % P
        for colour in COLOURS:
            put(translate(representative, zero_shift + colour), colour)

    if set(colouring) != set(itertools.combinations(LINK_POINTS, 3)):
        raise AssertionError("cyclic certificate does not colour every triple")
    if Counter(colouring.values()) != Counter({colour: 57 for colour in COLOURS}):
        raise AssertionError("cyclic colour classes have wrong sizes")
    for pair in itertools.combinations(LINK_POINTS, 2):
        seen = {
            colouring[canonical(pair + (third,))]
            for third in LINK_POINTS
            if third not in pair
        }
        if seen != set(COLOURS):
            raise AssertionError(f"cyclic link pair {pair} is not rainbow")
    return colouring


def primary_variable(block: tuple[int, ...], colour: int) -> int:
    return 17 * BLOCK_INDEX[block] + colour + 1


def expected_units() -> tuple[int, ...]:
    colouring = construct_link()
    colour_map = {
        colouring[canonical((0, 1, third))]: third - 2 for third in range(2, 19)
    }
    if set(colour_map) != set(COLOURS) or set(colour_map.values()) != set(COLOURS):
        raise AssertionError("colour normalization is not bijective")
    units = []
    for triple, old_colour in colouring.items():
        block = canonical((0,) + tuple(value + 1 for value in triple))
        units.append(primary_variable(block, colour_map[old_colour]))
    return tuple(sorted(units))


def verify_cnf(path: Path) -> None:
    if sha256(PARENT) != PARENT_SHA256:
        raise AssertionError("parent CNF hash mismatch")
    if sha256(path) != EXPECTED_CNF_SHA256:
        raise AssertionError("augmented CNF hash mismatch")

    parent_lines = PARENT.read_text(encoding="ascii").splitlines()
    actual_lines = path.read_text(encoding="ascii").splitlines()
    if actual_lines[0] != f"p cnf {PARENT_VARIABLES} {AUGMENTED_CLAUSES}":
        raise AssertionError("augmented CNF header mismatch")
    if actual_lines[1 : len(parent_lines)] != parent_lines[1:]:
        raise AssertionError("augmented CNF changed a parent clause")

    units = expected_units()
    unit_digest = hashlib.sha256()
    for literal in units:
        unit_digest.update(literal.to_bytes(4, "big"))
    if unit_digest.hexdigest() != EXPECTED_UNIT_SHA256:
        raise AssertionError("fixed-link unit digest mismatch")

    parent_units = {
        int(fields[0])
        for line in parent_lines[1:]
        if len(fields := line.split()) == 2 and fields[1] == "0"
    }
    if len(parent_units) != 17 or not parent_units <= set(units):
        raise AssertionError("parent root units do not match the fixed link")
    expected_added = [f"{literal} 0" for literal in sorted(set(units) - parent_units)]
    if actual_lines[len(parent_lines) :] != expected_added:
        raise AssertionError("appended unit clauses are not exact")
    if len(actual_lines) - 1 != AUGMENTED_CLAUSES:
        raise AssertionError("augmented clause count mismatch")


def parse_model(path: Path) -> set[int]:
    positives: set[int] = set()
    saw_sat = False
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            saw_sat = "SATISFIABLE" in line and "UNSATISFIABLE" not in line
        elif line.startswith("v "):
            positives.update(value for value in map(int, line[2:].split()) if value > 0)
    if not saw_sat:
        raise AssertionError("model file does not claim SATISFIABLE")
    return positives


def verify_model(path: Path) -> str:
    positives = parse_model(path)
    colours = []
    for index, block in enumerate(BLOCKS):
        assigned = [
            colour for colour in COLOURS if 17 * index + colour + 1 in positives
        ]
        if len(assigned) != 1:
            raise AssertionError(f"block {block} has {len(assigned)} colours")
        colours.append(assigned[0])

    for triple in TRIPLES:
        seen = {
            colours[BLOCK_INDEX[canonical(triple + (point,))]]
            for point in PARENT_POINTS
            if point not in triple
        }
        if seen != set(COLOURS):
            raise AssertionError(f"triple star {triple} is not rainbow")
    if not set(expected_units()) <= positives:
        raise AssertionError("model does not contain the fixed cyclic point link")
    return hashlib.sha256(bytes(colours)).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()
    verify_cnf(args.cnf)
    print("[ok] cyclic LS(2,3,19) independently reconstructed")
    print("[ok] parent clauses unchanged; exactly 952 compatible units appended")
    print(f"[exact] augmented CNF SHA-256: {sha256(args.cnf)}")
    if args.model is not None:
        digest = verify_model(args.model)
        print("[theorem] SAT witness is a complete LS(3,4,20)")
        print(f"[exact] block-colour SHA-256: {digest}")
    else:
        print("[scope] no SAT or UNSAT solver verdict is asserted")
    print("status: PASS")


if __name__ == "__main__":
    main()
