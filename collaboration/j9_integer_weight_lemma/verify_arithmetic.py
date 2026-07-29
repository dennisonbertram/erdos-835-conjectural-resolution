#!/usr/bin/env python3
"""Standard-library arithmetic audit for NOTE.md.

This is not a black-box search for 78 edge labels.  It exhausts the small
integer ranges in each implication of the human proof and raises immediately
if any claimed implication has an omitted numerical case.
"""

from itertools import product


def audit_row_bounds() -> None:
    allowed = {
        z
        for total, z in product(range(-26, 8), range(-20, 21))
        if -66 <= 10 * z + total <= 18
    }
    assert allowed == set(range(-7, 5)), allowed


def audit_edge_bounds() -> None:
    allowed = {
        edge
        for za, zb, edge in product(range(-7, 5), range(-7, 5), range(-20, 21))
        if -11 <= 9 * edge + za + zb <= 3
    }
    assert allowed == {-2, -1, 0, 1}, allowed


def audit_minus_two_exclusion() -> None:
    cases = 0
    for za, zb in product(range(-7, 5), repeat=2):
        if -18 + za + zb < -11:
            continue
        assert za >= 3 and zb >= 3
        for zac, zbc in product(range(-2, 2), repeat=2):
            if -2 + zac + zbc < -1:
                continue
            cases += 1
            assert zac == 1 or zbc == 1
            # Whichever endpoint supplies a positive edge has row sum >= 3.
            endpoint = za if zac == 1 else zb
            possible_zc = [
                zc for zc in range(-7, 5) if 9 + endpoint + zc <= 3
            ]
            assert not possible_zc, (za, zb, zac, zbc, possible_zc)
    assert cases > 0


def audit_negative_degree_bounds() -> None:
    possible_after_first_bound = []
    for k in range(13):
        if k < 2 or 2 * (2 * k - 14) <= -6:
            possible_after_first_bound.append(k)
    assert possible_after_first_bound == list(range(6))

    possible_after_clique_counts = []
    for k in possible_after_first_bound:
        if k < 2 or 2 * (k - 1) <= 4:
            possible_after_clique_counts.append(k)
    assert possible_after_clique_counts == [0, 1, 2, 3]


def audit_positive_edge_exclusion() -> None:
    cases = 0
    for na, nb, pa, pb in product(range(4), range(4), range(1, 13), range(1, 13)):
        za = pa - na
        zb = pb - nb
        cases += 1
        assert za + zb >= -4
        assert not (9 + za + zb <= 3)
    assert cases > 0


def main() -> None:
    audit_row_bounds()
    print("PASS row bounds: -7 <= Z_a <= 4")
    audit_edge_bounds()
    print("PASS edge bounds: z_ab in {-2,-1,0,1}")
    audit_minus_two_exclusion()
    print("PASS exclusion of z_ab=-2")
    audit_negative_degree_bounds()
    print("PASS negative degrees: first <=5, then <=3")
    audit_positive_edge_exclusion()
    print("PASS exclusion of positive edges")
    print("PASS: all arithmetic implications in the human proof were exhausted")


if __name__ == "__main__":
    main()
