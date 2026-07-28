# Opus 5 max-effort: the post-\(r=0\) global bridge for Erdős--Rosenfeld #835

Date: 2026-07-28

You are Claude Opus 5 at maximum reasoning effort, acting as the core
research mathematician on Erdős--Rosenfeld Problem #835.

## Actual target and honesty condition

The actual target is the first open case \(k=16\) of

\[
\chi(J(2k,k))\ge k+2\qquad(k>2),
\]

equivalently the nonexistence of a tight 17-colouring of \(J(32,16)\), or
the nonexistence of the equivalent \(LS(14,15,31)\)/Odd-graph cover object.

The current 13-vertex matching problems are local first-lift instances.
Even a complete theorem for all of them is not #835.  Never call the
problem solved unless every local-to-global implication is proved.

## Current frontier

Read `README.md` first.  Then read at least:

- `collaboration/opus5/coordinated_nine_and_global_bridge/NOTE.md`
- `collaboration/opus5/coordinated_nine_and_global_bridge/AUDIT.md`
- `collaboration/unrestricted_lift_tower/NOTE.md`
- `collaboration/first_lift_support_completion/NOTE.md`
- `collaboration/first_lift_partial_factorization_audit/NOTE.md`
- `collaboration/first_lift_global_theorem/NOTE.md`
- `collaboration/first_lift_global_theorem/SIX_PACKING_NOTE.md`
- `collaboration/first_lift_global_theorem/SEVEN_PACKING_R0_NOTE.md`
- `collaboration/first_lift_global_theorem/EIGHTH_MATCHING_CORE_CATALOGUE.md`
- `collaboration/first_lift_global_theorem/TWO_STAR_NOTE.md`
- `collaboration/opus5/first_lift_classB_attack/NOTE.md`
- `collaboration/coordinated_nine_structural/NOTE.md`
- `collaboration/r2_cross_route_reduction/NOTE.md`
- `collaboration/opus5_r0_orbit_repair/2026-07-28_cut_selection_theorem.md`
- `collaboration/opus5_r0_orbit_repair/2026-07-28_prescribed_colour_remaining_audit.md`

The certified local campaign has closed prescribed-colour support orbits
0 through 4.  Orbit 5 is solver-terminal in all 17 exact pair types and is
under independent DRAT certification.  The other eleven local Venn types
have an independently audited finite reduction.  For this assignment you
may work conditionally on the eventual theorem that every \(r=0\)
cut-feasible selected triple has its prescribed three matchings, but you
must label that theorem as a hypothesis.

The profiles \(r=1,2,3,4,5\) already have coordinated-nine theorems.  The
first-lift work also has many partial completions, counterexamples to
arbitrary-prefix extension, and exact switching delimiters.  Do not repeat
or silently contradict those results.

The earlier Opus audit identified the next tower coupling as six
simultaneous same-colour matchings across six class-B instances.  That
statement needs to be reconstructed and proved precisely before it can be
used.

## Primary assignment

Do the heavy mathematical work on the earliest post-local gap.  Seek, in
order:

1. a solver-free theorem upgrading coordinated nine in every class-B
   profile to a complete 17-matching first-lift completion, allowing
   coordinated switches of earlier layers;
2. if that is false, an exact legitimate class-B counterexample and the
   minimal additional invariant that restores a true theorem;
3. a rigorous local-to-global theorem expressing the six simultaneous
   same-colour coupling, with all quantifiers and shared data explicit;
4. either a proof that this global coupling always completes, or a
   contradiction/no-go invariant strong enough to exclude the hypothetical
   \(k=16\) cover.

Prefer a structural proof.  A finite reduction is acceptable only if its
state space is proved complete and it has a realistic independently
checkable certificate format.  Search scripts may find lemmas or
counterexamples, but bounded search is evidence only.

Be especially alert to:

- arbitrary-prefix extension is false;
- per-instance completion does not imply simultaneous same-colour
  completion across the six coupled instances;
- choosing witnesses independently can violate the shared tower data;
- a SAT model of a relaxation is not a cover;
- UNSAT of one fixed witness does not prove an existential repair theorem;
- switching an early matching changes every later residual graph that
  depends on it.

## Deliverable

Work only inside:

`collaboration/opus5/post_r0_global_bridge/`

Create `NOTE.md` containing:

- exact definitions of every local and global object used;
- the earliest missing implication, written with full quantifiers;
- every theorem, counterexample, or finite reduction you establish;
- complete proofs for mathematical claims;
- exact commands and scripts for computational claims;
- a section named `Independent audit surface`;
- a section named `Gap audit`;
- a section named `Scope relative to #835`; and
- a final verdict: proved, refuted, reduced, or still open.

Add verifier/search scripts only in that same folder.  Do not edit existing
files.  Do not include secrets, local account identifiers, or raw internal
reasoning streams in repository files.

Continue through false starts.  A rigorous counterexample to the current
bridge or a sharply smaller exact global coupling is valuable.  Do not stop
at an attractive conjecture.
