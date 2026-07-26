# The three-system defect map and its exact local boundary

Status: **proved reduction and exact local countermodels; not a
nonexistence proof.**

Let \(r\geq 3\) be odd, let \(X\) have \(2r+1\) points, and suppose
\(\mathcal A,\mathcal B,\mathcal C\) are three pairwise block-disjoint
systems \(S(r-1,r,2r+1)\).  For every \((r-1)\)-set \(F\), let
\[
 a_F,\quad b_F,\quad c_F
\]
be the respective unique extension points, so that
\[
 F+a_F\in\mathcal A,\qquad
 F+b_F\in\mathcal B,\qquad
 F+c_F\in\mathcal C.
\]
Pairwise block-disjointness makes these three points distinct.  Hence
\[
 T(F)=X\setminus(F\cup\{a_F,b_F,c_F\})                 \tag{1}
\]
is again an \((r-1)\)-set.

The tempting claim that \(T\) is automatically an involution, or even a
bijection, is not justified.  This note gives the exact local criterion
for bijectivity and shows why the local data alone cannot prove it.

## 1. The near-perfect matchings over one facet

Fix an \((r-1)\)-set \(R\), and put \(U=X\setminus R\), so
\(|U|=r+2\).  For a system \(\mathcal D\), complement every
\(\mathcal D\)-block contained in \(U\) inside \(U\):
\[
 M_{\mathcal D}(U)
 =\{\,U\setminus D:D\in\mathcal D,\ D\subset U\,\}.      \tag{2}
\]

**Lemma 1.**  \(M_{\mathcal D}(U)\) is a matching of
\((r+1)/2\) edges on \(U\), and its unique unmatched point is the
\(\mathcal D\)-extension point of \(R\).

**Proof.**  The number of \(\mathcal D\)-blocks contained in \(U\) is
constant in \(U\): it is the number of blocks avoiding the fixed
\((r-1)\)-set \(X\setminus U\), hence is determined by inclusion-exclusion
from the design parameters.  Averaging over all \(U\) gives
\[
 \frac{|\mathcal D|\binom{r+1}{2}}
      {\binom{2r+1}{r+2}}
 =\frac{r+1}{2}.                                      \tag{3}
\]
If two complementary edges in (2) met, the corresponding two blocks
would meet in \(r-1\) points, impossible in an
\(S(r-1,r,2r+1)\).  Thus (2) is a matching, using \(r+1\) of the
\(r+2\) points.

Let \(d_R\) be the extension point of \(R\) in \(\mathcal D\).
If \(d_R\) lay in an edge \(e\in M_{\mathcal D}(U)\), then
\(R+d_R\) and \(U\setminus e\) would be two disjoint blocks of
\(\mathcal D\).  The internal intersection equations give \(n_0=0\)
for a block of a boundary system, so this is impossible.  Therefore
\(d_R\) is the unique unmatched point. \(\square\)

For the three systems, the matchings
\[
 M_{\mathcal A}(U),\quad M_{\mathcal B}(U),\quad
 M_{\mathcal C}(U)                                    \tag{4}
\]
are pairwise edge-disjoint: a repeated edge would give a repeated block
\(U\setminus e\).  Their unmatched points are also distinct: a repeated
unmatched point would give the same extension block of \(R\).

At the target \(r=15\), (4) is therefore a triple of edge-disjoint
eight-edge near-perfect matchings on seventeen points, with three distinct
unmatched points.

## 2. Exact preimage theorem

Call a triangle in the union (4) **rainbow** if it has one edge of each
matching.  Equivalently, label its vertices \(a,b,c\) so that
\[
 \{b,c\}\in M_{\mathcal A}(U),\qquad
 \{a,c\}\in M_{\mathcal B}(U),\qquad
 \{a,b\}\in M_{\mathcal C}(U).                         \tag{5}
\]

**Theorem 2.**
\[
 \boxed{\quad |T^{-1}(R)|
   =\#\{\text{rainbow triangles in }(4)\}.\quad}        \tag{6}
\]

**Proof.**  If \(T(F)=R\), then
\[
 U=F\mathbin{\dot\cup}\{a_F,b_F,c_F\}.
\]
The three blocks through \(F\) are
\[
\begin{aligned}
 F+a_F&=U\setminus\{b_F,c_F\},\\
 F+b_F&=U\setminus\{a_F,c_F\},\\
 F+c_F&=U\setminus\{a_F,b_F\}.
\end{aligned}
\]
Their complementary edges form the rainbow triangle (5).

Conversely, from a rainbow triangle \(\{a,b,c\}\), put
\[
 F=U\setminus\{a,b,c\}.
\]
Equation (5) says exactly that \(F+a,F+b,F+c\) are the respective
blocks of the three systems through \(F\).  Therefore (1) gives
\(T(F)=R\).  The two constructions are inverse. \(\square\)

Distinct rainbow triangles need not be vertex-disjoint: two of them can
share their common edge of one colour and exchange the other two colours.
There is nevertheless a useful elementary bound.  In the union of the
three near-perfect matchings, the three distinct unmatched vertices have
degree two and the other \(r-1\) vertices have degree three.  A degree-two
vertex lies in at most one triangle, and a degree-three vertex in at most
three.  If \(t\) is the number of rainbow triangles, summing
triangle--vertex incidences gives
\[
 3t\leq 3+3(r-1)=3r.
\]
Consequently
\[
 0\leq |T^{-1}(R)|\leq r.                              \tag{7}
\]
For \(r=15\), every indegree lies between zero and fifteen.  The coherent
cross-link certificate in `verify_defect_cross_link_lsts19.py` already
realizes multiplicity six, so the earlier tempting
\(\lfloor(r+2)/3\rfloor\) bound is false.

Since \(T\) is a function on all \(\binom{2r+1}{r-1}\) facets,
\[
 \sum_R |T^{-1}(R)|=\binom{2r+1}{r-1}.                 \tag{8}
\]
Thus its average indegree is one.  Equations (6)--(8) show that
\[
 T\text{ is bijective}
 \quad\Longleftrightarrow\quad
 \text{every local union (4) has exactly one rainbow triangle}. \tag{9}
\]

## 3. Exact local countermodels at seventeen points

The conditions proved in Lemma 1 do not force the right side of (9).
The companion verifier checks three explicit triples on
\(\{0,\ldots,16\}\), always with edge-disjoint matchings and distinct
unmatched vertices:

* a triple with no rainbow triangle;
* a triple with exactly one rainbow triangle;
* a triple with exactly two rainbow triangles (the displayed certificate
  happens to make them vertex-disjoint).

For example, the zero-triangle triple has unmatched points
\((5,7,4)\) and matchings
\[
\begin{aligned}
M_A={}&
10\,16,\ 4\,11,\ 1\,15,\ 2\,12,\ 3\,8,\ 9\,13,\ 6\,7,\ 0\,14,\\
M_B={}&
4\,9,\ 5\,14,\ 1\,11,\ 12\,15,\ 3\,13,\ 0\,2,\ 8\,10,\ 6\,16,\\
M_C={}&
8\,15,\ 13\,14,\ 12\,16,\ 7\,11,\ 0\,3,\ 5\,10,\ 2\,9,\ 1\,6.
\end{aligned}                                          \tag{10}
\]

These are local matching countermodels, not restrictions of three known
\(S(14,15,31)\) systems.  They prove the precise logical boundary:
near-perfectness, edge-disjointness, and distinct unmatched points do not
imply that \(T\) is injective or surjective.  A proof of bijectivity would
have to use compatibility between the matching triples belonging to
different \(17\)-sets \(U\).

The zero-triangle triple in (10) also passes the **entire local-link**
condition forced by a hypothetical large set.  Pair its three unmatched
vertices with a new point \(\infty=17\).  The resulting three perfect
matchings extend to a full one-factorization of \(K_{18}\).  One exact
completion (the first three factors are (10) with the new edges) has the
remaining fourteen factors
\[
\begin{array}{rrrrrrrrr}
01&2\,16&36&45&78&9\,10&11\,14&12\,13&15\,17\\
04&12&3\,10&5\,12&68&7\,16&9\,11&13\,15&14\,17\\
05&14&23&69&7\,15&8\,13&10\,11&12\,14&16\,17\\
06&18&2\,13&35&47&9\,14&10\,12&11\,17&15\,16\\
07&13&24&5\,16&6\,10&8\,17&9\,12&11\,13&14\,15\\
08&1\,10&26&3\,11&4\,12&5\,15&7\,14&9\,16&13\,17\\
09&1\,12&27&3\,15&48&5\,11&6\,13&10\,17&14\,16\\
0\,10&17&2\,15&39&4\,13&58&6\,14&11\,16&12\,17\\
0\,11&1\,17&2\,10&3\,16&4\,15&59&6\,12&7\,13&8\,14\\
0\,12&1\,13&28&37&4\,16&56&9\,17&10\,14&11\,15\\
0\,13&1\,16&25&3\,14&4\,10&6\,17&7\,12&8\,11&9\,15\\
0\,15&15&2\,14&3\,17&46&7\,10&89&11\,12&13\,16\\
0\,16&1\,14&2\,17&34&5\,13&6\,11&79&8\,12&10\,15\\
0\,17&19&2\,11&3\,12&4\,14&57&6\,15&8\,16&10\,13.
\end{array}                                             \tag{11}
\]
The verifier checks that these seventeen factors partition all \(153\)
edges of \(K_{18}\).  Therefore even a complete local
one-factorization does not imply that the selected colour triple has a
rainbow triangle away from \(\infty\).  The missing input is genuinely
cross-link compatibility, not an unrecorded condition inside one link.

There is no genuine \(r=3\) or \(r=5\) three-system control: at both
parameters at most two pairwise disjoint boundary systems exist.  Using
three intersecting systems would invalidate (1), because their extension
points can coincide, so it cannot test the defect map defined here.

## 4. Exact scope

The defect map remains a potentially useful global object.  In particular,
an orientation theorem forcing every directed \(T\)-cycle to be even would
contradict the odd number
\[
 \binom{31}{14}=265\,182\,525
\]
of target facets, provided bijectivity were first established.  Neither
ingredient is proved here.

What is proved is:

1. the exact rainbow-triangle interpretation of every indegree;
2. the elementary local upper bound (7);
3. average indegree one; and
4. explicit local models showing that all of this falls short of
   bijectivity.

## 5. The first triangle-parity orientation closes exactly

There is a natural mod-two strengthening of the rainbow-triangle count, but
it also closes without contradiction.

Adjoin a point \(\infty\).  The unique extension of each
\(S(r-1,r,2r+1)\) to an \(S(r,r+1,2r+2)\) turns the near-perfect matching
of Lemma 1 into a perfect matching on
\[
 U\cup\{\infty\}
\]
by pairing \(\infty\) with its unmatched extension point.  For a fixed
triple of systems and facet \(R\), let

* \(d_R\) be the number of rainbow triangles avoiding \(\infty\); by
  Theorem 2 this is \(|T^{-1}(R)|\);
* \(e_R\) be the number of rainbow triangles containing \(\infty\); and
* \(\tau_R=d_R+e_R\).

If a full large set is present, the seventeen extended matching links form
a one-factorization of \(K_{r+3}\).  For every fixed pair of factor colours
\(\alpha,\beta\),
\[
 \sum_{\gamma\ne\alpha,\beta}\tau_R(\alpha,\beta,\gamma)=r+3. \tag{12}
\]
Indeed, at each vertex, the \(\alpha\)- and \(\beta\)-edges have two
distinct other endpoints; the edge joining those endpoints has one unique
third colour \(\gamma\).  A triangle with colours
\(\alpha,\beta,\gamma\) is counted exactly once, at the vertex incident
with its \(\alpha\)- and \(\beta\)-edges.  At \(r=15\), the right side of
(12) is \(18\), so the full triangle-parity vector is a binary
2-cycle on the colour simplex.

It is tempting to use Theorem 2 to say that, globally, the finite
triangle-parity vector sums to the all-one vector, which is not a 2-cycle
on seventeen colours.  The triangles through \(\infty\) cancel this
apparent defect exactly.

**Lemma 3.**  For any fixed three pairwise disjoint systems,
\[
 \sum_R d_R=rb,\qquad
 \sum_R e_R=3b,\qquad
 \sum_R\tau_R=(r+3)b,                                  \tag{13}
\]
where \(b\) is the number of blocks in one system.

**Proof.**  The first equality is (8), since the number of facets is
\(\binom{2r+1}{r-1}=rb\).

For the second, first prescribe which of the three colours is the finite
edge of a triangle through \(\infty\), say \(\mathcal C\).  Fix a
\(\mathcal C\)-block \(K\).  It has a unique disjoint
\(\mathcal A\)-block \(P\) and a unique disjoint
\(\mathcal B\)-block \(Q\).  Both \(P,Q\) are distinct \(r\)-subsets of
the \((r+1)\)-set \(X\setminus K\), so
\[
 R=P\cap Q
\]
has size \(r-1\).  In the extended link at \(R\), the blocks \(P,Q,K\)
give one triangle through \(\infty\) whose finite edge has colour
\(\mathcal C\).  This construction is reversible.  Thus there are \(b\)
such triangles for each choice of finite-edge colour, hence \(3b\).
Adding the first two equalities proves the last. \(\square\)

For \(r=15\), both \(rb\) and \(3b\) are odd, while their sum \(18b\)
is even.  Thus the through-\(\infty\) triangles supply exactly the missing
boundary of the finite rainbow-triangle vector.  The most immediate
one-factorization homology/orientation argument is therefore consistent,
not contradictory.  Any successful orientation refinement must retain
more than triangle counts modulo two.

Run

```bash
/opt/homebrew/bin/python3 -B evidence/verify_defect_facet_map_audit.py
```

for the finite checks.
