# Six or seven cores with exactly five non-\(K_6\) cores

Date: 2026-07-28.

## Result and scope

No six- or seven-core total obstruction in the exceptional \(r=0\)
profile has exactly five non-\(K_6\) cores.

Write
\[
 A=K_{5,1,1,1},\quad B=K_{3,3,1,1},\quad
 C=K_{3,1,1,1,1},\quad D=K_6.
\]
The computation exhausts all 21 multisets of five types from
\(\{A,B,C\}\), with one \(D\)-core in the six-core case and two
\(D\)-cores in the seven-core case.  Together with the preceding
layers, any surviving six- or seven-core obstruction must therefore
contain at least six non-\(K_6\) cores.

## Exact union minima

Fix the first exceptional core under \(S_{13}\), select the remaining
exceptional cores with their required types, and select the required
distinct \(D\)-cores.  Under only
\[
 |E(J)|\le31,\qquad \Delta(J)\le7,
\]
the complete list of feasible pairs \((w,e_k)\), where
\(w=|V(J)|\) and \(e_k\) is the exact minimum \(|E(J)|\), is
\[
\begin{array}{c|c|c}
\text{quintuple}&k=6&k=7\\ \hline
AAAAA&(8,25),(9,28)&(8,25),(9,28)\\
AAAAB&(8,25)&(8,25)\\
AAAAC&(8,23),(9,28)&(8,24),(9,28)\\
AAABB&(8,25)&(8,25)\\
AAABC&(8,25)&(8,25)\\
AAACC&(8,23),(9,28)&(8,24),(9,28)\\
AABBB&(8,25)&(8,25)\\
AABBC&(8,25)&(8,25)\\
AABCC&(8,25)&(8,25)\\
AACCC&(8,23),(9,27)&(8,24),(9,27)\\
ABBBB&(8,25)&(8,25)\\
ABBBC&(8,25)&(8,25)\\
ABBCC&(8,25)&(8,25)\\
ABCCC&(8,25)&(8,25)\\
ACCCC&(8,23),(9,28)&(8,23),(9,28)\\
BBBBB&(8,25)&(8,25)\\
BBBBC&(8,25)&(8,25)\\
BBBCC&(8,25),(9,30)&(8,25)\\
BBCCC&(8,25),(9,29)&(8,25)\\
BCCCC&(8,25)&(8,25)\\
CCCCC&(7,20),(8,24)&(7,20),(8,24)
\end{array} \tag{1}
\]
Every unlisted union order is graph-screen infeasible.

## Row-rank exclusion

For the union \(W\) of the core supports, the complement row identity
forces
\[
 2e(J)-2w
 \le
 15+\sum_i t_i\min(3,w-|C_i|). \tag{2}
\]
Here the five exceptional cores contribute \(0,1,2,\) or \(3\)
according to their support sizes and \(w\), while each \(D\)-core
contributes \(\min(3,w-6)\).  In the six-core case one of the six
distinct cores is used twice by the seven assigned triples; maximizing
over every core whose reuse ceiling permits this gives the same supply
ceiling as the two distinct \(D\)-cores in the seven-core case:
\[
\begin{array}{c|ccc}
 &w=7&w=8&w=9\\ \hline
15+\max\text{ triple incidences}
&17&19+\#C&26+\#C.
\end{array} \tag{3}
\]
A \(B\)-core is never eligible for the doubled assignment because its
reuse ceiling is one.

Substituting every entry of (1) into the left side of (2) gives a
strictly larger value than (3).  The closest cases are \(ACCCC\) at
\(w=8\), where both core counts give \(30>23\), and the six-core
\(AACCC\) branch at \(w=9\), where \(36>29\).  Hence all 21
five-exceptional branches are impossible.

## Reproduction

`verify_r0_six_seven_five_exceptional.py` rebuilds every fixed-first
candidate pool, proves all displayed optima and all unlisted
infeasibilities, and checks every strict row-rank inequality.
