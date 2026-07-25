# No projectivized sum of arbitrary \(\mathbb F_{16}^2\) labels

This note rules out a broad nonlinear construction for a \(17\)-colouring
of \(J(32,16)\).  In particular, it covers labels obtained from graphs
\(x\mapsto (x,f(x))\), including APN or other nonlinear functions, as
well as two-layer variants with completely arbitrary labels.

## The general theorem

Let \(q>2\) be a power of two, let \(P\) be a set of \(2q\) points, and
assign an arbitrary vector
\[
 v_p\in\mathbb F_q^2
 \qquad(p\in P).
\]
There is no proper \((q+1)\)-colouring of \(J(2q,q)\) of the form
\[
 c(S)=\left[\sum_{p\in S}v_p\right]\in
 \mathbb P^1(\mathbb F_q),                         \tag{1}
\]
where every vector sum in (1) is required to be nonzero.

For \(q=16\), this excludes every projectivized two-moment rule with
seventeen colours, regardless of how nonlinear the point embedding is.

## Proof

Suppose (1) is a proper colouring.  Fix a nonzero
\(\mathbb F_q\)-linear functional
\[
 \ell:\mathbb F_q^2\longrightarrow\mathbb F_q
\]
and put \(a_p=\ell(v_p)\).

Let \(T\subset P\) have size \(q-1\).  Its \(q+1\) extensions
\[
 T\cup\{x\},\qquad x\in P\setminus T,
\]
form a clique in \(J(2q,q)\).  Properness and the fact that there are
exactly \(q+1\) points in \(\mathbb P^1(\mathbb F_q)\) imply that their
colours run through the whole projective line exactly once.

The kernel of \(\ell\) is one of those projective points.  Consequently
there is exactly one \(x\in P\setminus T\) for which
\[
 0=\ell\left(\sum_{p\in T}v_p+v_x\right)
  =\sum_{p\in T}a_p+a_x .
\]
Because the characteristic is two, this gives the scalar condition
\[
 \boxed{\text{for every \((q-1)\)-set \(T\), exactly one
 \(x\notin T\) satisfies }
 a_x=\sum_{p\in T}a_p.}                            \tag{2}
\]

Now fix a \((q-2)\)-set \(R\), and write
\[
 U=P\setminus R,\qquad |U|=q+2,\qquad
 r=\sum_{p\in R}a_p.
\]
Apply (2) to \(T=R\cup\{i\}\) for each \(i\in U\).  It says
\[
 \text{for every \(i\in U\), exactly one \(j\in U\setminus\{i\}\)
 has }a_j=r+a_i.                                  \tag{3}
\]

Assume first that \(r\ne0\).  Let \(m(s)\) denote the multiplicity of
\(s\in\mathbb F_q\) among the values \(\{a_i:i\in U\}\), and let
\(D=\{s:m(s)>0\}\).  Since \(r+a_i\ne a_i\), equation (3) says
\[
 m(r+s)=1\qquad(s\in D).                           \tag{4}
\]
In particular \(r+D\subseteq D\).  Translation is a bijection, so
\(r+D=D\).  Every element of \(D\) is therefore \(r+s\) for some
\(s\in D\), and (4) shows that every multiplicity in \(D\) is one.
This would make the \(q+2\) values indexed by \(U\) distinct elements of
the \(q\)-element field, which is impossible.  Thus
\[
 \sum_{p\in R}a_p=0                               \tag{5}
\]
for every \((q-2)\)-set \(R\).

Because \(q\ge4\), two \((q-2)\)-sets can be chosen with a common
\((q-3)\)-subset and arbitrary distinct remaining elements \(i,j\).
Subtracting their two instances of (5) gives \(a_i=a_j\).  Hence all
\(2q\) scalars \(a_p\) have one common value \(a\).

Return to any \(R\) and its complement \(U\).  Since \(r=0\), (3) now
says that every \(i\in U\) has exactly one other index in \(U\) carrying
the value \(a_i\).  But all \(q+2\) indices carry the same value, so each
has \(q+1>1\) such indices.  This final contradiction proves the theorem.
\(\square\)

## Consequences and scope

Take \(q=16\).  The theorem permits the vectors \(v_p\) to be chosen
arbitrarily.  It therefore strictly strengthens the affine-line
obstruction in `constructive_no_go.md`: no nonlinear replacement of the
two affine lines can repair the construction.  For example, it excludes
all rules obtained by embedding one or two copies of \(\mathbb F_{16}\)
using graphs such as
\[
 x\longmapsto (x,x^3),\qquad x\longmapsto(x,x^9),
\]
or any APN-equivalent variants, then summing the sixteen selected graph
points and taking the projective class.

The argument is specifically about a fixed pointwise additive statistic
followed by projectivization.  It does not exclude higher-order subset
statistics, a rule that depends on the whole half-set polynomial, or an
arbitrary postprocessing in which the zero vector receives an additional
nonprojective meaning.

Run

```bash
python3 evidence/verify_nonlinear_projective_sum.py
```

for an exhaustive check of the finite multiplicity lemma used in the
proof at \(q=16\), together with the exceptional \(q=2\) sanity check.
