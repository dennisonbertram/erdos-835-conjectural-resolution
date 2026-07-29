# A K6-free mixed dead prefix, repaired by one further trade

Date: 2026-07-28.

## Exact result

There is a valid \(r=0\) class-B support instance and a packed
complement-cover six-prefix of profile \(10^3\,8^3\) such that

1. its edge union \(D\) has \(\Delta(D)=5\) and contains no \(K_6\);
2. all four remaining size-eight supports are blocked;
3. all seven remaining size-ten supports are individually matchable; but
4. no three of the eleven remaining colours admit pairwise edge-disjoint
   perfect matchings.

This proves that the \(K_6\)-removal switch in `K6_PREFIX_SWITCH.md` is
not, by itself, a mixed-support coordinated-nine theorem.  In the
six-fold common-forced-edge equality case, a remaining size-eight colour
need not break the collision: all four can be individually dead.

The example is nevertheless repaired by one further support-preserving
two-edge trade.  After that trade, three remaining size-ten colours have
explicit pairwise edge-disjoint perfect matchings.  Thus the certificate
does not refute a theorem that is allowed an additional core-breaking
trade, and it does not refute coordinated nine.

## The prefix

Let
\[
 C=\{c_0,\ldots,c_5\},\qquad O=\{o_0,\ldots,o_6\}.
\]
In the following table, the middle column uses \(c\)-labels and the last
column uses \(o\)-labels.

\[
\begin{array}{c|c|c}
 &E(C)&E(O)\\ \hline
M_0&14,\ 23&45,\ 23,\ 06\\
M_1&04,\ 35,\ 12&46,\ 25\\
M_2&03,\ 24,\ 15&26,\ 34\\
M_3&02,\ 45&56,\ 24\\
M_4&25,\ 34&35,\ 14\\
M_5&05,\ 13&36,\ 15
\end{array} \tag{1}
\]

These are pairwise edge-disjoint matchings of sizes
\(5,5,5,4,4,4\).  Their complements are
\[
\begin{aligned}
&\{c_0,c_5,o_1\},\quad
  \{o_0,o_1,o_3\},\quad
  \{o_0,o_1,o_5\},\\
&\{c_1,c_3,o_0,o_1,o_3\},\\
&\{c_0,c_1,o_0,o_2,o_6\},\\
&\{c_2,c_4,o_0,o_2,o_4\}.
\end{aligned} \tag{2}
\]
They cover all thirteen vertices.

Inside \(C\), the selected edges are
\[
 E(K_C)\setminus\{c_0c_1\}. \tag{3}
\]
There is no selected edge between \(C\) and \(O\).  If
\[
 H=K_{13}-D,
\]
then the edges of \(H[O]\) are
\[
 01,\ 02,\ 03,\ 04,\ 05,\ 12,\ 13,\ 16. \tag{4}
\]
Thus every edge of \(H[O]\) meets \(\{o_0,o_1\}\), and
\[
 \nu(H[O])=2. \tag{5}
\]

The \(D\)-degrees on \(C\) are \(4,4,5,5,5,5\), and those on \(O\)
are \(1,2,4,4,5,5,5\).  Hence \(\Delta(D)=5\).  The six-vertex
component on \(C\) is \(K_6-c_0c_1\), not \(K_6\); the component on
\(O\) has only thirteen edges.  Therefore \(D\) is \(K_6\)-free.

## The remaining complements

Use the four five-set complements
\[
 C\setminus\{c_0\},\quad C\setminus\{c_1\},\quad
 C\setminus\{c_2\},\quad C\setminus\{c_3\}. \tag{6}
\]
Use the six triple complements inside \(O\)
\[
 234,\quad245,\quad256,\quad346,\quad356,\quad456, \tag{7}
\]
and the final triple
\[
 \{c_2,c_3,o_1\}. \tag{8}
\]
Together with (2), these are seven distinct five-sets and ten distinct
triples.  Every vertex occurs in exactly five complements, so the
seventeen supports have profile \(8^7\,10^{10}\), with every vertex in
exactly twelve supports.  This is a valid \(r=0\) class-B instance.

## Why the prefix is dead

Every remaining size-eight support in (6) has the form
\[
 O\cup\{c_i\}\qquad(0\le i\le3). \tag{9}
\]
A perfect matching on it would match \(c_i\) to one vertex of \(O\),
then use three independent edges of \(H[O]\) on the other six vertices.
This contradicts (5).  Thus all four size-eight supports are blocked.

Put
\[
 e=c_0c_1.
\]
For any triple \(T\) in (7), the complementary support is
\(C\cup(O\setminus T)\).  Since
\[
 H[C]=\{e\},\qquad H[C,O]=K_{6,7}, \tag{10}
\]
every perfect matching on that support contains \(e\).  Conversely,
after using \(e\), any bijection between
\(C\setminus\{c_0,c_1\}\) and \(O\setminus T\) works.  Each of these
six supports therefore has exactly \(24\) perfect matchings, all sharing
\(e\).

The support complementary to (8) has \(96\) residual perfect matchings.
For example:
\[
 o_0o_2,\quad c_0o_3,\quad c_1o_4,\quad c_4o_5,\quad c_5o_6. \tag{11}
\]
Thus all seven size-ten supports are live.  But any three of them contain
two from the six families in (7), whose matchings collide on \(e\).
Since the four size-eight families are empty, no three of the eleven
remaining colours pack.

## One further trade repairs the equality case

In the selected layer \(M_0\), replace
\[
 c_1c_4,\ o_0o_6
 \quad\longmapsto\quad
 c_1o_6,\ c_4o_0. \tag{12}
\]
The four endpoints are distinct, both new edges were unselected, and the
support of \(M_0\) is unchanged.  The trade preserves all vertex degrees,
the complement cover, and pairwise edge-disjointness of the six selected
layers.

After (12), take the supports complementary to \(234\), \(245\), and
\(\{c_2,c_3,o_1\}\).  The following residual perfect matchings are
pairwise edge-disjoint:
\[
\begin{aligned}
&c_0c_1,\ c_2o_0,\ c_3o_1,\ c_4o_5,\ c_5o_6,\\
&c_0o_0,\ c_1c_4,\ c_2o_1,\ c_3o_6,\ c_5o_3,\\
&c_0o_2,\ c_1o_3,\ c_4o_4,\ c_5o_5,\ o_0o_6.
\end{aligned} \tag{13}
\]
The trade frees a second edge \(c_1c_4\) inside the almost-clique
\(C\).  The first two matchings in (13) can therefore use different
internal \(C\)-edges instead of sharing \(e\).

## Structural meaning of the equality case

The arithmetic behind this example is forced.  Suppose a \(K_6\)-free
six-prefix contains \(K_6-e\) on a six-set \(U\), and six of the seven
remaining triple complements avoid \(U\).  Let \(a\) be the number of
selected edges from the two endpoints of \(e\) to \(V\setminus U\), and
let \(r\) be the number of vertices of \(U\) in the seventh triple.
The four non-endpoints of \(e\) have \(D\)-degree five, while its
endpoints have total degree \(4+a_x,4+a_y\).  The remaining-complement
identity therefore requires the four five-sets to supply
\[
 22+a-r \tag{14}
\]
incidences on \(U\).  Their total capacity is twenty, so
\[
 r\ge2+a. \tag{15}
\]
As \(r\le3\), the only possibilities are
\[
 (a,r)=(0,2),\ (0,3),\ (1,3). \tag{16}
\]
In the first case all four five-sets lie inside \(U\); in the third case
the same is true, while in the middle case exactly three do and the
fourth has four vertices in \(U\).  The displayed certificate realizes
\((a,r)=(0,2)\).

This explains why the size-eight escape can disappear exactly at the
six-fold forced-edge boundary.

There is nevertheless a universal trade at this boundary.

> **Equality-core trade lemma.**  In any of the three cases (16), some
> selected layer admits a support-preserving two-edge trade that replaces
> one edge of \(K_6-e\) and one edge outside \(U\) by two cross-edges.
> After the trade, \(D\) is still \(K_6\)-free, and every one of the six
> formerly \(e\)-forced size-ten supports has a residual perfect matching
> using \(e\) and another using the newly freed core edge.  In particular,
> the trade simultaneously destroys the common forced edge in all six
> families.

Indeed, the fourteen selected edges of \(K_6-e\) meet at least five of
the six selected layers, since a matching contains at most three of them.
There are
\[
 27-14-a=13-a\ge12 \tag{17}
\]
selected edges inside the outside seven-set, so those edges meet at least
four layers.  Some layer therefore contains both a core edge \(uv\) and
an outside edge \(pq\).  At most one old cross-edge exists.  Of the two
re-pairings
\[
 \{up,vq\},\qquad\{uq,vp\}, \tag{18}
\]
at least one consists of unused edges; use it to replace \(uv,pq\).

The new union has at most \(a+2\le3\) cross-edges.  It has no \(K_6\):
the graph on \(U\) is now \(K_6-\{e,uv\}\), the graph outside \(U\)
has only \(12-a<15\) edges, and a mixed \(K_6\) would require at least
five cross-edges.

Finally, let \(Q\) be the four outside vertices in any one of the six
formerly forced supports.  After using either freed core edge \(e\) or
\(uv\), it remains to match four core vertices bijectively to \(Q\).
The relevant \(K_{4,4}\) has at most three missing cross-edges, so it has
a perfect matching.  (A Hall obstruction in \(K_{4,4}\) requires at
least four deleted edges.)  This proves the lemma.

The lemma strictly advances the equality case, but it does not yet
coordinate three colours: it gives two alternative internal edges to six
matching families, while a simultaneous choice must still avoid all
cross-edge collisions and accommodate the seventh size-ten support.  The
remaining universal task is to prove that this core-breaking trade always
coordinates two of the six families with the seventh, or to find a
trade-resistant equality configuration.  The explicit trade (12) and
matchings (13) prove that the displayed extremal certificate is repaired.

## Verification

Run:

```sh
python3 collaboration/r0_three_ten_obstruction/verify_k6_free_mixed_dead_prefix.py
```

The standard-library verifier reconstructs all data, checks that the
seventeen complements are distinct and have the class-B row and column
sums, verifies the prefix cover and the exact residual graph (4),
enumerates all perfect matchings on the eleven remaining supports, and
checks that none of the \(165\) support triples packs.  It also checks
the equality cases (16), the layer-count overlap, and the four-edge Hall
threshold used in the equality-core trade lemma.  It then performs (12),
rechecks the prefix invariants, obtains matching counts
\[
 0,0,0,0,42,42,42,42,42,42,96,
\]
and verifies the three-match extension (13).
