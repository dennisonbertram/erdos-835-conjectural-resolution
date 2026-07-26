# Elementary p-rank / Smith-form audit of S(14,15,31) and S(7,8,24)

Date: 2026-07-26.  Verifier: `verify_s141531_prank_snf_audit.py`
(deterministic, exact integer arithmetic; numpy only for mod-p integer
elimination; `--fast` skips the six large i=3 eliminations).
Status: **complete audit of the elementary modular tests explicitly listed
below; no obstruction; NOT a nonexistence proof and NOT a solution of #835.**

## 1. Parameters

S(14,15,31): b = 17 678 835, λ = (17678835, 8554275, 3991995, 1789515,
766935, 312455, 120175, 43263, 14421, 4389, 1197, 285, 57, 9, 1).
S(7,8,24): b = 43 263, λ = (43263, 14421, 4389, 1197, 285, 57, 9, 1).
Primes tested: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31 — and this list
is **provably exhaustive**: a prime dividing no Wilson diagonal entry
\(\binom{k-j}{i-j}\) gives the full-rank upper bound \(\binom vi\), so
no test can fire there; the verifier asserts every Wilson entry
factors inside the tested list.

## 2. Forced Gram spectra and the two sweep tests

For \(i\le\lfloor t/2\rfloor\), the i-set Gram \(N_iN_i^{\mathsf T}\)
has entries \(\lambda_{|S\cup T|}\); its exact eigenvalues
\(\theta_j\) (multiplicities \(m_j=\binom vj-\binom v{j-1}\)) are
certified by Eberlein second-orthogonality plus trace identities.
E.g. r=15, i=3: (814229325, 93054780, 7385300, 305900); i=7:
(278397405, 86612526, 24208470, 5925150, 1222650, 200070, 23166,
1430); S(7,8,24), i=3: (67032, 19152, 4104, 504).  Full tables for
every i are hardcoded and re-derived in the verifier.

Since \(N_i\) is a column submatrix of \(W_{i,k}(v)\), Wilson's
diagonal form (valid, \(v\ge k+i\)) gives
\(\operatorname{rank}_pN_i\le\operatorname{rank}_pW_{i,k}
=\sum_{p\nmid\binom{k-j}{i-j}}m_j\), and gcds of maximal minors give
the Cauchy–Binet test
\(\sum_jm_j\,v_p(\theta_j)\ \ge\ 2\sum_jm_j\,v_p\binom{k-j}{i-j}\).

The spectral count really is a lower bound even in non-semisimple
characteristic: reducing the characteristic polynomial gives
\(\prod_j(x-\theta_j)^{m_j}\), so the geometric multiplicity of zero
is at most its algebraic multiplicity
\(\sum_{p\mid\theta_j}m_j\).

**Result: over all i and all primes, neither the spectral lower bound
\(\sum_{p\nmid\theta_j}m_j\) ever exceeds the Wilson upper bound, nor
does the determinant test ever fail.**

## 3. Honest mod-p ranks (i ≤ 3)

The forced Gram's actual mod-p rank is a rigorous, design-independent
lower bound for \(\operatorname{rank}_pN_i\) — and is *not* captured
by eigenvalue counting (non-semisimple reduction).  All recorded
values, each asserted ≤ the Wilson bound:

| design | i | p=2 | p=3 | p=5 | p=7 | p=13 |
|---|---|---|---|---|---|---|
| r=15 | 1 | 1 | 0 | 0 | **31 = 31** | — |
| r=15 | 2 | 1 | 0 | 0 | **434 = 434** | — |
| r=15 | 3 | — | — | 0 | 464 ≤ 4464 | **4030 = 4030** |
| k=8 | 1 | 1 | 0 | **24 = 24** | **24 = 24** | — |
| k=8 | 2 | 1 | 0 | 24 | **252 = 252** | — |
| k=8 | 3 | 1 | 0 | — | 275 ≤ 2000 | — |

Bold = exact saturation: the design equations force the maximum p-rank
Wilson permits — zero slack, no contradiction.  Non-semisimple
witness: at (r=15, i=3, p=7) the honest rank 464 strictly exceeds the
optimistic eigenvalue count 434, so the honest computation was
necessary (and is the one the verifier reruns).

## 4. Chain squeeze — vacuous by scale

\(W_{i,t}N_t=\binom{k-i}{t-i}N_i\), so \(p\mid\binom{k-i}{t-i}\)
forces \(\operatorname{rank}_pN_t\le\binom vt-\operatorname{rank}_p
W_{i,t}\).  Minima: r=15: 145 422 675 (p=2), 195 892 564 (p=3),
240 851 988 (p=5), 259 923 345 (p=7), 265 155 555 (p=11),
265 182 091 (p=13) against \(\binom{31}{14}=265\,182\,525\); k=8:
245 157 (p=2), 313 974 (p=3), 344 356 (p=5), 346 081 (p=7) against
\(\binom{24}7=346\,104\).  Every forced *lower* bound used in this
audit lives below \(\binom v{\lfloor t/2\rfloor}\) = 2 629 575
(r=15) resp. 2 024 (k=8) — about \(55.3\times\) resp.
\(121.1\times\) below the best chain upper bound.  Thus this squeeze
does not close against the audited Gram-rank lower bounds; a genuinely
stronger lower bound is not excluded.

## 5. Two standard obstruction families (proved harmless here)

**(a) Bruck–Ryser–Chowla / rectangular Gram factorability.**  BRC applies to
**symmetric** 2-designs: its mechanism is squareness of \(N\)
(rational congruence of the square Gram via Hasse–Minkowski), not
intersection structure.  It is therefore not a theorem about these
non-symmetric designs.  The weaker necessary condition that the point
Gram admit an integral rectangular factorization also holds:
\(NN^{\mathsf T}=aI+cJ\)
with \((a,c)=(\lambda_1-\lambda_2,\lambda_2)\) always factorizes
integrally: pick 4-square representations \(a=|q_a|^2,c=|q_c|^2\)
(certificates: 4 562 280 = 2134²+88²+24²+2², 3 991 995 =
1997²+63²+4²+1²; 10 032 = 100²+4²+4²+0², 4 389 = 66²+5²+2²+2²), give
every point its own 4 columns holding \(q_a\) (disjoint supports ⟹
\(aI\)) plus 4 shared columns holding \(q_c\) (⟹ \(cJ\)): an explicit
\(X\in\mathbb Z^{v\times(4v+4)}\), \(4v+4\le b\), with
\(XX^{\mathsf T}=aI+cJ\), verified by direct multiplication.  Thus the
plain rectangular Gram-factorability test does not obstruct either
parameter set.  This says nothing about the required \(0/1\) entries,
prescribed row and column sums, higher incidence Grams, or other
structure not encoded by the point Gram alone.

**(b) Modular intersection (Frankl–Wilson-style) arguments — scoped.**
Two distinct forms with different verdicts:

- *The outright-contradiction family* (column Gram \(\equiv\)
  unit\(\cdot I\bmod p\), forcing \(\operatorname{rank}_p\ge b>\binom
  vi\)) requires \(p\nmid\binom ki\) and \(p\mid\binom ji\) for
  **every realized** intersection size j.  Both designs realize their
  full admissible spectrum (r=15: \(n_j>0\) for j = 1..13; k=8:
  \(n_j>0\) for j = 0..6 — forced distributions recomputed in the
  verifier).  This test is exhausted as follows.  If \(i\) is in the
  realized interval, \(j=i\) makes \(\binom ji=1\), so the divisibility
  hypothesis fails.  Below the interval, only \(i=0\) for the first
  design remains, and \(\binom j0=1\) again makes it fail.  Above the
  interval the off-diagonal divisibility can hold, but the required
  rank contradiction is already impossible:

  \[
  \begin{array}{c|cc}
  S(14,15,31)&b\le\binom{31}{14}=265\,182\,525&
                    b\le\binom{31}{15}=300\,540\,195\\
  S(7,8,24)&b\le\binom{24}{7}=346\,104&
                  b\le\binom{24}{8}=735\,471 .
  \end{array}
  \]

  These cases exhaust \(0\le i\le k\), so **this particular
  modular-rank contradiction family is closed exhaustively.**
- *The bound-form inequalities* (Ray-Chaudhuri–Wilson and
  Frankl–Wilson mod-p refinements) are **applicable but slack**, not
  vacuous: with s = number of realized intersection classes,
  \(b\le\binom vs\) reads \(17\,678\,835\le\binom{31}{13}=
  206\,253\,075\) and \(43\,263\le\binom{24}{7}=346\,104\)
  (verifier-checked).  In the standard residue-class formulation, the
  hypothesis that \(k\bmod p\) avoid the realized residues fails for
  every relevant prime through 13 (resp. 7) because the realized sizes
  form a full interval; the next prime is larger than \(k\), so it
  reproduces the same number of residue classes and the same slack
  bound.  We do **not** claim every polynomial-method variant is
  closed — only the
  divisibility-contradiction family (exhaustively) and the standard
  RW/FW bounds (numerically, with the stated slack).

Also: Wilson's diagonal form makes the integral system
\(W_{t,k}x=\mathbf 1\) solvable exactly when the \(\lambda_i\) are
integers (they are), so the SNF of the inclusion system yields nothing
beyond classical divisibility.

## 6. Scope — what is closed and what is not

Exhausted without contradiction by this audit: elementary p-rank
bounds (spectral, honest Gram, Wilson submatrix, chain),
determinant/minor divisibility, point-Gram factorability, and the
precisely stated Frankl–Wilson-style divisibility-contradiction family
— for both designs, all relevant primes — with the standard RW/FW
bound forms verified slack.  **Not
closed**: p-adic genus/lattice-theoretic analysis of the higher Grams,
Smith forms of Johnson-scheme idempotent lattices, and any argument
coupling modular structure to the 0/1 (nonnegativity) layer — those
remain open research directions, without precedent either way.

## 7. Literature correction

`s7824_literature_survey.md` calls the p-rank/SNF route "comparatively
unexplored".  As a statement about modular design exclusions in
general that is too strong, and the two precedent families should be
kept distinct because their hypotheses differ:
**Bruck–Ryser–Chowla** applies to *symmetric* 2-designs — its
mechanism is squareness of \(N\) (rational congruence of the square
Gram), and it is structurally void here because \(b\gg v\) and §5(a)
constructs the Gram factorization explicitly.
**Calderbank's** self-orthogonality exclusions apply to
*quasi-symmetric* designs — their mechanism needs **few intersection
classes** (two), and it is structurally void here because the designs
realize 13 resp. 7 classes.
The narrower historical statement supported by the survey is only
that it located no published example of a *Steiner system* excluded
by a p-rank/SNF argument; that is not a proof that no such example
exists.

## 8. Verdict

No contradiction occurs in any of the explicitly audited elementary
modular tests, and several are exactly saturated.  This closes those
tests, not modular theory as a whole and not the existence question:
**the existence of S(14,15,31) — and with it Erdős #835's first open
case k = 16 — remains open.**
