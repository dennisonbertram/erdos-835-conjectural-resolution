# Forced affine triples in a hypothetical \(S(14,15,31)\)

Date: 2026-07-26.

Status: **exact nonlinear middle-layer result and exact closure of the
best dimension-two shortening candidate; not a nonexistence proof for
\(S(14,15,31)\), and not a solution of Erdős--Rosenfeld Problem 835.**

The standard-library verifier is

```bash
python3 -B evidence/verify_s141531_affine_triple_forcing.py
```

It checks a static rational dual certificate, the fixed-block
intersection distribution, the affine translation, and all shortened-code
arithmetic.  The companion script
`explore_s141531_pair_profile_lp.py` explains how the certificate was
discovered; its floating-point output is not used in the proof.

## 1. The forced three-block profile

Assume that \({\cal A}\) is an \(S(14,15,31)\) on \(X\).  Fix blocks
\(B_1,B_2\in{\cal A}\) with

\[
 |B_1\cap B_2|=6.
\]

Partition \(X\) into

\[
\begin{aligned}
 I&=B_1\cap B_2, & |I|&=6,\\
 U&=B_1\setminus B_2, & |U|&=9,\\
 V&=B_2\setminus B_1, & |V|&=9,\\
 W&=X\setminus(B_1\cup B_2), & |W|&=7.
\end{aligned}
\tag{1}
\]

For a block \(B\), its profile is

\[
 \rho(B)=(|B\cap I|,|B\cap U|,|B\cap V|,|B\cap W|).
\]

Let \(N_x\) count the blocks with profile \(x=(a,b,c,d)\).  The target
profile is

\[
 x_*=(0,4,4,7).                                      \tag{2}
\]

Every target block \(B_3\) satisfies

\[
\begin{aligned}
 |B_1\cap B_3|&=4,\\
 |B_2\cap B_3|&=4,\\
 B_1\cap B_2\cap B_3&=\varnothing,\\
 B_1\cup B_2\cup B_3&=X.
\end{aligned}
\tag{3}
\]

The following bound is the new exact result.

> **Affine-triple forcing theorem.**  For every pair \(B_1,B_2\) as
> above,
> \[
> N_{(0,4,4,7)}\geq666.                              \tag{4}
> \]

### Proof

Let \(m=(i,j,k,l)\) be a profile of a \(14\)-subset, so
\(i+j+k+l=14\) and \(m\leq(6,9,9,7)\) coordinatewise.  Counting
incidences between actual \(14\)-subsets of profile \(m\) and their
unique containing design blocks gives

\[
 \sum_x
   \binom ai\binom bj\binom ck\binom dl\,N_x
 =
 \binom6i\binom9j\binom9k\binom7l.                   \tag{5}
\]

The two fixed profiles \((6,9,0,0)\) and \((6,0,9,0)\) each occur once.
Every other profile meeting either fixed block in at least fourteen
points occurs zero times, because two distinct blocks in a Steiner
\(S(14,15,31)\) cannot share a \(14\)-subset.  Move these fixed terms
out of (5), and call the remaining nonnegative variables *live*.

The certificate contains rational numbers \(y_m\) on 396 of the 406
facet profiles.  Exact arithmetic verifies

\[
 \sum_m y_m r_m=666,                                 \tag{6}
\]

where \(r_m\) is the right side of (5) after removing the two fixed
blocks, and, for every live block profile \(x\),

\[
 \sum_m y_m
   \binom{x_1}{m_1}\binom{x_2}{m_2}
   \binom{x_3}{m_3}\binom{x_4}{m_4}
 \leq {\bf1}_{\{x=x_*\}}.                            \tag{7}
\]

Multiply (5) by \(y_m\), sum over \(m\), use (7), and use
\(N_x\geq0\).  The result is

\[
 666
 \leq\sum_x N_x{\bf1}_{\{x=x_*\}}
 =N_{x_*},
\]

which proves (4).  The decoded certificate has SHA-256

```text
dc904285cac5b121f09553a930fb213a764bf31e216780e463491db43047fdef
```

and the verifier checks every rational coefficient and every one of the
410 live-profile inequalities.  Thus the floating-point search that
found the dual is absent from the proof. \(\square\)

Only the degree-\(14\) equations are needed.  They imply all lower
factorial moments by summing over the \(14\)-subsets containing any
fixed smaller subset.

## 2. Such pairs are forced

For a fixed block \(B_1\), let \(n_s\) count blocks meeting it in \(s\)
points, including \(n_{15}=1\).  The design parameters give

\[
 \sum_{s=j}^{15}\binom{s}{j}n_s
 =\binom{15}{j}\lambda_j
 \qquad(0\leq j\leq14),                              \tag{8}
\]

where

\[
 \lambda_j=\frac{\binom{31-j}{14-j}}{15-j}.
\]

Descending binomial inversion gives

\[
\begin{split}
(n_0,\ldots,n_{15})={}&
(0,120,3360,49140,349440,1417416,3363360,\\
&4877730,4324320,2362360,768768,147420,14560,840,0,1).
\end{split}
\tag{9}
\]

In particular, every block has \(3\,363\,360\) partners meeting it in
six points.  Combining (4) and (9), every hypothetical design contains
at least

\[
 \frac{17\,678\,835\cdot3\,363\,360}{2}\cdot666
 =
 19\,800\,275\,399\,704\,800                         \tag{10}
\]
unordered triples satisfying (3).  There is no overcount in (10):
within such a triple, exactly one pair has intersection six and the
other two pairs have intersection four.

## 3. Translation to an affine two-flat

Put \(D_i=X\setminus B_i\) for a triple satisfying (3), and set

\[
 q=D_1\mathbin\triangle D_2\mathbin\triangle D_3,
\qquad
 H=\langle D_1\mathbin\triangle D_2,\,
          D_1\mathbin\triangle D_3\rangle_{\mathbb F_2}.
\tag{11}
\]

Then

\[
 q+H=\{q,D_1,D_2,D_3\}.                              \tag{12}
\]

The three nonzero weights in \(H\) are

\[
 18,\ 22,\ 22,                                       \tag{13}
\]

and the four weights in \(q+H\) are

\[
 14,\ 16,\ 16,\ 16.                                  \tag{14}
\]

Up to a change of basis in \(H\), the four column multiplicities of
\(H\) on the 31 points are

\[
 (0,9,9,13),                                         \tag{15}
\]

and the corresponding profile of \(q\) is

\[
 (0,4,4,6).                                          \tag{16}
\]

These are exactly the best subspace and lower-weight coset found in the
exhaustive dimension-two endpoint audit.

## 4. The best dimension-two shortening is exact

Let \(C_0\) be the \(30\)-dimensional even point-incidence code of
\({\cal A}\), and shorten it to the coordinates on which every word of
\(H\) vanishes.  Character orthogonality and (13) give the exact length

\[
 n_H=4\,419\,003.                                    \tag{17}
\]

The original minimum distance is \(8\,809\,920\).  The removed
coordinate set has size \(13\,259\,832\), while

\[
 G_2(8\,809\,920,3)>13\,259\,832.
\]

Therefore the shortening kernel has dimension at most two; since it
contains \(H\), it is exactly \(H\), and the shortened image has
dimension \(28\).

An exhaustive exact profile calculation gives the safe lower bound

\[
 d_H\geq2\,197\,848.                                 \tag{18}
\]

The only uncertainty in that calculation occurs at weight sixteen.
Equations (4), (12), and (14) now show that three actual block complements
occur simultaneously in such a minimizing coset.  Hence all three upper
Fourier endpoints in (18) are attained together, producing an actual
word of weight \(2\,197\,848\).  Consequently

\[
 \boxed{C_0|_{Z_H}\text{ has exact parameters }
 [4\,419\,003,28,2\,197\,848].}                       \tag{19}
\]

Its binary Griesmer sum is

\[
 G_2(2\,197\,848,28)=4\,395\,712,
\]

leaving exact slack

\[
 4\,419\,003-4\,395\,712=23\,291.                    \tag{20}
\]

Thus higher-order coupling of the three middle-layer indicators cannot
improve the numerically best dimension-two shortening: that endpoint is
realized in every hypothetical design, many times over.

## 5. Scope

This result uses a genuinely nonlinear joint block-indicator condition,
but it confirms feasibility rather than producing a contradiction.  It
proves:

- the exact lower bound (4);
- abundant affine two-flats with three block complements;
- simultaneous attainment of the three unresolved endpoints in the
  best dimension-two shortening; and
- the exact shortened-code parameters (19).

It does **not** prove that \(S(14,15,31)\) exists, rule it out, or settle
the full large-set problem.  Other shortening subspaces, higher affine
dimensions, stronger code bounds, and compatibility among different
colour classes remain open.
