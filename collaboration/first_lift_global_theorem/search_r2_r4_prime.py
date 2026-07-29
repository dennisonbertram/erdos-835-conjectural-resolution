#!/usr/bin/env python3
"""Discover class-B-prime partial factorizations for the r=2/r=4 cases."""

from __future__ import annotations

import argparse

import verify_r2_dead_seven_prefix as r2
import verify_r4_dead_seven_prefix as r4
from search_dead_prefix_partial_factorizations import (
    print_certificate,
    solve,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    args = parser.parse_args()
    for name, module in (("r2", r2), ("r4", r4)):
        prefix, complements = module.build_certificate()
        supports = module.verify_certificate(prefix, complements)
        print_certificate(name, *solve(supports, args.seconds))


if __name__ == "__main__":
    main()
