# Teichmüller/Schur closure is not an obstruction at \(k=16\)

This note isolates one tempting algebraic attack on Erdős–Rosenfeld Problem
#835 and shows exactly where it stops.  Throughout, let

\[
r=15,\qquad p=r+2=17,\qquad
V=\binom{[31]}{15}.
\]

Two vertices are adjacent in the Odd graph when they are disjoint.  Suppose,
only for the first theorem, that there is a coloring
\(c:V\to\mathbf F_{17}\) for which every closed neighborhood contains every
color exactly once.

## Exact Teichmüller lift

Let \(\zeta\) be a primitive seventeenth root of unity and put

\[
f_m(x)=\zeta^{m c(x)}\quad (m\in\mathbf Z/17\mathbf Z).
\]

For \(m\ne0\), the colors on the 16 open neighbors of \(x\) are all field
elements except \(c(x)\).  Hence

\[
(Af_m)(x)
=\sum_{t\in\mathbf F_{17}\setminus\{c(x)\}}\zeta^{mt}
=-f_m(x).
\]

All color classes have the same size, because every perfect code has
\(|V|/17\) vertices.  Therefore the \(f_m\) are orthogonal:

\[
\langle f_m,f_n\rangle=|V|\delta_{mn}.
\]

Finally,

\[
f_m f_n=f_{m+n}
\]

for pointwise multiplication.  Thus

\[
U=\operatorname{span}_{\mathbf C}\{f_1,\ldots,f_{16}\}
\subseteq E_{-1}
\]

has dimension 16, and \(\mathbf C1\oplus U\) is a pointwise copy of the
function algebra on the cyclic group \(C_{17}\).  This is an exact
characteristic-zero statement; no modular lifting ambiguity remains.

## An exact abstract model

The preceding structure does not itself contradict the Bose--Mesner algebra.
For relation \(R_j\), defined by \(|X\cap Y|=j\), set

\[
v_j=\binom{15}{j}\binom{16}{j+1},\qquad
\eta_j=(-1)^{j+1}\binom{15}{j}.
\]

Here \(v_j\) is the valency and \(\eta_j\) is the eigenvalue of \(R_j\) on
the top Odd-graph constituent containing the \(-1\) eigenspace.  Define

\[
b_j=\frac{v_j-\eta_j}{17},\qquad
a_j=\frac{v_j+16\eta_j}{17}=b_j+\eta_j.
\]

These are nonnegative integers for every \(0\le j\le15\).  Integrality
already follows from

\[
\binom{16}{j+1}\equiv(-1)^{j+1}\pmod {17},
\]

which gives \(v_j\equiv\eta_j\pmod {17}\).  Nonnegativity at \(p=17\) is
checked exactly, with no floating arithmetic, by the accompanying verifier.

Now take \(W=\mathbf C^{\mathbf F_{17}}\), with its ordinary pointwise
product, and define

\[
T_j=\eta_j I+b_jJ.
\]

In the delta-function basis, \(T_j\) has entry \(a_j\) on the diagonal and
\(b_j\) off the diagonal.  In the Fourier basis
\(\chi_m(t)=\zeta^{mt}\),

\[
T_j\chi_0=v_j\chi_0,\qquad
T_j\chi_m=\eta_j\chi_m\quad(m\ne0).
\]

Consequently the \(T_j\) form the direct sum of the trivial Bose--Mesner
character and sixteen copies of the top character.  They obey every ordinary
Bose--Mesner multiplication identity.  In particular,

\[
T_0=J-I,\qquad T_{15}=I,
\]

while the Fourier vectors obey the full pointwise group law
\(\chi_m\chi_n=\chi_{m+n}\).

The verifier checks all \(16^2\) products

\[
T_iT_j=\sum_{k=0}^{15}p_{ij}^kT_k
\]

directly.  It computes \(p_{ij}^k\) by choosing a third 15-subset from the
four cells determined by a fixed pair whose intersection has size \(k\).

## Scope of the no-go

This is **not** a coloring of the 300,540,195 vertices of the Odd graph.
It is a coherent 17-point quotient model.  It proves that an impossibility
argument cannot use only:

1. the Teichmüller characters and their pointwise multiplication table;
2. membership of their nonconstant span in the \(-1\) eigenspace;
3. the ordinary Bose--Mesner multiplication rules; and
4. the same-color/different-color quotient counts \(a_j,b_j\).

Any successful obstruction must retain higher geometric information that the
17-point quotient forgets: triple intersections, four-point extension
compatibility, or a still higher tensor.  Thus the Teichmüller lift is an
exact reformulation of the desired coloring structure, but Schur closure at
the quotient level is not by itself a contradiction.

