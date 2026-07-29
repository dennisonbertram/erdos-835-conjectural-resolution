# The nilpotent-shift compression: exact consequences and breakpoint

This note studies the following necessary condition for a tight colouring
in Erdős--Rosenfeld problem 835.  Put
\[
 \Omega=\binom{[32]}{16},\qquad
 W=W_{15,16}(32),\qquad
 K=\ker_{\mathbb C}W,
\]
let \(P\) be the orthogonal projector onto \(K\), and let
\[
 D=\operatorname{diag}\bigl(\zeta^{c(S)}:S\in\Omega\bigr),
 \qquad \zeta=e^{2\pi i/17}.
\]
For a tight colouring, the normalized vectors
\[
 v_j(S)=|\Omega|^{-1/2}\zeta^{j c(S)},\qquad 1\le j\le16,
\]
are orthonormal members of \(K\).  The compression
\[
 T=PDP\big|_K
\]
therefore has the reducing block
\[
 v_1\longmapsto v_2\longmapsto\cdots\longmapsto v_{16}
 \longmapsto0.
\tag{0.1}
\]

The results below show exactly what can and cannot be extracted from
this block without introducing genuinely new information about the
colour classes.  In particular, the block is not a loose spectral
relaxation: it canonically reconstructs the seventeen-dimensional
colour algebra.  Trace, principal-angle, characteristic-polynomial,
and first \(17\)-adic tests are all compatible with the unresolved
\(k=16\) case.

## 1. A finite-dimensional dilation lemma

Let \(P\) be any orthogonal projection, let \(D\) be unitary with
\(D^q=I\), and put \(T=PDP|_{\operatorname{ran}P}\).

**Lemma 1.**  Suppose \(T\) has a reducing subspace with an orthonormal
basis \(x_1,\ldots,x_{q-1}\) on which
\[
 Tx_j=x_{j+1}\ (j<q-1),\qquad Tx_{q-1}=0,
\]
and the adjoint acts as the reverse shift.  Then, on putting
\[
 x_0=Dx_{q-1},
\]
the space
\[
 H=\langle x_0,x_1,\ldots,x_{q-1}\rangle
\]
is a common reducing subspace for \(P\) and \(D\), and
\[
 P|_H=I_H-x_0x_0^*,\qquad
 Dx_j=x_{j+1}\quad(j\ {\rm mod}\ q).
\tag{1.1}
\]
Conversely, (1.1) compresses to the reducing nilpotent shift of length
\(q-1\).

**Proof.**  For \(j<q-1\),
\[
 \|PDx_j\|=\|Tx_j\|=1=\|Dx_j\|.
\]
Equality for an orthogonal projection implies \(Dx_j\in\operatorname{ran}P\),
so \(Dx_j=x_{j+1}\).  At the other endpoint,
\(PDx_{q-1}=0\), whence \(x_0=Dx_{q-1}\in\ker P\) and has norm one.
Thus \(x_0\) is orthogonal to the other \(x_j\).  Also
\[
 x_0=D^{q-1}x_1,\qquad Dx_0=D^qx_1=x_1.
\]
This proves (1.1); the converse is immediate. \(\square\)

Consequently \(D|_H\) has every \(q\)-th root of unity exactly once.
If
\[
 g_a=q^{-1/2}\sum_{j=0}^{q-1}\zeta^{-aj}x_j,
\]
then \(Dg_a=\zeta^a g_a\), while in this eigenbasis
\[
 P|_H=I-\frac1qJ.
\tag{1.2}
\]
For a diagonal \(D\), each \(g_a\) is supported on the \(a\)-th phase
fibre.  In the colouring situation \(x_j=v_j\), and Fourier inversion
gives
\[
 g_a=|c^{-1}(a)|^{-1/2}\mathbf1_{c^{-1}(a)}.
\]
Thus the shift block is precisely the centred colour-indicator algebra
\[
 H=\langle\mathbf1_{c^{-1}(0)},\ldots,
          \mathbf1_{c^{-1}(16)}\rangle,\qquad
 H\cap K=\mathbf1^\perp\cap H.
\tag{1.3}
\]

This also gives the exact principal-angle statement.  The block
contributes fifteen singular values \(1\) and one singular value \(0\)
to \(PDP|_K\).  Equivalently, \(K\) and \(D^{-1}K\) have at least fifteen
zero principal angles and one right-angle endpoint on this reducing
summand.  For every \(m\ge1\),
\[
 \operatorname{tr}\bigl((T^*T)^m\bigr)\ge15.
\tag{1.4}
\]
The two defect operators restrict to the endpoint lines:
\[
 (I_K-T^*T)|_{H\cap K}=x_{q-1}x_{q-1}^*,\qquad
 (I_K-TT^*)|_{H\cap K}=x_1x_1^*.
\tag{1.5}
\]

There is also an exact orbit-of-projections formulation.  Put
\[
 P_j=D^jPD^{-j}\qquad(0\le j<q).
\]
On \(H\), after indexing \(x_j=D^jx_0\) cyclically,
\[
 P_j|_H=I_H-x_jx_j^*,\qquad
 \sum_{j=0}^{q-1}P_j|_H=(q-1)I_H.
\tag{1.6}
\]
If \(F_a\) is the coordinate projection onto the \(\zeta^a\)-eigenspace
of the diagonal \(D\), Fourier twirling gives the global identity
\[
 \frac1q\sum_{j=0}^{q-1}P_j=\sum_{a=0}^{q-1}F_aPF_a.
\tag{1.7}
\]
Thus the right side of (1.7) has eigenvalue \((q-1)/q\) on all of \(H\).
For the colouring vectors this is exactly the familiar
colour-fibre compression eigenvalue \(16/17\).

## 2. Sixteen vanishing characteristic coefficients

Let \(N=|\Omega|\) and \(d=\operatorname{rank}P=N/17=35\,357\,670\).
For \(I\subseteq\Omega\), write \(P[I]\) for the corresponding principal
submatrix and
\[
 c(I)=\sum_{S\in I}c(S)\pmod {17}.
\]

**Lemma 2.**  If the reducing block (0.1) exists, then for
\[
 d-15\le r\le d
\]
one has
\[
 \sum_{\substack{I\subseteq\Omega\\|I|=r}}
 \det P[I]\,\zeta^{c(I)}=0.
\tag{2.1}
\]
Moreover, for every \(a\in\mathbb Z/17\mathbb Z\),
\[
 \boxed{\displaystyle
 \sum_{\substack{|I|=r\\c(I)=a}}\det P[I]
 =\frac1{17}\binom dr.}
\tag{2.2}
\]

**Proof.**  Choose an isometry \(U:\mathbb C^d\to\mathbb C^N\) with
\(P=UU^*\).  The \(r\)-th elementary symmetric function of
\(U^*DU\) is, by applying Cauchy--Binet on the \(r\)-th exterior power,
\[
 e_r(U^*DU)=
 \sum_{|I|=r}\det P[I]\prod_{S\in I}\zeta^{c(S)}.
\tag{2.3}
\]
The reducing shift makes the characteristic polynomial of \(U^*DU\)
divisible by \(\lambda^{16}\), proving (2.1).

Group (2.1) by \(c(I)\).  Its seventeen coefficients are rational.
The minimal polynomial of \(\zeta\) is
\(1+X+\cdots+X^{16}\), so all seventeen grouped coefficients are equal.
Their sum is
\[
 \sum_{|I|=r}\det P[I]=e_r(P)=\binom dr,
\]
which proves (2.2). \(\square\)

Thus the principal-minor measure at any of the top sixteen possible
sizes has exactly uniform colour-sum modulo \(17\).  This looks
restrictive, but it is already a reformulation of the shift summand
rather than an independent condition: on the reducing decomposition,
\(\det(I+tT)\) contains the factor
\(\det(I+tS_{16})=1\).  A useful probabilistic shadow is supplied by the
rank-sixteen projector \(Q\) onto
\(\langle v_1,\ldots,v_{16}\rangle\), whose kernel is
\[
 Q_{A,B}=\frac{17\,\mathbf1_{c(A)=c(B)}-1}{N}.
\tag{2.4}
\]
A rank-sixteen determinantal sample from \(Q\) chooses one point in
sixteen distinct colour fibres, omitting a uniformly distributed
seventeenth fibre.  Its colour-sum is therefore uniform.  Orthogonally
splitting the operator as \(P=Q+(P-Q)\), and hence the compressed
operator into its reducing shift and complementary blocks, explains why
(2.2) is not, by itself, a new obstruction.  (This statement uses the
operator factorization; it does not assert that the two associated
determinantal point processes are independent.)

## 3. The explicit Johnson projector and its first 17-adic tangent

The top Johnson projector has the exact entry kernel
\[
 P_{A,B}=p_t,\qquad t=|A\cap B|,\qquad
 \boxed{\displaystyle
 p_t=\frac{(-1)^{16-t}}{17\binom{16}{t}}.}
\tag{3.1}
\]
Indeed \(p_{16}=1/17\), and summing a column over a \(15\)-star gives
\[
 (16-t)p_{t+1}+(t+1)p_t=0.
\]

Work in the localization \(\mathbb Z_{(17)}\) and define
\[
 B=\frac{17P-J}{17}=P-\frac1{17}J.
\tag{3.2}
\]
The entries of \(B\) are \(17\)-integral.  More exactly, using
\[
 \binom{16}{t}
 =(-1)^t\prod_{i=1}^t\left(1-\frac{17}{i}\right)
 \pmod {17^2},
\]
one obtains
\[
 \boxed{\displaystyle
 B_{A,B}\equiv H_{|A\cap B|}\pmod {17},\qquad
 H_t=\sum_{i=1}^t i^{-1}\in\mathbb F_{17}.}
\tag{3.3}
\]

This is the natural place to hope for a valuation contradiction in
(2.2).  The first-rank test is exactly compatible:

**Lemma 3.**
\[
 \operatorname{rank}_{\mathbb F_{17}}(\overline B)=d+1
 =35\,357\,671.
\tag{3.4}
\]

**Proof.**  Over \(\mathbb Q\), \(B\) has eigenvalue \(-d\) on the
constant line, eigenvalue \(1\) on \(K\), and eigenvalue \(0\) on the
other Johnson constituents.  Hence \(\operatorname{rank}_{\mathbb Q}B=d+1\),
so reduction cannot have larger rank.  Direct arithmetic gives
\[
 d=35\,357\,670\equiv-1\pmod {17}.
\]
The characteristic polynomial therefore reduces to
\[
 X^{N-d-1}(X-1)^{d+1}.
\]
The algebraic multiplicity of the nonzero eigenvalue forces the reduced
rank to be at least \(d+1\), proving equality. \(\square\)

In particular the tempting claim that every relevant large minor gains
an extra factor of \(17\) is false: the first tangent already has enough
rank to support those minors.  A successful \(17\)-adic continuation
would have to calculate the colour-refined cofactors (or a higher
tangent), not merely the rank of \(17P-J\).

## 4. Low-order Schatten data are much too slack

The one- and two-fibre intersection distributions determine the
Hilbert--Schmidt norm.  In the equivalent
\(LS(14,15,31)\) formulation, let \(F_a\) be the coordinate projection
onto a colour class and \(T_a=PF_aP\).  The exact pair moments are
\[
 \operatorname{tr}T_a^2=\frac{98\,215\,750}{289},\qquad
 \operatorname{tr}(T_aT_b)=\frac{31\,429\,040}{289}\quad(a\ne b).
\]
Fourier orthogonality gives
\[
 \boxed{\displaystyle
 \|PDP\|_{\mathrm{HS}}^2
 =17\left(
 \operatorname{tr}T_a^2-\operatorname{tr}(T_aT_b)\right)
 =3\,928\,630.}
\tag{4.1}
\]
The shift requires only the contribution \(15\), so (4.1) gives no
contradiction.  Higher Schatten moments introduce three- and
higher-colour block correlations; they are not fixed by the known
one- and two-fibre design equations.

## 5. Exact controls at \(k=2,4,6\)

The same formulation behaves correctly in the first three even cases.

* **\(k=2\), positive.**  Colour the six edges of \(K_4\) by its three
  perfect matchings.  Every vertex-star sees all three colours.  The two
  nontrivial Fourier characters span \(\ker W_{1,2}(4)\), and
  \(PDP\) is exactly the nilpotent shift of length two.  The
  colour-refined principal-minor identities (2.2) hold for both
  \(r=1,2\).

* **\(k=4\), negative.**  A tight colouring would derive at any fixed
  point to five pairwise block-disjoint Fano planes on seven points.
  Exact cover enumerates all thirty labelled Fano planes.  A fixed one
  has eight disjoint mates, and every pair of those mates intersects in
  one block.  Thus the disjointness graph has clique number two, not
  five.

* **\(k=6\), negative.**  A tight colouring would derive to seven
  pairwise block-disjoint Witt \(S(4,5,11)\) systems.  Exact cover gives
  144 systems disjoint from a fixed Witt system.  Among their
  \(\binom{144}{2}=10\,296\) pairs, 6,336 intersect in six blocks and
  3,960 intersect in eighteen blocks.  Again the disjointness graph has
  clique number two.

The accompanying verifier independently reproduces these finite
controls, (3.1)--(3.3), the \(d\equiv-1\pmod {17}\) arithmetic, (4.1),
and the \(k=2\) principal-minor sectors:

```bash
/opt/homebrew/bin/python3 evidence/verify_nilpotent_shift_obstruction.py
```

## 6. Exact remaining gap

The reducing shift, its principal-angle pattern, its characteristic
coefficient vanishings, and its common cyclic dilation are all
equivalent manifestations of the same seventeen-dimensional colour
algebra.  The universal trace identities through two fibres and the
first \(17\)-adic rank test admit this algebra.

To turn this route into a proof of nonexistence, one still needs at least
one genuinely new ingredient, for example:

1. a colour-refined cofactor congruence contradicting (2.2);
2. a bound on a third or higher Schatten moment using the actual Johnson
   kernel, not only its two-fibre marginals; or
3. a theorem excluding a seventeen-dimensional coordinatewise-product
   algebra inside \(E_0\oplus E_{16}\).

No such contradiction is proved here.  Therefore this note does **not**
resolve problem 835; it isolates the exact point at which the
nilpotent-shift approach becomes the original large-set problem again.
