#!/usr/bin/env python3
"""Independent byte-level and semantic audit of the cyclic fan CNF.

The committed cyclic LS(2,3,19) and its C17 quotient are reconstructed here
without importing the generator.  The resulting clause stream is compared
byte for byte with a generated DIMACS file.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import Iterator


MODULUS = 17
FINITE = tuple(range(MODULUS))
LEFT = 17
INFINITY = 18
POINTS = tuple(range(19))
COLOURS = tuple(range(17))
LABELS = 13
STARTERS = (
    (0, 2, 5, 9, 14, 16, 13, 15, 12, 4, 8, 7, 11, 10, 6, 3, 1),
    (0, 3, 1, 10, 12, 11, 15, 4, 13, 5, 14, 9, 6, 8, 7, 16, 2),
)
PHASES = (
    7,
    1,
    9,
    0,
    5,
    12,
    15,
    8,
    13,
    11,
    4,
    16,
    10,
    14,
    15,
    14,
    2,
    10,
    6,
    9,
    11,
    4,
    8,
    3,
    12,
    6,
    5,
    4,
    11,
    2,
    14,
    0,
    7,
    8,
    6,
    1,
    10,
    5,
    12,
    6,
)

Triple = tuple[int, int, int]
Quad = tuple[int, int, int, int]
Cell = tuple[Quad, int]


def canon(values: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    return tuple(sorted(values))


def finite_shift(values: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return canon(tuple((value + amount) % MODULUS for value in values))


def finite_triple_representatives() -> tuple[Triple, ...]:
    unused = set(combinations(FINITE, 3))
    representatives = []
    while unused:
        orbit_seed = min(unused)
        representative = min(
            finite_shift(orbit_seed, amount) for amount in FINITE
        )
        representatives.append(representative)
        for amount in FINITE:
            unused.discard(finite_shift(representative, amount))
    if len(representatives) != 40:
        raise AssertionError("finite triples should have forty C17 orbits")
    return tuple(representatives)


def latin_entry(starter: tuple[int, ...], left: int, right: int) -> int:
    return (starter[(left - right) % MODULUS] + right) % MODULUS


def construct_link() -> dict[Triple, int]:
    link: dict[Triple, int] = {}

    def insert(raw: tuple[int, int, int], colour: int) -> None:
        triple = canon(raw)
        if triple in link:
            raise AssertionError("duplicate triple in cyclic link")
        link[triple] = colour

    for point in FINITE:
        insert((LEFT, INFINITY, point), point)
    for left, right in combinations(FINITE, 2):
        insert((LEFT, left, right), latin_entry(STARTERS[0], left, right))
        insert((INFINITY, left, right), latin_entry(STARTERS[1], left, right))
    for orbit_number, representative in enumerate(finite_triple_representatives()):
        phase_shift = -PHASES[orbit_number] % MODULUS
        for colour in COLOURS:
            insert(finite_shift(representative, phase_shift + colour), colour)
    return link


def validate_link(link: dict[Triple, int]) -> None:
    if len(link) != comb(19, 3):
        raise AssertionError("cyclic link does not colour all triples")
    for pair in combinations(POINTS, 2):
        star = [
            link[canon((*pair, point))]
            for point in POINTS
            if point not in pair
        ]
        if sorted(star) != list(COLOURS):
            raise AssertionError("cyclic link has a non-rainbow pair-star")


def shift_point(point: int, amount: int) -> int:
    return (point + amount) % MODULUS if point < MODULUS else point


def shift_block(block: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return canon(tuple(shift_point(point, amount) for point in block))


def build_quotient(
    link: dict[Triple, int],
) -> tuple[tuple[Cell, ...], tuple[tuple[int, ...], ...]]:
    def shift_cell(cell: Cell, amount: int) -> Cell:
        quad, colour = cell
        return shift_block(quad, amount), (colour + amount) % MODULUS

    all_cells: list[Cell] = []
    for quad in combinations(POINTS, 4):
        forbidden = {link[face] for face in combinations(quad, 3)}
        if len(forbidden) != 4:
            raise AssertionError("quadruple faces do not have four link colours")
        all_cells.extend(
            (quad, colour) for colour in COLOURS if colour not in forbidden
        )
    representative = {
        cell: min(shift_cell(cell, amount) for amount in FINITE)
        for cell in all_cells
    }
    orbit_cells = tuple(sorted(set(representative.values())))
    if len(orbit_cells) != 2_964:
        raise AssertionError("expected 2,964 quotient cells")
    cell_number = {cell: number for number, cell in enumerate(orbit_cells)}

    quad_representatives = tuple(
        sorted(
            {
                min(shift_block(quad, amount) for amount in FINITE)
                for quad in combinations(POINTS, 4)
            }
        )
    )
    if len(quad_representatives) != 228:
        raise AssertionError("expected 228 quadruple orbits")

    groups: list[tuple[int, ...]] = []
    for quad in quad_representatives:
        forbidden = {link[face] for face in combinations(quad, 3)}
        members = tuple(
            cell_number[representative[(quad, colour)]]
            for colour in COLOURS
            if colour not in forbidden
        )
        if len(members) != 13 or len(set(members)) != 13:
            raise AssertionError("quotient Q-group is not a 13-set")
        groups.append(members)

    def shift_triple_colour(
        item: tuple[Triple, int], amount: int
    ) -> tuple[Triple, int]:
        triple, colour = item
        return shift_block(triple, amount), (colour + amount) % MODULUS

    triple_colours = (
        (triple, colour)
        for triple in combinations(POINTS, 3)
        for colour in COLOURS
        if colour != link[triple]
    )
    tc_representatives = tuple(
        sorted(
            {
                min(shift_triple_colour(item, amount) for amount in FINITE)
                for item in triple_colours
            }
        )
    )
    if len(tc_representatives) != 912:
        raise AssertionError("expected 912 triple-colour orbits")
    for triple, colour in tc_representatives:
        members = []
        for point in POINTS:
            if point in triple:
                continue
            quad = canon((*triple, point))
            forbidden = {link[face] for face in combinations(quad, 3)}
            if colour not in forbidden:
                members.append(cell_number[representative[(quad, colour)]])
        if len(members) != 13 or len(set(members)) != 13:
            raise AssertionError("quotient triple-colour group is not a 13-set")
        groups.append(tuple(members))

    if len(groups) != 1_140 or len(set(groups)) != 1_140:
        raise AssertionError("expected 1,140 distinct quotient groups")
    degrees = [0] * len(orbit_cells)
    for group in groups:
        for cell in group:
            degrees[cell] += 1
    if set(degrees) != {5}:
        raise AssertionError("every quotient cell should occur in five groups")
    return orbit_cells, tuple(groups)


def primary(cell: int, label: int) -> int:
    return cell * LABELS + label + 1


def auxiliary(cell: int, position: int, cell_count: int) -> int:
    return cell_count * LABELS + cell * (LABELS - 1) + position + 1


def expected_clauses(
    cell_count: int,
    groups: tuple[tuple[int, ...], ...],
    redundant_group_amo: bool,
    pairwise_cell_amo: bool,
) -> Iterator[tuple[int, ...]]:
    for cell in range(cell_count):
        xs = tuple(primary(cell, label) for label in range(LABELS))
        yield xs
        if pairwise_cell_amo:
            for left, right in combinations(range(LABELS), 2):
                yield (-xs[left], -xs[right])
        else:
            sequential = tuple(
                auxiliary(cell, position, cell_count)
                for position in range(LABELS - 1)
            )
            yield (-xs[0], sequential[0])
            for position in range(1, LABELS - 1):
                yield (-xs[position], sequential[position])
                yield (-sequential[position - 1], sequential[position])
                yield (-xs[position], -sequential[position - 1])
            yield (-xs[-1], -sequential[-1])
    for group in groups:
        for label in range(LABELS):
            yield tuple(primary(cell, label) for cell in group)
    if redundant_group_amo:
        conflict_edges = {
            tuple(sorted(edge)) for group in groups for edge in combinations(group, 2)
        }
        for left, right in sorted(conflict_edges):
            for label in range(LABELS):
                yield (-primary(left, label), -primary(right, label))
    for label, cell in enumerate(groups[0]):
        yield (primary(cell, label),)


def sinz_extension_exists(primary_bits: int) -> bool:
    """DP over the twelve sequential variables for one cell."""
    x = tuple(bool(primary_bits & (1 << index)) for index in range(LABELS))
    previous_values = {value for value in (False, True) if not x[0] or value}
    for position in range(1, LABELS - 1):
        next_values = set()
        for previous in previous_values:
            for current in (False, True):
                if x[position] and not current:
                    continue
                if previous and not current:
                    continue
                if x[position] and previous:
                    continue
                next_values.add(current)
        previous_values = next_values
    return any(not (x[-1] and previous) for previous in previous_values)


def audit_sinz_truth_table() -> None:
    for primary_bits in range(1 << LABELS):
        expected = bin(primary_bits).count("1") <= 1
        if sinz_extension_exists(primary_bits) != expected:
            raise AssertionError(f"Sinz truth-table mismatch at mask {primary_bits}")


def audit_dimacs(
    path: Path,
    cell_count: int,
    groups: tuple[tuple[int, ...], ...],
    redundant_group_amo: bool,
    pairwise_cell_amo: bool,
) -> tuple[str, Counter[int], int]:
    variable_count = cell_count * (
        LABELS if pairwise_cell_amo else 2 * LABELS - 1
    )
    conflict_edges = {
        tuple(sorted(edge)) for group in groups for edge in combinations(group, 2)
    }
    extra_clauses = LABELS * len(conflict_edges) if redundant_group_amo else 0
    per_cell_clauses = (
        1 + LABELS * (LABELS - 1) // 2 if pairwise_cell_amo else 36
    )
    clause_count = (
        cell_count * per_cell_clauses
        + len(groups) * LABELS
        + LABELS
        + extra_clauses
    )
    expected_variables = 38_532 if pairwise_cell_amo else 74_100
    expected_count = (
        1_400_672
        if pairwise_cell_amo and redundant_group_amo
        else 248_989
        if pairwise_cell_amo
        else 1_273_220
        if redundant_group_amo
        else 121_537
    )
    if (variable_count, clause_count) != (expected_variables, expected_count):
        raise AssertionError("reconstructed CNF dimensions are unexpected")
    digest = hashlib.sha256()
    lengths: Counter[int] = Counter()
    with path.open("rb") as handle:
        header = handle.readline()
        digest.update(header)
        expected_header = f"p cnf {variable_count} {clause_count}\n".encode("ascii")
        if header != expected_header:
            raise AssertionError("DIMACS header differs from reconstruction")
        for clause_number, clause in enumerate(
            expected_clauses(
                cell_count,
                groups,
                redundant_group_amo,
                pairwise_cell_amo,
            ),
            start=1,
        ):
            line = handle.readline()
            digest.update(line)
            expected_line = (" ".join(map(str, clause)) + " 0\n").encode("ascii")
            if line != expected_line:
                raise AssertionError(
                    f"DIMACS differs at clause {clause_number}: "
                    f"expected {expected_line!r}, found {line!r}"
                )
            lengths[len(clause)] += 1
            if any(abs(literal) not in range(1, variable_count + 1) for literal in clause):
                raise AssertionError("literal outside declared variable range")
        trailing = handle.read()
        digest.update(trailing)
        if trailing:
            raise AssertionError("DIMACS contains trailing bytes after declared clauses")
    cell_binary_clauses = (
        cell_count * LABELS * (LABELS - 1) // 2
        if pairwise_cell_amo
        else 103_740
    )
    expected_lengths = Counter(
        {2: cell_binary_clauses + extra_clauses, 13: 17_784, 1: 13}
    )
    if lengths != expected_lengths:
        raise AssertionError(f"unexpected clause-length census: {lengths}")
    return digest.hexdigest(), lengths, len(conflict_edges)


def load_module(path: Path, name: str) -> ModuleType:
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise AssertionError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def assert_raises(callable_object: object, *args: object) -> None:
    try:
        callable_object(*args)  # type: ignore[operator]
    except AssertionError:
        return
    raise AssertionError("expected AssertionError was not raised")


def audit_decoder(decoder_path: Path) -> str:
    decoder = load_module(decoder_path, "_audited_cyclic_decoder")
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        exact = root / "exact.model"
        exact.write_text("s SATISFIABLE\nv 1 -2 3 0\n", encoding="ascii")
        if decoder.positive_literals(exact) != {1, 3}:
            raise AssertionError("decoder failed ordinary SAT-model parsing")
        unsat = root / "unsat.model"
        unsat.write_text("s UNSATISFIABLE\n", encoding="ascii")
        assert_raises(decoder.positive_literals, unsat)
        missing = root / "missing.model"
        missing.write_text("v 1 0\n", encoding="ascii")
        assert_raises(decoder.positive_literals, missing)
        malformed = root / "malformed.model"
        malformed.write_text("s NOTSATISFIABLE\nv 1 0\n", encoding="ascii")
        assert_raises(decoder.positive_literals, malformed)

    synthetic_cells = tuple(range(LABELS))
    synthetic_groups = (tuple(range(LABELS)),)
    decoder.construct_large_set = lambda: {}
    decoder.verify_large_set = lambda _link: None
    decoder.build_orbit_hypergraph = lambda _link: (
        synthetic_cells,
        synthetic_groups,
    )
    good = {decoder.primary(cell, cell) for cell in range(LABELS)}
    decoder.positive_literals = lambda _path: good
    labels = decoder.decode(Path("unused"))
    if labels != tuple(range(LABELS)):
        raise AssertionError("decoder failed a synthetic valid rainbow model")
    two_hot = set(good)
    two_hot.add(decoder.primary(0, 1))
    decoder.positive_literals = lambda _path: two_hot
    assert_raises(decoder.decode, Path("unused"))
    duplicate = {decoder.primary(cell, 0) for cell in range(LABELS)}
    decoder.positive_literals = lambda _path: duplicate
    assert_raises(decoder.decode, Path("unused"))

    return "HARDENED: exact 's SATISFIABLE' required"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument(
        "--redundant-group-amo",
        action="store_true",
        help="expect the generator's optional direct conflict-edge clauses",
    )
    parser.add_argument(
        "--pairwise-cell-amo",
        action="store_true",
        help="expect direct pairwise rather than sequential cell AMO clauses",
    )
    parser.add_argument(
        "--decoder",
        type=Path,
        default=Path(__file__).parents[1]
        / "h3_simultaneous_fan_attack_2"
        / "decode_cyclic_invariant_fan_model.py",
    )
    args = parser.parse_args()

    link = construct_link()
    validate_link(link)
    cells, groups = build_quotient(link)
    audit_sinz_truth_table()
    digest, lengths, conflict_edges = audit_dimacs(
        args.cnf,
        len(cells),
        groups,
        args.redundant_group_amo,
        args.pairwise_cell_amo,
    )
    decoder_status = audit_decoder(args.decoder)

    print("independent cyclic CNF audit: PASS")
    print(f"orbit_cells={len(cells)} quotient_groups={len(groups)} cell_degree=5")
    clauses = (
        1_400_672
        if args.pairwise_cell_amo and args.redundant_group_amo
        else 248_989
        if args.pairwise_cell_amo
        else 1_273_220
        if args.redundant_group_amo
        else 121_537
    )
    variables = 38_532 if args.pairwise_cell_amo else 74_100
    print(f"variables={variables} clauses={clauses}")
    print(
        "clause_lengths="
        + ",".join(f"{length}:{count}" for length, count in sorted(lengths.items()))
    )
    print("sinz_amo_truth_table=PASS (all 8192 primary assignments)")
    print("group_coverage_plus_one_hot=rainbow because every group has 13 cells")
    print("first_group_label_normalization=13 unit clauses; lossless label symmetry")
    print(
        f"redundant_group_amo={args.redundant_group_amo} "
        f"pairwise_cell_amo={args.pairwise_cell_amo} "
        f"distinct_conflict_edges={conflict_edges}"
    )
    print(f"sha256={digest}")
    print(f"decoder_semantic_one_hot_and_rainbow_tests=PASS; status_parser={decoder_status}")
    print("scope=encoding audit only; no SAT model and no k=16/#835 solution")


if __name__ == "__main__":
    main()
