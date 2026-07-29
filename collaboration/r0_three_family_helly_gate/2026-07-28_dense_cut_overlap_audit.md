# Dense-cut overlap audit for the full \(r=0\) row setting

Date: 2026-07-28.

## Verdict

Let \(D\) be the union of the six prefix matchings in the full \(r=0\)
setting. Thus
\[
|E(D)|=27,\qquad \Delta(D)\le 5,
\]
and the seven remaining triple rows together with the four remaining
five-set rows satisfy
\[
\rho(v)=d_D(v)-1. \tag{1}
\]

The proposed overlap statements are true, with a stronger conclusion:

> **Dense-six overlap theorem.** If \(U_1,U_2\) are six-sets with
> \(e(D[U_1])=e(D[U_2])=13\), then either \(U_1=U_2\) or
> \(U_1\cap U_2=\varnothing\).

Consequently, for distinct dense six-sets, the occurrence sets
\[
A_U=\{R\text{ among the seven triple rows}:R\subseteq V\setminus U\}
\]
are disjoint.

There is also a rigid six-versus-seven conclusion:

> **Dense-six/binding-seven theorem.** If \(|U|=6\),
> \(e(D[U])=13\), and \(|Y|=7\) with
> \(e(D[Y])\in\{16,17\}\), then \(U\subset Y\). There is at most one such
> seven-set \(Y\).

In the branch \(|A_U|=6\), writing \(R_p\) for the seventh triple-row
occurrence, the \(17\)-edge seven-set is impossible. A \(16\)-edge
seven-set cannot violate the positive capacity inequality for any triple
\(\{R_p,R_x,R_y\}\) with \(R_x,R_y\in A_U\).

These are cut-covering statements. They do not prove that a chosen triple
has three edge-disjoint perfect matchings; cut sufficiency remains a
separate conjecture. In the standard preprocessed setting in which all seven
size-ten supports are individually live and \(D\) is \(K_6\)-free, however,
the certified pair gate and the full-row incompatibility theorem imply that
all seven rows are pairwise compatible. A tight eight-cut cannot coexist
with the dense six-cut, so all fifteen candidates
\(\{R_p,R_x,R_y\}\) satisfy every capacity cut. Thus
the \(|A_U|=6\) branch of cut-feasible selection is closed.

## 1. Exact assumptions

The two dense-six conclusions use only the displayed parameters
\[
|V|=13,\quad |E(D)|=27,\quad \Delta(D)\le5.
\]
The fact that \(D\) is a union of six matching layers is not used in their
proofs.

The special \(|A_U|=6\) conclusion additionally uses the complete
remaining-row equation (1), the inventory of seven triples and four
five-sets, and the fact that rows are occurrences: repeated underlying sets
are allowed and are counted with multiplicity.

For a remaining triple row \(R\), put \(S_R=V\setminus R\). For any cut
\(X\subseteq V\), the positive internal-edge demand of that row is
\[
\phi_X(R)^+=\max(0,|S_R\cap X|-5)
             =\max(0,|X|-|R\cap X|-5). \tag{2}
\]
A selected triple of rows violates the positive capacity inequality at
\(X\) exactly when the sum of (2) is greater than \(e(G[X])\), where
\(G=K_{13}-D\).

## 2. Two dense six-sets

Let \(U_1,U_2\) be six-sets and put
\[
C=U_1\cap U_2,\quad
P=U_1\setminus U_2,\quad
Q=U_2\setminus U_1,\quad
k=|C|.
\]
Then \(|P|=|Q|=6-k\).

In the sum
\[
e(D[U_1])+e(D[U_2])=26, \tag{3}
\]
the terms involving at least one vertex of \(C\) are
\[
2e(D[C])+e_D(C,P)+e_D(C,Q). \tag{4}
\]
Expression (4) is the sum, over \(c\in C\), of the number of
\(D\)-neighbours of \(c\) in \(U_1\cup U_2\). Hence
\[
2e(D[C])+e_D(C,P)+e_D(C,Q)\le5k. \tag{5}
\]
The remaining terms in (3) are \(e(D[P])+e(D[Q])\), so
\[
e(D[P])+e(D[Q])
\le 2\binom{6-k}{2}. \tag{6}
\]
Combining (3)--(6) gives the necessary inequality
\[
26\le 5k+2\binom{6-k}{2}. \tag{7}
\]
For \(k=1,2,3,4,5\), the right side of (7) is respectively
\[
25,\quad22,\quad21,\quad22,\quad25. \tag{8}
\]
Every value is less than \(26\). Therefore two dense six-sets are either
equal (\(k=6\)) or disjoint (\(k=0\)). In particular, intersections of
orders three, four, and five are impossible, as proposed; intersections of
orders one and two are impossible as well.

If \(U_1,U_2\) are distinct, they are disjoint and leave one vertex
\(z\) outside their union. Thus
\[
(V\setminus U_1)\cap(V\setminus U_2)=\{z\}. \tag{9}
\]
No three-set is contained in the singleton (9). Therefore no triple-row
occurrence belongs to both \(A_{U_1}\) and \(A_{U_2}\), proving
\[
A_{U_1}\cap A_{U_2}=\varnothing. \tag{10}
\]
This remains true when equal triple rows occur with multiplicity.

## 3. A dense six-set and a binding seven-set

Let \(|U|=6\), \(e(D[U])=13\), \(|Y|=7\), and
\[
e(D[Y])=s\in\{16,17\}.
\]
Put \(k=|U\cap Y|\). Repeating the preceding degree calculation with
parts of orders \(6-k\) and \(7-k\) gives
\[
13+s
\le 5k+\binom{6-k}{2}+\binom{7-k}{2}. \tag{11}
\]
For \(k=0,1,\ldots,6\), the right side is
\[
36,\quad30,\quad26,\quad24,\quad24,\quad26,\quad30. \tag{12}
\]
Since \(13+s\) is \(29\) or \(30\), equation (11) excludes
\[
k=2,3,4,5. \tag{13}
\]

If \(k=0\), the edge sets \(E(D[U])\) and \(E(D[Y])\) are disjoint and
already contain \(13+s\ge29\) edges, contradicting \(|E(D)|=27\). If
\(k=1\), an edge internal to both sets would need both endpoints in the
one-vertex intersection, so the two internal edge sets are again disjoint
and give the same contradiction. Hence
\[
k=6,\qquad U\subset Y. \tag{14}
\]

Write \(Y=U\cup\{w\}\), where \(w\in V\setminus U\). Then
\[
e(D[Y])=13+d_D(w,U), \tag{15}
\]
so \(d_D(w,U)=3\) for \(s=16\) and \(d_D(w,U)=4\) for \(s=17\).

The internal degree sum of \(D[U]\) is \(26\). Since the six vertices of
\(U\) have total \(D\)-degree at most \(30\),
\[
c:=e_D(U,V\setminus U)\le4. \tag{16}
\]
Two distinct vertices outside \(U\) cannot each have at least three
\(D\)-neighbours in \(U\), because that would make \(c\ge6\).
Consequently at most one seven-set with \(16\) or \(17\) internal
\(D\)-edges can coexist with the fixed dense six-set.

Moreover,
\[
A_Y
=\{R\in A_U:w\notin R\}
\subseteq A_U. \tag{17}
\]

## 4. The \(|A_U|=6\) branch

Assume now that six of the seven triple-row occurrences lie in
\(A_U\), and call the remaining occurrence \(R_p\). Put
\[
r=|R_p\cap U|.
\]
Since \(R_p\notin A_U\),
\[
1\le r\le3. \tag{18}
\]

Summing the full row equation (1) on \(U\) gives
\[
\sum_{u\in U}\rho(u)
=2e(D[U])+c-|U|
=20+c. \tag{19}
\]
The six rows in \(A_U\) contribute zero to (19), \(R_p\) contributes
\(r\), and the four five-set rows contribute at most \(20\). Therefore
\[
20+c\le20+r,\qquad c\le r\le3. \tag{20}
\]

By (15), a \(17\)-edge seven-set containing \(U\) would require four
crossing edges from one outside vertex into \(U\). This contradicts
\(c\le3\). Thus:
\[
\boxed{\text{No seven-set }Y\supset U\text{ has }e(D[Y])=17.} \tag{21}
\]

If \(e(D[Y])=16\), then
\[
e(G[Y])=\binom72-16=5. \tag{22}
\]
For a triple row \(R\), (2) on the seven-set \(Y\) is
\[
\phi_Y(R)^+=\max(0,2-|R\cap Y|)\le2. \tag{23}
\]
Three rows have total demand greater than five only when all three terms in
(23) equal two, equivalently when all three rows belong to \(A_Y\).
But (17) gives \(A_Y\subseteq A_U\), while \(R_p\notin A_U\). Hence no
triple
\[
\{R_p,R_x,R_y\},\qquad R_x,R_y\in A_U, \tag{24}
\]
is obstructed by a \(16\)-edge seven-set.

For completeness, without the special bound (20), a \(17\)-edge seven-set
has \(e(G[Y])=4\). A triple of the form (24) can then violate the cut only
if
\[
R_x,R_y\in A_Y,\qquad |R_p\cap Y|=1. \tag{25}
\]
Equation (21) shows that this nominal covering pattern is absent in the
\(|A_U|=6\) branch.

## 5. Consequences for covering the pairs \(\{x,y\}\)

The audited single-cut classification in
[`../opus5_r0_orbit_repair/2026-07-28_cut_selection_audit.md`](../opus5_r0_orbit_repair/2026-07-28_cut_selection_audit.md)
says that, under individual and pairwise compatibility, a genuinely
three-way positive capacity violation can come only from:

1. a six-set with \(e(G[X])=2\), equivalently \(e(D[X])=13\);
2. a seven-set with \(e(D[X])=16\) or \(17\); or
3. a tight eight-set, for which all three selected rows lie in its
   \(A\)-set of size at most three.

For the candidates (24):

- the original dense six-set \(U\) does not obstruct them because
  \(R_p\notin A_U\);
- any other dense six-set \(U'\) has
  \(A_{U'}\cap A_U=\varnothing\) by (10), hence
  \(|A_{U'}|\le1\) because six of the seven row occurrences lie in
  \(A_U\);
- no binding seven-set obstructs them, by (21)--(23).

A tight eight-set cannot coexist with \(U\). If \(X\) were such a set,
then \(|X|=8\) and \(e(D[X])=20\). Put \(k=|U\cap X|\). Since
\(|U|+|X|=14\), one has \(k\ge1\). The edge ledger
\[
e(D[U])+e(D[X])-|E(D)|=6
\]
forces \(\binom{k}{2}\ge6\), hence \(k\ge4\). The degree-cap calculation
on the intersection gives
\[
5k\ge33-\binom{6-k}{2}-\binom{8-k}{2}.
\]
For \(k=4,5,6\), the right side is respectively \(26,30,32\), while
the left side is \(20,25,30\). Every case is impossible.

It remains to justify compatibility. Work in the standard preprocessed
setting of
[`../r0_three_ten_obstruction/R0_INCOMPATIBILITY_GRAPH.md`](../r0_three_ten_obstruction/R0_INCOMPATIBILITY_GRAPH.md):
all seven size-ten supports are individually live, \(D\) is \(K_6\)-free,
and \(1\le d_D(v)\le5\) for every vertex. The certified pair gate and the
full-row incompatibility theorem say that an incompatible pair would force
a six-set \(C\) with
\[
e(D[C])=14. \tag{26}
\]
The alternative \(K_{5,5}-e\) forced-edge core cannot certify an
incompatible pair under the full row inventory.

Put \(k=|U\cap C|\). The same degree calculation as in (7), now using
\(e(D[U])+e(D[C])=27\), gives
\[
27\le5k+2\binom{6-k}{2}. \tag{27}
\]
For \(1\le k\le5\), the right side has the five values in (8), all at most
25. The case \(k=6\) is impossible because the same induced graph cannot
have both thirteen and fourteen edges. Hence \(k=0\).

But then the thirteen edges of \(D[U]\) and fourteen edges of \(D[C]\)
are disjoint and exhaust all \(27\) edges of \(D\). The unique vertex
outside the two disjoint six-sets has \(D\)-degree zero, contradicting the
preprocessed bound \(d_D(v)\ge1\). Therefore no \(K_6-e\) forced-edge core
exists, and the incompatibility graph is empty.

All fifteen pairs \(\{x,y\}\) are consequently individually and pairwise
compatible with \(R_p\). Dense six- and seven-sets cover none of them,
and no tight eight-set can coexist. Thus all
\[
15 \tag{28}
\]
of the triples
\[
\{R_p,R_x,R_y\},\qquad R_x,R_y\in A_U,
\]
satisfy every internal-edge capacity cut.

This closes the \(|A_U|=6\) branch of the cut-feasible selection problem
after the already-audited individual-blocker preprocessing. It remains only
a cut-feasibility theorem: converting one of these fifteen choices into
three edge-disjoint perfect matchings still requires the separate cut
sufficiency theorem or an exact matching certificate.

## 6. Arithmetic check

The two finite right-side tables used above are independently reproduced by

```sh
python3 -c 'from math import comb; print([5*k+2*comb(6-k,2) for k in range(1,6)]); print([5*k+comb(6-k,2)+comb(7-k,2) for k in range(7)])'
```

with output

```text
[25, 22, 21, 22, 25]
[36, 30, 26, 24, 24, 26, 30]
```
