#!/usr/bin/env python3
"""Independent audit of the C17-equivariant LS(3,4,20) extension search."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verify_fixed_link_cnf import construct_link  # noqa: E402


P = 17
POINTS = tuple(range(19))
PARENT_POINTS = tuple(range(20))
COLOURS = tuple(range(P))
EXPECTED_BLOCK_ORBITS = 228
EXPECTED_TRIPLE_ORBITS = 57


def canonical(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(values))


def translate(values: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return canonical(
        tuple((value + amount) % P if value < P else value for value in values)
    )


def make_orbits(size: int) -> tuple[tuple[int, ...], ...]:
    all_subsets = set(itertools.combinations(POINTS, size))
    result = []
    while all_subsets:
        seed = min(all_subsets)
        representative = min(translate(seed, amount) for amount in range(P))
        orbit = {translate(representative, amount) for amount in range(P)}
        if len(orbit) != P:
            raise AssertionError("non-free orbit in independent reconstruction")
        result.append(representative)
        all_subsets.difference_update(orbit)
    return tuple(sorted(result))


def locate(
    subset: tuple[int, ...],
    representatives: tuple[tuple[int, ...], ...],
) -> tuple[int, int]:
    candidates = []
    for orbit, representative in enumerate(representatives):
        for shift in range(P):
            if translate(representative, shift) == canonical(subset):
                candidates.append((orbit, shift))
    if len(candidates) != 1:
        raise AssertionError("subset does not have one orbit coordinate")
    return candidates[0]


def variable(orbit: int, colour: int) -> int:
    return 1 + P * orbit + colour


def expected_clauses(
    encoding: str,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    link = construct_link()
    block_representatives = make_orbits(4)
    triple_representatives = make_orbits(3)
    if (
        len(block_representatives) != EXPECTED_BLOCK_ORBITS
        or len(triple_representatives) != EXPECTED_TRIPLE_ORBITS
    ):
        raise AssertionError("wrong independently reconstructed orbit census")

    clauses = []
    for orbit in range(EXPECTED_BLOCK_ORBITS):
        clauses.append(tuple(variable(orbit, colour) for colour in COLOURS))
        for first, second in itertools.combinations(COLOURS, 2):
            clauses.append((-variable(orbit, first), -variable(orbit, second)))

    for triple in triple_representatives:
        entries = [
            locate(canonical(triple + (point,)), block_representatives)
            for point in POINTS
            if point not in triple
        ]
        if len(entries) != 16 or len(set(entries)) != 16:
            raise AssertionError("bad extension orbit coordinates")
        root_colour = link[triple]
        for orbit, shift in entries:
            clauses.append((-variable(orbit, (root_colour - shift) % P),))
        if encoding == "pairwise":
            for (orbit_a, shift_a), (orbit_b, shift_b) in itertools.combinations(
                entries, 2
            ):
                if orbit_a == orbit_b:
                    if shift_a == shift_b:
                        raise AssertionError("duplicate translated block")
                    continue
                for colour_a in COLOURS:
                    colour_b = (colour_a + shift_a - shift_b) % P
                    clauses.append(
                        (-variable(orbit_a, colour_a), -variable(orbit_b, colour_b))
                    )
        elif encoding == "cover":
            for required in COLOURS:
                if required == root_colour:
                    continue
                clauses.append(
                    tuple(
                        variable(orbit, (required - shift) % P)
                        for orbit, shift in entries
                    )
                )
        else:
            raise ValueError(f"unknown encoding: {encoding}")

    return (
        block_representatives,
        triple_representatives,
        tuple(clauses),
    )


def parse_cnf(path: Path) -> tuple[int, tuple[tuple[int, ...], ...]]:
    lines = path.read_text(encoding="ascii").splitlines()
    header = lines[0].split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise AssertionError("invalid DIMACS header")
    variables, declared_clauses = map(int, header[2:])
    clauses = []
    for line in lines[1:]:
        values = tuple(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise AssertionError("invalid DIMACS clause")
        clauses.append(values[:-1])
    if len(clauses) != declared_clauses:
        raise AssertionError("DIMACS clause count mismatch")
    return variables, tuple(clauses)


def verify_instance(
    cnf_path: Path, map_path: Path
) -> tuple[
    tuple[tuple[int, ...], ...],
    str,
    str,
]:
    mapping = json.loads(map_path.read_text(encoding="ascii"))
    encoding = mapping.get("encoding", "pairwise")
    block_representatives, triple_representatives, clauses = expected_clauses(encoding)
    variables, actual_clauses = parse_cnf(cnf_path)
    if variables != P * EXPECTED_BLOCK_ORBITS:
        raise AssertionError("wrong DIMACS variable count")
    if actual_clauses != clauses:
        raise AssertionError("DIMACS clauses differ from independent reconstruction")

    if mapping["schema"] != "erdos835-c17-equivariant-ls3420-v1":
        raise AssertionError("wrong map schema")
    expected_metadata = {
        "finite_points": list(range(P)),
        "fixed_points": [17, 18],
        "colour_modulus": P,
        "variable_rule": "1 + 17 * block_orbit_index + base_colour",
        "translate_rule": "finite points and colour add shift modulo 17",
        "variables": P * EXPECTED_BLOCK_ORBITS,
        "clauses": len(clauses),
    }
    for key, value in expected_metadata.items():
        if mapping.get(key) != value:
            raise AssertionError(f"wrong map metadata field: {key}")
    expected_scope = (
        "SAT constructs LS(3,4,20); UNSAT excludes only the C17-equivariant "
        "extension of this fixed cyclic LS(2,3,19)"
    )
    if mapping.get("scope") != expected_scope:
        raise AssertionError("wrong map scope")
    if mapping["block_representatives"] != [
        list(block) for block in block_representatives
    ]:
        raise AssertionError("block representatives differ")
    if mapping["triple_representatives"] != [
        list(triple) for triple in triple_representatives
    ]:
        raise AssertionError("triple representatives differ")
    cnf_digest = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    if mapping["cnf_sha256"] != cnf_digest:
        raise AssertionError("map carries the wrong CNF digest")
    map_digest = hashlib.sha256(map_path.read_bytes()).hexdigest()
    return block_representatives, cnf_digest, map_digest


def parse_model(path: Path) -> set[int]:
    positives = set()
    statuses = []
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            statuses.append(line.split()[1:])
        elif line.startswith("v "):
            positives.update(
                literal for literal in map(int, line[2:].split()) if literal > 0
            )
    if statuses != [["SATISFIABLE"]]:
        raise AssertionError("model must contain exactly 's SATISFIABLE'")
    return positives


def verify_model(
    path: Path,
    block_representatives: tuple[tuple[int, ...], ...],
) -> str:
    positives = parse_model(path)
    phases = []
    for orbit in range(EXPECTED_BLOCK_ORBITS):
        assigned = [
            colour for colour in COLOURS if variable(orbit, colour) in positives
        ]
        if len(assigned) != 1:
            raise AssertionError(f"orbit {orbit} has {len(assigned)} phases")
        phases.append(assigned[0])

    nonroot_colours = {}
    for orbit, representative in enumerate(block_representatives):
        for shift in range(P):
            block = translate(representative, shift)
            colour = (phases[orbit] + shift) % P
            if block in nonroot_colours:
                raise AssertionError("duplicate expanded quadruple")
            nonroot_colours[block] = colour
    if set(nonroot_colours) != set(itertools.combinations(POINTS, 4)):
        raise AssertionError("expanded phases do not cover all quadruples")

    link = construct_link()
    full_colours = {}
    for old_block, colour in nonroot_colours.items():
        full_colours[tuple(value + 1 for value in old_block)] = colour
    for old_triple, colour in link.items():
        full_colours[(0,) + tuple(value + 1 for value in old_triple)] = colour
    all_blocks = tuple(itertools.combinations(PARENT_POINTS, 4))
    if set(full_colours) != set(all_blocks):
        raise AssertionError("expanded witness does not colour every 4-set")

    for triple in itertools.combinations(PARENT_POINTS, 3):
        colours = {
            full_colours[canonical(triple + (point,))]
            for point in PARENT_POINTS
            if point not in triple
        }
        if colours != set(COLOURS):
            raise AssertionError(f"triple star {triple} is not rainbow")

    if Counter(full_colours.values()) != Counter({colour: 285 for colour in COLOURS}):
        raise AssertionError("colour classes do not all have 285 blocks")
    for colour in COLOURS:
        coverage = Counter(
            triple
            for block, assigned in full_colours.items()
            if assigned == colour
            for triple in itertools.combinations(block, 3)
        )
        if len(coverage) != len(tuple(itertools.combinations(PARENT_POINTS, 3))) or set(
            coverage.values()
        ) != {1}:
            raise AssertionError(f"colour {colour} is not an S(3,4,20)")

    colour_bytes = bytes(full_colours[block] for block in all_blocks)
    return hashlib.sha256(colour_bytes).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()
    representatives, cnf_digest, map_digest = verify_instance(args.cnf, args.map)
    print("[ok] independently reconstructed all 228 block and 57 triple orbits")
    print("[ok] every DIMACS clause and every map representative is exact")
    print(f"[exact] CNF SHA-256: {cnf_digest}")
    print(f"[exact] map SHA-256: {map_digest}")
    if args.model is None:
        print("[scope] no solver verdict is asserted")
    else:
        witness_digest = verify_model(args.model, representatives)
        print("[theorem] witness is a complete C17-equivariant LS(3,4,20)")
        print(f"[exact] canonical block-colour SHA-256: {witness_digest}")
    print("status: PASS")


if __name__ == "__main__":
    main()
