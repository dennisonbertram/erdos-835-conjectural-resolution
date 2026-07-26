#!/usr/bin/env python3
"""Emit the exact LP for the (0,9,9,13) shortened-code third moment.

This script originally tested a proposed obstruction based on the false
premise that the shortened even point code had dual A_3 = 0.  Its exact
optimum is instead a bound on the positive number of triangle dependencies.
The solver-free proof artifact is
``verify_s141531_triangle_third_moment.py``.
"""

from collections import defaultdict
from itertools import product
from math import comb


POINTS = 31
DESIGN_T = 14
BLOCK_SIZE = 15
BLOCKS = comb(POINTS, DESIGN_T) // BLOCK_SIZE
MIDDLE_CORRECTION = 1 << BLOCK_SIZE
H_COUNTS = (0, 9, 9, 13)
H_ORDER = 4
QUOTIENT_DIMENSION = 28
QUOTIENT_SIZE = 1 << QUOTIENT_DIMENSION

LAMBDA = tuple(
    comb(POINTS - level, DESIGN_T - level) // (BLOCK_SIZE - level)
    for level in range(DESIGN_T + 1)
)


def fourier_external(size: int) -> int:
    if size > BLOCK_SIZE:
        return -fourier_external(POINTS - size)
    return sum(
        (-2) ** level * comb(size, level) * LAMBDA[level]
        for level in range(min(size, DESIGN_T) + 1)
    )


FOURIER_LOWER = tuple(fourier_external(size) for size in range(POINTS + 1))


def dot(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def coset_types():
    weights_h = tuple(
        sum(H_COUNTS[column] for column in range(H_ORDER) if dot(word, column))
        for word in range(H_ORDER)
    )
    base_sum = sum(FOURIER_LOWER[weight] for weight in weights_h)
    length = base_sum // H_ORDER
    types = defaultdict(int)

    for profile in product(*(range(count + 1) for count in H_COUNTS)):
        if sum(profile) & 1:
            continue
        multiplicity = 1
        for count, selected in zip(H_COUNTS, profile):
            multiplicity *= comb(count, selected)
        weights = tuple(
            sum(
                H_COUNTS[column] - profile[column]
                if dot(word, column)
                else profile[column]
                for column in range(H_ORDER)
            )
            for word in range(H_ORDER)
        )
        translated_sum = sum(FOURIER_LOWER[weight] for weight in weights)
        numerator = base_sum - translated_sum
        assert numerator % (2 * H_ORDER) == 0
        base_weight = numerator // (2 * H_ORDER)
        capacity = weights.count(BLOCK_SIZE + 1)
        types[(base_weight, capacity)] += multiplicity

    for key in tuple(types):
        assert types[key] % H_ORDER == 0
        types[key] //= H_ORDER
    assert sum(types.values()) == QUOTIENT_SIZE
    return length, dict(sorted(types.items()))


def linear_expression(terms):
    pieces = []
    for coefficient, variable in terms:
        if coefficient == 0:
            continue
        sign = "+" if coefficient > 0 else "-"
        magnitude = abs(coefficient)
        atom = variable if magnitude == 1 else f"{magnitude} {variable}"
        if not pieces:
            pieces.append(atom if coefficient > 0 else f"- {atom}")
        else:
            pieces.append(f" {sign} {atom}")
    return "".join(pieces) if pieces else "0"


def main():
    length, types = coset_types()
    variables = {
        (base_weight, capacity, internal): (
            f"y_{base_weight}_{capacity}_{internal}"
        )
        for base_weight, capacity in types
        for internal in range(capacity + 1)
    }

    print("Maximize")
    objective = []
    for (base_weight, capacity, internal), variable in variables.items():
        weight = base_weight - (MIDDLE_CORRECTION // (2 * H_ORDER)) * internal
        centered = 2 * weight - length
        objective.append((centered**3, variable))
    print(" third:", linear_expression(objective))
    print("Subject To")

    for index, ((base_weight, capacity), multiplicity) in enumerate(types.items()):
        terms = [
            (1, variables[base_weight, capacity, internal])
            for internal in range(capacity + 1)
        ]
        print(f" type_{index}:", linear_expression(terms), "=", multiplicity)

    internal_terms = [
        (internal, variable)
        for (base_weight, capacity, internal), variable in variables.items()
    ]
    print(" total_internal:", linear_expression(internal_terms), "=", BLOCKS)

    first_terms = []
    second_terms = []
    for (base_weight, capacity, internal), variable in variables.items():
        weight = base_weight - (MIDDLE_CORRECTION // (2 * H_ORDER)) * internal
        centered = 2 * weight - length
        first_terms.append((centered, variable))
        second_terms.append((centered**2, variable))
    print(" moment_1:", linear_expression(first_terms), "=", 0)
    print(
        " moment_2:",
        linear_expression(second_terms),
        "=",
        QUOTIENT_SIZE * length,
    )

    print("Bounds")
    for variable in variables.values():
        print(" 0 <=", variable)
    print("End")


if __name__ == "__main__":
    main()
