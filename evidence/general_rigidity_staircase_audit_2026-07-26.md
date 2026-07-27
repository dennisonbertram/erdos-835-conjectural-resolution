# General rigidity and corrected staircase audit — 26 July 2026

## Scope

This checkpoint records conditional necessary theorems for a hypothetical
tight colouring and the audit corrections made before committing them.  It
does not contain a construction or a contradiction.  Erdős--Rosenfeld
Problem #835 remains open.

## Results retained after audit

1. **General \(H_1\) theorem.**  For every even \(k\) admitting a cover,
   \[
   \iota H_1\subseteq E_1\oplus E_{k-2}\oplus E_{k-1},
   \]
   with weights
   \[
   \frac1{k+1},\qquad \frac{2k-1}{3(k+1)},\qquad \frac13.
   \]
   Every fibre relation acts by a closed scalar.  The exact scalar-integrality
   criterion is a squarefree/base-\(p\)-digit condition; it is not equivalent
   to primality by the proof given.  The ordinary fibre indices separately
   recover the Ma--Tang composite exclusion.

2. **General \(H_2\) theorem.**  For every even \(k\ge6\) admitting a cover,
   \[
   \iota H_2\subseteq
   E_2\oplus E_{k-3}\oplus E_{k-2}\oplus E_{k-1},
   \]
   with weights
   \[
   \frac1{k+1},\qquad
   \frac{2k-3}{5(k+1)},\qquad
   \frac4{15},\qquad
   \frac13.
   \]
   The one-factorisation calculation proves
   \(RP_2=(k-2)(k-5)P_2/2\), and every fibre relation acts by a closed scalar.
   All resulting scalar divisibilities are automatic when \(k+1\) is prime.

3. **Staircase support at \(k=16\).**  For \(0\le a\le7\),
   \[
   \iota H_a\subseteq E_a\oplus E_{15-a}\oplus\cdots\oplus E_{15}.
   \]
   Combining this with \(N_aP_a=P_a/17\) supplies a certified family of
   compression relations and only the upper bound
   \[
   \dim {\cal J}P_a\le\max(1,a-1).
   \]
   Exact image rank is proved here only for \(a=1,2,3\), where it is
   \(1,1,2\).

4. **Automatic intersection.**  The fixed-block moments of every
   \(S(k-2,k-1,2k-1)\) force
   \[
   n_s=\frac{\binom{k-1}{s}}{k+1}
   \left(\binom{k}{s+1}+(-1)^{k-1-s}k\right).
   \]
   For even \(k\), \(n_0=0\).  Thus every \(S(14,15,31)\) is automatically
   intersecting, and the \(k=16\) cover is exactly an \(LS(14,15,31)\).

## Corrections caught before commit

The initial Opus staircase draft claimed
\(\dim{\cal J}P_a=a\).  This is false already at level two because
\(A_sP_2=a_sP_2\), so the image has rank one.  The corrected argument
distinguishes a support-derived upper bound from exact rank.

At level three the additional relation is
\[
A_{13}P_3=(R+372I)P_3.
\]
Consequently
\(\operatorname{tr}(P_3RA_{13})\) and
\(\operatorname{tr}(P_3A_{13}^2)\), initially called free, are forced.
The surviving second-order quantity is
\(\|P_3RP_3\|_F^2\).

The initial draft also called the within-fibre disjointness count \(d(B)\)
free.  Full Steiner moment inversion forces \(d(B)=n_0(B)=0\).  The
corrected note retracts the extra-intersecting-condition claim.

Finally, rational consistency and coordinate non-determinacy of a triple
profile equality system do not prove nonnegative integral feasibility.  The
corrected note leaves that question open.

## Independent verification run

The following checks were rerun locally:

```text
general H1:
  exact support, weights, relation formulas, design moments, and digit controls
  passed; Ruff passed

general H2:
  ALL 2,532,832 EXACT CHECKS PASSED
  Ruff check and format check passed

corrected Opus staircase:
  ALL 123 CHECKS PASSED
  includes exact elimination for thirteen 234-by-169 profile systems
  Ruff check and format check passed

Steiner automatic-intersection note:
  ALL 116 EXACT CHECKS PASSED
  Ruff check and format check passed
```

The long-running unrestricted/restricted SAT and CP-SAT searches had no
terminal verdict at this checkpoint.  Their continued execution is not
mathematical evidence for either existence or nonexistence.
