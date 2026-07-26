#!/usr/bin/env python3
"""Export and independently verify the Etzion--Hartman branch-0 hint.

The checked Etzion--Hartman partial is stored in labels whose usual
``(012, 01, 3)`` second-star row has branch 54 (one 16-cycle).  The exact
even-flag reduction identifies another fully assigned flag whose row has
cycle type ``2^8``.  This standard-library-only program reconstructs the
point and colour relabelling from the source data, applies it to all 4,845
blocks, and verifies the resulting branch-0 partial.

No SAT/CP-SAT solver is imported or launched.  The exported assignments are
only a search hint; they are not added as constraints by the CP-SAT driver.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_partial.txt"
BRANCH_MANIFEST = (
    REPO / "evidence" / "ls_3_4_20_second_star_branches" / "manifest.json"
)

SOURCE_SHA256 = "bca36685508a4cf396cec015c2cfe06239f018b1dba32cff41ea11ee6c601f33"
MANIFEST_SHA256 = "775eb65445ffe0c5010450d7b3356fd03f4ce1b1cd88522f88a771ece21c7159"
OUTPUT_SHA256 = "06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78"

EXPECTED_POINT_MAP = (
    0, 4, 6, 7, 2, 1, 8, 10, 5, 3, 11, 12, 14, 16, 18, 9, 17, 15, 13, 19,
)
EXPECTED_COLOUR_MAP = (11, 14, 12, 2, 1, 4, 6, 7, 16, 9, 3, 5, 8, 15, 10, 13, 0)

N = 20
C = 17
POINTS = tuple(range(N))
COLOURS = tuple(range(C))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
BLOCK_INDEX = {block: index for index, block in enumerate(BLOCKS)}
TRIPLES = tuple(itertools.combinations(POINTS, 3))

# Fully assigned even flag in the source Etzion--Hartman partial.
SOURCE_B = (0, 4, 5, 9)
SOURCE_T = (0, 4, 5)
SOURCE_E = (0, 5)
SOURCE_R = 4
SOURCE_Q = 9
TARGET_DOMAIN = tuple(range(4, 20))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_partial_bytes(data: bytes) -> list[int]:
    """Strictly parse the repository's canonical 4,845-row text format."""

    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as exc:
        raise AssertionError("partial is not ASCII") from exc
    colours: list[int] = []
    lines = text.splitlines()
    if len(lines) != len(BLOCKS) or not data.endswith(b"\n"):
        raise AssertionError("partial has the wrong row count or final newline")
    for expected, line in zip(BLOCKS, lines):
        fields = line.split()
        if len(fields) != 5:
            raise AssertionError(f"malformed partial row for {expected}")
        values = tuple(int(field) for field in fields)
        if values[:4] != expected:
            raise AssertionError(f"unexpected block row {values[:4]} != {expected}")
        if not -1 <= values[4] < C:
            raise AssertionError(f"invalid colour on block {expected}")
        colours.append(values[4])
    return colours


def partial_bytes(colours: Iterable[int]) -> bytes:
    values = tuple(colours)
    if len(values) != len(BLOCKS):
        raise AssertionError("wrong partial-vector length")
    return "".join(
        "{} {} {} {} {}\n".format(*block, colour)
        for block, colour in zip(BLOCKS, values)
    ).encode("ascii")


def colour_of(colours: list[int], block: Iterable[int]) -> int:
    canonical = tuple(sorted(block))
    if len(canonical) != 4 or len(set(canonical)) != 4:
        raise AssertionError(f"not a four-set: {canonical}")
    return colours[BLOCK_INDEX[canonical]]


def verify_proper_partial(colours: list[int]) -> tuple[int, int]:
    """Check the exact partial LS condition on every triple star."""

    if len(colours) != len(BLOCKS):
        raise AssertionError("wrong partial-vector length")
    assigned = sum(value >= 0 for value in colours)
    holes = len(colours) - assigned
    for triple in TRIPLES:
        seen: set[int] = set()
        for point in POINTS:
            if point in triple:
                continue
            value = colour_of(colours, triple + (point,))
            if value >= 0:
                if value in seen:
                    raise AssertionError(
                        f"repeated colour {value} above triple {triple}"
                    )
                seen.add(value)
    return assigned, holes


def inverse_root_star(
    colours: list[int], triple: tuple[int, int, int]
) -> dict[int, int]:
    """Return old-colour -> extension-point for a complete rainbow star."""

    inverse: dict[int, int] = {}
    for point in POINTS:
        if point in triple:
            continue
        value = colour_of(colours, triple + (point,))
        if value < 0 or value in inverse:
            raise AssertionError(f"root star {triple} is not fully rainbow")
        inverse[value] = point
    if set(inverse) != set(COLOURS):
        raise AssertionError(f"root star {triple} misses a colour")
    return inverse


def row_permutation(
    colours: list[int],
    root_triple: tuple[int, int, int],
    pair: tuple[int, int],
    row_point: int,
) -> dict[int, int]:
    """Normalize a fully assigned second-star row by ``root_triple``."""

    root_inverse = inverse_root_star(colours, root_triple)
    domain = tuple(
        point
        for point in POINTS
        if point not in set(root_triple) | {row_point}
    )
    result = {}
    for point in domain:
        value = colour_of(colours, pair + (row_point, point))
        if value < 0:
            raise AssertionError("selected second-star row has a hole")
        result[point] = root_inverse[value]
    if set(result) != set(result.values()):
        raise AssertionError("selected row is not a permutation")
    if any(result[point] == point for point in domain):
        raise AssertionError("selected row is not a derangement")
    return result


def cycles(permutation: dict[int, int]) -> tuple[tuple[int, ...], ...]:
    """Directed cycles, rotated to their minima and canonically sorted."""

    if set(permutation) != set(permutation.values()):
        raise AssertionError("mapping is not a permutation")
    unseen = set(permutation)
    answer = []
    while unseen:
        start = min(unseen)
        point = start
        cycle = []
        while point in unseen:
            unseen.remove(point)
            cycle.append(point)
            point = permutation[point]
        if point != start:
            raise AssertionError("mapping contains a non-cycle component")
        answer.append(tuple(cycle))
    return tuple(sorted(answer, key=lambda item: (len(item), item)))


def canonical_branch0() -> dict[int, int]:
    """The manifest's canonical ``2^8`` permutation on points 4,...,19."""

    result: dict[int, int] = {}
    for left in range(4, 20, 2):
        result[left] = left + 1
        result[left + 1] = left
    return result


def construct_maps(colours: list[int]) -> tuple[dict[int, int], dict[int, int]]:
    """Derive, rather than assume, the exact point and colour maps."""

    if set(SOURCE_T) | {SOURCE_Q} != set(SOURCE_B):
        raise AssertionError("source flag constants are inconsistent")
    if set(SOURCE_E) | {SOURCE_R, SOURCE_Q} != set(SOURCE_B):
        raise AssertionError("source flag constants are inconsistent")

    source = row_permutation(colours, SOURCE_T, SOURCE_E, SOURCE_Q)
    source_cycles = cycles(source)
    if tuple(len(item) for item in source_cycles) != (2,) * 8:
        raise AssertionError("selected source flag is not branch 0")

    target = canonical_branch0()
    target_cycles = cycles(target)
    point_map = {
        SOURCE_E[0]: 0,
        SOURCE_E[1]: 1,
        SOURCE_R: 2,
        SOURCE_Q: 3,
    }
    for source_cycle, target_cycle in zip(source_cycles, target_cycles):
        for old, new in zip(source_cycle, target_cycle):
            point_map[old] = new
    if set(point_map) != set(POINTS) or set(point_map.values()) != set(POINTS):
        raise AssertionError("constructed point map is not bijective")
    for point in source:
        if point_map[source[point]] != target[point_map[point]]:
            raise AssertionError("point map does not conjugate to branch 0")

    colour_map: dict[int, int] = {}
    for point in POINTS:
        if point in SOURCE_T:
            continue
        old_colour = colour_of(colours, SOURCE_T + (point,))
        new_point = point_map[point]
        if not 3 <= new_point < 20:
            raise AssertionError("root extension maps inside the new root")
        colour_map[old_colour] = new_point - 3
    if set(colour_map) != set(COLOURS):
        raise AssertionError("constructed colour map has the wrong domain")
    if set(colour_map.values()) != set(COLOURS):
        raise AssertionError("constructed colour map is not bijective")

    if tuple(point_map[point] for point in POINTS) != EXPECTED_POINT_MAP:
        raise AssertionError("derived point map changed")
    if tuple(colour_map[colour] for colour in COLOURS) != EXPECTED_COLOUR_MAP:
        raise AssertionError("derived colour map changed")
    return point_map, colour_map


def transform(
    colours: list[int],
    point_map: dict[int, int],
    colour_map: dict[int, int],
) -> list[int]:
    transformed = [-2] * len(BLOCKS)
    for block, value in zip(BLOCKS, colours):
        target = tuple(sorted(point_map[point] for point in block))
        index = BLOCK_INDEX[target]
        if transformed[index] != -2:
            raise AssertionError(f"block collision at {target}")
        transformed[index] = colour_map[value] if value >= 0 else -1
    if -2 in transformed:
        raise AssertionError("point map omitted a target block")
    return transformed


def inverse_transform(
    transformed: list[int],
    point_map: dict[int, int],
    colour_map: dict[int, int],
) -> list[int]:
    inverse_point = {new: old for old, new in point_map.items()}
    inverse_colour = {new: old for old, new in colour_map.items()}
    recovered = [-2] * len(BLOCKS)
    for block, value in zip(BLOCKS, transformed):
        source = tuple(sorted(inverse_point[point] for point in block))
        index = BLOCK_INDEX[source]
        if recovered[index] != -2:
            raise AssertionError(f"inverse block collision at {source}")
        recovered[index] = inverse_colour[value] if value >= 0 else -1
    if -2 in recovered:
        raise AssertionError("inverse map omitted a source block")
    return recovered


def verify_branch0(
    transformed: list[int], manifest: dict[str, object]
) -> tuple[int, int]:
    assigned, holes = verify_proper_partial(transformed)
    if (assigned, holes) != (4_773, 72):
        raise AssertionError("transformed assigned/hole counts changed")

    for point in range(3, 20):
        if colour_of(transformed, (0, 1, 2, point)) != point - 3:
            raise AssertionError("transformed root star is not canonical")

    branches = manifest.get("branches")
    if not isinstance(branches, list) or len(branches) != 55:
        raise AssertionError("invalid second-star branch manifest")
    branch0 = branches[0]
    if branch0.get("id") != 0 or branch0.get("cycle_type") != [2] * 8:
        raise AssertionError("manifest branch 0 changed")
    units = branch0.get("units")
    if not isinstance(units, list) or len(units) != 16:
        raise AssertionError("manifest branch 0 has the wrong units")
    for unit in units:
        block = tuple(unit["block"])
        expected = unit["colour"]
        if colour_of(transformed, block) != expected:
            raise AssertionError(f"branch-0 unit mismatch at {block}")

    observed = row_permutation(transformed, (0, 1, 2), (0, 1), 3)
    if observed != canonical_branch0():
        raise AssertionError("transformed row is not canonical branch 0")
    return assigned, holes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        help="write the deterministic transformed partial to this path",
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        help="write a deterministic JSON verification receipt",
    )
    parser.add_argument(
        "--verify",
        type=Path,
        help="authenticate an existing transformed partial byte-for-byte",
    )
    args = parser.parse_args()

    source_bytes = SOURCE.read_bytes()
    manifest_bytes = BRANCH_MANIFEST.read_bytes()
    if sha256(source_bytes) != SOURCE_SHA256:
        raise AssertionError("source Etzion--Hartman SHA-256 mismatch")
    if sha256(manifest_bytes) != MANIFEST_SHA256:
        raise AssertionError("second-star manifest SHA-256 mismatch")
    manifest = json.loads(manifest_bytes)
    if manifest.get("schema") != "ls-3-4-20-second-star-branches-v1":
        raise AssertionError("wrong second-star manifest schema")

    source = parse_partial_bytes(source_bytes)
    if verify_proper_partial(source) != (4_773, 72):
        raise AssertionError("source assigned/hole counts changed")
    point_map, colour_map = construct_maps(source)
    transformed = transform(source, point_map, colour_map)
    assigned, holes = verify_branch0(transformed, manifest)
    if inverse_transform(transformed, point_map, colour_map) != source:
        raise AssertionError("inverse relabelling does not recover the source")
    output_bytes = partial_bytes(transformed)
    output_hash = sha256(output_bytes)
    if output_hash != OUTPUT_SHA256:
        raise AssertionError("transformed output SHA-256 changed")

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(output_bytes)
        if args.output.read_bytes() != output_bytes:
            raise AssertionError("written output failed byte-for-byte reread")
    if args.verify is not None:
        supplied = args.verify.read_bytes()
        if supplied != output_bytes:
            raise AssertionError("supplied hint differs from the exact export")
        supplied_colours = parse_partial_bytes(supplied)
        if supplied_colours != transformed:
            raise AssertionError("supplied hint semantic parse changed")
        verify_branch0(supplied_colours, manifest)

    receipt = {
        "schema": "ls-3-4-20-eh15-branch0-hint-v1",
        "status": "PASS",
        "source": str(SOURCE.relative_to(REPO)),
        "source_sha256": SOURCE_SHA256,
        "branch_manifest": str(BRANCH_MANIFEST.relative_to(REPO)),
        "branch_manifest_sha256": MANIFEST_SHA256,
        "source_flag": {
            "B": list(SOURCE_B),
            "T": list(SOURCE_T),
            "e": list(SOURCE_E),
            "r": SOURCE_R,
            "q": SOURCE_Q,
        },
        "point_map_old_to_new": [point_map[point] for point in POINTS],
        "colour_map_old_to_new": [colour_map[colour] for colour in COLOURS],
        "target_branch_id": 0,
        "target_cycle_type": [2] * 8,
        "blocks": len(BLOCKS),
        "assigned": assigned,
        "holes": holes,
        "output_sha256": output_hash,
        "inverse_round_trip": "PASS",
        "partial_semantics": "PASS",
        "scope": (
            "search hint only; no completion and no SAT/UNSAT result is claimed"
        ),
    }
    if args.receipt is not None:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
