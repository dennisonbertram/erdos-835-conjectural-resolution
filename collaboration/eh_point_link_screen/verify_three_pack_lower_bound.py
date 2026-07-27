#!/usr/bin/env python3
"""Verify the canonical three-pack in every EH drop-three point-link.

For a discarded SQS(20), deriving at a point gives an STS(19).  Thus the
three discarded systems give three pairwise triple-disjoint STS(19)s inside
the five-fold derived leave.  This standard-library audit checks that claim
directly for all 455 discard triples at point 0.
"""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter

from point_link_cnf import build_instance, load_source


POINT = 0
OTHER_POINTS = tuple(range(1, 20))
PAIRS = set(itertools.combinations(OTHER_POINTS, 2))


def main() -> None:
    _, systems = load_source()
    digest = hashlib.sha256()
    cases = 0
    for drop in itertools.combinations(range(15), 3):
        leave, _ = build_instance(systems, drop, POINT)
        leave_rows = {triple: row for row, triple in enumerate(leave)}
        used: set[tuple[int, int, int]] = set()
        for system_number in drop:
            derived = tuple(
                tuple(value for value in block if value != POINT)
                for block in systems[system_number]
                if POINT in block
            )
            if not len(derived) == len(set(derived)) == 57:
                raise AssertionError("derived source system has wrong size")
            if not set(derived) <= set(leave):
                raise AssertionError("derived source system is outside leave")
            if used.intersection(derived):
                raise AssertionError("three-pack systems are not disjoint")
            used.update(derived)
            covered = Counter(
                pair for triple in derived for pair in itertools.combinations(triple, 2)
            )
            if set(covered) != PAIRS or set(covered.values()) != {1}:
                raise AssertionError("derived source system is not an STS(19)")
            rows = sorted(leave_rows[triple] for triple in derived)
            digest.update(bytes(drop))
            digest.update(system_number.to_bytes(1, "big"))
            for row in rows:
                digest.update(row.to_bytes(2, "big"))
        if len(used) != 3 * 57:
            raise AssertionError("canonical three-pack has wrong union size")
        cases += 1

    if cases != 455:
        raise AssertionError("did not audit all C(15,3)=455 drops")
    print("[ok] all 455 point-0 leaves contain the three discarded STS(19)s")
    print("[ok] every canonical three-pack has 171 distinct triples")
    print(f"[exact] canonical three-pack digest: {digest.hexdigest()}")
    print(
        "[lemma] in a five-fold leave, four disjoint STS(19)s force the "
        "unused fifth STS(19)"
    )
    print(
        "[scope] Therefore an UNSAT five-colouring certificate is also an "
        "upper bound of three on the STS packing number."
    )
    print("status: PASS")


if __name__ == "__main__":
    main()
