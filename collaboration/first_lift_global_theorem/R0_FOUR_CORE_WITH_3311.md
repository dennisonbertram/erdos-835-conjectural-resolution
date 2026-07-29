# Four-core families containing \(K_{3,3,1,1}\)

Date: 2026-07-27.

## Result and scope

Continue with
\[
 A=K_{5,1,1,1},\quad B=K_{3,3,1,1},\quad
 C=K_{3,1,1,1,1},\quad D=K_6,
\]
whose individual total-obstruction reuse ceilings are \(3,1,3,4\).

No family of four distinct obstruction cores containing a \(B\)-core can
collectively account for all seven remaining size-ten supports in the
exceptional \(r=0\) profile.

This excludes every capacity-sufficient four-core type multiset containing
\(B\):
\[
\begin{gathered}
 AAAB,\ AABB,\ AABC,\ AABD,\ ABBC,\ ABBD,\ ABCC,\ ABCD,\ ABDD,\\
 BBBD,\ BBCC,\ BBCD,\ BBDD,\ BCCC,\ BCCD,\ BCDD,\ BDDD.
\end{gathered} \tag{1}
\]
It does not say these cores cannot coexist.  It says that no positive
multiplicity assignment summing to seven satisfies the exact
subfamily-capacity inequalities.

## Exhaustive screen

Fix a canonical \(B\)-core under \(S_{13}\).  Its exact compatible-core
pools after the necessary prefix graph screens have sizes
\[
 |N_A(B)|=38,\quad |N_B(B)|=81,\quad
 |N_C(B)|=214,\quad |N_D(B)|=27. \tag{2}
\]
For each row in (1), enumerate every unordered selection from the required
pools, rejecting a partial union as soon as it violates
\[
 |E(J)|\le31,\quad \Delta(J)\le7,\quad
 |E(J)|+\left\lceil\frac{\sum_v(2-d_J(v))_+}{2}\right\rceil\le31,
\]
or a nine-vertex induced-capacity inequality.

For every retained four-core union, enumerate each positive multiplicity
assignment
\[
 t_1+t_2+t_3+t_4=7
\]
within the type ceilings.  For all fifteen nonempty core subfamilies
\(I\), impose the complement-capacity inequality from
`R0_THREE_CORE_CAPACITY.md`:
\[
 3\sum_{i\in I}t_i\le
 36+2|K_I|-\sum_{v\in K_I}d_J(v)-q(J,K_I),
 \qquad K_I=\bigcap_{i\in I}C_i. \tag{3}
\]
Every row has zero surviving multiplicity assignments.

The exact counts of four-core families reaching the final multiplicity
test are
\[
\begin{array}{c|r@{\quad}c|r@{\quad}c|r}
AAAB&276&AABB&1{,}404&AABC&10{,}980\\
AABD&1{,}836&ABBC&27{,}288&ABBD&4{,}680\\
ABCC&72{,}002&ABCD&23{,}976&ABDD&1{,}740\\
BBBD&3{,}204&BBCC&76{,}644&BBCD&26{,}352\\
BBDD&1{,}926&BCCC&122{,}040&BCCD&61{,}875\\
BCDD&8{,}988&BDDD&368&&
\end{array} \tag{4}
\]

## Reproduction and remaining frontier

`verify_r0_four_core_capacity.py` reproduces any row deterministically.
For example,

```text
python3 -B verify_r0_four_core_capacity.py 5111 3311 31111 6
python3 -B verify_r0_four_core_capacity.py 3311 31111 31111 31111
```

The all-\(D\) row is independently excluded in
`R0_FOUR_K6_CLASSIFICATION.md`.  The fourteen complementary \(A,C,D\)
type multisets
\[
\begin{gathered}
AAAA,\ AAAC,\ AAAD,\ AACC,\ AACD,\ AADD,\ ACCC,\\
ACCD,\ ACDD,\ ADDD,\ CCCC,\ CCCD,\ CCDD,\ CDDD.
\end{gathered} \tag{5}
\]
are now excluded in `R0_ALL_FOUR_CORE_FAMILIES.md`.  Thus a hypothetical
total obstruction must use at least five distinct cores.  Families of five
or more distinct cores remain open.
