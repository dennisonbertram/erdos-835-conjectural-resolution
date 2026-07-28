# Six or seven cores with exactly two non-\(K_6\) cores

Date: 2026-07-28.

## Result and scope

In the exceptional \(r=0\) profile, neither six nor seven distinct cores
can collectively account for all seven blocked size-ten supports when
exactly two cores are not \(K_6\)'s.

Write
\[
 A=K_{5,1,1,1},\quad B=K_{3,3,1,1},\quad
 C=K_{3,1,1,1,1},\quad D=K_6.
\]
This note treats all six unordered exceptional-type pairs
\[
 AA,\ AB,\ AC,\ BB,\ BC,\ CC,
\]
with four \(D\)-cores in the six-core case or five in the seven-core
case.  Families with at least three non-\(K_6\) cores remain open.

## Exact union table

Fix the first exceptional core under \(S_{13}\), select exactly one core
of the second exceptional type, and select the required distinct
\(D\)-cores.  Under only
\[
 |E(J)|\le31,\qquad \Delta(J)\le7,
\]
the complete list of feasible support-union orders and minimum union edge
counts is
\[
\begin{array}{c|c|c}
\text{exceptional pair}&|W|&\min |E(J)|\\ \hline
AA&8&25\\
AA&9&27\\
AB&8&26\\
AC&8&24\\
AC&9&28\\
BB&8&26\\
BC&8&26\\
CC&7&21\\
CC&8&25
\end{array} \tag{1}
\]
The table is identical for six and seven total cores.  Every unlisted
union order is infeasible under the displayed graph bounds.

## Union row-rank exclusion

Let \(t_i\) be the assigned multiplicities.  They sum to seven.  In the
six-core case exactly one core is doubled; the \(B\)-core, whose reuse
ceiling is one, is not eligible.

For \(W\), the union of all core supports, the complement-row identity
gives demand at least
\[
 2|E(J)|-2|W|. \tag{2}
\]
The three complement five-sets supply at most fifteen incidences in
\(W\).  A triple assigned to core support \(C_i\) supplies at most
\[
 \min\{3,|W|-|C_i|\}
\]
incidences in \(W\).  Maximizing over the eligible doubled-core choice
gives:
\[
\begin{array}{c|c|c|c}
\text{pair}&|W|&\text{demand from (2)}
 &15+\max\text{ triple incidences}\\ \hline
AA&8&34&25\\
AA&9&36&32\\
AB&8&36&25\\
AC&8&32&26\\
AC&9&38&33\\
BB&8&36&25\\
BC&8&36&26\\
CC&7&28&20\\
CC&8&34&27
\end{array} \tag{3}
\]
Every row is a strict contradiction.  The same upper bounds apply to the
seven-core all-singleton multiplicity assignment.

Thus no six- or seven-core total obstruction has exactly two
non-\(K_6\) cores.

## Reproduction

`verify_r0_six_seven_two_exceptional.py` rebuilds all six fixed-first
candidate pools, solves every fixed-\(|W|\) finite optimization, checks
the exact table (1), and verifies every strict inequality in (3).
