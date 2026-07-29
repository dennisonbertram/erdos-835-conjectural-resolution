#!/usr/bin/env python3
"""Bounded standalone one-slice / one-edge cex hunter for the k=16 JSONs.

Usage: python3 -B hunt_cex_k16.py perij|peruv [max_tries]
Loads falsify_k16_<kind>.json, rebuilds the base instance from its seed,
resamples ONLY the (0,1) slice (perij) or the N_{01} colouring (peruv)
until Hhat flips, then appends the cex pair to the JSON.
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_sign_head as V  # noqa: E402
import gen_tables as G  # noqa: E402


def main(kind, max_tries):
    k = 16
    name = HERE / f"falsify_k16_{kind}.json"
    F = V.wallis_sils()
    L, M = V.chart_from_sils(F, 17, 16)
    pairs = [(i, j) for i in range(k - 1) for j in range(i + 1, k - 1)]
    edges = [(u, v) for u in range(k) for v in range(u + 1, k)]
    if kind == "perij":
        rng = random.Random(40000)
        base = {p: G.gen_slice(L, k, p[0], p[1], rng) for p in pairs}
        Nb = G.perij_table_from_slices(base, k)
    else:
        rng = random.Random(50000)
        base = {e: G.gen_peruv_colouring(L, M, k, e[0], e[1], rng)
                for e in edges}
        Nb = G.peruv_table_from_colourings(base, k)
    hb, _ = V.hhat_of_table(Nb, k)
    print(f"base Hhat = {hb}", flush=True)
    for s in range(max_tries):
        rng2 = random.Random(900000 + s)
        if kind == "perij":
            mod = dict(base)
            mod[(0, 1)] = G.gen_slice(L, k, 0, 1, rng2)
            N2 = G.perij_table_from_slices(mod, k)
        else:
            mod = dict(base)
            mod[(0, 1)] = G.gen_peruv_colouring(L, M, k, 0, 1, rng2)
            N2 = G.peruv_table_from_colourings(mod, k)
        h2, _ = V.hhat_of_table(N2, k)
        print(f"try {s}: Hhat = {h2}", flush=True)
        if h2 != hb:
            cex = {"cex_base": {"tag": "cex_base", "seed": "base",
                                "N": G.enc_table(Nb), "Hhat": hb},
                   "cex_flip": {"tag": "cex_flip", "seed": 900000 + s,
                                "N": G.enc_table(N2), "Hhat": h2}}
            side = HERE / f"cex_k16_{kind}.json"
            side.write_text(json.dumps(cex))
            print(f"cex found at try {s}; wrote {side.name}", flush=True)
            if name.exists():
                obj = json.loads(name.read_text())
                obj["instances"].extend(cex.values())
                obj["counterexample"] = ["cex_base", "cex_flip"]
                name.write_text(json.dumps(obj))
                print("main JSON updated with cex pair", flush=True)
            return
    print("no cex within budget", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 40)
