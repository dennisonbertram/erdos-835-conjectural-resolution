#!/usr/bin/env python3
"""Verify the genuine five-saturated order-12 boundary counterexample.

This refutes an unrestricted five-row completion claim.  It is deliberately
not presented as a counterexample at the target order 18.
"""

from __future__ import annotations

import itertools


P_SIZE = 5
A_SIZE = 7
N_COLOURS = 11
DIAGONAL = N_COLOURS

# CROSS[a][p] is the colour of edge a--p.
CROSS = (
    (2, 4, 10, 1, 8),
    (6, 0, 2, 10, 7),
    (3, 9, 5, 0, 2),
    (5, 7, 3, 4, 1),
    (4, 5, 0, 2, 3),
    (1, 3, 7, 5, 4),
    (10, 2, 4, 3, 5),
)

INTERNAL = {
    (0, 1): 8,
    (2, 3): 8,
    (0, 2): 9,
    (3, 4): 9,
    (0, 3): 7,
    (0, 4): 0,
    (1, 2): 1,
    (1, 3): 6,
    (2, 4): 6,
    (1, 4): 10,
}


def verify_partial_colouring() -> None:
    palette = set(range(N_COLOURS))

    assert len(CROSS) == A_SIZE
    assert all(len(row) == P_SIZE for row in CROSS)
    # Properness at every A-vertex.
    assert all(len(set(row)) == P_SIZE for row in CROSS)

    p_edges = set(itertools.combinations(range(P_SIZE), 2))
    assert set(INTERNAL) == p_edges
    # Properness of the internal K5 colouring.
    for colour in palette:
        edges = [edge for edge, value in INTERNAL.items() if value == colour]
        assert all(set(e).isdisjoint(f) for e, f in itertools.combinations(edges, 2))

    # Every P-vertex is saturated: its 7 cross and 4 internal colours are
    # all distinct and together equal the full 11-colour palette.
    for p in range(P_SIZE):
        cross_colours = {CROSS[a][p] for a in range(A_SIZE)}
        internal_colours = {
            colour for edge, colour in INTERNAL.items() if p in edge
        }
        assert len(cross_colours) == A_SIZE
        assert len(internal_colours) == P_SIZE - 1
        assert cross_colours.isdisjoint(internal_colours)
        assert cross_colours | internal_colours == palette

    print(
        "partial K12-E(K7) colouring:",
        "proper with all five P-vertices saturated: PASS",
    )


def verify_latin_rectangle() -> None:
    # Columns 0..4 are P, columns 5..11 are A.  These are precisely the
    # five filled rows of the associated unipotent symmetric Latin square.
    rows = []
    for p in range(P_SIZE):
        row = []
        for q in range(P_SIZE):
            if p == q:
                row.append(DIAGONAL)
            else:
                row.append(INTERNAL[tuple(sorted((p, q)))])
        row.extend(CROSS[a][p] for a in range(A_SIZE))
        rows.append(tuple(row))

    full_symbol_set = set(range(N_COLOURS + 1))
    assert all(set(row) == full_symbol_set for row in rows)
    for column in range(P_SIZE + A_SIZE):
        values = [rows[p][column] for p in range(P_SIZE)]
        assert len(set(values)) == P_SIZE
    assert all(rows[p][q] == rows[q][p] for p in range(P_SIZE) for q in range(P_SIZE))
    assert all(rows[p][p] == DIAGONAL for p in range(P_SIZE))

    print(
        "5x12 Latin rectangle:",
        "Latin, symmetric on its principal 5x5 block, unipotent: PASS",
    )


def verify_forced_edge_obstruction() -> None:
    supports = {
        colour: {
            a for a, row in enumerate(CROSS) if colour not in row
        }
        for colour in range(N_COLOURS)
    }
    assert supports[3] == {0, 1}
    assert supports[5] == {0, 1}

    # A perfect matching on a two-set consists of its unique edge.  Thus
    # both colors demand edge 01, contradicting an edge partition.
    forced_edge_3 = tuple(sorted(supports[3]))
    forced_edge_5 = tuple(sorted(supports[5]))
    assert forced_edge_3 == forced_edge_5 == (0, 1)

    multiplicities = {
        colour: A_SIZE - len(support)
        for colour, support in supports.items()
    }
    assert all(value in {1, 3, 5} for value in multiplicities.values())
    assert all(sum(colour in row for colour in range(N_COLOURS)) == 5 for row in CROSS)

    print(
        "nonextension certificate:",
        "colours 3 and 5 are both forced onto hole edge 0-1: PASS",
    )
    print(
        "delimiter:",
        "order 12 refutes an unrestricted five-row theorem;",
        "it is not an order-18 counterexample",
    )


def main() -> int:
    verify_partial_colouring()
    verify_latin_rectangle()
    verify_forced_edge_obstruction()
    print(
        "scope:",
        "genuine class-B-prime boundary certificate only;",
        "target order-18 completion remains open",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
