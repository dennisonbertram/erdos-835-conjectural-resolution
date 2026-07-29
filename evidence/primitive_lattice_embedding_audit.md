# Primitive \(bA_{16}\) lattice audit for the \(k=16\) case

Date: 2026-07-24.

## Verdict

Let
\[
 W=W_{14,15}(31),\qquad L=\ker_{\mathbb Z}W,\qquad
 b=\frac1{17}\binom{31}{15}=17\,678\,835.
\]
If the \(k=16\) case of Erdős--Rosenfeld #835 had a colour partition
\(D_0,\ldots,D_{16}\), then
\[
 u_i=1_{D_i}-1_{D_0}\quad(1\leq i\leq16)
\]
would span a primitive copy
\[
 S\cong \sqrt b\,A_{16},\qquad
 \operatorname{Gram}(S)=b(I_{16}+J_{16}).
\]

Wilson Smith data, the discriminant form at \(17\), and the complete
local Jordan-capacity test do **not** forbid this primitive embedding.
In particular, a prime dividing \(\det S\) but not \(\det L\) is not an
obstruction: those primes occur to even exponent and can be removed by
primitive gluing.

This note does not construct \(S\subset L\), much less the required
\(0\)-\(1\) colour classes.  It closes only the proposed
Smith/discriminant/local-lattice obstruction.

## 1. The forced sublattice really is primitive

The \(D_i\) partition the coordinate set into seventeen sets of size
\(b\).  The rational span of the \(u_i\) consists of the vectors that
are constant on each \(D_i\), with the seventeen constants summing to
zero.  If such a vector has integral coordinates, all seventeen
constants are integers, so it is an integral combination of the
\(u_i\).  Hence
\[
 \mathbb Q S\cap\mathbb Z^{\binom{31}{15}}=S.
\]
Thus \(S\) is primitive in the coordinate lattice, and therefore in
the primitive kernel \(L\).

Disjointness and \(|D_i|=b\) give
\[
 (u_i,u_j)=
 \begin{cases}
 2b&i=j,\\
 b&i\ne j,
 \end{cases}
\]
and consequently
\[
 \det S=17b^{16},\qquad
 b=3^2\cdot5\cdot19\cdot23\cdot29\cdot31.
\tag{1}
\]

## 2. Wilson data and the ambient determinant

Wilson's diagonal form for the subset-inclusion matrix has nonzero
entries
\[
 15-i
 \quad\text{with multiplicity}\quad
 m_i=\binom{31}{i}-\binom{31}{i-1},
 \qquad0\leq i\leq14.
\tag{2}
\]
The corresponding eigenvalues of \(WW^{\mathsf T}\) are
\[
 (15-i)(17-i)
 \quad\text{with the same multiplicities}.
\tag{3}
\]
Because \(L\) is the orthogonal complement of the saturated row
lattice, the covolume formula gives
\[
 \det L
 =\prod_{i=0}^{14}
 \left(\frac{17-i}{15-i}\right)^{m_i}.
\tag{4}
\]
Thus
\[
\begin{aligned}
\operatorname{rank}L&=35\,357\,670,\\
\det L&=
2^{45\,703\,018}
3^{40\,050\,449}
5^{34\,011\,401}
7^{18\,936\,940}\\
&\hspace{2.8em}\cdot11^{539\,400}
13^{26\,536}\cdot17.
\end{aligned}
\tag{5}
\]

The primes \(19,23,29,31\) in (1) are absent from (5), but each has
valuation \(16\) in \(\det S\).  For a primitive sublattice with
orthogonal complement \(T\),
\[
 \det S\,\det T
 =\det L\,[L:S\mathbin\perp T]^2.
\tag{6}
\]
An absent prime can therefore be cancelled by a glue index of valuation
eight.  Determinant valuations supply no contradiction.

## 3. The distinguished \(17\)-primary line matches

Let \(P_L\) be orthogonal projection onto \(L_{\mathbb Q}\), and let
\(e_X\) be any coordinate vector.  Transitivity makes the diagonal of
\(P_L\) constant, so
\[
 (P_Le_X,P_Le_X)
 =\frac{\operatorname{rank}L}{\binom{31}{15}}
 =\frac2{17}.
\tag{7}
\]
Since \(v_{17}(\det L)=1\), this gives the unique order-\(17\)
discriminant line
\[
 q_{L,17}\cong\left\langle\frac2{17}\right\rangle.
\tag{8}
\]

The inverse of \(I_{16}+J_{16}\) is
\(I_{16}-J_{16}/17\).  Hence the order-\(17\) line of \(S^*/S\)
has coefficient
\[
 -\frac{b^{-1}}{17}.
\tag{9}
\]
Now \(b\equiv8\pmod {17}\), so \(-b^{-1}\equiv2\pmod {17}\).
Therefore
\[
 q_{S,17}\cong\left\langle\frac2{17}\right\rangle
 =q_{L,17}.
\tag{10}
\]
The strongest one-dimensional discriminant comparison is exactly
compatible.

## 4. Complete local capacity check

The elementary divisors of the two-row Specht Gram lattice give the
following Jordan ranks.  Here \(a:c\) means \(c\) directions of
Gram valuation \(a\).

| \(p\) | Jordan valuations in \(L\otimes\mathbb Z_p\) |
|---:|:---|
| \(2\) | \(0:32768,\ 1:24946816,\ 2:10378056,\ 3:30\) |
| \(3\) | \(0:1,\ 1:30664889,\ 2:4692780\) |
| \(5\) | \(0:1346269,\ 1:34011401\) |
| \(7\) | \(0:16420730,\ 1:18936940\) |
| \(11\) | \(0:34818270,\ 1:539400\) |
| \(13\) | \(0:35331134,\ 1:26536\) |
| \(17\) | \(0:35357669,\ 1:1\) |

These ranks accommodate the target at every listed prime:

* at \(3\), \(S\) has sixteen scale-\(3^2\) directions and the
  matching ambient constituent has rank \(4\,692\,780\);
* at \(5\), \(S\) has sixteen scale-\(5\) directions and the matching
  constituent has rank \(34\,011\,401\);
* at \(7,11,13\), the target is unimodular and the ambient unimodular
  constituent has rank far greater than sixteen;
* at \(17\), the target has Jordan ranks \(15\) and \(1\), while the
  ambient ranks are \(35\,357\,669\) and \(1\); (10) matches the
  only delicate scale-\(17\) coefficient.

For odd \(p\), a unimodular \(\mathbb Z_p\)-form is diagonalizable, and
its reduction is classified by dimension and determinant square class.
Once the complement has dimension at least two, it can be chosen with
the required square class.  Thus the rank comparisons above give
primitive local embeddings, rather than merely determinant
inequalities.

At \(p=2\), \(b(I_{16}+J_{16})\) is even unimodular and its reduced
quadratic form has Arf invariant zero, hence it is \(H^8\).  The
unimodular constituent of \(L\otimes\mathbb Z_2\) is even of rank
\(32768\).  An even unimodular \(2\)-adic lattice is a sum of
hyperbolic planes and at most one anisotropic plane, so it contains
\(H^8\).

For each new prime \(q\in\{19,23,29,31\}\), the ambient lattice is
unimodular.  The absence of \(q\) from (5) is harmless even
constructively.  Diagonalize
\[
 b(I_{16}+J_{16})\cong
 \langle q c_1,\ldots,q c_{16}\rangle
\quad\text{over }\mathbb Z_q,
\]
where every \(c_i\) is a unit.  In sixteen orthogonal hyperbolic planes
with \((e_i,f_i)=1\), the primitive vectors
\[
 e_i+\frac{q c_i}{2}f_i
\tag{11}
\]
have exactly those norms and are mutually orthogonal.  The same
construction handles every prime not dividing \(\det L\) when needed.

Consequently no completion \(L\otimes\mathbb Z_p\), including
\(p=2,17\) and every \(p\mid b\), yields an obstruction of the proposed
kind.

## 5. Exact determinant-only countermodel

There is also a small concrete primitive embedding which makes the
determinant warning unambiguous:
\[
 b=2495^2+1883^2+80^2+2811^2,
\qquad
\gcd(2495,1883,80,2811)=1.
\tag{12}
\]
Let \(A_{16}=\{x\in\mathbb Z^{17}:\sum x_i=0\}\), and define
\[
 \Phi(x)=(2495x,\ 1883x,\ 80x,\ 2811x)\in\mathbb Z^{68}.
\tag{13}
\]
Then
\[
 (\Phi(x),\Phi(y))=b(x,y),
\]
so \(\Phi(A_{16})\cong\sqrt b\,A_{16}\).  Both \(A_{16}\subset
\mathbb Z^{17}\) and the coefficient vector in (12) are primitive
direct summands as abelian groups, so (13) is a primitive embedding.
In particular, \(\det S\) contains
\((19\cdot23\cdot29\cdot31)^{16}\) although the ambient
\(\mathbb Z^{68}\) is unimodular.

More literally, let \(R=35\,357\,670\), let \(D\) denote the integer in
(5), and set
\[
 K=\mathbb Z^{R-1}\perp\langle D\rangle .
\tag{14}
\]
Embedding (13) into the first \(68\) unit coordinates gives a primitive
copy of \(S\) in a positive-definite integral lattice \(K\) with
\[
 \operatorname{rank}K=\operatorname{rank}L,\qquad
 \det K=\det L.
\]
Thus even the exact ambient rank and determinant cannot prohibit the
target.  The lattice \(K\) is only a determinant countermodel: it is
not asserted to lie in the genus of \(L\).

## Scope and reproduction

The result is negative but definitive for this route:

* **proved:** Wilson/SNF determinant data, the \(17\)-primary
  discriminant line, and all local Jordan/Witt capacity tests are
  compatible with the forced primitive \(bA_{16}\);
* **not proved:** an integral embedding \(S\hookrightarrow L\);
* **not proved:** seventeen disjoint Steiner systems or a colouring.

Run

```bash
python3 -B evidence/verify_primitive_lattice_embedding_audit.py
```

The Wilson diagonal-form input is stated in Peter Sin's survey,
[Smith Normal Forms of Incidence Matrices](https://people.clas.ufl.edu/sin/files/snf.pdf),
Theorem 3.6.  The two-row Specht elementary-divisor input is from
Künzer--Nebe,
[Elementary divisors of Gram matrices of certain Specht modules](https://arxiv.org/abs/math/0203129).
