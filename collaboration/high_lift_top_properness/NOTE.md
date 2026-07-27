# High-lift top-properness

Date: 2026-07-27.

## Scope

This note studies whether the locally forced constructions at
\(j=10,11,12\) automatically satisfy top-properness at the next level.
The setting and notation are those of the unrestricted lift tower, with
\[
 |U|=19,\qquad |A|=13,\qquad |{\cal C}|=17.
\]

The result below proves the implication at \(j=12\).  It is conditional on
the level-\(12\) tower laws and level-\(12\) top-properness already holding.
It does not construct lower levels or solve Erdős--Rosenfeld Problem #835.

## 1. The final \(j=12\) implication is automatic

At level \(12\), fix \(R\in\binom U{16}\).  For
\(B\in\binom A{12}\), the tower law is
\[
 \{G_B(R\setminus\{x\}):x\in R\}
 \mathbin{\dot\cup}
 \{G_A(R)\}
 ={\cal C}.
\tag{1}
\]
Level-\(12\) top-properness says that the first sixteen values are
distinct.  Thus \(G_A(R)\) is their unique missing colour.  The
fixed-\(R\) complement theorem independently shows that the same missing
colour works for all thirteen choices of \(B\), but that fact is not needed
in the argument once the tower law (1) is assumed.

> **Theorem 1 (automatic final top-properness).**  Suppose the maps
> \(G_B:\binom U{15}\to{\cal C}\), \(B\in\binom A{12}\), are
> top-proper at level \(12\), and suppose values
> \(G_A(R)\), \(R\in\binom U{16}\), satisfy every level-\(12\) tower
> law (1).  Then \(G_A\) is automatically top-proper:
> \[
> \bigl(G_A(P\setminus\{x\})\bigr)_{x\in P}
> \text{ are pairwise distinct}
> \qquad(P\in\binom U{17}).
> \tag{2}
> \]

### Proof

Fix \(P\in\binom U{17}\) and any \(B\in\binom A{12}\).  Colour the edges
of a complete graph on vertex set \(P\) by
\[
 \phi(\{x,y\})=G_B(P\setminus\{x,y\}).
\tag{3}
\]
At vertex \(x\), these are the sixteen values
\[
 G_B((P\setminus\{x\})\setminus\{y\}),
 \qquad y\in P\setminus\{x\}.
\]
They are distinct by level-\(12\) top-properness on the sixteen-set
\(P\setminus\{x\}\).  Hence \(\phi\) is a proper \(17\)-edge-colouring
of \(K_{17}\).

The tower law (1) on \(R=P\setminus\{x\}\) says that
\[
 m(x):=G_A(P\setminus\{x\})
\tag{4}
\]
is the unique colour missing at vertex \(x\) in \(\phi\).

For a colour \(\gamma\), its edge class is a matching \(M_\gamma\).
Consequently the number of vertices missing \(\gamma\) is
\[
 17-2|M_\gamma|,
\tag{5}
\]
which is a positive odd integer.  On the other hand, every vertex misses
exactly one of the seventeen colours, so the total number of
vertex--missing-colour incidences is \(17\).  There are seventeen colours,
and each contributes at least one incidence by (5); therefore each
contributes exactly one.  The missing colours \(m(x)\), \(x\in P\), are
pairwise distinct, proving (2). \(\square\)

The parity of the odd complete graph is essential to this short proof.
It is stronger than simply observing that every \(G_A(R)\) is locally
forced: it couples the seventeen overlapping sixteen-sets inside \(P\).

## 2. Remaining levels

The analogous \(j=11\) and \(j=10\) implications require more structure.
Their exact defect-array formulations and any countercontrols are developed
below as they are established; no automatic implication is asserted here.

## Verification

Run:

```sh
python3 -B \
  collaboration/high_lift_top_properness/verify_j12_top_properness.py
```

The standard-library checker constructs the cyclic proper
\(17\)-edge-colouring of \(K_{17}\), identifies its unique missing colour
at each vertex, and checks the matching-incidence count used in the proof.
It is a sanity control, not the basis of Theorem 1.
