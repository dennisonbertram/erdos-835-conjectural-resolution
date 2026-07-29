#!/usr/bin/env python3
"""Independent checker for a claimed LS(3,4,20) colour certificate."""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path


POINTS = tuple(range(20))
COLOURS = set(range(17))
BLOCKS = set(combinations(POINTS, 4))


def load(path: Path) -> dict[tuple[int, int, int, int], int]:
    values: dict[tuple[int, int, int, int], int] = {}
    for line_number, raw in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        fields = raw.split()
        if len(fields) != 5:
            raise ValueError(f"line {line_number}: expected five integers")
        *points, colour = map(int, fields)
        block = tuple(points)
        if block not in BLOCKS:
            raise ValueError(
                f"line {line_number}: not a sorted 4-subset of 0,...,19"
            )
        if colour not in COLOURS:
            raise ValueError(f"line {line_number}: colour outside 0,...,16")
        if block in values:
            raise ValueError(f"line {line_number}: repeated block {block}")
        values[block] = colour
    if set(values) != BLOCKS:
        missing = sorted(BLOCKS - set(values))
        raise ValueError(
            f"certificate has {len(values)} blocks; "
            f"first missing blocks: {missing[:5]}"
        )
    return values


def verify(values: dict[tuple[int, int, int, int], int]) -> None:
    for triple in combinations(POINTS, 3):
        extensions = [
            values[tuple(sorted((*triple, point)))]
            for point in POINTS
            if point not in triple
        ]
        if set(extensions) != COLOURS:
            raise ValueError(
                f"triple {triple}: extension colours are not 0,...,16"
            )

    for colour in sorted(COLOURS):
        class_blocks = [
            block for block, label in values.items() if label == colour
        ]
        if len(class_blocks) != 285:
            raise ValueError(
                f"colour {colour}: {len(class_blocks)} blocks, expected 285"
            )
        for triple in combinations(POINTS, 3):
            multiplicity = sum(
                set(triple).issubset(block) for block in class_blocks
            )
            if multiplicity != 1:
                raise ValueError(
                    f"colour {colour}, triple {triple}: "
                    f"multiplicity {multiplicity}, expected 1"
                )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    values = load(args.certificate)
    verify(values)
    print(
        "PASS: 4,845 blocks form a proper 17-colouring of J(20,4); "
        "all 17 colour classes are independently verified SQS(20)s."
    )


if __name__ == "__main__":
    main()
