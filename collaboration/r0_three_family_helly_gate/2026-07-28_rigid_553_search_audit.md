# Audit of the rigid \(5+5+3\) factor-witness search

Date: 2026-07-28.

## Purpose

`search_rigid_553_factor_witness.py` freezes the first equality case left by
the Tutte--Lovász factor audit.  It is a diagnostic and certificate
generator, not the primary proof: the two short capacity-cut contradictions
in `../opus5_r0_orbit_repair/2026-07-28_cut_sufficiency_agent_factor_complete.md`
now settle the case solver-free.

## Symmetry correction

The first experimental version reused vertex-symmetry constraints from the
general support-orbit search.  Those constraints permuted vertices within a
selected-row membership cell.  After fixing a new labelled
\(A\dot\cup B\dot\cup C\) partition, such permutations need not preserve the
new constraints and therefore were not valid symmetry breaking.

The shared builder now has an explicit `vertex_symmetry` option, defaulting
to the original behaviour.  The rigid driver sets it to `False`.  No UNSAT
result obtained before that correction is used.

## Corrected controls

With partition-preserving symmetry:

- the prefix-only model without capacity cuts is SAT;
- the exact full-row model without capacity cuts is SAT;
- after installing every capacity cut, all seven eligible support orbits
  and both boundary profiles \((3,1,1)\), \((3,3,1)\) are UNSAT.

The SAT controls are important: they show that the corrected encoding does
not accidentally forbid the rigid degree pattern and that condition (C) is
the exact ingredient eliminating it.

The corrected all-orbit run wrote fourteen CNFs under the temporary path
`/private/tmp/erdos835-rigid-553-corrected-20260728/`.  They are deliberately
marked `proof_claimed: false`, because the solver-free factor proof is
shorter and stronger.

## Code checks

Both modified search files pass Ruff and Python byte-compilation.  Existing
callers retain the original builder semantics because the new
`matching_constraints`, `fixed_prefix_sizes`, and `vertex_symmetry`
parameters all default to the prior settings.

