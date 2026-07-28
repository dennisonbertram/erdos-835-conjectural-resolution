#!/usr/bin/env python3
"""Dependency-free independent audit of the six r=1 SAT certificates.

This script does not import the generator.  It independently enumerates the
support matchings, reconstructs every semantic and unary-counter clause, checks
the DIMACS byte content through its parsed clauses, checks the recorded hashes,
and optionally invokes an external DRAT-trim binary.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import tempfile
from itertools import combinations
from pathlib import Path


POINTS = tuple(range(13))
ALL_EDGES = tuple(combinations(POINTS, 2))
FIRST_TRIPLE = frozenset((10, 11, 12))
FIRST_SUPPORT = frozenset(POINTS) - FIRST_TRIPLE
ORBIT_CASES = ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (3, 0))


def enumerate_one_factors(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return (frozenset(),)
    anchor = vertices[0]
    answer = []
    for position, mate in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        pair = tuple(sorted((anchor, mate)))
        for continuation in enumerate_one_factors(remainder):
            answer.append(frozenset((pair, *continuation)))
    return tuple(answer)


def second_support(intersection):
    shared = tuple(sorted(FIRST_TRIPLE))[:intersection]
    new = tuple(range(7, 10))[: 3 - intersection]
    second_triple = frozenset((*shared, *new))
    return frozenset(POINTS) - second_triple


def orbit_representative(intersection, internal_pairs):
    support1 = second_support(intersection)
    exceptional = sorted(FIRST_SUPPORT - support1)
    common = sorted(FIRST_SUPPORT & support1)
    pairs = []
    for _ in range(internal_pairs):
        pairs.append(tuple(sorted((exceptional.pop(0), exceptional.pop(0)))))
    while exceptional:
        pairs.append(tuple(sorted((exceptional.pop(0), common.pop(0)))))
    while common:
        pairs.append(tuple(sorted((common.pop(0), common.pop(0)))))
    return frozenset(pairs)


class IndependentEncoding:
    """A second implementation of the documented exact unary encoding."""

    def __init__(self):
        self.next_id = 1
        self.names = {}
        self.rows = []
        self.one = self._id(("truth", 1))
        self.zero = self._id(("truth", 0))
        self._clause(self.one)
        self._clause(-self.zero)

    def _id(self, description):
        value = self.names.get(description)
        if value is None:
            value = self.next_id
            self.next_id += 1
            self.names[description] = value
        return value

    def _clause(self, *row):
        self.rows.append(tuple(row))

    def _bounded_sum(self, label, inputs, minimum=None, maximum=None):
        length = len(inputs)
        needed = 0
        if minimum:
            needed = max(needed, minimum)
        if maximum is not None and maximum < length:
            needed = max(needed, maximum + 1)
        if needed == 0:
            return

        def prefix_count(prefix, count):
            if count == 0:
                return self.one
            if prefix == 0 or count > prefix:
                return self.zero
            return self._id(("count", label, prefix, count))

        for prefix in range(1, length + 1):
            item = inputs[prefix - 1]
            for count in range(1, min(prefix, needed) + 1):
                now = prefix_count(prefix, count)
                without_item = prefix_count(prefix - 1, count)
                prior_count = prefix_count(prefix - 1, count - 1)
                self._clause(-without_item, now)
                self._clause(-prior_count, -item, now)
                self._clause(-now, without_item, prior_count)
                self._clause(-now, without_item, item)
        if minimum:
            self._clause(prefix_count(length, minimum))
        if maximum is not None and maximum < length:
            self._clause(-prefix_count(length, maximum + 1))


def reconstruct(intersection, internal_pairs):
    if (intersection, internal_pairs) not in ORBIT_CASES:
        raise AssertionError("unexpected case")
    support0 = FIRST_SUPPORT
    support1 = second_support(intersection)
    factors = (
        enumerate_one_factors(sorted(support0)),
        enumerate_one_factors(sorted(support1)),
    )
    fixed = orbit_representative(intersection, internal_pairs)
    fixed_position = factors[0].index(fixed)
    model = IndependentEncoding()

    def colour_edge(colour, edge):
        return model._id(("coloured", colour, edge))

    def in_deletion(edge):
        return model._id(("deleted", edge))

    def survives(side, number):
        return model._id(("survives", side, number))

    for colour, required in enumerate((4, 4, 4, 4, 5, 5)):
        variables = [colour_edge(colour, edge) for edge in ALL_EDGES]
        model._bounded_sum(
            ("colour_total", colour),
            variables,
            minimum=required,
            maximum=required,
        )
        for point in POINTS:
            model._bounded_sum(
                ("colour_at_point", colour, point),
                [
                    colour_edge(colour, edge)
                    for edge in ALL_EDGES
                    if point in edge
                ],
                maximum=1,
            )

    for edge in ALL_EDGES:
        coloured = [colour_edge(colour, edge) for colour in range(6)]
        model._bounded_sum(("colours_on_edge", edge), coloured, maximum=1)
        for variable in coloured:
            model._clause(-variable, in_deletion(edge))
        model._clause(-in_deletion(edge), *coloured)

    for point in POINTS:
        model._bounded_sum(
            ("deletion_degree", point),
            [in_deletion(edge) for edge in ALL_EDGES if point in edge],
            minimum=1,
            maximum=5,
        )

    for side, family in enumerate(factors):
        for number, factor in enumerate(family):
            flag = survives(side, number)
            blockers = [in_deletion(edge) for edge in sorted(factor)]
            for blocker in blockers:
                model._clause(-flag, -blocker)
            model._clause(flag, *blockers)

    model._clause(survives(0, fixed_position))
    model._clause(*(survives(1, number) for number in range(len(factors[1]))))

    disjoint_count = 0
    for left_number, left in enumerate(factors[0]):
        for right_number, right in enumerate(factors[1]):
            if left.isdisjoint(right):
                disjoint_count += 1
                model._clause(
                    -survives(0, left_number),
                    -survives(1, right_number),
                )

    for edge in combinations(sorted(support0 & support1), 2):
        alternatives = []
        for side, family in enumerate(factors):
            alternatives.extend(
                survives(side, number)
                for number, factor in enumerate(family)
                if edge not in factor
            )
        model._clause(*alternatives)

    return model, {
        "variables": model.next_id - 1,
        "clauses": len(model.rows),
        "disjoint_pairs": disjoint_count,
        "fixed_matching": [list(edge) for edge in sorted(fixed)],
    }


def read_dimacs(payload):
    comments = []
    header = None
    clauses = []
    for raw_line in payload.decode("ascii").splitlines():
        if raw_line.startswith("c "):
            comments.append(raw_line[2:])
        elif raw_line.startswith("p cnf "):
            _, _, variables, count = raw_line.split()
            header = (int(variables), int(count))
        elif raw_line:
            values = tuple(map(int, raw_line.split()))
            if not values or values[-1] != 0:
                raise AssertionError("malformed DIMACS clause")
            clauses.append(values[:-1])
    if header is None or header[1] != len(clauses):
        raise AssertionError("bad or missing DIMACS header")
    return comments, header, clauses


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def check_orbits():
    observed = {}
    for intersection in range(4):
        support1 = second_support(intersection)
        exceptional = FIRST_SUPPORT - support1
        signatures = {
            sum(edge[0] in exceptional and edge[1] in exceptional for edge in factor)
            for factor in enumerate_one_factors(sorted(FIRST_SUPPORT))
        }
        expected = set(range(len(exceptional) // 2 + 1))
        if signatures != expected:
            raise AssertionError((intersection, signatures, expected))
        observed[intersection] = sorted(signatures)
    union = {
        (intersection, signature)
        for intersection, signatures in observed.items()
        for signature in signatures
    }
    if union != set(ORBIT_CASES):
        raise AssertionError("the six cases do not exhaust the support-pair orbits")
    return observed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate-dir",
        type=Path,
        default=Path(__file__).with_name("certificates"),
    )
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()

    manifest = json.loads(
        (args.certificate_dir / "manifest.json").read_text(encoding="utf-8")
    )
    print(f"PASS orbit exhaustion {check_orbits()}")

    for intersection, internal_pairs in ORBIT_CASES:
        stem = f"o{intersection}_x{internal_pairs}"
        record = manifest[stem]
        cnf_payload = gzip.decompress(
            (args.certificate_dir / f"{stem}.cnf.gz").read_bytes()
        )
        proof_payload = gzip.decompress(
            (args.certificate_dir / f"{stem}.drat.gz").read_bytes()
        )
        _, header, clauses = read_dimacs(cnf_payload)
        expected, facts = reconstruct(intersection, internal_pairs)
        if header != (facts["variables"], facts["clauses"]):
            raise AssertionError((stem, "header", header, facts))
        if clauses != expected.rows:
            raise AssertionError((stem, "semantic clause mismatch"))
        if digest(cnf_payload) != record["cnf_sha256"]:
            raise AssertionError((stem, "CNF hash mismatch"))
        if digest(proof_payload) != record["drat_sha256"]:
            raise AssertionError((stem, "DRAT hash mismatch"))
        for key in ("variables", "clauses", "disjoint_pairs", "fixed_matching"):
            if facts[key] != record[key]:
                raise AssertionError((stem, key, facts[key], record[key]))

        if args.drat_trim:
            with tempfile.TemporaryDirectory(prefix="r1-gate-audit-") as temp:
                cnf_path = Path(temp) / f"{stem}.cnf"
                proof_path = Path(temp) / f"{stem}.drat"
                cnf_path.write_bytes(cnf_payload)
                proof_path.write_bytes(proof_payload)
                checked = subprocess.run(
                    [str(args.drat_trim), str(cnf_path), str(proof_path)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if checked.returncode or "s VERIFIED" not in checked.stdout:
                    raise AssertionError(
                        (stem, "DRAT-trim failure", checked.stdout, checked.stderr)
                    )
        print(
            f"PASS {stem}: vars={header[0]} clauses={header[1]} "
            f"pairs={facts['disjoint_pairs']} hashes"
            + (" DRAT" if args.drat_trim else "")
        )

    print("PASS all six exact r=1 cross-family certificates")


if __name__ == "__main__":
    main()
