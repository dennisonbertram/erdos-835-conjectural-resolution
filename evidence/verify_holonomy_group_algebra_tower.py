"""Exact verifier for the group-algebra holonomy tower.

No solver, randomness, or network is used.

Run from the repository root:

    python3 -B evidence/verify_holonomy_group_algebra_tower.py
"""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOLO_DIR = REPO / "collaboration" / "opus5" / "unrestricted_ls3420_attack_2"
sys.path.insert(0, str(HOLO_DIR))
sys.path.insert(0, str(REPO))

from holonomy import cycle_type, derive, holonomy_census, star_map  # noqa: E402
from verify_star_sign import build_ls239  # noqa: E402

from evidence.verify_defect_cross_link_lsts19 import (  # noqa: E402
    construct_lsts19,
    verify_large_set,
)

Permutation = tuple[int, ...]
Colouring = dict[frozenset[int], int]

CHECKS: list[tuple[str, bool]] = []


def check(name: str, condition: bool) -> None:
    CHECKS.append((name, bool(condition)))
    print(("PASS  " if condition else "FAIL  ") + name)
    sys.stdout.flush()


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Composition left o right."""
    return tuple(left[right[x]] for x in range(len(right)))


def inverse(perm: Permutation) -> Permutation:
    out = [0] * len(perm)
    for x, image in enumerate(perm):
        out[image] = x
    return tuple(out)


def local_data(
    colouring: Colouring, ground: list[int], R: frozenset[int]
) -> tuple[list[int], dict[int, dict[int, int]], dict[int, dict[int, int]]]:
    rest = sorted(set(ground) - R)
    chi = {a: star_map(colouring, R | {a}, ground) for a in rest}
    inv = {a: {colour: x for x, colour in chi[a].items()} for a in rest}
    return rest, chi, inv


def sigma(
    colouring: Colouring,
    R: frozenset[int],
    a: int,
    b: int,
    chi: dict[int, dict[int, int]],
    inv: dict[int, dict[int, int]],
    m: int,
) -> Permutation:
    common = colouring[R | {a, b}]
    out: list[int] = []
    for colour in range(m):
        x = inv[a][colour]
        out.append(common if x == b else chi[b][x])
    return tuple(out)


def exact_holonomy_sum(
    colouring: Colouring, ground: list[int], t: int, m: int
) -> Counter[Permutation]:
    """The group-algebra element H(c), represented coefficientwise."""
    total: Counter[Permutation] = Counter()
    for raw_R in combinations(ground, t - 1):
        R = frozenset(raw_R)
        total += local_exact_holonomy_sum(colouring, ground, R, m)
    return total


def local_exact_holonomy_sum(
    colouring: Colouring, ground: list[int], R: frozenset[int], m: int
) -> Counter[Permutation]:
    """The summand H_R(c), retaining one overlap coordinate."""
    total: Counter[Permutation] = Counter()
    rest, chi, inv = local_data(colouring, ground, R)
    for a in rest:
        for b in rest:
            if a != b:
                total[sigma(colouring, R, a, b, chi, inv, m)] += 1
    return total


def check_tower(
    colouring: Colouring, ground: list[int], t: int, m: int
) -> tuple[bool, Counter[Permutation]]:
    top = exact_holonomy_sum(colouring, ground, t, m)
    derived: Counter[Permutation] = Counter()
    for p in ground:
        subground = [x for x in ground if x != p]
        derived += exact_holonomy_sum(derive(colouring, p), subground, t - 1, m)
    scaled = Counter({perm: (t - 1) * count for perm, count in top.items()})
    return derived == scaled, top


def hat_chart(
    colouring: Colouring,
    R: frozenset[int],
    a: int,
    rest: list[int],
    m: int,
) -> Permutation:
    """Tuple indexed by a point's position in rest, with infinity encoded as m."""
    return tuple(m if x == a else colouring[R | {a, x}] for x in rest)


def transition(
    colouring: Colouring,
    R: frozenset[int],
    a: int,
    b: int,
    rest: list[int],
    m: int,
) -> Permutation:
    """hat(chi)_b o hat(chi)_a^{-1} on [m] union {infinity}."""
    chart_a = hat_chart(colouring, R, a, rest, m)
    chart_b = hat_chart(colouring, R, b, rest, m)
    return compose(chart_b, inverse(chart_a))


def transposition(n: int, a: int, b: int) -> Permutation:
    out = list(range(n))
    out[a], out[b] = out[b], out[a]
    return tuple(out)


def check_augmented(
    colouring: Colouring, ground: list[int], t: int, m: int
) -> tuple[bool, bool, bool]:
    cocycle_ok = True
    relation_ok = True
    type_ok = True
    for raw_R in combinations(ground, t - 1):
        R = frozenset(raw_R)
        rest, chi, inv = local_data(colouring, ground, R)
        transitions: dict[tuple[int, int], Permutation] = {}
        for a in rest:
            for b in rest:
                if a == b:
                    continue
                tau = transition(colouring, R, a, b, rest, m)
                transitions[a, b] = tau
                sig = sigma(colouring, R, a, b, chi, inv, m)
                sig_extended = sig + (m,)
                common = colouring[R | {a, b}]
                predicted = compose(transposition(m + 1, m, common), sig_extended)
                relation_ok &= tau == predicted

                sig_type = list(cycle_type(dict(enumerate(sig))))
                tau_type = list(cycle_type(dict(enumerate(tau))))
                sig_type.remove(1)
                tau_type.remove(2)
                type_ok &= sorted(sig_type) == sorted(tau_type)

        for a in rest:
            for b in rest:
                if b == a:
                    continue
                for c in rest:
                    if c == a or c == b:
                        continue
                    cocycle_ok &= (
                        compose(transitions[b, c], transitions[a, b])
                        == transitions[a, c]
                    )
    return cocycle_ok, relation_ok, type_ok


def central_projection(
    exact: Counter[Permutation],
) -> Counter[tuple[int, ...]]:
    out: Counter[tuple[int, ...]] = Counter()
    for perm, count in exact.items():
        out[cycle_type(dict(enumerate(perm)))] += count
    return out


def natural_projection(
    exact: Counter[Permutation],
) -> tuple[tuple[int, ...], ...]:
    """Matrix of the natural permutation representation."""
    m = len(next(iter(exact)))
    matrix = [[0] * m for _ in range(m)]
    for perm, count in exact.items():
        for source, image in enumerate(perm):
            matrix[image][source] += count
    return tuple(tuple(row) for row in matrix)


def partitions(total: int) -> int:
    counts = [0] * (total + 1)
    counts[0] = 1
    for part in range(1, total + 1):
        for value in range(part, total + 1):
            counts[value] += counts[value - part]
    return counts[total]


def round_robin_labels(n: int) -> dict[frozenset[int], int]:
    """A 1-factorization of K_n, with edge labels 0,...,n-2."""
    if n < 2 or n % 2:
        raise ValueError("round-robin construction requires positive even n")
    modulus = n - 1
    fixed = n - 1
    labels: dict[frozenset[int], int] = {}
    for label in range(modulus):
        labels[frozenset({fixed, label})] = label
        for offset in range(1, n // 2):
            edge = frozenset({(label + offset) % modulus, (label - offset) % modulus})
            if edge in labels:
                raise AssertionError("round-robin edge repeated")
            labels[edge] = label
    if len(labels) != n * (n - 1) // 2:
        raise AssertionError("round-robin factorization incomplete")
    return labels


def transported_link_pseudogluing(
    base: Colouring,
) -> tuple[bool, int, int]:
    """Twenty genuine links passing every local-H equality but not gluing.

    Edge labels of a 1-factorization of K_20 identify the nineteen neighbours
    of every point with the nineteen points of one fixed LS(2,3,19).
    """
    points = list(range(20))
    edge_label = round_robin_labels(20)
    links: dict[int, Colouring] = {}
    for p in points:
        ground = [x for x in points if x != p]
        transport = {x: edge_label[frozenset({p, x})] for x in ground}
        if set(transport.values()) != set(range(19)):
            raise AssertionError("incident edge labels are not a bijection")
        links[p] = {
            frozenset(block): base[frozenset(transport[x] for x in block)]
            for block in combinations(ground, 3)
        }

    fingerprints_match = True
    agreements = 0
    disagreements = 0
    for p, q in combinations(points, 2):
        ground_p = [x for x in points if x != p]
        ground_q = [x for x in points if x != q]
        left = local_exact_holonomy_sum(links[p], ground_p, frozenset({q}), 17)
        right = local_exact_holonomy_sum(links[q], ground_q, frozenset({p}), 17)
        fingerprints_match &= left == right

        common = [x for x in points if x not in (p, q)]
        for a, b in combinations(common, 2):
            colour_left = links[p][frozenset({q, a, b})]
            colour_right = links[q][frozenset({p, a, b})]
            if colour_left == colour_right:
                agreements += 1
            else:
                disagreements += 1
    return fingerprints_match, agreements, disagreements


def run_case(
    name: str,
    colouring: Colouring,
    ground: list[int],
    t: int,
    m: int,
    expected_support: int,
    expected_odd: int,
) -> None:
    tower_ok, exact = check_tower(colouring, ground, t, m)
    check(f"{name}: exact group-algebra tower identity", tower_ok)

    unordered = holonomy_census(colouring, ground, t, m)
    projected = central_projection(exact)
    check(
        f"{name}: central projection is twice the unordered cycle census",
        projected == Counter({kind: 2 * count for kind, count in unordered.items()}),
    )
    check(
        f"{name}: every holonomy has exactly one fixed colour",
        all(
            sum(image == source for source, image in enumerate(perm)) == 1
            for perm in exact
        ),
    )

    cocycle_ok, relation_ok, type_ok = check_augmented(colouring, ground, t, m)
    check(f"{name}: augmented transition cocycle", cocycle_ok)
    check(f"{name}: tau = (infinity common-colour) sigma", relation_ok)
    check(f"{name}: sigma/tau cycle-type conversion", type_ok)

    odd = sum(count % 2 for count in exact.values())
    check(
        f"{name}: exact support and odd-coefficient census",
        len(exact) == expected_support and odd == expected_odd,
    )

    exact_local_kinds: Counter[tuple[tuple[Permutation, int], ...]] = Counter()
    central_local_kinds: Counter[tuple[tuple[tuple[int, ...], int], ...]] = Counter()
    natural_flat = True
    for raw_R in combinations(ground, t - 1):
        local = local_exact_holonomy_sum(colouring, ground, frozenset(raw_R), m)
        natural_flat &= natural_projection(local) == tuple(
            (m + 1,) * m for _ in range(m)
        )
        exact_local_kinds[tuple(sorted(local.items()))] += 1
        central_local_kinds[tuple(sorted(central_projection(local).items()))] += 1
    check(f"{name}: every natural local projection is universally flat", natural_flat)
    print(
        f"      exact support={len(exact)}, odd coefficients={odd}, "
        f"oriented summands={sum(exact.values())}\n"
        f"      exact local kinds={len(exact_local_kinds)}, "
        f"central local kinds={len(central_local_kinds)}, "
        f"central-kind multiplicities={sorted(central_local_kinds.values())}"
    )


def main() -> None:
    if not __debug__:
        raise SystemExit("do not run this verifier with python -O")

    ls9 = build_ls239()
    run_case(
        "LS(2,3,9)",
        ls9,
        list(range(9)),
        t=2,
        m=7,
        expected_support=280,
        expected_odd=140,
    )

    raw19 = construct_lsts19()
    verify_large_set(raw19)
    ls19 = {frozenset(block): colour for block, colour in raw19.items()}
    run_case(
        "cyclic LS(2,3,19)",
        ls19,
        list(range(19)),
        t=2,
        m=17,
        expected_support=5814,
        expected_odd=5814,
    )

    fingerprints_match, agreements, disagreements = transported_link_pseudogluing(ls19)
    check(
        "20 transported cyclic links satisfy all 190 exact local-H equalities",
        fingerprints_match,
    )
    check(
        "the same 20 links fail actual overlap consistency",
        agreements == 1592 and disagreements == 27478,
    )
    print(
        f"      pairwise overlap comparisons: agreements={agreements}, "
        f"disagreements={disagreements}"
    )
    check(
        "S_17 holonomy has p(16)-p(15)=55 possible cycle types",
        partitions(16) == 231
        and partitions(15) == 176
        and partitions(16) - partitions(15) == 55,
    )

    passed = sum(ok for _, ok in CHECKS)
    print(f"\n{passed}/{len(CHECKS)} checks passed")
    if passed != len(CHECKS):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
