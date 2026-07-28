# Six or seven cores with six or seven non-\(K_6\) cores

Date: 2026-07-28.

## Result and scope

No six- or seven-core total obstruction in the exceptional \(r=0\)
profile has six or seven non-\(K_6\) cores.

Write
\[
 A=K_{5,1,1,1},\quad B=K_{3,3,1,1},\quad
 C=K_{3,1,1,1,1},\quad D=K_6.
\]
There are 28 multisets of six types from \(\{A,B,C\}\).  They occur
either as all six cores, with one core receiving two of the seven
assigned triples, or together with one \(D\)-core in a seven-core
family.  There are a further 36 multisets of seven exceptional types;
these are the all-exceptional seven-core families.  The computation
exhausts all of them.

The six-core \(B^6\) branch is immediately impossible: every \(B\)-core
has reuse ceiling one, so six of them cannot receive seven positive
assignments.  Every other branch fails the support-union row-rank
inequality.

## Six exceptional cores

Fix one exceptional core under \(S_{13}\), select the other five with
their required types, and, in the seven-core case, select one distinct
\(D\)-core.  Under only
\[
 |E(J)|\le31,\qquad \Delta(J)\le7,
\]
the exact feasible-union histograms are
\[
\begin{array}{c|r|r}
(w,e_{\min})&k=6&k=7\\ \hline
(7,21)&1&1\\
(8,22)&3&0\\
(8,23)&1&4\\
(8,24)&2&1\\
(8,25)&21&23\\
(9,27)&1&1\\
(9,28)&4&4\\
(9,30)&1&1
\end{array} \tag{1}
\]
where \(w=|V(J)|\).  The six-core column omits \(B^6\), already excluded
by its reuse ceiling.  Every unlisted union order is graph-screen
infeasible.

For transparency, the exceptional minima in (1) are as follows.
At \(w=7\), only \(C^6\) occurs, with 21 edges.  At \(w=8\):

- for six cores, \(e=22\) for \(A^4C^2,A^3C^3,A^2C^4\);
  \(e=23\) for \(AC^5\); \(e=24\) for \(AB^3C^2,C^6\);
  and \(e=25\) otherwise;
- for seven cores, \(e=23\) for
  \(A^4C^2,A^3C^3,A^2C^4,AC^5\), \(e=24\) for \(C^6\), and
  \(e=25\) otherwise.

At \(w=9\), the only feasible types are
\[
 A^5C,A^4C^2,A^3C^3,A^2C^4,AC^5,B^3C^3,
\]
with minima \(28,28,28,27,28,30\), respectively, for both core
counts.

Let \(s_i=\min(3,w-|C_i|)\).  The maximum complement supply in the
six-core branch is
\[
 15+\sum_i s_i+\max_{i:\,\operatorname{cap}(i)\ge2}s_i, \tag{2}
\]
because exactly one eligible core is doubled.  In the seven-core branch
it is
\[
 15+\sum_i s_i+\min(3,w-6), \tag{3}
\]
the last term coming from the \(D\)-core.  In every row represented in
(1),
\[
 2e_{\min}-2w
\]
strictly exceeds (2) or (3), respectively.  Thus all 28 six-exceptional
type branches are impossible at both core counts.

## Seven exceptional cores

For seven exceptional cores, every assigned triple uses a distinct core.
The exact feasible-union histogram is
\[
\begin{array}{c|r}
(w,e_{\min})&\text{number of type multisets}\\ \hline
(7,21)&1\\
(8,22)&2\\
(8,24)&3\\
(8,25)&31\\
(9,27)&1\\
(9,28)&4
\end{array} \tag{4}
\]
The \(w=7\) row is \(C^7\).  At \(w=8\), the edge-22 types are
\(A^4C^3,A^3C^4\); the edge-24 types are
\(A^2C^5,AC^6,C^7\); all others have 25 edges.  At \(w=9\), the five
feasible types are
\[
 A^5C^2,A^4C^3,A^3C^4,A^2C^5,AC^6
\]
with minima \(28,28,28,27,28\).

The complement supply is
\[
15+\sum_i\min(3,w-|C_i|). \tag{5}
\]
Again \(2e_{\min}-2w\) strictly exceeds (5) in every row of (4), so all
36 all-exceptional seven-core type branches are impossible.

## Consequence

The preceding six-/seven-core notes exclude families with zero through
five exceptional cores.  The present result excludes the last two
layers.  Therefore no family of exactly six or exactly seven distinct
cores can account for all seven blocked size-ten supports in the
exceptional \(r=0\) profile.

## Reproduction

`verify_r0_six_seven_six_seven_exceptional.py` rebuilds every
fixed-first candidate pool, proves every displayed optimum and every
unlisted infeasibility, checks the exact histograms, and checks every
strict row-rank inequality.
