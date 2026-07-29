# Canonical finite-colour augmentation and its sign identity

This note is conditional on a radius-five local structure.  It concerns one
finite colour \(x\in V\); the root colour \(\infty\) is the separate
infinity-layer calculation.  No global colouring and no resolution of
Erdős--Rosenfeld Problem #835 is claimed.

The later proof in
[`../global_h_parity/README.md`](../global_h_parity/README.md) evaluates the
cofactor product below and proves that the total over all colours is
identically the previous flag formula \(F(L,M)\).  This note is retained for
the canonical finite-layer construction itself.

Let \(|V|=k\) be even, \(|A|=k-1\), and put

\[
 a_i=a_i(x):=L_i^{-1}(x).
\tag{1}
\]

The forced radius-five trace gives a matching \(D_x^{ij}\) of
\(V\setminus\{a_i,a_j\}\) for every \(ij\in E(K_A)\).  The finite
\(x\)-class of \(M_i\) is a matching on
\(V\setminus\{x,a_i\}\).

## 1. The no-hole augmentation

Adjoin one index \(*\), writing \(B=A\sqcup\{*\}\).  Define perfect
matchings of \(V\) by

\[
\begin{aligned}
 \widehat D_x^{ij}&=D_x^{ij}\sqcup\{\{a_i,a_j\}\},
 &&i,j\in A,\ i\ne j,\\
 \widehat D_x^{i*}&=M_i^{-1}(x)\sqcup\{\{x,a_i\}\}.
\end{aligned}
\tag{2}
\]

These matchings satisfy the no-hole dual condition: for every \(uv\in
E(K_V)\), the set of \(rs\in E(K_B)\) with
\(uv\in\widehat D_x^{rs}\) is a perfect matching of \(B\).

For \(x\notin\{u,v\}\), the original \(x\)-class of \(N_{uv}\) is a
matching on \(A\) with three holes

\[
 i_M:\ M_{i_M}(uv)=x,\qquad
 i_u:\ a_{i_u}=u,\qquad i_v:\ a_{i_v}=v.
\]

They are distinct.  Formula (2) adds exactly the two edges

\[
 \{i_u,i_v\},\qquad\{i_M,*\},
\tag{3}
\]

and hence fills all holes.  If \(x=u\), the sole old hole is \(i_v\) and
the added edge is \(\{i_v,*\}\); the \(x=v\) case is symmetric.  This
proves the stated dual condition in every case.

## 2. Universal no-hole sign

For any no-hole tensor on two even \(k\)-sets \(B,V\), define the link
permutations

\[
 \Theta_{r,u}:B\setminus\{r\}\longrightarrow V\setminus\{u\},
 \qquad \Theta_{r,u}(s)=\widehat D^{rs}(u).
\tag{4}
\]

Then

\[
 \boxed{\prod_{r\in B,\ u\in V}\operatorname{sgn}\Theta_{r,u}=+1.}
\tag{5}
\]

Here is an exact proof.  For a one-factorization \(\mathcal F\) of \(K_k\),
let \(P(\mathcal F)\) be the product of its \(k\) vertex-row signs, and let
\(\operatorname{pf}(Q)\) be the Pfaffian sign of a perfect matching \(Q\).
The directed-edge regrouping identity is
\[
 P(\mathcal F)=
 (-1)^{\binom{k/2}{2}}\prod_{Q\in\mathcal F}\operatorname{pf}(Q).
\]
For fixed \(r\), the matchings
\((\widehat D^{rs})_{s\ne r}\) form a one-factorization of \(K_V\), and
their vertex-row product is exactly
\(\prod_u\operatorname{sgn}\Theta_{r,u}\).  Multiply the displayed identity
over \(r\).  The fixed constant occurs the even number \(k\) of times, and
every matching \(\widehat D^{rs}\) occurs twice, once at each endpoint.
All signs therefore square to \(+1\), proving (5).  A full order audit of
the directed-edge identity is given independently in
[`../finite_total_identity/README.md`](../finite_total_identity/README.md).

Applying (5) to (2) gives an independent finite-colour sign equation.

## 3. Exact cofactor formula

The formula is easiest to state using one elementary cofactor sign.
Let \(R\subset X\) and \(C\subset Y\) be induced ordered subsets of equal
size, and let \(\alpha:X\setminus R\to Y\setminus C\) be a bijection.
Put

\[
 \operatorname{cof}_{X,Y}(R,C;\alpha)=
 \operatorname{sgn}[R,X\setminus R\to X]\,
 \operatorname{sgn}[C,Y\setminus C\to Y]\,
 \operatorname{sgn}(\alpha).
\tag{6}
\]

Here the first two signs are those of the displayed concatenated lists.
For every bijection \(f:R\to C\), its extension
\(f\sqcup\alpha:X\to Y\) obeys

\[
 \operatorname{sgn}(f\sqcup\alpha)=
 \operatorname{cof}_{X,Y}(R,C;\alpha)\operatorname{sgn}(f).
\tag{7}
\]

Fix \(i,u,x\), take \(X=B\setminus\{i\}\), \(Y=V\setminus\{u\}\),
and let \(R,C\) be the row and column sets of the original partial
permutation \(\Phi_{i,u,x}\).  Its complement bijection \(\alpha\) is
forced by (2):

* if \(u=a_i\), there is no old fibre and the full known map is
  \(j\mapsto a_j\) for \(j\ne i\), together with \(*\mapsto x\);
* if \(x=u\), \(*\mapsto a_i\);
* in the generic case, if \(j_0\) has \(a_{j_0}=u\), then
  \(j_0\mapsto a_i\) and \(*\mapsto m_{i,x}(u)\), where
  \(m_{i,x}\) is the completed \(x\)-matching of \(M_i\).

Call the corresponding value in (6) \(\kappa_{i,u,x}\), and call the
first, fully known sign in the \(u=a_i\) case \(\gamma_{i,x}\).

There is one further link in the augmented tensor: the one based at the
dummy index \(*\).  Let \(m_i^x\) denote the mate involution of the
completed matching \(M_i^{-1}(x)\sqcup\{\{x,a_i\}\}\), and put

\[
 P_x=\prod_{u\in V}\operatorname{sgn}
 \bigl(i\longmapsto m_i^x(u):A\longrightarrow V\setminus\{u\}\bigr).
\tag{8}
\]

The map in (8) is a permutation because the completed \(x\)-classes of
the \(M_i\) form a one-factorization.  The no-hole product (5) contains
both its dummy-index link and all the full completions of the old partial
links.  Since signs are their own inverses, (5) and (7) give the exact
finite-colour evaluation

\[
 \boxed{
 H_x:=\prod_{i\in A}\prod_{u\ne a_i}
       \operatorname{sgn}\Phi_{i,u,x}
 =P_x\prod_i\gamma_{i,x}\prod_{i,u\ne a_i}\kappa_{i,u,x}.}
\tag{9}
\]

The right side depends only on the radius-three \(L/M\) data and the fixed
orders.  It is not an assumption about, or a search over, the unknown
finite \(N\)-layer.

## 4. What this does and does not add

Multiplying (9) over the finite colours and multiplying by the separate
infinity formula gives a second evaluation of the total partial-fibre
sign.  For every genuine radius-five extension it must agree with the
already known flag-Latin identity

\[
 H=(-1)^{k(k-1)/2}\operatorname{AT}(T)\prod_i\delta(S_i).
\tag{10}
\]

This note itself stops at that conditional comparison.  The companion
global proof cited above carries out the determinant/Pfaffian simplification
for every radius-three chart and shows that the total is identically (10),
so the multiplied equation is not an additional obstruction.

Equation (9) fixes every finite-colour layer separately.  Whether those
layer equations yield further compatibility constraints, including between
different choices of root, remains open here; no root-coupling theorem is
claimed.

Run the stdlib verifier:

```bash
python3 -B collaboration/full_layer_augmentation/verify_full_layer_augmentation.py
```
