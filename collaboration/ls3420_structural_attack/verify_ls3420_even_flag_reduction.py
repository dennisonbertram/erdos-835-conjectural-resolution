#!/usr/bin/env python3
"""Independent verifier for the LS(3,4,20) even-flag reduction.

This script imports neither the existing branch generator nor its verifier.
It:

1. reconstructs the 55 derangement cycle types and the 28 even types;
2. checks those types against the committed second-star manifest;
3. exhausts the four-bijection parity lemma at the sign level; and
4. constructs, in memory, an exact point/colour relabelling taking the
   verified Etzion--Hartman partial from its old branch-54 row to branch 0.

No solver is launched and no file is written.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterator


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST = REPO / "evidence" / "ls_3_4_20_second_star_branches" / "manifest.json"
EH = REPO / "evidence" / "ls_3_4_20_eh15_partial.txt"
MANIFEST_SHA256 = "775eb65445ffe0c5010450d7b3356fd03f4ce1b1cd88522f88a771ece21c7159"
EH_SHA256 = "bca36685508a4cf396cec015c2cfe06239f018b1dba32cff41ea11ee6c601f33"

N = 20
C = 17
POINTS = tuple(range(N))
COLOURS = tuple(range(C))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
BLOCK_INDEX = {block: index for index, block in enumerate(BLOCKS)}
TRIPLES = tuple(itertools.combinations(POINTS, 3))

EVEN_BRANCH_IDS = (
    0, 3, 4, 5, 7, 11, 12, 15, 17, 18, 19, 23, 24, 25,
    27, 28, 33, 35, 36, 37, 39, 43, 44, 48, 50, 51, 52, 53,
)

# Source flag in the Etzion--Hartman partial.
SOURCE_B = (0, 4, 5, 9)
SOURCE_T = (0, 4, 5)
SOURCE_E = (0, 5)
SOURCE_R = 4
SOURCE_Q = 9


def partitions_minimum(
    total: int, lower: int = 2
) -> Iterator[tuple[int, ...]]:
    """Nondecreasing partitions of ``total`` with every part at least two."""

    if total == 0:
        yield ()
        return
    for first in range(lower, total + 1):
        remainder = total - first
        if remainder and remainder < first:
            continue
        for tail in partitions_minimum(remainder, first):
            yield (first,) + tail


def cycle_decomposition(
    permutation: dict[int, int]
) -> tuple[tuple[int, ...], ...]:
    """Directed cycles, rotated to their least point and canonically sorted."""

    if set(permutation) != set(permutation.values()):
        raise AssertionError("mapping is not a permutation")
    unseen = set(permutation)
    cycles = []
    while unseen:
        start = min(unseen)
        point = start
        cycle = []
        while point in unseen:
            unseen.remove(point)
            cycle.append(point)
            point = permutation[point]
        if point != start:
            raise AssertionError("mapping has a non-cyclic component")
        cycles.append(tuple(cycle))
    return tuple(sorted(cycles, key=lambda cycle: (len(cycle), cycle)))


def cycle_type(permutation: dict[int, int]) -> tuple[int, ...]:
    return tuple(sorted(len(cycle) for cycle in cycle_decomposition(permutation)))


def permutation_sign(permutation: dict[int, int]) -> int:
    """Sign from the exact cycle formula, independent of label order."""

    size = len(permutation)
    cycles = len(cycle_decomposition(permutation))
    return -1 if (size - cycles) % 2 else 1


def canonical_permutation(parts: tuple[int, ...]) -> dict[int, int]:
    domain = tuple(range(4, 20))
    answer: dict[int, int] = {}
    cursor = 0
    for size in parts:
        cycle = domain[cursor : cursor + size]
        if len(cycle) != size:
            raise AssertionError("cycle type overruns the canonical domain")
        for index, value in enumerate(cycle):
            answer[value] = cycle[(index + 1) % size]
        cursor += size
    if cursor != len(domain):
        raise AssertionError("cycle type does not fill the canonical domain")
    return answer


def load_partial() -> list[int]:
    colours: list[int] = []
    with EH.open(encoding="utf-8") as stream:
        for expected, line in itertools.zip_longest(BLOCKS, stream):
            if expected is None or line is None:
                raise AssertionError("partial has the wrong row count")
            fields = [int(field) for field in line.split()]
            if len(fields) != 5 or tuple(fields[:4]) != expected:
                raise AssertionError(f"unexpected row for block {expected}")
            if not -1 <= fields[4] < C:
                raise AssertionError(f"invalid colour at block {expected}")
            colours.append(fields[4])
    if len(colours) != len(BLOCKS):
        raise AssertionError("partial has the wrong number of blocks")
    return colours


def partial_colour(colours: list[int], block: tuple[int, ...]) -> int:
    return colours[BLOCK_INDEX[tuple(sorted(block))]]


def verify_partial(colours: list[int]) -> None:
    if len(colours) != len(BLOCKS):
        raise AssertionError("wrong partial vector length")
    for triple in TRIPLES:
        assigned = []
        for point in POINTS:
            if point in triple:
                continue
            value = partial_colour(colours, triple + (point,))
            if value >= 0:
                assigned.append(value)
        if len(assigned) != len(set(assigned)):
            raise AssertionError(f"colour collision over triple {triple}")


def root_inverse(
    colours: list[int], triple: tuple[int, int, int]
) -> dict[int, int]:
    """Map old colours to extension points for a fully assigned root star."""

    outside = [point for point in POINTS if point not in triple]
    values = [partial_colour(colours, triple + (point,)) for point in outside]
    if sorted(values) != list(COLOURS):
        raise AssertionError(f"root star {triple} is not fully rainbow")
    return {value: point for point, value in zip(outside, values)}


def flag_permutation(
    colours: list[int],
    triple: tuple[int, int, int],
    edge: tuple[int, int],
    row_point: int,
) -> dict[int, int]:
    """The normalized second-star row on the sixteen remaining points."""

    inverse = root_inverse(colours, triple)
    domain = [
        point
        for point in POINTS
        if point not in set(triple) | {row_point}
    ]
    answer = {}
    for point in domain:
        value = partial_colour(colours, edge + (row_point, point))
        if value < 0:
            raise AssertionError("selected flag row is not fully assigned")
        answer[point] = inverse[value]
    if set(answer) != set(answer.values()) or any(
        answer[point] == point for point in answer
    ):
        raise AssertionError("selected flag is not a derangement")
    return answer


def transformed_partial(
    colours: list[int],
    point_map: dict[int, int],
    colour_map: dict[int, int],
) -> list[int]:
    transformed = [-2] * len(BLOCKS)
    for block, value in zip(BLOCKS, colours):
        new_block = tuple(sorted(point_map[point] for point in block))
        index = BLOCK_INDEX[new_block]
        if transformed[index] != -2:
            raise AssertionError("point map collided on a block")
        transformed[index] = colour_map[value] if value >= 0 else -1
    if -2 in transformed:
        raise AssertionError("point map omitted a block")
    return transformed


def partial_bytes(colours: list[int]) -> bytes:
    return "".join(
        "{} {} {} {} {}\n".format(*block, value)
        for block, value in zip(BLOCKS, colours)
    ).encode("ascii")


def section_branch_and_parity() -> tuple[list[tuple[int, ...]], dict[str, object]]:
    parts = list(partitions_minimum(16))
    if len(parts) != 55:
        raise AssertionError("wrong number of derangement cycle types")

    # On sixteen points, sign = (-1)^(16-number_of_cycles).
    even_ids = tuple(
        index for index, item in enumerate(parts) if len(item) % 2 == 0
    )
    if even_ids != EVEN_BRANCH_IDS:
        raise AssertionError("even branch IDs changed")
    if len(even_ids) != 28 or len(parts) - len(even_ids) != 27:
        raise AssertionError("wrong parity split")

    manifest_bytes = MANIFEST.read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256:
        raise AssertionError("second-star manifest SHA-256 mismatch")
    manifest = json.loads(manifest_bytes)
    branches = manifest.get("branches")
    if manifest.get("schema") != "ls-3-4-20-second-star-branches-v1":
        raise AssertionError("wrong branch-manifest schema")
    if not isinstance(branches, list) or len(branches) != 55:
        raise AssertionError("wrong manifest branch count")
    for index, (item, branch) in enumerate(zip(parts, branches)):
        if branch.get("id") != index or tuple(branch.get("cycle_type", ())) != item:
            raise AssertionError(f"manifest mismatch at branch {index}")
        canonical = canonical_permutation(item)
        images = tuple(canonical[point] for point in range(4, 20))
        if tuple(branch.get("canonical_row_images", ())) != images:
            raise AssertionError(f"manifest permutation mismatch at branch {index}")
        expected_sign = 1 if index in EVEN_BRANCH_IDS else -1
        if permutation_sign(canonical) != expected_sign:
            raise AssertionError(f"cycle-sign mismatch at branch {index}")

    # Exhaust every possible assignment of four bijection signs.  At least
    # two of the six unordered relative maps have positive sign.
    same_pair_counts = []
    branch54_even_pair_counts = []
    for signs in itertools.product((-1, 1), repeat=4):
        relative = {
            (left, right): signs[left] * signs[right]
            for left, right in itertools.combinations(range(4), 2)
        }
        even_pairs = sum(value == 1 for value in relative.values())
        if even_pairs < 2:
            raise AssertionError("four-sign pigeonhole lemma failed")
        same_pair_counts.append(even_pairs)
        if relative[(2, 3)] == -1:
            branch54_even_pair_counts.append(even_pairs)
    if sorted(set(same_pair_counts)) != [2, 3, 6]:
        raise AssertionError("unexpected four-sign pair counts")
    if sorted(set(branch54_even_pair_counts)) != [2, 3]:
        raise AssertionError("unexpected branch-54 even-pair counts")

    print("[exact] derangement cycle types:", len(parts))
    print("[exact] even / odd cycle types:", len(even_ids), "/", 55 - len(even_ids))
    print("[exact] exhaustive even branch IDs:", ",".join(map(str, even_ids)))
    print("[exact] four-bijection parity controls: 16/16 PASS")
    print("[exact] same-parity unordered pairs per control:", sorted(set(same_pair_counts)))
    print("[exact] even pairs when the canonical pair is odd:",
          sorted(set(branch54_even_pair_counts)))
    print("[exact] branch 54 sign: odd; it is symmetry-redundant")
    return parts, manifest


def section_eh(
    parts: list[tuple[int, ...]], manifest: dict[str, object]
) -> tuple[dict[int, int], dict[int, int], str]:
    if hashlib.sha256(EH.read_bytes()).hexdigest() != EH_SHA256:
        raise AssertionError("Etzion--Hartman partial SHA-256 mismatch")
    colours = load_partial()
    verify_partial(colours)
    if sum(value >= 0 for value in colours) != 4_773:
        raise AssertionError("wrong assigned-block count")
    if sum(value < 0 for value in colours) != 72:
        raise AssertionError("wrong hole count")

    old_row = flag_permutation(colours, (0, 1, 2), (0, 1), 3)
    if cycle_type(old_row) != (16,) or parts.index(cycle_type(old_row)) != 54:
        raise AssertionError("old Etzion--Hartman row is not branch 54")

    source = flag_permutation(colours, SOURCE_T, SOURCE_E, SOURCE_Q)
    source_cycles = cycle_decomposition(source)
    source_type = tuple(sorted(len(cycle) for cycle in source_cycles))
    if source_type != (2, 2, 2, 2, 2, 2, 2, 2):
        raise AssertionError("selected Etzion--Hartman flag is not branch 0")
    if parts.index(source_type) != 0 or permutation_sign(source) != 1:
        raise AssertionError("selected flag has the wrong branch/sign")

    target = canonical_permutation(source_type)
    target_cycles = cycle_decomposition(target)
    if len(source_cycles) != len(target_cycles):
        raise AssertionError("source/target cycle count mismatch")

    # Map e -> 01, r -> 2, q -> 3, then conjugate the eight transpositions
    # on the complement to the canonical branch-0 transpositions.
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
            raise AssertionError("point map does not conjugate the selected row")

    # The colour map is uniquely forced by canonical normalization of the
    # transformed root star SOURCE_T -> 012.
    colour_map = {}
    for point in POINTS:
        if point in SOURCE_T:
            continue
        old_colour = partial_colour(colours, SOURCE_T + (point,))
        new_point = point_map[point]
        if not 3 <= new_point < 20:
            raise AssertionError("root-extension point mapped into the root")
        colour_map[old_colour] = new_point - 3
    if set(colour_map) != set(COLOURS) or set(colour_map.values()) != set(COLOURS):
        raise AssertionError("constructed colour map is not bijective")

    transformed = transformed_partial(colours, point_map, colour_map)
    verify_partial(transformed)
    if sum(value >= 0 for value in transformed) != 4_773:
        raise AssertionError("transformation changed the assigned-block count")
    if sum(value < 0 for value in transformed) != 72:
        raise AssertionError("transformation changed the hole count")

    for point in range(3, 20):
        if partial_colour(transformed, (0, 1, 2, point)) != point - 3:
            raise AssertionError("transformed root star is not canonical")

    branch0 = manifest["branches"][0]
    for unit in branch0["units"]:
        block = tuple(unit["block"])
        if partial_colour(transformed, block) != unit["colour"]:
            raise AssertionError(f"transformed partial misses branch-0 unit {block}")

    transformed_row = flag_permutation(transformed, (0, 1, 2), (0, 1), 3)
    if transformed_row != target:
        raise AssertionError("transformed row is not the canonical branch-0 row")

    digest = hashlib.sha256(partial_bytes(transformed)).hexdigest()
    print("[exact] Etzion--Hartman assigned / holes: 4773 / 72")
    print("[exact] old fixed flag type / branch: (16) / 54")
    print("[exact] selected flag B,T,e,r,q:",
          SOURCE_B, SOURCE_T, SOURCE_E, SOURCE_R, SOURCE_Q)
    print("[exact] selected flag type / branch:", source_type, "/ 0")
    print("[exact] point map:", [point_map[point] for point in POINTS])
    print("[exact] colour map:", [colour_map[colour] for colour in COLOURS])
    print("[exact] transformed branch-0 partial SHA-256:", digest)
    print("[exact] transformed partial semantic checks: PASS")
    return point_map, colour_map, digest


def main() -> None:
    parts, manifest = section_branch_and_parity()
    section_eh(parts, manifest)
    print()
    print("PASS: the 28 even branches are lossless for LS(3,4,20).")
    print("SCOPE: LS(3,4,20) remains unresolved.  Nonexistence would exclude")
    print("k=16 only; existence would not solve Erdos--Rosenfeld #835.")


if __name__ == "__main__":
    main()
