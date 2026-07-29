# Freeze record — sign-head export (2026-07-26)

Exported after coordinator-stop of the sign-head subagent (time-boxed);
`verify_sign_head.py` re-run at freeze: **ALL PARTS PASS**.

**Subsequent update.**  The open full-two-sided sign question recorded in this
freeze was later settled in
[`../global_h_parity/README.md`](../global_h_parity/README.md): the individual
layers have exact one-factorization formulas, and their total is identically
the existing flag formula \(F(L,M)\).  This bundle is preserved as the Fable
exploration and falsification record; its old “OPEN” labels are not the current
status of that sign subproblem.  Problem #835 itself remains open.

Contents and status labels:
- `sign_head_note.md`: the agent's corrected note — identity (H) with
  E-lemma (E(L,M) ≡ +1, PROVED, coordinator-audited independently),
  H_required vs observed products distinguished throughout, and the
  repaired §4 (no inference from nonextendible radius-3 charts).
- One-sided and partial two-sided falsification data (COMPUTATION):
  `cex_k16_perij.json` / `cex_k16_peruv.json` hold minimal-flip
  counterexample pairs with opposite observed products — each fibering
  alone cannot decide H; `joint_k16_pairs*.json` and
  `joint_k16_partial.json` show BOTH signs on partial two-sided
  tables. Each JSON records exactly which per-ij / per-uv / palette /
  shared-N constraints its instances satisfy (see the `note` and
  constraint fields; the verifier re-checks them with assertions).
- `joint_k8_trace_cond4.json`: solver-INFEASIBLE record for that
  joint relaxation at k=8 (no instances; nothing re-verifiable).
- Coloured-tensor augmentation insight (each finite colour x augments
  to a no-hole K_k x K_k tensor by adjoining {L_i^{-1}(x),L_j^{-1}(x)}
  and a dummy M_i x-matching; computations reproduce formula (F)):
  recorded as USER-STATED, audit **OPEN** — not certified here.
- OPEN: whether genuine complete two-sided N-tables force a universal
  or (L,M)-dependent H. Nothing here excludes unrestricted k=16.
  **#835 is not solved.**
Hashes: `SHA256SUMS` (this directory). Left uncommitted deliberately.
