#!/usr/bin/env python3
"""Audit a complement-cover six-prefix with only two live colours."""

from itertools import combinations


C = tuple(f"c{i}" for i in range(6))
OUTSIDE = tuple(f"o{i}" for i in range(7))
V = frozenset(C + OUTSIDE)


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def translate(prefix, pairs):
    return frozenset(edge(f"{prefix}{a}", f"{prefix}{b}") for a, b in pairs)


def support(edges):
    return frozenset().union(*edges)


def is_matching(edges):
    ends = [v for e in edges for v in e]
    return len(ends) == len(set(ends))


def perfect_matchings(vertices, allowed_edges):
    vertices = tuple(sorted(vertices))

    def rec(remaining):
        if not remaining:
            yield frozenset()
            return
        u = remaining[0]
        for i in range(1, len(remaining)):
            v = remaining[i]
            uv = edge(u, v)
            if uv not in allowed_edges:
                continue
            for rest in rec(remaining[1:i] + remaining[i + 1 :]):
                yield rest | {uv}

    yield from rec(vertices)


def maximum_matching_size(vertices, allowed_edges):
    vertices = tuple(sorted(vertices))

    def rec(remaining):
        if not remaining:
            return 0
        u = remaining[0]
        best = rec(remaining[1:])
        for i in range(1, len(remaining)):
            v = remaining[i]
            if edge(u, v) in allowed_edges:
                best = max(
                    best,
                    1 + rec(remaining[1:i] + remaining[i + 1 :]),
                )
        return best

    return rec(vertices)


def main():
    c_rows = (
        ((0, 5), (1, 4), (2, 3)),
        ((0, 4), (3, 5), (1, 2)),
        ((0, 3), (2, 4), (1, 5)),
        ((1, 3), (4, 5)),
        ((0, 1), (2, 5)),
        ((0, 2), (3, 4)),
    )
    o_rows = (
        ((0, 3), (1, 5)),
        ((0, 4), (2, 6)),
        ((0, 5), (3, 6)),
        ((0, 6), (4, 5)),
        ((3, 4), (5, 6)),
        ((3, 5), (4, 6)),
    )
    selected = tuple(
        translate("c", c_row) | translate("o", o_row)
        for c_row, o_row in zip(c_rows, o_rows)
    )
    assert [len(m) for m in selected] == [5, 5, 5, 4, 4, 4]
    assert all(is_matching(m) for m in selected)
    assert all(
        selected[i].isdisjoint(selected[j])
        for i, j in combinations(range(6), 2)
    )

    d_edges = frozenset().union(*selected)
    assert len(d_edges) == 27
    assert translate("c", combinations(range(6), 2)) <= d_edges
    degrees = {v: sum(v in e for e in d_edges) for v in V}
    assert {v: degrees[v] for v in C} == {v: 5 for v in C}
    assert [degrees[v] for v in OUTSIDE] == [4, 1, 1, 4, 4, 5, 5]
    assert max(degrees.values()) == 5

    selected_complements = tuple(V - support(m) for m in selected)
    assert [len(a) for a in selected_complements] == [3, 3, 3, 5, 5, 5]
    assert frozenset().union(*selected_complements) == V

    remaining_fives = tuple(
        frozenset(C) - {f"c{i}"} for i in range(4)
    )
    blocked_triples = tuple(
        frozenset(f"o{i}" for i in digits)
        for digits in ((0, 5, 6), (3, 4, 5), (3, 4, 6), (3, 5, 6), (4, 5, 6))
    )
    good_triples = (
        frozenset(("c0", "c1", "o0")),
        frozenset(("c2", "c3", "o0")),
    )
    five_sets = selected_complements[3:] + remaining_fives
    triples = selected_complements[:3] + blocked_triples + good_triples

    assert len(five_sets) == 7
    assert len(triples) == 10
    assert all(len(a) == 5 for a in five_sets)
    assert all(len(a) == 3 for a in triples)
    assert len(set(five_sets)) == 7
    assert len(set(triples)) == 10
    assert all(
        sum(v in a for a in five_sets + triples) == 5 for v in V
    )

    all_edges = frozenset(edge(u, v) for u, v in combinations(V, 2))
    residual = all_edges - d_edges
    residual_outside = frozenset(
        e for e in residual if e <= frozenset(OUTSIDE)
    )
    expected_outside = translate(
        "o",
        (
            (0, 1),
            (0, 2),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 6),
            (2, 3),
            (2, 4),
            (2, 5),
        ),
    )
    assert residual_outside == expected_outside
    assert all(
        ("o1" in e or "o2" in e) for e in residual_outside
    )
    assert maximum_matching_size(OUTSIDE, residual_outside) == 2

    remaining_complements = remaining_fives + blocked_triples + good_triples
    matching_counts = []
    for complement in remaining_complements:
        target = V - complement
        matchings = tuple(perfect_matchings(target, residual))
        matching_counts.append(len(matchings))

    assert matching_counts[:4] == [0, 0, 0, 0]
    assert matching_counts[4:9] == [0, 0, 0, 0, 0]
    assert all(count > 0 for count in matching_counts[9:])
    assert sum(count > 0 for count in matching_counts) == 2

    witnesses = (
        frozenset(
            (
                edge("o1", "o6"),
                edge("c2", "o2"),
                edge("c3", "o3"),
                edge("c4", "o4"),
                edge("c5", "o5"),
            )
        ),
        frozenset(
            (
                edge("o2", "o5"),
                edge("c0", "o1"),
                edge("c1", "o3"),
                edge("c4", "o4"),
                edge("c5", "o6"),
            )
        ),
    )
    for triple, witness in zip(good_triples, witnesses):
        assert len(witness) == 5
        assert is_matching(witness)
        assert support(witness) == V - triple
        assert witness <= residual

    print("dead r=0 complement-cover six-prefix audit: PASS")
    print("remaining live-colour counts:", matching_counts)


if __name__ == "__main__":
    main()
