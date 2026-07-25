# Two cyclic Cauchy--Pfaffian families fail at the \(p=7,11\) controls

This is an exact rejection of two particular, highly symmetric Pfaffian
ansatzes.  It is **not** a nonexistence proof for a general skew matrix,
and it does not resolve Erdős--Rosenfeld Problem #835.

Let \(p\in\{7,11\}\), let \(K=\mathbb F_{p^2}\), choose a primitive
element \(g\), and let \(H\le K^\times\) have order \(2(p-1)\).  Use the
\(2p-2\) ground points

\[
 X=gH.
\]

No two distinct points of \(X\) have product \(1\): otherwise
\(g^2\in H\), whereas \(g^2\) has order \((p^2-1)/2\), which does not
divide \(2(p-1)\).  Hence the Cauchy kernel

\[
 C_{xy}=\frac{x-y}{1-xy}\qquad(x\ne y)
\tag{1}
\]

is defined throughout.  It is skew-symmetric.  Under the fractional
linear change \(u=(1+x)/(1-x)\), it becomes Schur's kernel
\((u_x-u_y)/(u_x+u_y)\), so Schur's identity gives

\[
 \operatorname{Pf}(C[S])=
 \prod_{\{x,y\}\subset S,\ x<y}\frac{x-y}{1-xy}.
\tag{2}
\]

We checked the following two ways of turning (1) into an
\(\mathbb F_p\)-valued candidate colouring of the \((p-1)\)-subsets:

\[
\begin{aligned}
  c^{\rm entry}_\lambda(S)
   &=\operatorname{Pf}\left(\operatorname{Tr}_{K/\mathbb F_p}
       (\lambda C_{xy})\right)_{x,y\in S},\\
  c^{\rm Pf}_\lambda(S)
   &=\operatorname{Tr}_{K/\mathbb F_p}
       \left(\lambda\operatorname{Pf}(C[S])\right).
\end{aligned}
\tag{3}
\]

Here \(\lambda\ne0\).  Multiplication of \(\lambda\) by
\(\mathbb F_p^\times\) only scales every colour in a fixed candidate by a
nonzero constant (by that constant to the \((p-1)/2\)-th power in the
first line), so it preserves the rainbow condition.  Thus it is enough to
check the \(p+1\) projective directions

\[
 (a,1)\ (a\in\mathbb F_p),\quad (1,0),
\tag{4}
\]

in a basis \(K=\mathbb F_p(\sqrt d)\).

## Exact result

For every direction in (4), and for each of the two formulae (3), the
checker finds an explicit \((p-2)\)-set \(T\) whose \(p\) extensions do
not receive \(p\) distinct values.  Thus neither family produces the
required colouring at either adversarial control prime.

For example, in the \(p=7\) model \(K=\mathbb F_7(\sqrt3)\), the point
order is

\[
 ((1,1),(6,2),(5,5),(2,3),(4,4),(3,1),
   (6,6),(1,5),(2,2),(5,4),(3,3),(4,6)).
\]

For the first formula and \(\lambda=(0,1)\), the star

\[
 T=(0,1,2,3,4)
\]

has extension colours

\[
 (6,3,5,0,4,0,0),
\]

so it has only five distinct values.  For the second formula and the
same \(\lambda,T\), the colours are

\[
 (6,1,1,6,0,1,3),
\]

with only four distinct values.  The verifier checks every projective
trace direction, not merely these displayed witnesses.  It also compares
(2), on all seven extensions of the displayed star (and all eleven in the
\(p=11\) control), with an independent alternating Gaussian-elimination
Pfaffian computation over \(K\).

Run:

```bash
python3 evidence/pfaffian_cauchy_negative_controls.py
```

## Scope and next surviving family

The exact exclusion covers the single cyclic point set \(gH\), the
Cauchy/Schur kernel (1), and **all** linear trace descents in (3) for
\(p=7,11\).  It does not cover a different point configuration, a
different rational skew kernel, nonlinear postprocessing, or an arbitrary
\(\mathbb F_p\)-valued skew matrix \(M\) in

\[
 c(S)=\operatorname{Pf}(M[S]).
\]

That last unrestricted principal-Pfaffian family is the next surviving
algebraic family.  Unlike the maximal-minor ansatz, fixing \(p-3\) points
leaves a general alternating \((p+1)\)-by-\((p+1)\) Schur complement; its
edge labels can locally be a one-factorization of \(K_{p+1}\).  Thus the
rank-two argument that excludes maximal minors does not transfer to
Pfaffians, and these controls do not supply a general no-go lemma.
