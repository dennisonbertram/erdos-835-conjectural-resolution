# Top-degree pairing derivatives: exact identities and the matching-wise barrier

This note examines the remaining degree-(16) component in the first
unresolved case of Erdős--Rosenfeld Problem #835.  It proves exact frame
identities for the top polytabloid coefficients of a hypothetical colouring
and then gives a sharp local feasibility witness.  The result is a useful
barrier, **not** a solution of the problem.

Throughout, let

\[
 p=k+1,\qquad n=2k,
\]

where (p) is prime and (k) is even.  Suppose, only for the purpose of
deriving consequences, that

\[
 c:\binom{[2k]}k\longrightarrow\mathbb F_p
\]

is a tight (p)-colouring.  Its colour classes are denoted by (C_z).
In the first open case (p=17,k=16), each class has

\[
 d=\frac1p\binom{2k}k=35{,}357{,}670
\tag{1}
\]

members.

## 1. Signed colour counts on a matching cube

Let

\[
 M=\{(a_1,b_1),\ldots,(a_k,b_k)\}
\]

be a perfect matching of ([2k]), with an arbitrary orientation on every
edge.  Its (2^k) transversals form a (k)-cube.  Put

\[
 \epsilon_M(T)=\prod_{i=1}^k
 \bigl(\boldsymbol 1_{a_i\in T}-\boldsymbol 1_{b_i\in T}\bigr)
 \in\{+1,-1\}
\]

for a transversal (T), and define the integer vector

\[
 \Delta_M(z)=\sum_{\substack{T\text{ transversal of }M\\c(T)=z}}
 \epsilon_M(T).
\tag{2}
\]

Changing the orientation of one edge multiplies the entire vector by
(-1), so all identities below that use a product of two such vectors are
orientation independent.

The ordinary polytabloid associated with (M) is

\[
 e_M(S)=\prod_{i=1}^k
 \bigl(\boldsymbol 1_{a_i\in S}-\boldsymbol 1_{b_i\in S}\bigr).
\tag{3}
\]

It is supported precisely on the transversals and belongs to the top
Specht module

\[
 K_\mathbb Q=\ker_\mathbb Q W_{k-1,k}(2k).
\]

Thus

\[
 \Delta_M(z)=\langle\boldsymbol1_{C_z},e_M\rangle.
\tag{4}
\]

Complementation preserves every colour when (k) is even.  Antipodal
transversals have the same sign as well.  Therefore

\[
 \Delta_M(z)\in2\mathbb Z,\qquad
 \sum_{z\in\mathbb F_p}\Delta_M(z)=0.
\tag{5}
\]

Also, two adjacent cube vertices differ in one pair and hence share a
((k-1))-set.  Their colours differ.  Consequently the restriction of
(c) to every matching cube is a complement-invariant proper
(p)-colouring of (Q_k).

For a colour statistic (h:\mathbb F_p\to\mathbb F_p), the top derivative
of (h\circ c) is exactly the corresponding moment of (2):

\[
 \langle h\circ c,e_M\rangle
 =\sum_{z\in\mathbb F_p}h(z)\Delta_M(z)\pmod p.
\tag{6}
\]

In particular, all the conditions (W(h\circ c)=0) for
\(\sum_z h(z)=0\) constrain only these linear moments.  They see
\(\Delta_M\bmod p\) modulo an additive constant vector: the annihilator of
the hyperplane \(\{h:\sum h=0\}\) is \(\langle\boldsymbol1\rangle\).
This is an important small caveat in trying to use the powers
\(c,c^2,\ldots,c^{p-2}\): their top derivatives are a Vandermonde change of
coordinates of the pairwise differences
\(\Delta_M(a)-\Delta_M(b)\), not extra nonlinear equations on (2).

## 2. The exact top-polytabloid frame

Let (\mathcal M) be the set of *unoriented* perfect matchings of
([2k]).  Then

\[
 \boxed{\quad
 \sum_{M\in\mathcal M}\Delta_M\Delta_M^{\mathsf T}
 =k!\,d\,(pI-J).
 \quad}
\tag{7}
\]

Here (I,J) are the (p\times p) identity and all-one matrices.  At
the first open parameter this reads

\[
 \sum_{M\in\mathcal M}\Delta_M\Delta_M^{\mathsf T}
 =16!\cdot35{,}357{,}670\,(17I-J).
\tag{8}
\]

Equivalently, since

\[
 |\mathcal M|=\frac{(2k)!}{2^k k!},
\]

the average over matchings is

\[
 \boxed{\quad
 \mathbb E_M[\Delta_M\Delta_M^{\mathsf T}]
 =\frac{2^k}{p}(pI-J).
 \quad}
\tag{9}
\]

For (p=17), a fixed colour has mean square
\(16\cdot2^{16}/17\), two distinct colours have mean product
\(-2^{16}/17\), and

\[
 \mathbb E_M\|\Delta_M\|_2^2=16\cdot2^{16}=1{,}048{,}576.
\tag{10}
\]

### Proof of (7)

The operator

\[
 A=\sum_{M\in\mathcal M}e_Me_M^{\mathsf T}
\]

is (S_{2k})-invariant on the rational top Specht module
\(K_\mathbb Q\), which is irreducible.  Hence it is scalar.  Its trace is

\[
 |\mathcal M|2^k,
\]

because every (e_M) has (2^k) nonzero entries.  Since

\[
 \dim K_\mathbb Q
 =\binom{2k}k-\binom{2k}{k-1}
 =\frac1{k+1}\binom{2k}k,
\]

the scalar is

\[
 \frac{|\mathcal M|2^k}{\dim K_\mathbb Q}=(k+1)!=p!.
\tag{11}
\]

Set (r_z=\boldsymbol1_{C_z}-p^{-1}\boldsymbol1\).  The exact-cover
equations put (r_z\) in (K_\mathbb Q), while (4) gives
\(\langle r_z,e_M\rangle=\Delta_M(z)\).  Disjointness and (1) give

\[
 \langle r_z,r_w\rangle=
 \begin{cases}
 d(p-1)/p,&z=w,\\
 -d/p,&z\ne w.
 \end{cases}
\tag{12}
\]

Applying (11) to every pair (r_z,r_w) proves (7).
\(\square\)

## 3. The linear straightening constraints

The matching derivatives also obey every ordinary Specht straightening
relation, coordinate by coordinate.  The basic four-point instance is

\[
 e_{(a,b)(c,d)R}-e_{(a,c)(b,d)R}+e_{(a,d)(b,c)R}=0,
\tag{13}
\]

where (R) is a fixed pairing of the remaining (2k-4) points.  Hence
the same alternating relation holds with each (e) replaced by the
vector (\Delta).  It is simply the polynomial identity

\[
 (x_a-x_b)(x_c-x_d)-(x_a-x_c)(x_b-x_d)
 +(x_a-x_d)(x_b-x_c)=0.
\]

Together, all such straightening relations say that the collection of
top derivatives is a linear functional on (K_\mathbb Q).  They do not
use the fact that the functional arises from zero-one colour indicators.
The latter fact is the genuinely remaining global issue.

## 4. A sharp barrier for a matching-wise signed-count attack

The local cube condition and the global quadratic frame (9) are jointly
feasible in a strong convex sense.  This rules out a contradiction based
only on the signed count vector of one matching, its proper-cube condition,
and the second-moment identity (9).

First, a complement-invariant proper 17-colouring of (Q_{16}) with
\(\Delta=0\) exists.  One explicit linear construction is checked by the
companion verifier.  It uses a surjection
\(L:\mathbb F_2^{16}\to\mathbb F_2^4\) with no zero coordinate column and
with (L(\boldsymbol1)=0); its zero fibre is split into two colours using
a complement-invariant linear bit.  An odd kernel translation preserving
that bit pairs every colour class between the two cube parities, forcing
every signed count to vanish.

Second, for any (a\in\mathbb F_{17}), there is a complement-invariant
proper cube colouring whose signed vector is

\[
 E_a=32768e_a-2048(\boldsymbol1-e_a)
     =34816\left(e_a-\frac1{17}\boldsymbol1\right).
\tag{14}
\]

Colour all even cube vertices by (a), and partition the odd vertices,
in antipodal pairs, equally between the other sixteen colours.  No cube
edge has two endpoints of the same colour, and (14) follows at once.

Now take the zero vector with weight (1-1/1088), and with weight
\(1/1088) select (E_a) uniformly in (a).  It has mean zero and

\[
 \begin{aligned}
 \mathbb E[\Delta\Delta^{\mathsf T}]
 &=\frac1{1088}\cdot\frac1{17}
   \sum_a E_aE_a^{\mathsf T}\\
 &=\frac{2^{16}}{17}(17I-J),
 \end{aligned}
\tag{15}
\]

which is exactly (9) for (p=17).  This is a **weighted local witness**,
not a family indexed by the actual matchings and not a global colouring.
It shows precisely what it is intended to show: any proof that only
combines the one-matching constraints with the averaged quadratic frame
cannot reach a contradiction.  A successful top-degree argument must use
simultaneous straightening/cube data across different matchings, or another
genuinely global zero-one constraint.

## 5. Scope

Equations (5)--(13) are necessary consequences of a hypothetical tight
colouring.  The witness in Section 4 does not satisfy the cross-matching
straightening relations and makes no attempt to construct a colouring of
\(J(32,16)\).  Accordingly, this audit neither proves nor disproves the
existence of a tight 17-colouring.  It closes only the tempting
``one matching plus second moment'' top-degree route.

Run

```bash
python3 -B evidence/verify_top_degree_pairing_derivative.py
```

for direct checks of the (k=2) frame identity, the algebraic
straightening identity, the (p=17) arithmetic, and both explicit local
cube colourings.
