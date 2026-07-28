# Five-core families without \(K_{3,3,1,1}\)

Date: 2026-07-28.

## Result and scope

Write
\[
 A=K_{5,1,1,1},\qquad C=K_{3,1,1,1,1},\qquad D=K_6.
\]
No family of exactly five distinct \(A\)-, \(C\)-, and \(D\)-cores can
collectively account for all seven blocked size-ten supports in the
exceptional \(r=0\) profile.

Together with `R0_FIVE_CORE_HIGH_B.md`, this excludes every family of
exactly five distinct obstruction cores.  It is a cover-impossibility
theorem: the cores themselves can coexist, but they cannot receive positive
multiplicities summing to seven while respecting the necessary complement
constraints.

There are 21 type multisets:
\[
\begin{gathered}
A^5,A^4C,A^3C^2,A^2C^3,AC^4,C^5,\\
A^4D,A^3CD,A^2C^2D,AC^3D,C^4D,\\
A^3D^2,A^2CD^2,AC^2D^2,C^3D^2,\\
A^2D^3,ACD^3,C^2D^3,AD^4,CD^4,D^5.
\end{gathered} \tag{1}
\]

## Vertex-set complement-row lemma

Let \(J\) be the union of a candidate family of core graphs
\(J_1,\ldots,J_k\), let \(C_i=V(J_i)\), and assign positive
multiplicities \(t_i\) with \(\sum_i t_i=7\).  For every vertex set
\(X\subseteq V(K_{13})\), a necessary condition is
\[
\sum_{v\in X}\bigl(d_J(v)-2\bigr)-3\min(5,|X|)
\ \le\
\sum_{i=1}^k t_i\min\bigl(3,|X\setminus C_i|\bigr). \tag{2}
\]

Indeed, the exact complement-row identity says that the ten remaining
complement sets contain \(v\) exactly \(d_F(v)-2\) times, where \(F\) is
the 31-edge seven-prefix.  Since \(J\subseteq F\), their total incidence
with \(X\) is at least
\[
\sum_{v\in X}\bigl(d_J(v)-2\bigr).
\]
The three complement five-sets contribute at most
\(3\min(5,|X|)\).  A complement triple assigned to \(J_i\) is disjoint
from \(C_i\), so it contributes at most
\(\min(3,|X\setminus C_i|)\).  Summing gives (2).

For verification it is enough to enumerate subsets of vertices having
\(d_J(v)\ge3\).  If a violating \(X\) contains a vertex of degree at most
two, deleting that vertex weakly increases the left side of (2) and
weakly decreases its right side.

The earlier common-row contradiction is the singleton special case: if a
vertex belongs to every core support and has \(d_J(v)\ge6\), the left side
is positive and the right side is zero.

## Direct rank closure of the three C-heavy rows

The three largest family enumerations also admit a shorter exact
optimization proof.  Put \(W=\bigcup_i C_i\), \(w=|W|\), and \(e=|E(J)|\).
Taking \(X=W\) in (2) gives
\[
 2e-2w
 \le
 15+\sum_i t_i\min(3,w-|C_i|). \tag{3}
\]
An exact CP-SAT model minimizes \(e\) for each possible \(w\), subject only
to distinct cores, \(|E(J)|\le31\), and \(\Delta(J)\le7\).  It then
maximizes the right side over every positive reuse-bounded multiplicity
vector summing to seven.  The complete feasible table is
\[
\begin{array}{c|c|c|c|c}
\text{types}&w&\min e&2e-2w&
15+\max\text{ triple incidences}\\ \hline
AC^4&8&22&28&21\\
AC^4&9&28&38&28\\
C^5&7&20&26&15\\
C^5&8&24&32&22\\
C^4D&7&20&26&18\\
C^4D&8&23&30&25
\end{array} \tag{4}
\]
Every other \(w\) is infeasible even under those relaxed graph screens.
Every displayed demand strictly exceeds its maximum supply, so these
three rows are excluded independently of the longer family census.
`verify_r0_five_core_final_three.py` rebuilds all six optima, all
infeasibility results, and every strict inequality.

## Exact enumeration

For each multiset in (1), the verifier fixes a canonical core of the
cheapest anchor type under the \(S_{13}\)-action and enumerates every
compatible choice of the other four distinct cores.  A partial union is
discarded only when it violates a necessary condition:
\[
 |E(J)|\le31,\qquad \Delta(J)\le7,
\]
the degree-two completion deficit, or the nine-clique screen.

For every retained union it enumerates every positive multiplicity vector.
An unused core could be deleted, reducing to an already-excluded
four-or-fewer-core cover, so positivity loses no case.
Because five positive entries sum to seven, these have shape
\[
 3+1+1+1+1\qquad\text{or}\qquad2+2+1+1+1. \tag{5}
\]
For all 31 nonempty core subfamilies \(I\), it imposes the simultaneous
capacity inequality
\[
3\sum_{i\in I}t_i
\le
36+2|C_I|-\sum_{v\in C_I}d_J(v)-r_I, \tag{6}
\]
where \(C_I=\bigcap_{i\in I}C_i\), and \(r_I\) is the minimum number of
the \(31-|E(J)|\) completion edges forced to touch \(C_I\):
\[
r_I=\max\left\{0,\,
31-|E(J)|-\left|E(K_{V\setminus C_I})\setminus E(J)\right|
\right\}. \tag{7}
\]
Finally it checks the common-row special case and then every instance of
(2).

The exhaustive counts are below.  “Screened” counts fixed-canonical-anchor
families that reach the final multiplicity test; it is not an orbit count.

\[
\begin{array}{c|r|r|r|r|r}
\text{types}&\text{screened}&\text{capacity covers}&
\text{common row}&\text{other }X&\text{unresolved}\\ \hline
A^5&1{,}260&0&0&0&0\\
A^4C&27{,}294&0&0&0&0\\
A^3C^2&1{,}100{,}850&0&0&0&0\\
A^2C^3&4{,}730{,}720&0&0&0&0\\
AC^4&4{,}670{,}725&0&0&0&0\\
C^5&21{,}735{,}632&12{,}456&12{,}450&6&0\\
A^4D&14{,}870&0&0&0&0\\
A^3CD&355{,}800&0&0&0&0\\
A^2C^2D&2{,}362{,}000&0&0&0&0\\
AC^3D&2{,}970{,}585&0&0&0&0\\
C^4D&14{,}111{,}348&9{,}432&9{,}432&0&0\\
A^3D^2&25{,}425&0&0&0&0\\
A^2CD^2&342{,}240&0&0&0&0\\
AC^2D^2&613{,}395&0&0&0&0\\
C^3D^2&3{,}031{,}569&16{,}848&16{,}848&0&0\\
A^2D^3&14{,}060&0&0&0&0\\
ACD^3&48{,}535&0&0&0&0\\
C^2D^3&255{,}626&11{,}256&11{,}256&0&0\\
AD^4&1{,}240&110&110&0&0\\
CD^4&7{,}055&1{,}853&1{,}853&0&0\\
D^5&22{,}155&22{,}155&22{,}155&0&0
\end{array} \tag{8}
\]

Thus every row has zero unresolved assignments.
The six \(C^5\) families in the “other \(X\)” column are the only census
leaves needing more than the common-row singleton cut.  A canonical first
example has \(|E(J)|=25\), multiplicities \((1,1,1,2,2)\), and
\(X=\{5\}\): the complement-row demand is two incidences while the five
core classes' seven assigned complement triples can supply at most one.

## Reproduction

Run `verify_r0_four_core_capacity.py` once for each row of (1).  For
example,

```text
python3 -B verify_r0_four_core_capacity.py \
  31111 31111 31111 6 6
```

The following command replays the complete 21-row table:

```bash
printf '%s\n' \
  '5111 5111 5111 5111 5111' \
  '5111 5111 5111 5111 31111' \
  '5111 5111 5111 31111 31111' \
  '5111 5111 31111 31111 31111' \
  '5111 31111 31111 31111 31111' \
  '31111 31111 31111 31111 31111' \
  '5111 5111 5111 5111 6' \
  '5111 5111 5111 31111 6' \
  '5111 5111 31111 31111 6' \
  '5111 31111 31111 31111 6' \
  '31111 31111 31111 31111 6' \
  '5111 5111 5111 6 6' \
  '5111 5111 31111 6 6' \
  '5111 31111 31111 6 6' \
  '31111 31111 31111 6 6' \
  '5111 5111 6 6 6' \
  '5111 31111 6 6 6' \
  '31111 31111 6 6 6' \
  '5111 6 6 6 6' '31111 6 6 6 6' '6 6 6 6 6' |
xargs -P 4 -n 5 /opt/homebrew/bin/python3 -B \
  collaboration/first_lift_global_theorem/verify_r0_four_core_capacity.py
```

The optimized `covering_splits` implementation in
`verify_r0_three_core_capacity.py` caches the pattern-only multiplicity
demands, tests singleton subfamilies first, and computes each required
subfamily bound at most once per family.  This is a semantics-preserving
acceleration of the same finite test.

As regression controls after that acceleration, all sixteen rows in
`R0_THREE_CORE_CAPACITY.md` replay with `covering_families=0`; the
\(A^3CD\) five-core row reproduces
`screened_leaves=355800, covering_families=0`; and the nonzero-cover
\(CD^4\) row reproduces
`screened_leaves=7055, covering_families=1853,
row_identity_excluded=1853, unresolved=0`.
