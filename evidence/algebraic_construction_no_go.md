# Three exact no-go theorems for algebraic \(k=16\) constructions

This note rules out three natural finite-field constructions for a
17-colouring of \(J(32,16)\):

1. arbitrary postprocessing of the product of sixteen distinct 32nd roots
   of unity;
2. the trace of a Vandermonde determinant, for every trace direction and
   every ordering of the 32 ground points;
3. a single maximal minor (Pluecker coordinate) of sixteen column vectors
   over \(\mathbb F_{17}\).

These are **ansatz exclusions**, not a nonexistence proof for an arbitrary
colouring and not a solution of Erdős--Rosenfeld Problem #835.

All finite calculations below are reproduced by
`verify_algebraic_construction_no_go.py`.

## 1. Every fusion of the 32nd-root product needs 32 colours

Let \(H=\langle\beta\rangle\) be a cyclic group of order \(32\).  Label the
ground points by its elements and, for a 16-set \(S\subset H\), put
\[
 P(S)=\prod_{x\in S}x\in H.
\]

### Theorem 1

If
\[
 c(S)=h(P(S))
\]
is a proper colouring of \(J(32,16)\), for an arbitrary map
\(h:H\to\Omega\), then \(h\) is injective.  In particular
\(\lvert\Omega\rvert\ge32\), so this construction cannot use seventeen
colours.

### A fixed-size sum lemma in \(\mathbb Z_{32}\)

For every \(d\ne0\) and every \(u\in\mathbb Z_{32}\), there is a 15-set
\[
 T\subset\mathbb Z_{32}\setminus\{0,d\}
 \quad\text{with}\quad
 \sum_{t\in T}t=u.
 \tag{1}
\]

Here is a short Fourier proof with a large positive margin.  Let
\(N_u(d)\) count the sets in (1).  Fourier inversion in
\(\mathbb Z_{32}\) gives
\[
 32N_u(d)=
 \sum_{\chi}\chi(-u)\,[y^{15}]
 \prod_{a\ne0,d}(1+y\chi(a)).
 \tag{2}
\]
The trivial character contributes
\[
 \binom{30}{15}=155{,}117{,}520.
\]

If a nontrivial character has order
\(m\in\{2,4,8,16,32\}\), then
\[
 \prod_{a\in\mathbb Z_{32}}(1+y\chi(a))
 =(1-y^m)^{32/m}.
\]
Writing \(\zeta=\chi(d)\), the corresponding factor in (2) is
\[
 \frac{(1-y^m)^{32/m}}{(1+y)(1+\zeta y)}.
 \tag{3}
\]
The coefficient of \(y^r\) in the reciprocal of the denominator is
\[
 (-1)^r\sum_{j=0}^r\zeta^j,
\]
whose absolute value is at most \(r+1\).  Consequently the absolute
value of the coefficient of \(y^{15}\) in (3) is at most
\[
 B_m=\sum_{q=0}^{\lfloor15/m\rfloor}
 \binom{32/m}{q}(16-mq).
\]
The five bounds are
\[
\begin{array}{c|rrrrr}
m&2&4&8&16&32\\ \hline
B_m&102{,}960&560&48&16&16.
\end{array}
\]
There are respectively \(1,2,4,8,16\) characters of these orders, so
the total absolute contribution of every nontrivial character is at
most
\[
 102{,}960+2(560)+4(48)+8(16)+16(16)
 =104{,}656.
\]
It follows from (2) that
\[
 N_u(d)\ge
 \frac{155{,}117{,}520-104{,}656}{32}
 =4{,}844{,}152>0,
\]
proving (1).

### Proof of Theorem 1

Write the elements of \(H\) as \(\beta^j\),
\(j\in\mathbb Z_{32}\).  Given two distinct desired product exponents
\(u,v\), put \(d=v-u\).  Choose \(T\) as in (1), with exponent sum
\(u\).  Then
\[
 S=T\cup\{0\},\qquad S'=T\cup\{d\}
\]
are adjacent 16-sets whose products are respectively
\(\beta^u\) and \(\beta^v\).  Thus every two distinct product values
occur on adjacent vertices.  Properness forces \(h(\beta^u)\ne
h(\beta^v)\), so \(h\) is injective. \(\square\)

This rules out trace, norm, inversion-orbit fusion, power maps, arbitrary
lookup tables, and every other postprocessing of this product statistic.
It does not rule out a formula retaining additional information about the
selected roots.

## 2. No trace of a Vandermonde determinant

Work in
\[
 K=\mathbb F_{17}[\beta]/(\beta^2-3).
\]
The element \(3\) is a quadratic nonresidue modulo \(17\), and \(\beta\)
has order \(32\).  Again label the points by
\[
 H=\{\beta^j:0\le j<32\}.
\]

Fix any global ordering of these points.  For a 16-set \(S\), let
\[
 \Delta(S)=\prod_{\substack{x,y\in S\\x<y}}(y-x)
\]
be its ordered Vandermonde determinant.  For any nonzero
\(\lambda\in K\), the natural base-field proposal is
\[
 c_\lambda(S)=\operatorname{Tr}_{K/\mathbb F_{17}}
 \bigl(\lambda\Delta(S)\bigr)\in\mathbb F_{17}.
 \tag{4}
\]

### Theorem 2

For every \(\lambda\ne0\) and every global ordering of \(H\), the rule
(4) is not a proper 17-colouring of \(J(32,16)\).

### Proof

Take the 15-set \(T\) whose root exponents are
\[
 E=\{6,7,8,9,10,13,15,16,18,19,20,25,28,30,31\}.
 \tag{5}
\]
For \(x\in H\setminus T\), put
\[
 z_x=\prod_{t\in T}(x-t)=a_x+b_x\beta.
\]
Exact arithmetic in \(K\) gives
\[
 \sum_{x\notin T}a_x^2=9,\qquad
 \sum_{x\notin T}a_xb_x=0,\qquad
 \sum_{x\notin T}b_x^2=10
 \quad\text{in }\mathbb F_{17}.
 \tag{6}
\]

Write \(\mu=u+v\beta\), and normalize the trace by
\[
 L_\mu(z)=\tfrac12\operatorname{Tr}_{K/\mathbb F_{17}}(\mu z).
\]
For \(z=a+b\beta\),
\[
 L_\mu(z)=ua+3vb.
\]
Equation (6) therefore yields
\[
 \sum_{x\notin T}L_\mu(z_x)^2
 =9u^2+5v^2.
 \tag{7}
\]
The quadratic form on the right is anisotropic over \(\mathbb F_{17}\).
Indeed, if \(u\ne0\), a zero would give
\[
 (v/u)^2=-9/5=5,
\]
but \(5\) is a quadratic nonresidue modulo \(17\); if \(u=0\), the
value is \(5v^2\ne0\).

For every extension \(T\cup\{x\}\),
\[
 \Delta(T\cup\{x\})
 =\varepsilon_x\,\Delta(T)z_x,
 \qquad \varepsilon_x\in\{1,-1\}.
 \tag{8}
\]
The signs depend on the global point ordering.  They disappear after
squaring, and multiplication by the nonzero common factor
\(\lambda\Delta(T)\) merely replaces \(\mu\) in (7) by another nonzero
element of \(K\).  Thus (7) says that the sum of the squares of the
seventeen proposed colours on this star is nonzero.

If the star were rainbow, its colours would be all of
\(\mathbb F_{17}\), whose square sum is
\[
 \sum_{r\in\mathbb F_{17}}r^2=0.
\]
This contradiction proves the theorem, uniformly in \(\lambda\) and in
the global ordering. \(\square\)

## 3. No maximal-minor colouring

Let \(G\) be a \(16\times32\) matrix over \(\mathbb F_{17}\), with its
columns given a fixed global order.  The maximal-minor proposal is
\[
 c(S)=\det(G_S),\qquad G\in\mathbb F_{17}^{16\times32},
 \tag{9}
\]
where the columns in \(G_S\) retain their induced global order.  Composing
(9) with any fixed permutation of \(\mathbb F_{17}\) makes no difference:
a star is rainbow after the permutation exactly when its raw determinant
values are all of \(\mathbb F_{17}\).

### Theorem 3

No matrix \(G\in\mathbb F_{17}^{16\times32}\) makes (9) a proper
17-colouring of \(J(32,16)\).

### The exact ordered 14-column link

Suppose otherwise, and fix any fourteen columns \(R\).  They are
independent: if their rank were at most thirteen, adjoining any further
column would give a 15-set all of whose sixteen-dimensional extensions
have determinant zero.

Project the other eighteen columns to the two-dimensional quotient by
\(\langle R\rangle\).  They give nonzero vectors
\[
 u_0,u_1,\ldots,u_{17}\in\mathbb F_{17}^2
 \tag{10}
\]
in the inherited global order, after harmless individual sign changes.
More explicitly, if
\[
 s_i=(-1)^{|\{r\in R:r>i\}|},
\]
then multiplying the \(i\)-th projected vector by \(s_i\) absorbs the sign
needed to move it past the ordered columns of \(R\).  Consequently the
actual minor on \(R\cup\{i,j\}\), for \(i<j\), is a common nonzero scalar
times
\[
 d_{ij}=\det(u_i,u_j).
 \tag{11}
\]
The common scalar can be suppressed.  For every \(i\), the seventeen
*symmetric edge labels*
\[
 \{d_{ji}:j<i\}\ \cup\ \{d_{ij}:j>i\}
 \tag{12}
\]
are all of \(\mathbb F_{17}\).

In particular, every vector has exactly one parallel mate.  The eighteen
vectors therefore occupy nine projective directions, two vectors per
direction.

### Eighth powers forbid opposite mates

Choose a projective direction not among those nine and move it to infinity.
The nine used directions then have distinct finite slopes \(t_e\), and
their two vectors can be written
\[
 a_e(1,t_e),\qquad b_e(1,t_e),
 \qquad a_e,b_e\ne0.
\]

The sum of the eighth powers of all field elements is zero.  Eighth powers
also remove every ordering sign in (12).  The row belonging to either
vector in direction \(e\) therefore gives
\[
 \sum_{f\ne e}(a_f^8+b_f^8)(t_f-t_e)^8=0.
 \tag{13}
\]
Put
\[
 F(x)=\sum_f(a_f^8+b_f^8)(t_f-x)^8.
\]
Equation (13) says that this degree-at-most-eight polynomial vanishes at
the nine distinct values \(t_e\), so \(F=0\).  The nine polynomials
\((t_f-x)^8\) are linearly independent: after expansion, their coefficient
matrix is a nonsingular Vandermonde matrix times the nonzero binomial
coefficients \(\binom8j\).  Hence
\[
 a_e^8+b_e^8=0
 \quad\text{for every }e.
 \tag{14}
\]
Thus every mate ratio \(b_e/a_e\) has eighth power \(-1\).  In particular,
no parallel pair consists of opposite vectors, because
\((-1)^8=1\).

### First powers force an opposite pair

Let
\[
 W=\sum_{j=0}^{17}u_j,\qquad
 P_i=\sum_{j<i}u_j,\qquad
 Q_i=W-2P_i.
\]
The sum of the field elements in every row (12) is zero.  Written with the
ordered determinants, that identity is exactly
\[
\begin{aligned}
0
 &=\sum_{j<i}\det(u_j,u_i)+\sum_{j>i}\det(u_i,u_j)\\
 &=\det(u_i,W-2P_i)
 =\det(u_i,Q_i).
\end{aligned}
\tag{15}
\]
Moreover
\[
 Q_{i+1}=Q_i-2u_i.
 \tag{16}
\]

There must be an index \(i\le2\) with \(Q_i=0\).  Indeed, if
\(Q_0,Q_1,Q_2\) were all nonzero, (15)--(16) would successively make
\(u_0,u_1,u_2\) parallel to \(Q_0=W\), contradicting the fact that a
projective direction contains only two vectors.

Take the first such \(i\).  Equation (16) gives
\[
 Q_{i+1}=-2u_i\ne0,
\]
so (15) makes \(u_{i+1}\) the unique parallel mate of \(u_i\).  If
\(Q_{i+2}\ne0\), the same equations would make \(u_{i+2}\) a forbidden
third vector in that direction.  Therefore
\[
 Q_{i+2}=-2(u_i+u_{i+1})=0,
\]
and hence
\[
 u_{i+1}=-u_i.
\]
This is an opposite parallel pair, contradicting (14).  The contradiction
proves Theorem 3. \(\square\)

### Prime-\(p\) generalization

The same argument proves a little more.  Let \(p\equiv1\pmod4\) be prime,
put \(k=p-1\), and try to colour the \(k\)-sets of \(2k\) points by the
maximal minors of a \((p-1)\times(2p-2)\) matrix over \(\mathbb F_p\).
Fixing \(p-3\) columns leaves \(p+1\) vectors in a two-dimensional
quotient, paired into
\[
 \frac{p+1}{2}
\]
projective directions.  Set \(m=(p-1)/2\).  Since \(m\) is even, ordering
signs disappear from the \(m\)-th power sums.  The analogue of (13) is a
degree-\(m\) polynomial vanishing at \(m+1\) slopes.  Its shifted-power
coefficient matrix is Vandermonde because every
\(\binom mj\) is nonzero modulo the prime \(p\).  Thus every mate ratio
satisfies
\[
 r^m=-1.
\]
The first-power recurrence (15)--(16), which is independent of \(p\),
still forces one mate ratio to be \(-1\).  But
\[
 (-1)^m=1
\]
because \(m\) is even.  Hence no such determinant colouring exists for
any prime \(p\equiv1\pmod4\).

### Why the Singleton shortcut is still invalid

Theorem 3 is a local power-sum obstruction, not a Singleton-bound
argument.  Merely observing that every fifteen columns would be independent
does **not** imply code distance \(18\): fifteen independent columns can
span a hyperplane.  Without the ordered rainbow determinant values used in
(13) and (15), that shortcut proves nothing.

The theorem excludes a single maximal minor and any fixed relabelling of
its values.  It does not by itself exclude a ratio of two unrelated
maximal minors or a colouring retaining several coupled Pluecker
coordinates.

## Scope

The three theorems eliminate broad and particularly tempting algebraic
families.  None of these statements excludes an arbitrary asymmetric
colouring, an arbitrary large set \(LS(15,16,32)\), or a construction
using several coupled polynomial invariants.
