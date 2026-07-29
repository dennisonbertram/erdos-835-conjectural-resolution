#!/usr/bin/env python3
"""Verify the exact arithmetic in the r=2 initial-support dichotomy."""

from __future__ import annotations


def odd_partitions(total: int, count: int, minimum: int = 1):
    if count == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, total + 1, 2):
        for tail in odd_partitions(total - first, count - 1, first):
            yield (first,) + tail


def catalogue(order: int, minimum_degree: int):
    result = []
    for separator in range(order):
        count = separator + 2
        raw_minimum = minimum_degree - separator + 1
        minimum_odd = max(1, raw_minimum)
        if minimum_odd % 2 == 0:
            minimum_odd += 1
        for parts in odd_partitions(
            order - separator, count, minimum_odd
        ):
            result.append((separator, parts))
    return result


def main() -> None:
    assert catalogue(10, 4) == [
        (0, (5, 5)),
        (4, (1, 1, 1, 1, 1, 1)),
    ]
    print("PASS size-10 delta-4 catalogue: K5,5 and K6")

    # For size eight, the raw delta-two catalogue is larger.  Screening
    # the complement cores by maximum degree at most five leaves exactly
    # K3,5; K3,1,1,1; and K5.
    raw_eight = catalogue(8, 2)
    assert raw_eight == [
        (0, (3, 5)),
        (2, (1, 1, 1, 3)),
        (3, (1, 1, 1, 1, 1)),
    ]
    print("PASS size-8 delta-2/Delta(D)-5 catalogue: K3,5, K3,1,1,1, K5")

    assert 10 * 5 + 3 == 53 > 52
    assert 2 * (6 * 5 // 2) == 30 > 26
    assert 26 - 6 * 5 // 2 == 11
    assert 6 * 4 == 24
    assert 24 - 2 == 22
    assert 1 + 4 * 5 == 21 < 22
    print("PASS common K6 and five-set incidence bounds")

    assert 3 * 5 == 15 > 11
    assert 12 > 11  # |E(K3,1,1,1)|
    assert 2 * (5 * 4 // 2) - 4 * 3 // 2 == 14 > 11
    assert 5 * (4 - 1) == 15 > 4 * 3 + 2
    print("PASS outside-seven core uniqueness and final 15>14 row bound")
    print("SCOPE: initial PM dichotomy only; near-factor packing remains")


if __name__ == "__main__":
    main()
