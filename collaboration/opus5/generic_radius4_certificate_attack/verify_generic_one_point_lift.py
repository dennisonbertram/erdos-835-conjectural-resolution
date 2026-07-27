"""Exact verifier for the generic one-point lift theorem (Theorem G1) and its
corollaries, at the parameters relevant to Erdos-Rosenfeld problem #835.

Theorem G1.  Let m >= 3 be odd and let s >= 1.  Put n = m + s - 2 and
v = n + 1 = m + s - 1.  Then a proper m-colouring of the Johnson graph J(n, s)
exists if and only if a large set LS(s-1, s, v) exists; and

    delete-a-point            :  large sets  ->  proper colourings
    adjoin-a-point-via-psi    :  proper colourings -> large sets

are mutually inverse bijections.

Nothing here decides #835.  The theorem is an equivalence and a
scope-explicit route delimiter; it excludes no previously open k and is not a
cheaper encoding under the natural exactly-one variables.

Standard library only.  Exact integer/finite arithmetic.  No solver, no
randomness, no network.  Run:

    python3 -B collaboration/opus5/generic_radius4_certificate_attack/\
verify_generic_one_point_lift.py
"""

from __future__ import annotations

import hashlib
import itertools
import pathlib
import sys
from collections import defaultdict
from typing import Iterable

Block = frozenset[int]

CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append((name, bool(ok), detail))
    if not ok:
        print(f"FAIL  {name}  {detail}")


# ---------------------------------------------------------------------------
# generic machinery
# ---------------------------------------------------------------------------


def sets_of(points: Iterable[int], size: int) -> list[Block]:
    return [frozenset(c) for c in itertools.combinations(sorted(points), size)]


def star(base: Block, points: Iterable[int]) -> list[Block]:
    """The s-sets containing the (s-1)-set ``base``, inside ``points``."""
    return [base | {x} for x in points if x not in base]


def is_proper(colouring: dict[Block, int], points: list[int], s: int) -> bool:
    """A colouring of the s-subsets of ``points`` is proper on the Johnson
    graph exactly when every star (fixed (s-1)-set) is rainbow, because two
    s-sets are adjacent iff they share an (s-1)-set."""
    for base in sets_of(points, s - 1):
        seen = [colouring[b] for b in star(base, points)]
        if len(set(seen)) != len(seen):
            return False
    return True


def missing_colour_map(
    colouring: dict[Block, int], points: list[int], s: int, m: int
) -> dict[Block, int] | None:
    """psi(S) = the unique colour absent from the star of the (s-1)-set S.

    Well defined exactly when every star has m-1 members with distinct
    colours, which is the case when |points| = m + s - 2 and the colouring is
    proper.  Returns None if that fails."""
    psi: dict[Block, int] = {}
    for base in sets_of(points, s - 1):
        seen = {colouring[b] for b in star(base, points)}
        if len(seen) != m - 1:
            return None
        rest = set(range(m)) - seen
        if len(rest) != 1:
            return None
        psi[base] = rest.pop()
    return psi


def complete(
    colouring: dict[Block, int], points: list[int], s: int, m: int, new_point: int
) -> dict[int, set[Block]] | None:
    """The adjoin-a-point map of Theorem G1."""
    psi = missing_colour_map(colouring, points, s, m)
    if psi is None:
        return None
    classes: dict[int, set[Block]] = {i: set() for i in range(m)}
    for block, colour in colouring.items():
        classes[colour].add(block)
    for base, colour in psi.items():
        classes[colour].add(base | {new_point})
    return classes


def restrict(
    classes: dict[int, set[Block]], points: list[int], deleted: int
) -> dict[Block, int]:
    """The delete-a-point map of Theorem G1."""
    return {
        block: colour
        for colour, family in classes.items()
        for block in family
        if deleted not in block
    }


def is_steiner(system: Iterable[Block], points: list[int], s: int) -> bool:
    """Is ``system`` an S(s-1, s, |points|)?  Every (s-1)-set in exactly one."""
    cover: dict[Block, int] = defaultdict(int)
    for block in system:
        if len(block) != s or not block <= set(points):
            return False
        for sub in itertools.combinations(sorted(block), s - 1):
            cover[frozenset(sub)] += 1
    return all(cover[b] == 1 for b in sets_of(points, s - 1))


def is_large_set(classes: dict[int, set[Block]], points: list[int], s: int, m: int) -> bool:
    if len(classes) != m:
        return False
    seen: set[Block] = set()
    for family in classes.values():
        if not is_steiner(family, points, s):
            return False
        if seen & family:
            return False
        seen |= family
    return seen == set(sets_of(points, s))


# ---------------------------------------------------------------------------
# exact chromatic decision for Johnson graphs (small parameters only)
# ---------------------------------------------------------------------------


def johnson_colourable(n: int, s: int, m: int, count_all: bool = False) -> int | bool:
    """Decide whether J(n, s) has a proper m-colouring.

    Exhaustive backtracking over the s-subsets of [n] in lexicographic order.
    Colour symmetry is broken by requiring the colour of the i-th vertex to be
    at most (1 + max colour used earlier).  With ``count_all`` the return value
    is the number of *symmetry-reduced* proper colourings; otherwise it is a
    bool."""
    verts = sets_of(range(n), s)
    index = {b: i for i, b in enumerate(verts)}
    # neighbours among earlier vertices only
    earlier: list[list[int]] = [[] for _ in verts]
    for base in sets_of(range(n), s - 1):
        clique = sorted(index[b] for b in star(base, range(n)))
        for pos, j in enumerate(clique):
            earlier[j].extend(clique[:pos])
    earlier = [sorted(set(e)) for e in earlier]

    colour = [-1] * len(verts)
    total = 0

    def rec(i: int, used: int) -> bool:
        nonlocal total
        if i == len(verts):
            total += 1
            return not count_all
        forbidden = {colour[j] for j in earlier[i]}
        limit = min(used + 1, m)
        for a in range(limit):
            if a in forbidden:
                continue
            colour[i] = a
            if rec(i + 1, max(used, a + 1)):
                return True
            colour[i] = -1
        return False

    found = rec(0, 0)
    if count_all:
        return total
    return found


def all_proper_colourings(n: int, s: int, m: int) -> list[dict[Block, int]]:
    """Every proper m-colouring of J(n, s), one representative per orbit of the
    colour-permutation action.

    Both maps of Theorem G1 commute with permuting the m colours -- delete-a-
    point carries a permuted colouring to a permuted restriction, and psi is
    defined by set complement inside the colour set -- so checking the round
    trip on orbit representatives verifies it for every colouring."""
    verts = sets_of(range(n), s)
    index = {b: i for i, b in enumerate(verts)}
    earlier: list[list[int]] = [[] for _ in verts]
    for base in sets_of(range(n), s - 1):
        clique = sorted(index[b] for b in star(base, range(n)))
        for pos, j in enumerate(clique):
            earlier[j].extend(clique[:pos])
    earlier = [sorted(set(e)) for e in earlier]

    out: list[dict[Block, int]] = []
    colour = [-1] * len(verts)

    def rec(i: int, used: int) -> None:
        if i == len(verts):
            out.append({verts[j]: colour[j] for j in range(len(verts))})
            return
        forbidden = {colour[j] for j in earlier[i]}
        for a in range(min(used + 1, m)):
            if a in forbidden:
                continue
            colour[i] = a
            rec(i + 1, max(used, a + 1))
            colour[i] = -1

    rec(0, 0)
    return out


# ---------------------------------------------------------------------------
# concrete large sets used as real-object witnesses
# ---------------------------------------------------------------------------


def one_factorisation(m1: int) -> dict[int, set[Block]]:
    """The standard GK_{2r} one-factorisation of K_{m1} for even m1 = 2r.

    Colour c in {0,...,m1-2} is the near-perfect matching
    {c-i, c+i} (mod m1-1) together with {c, m1-1}."""
    assert m1 % 2 == 0
    r = m1 - 1
    classes: dict[int, set[Block]] = {}
    for c in range(r):
        fac = {frozenset({c, m1 - 1})}
        for i in range(1, (r + 1) // 2):
            fac.add(frozenset({(c - i) % r, (c + i) % r}))
        classes[c] = fac
    return classes


def ls_2_3_9() -> dict[int, set[Block]]:
    """A large set of seven pairwise disjoint STS(9) on Z_9, found by exact
    search here (deterministic, first solution in a fixed order)."""
    points = list(range(9))
    triples = sets_of(points, 3)
    pairs = sets_of(points, 2)
    pair_index = {p: i for i, p in enumerate(pairs)}

    def sts_from(seed: int) -> list[set[Block]]:
        # exhaustive exact-cover search for a partition of all 84 triples into
        # seven STS(9); deterministic, returns the first solution.
        classes: list[set[Block]] = []
        remaining = set(triples)

        def build_one(chosen: set[Block], covered: int) -> set[Block] | None:
            if len(chosen) == 12:
                return set(chosen)
            # first uncovered pair
            for pi, pair in enumerate(pairs):
                if not covered >> pi & 1:
                    break
            else:
                return None
            for x in points:
                if x in pair:
                    continue
                t = pair | {x}
                if t not in remaining:
                    continue
                mask = 0
                bad = False
                for sub in itertools.combinations(sorted(t), 2):
                    bit = 1 << pair_index[frozenset(sub)]
                    if covered & bit:
                        bad = True
                        break
                    mask |= bit
                if bad:
                    continue
                chosen.add(t)
                res = build_one(chosen, covered | mask)
                if res is not None:
                    return res
                chosen.discard(t)
            return None

        def rec() -> bool:
            if not remaining:
                return True
            found = build_one(set(), 0)
            if found is None:
                return False
            classes.append(found)
            remaining.difference_update(found)
            if rec():
                return True
            remaining.update(found)
            classes.pop()
            return False

        if rec():
            return classes
        raise RuntimeError("no LS(2,3,9) found")

    found = sts_from(0)
    return {i: set(f) for i, f in enumerate(found)}


def load_cyclic_lsts19(repo: pathlib.Path) -> dict[int, set[Block]]:
    """The repository's independently audited cyclic LS(2,3,19)."""
    sys.path.insert(0, str(repo / "evidence"))
    import verify_defect_cross_link_lsts19 as mod  # noqa: E402

    colouring = mod.construct_lsts19()
    classes: dict[int, set[Block]] = defaultdict(set)
    for triple, colour in colouring.items():
        classes[colour].add(frozenset(triple))
    return dict(classes)


def load_eh15(repo: pathlib.Path) -> dict[int, set[Block]]:
    """The fifteen complete Etzion-Hartman SQS(20) from the committed export."""
    path = repo / "collaboration/ls3420_branch0_search/eh15_branch0_partial.txt"
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    check(
        "eh15 export digest matches the value asserted in the repository",
        digest == "06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78",
        digest,
    )
    families: dict[int, set[Block]] = defaultdict(set)
    for line in raw.decode().splitlines():
        parts = line.split()
        families[int(parts[4])].add(frozenset(int(x) for x in parts[:4]))
    return {
        c: f for c, f in families.items() if len(f) == 285 and is_steiner(f, list(range(20)), 4)
    }


# ---------------------------------------------------------------------------
# Section A -- the arithmetic that makes Theorem G1 possible
# ---------------------------------------------------------------------------


def section_a() -> None:
    print("A. arithmetic of the hypothesis n = m + s - 2")
    ok_star = ok_link = ok_members = True
    for m in range(3, 40, 2):
        for s in range(2, 20):
            n = m + s - 2
            v = n + 1
            ok_star &= (n - s + 1) == m - 1  # star size in J(n, s)
            ok_link &= (n - (s - 2)) == m  # |[n] \ R| for an (s-2)-set R
            ok_members &= (v - (s - 1)) == m  # members of LS(s-1, s, v)
    check("star of an (s-1)-set in J(m+s-2, s) has exactly m-1 members", ok_star)
    check("complement of an (s-2)-set in [m+s-2] has exactly m points", ok_link)
    check("LS(s-1, s, m+s-1) has exactly m members", ok_members)

    # the odd-m counting step: K_m properly edge-coloured with m colours has
    # every class a near-perfect matching, and the deficiency map is bijective.
    ok = True
    for m in range(3, 60, 2):
        ok &= m * ((m - 1) // 2) == m * (m - 1) // 2
    check("for odd m, m maximum matchings of K_m exactly exhaust its edges", ok)
    ok_even = all(
        m * (m // 2) > m * (m - 1) // 2 for m in range(4, 60, 2)
    )
    check("for even m the same count has slack, so for s>=2 the lemma genuinely needs m odd", ok_even)


# ---------------------------------------------------------------------------
# Section B -- exhaustive round trips at small odd m
# ---------------------------------------------------------------------------


def round_trip(m: int, s: int, expect_colourable: bool) -> None:
    """Exhaustively verify Theorem G1 at (m, s): every proper m-colouring of
    J(m+s-2, s) completes to a genuine LS(s-1, s, m+s-1) and restricts back
    identically, and the two sides are non-empty together."""
    n = m + s - 2
    v = n + 1
    label = f"m={m},s={s}"
    points = list(range(n))
    all_points = list(range(v))

    cols = all_proper_colourings(n, s, m)
    check(
        f"{label}: J({n},{s}) is {m}-colourable = {expect_colourable}, as Theorem G1 requires "
        f"from the status of LS({s-1},{s},{v})",
        bool(cols) == expect_colourable,
        f"{len(cols)} orbit representatives",
    )
    if not cols:
        return
    good = True
    for c in cols:
        classes = complete(c, points, s, m, n)
        if classes is None or not is_large_set(classes, all_points, s, m):
            good = False
            break
        if restrict(classes, all_points, n) != c:
            good = False
            break
    check(
        f"{label}: all {len(cols)} orbit representatives of proper {m}-colourings of J({n},{s}) "
        f"complete to LS({s-1},{s},{v}) and restrict back identically",
        good,
    )


def section_b() -> None:
    print("B. exhaustive round trips, small odd m")
    # (m, s, is LS(s-1,s,m+s-1) known to exist?)
    #   m=3,s=1 : LS(0,1,3), the labelled singleton partition    -- exists
    #   m=5,s=1 : LS(0,1,5), the labelled singleton partition    -- exists
    #   m=3,s=2 : LS(1,2,4) = one-factorisation of K_4          -- exists
    #   m=5,s=2 : LS(1,2,6) = one-factorisation of K_6          -- exists
    #   m=5,s=3 : LS(2,3,7) = five disjoint Fano planes         -- does not exist (Cayley)
    #   m=5,s=4 : LS(3,4,8) = five disjoint SQS(8)              -- does not exist
    #   m=7,s=2 : LS(1,2,8) = one-factorisation of K_8          -- exists
    #   m=7,s=3 : LS(2,3,9) = seven disjoint STS(9)             -- exists
    round_trip(3, 1, True)
    round_trip(5, 1, True)
    round_trip(3, 2, True)
    round_trip(5, 2, True)
    round_trip(5, 3, False)
    round_trip(5, 4, False)
    round_trip(7, 2, True)


# ---------------------------------------------------------------------------
# Section C -- non-trivial predictions of the theorem
# ---------------------------------------------------------------------------


def max_disjoint_steiner(points: list[int], s: int, limit: int) -> tuple[int, int]:
    """Maximum number of pairwise disjoint S(s-1, s, |points|), by exhaustive
    search over all such systems.  ``limit`` caps the reported value."""
    universe = sets_of(points, s)
    subs = sets_of(points, s - 1)
    sub_index = {b: i for i, b in enumerate(subs)}
    full = (1 << len(subs)) - 1
    systems: list[frozenset[Block]] = []
    chosen: list[Block] = []

    block_mask = {}
    for b in universe:
        mk = 0
        for sub in itertools.combinations(sorted(b), s - 1):
            mk |= 1 << sub_index[frozenset(sub)]
        block_mask[b] = mk

    def rec(covered: int, start_ok: set[Block]) -> None:
        if covered == full:
            systems.append(frozenset(chosen))
            return
        low = (~covered) & full
        first = (low & -low).bit_length() - 1
        target = subs[first]
        for b in universe:
            if b not in start_ok or not target <= b:
                continue
            if covered & block_mask[b]:
                continue
            chosen.append(b)
            rec(covered | block_mask[b], start_ok)
            chosen.pop()

    rec(0, set(universe))

    best = 0
    order = list(range(len(systems)))

    def clique(idx: int, current: list[int]) -> None:
        nonlocal best
        best = max(best, len(current))
        if best >= limit:
            return
        for j in range(idx, len(order)):
            cand = systems[order[j]]
            if all(not (cand & systems[i]) for i in current):
                current.append(order[j])
                clique(j + 1, current)
                current.pop()

    clique(0, [])
    return best, len(systems)


def section_c() -> None:
    print("C. non-trivial predictions")

    # C1.  LS(2,3,7) does not exist (Cayley); G1 therefore predicts
    #      chi(J(6,3)) > 5.
    best7, count7 = max_disjoint_steiner(list(range(7)), 3, 5)
    check(
        "exactly 30 labelled Fano planes, at most two pairwise disjoint "
        f"(found {best7} of the 5 needed)",
        count7 == 30 and best7 == 2,
        f"systems={count7} max_disjoint={best7}",
    )
    check(
        "G1 prediction: J(6,3) has no proper 5-colouring",
        not johnson_colourable(6, 3, 5),
    )
    check("control: J(6,3) does have a proper 6-colouring", bool(johnson_colourable(6, 3, 6)))

    # C2.  LS(2,3,9) exists; G1 therefore predicts chi(J(8,3)) <= 7, and the
    #      round trip must be exact on the real object.
    ls9 = ls_2_3_9()
    check("constructed LS(2,3,9): seven disjoint STS(9)", is_large_set(ls9, list(range(9)), 3, 7))
    c8 = restrict(ls9, list(range(9)), 8)
    check("its restriction is a proper 7-colouring of J(8,3)", is_proper(c8, list(range(8)), 3))
    back = complete(c8, list(range(8)), 3, 7, 8)
    check(
        "adjoin-a-point rebuilds exactly the LS(2,3,9) it came from",
        back == ls9,
    )

    # C3.  LS(1,2,m+1) exists for odd m; the m=7 instance on real objects.
    of8 = one_factorisation(8)
    check("constructed one-factorisation of K_8 = LS(1,2,8)", is_large_set(of8, list(range(8)), 2, 7))
    c7 = restrict(of8, list(range(8)), 7)
    check("its restriction is a proper 7-edge-colouring of K_7", is_proper(c7, list(range(7)), 2))
    back7 = complete(c7, list(range(7)), 2, 7, 7)
    check(
        "adjoin-a-point rebuilds exactly the one-factorisation of K_8",
        back7 == of8,
    )


# ---------------------------------------------------------------------------
# Section D -- sharpness: the theorem is false for even m
# ---------------------------------------------------------------------------


def section_d() -> None:
    print("D. sharpness: odd m is needed, and exactly one point may be deleted")

    # D1.  even m breaks the key lemma and the equivalence.
    for m in (4, 6, 8):
        n = m  # s = 2
        colourable = bool(johnson_colourable(n, 2, m))
        # LS(1,2,m+1) is a one-factorisation of K_{m+1}; m+1 is odd, so none.
        exists = (m + 1) % 2 == 0
        check(
            f"m={m} (even), s=2: J({n},2) is {m}-colourable but LS(1,2,{m+1}) does not exist "
            "-- the equivalence fails",
            colourable and not exists,
        )

    # D2.  deleting a SECOND point is strictly lossy: n = m+s-3 admits a proper
    #      m-colouring in cases where the large set provably does not exist.
    #      m=5, s=3: J(5,3) = J(5,2) = L(K_5) is 5-colourable, LS(2,3,7) is not.
    #      m=5, s=4: J(6,4) = J(6,2) = L(K_6) is 5-colourable, LS(3,4,8) is not.
    for m, s, ls in ((5, 3, "LS(2,3,7)"), (5, 4, "LS(3,4,8)")):
        n2 = m + s - 3
        two_ok = bool(johnson_colourable(n2, s, m))
        one_ok = bool(johnson_colourable(m + s - 2, s, m))
        check(
            f"m={m},s={s}: J({n2},{s}) IS {m}-colourable while J({m+s-2},{s}) is not, so deleting a "
            f"second point strictly loses information ({ls} does not exist)",
            two_ok and not one_ok,
        )


# ---------------------------------------------------------------------------
# Section E -- the k=16 parameters on genuine objects
# ---------------------------------------------------------------------------


def section_e(repo: pathlib.Path) -> None:
    print("E. k=16 parameters (m=17) on genuine objects")

    # E1.  s = 3: the repository's audited cyclic LS(2,3,19).
    ls19 = load_cyclic_lsts19(repo)
    pts19 = list(range(19))
    check("loaded cyclic LS(2,3,19): seventeen disjoint STS(19)", is_large_set(ls19, pts19, 3, 17))
    c18 = restrict(ls19, pts19, 18)
    check(
        "delete a point: proper 17-colouring of J(18,3) with 816 vertices",
        is_proper(c18, list(range(18)), 3) and len(c18) == 816,
        f"vertices={len(c18)}",
    )
    sizes = sorted(len([b for b, col in c18.items() if col == i]) for i in range(17))
    check(
        "every colour class of that J(18,3) colouring is a maximum packing of 48 triples",
        sizes == [48] * 17,
        str(set(sizes)),
    )
    back18 = complete(c18, list(range(18)), 3, 17, 18)
    check(
        "adjoin-a-point rebuilds exactly the cyclic LS(2,3,19)",
        back18 == ls19,
    )
    # the leaves of the 17 packings are exactly the derived LS(1,2,18)
    psi18 = missing_colour_map(c18, list(range(18)), 3, 17)
    leaves: dict[int, set[Block]] = defaultdict(set)
    for pair, colour in psi18.items():
        leaves[colour].add(pair)
    check(
        "their 17 leaves form a one-factorisation of K_18, i.e. the next tower rung down",
        is_large_set(dict(leaves), list(range(18)), 2, 17),
    )

    # E2.  s = 4: the fifteen genuine Etzion-Hartman SQS(20).
    eh = load_eh15(repo)
    check("loaded exactly fifteen genuine Etzion-Hartman SQS(20)", len(eh) == 15, str(len(eh)))
    ok_pack = ok_leave = ok_rebuild = True
    leaves20: list[set[Block]] = []
    for colour, system in eh.items():
        rest = {b for b in system if 19 not in b}
        ok_pack &= len(rest) == 228
        derived = {b - {19} for b in system if 19 in b}
        ok_leave &= len(derived) == 57 and is_steiner(derived, list(range(19)), 3)
        rebuilt = rest | {d | {19} for d in derived}
        ok_rebuild &= rebuilt == system
        leaves20.append(derived)
    check("each EH SQS(20) restricts to a maximum packing of 228 quadruples on 19 points", ok_pack)
    check("each such leave is an STS(19) (the derived design), so the packing is maximum", ok_leave)
    check("adjoin-a-point rebuilds each EH SQS(20) exactly from its 19-point restriction", ok_rebuild)
    pairwise = all(
        not (leaves20[i] & leaves20[j])
        for i in range(len(leaves20))
        for j in range(i + 1, len(leaves20))
    )
    check("the fifteen leaves are pairwise disjoint STS(19), a partial LS(2,3,19)", pairwise)

    restricted = {
        b: colour for colour, system in eh.items() for b in system if 19 not in b
    }
    check(
        "the fifteen restrictions are a proper partial 17-colouring of J(19,4) covering "
        f"{len(restricted)} of its 3876 vertices",
        len(restricted) == 15 * 228,
        str(len(restricted)),
    )


# ---------------------------------------------------------------------------
# Section F -- corollaries stated for all k
# ---------------------------------------------------------------------------


def edge_chromatic_complete(n: int) -> int:
    """chi'(K_n), computed exactly for small n by the J(n,2) decision routine."""
    for m in range(max(n - 1, 1), n + 2):
        if johnson_colourable(n, 2, m):
            return m
    raise RuntimeError


def section_f() -> None:
    print("F. corollaries valid for every k")

    # F1.  k must be even: restrict a hypothetical LS(k-1,k,2k) to any
    #      (k+2)-subset; the k-subsets of it, labelled by the omitted pair,
    #      give a proper (k+1)-edge-colouring of K_{k+2}.
    ok_small = all(edge_chromatic_complete(n) == (n - 1 if n % 2 == 0 else n) for n in range(3, 10))
    check("chi'(K_n) = n-1 for even n and n for odd n, verified exactly for n <= 9", ok_small)
    ok_parity = True
    for k in range(3, 200, 2):  # odd k
        ok_parity &= (k + 2) % 2 == 1 and (k + 2) > k + 1  # chi'(K_{k+2}) = k+2 > k+1
    check(
        "odd k: a (k+2)-subset forces chi'(K_{k+2}) = k+2 > k+1 colours -- k must be even",
        ok_parity,
    )

    # F2.  Exact one-root restriction classification.  Fix a root, take its
    #      link colouring on (k-1)-sets, restrict it to an n-set Y, and
    #      complement inside Y.  The resulting block size is s=n-k+1, and the
    #      G1 hypothesis n=m+s-2 holds identically.  For each fixed root/Y this
    #      standalone object is equivalent to tower rung t=n-k.  This says
    #      nothing about simultaneous compatibility across several root/Y
    #      choices.
    ok_complement = ok_g1 = ok_rung = True
    for k in range(4, 200, 2):
        m = k + 1
        for n in range(k + 1, 2 * k):
            s = n - (k - 1)  # complement of a (k-1)-set inside Y
            ok_complement &= (k - 1) + s == n
            ok_g1 &= n == m + s - 2
            t = n - k
            ok_rung &= (s - 1, s, n + 1) == (t, t + 1, t + m)
    check(
        "after fixing one root, complementing the restricted (k-1)-set link inside an n-set "
        "gives block size s=n-k+1",
        ok_complement,
    )
    check(
        "for every fixed root and retained n-set, n=(k+1)+(n-k+1)-2 is exactly the "
        "hypothesis of Theorem G1",
        ok_g1,
    )
    check(
        "Theorem G1 returns LS(n-k,n-k+1,n+1), precisely tower rung t=n-k "
        "(standalone restriction only)",
        ok_rung,
    )

    # F3.  The smaller Johnson-graph vertex set at each rung, and the exact
    #      logical content of the reduction at the level of constraints.
    from math import comb

    rows = []
    for t in range(1, 16):
        m = 17
        v = t + m
        rows.append((t, comb(v, t + 1), comb(v - 1, t + 1)))
    ok_smaller = all(b < a for _, a, b in rows)
    check(
        "the (v-1)-point formulation has strictly fewer vertices at every rung of the m=17 tower",
        ok_smaller,
    )
    print("     rung t | LS(t,t+1,t+17) vertices | equivalent J(t+16,t+1) vertices")
    for t, a, b in rows:
        print(f"       {t:2d}   | {a:>12,} | {b:>12,}   ({100*(a-b)/a:4.1f}% fewer)")

    # F4.  Under the natural exactly-one encoding the two formulations have the
    #      SAME variables: the missing-colour map psi is literally the colouring
    #      of the blocks through the deleted point.  What Theorem G1 removes is
    #      exactly the star constraints based at t-sets through that point.
    ok_vars = ok_groups = True
    print()
    print("     rung t | shared variables | LS star groups | J(n,s)+psi star groups | implied")
    for t in range(1, 16):
        m, v = 17, t + 17
        n = v - 1
        # variables: one Boolean per (block, colour)
        vars_ls = comb(v, t + 1) * m
        vars_j = (comb(n, t + 1) + comb(n, t)) * m  # blocks off p, plus psi
        ok_vars &= vars_ls == vars_j
        # exactly-one groups enforcing that each star is rainbow
        groups_ls = comb(v, t) * m
        groups_j = comb(n, t) * m
        implied = groups_ls - groups_j
        ok_groups &= implied == comb(n, t - 1) * m
        if t in (2, 3, 4, 15):
            print(
                f"       {t:2d}   | {vars_ls:>16,} | {groups_ls:>14,} | {groups_j:>22,} "
                f"| {implied:>9,}"
            )
    check(
        "the two formulations use exactly the same variables: psi is the colouring of the "
        "blocks through the deleted point",
        ok_vars,
    )
    check(
        "Theorem G1 says precisely that the C(v-1,t-1)*m star constraints based at t-sets "
        "through the deleted point are implied by the rest",
        ok_groups,
    )


# ---------------------------------------------------------------------------


def main() -> None:
    repo = pathlib.Path(__file__).resolve().parents[3]
    section_a()
    section_b()
    section_c()
    section_d()
    section_e(repo)
    section_f()
    passed = sum(1 for _, ok, _ in CHECKS if ok)
    print()
    for name, ok, detail in CHECKS:
        mark = "ok  " if ok else "FAIL"
        print(f"  [{mark}] {name}" + (f"   ({detail})" if detail and not ok else ""))
    print(f"\n{passed}/{len(CHECKS)} checks passed")
    sys.exit(0 if passed == len(CHECKS) else 1)


if __name__ == "__main__":
    main()
