# High-lift complements: shadows of packings

Date: 2026-07-27.

## Scope

This note concerns one fixed local instance in the unrestricted lift tower
on the thirteen-point set \(A\).  It proves that the standard local
divisibility conditions are sufficient for the last three complement
parameters \(r=1,2,3\), and that the required cross-colour block partition
then follows from the tower's exact \(r\)-fold cover.

This does **not** construct the preceding tower levels or enforce
top-properness between different \(R\)'s.  In particular it does not solve
Erdős--Rosenfeld Problem #835.

Write
\[
 j=13-r,\qquad
 {\cal H}\subseteq\binom Aj,\qquad
 {\cal H}^{\star}
 =\{A\setminus B:B\in{\cal H}\}\subseteq\binom Ar.
\tag{1}
\]
For \({\cal X}\subseteq\binom A{r-1}\), its upper shadow is
\[
 \nabla{\cal X}
 =\{Z\in\binom Ar:\text{some }Y\in{\cal X}\text{ satisfies }Y\subset Z\}.
\tag{2}
\]
Call \({\cal X}\) a shadow packing when no \(r\)-set contains two members
of \({\cal X}\), equivalently the individual shadows
\(\nabla\{Y\}\) are pairwise disjoint.

## 1. Complement dictionary

> **Proposition 1.**  A \(K_{j+1}^{(j)}\)-decomposition of
> \({\cal H}\) is equivalent, under complementation in \(A\), to a shadow
> packing \({\cal X}\subseteq\binom A{r-1}\) satisfying
> \[
> {\cal H}^{\star}=\nabla{\cal X}.
> \tag{3}
> \]

### Proof

A block \(D\in\binom A{j+1}\) corresponds to
\(Y=A\setminus D\in\binom A{r-1}\).  The \(j\)-sets in the copy on \(D\)
are \(D\setminus\{x\}\), \(x\in D\).  Their complements are
\[
 A\setminus(D\setminus\{x\})=Y\cup\{x\},
 \qquad x\in A\setminus Y,
\]
which are precisely all \(r\)-sets in \(\nabla\{Y\}\).  Thus two block
copies are edge-disjoint exactly when their upper shadows are disjoint,
and they cover \({\cal H}\) exactly when (3) holds. \(\square\)

For the three cases of interest, a shadow packing is respectively:

* \(r=1\): either no \(0\)-set or the unique \(0\)-set \(\varnothing\);
* \(r=2\): either no vertex or one vertex;
* \(r=3\): a matching of pairs.

## 2. Divisibility after complementation

The standard conditions for a \(K_{j+1}^{(j)}\)-decomposition are
\[
 d_{\cal H}(I)\equiv0\pmod{j+1-|I|}
 \quad\left(I\in\binom Ai,\ 0\le i<j\right).
\tag{4}
\]
Put \(T=A\setminus I\) and \(t=|T|=13-i\).  Complementation gives the
exact identity
\[
 d_{\cal H}(I)=|{\cal H}^{\star}[T]|.
\tag{5}
\]
Since \(j=13-r\), conditions (4) are therefore precisely
\[
 |{\cal H}^{\star}[T]|
 \equiv0\pmod{t-r+1}
 \quad
 (T\subseteq A,\ t\ge r+1).
\tag{6}
\]

## 3. The cases \(r=1\) and \(r=2\)

> **Theorem 2 (\(r=1\), or \(j=12\)).**  Conditions (6) force
> \({\cal H}^{\star}\) to be either empty or all of \(\binom A1\).
> Hence \({\cal H}^{\star}\) is the upper shadow of, respectively,
> \(\varnothing\) or \(\{\varnothing\}\), and the required decomposition
> exists.

### Proof

For every two-set \(T\), (6) says that
\(|{\cal H}^{\star}\cap T|\) is divisible by two.  Thus the two points of
every pair have equal membership in \({\cal H}^{\star}\).  All thirteen
membership indicators are equal. \(\square\)

> **Theorem 3 (\(r=2\), or \(j=11\)).**  Conditions (6) force
> \({\cal H}^{\star}\) to be either the empty graph or a full star.
> Hence it is the upper shadow of either no vertex or one vertex, and the
> required decomposition exists.

### Proof

For every triple \(T\), (6) makes \(e({\cal H}^{\star}[T])\) even.
Fix a vertex \(v\), and put
\[
 S=\{x\ne v:vx\in{\cal H}^{\star}\}.
\]
Triple parity on \(vxy\) gives
\[
 {\bf1}_{xy\in{\cal H}^{\star}}
 =
 {\bf1}_{x\in S}+{\bf1}_{y\in S}\pmod2.
\]
Thus \({\cal H}^{\star}\) is the cut between \(S\) and its complement
(with \(v\) placed in the complement).

On a four-set having \(s\) points on one side of this cut, the edge count
is \(s(4-s)\).  Condition (6) makes this divisible by three.  The value is
\(4\), not divisible by three, when \(s=2\).  Therefore the global cut
cannot have two points on each side.  One side has size zero or one, so the
cut is empty or a full star. \(\square\)

## 4. The case \(r=3\)

Let \(h(Z)={\bf1}_{Z\in{\cal H}^{\star}}\) for triples \(Z\).
The four-set condition in (6) is
\[
 \sum_{Z\in\binom T3}h(Z)=0\pmod2
 \qquad(T\in\binom A4).
\tag{7}
\]

### 4.1 Two-graph representation

Fix \(v\in A\).  Define a graph \(G\) with \(v\) isolated by
\[
 g(xy)=h(vxy)\qquad(x,y\ne v).
\tag{8}
\]
Applying (7) to \(vxyz\) gives
\[
 h(xyz)=g(xy)+g(xz)+g(yz)\pmod2.
\tag{9}
\]
Equation (9) also holds for triples containing \(v\), by (8).  Thus
\({\cal H}^{\star}\) is the mod-two coboundary of \(G\).  A different
choice of gauge changes \(G\) by a cut, which is ordinary graph switching.

### 4.2 What the five-set condition says

Let \(S\subseteq A\setminus\{v\}\) have size four.  On
\(T=\{v\}\cup S\), the triples containing \(v\) contribute
\(e(G[S])\) to \(|{\cal H}^{\star}[T]|\).  The remaining contribution is
\[
 q(G[S])
 =\#\{\text{triples of }S\text{ spanning an odd number of }G\text{-edges}\}.
\]
The five-set case of (6) is therefore
\[
 e(G[S])+q(G[S])\equiv0\pmod3.
\tag{10}
\]

There are eleven isomorphism types of graphs on four vertices.  Direct
counting gives:

| \(G[S]\) | \(e\) | \(q\) | \(e+q\) | passes (10) |
|---|---:|---:|---:|:---:|
| empty | 0 | 0 | 0 | yes |
| one edge | 1 | 2 | 3 | yes |
| two disjoint edges | 2 | 4 | 6 | yes |
| \(P_3\) plus an isolated point | 2 | 2 | 4 | no |
| \(P_4\) | 3 | 2 | 5 | no |
| \(K_3\) plus an isolated point | 3 | 4 | 7 | no |
| \(K_{1,3}\) | 3 | 0 | 3 | yes |
| \(C_4\) | 4 | 0 | 4 | no |
| \(K_{1,3}\) plus one leaf edge | 4 | 2 | 6 | yes |
| \(K_4-e\) | 5 | 2 | 7 | no |
| \(K_4\) | 6 | 4 | 10 | no |

Hence every induced four-vertex subgraph of \(G-v\) is one of the five
types marked yes.

### 4.3 The graph lemma

> **Lemma 4.**  Let \(F\) be a graph on at least five vertices such that
> every induced four-vertex subgraph is empty, one edge, two disjoint
> edges, \(K_{1,3}\), or \(K_{1,3}\) plus one leaf edge.  Then either
> \(F\) is a matching, or \(F\) has a universal vertex \(u\) and
> \(F-u\) is a matching.

### Proof

If \(\Delta(F)\le1\), there is nothing to prove.  Choose a vertex \(c\)
with two neighbours \(a,b\).

First suppose that some such \(a,b\) are nonadjacent.  For every
\(x\notin\{a,b,c\}\), the allowed four-vertex list applied to
\(\{a,b,c,x\}\) forces \(cx\) to be an edge and permits at most one of
\(ax,bx\).  Hence \(c\) is universal.  Applying the list to
\(\{c,x,y,z\}\) shows that every triple of \(F-c\) spans at most one edge.
Equivalently, \(\Delta(F-c)\le1\), so \(F-c\) is a matching.

Now suppose every pair of neighbours of \(c\) is adjacent.  Three
neighbours together with \(c\) would induce \(K_4\), which is forbidden;
therefore \(N(c)=\{a,b\}\) and \(abc\) is a triangle.  For every
\(x\notin\{a,b,c\}\), the only allowed four-vertex type containing this
triangle is \(K_{1,3}\) plus one leaf edge.  Since \(c\) has no further
neighbour, \(x\) is adjacent to exactly one of \(a,b\).

There cannot be vertices \(x,y\) attached to different sides.  If there
were, \(\{a,b,x,y\}\) would induce \(P_4\) when \(xy\) is absent and
\(C_4\) when \(xy\) is present.  Thus every outside vertex attaches to
the same side, say \(a\), making \(a\) universal.  The four-vertex list
on \(a\) and any three other vertices again shows that \(F-a\) is a
matching. \(\square\)

Apply the lemma to \(F=G-v\).  If \(G-v=M\) is a matching, put
\({\cal X}=M\).  Otherwise,
\[
 G-v=K_{1,11}\text{ centred at }u\ \mathbin{\dot\cup}\ M,
\]
where \(M\) is a matching on the other vertices, and put
\[
 {\cal X}=\{vu\}\mathbin{\dot\cup}M.
\tag{11}
\]
In the second case \(G\) and \({\cal X}\) differ by the full cut
\(\delta(\{u\})\), so they have the same mod-two coboundary.  Thus in
both cases (9) says that a triple belongs to \({\cal H}^{\star}\) exactly
when it contains an edge of the matching \({\cal X}\).  No triple contains
two matching edges, and therefore
\[
 {\cal H}^{\star}=\nabla{\cal X}.
\tag{12}
\]

This proves:

> **Theorem 5 (\(r=3\), or \(j=10\)).**  The four-set and five-set
> conditions in (6) force \(G\) to be switching-equivalent to a matching
> \({\cal X}\), and force
> \({\cal H}^{\star}=\nabla{\cal X}\).  Hence the required
> \(K_{11}^{(10)}\)-decomposition exists.

The higher divisibility conditions add nothing.  For every
\(T\subseteq A\),
\[
 |{\cal H}^{\star}[T]|
 =(|T|-2)\,|{\cal X}\cap\binom T2|,
\tag{13}
\]
because each matching edge in \(T\) has exactly \(|T|-2\) triple
extensions in \(T\), and these extensions are disjoint for different
matching edges.  Equation (13) supplies every remaining condition in (6).

## 5. Cross-colour compatibility

Now restore the fixed-\(R\) tower setting and its seventeen colours.
For each colour \(\gamma\), let
\({\cal H}^{\star}_\gamma\subseteq\binom Ar\) be the complemented leave.
Top properness gives \(j+4\) distinct known colours at each \(j\)-set, so
exactly
\[
 17-(j+4)=13-j=r
\]
colours omit it.  Hence the complemented leaves form an exact \(r\)-fold
cover:
\[
 \sum_\gamma
 {\bf1}_{Z\in{\cal H}^{\star}_\gamma}=r
 \qquad(Z\in\binom Ar).
\tag{14}
\]

For \(r\le3\), Theorems 2, 3, and 5 produce a shadow packing
\({\cal X}_\gamma\subseteq\binom A{r-1}\) for every colour.  Put
\[
 m_Y=\#\{\gamma:Y\in{\cal X}_\gamma\}.
\]
Because every \({\cal X}_\gamma\) is a packing, (14) becomes
\[
 \sum_{Y\in\binom Z{r-1}}m_Y=r
 \qquad(Z\in\binom Ar).
\tag{15}
\]
This is the inclusion-matrix equation
\[
 W_{r-1,r}m=r{\bf1}.
\tag{16}
\]

For \(r=1\), (15) immediately gives \(m_\varnothing=1\).  For \(r=2\),
\[
 m_a+m_b=2\qquad(a\ne b),
\]
and comparison through a third vertex gives \(m_a=1\) for every \(a\).

For \(r=3\), set \(x_{ab}=m_{ab}-1\).  Equation (15) is
\[
 x_{ab}+x_{ac}+x_{bc}=0
\qquad(a,b,c\text{ distinct}).
\tag{17}
\]
For four distinct vertices, adding the equations on two opposite
triangles and subtracting the other two shows that opposite-edge values
are equal, for example \(x_{bc}=x_{ad}\).  When \(|A|\ge5\), any two
adjacent edges are both disjoint from some third edge, so all \(x_{ab}\)
are equal.  Equation (17) then makes their common value zero.  Therefore
\[
 m_Y=1\qquad\left(Y\in\binom A{r-1}\right)
\tag{18}
\]
in all three cases.

Under complementation, the new \((j+1)\)-blocks partition
\(\binom A{j+1}\) across colours exactly when the
\({\cal X}_\gamma\)'s partition \(\binom A{r-1}\).  Equation (18) proves
this cross-colour requirement automatically.  Equivalently,
\(W_{1,2}\) and \(W_{2,3}\) have full column rank here; the proof above
gives the required rank argument without relying on computation.

## 6. Exact tower consequence and limitation

At any fixed \(R\), conditional on the previously constructed level and
its top-properness:

* \(j=12\) (\(r=1\)): local divisibility forces the decomposition, and
  cross-colour compatibility is automatic;
* \(j=11\) (\(r=2\)): the same is true;
* \(j=10\) (\(r=3\)): already the four- and five-set divisibility
  conditions force the matching-shadow decomposition, all higher
  conditions follow, and cross-colour compatibility is automatic.

The unrestricted-tower theorem already proves these local divisibility
conditions for its leaves.  Thus no genuine **fixed-\(R\)**
decomposition obstruction remains at \(j=10,11,12\).

This does not make the final lifts automatic globally.  Choices made at
different \(R\)'s must still satisfy the next top-properness conditions.
Nothing here constructs those coupled choices or reaches the full Johnson
graph colouring.

## 7. Verification

Run:

```sh
python3 -B \
  collaboration/high_lift_complement_decomposition/verify_high_lift_complements.py
```

The standard-library verifier:

* checks Proposition 1 on every \(r\le3\) packing on seven points;
* exhausts all \(r=1\) systems and all \(r=2\) graphs on six points;
* checks all \(64\) labelled graphs in the four-vertex table;
* exhausts the canonical switching representatives through order seven,
  finding respectively \(8,26,76,232\) divisible classes, all and only
  matching shadows;
* verifies (13) on those controls; and
* computes full column rank of \(W_{1,2}\) and \(W_{2,3}\) for thirteen
  points modulo the prime \(1{,}000{,}003\).

The enumeration supports and audits the proofs.  It is not being used as
a substitute for the order-thirteen argument above.
