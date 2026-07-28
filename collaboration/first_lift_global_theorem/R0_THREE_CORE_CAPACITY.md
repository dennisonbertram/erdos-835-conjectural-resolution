# Three-core complement-capacity screen in the exceptional profile

Date: 2026-07-27.

## Result and scope

Continue in the exceptional \(r=0\) profile, where the union \(F\) of the
seven selected matchings satisfies
\[
 |E(F)|=31,\qquad 2\le d_F(v)\le7.
\]
After the earlier exclusions, abbreviate the four surviving size-ten
obstruction-core types by
\[
 A=K_{5,1,1,1},\quad B=K_{3,3,1,1},\quad
 C=K_{3,1,1,1,1},\quad D=K_6.
\]
Their already-proved individual reuse ceilings in a total-obstruction
argument are respectively
\[
 3,\quad1,\quad3,\quad4. \tag{1}
\]

The exact three-core enumeration below proves that all sixteen
three-core type multisets whose ceilings in (1) sum to at least seven
nevertheless **cannot collectively account for all seven blocked
supports**:
\[
 \begin{gathered}
 A^3,\ A^2B,\ A^2C,\ A^2D,\ ABC,\ ABD,\ AC^2,\ ACD,\\
 AD^2,\ BC^2,\ BCD,\ BD^2,\ C^3,\ C^2D,\ CD^2,\ D^3.
 \end{gathered} \tag{2}
\]

This does not say that the three cores in (2) cannot coexist.  It says that
whenever they coexist inside a graph passing the necessary prefix
conditions, their sharpened combined reuse ceiling is less than seven.

## Family-union capacity lemma

Let \(J\) be the union of a family of cores contained in \(F\), and fix one
core with vertex set \(C\).  Put \(O=V(K_{13})\setminus C\).  The exact
complement identity gives total complement capacity
\[
 \sum_v(d_F(v)-2)=36.
\]
Consequently the capacity outside this core is
\[
 P_F(O)
 =36-\sum_{v\in C}(d_F(v)-2)
 =36+2|C|-\sum_{v\in C}d_F(v). \tag{3}
\]

There are \(31-|E(J)|\) edges still to add when completing \(J\) to \(F\).
At most
\[
 \binom{|O|}{2}-|E_J(O)|
\]
of them can be added wholly inside \(O\).  Therefore at least
\[
 q(J,C)=\max\left\{0,\,
 31-|E(J)|-\left(\binom{|O|}{2}-|E_J(O)|\right)\right\} \tag{4}
\]
additional edges touch \(C\).  Each contributes at least one to the degree
sum over \(C\), so (3) implies
\[
 P_F(O)\le
 36+2|C|-\sum_{v\in C}d_J(v)-q(J,C). \tag{5}
\]

If this core is assigned \(t\) blocked supports, their complement triples
all lie in \(O\) and consume \(3t\) incidences.  Hence its family-sharpened
reuse bound is
\[
 u_J(C)=\min\left\{u(C),\
 \left\lfloor
 \frac{36+2|C|-\sum_{v\in C}d_J(v)-q(J,C)}3
 \right\rfloor\right\}, \tag{6}
\]
where \(u(C)\) is the appropriate ceiling in (1).

Assign each of the seven allegedly blocked supports to one core certifying
its blockage.  For a three-core family \(C_1,C_2,C_3\), (6) first gives the
necessary condition
\[
 u_J(C_1)+u_J(C_2)+u_J(C_3)\ge7. \tag{7}
\]
Although the three terms can double-count complement capacity, that only
makes (7) weaker and therefore safe as an impossibility screen.

The double counting can be removed for every subfamily.  Given a nonempty
index set \(I\subseteq\{1,2,3\}\), put
\[
 K_I=\bigcap_{i\in I}C_i.
\]
Every complement triple assigned to a core in \(I\) lies in
\[
 \bigcup_{i\in I}(V\setminus C_i)=V\setminus K_I.
\]
Applying (3)--(5) with \(K_I\) in place of \(C\) gives
\[
 3\sum_{i\in I}t_i\le
 36+2|K_I|-\sum_{v\in K_I}d_J(v)-q(J,K_I), \tag{8}
\]
where
\[
 q(J,K_I)=\max\left\{0,\,
 31-|E(J)|-
 \left(\binom{13-|K_I|}{2}-|E_J(V\setminus K_I)|\right)
 \right\}. \tag{9}
\]
These seven subset inequalities are still only elementary incidence
counting, but together they eliminate the double counting in (7).

## Exact three-core table

For each type multiset, the verifier fixes one core under the action of
\(S_{13}\), exhausts all labelled choices of the other two distinct cores,
and retains only unions \(J\) satisfying
\[
 |E(J)|\le31,\quad \Delta(J)\le7,\quad
 |E(J)|+\left\lceil\frac{\sum_v(2-d_J(v))_+}{2}\right\rceil\le31,
\]
together with the nine-vertex induced-capacity inequalities.  The next
column is the maximum value of the left side of (7) over those retained
unions.  Some entries reach seven or more, demonstrating why the subset
inequalities (8) are necessary.  The verifier enumerates every positive
integer assignment \(t_1+t_2+t_3=7\) within (1); no row admits an
assignment satisfying all seven instances of (8).

\[
\begin{array}{c|r|c@{\qquad}c|r|c}
\text{types}&\max\sum u_J&\text{status}&
\text{types}&\max\sum u_J&\text{status}\\ \hline
A^3   &6&\text{excluded}&A^2B&0&\text{excluded}\\
A^2C  &7&\text{excluded}&A^2D&7&\text{excluded}\\
ABC   &4&\text{excluded}&ABD&3&\text{excluded}\\
AC^2  &8&\text{excluded}&ACD&8&\text{excluded}\\
AD^2  &8&\text{excluded}&BC^2&5&\text{excluded}\\
BCD   &6&\text{excluded}&BD^2&6&\text{excluded}\\
C^3   &9&\text{excluded}&C^2D&10&\text{excluded}\\
CD^2  &11&\text{excluded}&D^3&12&\text{excluded}
\end{array} \tag{10}
\]

The \(A^2C\) and \(A^2D\) rows illustrate the subset mechanism.  Every
retained \(A^2C\) or \(A^2D\) family attaining summed capacity seven has
individual capacity vector \((2,2,3)\), and the two \(A\)-cores have the
same eight-vertex support.  To cover seven supports, both \(A\)-cores
would therefore have to attain capacity two, requiring four complement
triples, or twelve incidences, in their common five-vertex outside set.
But (3), applied once to that common set, bounds its total capacity by
eight incidences in the \(A^2C\) row and six in the \(A^2D\) row.  Thus
the apparent seven in the table double-counts common capacity, and both
rows are excluded.

For example, the \(A^3\) scan has 630 admissible ordered families and only
fifteen distinct union graphs after fixing the first core.  Five unions
give the capacity vector \((2,2,2)\), and the other ten give
\((0,0,0)\).  Thus three \(A\)-cores can cover at most six supports.

The zero in the \(A^2B\) row is not a non-coexistence statement: eleven
distinct union graphs survive the prefix screens.  Rather, all their
outside capacities vanish after the forced completion-edge correction
in (4).

## Reproduction and frontier

`verify_r0_three_core_capacity.py` reproduces any row deterministically.
For example,

```text
python3 -B verify_r0_three_core_capacity.py 5111 5111 5111
python3 -B verify_r0_three_core_capacity.py 3311 31111 6
```

Replay all sixteen capacity-sufficient type multisets separately from the
fast Tutte-CNF verifier with:

```bash
printf '%s\n' \
  '5111 5111 5111' '5111 5111 3311' \
  '5111 5111 31111' '5111 5111 6' \
  '5111 3311 31111' '5111 3311 6' \
  '5111 31111 31111' '5111 31111 6' '5111 6 6' \
  '3311 31111 31111' '3311 31111 6' '3311 6 6' \
  '31111 31111 31111' '31111 31111 6' \
  '31111 6 6' '6 6 6' |
xargs -P 4 -n 3 /opt/homebrew/bin/python3 -B \
  collaboration/first_lift_global_theorem/verify_r0_three_core_capacity.py
```

Every invocation must report `covering_families=0` and a final `PASS`.
This slower sixteen-family replay is deliberately not duplicated inside
`verify_r0_tutte_full_cnf.py`.

The optional `--stop-at-seven` flag stops only if it finds an assignment
that satisfies every subset inequality.  No capacity-sufficient
three-core pattern does.

Thus a hypothetical total obstruction among the four surviving core types
must use at least four distinct cores.  Families of four or more distinct
cores remain to be reduced.
