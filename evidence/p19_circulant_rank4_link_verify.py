#!/usr/bin/env python3
"""Exact exhaustion of arbitrarily lifted circulant rank-four links.

For n=p+1, an alternating circulant matrix has entries

    B[i,j] = f(j-i),  f(-d) = -f(d).

Over F_(p^2), its Fourier support occurs in pairs {a,-a}.  Each nonzero
pair contributes rank two.  This script enumerates every projective matrix
with at most two such pairs.  It then allows an arbitrary nonzero diagonal
congruence B -> D B D (independent vector-lift scalings) and proves that the
necessary sign-class system is inconsistent modulo three at p=19.
"""

from __future__ import annotations

from itertools import combinations, permutations, product
from random import Random


def prime_factors(value: int) -> list[int]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root_prime(prime: int) -> int:
    factors = prime_factors(prime - 1)
    return next(
        candidate
        for candidate in range(2, prime)
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        )
    )


class QuadraticField:
    def __init__(self, prime: int) -> None:
        self.prime = prime
        self.nonsquare = next(
            value
            for value in range(2, prime)
            if pow(value, (prime - 1) // 2, prime) == prime - 1
        )

    def add(self, left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
        return (
            (left[0] + right[0]) % self.prime,
            (left[1] + right[1]) % self.prime,
        )

    def negative(self, value: tuple[int, int]) -> tuple[int, int]:
        return (-value[0] % self.prime, -value[1] % self.prime)

    def multiply(
        self, left: tuple[int, int], right: tuple[int, int]
    ) -> tuple[int, int]:
        return (
            (
                left[0] * right[0]
                + self.nonsquare * left[1] * right[1]
            )
            % self.prime,
            (left[0] * right[1] + left[1] * right[0]) % self.prime,
        )

    def power(self, value: tuple[int, int], exponent: int) -> tuple[int, int]:
        answer = (1, 0)
        while exponent:
            if exponent & 1:
                answer = self.multiply(answer, value)
            value = self.multiply(value, value)
            exponent //= 2
        return answer

    def primitive(self) -> tuple[int, int]:
        order = self.prime * self.prime - 1
        factors = prime_factors(order)
        return next(
            (a, b)
            for a in range(self.prime)
            for b in range(self.prime)
            if (a, b) != (0, 0)
            and all(
                self.power((a, b), order // factor) != (1, 0)
                for factor in factors
            )
        )


def signless_rainbow(values: list[int], prime: int) -> bool:
    half = (prime - 1) // 2
    classes = [min(values[d], prime - values[d]) for d in range(1, half + 1)]
    return sorted(classes) == list(range(1, half + 1))


def matrix_rank(matrix: list[list[int]], prime: int) -> int:
    work = [[value % prime for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [value * inverse % prime for value in work[rank]]
        for row in range(rank + 1, len(work)):
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
    return rank


def ternary_consistent(
    equations: list[tuple[int, int]], variables: int
) -> bool:
    """Exact Gaussian consistency over F_3 using two bit planes."""

    width = variables + 1  # The final bit is the right-hand side.
    full = (1 << width) - 1
    rows = list(equations)

    def add(
        left: tuple[int, int], right: tuple[int, int]
    ) -> tuple[int, int]:
        left_one, left_two = left
        right_one, right_two = right
        left_zero = full ^ (left_one | left_two)
        right_zero = full ^ (right_one | right_two)
        one = (
            (left_zero & right_one)
            | (left_one & right_zero)
            | (left_two & right_two)
        )
        two = (
            (left_zero & right_two)
            | (left_two & right_zero)
            | (left_one & right_one)
        )
        assert one & two == 0
        return one, two

    pivot_row = 0
    for column in range(variables):
        bit = 1 << column
        pivot = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if (rows[row][0] | rows[row][1]) & bit
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        if rows[pivot_row][1] & bit:
            rows[pivot_row] = rows[pivot_row][1], rows[pivot_row][0]
        negative_pivot = rows[pivot_row][1], rows[pivot_row][0]
        for row in range(pivot_row + 1, len(rows)):
            if rows[row][0] & bit:
                rows[row] = add(rows[row], negative_pivot)
            elif rows[row][1] & bit:
                rows[row] = add(rows[row], rows[pivot_row])
        pivot_row += 1

    variable_mask = (1 << variables) - 1
    rhs_bit = 1 << variables
    return not any(
        ((one | two) & variable_mask) == 0 and ((one | two) & rhs_bit)
        for one, two in rows
    )


def audit_ternary_elimination() -> None:
    random = Random(83519)
    for variables in range(1, 6):
        for _ in range(40):
            dense = [
                [random.randrange(3) for _ in range(variables + 1)]
                for _ in range(random.randrange(1, 9))
            ]
            equations = []
            for row in dense:
                one = sum(1 << index for index, value in enumerate(row) if value == 1)
                two = sum(1 << index for index, value in enumerate(row) if value == 2)
                equations.append((one, two))
            brute = any(
                all(
                    sum(coefficient * value for coefficient, value in zip(row[:-1], assignment))
                    % 3
                    == row[-1]
                    for row in dense
                )
                for assignment in product(range(3), repeat=variables)
            )
            assert ternary_consistent(equations, variables) == brute


def scaling_relaxation_consistent(values: list[int], prime: int) -> bool:
    """Necessary independent row-scaling equations, reduced modulo three."""

    size = prime + 1
    half = (prime - 1) // 2
    variables = size * half
    rhs_bit = 1 << variables
    generator = primitive_root_prime(prime)
    logarithm = [-1] * prime
    power = 1
    for exponent in range(prime - 1):
        logarithm[power] = exponent % half
        power = power * generator % prime
    assert all(value >= 0 for value in logarithm[1:])

    equations: list[tuple[int, int]] = []
    for vertex in range(size):
        coefficients = sum(
            1 << (vertex * half + residue) for residue in range(half)
        )
        equations.append((coefficients | rhs_bit, 0))

    # A common shift of all lift exponents preserves uniformity.
    for residue in range(half):
        coefficient = 1 << residue
        equations.append(
            (coefficient | rhs_bit, 0)
            if residue == 0
            else (coefficient, 0)
        )

    for left in range(size):
        for residue in range(half):
            coefficients = 0
            for right in range(size):
                if left == right:
                    continue
                value = values[(right - left) % size]
                if value == 0:
                    continue
                required = (residue - logarithm[value]) % half
                coefficients |= 1 << (right * half + required)
            # The required multiplicity is 2, represented in the second
            # ternary bit plane.
            equations.append((coefficients, rhs_bit))
    return ternary_consistent(equations, variables)


def admits_order(values: list[int], prime: int) -> bool:
    size = prime + 1
    for order in permutations(range(size)):
        works = True
        for position in range(size):
            colours = set()
            for other in range(size):
                if other == position:
                    continue
                lower = min(position, other)
                upper = max(position, other)
                difference = (order[upper] - order[lower]) % size
                colours.add(values[difference])
            if len(colours) != prime:
                works = False
                break
        if works:
            return True
    return False


def exhaust(prime: int) -> tuple[int, int, int, int, int, int]:
    field = QuadraticField(prime)
    size = prime + 1
    half = (prime - 1) // 2
    primitive = field.primitive()
    root = field.power(primitive, prime - 1)
    assert field.power(root, size) == (1, 0)
    trace_zero = (0, 1)

    def sine(frequency: int, difference: int) -> int:
        positive = field.power(root, frequency * difference % size)
        negative = field.power(root, -frequency * difference % size)
        value = field.multiply(
            trace_zero,
            field.add(negative, field.negative(positive)),
        )
        assert value[1] == 0
        return value[0]

    basis = [
        [sine(frequency, difference) for difference in range(size)]
        for frequency in range(1, half + 1)
    ]
    survivors: list[list[int]] = []
    zero_pattern = 0
    scaled_linear_survivors = 0

    # One Fourier pair: common nonzero scaling is projectively irrelevant.
    for values in basis:
        assert values[0] == values[size // 2] == 0
        assert all(
            values[size - difference] == -values[difference] % prime
            for difference in range(1, size // 2)
        )
        matrix = [
            [values[(column - row) % size] for column in range(size)]
            for row in range(size)
        ]
        assert matrix_rank(matrix, prime) == 2
        has_zero_pattern = all(values[d] for d in range(1, half + 1))
        zero_pattern += has_zero_pattern
        if has_zero_pattern and scaling_relaxation_consistent(values, prime):
            scaled_linear_survivors += 1
        if signless_rainbow(values, prime):
            survivors.append(values)

    # Two Fourier pairs: normalize the first coefficient to one, and range
    # over every nonzero ratio for the second.
    for first, second in combinations(range(half), 2):
        for ratio in range(1, prime):
            values = [
                (basis[first][d] + ratio * basis[second][d]) % prime
                for d in range(size)
            ]
            matrix = [
                [values[(column - row) % size] for column in range(size)]
                for row in range(size)
            ]
            assert matrix_rank(matrix, prime) == 4
            has_zero_pattern = all(values[d] for d in range(1, half + 1))
            zero_pattern += has_zero_pattern
            if has_zero_pattern and scaling_relaxation_consistent(values, prime):
                scaled_linear_survivors += 1
            if signless_rainbow(values, prime):
                survivors.append(values)

    projective_matrices = half + (half * (half - 1) // 2) * (prime - 1)
    ordered = (
        sum(admits_order(values, prime) for values in survivors)
        if prime <= 5
        else 0
    )
    return (
        projective_matrices,
        zero_pattern,
        scaled_linear_survivors,
        len(survivors),
        ordered,
        half,
    )


def main() -> None:
    audit_ternary_elimination()
    results = {prime: exhaust(prime) for prime in (3, 5, 7, 11, 19)}
    assert results == {
        3: (1, 1, 1, 1, 1, 1),
        5: (6, 4, 4, 2, 0, 2),
        7: (21, 14, 0, 0, 0, 3),
        11: (105, 66, 42, 0, 0, 5),
        19: (657, 380, 0, 0, 0, 9),
    }
    for (
        prime,
        (
            tested,
            zero_pattern,
            scaled_linear,
            signless,
            ordered,
            _,
        ),
    ) in results.items():
        suffix = f" ordered={ordered}" if prime <= 5 else ""
        print(
            f"p={prime}: projective_rank<=4={tested} "
            f"zero_pattern={zero_pattern} "
            f"scaled_linear_mod3={scaled_linear} "
            f"unscaled_signless={signless}{suffix}"
        )
    print("circulant rank-at-most-four link exhaustion: PASS")


if __name__ == "__main__":
    main()
