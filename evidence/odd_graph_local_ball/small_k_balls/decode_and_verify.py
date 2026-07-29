#!/usr/bin/env python3
"""Decode a cadical SAT model for the encode_cnf encoding and verify it
with the independent semantic checker (ball_defs).

Usage: decode_and_verify.py K RADIUS cadical_output_file witness_out.json
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ball_defs  # noqa: E402
from encode_cnf import Enc, parse_cadical_model  # noqa: E402


def main():
    k = int(sys.argv[1])
    radius = int(sys.argv[2])
    model_file = sys.argv[3]
    out = sys.argv[4]

    enc = Enc(k, radius)  # rebuild variable numbering only (no clauses)
    with open(model_file) as fh:
        true_vars = parse_cadical_model(fh.read())
    L, M, N, P = enc.decode_model(true_vars)

    if radius == 4:
        fails = ball_defs.check_radius4(k, L, M, N)
    else:
        fails = ball_defs.check_radius5(k, L, M, N, P)
    if fails:
        print(f"SEMANTIC CHECK radius-{radius} k={k}: FAIL")
        for f in fails[:20]:
            print("  ", f)
        sys.exit(1)
    print(f"SEMANTIC CHECK radius-{radius} k={k}: PASS")

    with open(out, "w") as fh:
        json.dump(ball_defs.to_json_dict(k, L, M, N, P), fh, indent=1)
    print(f"witness written: {out}")


if __name__ == "__main__":
    main()
