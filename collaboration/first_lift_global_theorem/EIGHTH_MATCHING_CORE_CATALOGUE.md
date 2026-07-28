# Exact obstruction cores at the eighth matching

Date: 2026-07-27.

## Result and scope

Let \(F\) be the union of seven already selected support matchings in a
target \(n=13,q=17\) class-B instance, and let
\[
 H=K_{13}-F.
\]
This note classifies the complete multipartite cores that \(F\) must contain
if a remaining support of size ten or twelve has no perfect matching in
\(H\).

It is a reduction for a switching proof, not yet an eighth-colour packing
theorem.  Supports of size eight are deliberately not classified here:
after seven deletions their residual minimum degree may be zero, whereas
every target profile still has a remaining support of size ten or twelve.

## Prefix constraints

Every vertex belongs to twelve of all seventeen supports.  Only ten colours
remain, so every vertex belongs to at least two selected supports.  Since a
selected matching saturates its support,
\[
 2\le d_F(v)\le7. \tag{1}
\]
The possible seven-prefix profiles used by the seven-colour theorem have
the following edge totals:
\[
\begin{array}{c|c|c}
r&\text{selected support sizes}&|E(F)|\\ \hline
0&8^4\,10^3&31\\
1&8^4\,10^2\,12&32\\
2,3,4&8^4\,10\,12^2&33\\
5&8^4\,12^3&34.
\end{array} \tag{2}
\]
In particular, \(|E(F)|\le34\), \(\Delta(F)\le7\), and
\[
 |E(F[X])|\le7\left\lfloor |X|/2\right\rfloor
 \quad\text{for every }X. \tag{3}
\]

## Coarsened Tutte barriers

Let \(V\) be a remaining support of even size \(n\in\{10,12\}\), and suppose
\(H[V]\) has no perfect matching.  Tutte's theorem gives
\(S\subseteq V\), with \(s=|S|\), such that \(H[V]-S\) has more than \(s\)
odd components.  Parity makes their number at least \(s+2\).

Absorb every even component into an odd component.  If more than \(s+2\)
odd blocks remain, repeatedly merge three odd blocks into one.  We obtain
exactly \(s+2\) odd blocks partitioning \(V\setminus S\), with no
\(H\)-edge between distinct blocks.  Therefore \(F\) contains every edge
between distinct blocks.

If one block has order \(b\), each of its vertices has
\(n-s-b\) forced \(F\)-neighbours in the other blocks.  By
\(\Delta(F)\le7\),
\[
 b\ge n-s-7. \tag{4}
\]
The odd integer partitions satisfying (4) give the complete list below.

## Size-ten catalogue

For \(n=10\), the seven possible block-size patterns and their forced core
edge counts are
\[
\begin{array}{c|c|c|c|c|c}
s&\text{odd blocks}&\text{core}&|E(\text{core})|
   &\text{pointwise ceiling}&r=0\text{ ceiling}\\ \hline
0&3+7&K_{3,7}&21&5&5\\
0&5+5&K_{5,5}&25&7&5\\
1&3+3+3&K_{3,3,3}&27&6&4\\
2&5+1+1+1&K_{5,1,1,1}&18&5&5\\
2&3+3+1+1&K_{3,3,1,1}&22&5&5\\
3&3+1+1+1+1&K_{3,1,1,1,1}&18&6&6\\
4&1+1+1+1+1+1&K_6&15&7&6.
\end{array} \tag{5}
\]
Here \(K_{a_1,\ldots,a_k}\) denotes the complete multipartite graph with
those part sizes.

## Size-twelve catalogue

For \(n=12\), the numerical patterns are
\[
\begin{array}{c|c|c|c|c}
s&\text{odd blocks}&\text{core}&|E(\text{core})|
   &\text{reuse ceiling}\\ \hline
0&5+7&K_{5,7}&35&5\\
4&3+1+1+1+1+1&K_{3,1,1,1,1,1}&25&5\\
5&1+1+1+1+1+1+1&K_7&21&6.
\end{array} \tag{6}
\]
The first row cannot occur in a target seven-prefix because its forced
35-edge core exceeds the global bound \(|E(F)|\le34\) in (2).  Thus a
blocked size-twelve support forces only
\[
 K_{3,1,1,1,1,1}=K_8-E(K_3)
 \quad\text{or}\quad K_7. \tag{7}
\]

## Why the reuse ceilings hold

Suppose a fixed core \(J\subseteq F\) has maximum degree \(\Delta(J)\), and
let \(v\) be a core vertex of that degree.  The residual-degree identity is
\[
 d_H(v)=12-d_F(v).
\]
It is also the number of remaining supports containing \(v\).  Since
\(d_F(v)\ge\Delta(J)\), at most \(12-\Delta(J)\) remaining supports can
contain the whole core.  This gives the final columns of (5) and (6).

Consequently, one obstruction core cannot be invoked without limit.  For
example, a fixed \(K_{3,7}\) can obstruct at most five remaining supports,
a fixed \(K_{3,3,3}\) at most six, and a fixed \(K_6\) at most seven.  A
switching proof can therefore focus on how distinct cores overlap inside a
31-to-34-edge graph satisfying (1)--(3).

## Sharper reuse in the exceptional profile

For \(r=0\), seven size-ten and three size-eight supports remain.  Suppose a
fixed core \(J\), on a vertex set \(C\), is contained in \(t\) of the seven
size-ten supports.  Each of the three size-eight supports contains at least
\[
 8-(13-|C|)=|C|-5
\]
vertices of \(C\), so together they require at least
\[
 3|C|-15 \tag{8}
\]
small-support incidences inside \(C\).

On the other hand, a vertex \(v\in C\) belongs to at most
\(12-d_F(v)\le12-d_J(v)\) remaining supports.  The \(t\) size-ten supports
already consume \(t\) of those incidences.  Hence a necessary condition is
\[
 \sum_{v\in C}\max\{0,12-d_J(v)-t\}\ \ge\ 3|C|-15. \tag{9}
\]
Intersecting (9) with the pointwise ceiling gives the final column of (5).
In particular, no fixed core can obstruct all seven remaining size-ten
supports: the largest \(r=0\) reuse ceiling is six.  Therefore, if all seven
large supports were blocked after a seven-prefix, \(F\) would have to
contain at least two distinct obstruction cores.  This reduces the
exceptional profile to an overlap-or-switching problem.

## Remaining frontier

To prove an eighth-colour theorem it now suffices to show that the cores
needed to obstruct every remaining size-ten and size-twelve support cannot
coexist, or that a selected matching can be switched to destroy a surviving
core without creating another one.  The residual-degree identity alone
cannot provide that repair, as the minimal two-colour certificate in
`PROPAGATION_COUNTEREXAMPLE.md` shows.

`verify_eighth_matching_core_catalogue.py` exhausts the odd integer
partitions, checks every displayed edge count and reuse ceiling, and checks
the target profile totals.
