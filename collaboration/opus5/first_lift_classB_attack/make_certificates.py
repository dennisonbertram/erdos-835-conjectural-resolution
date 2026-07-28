#!/usr/bin/env python3
"""Produce the certificates re-checked by verify_classB.py.

Every certificate stores only data that the verifier re-derives or re-checks
from the definitions; nothing here is trusted.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

from classb import (check_class_B, cut_certificates, lp_feasible, solve_dfs,
                    solve_sat, supports, mvec)
from conditions import bc_violations, vertex_hall

HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "certificates")
OLD = os.path.join(HERE, "..", "first_lift_k13_hole", "certificates")


def frac_list(xs):
    return [[t.numerator, t.denominator] for t in xs]


def store(name, d):
    with open(os.path.join(CERTS, name), "w") as fh:
        json.dump(d, fh)
    print("wrote", name)


def build(name, n, q, forb, note):
    check_class_B(n, q, forb)
    st, _, nodes = solve_dfs(n, q, forb, node_budget=10 ** 9)
    assert st == "UNSAT", st
    assert solve_sat(n, q, forb)[0] == "UNSAT"
    d = dict(n=n, q=q, forb=list(forb), note=note,
             supports=supports(n, q, forb), m=mvec(n, q, forb),
             cut_violations=len(cut_certificates(n, q, forb)),
             hall_violations=len(vertex_hall(n, q, forb)),
             bc_violations=len(bc_violations(n, q, forb)) if n <= 9 else None,
             dfs_nodes=nodes)
    ok, w = lp_feasible(n, q, forb)
    d["lp_feasible"] = ok
    if ok:
        d["lp_point"] = frac_list(w)
    else:
        d["farkas"] = frac_list(w)
    store(name, d)
    return d


if __name__ == "__main__":
    os.makedirs(CERTS, exist_ok=True)

    # (1) n = 7, class B, (BC)-clean, LP INFEASIBLE, no completion.
    build("n07_BCclean_LPinfeasible.json", 7, 11,
          [465, 107, 1580, 908, 865, 796, 920],
          "class-B instance at n=7 violating no (BC) condition; the fractional "
          "relaxation is infeasible (exact Farkas certificate stored)")

    # (2) n = 7, class B, (BC)-clean, LP FEASIBLE, still no completion.
    build("n07_BCclean_LPfeasible.json", 7, 11,
          [307, 752, 1256, 181, 1828, 1039, 842],
          "class-B instance at n=7 violating no (BC) condition whose fractional "
          "relaxation IS feasible (exact rational point stored) and which still "
          "has no completion: the obstruction here is purely integral")

    # (3) n = 9, class B, (BC)-clean, no completion.
    build("n09_BCclean.json", 9, 13,
          [5145, 5920, 2466, 1832, 214, 7180, 5416, 4904, 2198],
          "class-B instance at n=9 violating no (BC) condition and with no "
          "completion; its fractional relaxation is infeasible")
