#!/usr/bin/env python3
"""Emit a complete symmetry-normalized CNF for LS(3,4,20).

An LS(3,4,20) is a colouring of all 4-subsets of a 20-point set with
17 colours such that the 17 extensions of every 3-subset receive all
17 colours.  Every LS(15,16,32) derives to this object, so a certified
UNSAT result for this CNF would exclude the k=16 case of Problem #835.
A SAT result is only a necessary derived-design witness.

The encoding has one primary variable x(B,c) for every block and colour.
A Sinz sequential counter gives each block exactly one colour.  For every
triple and colour, one at-least-one clause over its 17 extensions is then
enough: there are 17 singly coloured extensions and 17 colours, so the
clauses force a rainbow star.  The 17 extensions of {0,1,2} are assigned
the 17 colours to remove only the global colour symmetry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Iterator


POINTS = 20
BLOCK_SIZE = 4
STRENGTH = 3
COLOURS = 17
SCHEMA = "ls-3-4-20-generic-sinz-v1"
BLOCKS = tuple(combinations(range(POINTS), BLOCK_SIZE))
TRIPLES = tuple(combinations(range(POINTS), STRENGTH))
BLOCK_INDEX = {block: index for index, block in enumerate(BLOCKS)}


def primary(block: int, colour: int) -> int:
    return COLOURS * block + colour + 1


def auxiliary(block: int, position: int, primary_count: int) -> int:
    return primary_count + (COLOURS - 1) * block + position + 1


def dimensions() -> dict[str, int]:
    blocks = len(BLOCKS)
    triples = len(TRIPLES)
    primary_variables = blocks * COLOURS
    auxiliary_variables = blocks * (COLOURS - 1)
    block_alo_clauses = blocks
    block_amo_clauses = blocks * (3 * COLOURS - 4)
    star_alo_clauses = triples * COLOURS
    symmetry_unit_clauses = COLOURS
    return {
        "points": POINTS,
        "blocks": blocks,
        "triples": triples,
        "colours": COLOURS,
        "primary_variables": primary_variables,
        "auxiliary_variables": auxiliary_variables,
        "variables": primary_variables + auxiliary_variables,
        "block_alo_clauses": block_alo_clauses,
        "block_amo_clauses": block_amo_clauses,
        "star_alo_clauses": star_alo_clauses,
        "symmetry_unit_clauses": symmetry_unit_clauses,
        "clauses": (
            block_alo_clauses
            + block_amo_clauses
            + star_alo_clauses
            + symmetry_unit_clauses
        ),
    }


def symmetry_units() -> list[tuple[int, int]]:
    root = (0, 1, 2)
    units = []
    for colour, point in enumerate(range(3, POINTS)):
        block = tuple(sorted(root + (point,)))
        units.append((BLOCK_INDEX[block], colour))
    assert len(units) == COLOURS
    return units


def clause_lines(stats: dict[str, int]) -> Iterator[str]:
    primary_count = stats["primary_variables"]
    for block in range(len(BLOCKS)):
        yield " ".join(str(primary(block, colour)) for colour in range(COLOURS)) + " 0\n"
        yield f"{-primary(block, 0)} {auxiliary(block, 0, primary_count)} 0\n"
        for colour in range(1, COLOURS - 1):
            previous = auxiliary(block, colour - 1, primary_count)
            current = auxiliary(block, colour, primary_count)
            yield f"{-primary(block, colour)} {current} 0\n"
            yield f"{-previous} {current} 0\n"
            yield f"{-primary(block, colour)} {-previous} 0\n"
        yield (
            f"{-primary(block, COLOURS - 1)} "
            f"{-auxiliary(block, COLOURS - 2, primary_count)} 0\n"
        )

    universe = set(range(POINTS))
    for triple in TRIPLES:
        extensions = [
            BLOCK_INDEX[tuple(sorted(triple + (point,)))]
            for point in sorted(universe - set(triple))
        ]
        assert len(extensions) == COLOURS
        for colour in range(COLOURS):
            yield " ".join(
                str(primary(block, colour)) for block in extensions
            ) + " 0\n"

    for block, colour in symmetry_units():
        yield f"{primary(block, colour)} 0\n"


def canonical_map(stats: dict[str, int]) -> bytes:
    payload = {
        "schema": SCHEMA,
        "constants": {
            "points": POINTS,
            "block_size": BLOCK_SIZE,
            "strength": STRENGTH,
            "colours": COLOURS,
        },
        "variable_layout": {
            "primary": "x(B,c)=17*B+c+1 in lexicographic 4-subset order",
            "sinz_auxiliary": (
                "s(B,i)=primary_count+16*B+i+1 for 0<=i<16"
            ),
        },
        "blocks": [list(block) for block in BLOCKS],
        "counts": stats,
    }
    return (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def write_cnf(path: Path, stats: dict[str, int]) -> str:
    digest = hashlib.sha256()
    clauses = 0
    with path.open("wb") as stream:
        header = f"p cnf {stats['variables']} {stats['clauses']}\n".encode("ascii")
        stream.write(header)
        digest.update(header)
        for line in clause_lines(stats):
            encoded = line.encode("ascii")
            stream.write(encoded)
            digest.update(encoded)
            clauses += 1
    assert clauses == stats["clauses"]
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    stats = dimensions()
    assert stats == {
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
    for output in (args.cnf, args.map, args.manifest):
        output.parent.mkdir(parents=True, exist_ok=True)
    map_bytes = canonical_map(stats)
    cnf_sha256 = write_cnf(args.cnf, stats)
    args.map.write_bytes(map_bytes)
    manifest = {
        "schema": SCHEMA,
        "cnf_sha256": cnf_sha256,
        "map_sha256": hashlib.sha256(map_bytes).hexdigest(),
        "counts": stats,
        "symmetry_units": [
            {
                "block_index": block,
                "block": list(BLOCKS[block]),
                "colour": colour,
            }
            for block, colour in symmetry_units()
        ],
    }
    args.manifest.write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
