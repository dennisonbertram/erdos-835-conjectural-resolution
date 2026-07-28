#!/usr/bin/env python3
"""Audit the cut arithmetic in the rigid all-seven-rows repair branch."""

from __future__ import annotations


def maximum_lhs(p: int, q: int) -> int:
    """Worst capacity demand of three triple rows contained in a 7-set W."""
    size = p + q
    minimum_row_intersection = max(0, q - 4)
    per_row = max(0, size - 5 - minimum_row_intersection)
    return 3 * per_row


def residual_edge_lower_bound(p: int, q: int) -> int:
    """Lower bound after replacing one U-edge and one W-edge by two crossings."""
    crossing = max(0, p * q - 2)
    whole_u = 3 if p == 6 else 0
    whole_w = 8 if q == 7 else 0
    return crossing + whole_u + whole_w


def main() -> None:
    checked = []
    for p in range(7):
        for q in range(8):
            size = p + q
            if size not in (6, 7, 8):
                continue
            required = maximum_lhs(p, q)
            available = residual_edge_lower_bound(p, q)
            assert required <= available, (p, q, required, available)
            checked.append((p, q, required, available))

    # Larger cuts are automatic from minimum degree seven; smaller ones have
    # zero positive demand.
    assert len(checked) == 20
    print("PASS: all 20 feasible (p,q) types of sizes 6,7,8 satisfy (C)")
    print("PASS: bounds use only 3 U-edges, 8 W-edges, and at most 2 lost crossings")


if __name__ == "__main__":
    main()
