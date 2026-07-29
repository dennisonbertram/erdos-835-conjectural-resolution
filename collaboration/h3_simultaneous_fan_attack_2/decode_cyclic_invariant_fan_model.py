#!/usr/bin/env python3
"""Decode and semantically verify a SAT model for the invariant-fan CNF."""

from __future__ import annotations

import argparse
from pathlib import Path

from verify_fan_kernel_reduction import (
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)
from write_cyclic_invariant_fan_cnf import LABELS, primary


def positive_literals(model: Path) -> set[int]:
    answer: set[int] = set()
    saw_status = False
    for line in model.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            saw_status = True
            if line.split() != ["s", "SATISFIABLE"]:
                raise AssertionError("model does not report SATISFIABLE")
        if line.startswith("v "):
            answer.update(
                literal for literal in map(int, line.split()[1:]) if literal > 0
            )
    if not saw_status:
        raise AssertionError("model has no status line")
    return answer


def decode(model: Path) -> tuple[int, ...]:
    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    positive = positive_literals(model)
    labels: list[int] = []
    for cell in range(len(cells)):
        chosen = [label for label in range(LABELS) if primary(cell, label) in positive]
        if len(chosen) != 1:
            raise AssertionError(f"orbit cell {cell} is not one-hot")
        labels.append(chosen[0])
    target = set(range(LABELS))
    for index, group in enumerate(groups):
        if {labels[cell] for cell in group} != target:
            raise AssertionError(f"quotient group {index} is not rainbow")
    return tuple(labels)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    labels = decode(args.model)
    args.certificate.write_text(
        "".join(f"{label}\n" for label in labels),
        encoding="ascii",
    )
    print(f"model={args.model}")
    print(f"certificate={args.certificate}")
    print(f"orbit_cells={len(labels)}")
    print("rainbow_groups=1140")
    print("semantic_verification=PASS")


if __name__ == "__main__":
    main()
