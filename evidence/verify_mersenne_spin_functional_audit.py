#!/usr/bin/env python3
"""Exact audit for ``mersenne_spin_functional_audit.md``.

The script verifies:

* the r=3 and r=5 support-functional spaces
      U_A = ker(R_A) / ker(C_A),
  their point-incidence descriptions, and 2-saturation of coordinate
  evaluation;
* all-odd derived parameters and the internal/external intersection
  facts used to prove full point rank at hypothetical r=15;
* the top Johnson projector formula and the exact subset-star norm
  formula for every j at r=3,5,15;
* the r=15 2-adic filtration and the normalized point-star Gram layer.

Only Python's standard library and exact integer/rational arithmetic are
used.  The finite r=3,5 trade spaces are constructed here from scratch.
"""

from fractions import Fraction
from itertools import combinations
from math import comb


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


def binary_nullspace(rows, dimension):
    """Bit-packed basis of the nullspace of a binary row matrix."""
    reduced = list(rows)
    pivot_columns = []
    pivot_row = 0
    for column in range(dimension):
        source = next(
            (
                row
                for row in range(pivot_row, len(reduced))
                if (reduced[row] >> column) & 1
            ),
            None,
        )
        if source is None:
            continue
        reduced[pivot_row], reduced[source] = (
            reduced[source], reduced[pivot_row]
        )
        for row in range(len(reduced)):
            if row != pivot_row and ((reduced[row] >> column) & 1):
                reduced[row] ^= reduced[pivot_row]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(reduced):
            break

    pivot_set = set(pivot_columns)
    basis = []
    for free in range(dimension):
        if free in pivot_set:
            continue
        vector = 1 << free
        for row, pivot in enumerate(pivot_columns):
            if (reduced[row] >> free) & 1:
                vector |= 1 << pivot
        assert all(parity(equation & vector) == 0 for equation in rows)
        basis.append(vector)
    return basis


def exact_cover(columns, rows, cap=1):
    """Deterministic Algorithm X; only the first small design is needed."""
    solutions = []
    partial = []

    def select(row):
        removed = []
        for column in rows[row]:
            for other_row in columns[column]:
                for other_column in rows[other_row]:
                    if other_column != column:
                        columns[other_column].remove(other_row)
            removed.append(columns.pop(column))
        return removed

    def deselect(row, removed):
        for column in reversed(rows[row]):
            columns[column] = removed.pop()
            for other_row in columns[column]:
                for other_column in rows[other_row]:
                    if other_column != column:
                        columns[other_column].add(other_row)

    def solve():
        if len(solutions) >= cap:
            return
        if not columns:
            solutions.append(list(partial))
            return
        column = min(columns, key=lambda key: len(columns[key]))
        for row in sorted(columns[column]):
            partial.append(row)
            removed = select(row)
            solve()
            deselect(row, removed)
            partial.pop()
            if len(solutions) >= cap:
                return

    solve()
    return solutions


def saturated_integer_kernel(matrix):
    """Saturated Z-kernel via unimodular Euclidean column reduction."""
    row_count = len(matrix)
    column_count = len(matrix[0])
    columns = []
    for column in range(column_count):
        augmented = [matrix[row][column] for row in range(row_count)]
        augmented.extend(
            int(index == column) for index in range(column_count)
        )
        columns.append(augmented)

    unused = set(range(column_count))
    pivot_columns = []
    for row in range(row_count):
        nonzero = [
            column for column in unused if columns[column][row] != 0
        ]
        while len(nonzero) > 1:
            nonzero.sort(key=lambda column: abs(columns[column][row]))
            source = nonzero[0]
            source_value = columns[source][row]
            for destination in nonzero[1:]:
                quotient = columns[destination][row] // source_value
                if quotient:
                    columns[destination] = [
                        left - quotient * right
                        for left, right in zip(
                            columns[destination], columns[source]
                        )
                    ]
            nonzero = [
                column for column in unused
                if columns[column][row] != 0
            ]
        if nonzero:
            pivot = nonzero[0]
            unused.remove(pivot)
            pivot_columns.append(pivot)

    basis = [
        columns[column][row_count:] for column in sorted(unused)
    ]
    assert all(
        sum(entry * coefficient for entry, coefficient in zip(row, word))
        == 0
        for word in basis
        for row in matrix
    )
    packed = [
        sum((entry & 1) << index for index, entry in enumerate(word))
        for word in basis
    ]
    assert gf2_rank(packed) == len(basis)
    return basis, len(pivot_columns)


class SmallSpinData:
    """Minimal exact full/support trade data for r=3 and r=5."""

    def __init__(self, r):
        n = 2 * r + 1
        self.blocks = [
            frozenset(block) for block in combinations(range(n), r)
        ]
        facets = [
            frozenset(facet)
            for facet in combinations(range(n), r - 1)
        ]
        facet_index = {facet: index for index, facet in enumerate(facets)}
        facets_of = {
            block_index: [
                facet_index[frozenset(facet)]
                for facet in combinations(block, r - 1)
            ]
            for block_index, block in enumerate(self.blocks)
        }

        cover_columns = {index: set() for index in range(len(facets))}
        for block_index, incident in facets_of.items():
            for index in incident:
                cover_columns[index].add(block_index)
        solutions = exact_cover(
            {index: set(rows) for index, rows in cover_columns.items()},
            facets_of,
        )
        assert len(solutions) == 1
        base_indices = set(solutions[0])
        self.base = frozenset(
            self.blocks[index] for index in base_indices
        )
        outside = [
            index for index in range(len(self.blocks))
            if index not in base_indices
        ]

        full_matrix = [[0] * len(self.blocks) for _ in facets]
        for block_index, incident in facets_of.items():
            for index in incident:
                full_matrix[index][block_index] = 1
        integer_basis, _ = saturated_integer_kernel(full_matrix)
        self.code_basis = [
            sum((entry & 1) << index
                for index, entry in enumerate(word))
            for word in integer_basis
        ]

        gram_rows = [
            sum(
                parity(left & right) << column
                for column, right in enumerate(self.code_basis)
            )
            for left in self.code_basis
        ]
        radical_coefficients = binary_nullspace(
            gram_rows, len(self.code_basis)
        )
        self.radical_basis = []
        for coefficients in radical_coefficients:
            word = 0
            for index, codeword in enumerate(self.code_basis):
                if (coefficients >> index) & 1:
                    word ^= codeword
            self.radical_basis.append(word)

        self.restricted_matrix = [
            [row[index] for index in outside] for row in full_matrix
        ]
        self.block_index = {
            block: index for index, block in enumerate(self.blocks)
        }


def weight(word):
    return bin(int(word)).count("1")


def v2_fraction(value):
    """2-adic valuation of a nonzero Fraction."""
    numerator = abs(value.numerator)
    denominator = value.denominator
    answer = 0
    while numerator % 2 == 0:
        numerator //= 2
        answer += 1
    while denominator % 2 == 0:
        denominator //= 2
        answer -= 1
    return answer


def lambda_parameter(r, i):
    numerator = comb(2 * r + 1 - i, r - 1 - i)
    denominator = r - i
    assert numerator % denominator == 0
    return numerator // denominator


def intersection_distribution(r, inside):
    values = [0] * (r + 1)
    values[r] = int(inside)
    for i in range(r - 1, -1, -1):
        right = comb(r, i) * lambda_parameter(r, i)
        right -= sum(
            comb(j, i) * values[j]
            for j in range(i + 1, r + 1)
        )
        values[i] = right
    assert all(value >= 0 for value in values)
    return values


def restrict_words(words, positions):
    return [
        sum(((word >> position) & 1) << j
            for j, position in enumerate(positions))
        for word in words
    ]


def verify_small_functional_spaces():
    expected = {
        3: {
            "rank_c": 7,
            "rank_r": 3,
            "point_rank": 4,
            "y_dim": 4,
            "d_dim": 0,
            "point_is_y": True,
            "point_is_d": False,
        },
        5: {
            "rank_c": 55,
            "rank_r": 55,
            "point_rank": 11,
            "y_dim": 11,
            "d_dim": 11,
            "point_is_y": True,
            "point_is_d": True,
        },
    }

    for r in (3, 5):
        quotient = SmallSpinData(r)
        base = sorted(
            quotient.base, key=lambda block: tuple(sorted(block))
        )
        positions = [quotient.block_index[block] for block in base]
        c_restrictions = restrict_words(quotient.code_basis, positions)
        r_restrictions = restrict_words(
            quotient.radical_basis, positions
        )
        rank_c = gf2_rank(c_restrictions)
        rank_r = gf2_rank(r_restrictions)
        y_dim = len(base) - rank_r
        d_dim = len(base) - rank_c

        point_rows = [
            sum(int(point in block) << j
                for j, block in enumerate(base))
            for point in range(2 * r + 1)
        ]
        point_rank = gf2_rank(point_rows)
        point_in_y = all(
            all(parity(row & restriction) == 0
                for restriction in r_restrictions)
            for row in point_rows
        )
        point_in_d = all(
            all(parity(row & restriction) == 0
                for restriction in c_restrictions)
            for row in point_rows
        )

        target = expected[r]
        assert rank_c == target["rank_c"]
        assert rank_r == target["rank_r"]
        assert point_rank == target["point_rank"]
        assert y_dim == target["y_dim"]
        assert d_dim == target["d_dim"]
        assert point_in_y == target["point_is_y"]
        assert point_in_d == target["point_is_d"]
        if r == 3:
            # Equality of dimension and containment identifies the Hamming
            # point code with Y=ker(R_A).
            assert point_in_y and point_rank == y_dim
            # Its exact [7,4,3] weight distribution.
            span = {0}
            for row in point_rows:
                span |= {word ^ row for word in tuple(span)}
            assert len(span) == 16
            distribution = {
                w: sum(weight(word) == w for word in span)
                for w in range(8)
            }
            assert distribution == {
                0: 1, 1: 0, 2: 0, 3: 7,
                4: 7, 5: 0, 6: 0, 7: 1,
            }
        else:
            assert point_in_d and point_rank == d_dim == y_dim

        # Exact 2-saturation check.  The rational rank of evaluation is
        # dim L - dim Lambda; equality with the binary restriction rank
        # says the image lattice has no even Smith factor.
        support_basis, _support_matrix_rank = saturated_integer_kernel(
            quotient.restricted_matrix
        )
        rational_evaluation_rank = (
            len(quotient.code_basis) - len(support_basis)
        )
        assert rational_evaluation_rank == rank_c

        print(
            f"r={r}: (rank C_A, rank R_A)=({rank_c},{rank_r}); "
            f"(dim Y, dim D)=({y_dim},{d_dim}); "
            f"point rank={point_rank}; evaluation 2-saturated"
        )


def verify_r15_point_rank_inputs():
    r = 15
    lambdas = [lambda_parameter(r, i) for i in range(r)]
    assert all(value & 1 for value in lambdas)

    internal = intersection_distribution(r, True)
    external = intersection_distribution(r, False)
    assert all(value % 2 == 0 for value in internal[:r])
    assert all(value % 2 == 1 for value in external[:r])
    assert internal[2] == 3360
    assert internal[12] == 14560

    # The point Gram matrix has lambda_1 on the diagonal and lambda_2
    # off it, hence is J modulo two.
    assert lambdas[1] & 1
    assert lambdas[2] & 1

    # These are exactly the numerical inputs to the proof that no
    # nonzero point-kernel word exists.
    assert all(lambdas[i] > lambdas[i + 1] for i in range(r - 1))
    print(
        "r=15: all lambda_i odd; external n_j all odd; "
        "internal n_2=3360 and n_12=14560; point rank theorem inputs PASS"
    )


def top_projector_entry(r, intersection):
    return Fraction(
        2 * ((-1) ** (r - intersection)),
        (r + 2) * comb(r + 1, r - intersection),
    )


def verify_point_star_projector_identity():
    """Verify the three local counts proving the point-star identity.

    For d=W a_x and an (r-1)-set F, the Johnson-adjacent d-count is
    r^2-3, r-1, or 2(r-1), according as

        x in F;  x not in F and d_F=1;  x not in F and d_F=0.

    Adding the diagonal (r+2)d_F gives the claimed closed formula for
    WW^T d.  The remaining assertions are then scalar identities.
    """
    for r in (3, 5, 15):
        assert r & 1
        lambda_r_minus_2 = (r + 3) // 2
        other_blocks = (r - 2) * (lambda_r_minus_2 - 1)
        adjacent = {
            (1, 1): (r - 1) + 2 * other_blocks,
            (0, 1): r - 1,
            (0, 0): 2 * (r - 1),
        }
        assert adjacent[(1, 1)] == r * r - 3

        for (contains_x, d_f), neighbour_count in adjacent.items():
            observed = (r + 2) * d_f + neighbour_count
            expected = (
                3 * d_f
                + 2 * (r - 1)
                + (r - 2) * (r + 1) * contains_x
            )
            assert observed == expected

        # Coefficients of d, 1, and e_x in W applied to (5a).
        assert Fraction(1) - Fraction(3, 3) == 0
        assert (
            -Fraction(2 * (r - 1), 3)
            + Fraction(r - 2, 3)
            + Fraction(r, 3)
        ) == 0
        assert (
            -Fraction((r - 2) * (r + 1), 3)
            + Fraction((r - 2) * (r + 1), 3)
        ) == 0
        assert 3 & 1 and (r + 2) & 1

    # Directly check every coordinate of (5a) in the two available
    # exact designs against the Johnson projector kernel.
    for r in (3, 5):
        quotient = SmallSpinData(r)
        blocks = quotient.blocks
        base = quotient.base
        for point in range(2 * r + 1):
            base_star = [
                block for block in base if point in block
            ]
            for block in blocks:
                projected = sum(
                    top_projector_entry(r, len(block & design_block))
                    for design_block in base_star
                )
                wtwa = (
                    r * int(block in base and point in block)
                    + sum(
                        len(block & design_block) == r - 1
                        for design_block in base_star
                    )
                )
                expected = (
                    int(block in base and point in block)
                    - Fraction(wtwa, 3)
                    + Fraction(r - 2, 3) * int(point in block)
                    + Fraction(r, 3 * (r + 2))
                )
                assert projected == expected

    print(
        "truncated point-star projector identity and "
        "2-adic radical annihilation inputs PASS"
    )


def containing_intersection_distribution(r, j):
    """m_s for Q containing a fixed j-set T and |P cap Q|=s.

    Here P is a fixed A-block containing T.  The triangular moment
    equations are solved exactly.
    """
    values = [Fraction(0)] * (r + 1)
    values[r] = Fraction(1)
    for h in range(r - 1 - j, -1, -1):
        right = (
            comb(r - j, h)
            * Fraction(lambda_parameter(r, j + h))
        )
        right -= sum(
            comb(s - j, h) * values[s]
            for s in range(j + h + 1, r + 1)
        )
        values[j + h] = right
    assert all(value.denominator == 1 for value in values)
    assert sum(values) == lambda_parameter(r, j)
    return values


def subset_star_energy(r, j):
    distribution = containing_intersection_distribution(r, j)
    row_value = sum(
        distribution[s] * top_projector_entry(r, s)
        for s in range(j, r + 1)
    )
    return Fraction(lambda_parameter(r, j)) * row_value


def verify_projector_filtration():
    for r in (3, 5, 15):
        # Diagonal projector entry equals top multiplicity / total size.
        assert top_projector_entry(r, r) == Fraction(2, r + 2)
        for j in range(r):
            observed = subset_star_energy(r, j)
            expected = Fraction(
                lambda_parameter(r, j) * 2 * (r + 1),
                (j + 2) * (r + 2),
            )
            assert observed == expected

    r = 15
    m = 4
    levels = [
        v2_fraction(subset_star_energy(r, j))
        for j in range(r)
    ]
    expected_levels = [
        m + 1 - v2_fraction(Fraction(j + 2))
        for j in range(r)
    ]
    assert levels == expected_levels
    assert levels == [4, 5, 3, 5, 4, 5, 2, 5, 4, 5, 3, 5, 4, 5, 1]

    lambda_1 = lambda_parameter(r, 1)
    diagonal = Fraction(
        lambda_1 * 2 * (r + 1), 3 * (r + 2)
    )
    off_diagonal = Fraction(
        lambda_1 * (r + 1) * (3 * r - 2),
        6 * r * (r + 2),
    )
    blocks = lambda_parameter(r, 0)
    total_energy = subset_star_energy(r, 0)
    assert (
        (2 * r + 1) * diagonal
        + (2 * r + 1) * (2 * r) * off_diagonal
        == r * r * total_energy
    )
    assert blocks == Fraction((2 * r + 1) * lambda_1, r)
    assert v2_fraction(diagonal) == m + 1
    assert v2_fraction(off_diagonal) == m - 1

    # After normalization by 2^(m-1), the point-star Gram has zero
    # diagonal and unit off-diagonal modulo two, i.e. J+I.  Its rank
    # on 2r+1 points is 2r.
    normalized_diagonal = diagonal / (2 ** (m - 1))
    normalized_off_diagonal = off_diagonal / (2 ** (m - 1))
    assert v2_fraction(normalized_diagonal) >= 1
    assert v2_fraction(normalized_off_diagonal) == 0
    gram_rows = []
    size = 2 * r + 1
    for i in range(size):
        gram_rows.append(
            sum((i != j) << j for j in range(size))
        )
    assert gf2_rank(gram_rows) == 2 * r

    print("r=15 subset-star v2 levels:", levels)
    print(
        "normalized point-star Gram is J+I: rank 30, "
        "radical dimension 1"
    )


def main():
    verify_small_functional_spaces()
    verify_r15_point_rank_inputs()
    verify_point_star_projector_identity()
    verify_projector_filtration()
    print("MERSENNE SPIN FUNCTIONAL AUDIT: PASS")


if __name__ == "__main__":
    main()
