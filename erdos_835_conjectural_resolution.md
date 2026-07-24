# Erdős–Rosenfeld Problem #835: a researched conjectural resolution

## Honest status

This note gives a complete statement of a negative conjecture, proves several
reductions that substantially narrow it, and independently verifies the first
exceptional case.  It does **not** prove the still-open conjecture.

As of 24 July 2026, the Erdős Problems database still marks Problem #835
open.  Its discussion contains no accepted solution.  Exact recent searches
on X/Twitter found no claimed solution under the problem number, the
Johnson-graph formulation, or the Steiner-system formulation.  One post linked
an independent preliminary report proving the same prime sieve and small
cases, but that report also stops short of the open prime cases.  The available
X API covered only the preceding seven days; full-archive search was not
available on the connected tier, so this is evidence rather than a logical
guarantee.

## Problem and conjecture

For an integer \(k>2\), can the \(k\)-subsets of a \(2k\)-element set be
coloured with \(k+1\) colours so that the \(k+1\) subsets of every
\((k+1)\)-set have pairwise different colours?

Equivalently, does
\[
  \chi(J(2k,k))=k+1
\]
ever hold for \(k>2\)?

**Negative-resolution conjecture.**  For every \(k>2\),
\[
  \boxed{\chi(J(2k,k))\ge k+2.}
\]

The rest of the note records what can be proved rigorously in support of this
conjecture and identifies the first genuinely open case.

## 1. Exact equivalence with a large set of Steiner systems

Assume a colouring exists and fix a colour \(c\).  Every
\((k-1)\)-set \(T\) has exactly \(k+1\) extensions to a \(k\)-set.  Those
extensions form a clique in \(J(2k,k)\), so exactly one has colour \(c\).
Consequently the colour class \(\mathcal B_c\) is a Steiner system
\[
  S(k-1,k,2k).
\]

Conversely, a partition of all \(k\)-sets into \(k+1\) such Steiner systems
gives the required colouring.  Thus the problem is exactly the existence of
the large set
\[
  LS(k-1,k,2k).
\]

## 2. The elementary prime obstruction

In an \(S(k-1,k,2k)\), the number of blocks containing a fixed
\((k-j)\)-set is
\[
  \lambda_{k-j}
  =\frac{\binom{k+j}{j-1}}{j}
  =\frac{\binom{k+j}{j}}{k+1},
  \qquad 1\le j\le k.
\]
It must be an integer.  With \(n=k+1\), this says
\[
  n\mid\binom{n+j-1}{j}\qquad(1\le j\le n-1).
\]

If \(n\) is prime, this divisibility holds: in
\[
  \binom{n+j-1}{j}
  =\frac{n(n+1)\cdots(n+j-1)}{j!},
\]
the denominator is coprime to \(n\).

If \(n\) is composite, let \(p\) be its smallest prime divisor and take
\(j=p\).  Among \(n,n+1,\ldots,n+p-1\), only \(n\) is divisible by \(p\),
whereas \(p!\) contains one factor of \(p\).  Hence
\[
 v_p\!\left(\binom{n+p-1}{p}\right)=v_p(n)-1<v_p(n),
\]
contradicting the required divisibility.  Therefore
\[
  \boxed{k+1\text{ must be prime}.}
\]

This is the Ma–Tang obstruction, included here with its short proof.

## 3. A whole tower of derived large sets

The original large-set requirement has stronger consequences than the
existence of one constituent Steiner system.

**Derived-large-set theorem.**  If \(LS(k-1,k,2k)\) exists, then for every
\(1\le r\le k\),
\[
  LS(r-1,r,k+r)
\]
exists.

**Proof.** Fix a set \(U\) of \(k-r\) points.  In one colour class, retain
the blocks containing \(U\) and remove \(U\) from each.  Given any
\((r-1)\)-set \(R\) outside \(U\), the \((k-1)\)-set \(U\cup R\) has a
unique extension in that colour.  The added point lies outside \(U\), so the
retained blocks form an \(S(r-1,r,k+r)\).  As the original colour classes
partition all \(k\)-sets, the derived classes partition all \(r\)-sets
outside \(U\).  This is the claimed large set. \(\square\)

For the first open candidate \(k=16\), this forces, simultaneously and
compatibly,
\[
  LS(4,5,21),\qquad LS(3,4,20),\qquad LS(2,3,19),
\]
among all the other derived levels.  In particular, it requires seventeen
pairwise disjoint \(S(4,5,21)\) systems, not merely one.

## 4. Complement symmetry and an Odd-graph reformulation

All remaining candidates have \(k+1\) an odd prime, hence \(k\) is even.
In that case every colour class is closed under complementation.

Here is a concise proof.  Let \(M\) be the inclusion matrix whose rows are
indexed by \((k-1)\)-sets and columns by \(k\)-sets.  If \(x\) is the
indicator of a colour class, then
\[
  Mx=\mathbf 1,\qquad
  y:=x-\frac1{k+1}\mathbf 1\in\ker M.
\]
The standard polytabloid spanning vectors of \(\ker M\) have the form
\[
 h(S)=\prod_{i=1}^{k}
 \bigl(\mathbf 1_{a_i\in S}-\mathbf 1_{b_i\in S}\bigr),
\]
where the \(2k\) points are paired as
\((a_1,b_1),\ldots,(a_k,b_k)\).  Complementation sends every such vector to
\((-1)^k h\), and therefore acts as \(+1\) on \(\ker M\) when \(k\) is
even.  Thus \(x(S)=x(S^c)\).

Now distinguish one point \(\infty\).  A complementary pair of \(k\)-sets
is represented uniquely by the \((k-1)\)-set obtained from its member
containing \(\infty\).  These representatives are the vertices of the Odd
graph
\[
  O_k=KG(2k-1,k-1),
\]
where two vertices are adjacent when they are disjoint.

The original colouring becomes a map
\[
  c:O_k\longrightarrow K_{k+1}
\]
that is bijective on the neighbourhood of every vertex: a vertex and its
\(k\) neighbours receive all \(k+1\) colours.  In graph language, this is a
covering projection.  Conversely, such a covering projection colours
complementary middle-layer sets alike; vertices of \(O_k\) corresponding to
adjacent middle-layer sets are at distance one or two, so local bijectivity
forces different colours.

Hence, after the prime obstruction, Problem #835 is exactly:

**Equivalent Odd-cover conjecture.**  For every even \(k>2\), the Odd graph
\(O_k\) has no covering projection onto \(K_{k+1}\).

Equivalently, \(O_k\) cannot be partitioned into \(k+1\) perfect
one-error-correcting codes.

### 4.1 An exact one- and two-point lift

There is a second exact reformulation which explains why the natural
monotonicity attack does not lose information.

**Odd-neighbour lift theorem.**  Let \(m\ge3\) be odd and put \(q=m+2\).
Then
\[
 \boxed{
 \chi(J(2m,m))=q
 \iff \chi(J(2m+1,m))=q
 \iff \chi(J(2m+2,m+1))=q.}
\]

**Proof.**  First note that all three chromatic numbers are at least \(q\).
For \(J(2m,m)\), fixing an \((m-2)\)-set induces the line graph of \(K_q\),
whose chromatic number is the edge-chromatic number \(q\), because \(q\) is
odd.  In \(J(2m+1,m)\), the \(m\)-sets through a fixed \((m-1)\)-set form
a \(q\)-clique; in \(J(2m+2,m+1)\), the \((m+1)\)-sets through a fixed
\(m\)-set form a \(q\)-clique.  It therefore suffices to prove equivalence
of \(q\)-colourability.

Suppose that \(c\) is a proper \(q\)-colouring of \(J(2m,m)\), on a point
set \(X\).  The \(m+1=q-1\) blocks through an \((m-1)\)-set \(T\) have
distinct colours.  Denote the unique missing colour by \(d(T)\).

Fix an \((m-2)\)-set \(R\).  Colour the edge \(xy\) of the complete graph
on the \(q\) points \(X\setminus R\) by \(c(R\cup\{x,y\})\).  This is a
proper \(q\)-edge-colouring of \(K_q\).  Since \(q\) is odd, each colour
class is a matching of size at most \((q-1)/2\); equality in the total edge
count forces every colour class to have that size.  Each therefore misses
one vertex, and the missing vertices are distinct because the \(q-1\)
edges at any fixed vertex have distinct colours.  Consequently
\[
 x\longmapsto d(R\cup\{x\})
\]
is a bijection.  Thus \(d\) is an \(LS(m-2,m-1,2m)\).

For an \(m\)-set \(S\), the \(m\) facet colours
\[
 d(S\setminus\{x\}),\qquad x\in S,
\]
are distinct, because \(d\) is proper, and none equals \(c(S)\).  Let
\(e(S)\) be the unique colour other than \(c(S)\) omitted by these \(m\)
facet colours.  We claim that
\[
 e(S)=c(S^c). \tag{1}
\]

The local \(K_q\) calculation shows that every colour class
\(\mathcal C_a\) is an \((m-2)\)-design, with
\[
 \lambda_i(\mathcal C_a)
 =\frac{\binom{2m-i}{m-i}}q,\qquad 0\le i\le m-2.
\]
If \(S\in\mathcal C_a\), inclusion-exclusion counts the colour-\(a\)
blocks disjoint from \(S\) as
\[
 \frac1q\sum_{i=0}^{m-2}(-1)^i
 \binom mi\binom{2m-i}{m-i}+m-1=0.
\]
Here the \(m\) terms of size \(m-1\) each contribute \(+1\), while \(S\)
itself contributes \(-1\), since \(m\) is odd.  The numerical equality
follows by completing the sum through \(i=m\): the complete alternating
sum counts all \(m\)-sets disjoint from \(S\) and equals \(1\), while its
last two terms sum to \(m(m+1)-1\).  Thus \(S^c\notin\mathcal C_a\).

Now let
\[
 \mathcal D_a=\{T\in\binom X{m-1}:d(T)=a\}.
\]
This is an \(S(m-2,m-1,2m)\), with
\[
 \lambda_i(\mathcal D_a)
 =\frac{\binom{2m-i}{m-1-i}}q,\qquad 0\le i\le m-2.
\]
Because \(S\) itself has colour \(a\), no facet \(S\setminus\{x\}\)
belongs to \(\mathcal D_a\).  Inclusion-exclusion therefore gives
\[
 \#\{T\in\mathcal D_a:T\cap S=\varnothing\}
 =\frac1q\sum_{i=0}^{m-2}(-1)^i
 \binom mi\binom{2m-i}{m-1-i}=0.
\]
Indeed the corresponding complete sum through \(i=m-1\) counts all
\((m-1)\)-sets disjoint from \(S\) and equals \(m\), while its final term
is already \(m\).  Hence no facet of \(S^c\) has missing colour \(a\):
the colour \(a\) is available at \(S^c\).  Since \(c(S^c)\ne a\), it
follows that \(e(S^c)=a=c(S)\).  Replacing \(S\) by \(S^c\) proves (1).

Complementation is an automorphism of \(J(2m,m)\), so (1) shows immediately
that \(e\) is proper.  For a fixed \((m-1)\)-set \(T\), the \(q-1\)
values \(e(T\cup\{x\})\), \(x\in X\setminus T\), are distinct, and none
equals \(d(T)\), because \(d(T)\) is one of the forbidden facet colours.
Thus they are exactly the colours other than \(d(T)\), so \(e\) has the
same missing map \(d\).

Adding one point \(\infty\), define
\[
 F(S)=c(S),\qquad F(\{\infty\}\cup T)=d(T).
\]
If an \((m-1)\)-star is based at \(T\subset X\), its \(q-1\) old members
use every colour except \(d(T)\), and its member containing \(\infty\)
uses \(d(T)\).  If it is based at \(\{\infty\}\cup R\), its colours are
the \(q\) values \(d(R\cup\{x\})\).  Hence \(F\) properly colours
\(J(2m+1,m)\).

For the two-point lift, add new points \(\alpha,\beta\) and define
\[
\begin{aligned}
 C(\{\alpha,\beta\}\cup T)&=d(T)
   &&(|T|=m-1),\\
 C(\{\alpha\}\cup S)&=c(S)
   &&(|S|=m),\\
 C(\{\beta\}\cup S)&=e(S)=c(S^c)
   &&(|S|=m),\\
 C(U)&=d(X\setminus U)
   &&(U\subset X,\ |U|=m+1).
\end{aligned}
\]
Every \(m\)-star is rainbow, as follows.

- A base \(\{\alpha,\beta\}\cup R\), \(|R|=m-2\), receives the \(q\)
  colours \(d(R\cup\{x\})\).
- A base \(\{\alpha\}\cup T\), \(|T|=m-1\), receives \(d(T)\) after
  adding \(\beta\), and receives the \(q-1\) colours
  \(c(T\cup\{x\})\) after adding \(x\in X\setminus T\).
- A base \(\{\beta\}\cup T\) similarly receives \(d(T)\) after adding
  \(\alpha\), and the \(q-1\) colours \(e(T\cup\{x\})\) otherwise.
- A base \(T\subset X\), \(|T|=m\), receives \(c(T)\) after adding
  \(\alpha\), \(c(T^c)=e(T)\) after adding \(\beta\), and
  \[
  d(T^c\setminus\{x\}),\qquad x\in T^c,
  \]
  after adding \(x\).  These are precisely the two available colours of
  \(T^c\) together with its \(m\) distinct facet colours.

This gives a \(q\)-colouring of \(J(2m+2,m+1)\).  Conversely, a colouring
of \(J(2m+1,m)\) restricts to the \(m\)-sets avoiding the added point,
and a colouring of \(J(2m+2,m+1)\) restricts to the sets containing one
fixed point; removing that point gives \(J(2m+1,m)\).  Together with the
lower bounds above, this proves the three asserted equalities. \(\square\)

For the original candidate \(k=p-1\), take \(m=k-1=p-2\).  Thus proving
\(\chi(J(2p-4,p-2))\ge p+1\) is not an easier sufficient route: it is
exactly equivalent to ruling out the original \(p\)-colouring.
There is no conflict with the complement closure in Section 4: that result
applies to the even parameter \(k\), whereas the starting parameter \(m\)
in this theorem is odd; the two-point lift returns to the even middle layer.

The lift also forces a useful second-order regularity.  Let
\(N=\binom{2m}{m}\), and for \(a\ne b\) let \(n_{ab}\) count the \(m\)-sets
\(S\) with \(c(S)=a\) and \(c(S^c)=b\).  Then
\[
 \boxed{n_{ab}=\frac{N}{q(q-1)}\quad\text{for every }a\ne b.} \tag{2}
\]
For a fixed \(S\) of colour \(a\), group its neighbours into the \(m\)
rows indexed by \(x\in S\).  The row through the facet
\(S\setminus\{x\}\) contains one neighbour of colour \(b\), unless
\(d(S\setminus\{x\})=b\), in which case it contains none.  The \(m\)
facet colours of \(S\) are exactly all colours except
\(a\) and \(c(S^c)=e(S)\).  Hence \(S\) has \(m\) neighbours of colour
\(b\) when \(c(S^c)=b\), and \(m-1\) otherwise.  Summing over the
\(N/q\) sets of colour \(a\), the number of ordered adjacent
\((a,b)\)-pairs is
\[
 \frac Nq(m-1)+n_{ab}.
\]
On the other hand, an \((m-1)\)-set contributes one such ordered pair
exactly when its missing colour is neither \(a\) nor \(b\).  Since every
missing-colour class has size \(\binom{2m}{m-1}/q\), this count is
\[
 \frac{q-2}{q}\binom{2m}{m-1}
 =\frac{Nm^2}{q(m+1)}.
\]
Therefore
\[
 n_{ab}
 =\frac Nq\left(\frac{m^2}{m+1}-(m-1)\right)
 =\frac{N}{q(m+1)}
 =\frac{N}{q(q-1)}.
\]
This proves (2).  Thus complementary pairs form the
complete multigraph on the \(q\) colours with the same multiplicity on every
edge.  All resulting pairwise intersection numbers and Johnson-scheme
positivity conditions are nevertheless nonnegative and integral in every
prime case; this regularity is a genuine theorem, not yet a contradiction.

## 5. What is known for the small candidates

- \(3\le k\le8\) are ruled out.  Composite \(k+1\) are covered by the prime
  obstruction; the exceptional even cases are also known not to attain the
  clique bound.
- For \(k=4\), derivation would give \(LS(2,3,7)\), but at most two labelled
  Fano planes can be pairwise block-disjoint, far short of the five required.
  The accompanying `verify_k4.py` independently obtains the same maximum by
  generating all 30 labelled \(S(3,4,8)\) systems.
- For \(k=6\), the Witt system \(S(5,6,12)\) exists, but no required
  seven-colouring exists: Kramer and Mesner proved that at most two such
  systems can be mutually disjoint.
- \(k=10\) is ruled out because an \(S(9,10,20)\) would derive five times to
  an \(S(4,5,15)\), which Mendelsohn and Hung proved nonexistent.
- \(k=12\) is ruled out because an \(S(11,12,24)\) would derive seven times
  to an \(S(4,5,17)\), whose nonexistence was proved computationally by
  Östergård and Pottonen.
- Therefore the first open case is
  \[
    \boxed{k=16},
  \]
  requiring \(LS(15,16,32)\), and hence also \(LS(4,5,21)\) and
  \(LS(3,4,20)\).

If \(k=16\) is eventually ruled out, the next candidate is \(k=18\).  The
single-design derivation tactic no longer kills it: the relevant low-level
systems include the known \(S(4,5,23)\) and \(S(5,6,24)\).  Progress beyond
\(k=16\) therefore needs a large-set compatibility obstruction or an argument
uniform in \(k\), not only finite elimination of one derived constituent.

The existence of even one \(S(4,5,21)\) remains unresolved.  The paper of
Kiermaier, Krčadinac, and Wassermann concerns extensions of Steiner
3-designs; it does not report an exhaustive search for \(S(4,5,21)\).
An earlier draft of this note overstated its scope.  No computational
nonexistence evidence for a constituent \(S(4,5,21)\) is claimed here.

## 6. The most promising next attacks

The literature and the reductions above leave three concrete routes.

1. **Compatible derived designs.**  Attack the induced
   \(LS(4,5,21)\), not a lone \(S(4,5,21)\).  The large-set constraints are
   strictly stronger and are small enough to formulate as exact cover or
   integer linear programming.  Tactical decompositions offer a natural
   symmetry-aware search.

   There is no automatic converse that lifts a lower large set one level.
   Indeed \(LS(1,2,6)\) exists by a one-factorization of \(K_6\), whereas
   \(LS(2,3,7)\) does not: an independent enumeration of all 30 labelled
   Fano planes finds at most two pairwise disjoint systems, rather than the
   five required.  To lift
   \(LS(t,t+1,v)=\{\mathcal D_i\}\), one must choose residual families
   \(\mathcal R_i\) of \((t+2)\)-sets on the old points such that a
   \((t+1)\)-set \(U\) is covered zero times by \(\mathcal R_i\) when
   \(U\in\mathcal D_i\), exactly once otherwise, and the
   \(\mathcal R_i\) partition all \((t+2)\)-sets.  Repeating that simultaneous
   compatibility for eleven levels is essentially the missing problem.

2. **Odd-graph covering obstruction.**  A hypothetical solution partitions
   \(O_{16}\) into 17 perfect codes and makes \(O_{16}\) a
   \(17{,}678{,}835\)-sheeted cover of \(K_{17}\).  Its matchings between
   every pair of fibres must also reproduce the distance-regular
   intersection numbers and odd girth 31 of \(O_{16}\).  A contradiction
   from lifted triangles/6-cycles or from the Terwilliger algebra would rule
   out the whole compatible structure at once.  Concretely, the monodromy
   around any triangle of \(K_{17}\) can have no odd cycle of length below
   11: such a cycle of length \(r\) would lift to an odd cycle of length
   \(3r<31\) in \(O_{16}\).

3. **An exact finite-field nonlinear formulation.**  Label the colours by
   \(\mathbb F_p\), where \(p=k+1\), and let \(W\) be the inclusion matrix
   from \((k-1)\)-sets to \(k\)-sets.  Then a nonconstant function
   \(c:\binom{[2k]}k\to\mathbb F_p\) is a required colouring if and only if
   \[
     c,c^2,\ldots,c^{p-2}\in\ker_{\mathbb F_p}W. \tag{3}
   \]
   The forward implication follows by summing powers over each rainbow
   \(p\)-set star.

   Conversely, fix a star and let \(n_z\) be the multiplicity of
   \(z\in\mathbb F_p\) among its \(p\) values.  Equation (3), together with
   \(\sum_z n_z=p=0\) in \(\mathbb F_p\), says that
   \[
     \sum_z n_z z^a=0\qquad(0\le a\le p-2).
   \]
   The truncated Vandermonde matrix has one-dimensional nullspace, spanned
   by the all-one vector.  Since \(0\le n_z\le p\) and \(\sum_z n_z=p\),
   the star is therefore either rainbow or monochromatic.

   A monochromatic star propagates.  Around a fixed \((k-2)\)-set, regard
   the \(k\)-sets as the edges of \(K_{p+1}\) and its \((k-1)\)-stars as
   the vertices.  If one vertex is monochromatic in colour \(a\) and all
   others were rainbow, deleting it would give a proper edge-colouring of
   the odd complete graph \(K_p\) with only \(p-1\) colours, impossible.
   A second monochromatic vertex also has colour \(a\), after which no
   remaining vertex can be rainbow because it sees colour \(a\) twice.
   Hence every star around that \((k-2)\)-set is monochromatic in colour
   \(a\).  Connectivity of \(J(2k,k-1)\) then makes \(c\) globally
   constant.  Thus a nonconstant solution of (3) has every star rainbow,
   proving the equivalence.

   Over \(\mathbb C\), even one character
   \(\exp(2\pi i c/p)\) lying in \(\ker W\) is already equivalent to the
   colouring condition: a vanishing sum of \(p\) \(p\)-th roots of unity
   contains each root exactly once.  Its nontrivial powers are merely Galois
   conjugates.  They do not provide additional simultaneous constraints;
   the genuinely nonlinear formulation is (3).

## 7. A concrete cyclic attack and a proved dihedral obstruction

The accompanying `search_cyclic_ls_4_5_21.py` tests a natural construction
suggested by the prime \(17\).  Let \(\mathbb Z_{17}\) act regularly on
seventeen points and fix four more, and require translation by one to add one
to the colour.

Every orbit of five-sets has size 17.  Choosing the colour-zero member of each
orbit is therefore equivalent to choosing 1,197 blocks, one from each orbit,
so that every one of the 5,985 four-sets is covered once.  This is an exact
cover model with 20,349 Boolean choices and 7,182 exact-one constraints.
Conversely, any solution is an \(S(4,5,21)\) whose seventeen translates
partition all five-sets, hence a cyclic \(LS(4,5,21)\).

In fact, this captures every order-17 symmetry: an order-17 permutation of
21 points must be one 17-cycle with four fixed points.  It fixes no five-set,
so every five-set orbit has length 17.  It therefore cannot fix a large-set
class, since a class has 1,197 blocks, not divisible by 17; instead it cycles
the seventeen classes.  An `INFEASIBLE` result would rule out every
\(LS(4,5,21)\) with an automorphism of order 17, though it would say nothing
about asymmetric large sets.

Every constituent design has a unique block through the four fixed points.
Translation lets us normalize this block to
\(\{0,\infty_1,\infty_2,\infty_3,\infty_4\}\), removing a harmless
17-fold symmetry.  A five-minute CP-SAT run of this normalized model explored
2,952,703 branches and 1,800,519 conflicts.  It returned `UNKNOWN`: neither a
construction nor a nonexistence proof.  The linearized system is consistent
over \(\mathbb F_2\), of rank 5,757, so there is no immediate parity
contradiction.

Adding the natural reflection \(x\mapsto-x\) makes the model infeasible.  This
restricted nonexistence has a short proof independent of the solver.

**Five-fixed-point involution lemma.**  An \(S(4,5,21)\) cannot admit an
involution fixing exactly five points.

**Proof.**  Let \(F\) be the five fixed points and let \(P=\{x,x'\}\) be one
of the transposed pairs.  For every two-set \(A\subset F\), the invariant
four-set \(P\cup A\) lies in a unique block.  Uniqueness forces this block to
be invariant under the involution.  Since it already contains the full
transposed pair \(P\), its fifth point must be a fixed point.  Removing \(P\)
from these blocks would therefore give triples on \(F\) in which every pair
of \(F\) occurs exactly once: an \(S(2,3,5)\).  Such a system would have
\(\binom52/\binom32=10/3\) blocks, impossible. \(\square\)

There is also a clean restriction at the level of the entire large set.

**Large-set involution theorem.**  If an \(LS(4,5,21)\) admits a nonidentity
involution on its points which permutes its seventeen constituent designs,
then that involution fixes exactly one point.

**Proof.**  Let \(f\) be the number of fixed points.  Since the involution
acts on 21 points, \(f\) is odd.  It also induces an involution on the
seventeen classes; let \(h\) be the number of fixed classes, which is again
odd.

Let \(A\) be an invariant four-set containing \(a\) fixed points.  In every
class there is a unique five-set extending \(A\).  Such an extension is
invariant exactly when the class is fixed: one direction is uniqueness
inside a fixed class, and the other follows because the classes partition
all five-sets.  Hence \(A\) has exactly \(h\) invariant extensions.
An invariant five-set extending \(A\) must add one fixed point outside
\(A\), so it has exactly \(f-a\) invariant extensions.  Therefore
\[
 h=f-a \tag{4}
\]
for every invariant four-set \(A\).

If \(3\le f\le17\), then \((21-f)/2\ge2\), so invariant four-sets exist
with \(a=0\) (two transposed pairs) and with \(a=2\) (two fixed points and
one transposed pair).  If \(f=19\), invariant four-sets exist with \(a=2\)
and \(a=4\).  In either case (4) gives two different values for the same
\(h\), a contradiction.  Since a nonidentity involution cannot have
\(f=21\), only \(f=1\) remains. \(\square\)

Kolotoğlu and Magliveras proved the stronger published classification for a
single hypothetical \(S(4,5,21)\): its full automorphism group can have order
only \(1,2,3,4,5,6,7,\) or \(10\).  The theorem above instead constrains the
induced action on all seventeen classes simultaneously.

The reflection in the attempted dihedral construction fixes zero in
\(\mathbb Z_{17}\) and the four extra points, so the lemma rules it out.  A
merely cyclic \(LS(4,5,21)\) remains undecided.  More generally, every
nontrivial subgroup of the multiplier group
\(\mathbb F_{17}^{\times}\) contains this reflection (the multiplier group
has order \(16\)).  On the seventeen colours, such a reflection has a fixed
colour and hence stabilizes its constituent design, contradicting the lemma.
Thus an order-17 solution cannot extend to the natural affine symmetry.

### 7.1 Further symmetry and binary construction obstructions

A useful general observation rules out several large prime cycles.

**Large-prime-cycle lemma.**  Suppose a point permutation \(g\) of prime
order \(\ell>q\) preserves a proper \(q\)-colouring of a Johnson graph up
to a permutation of the colours.  If some vertex \(S\) is adjacent to
\(gS\), then no such colouring exists.

Indeed the induced colour permutation has order dividing \(\ell\).  A
permutation of fewer than \(\ell\) objects cannot have order \(\ell\), so
it is the identity; but then the adjacent vertices \(S\) and \(gS\) have
the same colour.  For \(J(32,16)\), this excludes point automorphisms of
prime order \(19,23,29,\) or \(31\): take sixteen consecutive points on
the prime cycle.  It also shows that the forced \(LS(3,4,20)\) cannot have
a 19-cycle.  On \(\mathbb Z_{19}\cup\{\infty\}\), the consecutive blocks
\(\{0,1,2,3\}\) and \(\{1,2,3,4\}\) make the contradiction explicit.

The identity \(32=2^5\) suggests putting the points on
\(V=\mathbb F_2^5\).  Two especially natural versions of that idea can be
excluded completely.

**Affine-equivariance theorem.**  There is no proper 17-colouring of
\(J(32,16)\) which is equivariant under
\(\operatorname{AGL}(5,2)\), even when the affine group is allowed to
permute the colours.

Here is the essential argument.  All 31 nonzero translations are conjugate.
If each fixes \(F\) of the seventeen colours, Burnside's lemma for the
translation group gives
\[
 \frac{17+31F}{32}\in\mathbb Z,
\]
so \(F=17\).  The colour action therefore factors through
\(\operatorname{GL}(5,2)\).  That group is simple and has an element of
order 31, whereas \(S_{17}\) has none; hence its colour action is also
trivial.

Every colour class would consequently be affine-invariant.  Its block count
is
\[
 \frac{\binom{32}{16}}{17}=35{,}357{,}670\equiv2\pmod4.
\]
Translation orbits on 16-sets have power-of-two sizes and no fixed
16-set, so each class must contain a translation orbit of size two.  Such
an orbit is exactly the pair of cosets of a four-dimensional hyperplane.
The linear group is transitive on the 31 hyperplane directions, forcing
every colour class to contain all 62 affine hyperplanes, contrary to
disjointness.

**XOR-fusion theorem.**  Let
\[
 \sigma(S)=\mathop{\mathrm{XOR}}_{x\in S}x\in\mathbb F_2^5.
\]
Although \(\sigma\) properly colours \(J(32,16)\) with 32 colours, no map
\(h:\mathbb F_2^5\to[17]\) makes \(h\circ\sigma\) proper.

Indeed choose distinct syndromes \(u,v\) fused by \(h\), put \(d=u+v\),
and take \(x,y\) with \(x+y=d\).  A character calculation shows that,
after deleting \(x,y\), the number of 15-subsets with any prescribed XOR
is either
\[
 4{,}850{,}640\quad\text{or}\quad4{,}847{,}208,
\]
and is therefore always positive.  Choose \(T\) with
\(\sigma(T)=u+x\).  The adjacent sets \(T\cup\{x\}\) and
\(T\cup\{y\}\) then have syndromes \(u\) and \(v\), producing a colour
collision.

The complete proofs, including the character sum and an exact verifier, are
in `evidence/constructive_no_go.md`.  These theorems do not exclude a
smaller-symmetry or genuinely higher-order construction.

## 8. Bottom line

The requested colouring is not presently solved in the literature, and this
work does not pretend otherwise.  The defensible complete conjecture is:

\[
\boxed{\text{No }LS(k-1,k,2k)\text{ exists for }k>2.}
\]

The strongest rigorously supported frontier is now \(k=16\), equivalently
the nonexistence of a covering \(O_{16}\to K_{17}\), with the compatible
derived large sets \(LS(4,5,21)\) and \(LS(3,4,20)\) as smaller shadows.

## Sources

- T. F. Bloom, [Erdős Problem #835](https://www.erdosproblems.com/835) and
  its [discussion thread](https://www.erdosproblems.com/forum/thread/835).
- J. Ma and Q. Tang,
  [A Note on Erdős Problem #835](https://github.com/QuanyuTang/erdos-problem-835/blob/main/On_Problem_835.pdf).
- P. Hammond and D. H. Smith,
  [Perfect codes in the graphs \(O_k\)](https://doi.org/10.1016/0095-8956(75)90087-8),
  *J. Combinatorial Theory, Series B* 19 (1975), 239–255.
- E. S. Kramer and D. M. Mesner,
  [Intersections among Steiner systems](https://doi.org/10.1016/0097-3165(74)90054-5),
  *J. Combinatorial Theory, Series A* 16 (1974), 273–285.
- N. S. Mendelsohn and S. H. Y. Hung, *On the Steiner systems
  \(S(3,4,14)\) and \(S(4,5,15)\)*, *Utilitas Mathematica* 1 (1972), 5–95.
- P. R. J. Östergård and O. Pottonen,
  [There exists no Steiner system \(S(4,5,17)\)](https://doi.org/10.1016/j.jcta.2008.04.005),
  *J. Combinatorial Theory, Series A* 115 (2008), 1570–1573.
- E. Kolotoğlu and S. S. Magliveras,
  [On the possible automorphism groups of a Steiner quintuple system of
  order 21](https://doi.org/10.1002/jcd.21370),
  *Journal of Combinatorial Designs* 22 (2014), 495–505.
- M. Kiermaier, V. Krčadinac, and A. Wassermann,
  [Steiner 3-designs as extensions](https://arxiv.org/abs/2509.23483),
  *Designs, Codes and Cryptography* 94 (2026), article 157.
- M. A. Fiol,
  [A new class of polynomials from the spectrum of a graph, and its
  application to bound the \(k\)-independence
  number](https://arxiv.org/abs/1907.08626).
- T. Etzion and J. Zhou,
  [Large Sets with Multiplicity](https://arxiv.org/abs/2007.09608).
- S. F. Jørgensen,
  [On the clique covering numbers of Johnson
  graphs](https://arxiv.org/abs/2502.15019).
