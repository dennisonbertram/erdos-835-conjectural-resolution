# Opus 5 max-effort task: apply Bailey--Cameron--Zhou to the Odd graph

Work in `/Users/dennison/Documents/Math Problem`.

## Objective

Try to resolve Erdős--Rosenfeld Problem #835 by applying the **full** two
equitable-partition theorem of Bailey--Cameron--Zhou, not just the elementary
cell-indicator spectral corollary already audited in the repository.

Primary source:

* R. A. Bailey, Peter J. Cameron, Sanming Zhou,
  "Equitable partitions of regular graphs, and perfect sets in normal Cayley
  graphs," arXiv:2605.17376, especially Theorem 2.3 and Corollary 2.4:
  https://arxiv.org/abs/2605.17376

Repository context:

* `collaboration/opus5/projection_rigidity_attack_2026-07-28/PROOF.md`
* `collaboration/opus5/projection_rigidity_attack_2026-07-28/STATUS.md`
* `collaboration/opus5/projection_rigidity_attack_2026-07-28/INDEPENDENT_AUDIT.md`
* `erdos_835_conjectural_resolution.md`

The independent audit corrected an overclosure: Corollary I1/I2 handles the
simple quotient-eigenspace condition visible in BCZ Corollary 2.4(a), but it
did not verify that all of Theorem 2.3 and Corollary 2.4(b), systems (6)--(8)
and (13), reduce to the same design-quadrature identity.

## Exact setting

Let \(\Gamma=O_k=KG(2k-1,k-1)\), degree \(k\), with \(q=k+1\).  A solution of
#835 gives an equitable partition
\(\tau=\{C_1,\ldots,C_q\}\) into perfect codes, with quotient matrix
\[
M_\tau=J_q-I_q.
\]
Each centered indicator
\(\mathbf1_{C_a}-q^{-1}\mathbf1\) lies in the \(-1\) eigenspace, the top
Johnson module.  The graph-free projector identities alone are known to be
vacuous.

Apply BCZ Theorem 2.3 in both orders:

1. \(\tau\) is the colour partition and \(\pi\) is a strategically chosen
   equitable partition of \(O_k\);
2. \(\pi\) and \(\tau\) are swapped, including every condition from
   Corollary 2.4(b).

Natural \(\pi\)'s to test include:

* distance partitions about a vertex or a completely regular subset;
* stabilizer-orbit partitions of \(O_k\) associated with a point, pair,
  \(s\)-set, complementary-pair structure, or a constituent Steiner block;
* partitions coming from Johnson-scheme relations or subgroup orbits;
* pairs of different such partitions, so that Theorem 2.3 sees their complete
  intersection-density matrix rather than one cell at a time.

## Required mathematical work

1. Specialize systems (6)--(8) and (13) symbolically when
   \(M_\tau=J_q-I_q\).  Determine the full solution spaces, not just one
   solution.
2. Decide rigorously whether every resulting condition follows from
   \(\mathbf1_{C_a}\in V_0\oplus V_{k-1}\) and the Steiner design equations.
   If yes, prove a route-closure theorem covering the **full** BCZ theorem in
   this setting.
3. If not, identify the first genuinely new constraint and evaluate it for a
   useful family of equitable partitions uniformly in \(k\).
4. Push any new constraint to a contradiction for every admissible
   \(k>2\), or to an explicit construction.  A contradiction only for
   \(k=16\) is useful but is not a full solution.
5. Check small controls \(k=2,4,6\).  In particular, do not infer existence
   from feasibility and do not infer a uniform theorem from the known
   nonexistence of the \(k=4,6\) large sets.

## Anti-overclaim rule

Do not claim #835 solved without an explicit construction for an admissible
\(k>2\) or a nonexistence theorem covering every admissible \(k>2\).  Clearly
separate:

* a restatement of design quadrature;
* a necessary but feasible constraint;
* an obstruction for one equitable partition or one \(k\);
* a uniform obstruction.

## Deliverables

Create only:

`collaboration/opus5/bcz_odd_graph_attack_2026-07-29/`

with:

* `PROOF.md` -- complete symbolic specialization and every proved theorem;
* `IDEAS.md` -- routes attempted, exact failure boundaries, and next live idea;
* `STATUS.md` -- first-line solved/not-solved verdict and exact scope;
* a standard-library exact verifier if finite computations are used.

Do not edit existing files, commit, or push.  Work at max effort.  Cost is not
a stopping criterion.
