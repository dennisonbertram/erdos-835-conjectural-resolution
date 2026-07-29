# Two dead but fully completable seven-prefixes for \(r=3\)

Date: 2026-07-27.

## Result and scope

There are two exact \(n=13,q=17\) class-B support instances with profile
\[
(n_8,n_{10},n_{12})=(10,4,3)
\]
and seven pairwise edge-disjoint support matchings of type
\[
8^4\,10\,12^2
\]
such that none of the ten remaining supports has a perfect matching
avoiding the seven selected matchings.

The two certificates realize the final nested one-core obstruction
classes
\[
C\subset G\qquad\text{and}\qquad D\subset G,
\]
where
\[
C=K_{3,1,1,1,1},\qquad D=K_6,\qquad G=K_7.
\]
In each case the three remaining size-ten supports are blocked by the
same \(C\)- or \(D\)-core, and the remaining size-twelve support is
blocked by the containing \(G\)-core.

Both underlying 17-support instances nevertheless have explicit full
17-matching decompositions.  Thus these are dead-prefix certificates,
not noncompletable class-B instances.

They prove that the exceptional-\(r=0\) statement “every seven-prefix
extends” cannot hold for \(r=3\).  A universal nonzero-\(r\) result must
coordinate the earlier matching choices or switch the dead prefix.  No
class-B-prime, fan, or full-factorization realization of the displayed
dead prefixes is asserted.

## The two prefix unions

Put \(U=\{0,\ldots,6\}\).  In both cases \(F\) contains \(K_U\).

For the \(C\subset G\) certificate,
\[
F=K_U\ \dot\cup\
K_{\{7,8,9,10,12\}}\ \dot\cup\
\{2\,11,3\,11\}. \tag{1}
\]
The six remaining complement five-sets are
\[
\begin{gathered}
01235,\ 12345,\ 01246,\ 02346,\ 12356,\ 03456,
\end{gathered} \tag{2}
\]
and the other four remaining complements are
\[
789,\quad 7\,10\,12,\quad 8\,9\,10,\quad\{12\}. \tag{3}
\]
The triples avoid \(U\), so their size-ten supports contain the
\(C=K_U-E(K_{\{0,1,2\}})\) core.  The singleton avoids \(U\), so its
size-twelve support contains \(G=K_U\).

For the \(D\subset G\) certificate,
\[
\begin{aligned}
F=K_U\ \dot\cup\ \{&
78,79,7\,10,7\,11,7\,12,89,8\,11,8\,12,\\
&9\,11,9\,12,10\,11,11\,12\}.
\end{aligned} \tag{4}
\]
The six complement five-sets are
\[
01234,\ 12345,\ 01256,\ 01356,\ 23456,\ 047\,11\,12, \tag{5}
\]
and the other complements are
\[
678,\quad 79\,11,\quad 89\,11,\quad\{12\}. \tag{6}
\]
The triples avoid \(\{0,\ldots,5\}\), so their supports contain
\(D=K_{\{0,\ldots,5\}}\); the singleton support again contains
\(G=K_U\).

In both cases the 33 edges in (1) or (4) are explicitly decomposed by the
verifier into matchings of sizes
\[
4,4,4,4,5,6,6.
\]
Together with the displayed remaining complements, the selected supports
form exactly the profile \((10,4,3)\), every vertex belongs to twelve of
the seventeen supports, and the remaining complements obey
\[
\#\{\text{remaining complements containing }v\}=d_F(v)-2. \tag{7}
\]

## Dead prefix and full repair

Exhaustive matching recursion confirms that all six remaining size-eight,
all three remaining size-ten, and the remaining size-twelve support are
blocked by each displayed prefix.

For each same support matrix, however, the verifier also contains a
different list of seventeen support-perfect matchings.  In each list the
matching endpoints equal the corresponding support and the 78 matching
edges partition \(E(K_{13})\).  Hence both support instances are fully
completable.

The full lists are kept as literal certificate data in
`verify_r3_dead_seven_prefixes.py`, where they can be checked without an
integer solver.

## Discovery and verification

The certificates were found by exact CP-SAT models enforcing the selected
matching layers, complement row sums, nested \(C/G\) or \(D/G\) cores,
and lazy perfect-matching cuts on every remaining size-eight support.  The
full completions were then found by an independent exact edge-partition
model.

The theorem above does not rely on those searches:
`verify_r3_dead_seven_prefixes.py` is a standard-library semantic replay.
It checks the two seven-prefix decompositions, the full class-B support
matrices, (7), exhaustive blockage of all ten remaining supports, and both
explicit 17-matching completion certificates.
