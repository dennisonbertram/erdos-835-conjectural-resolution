# Two-edge switching resilience on a twelve-vertex support

Date: 2026-07-27.

## Result and scope

The six-matching resilience lemma in `SEVEN_PACKING_NONZERO_R_NOTE.md`
proves that deleting the union of six matchings from \(K_{12}\) leaves a
perfect matching.  The following strengthens it in the direction needed for
a seven-to-eight switching argument.

> **Two-edge resilience lemma.**  Let \(D\) be the union of six matchings in
> \(K_{12}\), and let \(P\) be any matching with
> \(P\cap D=\varnothing\) and \(|P|\le2\).  Then
> \[
> K_{12}-(D\cup P)
> \]
> has a perfect matching.

In particular, every edge of \(K_{12}-D\) is avoidable by a perfect
matching, and any two disjoint available edges can be avoided
simultaneously.

This is a switching primitive, not yet a theorem coordinating two whole
perfect matchings.  A whole seventh matching can contribute three or more
edges to a critical core, exactly where the argument below becomes sharp.

## Proof

Suppose \(K_{12}-(D\cup P)\) has no perfect matching.  The coarsened Tutte
classification in `EIGHTH_MATCHING_CORE_CATALOGUE.md` says that \(D\cup P\)
must contain one of the following complete multipartite cores:
\[
 K_{5,7},\qquad K_{3,1,1,1,1,1}=K_8-E(K_3),\qquad K_7. \tag{1}
\]
Each case is impossible.

### The \(K_{5,7}\) core

Each of the six matchings in \(D\) contains at most five edges across a
fixed \(5\)-by-\(7\) bipartition.  Thus \(D\) covers at most thirty of the
thirty-five core edges.  The matching \(P\) contributes at most two more,
still fewer than thirty-five.

### The \(K_8-E(K_3)\) core

View this core as \(K_{3,1,1,1,1,1}\).  Each of the five singleton-part
vertices has core degree seven.  Since \(\Delta(D)\le6\), every one of those
five vertices must be incident with an edge of \(P\); otherwise its seven
core edges would all belong to \(D\).  But two matching edges cover at most
four vertices, a contradiction.

### The \(K_7\) core

Each matching contains at most three edges on a fixed seven-vertex set.
The six matchings in \(D\) therefore cover at most eighteen of the
twenty-one edges of \(K_7\), and \(P\) contributes at most two more.

All possible cores have been eliminated, proving the lemma.

## Sharp critical patterns

The proof records the minimum contribution that a further matching must
make before it can obstruct a twelve-vertex support:

\[
\begin{array}{c|c}
\text{core}&\text{edges required from the further matching}\\ \hline
K_{5,7}&\text{at least }5\\
K_8-E(K_3)&\text{at least }3,\text{ incident with all five degree-7 vertices}\\
K_7&\text{at least }3.
\end{array}
\]

Thus any failed attempt to coordinate a seventh matching against a
twelve-support perfect matching contains a critical matching pattern of
size at least three.  A full two-matching switching theorem must hit all
such patterns simultaneously or prove that their overlaps admit a trade.

`verify_twelve_support_switching.py` checks the finite Tutte patterns and
all three lower bounds.
