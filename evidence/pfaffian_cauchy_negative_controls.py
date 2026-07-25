#!/usr/bin/env python3
"""Exact adverse controls for trace-Cauchy Pfaffian colourings.

For p in {7,11}, work in F_{p^2}.  Let H be the subgroup of order
2(p-1) and take the coset gH, where g is primitive.  This gives exactly
2p-2 points and avoids all Cauchy poles x_i x_j=1.  For every F_p-linear
trace direction lambda (one representative for each point of P^1(F_p)),
we test both natural descents of the Cauchy kernel:

   M_ij = Tr(lambda * (x_i-x_j)/(1-x_i*x_j)),   i<j,
   c(S) = Pf(M[S]).

and

   c(S) = Tr(lambda * Pf_K(C[S])),
   C_ij = (x_i-x_j)/(1-x_i*x_j).

The program prints, and verifies, a non-rainbow (p-2)-star for every
trace direction in both families.  It is a control experiment, not a
no-go theorem for arbitrary skew matrices or arbitrary Pfaffian
constructions.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class QuadField:
    p: int
    nonsquare: int

    def add(self, x, y):
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)

    def neg(self, x):
        return ((-x[0]) % self.p, (-x[1]) % self.p)

    def sub(self, x, y):
        return self.add(x, self.neg(y))

    def mul(self, x, y):
        return (
            (x[0] * y[0] + self.nonsquare * x[1] * y[1]) % self.p,
            (x[0] * y[1] + x[1] * y[0]) % self.p,
        )

    def power(self, x, exponent):
        answer = (1, 0)
        while exponent:
            if exponent & 1:
                answer = self.mul(answer, x)
            x = self.mul(x, x)
            exponent >>= 1
        return answer

    def inverse(self, x):
        assert x != (0, 0)
        return self.power(x, self.p * self.p - 2)

    def trace(self, x):
        # conjugation is a+b sqrt(d) -> a-b sqrt(d)
        return 2 * x[0] % self.p

    def primitive_element(self):
        order = self.p * self.p - 1
        factors = prime_factors(order)
        for a in range(self.p):
            for b in range(self.p):
                candidate = (a, b)
                if candidate == (0, 0):
                    continue
                if all(self.power(candidate, order // q) != (1, 0) for q in factors):
                    return candidate
        raise AssertionError("no primitive element found")


def prime_factors(number):
    factors = []
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            factors.append(divisor)
            while number % divisor == 0:
                number //= divisor
        divisor += 1
    if number > 1:
        factors.append(number)
    return factors


def first_nonsquare(p):
    squares = {x * x % p for x in range(1, p)}
    return next(x for x in range(2, p) if x not in squares)


def pfaffian_mod(matrix, p):
    """Pfaffian of a skew matrix in the displayed coordinate order."""

    work = [row[:] for row in matrix]
    answer = 1
    for pivot in range(0, len(work), 2):
        mate = next(
            (j for j in range(pivot + 1, len(work)) if work[pivot][j] % p),
            None,
        )
        if mate is None:
            return 0
        if mate != pivot + 1:
            work[mate], work[pivot + 1] = work[pivot + 1], work[mate]
            for row in work:
                row[mate], row[pivot + 1] = row[pivot + 1], row[mate]
            answer = -answer
        edge = work[pivot][pivot + 1] % p
        answer = answer * edge % p
        inverse = pow(edge, -1, p)
        for i in range(pivot + 2, len(work)):
            for j in range(i + 1, len(work)):
                update = (
                    work[pivot][i] * work[pivot + 1][j]
                    - work[pivot][j] * work[pivot + 1][i]
                )
                work[i][j] = (work[i][j] - update * inverse) % p
                work[j][i] = -work[i][j] % p
    return answer % p


def pfaffian_quad(matrix, field):
    """The same pivoting Pfaffian algorithm, now over F_{p^2}."""

    work = [row[:] for row in matrix]
    answer = (1, 0)
    for pivot in range(0, len(work), 2):
        mate = next(
            (j for j in range(pivot + 1, len(work)) if work[pivot][j] != (0, 0)),
            None,
        )
        if mate is None:
            return (0, 0)
        if mate != pivot + 1:
            work[mate], work[pivot + 1] = work[pivot + 1], work[mate]
            for row in work:
                row[mate], row[pivot + 1] = row[pivot + 1], row[mate]
            answer = field.neg(answer)
        edge = work[pivot][pivot + 1]
        answer = field.mul(answer, edge)
        inverse = field.inverse(edge)
        for i in range(pivot + 2, len(work)):
            for j in range(i + 1, len(work)):
                update = field.sub(
                    field.mul(work[pivot][i], work[pivot + 1][j]),
                    field.mul(work[pivot][j], work[pivot + 1][i]),
                )
                work[i][j] = field.sub(work[i][j], field.mul(update, inverse))
                work[j][i] = field.neg(work[i][j])
    return answer


def cyclic_cauchy_points(field):
    p = field.p
    primitive = field.primitive_element()
    subgroup_order = 2 * (p - 1)
    generator = field.power(primitive, (p * p - 1) // subgroup_order)
    subgroup = [field.power(generator, exponent) for exponent in range(subgroup_order)]
    points = [field.mul(primitive, x) for x in subgroup]
    assert len(set(points)) == 2 * p - 2
    assert all(
        field.sub((1, 0), field.mul(x, y)) != (0, 0)
        for x, y in combinations(points, 2)
    )
    return points


def projective_trace_directions(p):
    # Representatives lambda=a+b sqrt(d), modulo F_p^*.
    return [(a, 1) for a in range(p)] + [(1, 0)]


def trace_cauchy_matrix(field, points, direction):
    size = len(points)
    matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            kernel = field.mul(
                field.sub(points[i], points[j]),
                field.inverse(field.sub((1, 0), field.mul(points[i], points[j]))),
            )
            value = field.trace(field.mul(direction, kernel))
            matrix[i][j] = value
            matrix[j][i] = -value % field.p
    return matrix


def star_colours(matrix, star, p):
    outside = [x for x in range(len(matrix)) if x not in star]
    colours = []
    for x in outside:
        subset = sorted((*star, x))
        minor = [[matrix[i][j] for j in subset] for i in subset]
        colours.append(pfaffian_mod(minor, p))
    return outside, colours


def cauchy_product_star_colours(field, points, direction, star):
    """Use Schur's Pfaffian product identity over the quadratic field."""

    def kernel(i, j):
        return field.mul(
            field.sub(points[i], points[j]),
            field.inverse(field.sub((1, 0), field.mul(points[i], points[j]))),
        )

    base = (1, 0)
    for i, j in combinations(sorted(star), 2):
        base = field.mul(base, kernel(i, j))
    outside = [x for x in range(len(points)) if x not in star]
    colours = []
    for x in outside:
        value = base
        for t in sorted(star):
            value = field.mul(value, kernel(min(t, x), max(t, x)))
        colours.append(field.trace(field.mul(direction, value)))
    return outside, colours


def verify_schur_product_identity(field, points, star):
    """Independently compare the product formula with Pfaffian elimination."""

    def kernel(i, j):
        return field.mul(
            field.sub(points[i], points[j]),
            field.inverse(field.sub((1, 0), field.mul(points[i], points[j]))),
        )

    # Recompute the untraced product separately.
    for x in range(len(points)):
        if x in star:
            continue
        subset = sorted((*star, x))
        matrix = [[(0, 0)] * len(subset) for _ in subset]
        product = (1, 0)
        for i, left in enumerate(subset):
            for j in range(i + 1, len(subset)):
                value = kernel(left, subset[j])
                matrix[i][j] = value
                matrix[j][i] = field.neg(value)
                product = field.mul(product, value)
        assert pfaffian_quad(matrix, field) == product


def first_nonrainbow_star(matrix, p):
    for star_tuple in combinations(range(2 * p - 2), p - 2):
        star = set(star_tuple)
        outside, colours = star_colours(matrix, star, p)
        if len(set(colours)) != p:
            return star_tuple, outside, colours
    return None


def first_nonrainbow_product_star(field, points, direction):
    p = field.p
    for star_tuple in combinations(range(2 * p - 2), p - 2):
        star = set(star_tuple)
        outside, colours = cauchy_product_star_colours(field, points, direction, star)
        if len(set(colours)) != p:
            return star_tuple, outside, colours
    return None


def run_control(p):
    field = QuadField(p, first_nonsquare(p))
    points = cyclic_cauchy_points(field)
    verify_schur_product_identity(field, points, set(range(p - 2)))
    print(f"p={p}, nonsquare={field.nonsquare}, points={points}")
    for direction in projective_trace_directions(p):
        matrix = trace_cauchy_matrix(field, points, direction)
        failure = first_nonrainbow_star(matrix, p)
        assert failure is not None
        star, outside, colours = failure
        assert len(star) == p - 2 and len(outside) == p
        assert len(set(colours)) < p
        print(
            f"  lambda={direction}: T={star}; outside={outside}; "
            f"colours={colours}; distinct={len(set(colours))}"
        )
    print(f"p={p}: every projective trace direction has an exact collision")
    for direction in projective_trace_directions(p):
        failure = first_nonrainbow_product_star(field, points, direction)
        assert failure is not None
        star, outside, colours = failure
        assert len(star) == p - 2 and len(outside) == p
        assert len(set(colours)) < p
        print(
            f"  Schur lambda={direction}: T={star}; outside={outside}; "
            f"colours={colours}; distinct={len(set(colours))}"
        )
    print(f"p={p}: every trace of the K-valued Schur Pfaffian also collides")


if __name__ == "__main__":
    for prime in (7, 11):
        run_control(prime)
