# Claude Fable 5 xhigh: unrestricted Erdős--Rosenfeld #835 resume

Work in `/Users/dennison/Documents/Math Problem`.

Use `/efficient-fable` first.  Act as the senior mathematical orchestrator and
skeptical final judge.  Cheaper agents are already doing the token-heavy
orbit-certificate generation and replay; reserve Fable's reasoning for
selecting and integrating a route that can actually settle the unrestricted
problem.

## Objective

Resolve Erdős--Rosenfeld Problem #835: decide whether there is any \(k>2\)
with

\[
\chi(J(2k,k))=k+1,
\]

equivalently any \(LS(k-1,k,2k)\).  A construction for one admissible \(k\)
settles it positively.  A negative solution must cover every admissible
parameter, hence the infinite surviving prime family.

Read these current frontier files rather than treating the long README as a
proof:

* `collaboration/opus5/full_problem_resume_2026-07-28/STATUS.md`
* `collaboration/opus5/full_problem_resume_2026-07-28/FIXED_RUNG_EXISTENCE.md`
* `collaboration/opus5/full_problem_resume_2026-07-28/PROOF.md`
* `collaboration/opus5/projection_rigidity_attack_2026-07-28/INDEPENDENT_AUDIT.md`
* `collaboration/opus5/post_r0_global_bridge/INDEPENDENT_AUDIT.md`
* `collaboration/independent/conflict_cohomology_2026-07-29/PROOF.md`
* `collaboration/independent/conflict_cohomology_2026-07-29/STATUS.md`
* `collaboration/opus5/prompts/2026-07-29_conflict_cycle_obstruction_prompt.md`
* `collaboration/opus5/prompts/2026-07-29_bcz_equitable_partition_prompt.md`
* `erdos_835_conjectural_resolution.md`

The fixed-rung correction is load-bearing: Keevash implies
\(LS(t,t+1,t+p)\) exists for every fixed \(t\) and all sufficiently large
primes \(p\).  Thus a uniform negative proof cannot obstruct one fixed low
rung.  It must use a rung \(t=t(p)\) growing with \(p\), the top rung, or an
interaction across rungs.

The restricted orbit campaign is independently closing a local \(r=0\)
matching lemma.  Even closing all sixteen support orbits would still leave
first-lift compatibility and fan-realizability.  Treat that campaign as
supporting evidence, not a substitute for the global theorem.

## Assignment

1. Compare the strongest surviving positive and negative routes and select the
   one most likely to reach unrestricted #835.
2. Perform one technically complete attack on the selected route.  High-value
   candidates include:
   * the exact \(\mathbb F_2\) cochain/row-space criterion for the residual
     two-colour conflict graph, especially its top-rung common
     odd-transversal/odd-trade form at \(t=p-2\);
   * complement-folded top-rung invariants stronger than the known vacuous
     parity count;
   * interaction between adjacent large-set rungs rather than a fixed-rung
     obstruction;
   * a construction mechanism that coherently lifts Keevash-style fixed-rung
     existence through the whole tower.
3. Check every proposed universal statement against the known positive
   \(LS(2,3,9)\) control and against the exact scope of Keevash's theorem.
4. If a route fails, prove the strongest exact failure theorem and identify
   one sharply formulated remaining lemma.  Do not turn a route closure,
   restricted case, or necessary feasible condition into a claimed solution.

## Deliverables

Create only `collaboration/fable_global_resume_2026-07-29/` containing:

* `JUDGMENT.md` -- solved/not-solved verdict, route comparison, and exact scope;
* `PROOF.md` -- complete proofs of unconditional new results only;
* `IDEAS.md` -- unproved directions, counterexamples, and the single best next
  attack;
* a standard-library exact verifier if computation supports any finite claim.

Do not edit existing files, commit, or push.  Do not claim #835 solved without
either an explicit block-by-block construction or a theorem covering the
entire admissible family.  Cost is not a stopping criterion.
