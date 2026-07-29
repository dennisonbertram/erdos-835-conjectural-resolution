# Opus 5 max-effort attack: the common odd-transversal bottleneck in Erdős--Rosenfeld #835

Work in `/Users/dennison/Documents/Math Problem`.

Use `/efficient-frontier` first. Reserve Opus reasoning for the decisive
unrestricted theorem; certificate generation for the local orbit campaign is
already running elsewhere.

## Objective and honesty boundary

Resolve Erdős--Rosenfeld Problem #835:

\[
\chi(J(2k,k))=k+1
\]

for some admissible \(k>2\), equivalently existence of
\(LS(k-1,k,2k)\), or prove that this never happens. The first unresolved
case is \(k=16\), but a negative solution must cover the full infinite
admissible family.

Do not count an equivalence, a fixed partial, a restricted ansatz, or closure
of the local orbit campaign as a solution.

## New exact frontier

Read and audit these first:

* `collaboration/independent/conflict_cohomology_2026-07-29/PROOF.md`
* `collaboration/independent/conflict_cohomology_2026-07-29/STATUS.md`
* `collaboration/opus5/full_problem_resume_2026-07-28/STATUS.md`
* `collaboration/opus5/full_problem_resume_2026-07-28/FIXED_RUNG_EXISTENCE.md`
* `collaboration/opus5/post_r0_global_bridge/INDEPENDENT_AUDIT.md`
* `erdos_835_conjectural_resolution.md`

At the top rung let \(k=p-1\) be even and suppose
\({\cal D}_1,\dots,{\cal D}_{k-1}\) are pairwise disjoint
\(S(k-1,k,2k)\)'s. Each system is complement-closed. After complementing
blocks, the systems define \(k-1\) partitions of

\[
V=\binom{X}{k-1}
\]

into Catalan-many cells of size \(k\), with cells from distinct partitions
meeting in at most one point.

Let \(Q\) be their point-versus-cell incidence matrix over \(\mathbf F_2\).
The last two systems exist exactly when

\[
Q^{\mathsf T}a=\mathbf 1
\]

is soluble: a common binary point set meeting every cell of every partition
oddly. Failure is exactly an odd vector in \(\ker Q\), equivalently an odd
binary \((k-1)\)-trade supported on the \(k-1\) systems.

Immediate row/column parity, Catalan parity, individual star, rank, and
system-difference vectors are already proved vacuous. Do not rediscover those
as the answer.

## Assignment

1. Recheck the exact equivalence. If it has a flaw, identify it precisely.
2. Decide the following strongest possible theorem or refute it with a
   rigorous countermodel:

   > Every \(k-1\) pairwise disjoint, complement-closed
   > \(S(k-1,k,2k)\)'s possess a common odd transversal.

   A proof would show every such partial top large set extends by two systems.
   A disproof should identify an invariant forcing an odd trade in every
   admissible family if possible; an arbitrary abstract partition
   counterexample is only a diagnostic because it may violate Steiner and
   complement geometry.
3. Exploit the structure discarded by the abstract hypergraph:
   complements, the Johnson association scheme, intersection numbers,
   quadratic refinements of the simplex boundary form, Pfaffian/Arf
   invariants, or coupling to the adjacent rung. Derive every claimed
   identity.
4. Test proposed universal claims against the positive `LS(2,3,9)` control,
   the authenticated negative EH fixed partial, and any actual small top-rung
   examples available in the repository.
5. If the theorem remains open, prove the strongest exact failure theorem and
   reduce the next step to one concrete lemma that is strictly stronger than
   the current equivalence.

## Deliverables

Create only:

`collaboration/opus5/common_odd_transversal_2026-07-29/`

containing:

* `STATUS.md` — first line `SOLVED` or `NOT SOLVED`, with exact scope;
* `PROOF.md` — complete proofs of unconditional results only;
* `IDEAS.md` — rejected routes, countermodels, and the single best remaining
  lemma;
* a standard-library verifier for any finite claim.

Do not edit existing files, commit, or push. Cost is not a stopping
criterion. A claim of resolution requires either a fully checkable
construction or an unrestricted theorem with every admissible parameter
covered.
