# Exhaustive dimension-two incidence-code shortening audit

Date: 2026-07-26.

Status: **exact no-go result for this particular shortening
strategy; not a nonexistence proof for \(S(14,15,31)\), and not a
solution of Erdős--Rosenfeld Problem 835**.

The verifier is

```bash
python3 -B evidence/verify_s141531_dim2_subcodes.py
```

Its SHA-256 is

```text
1d9a337582b01bcf5c41e0769564518f69374757dbfc11182fb8f0435522716c
```

The verifier's deterministic stream of all 1,450 labelled
dimension-two profile summaries has SHA-256

```text
f963ed6e72aa544385592c3c7379b8c99e3358960e626c54d42c986dd417a639
```

The latter digest is recomputed and checked on every run.

## 1. Fourier bounds and the shortened code

Assume that \(A\) is an \(S(14,15,31)\), and let \(C_0\) be the
30-dimensional even subcode of its binary point-incidence code.  For a
point subset \(S\), put

\[
 F(S)=\sum_{B\in A}(-1)^{|B\cap S|}.
\]

For every even \(|S|\ne16\), the design equations force \(F(S)\) from
\(|S|\) alone.  At size 16 there are two possibilities:

\[
 F_{\rm ext}(16)
 \ \leq\ F(S)\ \leq\
 F_{\rm ext}(16)+2^{15}.
\tag{1}
\]

The upper endpoint occurs exactly when the complementary 15-set is a
block.  This size-16 correction is essential when deriving a lower
bound for a shortened word.

Let \(H\leq C_0\), and let \(Z_H\) be the design blocks on which every
word of \(H\) is zero.  Character orthogonality gives

\[
 |Z_H|=\frac1{|H|}\sum_{h\in H}F(h),
\tag{2}
\]

and, for a coset \(c+H\),

\[
 \operatorname{wt}_{Z_H}(c+H)
 =\frac{\sum_{h\in H}F(h)-\sum_{h\in H}F(c+h)}
        {2|H|}.
\tag{3}
\]

In (2)--(3), replacing each numerator contribution by the appropriate
endpoint of (1) gives rigorous lower and upper bounds even though the
different size-16 events need not be simultaneously attainable.

The kernel of \(C_0\to C_0|_{Z_H}\) contains \(H\), but need not equal
\(H\) a priori.  If \(R=|A|-|Z_H|\), this kernel is a binary code of
length \(R\) and minimum distance at least

\[
 d(C_0)=8\,809\,920.
\]

The verifier therefore uses the Griesmer bound on the deleted
coordinates to obtain a rigorous upper bound on the kernel dimension,
and only then obtains a lower bound on the image dimension.

## 2. Exhaustive classification for \(\dim H=2\)

Choose a basis of \(H\).  Each of the 31 points has one of the four
column labels \(v\in\mathbb F_2^2\).  Write \(n_v\) for their
multiplicities.  A labelled tuple

\[
 (n_0,n_1,n_2,n_3),\qquad \sum_v n_v=31,
\]

defines a two-dimensional even subcode exactly when

\[
 n_1+n_3\equiv n_2+n_3\equiv0\pmod2
\]

and the positive nonzero column labels span \(\mathbb F_2^2\).
Conversely, every two-dimensional \(H\leq C_0\) has such a tuple.
The verifier retains the redundancy under
\(\operatorname{GL}(2,2)\); it checks all 1,450 valid labelled tuples.

For fixed \(n=(n_v)\), a point subset \(c\) is classified by

\[
 0\leq c_v\leq n_v.
\]

The verifier enumerates every profile with even \(\sum_v c_v\), except
the four profiles belonging to \(H\).  For each \(a\in\mathbb F_2^2\),
the translate has size

\[
 |c+h_a|
 =\sum_{a\cdot v=0}c_v
  +\sum_{a\cdot v=1}(n_v-c_v).
\tag{4}
\]

Thus (4) and the four multiplicities contain all data needed in
(2)--(3).  In total, the verifier checks 1,567,276 profile
representatives.  It deliberately counts the redundant representatives
of a coset; this avoids making any hidden orbit-size assumption.

There is no positive Griesmer margin.  The best margin is

\[
 G(d_{\rm lower},k_{\rm lower})-|Z_H|_{\rm upper}
 =-23\,291.
\]

One labelled best profile is

\[
 n=(0,9,9,13),\qquad
 (|h|:h\in H)=(0,22,22,18).
\]

For this profile, the length is exact:

\[
 |Z_H|=4\,419\,003,\qquad
 R=13\,259\,832.
\]

The deleted-coordinate Griesmer calculation proves that the kernel has
dimension exactly 2, so the image has dimension 28.  Exhaustive coset
enumeration gives

\[
 d_{\rm short}\geq2\,197\,848.
\]

The minimizing lower-bound profile has translate sizes

\[
 (14,16,16,16).
\]

Because its three size-16 upper endpoints need not be jointly
attainable, this is only a lower bound.  An actual coset avoiding the
middle layer has translate sizes

\[
 (14,12,8,28)
\]

and proves

\[
 d_{\rm short}\leq2\,201\,720.
\]

At the rigorous lower endpoint,

\[
 G(2\,197\,848,28)=4\,395\,712
 <4\,419\,003.
\]

Therefore no dimension-two shortening of this form yields a Griesmer
contradiction using the forced Fourier information.

## 3. Dimension three is not exhaustive

A separate random search suggested two dimension-three column
profiles.  The verifier exhausts all coset profiles for each of those
two fixed choices, but **does not enumerate all dimension-three
subcodes**.

For

\[
 (10,1,2,4,6,2,1,5)
\]

it checks 41,572 profile representatives and obtains Griesmer margin
\(-26\,669\).  For

\[
 (1,3,5,2,3,2,4,11)
\]

it checks 51,832 profile representatives and obtains margin
\(-23\,291\).  These computations rule out only these selected
profiles as sources of the desired contradiction.  They do not justify
any universal dimension-three claim.

## 4. Scope

The exhaustive conclusion is narrow:

> Under the safe size-16 Fourier bounds, no two-dimensional even
> point-subcode gives a Griesmer contradiction after puncturing to its
> common-zero coordinates.

It does not exclude higher-dimensional subcodes, sharper joint
constraints on which 15-sets are blocks, a different coding-theoretic
bound, or the design itself.
