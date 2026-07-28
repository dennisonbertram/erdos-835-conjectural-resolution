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

The exact three-core enumeration below proves that nine of the sixteen
three-core type multisets whose ceilings in (1) sum to at least seven
nevertheless **cannot collectively account for all seven blocked
supports**:
\[
 A^3,\ A^2B,\ A^2C,\ A^2D,\ ABC,\ ABD,\ BC^2,\ BCD,\ BD^2. \tag{2}
\]
The other seven patterns remain open under this screen.

This does not say that the three cores in (2) cannot coexist.  It says that
whenever they coexist inside a graph passing the necessary prefix
conditions, their sharpened combined reuse ceiling is less than seven.
Likewise, a surviving row below is only a necessary-condition witness, not
an actual seven-prefix or a total obstruction.

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
its blockage.  For a three-core family \(C_1,C_2,C_3\), (6) gives the
necessary condition
\[
 u_J(C_1)+u_J(C_2)+u_J(C_3)\ge7. \tag{7}
\]
Although the three terms can double-count complement capacity, that only
makes (7) weaker and therefore safe as an impossibility screen.

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
unions.

\[
\begin{array}{c|r|c@{\qquad}c|r|c}
\text{types}&\max\sum u_J&\text{status}&
\text{types}&\max\sum u_J&\text{status}\\ \hline
A^3   &6&\text{excluded}&A^2B&0&\text{excluded}\\
A^2C  &7&\text{excluded}^{*}&A^2D&7&\text{excluded}^{*}\\
ABC   &4&\text{excluded}&ABD&3&\text{excluded}\\
AC^2  &8&\text{open}&ACD&8&\text{open}\\
AD^2  &8&\text{open}&BC^2&5&\text{excluded}\\
BCD   &6&\text{excluded}&BD^2&6&\text{excluded}\\
C^3   &9&\text{open}&C^2D&10&\text{open}\\
CD^2  &11&\text{open}&D^3&12&\text{open}
\end{array} \tag{8}
\]

The two starred rows need one final shared-capacity observation.  Every
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

For an open row, `--stop-at-seven` stops as soon as it displays a union
passing every necessary screen whose summed bound reaches seven.  Such a
witness only proves that (6) alone does not eliminate the row.

The remaining three-core frontier is therefore
\[
 AC^2,\ ACD,\ AD^2,\ C^3,\ C^2D,\ CD^2,\ D^3. \tag{9}
\]
Families of four or more distinct cores also remain to be reduced.
