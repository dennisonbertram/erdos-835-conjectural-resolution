#!/usr/bin/env python3
"""Audit the exact Tutte-barrier exceptional-profile CNF."""

from __future__ import annotations

import argparse
from pathlib import Path

import verify_r0_compact_full_cnf as compact_audit
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
    if args.cnf:
        compact_audit.scan_dimacs(args.cnf)
    if args.witness:
        compact_audit.audit_witness(args.witness)
    print(
        "SCOPE: exact catalogue-dependent full model; terminal SAT or "
        "replay-checked UNSAT is still required"
    )


if __name__ == "__main__":
    main()
