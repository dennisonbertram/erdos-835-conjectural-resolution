# The residual-degree invariant does not propagate arbitrary prefixes

Date: 2026-07-27.

## Result and scope

For a packing prefix with residual graph \(H\) and remaining supports
\(V_1,\ldots,V_m\), one always has the exact degree identity
\[
 d_H(v)=|\{i:v\in V_i\}|. \tag{1}
\]
It is tempting to hope that (1) alone forces some \(H[V_i]\) to have a
perfect matching, which would extend every prefix one colour at a time.
The following target-order certificate disproves that statement, even for
an actual locally maximal prefix with only two colours remaining.

This does **not** disprove the existence of a different full packing for the
same support family.  It only rules out propagation from an arbitrary
prefix using (1) alone.

## Residual obstruction

Let the vertex set be \(\{0,\ldots,12\}\), put
\[
 U=\{0,\ldots,7\},
\]
and let
\[
 H=C_3(0,1,2)\mathbin{\dot\cup}C_5(3,4,5,6,7),
 \tag{2}
\]
with vertices \(8,\ldots,12\) isolated.  Take the two remaining supports to
be
\[
 V_{15}=V_{16}=U. \tag{3}
\]
Every vertex of \(U\) has degree two in \(H\) and belongs to both remaining
supports; every vertex outside \(U\) has degree zero and belongs to neither.
Thus (1) holds exactly.

But
\[
 H[U]=C_3\mathbin{\dot\cup}C_5
\]
has no perfect matching: each of its two components has odd order.  Hence
neither remaining colour extends the prefix.

The example is minimal in the number of remaining colours.  If \(m=1\),
(1) makes \(H[V_1]\) one-regular and therefore itself a perfect matching.

## An explicit fifteen-colour prefix

The obstruction above occurs after a genuine packing prefix.  The following
five four-edge matchings and ten five-edge matchings partition
\(E(K_{13})\setminus E(H)\):

\[
\begin{array}{c|l}
0&(1,10),(4,6),(7,8),(9,11)\\
1&(0,11),(5,7),(6,8),(9,12)\\
2&(1,12),(2,9),(4,7),(5,8)\\
3&(3,8),(5,9),(6,10),(7,11)\\
4&(2,4),(5,12),(7,10),(8,9)\\ \hline
5&(0,6),(2,5),(3,12),(7,9),(8,10)\\
6&(0,10),(2,8),(3,5),(4,11),(6,12)\\
7&(0,12),(1,7),(3,11),(4,10),(6,9)\\
8&(0,8),(1,9),(2,6),(3,10),(5,11)\\
9&(0,5),(1,4),(2,11),(3,6),(10,12)\\
10&(0,7),(1,8),(2,10),(3,9),(11,12)\\
11&(0,9),(1,5),(2,7),(4,12),(10,11)\\
12&(0,4),(1,11),(2,3),(8,12),(9,10)\\
13&(1,3),(2,12),(4,8),(5,10),(6,11)\\
14&(0,3),(1,6),(4,9),(7,12),(8,11).
\end{array}
\]

Use each matching's saturated vertex set as its prescribed support, and
append the two supports (3).  The resulting class-B profile is
\[
 (n_8,n_{10},n_{12})=(7,10,0).
\]
Indeed, a vertex in \(U\) has degree ten in \(K_{13}-H\), so it occurs in
ten prefix supports and the two remaining supports.  A vertex outside
\(U\) has degree twelve in \(K_{13}-H\), so it occurs in twelve prefix
supports and neither remaining support.  Thus every row has support sum
twelve, equivalently forbidden-colour sum five, exactly as required.

## Consequence for the global proof

Any completion argument must control more than the residual degrees.  In
particular, it needs either a carefully chosen extendible prefix, a
switching invariant that can repair a locally maximal prefix, or a genuinely
global factorization theorem.  The universal seven-prefix theorem remains
valid, but (1) by itself cannot iterate it through all seventeen colours.

`verify_propagation_counterexample.py` checks the partition, support profile,
row sums, residual-degree identity, and the absence of a perfect matching in
both remaining supports.
