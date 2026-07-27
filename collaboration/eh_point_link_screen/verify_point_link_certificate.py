#!/usr/bin/env python3
"""Independent semantic and optional DRAT verifier for one EH point-link.

This script deliberately does not import the CNF generator.  It reconstructs
the design, the derived leave, and every clause from the authenticated source,
then compares that serialization byte-for-byte with the committed CNF.
With ``--drat-trim``, it also streams the committed gzip proof into an
independent DRAT checker and requires ``s VERIFIED``.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_seed.txt"

SOURCE_SHA256 = "b1ea090d3e3b88366c87e95660c1c82a406d2c3b100cc1d39bcc2c7e8fde47f9"

POINTS = tuple(range(20))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
TRIPLES = tuple(itertools.combinations(POINTS, 3))
N_COLOURS = 5


@dataclass(frozen=True)
class Certificate:
    drop: tuple[int, int, int]
    point: int
    cnf: Path
    proof_gz: Path
    cnf_sha256: str
    proof_gz_sha256: str
    proof_raw_sha256: str
    proof_raw_bytes: int


CERTIFICATES = (
    Certificate(
        drop=(0, 1, 5),
        point=0,
        cnf=HERE / "drop_0_1_5_point_0.cnf",
        proof_gz=HERE / "drop_0_1_5_point_0.drat.gz",
        cnf_sha256="ac8e2176860e5f2d002a29e2592c4dc009d0262e7674fb35c47d11c9467f3e6f",
        proof_gz_sha256="648c029837933e1d4896b3342e6fc057c48540c2a7259e1a0c53e897745d9f51",
        proof_raw_sha256="06112a768e0892980bd02ffd21e2abca56324ee35c1c3d76be0ef828a12f63b9",
        proof_raw_bytes=2_380_258,
    ),
    Certificate(
        drop=(0, 5, 10),
        point=0,
        cnf=HERE / "drop_0_5_10_point_0.cnf",
        proof_gz=HERE / "drop_0_5_10_point_0.drat.gz",
        cnf_sha256="b0e0ebe97c289a9c44ff6ac48efbfecbf238d1b7f0dbfae2e934a9d6f1444654",
        proof_gz_sha256="195887f5ecebc335ecd80fae826d176b10c97f3122a38be1b896469666ad6f6b",
        proof_raw_sha256="9831caf77ec2588cbcbb695837d82201a037f06e5d9fbd90883c8595a60528a7",
        proof_raw_bytes=5_902_433,
    ),
)


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print(f"[ok] {label}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_and_audit_source() -> tuple[frozenset[tuple[int, ...]], ...]:
    raw = SOURCE.read_bytes()
    check(
        "authenticated EH source SHA-256",
        hashlib.sha256(raw).hexdigest() == SOURCE_SHA256,
    )
    lines = raw.decode("ascii").splitlines()
    check("source has C(20,4)=4,845 ordered rows", len(lines) == 4_845)

    owner: dict[tuple[int, ...], int] = {}
    for expected, line in zip(BLOCKS, lines):
        fields = tuple(map(int, line.split()))
        if len(fields) != 5 or fields[:4] != expected:
            raise AssertionError(f"malformed source row at {expected}")
        owner[expected] = fields[4]
    check(
        "source label census is seventeen classes of 285",
        Counter(owner.values()) == Counter({label: 285 for label in range(17)}),
    )

    systems = tuple(
        frozenset(block for block, label in owner.items() if label == number)
        for number in range(15)
    )
    check("fifteen EH classes each have 285 blocks", set(map(len, systems)) == {285})
    check(
        "fifteen EH classes are pairwise disjoint",
        len(set().union(*systems)) == 15 * 285,
    )
    for number, system in enumerate(systems):
        pair_counts = Counter(
            triple for block in system for triple in itertools.combinations(block, 3)
        )
        if set(pair_counts) != set(TRIPLES) or set(pair_counts.values()) != {1}:
            raise AssertionError(f"EH class {number} is not an SQS(20)")
    check("all fifteen EH classes are independently verified SQS(20)s", True)
    return systems


def derived_leave(
    systems: tuple[frozenset[tuple[int, ...]], ...],
    drop: tuple[int, int, int],
    point: int,
) -> tuple[
    tuple[tuple[int, int, int], ...],
    dict[tuple[int, int], tuple[int, ...]],
]:
    retained = set().union(
        *(system for number, system in enumerate(systems) if number not in drop)
    )
    derived = tuple(
        tuple(x for x in block if x != point)
        for block in BLOCKS
        if point in block and block not in retained
    )
    check(
        "derived leave has 285 distinct triples",
        len(derived) == len(set(derived)) == 285,
    )

    pair_rows: dict[tuple[int, int], list[int]] = defaultdict(list)
    for row, triple in enumerate(derived):
        for pair in itertools.combinations(triple, 2):
            pair_rows[pair].append(row)
    stars = {pair: tuple(rows) for pair, rows in pair_rows.items()}
    expected_pairs = set(
        itertools.combinations((value for value in POINTS if value != point), 2)
    )
    check("derived leave contains every pair", set(stars) == expected_pairs)
    check(
        "every pair has exactly five derived triples",
        set(map(len, stars.values())) == {5},
    )

    adjacency = [set() for _ in derived]
    for rows in stars.values():
        for left, right in itertools.combinations(rows, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
    check(
        "derived leave graph is simple and 12-regular", set(map(len, adjacency)) == {12}
    )
    return derived, stars


def var(row: int, colour: int) -> int:
    return 5 * row + colour + 1


def semantic_cnf(
    derived: tuple[tuple[int, int, int], ...],
    stars: dict[tuple[int, int], tuple[int, ...]],
) -> bytes:
    clauses: list[tuple[int, ...]] = []

    # Exactly one colour on each triple.
    for row in range(285):
        clauses.append(tuple(var(row, colour) for colour in range(5)))
        clauses.extend(
            (-var(row, left), -var(row, right))
            for left, right in itertools.combinations(range(5), 2)
        )

    # Every five-triple pair-star is rainbow.
    for rows in stars.values():
        for colour in range(5):
            clauses.append(tuple(var(row, colour) for row in rows))
            clauses.extend(
                (-var(left, colour), -var(right, colour))
                for left, right in itertools.combinations(rows, 2)
            )

    # Safe global colour symmetry: the first K5 can always be relabelled.
    root_rows = stars[min(stars)]
    clauses.extend((var(row, colour),) for colour, row in enumerate(root_rows))

    check("semantic encoding has 1,425 variables", len(derived) * 5 == 1_425)
    check("semantic encoding has 12,545 clauses", len(clauses) == 12_545)
    text = [f"p cnf 1425 {len(clauses)}\n"]
    text.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(text).encode("ascii")


def audit_certificate_bytes(certificate: Certificate, expected_cnf: bytes) -> None:
    check(
        f"{certificate.drop} committed CNF SHA-256",
        sha256(certificate.cnf) == certificate.cnf_sha256,
    )
    check(
        f"{certificate.drop} CNF is the exact independent semantic serialization",
        certificate.cnf.read_bytes() == expected_cnf,
    )
    check(
        f"{certificate.drop} committed gzip proof SHA-256",
        sha256(certificate.proof_gz) == certificate.proof_gz_sha256,
    )

    digest = hashlib.sha256()
    byte_count = 0
    with gzip.open(certificate.proof_gz, "rb") as proof:
        while chunk := proof.read(1 << 20):
            digest.update(chunk)
            byte_count += len(chunk)
    check(
        f"{certificate.drop} uncompressed DRAT byte count",
        byte_count == certificate.proof_raw_bytes,
    )
    check(
        f"{certificate.drop} uncompressed DRAT SHA-256",
        digest.hexdigest() == certificate.proof_raw_sha256,
    )


def replay_drat(certificate: Certificate, checker: Path) -> None:
    """Stream the binary proof to drat-trim without a large temporary file."""

    process = subprocess.Popen(
        [str(checker), str(certificate.cnf), "-i"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert process.stdin is not None
    with gzip.open(certificate.proof_gz, "rb") as proof:
        while chunk := proof.read(1 << 20):
            process.stdin.write(chunk)
    process.stdin.close()
    assert process.stdout is not None
    transcript = process.stdout.read().decode("utf-8", errors="replace")
    return_code = process.wait()
    print(transcript, end="")
    check(
        f"{certificate.drop} independent drat-trim replay returns s VERIFIED",
        return_code == 0 and "s VERIFIED" in transcript,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()

    systems = read_and_audit_source()
    for certificate in CERTIFICATES:
        derived, stars = derived_leave(systems, certificate.drop, certificate.point)
        expected_cnf = semantic_cnf(derived, stars)
        audit_certificate_bytes(certificate, expected_cnf)
        if args.drat_trim is not None:
            replay_drat(certificate, args.drat_trim)
            print(
                f"[theorem] drop {certificate.drop} cannot be retained: its "
                f"point-{certificate.point} derived leave has no partition "
                "into five STS(19)s."
            )
        else:
            print(
                f"[scope] {certificate.drop} semantic checks passed; "
                "DRAT replay was not requested, so no UNSAT theorem is claimed"
            )

    print(
        "[scope] These are the two legacy point-link certificates used by the "
        "separate all-455 aggregate coverage gate."
    )
    print("[scope] This does not decide LS(3,4,20) or Erdős--Rosenfeld #835.")
    if args.drat_trim is not None:
        print("status: PASS")
    else:
        print("status: PASS (semantic package audit only)")


if __name__ == "__main__":
    main()
