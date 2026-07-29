# Every target aggregate degree sequence is graphic

Date: 2026-07-27.

## Statement

In a class-B order-\(18\) first-lift instance, let \(A\) be the thirteen
hole vertices and let \(V_c\subseteq A\) be the support of colour \(c\).
There are seventeen colours, every vertex belongs to twelve supports, and
each colour is forbidden at \(1\), \(3\), or \(5\) vertices.  Equivalently,
\[
 |V_c|\in\{12,10,8\}.
\]

For a set \(C\) of colours, define
\[
 d_C(v)=|\{c\in C:v\in V_c\}|.
\tag{1}
\]
If the required matchings for the colours in \(C\) exist, their union is a
simple graph with degree sequence \((d_C(v):v\in A)\).  Thus graphicality of
every sequence (1) is a necessary condition for completion.

> **Proposition.**  For every class-B order-\(18\) instance and every subset
> \(C\) of its colours, the sequence (1) is graphic.

This proposition is an exact finite result, proved below by a relaxation and
an exhaustive Erdős--Gallai check.  It rules out all counterexamples detected
solely by the non-graphical degree sequence of the union of a colour
subfamily.  It does **not** prove that the individual prescribed matchings
can be chosen simultaneously.

## Proof

Put \(r=|C|\), and let \(b_v\) be the number of colours in \(C\) forbidden
at \(v\).  Then
\[
 d_C(v)=r-b_v.
\tag{2}
\]
The defining incidence constraints imply
\[
 \max(0,r-12)\leq b_v\leq\min(5,r).
\tag{3}
\]
Writing \(B=\sum_v b_v\), the selected \(r\) colour columns each have odd
sum in \(\{1,3,5\}\), while the other \(17-r\) columns do too.  Hence
\[
\begin{split}
  \max(r,5r-20)&\leq B\leq\min(5r,r+48),\\
  B&\equiv r\pmod2.
\end{split}
\tag{4}
\]
Indeed, the first lower and upper bounds in (4) come from the selected
columns.  The other two are the rearrangements of
\[
 17-r\leq65-B\leq5(17-r)
\]
for the unselected columns.

The verifier enumerates, for every \(0\leq r\leq17\), every nondecreasing
thirteen-term integer sequence \((b_v)\) satisfying (3)--(4).  This is a
relaxation: it includes every sequence induced by a class-B incidence
matrix, and may include sequences that no such matrix realizes.  For each
one it applies all thirteen Erdős--Gallai inequalities to the nonincreasing
sequence \((r-b_v)\), and independently runs the Havel--Hakimi reduction.
All \(18{,}032\) relaxed sequences pass both checks.  The handshake parity
condition holds automatically, since
\[
 \sum_v d_C(v)=13r-B\equiv r-B\equiv0\pmod2.
\]
By the Erdős--Gallai theorem, every sequence (2) in the relaxation is
graphic, and therefore so is every sequence arising from an actual class-B
instance. \(\square\)

## Why this does not finish the lift

For a single colour, its \(0/1\) degree sequence is realized by a matching.
Kundu's degree-packing theorem also shows that an aggregate graphic sequence
can be packed with one such \(0/1\) sequence when their sum is graphic.
Iterating that statement would require preserving decompositions already
chosen inside the aggregate realization; ordinary graphicality does not
supply that compatibility.  In fact, packing several prescribed degree
sequences is a strictly stronger problem.

The almost-regular specified-degree extension used in that comparison is:

* S. Kundu, *Generalizations of the \(k\)-factor theorem*,
  Discrete Mathematics 9 (1974), 173--179,
  [doi:10.1016/0012-365X(74)90147-2](https://doi.org/10.1016/0012-365X(74)90147-2).

Thus a target counterexample, if one exists, must be invisible to every
aggregate degree-sequence test in this proposition.  The surviving issue is
the colour-by-colour edge-disjoint realization.

No completion theorem and no resolution of Erdős--Rosenfeld Problem #835 is
claimed here.

## Verification

Run:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/first_lift_aggregate_graphicity/verify_aggregate_graphicity.py
```

The script is standard-library only and uses exact integer arithmetic.  Its
Erdős--Gallai and Havel--Hakimi implementations cross-check one another.
