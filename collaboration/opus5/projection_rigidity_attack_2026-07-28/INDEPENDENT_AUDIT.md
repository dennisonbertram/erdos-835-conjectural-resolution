# Independent audit — projection-rigidity attack

Date: 2026-07-29.

## Verdict

The core algebraic equivalences in `PROOF.md` are correct after the scope
corrections recorded below.  They do **not** resolve Erdős--Rosenfeld #835 and
do not exclude the first open case \(k=16\).

The genuinely established boundary is narrow:

* every equal equipartition gives the stated two-valued idempotent and all
  graph-free identities in Theorem A;
* conversely, for \(k=q-1\ge2\), a symmetric two-valued idempotent of the
  stated form forces an equal \(q\)-class partition;
* top-module containment \(AP=-P\) is not automatic and is exactly the hard
  perfect-code condition;
* the single scalar support test \(q^{k-1}_{k-1,k-1}\ne0\) cannot distinguish
  one constituent perfect code from a full partition;
* stronger subspace-orientation, Schur, Terwilliger, semidefinite, and
  equitable-partition constraints remain open.

## Hand audit

1. Theorem A follows from
   \(R^2=(N/q)R\), \(RJ=(N/q)J\), and \(J^2=NJ\).  These identities use only an
   equal partition and contain no Odd-graph adjacency information.
2. Theorem B's diagonal entry of \(P^2=P\) forces each same-relation
   neighbourhood to have size \(N/q\).  The off-diagonal entry forces two such
   neighbourhoods either to coincide or be disjoint.  Symmetry and the
   diagonal relation then give exactly \(q\) equal equivalence classes.
3. Theorem C is the exact calculation
   \(NAP=qAR-kJ\); comparing \(AP=-P\) gives \((A+I)R=J\), and conversely.
   This is not a relaxation: it is the original perfect-code partition
   condition.
4. Proposition F is a valid necessary support condition obtained by expanding
   \(P\circ P\) as a sum of rank-one Schur products.  Theorem G correctly
   shows only that this scalar support condition is nonzero whenever one
   constituent code exists.  It says nothing universal about the orientation
   of a full \(k\)-dimensional simplex subspace inside the top module.
5. Proposition H's quadratic and cubic formulas follow by direct evaluation
   on the \(q\) equal cells.  They are graph-free once the equipartition is
   given; the embedding problem inside \(V_{k-1}\) remains open.

## Executed verifier

Command:

```sh
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3 -B \
  collaboration/opus5/projection_rigidity_attack_2026-07-28/verify_projection_rigidity.py
```

Observed terminal result:

```text
RESULT: 0 failure(s)
```

The run checked the four random equal-partition controls, the exhaustive
\((N,q)=(6,3)\) converse (15 idempotents, exactly the 15 equipartitions), exact
Krein values at \(k=4,6,10,12,16\), all 30 Fano planes and their maximum
pairwise-disjoint subfamily, and a cyclic \(S(4,5,11)\) control.  It does not
test \(AP=-P\) at \(k=16\), a full 17-class partition, or any unrestricted
existence claim.

The verifier docstring originally said that it checked every identity in the
projection package and listed a \(q=2\) exhaustive case that the program does
not run.  It now says exactly what is checked: the graph-free identities and
the \(q=3\) converse.

## Corrections to Opus's original scope

The independent review made these material corrections:

1. Top-module containment was originally described too close to the automatic
   graph-free identities.  It is not automatic; by Theorem C it is exactly the
   hard condition \(AP=-P\), equivalently \((A+I)R=J\).
2. The basic Krein calculation closes only the scalar support test
   \(q^{k-1}_{k-1,k-1}\ne0\).  It does not close the whole Schur, Terwilliger,
   semidefinite, or subspace-orientation route.
3. Theorem G shows that a single constituent code makes the relevant scalar
   Krein parameter positive.  It does not show that one constituent satisfies
   every constraint imposed on a full simplex subspace.
4. Corollary I2 called its family of test vectors a *proper* subset without
   proving strictness.  The proof needs only “subset,” which is now stated.
5. The statement comparing the note with Bailey--Cameron--Zhou was too broad
   while their paper was unavailable.  The paper was retrieved during this
   audit:
   [arXiv:2605.17376](https://arxiv.org/abs/2605.17376).  Its Corollary 2.4(a),
   specialised to an \((a,b)\)-perfect set, contains the quotient-eigenspace
   condition proved in Corollary I1.  Its full Theorem 2.3 and Corollary 2.4(b)
   are expressed through the more general systems (6)--(8).  This audit does
   not identify all of those systems with Lemma I, so they remain an
   untested obstruction route rather than a closed one.

## Exact remaining gap

A solution still needs either an actual
\(LS(15,16,32)\), equivalently \(LS(14,15,31)\), or a theorem excluding every
admissible \(k>2\).  This package supplies neither.  It says where a successful
projection proof must use additional information: the placement of the
two-valued \(0/1\) simplex projector inside the top Johnson eigenspace, not
idempotency or entrywise powers alone.
