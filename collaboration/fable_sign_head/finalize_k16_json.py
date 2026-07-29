#!/usr/bin/env python3
"""Fallback finalizer: if a k16 sampler JSON is still missing, build it from
the secured cex side file plus the per-instance Hhat values recorded in the
sampler log.  Honest fields: n_sampled = lines actually completed; only the
cex tables are stored (sampled tables were not retained by the cut)."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_sign_head as V  # noqa: E402


def finalize(kind):
    main = HERE / f"falsify_k16_{kind}.json"
    if main.exists():
        print(f"[finalize] {kind}: sampler JSON already present, skipped")
        return
    side = HERE / f"cex_k16_{kind}.json"
    log = HERE / f"k16{kind}.log"
    cex = json.loads(side.read_text())
    vals = [int(m) for m in re.findall(r"instance \d+: Hhat = (-?1)",
                                       log.read_text())]
    F = V.wallis_sils()
    L, M = V.chart_from_sils(F, 17, 16)
    E, _, _ = V.E_of_chart(L, M, 16)
    rhs, _, _, _ = V.RHS_of_chart(L, M, 16)
    out = {"kind": kind, "k": 16, "chart": "wallis", "root": 16,
           "L": L, "M": M, "E": E, "RHS_F": rhs, "H_required": E * rhs,
           "n_sampled": len(vals),
           "Hhat_counts": {"+1": vals.count(1), "-1": vals.count(-1)},
           "instances": [cex["cex_base"], cex["cex_flip"]],
           "counterexample": ["cex_base", "cex_flip"],
           "note": ("Wallis chart; tables satisfy ONLY the per-ij trace"
                    if kind == "perij" else
                    "Wallis chart; tables satisfy ONLY condition 4")
           + "; sampling cut short under machine load -- n_sampled tables "
             "were computed (values in the log) but only the cex pair is "
             "stored; cex pair differs only in the "
           + ("(0,1) slice" if kind == "perij" else "N_{01} colouring")}
    main.write_text(json.dumps(out))
    print(f"[finalize] {kind}: built from cex + {len(vals)} logged samples "
          f"(+1: {vals.count(1)}, -1: {vals.count(-1)})")


if __name__ == "__main__":
    for kind in ("perij", "peruv"):
        finalize(kind)
