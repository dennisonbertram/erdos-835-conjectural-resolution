# Structural repair transport across the \(r=1\to2\) and \(r=3\to4\) lifts

Date: 2026-07-28.

## Exact results

For the verified dead prefixes, the exact repair distances are
\[
\begin{array}{c|cc}
\text{certificate}&\text{eighth admission}&\text{full completion}\\ \hline
r=1&1&3\\
r=2&1&3\\
r=3,\ C\subset G&1&4\\
r=4&1&4.
\end{array}
\]
In every row the one-layer repair is an alternating four-cycle switch, so it
changes the minimum possible two edges inside that layer.

The \(r=2\) full-repair optimum retains prefix layers \(3,4,5,6\); the
\(r=4\) optimum retains layers \(0,1,2\). Literal 17-layer completions in
`verify_r2_r4_structural_repair.py` prove the upper bounds. The lower bounds
are solver-free crossing-cut certificates, independently checked against
all 4,095 nontrivial cuts modulo complementation.

Both support matrices also have literal proper 17-colourings of
\(K_{18}-E(K_{13})\) inducing their prescribed holes. Combined with the
literal 17-layer completions inside the hole, this proves class-B-prime
realizability. It does not prove fan realizability.

## General crossing-cut bound

For a cut \(X\subset V(K_{13})\), a support \(S_i\), and an original selected
layer \(M_i\), put
\[
u_i(X)=\min(|S_i\cap X|,|S_i\setminus X|),\qquad
a_i(X)=|M_i\cap\delta(X)|.
\]
If a full completion changes the selected layers in \(T\), then
\[
\sum_{i\in T}(u_i-a_i)\ge
|X|(13-|X|)
-\sum_{i=7}^{16}u_i-\sum_{i=0}^{6}a_i. \tag{1}
\]
Thus the minimum number of changed layers is at least the least number of
largest gains \(u_i-a_i\) whose sum reaches the right side.

For \(r=2\), take \(X=\{0,\ldots,5\}\). The right side is 12 and the sorted
gains are
\[
6,4,4,4,4,4,4.
\]
The two largest sum to only 10, so at least three layers change. For \(r=4\),
take \(X=\{0,\ldots,6\}\). The deficit is 14 and the gains are
\[
4,4,4,2,2,2,2.
\]
The three largest sum to only 12, so at least four layers change.

## Lift-invariance lemma

The equality of the distances within each pair is structural.

**Cross-edge lift.** Suppose \(x\in X\), \(y\notin X\), and a lift adds the
edge \(xy\) to a selected layer while expanding that layer's support by
\(\{x,y\}\). Suppose it simultaneously adds \(\{x,y\}\) to one remaining
complement, shrinking that remaining support. Then:

- the selected layer's \(a_i\) and \(u_i\) both increase by one, so its gain
  \(u_i-a_i\) is unchanged;
- total remaining capacity decreases by one; and
- total original selected crossing count increases by one.

The last two changes cancel in the right side of (1). Hence the entire cut
lower bound is invariant. This is exactly the \(r=1\to r=2\) lift using
edge \(29\) across the \(6:7\) cut. The deficit remains 12 and the repair
distance remains three.

**Within-shore complement transfer.** Suppose a pair \(P\) lying in one
shore of a cut is moved from one remaining complement to another. One
remaining support gains \(P\), the other loses it. Whenever that shore is
the capacity-limiting side in both supports, their changes in \(u_i\) cancel.
The prefix is unchanged, so (1) is invariant. This is exactly the
\(r=3,\ C\subset G\to r=4\) transfer of \(P=\{10,12\}\) outside
\(\{0,\ldots,6\}\). The deficit remains 14 and the repair distance remains
four.

## Transport of the one-layer switch

A one-layer repair \((M_i\mapsto M'_i,N)\) survives a lift whenever:

1. the selected support of layer \(i\) and the enabled remaining support of
   \(N\) are unchanged;
2. every added prefix edge is outside \(M'_i\cup N\); and
3. the other selected layers remain edge-disjoint from \(M'_i\cup N\).

The \(r=1\) four-cycle switch in its size-twelve layer meets these conditions
after the \(r=2\) edge/complement lift. The \(r=3\) \(C\subset G\) switch
meets them after the \(r=4\) complement transfer because both its selected
and enabled remaining supports are untouched. Since the original prefixes
are semantically verified dead, distance zero is impossible; the transported
switch proves exact distance one.

This is a reusable certificate-transport lemma, not a universal assertion
that every class-B prefix admits such a switch.

## Reproduction and scope

`verify_r2_r4_structural_repair.py` uses only the Python standard library.
It checks:

- both explicit two-edge one-layer switches and eighth matchings;
- both literal optimal full completions and their retained-layer counts;
- the sharp cut lower bounds and the complete 4,095-cut censuses;
- the numerical lift-invariance identities; and
- both literal class-B-prime partial factorizations.

`search_r2_r4_repair.py` records the exact CP-SAT maximum-retention discovery
models. `search_r2_r4_prime.py` records the exact partial-factorization
discovery models. Their SAT output is telemetry; the literal standard-library
replay is the proof.

The conclusions concern these four explicit certificates. They do not give a
universal switching theorem, fan realizability, a full first-lift theorem, or
a solution of Erdős--Rosenfeld Problem #835.
