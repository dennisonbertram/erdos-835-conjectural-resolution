# The Norton \(1/3\)-gap is already a nonexistence theorem

This note closes one tempting continuation of the Norton-compression
attack.  It concerns only a **single hypothetical**
\[
S(14,15,31),
\]
which is a necessary consequence of a solution of Erdős--Rosenfeld
problem 835 at \(k=16\).  It does not construct a large set and it does
not resolve the full problem.

Let \(D\) be the block set of a hypothetical
\(S(r-1,r,2r+1)\), put \(q=r+2\), and let \(P\) be the orthogonal
projector onto the top Johnson kernel
\[
\ker W_{r-1,r}(2r+1).
\]
If \(F_D\) is the diagonal projector onto \(D\), write
\[
K=(F_DPF_D)|_{\mathbb R^D}.
\]
The matrix \(K\) is positive semidefinite and has the same nonzero
eigenvalues as \(PF_DP\).  Its entries are
\[
K_{A,B}=p_{|A\cap B|},\qquad
p_t=(-1)^{r-t}\frac{2}{q\binom{r+1}{t+1}}.
\tag{1}
\]

The Fano and Witt controls have nonzero spectra
\[
\{(1/3)^6,(4/5)^1\},\qquad
\{(1/3)^{54},(6/7)^1\}.
\]
This suggests trying to prove the universal gap
\[
\operatorname{Spec}(K)\subseteq \{0\}\cup[1/3,1].
\tag{2}
\]
At \(r=15\), however, (2) is not an auxiliary positivity fact waiting
to be combined with another obstruction.  It is already a complete
nonexistence theorem.

## 1. A negative diagonal certificate

The fixed-block intersection equations of a Steiner system give
\[
\operatorname{tr}K=\frac{2n}{q},\qquad
\operatorname{tr}K^2
=\frac{2n(3q-1)}{q^2(q+1)},
\tag{3}
\]
where
\[
n=|D|=\frac1q\binom{2r+1}{r}.
\]
Every row of \(K\) has the same intersection distribution.  Hence every
diagonal entry of \(K^2\) is \(\operatorname{tr}(K^2)/n\).  Since
\(K_{A,A}=2/q\), (3) gives
\[
\begin{aligned}
\left(K^2-\frac13K\right)_{A,A}
&=\frac{2(3q-1)}{q^2(q+1)}-\frac{2}{3q}\\
&=\frac{2(-q^2+8q-3)}{3q^2(q+1)}.
\end{aligned}
\tag{4}
\]
For \(q=17\), this is
\[
\boxed{-\frac{52}{2601}<0.}
\tag{5}
\]

But (2) is equivalent to
\[
K^2-\frac13K\succeq0,
\]
whose diagonal entries would all be nonnegative.  Thus proving (2) from
the full Steiner axioms would immediately contradict (4), and therefore
prove that \(S(14,15,31)\) does not exist.

In particular, there is no unconditional local-link or incidence-Gram
factorization of \(K^2-\frac13K\) into manifest squares that is compatible
with the universal fixed-block counts: its putative squared norm at every
coordinate is already the negative rational number (5).  A
sum-of-squares *certificate of nonexistence* is still logically possible,
but it would have to use enough of the global Steiner equations to derive
their inconsistency; it cannot be justified by the Fano/Witt controls
alone.

## 2. What a hypothetical compression must look like

The same conclusion follows spectrally from (3):
\[
\frac{\operatorname{tr}K^2}{\operatorname{tr}K}
=\frac{3q-1}{q(q+1)}.
\tag{6}
\]
The left side is the weighted average
\[
\frac{\sum_\lambda\lambda^2}{\sum_\lambda\lambda}
\]
of the positive eigenvalues of \(K\).  At \(q=17\), (6) equals
\[
\boxed{\frac{25}{153}<\frac13.}
\tag{7}
\]
Consequently, if an \(S(14,15,31)\) exists, its compression necessarily
has a nonzero eigenvalue at most \(25/153\).  Since the forced simplex
eigenvalue \(16/17\) is also present, the smallest positive eigenvalue is
in fact strictly below \(25/153\).

There must be not merely one but millions of sub-\(1/3\) eigenvalues.
Let \(m_<\) count the eigenvalues in \((0,1/3)\), with multiplicity, and
put
\[
\Delta=\frac13\operatorname{tr}K-\operatorname{tr}K^2.
\]
For \(0<\lambda<1/3\),
\[
\lambda(1/3-\lambda)\le\frac1{36},
\]
whereas an eigenvalue at least \(1/3\) contributes a nonpositive amount
to \(\Delta\).  Therefore
\[
\Delta
=\sum_\lambda\lambda(1/3-\lambda)
\le\frac{m_<}{36},
\]
and hence
\[
m_<\ge\lceil36\Delta\rceil.
\tag{8}
\]
At the target,
\[
n=17\,678\,835,\quad
\Delta=\frac{102\,144\,380}{289},
\]
so (8) becomes
\[
\boxed{m_<\ge 12\,723\,868.}
\tag{9}
\]

Thus the Fano/Witt three-eigenvalue pattern cannot persist even
approximately at \(q=17\): any hypothetical target constituent is forced
by its first two exact moments to have a very large low-spectrum sector.

## 3. Verdict

The \(1/3\)-gap route remains a logically valid route to proving
nonexistence of \(S(14,15,31)\), but no independent spectral-gap theorem
has been established.  Equations (4)--(9) show why: the desired gap is
already equivalent to supplying genuinely new global information strong
enough to contradict the Steiner axioms.  The small Fano and Witt spectra,
the exact Johnson kernel, and the universal one- and two-block counts do
not by themselves provide that information.

Reproduce the arithmetic with:

```bash
python3 evidence/verify_norton_one_third_gap_no_go.py
```
