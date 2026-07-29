# Triangle triples and the corrected third-moment shortening

Date: 2026-07-26.

Status: **exact conditional structure and exact closure of a false
third-moment obstruction; not a nonexistence proof for
\(S(14,15,31)\), and not a solution of Erdős--Rosenfeld Problem #835.**

The independent standard-library verifier is

```bash
python3 -B evidence/verify_s141531_triangle_third_moment.py
```

It reconstructs every number below from the design parameters.  No LP
solver or downloaded certificate is used.

## 1. The distinction that matters

Let \({\cal A}\) be a hypothetical \(S(14,15,31)\), let \(P\) be its
point--block incidence matrix over \(\mathbb F_2\), and let

\[
 C=\{c_S:S\subseteq X\},\qquad
 C_0=\{c_S:|S|\ {\rm even}\}.
\]

The full code \(C\) has dimension \(31\), while \(C_0\) has dimension
\(30\).  The already-audited weight enumerator of \(C\) gives
\(A_3(C^\perp)=0\).  This does **not** imply the same statement for
\(C_0\).

Indeed, a set of three block coordinates \(\{B_1,B_2,B_3\}\) is a
dual word of \(C_0\) precisely when

\[
 B_1\mathbin\triangle B_2\mathbin\triangle B_3
 \in E^\perp=\{\varnothing,X\},
 \tag{1}
\]

where \(E\) is the even-subset space of \(X\).  The symmetric
difference of three odd sets is odd, so the empty case is impossible.
Thus every weight-three dual word is exactly a **triangle triple**

\[
 B_1\mathbin\triangle B_2\mathbin\triangle B_3=X.
 \tag{2}
\]

For three \(15\)-sets, (2) forces every pairwise intersection to have
size \(7\); conversely, for blocks \(B_1,B_2\) meeting in seven points,
the only possible third block is
\((B_1\triangle B_2)^c\).

## 2. The exact global and local counts

The complete weight distribution of \(C_0\) is forced by the Steiner
parameters.  Its MacWilliams transform begins

\[
 (A_0^\perp,A_1^\perp,A_2^\perp,A_3^\perp,A_4^\perp)
 =
 (1,0,0,
 927\,696\,866\,625,
 3\,793\,226\,637\,448\,341\,180).
 \tag{3}
\]

Consequently, every hypothetical \(S(14,15,31)\) has exactly

\[
 \boxed{927\,696\,866\,625}
 \tag{4}
\]

unordered triangle triples.

There is also an exact local statement.  Fix a block \(B_0\).  Its
intersection distribution is

\[
\begin{split}
(n_0,\ldots,n_{15})={}&
(0,120,3360,49140,349440,1417416,3363360,\\
&4877730,4324320,2362360,768768,147420,14560,840,0,1).
\end{split}
\tag{5}
\]

This distribution determines the joint enumerator
\((\operatorname{wt}(c),c(B_0))\): away from the middle layer it is a
binomial count, and at size \(16\) the internal sets are complements
of blocks, whose parity against \(B_0\) is determined by (5).
Puncturing at \(B_0\) and applying MacWilliams gives

\[
 A_3\bigl((C_0\text{ punctured at }B_0)^\perp\bigr)
 =927\,696\,709\,200.
 \tag{6}
\]

The difference between (3) and (6) counts the triangle triples through
\(B_0\).  Hence every block lies in exactly

\[
 157\,425
 \tag{7}
\]

triangle triples.  Equivalently, among its \(4\,877\,730\) partners
meeting it in seven points, exactly

\[
 2\cdot157\,425=314\,850
 \tag{8}
\]

have the complementary symmetric difference as a block, while

\[
 4\,877\,730-314\,850=4\,562\,880
 \tag{9}
\]

do not.

In particular, the previously proposed universal triangle-closure law
at \(r=15\) cannot hold in a hypothetical design.  Universal closure
would produce

\[
 \frac{17\,678\,835\cdot4\,877\,730}{6}
 =14\,372\,097\,307\,425
 \tag{10}
\]

triangle triples, over fifteen times the forced count (4).

## 3. What happens in the dimension-two shortening

The forced affine-triple theorem supplies a two-dimensional even
subspace \(H\) with nonzero weights \(18,22,22\), whose point-column
multiplicities are \((0,9,9,13)\).  Let

\[
 Z_H=\{B\in{\cal A}:\langle B,h\rangle=0
                      \text{ for every }h\in H\}.
\]

The shortened code \(D=C_0|_{Z_H}\) has exact length \(4\,419\,003\)
and dimension \(28\).  A triangle triple from (2) survives whenever
all three blocks lie in \(Z_H\): because every \(h\in H\) is even,
\(\langle X,h\rangle=0\), so the three restricted column functionals
really do sum to zero.  Therefore \(A_3(D^\perp)\) is not forced to
vanish.

The exact coset inventory has \(57\) types.  For a type with external
base weight \(w_0\), middle capacity \(a\), and \(t\) actual
block-complements among those \(a\) middle translates, its shortened
weight and centered weight are

\[
 w=w_0-4096t,\qquad s=2w-4\,419\,003.
 \tag{11}
\]

Let \(y_{w_0,a,t}\) count cosets of that type.  Every actual design
satisfies:

- the \(57\) type-total equations;
- \(\sum t\,y=17\,678\,835\), since every block has one complementary
  \(16\)-set;
- \(\sum s\,y=0\); and
- \(\sum s^2y=2^{28}\cdot4\,419\,003\), since the shortened columns
  are nonzero and distinct.

Two static integer dual certificates, checked coefficient by
coefficient in the verifier, give

\[
-96\,749\,968\,713\,628\,778\,496
\ \leq\ \sum s^3y\ \leq\
-92\,587\,049\,516\,424\,757\,248.
\tag{12}
\]

For a binary \([n,28]\) code with no zero column,

\[
 \sum s^3=-6\cdot2^{28}A_3(D^\perp).
 \tag{13}
\]

Thus (12) is not a contradiction.  It proves the structural interval

\[
\boxed{
57\,485\,606\,222
\ \leq A_3(D^\perp)\leq\
60\,070\,286\,637.}
\tag{14}
\]

The exact calculation therefore says the opposite of the discarded
premise: the forced shortening must retain tens of billions of triangle
dependencies.

## 4. Scope

This audit:

- corrects the mistaken transfer of \(A_3^\perp=0\) from \(C\) to
  \(C_0\);
- gives exact global and per-block triangle counts;
- disproves universal triangle closure in every hypothetical
  \(S(14,15,31)\); and
- converts the dimension-two LP into the rigorous interval (14).

It does **not** construct or rule out \(S(14,15,31)\), does not rule
out \(k=16\) for Problem #835, and does not settle any other prime
case.
