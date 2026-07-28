# Reduction and a sharp pair obstruction for profile \(r=1\)

Date: 2026-07-28.

## Scope

In the class-B profile
\[
(n_8,n_{10},n_{12})=(8,8,1),
\]
start with the complement-cover six-prefix of type
\[
8^4\,10^2.
\]
Let \(D\) be its union and put
\[
H=K_{13}-D.
\]
The selected complements cover all thirteen vertices, so
\[
|E(D)|=26,\qquad \Delta(D)\le5,\qquad \delta(H)\ge7. \tag{1}
\]

This note proves three reductions.

1. A size-ten support is blocked immediately after the six-prefix if and
   only if it contains a unique possible saturated \(K_6\).
2. It gives the exact Tutte catalogues for the two natural orders
   \[
   D\to M_{10}\to M_{10}\to M_{12}
   \quad\text{and}\quad
   D\to M_{10}\to M_{12}\to M_{10}. \tag{2}
   \]
3. It gives a literal class-B certificate showing that two individually
   matchable size-ten supports need not admit edge-disjoint matchings,
   even when (1) holds.

Thus an arbitrary mixed-support theorem is false.  A proof of a coordinated
ninth matching must choose the two triples, or switch the six-prefix, using
the full six-triple inventory.  No ninth-matching theorem is claimed here.

## Complement-row identities

For a vertex \(v\), let \(\sigma(v)\) count selected complements and let
\(\rho(v)\) count the eleven remaining complements.  Since every class-B
row has sum five and every selected matching saturates its support,
\[
d_D(v)=6-\sigma(v),\qquad
\rho(v)=5-\sigma(v)=d_D(v)-1. \tag{3}
\]
The remaining complements consist of four five-sets, six triples, and one
singleton, of total incidence
\[
4\cdot5+6\cdot3+1=39. \tag{4}
\]

After one size-ten matching \(M\) has been selected, put \(E=D\cup M\).
Then
\[
|E(E)|=31,\qquad
\rho_7(v)=d_E(v)-2, \tag{5}
\]
where \(\rho_7\) counts the four five-sets, five triples, and singleton
remaining after seven colours.

After subsequently selecting the size-twelve matching \(N\), put
\(F=D\cup M\cup N\).  Then
\[
|E(F)|=37,\qquad
\rho_8(v)=d_F(v)-3. \tag{6}
\]

## Exact obstruction after the six-prefix

Let \(Y\) be an unused size-ten support.  The graph \(H[Y]\) has minimum
degree at least four.  If it has no perfect matching, coarsen a Tutte
barrier with separator \(S\), \(|S|=s\), to exactly \(s+2\) odd blocks.
All edges between distinct blocks lie in \(D\).  The bound
\(\Delta(D)\le5\) leaves only
\[
K_{5,5}\quad\text{or}\quad K_6. \tag{7}
\]

The first core is impossible.  If \(D\) contained a \(K_{5,5}\), all ten
core vertices would have \(D\)-degree five.  By (3), the remaining
complements would have to supply
\[
10(5-1)=40
\]
incidences on the core, more than their total capacity \(39\) in (4).

Consequently:

> **Six-prefix obstruction lemma.** An unused size-ten support \(Y\) is
> blocked after the complement-cover six-prefix if and only if \(D[Y]\)
> contains a \(K_6\).

The converse is immediate: if \(Y=C\mathbin{\dot\cup}Q\), where
\(|C|=6\), \(|Q|=4\), and \(D[C]=K_6\), then a matching in \(H[Y]\) can
match at most four vertices of \(C\) outside \(C\), leaving two unmatched.

There is at most one such \(K_6\) in \(D\).  For two distinct six-sets
with intersection \(k\), if \(k\le3\), their two cliques use at least
\[
30-\binom32=27>26
\]
edges.  If \(k=4\) or \(5\), a common vertex has degree respectively seven
or six in their union, contrary to \(\Delta(D)\le5\).

Finally, this unique \(K_6\), if present, blocks at most five of the six
remaining size-ten supports.  If all six triple complements avoided its
vertex set \(C\), then (3) would require \(6\cdot4=24\) remaining
complement incidences on \(C\).  The four remaining five-sets and the
singleton have total capacity only \(21\).  Hence at least one size-ten
support extends, recovering the seventh step of the coordinated
eight-packing proof with a sharper description of every failure.

### Switching away the initial \(K_6\)

The unique saturated \(K_6\), when present, can be destroyed without
changing any selected support.  Put \(C=V(K_6)\) and
\(O=V(K_{13})\setminus C\).  Since every vertex of \(C\) already has
\(D\)-degree five, no selected edge joins \(C\) to \(O\).

Choose a selected colour having an edge \(uv\) in \(C\).  The same colour
has an edge \(ab\) in \(O\): its support has order at least eight, and its
vertices in \(C\) and \(O\) must be matched separately, with at least two
support vertices in \(O\).  Replace
\[
uv,\ ab\longmapsto ua,\ vb. \tag{7a}
\]
Both new edges were outside \(D\), and the colour remains a perfect
matching on the same support.  Degrees in the six-prefix are unchanged.

The switched union contains no \(K_6\).  Any new \(K_6\) would have to use
one of the two new cross edges.  But the endpoint \(u\), for example, now
has \(D\)-neighbourhood
\[
(C\setminus\{u,v\})\cup\{a\},
\]
while \(a\) has no selected edge to any vertex of
\(C\setminus\{u,v\}\).  These six vertices therefore do not form a
clique, and the same argument applies to \(vb\).  The \(K_{5,5}\) branch
remains impossible by (3)--(4).  Thus after at most one switch, all six
remaining size-ten supports are individually matchable.

### Forced edges in an individual support

Let \(G=H[Y]\), \(|Y|=10\), so \(\delta(G)\ge4\), and suppose an edge
\(e\) belongs to every perfect matching of \(G\).  Apply Tutte to
\(G-e\).  The same component count as above has only two genuine equality
families.

* With no separator, \(G-e\) has two components of order five.  On the
  deletion side, \(D[Y]\) contains \(K_{5,5}-e\).
* With a separator \(Q\) of order four, \(G-e-Q\) has six singleton
  components \(U\).  On the deletion side,
  \[
  D[U]=K_6-e. \tag{7b}
  \]
  Equivalently, on the graph side \(G[U]=\{e\}\); the four non-endpoints
  of \(e\) are complete to \(Q\), each endpoint has at least three
  neighbours in \(Q\), and \(G[Q]\) is unrestricted.

The nominal separator-one \(3+3+3\) and separator-three
\(3+1+1+1+1\) rows cannot occur after deleting a single edge.  They have,
respectively, nine and four vertices whose internal-plus-separator degree
is only three, while the single deleted edge can supply the missing
incidence at at most two vertices.

The first forced-edge family is incompatible with the class-B rows.
In a \(K_{5,5}-e\), the eight non-endpoints already have \(D\)-degree
five, while the two endpoints have degree at least four.  Equation (3)
therefore requires at least
\[
8\cdot4+2\cdot3=38
\]
remaining-complement incidences on \(Y\).  The triple
\(V\setminus Y\) itself supplies another three incidences outside \(Y\),
exceeding the total \(39\) in (4).

Hence every forced edge in a remaining support comes from a
\(K_6-e\) deletion core.  Two such cores can coexist in \(D\) only on
the same six-set.  To see this, let their six-sets meet in \(k\) vertices.
If \(k\le2\), their union has at least
\[
14+14-\binom k2\ge27
\]
edges.  If \(3\le k\le5\), take the first core's \(k-2\) or more common
vertices that are not endpoints of its missing edge.  They already have
\(D\)-degree five and hence have no selected neighbour outside the first
six-set.  The second \(K_6\)-minus-edge core would require all but at most
one of the
\[
(k-2)(6-k)\ge3
\]
edges from those vertices to its new vertices, a contradiction.  On the
same six-set, two different missing edges unite to a full \(K_6\).

After switch (7a), there is consequently at most one forced-edge core,
with one missing edge \(e\).  It can make \(e\) forced only in supports
whose triple complements avoid its six-set \(U\), and there are at most
five of those.  If all six triples avoided \(U\), (3) would require at
least
\[
4\cdot4+2\cdot3=22
\]
incidences on \(U\) from the four remaining five-sets and singleton,
whose total capacity is \(21\).

This leaves a sharply isolated selectable-pair gate:

> **Cross-family gate.** If two individually matchable size-ten support
> graphs admit no edge-disjoint pair of perfect matchings, must they share
> an edge forced in both graphs?

The three literal obstructions below all have precisely this form, but a
proof of the gate is not supplied here.  If the gate holds, switch (7a)
and the \(22>21\) count immediately prove that some two of the six
size-ten supports pack: at least one support has no forced edge, so it is
compatible with every other support.

## First order: two size-ten matchings before the size-twelve matching

Choose an extendable size-ten support \(Y_0\) and a perfect matching
\[
M\subseteq H[Y_0].
\]
For another size-ten support \(Y\), put \(G=H[Y]\).  Then
\(\delta(G)\ge4\), and \(M\cap E(G)\) is a matching.  If
\[
G-M
\]
has no perfect matching, a vertex in an odd component of order \(c\) after
deleting a Tutte separator of order \(s\) has at most
\[
(c-1)+s+1=c+s
\]
neighbours in \(G\).  Thus \(c\ge4-s\).  The exact coarsened odd-block
catalogue is
\[
K_{5,5},\quad K_{3,3,3},\quad
K_{3,1,1,1,1},\quad K_6. \tag{8}
\]

The \(K_{3,3,3}\) row is incompatible with (5).  Its nine vertices
already contribute at least \(2\cdot27=54\) to the degree sum of \(E\).
On the four outside vertices, (5) gives total remaining-complement
capacity at most
\[
2\cdot31-54-2\cdot4=0. \tag{9}
\]
But the triple complement of a remaining support containing that
nine-vertex core would contribute three.  Therefore the exact
second-size-ten frontier is
\[
\boxed{K_{5,5},\quad K_{3,1,1,1,1},\quad K_6.} \tag{10}
\]

The row identity gives fixed-core reuse ceilings \(1,4,5\), respectively,
among the five remaining triples.  In particular, a \(K_{5,5}\) branch is
an equality branch and can block at most one remaining support.

This does not finish the first order in (2).  Even after two size-ten
matchings are coordinated, the unique size-twelve graph starts with
minimum degree at least six and then loses the union of two matchings.
Its possible Tutte barriers coarsen to
\[
K_{5,7},\qquad K_{3,1,1,1,1,1},\qquad K_7, \tag{11}
\]
and support-preserving switches are still required.

### The separator-three equality branch

The middle core in (10) has a useful exact local form.  Write the target
support as
\[
Y=S\mathbin{\dot\cup}C\mathbin{\dot\cup}T,
\qquad |S|=|C|=3,\quad |T|=4,
\]
where the four vertices of \(T\) are singleton components of
\((G-M)-S\).

Every \(t\in T\) is adjacent in \(G\) to all three vertices of \(S\), and
its fourth required \(G\)-edge is its \(M\)-edge into \(T\cup C\).
Consequently \(T\subseteq Y_0\).  If \(a\) and \(b\) count the
\(M\)-edges of types \(TT\) and \(TC\), then
\[
2a+b=4,\qquad b\le3,
\]
so
\[
(a,b)=(2,0)\quad\text{or}\quad(1,2). \tag{12}
\]

A rigid subbranch occurs when \(b=0\), the selected complement
\(V\setminus Y_0\) equals the separator \(S\), and the remaining perfect
matching on \(C\cup A\), where \(A=V\setminus Y\), uses three \(CA\)
edges.  In that subbranch the matching has the local form
\[
M=2(TT)+3(CA). \tag{13}
\]
There is a second endpoint pattern which must not be discarded:
\[
M=2(TT)+1(CC)+1(CA)+1(AA). \tag{13a}
\]
These are the only two possibilities, because the number of cross edges
in a perfect matching between two odd three-sets is odd.

In the three-\(CA\) subbranch, the obvious six-vertex switch
\[
t_1t_2,\ c_1a_1,\ c_2a_2
\longmapsto
t_1a_1,\ t_2a_2,\ c_1c_2 \tag{14}
\]
frees a \(TT\)-edge but consumes a residual \(C\)-edge.  If \(G-M\)
has only that one edge in \(C\), the standard target matching needs both
the freed \(TT\)-edge and the consumed \(C\)-edge.  Thus (14) is not a
proof.  This is an explicit switching gate, not a counterexample to
coordinated nine.

## Second order: insert the size-twelve matching before the last ten

The proved order-twelve resilience lemma allows one to choose \(N\) on the
unique size-twelve support after \(M\): \(H[X]\) has minimum degree at
least six, and it retains a perfect matching after deleting the matching
\(M\cap E(H[X])\).

For a final size-ten support \(Y\), start again from \(G=H[Y]\), where
\(\delta(G)\ge4\), and delete the union of the two matchings \(M,N\).
The component-degree bound is now
\[
4\le(c-1)+s+2,
\qquad c\ge3-s.
\]
The exact coarsened catalogue is
\[
\boxed{
K_{3,7},\ K_{5,5},\ K_{3,3,3},\
K_{5,1,1,1},\ K_{3,3,1,1},\
K_{3,1,1,1,1},\ K_6.
} \tag{15}
\]
Using (6), their fixed-core reuse ceilings among the five remaining
size-ten supports are, in the displayed order,
\[
(3,2,1,4,3,5,5). \tag{16}
\]
This is the exact final-size-ten switching frontier for the second order
in (2).  It is larger than (10), but it has the advantage that the
size-twelve matching is already secured.

## A literal obstruction to an arbitrary pair theorem

Label the vertices \(0,\ldots,12\).  The following six pairwise
edge-disjoint matchings form a valid complement-cover prefix:
\[
\begin{aligned}
P_0={}&02,14,3\,11,58,\\
P_1={}&01,25,6\,11,89,\\
P_2={}&05,29,48,11\,12,\\
P_3={}&04,18,37,10\,12,\\
P_4={}&15,24,6\,12,79,10\,11,\\
P_5={}&08,12,45,6\,10,7\,11.
\end{aligned} \tag{17}
\]
The first four have size four and the last two size five.  Their
complements are
\[
\begin{gathered}
679\,10\,12,\quad347\,10\,12,\quad1367\,10,\quad2569\,11,\\
038,\quad39\,12.
\end{gathered} \tag{18}
\]

Complete the complement family with the four five-sets
\[
01245,\quad1267\,11,\quad0246\,12,\quad01458, \tag{19}
\]
the six triples
\[
10\,11\,12,\quad7\,10\,11,\quad8\,9\,11,\quad234,\quad189,\quad058,
\tag{20}
\]
and the singleton \(\{5\}\).  Every vertex occurs in exactly five of
the seventeen complements, so this is a literal class-B profile \(r=1\).

Let \(D=\bigcup_iP_i\), \(H=K_{13}-D\), and take
\[
T_0=\{10,11,12\},\qquad T_1=\{7,10,11\}. \tag{21}
\]
Both \(H-T_0\) and \(H-T_1\) have exactly twenty-four perfect matchings.
However, no perfect matching of the first is edge-disjoint from a perfect
matching of the second.  This is checked by direct enumeration of all
perfect matchings, using only the standard library.

Index the six triples in the order displayed in (20).  The numbers of
available perfect matchings are
\[
(24,24,120,150,144,150).
\]
The full table of edge-disjoint ordered choices for an unordered pair of
supports is
\[
\begin{array}{c|rrrrrr}
 &0&1&2&3&4&5\\ \hline
0&-&0&1536&2496&2472&2800\\
1&&-&1536&2490&2406&2772\\
2&&&-&11760&9216&11628\\
3&&&&-&14556&15612\\
4&&&&&-&12444\\
5&&&&&&-
\end{array} \tag{22}
\]
Thus only the pair \(0,1\) is obstructed in this certificate.

Therefore the following tempting ambient statement is false:

> If \(H\) has order thirteen and minimum degree at least seven, and
> \(H-T_0,H-T_1\) are individually matchable, then their perfect
> matchings can be chosen edge-disjoint.

It remains false even after adding the full class-B row-sum condition.
The two obstructed triples in (21) overlap in two vertices.  In the same
certificate, table (22) shows that every other pair among the six triples
admits many edge-disjoint matching pairs.

Triple overlap alone does not characterize the obstruction.  The compact
data file `pair_obstructions.json` contains three literal class-B
six-prefix certificates whose obstructed pairs have respectively
\[
|T_0\cap T_1|=0,\quad1,\quad2. \tag{23}
\]
In every certificate, each of the two displayed support graphs has exactly
twenty-four perfect matchings, none of the \(24^2\) cross-pairs is
edge-disjoint, and every other pair among that certificate's six triples
does admit an edge-disjoint choice.

Thus even a low-overlap arbitrary-pair theorem is false.  The viable
selective target is instead to prove that the incompatibility graph on all
six remaining triples cannot be complete, using the simultaneous
row-capacity and obstruction-core reuse constraints.

## Verification

Run

```sh
python3 collaboration/coordinated_nine_r1_reduction/verify_reduction.py
```

The verifier uses only the Python standard library.  It checks both Tutte
catalogues, all capacity and uniqueness calculations, the literal
seventeen-column class-B certificates, the six-prefix matching structures,
all three exact \(24\times24\) pair obstructions, and table (22).
