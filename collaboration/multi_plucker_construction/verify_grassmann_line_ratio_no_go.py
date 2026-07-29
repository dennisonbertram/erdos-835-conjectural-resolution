#!/usr/bin/env python3
"""Exact finite checks for grassmann_line_ratio_no_go.md.

The mathematical no-go uses Segre's theorem that every oval in
PG(2,q), q odd, is a conic.  This dependency-free audit checks the
remaining finite-field claims exactly:

* the tangent/internal-point criterion for the standard conic;
* the maximum number of internal points on a projective line;
* the p=17 numerical gap 16 > 9 (and the sharp p=3 boundary);
* the exterior-square/projective-plane determinant dictionary; and
* the fact that the standard conic cannot be enlarged by another point.
"""

from __future__ import annotations

from itertools import combinations


def inverse(value: int, prime: int) -> int:
    return pow(value % prime, prime - 2, prime)


def normalize(vector: tuple[int, ...], prime: int) -> tuple[int, ...]:
    vector = tuple(value % prime for value in vector)
    pivot = next(value for value in vector if value)
    scale = inverse(pivot, prime)
    return tuple(value * scale % prime for value in vector)


def projective_points(prime: int) -> tuple[tuple[int, int, int], ...]:
    points = {
        normalize((x, y, z), prime)
        for x in range(prime)
        for y in range(prime)
        for z in range(prime)
        if (x, y, z) != (0, 0, 0)
    }
    answer = tuple(sorted(points))
    assert len(answer) == prime * prime + prime + 1
    return answer


def dot(left: tuple[int, ...], right: tuple[int, ...], prime: int) -> int:
    return sum(a * b for a, b in zip(left, right)) % prime


def determinant3(
    first: tuple[int, int, int],
    second: tuple[int, int, int],
    third: tuple[int, int, int],
    prime: int,
) -> int:
    return (
        first[0] * (second[1] * third[2] - second[2] * third[1])
        - first[1] * (second[0] * third[2] - second[2] * third[0])
        + first[2] * (second[0] * third[1] - second[1] * third[0])
    ) % prime


def conic_value(point: tuple[int, int, int], prime: int) -> int:
    x, y, z = point
    return (y * y - x * z) % prime


def tangent_at(point: tuple[int, int, int], prime: int) -> tuple[int, int, int]:
    """Gradient line of Y^2-XZ at a conic point."""
    x, y, z = point
    assert conic_value(point, prime) == 0
    return normalize((-z, 2 * y, -x), prime)


def legendre(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        return 0
    return 1 if pow(value, (prime - 1) // 2, prime) == 1 else -1


def check_conic_census(prime: int) -> dict[str, object]:
    points = projective_points(prime)
    lines = points  # normalized coefficient triples
    conic = tuple(point for point in points if conic_value(point, prime) == 0)
    assert len(conic) == prime + 1

    tangents = {tangent_at(point, prime) for point in conic}
    assert len(tangents) == prime + 1
    for point in conic:
        tangent = tangent_at(point, prime)
        on_tangent = [other for other in conic if dot(tangent, other, prime) == 0]
        assert on_tangent == [point]

    internal = set()
    external = set()
    for point in points:
        tangent_count = sum(dot(line, point, prime) == 0 for line in tangents)
        character = legendre(conic_value(point, prime), prime)
        if point in conic:
            assert tangent_count == 1
            assert character == 0
        elif tangent_count == 0:
            internal.add(point)
            assert character == -1
        else:
            external.add(point)
            assert tangent_count == 2
            assert character == 1

    internal_counts = []
    intersection_types = []
    for line in lines:
        points_on_line = [point for point in points if dot(line, point, prime) == 0]
        conic_count = sum(point in conic for point in points_on_line)
        internal_count = sum(point in internal for point in points_on_line)
        assert len(points_on_line) == prime + 1
        assert conic_count in (0, 1, 2)
        internal_counts.append(internal_count)
        intersection_types.append((conic_count, internal_count))

    expected_maximum = (prime + 1) // 2
    assert max(internal_counts) == expected_maximum
    assert all(internal_count <= expected_maximum for internal_count in internal_counts)

    # A direct finite control for the arc cap once Segre has identified
    # an arbitrary oval with this conic: every off-conic point lies on
    # a secant, so none can be adjoined to the q+1-arc.
    for point in points:
        if point in conic:
            continue
        assert any(
            determinant3(point, left, right, prime) == 0
            for left, right in combinations(conic, 2)
        )

    return {
        "prime": prime,
        "points": len(points),
        "conic_points": len(conic),
        "internal_points": len(internal),
        "external_points": len(external),
        "maximum_internal_points_on_a_line": max(internal_counts),
        "line_type_counts": {
            pair: intersection_types.count(pair)
            for pair in sorted(set(intersection_types))
        },
    }


def wedge(
    left: tuple[int, ...], right: tuple[int, ...], prime: int
) -> tuple[tuple[int, ...], ...]:
    size = len(left)
    return tuple(
        tuple((left[i] * right[j] - left[j] * right[i]) % prime for j in range(size))
        for i in range(size)
    )


def add_scaled(
    first: tuple[tuple[int, ...], ...],
    second: tuple[tuple[int, ...], ...],
    left_scale: int,
    right_scale: int,
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            (left_scale * first[i][j] + right_scale * second[i][j]) % prime
            for j in range(len(first))
        )
        for i in range(len(first))
    )


def check_pencil_dictionary(prime: int) -> None:
    """Check eta_[s:t](i,j)=det(P_i,P_j,N_[s:t]) exactly."""
    size = 9
    a = tuple((i * i + 3 * i + 1) % prime for i in range(size))
    b = tuple((2 * i * i + i + 4) % prime for i in range(size))
    c = tuple((4 * i * i + 2 * i + 2) % prime for i in range(size))
    first = wedge(a, b, prime)
    second = wedge(a, c, prime)
    points = tuple((a[i], b[i], c[i]) for i in range(size))

    parameters = tuple((1, value) for value in range(prime)) + ((0, 1),)
    for s, t in parameters:
        form = add_scaled(first, second, s, t, prime)
        center = (0, -t % prime, s)
        for i, j in combinations(range(size), 2):
            assert form[i][j] == determinant3(points[i], points[j], center, prime)

    # Exterior-square identity behind the line classification:
    # (A+tB)^2=0 because A=a^b and B=a^c share a three-space.
    for s, t in parameters:
        form = add_scaled(first, second, s, t, prime)
        for i, j, k, ell in combinations(range(size), 4):
            pfaffian4 = (
                form[i][j] * form[k][ell]
                - form[i][k] * form[j][ell]
                + form[i][ell] * form[j][k]
            ) % prime
            assert pfaffian4 == 0


def check_p3_boundary_link() -> dict[str, object]:
    """Build the sharp local p=3 chord-pencil/decoder control."""
    prime = 3
    points = projective_points(prime)
    conic = tuple(point for point in points if conic_value(point, prime) == 0)
    tangents = {tangent_at(point, prime) for point in conic}
    internal = {
        point
        for point in points
        if point not in conic and all(dot(line, point, prime) != 0 for line in tangents)
    }

    external_line = next(
        line
        for line in points
        if not any(dot(line, point, prime) == 0 for point in conic)
    )
    centers = tuple(point for point in points if dot(external_line, point, prime) == 0)
    internal_centers = tuple(point for point in centers if point in internal)
    external_centers = tuple(point for point in centers if point not in internal)
    assert len(internal_centers) == len(external_centers) == 2

    zero_edges = {}
    for center in centers:
        edges = {
            (i, j)
            for i, j in combinations(range(len(conic)), 2)
            if determinant3(conic[i], conic[j], center, prime) == 0
        }
        zero_edges[center] = edges

    for center in internal_centers:
        degrees = [
            sum(vertex in edge for edge in zero_edges[center])
            for vertex in range(len(conic))
        ]
        assert degrees == [1, 1, 1, 1]

    assert len(set().union(*(zero_edges[c] for c in external_centers))) == 2
    merged_degrees = [
        sum(
            vertex in edge for center in external_centers for edge in zero_edges[center]
        )
        for vertex in range(len(conic))
    ]
    assert merged_degrees == [1, 1, 1, 1]

    # Each chord meets the centre line once.  Fuse the two external
    # centre labels and retain the two internal labels: every K4 vertex
    # then sees all three decoded colours.
    edge_labels = {}
    for edge in combinations(range(len(conic)), 2):
        matching_centers = [center for center in centers if edge in zero_edges[center]]
        assert len(matching_centers) == 1
        edge_labels[edge] = matching_centers[0]

    for vertex in range(len(conic)):
        decoded = set()
        for edge, center in edge_labels.items():
            if vertex not in edge:
                continue
            decoded.add("merged" if center in external_centers else center)
        assert len(decoded) == 3

    return {
        "external_line": external_line,
        "internal_centers": internal_centers,
        "external_centers": external_centers,
        "edge_labels": edge_labels,
    }


def main() -> int:
    reports = []
    for prime in (3, 5, 7, 17):
        reports.append(check_conic_census(prime))
        check_pencil_dictionary(prime)

    for report in reports:
        print(
            "p={prime}: PG points={points}, conic={conic_points}, "
            "internal={internal_points}, external={external_points}, "
            "max internal/line={maximum_internal_points_on_a_line}".format(**report)
        )
        print("  line types:", report["line_type_counts"])

    p17 = reports[-1]
    assert p17["maximum_internal_points_on_a_line"] == 9
    assert 17 - 1 > p17["maximum_internal_points_on_a_line"]
    assert reports[0]["maximum_internal_points_on_a_line"] == 3 - 1
    boundary = check_p3_boundary_link()
    print("p=17 Grassmann-line gap: 16 required internal centers > 9 possible")
    print("p=3 boundary control: 2 required = 2 possible")
    print(
        "p=3 local fused chord-pencil exists:",
        "line=",
        boundary["external_line"],
        "internal=",
        boundary["internal_centers"],
        "merged=",
        boundary["external_centers"],
    )
    print("Grassmann-line ratio finite audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
