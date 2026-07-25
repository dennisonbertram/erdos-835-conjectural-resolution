#!/usr/bin/env python3
"""Exact checks for the algebraic F_32 coefficient-eight classification.

The first half verifies, without a subset search, that the sets

    U_b = {x in F_32^*: Tr(b*x) = 0}

are the thirty-one candidates predicted by the linearized-polynomial proof.
It checks their elementary coefficients and e_8(U_b)=b^(-8).  Exactly the
sixteen with Tr(b)=1 avoid the point 1.

The second half is an independent exhaustive meet-in-the-middle audit over
all 15-subsets of F_32^*.  It confirms that there are no further candidates.
Finally, the script constructs and checks the resulting 17-clique in every
nonzero lifted moment-curve layer.
"""

MODULUS = 0b100101  # X^5 + X^2 + 1
MAX_DEGREE = 8


def multiply(left, right):
    answer = 0
    while right:
        if right & 1:
            answer ^= left
        right >>= 1
        left <<= 1
        if left & 32:
            left ^= MODULUS
    return answer & 31


PRODUCT = tuple(tuple(multiply(x, y) for y in range(32)) for x in range(32))


def power(value, exponent):
    answer = 1
    while exponent:
        if exponent & 1:
            answer = PRODUCT[answer][value]
        value = PRODUCT[value][value]
        exponent >>= 1
    return answer


def trace(value):
    answer = 0
    current = value
    for _ in range(5):
        answer ^= current
        current = PRODUCT[current][current]
    assert answer in (0, 1)
    return answer


def add_point(series, point):
    answer = list(series)
    for degree in range(MAX_DEGREE, 0, -1):
        answer[degree] ^= PRODUCT[point][answer[degree - 1]]
    return tuple(answer)


def elementary_series(points):
    answer = (1,) + (0,) * MAX_DEGREE
    for point in points:
        answer = add_point(answer, point)
    return answer


def multiply_series(left, right):
    answer = [0] * (MAX_DEGREE + 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            if i + j <= MAX_DEGREE:
                answer[i + j] ^= PRODUCT[x][y]
    return tuple(answer)


def inverse_prefix(series):
    answer = [1] + [0] * 7
    for degree in range(1, 8):
        for i in range(1, degree + 1):
            answer[degree] ^= PRODUCT[series[i]][answer[degree - i]]
    return tuple(answer)


def enumerate_subsets(points):
    records = [(0, (1,) + (0,) * MAX_DEGREE, 0)] * (1 << len(points))
    for mask in range(1, 1 << len(points)):
        bit = mask & -mask
        index = bit.bit_length() - 1
        size, series, _ = records[mask ^ bit]
        records[mask] = (size + 1, add_point(series, points[index]), mask)
    return records


def main():
    # Construct all nonzero parts of trace hyperplanes and check the formulas.
    predicted_all = {}
    for b in range(1, 32):
        subset = frozenset(
            x for x in range(1, 32) if trace(PRODUCT[b][x]) == 0
        )
        assert len(subset) == 15
        series = elementary_series(subset)
        assert series[1:8] == (0,) * 7
        expected_eighth = power(b, 23)  # b^(-8), exponents modulo 31
        assert series[8] == expected_eighth
        assert trace(power(expected_eighth, 30)) == trace(b)
        predicted_all[subset] = expected_eighth
    assert len(predicted_all) == 31

    # Exhaustively enumerate all candidates in F_32^*, independently of the
    # trace construction.  The unequal split merely minimizes memory.
    left_points = tuple(range(1, 16))
    right_points = tuple(range(16, 32))
    left = enumerate_subsets(left_points)
    right = enumerate_subsets(right_points)
    right_index = {}
    for size, series, mask in right:
        right_index.setdefault((size, series[1:8]), []).append((series, mask))

    exhaustive = {}
    for left_size, left_series, left_mask in left:
        desired = inverse_prefix(left_series)
        for right_series, right_mask in right_index.get(
            (15 - left_size, desired[1:8]), ()
        ):
            product = multiply_series(left_series, right_series)
            assert product[1:8] == (0,) * 7
            subset = frozenset(
                left_points[i]
                for i in range(len(left_points))
                if left_mask & (1 << i)
            ) | frozenset(
                right_points[i]
                for i in range(len(right_points))
                if right_mask & (1 << i)
            )
            assert len(subset) == 15
            exhaustive[subset] = product[8]

    assert exhaustive == predicted_all
    spectrum = set(exhaustive.values())
    assert spectrum == set(range(1, 32))

    # Restricting to F_32 minus {0,1} leaves exactly the sixteen hyperplanes
    # with Tr(b)=1, and gives the trace-inverse spectrum in the original note.
    avoiding_one = {
        subset: eighth
        for subset, eighth in exhaustive.items()
        if 1 not in subset
    }
    trace_spectrum = {
        value for value in range(1, 32)
        if trace(power(value, 30)) == 1
    }
    assert len(avoiding_one) == 16
    assert set(avoiding_one.values()) == trace_spectrum

    # For lambda != 0, b=lambda^(-4)=lambda^27 gives the unique trace
    # hyperplane whose nonzero part has e_8=lambda.  Its complement, together
    # with zero, is a 17-set R.  Deleting a from R has moment-curve prefix
    # (a,a^2,...,a^7,a^8+lambda), so the 17 deletions form a clique.
    checked_clique_edges = 0
    for lam in range(1, 32):
        b = power(lam, 27)
        assert power(b, 23) == lam
        clique_roots = {
            0
        } | {
            x for x in range(1, 32) if trace(PRODUCT[b][x]) == 1
        }
        assert len(clique_roots) == 17
        states = {}
        for a in clique_roots:
            subset = clique_roots - {a}
            series = elementary_series(subset)
            expected = tuple(power(a, degree) for degree in range(1, 8))
            expected += (power(a, 8) ^ lam,)
            assert series[1:9] == expected
            states[a] = expected
        assert len(set(states.values())) == 17
        checked_clique_edges += 17 * 16 // 2

    # The canonical identification of each local clique with the fixed
    # 17-element palette {0} union {z: Tr(z)=1} does not extend naively.
    # This exact adjacent pair is a counterexample to the rule described in
    # the accompanying note.
    palette = {0} | {z for z in range(32) if trace(z) == 1}
    assert len(palette) == 17

    def naive_trace_colour(subset):
        series = elementary_series(subset)
        first = series[1]
        lam = series[8] ^ power(first, 8)
        if lam == 0:
            return 0
        normalized = PRODUCT[power(lam, 27)][first]
        return normalized if trace(normalized) == 1 else 0

    common = {0, 5, 6, 7, 8, 10, 11, 14, 16, 20, 24, 25, 26, 29, 31}
    adjacent_left = common | {2}
    adjacent_right = common | {21}
    assert len(adjacent_left & adjacent_right) == 15
    assert naive_trace_colour(adjacent_left) == 0
    assert naive_trace_colour(adjacent_right) == 0

    print("F_32 trace-hyperplane classification: PASS")
    print("classified nonzero hyperplane subsets:", len(exhaustive))
    print("subsets also avoiding 1:", len(avoiding_one))
    print("restricted spectrum:", sorted(trace_spectrum))
    print("restricted criterion: Tr(e_8^(-1)) = 1")
    print("checked lifted-curve clique edges:", checked_clique_edges)


if __name__ == "__main__":
    main()
