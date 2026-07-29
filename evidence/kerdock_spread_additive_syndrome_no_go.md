# No additive Kerdock/spread syndrome construction

This note closes the most direct Kerdock, symplectic-spread, and
orthogonal-spread construction route for \(k=16\). It is an ansatz
exclusion, not a solution of Erdős--Rosenfeld Problem #835.

Let \(P\) be a 32-point ground set. A binary 4-spread of an
eight-dimensional binary vector space \(W\) is a partition of
\(W\setminus\{0\}\) into seventeen four-dimensional \(\mathbb F_2\)-subspaces
with zero removed. A symplectic or orthogonal spread, including a
non-Desarguesian/Kerdock spread, is an example. The familiar
Desarguesian case is \(W=\mathbb F_{16}^2\), with its 17 projective lines.

The most direct code/spread proposal assigns an arbitrary binary syndrome
\(v_p\in W\) to each ground point, forms
\[
 \sigma(S)=\sum_{p\in S}v_p,\tag{1}
\]
and colours a 16-set by the spread member containing \(\sigma(S)\).
For this to be a colouring, every syndrome in (1) must be nonzero. The
theorem below does not assume that the point labels are distinct, linear in
the point coordinates, or compatible with the automorphism group of the
spread.

## Theorem

No colouring of \(J(32,16)\) of the form (1), decoded by **any** binary
4-spread of \(W\cong\mathbb F_2^8\), is proper.

## Proof

Suppose otherwise and fix one spread member \(L\). Put
\[
 Q=W/L\cong\mathbb F_2^4,
\]
and write \(a_p=v_p+L\in Q\). Every 15-star contains each of the
seventeen colours exactly once. In particular, for every 15-subset
\(T\subset P\), exactly one \(x\in P\setminus T\) has the colour
corresponding to \(L\). Equivalently,
\[
 \boxed{\text{exactly one }x\notin T\text{ satisfies }
 a_x=\sum_{p\in T}a_p.}\tag{2}
\]

We show (2) is impossible. Fix a 14-subset \(R\), set
\(U=P\setminus R\), and put \(r=\sum_{p\in R}a_p\). Thus \(|U|=18\).
Applying (2) to \(T=R\cup\{i\}\), for every \(i\in U\) there is exactly
one \(j\in U\setminus\{i\}\) satisfying
\[
 a_j=r+a_i.\tag{3}
\]

If \(r\ne0\), let \(m(s)\) be the multiplicity of \(s\in Q\) among the
18 values indexed by \(U\), and let \(D=\{s:m(s)>0\}\). Equation (3)
gives \(m(r+s)=1\) for every \(s\in D\). Hence \(r+D\subseteq D\), and
finite cardinality gives \(r+D=D\). Every member of \(D\) is consequently
of the form \(r+s\), so it has multiplicity one. This would give 18
distinct elements of \(Q\), although \(|Q|=16\), a contradiction.
Therefore
\[
 \sum_{p\in R}a_p=0\quad\text{for every 14-subset }R.\tag{4}
\]

Two 14-subsets sharing thirteen points and differing in arbitrary distinct
points \(i,j\) give, after subtracting their two equations (4),
\(a_i=a_j\). Hence all 32 labels have one common value. But then in
(3), with \(r=0\), every \(i\in U\) has the other seventeen elements of
\(U\) as possible choices for \(j\), rather than exactly one. This final
contradiction proves the theorem. \(\square\)

## Consequence

This genuinely extends the earlier projectivized \(\mathbb F_{16}^2\)-sum
no-go: it also excludes a nonlinear Kerdock spread. A Kerdock or
Preparata-based positive construction must therefore use a non-additive
subset statistic before its spread decoder; changing the spread alone
cannot evade the obstruction.

Run

```bash
python3 -B evidence/verify_kerdock_spread_additive_syndrome_no_go.py
```

for a finite audit of the only numerical step in the multiplicity argument.
