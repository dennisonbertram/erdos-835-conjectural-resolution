# An actual-edge \(K_{18}\) obstructs the two-statistic \(F_{32}\) formula

This note closes one concrete positive-construction route for \(k=16\).
It is an exact finite obstruction, not merely a failed heuristic search.

Let
\[
 F=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1).
\]
For a \(16\)-set \(S\subset F\), write
\[
 a(S)=e_1(S),\qquad
 \lambda(S)=e_8(S)+e_1(S)^8. \tag{1}
\]
Consider the quotient graph whose formal vertices are the \(1024\) pairs
\((a,\lambda)\in F^2\), joining two pairs when they are realized by adjacent
\(16\)-sets.  Here adjacency means intersection size \(15\), as in
\(J(32,16)\).

## Theorem

The actual-edge quotient graph for (1) contains a \(K_{18}\).  Consequently
there is no proper \(17\)-colouring of \(J(32,16)\) of the form
\[
 c(S)=G\bigl(e_1(S),e_8(S)+e_1(S)^8\bigr) \tag{2}
\]
for any function \(G:F^2\to\{1,\ldots,17\}\).

## Certificate

Start with
\[
 B=\{0,1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30\}. \tag{3}
\]
This is the \(\lambda=1\) trace-hyperplane \(17\)-set from the
coefficient-eight classification:
\[
 B=\{0\}\cup\{x\in F:\operatorname {Tr}(x)=1\}.
\]
For every \(a\in B\), direct expansion of
\(\prod_{x\in B\setminus\{a\}}(1+xt)\) through degree eight gives
\[
 \bigl(a(B\setminus\{a\}),\lambda(B\setminus\{a\})\bigr)=(a,1). \tag{4}
\]
The seventeen sets obtained by deleting one point from \(B\) are pairwise
adjacent.  Thus
\[
 {\cal K}_{17}=\{(a,1):a\in B\} \tag{5}
\]
is an actual-edge \(K_{17}\).

One more quotient vertex,
\[
 v=(29,27), \tag{6}
\]
is adjacent to every vertex in (5).  The following table is the complete
finite certificate.  A hexadecimal mask \(m\) encodes the \(17\)-set
\[
 R(m)=\{j\in\{0,\ldots,31\}:\text{bit }j\text{ of }m\text{ is }1\}.
\]
In the row indexed by \(a\), deleting \(x\) from \(R(m)\) gives statistic
\((a,1)\), while deleting \(y\) gives statistic \(v\).

| \(a\) | mask \(m\) | \(x\) | \(y\) |
|---:|:---:|---:|---:|
| 0 | `0x7913db25` | 9 | 20 |
| 1 | `0xa3b106bf` | 1 | 29 |
| 3 | `0xd197f846` | 24 | 6 |
| 5 | `0xa62abb4e` | 17 | 9 |
| 7 | `0x61769bb8` | 4 | 30 |
| 8 | `0xe6c12dbc` | 5 | 16 |
| 10 | `0xe74526da` | 16 | 7 |
| 12 | `0x2d8da91f` | 11 | 26 |
| 14 | `0x014bf9bd` | 22 | 5 |
| 17 | `0xd12fd05e` | 14 | 2 |
| 19 | `0x29baa4bb` | 21 | 27 |
| 21 | `0xec927533` | 23 | 31 |
| 23 | `0xcde2d662` | 6 | 12 |
| 24 | `0x6f032d5d` | 29 | 24 |
| 26 | `0x014bf9bd` | 2 | 5 |
| 28 | `0xf7513256` | 28 | 29 |
| 30 | `0x42e9c8f7` | 7 | 4 |

Every mask has exactly seventeen set bits.  In every row the two indicated
deletions therefore produce \(16\)-sets with a common \(15\)-set, and hence
an actual Johnson edge.  Expanding their elementary-symmetric generating
polynomials gives the two claimed statistic pairs.  These seventeen edges,
together with the \(136\) edges inside (5), give all
\(\binom{18}{2}=153\) edges of a \(K_{18}\).

The pigeonhole principle now proves the theorem: a map \(G\) with only
seventeen values must identify two vertices of this \(K_{18}\), and the
corresponding adjacent \(16\)-sets then receive the same colour in (2).

## Reproducibility and scope

The certificate was found by deterministic sampling of \(17\)-sets and
extension of the known trace-hyperplane \(K_{17}\):

```bash
python3 -B evidence/f32_two_statistic_k18_search.py \
  --trace-extension 1 --seed 836 --samples 5000 --batch 5000 --compact
```

The search is not part of the proof.  The independent checker contains the
static masks above, uses a separate polynomial long-division implementation
of \(F_{32}\) multiplication, recomputes every \(e_1\) and \(e_8\) directly
from each \(16\)-set, and checks all \(153\) actual Johnson edges:

```bash
python3 -B evidence/f32_two_statistic_k18_verifier.py
```

This rules out **every** arbitrary postprocessing of the two statistics in
(1), not just the earlier canonical trace rule.  It does not rule out a
formula using more coefficient information, and it does not prove that a
tight \(17\)-colouring of \(J(32,16)\) is impossible.  In particular, it is
not by itself a resolution of Erdős--Rosenfeld Problem #835.
