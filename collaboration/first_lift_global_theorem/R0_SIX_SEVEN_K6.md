# Six or seven distinct \(K_6\) obstruction cores

Date: 2026-07-28.

## Result and scope

In the exceptional \(r=0\) profile, neither six nor seven distinct
\(K_6\) cores can collectively account for all seven blocked size-ten
supports.

For six distinct cores the only positive multiplicity shape is
\[
 2+1+1+1+1+1,
\]
and for seven it is \(1+1+1+1+1+1+1\).  In either case the total
multiplicity is seven.

This result treats only the pure-\(K_6\) type branches.  Mixed six- and
seven-core families remain open.

## Exact union classification

Fix one canonical \(K_6\) under \(S_{13}\).  Among the other 1,715
\(K_6\)'s, exactly 364 pass the necessary two-core conditions
\[
 |E(J)|\le31,\qquad \Delta(J)\le7.
\]
Select five or six of those candidates and let \(W\) be the union of all
core supports.  An exact finite optimization gives
\[
\begin{array}{c|cc}
 &|W|=7&|W|=8\\ \hline
6\text{ cores: minimum }|E(J)|&21&26\\
7\text{ cores: minimum }|E(J)|&21&26
\end{array} \tag{1}
\]
and proves that no such family with \(9\le|W|\le13\) satisfies the
31-edge and maximum-degree bounds.

## Full row-rank contradiction

Apply the complement-row identity to \(W\).  The total number of
occurrences of vertices of \(W\) among all ten remaining complement sets
is
\[
 \sum_{v\in W}(d_F(v)-2)
 \ge 2|E(J)|-2|W|. \tag{2}
\]
The three complement five-sets contribute at most fifteen occurrences in
\(W\).

A complement triple assigned to a \(K_6\) core lies outside that core.
Since the core support is a six-set contained in \(W\), such a triple
contains at most
\[
 |W|-6
\]
vertices of \(W\).  The assigned multiplicities sum to seven, so all seven
triples contribute at most \(7(|W|-6)\) occurrences in \(W\).  Therefore
a total obstruction would require
\[
 2|E(J)|-2|W|
 \le 15+7(|W|-6). \tag{3}
\]

For \(|W|=7\), (1) makes the left side at least \(28\), while the right
side is \(22\).  For \(|W|=8\), the two sides are at least \(36\) and
at most \(29\), respectively.  Both are contradictions, and larger
support unions do not pass the exact graph screen.

Thus neither six nor seven distinct \(K_6\) cores can cover the seven
blocked supports.

## Reproduction

`verify_r0_six_seven_k6.py` independently rebuilds the 364-candidate pool,
solves every fixed-\(|W|\) finite optimization, checks the exact table
(1), and checks the two strict row-rank inequalities.
