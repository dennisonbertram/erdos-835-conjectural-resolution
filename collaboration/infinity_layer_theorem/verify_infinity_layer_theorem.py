#!/usr/bin/env python3
"""Exact finite checks for collaboration/infinity_layer_theorem/README.md.

No solver and no imported project code: this independently verifies the
two-sided matching axioms, the direct H_infinity product, and rho(Psi).
"""

from itertools import combinations


def sign_of_map(domain, target, mapping):
    position = {value: index for index, value in enumerate(target)}
    word = [position[mapping[value]] for value in domain]
    return -1 if sum(
        word[left] > word[right]
        for left in range(len(word))
        for right in range(left + 1, len(word))
    ) % 2 else 1


def mate_map(matching, vertices):
    result = {}
    for edge in matching:
        left, right = tuple(edge)
        result[left], result[right] = right, left
    assert sorted(result) == sorted(vertices)
    return result


def verify_two_sided(Psi, D, A, V):
    edges_a = [frozenset(edge) for edge in combinations(A, 2)]
    edges_v = [frozenset(edge) for edge in combinations(V, 2)]
    assert set(D) == set(edges_a)
    for edge in edges_a:
        assert len(D[edge]) == len(V) // 2
        assert set(mate_map(D[edge], V)) == set(V)
    for uv in edges_v:
        selected = [ij for ij in edges_a if uv in D[ij]]
        endpoints = [point for ij in selected for point in ij]
        assert sorted(endpoints) == [point for point in A if point != Psi[uv]]


def h_infinity(Psi, D, A, V):
    answer = 1
    for i in A:
        matching_i = [edge for edge, colour in Psi.items() if colour == i]
        mate_i = mate_map(matching_i, V)
        for u in V:
            domain = [j for j in A if j != i]
            target = [v for v in V if v not in (u, mate_i[u])]
            mapping = {}
            for j in domain:
                mate = mate_map(D[frozenset((i, j))], V)
                mapping[j] = mate[u]
            answer *= sign_of_map(domain, target, mapping)
    return answer


def rho(Psi, A, V):
    answer = 1
    for i in A:
        matching_i = [edge for edge, colour in Psi.items() if colour == i]
        mate_i = mate_map(matching_i, V)
        domain = [
            (u, v)
            for u in V
            for v in V
            if v not in (u, mate_i[u])
        ]
        target = [
            (f, u)
            for f in A
            if f != i
            for u in V
        ]
        answer *= sign_of_map(
            domain,
            target,
            {(u, v): (Psi[frozenset((u, v))], u) for u, v in domain},
        )
    return answer


def bose_sts15_colour():
    """A Bose STS(15), returned as its Steiner quasigroup on 0,...,14."""

    points = [(x, t) for x in range(5) for t in range(3)]
    blocks = []
    for x in range(5):
        blocks.append({(x, 0), (x, 1), (x, 2)})
    for x in range(5):
        for y in range(x + 1, 5):
            z = 3 * (x + y) % 5  # division by two in F_5
            for t in range(3):
                blocks.append({(x, t), (y, t), (z, (t + 1) % 3)})
    assert len(blocks) == 35
    third = {}
    for block in blocks:
        for left, right in combinations(block, 2):
            other = next(point for point in block if point not in (left, right))
            third[left, right] = third[right, left] = other
    assert len(third) == 15 * 14
    label = {point: 3 * point[0] + point[1] for point in points}
    return lambda left, right: label[third[points[left], points[right]]]


def xor_model():
    k = 16
    V, A = list(range(k)), list(range(1, k))
    Psi = {
        frozenset((u, v)): u ^ v
        for u, v in combinations(V, 2)
    }
    D = {
        frozenset((i, j)): {
            frozenset((u, u ^ (i ^ j)))
            for u in V
            if u < (u ^ (i ^ j))
        }
        for i, j in combinations(A, 2)
    }
    return Psi, D, A, V


def round_robin_factorization(k):
    result = {}
    for colour in range(k - 1):
        matching = {frozenset((colour, k - 1))}
        for offset in range(1, k // 2):
            matching.add(
                frozenset(((colour + offset) % (k - 1), (colour - offset) % (k - 1)))
            )
        result[colour] = matching
    return result


def round_robin_bose_model():
    k = 16
    V, A = list(range(k)), list(range(k - 1))
    factors = round_robin_factorization(k)
    Psi = {edge: colour for colour, matching in factors.items() for edge in matching}
    f = bose_sts15_colour()
    D = {
        frozenset((i, j)): factors[f(i, j)]
        for i, j in combinations(A, 2)
    }
    return Psi, D, A, V


def standard_rho_table():
    observed = []
    for k in range(4, 32, 2):
        A, V = list(range(k - 1)), list(range(k))
        factors = round_robin_factorization(k)
        Psi = {edge: colour for colour, matching in factors.items() for edge in matching}
        observed.append(rho(Psi, A, V))
        expected = -1 if ((k // 2 - 1) * (k // 2 - 2) // 2) % 2 else 1
        assert observed[-1] == expected
    return observed


def all_perfect_matchings(vertices):
    vertices = frozenset(vertices)
    result = []

    def visit(remaining, current):
        if not remaining:
            result.append(set(current))
            return
        left = min(remaining)
        for right in sorted(remaining - {left}):
            current.append(frozenset((left, right)))
            visit(remaining - {left, right}, current)
            current.pop()

    visit(vertices, [])
    return result


def enumerate_standard_models(k):
    """Independent exhaustive check for k=4 and k=6 only."""

    A, V = list(range(k - 1)), list(range(k))
    factors = round_robin_factorization(k)
    Psi = {edge: colour for colour, matching in factors.items() for edge in matching}
    edges_a = [frozenset(edge) for edge in combinations(A, 2)]
    edges_v = [frozenset(edge) for edge in combinations(V, 2)]
    choices = all_perfect_matchings(V)
    D, results = {}, []

    def visit(position):
        if position == len(edges_a):
            verify_two_sided(Psi, D, A, V)
            results.append(dict(D))
            return
        ij = edges_a[position]
        for matching in choices:
            D[ij] = matching
            valid = True
            for uv in edges_v:
                used = [point for edge, pm in D.items() if uv in pm for point in edge]
                if len(used) != len(set(used)) or Psi[uv] in used:
                    valid = False
                    break
            if valid:
                visit(position + 1)
            del D[ij]

    visit(0)
    return Psi, A, V, results


if __name__ == "__main__":
    for k, count in ((4, 1), (6, 7)):
        Psi, A, V, models = enumerate_standard_models(k)
        invariant = rho(Psi, A, V)
        assert len(models) == count
        assert {h_infinity(Psi, D, A, V) for D in models} == {invariant}
        print(f"k={k}: all {count} standard-Psi tensors have H_inf=rho={invariant:+d}")
    for name, factory, expected in (
        ("binary F_2^4", xor_model, 1),
        ("round-robin plus Bose STS(15)", round_robin_bose_model, -1),
    ):
        Psi, D, A, V = factory()
        verify_two_sided(Psi, D, A, V)
        direct = h_infinity(Psi, D, A, V)
        invariant = rho(Psi, A, V)
        assert direct == invariant == expected
        print(f"{name}: two-sided axioms PASS; H_inf=rho={direct:+d}")
    print("round-robin rho for k=4,6,...,30:", standard_rho_table())
    print("infinity-layer theorem finite checks: PASS")
