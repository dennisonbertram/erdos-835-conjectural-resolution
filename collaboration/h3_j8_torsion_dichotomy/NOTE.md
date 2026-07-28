# The \(j=8\) four-cube torsion dichotomy

## Scope

This note records two exact arithmetic reductions for the attempted automatic
\(j=8\to9\) top-properness lift.  They are necessary-condition results, not a
proof of the lift.  They do not construct a colouring and do not solve
Erdős--Rosenfeld Problem #835.

Let \(A\) be a 13-element set and let
\[
-1\le e_Q\le12\qquad\left(Q\in\binom A4\right).
\]
Assume the recurrence congruences
\[
\sum_{Q\in\binom S4}e_Q\equiv0\pmod q
\quad\text{whenever}\quad
2\le q\le8,\quad |S|=q+3.
\tag{1}
\]

## Four-cube dichotomy

Choose eight distinct points, grouped into four ordered pairs
\((a_i,b_i)\), \(1\le i\le4\).  Define
\[
\Delta=
\sum_{\epsilon\in\{0,1\}^4}
(-1)^{|\epsilon|}
e_{\{c_{1,\epsilon_1},\ldots,c_{4,\epsilon_4}\}},
\qquad c_{i,0}=a_i,\quad c_{i,1}=b_i.
\tag{2}
\]

### Proposition 1

Every coefficient (2) belongs to
\[
\{0,-60,60\}.
\]

### Proof

Fix \(q\in\{2,3,4,5,6\}\).  There are five points outside the cube, so
choose a filler set \(F\) of size \(q-1\).  Apply the four-fold alternating
difference to (1) on the sixteen sets
\[
F\cup\{c_{1,\epsilon_1},\ldots,c_{4,\epsilon_4}\}.
\]
Every term cancels unless its four-set selects exactly one point from each
pair.  The surviving sum is \(\Delta\), hence \(q\mid\Delta\).  Therefore
\[
\operatorname{lcm}(2,3,4,5,6)=60\mid\Delta.
\]

There are eight positive and eight negative terms in (2).  The coefficient
range gives
\[
\Delta\le8\cdot12-8\cdot(-1)=104
\]
and the same estimate for \(-\Delta\).  The only multiples of \(60\) in
\([-104,104]\) are \(0,\pm60\). \(\square\)

Thus any argument that separately eliminates the all-zero four-cube branch
reduces the general case to a normalized \(\Delta=60\) local configuration.
The present proposition does not eliminate that torsion configuration.

## Exact field-rank reduction

For \(4\le s\le13\), let \(M_s\) be the zero-one inclusion matrix whose rows
are indexed by \(\binom As\), whose columns are indexed by \(\binom A4\),
and whose \((S,Q)\) entry is \(1\) exactly when \(Q\subseteq S\).  All ranks
below are row ranks over the stated prime field.

### Proposition 2

The relevant ranks are
\[
\begin{array}{c|c}
\text{matrix or stacked matrices}&\text{rank}\\ \hline
M_5\text{ over }\mathbf F_2&495\\
[M_5;M_7;M_9;M_{11}]\text{ over }\mathbf F_2&495\\
M_6\text{ over }\mathbf F_3&441\\
[M_6;M_9]\text{ over }\mathbf F_3&441\\
M_8\text{ over }\mathbf F_5&429\\
M_{10}\text{ over }\mathbf F_7&208.
\end{array}
\tag{3}
\]

In particular, the \(q=6\) congruences on 9-sets are redundant: their
modulo-2 rows lie in the row span of \(M_5\), and their modulo-3 rows lie in
the row span of \(M_6\).  The \(q=2\) and \(q=3\) congruences therefore make
every 9-set sum divisible by both \(2\) and \(3\), hence by \(6\).

The field ranks in (3) do not replace the genuinely 2-adic congruences
modulo \(4\) and modulo \(8\); those must be retained in an exact reduced
model.

## Remaining gap

The unresolved local arithmetic branch has a four-cube with
\(\Delta=\pm60\), the full coefficient range, all congruences (1), and the
tower's triple-capacity inequalities.  Neither the rank reduction nor
finite solver silence decides whether that branch is feasible.

