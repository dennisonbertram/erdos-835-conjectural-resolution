# Three-way trade and resolution evidence

This note records an independent attack on the following strengthening of the
first open case of Erdős problem 835.

> Can three pairwise block-disjoint systems
> \(S(r-1,r,2r+1)\) exist when \(r\) is odd?

The case relevant to the first open Erdős parameter is \(r=15\).  The results
below do **not** prove nonexistence at \(r=15\).  They identify the exact first
nonlinear condition, prove several equivalent formulations, and show that the
usual divisibility, intersection, spectral, and local-incidence relaxations all
remain feasible.

## 1. Three systems are a three-way Steiner trade

Put
\[
 v=2r+1,\qquad k=r,\qquad t=r-1
\]
and let \(W=W_{t,k}(v)\) be the \(0\)-\(1\) inclusion matrix whose rows are
\(t\)-subsets and whose columns are \(k\)-subsets.  A Steiner system has
indicator \(x\) satisfying
\[
 Wx=\mathbf 1,\qquad x\in\{0,1\}^{\binom vr}.
\]
Its number of blocks is
\[
 b=\frac{\binom{2r+1}{r-1}}r
  =\frac{\binom{2r+1}{r}}{r+2}.
\]
Thus three pairwise disjoint systems are precisely a three-way Steiner
\((v,k,t)\)-trade whose three legs have volume \(b\) and whose foundation is
the full point set.  At \(r=15\),
\[
 b=17\,678\,835,\qquad 3b=53\,036\,505.
\]

Here “Steiner” in the trade definition matters: every \(t\)-set occurs at
most once in each leg.  Equal row counts and volume \(b\) then force every
row count to be one.  Without the at-most-one condition, a cube-root
equation \(Wh=0\) only says that the three phase counts are equal in every
row; it does not force their common value to be one.

## 2. Exact external intersection distribution

Let \(\mathcal D\) be an \(S(r-1,r,2r+1)\), let \(A\) be an \(r\)-set, and
write
\[
 n_j(A)=|\{B\in\mathcal D:|A\cap B|=j\}|.
\]
The derived parameters are
\[
 \lambda_i
 =\frac{\binom{2r+1-i}{r-1-i}}{r-i}
 \qquad(0\le i\le r-1).
\]
Double-counting pairs \((I,B)\), where \(I\subseteq A\cap B\) and
\(|I|=i\), gives the triangular moment equations
\[
 \sum_{j=i}^{r}\binom ji n_j(A)=\binom ri\lambda_i.
 \tag{2.1}
\]
Inverting (2.1) gives the following closed forms.

If \(A\notin\mathcal D\), then \(n_r=0\) and
\[
 \boxed{\displaystyle
 n_j(A)=
 \binom rj\,
 \frac{\binom{r+1}{j+1}+(-1)^j}{r+2}}
 \qquad(0\le j\le r-1).
 \tag{2.2}
\]
If \(A\in\mathcal D\), then \(n_r=1\) and
\[
 \boxed{\displaystyle
 n_j(A)=
 \binom rj\,
 \frac{\binom{r+1}{j+1}-(r+1)(-1)^j}{r+2}}
 \qquad(0\le j\le r-1).
 \tag{2.3}
\]

In particular, (2.2) gives \(n_0=1\), whereas (2.3) gives \(n_0=0\).
Consequently:

* every \(r\)-set outside a system has a unique disjoint system block;
* no two blocks of the same system are disjoint; and
* between two block-disjoint systems, disjointness is a perfect matching.

For \(r=15\), the external distribution for \(j=0,\ldots,15\) is
\[
\begin{split}
(&1,105,3465,48685,350805,1414413,3368365,4871295,\\
 &4330755,2357355,771771,146055,15015,735,15,0).
\end{split}
\tag{2.4}
\]
Every nonzero entry in (2.4) is odd.  The quotient in (2.2) is
\[
(1,7,33,107,257,471,673,757,673,471,257,107,33,7,1).
\]
Thus the complete one-system and pairwise intersection moment equations are
nonnegative and integral at \(r=15\); they do not give a parity
contradiction.

The identity \(n_0=1\) is also the standard perfect-code equivalence:
an \(S(r-1,r,2r+1)\) is a perfect radius-one code in the odd graph
\[
 O_{r+1}=KG(2r+1,r).
\]
Three disjoint systems would give three disjoint perfect codes.  Their
induced graph is 2-regular, and its cycles have lengths divisible by three.
This condition is feasible for an abstract graph and is not by itself an
obstruction.

## 3. Linear, lattice, and local relaxations pass

Let \(N=\binom{2r+1}{r}\), \(c=1/(r+2)\), and write a system indicator as
\[
 x_i=c\mathbf1+g_i,\qquad g_i\in\ker_{\mathbb R}W.
\]
Pairwise block-disjointness gives
\[
 \|g_i\|^2=\frac{N(r+1)}{(r+2)^2},\qquad
 \langle g_i,g_j\rangle=-\frac{N}{(r+2)^2}\quad(i\ne j).
\]
This is the Gram matrix of a feasible simplex; real spectral geometry allows
as many as \(r+2\) colors.

For differences \(u=x_1-x_2\) and \(v=x_1-x_3\),
\[
 \operatorname{Gram}(u,v)
 =b\begin{pmatrix}2&1\\1&2\end{pmatrix},
 \qquad\det=3b^2.
\]
No local lattice obstruction follows from this Gram matrix.  Wilson's
diagonal form for \(W_{r-1,r}\) has diagonal entries
\[
 r,r-1,\ldots,1
\]
with the standard binomial-difference multiplicities.  Its congruence
conditions are exactly the familiar one-design divisibility conditions, not
a new three-way obstruction.

Several stronger-looking relaxations also remain feasible:

1. **Fractional exact cover.**  Set \(x_{a,B}=1/(r+2)\) for each of three
   colors \(a\) and every block \(B\).  Every facet equation sums to one, and
   the block-capacity sum is \(3/(r+2)\le1\).
2. **Pairwise association counts.**  The degrees in (2.2) sum to \(b\).
   Abstractly, a 1-factorization of \(K_{b,b}\) can be grouped into regular
   bipartite relation graphs of precisely those degrees.
3. **Facet-incidence hypergraph.**  Ignoring subset labels, an
   \(r\)-regular linear 3-partite 3-uniform hypergraph on \(b+b+b\) vertices
   exists whenever \(b\) is odd.  On three copies of \(\mathbb Z_b\), take
   \[
   (a,a+s,a+2s),\qquad a\in\mathbb Z_b,\quad 0\le s<r.
   \]
   Since two is invertible modulo \(b\), no pair of vertices is repeated.
4. **Derived links.**  Fixing an \((r-2)\)-set turns each leg into a
   one-factor of \(K_{r+3}\).  Fixing an \((r-3)\)-set turns each leg into an
   \(STS(r+4)\).  At \(r=15\) this is \(STS(19)\), for which three disjoint
   systems are locally feasible.

The standard trade bounds are also too small.  The ordinary minimum volume
\(2^t\) and the known gaps close to \(2^{t+1}\) are tiny compared with
\(b=17\,678\,835\) at \(t=14\); the standard foundation lower bound
\(k+t+1=2r\) is below the actual \(v=2r+1\).

## 4. The first genuinely nonlinear condition

Suppose instead that one is given a simple
\[
 \mathcal U:(r-1)\text{-}(2r+1,r,3)
\]
design.  Let \(M=M(\mathcal U)\) be its facet-by-block incidence matrix.
Every row of \(M\) has weight three and every column has weight \(r\).

Resolving \(\mathcal U\) into three Steiner systems is exactly the problem of
coloring its blocks with three colors so that every row sees all three
colors.  This has a useful classification-free linearization over
\(\mathbb F_4\).

### Theorem 4.1 (nowhere-zero \(\mathbb F_4\)-flow criterion)

\(\mathcal U\) resolves into three Steiner systems if and only if there is a
vector
\[
 c\in(\mathbb F_4^\*)^{|\mathcal U|}
 \quad\text{such that}\quad Mc=0.
 \tag{4.1}
\]

**Proof.**  The three nonzero elements of \(\mathbb F_4\) sum to zero.  In
characteristic two, three nonzero elements \(a,b,c\) satisfy \(a+b+c=0\) if
and only if they are the three distinct nonzero elements: if two are equal,
the third would be zero.  Therefore each row of (4.1) is exactly a rainbow
constraint.  Conversely, labeling three Steiner legs by
\(\mathbb F_4^\*\) gives (4.1).  \(\square\)

Write \(\mathbb F_4=\mathbb F_2(\alpha)\).  With \(c=u+\alpha v\), (4.1) is
equivalent to
\[
 u,v\in C:=\ker_{\mathbb F_2}M,\qquad
 \operatorname{supp}(u)\cup\operatorname{supp}(v)=\mathcal U.
 \tag{4.2}
\]
Thus the obstruction is exactly that the binary cycle code \(C\) cannot be
covered by two codewords.  In binary-matroid language, \(M\) admits no
nowhere-zero 4-flow.

If the legs have indicators \(x_1,x_2,x_3\), one may take
\[
 u=x_1+x_3,\qquad v=x_2+x_3.
\]
Then
\[
 |u|=|v|=2b,\qquad |\operatorname{supp}(u)\cap\operatorname{supp}(v)|=b.
 \tag{4.3}
\]
This yields two immediate exact screening tests:

* \(\dim_{\mathbb F_2}\ker M\ge2\); and
* if \(b\) is odd, then \(\ker M\) cannot be self-orthogonal.

The second test is especially relevant at \(r=15\), where \(b\) is odd:
equation (4.3) would give \(u\cdot v=1\) over \(\mathbb F_2\).  Hence any
candidate simple \(14\)-\((31,15,3)\) design whose binary kernel is
self-orthogonal is rigorously nonresolvable.

The exact number of labeled resolutions is the nowhere-zero flow count
\[
 F_{\mathcal U}(4)
 =\sum_{A\subseteq\mathcal U}
   (-1)^{|\mathcal U|-|A|}\,
   4^{\,|A|-\operatorname{rank}_{\mathbb F_2}M_A}.
 \tag{4.4}
\]
It is zero precisely when no resolution exists, and the number of unlabeled
resolutions is \(F_{\mathcal U}(4)/6\).

There is an equivalent two-stage graph criterion.  A first Steiner leg
\(\mathcal D\subseteq\mathcal U\) selects one block in every row.  Delete it
from every row and join the two residual blocks.  This produces an
\(r\)-regular graph \(H_{\mathcal D}\) on \(2b\) vertices.  The remaining
two legs exist if and only if \(H_{\mathcal D}\) is bipartite.  Its connected
components are precisely the two-leg bitrade components on which a Kempe
switch can interchange the two residual colors.

Finally, fixing an \((r-2)\)-set \(Q\) in \(\mathcal U\) gives a cubic graph
on the \(r+3\) points outside \(Q\): its edges are the blocks containing
\(Q\).  A resolution of \(\mathcal U\) induces a 3-edge-coloring of every
one of these cubic link graphs.  A single snark link is therefore a local
certificate of nonresolvability, although link 3-edge-colorability is not
sufficient for a globally compatible resolution.

## 5. Tests at \(r=3,5,15\)

### \(r=3\)

There are 30 labeled Fano planes \(S(2,3,7)\).  Their block-disjointness graph
is 8-regular and triangle-free, so its maximum clique has size two.  For a
fixed Fano plane, its eight disjoint mates pairwise intersect in exactly one
block.

Take two disjoint Fano planes and let \(\mathcal U\) be the complement of
their 14 blocks among all 35 triples.  Then \(\mathcal U\) is a simple
\(2\)-\((7,3,3)\) design, proving that the union-design relaxation itself is
feasible.  Its binary incidence kernel has dimension six and weight
distribution
\[
 1+21z^8+42z^{12}.
\]
It is doubly even and self-orthogonal; the largest union of two kernel-word
supports has size 18 rather than 21.  The \(\mathbb F_4\)-flow criterion
therefore gives \(F_{\mathcal U}(4)=0\), exactly detecting
nonresolvability without enumerating colorings.

### \(r=5\)

Kramer and Mesner proved that at most two mutually disjoint
\(S(4,5,11)\) systems exist.  McKay and Radziszowski enumerated 67
nonisomorphic simple \(4\)-\((11,5,3)\) designs and proved that no such
design is resolvable into three Witt systems.  Thus the simple
\(\lambda=3\) relaxation is feasible, but its nowhere-zero
\(\mathbb F_4\)-flow count is zero in every case.  Here \(b=66\) is even,
so self-orthogonality alone would not contradict (4.3); the full support
condition, not just its parity shadow, is needed.

### \(r=15\)

All divisibility parameters, the complete intersection distribution (2.4),
the simplex Gram matrix, and the abstract local relaxations pass.  A simple
\(14\)-\((31,15,3)\) design is not presently known here, let alone a
resolution.  For any candidate \(\mathcal U\), the first decisive checks are:

1. compute \(\operatorname{rank}_{\mathbb F_2}M\);
2. test whether \(\ker M\) is self-orthogonal;
3. search for two kernel words whose supports cover all \(3b\) coordinates;
4. equivalently, solve the nowhere-zero \(\mathbb F_4\)-flow problem; and
5. reject immediately if any cubic \((r-2)\)-link is not 3-edge-colorable.

These are exact nonlinear obstructions, but no parameter-only proof that
they fail for every possible \(\mathcal U\) is currently known.

## 6. Why the broad binary sphere-kernel cannot prove the parity conjecture

Fix a hypothetical system \(\mathcal A=S(r-1,r,2r+1)\), and let
\(\mathcal O\) be the \(r\)-sets outside \(\mathcal A\).  Let \(N\) be the
facet-by-\(\mathcal O\) incidence matrix over \(\mathbb F_2\).  The unique
block of \(\mathcal A\) disjoint from an outside block partitions
\(\mathcal O\) into \(b\) spheres of size \(r+1\); write \(Q\) for their
incidence matrix.  The difference of two mates of \(\mathcal A\) lies in
\[
 K=\ker N\cap\ker Q.
\]
It is tempting, when \(r\equiv3\pmod4\), to try to prove that \(K\) is
doubly even.  This is impossible already at the level of dimensions for
\(r=15\).

Let \(W\) be the facet-by-all-block incidence matrix and let \(R\) contain
the columns belonging to \(\mathcal A\), so \(W=[N\ R]\).  The usual
boundary rank of the full simplex is
\[
 \operatorname{rank}W=\binom{2r}{r-1}.
\]
Moreover \(\operatorname{rank}N=\operatorname{rank}W\).  Indeed, for
\(P\in\mathcal A\) and \(x\notin P\), the mod-two boundary of
\(P\cup\{x\}\) expresses the column of \(P\) as the sum of the other \(r\)
columns.  Every one of those other blocks is outside \(\mathcal A\), since
it shares an \((r-1)\)-facet with \(P\).

The row space of \(W\) is nondegenerate.  One quick proof uses the two
consecutive unsigned boundary matrices \(W\) and \(U\).  Over
\(\mathbb F_2\),
\[
 W^{\mathsf T}W+UU^{\mathsf T}=I,\qquad WU=0,
\]
because \(2r+1\) is odd.  Hence a vector in
\(\operatorname{row}W\cap\ker W\) is zero.  It follows that
\(\operatorname{rank}(WW^{\mathsf T})=\operatorname{rank}W\).

Put \(C=\ker N\), \(c=\dim C\), and let \(\delta\) be the dimension of the
radical of the dot product on \(C\).  Since
\[
 NN^{\mathsf T}=WW^{\mathsf T}+RR^{\mathsf T},
\]
rank perturbation gives
\[
 \delta=\operatorname{rank}N-\operatorname{rank}(NN^{\mathsf T})\le b.
\]
Also \(\dim K\ge c-b\).  Every word of \(C\) has even weight when \(r\) is
odd: summing all facet equations counts each selected block \(r\) times.
Thus the dot product on \(C\) is alternating.  If \(K\) were
self-orthogonal, the standard bound in the possibly degenerate symplectic
space \(C\) would give
\[
 \dim K\le\frac{c+\delta}{2}\le\frac{c+b}{2}.
\]

At \(r=15\),
\[
\begin{aligned}
 b&=17\,678\,835,\\
 |\mathcal O|&=282\,861\,360,\\
 \operatorname{rank}N&=\binom{30}{14}=145\,422\,675,\\
 c&=137\,438\,685.
\end{aligned}
\]
Consequently
\[
 \dim K\ge119\,759\,850
 \quad\text{but}\quad
 \frac{c+b}{2}=77\,558\,760.
\]
Therefore \(K\) is necessarily non-self-orthogonal.  In fact it contains a
word of weight \(2\bmod4\): on an even code the quadratic form
\(q(z)=|z|/2\bmod2\) has polar form \(u\cdot v\), so a nonorthogonal pair
forces \(q\) to be nonzero on one of \(u,v,u+v\).

This does **not** disprove the narrower conjecture that differences of
actual exact-one mates have weight divisible by four.  It proves that any
such theorem must use the nonlinear exact-cover conditions, not merely the
binary facet and sphere equations.

## 7. References

* E. S. Kramer and D. M. Mesner, “Intersections among Steiner systems,”
  *Journal of Combinatorial Theory, Series A* **16** (1974), 273–285.
  <https://doi.org/10.1016/0097-3165(74)90054-5>
* B. D. McKay and S. P. Radziszowski, “The Nonexistence of
  \(4\)-\((12,6,6)\) Designs,” in *Computational and Constructive Design
  Theory* (1996), 177–188.
  <https://users.cecs.anu.edu.au/~bdm/papers/McKayRadziszowski12_6_6_designs.pdf>
* M. Asgari and N. Soltankhah, “On non-existence of some Steiner
  \(t\)-\((v,k)\) trades of certain volumes,”
  <https://arxiv.org/abs/0806.1390>.
* S. Rashidi and N. Soltankhah, “On possible volume of
  \(\mu\)-\((v,k,t)\) trades,” <https://arxiv.org/abs/1310.7759>.
* M. Golalizadeh and N. Soltankhah, “Minimum possible volume size of
  \(u\)-way trades,” <https://arxiv.org/abs/1908.01340>.
