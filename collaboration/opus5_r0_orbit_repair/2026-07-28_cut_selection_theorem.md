# The \(r=0\) cut-feasible repair-selection theorem

Date: 2026-07-28.

## Theorem and exact scope

Let \(D\) be the union of six pairwise edge-disjoint matchings of sizes
\[
4,4,4,5,5,5
\]
on a thirteen-vertex set \(V\). Assume
\[
|E(D)|=27,\qquad 1\le d_D(v)\le5,
\]
and let the eleven remaining complement rows consist of seven triples and
four five-sets satisfying
\[
\rho(v)=d_D(v)-1. \tag{1}
\]
Put \(G=K_{13}-D\), and write \(S_R=V\setminus R\) for the size-ten
support complementary to a remaining triple row.

> **Cut-feasible repair-selection theorem.** After at most one
> support-preserving two-edge switch in one prefix layer, there are three
> of the seven remaining triple-row occurrences such that
> \[
> \sum_{i=1}^3\max(0,|S_{R_i}\cap X|-5)\le e(G[X])
> \qquad(X\subseteq V). \tag{C}
> \]

When a switch is used, \(D\) and \(G=K_{13}-D\) in (C) denote the
post-switch prefix union and residual graph.

Repeated rows are allowed throughout.

This proves the repair-selection lemma isolated in
`2026-07-28_cut_selection_audit.md`. It does **not** prove that (C) is
sufficient for three pairwise edge-disjoint perfect matchings. That separate
cut-sufficiency statement remains open.

## 1. Preprocessing and the repair count

The prefix-switch theorem in
[`../r0_three_ten_obstruction/K6_PREFIX_SWITCH.md`](../r0_three_ten_obstruction/K6_PREFIX_SWITCH.md)
has the following consequence. After at most one support-preserving
two-edge switch:

1. \(D\) is \(K_6\)-free;
2. all seven remaining size-ten supports are individually matchable; and
3. every vertex degree and every row in (1) is unchanged.

If the original \(D\) is already \(K_6\)-free, this preprocessing uses no
switch. We will use a switch later only in that zero-cost branch.

The incompatibility theorem in
[`../r0_three_ten_obstruction/R0_INCOMPATIBILITY_GRAPH.md`](../r0_three_ten_obstruction/R0_INCOMPATIBILITY_GRAPH.md)
then says that the graph \(I\) on the seven row occurrences, joining two
rows when their supports do not have edge-disjoint perfect matchings, is
\[
I=K_t\mathbin{\dot\cup}(7-t)K_1,\qquad 0\le t\le6. \tag{2}
\]
The clique comes from a unique \(K_6-e\) core in \(D\). The possible
\(K_{5,5}-e\) forced-edge core does not certify an incompatible pair.
When \(t=6\), the equality-coordination theorem in
[`../r0_three_ten_obstruction/R0_EQUALITY_COORDINATION.md`](../r0_three_ten_obstruction/R0_EQUALITY_COORDINATION.md)
already constructs three simultaneous matchings using the one permitted
switch, so (C) follows.

This cannot consume a second switch after nontrivial \(K_6\)
preprocessing. The preprocessing trade removes one edge of the saturated
core \(C\) and adds two \(C\)-to-\((V\setminus C)\) edges. Thus the
resulting \(K_6-e\) core has
\[
a=e_D(C,V\setminus C)=2.
\]
The full-row incidence bound for a \(K_6-e\) core, proved in the cited
incompatibility theorem, gives
\[
t\le\left\lfloor\frac{19-a}{3}\right\rfloor=5.
\]
That core is unique, so \(t=6\) can occur only when preprocessing used no
switch. Hence below we may assume
\[
t\le5. \tag{3}
\]
An independent three-set of \(I\) is individually and pairwise compatible,
so the audited small-cut classification applies to it.

## 2. The complete small-cut catalogue

The degree bound gives \(\delta(G)\ge7\). The audited reduction in
`2026-07-28_cut_selection_audit.md` shows that, for an individually and
pairwise compatible triple, only the following genuinely three-way
violations of (C) are possible:

1. a six-set \(U\) with \(e(D[U])=13\), where all three rows lie in
   \[
   A_U=\{R:R\subseteq V\setminus U\};
   \]
2. a seven-set \(Y\) with \(e(D[Y])=17\), where either all three rows lie
   in \(A_Y\), or two lie in \(A_Y\) and the third lies in
   \[
   B_Y=\{R:|R\cap Y|=1\};
   \]
3. a seven-set \(Y\) with \(e(D[Y])=16\), where all three rows lie in
   \(A_Y\); or
4. a tight eight-set, whose complementary five-set contains all three
   rows.

Cuts of all other sizes, and all other incidence patterns on sizes six,
seven, and eight, are automatic.

The row equation (1) gives the sharp occurrence bounds
\[
|A_U|\le7,\qquad
|A_Y|\le4\ (e(D[Y])=17),\qquad
|A_Y|\le5\ (e(D[Y])=16), \tag{4}
\]
and at most three rows can lie in the complementary five-set of a tight
eight-cut.

## 3. The two large dense-six branches

Suppose first that a six-set \(U\) with \(e(D[U])=13\) has
\(|A_U|=7\). The rigid repair theorem proved in
`2026-07-28_cut_selection_audit.md` switches one prefix edge inside \(U\)
and one inside \(V\setminus U\) to two crossing edges. Its twenty-case
arithmetic check proves (C) for every three of the seven triple rows after
that switch.

This case cannot consume a second switch after nontrivial \(K_6\)
preprocessing. Indeed, the full row equations in the \(|A_U|=7\) case
force
\[
e_D(U,V\setminus U)=0,\quad e(D[U])=13,\quad
e(D[V\setminus U])=14. \tag{5}
\]
Suppose a saturated \(K_6\) on \(C\) had first been switched by deleting
one edge inside \(C\), deleting one edge inside \(V\setminus C\), and
adding two \(C\)-to-\((V\setminus C)\) edges. The switched graph retains
a \(K_6-e\) on \(C\). If \(C\) met both sides of (5), that \(K_6-e\)
would retain a crossing edge. If \(C=U\), it would put fourteen edges in
\(D[U]\). If \(C\subset V\setminus U\), both new switch edges would have
to end at the unique vertex of \((V\setminus U)\setminus C\) in order
not to cross (5), which is impossible for two disjoint new edges. Thus
the \(|A_U|=7\) branch can occur only when preprocessing used no switch.

Suppose next that \(|A_U|=6\), and call the seventh row \(R_p\). The
dense-cut overlap theorem in
[`../r0_three_family_helly_gate/2026-07-28_dense_cut_overlap_audit.md`](../r0_three_family_helly_gate/2026-07-28_dense_cut_overlap_audit.md)
proves:

1. two distinct thirteen-edge six-sets are disjoint and have disjoint
   \(A\)-sets;
2. every sixteen- or seventeen-edge seven-set contains \(U\);
3. the full row equation excludes the seventeen-edge case; and
4. a sixteen-edge seven-set cannot obstruct a triple
   \(\{R_p,R_x,R_y\}\) with \(R_x,R_y\in A_U\).

The same audit uses the certified pair gate to show that no incompatible
pair can coexist with this dense six-set. Hence all fifteen choices of
\(\{R_x,R_y\}\) are pairwise compatible with \(R_p\). Dense six- and
seven-cuts cover none of them. The edge and degree ledgers in the same
audit also show that a twenty-edge eight-set cannot coexist with a
thirteen-edge six-set. Consequently all fifteen choices satisfy (C),
without an additional switch.

We may now assume that every thirteen-edge six-set satisfies
\[
|A_U|\le5. \tag{6}
\]

## 4. How many obstruction cuts can coexist?

### Dense six-sets

Two distinct thirteen-edge six-sets are disjoint, by the overlap theorem.
There are therefore at most two. Their \(A\)-sets are disjoint. Under
(6), if their sizes are \(a,b\), then
\[
a,b\le5,\qquad a+b\le7.
\]
The total number of row triples covered by every dense six-cut is at most
\[
\binom a3+\binom b3\le10. \tag{7}
\]
The same bound includes the case of only one dense six-set.

### Binding seven-sets

There is at most one seven-set with sixteen or seventeen internal
\(D\)-edges. To prove this, let \(Y_1,Y_2\) be distinct seven-sets, put
\(k=|Y_1\cap Y_2|\), and suppose each has at least sixteen internal
edges. The terms incident with their intersection contribute at most
\(5k\), while the two disjoint remainders contribute at most
\(2\binom{7-k}{2}\). Thus
\[
32\le5k+2\binom{7-k}{2}. \tag{8}
\]
Since two seven-sets in a thirteen-set have \(k\ge1\), the right side for
\(k=1,\ldots,6\) is
\[
35,30,27,26,27,30.
\]
Only \(k=1\) survives this numerical bound, but then the two internal edge
sets are disjoint and already use at least \(32>|E(D)|\) edges. This is
impossible.

For the unique binding seven-set, a sixteen-edge cut covers at most
\[
\binom53=10 \tag{9}
\]
row triples. A seventeen-edge cut has disjoint occurrence sets \(A_Y,B_Y\)
with \(|A_Y|\le4\), and covers
\[
\binom{|A_Y|}{3}+
\binom{|A_Y|}{2}|B_Y|
\le \binom43+\binom42\cdot3=22. \tag{10}
\]

### Tight eight-sets

A tight eight-set \(X\) has \(e(G[X])=8\), hence \(e(D[X])=20\).
Every vertex of \(X\) is saturated at \(D\)-degree five, so \(D\) has no
edge from \(X\) to its complementary five-set. Two such eight-sets cannot
be distinct: a vertex in \(X_1\setminus X_2\) would have degree five but
would be confined to the four other vertices outside \(X_2\). Thus there
is at most one tight eight-cut.

Its complementary five-set \(W\) has seven \(D\)-edges, and
\[
\sum_{w\in W}\rho(w)=2\cdot7-5=9.
\]
At most three triple-row occurrences can be contained in \(W\), so the
tight cut covers at most one row triple. \(\tag{11}\)

## 5. Selection when no incompatibility core exists

If the incompatibility graph \(I\) is empty, all \(35\) triples are
individually and pairwise compatible. Equations (7), (10), and (11) show
that all possible obstruction cuts together cover at most
\[
10+22+1=33<35 \tag{12}
\]
row triples. Hence some triple satisfies every cut (C).

This union bound intentionally ignores overlaps between obstruction
families; it is therefore safe.

## 6. Selection in the \(K_t\) incompatibility branch

Suppose \(I\) has the nonempty clique \(Q\) of order \(t\le5\), arising
from a unique six-set \(C\) with
\[
D[C]=K_6-e,\qquad e(D[C])=14. \tag{13}
\]

No thirteen-edge dense six-set can coexist with (13). If such a set \(U\)
existed and \(k=|U\cap C|\), the degree calculation would give
\[
27\le5k+2\binom{6-k}{2}. \tag{14}
\]
For \(1\le k\le5\), the right side is at most \(25\); \(k=6\) is
incompatible with the two different internal edge counts. For \(k=0\),
the thirteen and fourteen internal edges exhaust \(D\), leaving the
thirteenth vertex with degree zero. Every case is impossible.

A seventeen-edge seven-set \(Y\) is also impossible. With
\(k=|C\cap Y|\),
\[
31\le5k+\binom{6-k}{2}+\binom{7-k}{2}. \tag{15}
\]
The right side for \(k=1,\ldots,6\) is at most \(30\), while \(k=0\)
would make the two internal edge sets disjoint and use \(31>27\) edges.

If \(e(D[Y])=16\), the analogous inequality has \(30\) on the left.
The cases \(k=0,1\) again contradict \(|E(D)|=27\), and the cases
\(2\le k\le5\) have right side below \(30\). Therefore \(k=6\):
\[
C\subset Y. \tag{16}
\]
It follows that \(A_Y\subseteq Q\), because every row avoiding \(Y\)
also avoids \(C\). A sixteen-edge seven-cut covers only triples wholly
inside \(A_Y\), and those contain at least two clique vertices. It
therefore covers no independent triple of \(I\).

There are
\[
\binom73-\binom t2(7-t)-\binom t3 \tag{17}
\]
independent triples in \(K_t\mathbin{\dot\cup}(7-t)K_1\). For
\(t=1,\ldots,5\), these counts are
\[
35,30,22,13,5. \tag{18}
\]
Dense six-cuts and seventeen-edge seven-cuts are absent, while the only
possible sixteen-edge seven-cut covers no independent triple. The unique
tight eight-cut covers at most one. Hence at least four independent
triples remain cut-feasible even in the worst case \(t=5\).

This proves (C) in every case and completes the theorem.

## 7. Verification and remaining obligation

The finite arithmetic in (7)--(10), (15), and (17)--(18) is reproduced by
`verify_cut_selection_counting.py`.

The theorem is solver-free apart from its already-certified pair-gate
dependency. The separate semantic-witness CEGIS independently searched the
same universal repair-selection statement and found no counterexample, but
that computational evidence is not used in this proof.

The exact remaining local obligation is:

> prove that, under the full row equations (1), a triple of size-ten
> supports satisfying (C) has three pairwise edge-disjoint perfect
> matchings.

Until that cut-sufficiency theorem is proved or independently certified by
an exact exhaustive search, coordinated nine at \(r=0\) and Problem #835
remain open.
