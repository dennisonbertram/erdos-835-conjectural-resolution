#!/usr/bin/env python3
"""Search and semantically verify the smallest nontrivial fan control.

For k=6 the general simultaneous-fan construction has:

* a common LS(2,3,9) link;
* q=k-3=3 extension labels; and
* a 378-cell conflict graph whose constraint groups all have size three.

This is a control for possible fan obstructions.  It says nothing directly
about k=16 or Erdős--Rosenfeld Problem #835.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from itertools import combinations
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OPUS = REPO / "collaboration" / "opus5" / "holonomy_followup"
sys.path.insert(0, str(OPUS))

from verify_holonomy_followup import build_ls239  # noqa: E402


Triple = tuple[int, int, int]
Quad = tuple[int, int, int, int]
Cell = tuple[Quad, int]
Group = tuple[int, ...]


def build_control_from_link(
    link: dict[frozenset[int], int],
) -> tuple[tuple[Cell, ...], tuple[Group, ...]]:
    """Build the q=3 cell hypergraph from a labelled LS(2,3,9)."""
    points = tuple(range(9))
    colours = tuple(range(7))
    if len(link) != 84:
        raise RuntimeError("large set has the wrong number of triples")
    for pair in combinations(points, 2):
        star = {link[frozenset((*pair, x))] for x in points if x not in pair}
        if star != set(colours):
            raise RuntimeError("large-set pair star is not rainbow")

    cells: list[Cell] = []
    allowed: dict[Quad, tuple[int, ...]] = {}
    for quad in combinations(points, 4):
        face_colours = {link[frozenset(face)] for face in combinations(quad, 3)}
        if len(face_colours) != 4:
            raise RuntimeError("quadruple faces are not rainbow")
        allowed[quad] = tuple(c for c in colours if c not in face_colours)
        if len(allowed[quad]) != 3:
            raise RuntimeError("quadruple does not allow three colours")
        cells.extend((quad, c) for c in allowed[quad])

    index = {cell: i for i, cell in enumerate(cells)}
    if len(index) != 378:
        raise RuntimeError("wrong cell count")

    groups: list[Group] = []
    for quad in combinations(points, 4):
        groups.append(tuple(index[(quad, c)] for c in allowed[quad]))

    for triple in combinations(points, 3):
        for colour in colours:
            if colour == link[frozenset(triple)]:
                continue
            members = tuple(
                index[(quad, colour)]
                for x in points
                if x not in triple
                for quad in (tuple(sorted(triple + (x,))),)
                if colour in allowed[quad]
            )
            if len(members) != 3:
                raise RuntimeError("triple-colour group does not have size three")
            groups.append(members)

    if len(groups) != 126 + 84 * 6 == 630:
        raise RuntimeError("wrong group count")
    if any(len(set(group)) != 3 for group in groups):
        raise RuntimeError("invalid group")
    return tuple(cells), tuple(groups)


def build_control() -> tuple[tuple[Cell, ...], tuple[Group, ...]]:
    """Build the control from the deterministic backtracking large set."""
    return build_control_from_link(build_ls239())


def var(cell: int, label: int) -> int:
    return 3 * cell + label + 1


def build_cnf(cell_count: int, groups: tuple[Group, ...]) -> list[tuple[int, ...]]:
    """Encode one label per cell and every label once in every 3-group."""
    clauses: list[tuple[int, ...]] = []
    for cell in range(cell_count):
        clauses.append(tuple(var(cell, a) for a in range(3)))
        for a, b in combinations(range(3), 2):
            clauses.append((-var(cell, a), -var(cell, b)))

    for group in groups:
        for label in range(3):
            clauses.append(tuple(var(cell, label) for cell in group))

    # Global extension-label symmetry.
    for label, cell in enumerate(groups[0]):
        clauses.append((var(cell, label),))
    return clauses


def solve(
    cells: tuple[Cell, ...],
    groups: tuple[Group, ...],
) -> tuple[str, tuple[int, ...] | None]:
    clauses = build_cnf(len(cells), groups)
    nvars = 3 * len(cells)
    with tempfile.TemporaryDirectory(prefix="erdos835-k6-fan-") as tmp:
        cnf = Path(tmp) / "control.cnf"
        model = Path(tmp) / "control.model"
        with cnf.open("w") as fh:
            fh.write(f"p cnf {nvars} {len(clauses)}\n")
            for clause in clauses:
                fh.write(" ".join(map(str, clause)) + " 0\n")
        proc = subprocess.run(
            ["cadical", "-q", "-t", "300", "-w", str(model), str(cnf)],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 20:
            return "UNSAT_UNCERTIFIED", None
        if proc.returncode != 10:
            return f"UNKNOWN(exit {proc.returncode})", None

        positive: set[int] = set()
        for line in model.read_text().splitlines():
            if line.startswith("v "):
                positive.update(int(x) for x in line.split()[1:] if int(x) > 0)
        labels = []
        for cell in range(len(cells)):
            chosen = [a for a in range(3) if var(cell, a) in positive]
            if len(chosen) != 1:
                raise RuntimeError("solver model is not one-hot")
            labels.append(chosen[0])
        return "SAT", tuple(labels)


def verify(
    cells: tuple[Cell, ...],
    groups: tuple[Group, ...],
    labels: tuple[int, ...],
) -> None:
    if len(labels) != len(cells):
        raise RuntimeError("wrong assignment length")
    if set(labels) - {0, 1, 2}:
        raise RuntimeError("label outside range")
    for group in groups:
        if {labels[cell] for cell in group} != {0, 1, 2}:
            raise RuntimeError("constraint group is not rainbow")


def main() -> None:
    cells, groups = build_control()
    status, labels = solve(cells, groups)
    print(f"status: {status}")
    print(f"cells: {len(cells)}")
    print(f"groups: {len(groups)}")
    if labels is None:
        print("scope: no certified mathematical conclusion")
        return
    verify(cells, groups, labels)
    payload = bytes(labels)
    print("semantic verification: PASS")
    print(f"assignment_sha256: {hashlib.sha256(payload).hexdigest()}")
    print("label_counts:", tuple(labels.count(a) for a in range(3)))
    print("scope: a k=6 fan control exists; this does not address k=16 or #835")


if __name__ == "__main__":
    main()
