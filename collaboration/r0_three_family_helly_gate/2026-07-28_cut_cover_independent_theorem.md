# An independent cut-cover theorem for the full \(r=0\) row model

Date: 2026-07-28.

## Verdict and exact scope

Let \(V\) have thirteen vertices.  Let \(D\) be the union of six pairwise
edge-disjoint prefix matchings of sizes
\[
4,4,4,5,5,5,
\]
so that
\[
|E(D)|=27,\qquad 1\le d_D(v)\le5.
\]
Assume that the eleven remaining complement rows are seven triples and four
five-sets and, counting row occurrences, satisfy
\[
\rho(v)=d_D(v)-1. \tag{1}
\]
For a triple row \(R\), put \(S_R=V\setminus R\), and put
\(G=K_{13}-D\).

> **Cut-cover theorem.**  After at most one support-preserving two-edge
> switch in one prefix matching, there are three of the seven triple-row
> occurrences such that
> \[
> \sum_{R}\max(0,|S_R\cap X|-5)\le e(G[X])
> \qquad\text{for every }X\subseteq V. \tag{C}
> \]

Here \(D\) and \(G\) in (C) mean the post-switch graphs when a switch is
used.  Equal rows are allowed and are still distinct occurrences.

This is a theorem about the necessary capacity cuts.  It does **not** prove
that the selected three supports have pairwise edge-disjoint perfect
matchings.  In particular, it does not close coordinated nine at \(r=0\)
and does not solve Erdős--Rosenfeld Problem #835.  The separate
cut-sufficiency/three-colour factor statement remains open.

The proof below does not use individual matchability, pairwise
compatibility, the pair gate, or an incompatibility graph.

## 1. Only cuts of sizes six, seven, and eight can bind

Because \(d_D(v)\le5\), the residual graph has \(\delta(G)\ge7\).  If
\(|X|=m\), then
\[
2e(G[X])
\ge 7m-m(13-m)=m(m-6). \tag{2}
\]
For one triple row \(R\), its demand at \(X\) is
\[
\max(0,m-5-|R\cap X|). \tag{3}
\]
It is zero for \(m\le5\).  For \(m\ge9\), (2) is at least
\(3(m-5)\), the maximum total demand of three rows.  Thus only
\(m=6,7,8\) need be considered.

All row families below are families of three-element subsets of the
seven **occurrence indices**.

### Six-sets

For a six-set \(U\), define
\[
A_U=\{R:R\cap U=\varnothing\},\qquad g_U=e(G[U]).
\]
The demand of a row is one precisely when it belongs to \(A_U\).
Therefore \(U\) obstructs a selected row triple exactly when
\[
|\{R\text{ selected}:R\in A_U\}|>g_U. \tag{4}
\]
Only \(g_U=0,1,2\) can obstruct.

### Seven-sets

For a seven-set \(Y\), define
\[
A_Y=\{R:R\cap Y=\varnothing\},\qquad
B_Y=\{R:|R\cap Y|=1\}.
\]
A row in \(A_Y\) has demand two, a row in \(B_Y\) has demand one, and
every other row has demand zero.  Equation (2) gives \(e(G[Y])\ge4\).
Consequently the only obstructions are
\[
\begin{array}{c|c}
e(G[Y])&\text{obstructing types}\\ \hline
4&AAA,\ AAB,\\
5&AAA.
\end{array} \tag{5}
\]

### Eight-sets

Equation (2) gives \(e(G[Q])\ge8\) for an eight-set \(Q\), while the
maximum total demand is nine.  Thus a violation requires
\[
e(G[Q])=8
\quad\text{and all three rows disjoint from }Q. \tag{6}
\]

No compatibility hypothesis was used in this catalogue.

## 2. Row budgets for seven- and eight-cuts

Let \(Y\) be a seven-set, \(Z=V\setminus Y\), and
\(c=e_D(Y,Z)\).  If \(g=e(G[Y])\), then \(e(D[Y])=21-g\), and (1)
gives
\[
\sum_{z\in Z}\rho(z)
=2e(D[Z])+c-6
=6+2g-c. \tag{7}
\]
If \(a=|A_Y|\) and \(b=|B_Y|\), the triple rows alone contribute
\(3a+2b\) on \(Z\).  Hence
\[
3a+2b\le6+2g-c. \tag{8}
\]
For \(g=4\), the family \(AAA\cup AAB\) therefore has size at most
\[
\binom a3+\binom a2b\le10. \tag{9}
\]
For \(g=5\), one has \(a\le5\), so the \(AAA\) family also has size at
most
\[
\binom53=10. \tag{10}
\]

If an eight-set \(Q\) satisfies (6), then \(e(D[Q])=20\).  Its internal
degree sum is forty, the maximum permitted by \(\Delta(D)\le5\).
Therefore every vertex of \(Q\) has \(D\)-degree five and
\[
e_D(Q,V\setminus Q)=0. \tag{11}
\]
Equation (1) gives total remaining-row incidence \(32\) on \(Q\).  The
four five-set rows contribute at most \(20\), so the seven triple rows
contribute at least \(12\).  If \(a\) triple rows avoid \(Q\), then
\[
3(7-a)\ge12,\qquad a\le3. \tag{12}
\]
Thus a tight eight-cut obstructs at most one row triple.

## 3. Dense cuts have a very small intersection pattern

The following elementary bound will be used repeatedly.  For sets
\(P,Q\) of orders \(p,q\), with \(k=|P\cap Q|\),
\[
e(D[P])+e(D[Q])
\le5k+\binom{p-k}{2}+\binom{q-k}{2}. \tag{13}
\]
Indeed, all terms incident with the intersection contribute at most
\(5k\), and the two remainder graphs contribute the two binomial terms.

### Critical six-sets

Every obstructing six-set has at least thirteen \(D\)-edges.  If two
distinct such six-sets intersect in \(k=1,\ldots,5\) vertices, (13)
would require
\[
26\le5k+2\binom{6-k}{2}.
\]
The right sides are
\[
25,22,21,22,25, \tag{14}
\]
all too small.  Hence distinct critical six-sets are disjoint, so there
are at most two.  Their \(A\)-sets are also disjoint, because the
complements of two disjoint six-sets meet in only one vertex.

Write \(g_i=e(G[U_i])\).  For two disjoint critical six-sets, their
internal edge sets are disjoint, so
\[
(15-g_1)+(15-g_2)\le27,\qquad g_1+g_2\ge3. \tag{15}
\]
Thus the only possible threshold pairs are \((1,2),(2,1),(2,2)\).
In particular, a \(g=0\) cut is the only critical six-cut.

### Critical seven-sets

There is at most one seven-set with at least sixteen \(D\)-edges.  For
two distinct such sets, (13) gives right sides
\[
35,30,27,26,27,30 \tag{16}
\]
for intersection orders \(1,\ldots,6\).  Orders two through six are
smaller than \(32\).  At intersection order one, the two internal edge
sets are disjoint and would use at least \(32>|E(D)|\) edges.

### Tight eight-sets

There is at most one tight eight-set.  If \(Q_1,Q_2\) were distinct,
choose \(w\in Q_2\setminus Q_1\).  By (11), all \(D\)-neighbours of
\(w\) would lie in the five-set \(V\setminus Q_1\), so
\(d_D(w)\le4\); but tightness of \(Q_2\) requires \(d_D(w)=5\).

Moreover, a tight eight-set coexists with no critical six- or seven-set.
Let \(Q\) be tight and put \(W=V\setminus Q\).  Then \(D[Q]\) is
5-regular, there are no \(Q\)-to-\(W\) edges, and \(e(D[W])=7\).
For a six-set \(U\), writing \(r=|U\cap Q|\), the elementary maxima for
\(e(D[U])\), for \(r=1,\ldots,6\), are at most
\[
10,7,6,7,10,11, \tag{17}
\]
all below thirteen.  For a seven-set \(Y\), \(r=|Y\cap Q|\ge2\), and
the corresponding maxima for \(r=2,\ldots,7\) are at most
\[
11,9,9,11,11,15, \tag{18}
\]
all below sixteen.  For \(r=6\), for example, deleting two vertices
from the 5-regular eight-vertex graph leaves at most
\(20-5-5+1=11\) edges.  The other entries follow from complete-graph
bounds on the two separated parts.

### A critical six-set versus a critical seven-set

Let \(U\) be a critical six-set with \(g_6=e(G[U])\in\{0,1,2\}\),
and let \(Y\) be a critical seven-set with
\(g_7=e(G[Y])\in\{4,5\}\).  Their internal \(D\)-edge counts sum to
\[
36-g_6-g_7. \tag{19}
\]
For intersection orders zero or one, the internal edge sets are
disjoint, and (19) is at least \(29>|E(D)|\).  For intersection orders
two through five, the right side of (13) is respectively
\[
26,24,24,26,
\]
again smaller than (19).  Hence coexistence requires \(U\subset Y\).
At intersection order six, (13) is at most \(30\), leaving exactly
\[
(g_6,g_7)=(1,5),(2,4),(2,5) \tag{20}
\]
as possibilities.

When \(U\subset Y\),
\[
A_Y\subseteq A_U\subseteq A_Y\cup B_Y. \tag{21}
\]
In particular, if \(g_6=1\), then necessarily \(g_7=5\), and every
seven-cut obstruction \(AAA\) is already a six-cut obstruction.

## 4. A fixed-prefix cut-cover lemma

For a critical six-set \(U\), put \(a=|A_U|\).  By (4), its obstruction
family covers all \(\binom73=35\) row triples exactly in the following
cases:
\[
\begin{array}{c|c|c}
g_U&\text{obstruction threshold}&\text{covers all triples iff}\\ \hline
0&\text{at least one row in }A_U&a\ge5,\\
1&\text{at least two rows in }A_U&a\ge6,\\
2&\text{all three rows in }A_U&a=7.
\end{array} \tag{22}
\]

> **Fixed-prefix lemma.**  If no single critical six-set satisfies the
> last column of (22), then some three row occurrences satisfy (C).

**Proof.**  A tight eight-cut, if present, is the only critical cut and
covers at most one triple, by (11)--(18).

Assume there is no tight eight-cut.  There is at most one critical
seven-cut, and its obstruction family has size at most ten by (9)--(10).
There are at most two critical six-cuts, and their \(A\)-sets are
disjoint.

If a \(g=0\) six-cut exists, it coexists with neither another critical
six-cut nor a critical seven-cut.  By (22), \(a\le4\); its obstruction
family has size
\[
35-\binom{7-a}{3}\le34. \tag{23}
\]

If a \(g=1\) six-cut exists, a second critical six-cut, if any, has
\(g=2\).  Let their disjoint \(A\)-set sizes be \(a_1,a_2\).
The hypothesis gives \(a_1\le5,a_2\le6\), and \(a_1+a_2\le7\).
Their obstruction families have total size at most
\[
\binom{a_1}{3}+\binom{a_1}{2}(7-a_1)+\binom{a_2}{3}\le30. \tag{24}
\]
Any coexisting critical seven-cut has \(g=5\), and (21) says its
obstruction family is already contained in that of the \(g=1\)
six-cut.

In the remaining case, every critical six-cut has \(g=2\).  Their
disjoint \(A\)-sets have sizes at most six and total size at most seven,
so together they cover at most
\[
\binom63=20 \tag{25}
\]
row triples.  Adding the at most ten triples covered by the unique
critical seven-cut still covers at most thirty.

Every case leaves at least one of the thirty-five row triples
unobstructed.  The small-cut catalogue then proves (C). \(\square\)

## 5. Removing the three all-cover branches

It remains to arrange, with at most one switch, that the hypothesis of
the fixed-prefix lemma holds.

For a six-set \(U\), let \(c=e_D(U,V\setminus U)\) and
\(g=e(G[U])\).  Summing (1) on \(V\setminus U\) gives the useful row
budget
\[
3|A_U|
\le \sum_{v\notin U}\rho(v)
=17+2g-c. \tag{26}
\]
Thus the three all-cover cases in (22) sharpen to
\[
(g,|A_U|)=(0,5),(1,6),(2,7). \tag{27}
\]

### The \(g=0\) branch

Here \(D[U]=K_6\).  Apply the support-preserving switch proved in
[`../r0_three_ten_obstruction/K6_PREFIX_SWITCH.md`](../r0_three_ten_obstruction/K6_PREFIX_SWITCH.md):
delete one prefix edge in \(U\) and one prefix edge outside \(U\), and
insert two crossing edges in that same prefix matching.  The switched
graph \(D'\) is \(K_6\)-free, so no \(g=0\) all-cover cut remains.

The old \(K_6\) becomes a \(K_6-e\) core \(C\) with exactly two
\(D'\)-edges leaving it.  It is the unique fourteen-edge six-set:
two distinct such sets cannot overlap by the calculation (14), and
cannot be disjoint because \(28>|E(D')|\).  Applying (26) to \(C\)
gives
\[
3|A_C|\le17+2-2=17,\qquad |A_C|\le5. \tag{28}
\]
Thus no \(g=1\) all-cover cut remains.

Nor can a \(g=2,\ |A_U|=7\) cut remain.  Equality in (26) would force
\[
e_{D'}(U,V\setminus U)=0,\quad
e(D'[U])=13,\quad e(D'[V\setminus U])=14. \tag{29}
\]
The \(K_6-e\) core \(C\) cannot straddle the two components in (29);
it cannot equal \(U\), which has only thirteen edges; and if
\(C\subset V\setminus U\), the two new switch edges would need their
two distinct outside endpoints to equal the unique vertex of
\((V\setminus U)\setminus C\).  That is impossible.  Therefore the
fixed-prefix lemma applies after this one switch.

### The \(g=1\) branch in a \(K_6\)-free prefix

Equation (26) shows that \(|A_U|=6\) exactly; here
\(D[U]=K_6-e\).  The solver-free equality-coordination theorem in
[`../r0_three_ten_obstruction/R0_EQUALITY_COORDINATION.md`](../r0_three_ten_obstruction/R0_EQUALITY_COORDINATION.md)
constructs one support-preserving two-edge trade and three pairwise
edge-disjoint perfect matchings: two supports from the six occurrences
in \(A_U\), and the seventh support.  These matchings imply (C).
Indeed, a perfect matching on \(S_R\) uses at least
\(\max(0,|S_R\cap X|-5)\) edges internally in \(X\); summing over three
edge-disjoint matchings gives (C).

### The \(g=2,\ |A_U|=7\) branch in a \(K_6\)-free prefix

The rigid all-seven-row repair proved in
[`../opus5_r0_orbit_repair/2026-07-28_cut_selection_audit.md`](../opus5_r0_orbit_repair/2026-07-28_cut_selection_audit.md)
uses one legal two-edge switch between an edge inside \(U\) and an edge
inside \(V\setminus U\).  Its direct twenty-case arithmetic verification
proves (C) after the switch for every three of the seven rows.

If the original prefix is \(K_6\)-free and none of these last two
branches occurs, the fixed-prefix lemma applies without a switch.  If it
contains a \(K_6\), the first branch uses the only switch and then the
fixed-prefix lemma applies.  This proves the theorem.

## 6. Verification and the remaining gap

Run:

```sh
python3 collaboration/r0_three_family_helly_gate/2026-07-28_cut_cover_independent_verify.py
```

The standard-library verifier checks:

1. the small-cut demand catalogue and all automatic cut sizes;
2. the six/six, seven/seven, six/seven, and tight-eight arithmetic;
3. the sharp seven- and eight-row budgets;
4. all-cover thresholds and the finite fixed-prefix family bounds; and
5. the post-\(K_6\)-switch row-budget calculation.

The separate restricted semantic-witness CEGIS, in which a repair was
limited to the identity or a single two-edge switch, reached 281 rounds,
58,800 semantic cuts, and 103,277 learned clauses in 300.105 seconds.
It found neither a counterexample nor a proof before the time limit.
That search is evidence only and is not used above.

The exact residual obligation is:

> Prove or refute that, under the full source model, three size-ten
> supports satisfying (C) necessarily admit three pairwise edge-disjoint
> perfect matchings (equivalently, the required prescribed
> three-colour \(b\)-factor).
