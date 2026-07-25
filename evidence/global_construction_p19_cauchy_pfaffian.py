#!/usr/bin/env python3
"""Exact random-star screen for the p=19, 36th-root Cauchy-Pfaffian route.

For k=18 take the 36-point coset gH in F_(19^2), where H has order 36,
and use the Cauchy kernel (x-y)/(1-xy).  This is the p=19 continuation of
the strongest cyclic Pfaffian family left open by the p=7,11 controls.

For every projective F_19 trace direction this script samples exact
17-stars, reports a concrete non-rainbow star when found, and verifies the
Schur product against independent Pfaffian elimination on the reported
star.  A collision rejects this specified formula/direction; absence of a
collision in a sample is explicitly not evidence of a colouring.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from itertools import combinations


P = 19


@dataclass(frozen=True)
class Field:
    nonsquare: int

    def add(self, x, y):
        return ((x[0] + y[0]) % P, (x[1] + y[1]) % P)

    def neg(self, x):
        return ((-x[0]) % P, (-x[1]) % P)

    def sub(self, x, y):
        return self.add(x, self.neg(y))

    def mul(self, x, y):
        return ((x[0] * y[0] + self.nonsquare * x[1] * y[1]) % P,
                (x[0] * y[1] + x[1] * y[0]) % P)

    def power(self, x, exponent):
        result = (1, 0)
        while exponent:
            if exponent & 1:
                result = self.mul(result, x)
            x = self.mul(x, x)
            exponent //= 2
        return result

    def inverse(self, x):
        assert x != (0, 0)
        return self.power(x, P * P - 2)

    def trace(self, x):
        return 2 * x[0] % P

    def primitive(self):
        # |F_(19^2)^*|=360=2^3*3^2*5.
        for a in range(P):
            for b in range(P):
                if (a, b) != (0, 0) and all(
                    self.power((a, b), 360 // q) != (1, 0) for q in (2, 3, 5)
                ):
                    return (a, b)
        raise AssertionError("primitive element missing")


def cauchy(field, points, i, j):
    return field.mul(field.sub(points[i], points[j]),
                     field.inverse(field.sub((1, 0), field.mul(points[i], points[j]))))


def pfaffian_quad(matrix, field):
    work = [row[:] for row in matrix]
    value = (1, 0)
    for pivot in range(0, len(work), 2):
        mate = next((j for j in range(pivot + 1, len(work))
                     if work[pivot][j] != (0, 0)), None)
        if mate is None:
            return (0, 0)
        if mate != pivot + 1:
            work[mate], work[pivot + 1] = work[pivot + 1], work[mate]
            for row in work:
                row[mate], row[pivot + 1] = row[pivot + 1], row[mate]
            value = field.neg(value)
        edge = work[pivot][pivot + 1]
        value = field.mul(value, edge)
        inverse = field.inverse(edge)
        for left in range(pivot + 2, len(work)):
            for right in range(left + 1, len(work)):
                update = field.sub(
                    field.mul(work[pivot][left], work[pivot + 1][right]),
                    field.mul(work[pivot][right], work[pivot + 1][left]),
                )
                work[left][right] = field.sub(work[left][right], field.mul(update, inverse))
                work[right][left] = field.neg(work[left][right])
    return value


def pfaffian_base(matrix):
    """Independent alternating elimination after taking the F_19 trace entrywise."""
    work = [row[:] for row in matrix]
    value = 1
    for pivot in range(0, len(work), 2):
        mate = next((j for j in range(pivot + 1, len(work)) if work[pivot][j] % P), None)
        if mate is None:
            return 0
        if mate != pivot + 1:
            work[mate], work[pivot + 1] = work[pivot + 1], work[mate]
            for row in work:
                row[mate], row[pivot + 1] = row[pivot + 1], row[mate]
            value = -value
        edge = work[pivot][pivot + 1] % P
        value = value * edge % P
        inverse = pow(edge, -1, P)
        for left in range(pivot + 2, len(work)):
            for right in range(left + 1, len(work)):
                update = (work[pivot][left] * work[pivot + 1][right]
                          - work[pivot][right] * work[pivot + 1][left])
                work[left][right] = (work[left][right] - update * inverse) % P
                work[right][left] = -work[left][right] % P
    return value % P


def make_points(field):
    primitive = field.primitive()
    subgroup = [field.power(primitive, 10 * exponent) for exponent in range(36)]
    points = [field.mul(primitive, x) for x in subgroup]
    assert len(set(points)) == 36
    assert all(field.sub((1, 0), field.mul(x, y)) != (0, 0)
               for x, y in combinations(points, 2))
    return points


def product_star_colours(field, points, direction, star):
    base = (1, 0)
    for i, j in combinations(sorted(star), 2):
        base = field.mul(base, cauchy(field, points, i, j))
    outside = [x for x in range(36) if x not in star]
    colours = []
    for x in outside:
        pf = base
        for t in sorted(star):
            pf = field.mul(pf, cauchy(field, points, min(t, x), max(t, x)))
        colours.append(field.trace(field.mul(direction, pf)))
    return outside, colours


def verify_product(field, points, star, outside):
    """Verify Schur's product on every extension of the displayed star."""
    for x in outside:
        subset = sorted((*star, x))
        matrix = [[(0, 0) for _ in subset] for _ in subset]
        product = (1, 0)
        for a, i in enumerate(subset):
            for b in range(a + 1, len(subset)):
                entry = cauchy(field, points, i, subset[b])
                matrix[a][b] = entry
                matrix[b][a] = field.neg(entry)
                product = field.mul(product, entry)
        assert pfaffian_quad(matrix, field) == product


def entry_trace_star_colours(field, points, direction, star):
    outside = [x for x in range(36) if x not in star]
    colours = []
    for x in outside:
        subset = sorted((*star, x))
        matrix = [[0 for _ in subset] for _ in subset]
        for a, i in enumerate(subset):
            for b in range(a + 1, len(subset)):
                entry = field.trace(field.mul(direction, cauchy(field, points, i, subset[b])))
                matrix[a][b] = entry
                matrix[b][a] = -entry % P
        colours.append(pfaffian_base(matrix))
    return outside, colours


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stars", type=int, default=300)
    parser.add_argument("--seed", type=int, default=83519)
    args = parser.parse_args()
    if args.stars <= 0:
        parser.error("--stars must be positive")

    field = Field(2)  # 2 is a nonsquare modulo 19.
    assert pow(field.nonsquare, 9, P) == P - 1
    points = make_points(field)
    stars = [tuple(sorted(random.Random(args.seed + n).sample(range(36), 17)))
             for n in range(args.stars)]
    directions = [(a, 1) for a in range(P)] + [(1, 0)]
    print(f"p=19 cyclic 36th-root Cauchy chart; stars={args.stars}; seed={args.seed}")
    for direction in directions:
        found = None
        for star in stars:
            outside, colours = product_star_colours(field, points, direction, set(star))
            if len(set(colours)) != P:
                found = star, outside, colours
                break
        if found is None:
            print(f"lambda={direction}: no sampled collision")
            continue
        star, outside, colours = found
        verify_product(field, points, set(star), outside)
        print(f"lambda={direction}: T={star}; outside={outside}; "
              f"colours={colours}; distinct={len(set(colours))}; Schur=Pf PASS")

    # The entry-trace Pfaffian is a separate, equally natural descent.  The
    # same sampled star is deliberately re-evaluated rather than inferred
    # from the K-valued product formula.
    base_star = set(stars[0])
    for direction in directions:
        outside, colours = entry_trace_star_colours(field, points, direction, base_star)
        print(f"entry-trace lambda={direction}: T={tuple(sorted(base_star))}; "
              f"colours={colours}; distinct={len(set(colours))}")


if __name__ == "__main__":
    main()
