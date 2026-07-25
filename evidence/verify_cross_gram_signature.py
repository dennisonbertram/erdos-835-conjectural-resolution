#!/usr/bin/env python3
"""Reproduce the oriented cross-Gram signature attack.

Exact checks:
  * T^2 = boundary^T boundary - v I on r=1,3,5 sample rows;
  * the r=1 counterexample;
  * H^2=8I on all 28 canonical Fano mate pairs;
  * full rank modulo 101 on all 10,296 canonical r=5 mate pairs;
  * tr(H), tr(H^3), tr(H^5)=0 on those 10,296 integer matrices;
  * signed-permutation anti-isometries for one representative of each
    r=5 intersection type.

Numerical diagnostic:
  * inertia of every r=5 H, with the minimum absolute eigenvalue printed.

Requires numpy.  It imports the deterministic exact-cover enumerator from
evidence/disjoint_mates.py.  Typical runtime on the development machine is
under 30 seconds.
"""

from collections import Counter
from itertools import combinations
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from disjoint_mates import algox_solutions, steiner_cover_instance  # noqa: E402


def permutation_sign(sequence):
    inversions = sum(
        sequence[i] > sequence[j]
        for i in range(len(sequence))
        for j in range(i + 1, len(sequence))
    )
    return -1 if inversions % 2 else 1


def t_sign(left, right, v):
    """Entry of T=i_u* in the increasing subset bases."""
    if not set(left).isdisjoint(right):
        return 0
    leftover = next(iter(set(range(v)) - set(left) - set(right)))
    return permutation_sign(left + right + (leftover,))


def boundary_gram(left, right):
    """<d_left,d_right>, including the diagonal."""
    if left == right:
        return len(left)
    common = set(left) & set(right)
    if len(common) != len(left) - 1:
        return 0
    i = next(i for i, x in enumerate(left) if x not in common)
    j = next(j for j, x in enumerate(right) if x not in common)
    return (-1) ** (i + j)


def exact_cover_family(v, r):
    blocks = list(combinations(range(v), r))
    x0, y0 = steiner_cover_instance(v, r - 1, blocks)
    base = sorted(algox_solutions(x0, y0, cap=1)[0])
    base_set = set(base)
    x1, y1 = steiner_cover_instance(
        v, r - 1, [block for block in blocks if block not in base_set]
    )
    mates = [sorted(mate) for mate in algox_solutions(x1, y1)]
    return base, mates


def cross_data(left_system, right_system, v, r):
    """Return B0,C0,P,G,U,H,Q using the definitions in the note."""
    shared = set(left_system) & set(right_system)
    left = sorted(set(left_system) - shared)
    right = sorted(set(right_system) - shared)
    pmat = np.array(
        [[t_sign(s, q, v) for q in right] for s in left], dtype=np.int64
    )
    gram = np.array(
        [[boundary_gram(s, q) for q in right] for s in left],
        dtype=np.int64,
    )
    if left:
        assert np.array_equal(pmat @ pmat.T, np.eye(len(left), dtype=np.int64))
    umat = gram @ pmat.T
    hmat = umat + umat.T
    qmat = umat != 0
    return left, right, pmat, gram, umat, hmat, qmat


def fast_h(left_system, right_system, v, r, right_facets=None):
    """Construct U,H,Q without forming dense P and G."""
    shared = set(left_system) & set(right_system)
    left = [s for s in sorted(left_system) if s not in shared]
    right = [s for s in sorted(right_system) if s not in shared]
    right_index = {s: i for i, s in enumerate(right)}
    if right_facets is None:
        right_facets = {
            s[:i] + s[i + 1 :]: (s, i)
            for s in right_system
            for i in range(r)
        }

    # Invert the direct signed disjoint matching B0 -> C0.
    inverse = {}
    for i, s in enumerate(left):
        q = next(q for q in right if set(s).isdisjoint(q))
        inverse[right_index[q]] = (i, t_sign(s, q, v))

    umat = np.zeros((len(left), len(left)), dtype=np.int64)
    for i, s in enumerate(left):
        for removed_position in range(r):
            facet = s[:removed_position] + s[removed_position + 1 :]
            q, added_position = right_facets[facet]
            # A shared q would be a distinct B-block sharing a facet with s.
            assert q not in shared
            j, direct_sign = inverse[right_index[q]]
            umat[i, j] += (
                (-1) ** (removed_position + added_position) * direct_sign
            )
    return umat, umat + umat.T, umat != 0


def rank_mod(matrix, prime):
    """Exact Gaussian rank over F_prime, vectorized with bounded int64."""
    a = (matrix.copy() % prime).astype(np.int64)
    nrows, ncols = a.shape
    rank = 0
    for col in range(ncols):
        pivot = next(
            (i for i in range(rank, nrows) if int(a[i, col]) != 0), None
        )
        if pivot is None:
            continue
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        inverse = pow(int(a[rank, col]), prime - 2, prime)
        a[rank] = (a[rank] * inverse) % prime
        if rank + 1 < nrows:
            a[rank + 1 :] = (
                a[rank + 1 :]
                - a[rank + 1 :, col, None] * a[rank]
            ) % prime
        rank += 1
        if rank == nrows:
            break
    return rank


def all_fano_planes():
    blocks = list(combinations(range(7), 3))
    x0, y0 = steiner_cover_instance(7, 2, blocks)
    return [sorted(system) for system in algox_solutions(x0, y0)]


def verify_t_squared():
    for r in (1, 3, 5):
        v = 2 * r + 1
        blocks = list(combinations(range(v), r))
        # All rows for r=1,3 and ten rows for r=5 are already 4,620
        # cross entries at the largest parameter.
        rows = blocks if r < 5 else blocks[:10]
        for left in rows:
            for right in blocks:
                t2 = sum(
                    t_sign(left, middle, v) * t_sign(middle, right, v)
                    for middle in blocks
                )
                expected = boundary_gram(left, right) - v * (left == right)
                assert t2 == expected
    print("[operator] T^2 = boundary^T boundary - vI: exact checks passed")


def verify_r1():
    _, _, pmat, gram, _, hmat, _ = cross_data(
        [(0,)], [(1,)], 3, 1
    )
    # Relabeling the ordered triple if necessary changes the overall sign
    # but cannot balance a one-dimensional form.
    assert gram.tolist() == [[1]]
    assert abs(int(pmat[0, 0])) == 1
    assert abs(int(hmat[0, 0])) == 2
    print("[r=1] exact counterexample: H is 1x1 with entry of magnitude 2")


def verify_r3():
    _, mates = exact_cover_family(7, 3)
    assert len(mates) == 8
    ident = np.eye(6, dtype=np.int64)
    q_symmetric = 0
    for left, right in combinations(mates, 2):
        _, _, pmat, gram, umat, hmat, qmat = cross_data(
            left, right, 7, 3
        )
        assert np.array_equal(umat, gram @ pmat.T)
        assert np.array_equal(hmat @ hmat, 8 * ident)
        assert int(np.trace(hmat)) == 0
        q_symmetric += np.array_equal(qmat, qmat.T)
    assert q_symmetric == 0
    print(
        "[r=3 canonical] 28/28: H^2=8I, inertia=(3,3,0), "
        "det=-512; Q symmetric 0/28"
    )

    controls = Counter()
    fanos = all_fano_planes()
    assert len(fanos) == 30
    for left, right in combinations(fanos, 2):
        _, _, _, _, _, hmat, _ = cross_data(left, right, 7, 3)
        eigenvalues = np.linalg.eigvalsh(hmat.astype(float))
        positive = int(np.sum(eigenvalues > 1e-8))
        negative = int(np.sum(eigenvalues < -1e-8))
        zero = len(hmat) - positive - negative
        assert zero == 0
        controls[(len(set(left) & set(right)), abs(positive - negative))] += 1
    expected = Counter({(0, 5): 120, (1, 0): 210, (3, 2): 105})
    assert controls == expected, controls
    print(f"[r=3 controls] exact family, numerical inertia: {dict(controls)}")


ANTI_CERTIFICATES = {
    # Deterministic exact-cover mate pair (0,4), intersection h=6.
    6: {
        "pair": (0, 4),
        "permutation": [
            9, 14, 16, 19, 46, 22, 59, 10, 49, 0, 7, 34, 20, 40, 1,
            36, 2, 55, 31, 3, 12, 33, 5, 26, 38, 39, 23, 48, 43, 52,
            44, 18, 45, 21, 11, 47, 15, 56, 24, 25, 13, 51, 53, 28,
            30, 32, 4, 35, 27, 8, 54, 41, 29, 42, 50, 17, 37, 58,
            57, 6,
        ],
        "signs": [
            1, -1, 1, 1, 1, -1, -1, -1, -1, -1, 1, 1, -1, 1, 1,
            1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, -1,
            -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1,
            1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1,
        ],
    },
    # Deterministic exact-cover mate pair (0,1), intersection h=18.
    18: {
        "pair": (0, 1),
        "permutation": [
            16, 39, 22, 46, 25, 41, 33, 17, 38, 19, 36, 23, 27, 47,
            44, 30, 0, 7, 24, 9, 45, 28, 2, 11, 18, 4, 35, 12, 21,
            32, 15, 40, 29, 6, 43, 26, 10, 42, 8, 1, 31, 5, 37, 34,
            14, 20, 3, 13,
        ],
        "signs": [
            1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, -1, 1,
            1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1,
            -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1,
            1, 1, 1,
        ],
    },
}


def verify_anti_certificate(hmat, certificate):
    permutation = certificate["permutation"]
    signs = certificate["signs"]
    n = len(hmat)
    assert len(permutation) == len(signs) == n
    rmat = np.zeros((n, n), dtype=np.int64)
    for i, (image, sign) in enumerate(zip(permutation, signs)):
        rmat[image, i] = sign
    ident = np.eye(n, dtype=np.int64)
    assert np.array_equal(rmat @ rmat, -ident)
    assert np.array_equal(rmat.T @ hmat @ rmat, -hmat)


def canonical_sigma(base, left_system, right_system):
    """Triangle monodromy on B\\C: direct inverse after the A route."""
    shared = set(left_system) & set(right_system)
    left = sorted(set(left_system) - shared)
    right = sorted(set(right_system) - shared)
    left_index = {block: i for i, block in enumerate(left)}
    direct_inverse = {
        target: next(source for source in left if set(source).isdisjoint(target))
        for target in right
    }
    sigma = []
    for source in left:
        middle = next(
            block for block in base if set(block).isdisjoint(source)
        )
        target = next(
            block for block in right if set(block).isdisjoint(middle)
        )
        sigma.append(left_index[direct_inverse[target]])
    return sigma


def permutation_cycles(permutation):
    seen = set()
    answer = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycle = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        assert current == start
        answer.append(cycle)
    return answer


def audit_certificate_vs_sigma(base, mates, intersection, certificate):
    """Show that the recorded anti-map is not a monodromy half-turn."""
    i, j = certificate["pair"]
    sigma = canonical_sigma(base, mates[i], mates[j])
    cycles = permutation_cycles(sigma)
    anti_permutation = certificate["permutation"]
    cycle_id = {
        point: index for index, cycle in enumerate(cycles) for point in cycle
    }

    whole_cycle_images = []
    for cycle in cycles:
        image = {anti_permutation[point] for point in cycle}
        whole_cycle_images.append(
            any(image == set(target) for target in cycles)
        )
    assert not any(whole_cycle_images)

    within = sum(
        cycle_id[point] == cycle_id[anti_permutation[point]]
        for point in range(len(sigma))
    )
    expected = {
        6: ([2, 2, 2, 4, 6, 44], 34),
        18: ([2, 2, 2, 2, 18, 22], 12),
    }
    assert sorted(map(len, cycles)) == expected[intersection][0]
    assert within == expected[intersection][1]

    inverse = [0] * len(sigma)
    for point, image in enumerate(sigma):
        inverse[image] = point
    conjugates_to_inverse = all(
        anti_permutation[sigma[anti_permutation[point]]] == inverse[point]
        for point in range(len(sigma))
    )
    assert not conjugates_to_inverse
    return sorted(map(len, cycles)), within


def verify_r5():
    base, mates = exact_cover_family(11, 5)
    assert len(mates) == 144
    mate_sets = [set(mate) for mate in mates]
    facet_maps = [
        {
            block[:i] + block[i + 1 :]: (block, i)
            for block in mate
            for i in range(5)
        }
        for mate in mates
    ]

    census = Counter()
    q_symmetric = Counter()
    minimum_gap = {6: float("inf"), 18: float("inf")}
    representatives = {}

    for i, j in combinations(range(144), 2):
        shared = len(mate_sets[i] & mate_sets[j])
        umat, hmat, qmat = fast_h(
            mates[i], mates[j], 11, 5, facet_maps[j]
        )
        n = len(hmat)

        # Exact finite claims.
        rank = rank_mod(hmat, 101)
        assert rank == n
        h2 = hmat @ hmat
        h3 = h2 @ hmat
        h5 = h3 @ h2
        assert int(np.trace(hmat)) == 0
        assert int(np.trace(h3)) == 0
        assert int(np.trace(h5)) == 0
        q_symmetric[shared] += int(np.array_equal(qmat, qmat.T))

        # Numerical inertia diagnostic, separated from the exact rank proof.
        eigenvalues = np.linalg.eigvalsh(hmat.astype(float))
        gap = float(np.min(np.abs(eigenvalues)))
        minimum_gap[shared] = min(minimum_gap[shared], gap)
        positive = int(np.sum(eigenvalues > 1e-8))
        negative = int(np.sum(eigenvalues < -1e-8))
        zero = n - positive - negative
        census[(shared, positive, negative, zero)] += 1

        for intersection, certificate in ANTI_CERTIFICATES.items():
            if (i, j) == certificate["pair"]:
                assert shared == intersection
                representatives[intersection] = hmat

    expected = Counter({
        (6, 30, 30, 0): 6336,
        (18, 24, 24, 0): 3960,
    })
    assert census == expected, census
    assert q_symmetric == Counter({6: 0, 18: 0})

    for intersection, hmat in representatives.items():
        verify_anti_certificate(hmat, ANTI_CERTIFICATES[intersection])
    assert set(representatives) == {6, 18}
    sigma_audit = {
        intersection: audit_certificate_vs_sigma(
            base, mates, intersection, certificate
        )
        for intersection, certificate in ANTI_CERTIFICATES.items()
    }

    # Nearby determinant shortcuts fail on the representatives.
    h6 = ANTI_CERTIFICATES[6]["pair"]
    u6, _, _ = fast_h(mates[h6[0]], mates[h6[1]], 11, 5, facet_maps[h6[1]])
    h18 = ANTI_CERTIFICATES[18]["pair"]
    u18, _, _ = fast_h(
        mates[h18[0]], mates[h18[1]], 11, 5, facet_maps[h18[1]]
    )
    assert np.linalg.matrix_rank(u6.astype(float)) == 59
    assert np.linalg.matrix_rank((u18 - u18.T).astype(float)) == 46

    print(
        "[r=5 exact] 144 mates, 10,296 pairs; H full rank mod 101 on all; "
        "tr H^(1,3,5)=0 on all; Q symmetric 0/10,296"
    )
    print(f"[r=5 numerical inertia] {dict(census)}")
    print(f"[r=5 numerical minimum |eigenvalue|] {minimum_gap}")
    print("[r=5 exact representatives] R^2=-I and R^T H R=-H: 2/2")
    print(
        "[r=5 anti-map vs sigma] no sigma cycle preserved setwise: "
        f"{sigma_audit}"
    )
    print("[r=5 no-go] rank(U_h=6)=59; rank(U_h=18-U_h=18^T)=46")


def main():
    verify_t_squared()
    verify_r1()
    verify_r3()
    verify_r5()
    print("RESULT: ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
