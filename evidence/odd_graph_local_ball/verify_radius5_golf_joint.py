#!/usr/bin/env python3
"""Independent semantic verifier for a fixed-golf joint radius-5 witness."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import deque
from itertools import combinations
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parents[1]
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))
from global_latin_audit import construct_golf17

COLORS = tuple(range(17))
FINITE = tuple(range(16))
SQUARES = tuple(range(15))
UVS = tuple(combinations(FINITE, 2))
IJS = tuple(combinations(SQUARES, 2))
TRIPLES = tuple(combinations(FINITE, 3))
ROOT = (1 << 15) - 1
ALL = (1 << 31) - 1
SCHEMA = "odd-graph-o16-radius5-fixed-golf-joint-v1"


def golf_sha256(golf: list[list[list[int]]]) -> str:
    return hashlib.sha256(bytes(value for square in golf for row in square for value in row)).hexdigest()


def n_allowed(golf: list[list[list[int]]], i: int, uv: tuple[int, int]) -> set[int]:
    u, v = uv
    return set(COLORS) - {golf[i][u][v], golf[i][u][16], golf[i][v][16]}


def verify_l_m(golf: list[list[list[int]]]) -> None:
    """Check Conditions 1--3 of the radius-four reduction independently."""
    for u in FINITE:
        assert {golf[i][u][16] for i in SQUARES} == set(FINITE) - {u}
    for i in SQUARES:
        assert {golf[i][u][16] for u in FINITE} == set(FINITE)
        assert all(golf[i][u][16] != u for u in FINITE)
        for u in FINITE:
            assert {golf[i][min(u, v)][max(u, v)] for v in FINITE if v != u} == set(COLORS) - {u, golf[i][u][16]}
    for u, v in UVS:
        assert {golf[i][u][v] for i in SQUARES} == set(COLORS) - {u, v}


def neighbours(vertex: int):
    complement = ALL ^ vertex
    while complement:
        bit = complement & -complement
        complement ^= bit
        yield ALL ^ vertex ^ bit


def make_ball():
    vertices, distances, positions = [ROOT], [0], {ROOT: 0}
    queue = deque([ROOT])
    while queue:
        vertex = queue.popleft()
        if distances[positions[vertex]] == 5:
            continue
        for other in neighbours(vertex):
            if other not in positions:
                positions[other] = len(vertices)
                vertices.append(other)
                distances.append(distances[positions[vertex]] + 1)
                queue.append(other)
    return vertices, distances, positions


def unpack(payload: dict[str, object]):
    values_n, values_p = payload.get("n_values"), payload.get("p_values")
    if not isinstance(values_n, list) or not isinstance(values_p, list) or len(values_n) != 12600 or len(values_p) != 58800:
        raise AssertionError("wrong N/P vector dimensions")
    if any(not isinstance(value, int) or value not in COLORS for value in values_n + values_p):
        raise AssertionError("N/P values are outside 0..16")
    n = {(u, v, i, j): values_n[index] for index, (u, v, i, j) in enumerate(a + b for a in UVS for b in IJS)}
    p = {(i, j, u, v, w): values_p[index] for index, (i, j, u, v, w) in enumerate(a + b for a in IJS for b in TRIPLES)}
    return n, p


def colour_ball(golf, n, p):
    vertices, distances, positions = make_ball()
    if [distances.count(level) for level in range(6)] != [1, 16, 240, 1800, 12600, 58800]:
        raise AssertionError("wrong radius-five ball layers")
    colours = []
    for mask in vertices:
        a = {item for item in SQUARES if (mask >> item) & 1}
        b = {item for item in FINITE if (mask >> (15 + item)) & 1}
        if len(a) == 15 and not b:
            value = 16
        elif not a and len(b) == 15:
            value = next(iter(set(FINITE) - b))
        elif len(a) == 14 and len(b) == 1:
            value = golf[next(iter(set(SQUARES) - a))][next(iter(b))][16]
        elif len(a) == 1 and len(b) == 14:
            i = next(iter(a)); u, v = sorted(set(FINITE) - b); value = golf[i][u][v]
        elif len(a) == 13 and len(b) == 2:
            i, j = sorted(set(SQUARES) - a); u, v = sorted(b); value = n[u, v, i, j]
        elif len(a) == 2 and len(b) == 13:
            i, j = sorted(a); u, v, w = sorted(set(FINITE) - b); value = p[i, j, u, v, w]
        else:
            raise AssertionError("unrecognized ball coordinate")
        colours.append(value)
    return vertices, distances, colours, positions


def verify_payload(payload: dict[str, object], semantic_ball: bool = True) -> dict[str, object]:
    unhashed = dict(payload)
    recorded = unhashed.pop("sha256_without_hash", None)
    if payload.get("schema") != SCHEMA or not isinstance(recorded, str):
        raise AssertionError("wrong certificate schema/hash")
    expected_hash = hashlib.sha256((json.dumps(unhashed, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")).hexdigest()
    if recorded != expected_hash:
        raise AssertionError("certificate self-hash mismatch")
    golf = construct_golf17()
    verify_l_m(golf)
    if payload.get("golf_sha256") != golf_sha256(golf):
        raise AssertionError("certificate is for a different golf L/M")
    n, p = unpack(payload)
    for u, v in UVS:
        for i in SQUARES:
            incident = {n[u, v, min(i, j), max(i, j)] for j in SQUARES if j != i}
            if incident != n_allowed(golf, i, (u, v)):
                raise AssertionError(f"N_{u}_{v} fails at {i}")
    for i, j in IJS:
        for u, v in UVS:
            values = {p[(i, j) + tuple(sorted((u, v, w)))] for w in FINITE if w not in (u, v)}
            expected = set(COLORS) - {n[u, v, i, j], golf[i][u][v], golf[j][u][v]}
            if values != expected:
                raise AssertionError(f"P_{i}_{j} fails extension at {(u, v)}")
    report: dict[str, object] = {"status": "PASS", "n_values": 12600, "p_values": 58800, "golf_sha256": golf_sha256(golf)}
    if semantic_ball:
        vertices, distances, colours, positions = colour_ball(golf, n, p)
        centres = 0
        for item, vertex in enumerate(vertices):
            if distances[item] == 5:
                continue
            closed = [colours[item]] + [colours[positions[other]] for other in neighbours(vertex)]
            if sorted(closed) != list(COLORS):
                raise AssertionError(f"non-bijective closed neighbourhood at {item}")
            centres += 1
        report.update({"vertices": len(vertices), "constrained_centres": centres, "semantic_ball_verified": True})
    return report


def audit_model() -> dict[str, object]:
    """Recompute fixed-golf domains, constraint counts, and ball geometry without CP-SAT."""
    golf = construct_golf17()
    verify_l_m(golf)
    n_domain_values = sum(
        len(n_allowed(golf, i, (u, v)) & n_allowed(golf, j, (u, v)))
        for u, v in UVS for i, j in IJS
    )
    p_domain_values = 0
    for i, j in IJS:
        for triple in TRIPLES:
            forbidden = {golf[i][u][v] for u, v in combinations(triple, 2)} | {golf[j][u][v] for u, v in combinations(triple, 2)}
            p_domain_values += 17 - len(forbidden)
    vertices, distances, _ = make_ball()
    if [distances.count(level) for level in range(6)] != [1, 16, 240, 1800, 12600, 58800]:
        raise AssertionError("radius-five ball count mismatch")
    report = {
        "status": "PASS", "schema": SCHEMA, "golf_sha256": golf_sha256(golf),
        "n_variables": len(UVS) * len(IJS), "p_variables": len(IJS) * len(TRIPLES),
        "integer_variables": len(UVS) * len(IJS) + len(IJS) * len(TRIPLES),
        "n_domain_values": n_domain_values, "p_domain_values": p_domain_values,
        "n_all_different": len(UVS) * len(SQUARES), "p_all_different": len(IJS) * len(UVS),
        "n_p_not_equal": len(IJS) * len(UVS) * 14,
        "vertices": len(vertices), "constrained_centres": sum(level < 5 for level in distances),
    }
    if (report["n_variables"], report["p_variables"], report["n_domain_values"], report["p_domain_values"]) != (12600, 58800, 143640, 670320):
        raise AssertionError("fixed-golf domain counts mismatch")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--reduced-only", action="store_true")
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    if args.audit_only:
        if args.certificate is not None:
            parser.error("--audit-only does not take --certificate")
        print(json.dumps(audit_model(), indent=2, sort_keys=True))
        return
    if args.certificate is None:
        parser.error("--certificate is required unless --audit-only is used")
    payload = json.loads(args.certificate.read_text(encoding="utf-8"))
    print(json.dumps(verify_payload(payload, semantic_ball=not args.reduced_only), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
