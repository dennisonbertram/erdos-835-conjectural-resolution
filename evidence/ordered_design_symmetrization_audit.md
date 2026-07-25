# Ordered-design symmetrization audit for Erdős–Rosenfeld #835

## Result

Teirlinck's theorem does supply
\(\operatorname{LOD}(k-1,k,2k)\) whenever \(k+1\) is prime, including
\(k=16\).  It does **not** supply a colouring of \(J(2k,k)\).  The exact
failure is that coordinate symmetrization produces a *weighted* Steiner
system, not a set of blocks.  Neither canonical ordering, summing/producting
over all orders, Wilson's congruence, nor the direct coordinate-coherence
argument removes those weights.

This is a negative audit of a proposed bridge, not an impossibility theorem
for \(\operatorname{LS}(15,16,32)\).

## Source check

The primary bibliographic record is L. Teirlinck, *On large sets of disjoint
ordered designs*, **Ars Combinatoria 25** (1988), 31--37; the publisher's
[volume archive](https://combinatorialpress.com/ars/vol25/) identifies the
article and pages.  An openly available modern paper states the theorem in
the needed form: if
\[
 m=\prod_i p_i^{\alpha_i},\qquad \alpha_i(p_i-1)>t\quad\text{for all }i,
\]
then \(\operatorname{LOD}(t,t+1,t+m)\) exists; see Jin--Zhu--Gu--Sun,
[pp. 2--3](https://mdpi-res.com/d_attachment/mathematics/mathematics-10-04703/article_deploy/mathematics-10-04703-v2.pdf?version=1671424711).
The same source defines an LOD as a partition of all ordered
\(n\)-tuples, not of supports.  The 1988 article itself was not available as
an open full-text scan from its publisher, so no unverified formula has been
attributed to it here.

Put \(t=k-1\), \(m=k+1\).  For prime \(p=k+1\), the condition is
\(p-1>p-2\), giving
\[
 \operatorname{LOD}(k-1,k,2k).
\]
In particular it gives \(\operatorname{LOD}(15,16,32)\).  It also gives
\(\operatorname{LOD}(5,6,12)\), a useful adversarial control.

## Exact symmetrization identity

Let \(A_0,\ldots,A_k\) be the ordered arrays in such an LOD.  For a
\(k\)-set \(B\), write
\[
 m_i(B)=\bigl|A_i\cap\operatorname{Ord}(B)\bigr|,
 \qquad \operatorname{Ord}(B)=\{\text{the }k!\text{ orderings of }B\}.
\tag{1}
\]
The LOD partition immediately gives
\[
 \sum_{i=0}^{k}m_i(B)=k!\quad\text{for every }B.
\tag{2}
\]
The OD condition gives the second, equally important, identity
\[
 \sum_{B\supset T}m_i(B)=k!
 \quad\text{for every }(k-1)\text{-set }T\text{ and every }i.
\tag{3}
\]
For (3), count pairs consisting of a column of \(A_i\) containing \(T\)
and the coordinate occupied by the unique point of \(B\setminus T\).
There are \(k\) choices of the omitted coordinate and \((k-1)!\) orders of
the remaining entries; the OD axiom supplies exactly one column for each
choice, giving \(k!\).  Grouping those columns by support gives the left
side.

Now apply every coordinate permutation to every column of \(A_i\), retaining
multiplicity.  Every ordering of a fixed support \(B\) occurs exactly
\(m_i(B)\) times.  Thus the symmetrized object is an \(S_k\)-invariant
ordered design with the integer weights \(m_i(B)\), and (3) says precisely
that its support is a weighted \(S(k-1,k,2k)\) of index \(k!\).

It becomes an ordinary Steiner system after dividing by \(k!\) **if and
only if**
\[
 m_i(B)\in\{0,k!\}\quad\text{for all }i,B.
\tag{4}
\]
Because of (2), (4) also says that all orderings of each support are in one
array.  This is exactly the missing support-orbit closure, not a consequence
of the ordered-design axioms.

## Why the proposed algebraic collapses do not work

For \(p=k+1\) prime, Wilson gives \(k!=(p-1)!\equiv-1\pmod p\).  Reducing
(2)--(3) modulo \(p\) gives only
\[
 \sum_i m_i(B)\equiv-1,\qquad
 \sum_{B\supset T}m_i(B)\equiv-1\pmod p.
\]
These linear congruences do not imply the nonlinear extreme condition (4).
For instance, a support split between two arrays has multiplicity vector
\((1,k!-1,0,\ldots,0)\), which obeys the first congruence but is not an
orbit.  The four-point control below realizes such splitting inside an actual
LOD.

Likewise, summing the array labels over all \(k!\) orders is only a function
of the vector \((m_i(B))_i\).  Coordinate symmetrization makes that function
well-defined on supports; it does not make it rainbow on stars.  A product
of labels in a cyclic group is the same construction after taking exponents,
so it has the same obstruction.

## Exhaustive \(k=2\) control

`verify_ordered_design_symmetrization.py` exhausts the four
\(\operatorname{LOD}(1,2,4)\)'s, viewed as partitions of the 12 directed
edges of \(K_4\) into three derangements.

* Exactly one is support-orbit closed: its three arrays are the directed
  versions of the three one-factors of \(K_4\).  Both sorted-coordinate
  evaluation and the sum over the two orders recover the true three-colouring.
* A non-orbit-closed LOD makes sorted-coordinate evaluation repeat a colour
  on a triangle.
* Another non-orbit-closed LOD makes the sum/product-over-orders rule fail
  for **all six** labelings of its three arrays.

Run:

```bash
python3 -B evidence/verify_ordered_design_symmetrization.py
```

The coordinate-cocycle idea has a still more basic issue.  To use the OD
axiom directly on every 1-star in the \(k=2\) case, one would need each
vertex \(x\) to occupy a fixed row \(r_x\in\{1,2\}\) in every canonically
ordered edge through \(x\).  Each edge \(\{x,y\}\) would then require
\(r_x\ne r_y\).  This is a two-colouring of \(K_4\), impossible.  Therefore
there is no globally coherent selection of coordinate positions from which
the OD star axiom alone could certify a support colouring, even in the
positive \(k=2\) case.  This does not rule out accidental success of a
specific formula; it rules out the purported automatic proof mechanism.

## \(k=6\) and \(k=16\) controls

At \(k=6\), Teirlinck supplies \(\operatorname{LOD}(5,6,12)\).  But an
orbit-closing rule applicable to every such LOD would yield
\(\operatorname{LS}(5,6,12)\), seven disjoint Witt systems.  This is known
to be impossible: Kramer and Mesner proved that at most two
\(S(5,6,12)\)'s are mutually disjoint (the citation is also recorded in
Jin--Zhu--Gu--Sun, p. 18).  Consequently no universal version of the proposed
canonical/sum/product/cocycle bridge can be valid.

At \(k=16\), the theorem gives the weighted identities (2)--(3) for an
\(\operatorname{LOD}(15,16,32)\), but no known argument forces (4), and no
explicit orbit-closed witness was obtained.  Therefore this route does not
solve Erdős--Rosenfeld Problem #835.
