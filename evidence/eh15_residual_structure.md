# Exact residual structure of the Etzion--Hartman 15-core

This note concerns only the reconstructed Etzion--Hartman family of fifteen
pairwise disjoint SQS(20)s.  It is **not** a universal obstruction to
`LS(3,4,20)`.

The independently checked construction in
`generate_eh_15_seed.py` uses 4,275 of the 4,845 quadruples.  Join two of the
570 unused quadruples when they contain the two unused extensions of the
same triple.  The resulting 4-regular residual graph has the exact component
decomposition

\[
 B_{250}\;\mathbin{\dot\cup}\;
 12(C_5\square C_5)\;\mathbin{\dot\cup}\;4K_5,
\]

where \(B_{250}\) is bipartite.  The script constructs the graph directly
from the fifteen block lists, checks every degree, and checks the twelve
25-vertex components against the Cartesian product of two 5-cycles.

Consequences:

1. The core cannot be extended by two SQSs, because its residual graph is
   not bipartite.
2. Its best residual two-colouring has exactly 136 monochromatic edges.
   A \(K_5\) contributes at least
   \(\binom2 2+\binom3 2=4\).  In \(C_5\square C_5\), its five disjoint row
   5-cycles and five disjoint column 5-cycles use disjoint edge sets, so
   every cut leaves at least ten monochromatic edges; the usual alternating
   toroidal pattern attains ten.  Thus the total is
   \(4\cdot4+12\cdot10=136\).
3. A maximum induced bipartite subgraph of the residual leaves exactly 72
   vertices out.  Each \(K_5\) requires deletion of three vertices.  The
   five disjoint row 5-cycles in \(C_5\square C_5\) require at least five
   deleted vertices, and a diagonal choice of five vertices attains this.
   Thus the total is \(4\cdot3+12\cdot5=72\).

The balanced 136-conflict seed and the 72-hole proper partial seed are both
generated and checked by `generate_eh_15_seed.py`.  Search failure from
either seed says nothing about other 15-cores or about the existence of a
large set.
