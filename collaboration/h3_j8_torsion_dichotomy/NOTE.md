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

## Local structure of a \(\Delta=60\) cube

Put \(d_Q=e_Q+1\), so \(0\le d_Q\le13\), and define the triple load
\[
L_T=\sum_{Q\supseteq T}d_Q.
\]
The tower's local capacity condition is \(L_T\le13\).

Orient a \(\Delta=60\) cube and let \(P\) and \(N\) be the sums of \(d_Q\)
over its eight positive and eight negative cells.  Then \(P-N=60\).
Every edge of the 4-cube joins a positive cell to a negative cell, and the
two endpoints contain their shared transversal triple.  Hence each edge
gives
\[
d_{Q_+}+d_{Q_-}\le L_{Q_+\cap Q_-}\le13.
\]
There are 32 edges and every cell lies on four, so
\[
4(P+N)\le32\cdot13.
\]
Consequently
\[
0\le N\le22,\qquad 60\le P\le82.
\tag{4}
\]

In fact the two endpoints in (4) can be removed.  Regard the positive and
negative cube cells as the two halves of the bipartite 4-cube.  For a subset
\(B\) of \(k\) negative cells, let \(f(k)\) be the minimum size of its
positive neighborhood.  The elementary neighborhood table is
\[
\bigl(f(0),\ldots,f(8)\bigr)=(0,4,6,7,7,8,8,8,8).
\tag{5}
\]
For \(k=1,2\), this follows directly from the fact that two same-parity
4-cube vertices have at least six distinct neighbors.  For \(k=3,4\), two
missed positive vertices would have at least six neighbors inside a
negative complement of size at most five.  For \(k\ge5\), one missed
positive vertex would need all four of its neighbors in a complement of
size at most three.

Write \(n_v=d_v\) on the negative cube cells, and put
\[
m_u=\max_{v\sim u}n_v
\]
on the positive cells.  The edge inequalities give
\[
d_u\le13-m_u,\qquad
P\le104-\sum_um_u.
\tag{6}
\]
For the level sets \(B_t=\{v:n_v\ge t\}\), with \(k_t=|B_t|\), layer-cake
counting and (5) give
\[
\sum_um_u=\sum_{t\ge1}|N(B_t)|\ge\sum_{t\ge1}f(k_t),
\qquad \sum_tk_t=N.
\tag{7}
\]
If \(N=21\) or \(22\), at least three levels are nonempty.  With exactly
three, every \(k_t\ge N-16\ge5\), so (7) is at least \(24\).  With at least
four, use \(f(k)\ge k\), with equality only at \(k=8\) and excess at least
one otherwise.  There can be at most two 8s because \(N\le22\).  Total
excess at most two would force two further values \(k=7\), already giving
sum at least \(30\).  Hence the excess is at least three and (7) is again
at least \(24\).

But \(P=N+60\) and (6) require
\(\sum_um_u\le44-N\), which is at most \(23\) for \(N=21,22\).  Therefore
\[
0\le N\le20,\qquad 60\le P\le80.
\tag{8}
\]

For later coupling to the five outside vertices, each of the 32 cube edges
has an edge-triple load \(L_T\).  Define its residual and deficiency totals
\[
R=\sum_{\text{edges }T}\bigl(L_T-d_{Q_+(T)}-d_{Q_-(T)}\bigr),
\qquad
H=\sum_{\text{edges }T}(13-L_T).
\]
Both are nonnegative.  Since every cube cell lies on four edges,
\[
R+H
=32\cdot13-4(P+N)
=176-8N.
\tag{9}
\]
In particular, the endpoint case \(N=20\) has \(R+H=16\).  At most 16
edge triples can then be unsaturated, so at least 16 of their loads equal
13.  The binary residue description below makes each such load the upper
choice \(6+7\).

There is also an exact binary description of every triple load.  Write
\(L_U=\sum_{Q\supseteq U}d_Q\), including \(L_\varnothing=\sum_Qd_Q\).
For a triple \(T\), the \(q=7\) congruence on \(A\setminus T\), together
with \(\binom{10}{4}=210\equiv0\pmod7\), gives
\[
0\equiv
L_\varnothing-\sum_{a\in T}L_a
+\sum_{\{a,b\}\in\binom T2}L_{ab}-L_T
\pmod7.
\tag{10}
\]
If \(r_T\in\{0,\ldots,6\}\) is the residue on the right of (10) before
subtracting \(L_T\), then the capacity range \(0\le L_T\le13\) implies
\[
L_T=r_T+7b_T,\qquad b_T\in\{0,1\}.
\tag{11}
\]
Thus a fixed torsion cube has only one binary \(7\)-adic choice per triple,
although coupling those 286 choices remains unresolved.

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

## Recurrence nonnegativity

Congruence is not the whole recurrence condition.  At the first derived
level, every 5-set satisfies
\[
2N_S+\sum_{Q\in\binom S4}d_Q=13.
\]
Thus an exact necessary-condition model must impose both odd parity and
\[
\sum_{Q\in\binom S4}d_Q\le13
\qquad\left(S\in\binom A5\right).
\tag{12}
\]
The analogous raw \(d\)-sum upper bounds at sizes \(7,9,11\) are
\(195,702,858\).  They are already implied by the triple capacities:
\[
4\sum_{Q\in\binom S4}d_Q
=\sum_{T\in\binom S3}L_T
\le13\binom{|S|}{3}.
\]
All other upper and lower recurrence bounds are automatic from
\(0\le d_Q\le13\) and the triple capacities.  The search model below
includes every inequality (12); earlier congruence-only experiments were
incomplete and carry no verdict.

## Remaining gap

The unresolved local arithmetic branch has a four-cube with
\(\Delta=\pm60\), the full coefficient range, all congruences (1), and the
tower's triple-capacity inequalities.  Neither the rank reduction nor
finite solver silence decides whether that branch is feasible.

## Reproducible exact model

[`search_fixed_delta60.py`](search_fixed_delta60.py) encodes the complete
fixed-cube necessary-condition model.  It uses independent original rows
for the prime-field reductions in (3), retains every modulo-4 and modulo-8
row, imposes all 1,287 size-5 recurrence inequalities (12), and adds only a
harmless ordering of the five points outside the normalized cube.  A run
returning `UNKNOWN` is not evidence of feasibility or infeasibility.

The smaller 70-coordinate projection to the cube's eight vertices is
feasible.  [`internal_cube_positive_control.json`](internal_cube_positive_control.json)
records all \(d_Q\) in lexicographic four-set order, and
[`verify_internal_cube_positive_control.py`](verify_internal_cube_positive_control.py)
checks every internal triple capacity, every internal \(q=2,3,4,5\)
congruence, and \((P,N,\Delta)=(60,0,60)\).  This positive control proves
that the eight-vertex constraints alone cannot eliminate torsion.  It does
not assert that the assignment extends to the five outside vertices.

Example:

```text
python3 collaboration/h3_j8_torsion_dichotomy/search_fixed_delta60.py \
  --seconds 600 --workers 16
```
