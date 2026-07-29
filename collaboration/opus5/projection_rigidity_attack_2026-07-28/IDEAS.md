# IDEAS — unproved ideas and exact failure boundaries

Companion to `PROOF.md` (proved statements only) and `STATUS.md` (verdict).
Everything here is either **unproved**, **already committed elsewhere in the
repository**, or a **recorded dead end**.  Labels are explicit.

## 1. Mod-\(p\) reduction of the two-valued projection — DERIVED, but already committed

**Derived (proof is complete and short).**  Put \(p=q=k+1\) and work over
\(\mathbb F_p\).  The \(q\) indicators \(\mathbf 1_{C_a}\) are independent over
any field (disjoint nonempty supports), so they span a \(p\)-dimensional space
\(S\).  On \(S\), \((A+I)\mathbf 1_{C_a}=\mathbf 1\) for every \(a\), so
\((A+I)S=\langle\mathbf 1\rangle\) has dimension 1.  Hence

\[
 \dim_{\mathbb F_p}\ker(A+I)\ \ge\ p-1=k,
 \qquad\text{i.e.}\qquad
 \operatorname{rank}_{\mathbb F_p}(A+I)\le N-k .
\]

**Failure boundary.**  This is the same layer as the committed critical-group
audit: \(O_k\) is \(k\)-regular, so its Laplacian is \(L=kI-A\equiv-(A+I)
\pmod p\), and the \(p\)-primary part of \(\operatorname{Jac}(O_k)\) is governed
by \(\operatorname{rank}_{\mathbb F_p}(A+I)\).
`evidence/critical_group_cover_audit.md` records that this test **passes the
known-false \(k=4\) control and gives no obstruction at \(k=16\)**.  I did not
check whether the bound above is off by one from the committed
\((\mathbb Z/p)^{p-2}\) statement; even if it is sharper by one dimension, the
committed audit's conclusion (non-obstructive at \(k=16\)) is about the same
invariant, so this is not a new route.

## 2. Integral short-vector formulation — DERIVED, already committed

**Derived.**  \(q y_a=q\mathbf 1_{C_a}-\mathbf 1\in\mathbb Z^N\), and
\(\langle qy_a,qy_b\rangle=qN\delta_{ab}-N\).  So a partition forces \(q\)
vectors of squared norm \(Nk\), pairwise inner product \(-N\), summing to zero,
inside the integral lattice \(\Lambda=\mathbb Z^N\cap V_{k-1}
=\ker_{\mathbb Z}(A+I)\).  Equivalently, \(\sqrt N\) times a fixed rank-\(k\)
lattice must embed isometrically in \(\Lambda\).

**Failure boundary.**  This is exactly `evidence/full_eigenlattice_audit.md`,
which reports that the local invariants (Jordan ranks, the \(p=k+1\)
discriminant component, 2-adic Witt type, primitivity, fibre-sum map) are all
compatible at \(k=16\), while a 3-adic unit-rank obstruction and an exhaustive
short-vector search do reject \(k=4\).  Nothing in the projection formulation
adds to that; by Theorem C1 it cannot.

## 3. Semidefinite / theta-body relaxation — OPEN, not attempted

**Idea.**  Theorem B says two-valuedness plus idempotency already forces
integrality, so the only remaining relaxation is to drop the two values and
optimise over projectors with entries in an interval.

**Current boundary.**  The natural graph relaxations are calibrated to
the chromatic number, and for Kneser graphs
\(\chi_f\bigl(KG(2k-1,k-1)\bigr)=\frac{2k-1}{k-1}<3\), while the target is a
covering onto \(K_{k+1}\).  Any Lovász-theta-type bound therefore has a gap of
roughly \(k-1\) and is unlikely to see the covering obstruction by itself.  A
covering-specific SDP would need to encode more of \((A+I)R=J\).  Theorem C1
does not prove that such an SDP is powerless: a hierarchy could still refute
the exact \(0/1\) system.  This branch was not attempted here.

## 4. Absolute-bound / rank version of the Schur identity — DEAD END, quantified

**Idea.**  \(P\circ P=\sum_{i,j}(w_i\circ w_j)(w_i\circ w_j)^{\mathsf T}\) gives
\(\operatorname{rank}(P\circ P)\le\binom{k+1}{2}\), the absolute-bound style
inequality.

**Exact failure boundary.**  \(\operatorname{rank}(P\circ P)=k+1\) by Theorem
A(6), and \(k+1\le\binom{k+1}2\) for all \(k\ge2\) with slack growing
quadratically.  No value of \(k\) is constrained.

## 5. Integral cubic-form rigidity — OPEN as a stronger relaxation

**Idea.**  Proposition H says the ambient invariant cubic \(\tau\) restricts to
\(W\) as \(\frac Nq\sum_at_a^3\).  \(\tau\) is integer-valued on \(\mathbb Z^N\),
so one might hope for an integrality obstruction to embedding the \(A_{q-1}\)
cubic-plus-quadratic structure into \((\Lambda,\tau)\).

**Current boundary.**  Theorem B shows that a two-valued idempotent already
*is* an equipartition, but this does not make necessary lattice or cubic-form
conditions useless: a non-embedding theorem could still exclude such a
partition once \(W\subseteq V_{k-1}\) is imposed.  A useful relaxation would
ask whether the required \(A_{q-1}\) quadratic-plus-cubic form embeds in the
top eigenlattice without assuming the full two-valued matrix.  Failure of that
relaxation would obstruct a colouring; success would not construct one.  This
stronger embedding problem remains open here.

## 6. Where the remaining information provably lives — OPEN

By Theorem C1, every symmetric function of the colour-class indicators is
determined.  The first quantities that are *not* determined involve the graph
and at least two classes asymmetrically:

* the \(\binom{q}{2}\) perfect matchings \(M_{ab}=E(O_k)\cap(C_a\times C_b)\)
  and their union's cycle structure (the covering's holonomy);
* the intersection pattern of the \(q\) Steiner systems with substructures of
  \(O_k\), including equitable partitions beyond the cell-indicator spectral
  specialisation closed by Corollary I2.

**Status of the first bullet:** committed as closed —
`collaboration/opus5/holonomy_followup` records that the holonomy census is
vacuous because the tower identity and all representation projections hold for
arbitrary bijection families.
**Status of the second bullet:** open.  The cubic/eigenlattice embedding and
covering-specific SDP/Terwilliger branches above also remain open.

## 7. Symmetry ansätze — NOT A GENERAL THEOREM

If a hypothetical colouring had automorphism group \(G\), then \(W\) would be a
\(k\)-dimensional \(G\)-submodule of \(V_{k-1}|_G\) isomorphic to the
augmentation submodule of the permutation module on the \(q\) colours.  This is
a real constraint and is how the committed cyclic-17 star theorem
(`evidence/cyclic17_star_centre0_infeasibility.md`) operates.

**Failure boundary.**  It is an ansatz.  A hypothetical \(LS(14,15,31)\) need
have no nontrivial automorphism, so no argument of this shape can settle #835.

## 8. Things I checked and found to be non-facts

* **"\(q^{d}_{dd}=0\) for \(J(2d+1,d)\)".**  This would have proved #835
  negatively for all even \(k>2\) via Proposition F.  It is **false**: for
  \(J(7,3)\), taking \(y=\mathbf 1_C-\frac15\mathbf 1\) for a Fano plane \(C\)
  gives \(\tau(y,y,y)=7\cdot(4/5)^3+28\cdot(-1/5)^3=420/125\ne0\).  The general
  refutation is Theorem G.  Recorded because the "\(i+j+l\le n\) vanishing
  rule" for Johnson Krein parameters is a plausible-looking but wrong
  recollection, and it is worth not re-deriving it.
* **"The equivalence-class count is an extra hypothesis."**  It is not
  (Theorem B).

## 9. Independent follow-up

* Opus could not retrieve arXiv:2605.17376 (Bailey–Cameron–Zhou).  The
  independent audit later retrieved it.  Corollary I2 covers the
  cell-indicator quotient-eigenspace specialisation visible in Corollary
  2.4(a), not the paper's full Theorem 2.3/Corollary 2.4(b) systems.  Those
  fuller systems remain an open route to test on the Odd graph.
* Opus did not execute `verify_projection_rigidity.py`.  The independent audit
  subsequently ran it and obtained `RESULT: 0 failure(s)`.  No proof in
  `PROOF.md` depends on it.
