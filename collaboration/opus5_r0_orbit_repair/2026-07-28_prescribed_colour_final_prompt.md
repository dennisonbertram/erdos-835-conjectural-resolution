# Claude Opus 5 max: finish the ambient prescribed-colour factor theorem

Work independently at maximum mathematical effort. Return at most 45,000
tokens. Read these repository artifacts first:

- `collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_final_prompt.md`
- `collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_gate.md`
- `collaboration/opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_complete.md`
- `collaboration/opus5_r0_orbit_repair/2026-07-28_colour_factor_agent_audit.md`
- `collaboration/r0_three_family_helly_gate/2026-07-28_orbit0_cut_sufficiency.md`

The factor theorem in the third file has now been independently line-audited:
the full row equations plus every capacity cut (C) imply a simple
`b`-factor `H subset G`, where `b(v)=3-t(v)`.  Orbit 0 (three identical
selected rows) also has a separate computer-assisted proof of the full
prescribed-colour conclusion.

The sole local gap is now:

> Prove that among the simple `b`-factors of `G`, at least one has a
> nowhere-zero `F_2^2` boundary flow with
> `sigma(v)=xor{i:v in S_i}`, equivalently splits into the three prescribed
> edge-disjoint perfect matchings; or give a complete full-row
> counterexample.

Do not claim that an arbitrary `b`-factor is colourable.  The colour audit
gives explicit uncolourable exact-degree factors in all 16 Venn types, and
even component balance plus every bridge-side test is insufficient.

Promising interface:

1. Choose a `b`-factor minimizing, lexicographically, the number of zero
   coordinates over its affine `F_2^2` boundary-flow space and the size of
   the smallest zero-coordinate cover.
2. Analyze degree-preserving alternating switches along even cycles or
   symmetric differences inside the dense ambient graph `G`.
3. Prove that any minimal uncolourable factor yields one of the binding
   six-, seven-, or eight-set cuts already forbidden by (C).

Other valid routes are welcome: an explicit resource gadget with a complete
Tutte/Hall family, a direct maximal-three-near-matchings argument, or a
finite reduction covering the remaining 15 Venn types.

Required return:

1. exact verdict;
2. every lemma instantiated in this 13-vertex/full-row setting;
3. a complete switching proof or a complete explicit counterexample;
4. no appeal to arbitrary-factor colourability, ordinary cubic
   colourability, component parity alone, or unproved minimal-obstruction
   folklore;
5. if incomplete, the earliest exact missing implication and the strongest
   rigorously proved new lemma.
