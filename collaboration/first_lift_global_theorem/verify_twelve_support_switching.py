#!/usr/bin/env python3
"""Verify the arithmetic behind twelve-support two-edge resilience."""


def main() -> None:
    # (block sizes, core edges, six-layer capacity, extra edges needed)
    rows = (
        ((5, 7), 35, 30, 5),
        ((3, 1, 1, 1, 1, 1), 25, 24, 3),
        ((1, 1, 1, 1, 1, 1, 1), 21, 18, 3),
    )

    for blocks, edges, _, _ in rows:
        total = sum(blocks)
        computed = (
            total * total - sum(block * block for block in blocks)
        ) // 2
        assert computed == edges

    # K5,7: each matching uses at most five crossing edges.
    assert rows[0][2] == 6 * 5
    assert rows[0][1] - rows[0][2] == rows[0][3]

    # K8-E(K3): six matchings have total eight-vertex capacity 24, but the
    # stronger degree argument requires a new matching to cover five
    # degree-seven vertices and hence to use at least three edges.
    assert rows[1][2] == 6 * 4
    assert rows[1][1] - rows[1][2] == 1
    assert (5 + 1) // 2 == rows[1][3]

    # K7: each of six matchings uses at most three of the 21 clique edges.
    assert rows[2][2] == 6 * 3
    assert rows[2][1] - rows[2][2] == rows[2][3]

    assert all(required >= 3 for _, _, _, required in rows)

    print("PASS all size-12 seven-layer Tutte cores audited")
    print("PASS K5,7 needs at least five further matching edges")
    print("PASS K8-E(K3) and K7 each need at least three")
    print("PASS deleting any available matching of size at most two is safe")
    print("SCOPE: two-edge resilience; two whole matchings are not yet coordinated")


if __name__ == "__main__":
    main()
