"""Solve every second-star branch of a G1 instance and record the verdicts.

Each branch CNF is written, solved with CaDiCaL, and deleted.  Progress is
printed as branches finish; a JSON record is written only after the whole
sweep returns.  A branch that times out is recorded as UNKNOWN and is NOT
evidence of anything.  An exit-code-20 result is only a candidate UNSAT
verdict: this script does not request or check a proof certificate.

    python3 -B run_branches.py <n> <s> <m> <workdir> <per_branch_seconds> [jobs]
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from g1_cnf import build_cnf, write_dimacs
from second_star_split import branch_representatives, branch_units


def solve_branch(args) -> dict:
    k, phi, clauses, nvars, n, s, m, workdir, limit = args
    fd, path = tempfile.mkstemp(suffix=f".b{k:03d}.cnf", dir=workdir)
    os.close(fd)
    model = f"{workdir}/branch{k:03d}.model"
    try:
        write_dimacs(path, clauses + branch_units(n, s, m, phi), nvars)
        proc = subprocess.run(
            ["cadical", "-q", "-t", str(limit), "-w", model, path],
            capture_output=True,
            text=True,
        )
        code = proc.returncode
        status = {10: "SAT", 20: "UNSAT"}.get(code, f"UNKNOWN(exit {code})")
    finally:
        Path(path).unlink(missing_ok=True)
    if status != "SAT":
        Path(model).unlink(missing_ok=True)
    rec = {
        "branch": k,
        "status": status,
        "phi": {str(a): b for a, b in sorted(phi.items())},
    }
    print(f"  branch {k:03d}: {status}", flush=True)
    return rec


def main() -> None:
    n, s, m = (int(a) for a in sys.argv[1:4])
    workdir = sys.argv[4]
    limit = int(sys.argv[5])
    jobs = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    Path(workdir).mkdir(parents=True, exist_ok=True)

    clauses, nvars, meta = build_cnf(n, s, m)
    reps = branch_representatives(m - 2)
    print(json.dumps(meta), flush=True)
    print(f"{len(reps)} branches, {limit}s each, {jobs} in parallel", flush=True)

    tasks = [
        (k, phi, clauses, nvars, n, s, m, workdir, limit) for k, phi in enumerate(reps)
    ]
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        recs = list(pool.map(solve_branch, tasks))

    with (Path(workdir) / "verdicts.json").open("w") as f:
        json.dump(recs, f, indent=1)

    counts: dict[str, int] = {}
    for r in recs:
        key = r["status"].split("(")[0]
        counts[key] = counts.get(key, 0) + 1
    print("SUMMARY", json.dumps(counts), flush=True)
    if counts.get("SAT"):
        print("SAT branch found -- run verify_solution.py on its model", flush=True)
    elif counts.get("UNKNOWN"):
        print("INCONCLUSIVE: some branches did not terminate; no verdict", flush=True)
    else:
        print(
            f"ALL {len(recs)} BRANCHES REPORTED UNSAT by the solver; "
            "no mathematical conclusion until proof certificates are independently checked",
            flush=True,
        )


if __name__ == "__main__":
    main()
