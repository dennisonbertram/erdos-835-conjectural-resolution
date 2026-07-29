# Small-k unrestricted local-ball decisions — certified results and pending runs

Date: 2026-07-26.  Instances defined by `ball_defs.py` + `encode_cnf.py`
(deterministic generators, this directory) from the radius-4/-5
conditions of `../radius4_reduction.md` and `../radius5_reduction.md`.
The forced-trace consequence is proved separately in
`../radius5_minimal_trace_forced.md`. Solver: CaDiCaL 3.0.1
(`cadical CNF PROOF` with DRAT output). Checker: drat-trim at source
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (built from
github marijnheule/drat-trim during this session; pigeonhole PHP(4,3)
control pipeline returned `s VERIFIED` before first use). Independent
semantic verifier: `decode_and_verify.py` (checks conditions 1–4 and
the radius-5 constraints directly from definitions, not the encoding).
Hashes: `SHA256SUMS` (CNFs, DRATs, gzipped pieces; the plain
`k6_r5.drat` hash is included; its gzip here is 13.4 MB, GitHub-safe).
The fresh source, certificate, and positive-control recheck is recorded in
`INDEPENDENT_AUDIT.md`.

## Encoder faithfulness gate (passed)

The radius-4 encoder, with (L, M) pinned to the audited k=16 Wallis
chart, is SATISFIABLE (`k16_r4_wallisfix.cadical.log`); the decoded
witness (`k16_r4_encoder_control_witness.json`,
`wallis_k16_radius4_witness.json`) passes the independent semantic
check on all 120 N-slices (`control_k16.py`).  The known-good chart
being admitted is a positive control against gross overconstraint. The
DRAT proofs certify the generated formulas; the mathematical conclusions
also depend on the audited correspondence between those formulas and the
definitions.

## CERTIFIED results (final)

| instance | meaning | verdict | proof | checker |
|---|---|---|---|---|
| `k4_r4` | radius-4 ball, k=4 | **UNSAT** | `k4_r4.drat` (8.6 KB) | drat-trim `s VERIFIED` (`k4_r4.drat-trim.out`) |
| `k4_r5` | radius-5 ball, k=4 | **UNSAT** | `k4_r5.drat` (14 KB) | drat-trim `s VERIFIED` (`k4_r5.drat-trim.out`) |
| `k6_r5` | radius-5 ball, k=6 | **UNSAT** | `k6_r5.drat.gz` (13.4 MB; plain hash in SHA256SUMS) | drat-trim `s VERIFIED`, 0 RAT, 472.074 s (`k6_r5.drat-trim.out`) |

Consequences, stated with the faithfulness caveat that the encoding is
audited via the Wallis gate and the semantic verifier: **the
unrestricted local ball of the odd graph fails already at radius 4 for
k=4, and at radius 5 for k=6** — purely local exclusions of those two
parameter values relevant to Erdős–Rosenfeld #835 (both exclusions were
long known globally; the local mechanism is the new content). No radius-5
witness exists at either decided value, so these tests do not supply a
positive small-order instance for the flag-sign programme.

## PENDING (explicitly not proved)

- `k6_r4`: an external CP-SAT run reported INFEASIBLE, but this directory
  contains no proof certificate for that run; the cadical DRAT run was
  still executing at the report date — **no certified verdict here**.
  Structural probe (CP-SAT OPTIMAL + semantic PASS): conditions 1–3
  alone are feasible at k=6, so any radius-4 failure lives at the joint
  N-layer (condition 4), unlike k=4 where conditions 1–2 already clash.
- `k8_r4`, `k8_r5`: cadical running — **no verdict**.  (Raw CNFs and
  eventual proofs will be appended when they land.)

## Reproduce

```sh
python3 -B encode_cnf.py 4 4 k4_r4.cnf   # etc.
cadical k4_r4.cnf k4_r4.drat            # exit 20 = UNSAT
drat-trim k4_r4.cnf k4_r4.drat          # s VERIFIED
python3 -B decode_and_verify.py 16 4 k16_r4_wallisfix.cadical.log witness.json
python3 -B control_k16.py                # regenerate the Wallis semantic witness
shasum -a 256 -c SHA256SUMS
```

Scope: these are statements about local balls of
\(O_k=KG(2k-1,k-1)\) at small even \(k\). Nothing here decides \(k=16\)
(its radius-4 ball EXISTS
— the Wallis witness above), and **#835 is not solved**.
