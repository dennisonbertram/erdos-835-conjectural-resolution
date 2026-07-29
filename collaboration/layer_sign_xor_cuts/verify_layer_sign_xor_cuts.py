#!/usr/bin/env python3
"""Audit the individual layer-sign XOR equations for the Wallis chart.

The reduced fixed-Wallis N model has integer variables N_uv(ij).  For a
colour x, introduce the Boolean indicator

    b[uv,ij,x] = [N_uv(ij) == x].

The parity of the x-layer link-sign product is the quadratic ANF

    q_x = XOR b[uv,ij,x] & b[uv',ij',x],

where the two cells share the flag (i,u), j < j', and v > v'.  This script
computes the exact Wallis targets, audits the hypotheses which make all
seventeen equations logical consequences of the existing reduced N
constraints, and optionally checks a concrete N certificate.

No solver result, and in particular no UNKNOWN result, is used as evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
EVIDENCE = REPO / "evidence"
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from global_latin_audit import construct_golf17  # noqa: E402


K = 16
FINITE = tuple(range(K))
INFINITY = K
COLORS = tuple(range(K + 1))
INDICES = tuple(range(K - 1))
UVS = tuple(combinations(FINITE, 2))
IJS = tuple(combinations(INDICES, 2))
EXPECTED_GOLF_SHA256 = (
    "e419aad73c4275a29702db282ea2378357435b330312bde8fed0c7829be3f857"
)
N_ONLY_SCHEMA = "odd-graph-o16-radius5-fixed-golf-n-forced-trace-v2"
JOINT_SCHEMA = "odd-graph-o16-radius5-fixed-golf-joint-v1"


def sign_sequence(values: list[int]) -> int:
    inversions = sum(
        values[left] > values[right]
        for left in range(len(values))
        for right in range(left + 1, len(values))
    )
    return -1 if inversions & 1 else 1


def sign_map(domain, target, mapping) -> int:
    domain = list(domain)
    target = list(target)
    if set(mapping) != set(domain) or set(mapping.values()) != set(target):
        raise AssertionError("map is not a bijection of the displayed orders")
    position = {value: index for index, value in enumerate(target)}
    return sign_sequence([position[mapping[value]] for value in domain])


def mate(matching: frozenset[frozenset[int]], vertex: int) -> int:
    hits = [edge for edge in matching if vertex in edge]
    if len(hits) != 1:
        raise AssertionError("not a perfect matching at the requested vertex")
    return next(other for other in hits[0] if other != vertex)


def golf_sha256(golf: list[list[list[int]]]) -> str:
    return hashlib.sha256(
        bytes(value for square in golf for row in square for value in row)
    ).hexdigest()


def l_value(golf, index: int, vertex: int) -> int:
    return golf[index][vertex][INFINITY]


def m_value(golf, index: int, u: int, v: int) -> int:
    return golf[index][u][v]


def n_allowed(golf, index: int, u: int, v: int) -> set[int]:
    return set(COLORS) - {
        m_value(golf, index, u, v),
        l_value(golf, index, u),
        l_value(golf, index, v),
    }


def verify_chart(golf) -> None:
    if golf_sha256(golf) != EXPECTED_GOLF_SHA256:
        raise AssertionError("unexpected Wallis chart hash")
    for u in FINITE:
        if {l_value(golf, i, u) for i in INDICES} != set(FINITE) - {u}:
            raise AssertionError("condition 1 fails")
    for i in INDICES:
        if {l_value(golf, i, u) for u in FINITE} != set(FINITE):
            raise AssertionError("L_i is not a permutation")
        for u in FINITE:
            row = {m_value(golf, i, min(u, v), max(u, v)) for v in FINITE if v != u}
            if row != set(COLORS) - {u, l_value(golf, i, u)}:
                raise AssertionError("condition 2 fails")
    for u, v in UVS:
        if {m_value(golf, i, u, v) for i in INDICES} != set(COLORS) - {u, v}:
            raise AssertionError("condition 3 fails")


def one_factorization_sign(factors) -> int:
    """P(Psi): product of the sixteen vertex-row permutation signs."""

    answer = 1
    for u in FINITE:
        answer *= sign_map(
            INDICES,
            [v for v in FINITE if v != u],
            {i: mate(factors[i], u) for i in INDICES},
        )
    return answer


def wallis_targets(golf):
    """Return the seventeen theorem-forced H_x signs and their ingredients."""

    inverse_l = {
        (i, x): next(u for u in FINITE if l_value(golf, i, u) == x)
        for i in INDICES
        for x in FINITE
    }
    lambda_signs = {}
    psi_signs = {}
    factors_by_colour = {}
    source = list(INDICES) + ["*"]
    for x in FINITE:
        mapping = {i: inverse_l[i, x] for i in INDICES}
        mapping["*"] = x
        lambda_signs[x] = sign_map(source, FINITE, mapping)

    for x in COLORS:
        factors = {}
        seen = set()
        for i in INDICES:
            edges = {frozenset((u, v)) for u, v in UVS if m_value(golf, i, u, v) == x}
            if x != INFINITY:
                edges.add(frozenset((x, inverse_l[i, x])))
            factor = frozenset(edges)
            if len(factor) != K // 2:
                raise AssertionError("wrong Psi factor size")
            if {u for edge in factor for u in edge} != set(FINITE):
                raise AssertionError("Psi factor is not perfect")
            if seen & set(factor):
                raise AssertionError("Psi factors overlap")
            seen.update(factor)
            factors[i] = factor
        if seen != {frozenset(edge) for edge in UVS}:
            raise AssertionError("Psi is not a one-factorization")
        factors_by_colour[x] = factors
        psi_signs[x] = one_factorization_sign(factors)

    target_signs = {}
    for x in FINITE:
        target_signs[x] = (
            (-1) ** (x + 1 + (K - 2) // 2) * lambda_signs[x] * psi_signs[x]
        )
    target_signs[INFINITY] = psi_signs[INFINITY]
    target_bits = {x: 0 if target_signs[x] == 1 else 1 for x in COLORS}
    return target_signs, target_bits, lambda_signs, psi_signs, factors_by_colour


def indicator_atom_count_by_colour(golf) -> dict[int, int]:
    counts = {x: 0 for x in COLORS}
    for u, v in UVS:
        for i, j in IJS:
            domain = n_allowed(golf, i, u, v) & n_allowed(golf, j, u, v)
            for x in domain:
                counts[x] += 1
    return counts


def inversion_monomial_count_by_colour(golf) -> dict[int, int]:
    """Count nonzero raw ANF monomials after deleting impossible literals.

    A monomial is selected by a flag (i,u), two increasing source rows
    j<j', and two decreasing target columns v>v'.  The common endpoints i
    and u are uniquely recoverable from the two N variables, so no monomial
    is counted twice.
    """

    counts = {x: 0 for x in COLORS}
    for x in COLORS:
        for i in INDICES:
            others = [j for j in INDICES if j != i]
            for u in FINITE:
                columns = {}
                for j in others:
                    ij = tuple(sorted((i, j)))
                    columns[j] = [
                        v
                        for v in FINITE
                        if v != u
                        and x
                        in (
                            n_allowed(golf, ij[0], min(u, v), max(u, v))
                            & n_allowed(golf, ij[1], min(u, v), max(u, v))
                        )
                    ]
                for left, j in enumerate(others):
                    for jp in others[left + 1 :]:
                        counts[x] += sum(
                            v > vp for v in columns[j] for vp in columns[jp]
                        )
    return counts


def audit_reduced_constraint_implication(golf) -> dict[str, int]:
    """Audit every finite support cap and every dual dummy completion.

    The reduced model contains:
      (D) the 1,800 condition-4 exact-one stars (implemented as domains plus
          AllDifferent(14)); and
      (T) the 1,680 trace AllDifferent(15) stars.

    (T) makes each fixed-(ij,x) class a matching on its prescribed support.
    The support capacities sum to all 120 ground edges, so every capacity is
    attained.  (D) supplies the dual matchings.  The asserted dummy edges
    below fill exactly the holes, which is the no-hole theorem hypothesis.
    """

    inverse_l = {
        (i, x): next(u for u in FINITE if l_value(golf, i, u) == x)
        for i in INDICES
        for x in FINITE
    }
    support_checks = 0
    capacity_sums = 0
    for i, j in IJS:
        capacity = 0
        for x in COLORS:
            support = (
                set(FINITE)
                if x == INFINITY
                else set(FINITE) - {inverse_l[i, x], inverse_l[j, x]}
            )
            expected = K // 2 if x == INFINITY else (K - 2) // 2
            if len(support) != 2 * expected:
                raise AssertionError("wrong trace support capacity")
            # Domain exclusion must forbid x at every edge incident with a
            # deleted support vertex.
            for u, v in UVS:
                domain = n_allowed(golf, i, u, v) & n_allowed(golf, j, u, v)
                if x in domain and not {u, v} <= support:
                    raise AssertionError("domain leaks outside trace support")
            capacity += expected
            support_checks += 1
        if capacity != len(UVS):
            raise AssertionError("trace capacities do not saturate K_16")
        capacity_sums += 1

    dual_checks = 0
    for u, v in UVS:
        for x in COLORS:
            holes = {i for i in INDICES if x not in n_allowed(golf, i, u, v)}
            if x == INFINITY:
                i_m = next(i for i in INDICES if m_value(golf, i, u, v) == x)
                expected_holes = {i_m}
                added = {frozenset((i_m, "*"))}
            elif x == u:
                i_v = next(i for i in INDICES if l_value(golf, i, v) == x)
                expected_holes = {i_v}
                added = {frozenset((i_v, "*"))}
            elif x == v:
                i_u = next(i for i in INDICES if l_value(golf, i, u) == x)
                expected_holes = {i_u}
                added = {frozenset((i_u, "*"))}
            else:
                i_u = next(i for i in INDICES if l_value(golf, i, u) == x)
                i_v = next(i for i in INDICES if l_value(golf, i, v) == x)
                i_m = next(i for i in INDICES if m_value(golf, i, u, v) == x)
                expected_holes = {i_u, i_v, i_m}
                if len(expected_holes) != 3:
                    raise AssertionError("generic dual holes are not distinct")
                added = {
                    frozenset((i_u, i_v)),
                    frozenset((i_m, "*")),
                }
            if holes != expected_holes:
                raise AssertionError("condition-4 palette gives wrong holes")
            if {point for edge in added for point in edge} != holes | {"*"}:
                raise AssertionError("dummy completion does not cover holes")
            dual_checks += 1
    return {
        "trace_support_checks": support_checks,
        "trace_capacity_sums": capacity_sums,
        "dual_dummy_completions": dual_checks,
    }


def decode_n_payload(path: Path, golf):
    payload = json.loads(path.read_text(encoding="utf-8"))
    schema = payload.get("schema")
    if schema not in {N_ONLY_SCHEMA, JOINT_SCHEMA}:
        raise AssertionError("unsupported certificate schema")
    unhashed = dict(payload)
    recorded = unhashed.pop("sha256_without_hash", None)
    expected = hashlib.sha256(
        (json.dumps(unhashed, sort_keys=True, separators=(",", ":")) + "\n").encode(
            "utf-8"
        )
    ).hexdigest()
    if not isinstance(recorded, str) or recorded != expected:
        raise AssertionError("certificate self-hash mismatch")
    if payload.get("golf_sha256") != golf_sha256(golf):
        raise AssertionError("certificate uses a different Wallis chart")
    values = payload.get("n_values")
    if not isinstance(values, list) or len(values) != len(UVS) * len(IJS):
        raise AssertionError("wrong N vector length")
    if any(not isinstance(value, int) or value not in COLORS for value in values):
        raise AssertionError("N value outside the colour range")
    return {
        uv + ij: values[position]
        for position, (uv, ij) in enumerate((uv, ij) for uv in UVS for ij in IJS)
    }


def n_entry(n, u: int, v: int, i: int, j: int) -> int:
    return n[(min(u, v), max(u, v), min(i, j), max(i, j))]


def verify_reduced_n(n, golf) -> None:
    # Domains and condition-4 exact-one stars.
    for u, v in UVS:
        for i, j in IJS:
            if n[u, v, i, j] not in (
                n_allowed(golf, i, u, v) & n_allowed(golf, j, u, v)
            ):
                raise AssertionError("N value outside its reduced domain")
        for i in INDICES:
            values = [n_entry(n, u, v, i, j) for j in INDICES if j != i]
            if len(set(values)) != K - 2:
                raise AssertionError("condition-4 AllDifferent star fails")
            if set(values) != n_allowed(golf, i, u, v):
                raise AssertionError("condition-4 exact palette fails")

    # Forced trace AllDifferent stars.
    for i, j in IJS:
        for u in FINITE:
            values = [n_entry(n, u, v, i, j) for v in FINITE if v != u]
            if len(set(values)) != K - 1:
                raise AssertionError("forced-trace AllDifferent star fails")


def observed_layer_bits(n, golf) -> dict[int, int]:
    """Evaluate the explicit inversion ANF q_x on a concrete N table."""

    parity = {x: 0 for x in COLORS}
    for i in INDICES:
        for u in FINITE:
            fibers = {x: [] for x in COLORS}
            for j in INDICES:
                if j == i:
                    continue
                for v in FINITE:
                    if v == u:
                        continue
                    x = n_entry(n, u, v, i, j)
                    fibers[x].append((j, v))
            for x, cells in fibers.items():
                if x == l_value(golf, i, u):
                    expected = 0
                elif x in {u, INFINITY}:
                    expected = K - 2
                else:
                    expected = K - 3
                if len(cells) != expected:
                    raise AssertionError("partial-fibre size is wrong")
                if len({j for j, _ in cells}) != len(cells):
                    raise AssertionError("partial fibre repeats a source row")
                if len({v for _, v in cells}) != len(cells):
                    raise AssertionError("partial fibre repeats a target column")
                cells.sort()
                parity[x] ^= (
                    sum(
                        cells[left][1] > cells[right][1]
                        for left in range(len(cells))
                        for right in range(left + 1, len(cells))
                    )
                    & 1
                )
    return parity


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certificate",
        type=Path,
        help=(
            "optionally verify a fixed-Wallis N-only v2 or full joint v1 "
            "certificate and check every layer XOR"
        ),
    )
    args = parser.parse_args()

    golf = construct_golf17()
    verify_chart(golf)
    (
        target_signs,
        target_bits,
        lambda_signs,
        psi_signs,
        _factors,
    ) = wallis_targets(golf)
    expected_signs = (
        1,
        -1,
        -1,
        -1,
        -1,
        -1,
        1,
        1,
        -1,
        -1,
        -1,
        1,
        1,
        1,
        1,
        1,
        1,
    )
    if tuple(target_signs[x] for x in COLORS) != expected_signs:
        raise AssertionError("Wallis layer target profile changed")
    if any(psi_signs[x] != 1 for x in COLORS):
        raise AssertionError("Wallis Psi signs are not all positive")

    implication = audit_reduced_constraint_implication(golf)
    atom_counts = indicator_atom_count_by_colour(golf)
    monomial_counts = inversion_monomial_count_by_colour(golf)
    if not all(monomial_counts.values()):
        raise AssertionError("a raw layer XOR row is empty")

    print("[exact] Wallis golf SHA-256:", golf_sha256(golf))
    print(
        "[exact] Wallis H_x target signs x=0..15,infinity:",
        [target_signs[x] for x in COLORS],
    )
    print(
        "[exact] Wallis H_x target bits  x=0..15,infinity:",
        [target_bits[x] for x in COLORS],
    )
    print(
        "[exact] Wallis lambda signs x=0..15:",
        [lambda_signs[x] for x in FINITE],
    )
    print(
        "[exact] Wallis P(Psi^x) signs x=0..15,infinity:",
        [psi_signs[x] for x in COLORS],
    )
    print(
        "[exact] allowed N-indicator atoms by layer:",
        [atom_counts[x] for x in COLORS],
    )
    print(
        "[exact] raw quadratic inversion monomials by layer:",
        [monomial_counts[x] for x in COLORS],
    )
    print("[exact] reduced-constraint structural audit:", implication)
    print("[rank] raw ANF/XOR row rank = 17 (nonempty disjoint colour supports)")
    print(
        "[rank] incremental rank modulo the reduced exact-one constraints = 0 "
        "(all 17 rows are entailed by the audited no-hole theorem)"
    )

    if args.certificate is not None:
        n = decode_n_payload(args.certificate, golf)
        verify_reduced_n(n, golf)
        observed = observed_layer_bits(n, golf)
        if observed != target_bits:
            raise AssertionError("certificate violates a layer-sign equation")
        print("[certificate] PASS: reduced N constraints and all 17 layer XORs")
    else:
        print("[certificate] not requested; no existence or nonexistence claim is made")


if __name__ == "__main__":
    main()
