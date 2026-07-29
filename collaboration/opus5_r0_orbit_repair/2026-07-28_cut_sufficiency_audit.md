# Audit of the second Opus 5 cut-sufficiency attack

Date: 2026-07-28.

## Verdict

The run does **not** prove or refute cut sufficiency under the full class-B
row equations.  It does give a correct counterexample after those equations
are removed, and a correct reason that the same counterexample cannot occur
as one of the seven remaining triple rows.

The target statement remains:

> If the six-prefix, all eleven remaining rows, and
> \(\rho(v)=d_D(v)-1\) are present, do the internal-edge capacity cuts
> characterize three simultaneously packable size-ten rows?

The exact full-row SAT search remains the relevant decision procedure.

## Independently verified weaker-ambient counterexample

Put
\[
A=\{0,1,2,3,4\},\quad B=\{5,6,7,8,9\},\quad R=\{10,11,12\}
\]
and let \(D=K_{5,5}[A,B]\cup\{10\,11,11\,12\}\).  It has the following
decomposition into six disjoint matching layers:
\[
\begin{array}{c|l}
L_0&05,16,27,38,49\\
L_1&06,17,28,39,45\\
L_2&07,18,29,35,46\\
L_3&08,19,25,36\\
L_4&47,09,15,10\,11\\
L_5&26,37,48,11\,12.
\end{array}
\]
Thus the layer-size multiset is \(4,4,4,5,5,5\),
\(|D|=27\), \(1\le d_D\le5\), and \(G=K_{13}-D\) has 51 edges and minimum
degree seven.

Take the three selected rows all equal to \(R\), with common support
\(S=A\cup B\).  Then
\[
G[S]=K_5[A]\mathbin{\dot\cup}K_5[B],
\]
so even one perfect matching is impossible.  Nevertheless all \(2^{13}\)
capacity cuts pass.  If \(a=|U\cap A|\), \(b=|U\cap B|\), and
\(s=a+b\), their positive side is
\[
3\max(0,s-5)\le {a\choose2}+{b\choose2}\le e(G[U]).
\]
The minimum right side for \(s=6,7,8,9,10\) is respectively
\(6,9,12,16,20\), while the left side is \(3,6,9,12,15\).
Applying the same calculation to \(V\setminus U\) checks the negative side.

This is an ambient counterexample only.  The class-B equation would give
\(\rho(v)=4\) on \(S\) and total remaining-row incidence 41.  Hence the
three vertices of \(R\) receive only one incidence in total, whereas making
\(R\) a remaining row would require at least three.

The standard-library verifier
`verify_weaker_ambient_cut_counterexample.py` checks the layer decomposition,
degrees, all 8192 cuts, nonmatchability, and this incidence contradiction.

## Correct positive reductions

Only cuts of size six, seven, and eight can bind.  For \(|U|=9\),
\(\sum_{v\in U}d_D(v)\le45\) gives \(e(D[U])\le22\), hence
\(e(G[U])\ge14>12\).  For larger \(U\), the global bound \(|D|=27\)
is already enough.

Under the full class-B equations and the capacity cuts, each selected
size-ten row is individually matchable.  Indeed
\(\delta(G[S])\ge4\), and the only coarsened Tutte obstructions on ten
vertices are:

1. two five-cliques, which force all 25 cross edges into \(D\) and therefore
   contradict the remaining-row incidence of the selected row; or
2. an independent six-set, which directly violates its positive capacity
   cut.

A support-preserving repack leaves all vertex degrees and row incidences
fixed.  On one cut it can reduce \(e(D[U])\) by at most two: for a layer
support \(W\), \(m=|W\cap U|\), its internal-edge count ranges from
\(\max(0,m-|W|/2)\) to \(\lfloor m/2\rfloor\), whose width is at most two
for \(|W|\in\{8,10\}\).

The stronger uniform density target
\[
e(D[U])\le12,15,19\quad\text{for }|U|=6,7,8
\]
would make every triple of size-ten supports cut-feasible, because the
corresponding residual edge counts are at least \(3,6,9\).

## Rejected or unproved parts of the Opus response

The claimed “exact deficit five” is invalid.  It used
\[
e_D(U,V\setminus U)\le3
\]
as though it were a lower bound.  For a critical seven-set the displayed
argument proves only
\[
\tau(U)\ge5+e_D(U,V\setminus U),
\]
not \(\tau(U)\ge8\).  Also, among seven triple rows, three rows meeting
\(U\) at least twice are forced once \(\tau(U)\ge12\), not only at 13.
Consequently neither the stated deficit nor the conclusion that the row
identity route is impossible follows.

The response also jumped from individual matchability plus nonbinding parity
cuts to a prescribed proper three-edge-colouring problem.  A valid triple is
indeed equivalent to a degree-constrained union admitting that colouring,
but the capacity and parity cuts have not yet proved that such an underlying
degree-constrained subgraph exists.  The honest target gap therefore has two
parts:

1. existence of a suitable degree-constrained union inside \(G\); and
2. existence of its proper three-edge-colouring with the prescribed missing
   colours.

Neither part is promoted to a theorem here.

## A single-cut selection reduction

There is one additional solver-free reduction for the repair-selection
problem.  It does **not** say that size-seven and size-eight cuts cannot
obstruct a particular pairwise-compatible triple.  It says that no single
such cut can obstruct all \(\binom73\) choices of three triple rows.

Let \(c=e_D(U,V\setminus U)\), let \(T\) be the total incidence of the seven
triple rows on \(U\), and use the fact that the four five-set rows contribute
at most 20 incidences.

For \(|U|=7\) and \(e(G[U])=4\), one has \(e(D[U])=17\), hence
\[
T\ge (34+c-7)-20=7+c.
\]
A triple row meeting \(U\) in \(j\) vertices contributes cut deficit
\(\max(0,2-j)\).  If every choice of three rows had total deficit at least
five, there could be no row with deficit zero and at most one row with
deficit one.  This would give \(T\le1\), a contradiction.

For \(|U|=7\) and \(e(G[U])=5\), similarly
\[
T\ge (32+c-7)-20=5+c.
\]
The only violating triple has three rows disjoint from \(U\).  Since some
row meets \(U\), a nonviolating choice exists.

For \(|U|=8\) and \(e(G[U])=8\), the internal deleted-degree sum is 40, so
all eight vertices have deleted degree five and \(c=0\).  Thus
\[
T\ge(40-8)-20=12.
\]
Again some row meets \(U\), whereas a violation requires all three selected
rows to be disjoint from \(U\).

The only single cuts that can themselves eliminate every row triple are
therefore dense six-sets.  If \(g=e(G[U])\in\{0,1,2\}\), a selected triple
must contain at least \(3-g\) rows meeting \(U\).  This does not yet prove
that one triple works for all cuts simultaneously, nor that one repair
simultaneously relaxes every dense six-set.  Those are the exact remaining
selection obligations tested by `search_cut_feasible_repair.py`.
