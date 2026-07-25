#!/usr/bin/env python3
"""Exact 2-adic audit of the support-restricted trade lattice.

Let A be an S(r-1,r,2r+1), let O be the r-subsets outside A, and let

    N = W_{r-1,r}(2r+1)[*, O].

The lattice relevant to the fixed-base parity attack is

    Lambda(A) = ker_Z N.

If H is the graph induced by the non-A vertices of the Odd graph and B is
the base-sphere incidence matrix, then the correct graph formula is

    Lambda(A) = ker_Z(H + I) intersect ker_Z B.

The second condition is essential: at r=5, ker_Z(H+I) has rank 88 while
Lambda has rank 77.  (They happen to coincide at r=3.)

Its reduction modulo two is generally *strictly smaller* than ker_F2 N.
This script computes a saturated Z-basis by unimodular column operations,
then classifies on Lambda/2Lambda

    B(x,y) = x.y (mod 2),
    q(x)   = x.x/2 (mod 2).

No floating point arithmetic or solver certificate is used.  The r=5 base
is the deterministic first exact cover returned by the same lexicographic
algorithm used in verify_fixed_base_parity.py.

Expected invariant output:

    r=3: rank_Z Lambda 7,  binary/stable quotient dimension 6,
         first Bockstein rank 6, polar rank 0, radical 7, q=0.
    r=5: rank_Z Lambda 77, binary/stable quotient dimension 109,
         first Bockstein rank 109, polar rank 32, radical 45,
         q vanishes on the radical, nonsingular quotient Arf invariant 0.

The script also records the decisive warning that the *full* trade lattice
ker_Z W is not 4-even even at r=3: two explicit disjoint Fano planes give a
norm-14 vector.  Finally, it exhaustively distinguishes full-radical from
support-radical mate differences:

    r=3: 0 of 28 unordered mate differences are full-radical;
    r=5: all 10,296 unordered mate differences are full-radical.

Thus sharing a common disjoint base does not, by itself, force radicality
in the full stable trade code.
"""

from itertools import combinations
from math import comb

try:
    # Direct execution: python3 evidence/verify_saturated_support_lattice.py
    from verify_fixed_base_parity import exact_cover
except ModuleNotFoundError:
    # Module execution/import from the repository root.
    from evidence.verify_fixed_base_parity import exact_cover


def gf2_rank(rows):
    """Rank of bit-packed binary row vectors."""
    pivots = {}
    for value in rows:
        value = int(value)
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def parity(value):
    return bin(int(value)).count("1") & 1


def build_restricted_matrix(n, r):
    """Return the facet-by-nonbase-block matrix and deterministic base."""
    blocks = [frozenset(c) for c in combinations(range(n), r)]
    facets = [frozenset(c) for c in combinations(range(n), r - 1)]
    facet_index = {facet: i for i, facet in enumerate(facets)}

    facets_of = {
        j: [
            facet_index[frozenset(facet)]
            for facet in combinations(block, r - 1)
        ]
        for j, block in enumerate(blocks)
    }
    cover_columns = {i: set() for i in range(len(facets))}
    for j, incident in facets_of.items():
        for i in incident:
            cover_columns[i].add(j)

    solution = exact_cover(
        {i: set(columns) for i, columns in cover_columns.items()},
        facets_of,
        cap=1,
    )
    assert len(solution) == 1
    base_indices = set(solution[0])
    outside = [j for j in range(len(blocks)) if j not in base_indices]

    matrix = [[0] * len(outside) for _ in facets]
    for outside_index, block_index in enumerate(outside):
        for facet_index_ in facets_of[block_index]:
            matrix[facet_index_][outside_index] = 1

    base = frozenset(blocks[j] for j in base_indices)
    return matrix, blocks, base, outside


def enumerate_disjoint_mates(blocks, base, r):
    """Exhaustively enumerate all designs whose blocks avoid ``base``."""
    n = 2 * r + 1
    facets = [
        frozenset(facet) for facet in combinations(range(n), r - 1)
    ]
    facet_index = {facet: i for i, facet in enumerate(facets)}
    candidates = [
        j for j, block in enumerate(blocks)
        if block not in base
    ]
    rows = {
        j: tuple(
            facet_index[frozenset(facet)]
            for facet in combinations(blocks[j], r - 1)
        )
        for j in candidates
    }
    columns = {i: set() for i in range(len(facets))}
    for j, incident in rows.items():
        for i in incident:
            columns[i].add(j)

    solutions = exact_cover(
        {i: set(candidate_rows) for i, candidate_rows in columns.items()},
        rows,
    )
    return [
        frozenset(blocks[j] for j in solution)
        for solution in solutions
    ]


def build_induced_odd_matrices(blocks, base, outside):
    """Return H+I and the base-sphere incidence B in outside coordinates."""
    n = len(next(iter(base))) * 2 + 1
    points = set(range(n))
    outside_index = {
        blocks[block_index]: i
        for i, block_index in enumerate(outside)
    }
    base_list = sorted(base, key=lambda block: tuple(sorted(block)))
    base_index = {block: i for i, block in enumerate(base_list)}

    size = len(outside)
    h_plus_i = [[0] * size for _ in range(size)]
    sphere_matrix = [[0] * size for _ in base_list]

    for i, block_index in enumerate(outside):
        block = blocks[block_index]
        complement = points - set(block)
        h_plus_i[i][i] = 1
        base_neighbours = []
        for omitted in complement:
            disjoint = frozenset(complement - {omitted})
            if disjoint in outside_index:
                h_plus_i[i][outside_index[disjoint]] = 1
            elif disjoint in base_index:
                base_neighbours.append(disjoint)
        assert len(base_neighbours) == 1
        sphere_matrix[base_index[base_neighbours[0]]][i] = 1

    return h_plus_i, sphere_matrix


def saturated_integer_kernel(matrix):
    """Compute a saturated Z-basis of ker(matrix) by column reduction.

    Each working column is augmented by the corresponding standard basis
    vector.  Only integral column additions are used, so the lower block is
    always a unimodular change-of-basis matrix.  Processing a row uses the
    Euclidean algorithm until at most one unused column is nonzero there.
    Previously processed rows are zero on every unused column, hence remain
    zero.  At termination the unused augmented columns are exactly a
    saturated basis of the integer kernel.
    """
    row_count = len(matrix)
    column_count = len(matrix[0])
    columns = []
    for j in range(column_count):
        column = [matrix[i][j] for i in range(row_count)]
        column.extend(1 if i == j else 0 for i in range(column_count))
        columns.append(column)

    unused = set(range(column_count))
    pivot_columns = []

    for row in range(row_count):
        nonzero = [column for column in unused if columns[column][row] != 0]
        while len(nonzero) > 1:
            nonzero.sort(key=lambda column: abs(columns[column][row]))
            source = nonzero[0]
            source_value = columns[source][row]
            for destination in nonzero[1:]:
                quotient = columns[destination][row] // source_value
                if quotient:
                    columns[destination] = [
                        x - quotient * y
                        for x, y in zip(columns[destination], columns[source])
                    ]
            nonzero = [
                column for column in unused if columns[column][row] != 0
            ]
        if nonzero:
            pivot = nonzero[0]
            unused.remove(pivot)
            pivot_columns.append(pivot)

    basis = [
        columns[column][row_count:]
        for column in sorted(unused)
    ]

    # Exact kernel verification.
    for vector in basis:
        for row in matrix:
            assert sum(a * b for a, b in zip(row, vector)) == 0

    # A primitive sublattice has independent basis reductions modulo 2.
    packed = [
        sum((entry & 1) << i for i, entry in enumerate(vector))
        for vector in basis
    ]
    assert gf2_rank(packed) == len(basis)

    return basis, len(pivot_columns)


def binary_matrix_rank(matrix):
    packed_rows = [
        sum((entry & 1) << j for j, entry in enumerate(row))
        for row in matrix
    ]
    return gf2_rank(packed_rows)


def binary_nullspace(matrix):
    """Bit-packed basis of the right kernel of a rectangular binary matrix."""
    row_count = len(matrix)
    column_count = len(matrix[0])
    reduced = [
        sum((entry & 1) << j for j, entry in enumerate(row))
        for row in matrix
    ]
    pivot_columns = []
    pivot_row = 0
    for column in range(column_count):
        source = next(
            (
                row
                for row in range(pivot_row, row_count)
                if (reduced[row] >> column) & 1
            ),
            None,
        )
        if source is None:
            continue
        reduced[pivot_row], reduced[source] = (
            reduced[source],
            reduced[pivot_row],
        )
        for row in range(row_count):
            if row != pivot_row and ((reduced[row] >> column) & 1):
                reduced[row] ^= reduced[pivot_row]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    pivot_set = set(pivot_columns)
    basis = []
    for free in range(column_count):
        if free in pivot_set:
            continue
        vector = 1 << free
        for row, pivot in enumerate(pivot_columns):
            if (reduced[row] >> free) & 1:
                vector |= 1 << pivot
        basis.append(vector)
    return basis


def first_bockstein_rank(matrix):
    """Rank of the mod-4 lifting obstruction on ker_F2(matrix).

    If u is a binary kernel word, N*lift(u) is even.  The obstruction to
    finding y with N(lift(u)+2y)=0 mod 4 is the class of N*lift(u)/2 in
    coker(N mod 2), paired here with the left binary kernel.
    """
    right_kernel = binary_nullspace(matrix)
    row_count = len(matrix)
    column_count = len(matrix[0])
    transpose = [
        [matrix[row][column] for row in range(row_count)]
        for column in range(column_count)
    ]
    left_kernel = binary_nullspace(transpose)

    obstruction_rows = [0] * len(left_kernel)
    for column, word in enumerate(right_kernel):
        selected = [
            index for index in range(column_count)
            if (word >> index) & 1
        ]
        half_image = 0
        for row, equation in enumerate(matrix):
            value = sum(equation[index] for index in selected)
            assert value % 2 == 0
            if (value // 2) & 1:
                half_image |= 1 << row
        for row, left_word in enumerate(left_kernel):
            if parity(left_word & half_image):
                obstruction_rows[row] |= 1 << column

    return (
        gf2_rank(obstruction_rows),
        len(right_kernel),
        len(left_kernel),
    )


def nullspace_binary(rows, dimension):
    """Bit-packed basis of the nullspace of a square binary matrix."""
    reduced = list(rows)
    pivot_columns = []
    pivot_row = 0
    for column in range(dimension):
        source = next(
            (
                row
                for row in range(pivot_row, dimension)
                if (reduced[row] >> column) & 1
            ),
            None,
        )
        if source is None:
            continue
        reduced[pivot_row], reduced[source] = (
            reduced[source],
            reduced[pivot_row],
        )
        for row in range(dimension):
            if row != pivot_row and ((reduced[row] >> column) & 1):
                reduced[row] ^= reduced[pivot_row]
        pivot_columns.append(column)
        pivot_row += 1

    free_columns = [
        column for column in range(dimension)
        if column not in set(pivot_columns)
    ]
    basis = []
    for free in free_columns:
        vector = 1 << free
        for row, pivot in enumerate(pivot_columns):
            if (reduced[row] >> free) & 1:
                vector |= 1 << pivot
        assert all(parity(equation & vector) == 0 for equation in rows)
        basis.append(vector)
    return basis


def quadratic_classification(basis):
    """Classify B and q on the mod-two reduction of an integral basis."""
    dimension = len(basis)
    packed = [
        sum((entry & 1) << i for i, entry in enumerate(vector))
        for vector in basis
    ]

    gram_rows = []
    for left in packed:
        row = 0
        for j, right in enumerate(packed):
            if parity(left & right):
                row |= 1 << j
        gram_rows.append(row)

    polar_rank = gf2_rank(gram_rows)
    radical_basis = nullspace_binary(gram_rows, dimension)
    assert len(radical_basis) == dimension - polar_rank

    q_on_basis = [
        (sum(entry * entry for entry in vector) // 2) & 1
        for vector in basis
    ]
    # Every kernel vector has even norm: summing all facet equations counts
    # every coordinate r times, with r odd.
    assert all(sum(entry * entry for entry in vector) % 2 == 0
               for vector in basis)

    def bilinear(left, right):
        value = 0
        cursor = left
        while cursor:
            low_bit = cursor & -cursor
            index = low_bit.bit_length() - 1
            value ^= parity(gram_rows[index] & right)
            cursor ^= low_bit
        return value

    def quadratic(coefficients):
        indices = []
        cursor = coefficients
        while cursor:
            low_bit = cursor & -cursor
            indices.append(low_bit.bit_length() - 1)
            cursor ^= low_bit
        value = 0
        for index in indices:
            value ^= q_on_basis[index]
        for position, left in enumerate(indices):
            for right in indices[position + 1:]:
                value ^= (gram_rows[left] >> right) & 1
        return value

    q_on_radical = [quadratic(vector) for vector in radical_basis]

    # Symplectic Gram-Schmidt.  Once a hyperbolic pair is removed, all
    # remaining spanning vectors are made orthogonal to it.  Unpaired
    # vectors span the radical.  If q vanishes on the radical, the usual
    # sum q(e_i)q(f_i) is the Arf invariant of the nonsingular quotient.
    remaining = [1 << i for i in range(dimension)]
    symplectic_pairs = []
    radical_from_decomposition = []
    while remaining:
        left = remaining.pop()
        partner_position = next(
            (
                i for i, right in enumerate(remaining)
                if bilinear(left, right)
            ),
            None,
        )
        if partner_position is None:
            radical_from_decomposition.append(left)
            continue
        right = remaining.pop(partner_position)
        orthogonalized = []
        for vector in remaining:
            if bilinear(vector, right):
                vector ^= left
            if bilinear(vector, left):
                vector ^= right
            orthogonalized.append(vector)
        remaining = orthogonalized
        symplectic_pairs.append((left, right))

    assert 2 * len(symplectic_pairs) == polar_rank
    assert len(radical_from_decomposition) == dimension - polar_rank
    assert all(bilinear(left, right) == 1
               for left, right in symplectic_pairs)

    arf = None
    if not any(q_on_radical):
        arf = sum(
            quadratic(left) * quadratic(right)
            for left, right in symplectic_pairs
        ) & 1

    return {
        "polar_rank": polar_rank,
        "radical_dimension": len(radical_basis),
        "q_nonzero_basis_count": sum(q_on_basis),
        "q_vanishes_on_radical": not any(q_on_radical),
        "arf_nonsingular_quotient": arf,
        "q_is_zero": polar_rank == 0 and not any(q_on_radical),
    }


def verify_full_fano_counterexample():
    """The unrestricted integral trade lattice is not 4-even at r=3."""
    first = {
        frozenset(block)
        for block in (
            (0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
            (1, 4, 6), (2, 3, 6), (2, 4, 5),
        )
    }
    second = {
        frozenset(block)
        for block in (
            (0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 2, 6),
            (1, 4, 5), (2, 3, 4), (3, 5, 6),
        )
    }
    assert not (first & second)
    all_blocks = [
        frozenset(block) for block in combinations(range(7), 3)
    ]
    vector = [
        (1 if block in first else 0) - (1 if block in second else 0)
        for block in all_blocks
    ]
    for facet in combinations(range(7), 2):
        facet = frozenset(facet)
        assert sum(
            coefficient
            for block, coefficient in zip(all_blocks, vector)
            if facet <= block
        ) == 0
    norm = sum(coefficient * coefficient for coefficient in vector)
    assert norm == 14 and norm % 4 == 2
    print("full r=3 trade lattice: explicit norm-14 counterexample verified")


def intersection_distribution(r, inside):
    """Exact n_j distribution against a block/nonblock from design moments."""
    values = [0] * (r + 1)
    values[r] = 1 if inside else 0
    for i in range(r - 1, -1, -1):
        numerator = comb(2 * r + 1 - i, r - 1 - i)
        denominator = r - i
        assert numerator % denominator == 0
        lambda_i = numerator // denominator
        right = comb(r, i) * lambda_i
        right -= sum(
            comb(j, i) * values[j]
            for j in range(i + 1, r + 1)
        )
        values[i] = right
    assert all(value >= 0 for value in values)
    return values


def verify_mersenne_parameter_parity():
    for r in (3, 15):
        lambdas = []
        for i in range(r):
            numerator = comb(2 * r + 1 - i, r - 1 - i)
            denominator = r - i
            assert numerator % denominator == 0
            lambdas.append(numerator // denominator)
        assert all(value & 1 for value in lambdas)

        internal = intersection_distribution(r, inside=True)
        external = intersection_distribution(r, inside=False)
        assert internal[r] == 1
        assert all(value % 2 == 0 for value in internal[:r])
        assert external[r] == 0
        assert all(value % 2 == 1 for value in external[:r])

    lambdas_r5 = [
        comb(11 - i, 4 - i) // (5 - i)
        for i in range(5)
    ]
    assert [i for i, value in enumerate(lambdas_r5) if value & 1] == [4]
    assert intersection_distribution(5, inside=True)[1] == 15
    print("Mersenne/all-odd parameter and intersection parities verified")


def full_trade_quotient(r, blocks, base, support_dimension):
    """Classify the full trade code and the support kernel's quotient image."""
    n = 2 * r + 1
    facets = [
        frozenset(facet) for facet in combinations(range(n), r - 1)
    ]
    full_matrix = [
        [int(facet <= block) for block in blocks]
        for facet in facets
    ]
    full_basis, full_rank = saturated_integer_kernel(full_matrix)
    full_classification = quadratic_classification(full_basis)

    packed_basis = [
        sum((entry & 1) << i for i, entry in enumerate(vector))
        for vector in full_basis
    ]
    gram_rows = [
        sum(parity(left & right) << j
            for j, right in enumerate(packed_basis))
        for left in packed_basis
    ]
    radical_coefficients = nullspace_binary(gram_rows, len(full_basis))
    radical_words = []
    for coefficients in radical_coefficients:
        word = 0
        for i, basis_word in enumerate(packed_basis):
            if (coefficients >> i) & 1:
                word ^= basis_word
        radical_words.append(word)

    block_index = {block: i for i, block in enumerate(blocks)}
    base_positions = [
        block_index[block]
        for block in sorted(base, key=lambda value: tuple(sorted(value)))
    ]
    radical_restrictions = [
        sum(((word >> position) & 1) << j
            for j, position in enumerate(base_positions))
        for word in radical_words
    ]
    radical_evaluation_rank = gf2_rank(radical_restrictions)
    support_intersection_radical = (
        len(radical_words) - radical_evaluation_rank
    )
    quotient_image_dimension = (
        support_dimension - support_intersection_radical
    )

    # Every pair of mates B,C gives an integral full trade 1_B-1_C, whose
    # mod-two word is 1_B+1_C.  Test whether that word is in the radical of
    # the *full* stable trade code, not merely the support lattice.
    mates = enumerate_disjoint_mates(blocks, base, r)
    mate_words = [
        sum(1 << block_index[block] for block in mate)
        for mate in mates
    ]
    reference_differences = [
        mate_words[0] ^ word for word in mate_words[1:]
    ]
    mate_difference_span = gf2_rank(reference_differences)
    full_radical_pairs = 0
    mate_pair_count = 0
    for i, left in enumerate(mate_words):
        for right in mate_words[i + 1:]:
            difference = left ^ right
            mate_pair_count += 1
            if all(
                parity(difference & codeword) == 0
                for codeword in packed_basis
            ):
                full_radical_pairs += 1

    return {
        "full_rank": full_rank,
        "full_dimension": len(full_basis),
        "polar_rank": full_classification["polar_rank"],
        "radical_dimension": full_classification["radical_dimension"],
        "q_vanishes_on_radical":
            full_classification["q_vanishes_on_radical"],
        "arf": full_classification["arf_nonsingular_quotient"],
        "radical_evaluation_rank": radical_evaluation_rank,
        "support_intersection_radical": support_intersection_radical,
        "quotient_image_dimension": quotient_image_dimension,
        "mate_count": len(mates),
        "mate_pair_count": mate_pair_count,
        "full_radical_mate_pairs": full_radical_pairs,
        "mate_difference_span": mate_difference_span,
    }


def run_case(r):
    n = 2 * r + 1
    matrix, blocks, base, outside = build_restricted_matrix(n, r)
    basis, rational_rank = saturated_integer_kernel(matrix)
    mod2_rank = binary_matrix_rank(matrix)
    binary_kernel_dimension = len(outside) - mod2_rank
    stable_dimension = len(basis)
    quotient_dimension = binary_kernel_dimension - stable_dimension
    bockstein_rank, right_nullity, left_nullity = first_bockstein_rank(
        matrix
    )
    assert right_nullity == binary_kernel_dimension
    assert left_nullity == len(matrix) - mod2_rank
    classification = quadratic_classification(basis)
    full_quotient = full_trade_quotient(
        r, blocks, base, stable_dimension
    )

    h_plus_i, sphere_matrix = build_induced_odd_matrices(
        blocks, base, outside
    )
    h_kernel_basis, h_rank = saturated_integer_kernel(h_plus_i)
    h_nullity = len(h_kernel_basis)

    # Every facet trade supported outside A is a -1 eigenvector of H and
    # has zero sum on each sphere.
    for vector in basis:
        assert all(
            sum(a * b for a, b in zip(row, vector)) == 0
            for row in h_plus_i
        )
        assert all(
            sum(a * b for a, b in zip(row, vector)) == 0
            for row in sphere_matrix
        )

    # Measure exactly how many extra -1 eigenvectors H has before imposing
    # the sphere equations.  Compose B with a saturated H-kernel basis.
    sphere_on_h_kernel = [
        [
            sum(a * b for a, b in zip(row, vector))
            for vector in h_kernel_basis
        ]
        for row in sphere_matrix
    ]
    _coefficient_kernel, sphere_image_rank = saturated_integer_kernel(
        sphere_on_h_kernel
    )
    assert h_nullity - sphere_image_rank == stable_dimension

    print("=" * 72)
    print(f"r={r}: |A|={len(base)}, outside columns={len(outside)}")
    print(
        "rank_Q N =", rational_rank,
        "; rank_F2 N =", mod2_rank,
    )
    print(
        "rank_Z Lambda =", stable_dimension,
        "; dim ker_F2 N =", binary_kernel_dimension,
        "; binary/stable quotient dimension =", quotient_dimension,
    )
    print(
        "first mod-4 Bockstein rank =", bockstein_rank,
        "; one-step liftable dimension =",
        binary_kernel_dimension - bockstein_rank,
    )
    print(
        "polar rank =", classification["polar_rank"],
        "; radical dimension =", classification["radical_dimension"],
    )
    print(
        "ker_Z(H+I) rank =", h_nullity,
        "; sphere-map rank on it =", sphere_image_rank,
        "; intersection rank =", h_nullity - sphere_image_rank,
    )
    print(
        "q=1 on chosen basis =", classification["q_nonzero_basis_count"],
        "; q vanishes on radical =",
        classification["q_vanishes_on_radical"],
        "; quotient Arf =", classification["arf_nonsingular_quotient"],
    )
    print("Lambda is 4-even:", classification["q_is_zero"])
    print(
        "full trade quotient: dimension =",
        full_quotient["polar_rank"],
        "; radical =", full_quotient["radical_dimension"],
        "; quotient Arf =", full_quotient["arf"],
    )
    print(
        "Lambda intersection full radical =",
        full_quotient["support_intersection_radical"],
        "; image in full quotient =",
        full_quotient["quotient_image_dimension"],
    )
    print(
        "mate differences in full radical =",
        full_quotient["full_radical_mate_pairs"],
        "of", full_quotient["mate_pair_count"],
        "; their span rank =", full_quotient["mate_difference_span"],
    )

    assert quotient_dimension == rational_rank - mod2_rank
    # Equality says every nonzero even Smith factor has 2-adic valuation
    # exactly one.  Thus lifting once, from mod 2 to mod 4, already cuts
    # the broad binary kernel down to the stable/integral reduction.
    assert bockstein_rank == quotient_dimension
    assert binary_kernel_dimension - bockstein_rank == stable_dimension
    if r == 3:
        assert (
            rational_rank,
            mod2_rank,
            stable_dimension,
            quotient_dimension,
        ) == (21, 15, 7, 6)
        assert classification == {
            "polar_rank": 0,
            "radical_dimension": 7,
            "q_nonzero_basis_count": 0,
            "q_vanishes_on_radical": True,
            "arf_nonsingular_quotient": 0,
            "q_is_zero": True,
        }
        assert (h_rank, h_nullity, sphere_image_rank) == (21, 7, 0)
        assert full_quotient == {
            "full_rank": 21,
            "full_dimension": 14,
            "polar_rank": 8,
            "radical_dimension": 6,
            "q_vanishes_on_radical": True,
            "arf": 0,
            "radical_evaluation_rank": 3,
            "support_intersection_radical": 3,
            "quotient_image_dimension": 4,
            "mate_count": 8,
            "mate_pair_count": 28,
            "full_radical_mate_pairs": 0,
            "mate_difference_span": 6,
        }
    elif r == 5:
        assert (
            rational_rank,
            mod2_rank,
            stable_dimension,
            quotient_dimension,
        ) == (319, 210, 77, 109)
        assert classification["polar_rank"] == 32
        assert classification["radical_dimension"] == 45
        assert classification["q_vanishes_on_radical"]
        assert classification["arf_nonsingular_quotient"] == 0
        assert not classification["q_is_zero"]
        assert (h_rank, h_nullity, sphere_image_rank) == (308, 88, 11)
        assert full_quotient == {
            "full_rank": 330,
            "full_dimension": 132,
            "polar_rank": 32,
            "radical_dimension": 100,
            "q_vanishes_on_radical": True,
            "arf": 0,
            "radical_evaluation_rank": 55,
            "support_intersection_radical": 45,
            "quotient_image_dimension": 32,
            "mate_count": 144,
            "mate_pair_count": 10296,
            "full_radical_mate_pairs": 10296,
            "mate_difference_span": 44,
        }


def main():
    verify_full_fano_counterexample()
    verify_mersenne_parameter_parity()
    run_case(3)
    run_case(5)
    print("=" * 72)
    print("ALL SATURATED-LATTICE CHECKS PASSED")


if __name__ == "__main__":
    main()
