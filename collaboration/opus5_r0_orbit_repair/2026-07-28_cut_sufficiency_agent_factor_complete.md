# Factor existence under the full-row capacity cuts

Date: 2026-07-28.

## Theorem and exact scope

Let \(D,G,R_i,S_i\) satisfy the hypotheses of the full-row cut-sufficiency
problem, and put
\[
t(v)=|\{i:v\in R_i\}|,\qquad b(v)=3-t(v).
\]
If every internal-edge capacity cut
\[
\sum_{i=1}^3\max(0,|S_i\cap X|-5)\le e(G[X])           \tag{C}
\]
holds, then \(G\) contains a simple \(b\)-factor:
\[
\boxed{\quad H\subseteq G,\qquad d_H(v)=b(v)\quad(v\in V).\quad}
\]

This proves factor existence only.  It does not prove that \(H\) can be
chosen with the prescribed proper three-edge-colouring, and therefore does
not by itself prove full-row cut sufficiency.

## 1. Criterion and previously closed range

Let \(u(v)\) be the incidence of \(v\) in the other eight remaining rows.
Thus
\[
\rho(v)=t(v)+u(v),\qquad 0\le u(v)\le4,\qquad b(V)=30.
\]
For disjoint \(A,B\subseteq V\), let \(q(A,B)\) count the components \(C\)
of \(G-(A\cup B)\) for which
\[
b(C)+e_G(C,B)\quad\text{is odd}.
\]
The Tutte--Lovász criterion is
\[
\Delta(A,B):=
b(A)+\sum_{v\in B}d_{G-A}(v)-b(B)-q(A,B)\ge0.          \tag{1}
\]

The full row equation gives
\[
d_G(v)-b(v)=8-u(v),
\]
and hence the exact normalization
\[
\Delta(A,B)
=b(A)+8|B|-u(B)-e_G(A,B)-q(A,B).                       \tag{2}
\]
Equivalently,
\[
\Delta(A,B)
=b(A)-b(B)+2e(G[B])+e_G(B,C)-q(A,B),                  \tag{3}
\]
where \(C=V\setminus(A\cup B)\).

Every \(\Delta(A,B)\) is even.  Every component \(K\) of
\(G-(A\cup B)\) satisfies
\[
|K|\ge8-|A|-|B|                                        \tag{4}
\]
when the right side is positive, because \(\delta(G)\ge7\).

The preceding note
[`2026-07-28_cut_sufficiency_agent_factor_gate.md`](2026-07-28_cut_sufficiency_agent_factor_gate.md)
proves (1) whenever
\[
B=\varnothing,\qquad |A|\le4,
\]
and also when
\[
|A|=5,\qquad 1\le|B|\le4.                              \tag{5}
\]
It leaves first the rigid \((|A|,|B|,|C|)=(5,5,3)\) case.

## 2. Closing the rigid \(5+5+3\) case

The equality analysis in the preceding note shows that a negative witness
with sizes \(5,5,3\) would have all of the following properties:

\[
\begin{gathered}
b(A)=6,\qquad R_1,R_2,R_3\subseteq A,\\
u(v)=4,\quad d_D(v)=5,\quad e_D(v,A)=0
\qquad(v\in B),\\
G[C]\ \text{edgeless},\qquad q(A,B)=3.
\end{gathered}                                         \tag{6}
\]

Put \(m=e_D(B,C)\).  Since \(D[C]=K_3\), counted-singleton parity gives
\[
d_D(c,B)\in\{1,3\}\qquad(c\in C).                      \tag{7}
\]
The deleted-degree sum on \(B\) is
\[
25=2e(D[B])+m.                                         \tag{8}
\]
The cut \(B\cup C\) is an eight-set contained in all three selected
supports.  It therefore needs nine residual edges, which gives
\[
e(D[B\cup C])\le19.                                    \tag{9}
\]
Equations (7)--(9) leave exactly
\[
m\in\{5,7\}.                                           \tag{10}
\]

If \(m=5\), then (8) gives \(e(D[B])=10\), so \(D[B]=K_5\).  The three odd
positive degrees in (7) sum to five and hence are \(3,1,1\).  Choose
\(c\in C\) with \(d_D(c,B)=3\).  The six-set \(B\cup\{c\}\) has
\[
e(D[B\cup\{c\}])=10+3=13,
\]
so it has only two residual edges.  All three selected supports contain
this six-set, and (C) demands three residual edges, a contradiction.

If \(m=7\), then (8) gives \(e(D[B])=9\).  The degrees in (7) are
\(3,3,1\).  Choose the two vertices \(c_1,c_2\in C\) of \(B\)-degree
three.  Since \(D[C]=K_3\), the seven-set
\(B\cup\{c_1,c_2\}\) has
\[
e(D[B\cup\{c_1,c_2\}])=9+3+3+1=16.
\]
It therefore has five residual edges.  Again all three selected supports
contain the set, and now (C) demands six residual edges.  This is a
contradiction.

Thus the first surviving factor case is impossible.

## 3. Closing the three remaining \(|A|=5\) cases

The preceding gate closes \(|B|\le4\), and Section 2 closes
\((|A|,|B|,|C|)=(5,5,3)\).  The same crude bound remains equal to \(-2\)
for
\[
(5,6,2),\qquad(5,7,1),\qquad(5,8,0).                 \tag{A1}
\]
A negative witness must attain equality throughout the derivation in the
preceding gate.  Thus
\[
\begin{gathered}
b(A)=6,\qquad R_1,R_2,R_3\subseteq A,\\
d_D(v)=5,\qquad e_D(v,A)=0\quad(v\in B),\\
G[C]\text{ is edgeless, and every vertex of }C
\text{ is a counted singleton.}
\end{gathered}                                       \tag{A2}
\]

For \((5,8,0)\), the deleted-degree sum on \(B\) gives
\[
2e(D[B])=40,\qquad e(D[B])=20.
\]
All three selected rows avoid the eight-set \(B\), so (C) requires nine
residual edges, equivalently \(e(D[B])\le19\), a contradiction.

For \((5,7,1)\), put \(C=\{c\}\) and \(m=e_D(B,C)\).  The deleted-degree
sum on \(B\) is
\[
35=2e(D[B])+m.                                       \tag{A3}
\]
The all-avoiding seven-set cut on \(B\) requires
\(e(D[B])\le15\), so \(m\ge5\).  The all-avoiding eight-set cut on
\(B\cup C\) requires
\[
e(D[B])+m=\frac{35+m}{2}\le19,
\]
so \(m\le3\), a contradiction.

For \((5,6,2)\), write \(C=\{c_1,c_2\}\) and
\[
m_j=e_D(c_j,B),\qquad m=m_1+m_2.
\]
Since \(G[C]\) is edgeless, \(D[C]=K_2\).  Counted-singleton parity gives
\[
3+e_G(c_j,B)=3+6-m_j\equiv1\pmod2,
\]
so each \(m_j\) is even; the deleted-degree cap gives \(m_j\le4\).
The \(B\)-degree sum is
\[
30=2e(D[B])+m.                                       \tag{A4}
\]
The all-avoiding six-set cut on \(B\) gives \(e(D[B])\le12\), hence
\(m\ge6\).  The all-avoiding eight-set cut on \(B\cup C\) gives
\[
e(D[B])+m+1=16+\frac m2\le19,
\]
hence \(m\le6\).  Therefore \(m=6\) and
\(\{m_1,m_2\}=\{2,4\}\).  For the vertex \(c_j\) with \(m_j=4\), the
all-avoiding seven-set \(B\cup\{c_j\}\) has
\[
e(D[B\cup\{c_j\}])=12+4=16,
\]
but (C) requires at least six residual edges, equivalently at most
fifteen deleted edges.  This contradiction closes \(|A|=5\).

## 4. Reduction of every \(|A|\ge6\) witness to ten size triples

Assume \(B\ne\varnothing\), and write
\[
a=|A|,\qquad k=|B|,\qquad c=|C|=13-a-k.
\]
For
\[
p(v)=8-u(v)-e_G(v,A)
\]
one has
\[
p(v)\ge4-a,\qquad b(A)\ge3a-9,\qquad q(A,B)\le c.
\]
Consequently
\[
\Delta(A,B)
\ge4a-22+(5-a)k.                                      \tag{11}
\]
Because \(\Delta\) is even, every size pair for which the right side of
(11) is at least \(-1\) is already closed.

For \(a\ge6\), the complete list not closed by (11) is
\[
\begin{array}{c|c|c}
a&k&c\\ \hline
6&4,5,6,7&3,2,1,0\\
7&4,5,6&2,1,0\\
8&4,5&1,0\\
9&4&0 .
\end{array}                                            \tag{12}
\]
There are no further cases for \(a\ge10\).

## 5. The four cases with \(C=\varnothing\)

When \(C=\varnothing\), (3) is
\[
\Delta=30-2b(B)+2e(G[B]).                              \tag{13}
\]
For \(|B|\le5\), \(b(B)\le3|B|\le15\), so (13) is
nonnegative.  This closes \((a,k)=(8,5),(9,4)\).

For \((a,k)=(7,6)\), put
\[
r_i=|R_i\cap B|,\qquad t(B)=\sum_i r_i.
\]
Then \(b(B)=18-t(B)\), so
\[
\Delta=2\bigl(e(G[B])+t(B)-3\bigr).                    \tag{14}
\]
On the six-set \(B\), condition (C) demands one edge for every selected
row avoiding \(B\).  If \(z=|\{i:r_i=0\}|\), then
\[
e(G[B])\ge z,\qquad t(B)+z\ge3.
\]
Equation (14) is therefore nonnegative.

For \((a,k)=(6,7)\), (13) becomes
\[
\Delta=2\bigl(e(G[B])+t(B)-6\bigr).                    \tag{15}
\]
The seven-set cut gives
\[
e(G[B])\ge\sum_i\max(0,2-r_i).
\]
For each \(i\),
\[
r_i+\max(0,2-r_i)\ge2.
\]
Summing proves \(e(G[B])+t(B)\ge6\), so (15) is
nonnegative.

## 6. The six cases with \(C\ne\varnothing\)

Put
\[
r_B=t(B),\qquad r_C=t(C),\qquad r_U=r_B+r_C,
\qquad U=B\cup C.
\]
From (3) and \(b(X)=3|X|-t(X)\),
\[
\Delta
=30-6k-3c+2r_B+r_C+2e(G[B])+e_G(B,C)-q.                \tag{16}
\]

When \(a=6\), \(|U|=7\), and the cut condition gives
\[
e(G[U])\ge\sum_i\max(0,2-|R_i\cap U|),
\]
so
\[
r_U+e(G[U])\ge6.                                      \tag{17}
\]
When \(a=7\), \(|U|=6\), the analogous inequality is
\[
r_U+e(G[U])\ge3.                                      \tag{18}
\]

### Case \((a,k,c)=(6,4,3)\)

Writing \(e_C=e(G[C])\), equation (16) becomes
\[
\Delta
=-3+(r_B+e(G[B]))+(r_U+e(G[U]))-e_C-q.                 \tag{19}
\]
For a graph on three vertices,
\[
e_C+q\le4.
\]
Using (17) in (19) gives \(\Delta\ge-1\), and parity gives
\(\Delta\ge0\).

### Case \((a,k,c)=(6,6,1)\)

The six-set \(B\) also satisfies
\[
r_B+e(G[B])\ge3,                                      \tag{20}
\]
by the same avoiding-row argument used in (14).  Since \(e(G[C])=0\),
(16) rewrites as
\[
\Delta
=-9+(r_B+e(G[B]))+(r_U+e(G[U]))-q.
\]
Equations (17), (20), and \(q\le1\) give
\(\Delta\ge-1\), so parity closes the case.

### Case \((a,k,c)=(6,5,2)\)

For a two-vertex graph \(C\),
\[
e(G[C])+q\le2.
\]
Equation (16) can be written
\[
\Delta
=-6+(r_B+e(G[B]))+(r_U+e(G[U]))-e(G[C])-q.             \tag{21}
\]
By (17), a negative even value in (21) forces equality throughout:
\[
r_B=0,\qquad e(G[B])=0,\qquad
r_U+e(G[U])=6,\qquad e(G[C])+q=2.                      \tag{22}
\]

Write \(C=\{c_1,c_2\}\), let \(n_j\) be the number of selected rows
containing \(c_j\), and put \(m_j=d_D(c_j,B)\).
Since \(G[B]\) is edgeless, \(D[B]=K_5\); hence each vertex of \(B\) has
room for at most one further deleted edge and
\[
m_1+m_2\le5.                                          \tag{23}
\]
Equality in the seven-set cut in (22) gives
\[
m_1+m_2=4+e(G[C])+n_1+n_2.                            \tag{24}
\]
Thus the only possibilities are
\[
(e(G[C]),n_1+n_2,m_1+m_2)
\in\{(1,0,5),(0,0,4),(0,1,5)\}.                       \tag{25}
\]

Apply (C) to the six-set \(B\cup\{c_j\}\).  It gives
\[
5-m_j=e_G(B,c_j)\ge3-n_j,
\qquad\text{so}\qquad m_j\le2+n_j.                    \tag{26}
\]
The first line of (25) contradicts (26) after summing.

In the second line, both singleton components are counted and
\(b(c_j)=3\).  Thus \(3+5-m_j\) is odd, so both \(m_j\) are odd.
Together with (26), this gives \(m_1+m_2=2\), not four.

In the third line, relabel so that \((n_1,n_2)=(1,0)\).  Counted-singleton
parity gives \(m_1\) even and \(m_2\) odd.  Equation (26) then gives
\[
m_1\le2,\qquad m_2=1,
\]
contradicting \(m_1+m_2=5\).  This closes the case.

### Case \((a,k,c)=(7,4,2)\)

Equation (16) is
\[
\Delta=2r_B+r_C+2e(G[B])+e_G(B,C)-q.
\]
A negative even value forces \(q=2\) and every displayed nonnegative term
to vanish.  Then \(G[B\cup C]\) is an independent six-set, while all three
selected rows avoid it.  Condition (C) demands three internal edges, a
contradiction.

### Case \((a,k,c)=(7,5,1)\)

Here (16) rewrites as
\[
\Delta
=-3+(r_B+e(G[B]))+(r_U+e(G[U]))-q.
\]
Equation (18) and \(q\le1\) give \(\Delta\ge-1\), and parity closes the
case.

### Case \((a,k,c)=(8,4,1)\)

Equation (16) directly gives
\[
\Delta
=3+2r_B+r_C+2e(G[B])+e_G(B,C)-q\ge2,
\]
because \(q\le1\).

All ten triples in (12) are now eliminated.

## 7. Conclusion and remaining colouring gap

Every Tutte--Lovász inequality (1) holds, so the theorem supplies a simple
\(b\)-factor \(H\subseteq G\).

To finish full-row cut sufficiency one must still choose such a factor
with a prescribed proper three-edge-colouring.  Equivalently, after
identifying the colours with the nonzero elements of \(\mathbb F_2^2\),
one needs a nowhere-zero solution
\[
x:E(H)\longrightarrow\mathbb F_2^2\setminus\{0\},\qquad
\sum_{e\ni v}x(e)=\sum_{i:v\in S_i}i.
\]
The factor theorem above proves neither the component-evenness conditions
for a suitable \(H\) nor the exclusion of zero labels.  Those are now the
earliest exact gaps; factor existence itself is closed.
