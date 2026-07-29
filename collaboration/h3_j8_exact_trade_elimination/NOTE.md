# The exact-trade branch at the \(j=8\) lift is zero

## Scope

This note eliminates one exact subcase of the attempted automatic
\(j=8\to9\) top-properness lift.  It does **not** prove the general lift,
because the tower gives triple degrees at most \(3\), not necessarily zero.
It does not construct a colouring and does not solve Erdős--Rosenfeld
Problem #835.

Let \(A\) be a 13-element set.  For each \(Q\in\binom A4\), let
\[
e_Q=d_Q-1,\qquad -1\le e_Q\le12.
\]
For \(U\subseteq A\), write
\[
D_U=\sum_{\substack{Q\in\binom A4\\U\subseteq Q}}e_Q,
\qquad E=D_\varnothing=\sum_Qe_Q.
\]
The exact-trade branch is
\[
D_T=0\qquad\text{for every }T\in\binom A3.
\]
The \(q=6\) recurrence congruence is
\[
\sum_{Q\in\binom S4}e_Q\equiv0\pmod6
\qquad (S\in\binom A9).
\]

## Proposition

Under the displayed hypotheses, \(e_Q=0\) for every \(Q\).

## Proof

Double counting extensions of a fixed pair, point, and the empty set gives
\[
\sum_{\substack{T\in\binom A3\\B\subseteq T}}D_T
=\binom{4-|B|}{3-|B|}D_B
\qquad (|B|\le2).
\]
Thus exact vanishing of all triple degrees successively gives
\[
D_B=0\quad (|B|=2,1,0);
\]
in particular every pair degree, every point degree, and \(E\) vanish.

Fix \(R\in\binom A4\), and put \(S=A\setminus R\).  Inclusion--exclusion
over the requirement \(Q\cap R=\varnothing\) gives
\[
\sum_{Q\in\binom S4}e_Q
=E-\sum_{a\in R}D_a+\sum_{\{a,b\}\in\binom R2}D_{ab}
-\sum_{T\in\binom R3}D_T+e_R
=e_R.
\]
Since \(|S|=9\), the \(q=6\) congruence now says \(6\mid e_R\).  But
\(-1\le e_R\le12\), so
\[
e_R\in\{0,6,12\}.
\]
All coefficients are nonnegative, while their sum is \(E=0\).  Therefore
every coefficient is zero. \(\square\)

## Consequence and remaining gap

A countermodel to automatic top properness cannot be a nonzero integral
\(3\)-\((13,4)\) trade.  Any remaining countermodel must use genuinely
nonzero triple degrees \(D_T\le3\).  The proof does not control that general
case because those degrees may be negative.

