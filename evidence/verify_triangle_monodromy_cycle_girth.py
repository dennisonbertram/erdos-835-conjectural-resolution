#!/usr/bin/env python3
"""Exact checks for triangle_monodromy_cycle_girth_audit.md.

This is deliberately a finite verification of the numerical and extremal
claims only.  The general implications in the note are proved there.
"""

from itertools import combinations
from math import comb


def vertices(k):
    return tuple(frozenset(S) for S in combinations(range(2 * k - 1), k - 1))


def adjacent(A, B):
    return not (A & B)


def has_odd_cycle_of_length(k, length):
    """Brute force simple cycles through a canonical least vertex, k <= 6."""
    V = vertices(k)
    index = {v: i for i, v in enumerate(V)}
    nbrs = {v: tuple(w for w in V if adjacent(v, w)) for v in V}

    def extend(path):
        if len(path) == length:
            return adjacent(path[-1], path[0])
        for w in nbrs[path[-1]]:
            if index[w] < index[path[0]] or w in path:
                continue
            if extend(path + (w,)):
                return True
        return False

    return any(extend((v,)) for v in V)


def extremal_cycle(k):
    q = 2 * k - 1
    r = k - 1
    cycle = tuple(frozenset((i + 2 * j) % q for j in range(r)) for i in range(q))
    assert len(set(cycle)) == q
    assert all(adjacent(cycle[i], cycle[(i + 1) % q]) for i in range(q))
    return cycle


def main():
    # Exact sheet parity at the parameter of the open problem.
    sheets = comb(31, 15) // 17
    assert sheets == 17_678_835 and sheets % 2 == 1
    print(f"k=16 sheets={sheets}: odd")

    # Construct equality cases of odd girth for several parameters.
    for k in (2, 3, 4, 6, 16):
        cycle = extremal_cycle(k)
        assert len(cycle) == 2 * k - 1
        print(f"O_{k}: explicit odd cycle length {len(cycle)}")

    # Independent exhaustive checks of the lower bound where enumeration is
    # tiny enough.  O_2=K_3 is the genuine cover control; O_4 and O_6 are
    # the standard single-code controls from the companion audit.
    for k in (2, 3, 4):
        target = 2 * k - 1
        assert all(not has_odd_cycle_of_length(k, ell)
                   for ell in range(3, target, 2))
        assert has_odd_cycle_of_length(k, target)
        print(f"O_{k}: exhaustive odd-girth check PASS ({target})")

    # The integer implication used at k=16.
    assert min(r for r in range(1, 100, 2) if 3 * r >= 31) == 11
    print("k=16 odd monodromy period bound: r >= 11")
    print("triangle monodromy cycle-girth audit: PASS")


if __name__ == "__main__":
    main()
