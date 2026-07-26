#!/usr/bin/env python3
"""Independently audit the generic LS(3,4,20) Sinz CNF.

This verifier intentionally does not import the generator.  It reconstructs
the 4-subsets, triple stars, Sinz clauses, symmetry normalization, exact byte
stream, and SHA-256 digest.  It also parses the supplied DIMACS file and
checks the canonical map and manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Iterator


N = 20
K = 4
T = 3
Q = 17
SCHEMA = "ls-3-4-20-generic-sinz-v1"
FOURS = tuple(combinations(range(N), K))
THREES = tuple(combinations(range(N), T))
FOUR_INDEX = {block: index for index, block in enumerate(FOURS)}


def x(block: int, colour: int) -> int:
    return Q * block + colour + 1


def s(block: int, position: int, primary_count: int) -> int:
    return primary_count + (Q - 1) * block + position + 1


def audited_counts() -> dict[str, int]:
    blocks = len(FOURS)
    triples = len(THREES)
    primary = blocks * Q
    auxiliary = blocks * (Q - 1)
    block_alo = blocks
    block_amo = blocks * (3 * Q - 4)
    star_alo = triples * Q
    units = Q
    return {
        "points": N,
        "blocks": blocks,
        "triples": triples,
        "colours": Q,
        "primary_variables": primary,
        "auxiliary_variables": auxiliary,
        "variables": primary + auxiliary,
        "block_alo_clauses": block_alo,
        "block_amo_clauses": block_amo,
        "star_alo_clauses": star_alo,
        "symmetry_unit_clauses": units,
        "clauses": block_alo + block_amo + star_alo + units,
    }


def normalized_units() -> list[tuple[int, int]]:
    root = (0, 1, 2)
    return [
        (FOUR_INDEX[tuple(sorted(root + (point,)))], colour)
        for colour, point in enumerate(range(3, N))
    ]


def expected_lines(stats: dict[str, int]) -> Iterator[bytes]:
    yield f"p cnf {stats['variables']} {stats['clauses']}\n".encode("ascii")
    primary_count = stats["primary_variables"]
    for block in range(len(FOURS)):
        yield (
            " ".join(str(x(block, colour)) for colour in range(Q)) + " 0\n"
        ).encode("ascii")
        yield f"{-x(block, 0)} {s(block, 0, primary_count)} 0\n".encode("ascii")
        for colour in range(1, Q - 1):
            previous = s(block, colour - 1, primary_count)
            current = s(block, colour, primary_count)
            yield f"{-x(block, colour)} {current} 0\n".encode("ascii")
            yield f"{-previous} {current} 0\n".encode("ascii")
            yield f"{-x(block, colour)} {-previous} 0\n".encode("ascii")
        yield (
            f"{-x(block, Q - 1)} {-s(block, Q - 2, primary_count)} 0\n"
        ).encode("ascii")

    all_points = set(range(N))
    for triple in THREES:
        extensions = [
            FOUR_INDEX[tuple(sorted(triple + (point,)))]
            for point in sorted(all_points - set(triple))
        ]
        if len(extensions) != Q:
            raise AssertionError("wrong star size")
        for colour in range(Q):
            yield (
                " ".join(str(x(block, colour)) for block in extensions) + " 0\n"
            ).encode("ascii")

    for block, colour in normalized_units():
        yield f"{x(block, colour)} 0\n".encode("ascii")


def parse_dimacs(path: Path) -> tuple[int, int, int, Counter[int], str]:
    variables = declared_clauses = None
    clauses = 0
    lengths: Counter[int] = Counter()
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for raw in stream:
            digest.update(raw)
            fields = raw.split()
            if not fields:
                raise AssertionError("blank DIMACS line")
            if fields[0] == b"c":
                raise AssertionError("canonical DIMACS must not contain comments")
            if fields[0] == b"p":
                if variables is not None or len(fields) != 4 or fields[1] != b"cnf":
                    raise AssertionError("invalid or duplicate DIMACS header")
                variables = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            if variables is None or fields[-1] != b"0":
                raise AssertionError("clause before header or missing terminator")
            literals = [int(field) for field in fields[:-1]]
            if not literals or any(literal == 0 or abs(literal) > variables for literal in literals):
                raise AssertionError("invalid literal")
            clauses += 1
            lengths[len(literals)] += 1
    if variables is None or declared_clauses is None:
        raise AssertionError("missing DIMACS header")
    return variables, declared_clauses, clauses, lengths, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    stats = audited_counts()
    expected_stats = {
        "points": 20,
        "blocks": 4_845,
        "triples": 1_140,
        "colours": 17,
        "primary_variables": 82_365,
        "auxiliary_variables": 77_520,
        "variables": 159_885,
        "block_alo_clauses": 4_845,
        "block_amo_clauses": 227_715,
        "star_alo_clauses": 19_380,
        "symmetry_unit_clauses": 17,
        "clauses": 251_957,
    }
    if stats != expected_stats:
        raise AssertionError(f"wrong reconstructed dimensions: {stats}")

    expected_digest = hashlib.sha256()
    expected_clauses = 0
    expected_lengths: Counter[int] = Counter()
    for line in expected_lines(stats):
        expected_digest.update(line)
        if not line.startswith(b"p "):
            expected_clauses += 1
            expected_lengths[len(line.split()) - 1] += 1
    if expected_clauses != stats["clauses"]:
        raise AssertionError("wrong reconstructed clause count")

    variables, declared, parsed, lengths, digest = parse_dimacs(args.cnf)
    if (variables, declared, parsed) != (
        stats["variables"],
        stats["clauses"],
        stats["clauses"],
    ):
        raise AssertionError("DIMACS dimensions disagree")
    if lengths != expected_lengths:
        raise AssertionError(f"clause lengths disagree: {lengths}")
    if digest != expected_digest.hexdigest():
        raise AssertionError("DIMACS byte stream differs from independent reconstruction")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA or manifest.get("counts") != stats:
        raise AssertionError("manifest schema or counts disagree")
    if manifest.get("cnf_sha256") != digest:
        raise AssertionError("manifest CNF hash disagrees")
    units = [
        {
            "block_index": block,
            "block": list(FOURS[block]),
            "colour": colour,
        }
        for block, colour in normalized_units()
    ]
    if manifest.get("symmetry_units") != units:
        raise AssertionError("symmetry units disagree")

    map_bytes = args.map.read_bytes()
    if manifest.get("map_sha256") != hashlib.sha256(map_bytes).hexdigest():
        raise AssertionError("manifest map hash disagrees")
    mapping = json.loads(map_bytes)
    if mapping.get("schema") != SCHEMA or mapping.get("counts") != stats:
        raise AssertionError("map schema or counts disagree")
    if mapping.get("blocks") != [list(block) for block in FOURS]:
        raise AssertionError("canonical block order disagrees")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema": SCHEMA,
                "cnf_sha256": digest,
                "map_sha256": hashlib.sha256(map_bytes).hexdigest(),
                "counts": stats,
                "clause_lengths": {
                    str(length): count
                    for length, count in sorted(lengths.items())
                },
                "symmetry_units": len(units),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
