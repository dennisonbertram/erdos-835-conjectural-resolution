# Triangle monodromy: cycle lengths forced by Odd-graph girth

Let
\[
  \pi:O_k=KG(2k-1,k-1)\longrightarrow K_{k+1}
\]
be a hypothetical cover, let the fibres be \(C_a\), and write
\[
 \tau_{abc}=m_{ca}m_{bc}m_{ab}\colon C_a\longrightarrow C_a
\]
for three distinct base colours.  This note records a sharp, elementary
cycle-length constraint on this permutation.  It is a constraint only; it
does **not** rule out a cover at \(k=16\).

## 1. A monodromy cycle lifts to a simple Odd-graph cycle

If \(x\in C_a\) has least \(\tau_{abc}\)-period \(r\), put
\[
 x_i=\tau_{abc}^i(x),\qquad y_i=m_{ab}(x_i),\qquad
 z_i=m_{bc}(y_i)\quad(0\leq i<r).
\]
Then
\[
 x_0,y_0,z_0,x_1,y_1,z_1,\ldots,x_{r-1},y_{r-1},z_{r-1},x_0 \tag{1}
\]
is a simple cycle of length \(3r\) in \(O_k\).

Indeed, consecutive terms are edges by the definitions of the matching
maps.  The \(x_i\)'s are distinct by minimality of the period; the \(y_i\)'s
and \(z_i\)'s are then distinct because matching maps are bijections.  Terms
from different displayed families lie in the distinct fibres \(C_a,C_b,C_c\),
so (1) has no other repetition.

## 2. Odd girth of the Odd graph

Put \(r_0=k-1\).  The odd girth of \(O_k=KG(2r_0+1,r_0)\) is
\[
  2r_0+1=2k-1. \tag{2}
\]
Here is a short proof.  Along a two-edge path of the Kneser graph, its two
endpoint \(r_0\)-sets both lie in the \((r_0+1)\)-element complement of the
middle set.  They therefore differ by at most one Johnson swap.  Along a
path of length \(2s\), its endpoints consequently have intersection at
least \(r_0-s\).  If this is the initial segment of an odd cycle of length
\(2s+1\), the last edge makes those endpoints disjoint, hence \(s\ge r_0\).
This proves the lower bound.  Equality is attained on \(\mathbb Z/(2r_0+1)\)
by the translates
\[
 \{i,i+2,\ldots,i+2(r_0-1)\}\qquad(i\in\mathbb Z/(2r_0+1)),
\]
whose consecutive terms are disjoint.

## 3. Consequence for triangle monodromy

Combining (1) and (2), every **odd** cycle of \(\tau_{abc}\) has length
\[
  r\ge \left\lceil\frac{2k-1}{3}\right\rceil. \tag{3}
\]
For the unresolved parameter \(k=16\), this says
\[
  r\text{ odd}\quad\Longrightarrow\quad r\ge 11. \tag{4}
\]
It also recovers that \(\tau_{abc}\) has no fixed point for \(k>2\): a fixed
point would give a triangle in \(O_k\).

The sheet number at \(k=16\) is
\[
 |C_a|=\frac{\binom{31}{15}}{17}=17,678,835,
\]
which is odd.  A fixed-point-free permutation of an odd set has at least
one odd cycle.  Therefore a hypothetical cover has the perhaps
counterintuitive necessary property
\[
 \boxed{\text{every triangle monodromy has an odd cycle, and each such
 odd cycle has length at least 11.}} \tag{5}
\]

In particular, an attempted proof which tries to derive that all triangle
monodromy cycles have even length cannot be a structural property of a
hypothetical \(O_{16}\) cover: it would itself be the desired contradiction.
The triangle factorisation
\[
 \sum_{b,c\ne a,\ b\ne c}P_{\tau_{abc}}=2R_1^a
\]
only fixes the first trace \(\sum\operatorname{tr}P_{\tau_{abc}}=0\); it
does not control the higher traces that would see the long odd cycles in
(5).  Thus exterior-power characters or mod-2 reductions applied solely to
that linear factorisation do not yet yield an obstruction.

`verify_triangle_monodromy_cycle_girth.py` checks the exact numerical
claims, the extremal odd-girth cycle, and direct small Odd-graph instances.
