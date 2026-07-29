# Monolithic centre-0 star SAT path — final status (2026-07-26)

Path stood down by coordinator: certificate strategy moved to six per-family
exhaustion DRATs plus a compact six-family master DRAT (other agent).
The monolithic proof below is non-load-bearing. **No verdict was reached on
this path** (0 `s ...` verdict lines in either attempt log).

## CNF

- File: `star_centre0.cnf` (this directory)
- SHA-256: `cebb356895b6ffe61cb76afd50927474ff75706042e3c4830cc3b97da939ddcd`
- 35,504 variables / 87,360 clauses (6,384 primary), matching
  `evidence/cyclic17_star_structure.md`
- Generated deterministically (byte-identical on regeneration) by
  `evidence/odd_graph_local_ball/search_radius5_golf_cyclic_star_sat.py
  --centre 0 --source evidence/cyclic17_all_105_exact_slices_cross_seed.json
  --dimacs ... --audit-only` (repo file unmodified); the script's internal
  `dimacs_sha256` equals the shasum above.

## Solver attempts (cadical /opt/homebrew/bin/cadical, `-t 14400` wall limit)

| Attempt | Log | Wall (real) | CPU (process) | Max RSS | Termination |
|---|---|---|---|---|---|
| 1 | `cadical_star.attempt1_sigterm.log` | 3600.10 s | 771.72 s | 221.11 MB | SIGTERM at 3600.10 s wall; cause not independently verified — consistent with the harness background-task 1 h cap (`-t 14400` had not triggered) |
| 2 | `cadical_star.log` | 3267.38 s | 374.45 s | 155.25 MB | SIGTERM sent by coordinator (path deprioritized); run was nohup-detached, PID 22795, start epoch 1785067621 |

CPU << wall in both attempts: the machine was concurrently running other
sessions' cadical/CP-SAT jobs, so this solver got a minority CPU share.

- Attempt 2 partial DRAT: `star_centre0.drat`, 544,275,790 bytes, SHA-256
  `e7c7da26cd1c6b5c83f401344662c89be80664e5ebfe236356ea7ca9112aa0d3`.
  It is incomplete and carries no verdict, so the raw 519 MiB transient file
  is intentionally not versioned; the deterministic CNF and both complete
  attempt logs are versioned here.
- Attempt 1 partial DRAT (1,015,392,722 bytes) was deleted when relaunching
  from scratch, before the preserve instruction arrived. Not recoverable.

## Toolchain (ready, verified)

- `drat-trim/` cloned from github.com/marijnheule/drat-trim and built (gcc -O2).
- Control pipeline verified: `php43.cnf` (PHP(4,3)) -> cadical
  `s UNSATISFIABLE` -> drat-trim `s VERIFIED` (proof `php43.drat`).
- SAT-branch tools ready but unused: `decode_star_model.py` (model -> phase
  witness via the repo encoder's variable layout) and
  `verify_star_witness.py` (independent semantic check; negative-tested —
  rejects an all-zero witness).

## Conclusion

Monolithic direct-star SAT route: UNKNOWN / abandoned by instruction.
No SAT model and no UNSAT proof exists on this path; the per-family
exhaustion + master DRAT route (other agent) is the load-bearing certificate.
