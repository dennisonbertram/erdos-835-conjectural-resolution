# Triangle-closure law for boundary Steiner systems

Date: 2026-07-25.  Validator: `verify_boundary_coset_cells.py`
(exhaustive at \(r=3\) and \(r=5\), <1 s).  Labels: PROVED /
FINITE-VERIFIED / CONJECTURAL as marked.

## Setting

\(A\) an \(S(r-1,r,2r+1)\), \(D=\{B^c:B\in A\}\) the block-complement
family, \(F(U)=\sum_{B\in A}(-1)^{|B\cap U|}\).

## PROVED structure (audited)

- \(F\) is constant on \(|U|\le r-1\); at \(|U|=r,r+1\) it is exactly
  two-valued, affine in the \(D\)-indicator with gap \(2^r\)
  (calibrated: \(7\) vs \(-1\) at \(r=3\); \(26\) vs \(-6\) at
  \(r=5\)).  Every 15/16-window distribution of a hypothetical
  \(S(14,15,31)\) is affine in \(1_D\) (moment count: one free
  parameter), and the 16-sets of \([31]\) partition exactly into the
  block shadow (16b sets, one block each) and \(D\) (b sets):
  \(17b=\binom{31}{16}\).
- Coset cells \((b\pm F(U_1)\pm F(U_2)\pm F(U_1\Delta U_2))/4\) are
  nonnegative integers in all exhaustive instances (min cell 0 at
  \(r=3\), 4 at \(r=5\)).
- The ONLY pairwise-undetermined combination is
  \(U_1,U_2\notin D\), \(|U_1\Delta U_2|=r+1\): there
  \(F(U_1\Delta U_2)\) genuinely depends on triple information (splits
  42/168 at \(r=3\), 5\,940/27\,720 at \(r=5\)).

## The laws (FINITE-VERIFIED exhaustively; CONJECTURAL beyond)

Since complementation cancels in symmetric differences, these are
block statements:

- **Triangle closure.**  If \(|B_1\cap B_2|=(r-1)/2\), then
  \((B_1\Delta B_2)^c=(B_1\cap B_2)\cup(B_1\cup B_2)^c\) is a block.
  Verified 21/21 pairs at \(r=3\) (the classical Fano pencil closure)
  and 660/660 at \(r=5\).  PROVED not to follow from pairwise
  intersection bounds alone (an interloper block would meet \(B_1\) in
  \((r\pm1)/2\) points, both admissible): the law is genuinely triple.
- **Mixed exclusion.**  \(U_1\in D\), \(U_2\notin D\),
  \(|U_1\Delta U_2|=r+1\) forces \(U_1\Delta U_2\notin D\)
  (84/84 and 11\,880/11\,880).

## Why it matters

These are exactly the "joint constraints on which complementary
15-sets can simultaneously be blocks" that the endpoint no-gos leave
open.  If triangle closure holds at \(r=15\), it forces
\(D\)-membership deterministically from pairs at the
\(|B_1\cap B_2|=7\) layer and feeds the exact-\(B(Q)\) coupling that
the shortening routes lack.  Open: prove or refute at general odd
\(r\); the two verified scales are unique designs with large groups,
so accidental rigidity is a live possibility.  Status at \(r=15\):
CONJECTURAL.
