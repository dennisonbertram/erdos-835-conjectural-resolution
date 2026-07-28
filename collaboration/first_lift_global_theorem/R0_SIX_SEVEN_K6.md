# Six or seven cores with at most one non-\(K_6\) core

Date: 2026-07-28.

## Result and scope

In the exceptional \(r=0\) profile, neither six nor seven distinct cores
can collectively account for all seven blocked size-ten supports when all
but at most one core are \(K_6\)'s.

For six distinct cores the only positive multiplicity shape is
\[
 2+1+1+1+1+1,
\]
and for seven it is \(1+1+1+1+1+1+1\).  In either case the total
multiplicity is seven.

The possible exceptional core may have any of the other three surviving
types:
\[
 K_{5,1,1,1},\qquad K_{3,3,1,1},\qquad K_{3,1,1,1,1}.
\]
Families with at least two non-\(K_6\) cores remain open.

## Exact union classification

Fix a canonical core \(X\) under \(S_{13}\), where
\[
 X\in\{A,B,C,D\}
 =\{K_{5,1,1,1},K_{3,3,1,1},K_{3,1,1,1,1},K_6\}.
\]
Enumerate the \(K_6\)'s that pass the necessary two-core conditions
\[
 |E(J)|\le31,\qquad \Delta(J)\le7.
\]
The pool sizes for \(X=A,B,C,D\) are respectively
\[
 28,\qquad28,\qquad133,\qquad364. \tag{1}
\]
Select five or six \(K_6\)'s as appropriate, and let \(W\) be the union of
all core supports.  Exact finite optimization gives the complete list of
feasible union orders and minimum edge counts:
\[
\begin{array}{c|c|c}
X&|W|&\min |E(J)|\\ \hline
A&8&24\\
B&8&26\\
C&7&21\\
C&8&25\\
D&7&21\\
D&8&26
\end{array} \tag{2}
\]
The table is the same for six and seven total cores.  Every unlisted union
order is infeasible under the 31-edge and maximum-degree bounds.

## Full row-rank contradiction

Apply the complement-row identity to \(W\).  The total number of
occurrences of vertices of \(W\) among all ten remaining complement sets
is
\[
 \sum_{v\in W}(d_F(v)-2)
 \ge 2|E(J)|-2|W|. \tag{3}
\]
The three complement five-sets contribute at most fifteen occurrences in
\(W\).

A complement triple assigned to a core with support \(C_i\subseteq W\)
contains at most
\[
 \min\{3,|W|-|C_i|\}
\]
vertices of \(W\).  Sum this bound with the assigned multiplicities.  In
the six-core case, check both possible doubled-core choices, except that
the \(B\)-core has reuse ceiling one and cannot be doubled.

For every row of (2), even the larger of the possible triple-incidence
bounds is strictly below the lower bound in (3):
\[
\begin{array}{c|c|c|c}
X&|W|&2|E(J)|-2|W|&
15+\max\text{ triple incidences}\\ \hline
A&8&32&27\\
B&8&36&27\\
C&7&28&21\\
C&8&34&28\\
D&7&28&22\\
D&8&36&29
\end{array} \tag{4}
\]
The same upper bounds cover the seven-core all-singleton assignment.

Thus no six- or seven-core branch with at most one non-\(K_6\) core can
cover the seven blocked supports.

## Reproduction

`verify_r0_six_seven_k6.py` independently rebuilds all four candidate
pools, solves every fixed-\(|W|\) finite optimization, checks the exact
table (2), and checks every strict row-rank inequality in (4).  It computes
the optimization table twice: once with CP-SAT and once with a separate
standard-library exhaustive backtracking search.  The latter fixes the
support union under the stabilizer of the canonical first core and exhausts
all distinct \(K_6\)-subfamilies subject to the edge and degree bounds.
