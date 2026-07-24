# Erdős–Rosenfeld Problem #835: a researched conjectural resolution

## Honest status

This note gives a complete statement of a negative conjecture, proves several
reductions that substantially narrow it, and independently verifies the first
exceptional case.  It does **not** prove the still-open conjecture.

As of 23 July 2026, the Erdős Problems database still marks Problem #835
open.  Its discussion contains no accepted solution.  Exact recent searches
on X/Twitter found no announcement under the problem number, the Johnson-graph
formulation, or the Steiner-system formulation.  The available X API covered
only the preceding seven days, so that search is evidence rather than a
logical guarantee.

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

The July 2026 paper of Kiermaier, Krčadinac, and Wassermann reports extensive
unsuccessful searches for even one \(S(4,5,21)\), but explicitly cautions
that these computations provide little evidence of nonexistence.

## 6. The most promising next attacks

The literature and the reductions above leave three concrete routes.

1. **Compatible derived designs.**  Attack the induced
   \(LS(4,5,21)\), not a lone \(S(4,5,21)\).  The large-set constraints are
   strictly stronger and are small enough to formulate as exact cover or
   integer linear programming.  Tactical decompositions, recommended in the
   2026 extension paper, offer the most plausible symmetry-aware search.

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

3. **Finite-field moment obstruction.**  Label the colours by
   \(\mathbb F_p\), where \(p=k+1\).  For every \((k-1)\)-set \(T\), the map
   \[
     x\longmapsto c(T\cup\{x\})
   \]
   from the \(p\) available points to \(\mathbb F_p\) is a permutation.
   Consequently, for \(1\le a\le p-2\),
   \[
     \sum_{x\notin T} c(T\cup\{x\})^a=0.
   \]
   Thus the powers \(c^a\), \(1\le a\le p-2\), lie in the same top
   inclusion-matrix kernel over \(\mathbb F_p\).  Classifying
   \(\mathbb F_p\)-valued functions with all these nonlinear kernel
   constraints would prove the conjecture.  Equivalently over
   \(\mathbb C\), the \(p-1\) nontrivial character functions
   \(\exp(2\pi i a c/p)\) all lie in the top Johnson eigenspace.  Ordinary
   Hoffman/Johnson bounds do not see these simultaneous power constraints.

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

The reflection in the attempted dihedral construction fixes zero in
\(\mathbb Z_{17}\) and the four extra points, so the lemma rules it out.  A
merely cyclic \(LS(4,5,21)\) remains undecided.  More generally, every
nontrivial subgroup of the multiplier group
\(\mathbb F_{17}^{\times}\) contains this reflection (the multiplier group
has order \(16\)).  On the seventeen colours, such a reflection has a fixed
colour and hence stabilizes its constituent design, contradicting the lemma.
Thus an order-17 solution cannot extend to the natural affine symmetry.

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
- E. S. Kramer and D. M. Mesner,
  [Intersections among Steiner systems](https://doi.org/10.1016/0097-3165(74)90054-5),
  *J. Combinatorial Theory, Series A* 16 (1974), 273–285.
- N. S. Mendelsohn and S. H. Y. Hung, *On the Steiner systems
  \(S(3,4,14)\) and \(S(4,5,15)\)*, *Utilitas Mathematica* 1 (1972), 5–95.
- P. R. J. Östergård and O. Pottonen,
  [There exists no Steiner system \(S(4,5,17)\)](https://doi.org/10.1016/j.jcta.2008.04.005),
  *J. Combinatorial Theory, Series A* 115 (2008), 1570–1573.
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
