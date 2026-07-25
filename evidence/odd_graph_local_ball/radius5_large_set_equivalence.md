# The minimal-trace radius-five slice is a prescribed-link \(LSTS(19)\)

This note gives an exact reformulation of one useful subfamily of the
fixed-golf radius-five model.  It is a construction route, not a
nonexistence claim and not a solution of Erdős--Rosenfeld Problem #835.

Let
\[
 {\cal C}=V\sqcup\{\infty\},\qquad |V|=16,
\]
and fix two distinct golf-square indices \(i,j\).  Write
\[
 S_i(u,v)=M_i(uv),\quad S_i(u,\infty)=L_i(u)
\]
and similarly for \(j\).  The \(S_i\) are the symmetric idempotent
Latin squares of the fixed cyclic \(G(17)\).

## 1. Joining \(P\) and the \(N\)-trace

For this one index pair, combine the \(560\) radius-five values and
the \(120\) entries of the \(N\)-trace into a colour map on the
triples of \({\cal C}\):
\[
 Q_{ij}(u,v,w)=
 \begin{cases}
 P_{ij}(uvw),&u,v,w\in V,\\
 N_{uv}(ij),&\{u,v,w\}=\{u,v,\infty\},\quad u,v\in V.
 \end{cases}
 \tag{1}
\]
For a moving pair \(xy\in\binom{\cal C}2\), consider the equation
\[
 \{S_i(x,y),S_j(x,y)\}\ \dot\cup\
 \{Q_{ij}(x,y,z):z\in{\cal C}\setminus\{x,y\}\}
 ={\cal C}.
 \tag{2}
\]
The dot denotes disjoint union.  When \(x,y\in V\), (2) is exactly
the radius-five extension equation: its \(z=\infty\) term is
\(N_{xy}(ij)\), and the other fourteen terms are the \(P\)-values.

The equations with \(y=\infty\) are additional structure.  They have
the following exact interpretation.  For a colour \(c\), let
\[
 D_{ij,c}=\{uv\in\binom V2:N_{uv}(ij)=c\}.
 \tag{3}
\]
Then (2) on every pair \(u\infty\) is equivalent to
\[
 \begin{aligned}
 D_{ij,\infty}&\text{ is a perfect matching of }V,\\
 D_{ij,c}&\text{ is a perfect matching of }
 V\setminus\{L_i^{-1}(c),L_j^{-1}(c)\}
 &&(c\in V).
 \end{aligned}
 \tag{4}
\]
Indeed, (2) says that the fifteen \(N_{uv}(ij)\), with \(v\ne u\),
are the fifteen distinct colours outside
\(\{L_i(u),L_j(u)\}\).  Equivalently, the degree of \(u\) in
\(D_{ij,c}\) is zero exactly when
\(c=L_i(u)\) or \(c=L_j(u)\), and is one otherwise.  Since
\(L_i,L_j\) are permutations and disagree pointwise, this is (4).
The converse is the same degree statement read backwards.

Thus (4) is the **minimal-trace ansatz**: it strengthens the necessary
degree parities in `radius5_reduction.md` to the smallest possible
nonnegative degrees.  It is not forced by an arbitrary radius-five
extension.

## 2. Exact large-set equivalence

Adjoin two new points \(a,b\) to \({\cal C}\), and colour the triples
of the resulting \(19\)-set \(W={\cal C}\sqcup\{a,b\}\) by
\[
 \begin{array}{rcl}
 \chi(\{a,b,x\})&=&x,\\
 \chi(\{a,x,y\})&=&S_i(x,y),\\
 \chi(\{b,x,y\})&=&S_j(x,y),\\
 \chi(\{x,y,z\})&=&Q_{ij}(x,y,z).
 \end{array}
 \tag{5}
\]

**Prescribed-link theorem.**  Equation (2) holds for every moving
pair \(xy\) if and only if the seventeen colour classes of \(\chi\)
are seventeen pairwise disjoint Steiner triple systems on \(W\).
Equivalently, \(\chi\) is a large set \(LS(2,3,19)\) whose links at
\(a\) and \(b\) are the prescribed one-factorizations coming from
\(S_i\) and \(S_j\).

**Proof.**  Fix a colour \(c\).  The pair \(ab\) lies in the unique
triple \(abc\) of colour \(c\).  For the pair \(ax\), the idempotent
Latin row of \(S_i\) says that its unique colour-\(c\) completion is
\(abx\) when \(c=x\), and otherwise is the unique \(axy\) with
\(S_i(x,y)=c\).  The argument for \(bx\) uses \(S_j\).

For a moving pair \(xy\), its possible third points are \(a,b\) and
the fifteen points of
\({\cal C}\setminus\{x,y\}\).  Their colours are exactly the
seventeen entries in (2), so each colour occurs exactly once.
Consequently every pair of \(W\) occurs in exactly one colour-\(c\)
triple.  Each colour class is an \(STS(19)\), and (5) assigns one
colour to every triple, so the seventeen systems are disjoint and
exhaustive.

Conversely, if the colour classes in (5) are Steiner triple systems,
then each colour occurs exactly once among the seventeen triples
containing a fixed moving pair.  Those colours are precisely the
entries in (2), which proves (2). \(\square\)

The boundary has \(17+2\binom{17}{2}=289\) already coloured triples.
For each colour it supplies \(1+8+8=17\) of the \(57\) blocks in an
\(STS(19)\).  The remaining
\[
 \binom{17}{3}=680=17\cdot40
\]
moving triples therefore ask for exactly forty further blocks of
each colour.

## 3. The cyclic exact-cover quotient

For the Wallis chart, each \(S_i\) obeys
\[
 S_i(x+t,y+t)=S_i(x,y)+t\pmod {17}.
 \tag{6}
\]
If \(Q\) is required to obey the analogous translation law, it is
enough to construct its colour-zero class.  The two zero-coloured
edge matchings of \(S_i\) and \(S_j\) are disjoint and contain
sixteen edges in total.  Hence the forty zero-coloured moving
triples must decompose
\[
 K_{17}-(S_i^{-1}(0)\cup S_j^{-1}(0))
 \tag{7}
\]
into triangles.

Translation has forty orbits on \(\binom{\mathbb Z_{17}}3\).  A
translation-equivariant \(Q\) selects exactly one translate from each
orbit for colour zero, and (7) is then a \(40\)-choice exact-cover
problem.  Developing those representatives through all seventeen
translations gives the whole prescribed-link \(LSTS(19)\).

`search_cyclic17_r3_extension.py` implements this quotient and checks
the resulting pair-star equations directly.  A SAT completion for a
single pair is therefore a compact, exact radius-five **slice** in
the minimal-trace ansatz.

## 4. The simultaneous \(105\)-slice condition

A completion for one \(ij\), or even an independently chosen
completion for every one of the \(105\) pairs, is not yet a
radius-five ball.  The traces
\[
 N_{uv}(ij)=Q_{ij}(u,v,\infty)
 \tag{8}
\]
must use the same \(N_{uv}\) table.  Explicitly, for every
\(uv\in\binom V2\) and every index \(i\),
\[
 \{Q_{ij}(u,v,\infty):j\ne i\}
 ={\cal C}\setminus
 \{M_i(uv),L_i(u),L_i(v)\}.
 \tag{9}
\]
Equation (9) is the shared list-edge-colouring constraint on
\(K_{15}\).  It couples the otherwise separate prescribed-link
\(LSTS(19)\) completions.  A family of \(105\) phase lists must be
checked against (9), not merely against the \(105\) individual
triangle decompositions.

Consequently:

* one prescribed-link completion proves feasibility of one \(ij\)
  slice only;
* \(105\) independent completions still do not prove radius-five
  feasibility;
* \(105\) completions satisfying (9), followed by
  `verify_radius5_golf_joint.py`, would give a genuine certificate
  for the fixed cyclic-golf radius-five ball;
* even that radius-five ball would not by itself be a global
  \(O_{16}\to K_{17}\) cover.
