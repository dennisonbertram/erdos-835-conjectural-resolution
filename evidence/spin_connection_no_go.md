# The Schur/spin refinement of the rank-15 connection is unobstructed

Status: **Proved no-go for the bare connection-holonomy route.**

This note tests the natural refinement of the determinant calculation in
`odd_matching_cells.md`.  That calculation gives a rank-15 permutation
connection on a hypothetical cover
\[
 c:O_{16}\longrightarrow K_{17}
\]
and proves that the holonomy around every closed walk is an even
permutation.  One might hope that lifting the holonomy from \(A_{15}\) to
the Schur double cover \(2.A_{15}\), or equivalently to the relevant spin
double cover, produces a central sign that obstructs a lifted base
triangle.

It does not.  The reason is topological and exact: the connection lives on
a graph.  Every \(A_{15}\)-connection on a graph lifts through every
central double cover.  A central sign assigned to an individual lifted
triangle is a choice of spin lift, not an invariant of the original
colouring.

## 1. From the determinant identity to an \(A_{15}\)-connection

At a vertex \(S\) of \(O_{16}\), let \(V_S\) be the 15-dimensional real
vector space with basis indexed by the points of \(S\).  For every edge
\(ST\), equation (6) of `odd_matching_cells.md` supplies a permutation
isometry
\[
 g_{ST}:V_S\longrightarrow V_T,\qquad
 g_{TS}=g_{ST}^{-1}.                                      \tag{1}
\]
Composition along paths therefore defines a representation of the
fundamental groupoid of \(O_{16}\).

Equation (9) of that note proves
\[
 \det(g_\gamma)=+1                                      \tag{2}
\]
for every closed walk \(\gamma\).  Choose an orientation at one vertex and
transport it along a spanning tree.  Equation (2) says that the resulting
orientation is independent of the chosen path.  Relative to these
orientations, all edge transports lie in \(SO(15)\), and after choosing a
base vertex the holonomy is a homomorphism
\[
 \rho:\pi_1(O_{16})\longrightarrow A_{15}\subset SO(15). \tag{3}
\]
Thus the determinant calculation kills the first obstruction \(w_1\)
exactly.

## 2. The ordinary spinor norm is already trivial

There is also a direct answer if “spin refinement” means the classical
spinor norm.  Work over any field of characteristic different from two
with the standard coordinate quadratic form.  A coordinate transposition
\((ij)\) is the orthogonal reflection in \(e_i-e_j\), whose quadratic
value is \(2\) (up to the harmless global normalization of the form).
Consequently, if a permutation \(\pi\) is written as a product of \(m\)
transpositions, its spinor norm is
\[
 \theta(\pi)=2^m\quad\text{in }F^\*/(F^\*)^2.             \tag{4}
\]
The parity of \(m\) is the sign of \(\pi\).  Every holonomy permutation
here lies in \(A_{15}\), so \(m\) is even and
\[
 \boxed{\theta(\pi)=1\quad(\pi\in A_{15}).}               \tag{5}
\]
Over the positive-definite real form this is also immediate because every
reflection vector has positive norm.  Thus the ordinary spinor norm gives
exactly the already-known determinant information and no finer sign.

## 3. Universal lifting theorem for graph connections

**Theorem.**  Let \(G\) be a connected graph, let
\[
 1\longrightarrow \{\pm1\}\longrightarrow \widetilde H
 \mathop{\longrightarrow}^{p} H\longrightarrow1          \tag{6}
\]
be any central double cover, and let
\(\rho:\pi_1(G)\to H\) be any homomorphism.  Then there is a homomorphism
\(\widetilde\rho:\pi_1(G)\to\widetilde H\) with
\(p\widetilde\rho=\rho\).

**Proof.**  Choose a spanning tree of \(G\).  The oriented edges outside
the tree give a free basis \(x_1,\ldots,x_s\) of \(\pi_1(G)\).  For every
\(i\), choose either of the two lifts
\(\widetilde h_i\in p^{-1}(\rho(x_i))\).  Since the domain is the free
group on the \(x_i\), the assignments
\[
 x_i\longmapsto\widetilde h_i
\]
extend uniquely to a homomorphism \(\widetilde\rho\).  Its projection and
\(\rho\) agree on the free generators and hence everywhere. \(\square\)

Apply the theorem to \(H=A_{15}\) and either the Schur cover \(2.A_{15}\)
or the pullback of
\(\operatorname{Spin}(15)\to SO(15)\).  The rank-15 holonomy (3) always
lifts.

Equivalently, the central extension represents a class
\[
 \alpha\in H^2(A_{15};\mathbb F_2).
\]
Its pullback is
\[
 \rho^*\alpha=0\in H^2(\pi_1(G);\mathbb F_2),              \tag{7}
\]
because a graph has cohomological dimension one and its fundamental group
is free.  This is the precise \(w_2\) statement: after \(w_1\) vanishes,
there is no second obstruction on a one-dimensional base.

## 4. Explicit cocycle cancellation

The same conclusion can be seen without invoking cohomology.  Choose a
set-theoretic section \(s:H\to\widetilde H\), \(s(1)=1\), and write its
Schur cocycle as
\[
 a(g,h)=s(g)s(h)s(gh)^{-1}\in\{\pm1\}.                    \tag{8}
\]
Let \(\widetilde\rho\) be the lift constructed in the theorem and define
\[
 b(w)=\widetilde\rho(w)s(\rho(w))^{-1}\in\{\pm1\}.         \tag{9}
\]
Direct multiplication gives
\[
 a(\rho(u),\rho(v))
 =b(u)b(v)b(uv)^{-1}.                                    \tag{10}
\]
Thus the Schur cocycle pulled back to the graph holonomy is an explicit
coboundary.  Any nonzero value obtained by multiplying a preferred
set-theoretic section around a word records the choice of section \(s\)
and the 1-cochain \(b\); it is not a contradiction.

## 5. Why a lifted base triangle has no canonical central sign

There are two lifts of every free generator.  Replacing
\(\widetilde h_i\) by \(-\widetilde h_i\) gives another equally valid
spin lift of exactly the same \(A_{15}\)-connection.  More generally, the
set of lifts is a torsor for
\[
 H^1(G;\mathbb F_2)=\operatorname{Hom}(\pi_1(G),\{\pm1\}).
                                                               \tag{11}
\]
Consequently the central phase of a closed walk \(\gamma\) changes by
\(\chi(\gamma)\) under the lift indexed by
\(\chi\in H^1(G;\mathbb F_2)\).

In particular, a nontrivial simple monodromy-orbit cycle has a nonzero
class in \(H_1(G;\mathbb F_2)\).  Choose \(\chi\) pairing nontrivially
with that class.  The two spin lifts then give opposite central signs on
that very orbit while projecting to identical point permutations on
every edge.  Hence neither sign can be forbidden by the Odd-graph cover
axioms.

For scale, \(O_{16}\) has
\[
\begin{aligned}
 |V|&=\binom{31}{15}=300\,540\,195,\\
 |E|&=8|V|=2\,404\,321\,560,\\
 \dim H^1(O_{16};\mathbb F_2)
 &=|E|-|V|+1=2\,103\,781\,366.
\end{aligned}                                             \tag{12}
\]
Thus, if the hypothetical colouring existed, its oriented connection
would have
\(2^{\,2\,103\,781\,366}\) spin lifts.  The large number is not the
argument, but it makes the freedom in (9) concrete.

## 6. Exact scope of the no-go

This proves that the following route cannot obstruct the colouring:

> take the already-even rank-15 connection holonomy, pull the Schur
> \(2\)-cocycle or spin double cover back along graph loops, and demand a
> canonical positive central phase on lifted triangles.

No such positivity demand is supplied by a graph connection.  The
original large-set data determine the projected bijections \(g_{ST}\),
but not one of their two spin lifts; changing an edge lift is invisible
to every Steiner and Odd-graph incidence equation.

A spin argument could become substantive only after proving additional
two-dimensional structure not present in the current formulation: for
example, a canonically defined 2-complex whose face boundaries carry
prescribed *trivial spin holonomy*.  Then the Schur class could be
evaluated on genuine 2-cycles.  Merely declaring selected 6-cycles or
lifted base triangles to be faces is not valid: the existing connection
does not have trivial \(A_{15}\)-holonomy around those cycles, and the
Steiner axioms provide no such 2-cell relation.

Therefore the Schur/spin refinement, by itself, adds no obstruction
beyond the determinant identity already proved.
