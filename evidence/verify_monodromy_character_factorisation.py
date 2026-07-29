#!/usr/bin/env python3
"""Exact Walecki countermodel for monodromy_character_factorisation_audit."""

from fractions import Fraction


def walecki_cycles(n):
    """Partition K_n, n=2m+1, into m Hamilton cycles."""
    assert n % 2 == 1
    m = (n - 1) // 2
    infinity = 2 * m
    cycles = []
    for shift in range(m):
        cycle = [infinity]
        for t in range(m):
            cycle.extend(((shift - t) % (2 * m), (shift + t + 1) % (2 * m)))
        assert len(cycle) == n and len(set(cycle)) == n
        cycles.append(tuple(cycle))
    return tuple(cycles)


def permutation_from_cycle(cycle):
    n = len(cycle)
    p = [None] * n
    for i, x in enumerate(cycle):
        p[x] = cycle[(i + 1) % n]
    return tuple(p)


def inverse(p):
    q = [None] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)


def fixed(p):
    return sum(i == x for i, x in enumerate(p))


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def matrix_of_perm(p):
    n = len(p)
    M = [[0] * n for _ in range(n)]
    for i, j in enumerate(p):
        M[j][i] = 1
    return M


def add_into(A, B, scale=1):
    for i, row in enumerate(B):
        for j, value in enumerate(row):
            A[i][j] += scale * value


def matmul_trace(A, B):
    return sum(A[i][j] * B[j][i] for i in range(len(A)) for j in range(len(A)))


def main():
    n = 121
    cycles = walecki_cycles(n)
    assert len(cycles) == 60

    # Verify Walecki is an edge partition of K_121.
    edges = set()
    for cycle in cycles:
        for i, x in enumerate(cycle):
            edge = tuple(sorted((x, cycle[(i + 1) % n])))
            assert edge not in edges
            edges.add(edge)
    assert len(edges) == n * (n - 1) // 2

    generators = tuple(permutation_from_cycle(cycle) for cycle in cycles)
    assert all(fixed(g) == 0 and fixed(compose(g, g)) == 0 for g in generators)
    assert all(sorted(g) == list(range(n)) for g in generators)

    # Two copies of each unoriented factor, with inverse orientations,
    # give 240 permutation matrices in the displayed factorisation.
    oriented = []
    for g in generators:
        oriented.extend((g, g, inverse(g), inverse(g)))
    assert len(oriented) == 240

    T = [[0] * n for _ in range(n)]
    for g in oriented:
        add_into(T, matrix_of_perm(g))

    R = [[0] * n for _ in range(n)]
    for g in generators:
        add_into(R, matrix_of_perm(g))
        add_into(R, matrix_of_perm(inverse(g)))
    assert all(R[i][i] == 0 for i in range(n))
    assert all(sum(row) == 120 for row in R)
    assert all(R[i][j] in (0, 1) for i in range(n) for j in range(n))
    assert T == [[2 * R[i][j] for j in range(n)] for i in range(n)]

    # Standard and exterior-square identities.
    assert sum(fixed(g) - 1 for g in oriented) == -240
    assert all(Fraction(fixed(g) ** 2 - fixed(compose(g, g)), 2) == 0
               for g in oriented)
    tr_T = sum(T[i][i] for i in range(n))
    tr_T2 = matmul_trace(T, T)
    assert tr_T == 0
    assert tr_T2 == 4 * n * 120
    assert Fraction(tr_T * tr_T - tr_T2, 2) == -2 * n * 120

    print("Walecki K_121 factorisation: PASS")
    print("240 fixed-point-free 121-cycles; every exterior-square character is 0")
    print(f"tr(T^2)={tr_T2}; tr(wedge^2 T)={-2 * n * 120}")
    print("monodromy character-factorisation audit: PASS")


if __name__ == "__main__":
    main()
