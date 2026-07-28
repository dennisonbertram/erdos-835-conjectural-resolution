# Six or seven cores with exactly four non-\(K_6\) cores

Date: 2026-07-28.

## Result and scope

No six- or seven-core total obstruction in the exceptional \(r=0\)
profile has exactly four non-\(K_6\) cores.

With
\[
 A=K_{5,1,1,1},\quad B=K_{3,3,1,1},\quad
 C=K_{3,1,1,1,1},\quad D=K_6,
\]
this exhausts the fifteen exceptional quadruples
\[
\begin{gathered}
AAAA,AAAB,AAAC,AABB,AABC,AACC,ABBB,ABBC,ABCC,ACCC,\\
BBBB,BBBC,BBCC,BCCC,CCCC
\end{gathered}
\]
with two \(D\)-cores in the six-core case or three in the seven-core
case.  Consequently, any surviving six- or seven-core obstruction must
contain at least five non-\(K_6\) cores.

## Exact union and rank table

Fix one exceptional core under \(S_{13}\), select the other three
exceptional cores with their required types, and select the required
distinct \(D\)-cores.  Under only
\[
 |E(J)|\le31,\qquad \Delta(J)\le7,
\]
the following table gives every feasible support-union order \(w=|W|\),
the exact minimum edge counts for six and seven total cores, and the
largest possible complement supply.  The two demand columns are shown
separately because their minima can differ.

\[
\begin{array}{c|c|cc|cc|c}
\text{quadruple}&w&e_6&e_7&2e_6-2w&2e_7-2w&
15+\max\text{ triple incidences}\\ \hline
AAAA&8&24&25&32&34&21\\
AAAA&9&28&28&38&38&28\\
AAAB&8&25&25&34&34&21\\
AAAC&8&24&25&32&34&22\\
AAAC&9&28&28&38&38&29\\
AABB&8&25&25&34&34&21\\
AABC&8&25&25&34&34&22\\
AACC&8&24&25&32&34&23\\
AACC&9&27&27&36&36&30\\
ABBB&8&25&25&34&34&21\\
ABBC&8&25&25&34&34&22\\
ABCC&8&25&25&34&34&23\\
ACCC&8&23&24&30&32&24\\
ACCC&9&28&28&38&38&31\\
BBBB&8&25&25&34&34&21\\
BBBC&8&25&25&34&34&22\\
BBCC&8&25&25&34&34&23\\
BCCC&8&25&25&34&34&24\\
CCCC&7&20&21&26&28&18\\
CCCC&8&24&25&32&34&25
\end{array} \tag{1}
\]

Every unlisted union order is graph-screen infeasible.  In every
displayed row, both demand columns strictly exceed the maximum supply
from the three complement five-sets and the seven assigned complement
triples.  In the six-core case the supply column maximizes over every
eligible doubled core; a \(B\)-core is never doubled because its reuse
ceiling is one.

Thus all fifteen four-exceptional type branches are impossible for both
six and seven distinct cores.

## Reproduction

`verify_r0_six_seven_four_exceptional.py` rebuilds every fixed-first
candidate pool, proves all displayed optima and all unlisted
infeasibilities, and checks every strict row-rank inequality.
