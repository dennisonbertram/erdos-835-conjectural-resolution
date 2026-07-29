# Opus 5 maximum-effort resume: resolve the full Erdős--Rosenfeld #835

Date: 2026-07-28

You are Claude Opus 5 at maximum reasoning effort, acting as the principal
research mathematician. Invoke `/efficient-frontier` first if it is
available. Cost is not a stopping condition.

## Exact objective

Resolve the full existential problem:

> Does there exist any integer \(k>2\) for which
> \(\chi(J(2k,k))=k+1\)?

Equivalently: does any large set \(LS(k-1,k,2k)\) exist for \(k>2\)?

A single rigorously verified construction for one admissible \(k\) resolves
the problem positively. A negative resolution must cover every \(k>2\), not
only \(k=16\). Excluding \(k=16\) alone is not a solution.

## Mandatory strategic correction

The current local \(K_{13}\)-matching/orbit campaign is only a first-lift
gate at \(k=16\). Even closing all sixteen local orbit types leaves:

1. existential completion from coordinated nine to all seventeen matchings;
2. simultaneous choices across all \(5\)-sets and \(6\)-sets;
3. construction of the simultaneous \(13\)-fan / \(LS(3,4,20)\) shadow;
4. every higher level through the full \(LS(15,16,32)\) tower.

Do not spend this run improving those local orbit certificates. The previous
run in `collaboration/opus5/post_r0_global_bridge/` already isolated the
level-2 coupling and proved that a single \(R\)-local condition is only a
partial \(LS(2,3,19)\), hence not an obstruction.

## Authoritative starting record

Read:

- `README.md`, especially its status and scope statements;
- `collaboration/opus5_full_resolution_brief.md`;
- `collaboration/opus5_frontier_resume_v2_prompt.md`;
- `collaboration/opus5/post_r0_global_bridge/NOTE.md`;
- `collaboration/opus5/post_spectrum_kernel_synthesis/NOTE.md`;
- `collaboration/opus5/joint_schreier_krein_attack/NOTE.md`;
- `collaboration/opus5/staircase_support_frontier/NOTE.md`;
- `collaboration/general_h1_rigidity/README.md`;
- `collaboration/general_h2_rigidity/README.md`;
- `collaboration/schreier_h3_support/README.md`;
- `collaboration/schreier_h4_support/README.md`;
- `collaboration/fable_e4_v2/JUDGMENT.md`;
- `collaboration/fable_e4_v2/PROOF.md`.

Use targeted search to inspect directly relevant verifier sources and other
notes. Do not reread the entire repository linearly.

Current honest frontier:

- divisibility reduces possible parameters to \(k=p-1\) with \(p\) prime;
- known results exclude the small cases through \(k=14\);
- \(k=16\) is the first open candidate and \(k=18\) is the next;
- the main additive, low-degree finite-field, few-coefficient, low-rank
  Pfaffian/Plücker, levelwise tower, coarse moment, quadratic leakage, and
  local counting routes have exact no-go/delimiter results;
- at \(k=16\), the Odd-graph cover formulation yields strong exact
  intersection-module and triangle-monodromy constraints but no
  contradiction;
- solver silence, a bounded search, a restricted ansatz, or one absent
  symmetric construction has no negative evidentiary value.

## Primary assignment

Personally choose and push the highest-value route capable of resolving the
full problem. Work through false starts. Favor one of:

1. **Positive construction.** Seek a tight colouring at \(k=16\), \(k=18\),
   or a later prime-form candidate using structure not already excluded.
   A formula must be proved proper on every Johnson edge; a finite witness
   must have a complete independently checkable certificate.
2. **Uniform negative theorem.** Seek an invariant applying to every
   prime-form \(k=p-1>2\), using the full family of colour classes rather
   than a single Steiner system. Plausible surfaces include higher
   Johnson-module Schur/Krein positivity, integral or 2-adic constraints,
   covering monodromy, and cross-colour compatibility.
3. **A decisive finite reduction for one positive candidate.** This is useful
   only if SAT would yield a full colouring and UNSAT has a proved-complete,
   independently replayable certificate. A shadow such as
   \(LS(3,4,20)\) is not the full object.

Do not return only a survey or a list of ideas. Establish at least one new
rigorous lemma, exact failure boundary, construction candidate with complete
edge proof, or sharply smaller complete decision problem.

## Deliverable

Work only inside:

`collaboration/opus5/full_problem_resume_2026-07-28/`

Create:

- `STATUS.md`: live verdict, strongest new result, exact gap;
- `PROOF.md`: complete arguments only;
- `IDEAS.md`: unproved ideas and failed routes, labelled honestly;
- verifier/search scripts for finite claims.

Include sections:

- `Independent audit surface`
- `Scope relative to the full #835`
- `Why this does or does not prove the full problem`

Do not edit existing files. Do not include secrets, account identifiers, or
raw internal reasoning. Continue through false starts and use the available
time for decisive mathematics.
