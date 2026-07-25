# Primary-literature and repository audit for the \(k=16\) frontier

Checked 2026-07-25.  This note concerns the exact target
\[
   \operatorname{LS}(15,16,32),
\]
not merely an ordered design, a constituent Steiner system, a derived design,
or a symmetric ansatz.

## Exact reduction to \(O_{16}\)

A tight 17-colouring of \(J(32,16)\) is exactly a partition of all 16-subsets
into 17 Steiner systems \(S(15,16,32)\).  Indeed, the 17 extensions of any
fixed 15-set form a clique, so each colour occurs exactly once on them.  Thus
each colour class is an \(S(15,16,32)\), and the converse is immediate.

There is a second exact equivalence which is useful for construction searches:

> An \(\operatorname{LS}(15,16,32)\) exists if and only if the vertices of
> the odd graph \(O_{16}\) can be partitioned into 17 perfect 1-codes.

Here \(O_{16}\) has the 15-subsets of a 31-set as vertices, adjacent when
disjoint.  Given a constituent \(S(15,16,32)\), derive at a fixed point
\(\infty\).  The resulting \(S(14,15,31)\) is a perfect 1-code in \(O_{16}\);
this is the Hammond--Smith correspondence.  Across the 17 constituents the
derived codes partition all \(\binom{31}{15}\) vertices.

Conversely, Mendelsohn's extension theorem says that every
\(S(14,15,31)\) extends uniquely to an \(S(15,16,32)\).  Explicitly, for a
code block \(C\subset[31]\), the extension contains
\(\{\infty\}\cup C\) and its complement \([31]\setminus C\).  Therefore a
partition of the 15-subsets into 17 codes partitions both the 16-subsets
containing \(\infty\) and, by complementation, those avoiding \(\infty\).

The exact sizes are
\[
 |V(O_{16})|=\binom{31}{15}=300\,540\,195,\qquad
 |C_i|=\frac1{17}\binom{31}{15}=17\,678\,835,
\]
and every extended constituent has \(35\,357\,670\) blocks.

Primary sources:

* P. Hammond and D. H. Smith, *Perfect codes in the graphs \(O_k\)*,
  J. Combin. Theory Ser. B **19** (1975), 239--255,
  <https://doi.org/10.1016/0095-8956(75)90087-8>.  Its abstract states the
  perfect-code/Steiner-system correspondence and that the numerical
  necessities hold when \(k+1\) is prime.
* N. S. Mendelsohn, *A theorem on Steiner systems*, Canad. J. Math. **22**
  (1970), 1010--1015,
  <https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DE878868DEAB0C05C5D2FD1829E4A656/S0008414X00047775a.pdf/a-theorem-on-steiner-systems.pdf>.
  Theorem 1 gives the existence equivalence and unique extension between
  \(S(t-1,t,2t+1)\) and \(S(t,t+1,2t+2)\).

This reduction does not make the target easier by itself: a current monograph
still states that the only known nontrivial perfect codes in odd graphs are
those arising from \(S(3,4,8)\) and \(S(5,6,12)\), and identifies \(O_{16}\)
as the first open case.  See D. Krotov and V. Potapov, *Completely Regular
Codes in Distance Regular Graphs* (2025), preview pp. 73--74:
<https://api.pageplace.de/preview/DT0400.9781040309025_A49868910/preview-9781040309025_A49868910.pdf>.

## Exact theorems that do not decide \(k=16\)

### Prime obstruction

Ma--Tang prove that a tight colouring can exist only when \(k+1\) is prime.
For \(k=16\), the surviving prime is 17, so their theorem does not decide this
case:
<https://github.com/QuanyuTang/erdos-problem-835/blob/main/On_Problem_835.pdf>.

### Odd-index spectral obstruction

Fiol proves that \(O_\ell\) has no perfect 1-code when \(\ell\) is odd.
The live graph is \(O_{16}\), so the parity is the opposite one:
M. A. Fiol, *A new class of polynomials from the spectrum of a graph, and its
application to bound the \(k\)-independence number*, LAA **605** (2020),
1--19, <https://arxiv.org/abs/1907.08626>.

### The misleading 1974 “non-existence” title

Assmus--Hermoso's paper is titled *Non-Existence of Steiner Systems of Type
\(S(d-1,d,2d)\)*, but its theorem is conditional: if the automorphism group
acts flag-transitively, then \(d=2,4,6\).  It therefore excludes a
flag-transitive \(S(15,16,32)\), not an arbitrary constituent and certainly
not an arbitrary large set.  The paper itself explicitly suggests that
asymmetric examples with \(d>6\) might still exist.

Primary scan, pp. 171--172:
<https://gdz.sub.uni-goettingen.de/id/PPN266833020_0138?tify=%7B%22view%22:%22info%22,%22pages%22:%5B179,180%5D%7D>.

### Derived \(S(4,5,21)\) and a symmetry exclusion

Eleven derivations of any \(S(15,16,32)\) give an \(S(4,5,21)\).  Thus
nonexistence of \(S(4,5,21)\) would exclude \(k=16\), but its existence would
still be only a necessary shadow.

Chee--Kreher prove only a symmetry-restricted negative result: a
\(4\)-\((21,5,1)\) design cannot have the order-57 subgroup of their
order-171 Frobenius group as an automorphism group.  They do not prove
unconditional nonexistence:
Y. M. Chee and D. L. Kreher, *\(4\)-\((21,5,\lambda)\) Designs from a Group
of Order 171*, Ars Combin. **36** (1993), 199--205,
<https://combinatorialpress.com/ars-articles/volume-036-ars-articles/4-215lambda-designs-from-a-group-of-order-171/>.

The maintained small-parameter table still marks \(S(4,5,21)\) with “?”:
<https://marwahaha.github.io/steinersystems/>.
This table is a secondary status check, not a nonexistence source.

### General large-set existence theorems

Keevash proves that for fixed block size \(q\) and strength \(r\), all
sufficiently large admissible \(n\) have the required large sets.  Theorem
`\(\ref{large}\)` in the source fixes \(q,r\) and assumes
\(n>n_0(q,r)\).  Substituting \((q,r,n)=(16,15,32)\) is not licensed: the
theorem supplies no assertion that 32 exceeds its threshold.
P. Keevash, *The existence of designs II*,
<https://arxiv.org/abs/1802.05900>.

Lovett--Rao--Vardy's explicit parameter regime is even farther away.  Their
Theorem 1 assumes \(q>9r\) and sufficiently large \(n\); here
\(16\not>9\cdot15\):
S. Lovett, S. Rao, A. Vardy, *Probabilistic Existence of Large Sets of
Designs*, <https://arxiv.org/abs/1704.07964>.

Teirlinck's ordered-design theorem does give
\(\operatorname{LOD}(15,16,32)\), but an LOD partitions ordered 16-tuples.
It need not keep all \(16!\) orderings of one support in a single part, so it
does not produce \(\operatorname{LS}(15,16,32)\).  The exact weighted-support
gap is audited separately in `ordered_design_symmetrization_audit.md`.

## Public repository check

The following exact GitHub code searches were run on 2026-07-25:

* `"LS(15,16,32)"`: no results;
* `"S(15,16,32)"`: one result, an exploratory obstruction table in
  `Siddhartha-Mahajan/attacking-erdos-problems`;
* `"O_16" "perfect code"`: no results.

The one exact-parameter artifact explicitly records \(k=16\) as
“not eliminated” and \(S(4,5,21)\) as open:
<https://github.com/Siddhartha-Mahajan/attacking-erdos-problems/blob/main/problems/problem_835_johnson_coloring/SUMMARY.md>.
Its \(S(4,5,21)\) artifact is build-only, not a solved certificate.

The Ma--Tang repository is public and contains the prime obstruction, not a
construction:
<https://github.com/QuanyuTang/erdos-problem-835>.

Search absence is not evidence of novelty or nonexistence.  It only establishes
that this audit found no posted exact witness or verifier under the direct
parameter spellings.

## Bottom line

No construction data for \(\operatorname{LS}(15,16,32)\), no perfect-code
partition of \(O_{16}\), and no unconditional nonexistence theorem were found.
The most useful exact reformulation is the 17-way perfect-code partition of
\(O_{16}\).  The strongest construction theorem nearby is asymptotic and has
an uninstantiated threshold; the strongest direct nonexistence results exclude
only odd-index or highly symmetric cases.
