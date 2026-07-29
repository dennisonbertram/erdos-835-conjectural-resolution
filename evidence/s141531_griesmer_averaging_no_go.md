# A global averaging no-go for endpoint-only Griesmer shortening

Date: 2026-07-26.

Status: **proved limitation of one coding-theoretic strategy; not a
nonexistence proof for \(S(14,15,31)\), and not a solution of
Erdős--Rosenfeld Problem 835**.

The exact verifier is

```bash
python3 -B evidence/verify_s141531_griesmer_averaging_no_go.py
```

Its SHA-256 is

```text
8fe24fc91b1034f5eb7b5b039d8c7e4e9663e8d1692754b2c2080f03425f35b3
```

## 1. Safe radial endpoints

Assume that \(A\) is an \(S(14,15,31)\), with

\[
 b=|A|=17\,678\,835.
\]

The full-rank point theorem identifies the even point subsets

\[
 E=\{S\subseteq[31]:|S|\equiv0\pmod2\}
\]

with the 30-dimensional even point-incidence code.  Put

\[
 F(S)=\sum_{B\in A}(-1)^{|B\cap S|}.
\]

Let \(F_{\rm ext}(s)\) be the value forced by the first fourteen design
moments, with the external value used at sizes 15 and 16.  On \(E\),
define the two radial functions

\[
 F^-(S)=F_{\rm ext}(|S|),
\qquad
 F^+(S)=F^-(S)+2^{15}\mathbf1_{\{|S|=16\}}.
\tag{1}
\]

For every even \(S\),

\[
 F^-(S)\leq F(S)\leq F^+(S).
\tag{2}
\]

The only possible inequality in (2) is at size 16.  Its upper endpoint
occurs when the complementary 15-set is a block.

## 2. Shortening on an arbitrary subspace

Let \(H\leq E\) have dimension \(m<30\), and put

\[
 q=|H|=2^m,\qquad
 k=30-m,\qquad
 N=2^k.
\]

Thus \(N\) is the number of cosets of \(H\) in \(E\).  Define

\[
 A^\pm=\sum_{h\in H}F^\pm(h)
\]

and, for a coset \(Q=c+H\),

\[
 B^+(Q)=\sum_{x\in Q}F^+(x).
\]

Let \(Z_H\) be the design blocks on which all words of \(H\) vanish.
Character orthogonality and (2) give the safe length upper bound

\[
 |Z_H|
 =\frac1q\sum_{h\in H}F(h)
 \leq
 n^+:=\left\lfloor\frac{A^+}{q}\right\rfloor.
\tag{3}
\]

All representatives of one coset have the same restriction to \(Z_H\).
Their common weight is

\[
 \operatorname{wt}_{Z_H}(Q)
 =
 \frac{\sum_{h\in H}F(h)-\sum_{x\in Q}F(x)}{2q}.
\]

Consequently the endpoint-only lower bound over outside cosets is

\[
 d^-=
 \min_{Q\ne H}
 \left\lceil
 \frac{A^- - B^+(Q)}{2q}
 \right\rceil.
\tag{4}
\]

If \(d^-\leq0\), this method supplies no positive minimum-distance
bound.  If \(d^->0\), every outside coset has nonzero restriction, so
the shortening kernel is exactly \(H\) and its image dimension is
exactly \(k\).

## 3. Exact Fourier averaging

Regard \(E\) as an abelian group under symmetric difference, and set
\(g=F^+\).  Its total sum is

\[
 T=\sum_{S\in E}g(S)=2^{19}b
   =9\,268\,801\,044\,480.
\tag{5}
\]

One way to see (5) is to first sum the actual \(F\).  For each
15-block \(B\), its character is nontrivial on \(E\), so

\[
 \sum_{S\in E}F(S)=0.
\]

Exactly \(b\) size-16 subsets are complements of blocks.  Hence

\[
 \sum_{S\in E}F^-(S)=-2^{15}b.
\]

There are

\[
 \binom{31}{16}=17b
\]

size-16 subsets, and adding the artificial upper correction in (1)
proves (5).

A character of \(E\) is indexed by a subset \(U\subseteq[31]\), with
\(U\) and its complement giving the same character.  It therefore
suffices to calculate character weights \(0,\ldots,15\).  The exact
Krawtchouk transform of \(g\) is

\[
\begin{array}{c|r}
|U|&\widehat g(U)\\ \hline
0&9\,268\,801\,044\,480\\
1,2&-298\,993\,582\,080\\
3,4&30\,930\,370\,560\\
5,6&-5\,727\,846\,400\\
7,8&1\,603\,796\,992\\
9,10&-627\,572\,736\\
11,12&328\,728\,576\\
13,14&-224\,919\,552\\
15&261\,619\,712
\end{array}
\tag{6}
\]

Thus the largest nonprincipal transform value is

\[
 R=30\,930\,370\,560.
\tag{7}
\]

Let \(H^\perp\) be the character annihilator of \(H\), of order \(N\).
Fourier inversion and (7) give

\[
 A^+
 =\frac1N\sum_{u\in H^\perp}\widehat g(u)
 \leq\frac{T+(N-1)R}{N}.
\tag{8}
\]

The \(B^+(Q)\) over all \(N\) cosets sum to \(T\), while the value at
the zero coset is \(A^+\).  Therefore some outside coset has

\[
\begin{aligned}
 M:=\max_{Q\ne H}B^+(Q)
 &\geq\frac{T-A^+}{N-1}\\
 &\geq\frac{T-R}{N}\\
 &=q\,\frac{T-R}{2^{30}}
 =q\,\frac{137\,655}{16}.
\end{aligned}
\tag{9}
\]

In particular,

\[
 M>31q\geq q(k+1).
\tag{10}
\]

This is the step that covers all proper subspace dimensions at once,
including \(m=28\) and \(m=29\).

## 4. The Griesmer comparison can never be strict

Assume that the endpoint lower bound \(d^-\) in (4) is positive.
Since (4) is minimized at a coset attaining \(M\),

\[
 d^-=
 \left\lceil\frac{A^- - M}{2q}\right\rceil
 <
 \frac{A^- - M}{2q}+1.
\tag{11}
\]

For every positive integer \(d\) and \(k\geq1\), the binary Griesmer
sum satisfies

\[
 G(d,k)=\sum_{i=0}^{k-1}\left\lceil\frac d{2^i}\right\rceil
 \leq2d+k-1.
\tag{12}
\]

Combining (10)--(12) gives

\[
\begin{aligned}
 G(d^-,k)
 &<\frac{A^- - M}{q}+k+1\\
 &<\frac{A^-}{q}\\
 &\leq\frac{A^+}{q}.
\end{aligned}
\]

The Griesmer sum is an integer, so

\[
 G(d^-,k)\leq
 \left\lfloor\frac{A^+}{q}\right\rfloor=n^+.
\tag{13}
\]

Thus the safe endpoint bounds can never produce the strict inequality
\(G(d^-,k)>n^+\) needed for a contradiction.  If \(d^-\leq0\), the
method was already vacuous.  This proves:

> **Endpoint-averaging no-go.**  For every proper subspace
> \(H<E\), in every dimension \(0\leq m\leq29\), independently
> maximizing every unresolved size-16 Fourier value and then applying
> the binary Griesmer bound to the common-zero shortening cannot
> disprove the existence of \(S(14,15,31)\).

For \(m=30\), \(H=E\), there is no outside coset and the shortened
image is zero, so there is no missing case.

## 5. Scope

This theorem supersedes random searches for a Griesmer contradiction
that use only the independent endpoints (1).  It does **not** exclude:

- joint constraints on which complementary 15-sets can simultaneously
  be blocks;
- an exact rather than independently maximized value of \(B(Q)\);
- stronger coding-theoretic inequalities;
- shortenings not defined by common-zero coordinates; or
- a different obstruction to the design or to a 17-member large set.

The averaging theorem closes a proof route.  It does not settle the
existence of the design.
