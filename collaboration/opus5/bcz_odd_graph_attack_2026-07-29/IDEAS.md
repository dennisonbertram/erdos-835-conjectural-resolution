# IDEAS — routes attempted, exact failure boundaries, next live idea

Companion to `PROOF.md` (proved statements only) and `STATUS.md` (verdict).
Date 2026-07-29.  Nothing here is claimed as proved unless it points at a
numbered theorem in `PROOF.md`.

---

## 0. Session constraints that shaped the work

* **The Opus author could not retrieve arXiv:2605.17376.**  The later
  independent audit retrieved the primary source and checked Theorem 2.3,
  Corollary 2.4, and systems (6)--(8), (13); see `INDEPENDENT_AUDIT.md`.
* **No Python interpreter was permitted.**  Every number in `PROOF.md` was
  hand-computed, and each table was produced twice by two independent routes
  (Möbius inversion of the design equations, and the closed form of Theorem 8).
  The independent audit later ran `verify_bcz_odd_graph.py`: 0 failures.
* The Opus derivation reconstructs the projection/intertwining system from
  scratch.  The audit confirms that the concrete BCZ systems specialize to
  this data, but retracts the broader claim that every theorem expressible
  through \((B_\pi,B_\tau,S)\) has thereby been classified.

---

## 1. Route attempted: the two-equitable-partition system, in both orders

**What was done.**  Proved the intertwining identity \(B_\pi^{\mathsf T}S=SB_\tau\)
(Theorem 1), proved that the swap \(\pi\leftrightarrow\tau\) is the same
constraint (Theorem 2), specialized to \(B_\tau=J_q-I_q\) to get
\((B_\pi+I)T=J\) with the complete solution space
\(T=\frac1qJ+Z\), columns of \(Z\) in \(\ker(B_\pi+I)\), \(Z\mathbf1_q=0\),
dimension \(\varepsilon_\pi(q-1)\) (Theorem 3), and added the second-order
Gram/rank conditions (§10).

**Exact failure boundary.**  Theorem 4.  The system is not a relaxation of #835
and not a strengthening of it: taking \(\pi\) to be the partition into
singletons (which *is* equitable, with quotient matrix \(A\)) turns the system
into \((A+I)X_\tau=J\), literally the perfect-code condition.  For any single
\(\pi\) the linear system is the orthogonal projection of design quadrature
onto \(U_\pi\), hence discards real-linear directions whenever
\(U_\pi\ne\mathbb R^X\).  This does not by itself prove strict weakening on the
zero-one partition domain.  Families of
\(\pi\)'s give the projection onto \(\sum_tU_{\pi^{(t)}}\); joins give
intersections, i.e. even less.

**Exact delimiter, not a route impossibility.**  Theorem 5: the projected
linear equations are columnwise apart from the zero-one partition identity.
They introduce no explicit cross-colour transport variable.  But that
partition identity is itself a global disjointness condition, and the
singleton auxiliary partition recovers the whole problem.  Thus the package
does not prove that equitable-partition methods cannot work; it proves the
precise projection form of their linear constraints and closes the tested
stabilizer/distance families below.

---

## 2. Route attempted: \(s\)-set stabilizer orbit partitions (\(\varepsilon=0\))

**Idea.**  If \(-1\notin\operatorname{spec}B_\pi\) the deviation vanishes and one
gets \(|P_i\cap C_a|=|P_i|/q\), so \(q\) must divide every cell size.  Find one
cell size not divisible by \(q\) and the problem is solved.

**Result: closed, uniformly in \(k\), twice.**

* Theorem 7 (elementary, Kummer): for \(0\le j\le m\le k-2\),
  \(q\mid\binom{2k-1-m}{k-1-j}\), because \(k-1-j\) and \(k-m+j\) are both
  nonzero base-\(q\) digits summing to \(\ge q\).  So every stabilizer-orbit
  cell size is divisible by \(q\), for every admissible \(k\).
* Theorem 6 (via Wilson's diagonal form): **every** subset \(P\subseteq X\) with
  \(\mathbf1_P\perp V_{k-1}\) has \(q\mid|P|\), unconditionally, with no
  hypothesis about codes at all.  Corollary 6.1: the divisibility test can never
  fire for **any** equitable partition with \(\varepsilon_\pi=0\).

**Exact boundary.**  \(m\le k-2\) gives \(\varepsilon=0\); \(m=k-1\) gives
\(\varepsilon=1\) and the singleton cell \(|P_{k-1}|=1\), which is not divisible
by \(q\) — exactly where the test stops applying.  Nothing is lost there,
because that case is the distance partition and is handled in §3.

---

## 3. Route attempted: distance partitions and completely regular sets
## (\(\varepsilon=1\))

**Idea.**  With \(\varepsilon_\pi=1\) the deviation table is rank one, and the
singleton cell \(\{M\}\) pins the single free scalar.  Everything is forced;
maybe the forced numbers are not integers, or are negative.

**Result: closed, uniformly in \(k\).**  Theorem 8 gives the exact closed form
\[
 |P_j\cap C_a|=\frac{|P_j|}q+(-1)^{k-1-j}\binom{k-1}j\Bigl([M\in C_a]-\frac1q\Bigr),
 \qquad |P_j|=\binom{k-1}j\binom k{k-1-j},
\]
and Theorem 8.1 proves these are nonnegative integers for every even \(k\) with
\(q=k+1\) prime, using \(\binom{q-1}{s}\equiv(-1)^s\pmod q\).  So the family is
feasible at every admissible \(k\), including \(k=16\).

**Exact boundary.**  Corollary 4.2 explains why: for a single \(M\) the
condition is literally \((E_iy_a)_M=0\) for \(1\le i\le k-2\), i.e. design
quadrature read off at one vertex.  Ranging over all \(M\in X\) recovers design
quadrature exactly — so the natural family is already saturated and gives back
the problem, not a lever on it.

**What this also kills.**  Theorem 8 is the classical statement that a perfect
code in a distance-regular graph is completely regular.  Any "distance partition
about a completely regular subset" variant is the same statement one level up
and is still single-class by Theorem 5.

---

## 4. Route attempted: pairs of auxiliary partitions, joins, and the
## "complete intersection-density matrix"

**Idea (from the task).**  Feed the theorem two different \(\pi\)'s so that it
sees a whole intersection-density matrix rather than one cell at a time.

**Result: no gain, proved.**  Theorem 4(3).  The conjunction of the pairwise
systems for \((\pi^{(1)},\tau),\dots,(\pi^{(s)},\tau)\) is the single condition
(4.1) for \(U=\sum_tU_{\pi^{(t)}}\), which is \(A\)-invariant, i.e. it is again
one instance of the same theorem.  The pairwise system for
\((\pi^{(t)},\pi^{(s)})\) contains no \(C_a\) at all.  Joins are worse:
\(U_{\pi\vee\rho}=U_\pi\cap U_\rho\) (Lemma 1.4), so the join's condition is a
subfamily of each factor's.

**Boundary.**  The one lattice operation that would help is the **meet**
\(\pi\wedge\tau\) — but the meet of two equitable partitions is in general not
equitable, and here it demonstrably is not: for \(u\in P_i\cap C_a\), the number
of neighbours in \(P_{j'}\cap C_{a'}\) is \([\sigma_{a'}(u)\in P_{j'}\,]\), which
is exactly the non-constant quantity §11 of `PROOF.md` measures.  That is where
the route stops and the next one starts.

---

## 5. Route attempted (partially): second-order / semidefinite conditions

**Idea.**  \(G_\pi=Y^{\mathsf T}\Pi_{U_\pi}Y\) is a \(q\times q\) Gram matrix with
\(0\preceq G_\pi\preceq\frac Nq(I_q-\frac1qJ_q)\) and rank \(\le\varepsilon_\pi\);
maybe a clever \(\pi\), or a family of mutually orthogonal \(\pi\)'s, overfills
the budget.

**Result: closed, but cheaply.**  Propositions 10.1--10.2 and Corollary 10.3:
both the sandwich and the rank bound follow from \(y_a\in V_{k-1}\) plus
\(Y^{\mathsf T}Y=\frac Nq(I_q-\frac1qJ_q)\), so Theorem 4 applies to them
verbatim.  Summing over \(\pi\)'s whose top-module pieces are orthogonal gives
\(\sum G_\pi\preceq Y^{\mathsf T}Y\) with equality once the pieces exhaust
\(V_{k-1}\) — an identity, not a constraint.

**Boundary.**  A genuinely new semidefinite condition would need a matrix built
from *two* colour classes.  Not attempted here beyond §6 below.

---

## 6. Scalar transport closed; next live idea

**Condition (11.2) of `PROOF.md` is now closed uniformly in \(k\).**

Setup: \(\sigma_{a'}:C_a\to C_{a'}\) sends each block to its unique disjoint
partner of colour \(a'\).  Fixing a vertex \(M\) and writing
\(\alpha_j(a)=|\{S\in C_a:|S\cap M|=j\}|\) (known exactly, Theorem 8), the
number
\[
 x_i^{a,a'}=\#\{u\in P_i\cap C_a:\sigma_{a'}(u)\in P_{k-2-i}\}
\]
is **forced**:
\(x_i^{a,a'}=\sum_{t\le i}[\alpha_t(a)-\alpha_{k-1-t}(a')]\), and it must satisfy
\(0\le x_i^{a,a'}\le\alpha_i(a)\).

Why it was worth checking:

* It is genuinely two-colour, so it is outside the closure of Theorem 5 — the
  first such condition this file produces.
* It is completely explicit: closed form (11.3) in binomials, no search.
* Both bounds are *tight somewhere* at every \(k\) tested (\(x_0=\alpha_0\) and
  \(x_1=\alpha_1\) occur), so the inequality is not slack by construction.
* A single violation would have ruled out that \(k\).

The independent verifier found no violation for all 45 admissible
\(k\le200\).  More importantly, Theorem 11.4 now proves feasibility for every
admissible \(k\) by telescoping the binomial sum and writing the three upper
slacks explicitly.  Thus this scalar transport condition is no longer a live
obstruction.

**Next live idea.**  Replace the
distance partition \(\pi_M\) by any equitable \(\pi\): Lemma 11.1 becomes "the
neighbours of \(u\in P_i\) are distributed over cells according to row \(i\) of
\(B_\pi\)", and the transport identity becomes a **transportation-polytope
feasibility problem**: find nonnegative integers \(x_{i\to j}^{a,a'}\) with row
sums \(\alpha_i(a)\), column sums \(\alpha_j(a')\), and \(x_{i\to j}=0\) unless
\((B_\pi)_{ij}>0\).  By Gale--Hoffman this is feasible iff a family of cut
inequalities holds; those cut inequalities add explicit two-colour transport
data absent from the projected linear equations.  Choosing \(\pi\) to make the support
of \(B_\pi\) sparse (distance partitions are the extreme case: bandwidth 2) makes
the cuts strongest.  The next executable problem is to identify a uniform
family whose Gale--Hoffman cuts do not collapse to the three scalar slack
formulas of Theorem 11.4.

---

## 7. Routes considered and rejected before spending effort

* **Normal Cayley graph specialization.**  I do not know whether \(O_k\) is a
  Cayley graph, and \(O_3\) (Petersen) classically is not one.  Without the
  paper I could not check whether their normal-Cayley hypotheses apply.  Nothing
  in `PROOF.md` uses any Cayley structure; if \(O_k\) is not a normal Cayley
  graph this branch is vacuous anyway.
* **Making \(\tau\) the auxiliary partition and some \(\pi\) the "perfect set".**
  Theorem 2 shows the swap is the transpose of the same identity.  There is no
  second theorem hiding in the other order.
* **Orbit partitions of large sporadic subgroups (\(M_{11}\), \(\mathrm{PSL}\),
  Frobenius groups).**  These give specific \(\varepsilon_\pi\) values but are
  still single-class by Theorem 5, and by Corollary 6.1 the \(\varepsilon=0\)
  ones are automatically consistent.  Without Python I could not enumerate them,
  and Theorem 6 makes the enumeration pointless for the divisibility test.
* **Krein / Terwilliger sharpening.**  Already audited in
  `projection_rigidity_attack_2026-07-28`; the scalar test is proved blind
  there, and the present Theorem 5 explains structurally why: everything derived
  from \(\Pi_{U_\pi}\) is single-class.

---

## 8. Honest assessment

The exact BCZ systems specialize to the projection identities in this package.
Ranging over all auxiliary partitions recovers design quadrature because the
singleton partition is the original equation; this is an equivalence, not a
vacuity theorem.  The two natural families tested here — \(s\)-set stabilizer
orbits and distance partitions — are non-obstructive uniformly in \(k\).

The payoff is the diagnosis, not a solution: simple divisibility,
distance-distribution, Gram, and scalar two-colour transport constraints all
close uniformly.  The live frontier is a genuinely higher-dimensional
transportation cut, a strategically chosen auxiliary partition whose
zero-one domain adds force, or higher-order colour coupling.
