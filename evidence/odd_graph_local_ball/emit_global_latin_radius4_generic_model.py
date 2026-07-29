#!/usr/bin/env python3
"""Emit a fully assigned generic radius-four CNF model from the L/M/N witness.

The L/M/N witness in ``../global_latin_radius4_certificate.py`` uses the
coordinates from ``radius4_reduction.md``: its root has colour infinity (16),
and the root neighbour B minus {u} has colour u.  The generic CNF instead
normalizes the root to 0 and those neighbours (in omitted-bit order) to
1,...,16.  This program applies the forced colour relabelling

    16 -> 0,  u -> u+1,

and the remaining free permutation of the fifteen root points.  The latter is
chosen so that the fifteen C_(0,i) branch vertices receive the further CNF
normalization 2,...,16.  It is therefore a genuine witness for the *generic*
unrestricted radius-four CNF, not merely for the coordinate-specific L/M/N
reduction.

The output is a complete SAT-competition assignment: every primary and every
Sinz auxiliary variable is written.  The companion verifier independently
checks both the subset-colouring semantics and every DIMACS clause.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

# The L/M/N construction deliberately remains the source of the certificate.
EVIDENCE = Path(__file__).resolve().parents[1]
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from global_latin_audit import construct_golf17
from global_latin_radius4_certificate import (  # type: ignore[import-not-found]
    COLORS,
    FINITE,
    FINITE_EDGES,
    INDEX_EDGES,
    INFINITY,
    SQUARES,
    construct_one_n,
    verify_l_m,
)


POINTS = 31
SET_SIZE = 15
COLOURS = 17
ROOT = (1 << SET_SIZE) - 1
ALL_POINTS = (1 << POINTS) - 1
PRIMARY_COUNT = 14657 * COLOURS
AUXILIARY_COUNT = 14657 * (COLOURS - 1)
VARIABLE_COUNT = PRIMARY_COUNT + AUXILIARY_COUNT


def primary(vertex: int, colour: int) -> int:
    return COLOURS * vertex + colour + 1


def auxiliary(vertex: int, index: int) -> int:
    return PRIMARY_COUNT + (COLOURS - 1) * vertex + index + 1


def neighbours(vertex: int):
    complement = ALL_POINTS ^ vertex
    while complement:
        bit = complement & -complement
        complement ^= bit
        yield ALL_POINTS ^ vertex ^ bit


def make_ball() -> tuple[list[int], list[int], dict[int, int]]:
    vertices, distances, positions = [ROOT], [0], {ROOT: 0}
    cursor = 0
    while cursor < len(vertices):
        vertex = vertices[cursor]
        distance = distances[cursor]
        cursor += 1
        if distance == 4:
            continue
        for next_vertex in neighbours(vertex):
            if next_vertex not in positions:
                positions[next_vertex] = len(vertices)
                vertices.append(next_vertex)
                distances.append(distance + 1)
    return vertices, distances, positions


def old_colour(colour: int) -> int:
    """The generic-CNF colour corresponding to the L/M/N colour."""

    if colour == INFINITY:
        return 0
    assert colour in FINITE
    return colour + 1


def branch_point_permutation(golf: list[list[list[int]]]) -> list[int]:
    """Map generic A-point i to an old L/M/N square index.

    In the generic ball the branch vertices adjacent to B minus {0} are
    enumerated as C_(0,0),...,C_(0,14), and must get colours 2,...,16.  The
    golf identity says the old values L_i(0) are precisely 1,...,15, so this
    map exists uniquely.
    """

    old_for_value = {golf[old_i][0][INFINITY]: old_i for old_i in SQUARES}
    if set(old_for_value) != set(range(1, 16)):
        raise AssertionError("golf branch values are not exactly 1,...,15")
    permutation = [old_for_value[generic_i + 1] for generic_i in SQUARES]
    if sorted(permutation) != list(SQUARES):
        raise AssertionError("branch normalization is not a permutation")
    return permutation


def old_sets(mask: int, point_permutation: list[int]) -> tuple[set[int], set[int]]:
    """Translate a generic subset to old A/B coordinate labels.

    A generic point i maps to the old A point point_permutation[i].  A generic
    point 15+u maps to the old B point u.  This only permutes the 31 ground
    points, hence preserves Odd-graph adjacency and the radius-four ball.
    """

    old_a, old_b = set(), set()
    for generic_point in range(POINTS):
        if not (mask >> generic_point) & 1:
            continue
        if generic_point < 15:
            old_a.add(point_permutation[generic_point])
        else:
            old_b.add(generic_point - 15)
    return old_a, old_b


def construct_colours() -> tuple[list[int], dict[str, object]]:
    golf = construct_golf17()
    verify_l_m(golf)
    point_permutation = branch_point_permutation(golf)

    certificates: dict[tuple[int, int], dict[tuple[int, int], int]] = {}
    serial = bytearray()
    for u, v in FINITE_EDGES:
        certificate, _ = construct_one_n(golf, u, v)
        certificates[u, v] = certificate
        serial.extend(certificate[edge] for edge in INDEX_EDGES)
    n_sha256 = hashlib.sha256(serial).hexdigest()
    expected_n_sha256 = "f03067f8614037a067820970da11ca73cba16e6a62cab334c11a70a44e399cba"
    if n_sha256 != expected_n_sha256:
        raise AssertionError(f"unexpected deterministic N hash: {n_sha256}")

    vertices, distances, _ = make_ball()
    if [distances.count(layer) for layer in range(5)] != [1, 16, 240, 1800, 12600]:
        raise AssertionError("unexpected generic radius-four ball")
    colours: list[int] = []
    for position, mask in enumerate(vertices):
        old_a, old_b = old_sets(mask, point_permutation)
        if len(old_a) == 15 and not old_b:
            value = INFINITY
        elif not old_a and len(old_b) == 15:
            (u,) = set(FINITE) - old_b
            value = u
        elif len(old_a) == 14 and len(old_b) == 1:
            (i,) = set(SQUARES) - old_a
            (u,) = old_b
            value = golf[i][u][INFINITY]
        elif len(old_a) == 1 and len(old_b) == 14:
            (i,) = old_a
            u, v = sorted(set(FINITE) - old_b)
            value = golf[i][u][v]
        elif len(old_a) == 13 and len(old_b) == 2:
            i, j = sorted(set(SQUARES) - old_a)
            u, v = sorted(old_b)
            value = certificates[u, v][i, j]
        else:
            raise AssertionError(f"unexpected sphere coordinate at {position}: {len(old_a)}, {len(old_b)}")
        colours.append(old_colour(value))

    metadata: dict[str, object] = {
        "schema": "odd-graph-o16-radius4-global-latin-bridge-v1",
        "n_certificate_sha256": n_sha256,
        "old_to_generic_colour": {"16": 0, **{str(u): u + 1 for u in FINITE}},
        "generic_a_to_lmn_square": point_permutation,
        "layer_sizes": [distances.count(layer) for layer in range(5)],
    }
    return colours, metadata


def write_complete_model(path: Path, colours: list[int]) -> str:
    """Write a full assignment satisfying the primary and Sinz clauses."""

    digest = hashlib.sha256()
    with path.open("w", encoding="utf-8") as stream:
        def emit(line: str) -> None:
            stream.write(line)
            digest.update(line.encode("ascii"))

        emit("s SATISFIABLE\n")
        line: list[str] = []
        # The Sinz state s(v,i) is true iff the selected primary colour <= i.
        for vertex, selected in enumerate(colours):
            for colour in range(COLOURS):
                literal = primary(vertex, colour)
                line.append(str(literal if colour == selected else -literal))
                if len(line) == 1000:
                    emit("v " + " ".join(line) + "\n")
                    line = []
            for index in range(COLOURS - 1):
                literal = auxiliary(vertex, index)
                line.append(str(literal if selected <= index else -literal))
                if len(line) == 1000:
                    emit("v " + " ".join(line) + "\n")
                    line = []
        if line:
            emit("v " + " ".join(line) + "\n")
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True, help="complete SAT-competition model output")
    parser.add_argument("--colouring", type=Path, required=True, help="semantic colouring JSON output")
    parser.add_argument("--manifest", type=Path, required=True, help="bridge metadata JSON output")
    args = parser.parse_args()

    colours, metadata = construct_colours()
    for output in (args.model, args.colouring, args.manifest):
        output.parent.mkdir(parents=True, exist_ok=True)
    model_sha256 = write_complete_model(args.model, colours)
    colouring = {
        "schema": metadata["schema"],
        "colours": colours,
        "colour_histogram": [colours.count(colour) for colour in range(COLOURS)],
    }
    colouring_bytes = (json.dumps(colouring, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    args.colouring.write_bytes(colouring_bytes)
    metadata["model_sha256"] = model_sha256
    metadata["colouring_sha256"] = hashlib.sha256(colouring_bytes).hexdigest()
    metadata["variables"] = VARIABLE_COUNT
    args.manifest.write_text(json.dumps(metadata, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
