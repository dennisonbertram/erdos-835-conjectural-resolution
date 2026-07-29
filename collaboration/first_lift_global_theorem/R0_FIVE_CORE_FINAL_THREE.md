# Final three zero-\(B\) five-core patterns

Date: 2026-07-28.

## Result and scope

The three five-core patterns
\[
 AC^4,\qquad C^5,\qquad C^4D,
\]
where
\[
 A=K_{5,1,1,1},\quad C=K_{3,1,1,1,1},\quad D=K_6,
\]
cannot account for all seven blocked size-ten supports in the
exceptional \(r=0\) profile.  These are the final three rows left pending
by the full zero-\(B\) five-core family enumeration.

## Exact support-union classification

Fix one core under the \(S_{13}\)-action and enumerate every choice of
the other four distinct cores.  Let \(J\) be their edge union and
\(W=V(J)\).  Under only
\[
 |E(J)|\le31,\qquad \Delta(J)\le7,
\]
exact finite optimization gives every feasible union order and its
minimum edge count:
\[
\begin{array}{c|c|c|c|c}
\text{types}&|W|&\min|E(J)|&
2|E(J)|-2|W|&15+\max\text{ triple incidences}\\ \hline
AC^4&8&22&28&21\\
AC^4&9&28&38&28\\
C^5&7&20&26&15\\
C^5&8&24&32&22\\
C^4D&7&20&26&18\\
C^4D&8&23&30&25
\end{array} \tag{1}
\]
Every unlisted union order is infeasible under these graph screens.

For each row, the last column is maximized over every positive
multiplicity vector
\[
 t_1+\cdots+t_5=7
\]
respecting the reuse ceilings \(3,3,4\) for \(A,C,D\), respectively.
No multiplicity shape is assumed.

## Row-rank contradiction

The complement-row identity on \(W\) requires
\[
2|E(J)|-2|W|
\le
15+\sum_i t_i\min(3,|W|-|C_i|). \tag{2}
\]
The left side of every row in (1) strictly exceeds the maximum possible
right side.  Therefore all three type patterns are impossible.

Together with the already terminal other 18 zero-\(B\) rows and the
separate \(B\)-containing theorem, this closes every exactly-five-core
family in the exceptional \(r=0\) profile.

## Reproduction

`verify_r0_five_core_final_three.py` rebuilds all exact minima and
unlisted infeasibilities, exhausts every legal positive multiplicity
vector, and checks all six strict inequalities in (1).
