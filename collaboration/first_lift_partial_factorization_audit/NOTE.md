# Five-saturated partial one-factorizations: exact scope audit

Date: 2026-07-27.

## Scope

This note audits the corrected first-lift question at the
**partial-factorization-realizable** tier.  At the target order, let
\[
 P=\{p_0,\ldots,p_4\},\qquad |A|=13,\qquad |{\cal C}|=17.
\]
The input is a proper \(17\)-edge-colouring of
\[
 H=K_{P\cup A}-E(K_A),
\tag{1}
\]
so all edges incident with \(P\) are coloured and each vertex of \(P\) is
saturated: it sees every colour once.  The question is whether every such
colouring extends to a one-factorization of \(K_{18}\).

The conclusions are:

1. the support, partial-colouring, and Latin-rectangle formulations are
   exactly equivalent at this tier;
2. none of the four nearby completion/detachment results checked below
   proves the required five-row statement;
3. the unrestricted statement “five saturated vertices always extend” is
   false: an explicit genuine order-\(12\) example has two colours forced
   onto the same remaining edge;
4. that example does **not** answer the order-\(18\) question.  At order
   \(18\), every remaining colour support has size \(8,10\), or \(12\), so
   the pinned-edge obstruction used at order \(12\) is unavailable.

No universal order-\(18\) proof or counterexample is claimed here, and no
claim about fan-realizability or Erdős--Rosenfeld Problem #835 is made.

## 1. Exact equivalences

For \(c\in{\cal C}\), let \(V_c\subseteq A\) be the set of vertices of
\(A\) not incident with a colour-\(c\) edge of \(H\).  The colour-\(c\)
edges already form a matching saturating \(P\).  Thus the unmatched vertices
of that matching are exactly \(V_c\).

> **Proposition 1.**  The following are equivalent.
>
> 1. The colouring of \(H\) extends to a one-factorization of \(K_{18}\).
> 2. For every \(c\), one can choose a perfect matching \(M_c\) on \(V_c\)
>    such that the \(M_c\)'s partition \(E(K_A)\).
> 3. The associated \(5\times18\) Latin rectangle completes to a unipotent
>    symmetric Latin square of order \(18\).

For (1)\(\Leftrightarrow\)(2), the uncoloured edges are exactly
\(E(K_A)\), and a colour class becomes a one-factor precisely when its new
edges perfectly match its currently unmatched set \(V_c\).  The equivalence
with (3) is the standard edge-colouring translation: put the colour of
\(uv\) in cells \((u,v)\) and \((v,u)\), and put one new common symbol on
the diagonal.  Saturation of the five \(P\)-vertices makes their five rows
Latin; completing symmetrically and unipotently is exactly adding the
missing one-factor edges.

This also clarifies the relation between the two incidence classes:

* **class B:** every \(a\in A\) forbids five colours, and every colour is
  forbidden at an odd number at most five of the \(a\)'s;
* **class B-prime:** the incidence matrix is induced by an actual proper
  colouring (1).

Kőnig's theorem supplies a five-edge-colouring of the missing-incidence
bipartite graph for class B, but class B-prime additionally requires the
ten internal edges of \(K_P\) to fill the unused colour incidences at \(P\).
That is genuine extra data; the two classes must not be identified.

## 2. A genuine five-saturated counterexample at order 12

The following example has \(|P|=5\), \(|A|=7\), and eleven colours
\(\{0,\ldots,10\}\).  The colour on cross edge \(p_i a\) is entry \(i\) of
row \(a\):
\[
\begin{array}{c|ccccc}
a&p_0&p_1&p_2&p_3&p_4\\ \hline
0&2&4&10&1&8\\
1&6&0&2&10&7\\
2&3&9&5&0&2\\
3&5&7&3&4&1\\
4&4&5&0&2&3\\
5&1&3&7&5&4\\
6&10&2&4&3&5
\end{array}
\tag{2}
\]
Colour the edges of \(K_P\) as follows:
\[
\begin{array}{c|l}
8&01,\ 23\\
9&02,\ 34\\
7&03\\
0&04\\
1&12\\
6&13,\ 24\\
10&14 .
\end{array}
\tag{3}
\]
The omitted colours in (3) have no internal \(P\)-edge.

Every row of (2) has five distinct colours.  At each \(p_i\), its seven
cross-edge colours together with its four internal-edge colours from (3)
are exactly \(\{0,\ldots,10\}\).  Hence (2)--(3) is a genuine proper
eleven-edge-colouring of \(K_{12}-E(K_7)\), with all five vertices of \(P\)
saturated.  Equivalently, it is a genuine \(5\times12\) unipotent symmetric
Latin-rectangle prefix.

It cannot extend.  Directly from (2), the vertices of \(A\) missing colour
\(3\) are exactly \(\{0,1\}\), and the vertices missing colour \(5\) are
also exactly \(\{0,1\}\).  Therefore both colour \(3\) and colour \(5\)
would have to use the unique edge \(01\) in the hole.  Two colour classes
cannot use the same edge.

This is a solver-free obstruction.  It proves that no theorem asserting
completion for an arbitrary number of five saturated rows can be invoked.
It does **not** refute the target order-\(18\) statement: its two obstructing
supports have size \(2\), whereas target supports have size at least \(8\).

## 3. Why the nearby theorems do not close order 18

The literature check used primary statements, not title-level analogy.

### Bryant--Rodger

Bryant and Rodger give necessary and sufficient conditions for a
\(2\times n\) Latin rectangle to complete to a unipotent symmetric Latin
square, equivalently for colours at **two** prescribed vertices of an even
complete graph.  Their theorem does not state an \(r=5\) result:

* D. Bryant and C. A. Rodger,
  [On the completion of latin rectangles to symmetric latin squares](https://doi.org/10.1017/S1446788700008739),
  J. Aust. Math. Soc. 76 (2004), 109--124.

The order-\(12\) example above also shows that a naive extension of their
two-row theorem to five rows would be false.

### Cruse and Andersen--Hoffman

Cruse's symmetric completion theorem, and the recent equitable-rectangle
generalization of Andersen--Hoffman, begin with a filled symmetric
**principal \(r\times r\) block**.  Our input instead prescribes five
complete rows, including all \(5\cdot13\) cross cells.  Applying a
principal-block theorem to the \(5\times5\) block forgets those cross
entries:

* A. Bahmanian and A. Johnsen-Yu,
  [The Andersen-Hoffman Theorem for Equitable Rectangles](https://arxiv.org/abs/2606.28634),
  2026, especially its stated \(r\times r\) input.

### Henderson--Hilton

Henderson and Hilton characterize precolourings whose prescribed graph is
\(K_r\) plus independent edges.  The prescribed cross graph here is the
whole \(K_{5,13}\), not a matching:

* M. J. Henderson and A. J. W. Hilton,
  [Completing an edge-colouring of \(K_{2m}\) with \(K_r\) and independent
  edges precoloured](https://doi.org/10.1112/S0024610704005526),
  J. London Math. Soc. 70 (2004), 545--566.

### Fair detachment

Amalgamate all thirteen vertices of \(A\) to one vertex \(\alpha\).  For a
colour having \(t_c\) edges inside \(P\), the outline has
\[
 5-2t_c\quad\hbox{colour-\(c\) edges between \(P\) and \(\alpha\)},\qquad
 4+t_c\quad\hbox{colour-\(c\) loops at \(\alpha\)}.
\tag{4}
\]
Thus its colour degree at \(\alpha\) is \(13\), exactly what fair
detachment needs to produce degree one at each of thirteen clones.
Likewise the total multiplicities force the detached underlying graph to
be \(K_{18}\).

But amalgamation has erased which original \(a\in A\) was the endpoint of
each cross edge.  Fair detachment distributes those cross-edge hinges
among new clones; its balance conclusions do not require each hinge to
return to its prescribed old endpoint.  The order-\(12\) counterexample
makes this logical gap concrete: its amalgamated outline has a fair
detachment to some one-factorization of \(K_{12}\), yet no detachment
preserving (2) can exist.

The relevant theorem is:

* A. Bahmanian and C. A. Rodger,
  [Multiply Balanced Edge Colorings of Multigraphs](https://arxiv.org/abs/1710.03836),
  Theorem 3.1.

Therefore the outline arithmetic is necessary and useful, but is not an
extension proof for a prescribed class-B-prime instance.

## 4. Exact frontier

The surviving target question is:

> Does every proper \(17\)-edge-colouring of
> \(K_{18}-E(K_{13})\) that saturates the same five vertices extend to a
> one-factorization of \(K_{18}\)?

The searches already in the repository provide positive samples, not a
universal result.  The small counterexample proves that any proof at order
\(18\) must use the target dense-support regime, not merely “five rows,”
parity, or amalgamated colour degrees.

## Verification

Run:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/first_lift_partial_factorization_audit/verify_boundary.py
```

The standard-library verifier reconstructs (2)--(3), checks properness and
saturation from the definitions, constructs the five Latin rows, and
checks that colours \(3\) and \(5\) are both forced onto edge \(01\).
