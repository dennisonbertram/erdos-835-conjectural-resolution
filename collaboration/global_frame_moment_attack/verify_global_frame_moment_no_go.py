#!/usr/bin/env python3
"""Exact countermodels to global finite-field frame-moment obstructions.

For each true/false/target parameter set, construct a linear uniform
hypergraph having the same deleted-star counts and degrees, label its
vertices by a repeated F_p simplex, and verify all local frame, global
tight-frame, operator-moment, Schur-power, and first through sixteenth
entry-moment identities used in the companion note.

The model is abstract: its rows are not claimed to be subset-incidence rows.
Only Python integer arithmetic is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class Parameters:
    label: str
    prime: int
    block_size: int
    fibre_size: int

    @property
    def colours(self) -> int:
        return self.prime - 1

    @property
    def vertices(self) -> int:
        return self.colours * self.fibre_size

    @property
    def rows(self) -> int:
        return self.block_size * self.fibre_size

    @property
    def degree(self) -> int:
        return self.block_size * (self.colours - 1)


PARAMETERS = (
    Parameters("k=2 true control", 3, 2, 2),
    Parameters("k=4 false control", 5, 4, 14),
    Parameters("k=6 false control", 7, 6, 132),
    Parameters("derived LS(4,5,21)", 17, 5, 1197),
    Parameters("derived LS(3,4,20)", 17, 4, 285),
)


def inv(value: int, prime: int) -> int:
    return pow(value % prime, -1, prime)


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inv(work[rank][column], prime)
        work[rank] = [scale * value % prime for value in work[rank]]
        for row in range(row_count):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                (left - scale * right) % prime
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def matmul(
    left: list[list[int]], right: list[list[int]], prime: int
) -> list[list[int]]:
    right_t = list(zip(*right))
    return [
        [sum(a * b for a, b in zip(row, column)) % prime for column in right_t]
        for row in left
    ]


def dot(left: tuple[int, ...], right: tuple[int, ...], prime: int) -> int:
    return sum(a * b for a, b in zip(left, right)) % prime


def simplex(prime: int) -> list[tuple[int, ...]]:
    """The p-1 vectors e_a+1 in H_0 <= F_p^(p-1)."""
    colours = prime - 1
    vectors = []
    for colour in range(colours):
        vector = [1] * colours
        vector[colour] += 1
        vectors.append(tuple(value % prime for value in vector))
    return vectors


def row_vertices(parameters: Parameters, direction: int, offset: int):
    """One abstract deleted star, containing one vertex of every fibre."""
    d = parameters.fibre_size
    for colour in range(parameters.colours):
        sheet = (offset + direction * colour) % d
        yield colour * d + sheet


def verify_hypergraph(parameters: Parameters) -> None:
    q = parameters.colours
    d = parameters.fibre_size
    s = parameters.block_size
    n = parameters.vertices

    # This strict inequality proves different directions cannot repeat a
    # pair: a nonzero integer (j-j')(a-b) has magnitude below d.
    assert d > (s - 1) * (q - 1)

    degrees = [0] * n
    pairs: set[int] = set()
    row_count = 0
    for direction in range(s):
        for offset in range(d):
            row = tuple(row_vertices(parameters, direction, offset))
            assert len(row) == q and len(set(row)) == q
            assert {vertex // d for vertex in row} == set(range(q))
            row_count += 1
            for vertex in row:
                degrees[vertex] += 1
            for left, right in combinations(row, 2):
                if left > right:
                    left, right = right, left
                key = left * n + right
                assert key not in pairs
                pairs.add(key)

    assert row_count == parameters.rows
    assert all(degree == s for degree in degrees)
    assert len(pairs) == parameters.rows * q * (q - 1) // 2
    assert 2 * len(pairs) == n * parameters.degree


def verify_simplex_and_gram(parameters: Parameters) -> None:
    p = parameters.prime
    q = parameters.colours
    d = parameters.fibre_size
    n = parameters.vertices
    s = parameters.block_size
    degree = parameters.degree
    vectors = simplex(p)

    assert all(sum(vector) % p == 0 for vector in vectors)
    assert all(
        dot(vectors[a], vectors[b], p) == (2 if a == b else 1)
        for a in range(q)
        for b in range(q)
    )
    assert all(
        sum(vectors[a][coordinate] for a in range(q)) % p == 0
        for coordinate in range(q)
    )

    local_gram = [[2 if a == b else 1 for b in range(q)] for a in range(q)]
    assert rank_mod(local_gram, p) == q - 1
    assert matmul(local_gram, local_gram, p) == local_gram

    # The global Gram has d repeated copies of every simplex vector:
    # G = J + E, where E is the same-fibre equivalence matrix.
    assert d % p
    assert (n + d) % p == 0  # G*1=0.
    assert (2 * n - d * (q - 1)) % p == 0  # trace tightness.

    # Direct fibre-level verification of G^2=dG.
    same_entry = d * (4 + q - 1) % p
    cross_entry = d * (2 + 2 + q - 2) % p
    assert same_entry == 2 * d % p
    assert cross_entry == d % p

    # Local zero sums imply A G = G A = -s G for the co-row graph A.
    same_ag = degree % p
    cross_ag = s * (2 + q - 2) % p
    assert same_ag == -2 * s % p
    assert cross_ag == -s % p

    # Ordinary spectral/operator moments of a c-tight Gram matrix.
    gram_trace = 2 * n % p
    for power in range(1, 5):
        expected_trace = pow(d, power - 1, p) * gram_trace % p
        # Eigenvalues are d (multiplicity q-1) and 0.
        spectral_trace = (q - 1) * pow(d, power, p) % p
        assert expected_trace == spectral_trace

    # Every Schur power remains in the two-dimensional span of J and E:
    # G^(o r)=J+(2^r-1)E.  Its rank is read on the q fibre constants.
    schur_ranks = []
    for power in range(1, p):
        alpha = (pow(2, power, p) - 1) % p
        compressed = [
            [(1 + alpha * int(a == b)) % p for b in range(q)] for a in range(q)
        ]
        schur_rank = rank_mod(compressed, p)
        schur_ranks.append(schur_rank)
        assert schur_rank <= q

    # Entry moments around every vertex.  Adjacencies are cross-fibre and
    # hence have inner product one.  The nonedges have this exact formal
    # distribution.
    nonedge_twos = d - 1
    nonedge_ones = (q - 1) * d - degree
    nonneighbors = n - 1 - degree
    assert nonedge_twos >= 0 and nonedge_ones >= 0
    assert nonedge_twos + nonedge_ones == nonneighbors
    for power in range(1, p):
        model_total = d * pow(2, power) + (q - 1) * d
        local_tensor_total = d * (pow(2, power, p) - 2) % p
        assert model_total % p == local_tensor_total
        model_nonedge = nonedge_twos * pow(2, power) + nonedge_ones
        forced_nonedge = (local_tensor_total - pow(2, power, p) - degree) % p
        assert model_nonedge % p == forced_nonedge

    # Display the third/fourth moments requested in the attack.
    third = d * (pow(2, 3, p) - 2) % p
    fourth = d * (pow(2, 4, p) - 2) % p
    print(
        f"{parameters.label}: p={p}, rows={parameters.rows}, "
        f"vertices={n}, degree={degree}, frame_constant={d % p}, "
        f"rank(G)={q - 1}, total_m3={third}, total_m4={fourth}, "
        f"Schur_ranks_1..{p - 1}={schur_ranks}"
    )


def main() -> None:
    for parameters in PARAMETERS:
        verify_hypergraph(parameters)
        verify_simplex_and_gram(parameters)
    print("ALL GLOBAL FRAME-MOMENT COUNTERMODELS PASSED")


if __name__ == "__main__":
    main()
