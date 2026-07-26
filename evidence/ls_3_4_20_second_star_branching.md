# Lossless second-star branches for the unrestricted \(LS(3,4,20)\) CNF

## Status and exact scope

This note gives a **lossless 55-way symmetry decomposition** of the complete
unrestricted \(LS(3,4,20)\) CNF.  It does not assume that a solution has an
automorphism.

No branch has been proved SAT or UNSAT here.  Therefore this is a search
reduction, not a solution of \(LS(3,4,20)\) or Erdős--Rosenfeld #835.

Every \(LS(15,16,32)\) derives to an \(LS(3,4,20)\).  Consequently, checked
UNSAT proofs for **all 55 branches** would exclude the \(k=16\) case of
#835.  A satisfying branch would construct the necessary derived large set
only; it would not by itself construct an \(LS(15,16,32)\).  These branches
say nothing about the later prime cases.

## 1. The residual group after the root-star normalization

The parent CNF fixes the 17 extensions of
\[
 R=\{0,1,2\}
\]
by assigning
\[
 c(R\cup\{q\})=q-3\qquad(3\le q\le19).
\tag{1}
\]
It is convenient to identify colour \(q-3\) with the point \(q\), and to
write \(Q=\{3,\ldots,19\}\).

The geometric point-colour symmetries preserving (1) are exactly
\[
 \operatorname{Sym}(R)\times\operatorname{Sym}(Q),
\tag{2}
\]
where the second factor acts diagonally on the points \(Q\) and their
identified colours.  Indeed, a point permutation preserving \(R\) is an
arbitrary element of
\(\operatorname{Sym}(R)\times\operatorname{Sym}(Q)\), and (1) forces its
colour action on \(Q\) to be the same permutation.  Conversely every such
diagonal action preserves (1) and the \(LS(3,4,20)\) condition.

The Sinz auxiliaries make (2) a semantic symmetry of the primary solution
set rather than necessarily a literal automorphism of the particular
sequential-counter clauses.  This is sufficient: every one-hot primary
colouring has a Sinz extension, before and after the symmetry.

## 2. One second-star row is a derangement

Fix the pair \(\{0,1\}\) and the point \(q_0=3\).  For
\(r\in Q\setminus\{3\}\), define the point-valued colour
\[
 \pi(r)=c(\{0,1,3,r\})+3.
\tag{3}
\]
The 17 blocks extending the triple \(\{0,1,3\}\) are rainbow.  Its extension
by point \(2\) has point-valued colour \(3\) by (1), so (3) is a permutation
of \(Q\setminus\{3\}\).

It has no fixed point.  If \(\pi(r)=r\), then both
\[
 \{0,1,2,r\}\quad\hbox{and}\quad\{0,1,3,r\}
\]
would have colour \(r-3\), contradicting the rainbow star on the common
triple \(\{0,1,r\}\).  Thus \(\pi\) is a derangement of 16 objects.

This is also the first row of the symmetric idempotent Latin square
\[
 L_{01}(q,r)=c(\{0,1,q,r\})+3,\qquad L_{01}(q,q)=q,
\]
forced by the large-set axioms, but the branching proof needs only the two
rainbow-star arguments above.

## 3. Cycle type gives 55 lossless branches

The subgroup of (2) which fixes \(0,1,2,3\) and permutes the other sixteen
points of \(Q\) acts on (3) by conjugation:
\[
 \pi\longmapsto h\pi h^{-1},\qquad
 h\in\operatorname{Sym}(Q\setminus\{3\}).
\tag{4}
\]
Two permutations are conjugate precisely when they have the same cycle
type.  Since \(\pi\) is fixed-point-free, its cycle type is a partition of
16 with every part at least 2.  There are
\[
 p(16)-p(15)=231-176=55
\tag{5}
\]
such partitions.

For each partition \(\lambda\), the generator puts its cycles consecutively
on \(4,5,\ldots,19\), producing a canonical permutation
\(\pi_\lambda\), and appends the sixteen units
\[
 x_{\{0,1,3,r\},\,\pi_\lambda(r)-3}
\qquad(4\le r\le19).
\tag{6}
\]

Now let \(c\) be any model of the normalized parent CNF.  Its row (3) has
some type \(\lambda\).  A relabelling \(h\) in (4) conjugates that row to
\(\pi_\lambda\), while preserving the root normalization and every
\(LS(3,4,20)\) axiom.  Hence the relabelled model satisfies branch
\(\lambda\).  Conversely every branch model is a parent model.  Therefore
\[
 \boxed{
 F\text{ is SAT}\iff\bigvee_{\lambda\vdash16,\;1\notin\lambda}
 (F\wedge\text{units}_\lambda)\text{ is SAT}.}
\tag{7}
\]
In particular, all 55 checked UNSAT proofs are necessary and sufficient for
parent UNSAT.

The cube file contains orbit representatives, not a literal disjoint
partition of all labelled parent models.  Equation (7) is WLOG because of
the proved residual symmetry.

For \(\lambda\) with \(m_j\) parts of size \(j\), its centralizer in
\(\operatorname{Sym}(16)\) has order
\[
 z_\lambda=\prod_j j^{m_j}m_j!,
\tag{8}
\]
and its conjugacy class has \(16!/z_\lambda\) derangements.  The independent
verifier checks the exact exhaustiveness identity
\[
 \sum_{\lambda\vdash16,\;1\notin\lambda}\frac{16!}{z_\lambda}
 = {!16}=7\,697\,064\,251\,745.
\tag{9}
\]
It also exhaustively reconstructs the same classification for every degree
2 through 8 as a finite control.

The geometric symmetries visibly preserving one canonical branch include
the swap \(0\leftrightarrow1\) and the centralizer of
\(\pi_\lambda\), giving branch stabilizer order \(2z_\lambda\).  The
manifest records this for possible further symmetry breaking; no extra
breaker is asserted here.

## 4. Deterministic artifacts and independent verification

Generate the 55 representatives:

```sh
python3 -B evidence/generate_ls_3_4_20_second_star_branches.py \
  --parent-cnf evidence/ls_3_4_20_generic_cnf/instance.cnf \
  --parent-manifest evidence/ls_3_4_20_generic_cnf/manifest.json \
  --manifest evidence/ls_3_4_20_second_star_branches/manifest.json \
  --cubes evidence/ls_3_4_20_second_star_branches/branches.cubes
```

Audit them independently:

```sh
python3 -B evidence/verify_ls_3_4_20_second_star_branches.py \
  --parent-cnf evidence/ls_3_4_20_generic_cnf/instance.cnf \
  --parent-manifest evidence/ls_3_4_20_generic_cnf/manifest.json \
  --manifest evidence/ls_3_4_20_second_star_branches/manifest.json \
  --cubes evidence/ls_3_4_20_second_star_branches/branches.cubes
```

Materialize branch \(i\) on demand:

```sh
python3 -B evidence/materialize_ls_3_4_20_second_star_branch.py \
  --parent-cnf evidence/ls_3_4_20_generic_cnf/instance.cnf \
  --manifest evidence/ls_3_4_20_second_star_branches/manifest.json \
  --branch-id i --output /tmp/ls3420-branch-i.cnf
```

The manifest records the exact SHA-256 of every such plain branch CNF.  The
verifier can authenticate a materialized branch with
`--branch-cnf PATH --branch-id i`.

For stronger propagation, the materializer's optional
`--star-pairwise-amo` switch appends all
\[
 \binom{20}{3}\cdot17\cdot\binom{17}{2}
 =2\,635\,680
\tag{10}
\]
binary clauses saying that a fixed colour occurs at most once in a triple
star.  These clauses are logically implied by the parent encoding: its
seventeen blocks each have exactly one colour, while the seventeen
star-at-least-one clauses require all seventeen colours, so pigeonhole
forces each exactly once.  The verifier independently reconstructs the
complete augmented byte stream when passed `--star-pairwise-amo`.

No solver exit caused by a time limit is evidence of SAT or UNSAT.  Only a
model checked as an \(LS(3,4,20)\), or a proof checked against the exact
authenticated branch CNF, can settle a branch.

## 5. Bounded encoding probe

On 2026-07-26, branch 54 (cycle type \(16\)) was materialized and
independently authenticated in both forms:

| encoding | clauses | bytes | SHA-256 |
|---|---:|---:|---|
| plain branch | 251,973 | 6,168,479 | `851f56c6852d8c2c9774dd6414120d70e26f313a275674519f50c8efd77f03d2` |
| with implied star AMO | 2,887,653 | 47,628,576 | `fa5e0ef484abd2262517a60c36bf42f399ed264068d9b83e8e6bc7a88c23eef8` |

CaDiCaL 3.0.1 returned `UNKNOWN` after a 10-second wall-clock limit on
each.  These runs establish only that both authenticated encodings parse
and enter search successfully.  They provide no evidence that the branch is
SAT or UNSAT.  The machine-readable record is
`evidence/ls_3_4_20_second_star_branches/probe_2026-07-26.json`.
