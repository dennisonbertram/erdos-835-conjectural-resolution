# Full integral \(-1\)-eigenlattice audit

This note tests whether the putative \(17\)-colour perfect-code partition of
the Odd graph \(O_{16}\) can be ruled out by the integral \(-1\)
eigenlattice alone.  The answer is sharply mixed:

* at the false \(k=4\) parameter, the lattice gives both a very short
  **3-adic unit-rank obstruction** and an independent exhaustive
  short-vector obstruction;
* the complete relevant local Jordan ranks, the distinguished \(p=k+1\)
  discriminant component, the 2-adic Witt type, primitivity, and the
  fibre-sum map are all compatible at \(k=16\).

Thus the local invariant which correctly rejects the control case does
not reject \(k=16\).  Any successful lattice proof at the target
parameter must retain more of the coordinate \(0/1\) geometry or find a
genuinely global short-vector obstruction.

## 1. The lattice forced by a perfect-code partition

Put

\[
 r=k-1,\qquad v=2r+1,
\]

and index coordinates by the \(r\)-subsets of a \(v\)-set.  Let \(D\) be
the adjacency matrix of the Odd graph, and let

\[
 W=W_{r-1,r}(v)
\]

be the unsigned inclusion matrix whose rows are \((r-1)\)-sets and whose
columns are \(r\)-sets.

For odd \(r\),

\[
 L_r:=\ker_{\mathbb Z}(D+I)
     =\ker_{\mathbb Z}W.
\]

Here is a direct proof of the non-obvious inclusion.  If \(Wx=0\), then
the sum of \(x_T\) over all \(r\)-sets containing any fixed \(s\)-set
vanishes for every \(0\leq s<r\).  Fix an \(r\)-set \(S\), and put

\[
 A_j=\sum_{\lvert T\cap S\rvert=j}x_T,\qquad
 P(t)=\sum_{j=0}^r A_jt^j.
\]

The preceding incidence sums say that \(P^{(s)}(1)=0\) for
\(0\leq s<r\).  Hence

\[
 P(t)=x_S(t-1)^r.
\]

The \(r\)-sets disjoint from \(S\) contribute
\(A_0=(-1)^rx_S=-x_S\), so \(Dx=-x\).  Conversely, the two rational
kernels have the same dimension

\[
 \binom{2r+1}{r}-\binom{2r+1}{r-1},
\]

and taking their intersections with the coordinate lattice proves the
integral equality.

Suppose the vertices are partitioned into \(p=k+1=r+2\) perfect codes,
with indicator vectors \(f_0,\ldots,f_{p-1}\).  Each fibre has

\[
 n=\frac{\binom{2r+1}{r}}{r+2}
\]

vertices, and

\[
 (D+I)f_i=\mathbf 1,\qquad \sum_i f_i=\mathbf 1.
\]

Therefore

\[
 u_i=f_i-f_{p-1}\in L_r\quad(0\leq i<p-1)
\]

and

\[
 (u_i,u_j)=
 \begin{cases}
 2n,&i=j,\\
 n,&i\ne j.
 \end{cases}
\]

The \(u_i\) span

\[
 S\cong \sqrt n\,A_{p-1},\qquad
 \operatorname{Gram}(S)=n(I_{p-1}+J_{p-1}).
\]

This copy is primitive even in the full coordinate lattice.  Indeed, a
vector in its rational span is constant on every fibre.  If an integer
multiple of it has integral coefficients, the constants in the
\(A_{p-1}\) parametrisation are divisible by that integer.  It follows
that \(S\) is also primitive in \(L_r\).

## 2. Determinant of the full trade lattice

Write

\[
 m_i=\binom{2r+1}{i}-\binom{2r+1}{i-1}.
\]

The eigenvalues of \(WW^{\mathsf T}\) are

\[
 (r-i)(r+2-i)\quad\text{with multiplicity }m_i
 \qquad(0\leq i<r).
\]

The nonzero Smith entries of \(W\) are \(r-i\), with the same
multiplicities.  The covolume formula for a saturated kernel consequently
gives

\[
 \boxed{\displaystyle
 \det L_r=
 \prod_{i=0}^{r-1}
 \left(\frac{r+2-i}{r-i}\right)^{m_i}.}
\]

For \(k=4\), this is

\[
 \det L_3=2^6\,3^{13}\,5.
\]

For \(k=16\), the rank and determinant are

\[
 \operatorname{rank}L_{15}=35\,357\,670
\]

and

\[
\det L_{15}
=2^{45\,703\,018}
 3^{40\,050\,449}
 5^{34\,011\,401}
 7^{18\,936\,940}
 11^{539\,400}
 13^{26\,536}
 17.
\]

The required sublattice has

\[
 \det S=n^{16}\,17,
\quad
n=17\,678\,835
=3^2\cdot5\cdot19\cdot23\cdot29\cdot31.
\]

The new primes \(19,23,29,31\) occur to the even exponent \(16\).  Hence
determinant orders alone give no primitive-embedding contradiction.  The
\(k=4\) control already shows why this observation cannot be sharpened
merely to “a prime absent from \(\det L\)”: its target determinant
\(7^4\cdot5\) contains the absent prime \(7\), again to an even exponent.

## 3. The fibre-sum map and the distinguished \(p\)-part

There is one useful restriction which determinant orders alone miss.  For
\(x\in L_r\), define its fibre sums

\[
 \theta(x)=
 \left(
 \sum_{a\in F_0}x_a,\ldots,
 \sum_{a\in F_{p-1}}x_a
 \right)\in A_{p-1}.
\]

The total coordinate sum of every element of \(L_r\) is zero, so the
displayed membership is literal.  Under \(S\cong A_{p-1}\) with its form
scaled by \(n\), restriction of the inner product sends \(x\) to

\[
 \frac{\theta(x)}n\in S^*.
\]

Consequently the gluing subgroup seen on the \(S\)-side lies in

\[
 \frac{(1/n)A_{p-1}}{A_{p-1}}\cong(\mathbb Z/n)^{p-1}.
\]

Since \(\gcd(n,p)=1\) in both cases, **the fibre-sum gluing has no
\(p\)-primary part**.  The unique \(p\)-primary discriminant form of
\(S\) must therefore agree directly with that of \(L_r\).

It does.

Let \(P_L\) be orthogonal projection from the coordinate space onto
\(L_r\), and let \(e_T\) be a coordinate vector.  Then

\[
 y=P_Le_T\in L_r^*,
\qquad
 (y,y)=(P_L)_{T,T}
=\frac{\operatorname{rank}L_r}{\binom{2r+1}{r}}
=\frac2p.
\]

Because \(v_p(\det L_r)=1\), the \(p\)-part of \(y\) generates the unique
order-\(p\) discriminant group.  Thus

\[
 q_{L_r,p}\cong\left\langle\frac2p\right\rangle.
\]

On the target side, a fundamental weight of \(A_{p-1}\) has norm
\((p-1)/p\).  Scaling the form by \(n\) gives

\[
 q_{S,p}\cong
\left\langle-\frac{n^{-1}}p\right\rangle.
\]

For prime \(p\geq5\),

\[
 n=\frac1p\binom{2p-3}{p-2}
   =\frac1{2p}\binom{2p-2}{p-1}
   \equiv-\frac12=\frac{p-1}{2}\pmod p.
\]

The congruence follows from
\(\binom{2p-2}{p-1}\equiv-p\pmod{p^2}\) (itself the immediate
one-step form of Wolstenholme's binomial congruence).  Hence

\[
 -n^{-1}\equiv2\pmod p
\]

and the two discriminant forms agree exactly.

For \(k=4\), both are \(\langle2/5\rangle\); in the particular integral
bases used by the verifier the displayed generator is
\(\langle3/5\rangle\), the same square class.  For \(k=16\),

\[
 n\equiv8\pmod{17},
\qquad
 q_{L_{15},17}=q_{S,17}
=\left\langle\frac2{17}\right\rangle.
\]

Thus the strongest extra condition supplied by the fibre-sum map is
compatible, not obstructive.

## 4. Complete local Jordan-rank test

The order of a discriminant group is not enough: a primitive embedding
of a \(q\)-unimodular rank-\(a\) lattice requires at least \(a\)
unimodular directions in the ambient \(q\)-adic lattice.  This is exactly
where the \(k=4\) control fails.

For the two-row Specht lattice \(L_r=S^{(r+1,r)}\), the
Künzer--Nebe/James--Schaper formula determines every \(q\)-adic Gram
elementary divisor.  The verifier implements that formula directly.
The notation below is

\[
 e:c
\quad\Longleftrightarrow\quad
\text{\(c\) Jordan directions have Gram valuation \(e\).}
\]

At \(k=4\):

\[
\begin{array}{c|l}
q&\text{valuation : multiplicity}\\ \hline
2&0:8,\ 1:6\\
3&0:1,\ 1:13\\
5&0:13,\ 1:1.
\end{array}
\]

The target \(7A_4\) is unimodular over \(\mathbb Z_3\), of rank \(4\).
But \(L_3\) has unimodular 3-adic rank only \(1\).  A primitive
embedding would remain injective after reduction modulo \(3\) and would
embed a nondegenerate four-dimensional form into a form of rank one,
which is impossible.  Therefore

\[
\boxed{7A_4\not\hookrightarrow L_3\otimes\mathbb Z_3.}
\]

This is a clean local explanation of the false control case.

At \(k=16\), the exact table is

\[
\begin{array}{c|l}
q&\text{valuation : multiplicity}\\ \hline
2&0:32\,768,\ 1:24\,946\,816,\ 2:10\,378\,056,\ 3:30\\
3&0:1,\ 1:30\,664\,889,\ 2:4\,692\,780\\
5&0:1\,346\,269,\ 1:34\,011\,401\\
7&0:16\,420\,730,\ 1:18\,936\,940\\
11&0:34\,818\,270,\ 1:539\,400\\
13&0:35\,331\,134,\ 1:26\,536\\
17&0:35\,357\,669,\ 1:1.
\end{array}
\]

Compare this with

\[
 n=3^2\cdot5\cdot19\cdot23\cdot29\cdot31.
\]

At \(3\), the target is \(3^2\) times a unimodular rank-\(16\)
lattice, and the ambient scale-\(3^2\) constituent has rank
\(4\,692\,780\).  At \(5\), the target has scale \(5\), and the matching
ambient constituent has rank \(34\,011\,401\).  At \(7,11,13\), the
target is unimodular and the ambient unimodular ranks are respectively
\(16\,420\,730\), \(34\,818\,270\), and \(35\,331\,134\).  At \(17\),
the target has Jordan ranks \(15\) and \(1\), while the ambient ranks are
\(35\,357\,669\) and \(1\); Section 3 proves that the unique
scale-\(17\) lines have the same discriminant coefficient.

These comparisons give actual local embeddings, not only inequalities.
For odd \(q\), unimodular forms over \(\mathbb Z_q\) are classified by
their nonsingular reductions over \(\mathbb F_q\).  Given the
rank-\(16\) target form, choose a complement of the required determinant
class inside the indicated high-rank Jordan constituent; finite-field
Witt decomposition gives the isometry, and integral Gram--Schmidt lifts
it.  Multiplying the form by \(q\) or \(q^2\) handles the \(5\)- and
\(3\)-constituents without changing primitivity of the underlying
module.

At the new primes \(19,23,29,31\), the ambient lattice is unimodular of
enormous rank.  A primitive vector of norm \(q^a u\) embeds in a
hyperbolic plane by

\[
 e+\frac{q^a u}{2}f
\]

when \((e,f)=1\); using independent hyperbolic planes handles all sixteen
target directions.  Over odd residue fields, the remaining high-rank
form has anisotropic dimension at most two, so the required unit forms
and complements have no Witt obstruction.

Thus the complete odd-prime **rank and Witt-capacity** test passes at
\(k=16\).  The one-dimensional scale-\(17\) discriminant form, where
rank alone would not suffice, was matched exactly in Section 3.

### The 2-adic refinement

Every vector in \(L_r\) has even norm: summing all rows of \(Wx=0\)
gives \(\sum_Tx_T=0\), and
\(\sum_Tx_T^2\equiv\sum_Tx_T\pmod2\).  Therefore

\[
 q(\bar x)=\frac{(x,x)}2\pmod2
\]

is a quadratic refinement of the reduced dot product.

#### The \(k=4\) control

The exact Gram computation gives

\[
 \operatorname{rank}_{\mathbb F_2}(\,\cdot\,,\,\cdot\,)=8,
\qquad
 \dim\operatorname{rad}=6,
\]

the quadratic form vanishes on the radical, and the nonsingular quotient
is hyperbolic.  Nevertheless, the required four-dimensional form embeds
in it: in the deterministic basis of the verifier, the four binary
coefficient words

\[
 0x24,\quad0x48,\quad0x6d,\quad0x109
\]

all have \(q=1\), and every distinct pair has polar product \(1\).
That is exactly the reduction of \(7(I_4+J_4)\).  By the classification
of even unimodular 2-adic lattices, the ambient hyperbolic rank-eight
constituent contains this Arf-one rank-four lattice (with another
Arf-one rank-four complement).  So \(2\)-adic data cannot explain the
\(k=4\) failure; the 3-adic test above does.

#### The \(k=16\) parameter

The lattice \(L_{15}\) is the integral two-row Specht lattice of shape
\((16,15)\).  A standard theorem on Specht Gram forms says that the rank
of its Gram matrix modulo \(2\) is the dimension of
\(D^{(16,15)}\).  This is the basic-spin module, of dimension

\[
 2^{15}=32\,768.
\]

Equivalently, the unimodular Jordan constituent of
\(L_{15}\otimes\mathbb Z_2\) is an even unimodular lattice of rank
\(32\,768\).

Meanwhile \(n\) is odd, and

\[
 n(I_{16}+J_{16})
\]

is even unimodular over \(\mathbb Z_2\).  Its reduced quadratic form has
\(32\,896\) zeros and Arf invariant \(0\), so it is the split lattice
\[
 H^8.
\]

The classification of even unimodular \(2\)-adic lattices writes the
ambient rank-\(32\,768\) constituent as hyperbolic planes plus at most
one anisotropic plane.  It therefore contains \(H^8\) as an orthogonal
direct summand.  This gives a primitive \(\mathbb Z_2\)-embedding of the
target.  Notice that this conclusion does **not** require knowing the
ambient Arf invariant.

Thus the 2-adic Arf/Witt test is precisely compatible at \(k=16\).

## 5. Independent global short-vector certificate at \(k=4\)

For \(k=4\), \(L_3\) has rank \(14\), Gram Smith diagonal

\[
 1,\ 3^7,\ 6^5,\ 30.
\]

The verifier constructs a saturated basis and performs an exact
Fincke--Pohst enumeration using a rational \(LDL^{\mathsf T}\)
decomposition.  The complete short-vector inventory is

\[
\begin{array}{c|rrrr}
\text{norm}&0&8&12&14\\ \hline
\text{number}&1&210&1260&5280.
\end{array}
\]

Every norm-\(14\) vector has fourteen nonzero coordinates, all
\(\pm1\).  Form the graph whose 5,280 vertices are these vectors and
join \(x\) to \(y\) when \(x\cdot y=7\).  It has

\[
 403\,200\text{ edges},\qquad
 152\leq\deg(x)\leq168,
\]

and an exhaustive exact bitset check finds no \(K_4\).

But a copy of \(\sqrt7A_4\) would supply four norm-\(14\) basis vectors
with every pairwise product equal to \(7\), exactly such a \(K_4\).
Therefore

\[
 \boxed{\sqrt7A_4\not\hookrightarrow L_3.}
\]

This is stronger than the known absence of five disjoint Fano planes:
even arbitrary signed integral vectors cannot realise the target Gram
matrix.

The 3-adic unit-rank test already rejects \(k=4\), while the computation
in this section gives an independent and strictly integral certificate.
The important warning for \(k=16\) is that the target's factor
\(3^2\) moves its 3-adic lattice into a scale where the ambient lattice
has millions of available directions.  At rank \(35\,357\,670\) and
target norm \(2n=35\,357\,670\), an analogous complete short-vector
enumeration is not presently available.  The complete local
Jordan-rank, discriminant-form, 2-adic Witt, and fibre-sum tests do not
close the problem.

## Reproduction

From the repository root:

```bash
python3 evidence/verify_full_eigenlattice.py
```

The script prints `full eigenlattice audit: PASS` only after checking the
determinants, Smith data, complete short-vector inventory, absence of the
dot-\(7\) four-clique, the explicit mod-\(2\) embedding, the complete
local Jordan multiplicities listed above, and the \(17\)-primary
coefficient calculation.

For the modular Specht-rank input used in the 2-adic paragraph, see
Künzer and Nebe, *Elementary divisors of Gram matrices of certain Specht
modules*, [arXiv:math/0203129](https://arxiv.org/abs/math/0203129).
