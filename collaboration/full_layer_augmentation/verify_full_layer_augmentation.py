#!/usr/bin/env python3
"""Exact checks for the no-hole sign and the cofactor bookkeeping.

Stdlib only.  The k=4 search exhausts complete no-hole tensors, and the k=6
search fixes the first matching without loss under vertex relabelling.  The
cofactor test is independent of any design.
"""

from itertools import combinations
from random import Random


def sign_of_map(domain, target, mapping):
    position = {value: index for index, value in enumerate(target)}
    word = [position[mapping[value]] for value in domain]
    return -1 if sum(
        word[i] > word[j]
        for i in range(len(word))
        for j in range(i + 1, len(word))
    ) % 2 else 1


def mate_map(matching, vertices):
    result = {}
    for edge in matching:
        left, right = tuple(edge)
        result[left], result[right] = right, left
    assert sorted(result) == sorted(vertices)
    return result


def all_perfect_matchings(vertices):
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

    visit(frozenset(vertices), [])
    return result


def enumerate_no_hole(k, fix_first=False):
    B, V = list(range(k)), list(range(k))
    edges_b = [frozenset(edge) for edge in combinations(B, 2)]
    edges_v = [frozenset(edge) for edge in combinations(V, 2)]
    choices = all_perfect_matchings(V)
    tensor, answers = {}, []

    def visit(index):
        if index == len(edges_b):
            answers.append(dict(tensor))
            return
        rs = edges_b[index]
        for matching in choices:
            tensor[rs] = matching
            okay = True
            for uv in edges_v:
                used = [point for edge, pm in tensor.items() if uv in pm for point in edge]
                if len(used) != len(set(used)):
                    okay = False
                    break
            if okay:
                visit(index + 1)
            del tensor[rs]

    if fix_first:
        tensor[edges_b[0]] = choices[0]
        visit(1)
        del tensor[edges_b[0]]
    else:
        visit(0)
    return B, V, answers


def no_hole_link_product(B, V, tensor):
    answer = 1
    for r in B:
        for u in V:
            domain = [s for s in B if s != r]
            target = [v for v in V if v != u]
            mapping = {
                s: mate_map(tensor[frozenset((r, s))], V)[u]
                for s in domain
            }
            assert set(mapping.values()) == set(target)
            answer *= sign_of_map(domain, target, mapping)
    return answer


def cofactor_sign(X, Y, R, C, alpha):
    RD = [value for value in X if value in R]
    RX = [value for value in X if value not in R]
    CD = [value for value in Y if value in C]
    CY = [value for value in Y if value not in C]
    return (
        sign_of_map(RD + RX, X, {value: value for value in RD + RX})
        * sign_of_map(CD + CY, Y, {value: value for value in CD + CY})
        * sign_of_map(RX, CY, alpha)
    )


def verify_cofactor_identity():
    rng = Random(835)
    X = list(range(8))
    Y = list(range(8))
    for _ in range(200):
        size = rng.choice((0, 1, 2, 3, 4, 5, 6, 7, 8))
        R = set(rng.sample(X, size))
        C = set(rng.sample(Y, size))
        RD, CD = sorted(R), sorted(C)
        RX = [value for value in X if value not in R]
        CY = [value for value in Y if value not in C]
        rng.shuffle(CD)
        rng.shuffle(CY)
        f = dict(zip(RD, CD))
        alpha = dict(zip(RX, CY))
        full = f | alpha
        assert sign_of_map(X, Y, full) == (
            cofactor_sign(X, Y, R, C, alpha) * sign_of_map(RD, sorted(C), f)
        )
    print("200 random cofactor extensions: PASS")


def verify_hole_completion_patterns():
    # Generic x: three holes plus *, completed as {i_u,i_v},{i_M,*}.
    star = 7
    holes = (1, 3, 5)
    old = {frozenset((0, 2)), frozenset((4, 6))}
    completed = old | {frozenset((holes[1], holes[2])), frozenset((holes[0], star))}
    assert sorted(point for edge in completed for point in edge) == list(range(8))
    # Endpoint case: exactly one A-hole joins the dummy index.
    old = {frozenset((0, 1)), frozenset((3, 4)), frozenset((5, 6))}
    completed = old | {frozenset((2, star))}
    assert sorted(point for edge in completed for point in edge) == list(range(8))
    print("generic and endpoint dual-hole completions: PASS")


if __name__ == "__main__":
    verify_cofactor_identity()
    verify_hole_completion_patterns()
    for k, expected_count, fixed in ((4, 6, False), (6, 336, True)):
        B, V, tensors = enumerate_no_hole(k, fix_first=fixed)
        assert len(tensors) == expected_count
        assert {no_hole_link_product(B, V, tensor) for tensor in tensors} == {1}
        qualifier = "all" if not fixed else "all first-matching-normalized"
        print(f"k={k}: {qualifier} {expected_count} no-hole tensors have link product +1")
    print("full-layer augmentation finite checks: PASS")
