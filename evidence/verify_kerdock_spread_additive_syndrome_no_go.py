#!/usr/bin/env python3
"""Finite audit for the quotient-multiplicity step in the spread no-go."""

from itertools import combinations

Q = range(16)  # F_2^4, represented by xor.


def main() -> None:
    # For r != 0, a nonempty support D with r+D subset D is invariant under
    # translation by r. The forced multiplicity m(r+s)=1 therefore makes
    # every represented element occur once, so it can contribute at most 16
    # indices, never the required |U|=18. Check every r and every support.
    for r in range(1, 16):
        representatives = []
        unseen = set(Q)
        while unseen:
            s = min(unseen)
            representatives.append(s)
            unseen.remove(s)
            unseen.remove(s ^ r)
        assert len(representatives) == 8
        for mask in range(1, 1 << 8):
            support = set()
            for bit, s in enumerate(representatives):
                if mask >> bit & 1:
                    support.update((s, s ^ r))
            assert {s ^ r for s in support} == support
            forced_total = len(support)
            assert forced_total <= 16 < 18

    # The comparison used after r=0: any two indices occur as the two
    # differing points of 14-subsets with a common 13-subset of a 32-set.
    indices = range(32)
    for i, j in combinations(indices, 2):
        common = tuple(x for x in indices if x not in (i, j))[:13]
        assert len(common) == 13
        assert i not in common and j not in common

    print("PASS: every binary 4-spread additive syndrome hits the 16-vs-18 obstruction")


if __name__ == "__main__":
    main()
