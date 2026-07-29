# Hoffman, intersection, and Odd-cover audit

## Status

This is a necessary-condition audit for a hypothetical tight colouring in
Erdős--Rosenfeld Problem #835.  It does **not** prove nonexistence, either for
all even \(k>2\) or for the first open case \(k=16\).

Assume throughout that \(k>2\) is even, \(q=k+1\), and
\[
 c:\binom{V}{k}\longrightarrow {\cal Q},\qquad |V|=2k,\quad |{\cal Q}|=q,
\]
is a proper \(q\)-colouring of \(J(2k,k)\).  The primality of \(q\) is the
remaining admissible case, but none of the lemmas below uses more than the
existence of this tight colouring.

## 1. The rooted large set and Hoffman equality

Fix \(\infty\in V\), put \(X=V\setminus\{\infty\}\), and define
\[
 \phi(A)=c(\{\infty\}\cup A)
 \quad\left(A\in\binom X{k-1}\right).
\]
Every \((k-2)\)-set \(T\subset X\) has \(k+1=q\) extensions
\(\{\infty\}\cup T\cup\{x\}\), and they form a \(q\)-clique.  Hence each
colour class
\[
 {\cal D}_i=\left\{A\in\binom X{k-1}:\phi(A)=i\right\}
\]
is an \(S(k-2,k-1,2k-1)\), and the \(q\) classes partition
\(\binom X{k-1}\).  Thus a tight colouring gives
\[
 LS(k-2,k-1,2k-1).                                      \tag{1}
\]

Complement the blocks in \(X\):
\[
 {\cal C}_i=\{X\setminus A:A\in{\cal D}_i\}
 \subseteq\binom Xk.
\]
Each \({\cal C}_i\) is independent in \(J(2k-1,k)\), and
\[
 |{\cal C}_i|
 =\frac1{k+1}\binom{2k-1}{k}.
\]
The graph \(J(2k-1,k)\) has valency \(k(k-1)\) and least eigenvalue
\(-(k-1)\), so this is equality in the Hoffman bound.  Consequently
\[
 {\bf 1}_{{\cal C}_i}\in E_0\oplus E_{k-1}.              \tag{2}
\]
Every matrix in the Johnson scheme acts scalarly on both summands in
(2).  It follows that every exact-intersection relation is equitable:
for fixed \(s\), the number of \(D\in{\cal C}_j\) satisfying
\(|B\cap D|=s\) depends only on whether \(j=c(B)\) or \(j\ne c(B)\).
In particular, all other colours have the same count.  For ordinary
Johnson adjacency this says that every vertex has \(k-1\) neighbours in
each other colour and none in its own colour.

## 2. Fixed-block intersection numbers

Fix \(A\in{\cal D}_i\), put \(b=k-1\), and let
\[
 m_r=\#\{A'\in{\cal D}_i:|A\cap A'|=r\}\qquad(0\le r\le b).
\]
For \(0\le j\le b-1\), the number of blocks of \({\cal D}_i\) through a
fixed \(j\)-set is
\[
 \lambda_j
 =\frac{\binom{2k-1-j}{k-2-j}}{k-1-j},
 \qquad \lambda_b:=1.                                   \tag{3}
\]
Counting pairs \((J,A')\) with \(J\subseteq A\cap A'\), \(|J|=j\),
gives the Mendelsohn equations
\[
 \sum_{r=0}^{b}\binom rj m_r=\binom bj\lambda_j.
\]
Binomial inversion therefore gives the complete forced distribution
\[
 \boxed{\displaystyle
 m_r=\binom br\sum_{j=r}^{b}(-1)^{j-r}
       \binom{b-r}{j-r}\lambda_j.}                       \tag{4}
\]
In particular, direct simplification of (4) gives
\[
 m_0=\frac{k}{k+1}\bigl(1-(-1)^k\bigr),\qquad
 m_1=\binom k2\quad(k\ {\rm even}).                      \tag{5}
\]
Thus every \({\cal D}_i\) is intersecting when \(k\) is even.

If \(B=X\setminus A\) and \(B'=X\setminus A'\), then
\[
 |B\cap B'|=1+|A\cap A'|.
\]
Hence the same-colour counts for the complementary \(k\)-sets are
\[
 n_s=m_{s-1}.                                            \tag{6}
\]
There are
\[
 \binom{k}{2}\binom{k-1}{k-2}
 =\binom{k}{2}(k-1)
\]
total \(k\)-sets meeting a fixed \(k\)-set in exactly two points.  By
(5), (6), and equitability, the count in every other colour is
\[
 \frac{\binom{k}{2}(k-1)-\binom{k}{2}}{k}
 =\boxed{\binom{k-1}{2}}.                                \tag{7}
\]

## 3. The complement-missing law

Let \(B\in\binom Xk\), and consider the upper \(q\)-clique on
\(\{\infty\}\cup B\).  Its \(k\) rooted members have colours
\[
 \phi(B\setminus\{x\})\qquad(x\in B),
\]
so \(c(B)\) is the unique colour missing from these \(k\) colours.

Put \(A_0=X\setminus B\).  Every \(B\setminus\{x\}\) is disjoint from
\(A_0\).  Equation (5) says that two blocks in one \({\cal D}_i\) cannot
be disjoint.  Therefore \(\phi(A_0)\) occurs on none of the \(k\) faces
and must be the missing colour:
\[
 \boxed{c(B)=\phi(X\setminus B).}                         \tag{8}
\]
Equivalently, the original colour is invariant under complementation in
\(V\).  This proves that the rooted large set determines the whole tight
colouring; it is not an additional assumption.

## 4. The Odd-graph cover

Represent each complementary pair of middle-layer \(k\)-sets by its
\((k-1)\)-set \(A\subset X\).  Two representatives are joined precisely
when they are disjoint, giving
\[
 O_k=KG(2k-1,k-1).
\]
Equation (8), together with the Steiner uniqueness condition, shows that
the closed neighbourhood of every vertex contains all \(q\) colours
exactly once.  Thus
\[
 \pi:O_k\longrightarrow K_{k+1}                          \tag{9}
\]
is a covering projection.

Write \(F_i=\pi^{-1}(i)\).  For every \(i\ne j\), the edges between
\(F_i\) and \(F_j\) form a perfect matching
\[
 M_{ij}:F_i\longrightarrow F_j,\qquad M_{ji}=M_{ij}^{-1}. \tag{10}
\]
This is the exact content of the disjointness relation.  A generic graph
cover permits arbitrary matching monodromy, so (10) by itself supplies no
fixed permutation sign.

## 5. Exact two-geodesic \(2\)-to-\(1\) lemma

Fix \(A\in F_i\), a different colour \(j\), and define
\[
 E_{ij}(A)=\{D\in F_j:|A\cap D|=1\}.
\]
By (7), after taking complements,
\[
 |E_{ij}(A)|=\binom{k-1}{2}.                              \tag{11}
\]

Let \(D\in E_{ij}(A)\), write \(A\cap D=\{y\}\), and write
\[
 X\setminus(A\cup D)=\{x,z\}.
\]
There are exactly two length-three paths from \(A\) to \(D\):
\[
\begin{aligned}
A&\longrightarrow(D\setminus\{y\})\cup\{z\}
 \longrightarrow(A\setminus\{y\})\cup\{x\}
 \longrightarrow D,\\
A&\longrightarrow(D\setminus\{y\})\cup\{x\}
 \longrightarrow(A\setminus\{y\})\cup\{z\}
 \longrightarrow D.                                     \tag{12}
\end{aligned}
\]
Conversely, every nonbacktracking length-three path from \(A\) ends in a
set meeting \(A\) in exactly one point.  These assertions follow directly
by writing the first neighbour as
\((X\setminus A)\setminus\{x\}\) and successively imposing
nonbacktracking.

For an ordered pair of distinct colours
\[
 (a,b)\in({\cal Q}\setminus\{i,j\})^2,\qquad a\ne b,
\]
the base path \(i,a,b,j\) lifts uniquely from \(A\).  Its four colours are
distinct: a repetition at distance two would force an immediate lifted
backtrack through the unique matching in (10).  Therefore its endpoint is
in \(E_{ij}(A)\).  Equations (11)--(12) prove the exact statement
\[
 \boxed{\begin{array}{c}
 \{(a,b):a,b\notin\{i,j\},\ a\ne b\}
 \longrightarrow E_{ij}(A)\\[2mm]
 \text{is \(2\)-to-\(1\).}
 \end{array}}                                             \tag{13}
\]
Indeed the domain has \((k-1)(k-2)\) elements and every fibre consists of
the two paths in (12).

Equivalently, if \(P_\sigma\) denotes the matrix of a matching
permutation and \(R_{ij}(A,D)=1\) exactly when \(|A\cap D|=1\), then
\[
 \sum_{\substack{a,b\notin\{i,j\}\\a\ne b}}
 P_{\,M_{bj}M_{ab}M_{ia}}
 =2R_{ij}.                                                \tag{14}
\]

## 6. The failed leap

Suppose the two paths to one endpoint have intermediate colour sequences
\((a,b)\) and \((a',b')\).  The subset geometry proves
\[
 a'\ne a,\qquad b'\ne b,
\]
because the two first internal vertices meet in \(k-2\) points, as do the
two second internal vertices.  It does **not** prove
\[
 (a',b')=(b,a).                                          \tag{15}
\]
Thus (13) gives a pairing of the directed edges on the \(k-1\) internal
colours, not a canonical identification with the undirected edges.  A
reversal rule, commutativity law, or ordinary edge-colouring extracted
from (13) would require a new global compatibility argument.

Even the elementary local restrictions admit non-reversal pairings.  On
three internal colours, for example, the directed edges can be paired as
\[
 (01,12),\qquad(02,20),\qquad(10,21);
\]
the tails and heads differ within every pair, but two pairs are not
reversals.  This is not asserted to extend to an Odd-graph cover; it shows
only that (15) cannot be inferred from the proved local conditions.

At \(k=16\), a fibre has
\[
 |F_i|=\frac1{17}\binom{31}{15}=17\,678\,835
\]
vertices, and \(R_{ij}\) is \(105\)-regular.  Both numbers are odd, but
this is not a contradiction: every regular bipartite graph has a
one-factorization.  Likewise, triangle monodromies in (10) are
fixed-point-free because \(O_k\) is triangle-free, but fixed-point-free
permutations of an odd set can have either sign.  No determinant or
matching-sign identity follows from (10), (13), or (14).

## 7. Small-case controls and falsification

The exact distributions from (4) are:
\[
\begin{array}{c|l}
k&(m_0,m_1,\ldots,m_{k-1})\\ \hline
2&(0,1)\\
4&(0,6,0,1)\\
6&(0,15,20,30,0,1)\\
16&(0,120,3360,49140,349440,1417416,3363360,4877730,\\
&\quad4324320,2362360,768768,147420,14560,840,0,1).
\end{array}
\]

- For \(k=2\), \(O_2=K_3\) really covers \(K_3\).  Any proposed universal
  sign obstruction must account for this degenerate positive case.
- For \(k=4\), a Fano plane \(S(2,3,7)\) realizes the complete local
  distribution \((0,6,0,1)\), but \(LS(2,3,7)\) does not exist.  Exhaustive
  enumeration of the 30 labelled Fano planes shows that each has only one
  block-disjoint mate, so at most two, not five, can occur together.
- For \(k=6\), the Witt system \(S(4,5,11)\) realizes
  \((0,15,20,30,0,1)\), but there is no required seven-class partition.

The Fano and Witt controls are decisive falsifiers of any argument claiming
that the one-class intersection distribution alone is contradictory.  The
missing obstruction is simultaneous cross-colour compatibility.

## Verdict

The valid output of this route is the complement-missing law, the
association-scheme equitability, the Odd-cover formulation, and the labelled
two-geodesic factorization (13)--(14).  The attempted parity/sign conclusion
depends on the unjustified reversal step (15).  Therefore this route closes
**neither** all admissible \(k\) **nor** \(k=16\).
