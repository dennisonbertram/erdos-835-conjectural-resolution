"""Verifier for the star-sign results of this directory.

Standard library only, exact finite arithmetic, no solver, no randomness, no
network.  Every claim of NOTE.md that is finite is replayed here.

    python3 -B verify_star_sign.py
"""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations, permutations
from math import comb
from pathlib import Path

from sign_census import canonical_one_factorizations
from star_sign import (
    bijection_sign,
    derive,
    invariance_exponents,
    one_factorizations,
    perm_sign,
    relabel_colours,
    relabel_points,
    star_sign,
)

REPO = Path(__file__).resolve().parents[3]

CHECKS: list[tuple[str, bool]] = []


def check(name: str, ok: bool) -> None:
    CHECKS.append((name, bool(ok)))
    print(("PASS  " if ok else "FAIL  ") + name)
    sys.stdout.flush()


def ground_minus(v: int, p: int) -> list[int]:
    return [x for x in range(v) if x != p]


# --------------------------------------------------------------- section 1
# Well-definedness and the exact relabelling exponents.


def section_restriction_lemma() -> None:
    """Independent brute-force check of the permutation identity behind Thm 1.

    For every permutation tau of [v] and every t,

        prod over t-subsets T of  sgn(tau : [v]\\T -> [v]\\tau T)
            = sgn(tau)^(C(v,t) + C(v-1,t-1)) * sgn(tau^(t)),

    and for a transposition sgn(tau^(t)) = (-1)^C(v-2,t-1).  This is proved in
    NOTE.md via the t-th compound matrix; it is checked here with no design
    theory involved at all.
    """
    ok_all, ok_transp = True, True
    for v in range(2, 8):
        base = list(range(v))
        for tau_t in permutations(base):
            tau = dict(enumerate(tau_t))
            sgn_tau = perm_sign(list(tau_t))
            for t in range(1, v):
                tsets = list(combinations(base, t))
                pos = {T: i for i, T in enumerate(tsets)}
                # left-hand side
                lhs = 1
                for T in tsets:
                    Ts = set(T)
                    dom = [x for x in base if x not in Ts]
                    img = [tau[x] for x in dom]
                    cod = sorted(tau[x] for x in dom)
                    lhs *= bijection_sign(dom, img, cod)
                # induced permutation on t-sets
                induced = [pos[tuple(sorted(tau[x] for x in T))] for T in tsets]
                rhs = (sgn_tau ** (comb(v, t) + comb(v - 1, t - 1))) * perm_sign(
                    induced
                )
                if lhs != rhs:
                    ok_all = False
                # transposition specialisation
                moved = [i for i in base if tau[i] != i]
                if len(moved) == 2:
                    if perm_sign(induced) != (-1) ** comb(v - 2, t - 1):
                        ok_transp = False
    check(
        "restriction-product identity holds for every tau in S_v, v<=7, every t", ok_all
    )
    check(
        "sgn(tau^(t)) = (-1)^C(v-2,t-1) for every transposition, v<=7, every t",
        ok_transp,
    )


def section_commutator() -> None:
    """Finite control for Theorem 6: S_m has abelianisation Z/2 for m=3,4,5,
    i.e. the commutator subgroup is exactly the alternating group."""
    ok = True
    for m in (3, 4, 5):
        elems = list(permutations(range(m)))
        idx = {e: i for i, e in enumerate(elems)}

        def mul(a, b):
            return tuple(a[b[i]] for i in range(m))

        def inv(a):
            out = [0] * m
            for i, x in enumerate(a):
                out[x] = i
            return tuple(out)

        gens = {mul(mul(a, b), inv(mul(b, a))) for a in elems for b in elems}
        # closure
        sub = set(gens)
        changed = True
        while changed:
            changed = False
            for a in list(sub):
                for b in list(sub):
                    c = mul(a, b)
                    if c not in sub:
                        sub.add(c)
                        changed = True
        alt = {e for e in elems if perm_sign(list(e)) == 1}
        if sub != alt:
            ok = False
        del idx
    check("Theorem 6 control: [S_m,S_m] = A_m for m = 3,4,5, so S_m^ab = Z/2", ok)


def section_definition() -> None:
    # A transposition multiplies E_t by (-1)^(C(v,t)+C(v-1,t-1)+C(v-2,t-1));
    # a colour transposition by (-1)^C(v,t).  Cross-check the closed form
    # against brute force on a small genuine object.
    f0 = next(one_factorizations(6))
    base = star_sign(f0, v=6, t=1, m=5)
    ok_c = all(
        star_sign(relabel_colours(f0, dict(enumerate(pi))), v=6, t=1, m=5) == base
        for pi in permutations(range(5))
    )
    ok_p = all(
        star_sign(relabel_points(f0, dict(enumerate(tau))), v=6, t=1, m=5) == base
        for tau in permutations(range(6))
    )
    check("E_1 on K_6 is invariant under all 5! colour relabellings", ok_c)
    check("E_1 on K_6 is invariant under all 6! point relabellings", ok_p)
    check(
        "closed form agrees: invariance_exponents(6,1) == (0,0)",
        invariance_exponents(6, 1) == (0, 0),
    )

    # The closed form must also correctly predict a NON-invariance.  On
    # LS(2,3,9) the colour exponent is even (E_2 is colour invariant) but the
    # point exponent is odd, so a point transposition must flip E_2.
    ls9 = build_ls239()
    e = star_sign(ls9, v=9, t=2, m=7)
    swap = {i: {0: 1, 1: 0}.get(i, i) for i in range(9)}
    swap_c = {i: {0: 1, 1: 0}.get(i, i) for i in range(7)}
    check(
        "closed form: on LS(2,3,9) E_2 is colour invariant and point anti-invariant",
        invariance_exponents(9, 2) == (0, 1)
        and star_sign(relabel_colours(ls9, swap_c), 9, 2, 7) == e
        and star_sign(relabel_points(ls9, swap), 9, 2, 7) == -e,
    )
    # ... and on LS(2,3,19) the colour exponent is odd, so E_2 there is not an
    # isomorphism invariant at all -- this is what kills any rigidity at rung 2.
    check(
        "closed form: on LS(2,3,19) E_2 is colour anti-invariant",
        invariance_exponents(19, 2) == (1, 0),
    )
    reversed_order = [1, 0, *range(2, 9)]
    check(
        "an explicitly supplied ground order is preserved",
        star_sign(ls9, 9, 2, 7, ground=reversed_order) == -e,
    )


# --------------------------------------------------------------- section 2
# The one-factorization census: K_4, K_6 rigid; K_8 not.


def section_census() -> None:
    c4 = Counter(star_sign(f, v=4, t=1, m=3) for f in canonical_one_factorizations(4))
    c6 = Counter(star_sign(f, v=6, t=1, m=5) for f in canonical_one_factorizations(6))
    c8 = Counter(star_sign(f, v=8, t=1, m=7) for f in canonical_one_factorizations(8))
    print(f"      K_4 {dict(c4)}   K_6 {dict(c6)}   K_8 {dict(c8)}")
    check("K_4: 1 one-factorization, star sign identically +1", dict(c4) == {1: 1})
    check("K_6: 6 one-factorizations, star sign identically -1", dict(c6) == {-1: 6})
    check(
        "K_8: 6240 one-factorizations, 5280 of sign +1 and 960 of sign -1",
        c8[1] == 5280 and c8[-1] == 960 and sum(c8.values()) == 6240,
    )
    check("K_8 star sign is NOT constant", len(c8) == 2)


# --------------------------------------------------------------- section 3
# LS(2,3,9) built exhaustively; the tower identity.


def build_ls239() -> dict[frozenset[int], int]:
    points = list(range(9))
    triples = [frozenset(t) for t in combinations(points, 3)]
    pairs = {frozenset(p): i for i, p in enumerate(combinations(points, 2))}
    tp = {t: [pairs[frozenset(p)] for p in combinations(sorted(t), 2)] for t in triples}
    colouring: dict[frozenset[int], int] = {}
    covered = [0] * 7
    order = sorted(triples, key=sorted)

    def rec(i: int) -> bool:
        if i == len(order):
            return True
        t = order[i]
        mask = 0
        for pi in tp[t]:
            mask |= 1 << pi
        used = max((c for c in range(7) if covered[c]), default=-1)
        for colour in range(min(used + 2, 7)):
            if covered[colour] & mask:
                continue
            covered[colour] |= mask
            colouring[t] = colour
            if rec(i + 1):
                return True
            covered[colour] &= ~mask
            del colouring[t]
        return False

    if not rec(0):
        raise AssertionError("no LS(2,3,9) found")
    return dict(colouring)


def tower_identity(
    ls: dict[frozenset[int], int], v: int, t: int, m: int
) -> tuple[int, list[int]]:
    signs = [
        star_sign(derive(ls, p), v=v - 1, t=t - 1, m=m, ground=ground_minus(v, p))
        for p in range(v)
    ]
    prod = 1
    for s in signs:
        prod *= s
    return prod, signs


def section_identity() -> None:
    ls9 = build_ls239()
    check(
        "LS(2,3,9): genuine large set (84 triples, 7 classes of 12)",
        len(ls9) == 84 and sorted(Counter(ls9.values()).values()) == [12] * 7,
    )
    prod, signs = tower_identity(ls9, v=9, t=2, m=7)
    e2 = star_sign(ls9, v=9, t=2, m=7)
    check("LS(2,3,9): prod_p E_1^(p) == E_2^2 == +1", prod == e2**2 == 1)
    print("      LS(2,3,9) derived K_8 signs:", dict(Counter(signs)))

    sys.path.insert(0, str(REPO))
    from evidence.verify_defect_cross_link_lsts19 import (  # noqa: PLC0415
        construct_lsts19,
        verify_large_set,
    )

    raw = construct_lsts19()
    verify_large_set(raw)
    ls19 = {frozenset(t): c for t, c in raw.items()}
    check(
        "LS(2,3,19): repository object is a genuine large set (969 triples, 17x57)",
        len(ls19) == 969 and sorted(Counter(ls19.values()).values()) == [57] * 17,
    )
    prod, signs = tower_identity(ls19, v=19, t=2, m=17)
    e2 = star_sign(ls19, v=19, t=2, m=17)
    check("LS(2,3,19): prod_p E_1^(p) == E_2^2 == +1", prod == e2**2 == 1)
    census = dict(Counter(signs))
    print("      LS(2,3,19) derived K_18 signs:", census)
    check(
        "K_18 star sign is NOT constant: both values occur among the 19 point links",
        set(signs) == {1, -1},
    )
    check(
        "LS(2,3,19): the number of sign -1 point links is even",
        signs.count(-1) % 2 == 0,
    )


# --------------------------------------------------------------- section 4
# The LS(2,3,7) exclusion, and the negative controls.


def section_exclusion() -> None:
    signs6 = {star_sign(f, v=6, t=1, m=5) for f in canonical_one_factorizations(6)}
    check(
        "all one-factorizations of K_6 have star sign -1 (exhaustive)", signs6 == {-1}
    )
    check("hence LS(2,3,7) is excluded: (-1)^7 != +1", (-1) ** 7 != 1)

    # Control: the same argument must NOT fire for LS(2,3,9) or LS(2,3,19),
    # both of which exist.  It fires only when the predecessor rung is rigid
    # with sign -1 and the number of points is odd.
    c8 = Counter(star_sign(f, v=8, t=1, m=7) for f in canonical_one_factorizations(8))
    check(
        "control: the argument cannot fire at LS(2,3,9), since K_8 is not rigid",
        len(c8) == 2,
    )

    # Control: a direct exhaustive check that no LS(2,3,7) exists, independent
    # of the sign argument (35 triples, 5 Fano planes).
    check("control: exhaustive search confirms no LS(2,3,7)", not exists_ls237())


def exists_ls237() -> bool:
    points = list(range(7))
    triples = [frozenset(t) for t in combinations(points, 3)]
    pairs = {frozenset(p): i for i, p in enumerate(combinations(points, 2))}
    tp = {t: [pairs[frozenset(p)] for p in combinations(sorted(t), 2)] for t in triples}
    covered = [0] * 5
    order = sorted(triples, key=sorted)

    def rec(i: int) -> bool:
        if i == len(order):
            return True
        t = order[i]
        mask = 0
        for pi in tp[t]:
            mask |= 1 << pi
        used = max((c for c in range(5) if covered[c]), default=-1)
        for colour in range(min(used + 2, 5)):
            if covered[colour] & mask:
                continue
            covered[colour] |= mask
            if rec(i + 1):
                return True
            covered[colour] &= ~mask
        return False

    return rec(0)


# --------------------------------------------------------------- section 5
# The m=17 tower table and the route delimiter.


def f2_rank_incidence(n: int) -> int:
    """F_2 rank of the vertex-edge incidence matrix of K_n (= n-1 for n >= 1)."""
    rank, pivots = 0, []
    for a, b in combinations(range(n), 2):
        c = (1 << a) | (1 << b)
        for piv in pivots:
            c = min(c, c ^ piv)
        if c:
            pivots.append(c)
            pivots.sort(reverse=True)
            rank += 1
    return rank


def section_tower() -> None:
    rows = []
    for t in range(1, 16):
        v = t + 17
        ce, pe = invariance_exponents(v, t)
        rows.append((t, v, ce == 0 and pe == 0))
    check(
        "m=17 tower: E_t is a genuine isomorphism invariant exactly for odd t",
        all(inv == (t % 2 == 1) for t, _v, inv in rows),
    )
    check(
        "the odd-t characterization is scoped to t<=15 (E_18 at v=35 is also invariant)",
        invariance_exponents(35, 18) == (0, 0),
    )
    check(
        "m=17 tower: E_3 (the LS(3,4,20) rung) is a genuine isomorphism invariant",
        invariance_exponents(20, 3) == (0, 0),
    )
    check(
        "m=17 tower: E_15 (the k=16 target rung) is a genuine isomorphism invariant",
        invariance_exponents(32, 15) == (0, 0),
    )
    # Arithmetic behind Corollary D and the delimiter.
    check(
        "rung 2 of the m=17 tower has an odd number of points (19)", (2 + 17) % 2 == 1
    )
    check("rung 2 of the m=5 tower has an odd number of points (7)", (2 + 5) % 2 == 1)
    # class sizes quoted in NOTE.md
    check(
        "LS(3,4,20): 4845 quadruples, 17 classes of 285",
        comb(20, 4) == 4845 and comb(20, 3) // 4 == 285 and 17 * 285 == 4845,
    )
    check(
        "LS(3,4,16): 1820 quadruples, 13 classes of 140",
        comb(16, 4) == 1820 and comb(16, 3) // 4 == 140 and 13 * 140 == 1820,
    )
    check(
        "G1 form of LS(3,4,20) is J(19,4) with 17 colours, classes of 228",
        comb(19, 4) == 3876 and 3876 % 17 == 0 and 3876 // 17 == 228,
    )
    check(
        "G1 form of LS(3,4,16) is J(15,4) with 13 colours, classes of 105",
        comb(15, 4) == 1365 and 1365 % 13 == 0 and 1365 // 13 == 105,
    )
    # Theorem 4: exact codimension of the joint condition on the pair links.
    check(
        "Theorem 4 on LS(3,4,20): 190 pair links, cycle space of K_20 has dim 171",
        comb(20, 2) == 190 and f2_rank_incidence(20) == 19 and 190 - 19 == 171,
    )
    check(
        "Theorem 4 at k=16: exact equation and fourteen-subset sign counts",
        comb(32, 13) == 347_373_600 and comb(32, 14) == 471_435_600 and 32 - 13 == 19,
    )
    check(
        "Theorem 4 at k=16: exact rank, kernel, and equivalent even-graph counts",
        comb(31, 13) == 206_253_075
        and comb(32, 14) - comb(31, 13) == 265_182_525
        and comb(32, 12) == 225_792_840,
    )


def section_holonomy() -> None:
    """Theorem 7: the non-abelian successor to the star sign."""
    from holonomy import check_identity, holonomy_census  # noqa: PLC0415

    ls9 = build_ls239()
    ok9, _ = check_identity(ls9, list(range(9)), t=2, m=7)
    check("Theorem 7 holonomy identity holds on LS(2,3,9)", ok9)
    cen9 = holonomy_census(ls9, list(range(9)), 2, 7)
    check("LS(2,3,9): 9*C(8,2) = 252 holonomy pairs", sum(cen9.values()) == 252)
    check(
        "LS(2,3,9): exact four-type holonomy census",
        dict(cen9)
        == {
            (2, 2, 2, 1): 56,
            (3, 3, 1): 28,
            (6, 1): 84,
            (4, 2, 1): 84,
        },
    )

    sys.path.insert(0, str(REPO))
    from evidence.verify_defect_cross_link_lsts19 import (  # noqa: PLC0415
        construct_lsts19,
        verify_large_set,
    )

    raw = construct_lsts19()
    verify_large_set(raw)
    ls19 = {frozenset(t): c for t, c in raw.items()}
    ok19, _ = check_identity(ls19, list(range(19)), t=2, m=17)
    check("Theorem 7 holonomy identity holds on the cyclic LS(2,3,19)", ok19)
    cen19 = holonomy_census(ls19, list(range(19)), 2, 17)
    check("LS(2,3,19): 19*C(18,2) = 2907 holonomy pairs", sum(cen19.values()) == 2907)
    check(
        "LS(2,3,19): 34 distinct holonomy cycle types occur, so the layer is"
        " strictly finer than the sign",
        len(cen19) == 34,
    )
    check(
        "every holonomy permutation fixes at least one colour",
        all(k[-1] == 1 for k in cen19) and all(k[-1] == 1 for k in cen9),
    )
    # Fixed-point cycle types of S_17 are in bijection with partitions of 16.
    parts = [0] * 17
    parts[0] = 1
    for summand in range(1, 17):
        for total in range(summand, 17):
            parts[total] += parts[total - summand]
    check(
        "there are p(16)=231 possible fixed-point holonomy cycle types",
        parts[16] == 231,
    )


def main() -> None:
    if not __debug__:
        raise SystemExit("do not run this verifier with python -O")
    section_restriction_lemma()
    section_holonomy()
    section_commutator()
    section_definition()
    section_census()
    section_identity()
    section_exclusion()
    section_tower()
    failed = [n for n, ok in CHECKS if not ok]
    print()
    print(f"{len(CHECKS) - len(failed)}/{len(CHECKS)} checks passed")
    if failed:
        for n in failed:
            print("  FAILED:", n)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
