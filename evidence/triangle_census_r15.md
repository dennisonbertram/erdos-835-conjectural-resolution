# Triangle census: independent confirmation, forced closure identity, and the localized LP no-go

Date: 2026-07-26.  Validator: `verify_triangle_census.py` (all checks
pass; fully independent code path from
`verify_s141531_triangle_third_moment.py`).  Companion to
`s141531_triangle_third_moment_audit.md`, which states the refutation
and the exact interval; this note records the independent replication
and three complements.

## 1. Independent confirmation (different formula, same numbers)

Computed via the all-subsets signed sum
\(6\cdot2^{2r+1}T=\sum_{S\subseteq X}(-1)^{|S|}F(S)^3\)
(equivalent to the even-only form by \(F(S^c)=-F(S)\); the signed
power-1 and power-2 sums vanish identically — no weight-1/2 dual
analogues):

- \(T(15)=A_3^\perp(C_0)=927\,696\,866\,625\); divisibility by
  \(6\cdot2^{31}\) passes.
- \(P_7\) by **two** independent routes: intra-distribution inversion
  (\(n_7=4\,877\,730\), \(P_7=b\,n_7/2\)) **and** the derived-design
  count \(\binom{31}{7}\cdot43263\cdot758/2\), both giving
  \(43\,116\,291\,922\,275\).
- Non-closing critical pairs: \(P_7-3T=40\,333\,201\,322\,400\)
  (93.55 %).

## 2. Closure at r=3,5 is parameter-forced, not just observed

The census formula gives \(T(3)=7\), \(T(5)=220\) from parameters
alone, and \(3T=P\) **exactly** (21, 660).  Since a critical pair has
at most one completion, \(3T=P\) already implies every critical pair
completes.  So full closure at \(r=3,5\) is forced by the parameters —
a second complete explanation alongside the \(N_0=2\) mechanism of
`triangle_closure_derived_reduction.md` — and the validator confirms
the actual designs (Fano: 7 triples, 21/21; \(S(4,5,11)\): 220,
660/660) against the forced values.  The general-\(r\) forced census
(with layers \(r,r+1\) split by \(|A|=b\) alone) supplies new
necessary conditions at any odd \(r\): integrality of
\(T\), \(T\ge0\), and \(3T\le P\).

## 3. Localized first-order counting could never have decided this

Exact rational LP with verified certificates
(`verify_ambient_moment_lp.py`; derived-level in
`verify_derived_closure_lp.py`, now vendored so both run from this
directory):

- The complete mixed-moment system of the derived \(S(7,8,24)\)
  (45 cells, rank 41, dim 4) admits an exact nonnegative solution with
  the closing block absent — verified against all 36 moment equations.
- The complete **ambient** 4-cell system of \(S(14,15,31)\) over
  \(I\sqcup S_1\sqcup S_2\sqcup W\) (480 cells, 2472 moment
  identities, rank 434, dim 10; the derived system is its
  \(p=7\) subsystem) admits an exact nonnegative **integral** solution
  with \(z=0\) and a rational one with \(z=1\); the r=5 control is
  equality-infeasible at \(z=0\) (there the ambient rank is full and
  \(z\) is forced to 1 — closure proved by counting alone), and r=9 is
  feasible both ways.

So closure and its failure are invisible to every counting argument
localized to one configuration: the census decides globally, through
the only unforced global datum \(|A|=b\).  This also retro-explains the
LP verdict pattern: forcing exists exactly where closure is
parameter-forced (\(r=5\)), and nowhere else.

## 4. Status of the localized count \(A_3(Z_H)\)

Not forced (see `s141531_triangle_third_moment_audit.md` §3).  The exact
rational certification has since completed and supersedes the float
estimate: two static integer dual certificates give

\[
 57\,485\,606\,222\ \le\ A_3(D^\perp)\ \le\ 60\,070\,286\,637 .
\]

The uniform syndrome value \(A_3/16=57\,981\,054\,164\) lies strictly
inside that interval, so the localized count is consistent with the
naive estimate and the route yields no contradiction.  (The earlier
float-derived lower bound \(\approx5.7485576\times10^{10}\) was a
five-significant-figure rounding artifact and should not be quoted; the
exact endpoints come from dividing the certified \(\sum s^3\) bounds by
\(6\cdot2^{28}\) and rounding inward.)

## Scope

Conditional on the existence of an \(S(14,15,31)\) throughout; no
bearing on #835 beyond killing the universal-closure proof route and
adding the forced census as a new exact structure.
