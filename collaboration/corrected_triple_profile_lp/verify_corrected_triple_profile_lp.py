#!/usr/bin/env python3
"""Exact audit and LP certificate for the ordered pair triple-profile system.

This verifier is deliberately self-contained.  It builds every currently
proved right-module relation used in the audit, checks exact ranks over Q,
and verifies persisted exact nonnegative rational witnesses.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Fr
from math import comb, gcd, lcm


V, K = 31, 15
NV = comb(V, K)
NF = NV // 17
CLASSES = tuple(range(1, 14))
PAIRS = tuple((s, t) for s in CLASSES for t in CLASSES)
INDEX = {pair: i for i, pair in enumerate(PAIRS)}
NVAR = len(PAIRS)


def eberlein(i: int, j: int) -> int:
    return sum(
        (-1) ** (i - h) * comb(K - h, i - h) * comb(K - j, h) * comb(V - K + h - j, h)
        for h in range(i + 1)
    )


def valency(i: int) -> int:
    return comb(K, i) * comb(V - K, i)


def multiplicity(j: int) -> int:
    return comb(V, j) - (comb(V, j - 1) if j else 0)


def fibre_intersection_numbers() -> dict[int, int]:
    out: dict[int, int] = {}
    for s in range(13, 0, -1):
        lam = comb(V - s, 14 - s) // comb(K - s, 14 - s)
        out[s] = comb(K, s) * (lam - 1) - sum(
            comb(t, s) * out[t] for t in range(s + 1, 14)
        )
    assert sum(out.values()) == NF - 1
    return out


FIBRE_NUMBERS = fibre_intersection_numbers()


def ambient_cell_capacity(u: int, s: int, t: int) -> int:
    """Number of all 15-sets D having the requested two intersections."""
    total = 0
    for a in range(u + 1):
        b = s - a
        c = t - a
        d = 15 - s - t + a
        if 0 <= b <= 15 - u and 0 <= c <= 15 - u and 0 <= d <= u + 1:
            total += comb(u, a) * comb(15 - u, b) * comb(15 - u, c) * comb(u + 1, d)
    return total


# Clearing all Johnson-kernel denominators once makes every profile equation
# integral without changing its row space.
KERNEL_SCALE = lcm(*(valency(i) for i in range(1, 15)))


def kernel(a: int, s: int) -> int:
    """A common integral multiple of the P_a kernel at intersection s."""
    if s == 15:
        return KERNEL_SCALE
    i = 15 - s
    assert KERNEL_SCALE % valency(i) == 0
    return eberlein(i, a) * (KERNEL_SCALE // valency(i))


Relation = tuple[int, ...]  # coordinates (I,A_1,...,A_13)


H1_SCALARS = {
    1: -97,
    2: -2282,
    3: -27027,
    4: -147056,
    5: -413413,
    6: -546546,
    7: -162591,
    8: 414414,
    9: 531531,
    10: 272272,
    11: 71253,
    12: 8918,
    13: 623,
}

H2_SCALARS = {
    1: 77,
    2: 1488,
    3: 13689,
    4: 52000,
    5: 75933,
    6: -24024,
    7: -162591,
    8: -108108,
    9: 42185,
    10: 73216,
    11: 30537,
    12: 5148,
    13: 449,
}

H3_ACTION = {
    1: (0, 1),
    2: (-1638, -12),
    3: (-2193, 66),
    4: (-26100, -220),
    5: (35442, 495),
    6: (-4026, -792),
    7: (72765, 924),
    8: (-88110, -792),
    9: (1694, 495),
    10: (-4884, -220),
    11: (14655, 66),
    12: (2022, -12),
    13: (372, 1),
}

H4_ACTION = {
    1: (0, 1, 0),
    2: (1234, -11, -1),
    3: (-2535, 55, 11),
    4: (19110, -165, -55),
    5: (-59488, 330, 165),
    6: (84084, -462, -330),
    7: (-99099, 462, 462),
    8: (118404, -330, -462),
    9: (-87516, 165, 330),
    10: (31746, -55, -165),
    11: (-9555, 11, 55),
    12: (3614, -1, -11),
    13: (0, 0, 1),
}

# Exact free-coordinate values for one strictly positive rational witness in
# each affine profile space.  The free coordinates are determined by the
# verifier's deterministic RREF; the dictionary keys make that ordering
# auditable.  Empty dictionaries mean the equality system has a unique
# solution.
RATIONAL_WITNESS_PARAMETERS: dict[int, dict[int, Fr]] = {
    1: {},
    2: {},
    3: {159: Fr(693, 2), 160: Fr(297)},
    4: {148: Fr(9499, 2), 149: Fr(1512), 160: Fr(665, 2), 161: Fr(421, 2)},
    5: {
        137: Fr(134975, 8),
        138: Fr(10755, 4),
        149: Fr(13879, 4),
        150: Fr(2985, 4),
        161: Fr(955, 4),
        162: Fr(1275, 8),
    },
    6: {
        126: Fr(4969812, 385),
        127: Fr(65178, 77),
        138: Fr(3184437, 385),
        139: Fr(72378, 77),
        150: Fr(9276, 5),
        151: Fr(1571, 4),
        162: Fr(144),
        163: Fr(489, 4),
    },
    7: {
        115: Fr(14),
        116: Fr(42),
        127: Fr(3080),
        128: Fr(434),
        139: Fr(4480),
        140: Fr(28),
        151: Fr(238),
        152: Fr(854, 3),
        163: Fr(42),
        164: Fr(98),
    },
    8: {
        116: Fr(29, 2),
        128: Fr(706),
        129: Fr(265, 4),
        140: Fr(1049147, 840),
        141: Fr(29, 2),
        152: Fr(29, 2),
        153: Fr(14077, 120),
        164: Fr(29, 2),
        165: Fr(265, 4),
    },
    9: {
        129: Fr(1277, 52),
        141: Fr(51, 4),
        142: Fr(1855, 52),
        153: Fr(51, 4),
        154: Fr(177, 4),
        165: Fr(51, 4),
        166: Fr(309, 8),
    },
    10: {
        142: Fr(625, 12),
        154: Fr(35, 4),
        155: Fr(235, 24),
        166: Fr(35, 4),
        167: Fr(165, 8),
    },
    11: {155: Fr(79, 3), 167: Fr(79, 3), 168: Fr(13, 3)},
    12: {168: Fr(15)},
    13: {},
}

# Independently discovered integer points, again stored only by their free
# profile coordinates.  The default standard-library audit reconstructs all
# pivot coordinates over Q and checks that every resulting entry is a
# nonnegative integer satisfying every equality exactly.  CP-SAT is not part
# of that certificate.
INTEGER_WITNESS_PARAMETERS: dict[int, dict[int, Fr]] = {
    1: {},
    2: {},
    3: {159: Fr(378), 160: Fr(288)},
    4: {148: Fr(4503), 149: Fr(1607), 160: Fr(387), 161: Fr(195)},
    5: {
        137: Fr(17710),
        138: Fr(2205),
        149: Fr(2860),
        150: Fr(960),
        161: Fr(385),
        162: Fr(120),
    },
    6: {
        126: Fr(12881),
        127: Fr(490),
        138: Fr(7273),
        139: Fr(1298),
        150: Fr(2555),
        151: Fr(246),
        162: Fr(119),
        163: Fr(130),
    },
    7: {
        115: Fr(0),
        116: Fr(91),
        127: Fr(1711),
        128: Fr(340),
        139: Fr(24),
        140: Fr(327),
        151: Fr(15),
        152: Fr(520),
        163: Fr(420),
        164: Fr(0),
    },
    8: {
        116: Fr(0),
        128: Fr(0),
        129: Fr(68),
        140: Fr(0),
        141: Fr(120),
        152: Fr(0),
        153: Fr(165),
        164: Fr(79),
        165: Fr(48),
    },
    9: {
        129: Fr(0),
        141: Fr(0),
        142: Fr(41),
        153: Fr(0),
        154: Fr(40),
        165: Fr(0),
        166: Fr(41),
    },
    10: {142: Fr(0), 154: Fr(0), 155: Fr(23), 166: Fr(49), 167: Fr(10)},
    11: {155: Fr(41), 167: Fr(45), 168: Fr(0)},
    12: {168: Fr(18)},
    13: {},
}


def relation(*, identity: int = 0, entries: dict[int, int] | None = None) -> Relation:
    row = [identity] + [0] * 13
    for s, value in (entries or {}).items():
        row[s] = value
    return tuple(row)


def exact_action_relations() -> dict[int, list[Relation]]:
    """Complete kernels proved at levels H1 through H4."""
    rels: dict[int, list[Relation]] = {
        1: [relation(identity=-H1_SCALARS[s], entries={s: 1}) for s in CLASSES],
        2: [relation(identity=-H2_SCALARS[s], entries={s: 1}) for s in CLASSES],
        3: [
            relation(identity=-H3_ACTION[s][0], entries={1: -H3_ACTION[s][1], s: 1})
            for s in range(2, 14)
        ],
        4: [
            relation(
                identity=-H4_ACTION[s][0],
                entries={1: -H4_ACTION[s][1], 13: -H4_ACTION[s][2], s: 1},
            )
            for s in range(2, 13)
        ],
    }
    return rels


def fraction_rref(
    rows: list[list[int | Fr]],
    rhs: list[int | Fr],
    ncol: int,
) -> tuple[list[list[Fr]], list[int], list[int]]:
    """Reduced row echelon form over Q; returns matrix, pivots, bad rows."""
    mat = [[Fr(x) for x in row] + [Fr(rhs[i])] for i, row in enumerate(rows)]
    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(ncol):
        candidates = [i for i in range(pivot_row, len(mat)) if mat[i][col]]
        if not candidates:
            continue
        chosen = min(candidates, key=lambda i: len(str(mat[i][col])))
        mat[pivot_row], mat[chosen] = mat[chosen], mat[pivot_row]
        pivot = mat[pivot_row][col]
        mat[pivot_row] = [x / pivot for x in mat[pivot_row]]
        for i, row in enumerate(mat):
            if i == pivot_row or not row[col]:
                continue
            multiple = row[col]
            mat[i] = [x - multiple * y for x, y in zip(row, mat[pivot_row])]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == len(mat):
            break
    bad = [
        i
        for i in range(pivot_row, len(mat))
        if all(mat[i][j] == 0 for j in range(ncol)) and mat[i][ncol] != 0
    ]
    return mat, pivot_cols, bad


def nullspace(rows: list[list[int | Fr]], ncol: int) -> list[list[Fr]]:
    mat, pivots, bad = fraction_rref(rows, [0] * len(rows), ncol)
    assert not bad
    free = [j for j in range(ncol) if j not in pivots]
    basis = []
    for j in free:
        vec = [Fr(0)] * ncol
        vec[j] = 1
        for i, pivot in enumerate(pivots):
            vec[pivot] = -mat[i][j]
        basis.append(vec)
    return basis


def rational_rank(rows: list[list[int | Fr]], ncol: int) -> int:
    return len(fraction_rref(rows, [0] * len(rows), ncol)[1])


SUPPORT = {a: sorted({a} | set(range(15 - a, 16))) for a in range(8)}


def certified_relations(a: int) -> list[Relation]:
    """The safe staircase/strength-14 annihilator family at level a."""
    spectral_kernel = nullspace(
        [[eberlein(i, j) for i in range(16)] for j in SUPPORT[a]],
        16,
    )
    candidates: list[list[Fr]] = []
    for z in spectral_kernel:
        row = [z[0]] + [z[15 - s] for s in CLASSES]
        candidates.append(row)
    independent: list[list[Fr]] = []
    for row in candidates:
        if rational_rank(independent + [row], 14) > len(independent):
            independent.append(row)

    # Z_a = 17 iota^* E_a iota - I.
    extra = [
        Fr(17 * multiplicity(a), NV) - 1,
        *[
            Fr(17 * multiplicity(a) * eberlein(15 - s, a), NV * valency(15 - s))
            for s in CLASSES
        ],
    ]
    if rational_rank(independent + [extra], 14) > len(independent):
        independent.append(extra)

    cleared: list[Relation] = []
    for row in independent:
        denominator = lcm(*(x.denominator for x in row))
        ints = [int(x * denominator) for x in row]
        divisor = gcd(*ints)
        cleared.append(tuple(x // divisor for x in ints))
    return cleared


def all_relations() -> dict[int, list[Relation]]:
    """Union of the strongest currently proved module relations.

    H1--H4 use the exact action tables.  H5--H7 use only the safe
    staircase/strength-14 annihilator family, with no exact-rank claim.
    """
    out = exact_action_relations()
    for a in range(5, 8):
        out[a] = certified_relations(a)
    return out


def build_system(
    u: int,
    *,
    include_structural_zeros: bool = True,
) -> tuple[list[list[int]], list[int], dict[int, list[Relation]]]:
    rels = all_relations()
    rows: list[list[int]] = []
    rhs: list[int] = []

    # Structural zeros.  Partition [31] into B∩C, B\\C, C\\B, and the
    # complement of B∪C.  If no choice of the four occupation numbers can
    # realise (s,t), then the corresponding profile coordinate is exactly 0.
    if include_structural_zeros:
        for s, t in PAIRS:
            possible = ambient_cell_capacity(u, s, t) > 0
            if not possible:
                row = [0] * NVAR
                row[INDEX[(s, t)]] = 1
                rows.append(row)
                rhs.append(0)

    # P_0 / valency equations.
    for s in CLASSES:
        row = [0] * NVAR
        for t in CLASSES:
            row[INDEX[(s, t)]] = 1
        rows.append(row)
        rhs.append(FIBRE_NUMBERS[s] - int(s == u))
    for t in CLASSES:
        row = [0] * NVAR
        for s in CLASSES:
            row[INDEX[(s, t)]] = 1
        rows.append(row)
        rhs.append(FIBRE_NUMBERS[t] - int(t == u))

    for a, family in rels.items():
        for z in family:
            for orientation in (0, 1):
                row = [0] * NVAR
                for s, t in PAIRS:
                    row[INDEX[(s, t)]] = (
                        z[s] * kernel(a, t) if orientation == 0 else kernel(a, s) * z[t]
                    )
                rows.append(row)
                rhs.append(-z[0] * kernel(a, u) - z[u] * kernel(a, 15))
    return rows, rhs, rels


def audit_witness(
    u: int,
    rows: list[list[int]],
    rhs: list[int],
    values: list[Fr],
) -> None:
    assert len(values) == NVAR
    assert min(values) >= 0
    assert all(
        values[INDEX[(s, t)]] <= ambient_cell_capacity(u, s, t) for s, t in PAIRS
    )
    for row, target in zip(rows, rhs):
        assert sum(Fr(a) * x for a, x in zip(row, values)) == target


def reconstruct_from_parameters(
    rref_matrix: list[list[Fr]],
    pivot_columns: list[int],
    parameters: dict[int, Fr],
) -> list[Fr]:
    free = [j for j in range(NVAR) if j not in pivot_columns]
    assert set(parameters) == set(free)
    values = [Fr(0)] * NVAR
    for col in free:
        values[col] = parameters[col]
    for i, pivot in enumerate(pivot_columns):
        values[pivot] = rref_matrix[i][NVAR] - sum(
            rref_matrix[i][col] * values[col] for col in free
        )
    return values


def solve_and_print(
    u: int,
    rows: list[list[int]],
    rhs: list[int],
    rref_matrix: list[list[Fr]],
    pivot_columns: list[int],
    *,
    emit_values: bool = True,
) -> list[Fr] | None:
    """Development helper: solve the small exact affine parameter LP."""
    import numpy as np
    from scipy.optimize import linprog

    free = [j for j in range(NVAR) if j not in pivot_columns]
    dim = len(free)
    constants = [Fr(0)] * NVAR
    coefficients = [[Fr(0)] * dim for _ in range(NVAR)]
    for q, col in enumerate(free):
        coefficients[col][q] = 1
    for i, pivot in enumerate(pivot_columns):
        constants[pivot] = rref_matrix[i][NVAR]
        for q, col in enumerate(free):
            coefficients[pivot][q] = -rref_matrix[i][col]

    # Coordinates identically zero are certified structural/derived zeros and
    # are omitted from the max-min objective.
    live = [i for i in range(NVAR) if constants[i] != 0 or any(coefficients[i])]
    if dim == 0:
        values = constants
        audit_witness(u, rows, rhs, values)
        print(
            f"unique exact witness: support={sum(x > 0 for x in values)}, "
            f"min positive={min(x for x in values if x > 0)}"
        )
        if emit_values:
            print("free:")
        return values

    # Maximise delta over the genuinely live coordinates:
    # const_i + coeff_i*y >= delta.
    objective = np.zeros(dim + 1)
    objective[-1] = -1
    aub = []
    bub = []
    for i in live:
        raw = [-float(x) for x in coefficients[i]] + [1.0]
        scale = max(1.0, max(abs(x) for x in raw), abs(float(constants[i])))
        aub.append([x / scale for x in raw])
        bub.append(float(constants[i]) / scale)
    result = linprog(
        objective,
        A_ub=np.array(aub),
        b_ub=np.array(bub),
        bounds=[(None, None)] * (dim + 1),
        method="highs",
    )
    print(
        f"parameter LP status={result.message}; "
        f"live-cell delta={result.x[-1] if result.success else None}"
    )
    if not result.success:
        return None

    # Rationalise only d<=10 free parameters, then reconstruct every profile
    # coordinate exactly from RREF.
    for denominator in (10**3, 10**5, 10**7, 10**9):
        free_values = [
            Fr(float(result.x[q])).limit_denominator(denominator) for q in range(dim)
        ]
        values = [
            constants[i] + sum(coefficients[i][q] * free_values[q] for q in range(dim))
            for i in range(NVAR)
        ]
        if min(values) < 0:
            continue
        audit_witness(u, rows, rhs, values)
        print(
            f"exact witness: dimension={dim}, forced zeros={NVAR - len(live)}, "
            f"support={sum(x > 0 for x in values)}, "
            f"min positive={min(x for x in values if x > 0)}, "
            f"max denominator={max(x.denominator for x in values)}"
        )
        if emit_values:
            print("free:", " ".join(f"{free[q]}={free_values[q]}" for q in range(dim)))
        return values
    raise AssertionError("could not rationalise the parameter-LP solution")


def integer_solve_and_print(
    u: int,
    rows: list[list[int]],
    rhs: list[int],
    rref_matrix: list[list[Fr]],
    pivot_columns: list[int],
) -> list[int] | None:
    """Development helper: find an exact nonnegative integral profile."""
    from ortools.sat.python import cp_model

    model = cp_model.CpModel()
    variables = []
    for s, t in PAIRS:
        upper = min(
            FIBRE_NUMBERS[s] - int(s == u),
            FIBRE_NUMBERS[t] - int(t == u),
        )
        variables.append(model.NewIntVar(0, upper, f"x_{s}_{t}"))

    free = [j for j in range(NVAR) if j not in pivot_columns]
    for i, pivot in enumerate(pivot_columns):
        coefficients = [Fr(1), *[rref_matrix[i][col] for col in free]]
        target = rref_matrix[i][NVAR]
        denominator = lcm(target.denominator, *(x.denominator for x in coefficients))
        ints = [int(x * denominator) for x in coefficients]
        integer_target = int(target * denominator)
        divisor = gcd(abs(integer_target), *(abs(x) for x in ints))
        ints = [x // divisor for x in ints]
        integer_target //= divisor
        model.Add(
            ints[0] * variables[pivot]
            + sum(
                ints[q + 1] * variables[col]
                for q, col in enumerate(free)
                if ints[q + 1]
            )
            == integer_target
        )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300
    solver.parameters.num_search_workers = 8
    solver.parameters.log_search_progress = False
    status = solver.Solve(model)
    print(f"integer CP-SAT status={solver.StatusName(status)}")
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    values = [solver.Value(x) for x in variables]
    audit_witness(u, rows, rhs, [Fr(x) for x in values])
    print(
        f"integer witness: support={sum(x > 0 for x in values)}, "
        f"min positive={min(x for x in values if x > 0)}"
    )
    print("integer-free:", " ".join(f"{j}={values[j]}" for j in free))
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solve", type=int, choices=range(1, 14))
    parser.add_argument("--solve-all", action="store_true")
    parser.add_argument("--integer-solve", type=int, choices=range(1, 14))
    parser.add_argument("--integer-solve-all", action="store_true")
    parser.add_argument("--no-values", action="store_true")
    parser.add_argument("--rank-only", action="store_true")
    args = parser.parse_args()

    relation_counts = []
    strongest = all_relations()
    for a, family in strongest.items():
        expected = {1: 13, 2: 13, 3: 12, 4: 11, 5: 10, 6: 9, 7: 8}[a]
        rank = rational_rank([list(row) for row in family], 14)
        assert len(family) == rank == expected
        safe = certified_relations(a)
        if a <= 4:
            # The explicit scalar/two-map/three-map action tables span the
            # full same annihilator spaces as the independent staircase
            # construction.  Thus no H2 relation is silently absent.
            assert (
                rational_rank(
                    [list(row) for row in family + safe],
                    14,
                )
                == expected
            )
        relation_counts.append(rank)
    print(f"module relation dimensions H1..H7: {relation_counts}")

    # The 28 staircase-vanishing N_j P_a relations are contained in the
    # complete annihilator families (or the valency family at a=0), so their
    # two oriented profile evaluations add displayed rows but no information.
    h0 = [relation(identity=-FIBRE_NUMBERS[s], entries={s: 1}) for s in CLASSES]
    redundant_vanishing = 0
    for a in range(8):
        family = h0 if a == 0 else strongest[a]
        family_rank = rational_rank([list(row) for row in family], 14)
        for j in range(8, 15):
            if j in SUPPORT[a]:
                continue
            zonal = relation(
                identity=kernel(j, 15),
                entries={s: kernel(j, s) for s in CLASSES},
            )
            assert (
                rational_rank(
                    [list(row) for row in family + [zonal]],
                    14,
                )
                == family_rank
            )
            redundant_vanishing += 1
    assert redundant_vanishing == 28
    print("28 staircase-vanishing relations are exactly redundant")

    base_rows, base_rhs, _ = build_system(1, include_structural_zeros=False)
    base_mat, base_pivots, base_bad = fraction_rref(base_rows, base_rhs, NVAR)
    assert not base_bad and len(base_rows) == 178 and len(base_pivots) == 114
    del base_mat
    print("base system: 178 displayed equations, exact rank 114")

    selected = args.solve or args.integer_solve
    targets = [selected] if selected else list(CLASSES)
    for u in targets:
        rows, rhs, _ = build_system(u)
        mat, pivots, bad = fraction_rref(rows, rhs, NVAR)
        assert not bad
        print(
            f"u={u:2d}: equations={len(rows)}, rank={len(pivots)}, "
            f"affine dimension={NVAR - len(pivots)}"
        )
        if args.solve or args.solve_all:
            solve_and_print(
                u,
                rows,
                rhs,
                mat,
                pivots,
                emit_values=not args.no_values,
            )
        elif args.integer_solve or args.integer_solve_all:
            integer_solve_and_print(u, rows, rhs, mat, pivots)
        elif not args.rank_only:
            rational_values = reconstruct_from_parameters(
                mat,
                pivots,
                RATIONAL_WITNESS_PARAMETERS[u],
            )
            audit_witness(u, rows, rhs, rational_values)
            possible = [
                rational_values[INDEX[(s, t)]]
                for s, t in PAIRS
                if ambient_cell_capacity(u, s, t)
            ]
            assert min(possible) > 0
            integer_values = reconstruct_from_parameters(
                mat,
                pivots,
                INTEGER_WITNESS_PARAMETERS[u],
            )
            audit_witness(u, rows, rhs, integer_values)
            assert all(x.denominator == 1 for x in integer_values)
            print(
                f"       strict rational witness min={min(possible)}, "
                f"integer witness support={sum(x > 0 for x in integer_values)}"
            )


if __name__ == "__main__":
    main()
