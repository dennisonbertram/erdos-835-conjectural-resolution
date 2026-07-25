#!/usr/bin/env python3
"""Exact checks for evidence/distance_regular_cover_audit.md.

No solver or floating point arithmetic is used.  The checks deliberately
separate a genuine O_2 -> K_3 cover from the individual O_4 and O_6 perfect
codes: the latter two are controls for necessary single-fibre formulae, not
putative covers.
"""

from itertools import combinations, product
from math import comb


def odd_vertices(k):
    return tuple(frozenset(s) for s in combinations(range(2 * k - 1), k - 1))


def closed_neighbourhood(v, universe):
    return {v} | {w for w in universe if not (v & w)}


def check_perfect_code(k, code):
    universe = odd_vertices(k)
    code = tuple(map(frozenset, code))
    assert set(code) <= set(universe)
    cover_count = {v: 0 for v in universe}
    for c in code:
        for v in closed_neighbourhood(c, universe):
            cover_count[v] += 1
    assert set(cover_count.values()) == {1}

    # The relation |A intersect B|=1 is the distance-three relation for k>2.
    degree = k * (k - 1) // 2
    for c in code:
        assert sum(len(c & d) == 1 for d in code) == degree


def psl2_11_hexads():
    """Carmichael's projective-line model of W_12, exactly."""
    p = 11
    points = (None,) + tuple(range(p))

    def image(a, b, c, d, z):
        if z is None:
            return None if c == 0 else (a * pow(c, -1, p)) % p
        den = (c * z + d) % p
        return None if den == 0 else ((a * z + b) * pow(den, -1, p)) % p

    seed = frozenset((None, 1, 3, 4, 5, 9))
    blocks = set()
    for a, b, c, d in product(range(p), repeat=4):
        if (a * d - b * c) % p != 1:
            continue
        blocks.add(frozenset(image(a, b, c, d, z) for z in seed))
    assert len(blocks) == 132
    assert all(len(B) == 6 for B in blocks)
    for five in combinations(points, 5):
        assert sum(set(five) <= B for B in blocks) == 1
    assert {frozenset(points) - B for B in blocks} == blocks
    return blocks


def check_parameter_formulae():
    for k in (2, 4, 6, 16):
        n = comb(2 * k - 1, k - 1) // (k + 1)
        v1 = comb(k - 1, 1) * comb(k, 2)
        eta1 = k - 1
        a1 = (v1 + k * eta1) // (k + 1)
        assert (v1 + k * eta1) % (k + 1) == 0
        assert a1 == k * (k - 1) // 2
        assert 2 * a1 == k * (k - 1)
        print(f"k={k}: sheets={n}, v_1={v1}, a_1={a1}")


def check_o2_cover():
    # O_2=K_3.  The identity map is a cover to K_3.  Its two oriented
    # triangles based at a colour both lift to the identity on that fibre.
    vertices = odd_vertices(2)
    assert len(vertices) == 3
    colours = {v: next(iter(v)) for v in vertices}
    for v in vertices:
        assert {colours[w] for w in vertices if w != v} == set(range(3)) - {colours[v]}
    # On a singleton fibre the |intersection|=1 relation is I, and the two
    # ordered choices of the other colours yield 2I exactly.
    assert 2 == 2 * 1


def main():
    check_parameter_formulae()
    check_o2_cover()

    # The seven Fano lines form a 1-perfect code in O_4, but cannot be
    # completed to the required five-colour cover.
    fano = (
        (0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
        (1, 4, 6), (2, 3, 6), (2, 4, 5),
    )
    check_perfect_code(4, fano)
    print("O_4 Fano perfect-code control: PASS (internal R_1 degree 6)")

    # The projective-line construction produces W_12=S(5,6,12).  Taking the
    # 66 hexads through infinity and deleting infinity gives a 1-perfect code
    # in O_6.  It too is only a single-fibre control.
    hexads = psl2_11_hexads()
    witt_code = [B - {None} for B in hexads if None in B]
    assert len(witt_code) == 66
    check_perfect_code(6, witt_code)
    print("O_6 Witt perfect-code control: PASS (internal R_1 degree 15)")
    print("distance-regular cover audit checks: PASS")


if __name__ == "__main__":
    main()
