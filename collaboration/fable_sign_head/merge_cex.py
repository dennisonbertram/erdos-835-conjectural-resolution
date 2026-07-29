#!/usr/bin/env python3
"""Merge cex_k16_<kind>.json side files (from hunt_cex_k16.py) into the
main falsify_k16_<kind>.json files, idempotently."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

for kind in ("perij", "peruv"):
    main = HERE / f"falsify_k16_{kind}.json"
    side = HERE / f"cex_k16_{kind}.json"
    if not (main.exists() and side.exists()):
        print(f"[merge] {kind}: skipped (main {main.exists()}, "
              f"side {side.exists()})")
        continue
    obj = json.loads(main.read_text())
    if obj.get("counterexample"):
        print(f"[merge] {kind}: main already has cex, skipped")
        continue
    cex = json.loads(side.read_text())
    obj["instances"].extend([cex["cex_base"], cex["cex_flip"]])
    obj["counterexample"] = ["cex_base", "cex_flip"]
    obj["note"] += ("; cex pair differs only in the (0,1) slice"
                    if kind == "perij"
                    else "; cex pair differs only in the N_{01} colouring")
    main.write_text(json.dumps(obj))
    print(f"[merge] {kind}: cex pair merged "
          f"({cex['cex_base']['Hhat']} vs {cex['cex_flip']['Hhat']})")
