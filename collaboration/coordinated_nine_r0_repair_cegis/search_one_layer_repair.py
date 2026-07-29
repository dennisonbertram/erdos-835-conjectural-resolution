#!/usr/bin/env python3
"""Exact CEGIS search for a one-layer repair of an r=0 six-prefix.

This is a search program, not a proof certificate.  In particular, an UNSAT
answer from the incremental solver is reported as ``unsat_uncertified``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Iterable

from pysat.solvers import Cadical195


VERTICES = tuple(range(13))
VERTEX_SET = frozenset(VERTICES)
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
PREFIX_SIZES = (4, 4, 4, 5, 5, 5)
REMAINING_SIZES = (3,) * 7 + (5,) * 4
DEFAULT_TIME_LIMIT_SECONDS = 600.0
WITNESS_STRATEGIES = ("dense", "diverse")
ROUTE_TYPES = ("10+10+10", "10+10+8", "10+8+8", "8+8+8")


class DeadlineExceeded(RuntimeError):
    """Internal signal used to enforce the wall-clock search limit."""


def edge_mask(edge_indices: Iterable[int]) -> int:
    result = 0
    for edge_index in edge_indices:
        result |= 1 << edge_index
    return result


def endpoints(matching: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(vertex for edge_index in matching for vertex in EDGES[edge_index])
    )


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Enumerate all labelled perfect matchings on an even vertex tuple."""
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        edge_index = EDGE_INDEX[tuple(sorted((first, second)))]
        for tail in perfect_matchings(rest):
            result.append(tuple(sorted((edge_index, *tail))))
    return tuple(result)


@lru_cache(maxsize=None)
def matching_family(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, ...], int], ...]:
    return tuple(
        (matching, edge_mask(matching)) for matching in perfect_matchings(vertices)
    )


class Cnf:
    """Small deterministic CNF builder with exact unary cardinality."""

    def __init__(self) -> None:
        self.top = 0
        self.variables: dict[tuple, int] = {}
        self.clauses: list[tuple[int, ...]] = []
        self.true = self.variable(("constant", True))
        self.false = self.variable(("constant", False))
        self.add(self.true)
        self.add(-self.false)

    def variable(self, key: tuple) -> int:
        if key not in self.variables:
            self.top += 1
            self.variables[key] = self.top
        return self.variables[key]

    def add(self, *literals: int) -> None:
        self.clauses.append(tuple(literals))

    def cardinality(
        self,
        tag: tuple,
        literals: list[int],
        *,
        lower: int | None = None,
        upper: int | None = None,
    ) -> None:
        count_literals = len(literals)
        if lower is not None and not 0 <= lower <= count_literals:
            raise ValueError("invalid lower bound")
        if upper is not None and not 0 <= upper <= count_literals:
            raise ValueError("invalid upper bound")
        if lower is not None and upper is not None and lower > upper:
            raise ValueError("inconsistent bounds")

        largest = 0
        if lower:
            largest = max(largest, lower)
        if upper is not None and upper < count_literals:
            largest = max(largest, upper + 1)
        if not largest:
            return

        def state(prefix: int, count: int) -> int:
            if count == 0:
                return self.true
            if prefix == 0 or count > prefix:
                return self.false
            return self.variable(("counter", tag, prefix, count))

        for prefix, literal in enumerate(literals, start=1):
            for count in range(1, min(prefix, largest) + 1):
                current = state(prefix, count)
                old_same = state(prefix - 1, count)
                old_previous = state(prefix - 1, count - 1)
                self.add(-old_same, current)
                self.add(-old_previous, -literal, current)
                self.add(-current, old_same, old_previous)
                self.add(-current, old_same, literal)

        if lower:
            self.add(state(count_literals, lower))
        if upper is not None and upper < count_literals:
            self.add(-state(count_literals, upper + 1))


def lexicographic_leq(
    cnf: Cnf,
    tag: tuple,
    left: list[int],
    right: list[int],
) -> None:
    """Encode the bit vector ``left`` as lexicographically <= ``right``."""
    if len(left) != len(right):
        raise ValueError("lexicographic vectors have different lengths")
    prefix_equal = cnf.true
    for position, (left_bit, right_bit) in enumerate(zip(left, right)):
        cnf.add(-prefix_equal, -left_bit, right_bit)
        next_equal = cnf.variable(("lex_equal", tag, position))
        cnf.add(-next_equal, prefix_equal)
        cnf.add(-next_equal, -left_bit, right_bit)
        cnf.add(-next_equal, left_bit, -right_bit)
        cnf.add(-prefix_equal, -left_bit, -right_bit, next_equal)
        cnf.add(-prefix_equal, left_bit, right_bit, next_equal)
        prefix_equal = next_equal


def colour_edge(cnf: Cnf, colour: int, edge_index: int) -> int:
    return cnf.variable(("colour_edge", colour, edge_index))


def deleted_edge(cnf: Cnf, edge_index: int) -> int:
    return cnf.variable(("deleted_edge", edge_index))


def support_vertex(cnf: Cnf, colour: int, vertex: int) -> int:
    return cnf.variable(("support_vertex", colour, vertex))


def remaining_row(cnf: Cnf, row: int, vertex: int) -> int:
    return cnf.variable(("remaining_row", row, vertex))


def other_occupied(cnf: Cnf, colour: int, edge_index: int) -> int:
    return cnf.variable(("other_occupied", colour, edge_index))


def build_instance() -> Cnf:
    """Build the exact r=0 complement-cover prefix and remaining-row CNF."""
    cnf = Cnf()

    for colour, size in enumerate(PREFIX_SIZES):
        cnf.cardinality(
            ("colour_size", colour),
            [
                colour_edge(cnf, colour, edge_index)
                for edge_index in range(len(EDGES))
            ],
            lower=size,
            upper=size,
        )
        for vertex in VERTICES:
            incident = [
                colour_edge(cnf, colour, edge_index)
                for edge_index, edge in enumerate(EDGES)
                if vertex in edge
            ]
            cnf.cardinality(
                ("colour_vertex", colour, vertex),
                incident,
                upper=1,
            )
            support = support_vertex(cnf, colour, vertex)
            for literal in incident:
                cnf.add(-literal, support)
            cnf.add(-support, *incident)

    for left, right in ((0, 1), (1, 2), (3, 4), (4, 5)):
        lexicographic_leq(
            cnf,
            ("prefix", left, right),
            [
                colour_edge(cnf, left, edge_index)
                for edge_index in range(len(EDGES))
            ],
            [
                colour_edge(cnf, right, edge_index)
                for edge_index in range(len(EDGES))
            ],
        )

    for edge_index, edge in enumerate(EDGES):
        colours = [
            colour_edge(cnf, colour, edge_index) for colour in range(6)
        ]
        cnf.cardinality(("edge_colour", edge), colours, upper=1)
        deleted = deleted_edge(cnf, edge_index)
        for literal in colours:
            cnf.add(-literal, deleted)
        cnf.add(-deleted, *colours)

        for colour in range(6):
            others = [
                colour_edge(cnf, other, edge_index)
                for other in range(6)
                if other != colour
            ]
            occupied = other_occupied(cnf, colour, edge_index)
            for literal in others:
                cnf.add(-literal, occupied)
            cnf.add(-occupied, *others)

    for row, size in enumerate(REMAINING_SIZES):
        cnf.cardinality(
            ("remaining_row_size", row),
            [remaining_row(cnf, row, vertex) for vertex in VERTICES],
            lower=size,
            upper=size,
        )

    for vertex in VERTICES:
        literal = remaining_row(cnf, 0, vertex)
        cnf.add(literal if vertex in (0, 1, 2) else -literal)

    for left, right in tuple(zip(range(1, 6), range(2, 7))) + tuple(
        zip(range(7, 10), range(8, 11))
    ):
        lexicographic_leq(
            cnf,
            ("remaining", left, right),
            [remaining_row(cnf, left, vertex) for vertex in VERTICES],
            [remaining_row(cnf, right, vertex) for vertex in VERTICES],
        )

    for vertex in VERTICES:
        incident_deletions = [
            deleted_edge(cnf, edge_index)
            for edge_index, edge in enumerate(EDGES)
            if vertex in edge
        ]
        cnf.cardinality(
            ("deleted_degree", vertex),
            incident_deletions,
            lower=1,
            upper=5,
        )
        absent_from_rows = [
            -remaining_row(cnf, row, vertex) for row in range(11)
        ]
        cnf.cardinality(
            ("class_b_column", vertex),
            incident_deletions + absent_from_rows,
            lower=12,
            upper=12,
        )

    return cnf


@dataclass(frozen=True)
class Witness:
    """Semantic data determining one witness-negation clause."""

    repair_layer: int
    replacement: tuple[int, ...]
    colours: tuple[int, int, int]
    complements: tuple[tuple[int, ...], ...]
    extensions: tuple[tuple[int, ...], ...]

    def record(self) -> dict[str, object]:
        return {
            "repair_layer": self.repair_layer,
            "replacement": list(self.replacement),
            "colours": list(self.colours),
            "complements": [list(row) for row in self.complements],
            "extensions": [list(matching) for matching in self.extensions],
        }


def is_matching_on(matching: tuple[int, ...], vertices: frozenset[int]) -> bool:
    matching_endpoints = [
        vertex for edge_index in matching for vertex in EDGES[edge_index]
    ]
    return (
        len(matching_endpoints) == len(vertices)
        and len(matching_endpoints) == len(set(matching_endpoints))
        and frozenset(matching_endpoints) == vertices
    )


def validate_witness_static(witness: Witness) -> None:
    layer = witness.repair_layer
    if not 0 <= layer < 6:
        raise AssertionError("invalid repair layer")
    if not (
        len(witness.colours)
        == len(witness.complements)
        == len(witness.extensions)
        == 3
    ):
        raise AssertionError("witness must contain exactly three extensions")
    all_matchings = (witness.replacement, *witness.extensions)
    if any(
        tuple(sorted(matching)) != matching
        or len(set(matching)) != len(matching)
        or any(not 0 <= edge_index < len(EDGES) for edge_index in matching)
        for matching in all_matchings
    ):
        raise AssertionError("matching edge indices are not canonical")
    support = frozenset(endpoints(witness.replacement))
    if len(witness.replacement) != PREFIX_SIZES[layer]:
        raise AssertionError("replacement has the wrong size")
    if not is_matching_on(witness.replacement, support):
        raise AssertionError("replacement is not a perfect matching")
    if tuple(sorted(witness.colours)) != witness.colours:
        raise AssertionError("remaining colours are not canonical")
    if len(set(witness.colours)) != 3 or any(
        not 0 <= colour < 11 for colour in witness.colours
    ):
        raise AssertionError("remaining colours are not distinct")

    matching_masks = [edge_mask(witness.replacement)]
    for colour, complement, matching in zip(
        witness.colours,
        witness.complements,
        witness.extensions,
    ):
        if (
            tuple(sorted(complement)) != complement
            or len(set(complement)) != len(complement)
            or any(vertex not in VERTEX_SET for vertex in complement)
        ):
            raise AssertionError("complement is not canonical")
        if len(complement) != REMAINING_SIZES[colour]:
            raise AssertionError("complement has the wrong size")
        target_support = VERTEX_SET - frozenset(complement)
        if not is_matching_on(matching, target_support):
            raise AssertionError("extension is not a perfect matching")
        matching_masks.append(edge_mask(matching))
    if any(
        left & right
        for left, right in combinations(matching_masks, 2)
    ):
        raise AssertionError("witness matchings are not edge-disjoint")


def witness_clause(cnf: Cnf, witness: Witness) -> tuple[int, ...]:
    """Reconstruct the exact clause negating a semantic witness."""
    validate_witness_static(witness)
    support = frozenset(endpoints(witness.replacement))
    literals: list[int] = []
    for vertex in VERTICES:
        literal = support_vertex(cnf, witness.repair_layer, vertex)
        literals.append(-literal if vertex in support else literal)

    used_edges = set(witness.replacement)
    for matching in witness.extensions:
        used_edges.update(matching)
    literals.extend(
        other_occupied(cnf, witness.repair_layer, edge_index)
        for edge_index in sorted(used_edges)
    )

    for colour, complement in zip(witness.colours, witness.complements):
        complement_set = frozenset(complement)
        for vertex in VERTICES:
            literal = remaining_row(cnf, colour, vertex)
            literals.append(-literal if vertex in complement_set else literal)

    return tuple(dict.fromkeys(literals))


def available_families(
    rows: tuple[tuple[int, ...], ...],
    deleted_mask: int,
) -> tuple[tuple[tuple[tuple[int, ...], int], ...], ...]:
    result = []
    for row in rows:
        support = tuple(sorted(VERTEX_SET - frozenset(row)))
        result.append(
            tuple(
                (matching, mask)
                for matching, mask in matching_family(support)
                if not mask & deleted_mask
            )
        )
    return tuple(result)


def extension_choices(
    families: tuple[tuple[tuple[tuple[int, ...], int], ...], ...],
    colours: tuple[int, int, int],
    *,
    limit: int,
    deadline: float,
) -> Iterable[tuple[tuple[int, ...], ...]]:
    """Yield up to ``limit`` disjoint matching triples for fixed colours."""
    ordered_colours = tuple(sorted(colours, key=lambda colour: len(families[colour])))
    selected: dict[int, tuple[int, ...]] = {}
    found = 0

    def visit(position: int, used_mask: int) -> Iterable[tuple[tuple[int, ...], ...]]:
        nonlocal found
        if time.monotonic() >= deadline:
            raise DeadlineExceeded
        if found >= limit:
            return
        if position == len(ordered_colours):
            found += 1
            yield tuple(selected[colour] for colour in colours)
            return
        colour = ordered_colours[position]
        for matching, mask in families[colour]:
            if mask & used_mask:
                continue
            selected[colour] = matching
            yield from visit(position + 1, used_mask | mask)
            del selected[colour]
            if found >= limit:
                return

    yield from visit(0, 0)


def find_witnesses(
    prefix: tuple[tuple[int, ...], ...],
    rows: tuple[tuple[int, ...], ...],
    *,
    limit: int,
    deadline: float,
    strategy: str,
) -> tuple[tuple[Witness, ...], bool]:
    """Find witnesses according to ``strategy``; return a timed-out flag."""
    if strategy not in WITNESS_STRATEGIES:
        raise ValueError("unknown witness strategy")
    if strategy == "dense":
        return find_witnesses_pass(
            prefix,
            rows,
            limit=limit,
            deadline=deadline,
            unique_signatures=False,
            excluded=frozenset(),
        )

    diverse, timed_out = find_witnesses_pass(
        prefix,
        rows,
        limit=limit,
        deadline=deadline,
        unique_signatures=True,
        excluded=frozenset(),
    )
    if timed_out or not diverse or len(diverse) >= limit:
        return diverse, timed_out

    # The first pass reached the end, so every signature which has any
    # witness is now represented once.  Only now may a signature repeat.
    repeated, timed_out = find_witnesses_pass(
        prefix,
        rows,
        limit=limit - len(diverse),
        deadline=deadline,
        unique_signatures=False,
        excluded=frozenset(diverse),
    )
    return diverse + repeated, timed_out


def find_witnesses_pass(
    prefix: tuple[tuple[int, ...], ...],
    rows: tuple[tuple[int, ...], ...],
    *,
    limit: int,
    deadline: float,
    unique_signatures: bool,
    excluded: frozenset[Witness],
) -> tuple[tuple[Witness, ...], bool]:
    """Run one exhaustive witness pass with an optional signature cap."""
    prefix_masks = tuple(edge_mask(layer) for layer in prefix)
    witnesses: list[Witness] = []
    represented_signatures: set[tuple[int, int, int, int]] = set()
    for repair_layer in range(6):
        if time.monotonic() >= deadline:
            return tuple(witnesses), True
        other_mask = 0
        for colour, mask in enumerate(prefix_masks):
            if colour != repair_layer:
                other_mask |= mask
        support = endpoints(prefix[repair_layer])
        for replacement, replacement_mask in matching_family(support):
            if replacement_mask & other_mask:
                continue
            if time.monotonic() >= deadline:
                return tuple(witnesses), True
            families = available_families(rows, other_mask | replacement_mask)
            for colours in combinations(range(11), 3):
                signature = (repair_layer, *colours)
                if unique_signatures and signature in represented_signatures:
                    continue
                if any(not families[colour] for colour in colours):
                    continue
                remaining = 1 if unique_signatures else limit - len(witnesses)
                try:
                    for extensions in extension_choices(
                        families,
                        colours,
                        limit=remaining,
                        deadline=deadline,
                    ):
                        witness = Witness(
                            repair_layer=repair_layer,
                            replacement=replacement,
                            colours=colours,
                            complements=tuple(rows[colour] for colour in colours),
                            extensions=extensions,
                        )
                        validate_witness_static(witness)
                        if witness in excluded:
                            continue
                        witnesses.append(witness)
                        represented_signatures.add(signature)
                        if len(witnesses) >= limit:
                            return tuple(witnesses), False
                        if unique_signatures:
                            break
                except DeadlineExceeded:
                    return tuple(witnesses), True
            if time.monotonic() >= deadline:
                return tuple(witnesses), True
    return tuple(witnesses), False


def validate_raw_instance(
    prefix: tuple[tuple[int, ...], ...],
    rows: tuple[tuple[int, ...], ...],
) -> None:
    """Check a decoded model without referring to SAT variables."""
    if tuple(map(len, prefix)) != PREFIX_SIZES:
        raise AssertionError("wrong prefix sizes")
    for layer in prefix:
        if not is_matching_on(layer, frozenset(endpoints(layer))):
            raise AssertionError("prefix layer is not a matching")
    prefix_masks = tuple(edge_mask(layer) for layer in prefix)
    if any(left & right for left, right in combinations(prefix_masks, 2)):
        raise AssertionError("prefix layers are not edge-disjoint")
    if tuple(map(len, rows)) != REMAINING_SIZES:
        raise AssertionError("wrong remaining row sizes")
    if rows[0] != (0, 1, 2):
        raise AssertionError("anchor triple is not fixed")

    deleted = frozenset(
        edge_index for layer in prefix for edge_index in layer
    )
    degrees = tuple(
        sum(edge_index in deleted for edge_index, edge in enumerate(EDGES) if vertex in edge)
        for vertex in VERTICES
    )
    if not all(1 <= degree <= 5 for degree in degrees):
        raise AssertionError("prefix is not complement-covering")
    rho = tuple(
        sum(vertex in row for row in rows) for vertex in VERTICES
    )
    if rho != tuple(degree - 1 for degree in degrees):
        raise AssertionError("class-B column equations fail")


def independent_has_witness(
    prefix: tuple[tuple[int, ...], ...],
    rows: tuple[tuple[int, ...], ...],
    *,
    deadline: float,
) -> tuple[bool, bool]:
    """Second raw exhaustive replay, independent of witness-cut construction."""
    prefix_masks = tuple(edge_mask(layer) for layer in prefix)
    for repair_layer in range(6):
        other_mask = 0
        for colour, mask in enumerate(prefix_masks):
            if colour != repair_layer:
                other_mask |= mask
        support = endpoints(prefix[repair_layer])
        for _, replacement_mask in matching_family(support):
            if replacement_mask & other_mask:
                continue
            families = available_families(rows, other_mask | replacement_mask)
            for colours in combinations(range(11), 3):
                left, middle, right = (families[colour] for colour in colours)
                for _, left_mask in left:
                    for _, middle_mask in middle:
                        if time.monotonic() >= deadline:
                            return False, True
                        if left_mask & middle_mask:
                            continue
                        union = left_mask | middle_mask
                        if any(not union & right_mask for _, right_mask in right):
                            return True, False
                if time.monotonic() >= deadline:
                    return False, True
    return False, False


def decode_model(
    cnf: Cnf,
    model: set[int],
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    prefix = tuple(
        tuple(
            edge_index
            for edge_index in range(len(EDGES))
            if colour_edge(cnf, colour, edge_index) in model
        )
        for colour in range(6)
    )
    rows = tuple(
        tuple(
            vertex
            for vertex in VERTICES
            if remaining_row(cnf, row, vertex) in model
        )
        for row in range(11)
    )
    return prefix, rows


def display_edges(matching: tuple[int, ...]) -> list[list[int]]:
    return [list(EDGES[edge_index]) for edge_index in matching]


def canonical_record(witness: Witness, clause: tuple[int, ...]) -> str:
    record = witness.record()
    record["clause_sha256"] = hashlib.sha256(
        " ".join(map(str, clause)).encode("ascii")
    ).hexdigest()
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """JSON object hook which rejects duplicate keys at every nesting level."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def integer_list(value: object, *, field: str) -> tuple[int, ...]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError(f"{field} must be a JSON list of integers")
    return tuple(value)


def nested_integer_lists(
    value: object,
    *,
    field: str,
) -> tuple[tuple[int, ...], ...]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a JSON list")
    return tuple(
        integer_list(item, field=f"{field}[{index}]")
        for index, item in enumerate(value)
    )


def decode_witness_record(value: object) -> tuple[Witness, str]:
    """Decode one strict canonical witness-log object."""
    if not isinstance(value, dict):
        raise ValueError("witness record must be a JSON object")
    expected_keys = {
        "repair_layer",
        "replacement",
        "colours",
        "complements",
        "extensions",
        "clause_sha256",
    }
    if set(value) != expected_keys:
        missing = sorted(expected_keys - set(value))
        extra = sorted(set(value) - expected_keys)
        raise ValueError(
            f"witness record keys mismatch: missing={missing}, extra={extra}"
        )
    repair_layer = value["repair_layer"]
    if type(repair_layer) is not int:
        raise ValueError("repair_layer must be an integer")
    clause_sha256 = value["clause_sha256"]
    if (
        not isinstance(clause_sha256, str)
        or len(clause_sha256) != 64
        or any(character not in "0123456789abcdef" for character in clause_sha256)
    ):
        raise ValueError("clause_sha256 must be 64 lowercase hexadecimal digits")
    witness = Witness(
        repair_layer=repair_layer,
        replacement=integer_list(value["replacement"], field="replacement"),
        colours=integer_list(value["colours"], field="colours"),
        complements=nested_integer_lists(
            value["complements"],
            field="complements",
        ),
        extensions=nested_integer_lists(value["extensions"], field="extensions"),
    )
    validate_witness_static(witness)
    return witness, clause_sha256


def replay_witnesses(
    cnf: Cnf,
    path: Path,
) -> Iterable[tuple[Witness, str]]:
    """Stream, validate, and reconstruct every canonical replay record."""
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            raw = line.rstrip("\r\n")
            if not raw:
                raise ValueError(f"{path}:{line_number}: blank JSONL record")
            try:
                value = json.loads(raw, object_pairs_hook=reject_duplicate_keys)
                witness, recorded_hash = decode_witness_record(value)
                clause = witness_clause(cnf, witness)
                expected = canonical_record(witness, clause)
            except (AssertionError, json.JSONDecodeError, ValueError) as error:
                raise ValueError(f"{path}:{line_number}: {error}") from error
            expected_hash = json.loads(expected)["clause_sha256"]
            if recorded_hash != expected_hash:
                raise ValueError(
                    f"{path}:{line_number}: clause_sha256 mismatch: "
                    f"recorded={recorded_hash}, reconstructed={expected_hash}"
                )
            if raw != expected:
                raise ValueError(f"{path}:{line_number}: record is not canonical JSON")
            cnf.add(*clause)
            yield witness, expected


def route_type(colours: tuple[int, int, int]) -> str:
    size_ten = sum(colour < 7 for colour in colours)
    return "+".join(("10",) * size_ten + ("8",) * (3 - size_ten))


def solve(
    *,
    max_rounds: int,
    cuts_per_model: int,
    time_limit_seconds: float,
    witness_log: Path | None,
    witness_strategy: str,
    replay_witness_log: Path | None,
) -> dict[str, object]:
    start = time.monotonic()
    deadline = start + time_limit_seconds
    cnf = build_instance()
    initial_clauses = len(cnf.clauses)
    witness_hasher = hashlib.sha256()
    replay_hasher = hashlib.sha256()
    cuts = 0
    replayed_cuts = 0
    new_cuts = 0
    rounds = 0
    cuts_by_repair_layer = {str(layer): 0 for layer in range(6)}
    cuts_by_route_type = {name: 0 for name in ROUTE_TYPES}
    repair_route_signatures: set[tuple[int, int, int, int]] = set()
    last_witness: dict[str, object] | None = None

    def account(witness: Witness) -> None:
        nonlocal cuts
        cuts += 1
        cuts_by_repair_layer[str(witness.repair_layer)] += 1
        cuts_by_route_type[route_type(witness.colours)] += 1
        repair_route_signatures.add((witness.repair_layer, *witness.colours))

    if replay_witness_log:
        for witness, record in replay_witnesses(cnf, replay_witness_log):
            encoded = record.encode("utf-8") + b"\n"
            replay_hasher.update(encoded)
            witness_hasher.update(encoded)
            account(witness)
            replayed_cuts += 1
            last_witness = witness.record()
    clauses_after_replay = len(cnf.clauses)
    solver = Cadical195(bootstrap_with=cnf.clauses)
    log_stream = witness_log.open("w", encoding="utf-8") if witness_log else None
    result: dict[str, object]
    try:
        while max_rounds == 0 or rounds < max_rounds:
            if time.monotonic() >= deadline:
                result = {"status": "time_limit"}
                break
            rounds += 1
            if not solver.solve():
                result = {
                    "status": "unsat_uncertified",
                    "proof_claimed": False,
                }
                break
            model = {literal for literal in solver.get_model() if literal > 0}
            prefix, rows = decode_model(cnf, model)
            validate_raw_instance(prefix, rows)
            witnesses, timed_out = find_witnesses(
                prefix,
                rows,
                limit=cuts_per_model,
                deadline=deadline,
                strategy=witness_strategy,
            )
            if timed_out:
                result = {"status": "time_limit"}
                break
            if not witnesses:
                has_witness, validation_timed_out = independent_has_witness(
                    prefix,
                    rows,
                    deadline=deadline,
                )
                if validation_timed_out:
                    result = {"status": "time_limit"}
                    break
                if has_witness:
                    raise AssertionError(
                        "independent replay found a missed repair witness"
                    )
                result = {
                    "status": "counterexample",
                    "counterexample_validated": True,
                    "prefix": [display_edges(layer) for layer in prefix],
                    "remaining_complements": [list(row) for row in rows],
                }
                break

            for witness in witnesses:
                clause = witness_clause(cnf, witness)
                solver.add_clause(clause)
                cnf.add(*clause)
                record = canonical_record(witness, clause)
                witness_hasher.update(record.encode("utf-8"))
                witness_hasher.update(b"\n")
                if log_stream:
                    log_stream.write(record + "\n")
                    log_stream.flush()
                account(witness)
                new_cuts += 1
                last_witness = witness.record()
        else:
            result = {"status": "round_limit"}
    finally:
        solver.delete()
        if log_stream:
            log_stream.close()

    result.update(
        {
            "rounds": rounds,
            "cuts": cuts,
            "replayed_cuts": replayed_cuts,
            "new_cuts": new_cuts,
            "variables": cnf.top,
            "initial_clauses": initial_clauses,
            "clauses_after_replay": clauses_after_replay,
            "final_clauses": len(cnf.clauses),
            "witness_sha256": witness_hasher.hexdigest(),
            "replay_sha256": replay_hasher.hexdigest(),
            "witness_strategy": witness_strategy,
            "cuts_by_repair_layer": cuts_by_repair_layer,
            "cuts_by_route_type": cuts_by_route_type,
            "unique_repair_route_signatures": len(repair_route_signatures),
            "repeated_repair_route_cuts": cuts - len(repair_route_signatures),
            "elapsed_seconds": round(time.monotonic() - start, 3),
        }
    )
    if last_witness is not None:
        result["last_witness"] = last_witness
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=0,
        help="zero means no round limit",
    )
    parser.add_argument(
        "--cuts-per-model",
        type=int,
        default=16,
    )
    parser.add_argument(
        "--time-limit-seconds",
        type=float,
        default=DEFAULT_TIME_LIMIT_SECONDS,
    )
    parser.add_argument(
        "--witness-strategy",
        choices=WITNESS_STRATEGIES,
        default="dense",
    )
    parser.add_argument("--witness-log", type=Path)
    parser.add_argument("--replay-witness-log", type=Path)
    args = parser.parse_args()
    if args.max_rounds < 0:
        parser.error("--max-rounds must be nonnegative")
    if args.cuts_per_model <= 0:
        parser.error("--cuts-per-model must be positive")
    if not 0 < args.time_limit_seconds <= DEFAULT_TIME_LIMIT_SECONDS:
        parser.error("--time-limit-seconds must be in (0, 600]")
    if (
        args.replay_witness_log
        and args.witness_log
        and args.replay_witness_log.resolve() == args.witness_log.resolve()
    ):
        parser.error(
            "--witness-log must differ from --replay-witness-log "
            "to protect the replay input"
        )
    result = solve(
        max_rounds=args.max_rounds,
        cuts_per_model=args.cuts_per_model,
        time_limit_seconds=args.time_limit_seconds,
        witness_log=args.witness_log,
        witness_strategy=args.witness_strategy,
        replay_witness_log=args.replay_witness_log,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
