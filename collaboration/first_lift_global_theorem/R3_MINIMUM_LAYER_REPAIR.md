# Exact layer-repair distances for the two \(r=3\) dead prefixes

Date: 2026-07-27.

## Result and scope

Fix either support matrix and its ordered dead seven-prefix
\((M_0,\ldots,M_6)\) from `R3_DEAD_SEVEN_PREFIXES.md`.
There are two distinct repair quantities.

1. The **eighth-admission distance** is the least number of the seven
   selected layers that must be replaced by perfect matchings on the same
   prescribed supports before some remaining prescribed support admits a
   matching disjoint from the repaired prefix.
2. The **full-completion distance** is the least number of the seven
   selected layers that differ from the original prefix in any complete
   17-layer edge partition on the same ordered support matrix.  Every
   selected layer not counted as changed is retained verbatim.

Their exact values are
\[
\begin{array}{c|cc}
\text{certificate}&\text{eighth admission}&\text{full completion}\\ \hline
C\subset G&1&4\\
D\subset G&1&3
\end{array} \tag{1}
\]

These are exact facts about the two displayed class-B support
certificates only.  They do not prove a universal switching theorem,
class-B-prime or fan realization, or Problem #835.

## One-layer eighth repairs

For \(C\subset G\), selected layer zero is
\[
M_0=\{05,26,34,7\,10\}.
\]
Replace it by
\[
M'_0=\{05,26,37,4\,10\}. \tag{2}
\]
The first remaining size-eight support, whose complement is
\(\{0,1,2,3,5\}\), then admits
\[
N=\{48,69,7\,10,11\,12\}. \tag{3}
\]

For \(D\subset G\), selected layer zero is
\[
M_0=\{06,12,35,8\,12\}.
\]
Replace it by
\[
M'_0=\{06,12,38,5\,12\}. \tag{4}
\]
The first remaining size-eight support, whose complement is
\(\{0,1,2,3,4\}\), then admits
\[
N=\{57,6\,11,8\,12,9\,10\}. \tag{5}
\]

Each replacement is a four-cycle switch: it changes two old layer edges,
preserves the selected support, and remains disjoint from the other six
original layers.  The displayed \(N\) is disjoint from all seven repaired
layers.  The original prefix blocks all ten remaining supports, so
distance zero is impossible.  Thus both eighth-admission distances are
one.  Two changed edges inside the replacement layer are also minimal,
because two distinct perfect matchings on the same support have symmetric
difference equal to a nonempty union of alternating even cycles.

## Crossing-cut lower bound for full completion

Let \(X\subset V(K_{13})\).  For prescribed support \(S_i\), put
\[
u_i(X)=\min\{|S_i\cap X|,\ |S_i\setminus X|\}. \tag{6}
\]
Every perfect matching on \(S_i\) uses at most \(u_i(X)\) edges crossing
the cut \(\delta(X)\).  For an original selected layer \(M_i\), put
\[
a_i(X)=|M_i\cap\delta(X)|. \tag{7}
\]

Suppose a full completion changes the selected layers indexed by
\(T\subseteq\{0,\ldots,6\}\).  The unchanged selected layers contribute
exactly their \(a_i\), the changed selected layers contribute at most
their \(u_i\), and the ten remaining layers contribute at most
\(\sum_{i=7}^{16}u_i\).  Because a full edge partition covers every edge
of \(\delta(X)\), necessarily
\[
\sum_{i\in T}\bigl(u_i(X)-a_i(X)\bigr)
\ \ge\
|X|(13-|X|)
-\sum_{i=7}^{16}u_i(X)
-\sum_{i=0}^{6}a_i(X). \tag{8}
\]
This is a solver-free lower bound on the number of changed selected
layers.

Take \(U=\{0,\ldots,6\}\).  For the \(C\subset G\) certificate,
\[
(a_0,\ldots,a_6)=(0,0,0,0,0,1,1),\qquad
\sum_{i=7}^{16}u_i=26. \tag{9}
\]
The right side of (8) is therefore \(42-26-2=14\), while the seven
available gains \(u_i-a_i\), in decreasing order, are
\[
4,4,4,2,2,2,2. \tag{10}
\]
The three largest gains sum to only \(12\), so at least four selected
layers must change.

For the \(D\subset G\) certificate,
\[
(a_0,\ldots,a_6)=(0,0,0,0,0,0,0),\qquad
\sum_{i=7}^{16}u_i=28. \tag{11}
\]
The deficit is again \(42-28=14\), and the decreasing gains are
\[
6,6,4,2,2,2,2. \tag{12}
\]
The two largest gains sum to only \(12\), so at least three selected
layers must change.

## Full-completion upper bounds

For \(C\subset G\), the literal full completion in
`verify_r3_minimum_layer_repair.py` retains exactly selected layers
\(1,2,3\) and replaces exactly layers \(0,4,5,6\).  Its four replacement
layers are
\[
\begin{aligned}
M'_0&=\{05,24,3\,10,67\},\\
M'_4&=\{09,15,27,3\,12,68\},\\
M'_5&=\{03,17,28,49,5\,10,6\,11\},\\
M'_6&=\{0\,11,16,2\,12,38,4\,10,59\}.
\end{aligned} \tag{13}
\]
Together with the ten literal remaining-layer matchings, these seventeen
matchings partition all 78 edges of \(K_{13}\).  Hence the lower bound
four is attained.

For \(D\subset G\), the literal full completion retains exactly selected
layers \(0,1,2,3\) and replaces exactly layers \(4,5,6\), by
\[
\begin{aligned}
M'_4&=\{03,17,28,49,5\,11\},\\
M'_5&=\{07,26,3\,11,4\,10,58,9\,12\},\\
M'_6&=\{0\,10,19,27,3\,12,48,6\,11\}.
\end{aligned} \tag{14}
\]
The ten remaining literal matchings again complete an edge partition of
\(K_{13}\), attaining the lower bound three.  This proves (1).

## Verification and discovery

`verify_r3_minimum_layer_repair.py` uses only the Python standard library.
It rechecks the original dead-prefix obstruction, both one-layer eighth
repairs, the two literal full completions, and the crossing-cut
calculations above.  As a secondary audit it exhausts all 4,095
nontrivial cuts modulo complementation by requiring \(0\in X\).  The
strongest cut lower bound is four only at \(U\) for \(C\subset G\), and
three at \(U\) and \(U\cup\{10\}\) for \(D\subset G\).

`search_r3_complete_layer_repair.py` is a separate CP-SAT discovery
helper.  Its optimization output suggested the literal completions, but
the exact proof above does not rely on CP-SAT or an unrecorded solver
claim.
