# The mod-4 quadratic form of the pair-trade code

Status labels used below: **Proved** (complete proof given), **Verified**
(finite computation, script and date recorded), **Conjectural** (clearly
open; stated with all known evidence).

Setting: \(r\) odd, \(v=2r+1\), legs are Steiner systems \(S(r-1,r,v)\)
with \(b=\binom{v}{r}/(r+2)\) blocks.  \(W\) is the facet–block inclusion
matrix (rows: \((r-1)\)-sets; columns: \(r\)-sets).  For two
block-disjoint legs \(D_1,D_2\), let
\[
 U=\{\,r\text{-sets}\}\setminus(D_1\sqcup D_2),\qquad |U|=rb,
\]
so that every facet lies in exactly \(r\) blocks of \(U\).  Define the
**pair-trade code**
\[
 C=C(D_1,D_2):=\ker_{\mathbb F_2}\bigl(W|_U\bigr).
\]

## Lemma 1 (Proved).  \(C\) is an even code

The column of a block \(B\in U\) has weight \(r\), which is odd.  Hence
the sum of all rows of \(W|_U\) is the all-ones vector \(\mathbf 1\), so
\(\mathbf 1\in\operatorname{rowspace}(W|_U)=C^\perp\), i.e. every
\(c\in C\) has even weight. \(\square\)

## Lemma 2 (Proved).  The quadratic form

On any even binary code, \(q(c):=\operatorname{wt}(c)/2 \bmod 2\)
satisfies
\[
 q(a+b)=q(a)+q(b)+|a\cap b| \bmod 2 ,
\]
because \(\operatorname{wt}(a+b)=\operatorname{wt}(a)+\operatorname{wt}(b)
-2|a\cap b|\).  Thus \(q\) is a quadratic form on \(C\) with polar form
\(B(a,b)=|a\cap b|\bmod2\).  \(C\) is self-orthogonal iff \(B\equiv0\),
and doubly even (all weights \(\equiv0\bmod4\)) iff \(q\equiv0\); doubly
even implies self-orthogonal. \(\square\)

## Theorem A (Proved).  Third-leg correspondence

A third leg (an \(S(r-1,r,v)\) block-disjoint from \(D_1\sqcup D_2\))
exists **iff** \(C\) contains a word \(c\) whose support meets every
facet-row in exactly \(r-1\) blocks.  The correspondence is
\(x=\mathbf 1_U-c\); such \(c\) has \(\operatorname{wt}(c)=(r-1)b\).

**Proof.**  If \(x\) is a third-leg indicator, then \(c=\mathbf 1_U-x\)
is 0–1, and each facet sees \(r-1\) of its \(r\) \(U\)-blocks in
\(\operatorname{supp}(c)\); since \(r-1\) is even, \(c\in C\).
Conversely if \(c\in C\) has every facet-degree exactly \(r-1\), then
\(x=\mathbf 1_U-c\) is 0–1 with every facet-sum exactly one, a Steiner
leg.  The weight count is \(|U|-b=(r-1)b\). \(\square\)

**Stress test (Verified, 2026-07-24).**  Positive control on the
resolvable family \(v=9\), \(k=3\): three pairwise disjoint
\(STS(9)\) were constructed; with \(U\) the complement of the first two
(60 triples, facet-replication \(\rho=5\)), the word
\(c=\mathbf 1_U-x_3\) has facet-degree exactly \(4=\rho-1\) on all 36
pairs, weight \(48=|U|-12\), and \(q(c)=0=(\rho-1)\cdot12/2\bmod2\), as
predicted.  Negative consistency at \(r=3,5\) below.

## Theorem B (Proved).  Mod-4 obstruction for odd \(r\)

The word required by Theorem A has
\[
 q(c)=\tfrac{(r-1)b}2 \bmod 2
 =\begin{cases}
   b\bmod 2, & r\equiv3\pmod4,\\
   0, & r\equiv1\pmod4.
  \end{cases}
\]
Hence **if \(r\equiv3\pmod4\), \(b\) is odd, and \(C(D_1,D_2)\) is doubly
even, then no third leg exists.**

At \(r=15\): \(b=17\,678\,835\) is odd and \(r\equiv3\pmod4\), so the
hypothesis "\(C\) doubly even" excludes any third disjoint
\(S(14,15,31)\).  At \(r=5\): \((r-1)b/2=132\) is even, so **no**
mod-4 obstruction is possible there regardless of the code — the
known nonexistence of a third \(S(4,5,11)\) is invisible to this
invariant, which is consistent, and the observed failure of
self-orthogonality at \(r=5\) is **not** a counterexample to the
\(r\equiv3\) conjecture below. \(\square\)

## Theorem C (Proved).  Reduction of the 17-clique at \(r=15\)

Suppose seventeen pairwise disjoint \(S(14,15,31)\) exist (equivalently
\(LS(14,15,31)\); equivalently \(\chi(J(32,16))=17\)).  Fix any two of
them as \(D_1,D_2\) and let \(L_3,\dots,L_{17}\) be the rest.  Then the
fifteen words \(c_i=\mathbf 1_U-x_{L_i}\in C\) satisfy
\[
 q(c_i)=1,\qquad B(c_i,c_j)=1\ (i\ne j),
\]
since \(|\operatorname{supp}(c_i)\cap\operatorname{supp}(c_j)|
=|U|-2b+0=(r-2)b=13b\) is odd.  (Consistency:
\(q(c_i+c_j)=q(x_{L_i}+x_{L_j})=b\bmod2=1=1+1+1\).)  Hence **doubly
evenness of a single pair-trade code at \(r=15\) excludes the entire
17-clique**, i.e. proves \(\chi(J(32,16))\ge18\). \(\square\)

## Lemma 3 (Proved).  The polar form counts facet-sharing pairs

For \(a,b\in C\), let \(I_{r-1}(a,b)\) be the number of pairs
\((S,T)\in\operatorname{supp}(a)\times\operatorname{supp}(b)\) with
\(|S\cap T|=r-1\).  Then
\[
 B(a,b)\equiv I_{r-1}(a,b)\pmod2 .
\]

**Proof.**  Counting facet-incidences,
\(\sum_f \deg_a(f)\deg_b(f)=I_{r-1}(a,b)+r\,I_r(a,b)\) over \(\mathbb Z\),
where \(I_r(a,b)=|a\cap b|\) counts common blocks.  Every
\(\deg_a(f)\) is even because \(a\in C\), so the left side is even; and
\(r\) is odd.  Hence \(I_r\equiv I_{r-1}\pmod2\). \(\square\)

## Lemma 4 (Proved).  The quadratic form counts internal pairs

For \(c\in C\), let \(N_2(c)\) be the number of unordered pairs of
distinct blocks of \(\operatorname{supp}(c)\) sharing a facet.  Then
\[
 q(c)\equiv N_2(c)\pmod2 .
\]

**Proof.**  \(\sum_f\binom{\deg_c(f)}2=N_2(c)\).  Writing
\(\deg_c(f)=2d_f\), \(\binom{2d_f}2=d_f(2d_f-1)\equiv d_f\pmod2\), so
\(N_2(c)\equiv\sum_f d_f=\tfrac12\sum_f\deg_c(f)
=\tfrac r2\operatorname{wt}(c)\equiv q(c)\pmod2\), using \(r\) odd.
\(\square\)

**Stress test (Verified, 2026-07-24).**  Both identities hold on 40/40
random words of an \(r=5\) pair-trade code.

**Consequence.**  A doubly-even pair-trade code would be equivalent to the
purely combinatorial statement: *every even-degree block-set inside the
complement of the two legs spans an even number of facet-sharing pairs.*
The dimension theorem below proves that this statement cannot hold at
\(r=15\).

## Data (Verified, 2026-07-24; scripts in session scratchpad)

- \(r=3\): all **8/8** pair-trade codes (one Fano and each of its eight
  disjoint mates) have \(\dim C=6\), weight enumerator
  \(1+21z^8+42z^{12}\), doubly even.  With Theorem B this re-proves that
  no three pairwise disjoint Fano planes exist.
- \(r=5\): for 10 pairs (a fixed \(S(4,5,11)\) and ten of its 144
  disjoint mates), \(\operatorname{rank}_2(W|_U)=210\), \(\dim C=120\),
  all weights even, **not** self-orthogonal; for the 4 pairs where the
  full Gram matrix was computed, \(B\) is **nondegenerate**
  (\(\operatorname{rank}B=120\), radical \(0\)).
- The 67 simple \(4\)-\((11,5,3)\) designs of McKay–Radziszowski were
  not obtainable in this environment; the computations above use the
  pair-complements, which are the objects relevant to the third-leg
  question.

Observed small-case dichotomy: at \(r=3\) the form is totally degenerate
(\(B\equiv0\), \(q\equiv0\)); at \(r=5\) it is nondegenerate.

## Theorem D (Proved, negative): the \(r=15\) code is not self-orthogonal

Conditionally on the existence of any two block-disjoint
\(S(14,15,31)\), their pair-trade code \(C\) is not self-orthogonal and
hence is not doubly even.  More precisely,
\[
 \dim C\ge119\,759\,850,
 \qquad
 \dim\operatorname{rad}(C)\le35\,357\,670. \tag{6}
\]
Consequently \(C\) contains words of weight \(2\bmod4\).

**Proof.**  Work over \(\mathbb F_2\).  Let \(W\) be the incidence matrix
from 14-subsets to all 15-subsets of a 31-set.  Let \(N=W|_U\), and let
\(R\) consist of the columns in the two deleted legs, so \(W=[N\ R]\).
The standard boundary rank of the full simplex is
\[
 s=\operatorname{rank}W=\binom{30}{14}=145\,422\,675. \tag{7}
\]

The row space of \(W\) is nondegenerate.  To see this directly, let \(V\)
be the incidence matrix from 15-subsets to 16-subsets.  Comparing entries
over \(\mathbb F_2\) gives
\[
 W^{\mathsf T}W+VV^{\mathsf T}=I,\qquad WV=0. \tag{8}
\]
On the diagonal, a 15-set has 15 facets and lies in 16 16-sets, whose
sum is one modulo two.  Off the diagonal, the common
Johnson-neighbour entry occurs once in each summand and cancels.  If
\(z\in\operatorname{row}W\cap\ker W\), write \(z=W^{\mathsf T}y\).
Equation (8) and \(V^{\mathsf T}W^{\mathsf T}=0\) give \(z=0\).
Therefore
\[
 \operatorname{rank}(WW^{\mathsf T})=s. \tag{9}
\]

The two removed legs contain \(2b\) columns, so
\(\operatorname{rank}(RR^{\mathsf T})\le2b\).  From
\[
 NN^{\mathsf T}=WW^{\mathsf T}+RR^{\mathsf T}
\]
and (9),
\[
 \operatorname{rank}(NN^{\mathsf T})\ge s-2b. \tag{10}
\]
Since \(C^\perp=\operatorname{row}N\),
\[
\begin{aligned}
 \dim\operatorname{rad}(C)
 &=\dim(C\cap C^\perp)\\
 &=\operatorname{rank}N-\operatorname{rank}(NN^{\mathsf T})\\
 &\le s-(s-2b)=2b=35\,357\,670. \tag{11}
\end{aligned}
\]

There are
\[
 |U|=\binom{31}{15}-2b=15b=265\,182\,525
\]
columns in \(N\).  Since \(\operatorname{rank}N\le s\),
\[
 \dim C=|U|-\operatorname{rank}N
 \ge15b-s=119\,759\,850. \tag{12}
\]
If \(C\) were self-orthogonal, then \(C\subseteq C^\perp\), so
\(\operatorname{rad}(C)=C\), contradicting (11)--(12).

Finally \(C\) is even by Lemma 1.  On an even code the polar form of
\(q(z)=\operatorname{wt}(z)/2\bmod2\) is the dot product.  Because the dot
product is nonzero on \(C\), one of \(u,v,u+v\) has \(q=1\) for a suitable
nonorthogonal pair \(u,v\).  Thus \(C\) contains a word of weight
\(2\bmod4\). \(\square\)

Theorem B remains a correct conditional obstruction for a particular
candidate code or subcode.  Theorem D rules out the proposed universal
claim that the whole \(r=15\) pair-trade kernel is doubly even.  Therefore
the broad mod-four code route cannot resolve \(k=16\); a successful parity
obstruction must use the exact facet-degree condition of Theorem A or
other nonlinear large-set compatibility.

## Provenance

All computations 2026-07-24, session scratchpad scripts
(`disjoint_mates.py` and inline derivatives); exact integer/bitmask
arithmetic throughout; Steiner constructions by exhaustive exact cover
(Algorithm X), verified by direct recount.  Theorems A–C and Lemmas 1–2
are proved above in full and were additionally machine-checked at
\(r=3\), \(r=5\), and on the \(STS(9)\) positive control.  Theorem D is
an exact dimension argument and uses no unrecorded computation.
