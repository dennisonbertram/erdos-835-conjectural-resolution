# Full-colour block Hodge audit

Date: 2026-07-24.  Exact arithmetic and the finite symbolic
countermodels below are checked by
`evidence/verify_full_color_block_hodge_audit.py`.

## Verdict

The proposed full-matrix and majority-colour scalar
determinant/Pfaffian, signature, and canonical-reflection/Clifford
routes do not yield a contradiction.

There are two rigorous reasons.

1. The Hodge operator has such a large canonical kernel that every
   principal block containing at least nine colour fibres is singular,
   with a parity-compatible lower bound on its nullity.
2. The seventeen canonical reflection projections form, after
   centering, an exact regular \(16\)-simplex in Hilbert--Schmidt
   space.  In particular their pairwise traces are not Clifford
   anticommutation traces; their ranks and pairwise Hilbert--Schmidt
   trace data are perfectly feasible.

There is also a concrete parameter-size voltage model showing that
diagonal-zero blocks, signed-permutation off-diagonal blocks, and the
entire stated blockwise two-step support-count pattern of \(T^2\) are
simultaneously feasible.
That model deliberately fails the positive-semidefinite Hodge
factorisation and the cubic identity \(T^3=-31T\).  Thus the listed
block-and-count conditions alone are insufficient.  A continuation
would have to add the Hodge/cubic identities or other comparably global
labelled-incidence information.

Nothing here proves or disproves the existence of the large set.

## 1. The exact block operator

Assume hypothetically that there is a locally bijective cover
\(O_{16}\to K_{17}\), equivalently the derived large-set partition of
the \(15\)-subsets of a 31-set into seventeen systems
\[
 {\cal D}_a=S(14,15,31),\qquad 0\le a<17.
\]
Put
\[
 {\cal H}=\mathbb R^{\binom{[31]}{15}},
 \qquad
 T=\iota_{e_0+\cdots+e_{30}}* .
\]
In the increasing \(15\)-subset basis, \(T_{A,B}\) is zero unless
\(A\cap B=\varnothing\), and otherwise is the orientation sign of the
complementary wedge.  Since 15 is odd,
\[
 T^{\mathsf T}=-T.                                      \tag{1}
\]

Order the basis first by colour and then within each fibre.  In the
cover formulation each colour fibre is independent and every block has
exactly one disjoint block in each of the other sixteen fibres.  (The
same independence follows in the large-set formulation from the
standard boundary intersection equations, whose internal disjointness
number is \(n_0=0\).)  Consequently
\[
 T=(T_{ab})_{0\le a,b<17},\qquad
 T_{aa}=0,\qquad
 T_{ab}\text{ is a signed permutation matrix }(a\ne b),
 \tag{2}
\]
with \(T_{ba}=-T_{ab}^{\mathsf T}\).

Let \(\partial\) be oriented simplicial boundary from 15-subsets to
14-subsets.  The exterior-algebra identity is
\[
 \boxed{T^2=\partial^{\mathsf T}\partial-31I,\qquad
        T^3=-31T.}                                     \tag{3}
\]
The diagonal block of \(T^2\) is \(-16I\).  For \(a\ne b\),
\[
 (T^2)_{ab}
 =(\partial^{\mathsf T}\partial)_{ab}                  \tag{4}
\]
has exactly fifteen entries of magnitude one in every row and column:
each of the fifteen facets of a block in \({\cal D}_a\) has a unique
extension in \({\cal D}_b\).

Write
\[
 \mu=570\,285.
\]
The exact dimensions are
\[
\begin{array}{c|c}
\text{one colour fibre}&b=17\,678\,835=31\mu\\
\dim{\cal H}&N=300\,540\,195=527\mu\\
\operatorname{rank}T&d=155\,117\,520=272\mu\\
\dim\ker T&z=145\,422\,675=255\mu.
\end{array}                                            \tag{5}
\]
Indeed, \(\partial^{\mathsf T}\partial\) is \(31\) times the
projection onto \(\operatorname{im}\partial^{\mathsf T}\), while
\(-T^2\) is \(31\) times the complementary projection.  Hence
\[
 \boxed{\chi_T(x)=x^{255\mu}(x^2+31)^{136\mu}.}         \tag{6}
\]

This already makes all global scalar spectral invariants compatible:
\(iT\) has inertia
\[
 (136\mu,136\mu,255\mu),
\]
the global determinant is zero, and every nonzero spectral determinant
is a positive power of \(31\).  These facts depend only on the fixed
Hodge operator, not on a colouring.

The first two even traces also close without residue.  Every row of
\(T^2\) has diagonal entry \(-16\) and \(16\cdot15=240\)
off-diagonal entries of magnitude one, so
\[
 -\operatorname{tr}T^2=16N=31d,\qquad
 \operatorname{tr}T^4=496N=31^2d.                       \tag{6a}
\]
Thus trace order two and four merely recount the already known block
degrees.

## 2. Majority-block Pfaffians vanish for dimensional reasons

For a set \(Y\) of \(q\) colours, let \({\cal H}_Y\) be the union of
their coordinate fibres and put
\[
 T_Y=P_YTP_Y.
\]

**Theorem 2.1.**  If \(q\ge9\), then
\[
 \boxed{\dim\ker T_Y\ \ge\ (31q-272)\mu.}               \tag{7}
\]
Also the principal boundary Gram matrix
\[
 G_Y=P_Y(T^2+31I)P_Y
     =\partial_Y^{\mathsf T}\partial_Y
\]
satisfies
\[
 \boxed{\dim\ker G_Y\ \ge\ (31q-255)\mu.}               \tag{8}
\]

**Proof.**  Grassmann's dimension inequality gives
\[
\begin{aligned}
\dim(\ker T\cap{\cal H}_Y)
&\ge255\mu+31q\mu-527\mu,\\
\dim(\ker\partial\cap{\cal H}_Y)
&\ge272\mu+31q\mu-527\mu.
\end{aligned}
\]
A globally \(T\)-null vector supported on \(Y\) is \(T_Y\)-null,
and a globally \(\partial\)-null vector supported on \(Y\) is
\(G_Y\)-null.  This proves (7)--(8). \(\square\)

The first lower bounds for \(q=9,\ldots,17\), after removing the common
factor \(\mu\), are
\[
 7,38,69,100,131,162,193,224,255.                       \tag{9}
\]
Because both \(31\) and \(\mu\) are odd,
\[
 (31q-272)\mu\equiv q
 \equiv \dim{\cal H}_Y\pmod2.                           \tag{10}
\]
Thus the forced nullity has exactly the parity required of a
skew-symmetric matrix.  There is no hidden Pfaffian parity mismatch.

Consequences:

* the full \(17\)-block determinant is zero for the known Hodge-kernel
  reason;
* every even principal union of \(10,12,14,\) or \(16\) colours has
  zero Pfaffian;
* every odd principal union is singular for the elementary odd-order
  skew reason, and for \(q\ge9\) has the stronger bound (7);
* only unions of at most eight colours can support a nonzero
  colour-principal Pfaffian, and their values depend on higher
  transition holonomy rather than on the global spectrum.

This closes the proposed route of extracting a nonzero full or
majority-block Pfaffian and then contradicting its sign.

## 3. The full reflection system is a regular simplex

Let \(E_a:\mathbb R^b\to{\cal H}\) be the coordinate inclusion of the
\(a\)-th colour and put
\[
 V_a=TE_a,\qquad
 R_a=\frac1{16}V_aV_a^{\mathsf T},\qquad
 J_a=I-2R_a.                                           \tag{11}
\]
Since
\[
 V_a^{\mathsf T}V_a=-T^2[a,a]=16I,
\]
\(R_a\) is an orthogonal rank-\(b\) projection and \(J_a\) is an
orthogonal reflection.

Let
\[
 P=-\frac1{31}T^2
\]
be the projection onto \(\operatorname{im}T\).  Summing (11) over all
colours gives the exact tight-fusion identity
\[
 \boxed{\sum_{a=0}^{16}R_a=\frac{31}{16}P.}             \tag{12}
\]
For \(a\ne b\), the cross-boundary block in (4) has \(15b\) nonzero
entries of magnitude one, so
\[
\boxed{\operatorname{tr}(R_aR_b)
 =\frac1{256}\|V_a^{\mathsf T}V_b\|_{\rm F}^2
 =\frac{15b}{256}.}                                    \tag{13}
\]

Restrict to \(W=\operatorname{im}T\), of dimension \(d=272\mu\), and
set
\[
 \alpha=\frac bd=\frac{31}{272},\qquad
 F_a=R_a-\alpha P.
\]
Equations (12)--(13) give
\[
\begin{aligned}
 \sum_aF_a&=0,\\
 \|F_a\|_{\rm HS}^2&=\frac{241b}{272},\\
 \langle F_a,F_b\rangle_{\rm HS}
 &=-\frac{241b}{4352}
   =-\frac1{16}\|F_a\|_{\rm HS}^2
   \qquad(a\ne b).
\end{aligned}                                          \tag{14}
\]
Thus the seventeen centred projections are exactly the vertices of a
regular \(16\)-simplex in Hilbert--Schmidt space.  The full pair-trace
system is positive semidefinite and has precisely the expected
one-dimensional relation \(\sum_aF_a=0\).

This also rules out identifying the canonical \(J_a\)'s with Clifford
generators.  Directly,
\[
 \boxed{\operatorname{tr}(J_aJ_b)
 =N-4b+4\operatorname{tr}(R_aR_b)
 =\frac{847b}{64}>0\qquad(a\ne b).}                    \tag{15}
\]
Pairwise anticommuting involutions would have
\(\operatorname{tr}(J_aJ_b)=0\).  Hence the projected subspaces
\(\operatorname{im}R_a\) form an equichordal tight fusion frame, while
the associated natural reflections do not form a Clifford system.

The reflection determinant gives no parity either:
\[
 \det J_a=(-1)^b=-1
\]
for every colour, which is fully compatible with seventeen
orientation-reversing reflections.

## 4. A parameter-size countermodel to block-and-two-step arguments

The global Hodge identities in (3) are not consequences of the
block-and-count data alone.  Here is a concrete model with the actual
seventeen colours and the actual fibre size \(b\) which satisfies all
of (1)--(2), has the correct diagonal of \(T^2\), and has the exact
off-diagonal support counts in (4), but is not a Hodge boundary system.

Let the sheet group be
\[
 G=\mathbb Z/b\mathbb Z.
\]
Index the 136 unordered edges of \(K_{17}\) lexicographically by
\[
 e(a,c)\in\{0,\ldots,135\}\qquad(a<c)
\]
and define voltages
\[
 h_{ac}=2^{e(a,c)}\pmod b,\qquad
 h_{ca}=-h_{ac}.                                      \tag{16}
\]
On the vertices \((a,g)\in\{0,\ldots,16\}\times G\), join
\[
 (a,g)\longmapsto(c,g+h_{ac}).
\]
This is a \(b\)-sheeted cover of \(K_{17}\).  Give the block from
colour \(a\) to colour \(c\) coefficient \(+1\) when \(a<c\) and
\(-1\) in the reverse direction.  Its signed adjacency matrix
\(\widetilde T\) is skew, has zero diagonal blocks, and has a signed
permutation in every off-diagonal block.

Exact modular enumeration verifies that for every ordered
\(a\ne c\), the fifteen two-step voltages
\[
 h_{ax}+h_{xc}\qquad(x\notin\{a,c\})                   \tag{17}
\]
are distinct.  It also verifies that every triangle voltage is
nonzero.  Therefore the cover has no triangles or 4-cycles, and
\[
\begin{aligned}
 (\widetilde T^2)_{aa}&=-16I,\\
 (\widetilde T^2)_{ac}&=
 \text{a disjoint sum of fifteen signed permutations}
 \qquad(a\ne c).
\end{aligned}                                         \tag{18}
\]
Consequently \(\widetilde T^2+31I\) has diagonal \(15I\) and exactly
fifteen entries of magnitude one in every row and column of every
off-diagonal colour block, precisely the scalar support pattern of
the Johnson facet Gram.

This construction is a countermodel to any proof using only:

* the \(17\times17\) zero/permutation block pattern;
* skew-symmetry;
* uniqueness of two-step paths; and
* the diagonal and off-diagonal support counts of \(T^2+31I\).

It is **not** a counterexample to the full Hodge identity.  On the
sheet-constant subspace, \(\widetilde T\) restricts to the transitive
skew tournament matrix
\[
 S_{ac}=\begin{cases}
 1,&a<c,\\
 -1,&a>c,\\
 0,&a=c.
 \end{cases}
\]
For the all-one vector,
\[
 \|S\mathbf1\|^2
 =\sum_{a=0}^{16}(16-2a)^2=1632,
\]
so
\[
 \mathbf1^{\mathsf T}(31I+S^2)\mathbf1
 =527-1632=-1105<0.                                  \tag{19}
\]
Thus \(\widetilde T^2+31I\) is not positive semidefinite, and
\(\widetilde T^3\ne-31\widetilde T\).

Equation (19) exhibits concrete extra content of (3): the true Johnson
block is not merely a matrix with the right support counts; it is the
positive Gram matrix of one globally coherent oriented boundary.

For comparison, the full formal package is genuinely realizable at the
positive boundary case \(r=1\).  With three singleton colour fibres,
\[
 T_1=\begin{pmatrix}
 0&1&-1\\
 -1&0&1\\
 1&-1&0
 \end{pmatrix}
\]
has signed-permutation off-diagonal blocks and satisfies
\[
 T_1^2=J-3I,\qquad T_1^3=-3T_1.
\]
Its three canonical rank-one reflection projections form the expected
regular triangle, with pair trace \(1/4\).  This is an exact positive
control showing that these formal Pfaffian and reflection identities
are not intrinsically inconsistent.

## 5. What remains open

The scalar full-block routes are exhausted as follows.

* **Determinant/Pfaffian:** the global and all majority colour-principal
  matrices are singular for the exact dimensions in Theorem 2.1.
* **Signature:** \(iT\) has the fixed balanced nonzero spectrum in
  (6), independent of any colour partition.
* **Reflection/Clifford:** the canonical reflections give the regular
  fusion simplex (14), and fail Clifford anticommutation by (15).
* **Block sparsity and two-step uniqueness:** the voltage construction
  satisfies them at the exact fibre size.

One route not exhausted is the entrywise interaction between the
signed-permutation blocks and the global cubic identity
\[
 T^3=-31T,
\]
along with the stronger, specifically labelled positive boundary
factorisation in (3).
At block level this couples signed triangle holonomies across all
seventeen colours.  The calculations above do not determine it from
individual matching-block determinants, pairwise traces, or the
blockwise support counts of \(T^2\).

A successful continuation along this operator route would need a
genuinely three-or-more-colour signed-incidence identity strong enough
to exploit those global constraints.  A different proof could instead
use exact labelled Johnson-incidence information absent from the
voltage model.  Both possibilities remain open here.
