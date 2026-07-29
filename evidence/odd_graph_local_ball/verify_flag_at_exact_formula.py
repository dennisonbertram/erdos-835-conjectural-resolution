#!/usr/bin/env python3
"""Stdlib audit for the exact global flag Alon--Tarsi formula.

This checks:

1. the deletion/cofactor sign identity exhaustively through order 8;
2. the two-completion identity exhaustively through order 8;
3. the dummy-l, dummy-m, and dummy-* sign transformations on deterministic
   even-order synthetic controls; and
4. the genuine k=2 radius-5 control, including every flag square Q, T, S,
   the boxed global formula, and the symbol-sign evaluation.

It is a verifier for the finite sign algebra, not a solver for #835.
"""

from itertools import permutations


def prod(values):
    out = 1
    for value in values:
        out *= value
    return out


def permutation_sign(sequence):
    """Sign of a permutation written as its zero-based image sequence."""
    sequence = list(sequence)
    assert sorted(sequence) == list(range(len(sequence)))
    inversions = sum(
        sequence[i] > sequence[j]
        for i in range(len(sequence))
        for j in range(i + 1, len(sequence))
    )
    return -1 if inversions % 2 else 1


def bijection_sign(domain, codomain, mapping):
    """Sign of a bijection between two explicitly ordered finite sets."""
    domain = list(domain)
    codomain = list(codomain)
    # A full permutation may be supplied when checking an induced cofactor.
    assert set(domain).issubset(mapping)
    assert {mapping[x] for x in domain} == set(codomain)
    position = {value: index for index, value in enumerate(codomain)}
    return permutation_sign(position[mapping[x]] for x in domain)


def test_cofactor_identity():
    cases = 0
    for n in range(2, 9):
        full_domain = list(range(n))
        full_target = list(range(n))
        for image_sequence in permutations(full_target):
            mapping = dict(zip(full_domain, image_sequence))
            full_sign = bijection_sign(full_domain, full_target, mapping)
            for r in full_domain:
                s = mapping[r]
                restricted_domain = [x for x in full_domain if x != r]
                restricted_target = [x for x in full_target if x != s]
                got = bijection_sign(
                    restricted_domain, restricted_target, mapping
                )
                want = (-1) ** (r + s) * full_sign
                assert got == want, (n, image_sequence, r, s, got, want)
                cases += 1
    print(f"[ok] cofactor identity: {cases:,} exhaustive cases (n=2..8)")


def test_completion_identity():
    cases = 0
    for n in range(2, 9):
        colours = list(range(n))
        domain = [("d", index) for index in range(n - 2)]
        star = ("star",)
        for a in colours:
            for b in colours:
                if a == b:
                    continue
                remaining = [x for x in colours if x not in {a, b}]
                for image_sequence in permutations(remaining):
                    common = dict(zip(domain, image_sequence))
                    f_a = dict(common)
                    f_a[star] = b
                    f_b = dict(common)
                    f_b[star] = a
                    got = (
                        bijection_sign(
                            domain + [star],
                            [x for x in colours if x != a],
                            f_a,
                        )
                        * bijection_sign(
                            domain + [star],
                            [x for x in colours if x != b],
                            f_b,
                        )
                    )
                    want = (-1) ** (a + b + 1)
                    assert got == want, (n, a, b, image_sequence, got, want)
                    cases += 1
    print(
        f"[ok] two-completion identity: {cases:,} exhaustive cases (n=2..8)"
    )


def cyclic_latin_control(k):
    """Return L_i(u)=u+i+1 mod k, with the identity row reserved for e."""
    return [[(u + i + 1) % k for u in range(k)] for i in range(k - 1)]


def make_pi_row(k, u, a):
    """A deterministic permutation of C fixing u and sending infinity to a."""
    infinity = k
    domain = list(range(k + 1))
    mapping = {u: u, infinity: a}
    remaining_domain = [x for x in domain if x not in {u, infinity}]
    remaining_target = [x for x in domain if x not in {u, a}]
    # A reversal exercises both cofactor signs without adding assumptions.
    mapping.update(zip(remaining_domain, reversed(remaining_target)))
    return mapping


def test_dummy_line_transformations():
    for k in (2, 4, 6, 8):
        colours = list(range(k + 1))
        finite = list(range(k))
        infinity = k
        A = list(range(k - 1))
        L = cyclic_latin_control(k)

        # Dummy l rows: delete u -> L_i(u) from L_i + fixed infinity.
        for i in A:
            full = {u: L[i][u] for u in finite}
            full[infinity] = infinity
            full_sign = bijection_sign(colours, colours, full)
            line_signs = []
            for u in finite:
                a = L[i][u]
                domain = [v for v in finite if v != u] + [infinity]
                target = [x for x in colours if x != a]
                got = bijection_sign(domain, target, full)
                assert got == (-1) ** (u + a) * full_sign
                line_signs.append(got)
            assert prod(line_signs) == 1

        # Dummy m rows: delete infinity -> a, then move u to final "*".
        for i in A:
            finite_row_signs = []
            m_signs = []
            for u in finite:
                a = L[i][u]
                pi = make_pi_row(k, u, a)
                pi_sign = bijection_sign(colours, colours, pi)
                finite_row_signs.append(pi_sign)
                star = ("star",)
                desired_domain = [v for v in finite if v != u] + [star]
                desired_map = {
                    v: pi[v] for v in finite if v != u
                }
                desired_map[star] = pi[u]
                target = [x for x in colours if x != a]
                got = bijection_sign(desired_domain, target, desired_map)
                want = (-1) ** (1 + u + a) * pi_sign
                assert got == want
                m_signs.append(got)
            assert prod(m_signs) == prod(finite_row_signs)

        # Dummy * columns: cofactor columns of Lambda_u, and aggregate them.
        star_signs = []
        lambda_signs = []
        for u in finite:
            full_domain = A + [("m",), ("l",)]
            Lambda = {i: L[i][u] for i in A}
            Lambda[("m",)] = u
            Lambda[("l",)] = infinity
            lambda_sign = bijection_sign(full_domain, colours, Lambda)
            lambda_signs.append(lambda_sign)
            for i in A:
                a = L[i][u]
                domain = [j for j in A if j != i] + [("m",), ("l",)]
                target = [x for x in colours if x != a]
                got = bijection_sign(domain, target, Lambda)
                assert got == (-1) ** (i + a) * lambda_sign
                star_signs.append(got)
        want = (-1) ** (k * (k - 1) // 2) * prod(lambda_signs)
        assert prod(star_signs) == want

    print("[ok] dummy-line cofactor transformations (k=2,4,6,8)")


def test_symbol_fiber_completions():
    """Check the exact 2-row and 3-row completions of a symbol fiber."""
    cases = 0
    for k in (2, 4, 6, 8):
        existing_rows = [("e", r) for r in range(k - 2)]
        finite_columns = [("f", t) for t in range(k - 1)]
        m, ell, star = ("m",), ("l",), ("star",)
        full_rows = existing_rows + [m, ell]
        full_columns = finite_columns + [star]

        # Infinity: existing rows hit all finite columns except t; m fills t
        # and l fills star.
        for t in range(k - 1):
            reduced_columns = [
                column
                for column in finite_columns
                if column != ("f", t)
            ]
            for images in permutations(reduced_columns):
                partial = dict(zip(existing_rows, images))
                full = dict(partial)
                full[m], full[ell] = ("f", t), star
                partial_sign = bijection_sign(
                    existing_rows, reduced_columns, partial
                )
                full_sign = bijection_sign(full_rows, full_columns, full)
                want = (-1) ** (k - 2 - t) * partial_sign
                assert full_sign == want
                cases += 1

        # Symbol u: existing rows again miss one finite column; m fills star
        # and l fills the finite hole.
        for t in range(k - 1):
            reduced_columns = [
                column
                for column in finite_columns
                if column != ("f", t)
            ]
            for images in permutations(reduced_columns):
                partial = dict(zip(existing_rows, images))
                full = dict(partial)
                full[m], full[ell] = star, ("f", t)
                partial_sign = bijection_sign(
                    existing_rows, reduced_columns, partial
                )
                full_sign = bijection_sign(full_rows, full_columns, full)
                want = (-1) ** (k - 1 - t) * partial_sign
                assert full_sign == want
                cases += 1

        # A generic symbol misses existing row r and finite columns t_m,t_l.
        # The dummy map is r->star, m->t_m, l->t_l.  Its residual sign is
        # the orientation of the ordered pair (t_m,t_l).
        for r in range(k - 2):
            reduced_rows = [
                row for row in existing_rows if row != ("e", r)
            ]
            for t_m in range(k - 1):
                for t_l in range(k - 1):
                    if t_m == t_l:
                        continue
                    reduced_columns = [
                        column
                        for column in finite_columns
                        if column not in {("f", t_m), ("f", t_l)}
                    ]
                    epsilon = 1 if t_m < t_l else -1
                    for images in permutations(reduced_columns):
                        partial = dict(zip(reduced_rows, images))
                        full = dict(partial)
                        full[("e", r)] = star
                        full[m], full[ell] = ("f", t_m), ("f", t_l)
                        partial_sign = bijection_sign(
                            reduced_rows, reduced_columns, partial
                        )
                        full_sign = bijection_sign(
                            full_rows, full_columns, full
                        )
                        want = (
                            (-1) ** (r + t_m + t_l)
                            * epsilon
                            * partial_sign
                        )
                        assert full_sign == want
                        cases += 1
    print(f"[ok] symbol-fiber completion signs: {cases:,} exact cases")


def latin_signs(rows, columns, symbols, square):
    row_product = prod(
        bijection_sign(
            columns, symbols, {column: square[(row, column)] for column in columns}
        )
        for row in rows
    )
    column_product = prod(
        bijection_sign(
            rows, symbols, {row: square[(row, column)] for row in rows}
        )
        for column in columns
    )
    symbol_product = 1
    for symbol in symbols:
        location = {}
        for row in rows:
            hits = [
                column
                for column in columns
                if square[(row, column)] == symbol
            ]
            assert len(hits) == 1
            location[row] = hits[0]
        symbol_product *= bijection_sign(rows, columns, location)
    return row_product, column_product, symbol_product


def test_genuine_k2():
    k = 2
    A = [0]
    V = [0, 1]
    infinity = 2
    colours = V + [infinity]
    L = {(0, 0): 1, (0, 1): 0}
    M = {(0, frozenset({0, 1})): infinity}

    flag_at = []
    flag_symbol = []
    for i in A:
        for u in V:
            a = L[(i, u)]
            rows = ["m", "l"]
            other_v = [v for v in V if v != u]
            columns = other_v + ["*"]
            symbols = [x for x in colours if x != a]
            square = {}
            for v in other_v:
                square[("m", v)] = M[(i, frozenset({u, v}))]
                square[("l", v)] = L[(i, v)]
            square[("m", "*")] = u
            square[("l", "*")] = infinity
            row_sign, column_sign, symbol_sign = latin_signs(
                rows, columns, symbols, square
            )
            assert row_sign * column_sign == 1
            assert row_sign * column_sign * symbol_sign == -1
            flag_at.append(row_sign * column_sign)
            flag_symbol.append(symbol_sign)

    # T: rows A,e; columns and symbols V.
    t_rows = [0, "e"]
    T = {}
    for u in V:
        T[(0, u)] = L[(0, u)]
        T[("e", u)] = u
    t_row, t_column, _ = latin_signs(t_rows, V, V, T)
    at_T = t_row * t_column
    assert at_T == 1

    # S_0 on C.
    S = {}
    for x in colours:
        for y in colours:
            if x == y:
                S[(x, y)] = x
            elif infinity in {x, y}:
                finite = y if x == infinity else x
                S[(x, y)] = L[(0, finite)]
            else:
                S[(x, y)] = M[(0, frozenset({x, y}))]
    delta_S = prod(
        bijection_sign(
            colours,
            colours,
            {column: S[(row, column)] for column in colours},
        )
        for row in colours
    )
    assert delta_S == -1

    left = prod(flag_at)
    right = (-1) ** (k * (k - 1) // 2) * at_T * delta_S
    assert left == right == 1
    # Two flags make the universal per-flag factor (-1) cancel globally.
    assert prod(flag_symbol) == left
    print(
        "[ok] genuine k=2 control: two AT(Q)=+1, AT(T)=+1, "
        "delta(S)=-1, both global evaluations=+1"
    )


def test_global_symbol_equivalence():
    # The universal Latin identity gives symbol=(-1)^t*AT per flag.
    # There are k(k-1) flags, an even number for every even k.
    for k in range(2, 34, 2):
        t = k * (k - 1) // 2
        number_of_flags = k * (k - 1)
        assert (-1) ** (t * number_of_flags) == 1
    print("[ok] universal completed-symbol/global-AT factor cancels for every even k<=32")


def main():
    test_cofactor_identity()
    test_completion_identity()
    test_dummy_line_transformations()
    test_symbol_fiber_completions()
    test_genuine_k2()
    test_global_symbol_equivalence()
    print("ALL FLAG AT FORMULA AUDITS PASSED")
    print("SCOPE: finite sign algebra only; Erdős--Rosenfeld #835 remains open.")


if __name__ == "__main__":
    main()
