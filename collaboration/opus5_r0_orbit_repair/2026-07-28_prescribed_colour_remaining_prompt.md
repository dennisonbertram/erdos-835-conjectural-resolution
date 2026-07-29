# Claude Opus 5 max: close the remaining prescribed-colour support orbits

Work independently at maximum mathematical effort.  This is Erdős–Rosenfeld
Problem #835, and the immediate target is the remaining local theorem in the
`r=0` coordinated-nine branch.  Return a rigorous proof, a rigorously
verified counterexample, or the strongest exact lemma with the first missing
implication.  Keep the final response under 80,000 tokens.

Read these current artifacts before reasoning:

- `collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_complete.md`
- `collaboration/opus5_r0_orbit_repair/2026-07-28_factor_complete_central_audit.md`
- `collaboration/opus5_r0_orbit_repair/2026-07-28_colour_factor_agent_audit.md`
- `collaboration/r0_three_family_helly_gate/2026-07-28_orbit0_cut_sufficiency.md`
- `collaboration/r0_three_family_helly_gate/2026-07-28_orbit1_cut_sufficiency.md`
- `collaboration/r0_three_family_helly_gate/2026-07-28_orbit1_support_cut_closure.py`
- `collaboration/opus5_r0_orbit_repair/2026-07-28_orbit3_support_closure.py`
- `collaboration/r0_three_family_helly_gate/search_counterexamples.py`

Established facts:

1. The full eleven-row equations plus every capacity cut (C) imply a simple
   exact-degree `b`-factor.  This theorem has been independently line-audited.
2. An arbitrary `b`-factor need not admit the prescribed
   nowhere-zero `F_2^2` boundary flow; explicit failures exist in all 16
   Venn types.  The ambient residual graph and factor switching are essential.
3. Orbit 0 is certified by two compatible-pair types.
4. Orbit 1 is now certified by five exhaustive terminal-path/cycle types;
   all five frozen UNSAT CNFs have independent DRAT verification.
5. Orbit 2 has a new, much shorter reduction.  Its rows are
   `012,012,123`, so the first two supports are identical.  Fix their
   compatible pair.  Its alternating two-factor has exactly three marked
   types: `C10`, `C4+C6` with the distinguished support-only vertex on
   `C4`, and `C4+C6` with it on `C6`.  A support-level relaxation using
   only `Delta(D)<=5`, `e_D(active)<=23`, and every capacity cut is UNSAT
   in all three types.  The actual two universally omitted vertices even
   give the stronger bound `e_D(active)<=20`.
6. Orbit 3 currently has 16 terminal UNSAT fixed-pair subcases in a sound
   support relaxation; external certificate replay is being completed.

Primary task:

> Find a human switching theorem, a compact exhaustive pair-union
> classification, or another exact reduction that proves cut sufficiency
> for all remaining Venn orbits.  Prefer a theorem parameterized by the
> seven Venn-cell counts rather than twelve unrelated solver campaigns.

You may use finite classification, but every symmetry reduction must be
proved orbit-complete and every SAT claim must be separable into a semantic
CNF reconstruction plus independently checkable proof traces.

In particular investigate:

- choosing the pair of supports with largest intersection or repeated row;
- the union of two perfect matchings on unequal ten-vertex supports, which
  is one terminal-to-terminal alternating path plus even cycles;
- whether the number of common-core vertices bounds the complete canonical
  pair catalogue uniformly;
- deletion-edge bounds obtained by removing vertices omitted from all three
  supports;
- whether the orbit-1 terminal-path catalogue extends directly to every
  Venn type after conditioning on a compatible pair;
- a lexicographically minimal uncolourable `b`-factor and its available
  two-switches.

Do not:

- assert arbitrary-factor colourability;
- infer the unrestricted theorem from orbit 0, 1, 2, or 3 alone;
- use component parity, bridge tests, or ordinary cubic colourability as if
  sufficient;
- hide a vertex-symmetry assumption after fixing row supports or a factor;
- call a bounded search a proof.

Required return:

1. exact verdict;
2. a self-contained mathematical reduction;
3. every remaining case and why the list is exhaustive;
4. a complete proof if achieved, otherwise the earliest exact gap;
5. any finite certificate specification detailed enough to reconstruct
   independently.
