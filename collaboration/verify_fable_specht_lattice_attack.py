#!/usr/bin/env python3
"""Verifier for collaboration/fable_specht_lattice_attack.md (2026-07-24).

Exact integer/rational arithmetic only (stdlib + optional numpy for the
r=3 short-vector sweep cross-check; every numpy candidate is re-checked in
exact int arithmetic).  Reuses the deterministic bases and the saturated
kernel routine of evidence/verify_saturated_support_lattice.py.

Sections
  S1  admissibility survey for S(r-1, r, 2r+1), r odd <= 31
  S2  structure battery at r=3 and r=5:
      - facet partition into b block-cliques; blocks-per-Y count
      - H-edge classification (edges <-> 2x 1-intersecting base pairs)
      - Johnson-edge classification (spheres are cliques; Y-pair cross edges)
      - norm identities  z.z = -2 Sum_{E(H)} z_K z_L,
                         r z.z = -2 Sum_{E(J)} z_K z_L,
                         z.w  = -z^T H w
      - q = H-edge parity = J-edge parity on the stable kernel
      - sphere weights even; per-Y u-bit sums even; Y-activity identity
      - Gram matrix, Smith normal form, determinant, 2-adic profile
      - r=3: rigorous short-vector enumeration and lattice identification
      - rank-drop space  {c : sum_P c_P E_r e_P = 0}  and mu_x tests
"""

import os
import sys
import random
from fractions import Fraction
from itertools import combinations
from math import comb, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "evidence"))

from verify_saturated_support_lattice import (  # noqa: E402
    build_restricted_matrix,
    saturated_integer_kernel,
    build_induced_odd_matrices,
)

random.seed(20260724)


# ----------------------------------------------------------------------
# S1: admissibility survey
# ----------------------------------------------------------------------

def lambda_values(r):
    """All lambda_i of S(r-1, r, 2r+1), or None if some is non-integral."""
    values = []
    for i in range(r):
        numerator = comb(2 * r + 1 - i, r - 1 - i)
        denominator = r - i
        if numerator % denominator:
            return None, i
        values.append(numerator // denominator)
    return values, None


def survey():
    print("S1: admissibility of S(r-1, r, 2r+1) for odd r <= 31")
    admissible = []
    failures = {}
    for r in range(3, 32, 2):
        values, bad_index = lambda_values(r)
        if values is None:
            failures[r] = bad_index
            continue
        b = comb(2 * r + 1, r) // (r + 2)
        admissible.append((r, b, b % 2, r % 4))
    for r, b, b_parity, r_mod4 in admissible:
        print(f"  r={r:2d} admissible; b={b} (parity {b_parity}), "
              f"r mod 4 = {r_mod4}")
    print("  divisibility failures (r: first bad i):",
          dict(sorted(failures.items())))
    assert failures[7] == 1 and failures[13] == 2
    assert all(r in dict((a, None) for a, *_ in admissible)
               for r in (3, 5, 9, 11, 15))
    odd_b = [r for r, b, parity, _ in admissible if parity]
    print("  admissible r with b odd:", odd_b)
    return admissible


# ----------------------------------------------------------------------
# generic exact linear algebra helpers
# ----------------------------------------------------------------------

def fraction_rank_nullspace(rows, ncols):
    """Exact rank and a nullspace basis of a rational matrix (list rows)."""
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    pivots = []
    pivot_row = 0
    for col in range(ncols):
        src = next((i for i in range(pivot_row, len(matrix))
                    if matrix[i][col] != 0), None)
        if src is None:
            continue
        matrix[pivot_row], matrix[src] = matrix[src], matrix[pivot_row]
        inv = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / inv for entry in matrix[pivot_row]]
        for i in range(len(matrix)):
            if i != pivot_row and matrix[i][col] != 0:
                factor = matrix[i][col]
                matrix[i] = [a - factor * b
                             for a, b in zip(matrix[i], matrix[pivot_row])]
        pivots.append(col)
        pivot_row += 1
    pivot_set = set(pivots)
    basis = []
    for free in range(ncols):
        if free in pivot_set:
            continue
        vec = [Fraction(0)] * ncols
        vec[free] = Fraction(1)
        for row_i, piv in enumerate(pivots):
            vec[piv] = -matrix[row_i][free]
        basis.append(vec)
    return len(pivots), basis


def smith_invariants(matrix):
    """Nonzero invariant factors (positive) of an integer matrix."""
    a = [row[:] for row in matrix]
    m = len(a)
    n = len(a[0]) if m else 0
    t = 0
    diag = []
    while t < min(m, n):
        best = None
        for i in range(t, m):
            for j in range(t, n):
                if a[i][j] and (best is None or abs(a[i][j]) < best[0]):
                    best = (abs(a[i][j]), i, j)
        if best is None:
            break
        _, bi, bj = best
        a[t], a[bi] = a[bi], a[t]
        for row in a:
            row[t], row[bj] = row[bj], row[t]
        done = False
        while not done:
            done = True
            for i in range(t + 1, m):
                if a[i][t]:
                    q = a[i][t] // a[t][t]
                    if q:
                        a[i] = [x - q * y for x, y in zip(a[i], a[t])]
                    if a[i][t]:
                        a[t], a[i] = a[i], a[t]
                        done = False
            for j in range(t + 1, n):
                if a[t][j]:
                    q = a[t][j] // a[t][t]
                    if q:
                        for row in a:
                            row[j] -= q * row[t]
                    if a[t][j]:
                        for row in a:
                            row[t], row[j] = row[j], row[t]
                        done = False
        pivot = abs(a[t][t])
        offender = None
        for i in range(t + 1, m):
            for j in range(t + 1, n):
                if a[i][j] % pivot:
                    offender = i
                    break
            if offender is not None:
                break
        if offender is not None:
            a[t] = [x + y for x, y in zip(a[t], a[offender])]
            continue
        diag.append(pivot)
        t += 1
    for i in range(len(diag) - 1):
        assert diag[i + 1] % diag[i] == 0
    return diag


def two_adic_profile(values):
    profile = {}
    for value in values:
        v2 = 0
        while value % 2 == 0:
            value //= 2
            v2 += 1
        profile[v2] = profile.get(v2, 0) + 1
    return dict(sorted(profile.items()))


# ----------------------------------------------------------------------
# S2: main battery
# ----------------------------------------------------------------------

def run_case(r, sample_count):
    n = 2 * r + 1
    points = frozenset(range(n))
    b = comb(n, r) // (r + 2)
    print("=" * 72)
    print(f"S2: r={r}, v={n}, b={b}")

    matrix, blocks, base, outside = build_restricted_matrix(n, r)
    facets = [frozenset(c) for c in combinations(range(n), r - 1)]
    base_list = sorted(base, key=lambda blk: tuple(sorted(blk)))
    base_set = set(base_list)
    out_blocks = [blocks[j] for j in outside]
    out_index = {block: i for i, block in enumerate(out_blocks)}

    # --- facet partition into b cliques of size r --------------------
    block_of_facet = []
    for facet in facets:
        owners = [P for P in base_list if facet <= P]
        assert len(owners) == 1
        block_of_facet.append(owners[0])
    from collections import Counter
    counts = Counter(block_of_facet)
    assert set(counts.values()) == {r} and len(counts) == b
    print(f"  facet partition: {len(facets)} facets = {b} cliques x {r}")

    # --- blocks per (r+2)-set Y --------------------------------------
    blocks_in_Y = []
    for facet in facets:
        Y = points - facet
        inside = [P for P in base_list if P <= Y]
        assert len(inside) == (r + 1) // 2
        for P, Q in combinations(inside, 2):
            assert len(P & Q) == r - 2 and (P | Q) == Y
        blocks_in_Y.append((Y, inside))
    print(f"  every (r+2)-set contains exactly {(r + 1) // 2} base blocks")

    # --- sphere coordinates ------------------------------------------
    sphere_block = []
    missing_point = []
    for K in out_blocks:
        complement = points - K
        partners = [complement - {p} for p in complement
                    if frozenset(complement - {p}) in base_set]
        partners = [frozenset(P) for P in partners]
        assert len(partners) == 1
        P = partners[0]
        (a,) = tuple(complement - P)
        sphere_block.append(P)
        missing_point.append(a)

    # --- H edges and classification ----------------------------------
    h_edges = []
    for i, K in enumerate(out_blocks):
        complement = points - K
        for omitted in complement:
            L = frozenset(complement - {omitted})
            j = out_index.get(L)
            if j is not None and j > i:
                h_edges.append((i, j))
    degree = Counter()
    for i, j in h_edges:
        degree[i] += 1
        degree[j] += 1
    assert set(degree.values()) == {r}
    assert len(h_edges) == b * (r + 1) * r // 2

    one_int_pairs = set()
    for i, j in h_edges:
        P, Q = sphere_block[i], sphere_block[j]
        a_i, a_j = missing_point[i], missing_point[j]
        assert P != Q and len(P & Q) == 1
        assert {a_i, a_j} == set(points - (P | Q))
        one_int_pairs.add(frozenset((P, Q)))
    pair_count = sum(1 for P, Q in combinations(base_list, 2)
                     if len(P & Q) == 1)
    assert pair_count == len(one_int_pairs) == b * (r + 1) * r // 4
    one_int_degree = Counter()
    for pair in one_int_pairs:
        for P in pair:
            one_int_degree[P] += 1
    assert set(one_int_degree.values()) == {r * (r + 1) // 2}
    print(f"  H: {r}-regular, {len(h_edges)} edges = 2 x {pair_count} "
          f"one-intersecting base pairs; per-block 1-int degree "
          f"{r * (r + 1) // 2} ({'odd' if (r * (r + 1) // 2) % 2 else 'even'})")

    # --- Johnson edges and classification ----------------------------
    j_edges = []
    for i, j in combinations(range(len(out_blocks)), 2):
        if len(out_blocks[i] & out_blocks[j]) == r - 1:
            j_edges.append((i, j))
    same_sphere = cross = 0
    for i, j in j_edges:
        P, Q = sphere_block[i], sphere_block[j]
        if P == Q:
            same_sphere += 1
        else:
            assert len(P & Q) == r - 2
            assert missing_point[i] in Q and missing_point[j] in P
            cross += 1
    assert same_sphere == b * comb(r + 1, 2)
    assert cross == 4 * len(facets) * comb((r + 1) // 2, 2)
    assert len(j_edges) == b * r * r * (r + 1) // 2
    print(f"  J-edges among outside blocks: {len(j_edges)} = "
          f"{same_sphere} in-sphere + {cross} cross (Y-pairs)")

    # --- stable kernel -----------------------------------------------
    basis, rational_rank = saturated_integer_kernel(matrix)
    dim = len(basis)
    print(f"  rank_Q N = {rational_rank}, rank_Z Lambda = {dim} "
          f"(b = {b}, 2b = {2 * b})")
    if r == 3:
        assert (rational_rank, dim) == (21, 7)
    if r == 5:
        assert (rational_rank, dim) == (319, 77)

    h_plus_i, sphere_matrix = build_induced_odd_matrices(
        blocks, base, outside)

    # --- identity battery --------------------------------------------
    def random_vector():
        coefficients = [random.randint(-2, 2) for _ in range(dim)]
        vec = [0] * len(out_blocks)
        for c, bv in zip(coefficients, basis):
            if c:
                for k, entry in enumerate(bv):
                    vec[k] += c * entry
        return vec

    samples = [list(bv) for bv in basis] + [
        random_vector() for _ in range(sample_count)]

    sphere_rows = [[k for k, entry in enumerate(row) if entry]
                   for row in sphere_matrix]
    y_pair_coords = []
    for Y, inside in blocks_in_Y:
        entry = []
        for P in inside:
            q1, q2 = tuple(Y - P)
            k1 = out_index[frozenset(points - P - {q1})]
            k2 = out_index[frozenset(points - P - {q2})]
            entry.append((k1, k2))
        y_pair_coords.append(entry)

    for z in samples:
        norm = sum(entry * entry for entry in z)
        eh = sum(z[i] * z[j] for i, j in h_edges)
        ej = sum(z[i] * z[j] for i, j in j_edges)
        assert norm == -2 * eh                      # Kneser norm identity
        assert r * norm == -2 * ej                  # Johnson norm identity
        odd = [entry & 1 for entry in z]
        q_bit = (norm // 2) & 1
        eh_parity = sum(odd[i] & odd[j] for i, j in h_edges) & 1
        ej_parity = sum(odd[i] & odd[j] for i, j in j_edges) & 1
        assert q_bit == eh_parity == ej_parity      # q = edge parity
        for row in sphere_rows:                     # sphere weights even
            assert sum(odd[k] for k in row) % 2 == 0
        activity = 0
        for entry in y_pair_coords:                 # Y-activity identity
            weight = sum((odd[k1] ^ odd[k2]) for k1, k2 in entry)
            assert weight % 2 == 0
            activity ^= (weight // 2) & 1
        assert activity == 0

    for _ in range(30):                             # polarized identity
        z = random.choice(samples)
        w = random.choice(samples)
        dot = sum(x * y for x, y in zip(z, w))
        hzw = sum(z[i] * w[j] + z[j] * w[i] for i, j in h_edges)
        assert dot == -hzw
    print(f"  identity battery passed on {len(samples)} vectors "
          f"(norm, polarization, q = H-parity = J-parity, sphere/Y parities)")

    # --- Gram, SNF, determinant --------------------------------------
    gram = [[sum(x * y for x, y in zip(u, v)) for v in basis]
            for u in basis]
    invariants = smith_invariants(gram)
    determinant = 1
    for value in invariants:
        determinant *= value
    profile = two_adic_profile(invariants)
    print(f"  Gram SNF invariants: {invariants}")
    print(f"  det Lambda = {determinant} = 2^{sum(k * c for k, c in profile.items())}"
          f" x odd; 2-adic profile {profile}")
    even_dots = all(gram[i][j] % 2 == 0
                    for i in range(dim) for j in range(dim) if i != j)
    diag_mod4 = {gram[i][i] % 4 for i in range(dim)}
    print(f"  pairwise dots all even: {even_dots}; "
          f"diagonal mod 4 values: {sorted(diag_mod4)}")
    result = {"gram": gram, "invariants": invariants,
              "determinant": determinant, "basis": basis,
              "even_dots": even_dots}

    # --- rank-drop space ----------------------------------------------
    full_matrix = [[int(facet <= block) for block in blocks]
                   for facet in facets]
    full_basis, full_rank = saturated_integer_kernel(full_matrix)
    assert len(full_basis) == 2 * b
    block_index = {block: i for i, block in enumerate(blocks)}
    base_positions = [block_index[P] for P in base_list]
    k_a = [[vec[pos] for pos in base_positions] for vec in full_basis]
    rank_ka, null_ka = fraction_rank_nullspace(k_a, b)
    drop = b - rank_ka
    assert dim == 2 * b - rank_ka
    print(f"  evaluation map ker_Z W -> Z^A: rank {rank_ka}, "
          f"rank drop {drop} (rank_Z Lambda = 2b - rank = {dim})")

    ones_image = [sum(row) for row in k_a]
    assert any(ones_image), "chi_A unexpectedly orthogonal to ker W"
    print("  chi_A not orthogonal to ker W (E_r chi_A = chi_A - 1/(r+2) != 0)"
          " : verified")

    if drop:
        mu_matrix = []
        for x in range(n):
            mu = [n * (1 if x in P else 0) - r for P in base_list]
            mu_matrix.append(mu)
        mu_rank, _ = fraction_rank_nullspace(mu_matrix, b)
        image = [[sum(row[k] * mu[k] for k in range(b)) for mu in mu_matrix]
                 for row in k_a]
        image_rank, _ = fraction_rank_nullspace(image, n)
        nonzero_mu = 0
        for x in range(n):
            column = [sum(row[k] * mu_matrix[x][k] for k in range(b))
                      for row in k_a]
            if any(column):
                nonzero_mu += 1
        print(f"  rank-drop space dimension {drop}; "
              f"span(mu_x) rank {mu_rank}, image rank {image_rank}, "
              f"mu_x outside drop space for {nonzero_mu}/{n} points")
        assert image_rank == mu_rank, (
            "point-type vectors meet the drop space")
    return result


# ----------------------------------------------------------------------
# r=3 lattice identification
# ----------------------------------------------------------------------

def identify_r3(result):
    print("=" * 72)
    print("S3: r=3 lattice identification")
    gram = result["gram"]
    basis = result["basis"]
    dim = len(gram)

    inverse = invert_fraction_matrix(gram)
    norm_bound = 16
    box = [isqrt(int(norm_bound * inverse[i][i]) + 1) + 1
           for i in range(dim)]
    counts = {}
    total = 1
    for width in box:
        total *= 2 * width + 1
    assert total < 40_000_000, total
    coefficients = [0] * dim

    def enumerate_box(position):
        if position == dim:
            if all(c == 0 for c in coefficients):
                return
            norm = 0
            for i in range(dim):
                for j in range(dim):
                    norm += coefficients[i] * gram[i][j] * coefficients[j]
            if norm <= norm_bound:
                counts[norm] = counts.get(norm, 0) + 1
            return
        for value in range(-box[position], box[position] + 1):
            coefficients[position] = value
            enumerate_box(position + 1)
        coefficients[position] = 0

    enumerate_box(0)
    print(f"  coefficient box {box}; norms <= {norm_bound}: {counts}")

    # cross-check the norm-8 count by direct +-1 signature collision
    n, r = 7, 3
    points = frozenset(range(n))
    matrix_rows = len(basis[0])
    # rebuild outside blocks in the same order as the basis coordinates
    _, blocks, base, outside = build_restricted_matrix(n, r)
    out_blocks = [blocks[j] for j in outside]
    assert len(out_blocks) == matrix_rows
    facets = [frozenset(c) for c in combinations(range(n), r - 1)]
    facet_list = list(facets)
    signature_of = {}
    for quad in combinations(range(len(out_blocks)), 4):
        signature = tuple(
            sum(1 for k in quad if facet <= out_blocks[k])
            for facet in facet_list)
        signature_of.setdefault(signature, []).append(quad)
    norm8 = 0
    for quads in signature_of.values():
        for left, right in combinations(quads, 2):
            if not (set(left) & set(right)):
                norm8 += 1
            else:
                raise AssertionError("support-<8 kernel vector found")
    print(f"  +-1 support-8 vectors: {2 * norm8} "
          f"(signature collisions x 2 signs)")
    assert counts.get(8, 0) == 2 * norm8
    return counts


def invert_fraction_matrix(mat):
    dim = len(mat)
    work = [[Fraction(entry) for entry in row] +
            [Fraction(1 if i == j else 0) for j in range(dim)]
            for i, row in enumerate(mat)]
    for col in range(dim):
        src = next(i for i in range(col, dim) if work[i][col] != 0)
        work[col], work[src] = work[src], work[col]
        inv = work[col][col]
        work[col] = [entry / inv for entry in work[col]]
        for i in range(dim):
            if i != col and work[i][col] != 0:
                factor = work[i][col]
                work[i] = [a - factor * c
                           for a, c in zip(work[i], work[col])]
    return [row[dim:] for row in work]


def main():
    survey()
    result3 = run_case(3, sample_count=200)
    identify_r3(result3)
    run_case(5, sample_count=40)
    print("=" * 72)
    print("ALL SPECHT-LATTICE-ATTACK CHECKS PASSED")


if __name__ == "__main__":
    main()
