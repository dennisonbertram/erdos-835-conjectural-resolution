#!/usr/bin/env python3
"""Audit the exact Tutte-barrier exceptional-profile CNF."""

from __future__ import annotations

import argparse
import subprocess
from collections.abc import Iterator
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory

import verify_r0_compact_full_cnf as compact_audit
import verify_r0_core_pairs as core_pairs
import write_r0_tutte_full_cnf as tutte


def odd_partitions(
    total: int,
    count: int,
    lower: int = 1,
) -> tuple[tuple[int, ...], ...]:
    if count == 0:
        return ((),) if total == 0 else ()
    result = []
    for first in range(lower, total + 1, 2):
        for tail in odd_partitions(total - first, count - 1, first):
            result.append((first, *tail))
    return tuple(result)


def audit_catalogue() -> None:
    enumerated = set()
    for separator_size in range(5):
        degree_lower_bound = max(1, 10 - separator_size - 7)
        if degree_lower_bound % 2 == 0:
            degree_lower_bound += 1
        for blocks in odd_partitions(
            10 - separator_size,
            separator_size + 2,
            degree_lower_bound,
        ):
            enumerated.add((separator_size, blocks))

    encoded = {
        (separator_size, tuple(sorted(block_sizes)))
        for _, separator_size, block_sizes in tutte.BARRIERS
    }
    assert encoded == enumerated
    assert len(encoded) == 7
    for separator_size, blocks in encoded:
        assert len(blocks) == separator_size + 2
        assert sum(blocks) + separator_size == 10
        assert all(size % 2 == 1 for size in blocks)
    print("PASS exhaustive seven-shape size-ten Tutte catalogue")


def canonical_block_partitions(
    block_sizes: tuple[int, ...],
    remaining: int,
    index: int = 0,
    previous: int = 0,
) -> Iterator[tuple[int, ...]]:
    """Yield each block partition in the CNF's lexicographic normal form."""
    if index == len(block_sizes):
        yield ()
        return

    size = block_sizes[index]
    minimum = previous if index and block_sizes[index - 1] == size else -1
    vertices = [vertex for vertex in core_pairs.VERTICES if remaining >> vertex & 1]
    for subset in combinations(vertices, size):
        block = sum(1 << vertex for vertex in subset)
        if block <= minimum:
            continue
        for tail in canonical_block_partitions(
            block_sizes,
            remaining ^ block,
            index + 1,
            block,
        ):
            yield (block, *tail)


def packed_descriptor(
    barrier_index: int,
    blocks: tuple[int, ...],
) -> int:
    """Pack the exact choice-plus-block descriptor used by the CNF."""
    descriptor = 1 << barrier_index
    offset = len(tutte.BARRIERS[3:])
    for current_index, (_, _, block_sizes) in enumerate(tutte.BARRIERS[3:]):
        if current_index == barrier_index:
            assert len(blocks) == len(block_sizes)
            for block_index, block in enumerate(blocks):
                descriptor |= block << (offset + core_pairs.N * block_index)
        offset += core_pairs.N * len(block_sizes)
    return descriptor


def forced_core_mask(blocks: tuple[int, ...]) -> int:
    support = 0
    inside_blocks = 0
    for block in blocks:
        support |= block
        inside_blocks |= core_pairs.CLIQUE[block]
    return core_pairs.CLIQUE[support] ^ inside_blocks


def audit_surviving_core_descriptors() -> None:
    """Check descriptor equality iff the forced surviving core is equal."""
    expected_counts = {
        "5111": 72072,
        "3311": 360360,
        "31111": 60060,
        "6": 1716,
    }
    all_vertices = (1 << core_pairs.N) - 1
    core_to_descriptor: dict[int, int] = {}
    observed_counts = {}

    for barrier_index, (name, _, block_sizes) in enumerate(tutte.BARRIERS[3:]):
        type_masks = set()
        for blocks in canonical_block_partitions(
            block_sizes,
            all_vertices,
        ):
            core = forced_core_mask(blocks)
            descriptor = packed_descriptor(barrier_index, blocks)
            assert core not in type_masks
            type_masks.add(core)

            previous = core_to_descriptor.get(core)
            assert previous is None or previous == descriptor
            core_to_descriptor[core] = descriptor

        independently_generated = set(core_pairs.embeddings(name))
        assert type_masks == independently_generated
        observed_counts[name] = len(type_masks)

    assert observed_counts == expected_counts
    assert len(core_to_descriptor) == sum(expected_counts.values())
    print(
        "PASS descriptor/core-mask bijection for all 494,208 surviving labelled cores"
    )


def audit_four_core_projection() -> None:
    cases = (
        ((0, 0, 0, 0, 0, 0, 0), False),
        ((0, 1, 0, 1, 0, 1, 0), False),
        ((0, 1, 2, 0, 1, 2, 0), False),
        ((0, 1, 2, 3, 0, 1, 2), True),
        ((0, 1, 2, 3, 0, 1, 3), True),
    )
    with TemporaryDirectory(prefix="r0-four-core-") as directory:
        for case_index, (values, expected_sat) in enumerate(cases):
            path = Path(directory) / f"case-{case_index}.cnf"
            writer = tutte.compact.Writer(path)
            descriptors = [writer.variables_block(2) for _ in range(7)]
            tutte.require_four_distinct_cores(writer, descriptors)
            for descriptor, value in zip(descriptors, values):
                for bit_index, variable in enumerate(descriptor):
                    writer.add([variable if value >> bit_index & 1 else -variable])
            writer.finish()
            result = subprocess.run(
                ["/opt/homebrew/bin/cadical", "-q", str(path)],
                check=False,
                capture_output=True,
            )
            observed_sat = result.returncode == 10
            assert result.returncode in (10, 20)
            assert observed_sat == expected_sat
    print("PASS four-distinct-core projection on 1/2/3/4-class controls")


def audit_b_needs_five_projection() -> None:
    cases = (
        ((0, 1, 2, 3, 0, 1, 2), False, True),
        ((0, 1, 2, 3, 0, 1, 2), True, False),
        ((0, 1, 2, 3, 4, 0, 1), True, True),
    )
    with TemporaryDirectory(prefix="r0-b-five-core-") as directory:
        for case_index, (values, has_b, expected_sat) in enumerate(cases):
            path = Path(directory) / f"case-{case_index}.cnf"
            writer = tutte.compact.Writer(path)
            descriptors = [writer.variables_block(3) for _ in range(7)]
            choices = [writer.variables_block(2) for _ in range(7)]
            different = tutte.require_four_distinct_cores(
                writer, descriptors
            )
            tutte.require_five_cores_if_barrier_b(
                writer, choices, different
            )
            for descriptor, value in zip(descriptors, values):
                for bit_index, variable in enumerate(descriptor):
                    writer.add(
                        [variable if value >> bit_index & 1 else -variable]
                    )
            for row_choices in choices:
                writer.add(
                    [row_choices[1] if has_b else -row_choices[1]]
                )
            writer.finish()
            result = subprocess.run(
                ["/opt/homebrew/bin/cadical", "-q", str(path)],
                check=False,
                capture_output=True,
            )
            observed_sat = result.returncode == 10
            assert result.returncode in (10, 20)
            assert observed_sat == expected_sat
    print("PASS K3311-implies-five-core projection controls")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--witness", type=Path)
    args = parser.parse_args()

    compact_audit.audit_cardinality_projection()
    compact_audit.audit_gated_cardinality_projection()
    compact_audit.audit_lex_projection()
    compact_audit.audit_matching_enumeration()
    audit_catalogue()
    audit_surviving_core_descriptors()
    audit_four_core_projection()
    audit_b_needs_five_projection()
    if args.cnf:
        compact_audit.scan_dimacs(args.cnf)
    if args.witness:
        compact_audit.audit_witness(args.witness)
    print(
        "SCOPE: exact catalogue-dependent full model and exhaustive "
        "surviving-core descriptor audit; the separate three-core-family "
        "replay and terminal SAT or replay-checked UNSAT are still required"
    )


if __name__ == "__main__":
    main()
