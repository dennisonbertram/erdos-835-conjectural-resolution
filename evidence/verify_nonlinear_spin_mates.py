#!/usr/bin/env python3
"""Exact nonlinear spin audit for fixed-base mate differences.

Let

    L = ker_Z W_{r-1,r}(2r+1),
    C = L mod 2,
    S = C / rad(C).

For r=3 and r=5 this script constructs S directly from a saturated
integer kernel.  The adjacent point transpositions s_i act on S by
matrices gamma_i.  Exact computation verifies the Clifford relations

    gamma_i^2 = 1,
    gamma_i gamma_j + gamma_j gamma_i =
        1  if |i-j| = 1,
        0  if |i-j| > 1.

Thus, for the simple-root basis alpha_i=e_i+e_{i+1} of the even-weight
point space V, c(sum a_i alpha_i)=sum a_i gamma_i is Clifford
multiplication.  A nonzero spinor is called pure here when its Clifford
annihilator has dimension r in the plus-type cases r=3 and r=15.  (The
r=5 natural quadratic space is minus type and has Witt index 4; genuine
Witt differences are zero, so the script draws no nonzero purity evidence
from that case.)

The exact conclusions are:

* r=3: every nonzero difference of two mates of a fixed Fano plane is a
  pure spinor.  The seven quotient classes have q=0 and annihilator
  dimension 3.  In contrast, the eight affine classes x_A+x_B are
  anisotropic and have zero annihilator.
* r=5: all 5,040 labelled Witt systems have one common class modulo the
  radical, so every difference of two such systems is zero in S.  This
  makes the pure-spin test vacuous on genuine Witt differences.
* The recorded r=5 odd shaped-kernel counterexample is nonzero in S,
  anisotropic, and has zero Clifford annihilator.  Hence a proposed
  "zero or pure" mate constraint is genuinely stronger than the ambient
  support and shaped-kernel equations.

This is a finite audit, not a proof of the corresponding r=15 statement.
"""

from collections import Counter, deque
from itertools import combinations

try:
    from verify_r5_odd_witness import WITNESS
    from verify_saturated_support_lattice import (
        build_restricted_matrix,
        enumerate_disjoint_mates,
        exact_cover,
        gf2_rank,
        nullspace_binary,
        parity,
        saturated_integer_kernel,
    )
except ModuleNotFoundError:
    from evidence.verify_r5_odd_witness import WITNESS
    from evidence.verify_saturated_support_lattice import (
        build_restricted_matrix,
        enumerate_disjoint_mates,
        exact_cover,
        gf2_rank,
        nullspace_binary,
        parity,
        saturated_integer_kernel,
    )


def weight(word):
    return bin(int(word)).count("1")


def apply_matrix(columns, vector):
    """Apply a bit-packed binary matrix stored by columns."""
    answer = 0
    cursor = vector
    while cursor:
        low_bit = cursor & -cursor
        answer ^= columns[low_bit.bit_length() - 1]
        cursor ^= low_bit
    return answer


def compose(left, right):
    return [apply_matrix(left, column) for column in right]


def matrix_sum(left, right):
    return [a ^ b for a, b in zip(left, right)]


def coordinates_in_basis(basis, vector):
    """Express vector in a full bit-packed binary basis."""
    pivots = {}
    for i, basis_vector in enumerate(basis):
        remainder = basis_vector
        tag = 1 << i
        while remainder:
            pivot = remainder.bit_length() - 1
            if pivot in pivots:
                old_vector, old_tag = pivots[pivot]
                remainder ^= old_vector
                tag ^= old_tag
            else:
                pivots[pivot] = (remainder, tag)
                break
        assert remainder

    remainder = vector
    tag = 0
    while remainder:
        pivot = remainder.bit_length() - 1
        assert pivot in pivots
        basis_vector, basis_tag = pivots[pivot]
        remainder ^= basis_vector
        tag ^= basis_tag
    return tag


def insert_tagged_basis(pivots, vector, tag):
    """Insert an ambient word while tracking its quotient coordinate."""
    while vector:
        pivot = vector.bit_length() - 1
        if pivot in pivots:
            basis_vector, basis_tag = pivots[pivot]
            vector ^= basis_vector
            tag ^= basis_tag
        else:
            pivots[pivot] = (vector, tag)
            return True
    return False


class SpinQuotient:
    """Exact quotient C/rad(C), with its permutation and Clifford actions."""

    def __init__(self, r):
        self.r = r
        self.n = 2 * r + 1
        (
            self.restricted_matrix,
            self.blocks,
            self.base,
            self.outside,
        ) = build_restricted_matrix(self.n, r)
        self.block_index = {
            block: i for i, block in enumerate(self.blocks)
        }

        facets = [
            frozenset(facet)
            for facet in combinations(range(self.n), r - 1)
        ]
        full_matrix = [
            [int(facet <= block) for block in self.blocks]
            for facet in facets
        ]
        integer_basis, _rank = saturated_integer_kernel(full_matrix)
        self.code_basis = [
            sum((entry & 1) << i for i, entry in enumerate(vector))
            for vector in integer_basis
        ]

        gram_rows = [
            sum(
                parity(left & right) << j
                for j, right in enumerate(self.code_basis)
            )
            for left in self.code_basis
        ]
        radical_coefficients = nullspace_binary(
            gram_rows, len(self.code_basis)
        )
        self.radical_basis = []
        for coefficients in radical_coefficients:
            word = 0
            for i, codeword in enumerate(self.code_basis):
                if (coefficients >> i) & 1:
                    word ^= codeword
            self.radical_basis.append(word)

        # First insert the radical with tag zero, then extend it to C.
        self._tagged_pivots = {}
        for word in self.radical_basis:
            assert insert_tagged_basis(self._tagged_pivots, word, 0)

        self.quotient_basis = []
        for word in self.code_basis:
            remainder = word
            while remainder:
                pivot = remainder.bit_length() - 1
                if pivot not in self._tagged_pivots:
                    break
                remainder ^= self._tagged_pivots[pivot][0]
            if remainder:
                coordinate = 1 << len(self.quotient_basis)
                self.quotient_basis.append(word)
                assert insert_tagged_basis(
                    self._tagged_pivots, word, coordinate
                )

        self.dimension = len(self.quotient_basis)
        assert self.dimension == 2 ** r
        assert all(
            self.coordinate(word) == 1 << i
            for i, word in enumerate(self.quotient_basis)
        )

        self.gamma = [
            [
                self.coordinate(
                    self._adjacent_transposition(word, point)
                )
                for word in self.quotient_basis
            ]
            for point in range(2 * r)
        ]
        self._verify_clifford_relations()

    def coordinate(self, word):
        """Return the coordinate of a stable word modulo the radical."""
        tag = 0
        remainder = word
        while remainder:
            pivot = remainder.bit_length() - 1
            assert pivot in self._tagged_pivots
            basis_vector, basis_tag = self._tagged_pivots[pivot]
            remainder ^= basis_vector
            tag ^= basis_tag
        return tag

    def lift_coordinate(self, coordinate):
        """Choose the quotient-basis representative in the ambient code."""
        word = 0
        cursor = coordinate
        while cursor:
            low_bit = cursor & -cursor
            word ^= self.quotient_basis[low_bit.bit_length() - 1]
            cursor ^= low_bit
        return word

    def quadratic(self, coordinate):
        word = self.lift_coordinate(coordinate)
        assert weight(word) % 2 == 0
        return (weight(word) // 2) & 1

    def polar(self, left, right):
        return parity(
            self.lift_coordinate(left) & self.lift_coordinate(right)
        )

    def block_word(self, design):
        return sum(1 << self.block_index[block] for block in design)

    def _adjacent_transposition(self, word, point):
        permutation = {point: point + 1, point + 1: point}
        answer = 0
        cursor = word
        while cursor:
            low_bit = cursor & -cursor
            block = self.blocks[low_bit.bit_length() - 1]
            image = frozenset(permutation.get(x, x) for x in block)
            answer ^= 1 << self.block_index[image]
            cursor ^= low_bit
        return answer

    def _verify_clifford_relations(self):
        identity = [1 << i for i in range(self.dimension)]
        zero = [0] * self.dimension
        for generator in self.gamma:
            assert compose(generator, generator) == identity
        for i, left in enumerate(self.gamma):
            for j, right in enumerate(self.gamma[i + 1:], i + 1):
                anticommutator = matrix_sum(
                    compose(left, right),
                    compose(right, left),
                )
                assert anticommutator == (
                    identity if j == i + 1 else zero
                )

    def clifford_matrix(self, simple_root_coefficients):
        answer = [0] * self.dimension
        for i, generator in enumerate(self.gamma):
            if (simple_root_coefficients >> i) & 1:
                answer = matrix_sum(answer, generator)
        return answer

    def point_vector(self, simple_root_coefficients):
        """Convert simple-root coordinates to an even point subset."""
        answer = 0
        for i in range(2 * self.r):
            if (simple_root_coefficients >> i) & 1:
                answer ^= (1 << i) | (1 << (i + 1))
        return answer

    def natural_quadratic(self, simple_root_coefficients):
        return (weight(self.point_vector(simple_root_coefficients)) // 2) & 1

    def annihilator_dimension(self, spinor):
        images = [
            apply_matrix(generator, spinor)
            for generator in self.gamma
        ]
        return 2 * self.r - gf2_rank(images)

    def verify_singular_images_are_totally_singular(self):
        """Check the Clifford implication Ann(psi)>0 => q(psi)=0.

        For each nonzero singular v in the natural module, im c(v) is
        checked to be a totally singular subspace of the spin module.
        Since c(v)^2=0 and a complementary w gives
        c(v)c(w)+c(w)c(v)=1, ker c(v)=im c(v).
        """
        identity = [1 << i for i in range(self.dimension)]
        zero = [0] * self.dimension
        for coefficients in range(1, 1 << (2 * self.r)):
            clifford = self.clifford_matrix(coefficients)
            square = compose(clifford, clifford)
            assert square == (
                identity if self.natural_quadratic(coefficients) else zero
            )
            if self.natural_quadratic(coefficients):
                continue
            image_basis = []
            pivots = {}
            for column in clifford:
                remainder = column
                while remainder:
                    pivot = remainder.bit_length() - 1
                    if pivot in pivots:
                        remainder ^= pivots[pivot]
                    else:
                        pivots[pivot] = remainder
                        image_basis.append(remainder)
                        break
            assert all(self.quadratic(vector) == 0 for vector in image_basis)
            assert all(
                self.polar(left, right) == 0
                for i, left in enumerate(image_basis)
                for right in image_basis[i + 1:]
            )


def enumerate_witt_orbit(quotient):
    """Generate all 5,040 labelled Witt systems by adjacent swaps."""
    assert quotient.r == 5
    start = tuple(
        sorted(
            sum(1 << point for point in block)
            for block in quotient.base
        )
    )

    def swap_block(block, point):
        left = (block >> point) & 1
        right = (block >> (point + 1)) & 1
        if left == right:
            return block
        return block ^ (1 << point) ^ (1 << (point + 1))

    seen = {start}
    pending = deque([start])
    while pending:
        design = pending.popleft()
        for point in range(quotient.n - 1):
            image = tuple(
                sorted(swap_block(block, point) for block in design)
            )
            if image not in seen:
                seen.add(image)
                pending.append(image)
    assert len(seen) == 5040
    return seen


def audit_r3():
    quotient = SpinQuotient(3)
    quotient.verify_singular_images_are_totally_singular()
    assert (
        len(quotient.code_basis),
        len(quotient.radical_basis),
        quotient.dimension,
    ) == (14, 6, 8)

    # Enumerate the full eight-dimensional quotient.  Purity is strictly
    # stronger than q=0: 30 of the 135 nonzero singular vectors are pure.
    full_distribution = Counter()
    for spinor in range(1, 1 << quotient.dimension):
        full_distribution[(
            quotient.annihilator_dimension(spinor),
            quotient.quadratic(spinor),
        )] += 1
    assert full_distribution == Counter({
        (0, 1): 120,
        (2, 0): 105,
        (3, 0): 30,
    })

    # Enumerate all 30 labelled Fano planes.  This gives an intrinsic
    # three-way characterization: a pair has a common disjoint Fano plane
    # exactly when its difference is pure.  Such a pair has four common
    # disjoint bases.
    facets = [
        frozenset(facet)
        for facet in combinations(range(quotient.n), quotient.r - 1)
    ]
    facet_index = {facet: i for i, facet in enumerate(facets)}
    rows = {
        j: tuple(
            facet_index[frozenset(facet)]
            for facet in combinations(block, quotient.r - 1)
        )
        for j, block in enumerate(quotient.blocks)
    }
    columns = {i: set() for i in range(len(facets))}
    for j, incident in rows.items():
        for i in incident:
            columns[i].add(j)
    solutions = exact_cover(
        {i: set(candidates) for i, candidates in columns.items()},
        rows,
    )
    all_fanos = [
        frozenset(quotient.blocks[j] for j in solution)
        for solution in solutions
    ]
    assert len(all_fanos) == 30
    all_fano_words = [
        quotient.block_word(design) for design in all_fanos
    ]
    pair_types = Counter()
    common_base_types = Counter()
    for i, j in combinations(range(len(all_fanos)), 2):
        spinor = quotient.coordinate(
            all_fano_words[i] ^ all_fano_words[j]
        )
        intersection = len(all_fanos[i] & all_fanos[j])
        annihilator = quotient.annihilator_dimension(spinor)
        pair_types[(
            intersection,
            quotient.quadratic(spinor),
            annihilator,
        )] += 1
        common_bases = sum(
            int(
                not (base & all_fanos[i])
                and not (base & all_fanos[j])
            )
            for base in all_fanos
        )
        common_base_types[(intersection, common_bases)] += 1
        assert (common_bases > 0) == (
            spinor != 0 and annihilator == quotient.r
        )
    assert pair_types == Counter({
        (0, 1, 0): 120,
        (1, 0, 3): 210,
        (3, 0, 2): 105,
    })
    assert common_base_types == Counter({
        (0, 0): 120,
        (1, 4): 210,
        (3, 0): 105,
    })

    mates = enumerate_disjoint_mates(
        quotient.blocks, quotient.base, quotient.r
    )
    assert len(mates) == 8
    base_word = quotient.block_word(quotient.base)
    mate_words = [quotient.block_word(mate) for mate in mates]

    states = {
        quotient.coordinate(base_word ^ mate_word)
        for mate_word in mate_words
    }
    assert len(states) == 8
    assert all(quotient.quadratic(state) == 1 for state in states)
    assert all(
        quotient.annihilator_dimension(state) == 0
        for state in states
    )

    pair_classes = Counter()
    for i, left in enumerate(mate_words):
        for right in mate_words[i + 1:]:
            spinor = quotient.coordinate(left ^ right)
            assert spinor != 0
            assert quotient.quadratic(spinor) == 0
            assert quotient.annihilator_dimension(spinor) == 3
            pair_classes[spinor] += 1
    assert len(pair_classes) == 7
    assert set(pair_classes.values()) == {4}

    # The support image is a four-space.  It contains both pure and
    # non-pure singular vectors, so the pure constraint is not merely the
    # linear support condition or a renaming of q=0.
    support_basis, _rank = saturated_integer_kernel(
        quotient.restricted_matrix
    )
    support_generators = []
    for vector in support_basis:
        word = 0
        for block_index, entry in zip(quotient.outside, vector):
            if entry & 1:
                word ^= 1 << block_index
        support_generators.append(quotient.coordinate(word))
    assert gf2_rank(support_generators) == 4
    support_space = {0}
    for generator in support_generators:
        support_space |= {
            vector ^ generator for vector in list(support_space)
        }
    assert len(support_space) == 16
    support_distribution = Counter(
        quotient.annihilator_dimension(vector)
        for vector in support_space
        if vector
    )
    assert support_distribution == Counter({3: 8, 2: 7})

    # Explicit all-odd shaped counterexample to deriving purity from the
    # *linear* moment equations.  The entries are
    # (base block, plus missing point, minus missing point); None denotes
    # the one inactive sphere.
    shaped_certificate = [
        ((0, 1, 2), None, None),
        ((0, 3, 4), 1, 2),
        ((0, 5, 6), 2, 1),
        ((1, 3, 5), 6, 4),
        ((1, 4, 6), 5, 3),
        ((2, 3, 6), 4, 5),
        ((2, 4, 5), 3, 6),
    ]
    points = frozenset(range(quotient.n))
    base_by_tuple = {
        tuple(sorted(block)): block for block in quotient.base
    }
    integer_trade = {}
    for block_tuple, plus_point, minus_point in shaped_certificate:
        base_block = base_by_tuple[block_tuple]
        if plus_point is None:
            assert minus_point is None
            continue
        plus_block = points - base_block - {plus_point}
        minus_block = points - base_block - {minus_point}
        integer_trade[plus_block] = 1
        integer_trade[minus_block] = -1
    assert len(integer_trade) == 12
    for size in range(quotient.r):
        for subset in combinations(range(quotient.n), size):
            subset = frozenset(subset)
            assert sum(
                coefficient
                for block, coefficient in integer_trade.items()
                if subset <= block
            ) == 0
    shaped_word = sum(
        1 << quotient.block_index[block]
        for block in integer_trade
    )
    shaped_spinor = quotient.coordinate(shaped_word)
    assert quotient.quadratic(shaped_spinor) == 0
    assert quotient.annihilator_dimension(shaped_spinor) == 2

    # Make the failed pure-spin equation completely explicit.  The following
    # simple-root coefficient vectors form a hyperbolic basis E_i,F_i of the
    # six-dimensional natural quadratic space.  In point-subset notation,
    #
    #   E = (0123, 0145, 1256),
    #   F = (1234, 0245, 0346).
    #
    # A common Clifford kernel of E is the one-dimensional vacuum line.
    # Applying subsets of the F_i gives the Fock basis indexed by I <= {1,2,3}.
    hyperbolic_e = [5, 17, 34]
    hyperbolic_f = [10, 19, 55]
    for vector in hyperbolic_e + hyperbolic_f:
        assert quotient.natural_quadratic(vector) == 0
    for family in (hyperbolic_e, hyperbolic_f):
        for left, right in combinations(family, 2):
            assert (
                quotient.natural_quadratic(left ^ right)
                ^ quotient.natural_quadratic(left)
                ^ quotient.natural_quadratic(right)
            ) == 0
    for i, left in enumerate(hyperbolic_e):
        for j, right in enumerate(hyperbolic_f):
            assert (
                quotient.natural_quadratic(left ^ right)
                ^ quotient.natural_quadratic(left)
                ^ quotient.natural_quadratic(right)
            ) == int(i == j)

    vacua = [
        spinor
        for spinor in range(1, 1 << quotient.dimension)
        if all(
            apply_matrix(quotient.clifford_matrix(vector), spinor) == 0
            for vector in hyperbolic_e
        )
    ]
    assert vacua == [50]
    fock_basis = []
    for subset in range(1 << quotient.r):
        spinor = vacua[0]
        for i, vector in enumerate(hyperbolic_f):
            if (subset >> i) & 1:
                spinor = apply_matrix(
                    quotient.clifford_matrix(vector), spinor
                )
        fock_basis.append(spinor)
    assert gf2_rank(fock_basis) == quotient.dimension

    # The shaped certificate is p_{1} + p_{12}.  Hence it violates the
    # mixed-chirality pure-spin equation p_{1} p_{12}=0 explicitly.
    shaped_fock = coordinates_in_basis(fock_basis, shaped_spinor)
    assert shaped_fock == (1 << 1) | (1 << 3)

    # In the same polarization, every genuine mate-pair difference for the
    # fixed base lies wholly in the even half-spin summand.
    for left, right in combinations(mate_words, 2):
        fock = coordinates_in_basis(
            fock_basis, quotient.coordinate(left ^ right)
        )
        assert all(
            weight(subset) % 2 == 0
            for subset in range(1 << quotient.r)
            if (fock >> subset) & 1
        )

    # Filling the inactive sphere identically on the two sides never even
    # gives the correct point degrees, so the certificate does not satisfy
    # the nonlinear endpoint design equations.
    inactive_block = base_by_tuple[(0, 1, 2)]
    for common_point in points - inactive_block:
        plus_side = [
            block for block, coefficient in integer_trade.items()
            if coefficient == 1
        ] + [points - inactive_block - {common_point}]
        point_degrees = [
            sum(point in block for block in plus_side)
            for point in range(quotient.n)
        ]
        assert point_degrees != [3] * quotient.n

    print("r=3 quotient: dimension 8, Clifford relations verified")
    print(
        "r=3 nonzero spinors by (annihilator dimension, q):",
        dict(sorted(full_distribution.items())),
    )
    print(
        "r=3 all Fano pairs by (intersection, q, annihilator):",
        dict(sorted(pair_types.items())),
    )
    print(
        "r=3 common-base characterization:",
        "pure iff a common disjoint Fano exists",
    )
    print(
        "r=3 mate-pair classes: 7 nonzero pure classes,",
        "each attained by 4 of 28 pairs",
    )
    print(
        "r=3 support four-space: nonzero annihilator distribution",
        dict(sorted(support_distribution.items())),
    )
    print(
        "r=3 shaped linear-moment certificate:",
        "q=0 but annihilator dimension 2; Fock state p_1 + p_12",
    )


def audit_r5():
    quotient = SpinQuotient(5)
    quotient.verify_singular_images_are_totally_singular()
    assert (
        len(quotient.code_basis),
        len(quotient.radical_basis),
        quotient.dimension,
    ) == (132, 100, 32)

    # All labelled Witt systems lie in one affine radical coset.
    orbit = enumerate_witt_orbit(quotient)
    mask_to_index = {
        sum(1 << point for point in block): i
        for i, block in enumerate(quotient.blocks)
    }
    base_word = quotient.block_word(quotient.base)
    intersection_distribution = Counter()
    for design in orbit:
        word = sum(1 << mask_to_index[block] for block in design)
        assert quotient.coordinate(base_word ^ word) == 0
        intersection_distribution[weight(base_word & word)] += 1
    assert intersection_distribution == Counter({
        0: 144,
        6: 2574,
        12: 1760,
        18: 495,
        30: 66,
        66: 1,
    })

    # The support image is the full spin quotient.
    support_basis, _rank = saturated_integer_kernel(
        quotient.restricted_matrix
    )
    support_generators = []
    for vector in support_basis:
        word = 0
        for block_index, entry in zip(quotient.outside, vector):
            if entry & 1:
                word ^= 1 << block_index
        support_generators.append(quotient.coordinate(word))
    assert gf2_rank(support_generators) == 32

    # The known shaped-kernel false positive is anisotropic and has no
    # Clifford annihilator.
    points = frozenset(range(quotient.n))
    witness_word = 0
    for base_block, plus_point, minus_point in WITNESS:
        base_block = frozenset(base_block)
        plus_block = points - base_block - {plus_point}
        minus_block = points - base_block - {minus_point}
        witness_word ^= 1 << quotient.block_index[plus_block]
        witness_word ^= 1 << quotient.block_index[minus_block]
    witness_spinor = quotient.coordinate(witness_word)
    assert witness_spinor != 0
    assert quotient.quadratic(witness_spinor) == 1
    assert quotient.annihilator_dimension(witness_spinor) == 0

    print("r=5 quotient: dimension 32, Clifford relations verified")
    print(
        "r=5 all 5,040 labelled Witt systems have one spin class;",
        "intersection distribution =", dict(sorted(
            intersection_distribution.items()
        )),
    )
    print("r=5 support image has full dimension 32")
    print(
        "r=5 odd shaped witness: nonzero, q=1,",
        "Clifford annihilator dimension 0",
    )


def main():
    audit_r3()
    audit_r5()
    print("ALL NONLINEAR SPIN-MATE CHECKS PASSED")


if __name__ == "__main__":
    main()
