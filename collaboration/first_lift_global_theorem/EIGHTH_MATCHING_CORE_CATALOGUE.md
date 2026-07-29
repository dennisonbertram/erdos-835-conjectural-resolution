# Exact obstruction cores at the eighth matching

Date: 2026-07-27.

## Result and scope

Let \(F\) be the union of seven already selected support matchings in a
target \(n=13,q=17\) class-B instance, and let
\[
 H=K_{13}-F.
\]
This note classifies the complete multipartite cores that \(F\) must contain
if a remaining support of size ten or twelve has no perfect matching in
\(H\).

It is a reduction for a switching proof, not yet an eighth-colour packing
theorem.  Supports of size eight are deliberately not classified here:
after seven deletions their residual minimum degree may be zero, whereas
every target profile still has a remaining support of size ten or twelve.

## Prefix constraints

Every vertex belongs to twelve of all seventeen supports.  Only ten colours
remain, so every vertex belongs to at least two selected supports.  Since a
selected matching saturates its support,
\[
 2\le d_F(v)\le7. \tag{1}
\]
The possible seven-prefix profiles used by the seven-colour theorem have
the following edge totals:
\[
\begin{array}{c|c|c}
r&\text{selected support sizes}&|E(F)|\\ \hline
0&8^4\,10^3&31\\
1&8^4\,10^2\,12&32\\
2,3,4&8^4\,10\,12^2&33\\
5&8^4\,12^3&34.
\end{array} \tag{2}
\]
In particular, \(|E(F)|\le34\), \(\Delta(F)\le7\), and
\[
 |E(F[X])|\le7\left\lfloor |X|/2\right\rfloor
 \quad\text{for every }X. \tag{3}
\]

## Coarsened Tutte barriers

Let \(V\) be a remaining support of even size \(n\in\{10,12\}\), and suppose
\(H[V]\) has no perfect matching.  Tutte's theorem gives
\(S\subseteq V\), with \(s=|S|\), such that \(H[V]-S\) has more than \(s\)
odd components.  Parity makes their number at least \(s+2\).

Absorb every even component into an odd component.  If more than \(s+2\)
odd blocks remain, repeatedly merge three odd blocks into one.  We obtain
exactly \(s+2\) odd blocks partitioning \(V\setminus S\), with no
\(H\)-edge between distinct blocks.  Therefore \(F\) contains every edge
between distinct blocks.

If one block has order \(b\), each of its vertices has
\(n-s-b\) forced \(F\)-neighbours in the other blocks.  By
\(\Delta(F)\le7\),
\[
 b\ge n-s-7. \tag{4}
\]
The odd integer partitions satisfying (4) give the complete list below.

## Size-ten catalogue

For \(n=10\), the seven possible block-size patterns and their forced core
edge counts are
\[
\begin{array}{c|c|c|c|c|c}
s&\text{odd blocks}&\text{core}&|E(\text{core})|
   &\text{pointwise ceiling}&r=0\text{ ceiling}\\ \hline
0&3+7&K_{3,7}&21&5&2\\
0&5+5&K_{5,5}&25&7&1\\
1&3+3+3&K_{3,3,3}&27&6&0\\
2&5+1+1+1&K_{5,1,1,1}&18&5&4\\
2&3+3+1+1&K_{3,3,1,1}&22&5&2\\
3&3+1+1+1+1&K_{3,1,1,1,1}&18&6&4\\
4&1+1+1+1+1+1&K_6&15&7&6.
\end{array} \tag{5}
\]
Here \(K_{a_1,\ldots,a_k}\) denotes the complete multipartite graph with
those part sizes.

## Size-twelve catalogue

For \(n=12\), the numerical patterns are
\[
\begin{array}{c|c|c|c|c}
s&\text{odd blocks}&\text{core}&|E(\text{core})|
   &\text{reuse ceiling}\\ \hline
0&5+7&K_{5,7}&35&5\\
4&3+1+1+1+1+1&K_{3,1,1,1,1,1}&25&5\\
5&1+1+1+1+1+1+1&K_7&21&6.
\end{array} \tag{6}
\]
The first row cannot occur in a target seven-prefix because its forced
35-edge core exceeds the global bound \(|E(F)|\le34\) in (2).  Thus a
blocked size-twelve support forces only
\[
 K_{3,1,1,1,1,1}=K_8-E(K_3)
 \quad\text{or}\quad K_7. \tag{7}
\]

## Why the reuse ceilings hold

Suppose a fixed core \(J\subseteq F\) has maximum degree \(\Delta(J)\), and
let \(v\) be a core vertex of that degree.  The residual-degree identity is
\[
 d_H(v)=12-d_F(v).
\]
It is also the number of remaining supports containing \(v\).  Since
\(d_F(v)\ge\Delta(J)\), at most \(12-\Delta(J)\) remaining supports can
contain the whole core.  This gives the final columns of (5) and (6).

Consequently, one obstruction core cannot be invoked without limit.  For
example, a fixed \(K_{3,7}\) can obstruct at most five remaining supports,
a fixed \(K_{3,3,3}\) at most six, and a fixed \(K_6\) at most seven.  A
switching proof can therefore focus on how distinct cores overlap inside a
31-to-34-edge graph satisfying (1)--(3).

## Exact complement-degree reuse in the exceptional profile

For \(r=0\), seven size-ten and three size-eight supports remain.  Suppose a
fixed core \(J\), on a vertex set \(C\), is contained in \(t\) of the seven
size-ten supports.

Take complements inside the thirteen-vertex set.  The seven size-ten
supports give seven triples, and the three size-eight supports give three
five-sets.  A vertex \(v\) is omitted by exactly five of all seventeen
colours.  It is omitted by \(7-d_F(v)\) selected colours, so among these ten
remaining complement sets it occurs exactly
\[
 5-(7-d_F(v))=d_F(v)-2 \tag{8}
\]
times.

Every size-ten support containing \(C\) has its complement triple wholly in
\(O=V(K_{13})\setminus C\).  Thus the \(t\) blocked supports consume \(3t\)
complement incidences in \(O\).  Since \(\sum_vd_F(v)=62\) and
\(\sum_{v\in C}d_F(v)\ge2|E(J)|\),
\[
\begin{aligned}
3t
 &\le \sum_{v\in O}(d_F(v)-2)\\
 &\le 62-2|E(J)|-2(13-|C|)\\
 &=36+2|C|-2|E(J)|. \tag{9}
\end{aligned}
\]
There is a further simple-graph correction.  Of the
\(31-|E(J)|\) edges of \(F\) outside \(J\), at most
\(\binom{13-|C|}{2}\) lie wholly outside \(C\).  Therefore at least
\[
 r_J=\max\left\{0,\,
 31-|E(J)|-\binom{13-|C|}{2}\right\} \tag{10}
\]
touch \(C\) and contribute at least \(r_J\) more to
\(\sum_{v\in C}d_F(v)\).  Thus (9) sharpens to
\[
 3t\le36+2|C|-2|E(J)|-r_J. \tag{11}
\]
The final column of (5) is
\[
 \left\lfloor
 \frac{36+2|C|-2|E(J)|-r_J}{3}
 \right\rfloor,
 \tag{12}
\]
intersected with the pointwise ceiling.

In particular, a \(K_{3,3,3}\) core cannot obstruct even one actual
remaining support; a fixed \(K_{5,5}\) obstructs at most one; a fixed
\(K_{3,7}\) or \(K_{3,3,1,1}\) obstructs at most two; and no fixed core
obstructs all seven.  Therefore, if all seven large
supports were blocked after a seven-prefix, \(F\) would have to contain at
least two distinct obstruction cores.  This reduces the exceptional profile
to an overlap-or-switching problem.

### Equality exclusion for \(K_6\)

In a hypothetical obstruction of all seven size-ten supports, the \(K_6\)
ceiling in (5) improves from six to five.  Suppose a \(K_6\) on \(C\) were
reused six times, and put \(O=V(K_{13})\setminus C\).  Then equality holds
throughout the uncorrected bound (9):
\[
 3\cdot6=18=36+2\cdot6-2\cdot15.
\]
Consequently \(\sum_{v\in C}d_F(v)=30\).  Every vertex of \(C\) already has
degree five in the clique, so there is no \(F\)-edge from \(C\) to \(O\).
The six complement triples in \(O\) consume all eighteen available
complement incidences there.  The seventh triple and all three remaining
five-set complements therefore lie inside \(C\).

The seventh size-ten support contains all seven vertices of \(O\) but only
three vertices of \(C\).  Its obstruction core is connected and has at
least six vertices.  Since \(F\) has no \(C\)-to-\(O\) edge, that core must
lie wholly in \(O\).  The graph \(F[O]\) has
\[
 31-\binom62=16
\]
edges.  Of the seven core types in (5), only \(K_6\), with fifteen edges,
fits on at most seven vertices and within this edge budget.  But after
placing that clique, the one remaining edge gives the seventh vertex of
\(O\) degree at most one, contradicting \(\delta(F)\ge2\).

Thus a fixed \(K_6\) can account for at most five of the seven supports in a
total-obstruction argument.

### Three more equality exclusions

The same complement accounting, followed by a direct matching construction,
sharpens three other ceilings in a total-obstruction argument.

#### The \(K_{5,1,1,1}\) ceiling is three

Write the core vertex set as \(C=L\mathbin{\dot\cup}S\), where
\((|L|,|S|)=(5,3)\), and put \(O=V(K_{13})\setminus C\).  The vertices of
\(S\) already have core degree seven.  Classify the thirteen noncore edges
of \(F\) as
\[
 a=|E_F(L,O)|,\qquad b=|E_F(L)|,\qquad c=|E_F(O)|.
\]
Then
\[
 a+b+c=13,\qquad c\le10. \tag{13}
\]
The total complement capacity in \(O\) is
\[
 \sum_{v\in O}(d_F(v)-2)=2c+a-10.
\]
If four complement triples lay in \(O\), this quantity would be at least
twelve.  Substituting (13) gives \(a+2b\le4\).  Together with \(c\le10\),
the only possibilities for \((c,a,b)\) are
\[
 (10,3,0),\qquad(10,2,1),\qquad(9,4,0). \tag{14}
\]
Thus the four triples consume twelve of at most thirteen complement
incidences in \(O\).  At least two of the other three large complement
triples lie wholly in \(C\).

For either such triple \(T\), its support is \(O\mathbin{\dot\cup}R\), where
\(|O|=|R|=5\) and \(R=C\setminus T\).  Between \(O\) and \(R\), the residual
graph contains \(K_{5,5}\) minus at most \(a\le4\) edges.  Deleting fewer
than five edges from \(K_{5,5}\) cannot destroy all perfect matchings:
a Hall-deficient \(k\)-set would require deleting at least
\(k(6-k)\ge5\) edges.  Hence this support has a perfect matching, a
contradiction.  A fixed \(K_{5,1,1,1}\) can therefore be reused at most
three times.

#### The \(K_{3,3,1,1}\) ceiling is one

Here \(|C|=8\), \(|E(J)|=22\), and \(|O|=5\).  Let \(a,b,c\) count,
respectively, noncore edges crossing from \(O\) to \(C\), lying inside
\(C\), and lying inside \(O\).  Then
\[
 a+b+c=9,\qquad
 \sum_{v\in O}(d_F(v)-2)=2c+a-10=8-a-2b.
\]
If two blocked supports reused the core, the last expression would be at
least six, so \(a+2b\le2\).  After their two triples consume six
incidences, at most two \(O\)-incidences remain.  At least one of the other
five large complement triples lies wholly in \(C\).  Its support splits as
two five-sets \(O\) and \(R=C\setminus T\), and the residual graph contains
\(K_{5,5}\) between them minus at most \(a\le2\) edges.  It has a perfect
matching, again a contradiction.  Thus the reuse ceiling is one.

#### The \(K_{3,1,1,1,1}\) ceiling is three

Now \(|C|=7\), \(|E(J)|=18\), and \(|O|=6\).  With the same notation,
\[
 a+b+c=13,\qquad
 \sum_{v\in O}(d_F(v)-2)=2c+a-12=14-a-2b.
\]
Four reused triples would force \(a+2b\le2\), hence \(a\le2\).  They leave
at most two complement incidences in \(O\), so at least one of the other
three large triples \(T\) lies wholly in \(C\).

The support of \(T\) is \(O\mathbin{\dot\cup}R\), with
\((|O|,|R|)=(6,4)\).  Moreover
\[
 |E(H[O])|=\binom62-c=2+a+b\ge2.
\]
Choose one residual edge inside \(O\).  The four unused vertices of \(O\)
and the four vertices of \(R\) span \(K_{4,4}\) minus at most \(a\le2\)
edges in \(H\), so they have a perfect matching.  Together with the chosen
edge this is a perfect matching of the support, a contradiction.  The
reuse ceiling is three.

Combining these arguments with (12) and the \(K_6\) equality exclusion, the
ceilings for a hypothetical obstruction of all seven size-ten supports are
\[
 (2,1,0,3,1,3,5) \tag{15}
\]
for the core types in the order displayed in (5).

### The \(K_{3,7}\) ceiling is one

It remains to exclude equality in the first entry of (15).  Write a
\(K_{3,7}\) core as \(K_{A,B}\), where \((|A|,|B|)=(3,7)\), and let \(O\)
be the three outside vertices.  The vertices of \(A\) already have degree
seven in the core.  For the ten noncore edges of \(F\), put
\[
 a=|E_F(B,O)|,\qquad b=|E_F(B)|,\qquad c=|E_F(O)|.
\]
If the core were reused twice, its two complement triples would both equal
\(O\).  Hence
\[
 a+b+c=10,\qquad c\le3,\qquad 2c+a-6\ge6.
\]
The only possibilities are
\[
 (c,a,b)=(3,7,0),\quad(2,8,0),\quad(3,6,1). \tag{16}
\]
The two triples consume six of at most seven complement incidences in
\(O\), so at least four of the other five large complement triples lie
wholly in \(A\cup B\).

Fix any such triple \(T\), put
\[
 R=(A\cup B)\setminus T,\qquad
 \alpha=|R\cap A|,\quad \beta=|R\cap B|=7-\alpha.
\]
The residual graph has every \(O\)-to-\(A\) edge, and its graph on
\(R\cap B\) is a clique minus at most the one edge counted by \(b\).
It is enough to find a matching of size \(3-\alpha\) from \(O\) into
\(R\cap B\): match the other \(\alpha\) vertices of \(O\) to \(R\cap A\).
Exactly four vertices of \(R\cap B\) remain, and their \(K_4\) minus at most
one edge has a perfect matching.

The required cross matching always exists:

* If \(\alpha=0\), the bipartite graph from \(O\) to \(B\) has at least
  \(21-a\ge13\) edges.  Every vertex of \(O\) has a residual neighbour:
  (16) and \(\Delta(F)\le7\) allow at most six deleted \(O\)-to-\(B\)
  edges at any one vertex.  If its maximum matching had size at most two,
  König's theorem would give a vertex cover of size two.  Two \(O\)-vertices
  cannot cover because the third has a neighbour; one vertex from each side
  covers at most nine edges; and two \(B\)-vertices cover at most six.
* If \(\alpha=1\), the \(3\)-by-\(6\) graph has at least
  \(18-a\ge10\) edges.  A bipartite graph with matching number at most one
  has a one-vertex cover and therefore at most six edges.
* If \(\alpha=2\), the \(3\)-by-\(5\) graph has at least
  \(15-a\ge7\) edges, so it has the required one edge.
* If \(\alpha=3\), no edge into \(B\) is required.

Thus every one of those at least four supports has a perfect matching,
contradicting total blockage.  A fixed \(K_{3,7}\) can be reused at most
once, and the total-obstruction ceiling vector improves to
\[
 (1,1,0,3,1,3,5). \tag{17}
\]

## Remaining frontier

To prove an eighth-colour theorem it now suffices to show that the cores
needed to obstruct every remaining size-ten and size-twelve support cannot
coexist, or that a selected matching can be switched to destroy a surviving
core without creating another one.  The residual-degree identity alone
cannot provide that repair, as the minimal two-colour certificate in
`PROPAGATION_COUNTEREXAMPLE.md` shows.

`verify_eighth_matching_core_catalogue.py` exhausts the odd integer
partitions, checks every displayed edge count and reuse ceiling, and checks
the target profile totals.
