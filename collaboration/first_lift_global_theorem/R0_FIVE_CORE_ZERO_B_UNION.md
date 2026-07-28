# All zero-\(B\) five-core families by support-union rank

Date: 2026-07-28.

## Theorem and scope

In the exceptional \(r=0\) profile, no family of exactly five distinct
cores of types
\[
 A=K_{5,1,1,1},\qquad
 C=K_{3,1,1,1,1},\qquad
 D=K_6
\]
can account for all seven blocked size-ten supports.

This gives a compact independent proof of all 21 zero-\(B\) type
multisets.  It uses only exact support-union optimization and the full
support-union instance of the complement-row inequality; it does not rely
on the longer family census.

## Exact union classification

Fix one non-\(D\) core under the \(S_{13}\)-action and select the remaining
distinct cores with the prescribed types.  For \(D^5\), fix one canonical
\(D\)-core instead.  Let \(J\) be the core-edge union and \(W=V(J)\).
Under only
\[
 |E(J)|\le31,\qquad \Delta(J)\le7,
\]
the exact feasible pairs \((|W|,\min|E(J)|)\) are:

\[
\begin{array}{c|l}
\text{types}&(|W|,\min|E(J)|)\\ \hline
A^5&(8,25),(9,28)\\
A^4C&(8,22),(9,28)\\
A^4D&(8,23),(9,28)\\
A^3C^2&(8,22),(9,28)\\
A^3CD&(8,23),(9,28)\\
A^3D^2&(8,24),(9,28)\\
A^2C^3&(8,22),(9,27)\\
A^2C^2D&(8,23),(9,27)\\
A^2CD^2&(8,24),(9,27)\\
A^2D^3&(8,25),(9,27)\\
AC^4&(8,22),(9,28)\\
AC^3D&(8,23),(9,28)\\
AC^2D^2&(8,23),(9,28)\\
ACD^3&(8,24),(9,28)\\
AD^4&(8,24)\\
C^5&(7,20),(8,24)\\
C^4D&(7,20),(8,23)\\
C^3D^2&(7,20),(8,24)\\
C^2D^3&(7,21),(8,25)\\
CD^4&(7,21),(8,25)\\
D^5&(7,21),(8,26)
\end{array} \tag{1}
\]

Every unlisted union order is infeasible under the two displayed graph
screens.  Aggregating (1) gives the exact histogram
\[
\begin{array}{c|rrrrrrrrr}
(w,e)&(7,20)&(7,21)&(8,22)&(8,23)&(8,24)&
(8,25)&(8,26)&(9,27)&(9,28)\\ \hline
\text{count}&3&3&4&6&6&4&1&4&10.
\end{array} \tag{2}
\]

## Row-rank contradiction

Give the five distinct cores positive multiplicities \(t_i\), respecting
their reuse ceilings
\[
u(A)=3,\qquad u(C)=3,\qquad u(D)=4,
\qquad \sum_i t_i=7.
\]
For \(W\), the complement-row identity requires
\[
2|E(J)|-2|W|
\le
15+\sum_i t_i\min(3,|W|-|C_i|). \tag{3}
\]

For every row of (1), maximize the right side of (3) over every legal
positive multiplicity vector.  Even at that maximum, the exact minimum
edge count on the left gives a strict violation.  Thus no labelled family
in any of the 21 type multisets can cover the seven supports.

Together with `R0_FIVE_CORE_HIGH_B.md`, this excludes every exactly-five-
core total obstruction in the exceptional \(r=0\) profile.

## Reproduction

`verify_r0_five_core_zero_b_union.py` rebuilds all 21 fixed-first
optimizations, checks the exact table and histogram, proves every unlisted
union order infeasible, maximizes over every legal positive multiplicity
vector, and checks every strict inequality.
