#!/usr/bin/env python3
"""Independent semantic and byte-level audit of the 55 second-star branches.

This verifier deliberately does not import either generator.  It reconstructs
the block order, all cycle types, canonical permutations, primary literals,
cube byte stream, branch-CNF hashes, conjugacy-class sizes, and the manifest
self-hash.  The equality between the sum of the 55 class sizes and !16 is an
exact exhaustiveness check for all possible derangement rows.

Optionally, it also reconstructs and authenticates one materialized plain or
pairwise-star-AMO branch CNF byte for byte via SHA-256 and DIMACS counts.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Iterator


N = 20
C = 17
QPOINTS = tuple(range(3, 20))
DOMAIN = tuple(range(4, 20))
FOURS = tuple(combinations(range(N), 4))
THREES = tuple(combinations(range(N), 3))
FOUR_INDEX = {block: index for index, block in enumerate(FOURS)}
SCHEMA = "ls-3-4-20-second-star-branches-v1"


def x(block: int, colour: int) -> int:
    return C * block + colour + 1


def partitions(total: int, lower: int = 2) -> Iterator[tuple[int, ...]]:
    if total == 0:
        yield ()
        return
    for first in range(lower, total + 1):
        remaining = total - first
        if remaining and remaining < first:
            continue
        for tail in partitions(remaining, first):
            yield (first,) + tail


def permutation_for(parts: tuple[int, ...]) -> dict[int, int]:
    answer: dict[int, int] = {}
    cursor = 0
    for size in parts:
        cycle = DOMAIN[cursor : cursor + size]
        if len(cycle) != size:
            raise AssertionError("cycle type overruns the domain")
        for index, value in enumerate(cycle):
            answer[value] = cycle[(index + 1) % size]
        cursor += size
    if cursor != len(DOMAIN):
        raise AssertionError("cycle type does not fill the domain")
    return answer


def cycle_type(permutation: dict[int, int]) -> tuple[int, ...]:
    unseen = set(permutation)
    result = []
    while unseen:
        start = min(unseen)
        current = start
        length = 0
        while True:
            if current not in unseen:
                if current != start:
                    raise AssertionError("mapping is not a permutation")
                break
            unseen.remove(current)
            length += 1
            current = permutation[current]
        result.append(length)
    return tuple(sorted(result))


def centralizer(parts: tuple[int, ...]) -> int:
    counts = Counter(parts)
    answer = 1
    for length, multiplicity in counts.items():
        answer *= length**multiplicity * math.factorial(multiplicity)
    return answer


def derangements(n: int) -> int:
    if n == 0:
        return 1
    if n == 1:
        return 0
    before, current = 1, 0
    for size in range(2, n + 1):
        before, current = current, (size - 1) * (current + before)
    return current


def parse_parent(parent: bytes) -> tuple[int, int, bytes]:
    header, newline, body = parent.partition(b"\n")
    if not newline:
        raise AssertionError("parent has no header newline")
    fields = header.split()
    if len(fields) != 4 or fields[:2] != [b"p", b"cnf"]:
        raise AssertionError("invalid parent header")
    return int(fields[2]), int(fields[3]), body


def expected_branch_hash(
    body: bytes,
    variables: int,
    clauses: int,
    assumptions: list[int],
) -> str:
    digest = hashlib.sha256()
    digest.update(
        f"p cnf {variables} {clauses + len(assumptions)}\n".encode("ascii")
    )
    digest.update(body)
    for literal in assumptions:
        digest.update(f"{literal} 0\n".encode("ascii"))
    return digest.hexdigest()


def expected_cubes(parent_hash: str, branches: list[dict[str, object]]) -> bytes:
    lines = [
        f"c {SCHEMA}\n",
        f"c parent_cnf_sha256 {parent_hash}\n",
        (
            "c WLOG orbit representatives under the residual diagonal "
            "point-colour symmetry; not a literal partition of labelled models\n"
        ),
    ]
    for branch in branches:
        label = ",".join(str(part) for part in branch["cycle_type"])
        lines.append(f"c branch {branch['id']:02d} cycle_type {label}\n")
        lines.append(
            "a "
            + " ".join(str(value) for value in branch["assumptions"])
            + " 0\n"
        )
    return "".join(lines).encode("ascii")


def expected_augmented_hash(
    body: bytes,
    variables: int,
    clauses: int,
    assumptions: list[int],
) -> tuple[str, int]:
    amo_count = len(THREES) * C * math.comb(C, 2)
    output_clauses = clauses + amo_count + len(assumptions)
    digest = hashlib.sha256()
    digest.update(f"p cnf {variables} {output_clauses}\n".encode("ascii"))
    digest.update(body)
    universe = set(range(N))
    for triple in THREES:
        extensions = [
            FOUR_INDEX[tuple(sorted(triple + (point,)))]
            for point in sorted(universe - set(triple))
        ]
        if len(extensions) != C:
            raise AssertionError("wrong reconstructed star size")
        for colour in range(C):
            for left, right in combinations(extensions, 2):
                digest.update(
                    f"{-x(left, colour)} {-x(right, colour)} 0\n".encode("ascii")
                )
    for literal in assumptions:
        digest.update(f"{literal} 0\n".encode("ascii"))
    return digest.hexdigest(), output_clauses


def parse_dimacs(path: Path) -> tuple[int, int, int, str]:
    variables = declared = None
    actual = 0
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for raw in stream:
            digest.update(raw)
            fields = raw.split()
            if not fields:
                raise AssertionError("blank DIMACS line")
            if fields[0] == b"p":
                if variables is not None or len(fields) != 4 or fields[1] != b"cnf":
                    raise AssertionError("invalid or repeated DIMACS header")
                variables, declared = int(fields[2]), int(fields[3])
            else:
                if variables is None or fields[-1] != b"0":
                    raise AssertionError("invalid DIMACS clause")
                literals = [int(value) for value in fields[:-1]]
                if (
                    not literals
                    or any(value == 0 or abs(value) > variables for value in literals)
                ):
                    raise AssertionError("invalid literal in DIMACS clause")
                actual += 1
    if variables is None or declared is None:
        raise AssertionError("missing DIMACS header")
    return variables, declared, actual, digest.hexdigest()


def small_exact_control() -> None:
    """Exhaustively check the conjugacy classification through degree eight."""

    for degree in range(2, 9):
        observed: Counter[tuple[int, ...]] = Counter()
        for values in itertools.permutations(range(degree)):
            if any(index == value for index, value in enumerate(values)):
                continue
            mapping = {index: value for index, value in enumerate(values)}
            observed[cycle_type(mapping)] += 1
        expected = {}
        for parts in partitions(degree):
            expected[parts] = math.factorial(degree) // centralizer(parts)
        if dict(observed) != expected:
            raise AssertionError(f"small conjugacy control failed at degree {degree}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-cnf", type=Path, required=True)
    parser.add_argument("--parent-manifest", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--cubes", type=Path, required=True)
    parser.add_argument("--branch-cnf", type=Path)
    parser.add_argument("--branch-id", type=int)
    parser.add_argument("--star-pairwise-amo", action="store_true")
    args = parser.parse_args()
    if (args.branch_cnf is None) != (args.branch_id is None):
        parser.error("--branch-cnf and --branch-id must be supplied together")
    if args.star_pairwise_amo and args.branch_cnf is None:
        parser.error("--star-pairwise-amo requires --branch-cnf")

    parent_bytes = args.parent_cnf.read_bytes()
    parent_hash = hashlib.sha256(parent_bytes).hexdigest()
    variables, clauses, body = parse_parent(parent_bytes)
    if (variables, clauses) != (159_885, 251_957):
        raise AssertionError("wrong parent dimensions")
    parent_manifest = json.loads(args.parent_manifest.read_text(encoding="utf-8"))
    if parent_manifest.get("cnf_sha256") != parent_hash:
        raise AssertionError("parent manifest hash mismatch")

    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    if payload.get("schema") != SCHEMA:
        raise AssertionError("wrong schema")
    if payload.get("parent") != {
        "path": str(args.parent_cnf),
        "sha256": parent_hash,
        "variables": variables,
        "clauses": clauses,
    }:
        raise AssertionError("parent metadata mismatch")

    parts_list = list(partitions(len(DOMAIN)))
    if len(parts_list) != 55:
        raise AssertionError("there are not 55 derangement cycle types")
    recorded_branches = payload.get("branches")
    if not isinstance(recorded_branches, list) or len(recorded_branches) != 55:
        raise AssertionError("wrong branch list")

    reconstructed = []
    class_total = 0
    for branch_id, parts in enumerate(parts_list):
        permutation = permutation_for(parts)
        if cycle_type(permutation) != parts:
            raise AssertionError("canonical permutation has wrong type")
        if any(permutation[value] == value for value in DOMAIN):
            raise AssertionError("canonical row is not a derangement")
        assumptions = []
        units = []
        for point in DOMAIN:
            image = permutation[point]
            block = tuple(sorted((0, 1, 3, point)))
            colour = image - 3
            literal = x(FOUR_INDEX[block], colour)
            assumptions.append(literal)
            units.append(
                {
                    "point": point,
                    "image_point": image,
                    "block_index": FOUR_INDEX[block],
                    "block": list(block),
                    "colour": colour,
                    "colour_point": image,
                    "literal": literal,
                }
            )

        # The root extension by point 2 has colour-point 3.  The canonical
        # row supplies every other colour exactly once.
        row_colours = [3] + [permutation[value] for value in DOMAIN]
        if sorted(row_colours) != list(QPOINTS):
            raise AssertionError("second star is not rainbow")
        # For triple {0,1,r}, its root-normalized extension by point 2 has
        # colour-point r.  Derangement is exactly the immediate noncollision.
        if any(permutation[value] == value for value in DOMAIN):
            raise AssertionError("second row collides with a root unit")

        z_value = centralizer(parts)
        class_size = math.factorial(16) // z_value
        class_total += class_size
        reconstructed.append(
            {
                "id": branch_id,
                "cycle_type": list(parts),
                "canonical_row_images": [
                    permutation[point] for point in DOMAIN
                ],
                "assumptions": assumptions,
                "units": units,
                "centralizer_order_in_sym16": z_value,
                "derangement_conjugacy_class_size": class_size,
                "geometric_branch_stabilizer_order": 2 * z_value,
                "branch_cnf_variables": variables,
                "branch_cnf_clauses": clauses + 16,
                "branch_cnf_sha256": expected_branch_hash(
                    body, variables, clauses, assumptions
                ),
            }
        )
    if reconstructed != recorded_branches:
        raise AssertionError("branch manifest differs from independent reconstruction")

    exact_derangements = derangements(16)
    if class_total != exact_derangements:
        raise AssertionError("cycle-type classes do not exhaust all derangements")
    if payload.get("derangement_count") != exact_derangements:
        raise AssertionError("manifest derangement total mismatch")
    if payload.get("branch_count") != 55 or payload.get(
        "cube_literal_count_per_branch"
    ) != 16:
        raise AssertionError("wrong summary counts")

    cubes = expected_cubes(parent_hash, reconstructed)
    if args.cubes.read_bytes() != cubes:
        raise AssertionError("cube byte stream mismatch")
    if payload.get("cubes_sha256") != hashlib.sha256(cubes).hexdigest():
        raise AssertionError("cube hash mismatch")

    unhashed = dict(payload)
    self_hash = unhashed.pop("manifest_sha256_without_self", None)
    canonical = (
        json.dumps(unhashed, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    if self_hash != hashlib.sha256(canonical).hexdigest():
        raise AssertionError("manifest self-hash mismatch")

    small_exact_control()

    branch_report = None
    if args.branch_cnf is not None and args.branch_id is not None:
        if not 0 <= args.branch_id < len(reconstructed):
            raise AssertionError("branch id out of range")
        branch = reconstructed[args.branch_id]
        if args.star_pairwise_amo:
            expected_hash, expected_clauses = expected_augmented_hash(
                body,
                variables,
                clauses,
                branch["assumptions"],
            )
        else:
            expected_hash = branch["branch_cnf_sha256"]
            expected_clauses = branch["branch_cnf_clauses"]
        parsed = parse_dimacs(args.branch_cnf)
        if parsed != (variables, expected_clauses, expected_clauses, expected_hash):
            raise AssertionError(
                f"materialized branch mismatch: parsed {parsed}, "
                f"expected {(variables, expected_clauses, expected_clauses, expected_hash)}"
            )
        branch_report = {
            "branch_id": args.branch_id,
            "cycle_type": branch["cycle_type"],
            "star_pairwise_amo": args.star_pairwise_amo,
            "variables": variables,
            "clauses": expected_clauses,
            "sha256": expected_hash,
        }

    report = {
        "status": "PASS",
        "schema": SCHEMA,
        "parent_cnf_sha256": parent_hash,
        "branch_count": 55,
        "cycle_types": len(parts_list),
        "derangement_count": exact_derangements,
        "sum_of_conjugacy_class_sizes": class_total,
        "small_exact_conjugacy_controls": "degrees 2 through 8 PASS",
        "cubes_sha256": hashlib.sha256(cubes).hexdigest(),
        "manifest_sha256_without_self": self_hash,
        "materialized_branch": branch_report,
        "scope": (
            "lossless for LS(3,4,20); UNSAT of all branches would exclude "
            "only the k=16 case of Erdos-Rosenfeld #835"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
