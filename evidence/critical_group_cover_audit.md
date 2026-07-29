# Critical-group audit for \(O_k\to K_{k+1}\)

A partition of the Odd graph \(O_k\) into \(k+1\) perfect codes is not
merely an equitable colouring.  Sending every vertex to its colour is a
genuine graph covering

\[
 \pi:O_k\longrightarrow K_{k+1}.
\]

This note checks the induced constraint on graph Jacobians (critical
groups), including the transfer identity at the prime \(p=k+1\).  The
result is exact:

\[
\boxed{\text{the critical group gives no obstruction at }k=16.}
\]

It also passes the known-false \(k=4\) control, so it is strictly weaker
than the full integral short-vector test in
`full_eigenlattice_audit.md`.

## 1. Pullback and transfer

Put \(p=k+1\), and let

\[
 n=\frac{\binom{2k-1}{k-1}}{k+1}
\]

be the number of sheets.  Pullback and pushforward of degree-zero
divisors descend to

\[
 \pi^*:\operatorname{Jac}(K_p)\longrightarrow
       \operatorname{Jac}(O_k),
\qquad
 \pi_*:\operatorname{Jac}(O_k)\longrightarrow
       \operatorname{Jac}(K_p),
\]

and satisfy

\[
 \pi_*\pi^*=n\,\mathrm{id}.
\]

Since

\[
 \operatorname{Jac}(K_p)\cong(\mathbb Z/p)^{p-2},
\]

if \(p\nmid n\), multiplication by \(n^{-1}\pi_*\) is a retraction on
the \(p\)-primary part.  Thus a cover would force a split injection

\[
 (\mathbb Z/p)^{p-2}
 \ \mid\
 \operatorname{Jac}(O_k)_{(p)}.
\]

For the two parameters of interest,

\[
 (k,p,n)=(4,5,7)
\]

and

\[
 (k,p,n)=(16,17,17\,678\,835),
\qquad n\equiv8\pmod {17}.
\]

The coprimality hypothesis therefore holds in both cases.

## 2. The entire \(p\)-primary group of the Odd graph

The adjacency eigenvalues of \(O_k\) are

\[
 \theta_i=(-1)^i(k-i)
\]

with multiplicity

\[
 m_i=\binom{2k-1}{i}-\binom{2k-1}{i-1},
\qquad 0\leq i\leq k-1.
\]

Hence the nonzero Laplacian eigenvalues are

\[
 \lambda_i=
 \begin{cases}
 i,&i>0\text{ even},\\
 2k-i,&i\text{ odd},
 \end{cases}
\]

with the same multiplicities.  When \(p=k+1\) and \(k\) is even, the
only nonzero eigenvalue divisible by \(p\) is

\[
 \lambda_{k-1}=p.
\]

Also \(v_p(|V(O_k)|)=1\), because the sheet degree \(n\) is a
\(p\)-adic unit.  The Matrix-Tree Theorem now gives

\[
 v_p\!\left(\lvert\operatorname{Jac}(O_k)\rvert\right)
 =m_{k-1}-1.
\]

This order calculation alone does not yet show that the group is
elementary abelian.  The integral \(-1\)-eigenlattice supplies the
missing rank bound.  It is saturated and has rank \(m_{k-1}\); on it
the Laplacian acts as multiplication by \(p\).  Its reduction therefore
gives \(m_{k-1}\) independent vectors in the kernel of the Laplacian
modulo \(p\).  Since

\[
 \dim_{\mathbb F_p}\ker(\Delta\bmod p)
 =1+\operatorname{rank}_p\operatorname{Jac}(O_k),
\]

the critical-group \(p\)-rank is at least \(m_{k-1}-1\).  Comparing this
with the total \(p\)-valuation above forces equality and forces every
nontrivial \(p\)-primary invariant factor to have exponent one:

\[
 \boxed{\displaystyle
 \operatorname{Jac}(O_k)_{(p)}
 \cong(\mathbb Z/p)^{m_{k-1}-1}.}
\]

This is much more than the covering requires.

At \(k=4\), an independent Smith-normal-form calculation gives

\[
 \operatorname{Jac}(O_4)
 \cong
 \mathbb Z/2
 \oplus(\mathbb Z/10)^8
 \oplus(\mathbb Z/70)^5,
\]

so

\[
 \operatorname{Jac}(O_4)_{(5)}
 \cong(\mathbb Z/5)^{13},
\]

whereas the base needs only \((\mathbb Z/5)^3\).

At \(k=16\),

\[
 m_{15}=35\,357\,670
\]

and therefore

\[
 \boxed{\displaystyle
 \operatorname{Jac}(O_{16})_{(17)}
 \cong(\mathbb Z/17)^{35\,357\,669}.}
\]

The base contribution \(\operatorname{Jac}(K_{17})\cong
(\mathbb Z/17)^{15}\) fits with enormous room to spare.

## 3. The monodromy pairing also fits

The critical group carries its nondegenerate monodromy pairing.  For a
degree-\(n\) graph cover,

\[
 \langle\pi^*a,\pi^*b\rangle_{O_k}
 =n\,\langle a,b\rangle_{K_p}.
\]

Because \(n\) is a \(p\)-adic unit, the desired image is a nondegenerate
\((p-2)\)-dimensional quadratic space over \(\mathbb F_p\).  The ambient
\(p\)-primary group above is elementary abelian, so its pairing is a
nondegenerate symmetric form of dimension \(m_{k-1}-1\).

There is no Witt obstruction.  Over a finite field of odd order, every
nondegenerate quadratic space is a sum of hyperbolic planes and an
anisotropic part of dimension at most two.  After embedding the
hyperbolic part of the \(15\)-dimensional target, the ambient orthogonal
remainder still has dimension far above three; such a space represents
every nonzero field element and therefore also contains the target's
last anisotropic line.  The same argument passes the \(3\)-dimensional
\(k=4\) control target.

Thus group structure, split transfer, and pairing type are all
compatible.

## 4. Comparison with the eigenlattice audit

The critical-group \(p\)-part is controlled by exactly the same
top-eigenspace which produced the primitive scaled \(A_{k}\) lattice:
the latter reduces modulo \(p\) into the Laplacian kernel.  The
Matrix-Tree valuation leaves no higher \(p\)-power structure, so the
Jacobian condition collapses to a very loose dimension requirement.

It cannot see the decisive \(k=4\) fact that no four norm-\(14\)
vectors have mutual product \(7\).  Consequently the critical group is
not stronger than the full \(-1\)-eigenlattice discriminant/geometry
route for this problem.

## Reproduction

```bash
python3 evidence/verify_critical_group_cover.py
```

The script computes the complete \(34\times34\) reduced-Laplacian Smith
form for \(O_4\) and independently checks the symbolic \(p\)-valuation
and rank formulas for \(O_{16}\).
