#!/usr/bin/env python3
"""Standard-library verifier for an EH j=5 repair witness.

This program does not import OR-Tools or the search code.  It authenticates
the source fifteen-system core, verifies the twelve claimed retained systems,
and checks all 1,140 triple stars of the proposed LS(3,4,20).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_seed.txt"
SOURCE_SHA256 = "b1ea090d3e3b88366c87e95660c1c82a406d2c3b100cc1d39bcc2c7e8fde47f9"
POINTS = tuple(range(20))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
TRIPLES = tuple(itertools.combinations(POINTS, 3))
COLOURS = set(range(17))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(
    path: Path,
    expected_sha256: str | None = None,
) -> dict[tuple[int, ...], int]:
    if expected_sha256 is not None and sha256(path) != expected_sha256:
        raise AssertionError(f"{path}: source SHA-256 mismatch")
    rows = path.read_text(encoding="ascii").splitlines()
    if len(rows) != len(BLOCKS):
        raise AssertionError(f"{path}: expected 4,845 rows")
    answer: dict[tuple[int, ...], int] = {}
    for line_number, (expected_block, raw) in enumerate(zip(BLOCKS, rows), 1):
        fields = tuple(map(int, raw.split()))
        if len(fields) != 5 or fields[:4] != expected_block:
            raise AssertionError(f"{path}:{line_number}: malformed/out-of-order block")
        if fields[4] not in COLOURS:
            raise AssertionError(f"{path}:{line_number}: invalid colour")
        answer[expected_block] = fields[4]
    return answer


def parse_drop(values: list[int]) -> tuple[int, int, int]:
    case = tuple(sorted(values))
    if len(case) != 3 or len(set(case)) != 3 or case[0] < 0 or case[-1] >= 15:
        raise argparse.ArgumentTypeError(
            "--drop needs three distinct source labels in 0,...,14"
        )
    return case


def verify(
    source: dict[tuple[int, ...], int],
    witness: dict[tuple[int, ...], int],
    dropped: tuple[int, int, int],
) -> None:
    source_counts = Counter(source.values())
    if source_counts != Counter({colour: 285 for colour in range(17)}):
        raise AssertionError("authenticated source has unexpected counts")

    for colour in range(15):
        source_system = {block for block, value in source.items() if value == colour}
        triple_counts: Counter[tuple[int, ...]] = Counter(
            triple
            for block in source_system
            for triple in itertools.combinations(block, 3)
        )
        if (
            len(source_system) != 285
            or set(triple_counts) != set(TRIPLES)
            or set(triple_counts.values()) != {1}
        ):
            raise AssertionError(f"source colour {colour} is not an SQS(20)")
        if colour not in dropped and any(
            witness[block] != colour for block in source_system
        ):
            raise AssertionError(f"witness changed retained system {colour}")

    for triple in TRIPLES:
        extensions = [
            witness[tuple(sorted((*triple, point)))]
            for point in POINTS
            if point not in triple
        ]
        if set(extensions) != COLOURS:
            raise AssertionError(f"triple {triple}: extensions are not all 17 colours")

    witness_counts = Counter(witness.values())
    if witness_counts != Counter({colour: 285 for colour in range(17)}):
        raise AssertionError("witness classes do not all have 285 blocks")

    for colour in range(17):
        system = {block for block, value in witness.items() if value == colour}
        triple_counts: Counter[tuple[int, ...]] = Counter(
            triple for block in system for triple in itertools.combinations(block, 3)
        )
        if set(triple_counts) != set(TRIPLES) or set(triple_counts.values()) != {1}:
            raise AssertionError(f"witness colour {colour} is not an SQS(20)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("witness", type=Path)
    parser.add_argument("--drop", type=int, nargs=3, required=True)
    args = parser.parse_args()
    dropped = parse_drop(args.drop)
    source = load(SOURCE, SOURCE_SHA256)
    witness = load(args.witness)
    verify(source, witness, dropped)
    print(
        "PASS: exact LS(3,4,20); all 17 classes are SQS(20)s; "
        f"the 12 EH systems outside {dropped} are retained."
    )


if __name__ == "__main__":
    main()
