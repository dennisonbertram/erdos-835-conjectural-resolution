#!/usr/bin/env python3
"""Run the exact dead-prefix CEGAR engine on the r=4 certificate."""

from __future__ import annotations

import search_r2_dead_seven_prefix as engine
import verify_r4_dead_seven_prefix as certificate


def main() -> None:
    # The selected layer sizes are the same as r=2.  Only the ten remaining
    # complement sizes and the semantic certificate module differ.
    engine.COMPLEMENT_SIZES = (5,) * 7 + (3,) + (1,) * 2
    engine.build_certificate = certificate.build_certificate
    engine.verify_certificate = certificate.verify_certificate
    engine.main()


if __name__ == "__main__":
    main()
