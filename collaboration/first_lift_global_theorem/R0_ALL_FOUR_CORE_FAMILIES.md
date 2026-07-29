# Exclusion of every four-core obstruction cover

Date: 2026-07-27.

## Theorem and scope

In the exceptional \(r=0\) profile, no family of exactly four distinct
size-ten obstruction cores can collectively account for all seven blocked
supports.

Equivalently, after the earlier type and reuse exclusions, any hypothetical
total obstruction must use at least five distinct cores.

This is a cover theorem, not a non-coexistence theorem.  Many four-core
unions satisfy the necessary graph conditions.  They fail because no
positive assignment of seven blocked supports fits the simultaneous
complement capacities, or because the few capacity survivors have a
common high-degree vertex that violates the exact complement-row identity.
Families of five or more distinct cores remain open.

## Complete type split

Use the abbreviations
\[
 A=K_{5,1,1,1},\quad B=K_{3,3,1,1},\quad
 C=K_{3,1,1,1,1},\quad D=K_6.
\]
There are 32 four-core type multisets whose individual reuse ceilings sum
to at least seven.

* The 17 rows containing \(B\) are excluded in
  `R0_FOUR_CORE_WITH_3311.md`.
* The all-\(D\) row is excluded in
  `R0_FOUR_K6_CLASSIFICATION.md`.
* The remaining fourteen rows are
  \[
  \begin{gathered}
  AAAA,\ AAAC,\ AAAD,\ AACC,\ AACD,\ AADD,\ ACCC,\\
  ACCD,\ ACDD,\ ADDD,\ CCCC,\ CCCD,\ CCDD,\ CDDD.
  \end{gathered} \tag{1}
  \]
  The exact generalized screen below excludes all fourteen.

## Generalized subset and row screen

Fix one core under \(S_{13}\), exhaust the compatible pools for the other
three cores, and retain only unions satisfying the 31-edge, maximum-degree,
minimum-degree-extension, and nine-vertex induced-capacity conditions.

For every retained union \(J\), enumerate every positive multiplicity
assignment
\[
 t_1+t_2+t_3+t_4=7
\]
within the individual type ceilings.  For all fifteen nonempty core
subfamilies \(I\), impose
\[
 3\sum_{i\in I}t_i\le
 36+2|K_I|-\sum_{v\in K_I}d_J(v)-q(J,K_I),
 \qquad K_I=\bigcap_{i\in I}C_i, \tag{2}
\]
with the forced completion-edge correction
\[
 q(J,K_I)=\max\left\{0,\,
 31-|E(J)|-
 \left(\binom{13-|K_I|}{2}-|E_J(V\setminus K_I)|\right)
 \right\}. \tag{3}
\]

Eleven rows in (1) have no multiplicity assignment satisfying (2).
The other three have capacity survivors, but every survivor has a vertex
\(v\) common to all four core supports with \(d_J(v)\ge6\).  Such a vertex
is in none of the seven complement triples assigned to the four cores.
It can occur in at most the three remaining complement five-sets, whereas
the exact row identity requires
\[
 d_F(v)-2\ge d_J(v)-2\ge4
\]
remaining complement occurrences.  This contradiction excludes every
survivor.

## Exact terminal counts

The number of four-core families reaching the final multiplicity test is
\[
\begin{array}{c|r@{\qquad}c|r}
AAAA&825&AAAC&14{,}136\\
AAAD&5{,}730&AACC&270{,}700\\
AACD&88{,}700&AADD&6{,}465\\
ACCC&326{,}815&ACCD&146{,}195\\
ACDD&19{,}065&ADDD&725\\
CCCC&1{,}522{,}958&CCCD&712{,}155\\
CCDD&100{,}308&CDDD&4{,}325
\end{array} \tag{4}
\]

The first eleven rows in the displayed order, through \(CCCC\), have zero
capacity-covering families.  The final three have respectively
\[
 648,\qquad288,\qquad396 \tag{5}
\]
capacity-covering families, all excluded by the common-row argument.

Together with the exact counts in the two companion notes, this exhausts
all 32 capacity-sufficient four-core type multisets.

## Reproduction

`verify_r0_four_core_capacity.py` reproduces any mixed row
deterministically and reports separately:

* families reaching the multiplicity test;
* families satisfying all fifteen subset inequalities;
* capacity survivors excluded by the common-row identity; and
* genuinely unresolved survivors.

For every row in (1), the final unresolved count is zero.
