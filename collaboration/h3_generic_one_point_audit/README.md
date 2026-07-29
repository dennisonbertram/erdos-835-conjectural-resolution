# Independent audit of the generic one-point lift

## Verdict

The generic one-point theorem is correct, including the stated boundary
case \(s=1\), provided that a large set has its \(m\) constituent Steiner
systems labelled by the \(m\) colours.  For the usual unlabelled notion of a
large set, the statement is a bijection only after quotienting colourings by
colour permutations.

The pre-remediation verifier snapshot
`collaboration/opus5/generic_radius4_certificate_attack/verify_generic_one_point_lift.py`
ran successfully with `43/43 checks passed`.  (The Opus artifact continued
changing during this independent audit, so that count is a snapshot, not the
final suite count.)  Its finite checks were
consistent with the theorem, but they do not constitute its general proof
and leave two real coverage gaps:

1. the theorem says \(s\geq1\), while every parameter loop and round-trip
   test starts at \(s=2\);
2. the real-object “rebuilds exactly” checks compare only the unlabelled set
   of colour classes, so a bug that permuted class labels would pass.

The independent verifier in this directory covers \(s=1\) in both
directions with labels retained.  It also independently enumerates every
labelled \(SQS(10)\) and \(S(4,5,11)\), proving
\[
 D(10)=5,\qquad
 \max\{\hbox{pairwise disjoint }S(4,5,11)\}=2.
\]
These values are classical, not new: Etzion--Hartman (1991) explicitly
attribute both results to Kramer and Mesner.

A direct smoke call to the pre-remediation implementation at \(s=1\), for
\(m=3,5,7\), also passes completion, large-set validation, and exact
restriction.  Thus this was a missing test/proof branch, not an implementation
failure.

## 1. Exact statement

Let \(m\geq3\) be odd, let \(s\geq1\), and put
\[
 n=m+s-2,\qquad v=n+1=m+s-1.
\]
Fix an \(n\)-set \(X\), a new point \(\infty\), and a colour set
\({\cal Q}\) of size \(m\).

There is a bijection between

- proper maps \(c:\binom Xs\to{\cal Q}\), and
- labelled large sets
  \(({\cal D}_i)_{i\in{\cal Q}}\) of type \(LS(s-1,s,v)\)
  on \(X\cup\{\infty\}\).

The forward map adjoins the point using the missing-colour map
\[
 \psi(T)={\cal Q}\setminus
 \{c(T\cup\{x\}):x\in X\setminus T\},
 \qquad T\in\binom X{s-1}.                               \tag{1}
\]
The reverse map deletes \(\infty\) and colours each remaining block by the
label of its large-set member.

## 2. Proof from a colouring to a large set

Every star over \(T\in\binom X{s-1}\) has
\[
 |X\setminus T|=n-s+1=m-1
\]
members.  It is a clique in \(J(n,s)\), so its colours are distinct and
there is a unique missing colour.  Thus (1) is well defined.  Define
\[
 {\cal D}_i=
 \{B\in\textstyle\binom Xs:c(B)=i\}
 \ \cup\
 \{\{\infty\}\cup T:\psi(T)=i\}.                         \tag{2}
\]
The families in (2) plainly partition all \(s\)-subsets.  It remains to
prove that every \((s-1)\)-set lies in exactly one block of each family.

First let \(T\subset X\), \(|T|=s-1\).  Its \(m-1\) unrooted extensions
have every colour except \(\psi(T)\), exactly once.  Its rooted extension
\(\{\infty\}\cup T\) has colour \(\psi(T)\).  Hence \(T\) has one
extension in each \({\cal D}_i\).

Now suppose \(s\geq2\), and consider a rooted \((s-1)\)-set
\(\{\infty\}\cup R\), where \(|R|=s-2\).  Put \(Y=X\setminus R\); then
\(|Y|=m\).  Colour the edge \(xy\) of \(K_Y\) by
\[
 c(R\cup\{x,y\}).
\]
This is a proper edge-colouring with the palette \({\cal Q}\).  Each colour
class is a matching of size at most \((m-1)/2\).  Since
\[
 |E(K_m)|=\frac{m(m-1)}2
\]
is exactly \(m\) times this bound, every colour class is a maximum matching
and misses exactly one vertex.  Consequently the deficiency map
\[
 x\longmapsto \psi(R\cup\{x\})
\]
is a bijection \(Y\to{\cal Q}\): the colour missing at vertex \(x\) is
precisely \(\psi(R\cup\{x\})\), and every colour misses one vertex.
Therefore \(\{\infty\}\cup R\) also has exactly one extension in every
\({\cal D}_i\).

For \(s=1\) there is no \(R\) of size \(-1\).  The graph
\(J(m-1,1)=K_{m-1}\) receives \(m-1\) distinct colours, and (2) assigns
the new singleton \(\{\infty\}\) the unique missing colour.  Each
\({\cal D}_i\) is one singleton, exactly an \(S(0,1,m)\).  Thus the
boundary case is valid without invoking the edge-colouring lemma.  In
fact, only at \(s=1\), oddness of \(m\) is unnecessary.

## 3. Proof in the reverse direction and mutual inverse

Let \(({\cal D}_i)_{i\in{\cal Q}}\) be a labelled
\(LS(s-1,s,v)\), delete \(\infty\), and colour every unrooted block by its
class label.  Two adjacent unrooted \(s\)-sets share an \((s-1)\)-set.
One Steiner system cannot contain both, so their colours differ.  The
restriction is a proper colouring.

Starting with a colouring, (2) leaves every unrooted block unchanged, so
deleting \(\infty\) returns the original colouring.

Conversely, start with a labelled large set.  For
\(T\in\binom X{s-1}\), suppose \(\{\infty\}\cup T\in{\cal D}_i\).
The Steiner property says that \({\cal D}_i\) has no unrooted block through
\(T\), while every other \({\cal D}_j\) has exactly one.  Thus \(i\) is
exactly the missing colour \(\psi(T)\), and (2) restores every rooted block
to its original labelled class.  The two maps are mutually inverse.

## 4. What “two points are lossy” proves

Deleting one point is exact at the special parameter
\(n=m+s-2\).  After deleting a second point, a star has only \(m-2\)
members, so it omits two colours and the canonical map (1) disappears.

The current verifier gives two valid strict examples:
\[
\begin{array}{c|c|c}
(m,s)&\text{two-point graph}&\text{nonexistent large set}\\ \hline
(5,3)&J(5,3)\cong L(K_5)\text{ is 5-colourable}&LS(2,3,7)\\
(5,4)&J(6,4)\cong L(K_6)\text{ is 5-colourable}&LS(3,4,8).
\end{array}
\]
The independent verifier constructs both colourings explicitly and
enumerates all relevant Fano planes and \(SQS(8)\)'s to check that the
required large sets do not exist.

This establishes that a two-point analogue is lossy **in general**: its
smaller search space can contain false positives.  It does not establish
that every two-point restriction at every parameter is noninjective, so
“exactly one point may be deleted” should not be read as a universal
pointwise claim.

## 5. Exact correction to Section F2

The audited Section F2 said that every point restriction “of the top-level
colouring” is a colouring of \(J(n,k-1)\).  That is not true for direct
restrictions of the original colouring on \(J(2k,k)\): retaining an
\(n\)-set gives \(J(n,k)\), not \(J(n,k-1)\).  Nor does repeatedly deleting
points from the one-point formulation \(J(2k-1,k)\) change the block size
from \(k\) to \(k-1\).

The correct statement is:

1. Fix \(\infty\) and first form the derived/link colouring
   \[
   \phi(A)=c(\{\infty\}\cup A),
   \qquad A\in\binom{V\setminus\{\infty\}}{k-1}.
   \]
   Equivalently, derive each member of
   \(LS(k-1,k,2k)\) at \(\infty\), obtaining
   \(LS(k-2,k-1,2k-1)\).
2. For \(Y\subseteq V\setminus\{\infty\}\), \(|Y|=n\), restrict
   \(\phi\) to \(J(n,k-1)\).
3. Complementation inside \(Y\) identifies this graph with \(J(n,s)\),
   where
   \[
   s=n-k+1,\qquad n=(k+1)+s-2.
   \]
   The one-point theorem now identifies this restricted **link**
   colouring with
   \[
   LS(n-k,n-k+1,n+1),
   \]
   the tower rung \(t=n-k\).

At \(n=2k-1\), \(J(2k-1,k-1)\) happens to be complement-isomorphic to the
one-point graph \(J(2k-1,k)\).  For smaller \(n\), this coincidence no
longer holds.  The tower conclusion is valid after the above correction;
the direct-restriction wording is an overclaim.

There is also an important quantifier on “never stronger.”  For each
**fixed** root \(\infty\), retained set \(Y\), and size \(n\), the standalone
existence of the resulting \(J(n,s)\) colouring is exactly equivalent to
existence of the one tower rung.  It does not follow that an arbitrary
colouring of that rung extends to the top.  Nor does the theorem remove the
simultaneous compatibility conditions among the restrictions for different
roots or overlapping retained sets.  A joint test of several restrictions
can therefore be stronger even though each restriction considered in
isolation is not.  Section F2 should state these quantifiers explicitly.

## 6. Independent small-tower computation

`verify_generic_one_point_audit.py` uses a different exact algorithm from
the current tower script:

1. columns are all \(t\)-subsets and rows all \((t+1)\)-subsets;
2. an integer-bitset Algorithm X enumerates every exact cover;
3. an independent orbit traversal under adjacent point transpositions
   confirms that the enumerated systems form one labelled isomorphism
   orbit;
4. because the disjointness graph is vertex-transitive, one system is fixed;
5. an exhaustive maximum-clique search is run on its mate graph.

The upper bound is exact, not a heuristic consequence of the displayed
witness.  Given any global disjoint family, transitivity moves one of its
members to the fixed system.  Every remaining member is then a vertex of
the fixed system's mate graph, and those vertices form a clique.  Conversely,
the fixed system together with any clique in its mate graph is a global
disjoint family.  Hence
\[
\omega(G)=1+\omega(G[N(D_0)]).
\]
The verifier's include/exclude recursion exhausts every clique of
\(G[N(D_0)]\), while the returned masks independently validate the matching
lower-bound family.  This proves both sides of each reported maximum.

The exact results are
\[
\begin{array}{c|c|c|c|c}
\text{design}&\text{labelled systems}&\text{mates of a fixed system}&
\text{edges among mates}&\text{packing maximum}\\ \hline
S(2,3,7)&30&8&0&2\\
S(3,4,8)&30&8&0&2\\
S(3,4,10)&2520&144&576&5\\
S(4,5,11)&5040&144&0&2.
\end{array}
\]
For \(SQS(10)\), the mate graph has clique number \(4\), giving
\(D(10)=1+4=5\).  For \(S(4,5,11)\), no two mates of a fixed system are
disjoint, so no triple exists and the maximum is \(2\).

These computations independently reproduce the classical
Kramer--Mesner facts.  The audited `tower_profile.py` called \(D(10)=5\) a
“substantive new number.”  That was a mathematical novelty overclaim; the
corrected wording is “an independent exact reproduction of the classical
value \(D(10)=5\).”

One convenient published attribution is T. Etzion and A. Hartman,
[*Towards a Large Set of Steiner Quadruple
Systems*](https://doi.org/10.1137/0404018), SIAM J. Discrete Math. **4**
(1991), 182--195, which states that Kramer and Mesner proved \(D(10)=5\).

## Reproduction

```text
python3 -B collaboration/h3_generic_one_point_audit/verify_generic_one_point_audit.py
```
