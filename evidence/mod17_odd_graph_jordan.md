# The required mod-17 Jordan block already exists in \(O_{16}\)

Let \(M\) be the adjacency matrix of the odd graph
\[
 O_{16}=KG(31,15)
\]
and work over \(\mathbb F_{17}\).  If a locally bijective colouring
\(O_{16}\to K_{17}\) existed and \(H\) were its vertex-by-colour
indicator matrix, then
\[
 (M+I)H=\mathbf1\mathbf1^{\mathsf T}. \tag{1}
\]
The columns of \(H\) span a nondegenerate 17-dimensional space: their
Gram matrix is \(nI_{17}\), where
\[
 n=17\,678\,835\equiv8\pmod {17}.
\]
On this space \(M+I\) has one nilpotent Jordan block of size two and
fifteen zero blocks.  This note shows that the known integral adjacency
module already contains exactly this local structure.  Hence the
mod-17 Jordan condition gives no obstruction.

## 1. An explicit generalized eigenvector

The distinct eigenvalues of \(M\) are
\[
 \lambda_i=(-1)^i(16-i),\qquad0\le i\le15.
\]
Put
\[
 q(t)=\prod_{i=1}^{14}(t-\lambda_i).
\]
The polynomial
\[
 g(t)=(t+1)q(t)=\prod_{i=1}^{15}(t-\lambda_i)
\]
vanishes on every eigenspace except the constant eigenspace
\(\lambda_0=16\).  Since \(O_{16}\) has
\[
 N=\binom{31}{15}=300\,540\,195
\]
vertices, spectral projection onto the constants gives the exact integer
matrix identity
\[
 (M+I)q(M)
 =\frac{g(16)}N J
 =203\,212\,800\,J. \tag{2}
\]
The scalar on the right is \(2\bmod17\).  Thus, for every vertex \(v\),
\[
 x_v=9q(M)e_v \tag{3}
\]
satisfies
\[
 (M+I)x_v=\mathbf1 \quad\text{over }\mathbb F_{17}. \tag{4}
\]
Since \((M+I)\mathbf1=17\mathbf1=0\), the plane
\(\langle\mathbf1,x_v\rangle\) carries the required size-two Jordan
block.

It also has exactly the Gram data of one colour column and the sum of all
colour columns:
\[
\begin{aligned}
 \langle\mathbf1,\mathbf1\rangle&=N=0,\\
 \langle\mathbf1,x_v\rangle&=8,\\
 \langle x_v,x_v\rangle&=8
 \qquad\text{in }\mathbb F_{17}. \tag{5}
\end{aligned}
\]
For the middle identity, use \(q(16)\equiv16\), so
\(9q(16)\equiv8\).  For the last, vertex transitivity and the spectral
multiplicities give
\[
 (q(M)^2)_{vv}
 =
 \frac{q(16)^2+
  \left(\binom{31}{15}-\binom{31}{14}\right)q(-1)^2}{N}
 \equiv15\pmod {17};
\]
multiplication by \(9^2\equiv13\) gives \(8\).
In particular the Jordan plane in (5) is nondegenerate.

## 2. There is exactly one size-two block in the zero-primary part

Over \(\mathbb Q_{17}\), the only eigenvalues of \(M\) congruent to
\(-1\bmod17\) are
\[
 16\quad\text{and}\quad-1,
\]
with multiplicities \(1\) and
\[
 m=\binom{31}{15}-\binom{31}{14}=35\,357\,670,
\]
respectively.  On their direct sum, \(M+I\) is \(17\) times the projection
onto the one-dimensional 16-eigenspace.  For any \(M\)-stable
\(\mathbb Z_{17}\)-lattice, reduction modulo 17 therefore has nilpotent
rank at most one on this primary component: its image is a quotient of
that one-dimensional rational summand.  Equation (4) shows that the rank
is at least one.  Hence it is exactly one.

The zero-primary component of \(M+I\) consequently consists of one
size-two Jordan block and \(m-1\) size-one zero blocks.  Because \(M+I\)
is self-adjoint, the radical of its kernel on this component is the
one-dimensional image of the size-two block.  The nondegenerate
orthogonal complement of the plane in (5) therefore contains a
nondegenerate \((m-1)\)-dimensional zero eigenspace.  In particular, it
contains a nondegenerate 15-dimensional subspace.

Taking that 15-space together with
\(\langle\mathbf1,x_v\rangle\) produces a nondegenerate 17-dimensional
invariant subspace on which \(M+I\) has precisely one size-two Jordan
block and fifteen zero blocks—the full linear-algebra structure demanded
by (1).

## 3. Scope

This does not construct the \(0\)-\(1\), disjoint-support columns of a
colouring matrix \(H\).  It proves that adjacency eigenvalues, the
mod-17 Jordan form, and the invariant dot product all permit the required
17-dimensional module.  Any successful characteristic-17 obstruction
must use the coordinatewise partition identities in \(H\), not the
Jordan/Smith structure of \(M+I\) alone.

Run:

```bash
python3 evidence/verify_mod17_odd_graph_jordan.py
```

