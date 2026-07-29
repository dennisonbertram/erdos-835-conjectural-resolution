#!/usr/bin/env python3
"""Exact arithmetic audit for evidence/transposition_flow_cocycle.md.

This verifies the stated universal arithmetic identities and the explicit
small-k=4 control.  It does not search for, reconstruct, or certify a
colouring of J(32,16).
"""

from itertools import combinations, permutations
from math import comb


def rank_mod_p(matrix, p):
    """Return the row rank of a small matrix over F_p."""
    a = [[entry % p for entry in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if a[row][col]), None
        )
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        inverse = pow(a[pivot_row][col], -1, p)
        a[pivot_row] = [(inverse * entry) % p for entry in a[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not a[row][col]:
                continue
            factor = a[row][col]
            a[row] = [
                (left - factor * right) % p
                for left, right in zip(a[row], a[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def verify_k16_arithmetic():
    p = 17
    columns = comb(30, 15)
    rows = comb(30, 14)
    dimension = columns - rows
    factors = tuple(15 - j for j in range(15))

    assert columns == 155_117_520
    assert rows == 145_422_675
    assert dimension == 9_694_845 == columns // 16
    assert factors == tuple(range(15, 0, -1))
    assert all(factor % p for factor in factors)
    assert sum(range(p)) % p == 0

    # Every possible omitted colour admits the row algebra: a derangement
    # of the other sixteen colours has nonzero differences summing to zero.
    for omitted in range(p):
        domain = tuple(t for t in range(p) if t != omitted)
        image = domain[1:] + domain[:1]
        assert set(image) == set(domain)
        assert all(t != u for t, u in zip(domain, image))
        differences = tuple((t - u) % p for t, u in zip(domain, image))
        assert all(differences)
        assert sum(differences) % p == 0

    # Pointwise Frobenius identities for every nonzero field element.
    assert all(pow(t, 16, p) == 1 for t in range(1, p))
    assert all(pow(t, 17, p) == t for t in range(p))

    # Audit the two set complements responsible for the minus sign.
    X = frozenset(range(32))
    x, y = 30, 31
    Z = X - {x, y}
    B = frozenset(range(15))
    B_complement_in_Z = Z - B
    assert X - (B_complement_in_Z | {x}) == B | {y}
    assert X - (B_complement_in_Z | {y}) == B | {x}

    # Audit the triangle sign/order as an exact telescoping identity.
    gx, gy, gz = 2, 9, 14
    assert ((gx - gy) + (gy - gz) + (gz - gx)) % p == 0

    return columns, rows, dimension


def verify_k4_control():
    p = 5
    points = frozenset(range(6))
    row_sets = tuple(combinations(range(6), 2))
    column_sets = tuple(combinations(range(6), 3))
    vector = (
        3, 4, 4, 4,
        4, 4, 4, 1, 1, 1,
        4, 4, 4, 1, 1, 1,
        1, 1, 1, 2,
    )
    assert len(row_sets) == 15
    assert len(column_sets) == 20 == len(vector)
    value = {
        frozenset(column): entry
        for column, entry in zip(column_sets, vector)
    }
    assert all(entry % p for entry in vector)

    incidence = []
    row_patterns = set()
    for row_tuple in row_sets:
        row = frozenset(row_tuple)
        extensions = tuple(
            row | {z}
            for z in sorted(points - row)
        )
        assert len(extensions) == 4
        entries = tuple(value[extension] for extension in extensions)
        assert sum(entries) % p == 0
        row_patterns.add(tuple(sorted(entries)))
        incidence.append([
            int(row.issubset(frozenset(column)))
            for column in column_sets
        ])

    expected_patterns = {
        (1, 1, 4, 4),
        (3, 4, 4, 4),
        (1, 1, 1, 2),
    }
    assert row_patterns == expected_patterns

    # W_{2,3}(6) has full row rank over F_5, and v is in its kernel.
    rank = rank_mod_p(incidence, p)
    assert rank == len(row_sets) == 15
    assert len(column_sets) - rank == 5
    for row in incidence:
        assert sum(coefficient * entry for coefficient, entry in zip(row, vector)) % p == 0

    # Anti-complementarity on all twenty coordinates.
    for triple, entry in value.items():
        assert value[points - triple] == (-entry) % p

    nonzero = tuple(range(1, p))
    derangement_patterns = set()
    for image in permutations(nonzero):
        if all(t != u for t, u in zip(nonzero, image)):
            differences = tuple(
                sorted((t - u) % p for t, u in zip(nonzero, image))
            )
            derangement_patterns.add(differences)
    assert row_patterns <= derangement_patterns

    explicit_images = {
        (1, 1, 4, 4): (2, 1, 4, 3),
        (3, 4, 4, 4): (2, 3, 4, 1),
        (1, 1, 1, 2): (4, 1, 2, 3),
    }
    for expected, image in explicit_images.items():
        assert set(image) == set(nonzero)
        assert all(t != u for t, u in zip(nonzero, image))
        actual = tuple(
            sorted((t - u) % p for t, u in zip(nonzero, image))
        )
        assert actual == expected

    return rank, row_patterns


def main():
    columns, rows, dimension = verify_k16_arithmetic()
    rank, patterns = verify_k4_control()
    print(
        "k=16 arithmetic: "
        f"length={columns}, row rank={rows}, top-kernel dim={dimension}"
    )
    print("F17 row/derangement/Frobenius/complement-sign identities: PASS")
    print(
        "k=4 control: full-support W_{2,3}(6) flow, "
        f"rank={rank}, anti-complement, 15 row sums, "
        f"{len(patterns)} rowwise derangement patterns: PASS"
    )
    print("TRANSPOSITION FLOW COCYCLE AUDIT: PASS")


if __name__ == "__main__":
    main()
