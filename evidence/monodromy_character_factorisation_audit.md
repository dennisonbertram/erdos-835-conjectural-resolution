# Character traces of the triangle factorisation

For a fixed fibre of a hypothetical \(O_{16}\to K_{17}\) cover, write
\[
 T=\sum_{\alpha=1}^{240}P_{\tau_\alpha}=2R, \tag{1}
\]
where the \(240\) indices are the ordered pairs of the other base colours
and \(R=R_1^a\) is a zero-one graph of degree \(d=120\).  Reversing the
two intermediate colours pairs \(\tau_\alpha\) with
\(\tau_{\alpha^*}=\tau_\alpha^{-1}\).

This note checks the standard and exterior-square character consequences of
(1).  They give exact aggregate identities, but no parity contradiction
with the cycle-girth constraint: every \(\tau_\alpha\) has an odd cycle of
length at least \(11\).  An explicit permutation model proves that this is
not merely a failure of a loose estimate.

## 1. What the first two traces say

The absence of triangles in \(O_{16}\) makes every \(\tau_\alpha\)
fixed-point-free.  Therefore
\[
 \operatorname{tr}T=\sum_\alpha\operatorname{fix}(\tau_\alpha)=0,
\]
which is also immediate from the zero diagonal of \(2R\).  The standard
character \(\chi_{\rm std}(g)=\operatorname{fix}(g)-1\) consequently gives
only
\[
 \sum_\alpha\chi_{\rm std}(\tau_\alpha)=-240. \tag{2}
\]
It records the already-known absence of fixed points and nothing about long
odd cycles.

Squaring the *linear* identity gives the stronger exact equality
\[
 \sum_{\alpha,\beta}
   \operatorname{fix}(\tau_\alpha\tau_\beta)
 =\operatorname{tr}(T^2)=4\operatorname{tr}(R^2)=4nd=480n. \tag{3}
\]
The \(240\) inverse-paired ordered terms
\((\alpha,\alpha^*)\) already contribute \(240n\).  The remaining terms
have total fixed-point count \(240n\), a nonnegative aggregate condition.
Equation (3) has no mod-2 defect: both sides are even (indeed divisible by
\(4\)) for every \(n\).

## 2. Exterior square does not linearise the problem

For a permutation \(g\),
\[
 \chi_{\wedge^2}(g)=
 \frac{\operatorname{fix}(g)^2-\operatorname{fix}(g^2)}2. \tag{4}
\]
Thus a fixed-point-free permutation with no 2-cycles has individual
exterior-square character zero.  In particular this holds for an odd
full cycle, which is compatible with the girth lower bound.

It is invalid to apply \(\bigwedge^2\) termwise to (1).  The exact trace
identity is instead
\[
 \operatorname{tr}(\wedge^2T)
 =\frac{(\operatorname{tr}T)^2-\operatorname{tr}(T^2)}2
 =-2nd=-240n. \tag{5}
\]
The nonzero quantity in (5) comes entirely from mixed terms involving
*two different* triangle permutations.  It cannot be compared with
\(\sum_\alpha\chi_{\wedge^2}(\tau_\alpha)\).  Higher exterior powers have
the same issue: they are polynomial, rather than linear, in \(T\), and
introduce mixed products of several unrelated monodromies.

## 3. Exact countermodel for all one-fibre character constraints

The following construction has the exact form (1), while every displayed
triangle permutation is a single odd cycle.  It does not claim to be an
Odd-graph cover; it proves that the one-fibre factorisation and the
standard/exterior character traces considered here cannot themselves create the desired
contradiction.

Let \(n\ge121\) be odd.  Walecki's decomposition partitions \(K_n\) into
\((n-1)/2\) edge-disjoint Hamilton cycles.  Take any sixty of them, orient
them, and call their permutations \(g_1,\ldots,g_{60}\).  Let \(R\) be the
union of these sixty cycles.  It is a simple \(120\)-regular graph.  Now
make a list of 120 unoriented triangle factors by repeating each \(g_j\)
twice, and include the inverse factor for each orientation.  Then exactly
\[
 \sum_{j=1}^{60}2(P_{g_j}+P_{g_j}^{-1})=2R. \tag{6}
\]
Every \(g_j\) and \(g_j^{-1}\) is an \(n\)-cycle, hence is
fixed-point-free, has no 2-cycle, and has one odd cycle of length
\(n\ge121\).  For it,
\[
 \chi_{\rm std}(g_j)=-1,
 \qquad\chi_{\wedge^s}(g_j)=0\quad(1\le s<n), \tag{7}
\]
the latter because the nontrivial elementary symmetric functions of all
\(n\)-th roots of unity vanish.  Yet (2), (3), and (5) all hold exactly.

The open parameter's sheet number \(n=17,678,835\) is odd and vastly
larger than \(121\), so the construction applies at the same cardinality.
It is therefore a direct feasibility witness against any obstruction using
only (1), standard/exterior characters, products obtained by expanding
(1), and the long-odd-cycle condition.

## 4. Different base fibres

For a second fibre \(C_b\), transporting its identity by a matching gives
\[
 m_{ba}(2R_1^b)m_{ab}=
 \sum_{c,d\ne b,\ c\ne d}
 m_{ba}P_{\tau_{bcd}}m_{ab}. \tag{8}
\]
There is no relation in the triangle factorisation alone between the
transported graph on the left of (8) and \(R_1^a\).  Taking traces of a
product of (1) and (8) simply counts fixed points of six-step lifted
walks with the indicated base colour word.  Such walks may close in
\(O_{16}\) (the graph has 6-cycles), and their nonnegative counts are not
specified by the one-fibre identity.  Consequently cross-fibre character
traces require genuinely new labelled incidence information, beyond (1).

The companion verifier constructs (6) for \(n=121\) with integer matrices
and checks every displayed character and trace identity.
