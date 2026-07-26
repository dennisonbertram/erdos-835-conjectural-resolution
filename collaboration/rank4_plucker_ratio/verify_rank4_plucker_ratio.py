#!/usr/bin/env python3
"""Exact controls for rank4_plucker_ratio.md.

This verifies the shared-support/generic pencil split and an explicit
p=17 generic-rank-4 local control on the normal rational curve.  The
control has:

* decomposable, independent endpoint forms A and B;
* no edge on which both endpoint coordinates vanish;
* rank four for every non-endpoint pencil member; and
* one rank-four member whose zero graph is a perfect matching of K_18.

It is deliberately not reported as a decoder witness: its raw projective
edge labels have only 9 or 10 distinct values around a vertex.
"""

from __future__ import annotations

from itertools import combinations


P = 17
# Alternating coefficients are ordered 01,02,03,12,13,23.
Form = tuple[int, int, int, int, int, int]
Vector = tuple[int, int, int, int]


def mod(value: int) -> int:
    return value % P


def inverse(value: int) -> int:
    return pow(value % P, P - 2, P)


def add(left: Form, right: Form, scale: int = 1) -> Form:
    return tuple(mod(a + scale * b) for a, b in zip(left, right))  # type: ignore[return-value]


def wedge(left: Vector, right: Vector) -> Form:
    return (
        mod(left[0] * right[1] - left[1] * right[0]),
        mod(left[0] * right[2] - left[2] * right[0]),
        mod(left[0] * right[3] - left[3] * right[0]),
        mod(left[1] * right[2] - left[2] * right[1]),
        mod(left[1] * right[3] - left[3] * right[1]),
        mod(left[2] * right[3] - left[3] * right[2]),
    )


def pfaffian(form: Form) -> int:
    return mod(form[0] * form[5] - form[1] * form[4] + form[2] * form[3])


def alternating_rank(form: Form) -> int:
    if not any(form):
        return 0
    return 4 if pfaffian(form) else 2


def evaluate(form: Form, left: Vector, right: Vector) -> int:
    minors = wedge(left, right)
    return mod(sum(a * b for a, b in zip(form, minors)))


def twisted_cubic_points() -> tuple[Vector, ...]:
    finite = tuple(
        (1, value, value * value % P, value * value * value % P) for value in range(P)
    )
    return (*finite, (0, 0, 0, 1))


def projective_label(first: int, second: int) -> int:
    """Encode [first:second] as second/first in F_17, or 17 for infinity."""
    first %= P
    second %= P
    assert first or second
    if first == 0:
        return 17
    return second * inverse(first) % P


def zero_edges(form: Form, points: tuple[Vector, ...]) -> set[tuple[int, int]]:
    return {
        edge
        for edge in combinations(range(len(points)), 2)
        if evaluate(form, points[edge[0]], points[edge[1]]) == 0
    }


def degrees(edges: set[tuple[int, int]], size: int) -> tuple[int, ...]:
    return tuple(sum(vertex in edge for edge in edges) for vertex in range(size))


def matrix_rank(rows: list[list[int]]) -> int:
    work = [[entry % P for entry in row] for row in rows]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inverse(work[rank][column])
        work[rank] = [entry * scale % P for entry in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            factor = work[row][column]
            work[row] = [
                (entry - factor * pivot_entry) % P
                for entry, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def check_canonical_classification() -> None:
    e0 = (1, 0, 0, 0)
    e1 = (0, 1, 0, 0)
    e2 = (0, 0, 1, 0)
    e3 = (0, 0, 0, 1)

    shared_first = wedge(e0, e1)
    shared_second = wedge(e0, e2)
    assert matrix_rank([list(e0), list(e1), list(e0), list(e2)]) == 3
    assert all(
        alternating_rank(add(shared_first, shared_second, scalar)) == 2
        for scalar in range(1, P)
    )

    generic_first = wedge(e0, e1)
    generic_second = wedge(e2, e3)
    assert matrix_rank([list(e0), list(e1), list(e2), list(e3)]) == 4
    assert alternating_rank(generic_first) == 2
    assert alternating_rank(generic_second) == 2
    assert all(
        alternating_rank(add(generic_first, generic_second, scalar)) == 4
        for scalar in range(1, P)
    )


def check_explicit_rank4_control() -> dict[str, object]:
    points = twisted_cubic_points()
    assert len(points) == P + 1

    # These displayed factorizations make endpoint decomposability
    # independently transparent.
    a_left = (1, 0, 9, 8)
    a_right = (0, 9, 2, 6)
    b_left = (1, 5, 0, 7)
    b_right = (0, 0, 15, 11)
    form_a = wedge(a_left, a_right)
    form_b = wedge(b_left, b_right)
    assert form_a == (9, 2, 6, 4, 13, 4)
    assert form_b == (0, 15, 11, 7, 4, 14)
    assert alternating_rank(form_a) == alternating_rank(form_b) == 2
    assert matrix_rank([list(a_left), list(a_right), list(b_left), list(b_right)]) == 4

    form_c = add(form_a, form_b)
    assert form_c == (9, 0, 0, 11, 0, 1)
    assert pfaffian(form_c) == 9
    assert alternating_rank(form_c) == 4

    # The pencil is generic: only [1:0] and [0:1] have rank two.
    assert all(
        alternating_rank(add(form_a, form_b, scalar)) == 4 for scalar in range(1, P)
    )

    # The endpoint feature pair is defined on all 153 edges.
    for i, j in combinations(range(P + 1), 2):
        pair = (
            evaluate(form_a, points[i], points[j]),
            evaluate(form_b, points[i], points[j]),
        )
        assert pair != (0, 0)

    # For finite s,t, C(s,t)=(t-s)(st-3)^2.  The infinity values are s^2.
    for left, right in combinations(range(P), 2):
        expected = (right - left) * (left * right - 3) ** 2 % P
        assert evaluate(form_c, points[left], points[right]) == expected
    for finite in range(P):
        assert evaluate(form_c, points[finite], points[P]) == finite * finite % P

    matching = zero_edges(form_c, points)
    expected_matching = {
        (0, 17),
        (1, 3),
        (2, 10),
        (4, 5),
        (6, 9),
        (7, 15),
        (8, 11),
        (12, 13),
        (14, 16),
    }
    assert matching == expected_matching
    assert degrees(matching, P + 1) == (1,) * (P + 1)

    # Audit all raw ratio classes.  This is a positive control for one
    # rank-four perfect-matching zero class, not a full decoder.
    classes = [set() for _ in range(P + 1)]
    rows = [set() for _ in range(P + 1)]
    for i, j in combinations(range(P + 1), 2):
        label = projective_label(
            evaluate(form_a, points[i], points[j]),
            evaluate(form_b, points[i], points[j]),
        )
        classes[label].add((i, j))
        rows[i].add(label)
        rows[j].add(label)

    class_sizes = tuple(len(edges) for edges in classes)
    row_sizes = tuple(len(labels) for labels in rows)
    assert class_sizes == (
        7,
        10,
        12,
        8,
        11,
        9,
        11,
        10,
        10,
        7,
        7,
        8,
        7,
        0,
        7,
        11,
        9,
        9,
    )
    assert row_sizes == (
        10,
        9,
        10,
        10,
        10,
        10,
        9,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        9,
        10,
        10,
    )
    assert max(row_sizes) == 10 < P

    return {
        "form_a": form_a,
        "form_b": form_b,
        "form_c": form_c,
        "matching": tuple(sorted(matching)),
        "class_sizes": class_sizes,
        "row_sizes": row_sizes,
    }


def main() -> int:
    check_canonical_classification()
    report = check_explicit_rank4_control()
    print("alternating-pencil classification: PASS")
    print("A =", report["form_a"])
    print("B =", report["form_b"])
    print("A+B =", report["form_c"], "rank=4")
    print("rank-4 zero matching =", report["matching"])
    print("raw ratio class sizes =", report["class_sizes"])
    print("raw distinct labels per vertex =", report["row_sizes"])
    print("decoder status for this control: FAILS (10 < 17 at every star)")
    print("rank-4 Plucker-ratio finite audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
