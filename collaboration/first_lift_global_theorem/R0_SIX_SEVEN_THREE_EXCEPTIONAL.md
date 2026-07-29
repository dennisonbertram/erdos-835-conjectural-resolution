# Six or seven cores with exactly three non-\(K_6\) cores

Date: 2026-07-28.

## Result and scope

No six- or seven-core total obstruction in the exceptional \(r=0\)
profile has exactly three non-\(K_6\) cores.

With
\[
 A=K_{5,1,1,1},\quad B=K_{3,3,1,1},\quad
 C=K_{3,1,1,1,1},\quad D=K_6,
\]
this exhausts the ten exceptional triples
\[
 AAA,AAB,AAC,ABB,ABC,ACC,BBB,BBC,BCC,CCC
\]
with three \(D\)-cores in the six-core case or four in the seven-core
case.  Families with at least four non-\(K_6\) cores remain open.

## Exact union and rank table

Fix one exceptional core under \(S_{13}\), select the other two
exceptional cores with their required types, and select the required
distinct \(D\)-cores.  Under only
\[
 |E(J)|\le31,\qquad \Delta(J)\le7,
\]
the following table gives every feasible support-union order \(w=|W|\),
the exact minimum edge counts for six and seven total cores, and the
largest possible complement supply.  The demand column uses the smaller
six-core edge minimum; when the seven-core minimum is larger, its demand
only increases.

\[
\begin{array}{c|c|cc|c|c}
\text{triple}&w&e_6&e_7&2e_6-2w&
15+\max\text{ triple incidences}\\ \hline
AAA&8&25&25&34&23\\
AAA&9&28&28&38&30\\
AAB&8&25&26&34&23\\
AAC&8&25&25&34&24\\
AAC&9&27&27&36&31\\
ABB&8&25&26&34&23\\
ABC&8&25&26&34&24\\
ACC&8&24&24&32&25\\
ACC&9&28&28&38&32\\
BBB&8&25&26&34&23\\
BBC&8&25&26&34&24\\
BCC&8&25&26&34&25\\
CCC&7&21&21&28&19\\
CCC&8&25&25&34&26
\end{array} \tag{1}
\]

Every unlisted union order is graph-screen infeasible.  Every displayed
demand strictly exceeds the maximum supply from the three complement
five-sets and the seven assigned complement triples.  In the six-core
case the supply column maximizes over every eligible doubled core; a
\(B\)-core is never doubled because its reuse ceiling is one.

Thus all ten three-exceptional type branches are impossible for both six
and seven distinct cores.

## Reproduction

`verify_r0_six_seven_three_exceptional.py` rebuilds every fixed-first
candidate pool, proves all displayed optima and all unlisted
infeasibilities, and checks every strict row-rank inequality.
