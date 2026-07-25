# Mersenne support functionals: exact point rank and 2-adic filtration

Date: 2026-07-24.

Status: **proved reduction and conditional parameter theorems; not a
solution of Erdős--Rosenfeld Problem 835**.

This note audits the proposed route from the support-restricted trade
lattice to a \(2^{14}\)-dimensional Lagrangian in the basic-spin
quotient.  It proves three things:

1. the exact functional space dual to the support constraint, including
   a necessary \(2\)-saturation caveat;
2. the point-by-block incidence matrix of a hypothetical
   \(S(14,15,31)\) has full binary row rank \(31\);
3. all truncated subset stars have an exact top-Specht projection norm,
   whose \(2\)-adic valuations give a sharp filtration at \(r=15\).

The deterministic checker is

```bash
python3 -B evidence/verify_mersenne_spin_functional_audit.py
```

It uses exact integer, rational, and bit-packed binary arithmetic.

## 1. The exact functional space and the saturation caveat

Let
\[
 W=W_{r-1,r}(2r+1),\qquad
 L=\ker_{\mathbb Z}W,\qquad C=L/2L.
\]
Write \(R=\operatorname{rad}C\) for the radical of the coordinate dot
product and \(S=C/R\).  Let \(A\) be an
\(S(r-1,r,2r+1)\), and let
\[
 \epsilon_A:L\longrightarrow\mathbb Z^A
\]
be coordinate restriction.  Put \(M_A=\epsilon_A(L)\) and
\(\Lambda(A)=\ker\epsilon_A\).  Since \(M_A\) is free, reduction of the
exact sequence \(0\to\Lambda(A)\to L\to M_A\to0\) gives
\[
 0\longrightarrow \Lambda(A)/2\Lambda(A)
 \longrightarrow C
 \longrightarrow M_A/2M_A
 \longrightarrow0.                                      \tag{1}
\]

This is the exact support map.  It is not automatically the ordinary
binary coordinate restriction \(C\to\mathbb F_2^A\).  Those maps agree
precisely when the image lattice \(M_A\) is \(2\)-saturated in its
rational span.  Equivalently,
\[
 \operatorname{rank}_{\mathbb F_2}(\operatorname{res}_A C)
 =\operatorname{rank}_{\mathbb Q}\epsilon_A.              \tag{2}
\]
Thus any \(r=15\) spin-Lagrangian proof must either prove (2) or work
with the dual image lattice \(M_A^*\), whose functionals can be divided
\(2\)-adically and need not be ordinary binary vectors on \(A\).

Assume (2), and choose binary bases of \(C\) and \(R\).  Restrict their
words to the coordinates in \(A\), obtaining row matrices \(C_A,R_A\).
The ordinary \(A\)-supported functionals which descend to \(S\) form
\[
 U_A=\ker R_A/\ker C_A,                                  \tag{3}
\]
because \(\ker R_A\) consists exactly of the coordinate functionals
vanishing on \(R\), while \(\ker C_A\) consists of those already
vanishing on all of \(C\).  Under the nondegenerate pairing on \(S\),
the image of the support kernel is
\[
 \operatorname{im}(\bar\Lambda(A)\to S)=U_A^\perp.        \tag{4}
\]
In particular, a Lagrangian image at \(r=15\) requires
\(\dim U_A=2^{14}=16\,384\), together with total singularity.

The exact small cases are:
\[
\begin{array}{c|ccccc}
r&\operatorname{rank}C_A&\operatorname{rank}R_A&
\dim\ker R_A&\dim\ker C_A&\dim U_A\\ \hline
3&7&3&4&0&4\\
5&55&55&11&11&0.
\end{array}
\]
At \(r=3\), \(\ker R_A\) is exactly the \([7,4,3]\) Hamming
code, namely the row space of the point-by-\(A\)-block incidence
matrix.  At \(r=5\), both kernels are the same \(11\)-dimensional
point-incidence code, so every one of those functionals is already a
row dependency and contributes zero to \(U_A\).  Equality (2) holds in
both cases, with common ranks \(7\) and \(55\).

This explains the small-case split exactly.  It does **not** justify
extrapolating either behavior to \(r=15\).

### Truncated point stars always annihilate the full radical

There is nevertheless one uniform point-functional theorem.  It applies
directly to ordinary binary vectors supported on \(A\), and therefore does
not require the \(2\)-saturation assumption (2).

For \(x\in X\), write \(a_x\) for the vector supported on the \(A\)-blocks
containing \(x\), and write \(s_x\) for the **full** point-star on all
\(r\)-sets.  Let \(E_r\) be the rational orthogonal projector onto
\(\ker_{\mathbb Q}W\).

> **Proposition.**  If \(r\) is odd, then
> \[
>  E_ra_x
>  =a_x-\frac13W^{\mathsf T}Wa_x
>       +\frac{r-2}{3}s_x
>       +\frac{r}{3(r+2)}\mathbf1.                       \tag{5a}
> \]
> In particular \(E_ra_x\in L\otimes\mathbb Z_2\), and
> \[
>  a_x\in R^\perp=C+C^\perp .
> \]
> Equivalently, if \(P_A\) is the point-by-\(A\)-block incidence
> matrix, then
> \[
>  \operatorname{row}_{\mathbb F_2}P_A
>  \subseteq(\operatorname{res}_A R)^\perp.              \tag{5b}
> \]

**Proof.**
Put \(d=Wa_x\), and let \(e_x\) be the indicator of the
\((r-1)\)-sets containing \(x\).  Directly,
\[
 Ws_x=\mathbf1+(r+1)e_x,\qquad
 W\mathbf1=(r+2)\mathbf1.                               \tag{5c}
\]
We claim
\[
 WW^{\mathsf T}d
 =3d+2(r-1)\mathbf1+(r-2)(r+1)e_x.                      \tag{5d}
\]
Indeed,
\[
 WW^{\mathsf T}=(r+2)I+A_{J(2r+1,r-1)}.
\]
Fix an \((r-1)\)-set \(F\).  The coordinate \(d_F\) is one exactly
when the unique \(A\)-block containing \(F\) also contains \(x\).
The number of adjacent \(G\) with \(d_G=1\) is
\[
\begin{array}{c|c|c}
x\in F&d_F&\#\{G\sim F:d_G=1\}\\ \hline
1&1&r^2-3\\
0&1&r-1\\
0&0&2(r-1).
\end{array}                                              \tag{5e}
\]
For the first row, the block through \(F\) contributes \(r-1\).
There are
\[
 (r-2)(\lambda_{r-2}-1)
 =\frac{(r-2)(r+1)}2
\]
other \(A\)-blocks containing \(x\) and meeting \(F\) in \(r-2\)
points, and each contributes two adjacent facets.  Here
\(\lambda_{r-2}=(r+3)/2\).  In the second row, uniqueness of the
block through every \((r-1)\)-set leaves only the \(r-1\) other
facets of \(F\cup\{x\}\).  In the third row, each of the \(r-1\)
sets \(H\subset F\) of size \(r-2\) has a distinct block through
\(H\cup\{x\}\), and each contributes two facets.  Adding the
diagonal term \((r+2)d_F\) proves (5d).

If the right side of (5a) is denoted by \(h_x\), equations
(5c)--(5d) give \(Wh_x=0\).  Moreover \(h_x-a_x\) lies in
\(\operatorname{row}_{\mathbb Q}W\): this is clear for
\(W^{\mathsf T}Wa_x\), while \(s_x\) and \(\mathbf1\) are rational
linear combinations of the rows of \(W\).  Hence \(h_x=E_ra_x\).

All denominators in (5a) are odd when \(r\) is odd.  Thus \(h_x\) is
an ambient \(2\)-adic integral vector.  Since \(L=\ker_{\mathbb Z}W\)
is primitive,
\[
 h_x\in(\ker_{\mathbb Q_2}W)\cap\mathbb Z_2^{\binom{2r+1}r}
     =L\otimes\mathbb Z_2.
\]
Now let \(u\in R\), represented by \(\ell\in L\).  Radicality says
\(\langle\ell,L\rangle\subseteq2\mathbb Z\), hence
\(\langle\ell,h_x\rangle\in2\mathbb Z_2\).  Since
\(a_x-h_x\in\operatorname{row}_{\mathbb Q_2}W\), it is orthogonal to
\(\ell\), and therefore
\[
 \langle u,a_x\rangle
 \equiv\langle\ell,a_x\rangle
 =\langle\ell,h_x\rangle\equiv0\pmod2.
\]
This proves (5b) directly, without identifying the exact support map
in (1) with ordinary coordinate restriction. \(\square\)

The proposition proves the inclusion seen at \(r=3,5\).  It does not
prove the reverse inclusion
\((\operatorname{res}_A R)^\perp\subseteq\operatorname{row}P_A\);
that extension/surjectivity statement remains open at \(r=15\).

## 2. Full point rank at \(r=15\)

Suppose \(A\) is an \(S(14,15,31)\).  Let \(P\) be its
\(31\)-by-\(|A|\) point-by-block incidence matrix over \(\mathbb F_2\).
All derived parameters
\[
 \lambda_i=\frac{\binom{31-i}{14-i}}{15-i},
 \qquad 0\leq i\leq14,
\]
are odd.  Hence
\[
 PP^{\mathsf T}=J_{31},                                  \tag{5}
\]
because diagonal entries are \(\lambda_1\) and off-diagonal entries
are \(\lambda_2\).

The stronger fact is:

> **Theorem 1.**  \(P\) has binary row rank \(31\).

**Proof.**
Let \(T\subseteq X\) represent a word of
\(\ker P^{\mathsf T}\), so every block of \(A\) meets \(T\) evenly.
Write \(w=|T|\).

First suppose \(1\leq w\leq14\).  If \(w\) is odd, any block containing
\(T\) meets it oddly.  If \(w\) is even, choose \(x\in T\).  There are
\(\lambda_{w-1}-\lambda_w>0\) blocks containing
\(T\setminus\{x\}\) but omitting \(x\), and each meets \(T\) in
\(w-1\) points.  Both cases are impossible.

If \(w=15\) and \(T\in A\), the block \(T\) itself meets \(T\) oddly.
If \(T\notin A\), let \(n_j(T)\) count blocks of \(A\) meeting \(T\)
in \(j\) points.  The design moment equations, reduced modulo two and
solved downward, give
\[
 n_j(T)\equiv1\pmod2\qquad(0\leq j<15),
 \]
because every \(\lambda_i\) and every \(\binom{15}{i}\) is odd.
In particular an odd-intersection block exists.  Thus no nonzero kernel
word has weight at most \(15\).

Now put \(H=X\setminus T\).  Since every block has odd size \(15\), the
kernel condition says that every block meets \(H\) oddly.  If
\(|H|\leq14\), the preceding containment argument with parities reversed
produces a block meeting \(H\) evenly: for even \(|H|\), take a block
containing \(H\); for odd \(|H|\), take one containing
\(H\setminus\{x\}\) but omitting \(x\).  Hence \(w\geq17\) is impossible.

The only remaining case is \(w=16\), so \(|H|=15\).  If \(H\notin A\),
the external intersection distribution has a block meeting \(H\) in an
even number of points.  If \(H\in A\), the internal distribution has
\[
 n_2(H)=3360>0
\]
(equivalently \(n_{12}(H)=14560>0\)).  This again contradicts the
requirement that all intersections with \(H\) be odd.  Therefore
\(\ker P^{\mathsf T}=0\), proving the theorem. \(\square\)

For comparison, the same argument at \(r=3\) stops in exactly the
exceptional place: complements of Fano blocks are the seven weight-four
words in the \(3\)-dimensional simplex kernel of the Fano incidence
matrix.

Theorem 1 says that the raw truncated point stars span only a
\(31\)-dimensional functional space.  They therefore cannot by
themselves be the required \(16\,384\)-dimensional \(U_A\).  Any
Lagrangian theorem must produce at least \(16\,353\) additional
independent, genuinely higher or \(2\)-adically divided functionals.

## 3. Exact subset-star projection norms

Let \(E_r\) be the orthogonal projector, over \(\mathbb Q\), from the
permutation space on \(r\)-sets onto the top Johnson/Specht constituent
of shape \((r+1,r)\).  If \(K,L\) are \(r\)-sets and
\(s=|K\cap L|\), then
\[
 (E_r)_{K,L}
 =\frac{2(-1)^{r-s}}
 {(r+2)\binom{r+1}{r-s}}.                                \tag{6}
\]

For a \(j\)-set \(T\), \(0\leq j\leq r-1\), let \(a_T\) be the
characteristic vector of the blocks of \(A\) containing \(T\), embedded
in the full \(r\)-set coordinate space.

> **Theorem 2.**  For every \(S(r-1,r,2r+1)\),
> \[
> \boxed{\quad
> \|E_r a_T\|^2
> =\lambda_j\frac{2(r+1)}{(j+2)(r+2)}.
> \quad}                                                   \tag{7}
> \]

**Proof.**
Fix \(P\in A\) containing \(T\), and let \(m_s\) count blocks
\(Q\in A\) containing \(T\) with \(|P\cap Q|=s\).  Double counting
subsets of \(P\setminus T\) gives the triangular system
\[
 \sum_{s=j}^r\binom{s-j}{h}m_s
 =\binom{r-j}{h}\lambda_{j+h},
 \qquad 0\leq h\leq r-1-j,                                \tag{8}
\]
with \(m_r=1\).  Binomial inversion of (8), followed by substitution
of (6), gives
\[
 \sum_{s=j}^r m_s(E_r)_{P,Q(s)}
 =\frac{2(r+1)}{(j+2)(r+2)}.                              \tag{9}
\]
The left side is \((E_ra_T)_P\), independent of the chosen
\(P\in A_T\).  Summing it over the \(\lambda_j\) possible \(P\)
proves (7).  The checker performs (8)--(9) directly in exact rational
arithmetic for every \(j\) at \(r=3,5,15\). \(\square\)

For \(r=2^m-1\), whenever all \(\lambda_j\) are odd, (7) gives
\[
 v_2(\|E_ra_T\|^2)=m+1-v_2(j+2).                          \tag{10}
\]
At \(r=15\), the levels for \(j=0,\ldots,14\) are
\[
 4,5,3,5,4,5,2,5,4,5,3,5,4,5,1.                         \tag{11}
\]

For point stars \(a_x\), the same moment calculation shows that the
off-diagonal inner product is independent of the ordered pair of
distinct points.  Moreover
\[
 \sum_x a_x=r\,1_A
\]
over \(\mathbb Q\), since every block has \(r\) points.  Write the
common diagonal and off-diagonal inner products as \(d_0,d_1\).
Equation (7), first with \(j=1\) and then with \(j=0\), and
\(b=|A|=(2r+1)\lambda_1/r\), give
\[
 d_0=\lambda_1\frac{2(r+1)}{3(r+2)},\qquad
 (2r+1)d_0+(2r+1)(2r)d_1
 =r^2b\frac{r+1}{r+2}.
\]
Consequently
\[
\begin{aligned}
\langle E_ra_x,E_ra_x\rangle
 &=\lambda_1\frac{2(r+1)}{3(r+2)},\\
\langle E_ra_x,E_ra_y\rangle
 &=\lambda_1\frac{(r+1)(3r-2)}
 {6r(r+2)}\qquad(x\ne y).
\end{aligned}                                             \tag{12}
\]
In the Mersenne case their \(2\)-adic valuations are \(m+1\) and
\(m-1\).  After division by \(2^{m-1}\), the Gram matrix reduces modulo
two to \(J+I\), of rank \(2r\) with radical spanned by the all-ones
point vector.  Thus the first point-star layer is exactly the natural
\(2r\)-dimensional symplectic module underlying the Clifford model.

This makes the remaining burden precise: one would have to show that
appropriately divided higher subset-star combinations generate a
half-spin functional space of dimension \(2^{14}\), and then prove
that its orthogonal support image is totally singular.  Equations
(7)--(12) identify the filtration but do not construct that family.

## 4. Scope

Theorems 1 and 2 are exact consequences of the hypothetical
\(S(14,15,31)\) parameters.  They do not prove that such a Steiner
system exists, do not prove that \(\Lambda(A)\) is \(4\)-even, and do
not rule out a large set.  In particular:

* the point functionals are far too small to establish the proposed
  Lagrangian;
* the ordinary binary functional model still requires the unproved
  \(2\)-saturation condition (2) at \(r=15\);
* the \(16\,384\) higher/divided functionals and their total singularity
  remain open.
