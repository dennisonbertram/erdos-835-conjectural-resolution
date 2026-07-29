#!/usr/bin/env python3
"""Exact arithmetic checks for the Schur-product literature audit.

This script does not assume that either LS(4,5,21) or LS(3,4,20) exists.
It checks consequences that would hold for the 15-dimensional space forced by
the deleted-colour Hadamard-kernel theorem, and it evaluates the numerical
hypotheses of the cited coding, frame, and inclusion-matrix results.

Only Python's standard library is used.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb


Q = 17
DIM = 15
STAR_SIZE = 16
SYMMETRIC_SQUARE_DIMENSION = DIM * (DIM + 1) // 2


def inv(x: int) -> int:
    x %= Q
    assert x
    return pow(x, Q - 2, Q)


def transpose(a: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) % Q for col in bt] for row in a]


def rank_mod(a: list[list[int]]) -> int:
    m = [row[:] for row in a]
    if not m:
        return 0
    rows = len(m)
    cols = len(m[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if m[r][col] % Q), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        scale = inv(m[rank][col])
        m[rank] = [(scale * x) % Q for x in m[rank]]
        for r in range(rows):
            if r == rank or not m[r][col]:
                continue
            scale = m[r][col]
            m[r] = [(x - scale * y) % Q for x, y in zip(m[r], m[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def dot(x: list[int], y: list[int]) -> int:
    return sum(a * b for a, b in zip(x, y)) % Q


def standard_simplex_checks() -> None:
    # In H_0 <= F_17^16, f_i = e_i + 1 has Gram I+J.
    simplex = []
    for i in range(STAR_SIZE):
        v = [1] * STAR_SIZE
        v[i] += 1
        simplex.append([x % Q for x in v])

    assert all(sum(v) % Q == 0 for v in simplex)
    assert all(dot(simplex[i], simplex[i]) == 2 for i in range(STAR_SIZE))
    assert all(
        dot(simplex[i], simplex[j]) == 1
        for i in range(STAR_SIZE)
        for j in range(STAR_SIZE)
        if i != j
    )
    assert all(
        sum(simplex[i][j] for i in range(STAR_SIZE)) % Q == 0 for j in range(STAR_SIZE)
    )

    p = [[(1 + (i == j)) % Q for j in range(STAR_SIZE)] for i in range(STAR_SIZE)]
    assert rank_mod(p) == DIM
    assert matmul(p, p) == p
    assert all(sum(row) % Q == 0 for row in p)

    # The Schur square of the [16,15] single-parity-check code H_0 is all F^16.
    h0_basis = []
    for i in range(DIM):
        v = [0] * STAR_SIZE
        v[i] = 1
        v[-1] = -1 % Q
        h0_basis.append(v)
    products = []
    for i in range(DIM):
        for j in range(i, DIM):
            products.append([(a * b) % Q for a, b in zip(h0_basis[i], h0_basis[j])])
    assert rank_mod(products) == STAR_SIZE

    print(
        "local simplex: Gram=I+J has rank 15; "
        "H_0 Schur-square rank=16 (the whole punctured space)"
    )


def permutation_cross_matrix(
    p: list[list[int]], permutation: list[int]
) -> list[list[int]]:
    # C = P * Pi, where column j of Pi is e_{permutation[j]}.
    return [[p[i][permutation[j]] for j in range(STAR_SIZE)] for i in range(STAR_SIZE)]


def adjacent_star_pair_checks() -> None:
    # A cross-Gram matrix C between two simplex frames must satisfy
    # C C^T = C^T C = P and have zero row/column sums.  Permuting the same
    # standard simplex supplies exact local gluings.
    p = [[(1 + (i == j)) % Q for j in range(STAR_SIZE)] for i in range(STAR_SIZE)]

    # If the union block is deleted, the two frames share no vector.  A
    # 16-cycle makes every corresponding outside-point cross entry equal to 1.
    no_shared_perm = [(i + 1) % STAR_SIZE for i in range(STAR_SIZE)]
    no_shared = permutation_cross_matrix(p, no_shared_perm)
    assert all(no_shared[i][i] == 1 for i in range(STAR_SIZE))

    # If the union block is not deleted, coordinate 0 is the shared vector.
    # Fix it and derange the remaining 15 positions.
    shared_perm = [0] + [i + 1 if i < STAR_SIZE - 1 else 1 for i in range(1, STAR_SIZE)]
    shared = permutation_cross_matrix(p, shared_perm)
    assert shared[0][0] == 2
    assert all(shared[0][j] == 1 for j in range(1, STAR_SIZE))
    assert all(shared[i][0] == 1 for i in range(1, STAR_SIZE))
    assert all(shared[i][i] == 1 for i in range(1, STAR_SIZE))

    for name, c in (("no-shared", no_shared), ("shared", shared)):
        assert all(sum(row) % Q == 0 for row in c)
        assert all(
            sum(c[i][j] for i in range(STAR_SIZE)) % Q == 0 for j in range(STAR_SIZE)
        )
        assert matmul(c, transpose(c)) == p
        assert matmul(transpose(c), c) == p
        print(f"adjacent-star local {name} permutation gluing: PASS")


def layer_checks(t: int, v: int, label: str) -> None:
    block_size = t + 1
    row_count = comb(v, t)
    total_blocks = comb(v, block_size)
    assert row_count % block_size == 0
    deleted_blocks = row_count // block_size
    remaining_blocks = total_blocks - deleted_blocks
    assert v - t == Q
    assert remaining_blocks == 16 * deleted_blocks

    # Wilson diagonal factors for the complete W_{t,t+1}(v).
    wilson_factors = [block_size - i for i in range(t + 1)]
    assert all(factor % Q for factor in wilson_factors)
    wilson_rank = sum(comb(v, i) - (comb(v, i - 1) if i else 0) for i in range(t + 1))
    assert wilson_rank == row_count

    # Q_D = {z : M_D z is constant}.  Since M_D 1 = 16*1 = -1,
    # the constant line lies in the image and
    # dim Q_D = N-rank(M_D)+1 >= N-R+1.
    qd_dimension_floor = remaining_blocks - row_count + 1
    assert qd_dimension_floor > SYMMETRIC_SQUARE_DIMENSION

    # Plaza-Xiang Theorem 4 only permits this many arbitrary deleted rows
    # from the transpose of the complete inclusion matrix.
    resilience_threshold = Fraction(v - 1, block_size)
    assert deleted_blocks > resilience_threshold

    # Sum the R local identity frame operators.  Each remaining block occurs
    # in block_size stars, so the global frame constant is R/block_size.
    frame_constant = row_count * inv(block_size) % Q
    assert frame_constant == deleted_blocks % Q
    assert (remaining_blocks * 2 - DIM * frame_constant) % Q == 0

    # The induced nondeleted Johnson graph is regular.  For each of the
    # block_size facets, the deleted extension removes one of the 16 other
    # neighbours in the full 17-extension star, leaving 15.
    degree = 15 * block_size
    nonneighbors = remaining_blocks - 1 - degree
    assert nonneighbors > 0

    # From sum(v_T)=0 and global tightness:
    #   sum_nonedge <v_S,v_T>   = -(2+degree)
    #   sum_nonedge <v_S,v_T>^2 = 2c-4-degree.
    nonedge_sum = (-2 - degree) % Q
    nonedge_square_sum = (2 * frame_constant - 4 - degree) % Q
    assert nonneighbors % Q
    forced_constant_square = (nonedge_square_sum * inv(nonneighbors)) % Q
    quadratic_residues = {(x * x) % Q for x in range(Q)}
    assert forced_constant_square not in quadratic_residues

    gerzon_bound = DIM * (DIM + 1) // 2
    assert remaining_blocks > gerzon_bound

    product_singleton_upper = remaining_blocks - 2 * DIM + 2

    print(f"{label}:")
    print(
        f"  rows={row_count}, deleted={deleted_blocks}, "
        f"remaining={remaining_blocks}, M_D={row_count}x{remaining_blocks}"
    )
    print(
        f"  Wilson factors={wilson_factors}, complete rank={wilson_rank}; "
        f"Plaza-Xiang deletion threshold={resilience_threshold}, "
        f"actual deletions={deleted_blocks}"
    )
    print(
        f"  dim Q_D >= {qd_dimension_floor}, while dim Sym^2(U) <= "
        f"{SYMMETRIC_SQUARE_DIMENSION}; local square gives dim U^2 >= 16"
    )
    print(f"  Product-Singleton only gives d_min(U^2) <= {product_singleton_upper}")
    print(
        f"  global NTF: dimension={DIM}, norm=2, "
        f"size={remaining_blocks}, frame constant={frame_constant}, "
        f"degree={degree}"
    )
    print(
        f"  per vertex nonedge sums: first={nonedge_sum}, "
        f"squares={nonedge_square_sum}; a constant nonedge square would be "
        f"{forced_constant_square}, a nonsquare mod 17"
    )
    print(
        f"  Gerzon conditional: {remaining_blocks} > {gerzon_bound}, "
        "so the global frame cannot have all off-diagonal squares equal to 1"
    )


def main() -> None:
    standard_simplex_checks()
    adjacent_star_pair_checks()
    layer_checks(4, 21, "LS(4,5,21)")
    layer_checks(3, 20, "LS(3,4,20)")
    print("ALL LITERATURE-HYPOTHESIS AND FRAME-CONSEQUENCE CHECKS PASSED")


if __name__ == "__main__":
    main()
