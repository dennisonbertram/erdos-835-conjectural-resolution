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

## The mate-intersection parity conjecture

After Theorem D, the surviving narrow statement is:

**Conjecture E (Conjectural; decisive at \(r=15\)).**  If \(B,C\) are
legs block-disjoint from a common leg \(A\), then
\(|B\cap C|\equiv b\pmod2\); equivalently
\(\operatorname{wt}(x_B+x_C)\equiv0\pmod4\).

If true at \(r=15\), where \(b\) is odd, two mates of a common leg can
never be disjoint: no three pairwise disjoint \(S(14,15,31)\) exist,
hence no \(LS(14,15,31)\) and \(\chi(J(32,16))\ge18\).

**Lemma 5 (Proved).  Agreement reformulation.**  The unique-disjoint-mate
map \(\nu(S)=\) (the \(A\)-block disjoint from \(S\)) restricts to a
bijection from \(B\cap C\) onto
\(\{D\in A:\ w_B(D)=w_C(D)\}\), where \(w_X(D)\) is the point missing
from \(D\sqcup\mu_{AX}(D)\).  Hence
\[
 |B\cap C|=\#\{D\in A:\ w_B(D)=w_C(D)\},
\]
an agreement count of two \(b/v\)-uniform maps \(A\to\) points.
*Proof.*  For \(S\in B\cap C\), \(\nu(S)\) is defined by the external
identity \(n_0=1\) and \(\mu_{AB}(\nu(S))=S=\mu_{AC}(\nu(S))\) since mate
maps are inverse bijections; conversely
\(\mu_{AB}(D)=\mu_{AC}(D)\iff D^c\setminus\{w_B(D)\}
=D^c\setminus\{w_C(D)\}\iff w_B(D)=w_C(D)\), and then the common block
lies in \(B\cap C\). \(\square\)

**Verified (2026-07-24).**
- \(r=3\): all 28 mate pairs of a fixed Fano have \(|B\cap C|=1\equiv
  b\pmod2\).
- \(r=5\): all \(10\,296\) mate pairs of a fixed \(S(4,5,11)\) have
  \(|B\cap C|\in\{6,18\}\) — every value even \(\equiv b=66\), and
  moreover an **odd multiple of \(b/v\)** (\(6=b/11\), \(18=3b/11\);
  at \(r=3\), \(1=b/7\)).  Since \(v\) is odd, the odd-multiple law
  implies Conjecture E wherever it holds.  Co-mate degrees: each mate
  has 88 co-mates at intersection \(6\) and 55 at \(18\).

**Refuted refinements (Verified, 2026-07-24).**
- *Per-point*: \(|w_B^{-1}(x)\cap w_C^{-1}(x)|\) is NOT
  \(\equiv b/v\pmod2\) pointwise (values \(0,1,2,3\) all occur;
  53\,856 of 113\,256 instances odd).  Only the sum over all \(v\)
  points obeys the parity.
- *Per-link local signs* (Proved no-go): there is no per-\((r-2)\)-set
  cocycle \(g\) on perfect matchings with
  \(|M\cap M'|\equiv g(M)+g(M')+\text{const}\): the link \(K_{18}\)
  contains three pairwise disjoint perfect matchings, which would need
  three pairwise distinct values in \(\mathbb F_2\).  Plain sign
  products of matchings are identically \(+1\) (tautological).  Any
  proof of Conjecture E must couple the links globally.

## The transition matrix and the canonical permutation

For mates \(B,C\) of \(A\) let
\(m_{pq}=\#\{D\in A: w_B(D)=p,\ w_C(D)=q\}\).  All row and column sums
equal \(b/v\) (uniformity theorem), so the off-diagonal part is an
Eulerian directed multigraph and \(|B\cap C|=\operatorname{tr}m\).

**Refuted (Verified, 2026-07-24).**  Neither \(m=m^{\mathsf T}\) nor the
weaker "\(m_{pq}+m_{qp}\) even for every unordered pair" holds in ANY
instance: 0/28 at \(r=3\), 0/10\,296 at \(r=5\).  Sample counterexample
(\(r=3\), first mate pair): odd unordered entries at
\((p,q)\in\{(0,1),(0,3),(1,3),(2,4),(2,5),(4,5)\}\).

**Lemma 6 (Proved).  Two canonical matchings and a fixed-point-free
permutation.**  On the trade bipartition \((B\setminus C)\sqcup
(C\setminus B)\) (each side of size \(t=b-|B\cap C|\)):
1. the graph with edges "share a facet" is simple and 15-regular; hence
   \(t=0\) or \(t\ge15\);
2. \(\varphi_1(S)=\mu_{AC}(\nu(S))\) (partner through the common
   \(A\)-mate) is a perfect matching realized by edges
   (\(|S\cap\varphi_1(S)|=r-1\));
3. \(\varphi_2(S)=\nu_C(S)\) (the unique \(C\)-block disjoint from
   \(S\), which lies in \(C\setminus B\) because intra-\(n_0=0\)) is a
   second perfect matching, disjoint from the first in the strongest
   sense: \(|S\cap\varphi_2(S)|=0\);
4. therefore \(\sigma:=\varphi_2^{-1}\circ\varphi_1\) is a canonical
   permutation of \(B\setminus C\), and it is fixed-point-free
   (\(\varphi_1(S)=\varphi_2(S)\) would force \(r-1=0\)).
Consequently \(t\equiv\#\{\text{odd cycles of }\sigma\}\pmod2\).
\(\square\)

**The even-cycle identity (Conjectural; Verified exhaustively,
2026-07-24).**  In every existing instance, \(\sigma\) has **only even
cycles** — equivalently, every \(\varphi_1/\varphi_2\)-alternating cycle
has length \(\equiv0\pmod4\):
- \(r=3\): all 28 mate pairs give the single cycle type \((6)\).
- \(r=5\): all 10\,296 mate pairs realize exactly four cycle types:
  \((2,2,2,2,18,22)\) for all 3960 pairs with \(|B\cap C|=18\), and
  \((2,2,2,4,6,44)\times3960\), \((4,4,4,4,4,40)\times1584\),
  \((2,2,2,2,2,10,20,20)\times792\) for the 6336 pairs with
  \(|B\cap C|=6\).
The even-cycle identity implies \(t\) even, i.e. Conjecture E, in every
case; at \(r=15\) it would give
\(\chi(J(32,16))\ge18\).  The extreme rigidity of the cycle-type census
(four types across \(10\,296\) pairs) indicates a strong hidden
invariant; the proposed proof target is a \(\mathbb Z_4\)-valued
refinement along alternating cycles (a relative quadratic function on
the two matchings) forcing length \(\equiv0\bmod4\).  A per-link or
per-point localization of this invariant is already excluded by the
no-go results above.

## Blockwise structure of \(\sigma\) and the chain law

**Lemma 7 (Proved).  Blockwise formulas.**  For \(S\in B\setminus C\)
with \(A\)-mate \(D=S^c\setminus\{\alpha\}\):
\(\varphi_1(S)=(S\setminus\beta)\cup\{\alpha\}\) for a unique
\(\beta\in S\) (a single swap; \((\alpha,\beta)=(w_B,w_C)(D)\)), and
\(\sigma(S)=(D\setminus\delta)\cup\{\beta\}\) for a unique
\(\delta\in D\).  Hence \(|\sigma(S)\cap S|=\{\beta\}\), and the
alternating cycle lifts to a closed walk
\(S_0\,D_0\,T_0\,S_1\cdots\) of length \(3\ell\) in the odd graph
\(O_{r+1}\), where \(D_i\) is the unique common neighbour of \(S_i\) and
\(T_i\).  For odd \(\ell\) this re-derives (only) the girth bound
\(3\ell\ge2r+1\).

**Lemma 8 (Proved).  Chain law.**  Consecutive \(A\)-mates satisfy
\(D_i\cap D_{i+1}=\{\delta_i\}\) exactly.  *Proof.*  Computing,
\(D\cap D'=\{\delta\}\setminus\{\alpha'\}\); if \(\alpha'=\delta\) then
\(D'=(S\setminus\beta)\cup\{\alpha\}=\varphi_1(S)\in C\), contradicting
\(D'\in A\). \(\square\)  (Machine census: 336/336 steps at \(r=3\),
33\,180/33\,180 at \(r=5\) have \(|D_i\cap D_{i+1}|=1\).)

**Lemma 9 (Proved).  Transport to the disagreement set.**  \(\nu\)
conjugates \(\sigma\) to a canonical permutation \(\sigma_\Delta\) of the
disagreement set \(\Delta=\{D:w_B(D)\ne w_C(D)\}\subseteq A\), with
\(|D\cap\sigma_\Delta(D)|=1\) and step labels
\((\alpha,\beta)=(w_B,w_C)(D)\).  The even-cycle identity is thus a
statement about closed 1-intersection chains inside the single Steiner
system \(A\), decorated by the two \(w\)-maps.

**Tautology screen (Proved).**  The candidate local bits
\([\alpha=\gamma]\), \([\beta_{i+1}=\delta_i]\),
\([\alpha_{i+1}=\beta_i]\) are identically zero (each equality would
force a block into two disjoint legs or a point into a set excluding
it); their empirical "success" in the cycle-sum test is exactly the
even-cycle identity restated, not an invariant.  The telescoped
position identity
\(\sum_i(e_{\alpha_i}+e_{\beta_i}+e_{\delta_i})=\ell\cdot\mathbf 1\)
over \(\mathbb F_2^v\) (every point covered with multiplicity
\(\equiv\ell\)) is proved, and for odd \(\ell\) yields only the known
girth bound — the identity lies strictly deeper.

**No off-boundary control exists (Proved).**  For \(v>2r+1\)
(e.g. \(STS(9)\)) the disjoint partner of an external block is neither
unique nor of complement-minus-a-point shape, so
\(\varphi_1,\varphi_2,\sigma\) are undefined: the canonical machinery is
special to the boundary family \(v=2r+1\).

Verification script: `sigma_battery.py` (session scratchpad).

## The H-system counting identity and the mod-4 reduction

**Theorem E1 (Proved; verifier `verify_H_identity.py`).**  For mates
\(B,C\) of \(A\), with \(H_X(P)=P\cup\{w_X(P)\}\):
1. every \((r+2)\)-set contains exactly one \(H_B(P)\) (existence via
   \(P=\mu_{BA}(T_f)\) for the \(B\)-block \(T_f\) through the facet
   \(f=Y^c\); uniqueness by Steiner uniqueness of \(T_f\));
2. \(\binom{2r+1}{r+2}=b+(r-1)h+X(B,C)\), where \(h=|B\cap C|\) and
   \(X\) counts ordered pairs \(P\ne Q\) in \(A\) with
   \(|P\cap Q|=r-2\), \(w_B(P)\in Q\setminus P\),
   \(w_C(Q)\in P\setminus Q\)  (diagonal \(r\)-vs-1 count plus the
   \(|H\cap H|=r\) classification; \(H_B(P)=H_C(Q)\) impossible);
3. \(X=\sum_R\#\mathrm{fix}(c_R\circ b_R)\) over \((r-2)\)-links, where
   \(b_R,c_R\) are the fixed-point-free edge maps induced by
   \(w_B,w_C\) on the link matching \(M_A(R)\) (using
   \(P^c=\mathrm{link}\setminus e\)).

Machine-verified on all 56 (\(r=3\)) and all 20\,592 (\(r=5\)) ordered
mate pairs: \((h,X)=(1,12)\) and \((6,240),(18,192)\), matching
\(X=14-2h\) and \(264-4h\).

**Corollary (Proved).**  At \(r\equiv3\pmod4\):
\(X\equiv\binom{2r+1}{r+2}-b-2h\pmod4\), and Conjecture E is equivalent
to \(X\equiv\binom{2r+1}{r+2}-3b\pmod4\); at \(r=15\) both constants are
\(1\bmod4\), so **Conjecture E \(\iff X\equiv0\pmod4\)**.  At
\(r\equiv1\pmod4\) the \(h\)-term is \(4h\), so \(X\equiv0\pmod4\) is
automatic and carries no information (tautology flagged; \(r=5\) can
test only finer link structure).  The link matching has
\(m=(r+3)/2\) edges — odd exactly at \(r\equiv3\pmod4\).

**Census (Verified, 2026-07-24).**  \(r=3\): per-link
\(\#\mathrm{fix}\in\{0,3\}\) only (all-or-nothing); \(b_R\) injective in
392/392 links, and \(c_R\circ b_R\) is never a transposition — a
sign-coherence law \(\operatorname{sgn}b_R=\operatorname{sgn}c_R\); the
four endpoint-bit classes of \(X\)-configurations are EXACTLY
equinumerous, globally (168 each) and per mate pair (3 each = X/4).
\(r=5\): per-link \(\#\mathrm{fix}\in\{0,\dots,4\}\) spread, \(b_R\)
non-injective in 2/3 of links, endpoint classes only approximately
balanced — consistent with the mod-4 statement being substantive only
at \(r\equiv3\pmod4\).  \(X\equiv0\pmod4\) in all 256 pairs tested.

**Fibre lemma (Proved, 2026-07-25).**  For a disagreement base \(P\),
the \((r+2)\)-sets containing \(H_B(P)\) are \(H_B(P)\cup\{z\}\) for the
\(r\) outside points \(z\); the one with \(z=w_C(P)\) is diagonal, and
each of the other \(r-1\) automatically yields an \(X\)-configuration
\((P,Q_z)\) (the \(|H\cap H|=r\) classification admits no other case).
Agreement bases carry none.  Hence
\[
 \boxed{X=(r-1)(b-h)\ \text{identically}},
\]
machine-checked on all \(56+20\,592\) ordered mate pairs
(\(2\cdot6=12\); \(4\cdot60=240\), \(4\cdot48=192\)).

**Scope corollary (Proved).**  The counting identity collapses to
\(\binom{2r+1}{r+2}=rb\) (both sides count facets); \(X\) is an affine
function of \(h\), so "evaluate \(X\bmod4\) independently" is the same
statement as Conjecture E, not a separate route.  A canonical free
group action of order \(\equiv0\pmod4\) on the configuration set would
still prove it.

**Klein-four mechanism (Refuted, exhaustive).**  The canonical fibre
involutions \(\tau_B,\tau_C\) (swap within a size-2 fibre; canonical
only at \(r=3\)) commute in 0/56 ordered mate pairs; witness recorded in
`verify_H_identity.py` output.

**D6-torsor theorem at \(r=3\) (Verified exhaustively, 56/56).**  The
product \(\tau_B\tau_C\) always has cycle type \((6,6)\), and
\(\langle\tau_B,\tau_C\rangle\) has order exactly 12 acting freely and
transitively: the 12 configurations form a torsor for the dihedral
group \(D_6\).  Since \(4\mid12\), this forces \(X\equiv0\pmod4\), i.e.
\(t\) even — a group-action proof of Conjecture E at \(r=3\)
(exhaustive over the isomorphism-complete mate census).  Equivalently,
the bipartite fibration graph (configurations as edges between
\(B\)-bases and \(C\)-bases, \((r-1)\)-regular) is a single 12-cycle in
every instance.

**Proof target (Conjectural, updated).**  At \(r\equiv3\pmod4\) the
configuration set of any mate pair carries a canonical free action of a
group of order \(\equiv0\pmod4\) (at \(r=3\): \(D_6\)); equivalently a
parity-coherent structure on the \((r-1)\)-regular bipartite fibration
graph on \(\Delta\sqcup\Delta\) forcing \(t\) even.  Note the fibration
graph has the same shape (14-regular bipartite on \(t+t\) at \(r=15\))
as the trade-graph remainder of Lemma 6 — possibly the same object
under the canonical bijections; unchecked.  Secondary verified-only
laws at \(r=3\): per-link all-or-nothing, sign coherence
\(\operatorname{sgn}b_R=\operatorname{sgn}c_R\), fourfold endpoint
balance.

## Provenance

All computations 2026-07-24, session scratchpad scripts
(`disjoint_mates.py` and inline derivatives); exact integer/bitmask
arithmetic throughout; Steiner constructions by exhaustive exact cover
(Algorithm X), verified by direct recount.  Theorems A–C and Lemmas 1–2
are proved above in full and were additionally machine-checked at
\(r=3\), \(r=5\), and on the \(STS(9)\) positive control.  Theorem D is
an exact dimension argument and uses no unrecorded computation; its
nondegeneracy identity (8) was additionally machine-checked at
\(r=3,5\) (\(\operatorname{rank}_2 WW^{\mathsf T}
=\operatorname{rank}_2W\): \(15\) and \(210\)).  Lemma 6 and the
even-cycle census were machine-verified on all 28 (\(r=3\)) and all
10\,296 (\(r=5\)) mate pairs of a fixed base leg.
