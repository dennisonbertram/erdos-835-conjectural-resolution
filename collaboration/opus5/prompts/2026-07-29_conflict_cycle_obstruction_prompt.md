# Opus 5 max-effort task: the leftover conflict-graph obstruction for Erdős--Rosenfeld #835

Work in the repository `/Users/dennison/Documents/Math Problem`.

## Objective

Try to resolve Erdős--Rosenfeld Problem #835, not merely a restricted ansatz.
Use the exact tail reduction already proved in

* `collaboration/opus5/full_problem_resume_2026-07-28/PROOF.md`, especially
  Theorem 5 and Corollary 5.3;
* `collaboration/opus5/full_problem_resume_2026-07-28/IDEAS.md`, especially
  B.1;
* `erdos_835_conjectural_resolution.md`.

The decisive open question is this.  Put \(q=p\), where \(p=k+1\) is an odd
prime.  After choosing \(p-2\) pairwise block-disjoint
\(S(t,t+1,t+p)\)'s, the leftover \((t+1)\)-blocks form a
\((t+1)\)-regular conflict graph \(G_{\mathcal E}\): the two leftover
extensions of each \(t\)-set form one edge.  The partial large set extends
iff \(G_{\mathcal E}\) is bipartite.  A uniform proof that every such
leftover graph is non-bipartite at some necessary rung, for every prime
\(p\ge17\), would resolve #835 negatively.  An actual bipartition coherently
extending through the tower could support a positive construction.

Do the heavy mathematical lifting on that exact question.

## Required first move: derive the affine obstruction exactly

Let \(H_{\mathcal E}\) be the incidence matrix over \(\mathbb F_2\) whose rows
are \(t\)-sets and whose columns are leftover \((t+1)\)-blocks.  Every row has
two ones.  Prove carefully that bipartiteness is equivalent to solvability of

\[
H_{\mathcal E}x=\mathbf 1
\]

and hence to

\[
z^\mathsf T\mathbf 1=0
\quad\text{for every }z\in\ker(H_{\mathcal E}^\mathsf T).
\]

Then characterize this left kernel using the full inclusion matrix and the
incidence vectors of the \(p-2\) deleted Steiner systems.  The characterization
must retain the design/disjointness information; a dimension count or the
even order of a regular graph is already known to be vacuous.

## Attack directions

Pursue all of these far enough to reach a proof or a precise failure theorem:

1. **Simplicial/cohomological route.**  Express the edge equations as a
   cochain condition on the Boolean lattice or simplex.  Determine whether
   boundaries of \((t+2)\)- or larger faces force a dual vector \(z\) of odd
   weight after \(p-2\) systems are deleted.
2. **Inclusion-matrix rank route.**  Use exact \(p\)-rank/2-rank facts for
   inclusion matrices, but derive any rank formula you need.  Look for a
   parity obstruction uniform in \(p\) at rung \(t=3\), \(t=4\), or the top
   rung \(t=p-2\).
3. **Local face route.**  Determine exactly when a \((t+2)\)-set, or another
   bounded point set, creates a triangle or a forced odd closed walk in the
   leftover graph.  Translate absence of all such witnesses into a structural
   condition on the deleted systems and try to contradict their design
   equations.
4. **Complement-fold route.**  At the top rung use complement closure and the
   half-sized folded graph.  Seek a signed determinant, Arf invariant,
   Pfaffian, or quadratic-form obstruction stronger than vertex parity.
5. **Positive direction check.**  If the affine system is not universally
   inconsistent, determine whether it supplies an inductive construction or
   a switch operation capable of repairing odd cycles without destroying the
   \(p-2\) systems.

## Mandatory controls and anti-overclaim rules

Any purported universal obstruction must survive known positive examples of
large sets, especially `LS(2,3,9)`, whose last-two residual graph is
bipartite.  Also check small excluded tower primes \(p=5,7,11,13\) only as
controls; finite failure there is not a uniform proof.

Read these repository controls before generalizing:

* `collaboration/eh_residual_odd_cycle/README.md` -- one particular
  15-system partial at `(t,v,p)=(3,20,17)` has an explicit residual triangle,
  but this does not constrain another partial;
* `collaboration/opus5/large_set_completion_colouring/NOTE.md` -- scope and
  retractions for residual-graph claims;
* `collaboration/opus5/projection_rigidity_attack_2026-07-28/STATUS.md` -- the
  graph-free projection identities are vacuous; top-module containment is the
  hard condition.

Do not claim #835 solved unless you have either:

* an explicit valid construction for some admissible \(k>2\), independently
  checkable block by block; or
* a theorem covering every admissible \(k>2\), with all smaller cases and the
  infinite prime family handled rigorously.

A theorem excluding only \(k=16\), a cyclic ansatz, one fixed partial packing,
or one local orbit does not solve #835.

## Deliverables

Create only this new directory:

`collaboration/opus5/conflict_cycle_obstruction_2026-07-29/`

and write:

1. `PROOF.md` -- definitions and every proved lemma/theorem in complete proof
   form.  Explicitly separate equivalences from genuine new obstructions.
2. `IDEAS.md` -- attempted routes, counterexamples, precise failure boundaries,
   and the strongest surviving next conjecture.
3. `STATUS.md` -- first line verdict: solved / not solved.  State exact scope
   relative to unrestricted #835, the first open case \(k=16\), and all
   parameters covered.
4. A standard-library verifier if any finite calculation informs a theorem.
   It must validate its inputs and print explicit pass/fail output.  Computation
   may discover a lemma but must not replace a proof of an infinite claim.

You may read and execute anything in the repository, but do not edit existing
files and do not commit or push.  Work until the best rigorous result and its
failure boundary are explicit.  Cost is not a stopping criterion.  If the
route fails, prove as much of the failure as possible rather than dressing it
up as progress.
