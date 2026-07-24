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

**Consequence.**  Conjecture D below is equivalent to the purely
combinatorial statement: *for \(r\equiv3\pmod4\), every even-degree
block-set inside the complement of two disjoint legs spans an even
number of facet-sharing pairs.*  This removes all coding-theoretic
language from the target.

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

Observed dichotomy: at \(r=3\) the form is totally degenerate
(\(B\equiv0\), \(q\equiv0\)); at \(r=5\) it is nondegenerate.

## Conjecture D (Conjectural; the decisive statement)

For \(r\equiv3\pmod4\), the pair-trade code of any two block-disjoint
\(S(r-1,r,2r+1)\) is doubly even.

Evidence: true in all 8 instances at \(r=3\); no counterexample is
possible at \(r\equiv1\pmod4\) (different residue); no further test
instances exist — the family requires \(r+2\) prime, and \(r=11\) is
empty because \(S(10,11,23)\) would derive to the nonexistent
\(S(4,5,17)\), while \(r=15\) instances require a first
\(S(14,15,31)\), itself open.  If Conjecture D holds at \(r=15\), then
by Theorems B–C, \(\chi(J(32,16))\ge18\): the first open case of
Erdős #835 is resolved negatively.

## Remark (Proved, negative).  No abstract rank bound can substitute

A configuration of fifteen vectors with \(q=1\) and pairwise \(B=1\)
exists in nondegenerate quadratic \(\mathbb F_2\)-spaces of either Arf
type once the dimension is moderately large (embed the span, whose Gram
is \(J-I\) of rank 14, and extend \(q\) accordingly; both Arf classes of
forms of dimension \(\ge16\) contain isometric copies).  Since
\(\dim C\) at \(r=15\) is astronomically large, no bound on dimensions
or ranks alone can exclude the 17-clique: the route **must** prove the
degeneracy/doubly-evenness of Conjecture D, e.g. through a mod-4
refinement of Wilson's diagonal form for inclusion matrices restricted
to complements of two Steiner legs.  This is the proposed next step.

## Provenance

All computations 2026-07-24, session scratchpad scripts
(`disjoint_mates.py` and inline derivatives); exact integer/bitmask
arithmetic throughout; Steiner constructions by exhaustive exact cover
(Algorithm X), verified by direct recount.  Theorems A–C and Lemmas 1–2
are proved above in full and were additionally machine-checked at
\(r=3\), \(r=5\), and on the \(STS(9)\) positive control.
