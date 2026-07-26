# Complete pair-difference regularity of S(14,15,31)

Date: 2026-07-26.  Validator: `verify_pair_difference_regularity.py`
(all checks pass).  Status: **exact theorem about every hypothetical
\(S(14,15,31)\); not a nonexistence proof and not a solution of #835.**

## Theorem

For every even \(D\subseteq X\), the number \(m_D\) of unordered block
pairs with \(B_1\Delta B_2=D\) depends only on \(|D|\) — refined at
\(|D|=16\) by whether \(D^c\) is a block:

| \(|D|\) | 4 | 6 | 8 | 10 | 12 | 14 | 16 int | 16 ext |
|---|---|---|---|---|---|---|---|---|
| \(m_D\) | 235980 | 174800 | 165186 | 153216 | 147972 | 144144 | **157425** | **142590** |

with \(m_D=m_{32-|D|}\) for \(18\le|D|\le28\) and layers \(2,30\)
empty.  In particular **every** even set of size \(4\le|D|\le28\) is a
block-pair difference, in an exactly forced number of ways.

## Proof (three forced ingredients + convexity)

1. \(3A_4=\sum_D\binom{m_D}2\): a weight-4 dual word of the even code
   (= block 4-subset with XOR 0; the all-ones case is parity-impossible
   for four odd sets, so this count is the same for the full and even
   codes) splits into equal-difference pairs in exactly 3 ways, and two
   equal-difference pairs cannot share a block.  \(A_4\) is forced:
   \(A_4=\bigl(2^{-31}\sum_S F(S)^4-b-3b(b-1)\bigr)/24
   =3\,793\,226\,637\,448\,341\,180\), matching the MacWilliams table
   of `s141531_incidence_code_audit.md` (8).
2. Layer totals \(\sum_{|D|=d}m_D=b\,n_j/2\) are forced (intra
   distribution), the internal-16 values are forced **individually**
   (\(m_{B^c}=157425\), the per-block triangle count of
   `s141531_triangle_third_moment_audit.md`), and every layer average
   is an integer.
3. The uniform assignment already achieves
   \(\sum_D\binom{m_D}2=3A_4=11\,379\,679\,912\,345\,023\,540\)
   **exactly**; strict convexity of \(\binom m2\) makes any deviation
   strictly larger, so equality forces uniformity.  \(\square\)

## Group-ring form and consistency

With \(A=\sum_Bx^{1_B}\in\mathbb Z[\mathbb Z_2^{31}]\),
\(\bar x=x^{1_X}\), \(\delta=157425-142590=14835\):
\[
 A^2=b+2\sum_dq_dK_d+2\delta\,\bar xA,
 \qquad\text{i.e.}\qquad
 (A-\delta\bar x)^2=E\ \text{forced},
\]
verified at **every** character: \(F(S)^2=b+2\sum_Dm_D(-1)^{|D\cap S|}\)
for all 32 size classes, including both middle splits (Vieta at
15/16: root sum \(\mp2\delta\), roots \(\{1549,-31219\}\) and
\(\{-1549,31219\}\)).  The sought group-ring/character contradiction
does **not** occur: the identity is exactly self-consistent.  Verdict
per the audit request: **complete regularity, no contradiction at this
level.**

## The family picture (controls)

The actual designs satisfy the same statement: \(r=3\): layer 4 =
internal 3 / external 0; \(r=5\): layer 4 all 3, layer 6 internal 10 /
external 0, layer 8 all 3.  **External middle value \(=0\) is exactly
full triangle closure** — true at \(r=3,5\), while \(r=15\) has
external value \(142590>0\): the regularity theorem contains the
closure refutation as its middle-layer entry and quantifies it
per-set: every non-block-complement 16-set is the difference of
exactly \(142\,590\) critical pairs.

## New levers this opens

- Per-set localization: for every 4-set \(D\), exactly \(471\,960\)
  blocks \(B\) satisfy \(|B\cap D|=2\) and \(B\Delta D\in A\)
  (\(=2q_4\)); analogues at every layer — strong local constraints for
  future structure/SAT attacks.
- Next identities up: \(A_5\) (5-subsets with XOR \(=1_X\)) and
  \(A_6\) couple \(m_D\) to the triple-difference distribution
  \(t_D\); an LTS-style over-determination hunt at the quintic level
  is the natural continuation.
- The \(\binom{v}{k}=17b\) dichotomy and the Delsarte tail
  \(B=(1,0,\dots,0,16)\) hold across the whole derived tower
  (S(7,8,24), S(6,7,23), S(5,6,22), S(4,5,21)) — see the tower sweep
  note.

## Scope

Conditional structure of a hypothetical design; no contradiction
found; nothing here bears on #835 beyond adding forced structure.
