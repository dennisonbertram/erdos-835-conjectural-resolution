# The generic rank-four two-Plücker link

Status: **the generic pair is classified, and an exact \(p=17\)
positive control proves that the rank-two oval argument does not extend
to it.  The control is not a decoder witness, and the unrestricted
generic rank-four ratio case remains open.  This does not solve
Erdős--Rosenfeld Problem #835.**

This note continues the Grassmann-line ratio exclusion in
`collaboration/multi_plucker_construction/grassmann_line_ratio_no_go.md`.
There the two contracted alternating forms span a line consisting
entirely of rank-two forms.  Here the endpoint forms are still
decomposable, but a generic member of their pencil has rank four.

The dependency-free exact audit is
`verify_rank4_plucker_ratio.py`.

## 1. Congruence classification of two decomposable forms

Let \(E\) be a vector space over a field of odd characteristic, and let
\[
 A=a_0\wedge a_1,\qquad B=b_0\wedge b_1               \tag{1}
\]
be independent decomposable two-forms.  Put
\[
 U=\langle a_0,a_1\rangle,\qquad W=\langle b_0,b_1\rangle.
\]
There are exactly two cases.

### Shared-factor case

If \(\dim(U+W)=3\), then \(U\cap W\) has dimension one.  After a
congruence change of basis,
\[
 A=x_0\wedge x_1,\qquad B=x_0\wedge x_2.              \tag{2}
\]
Every member \(sA+tB\) has rank two.  This is the Grassmann-line case
already excluded.

### Generic case

If \(\dim(U+W)=4\), then \(U\cap W=0\).  After congruence,
\[
 A=x_0\wedge x_1,\qquad B=x_2\wedge x_3.              \tag{3}
\]
The endpoints have rank two, while
\[
 (sA+tB)\wedge(sA+tB)=2st\,
 x_0\wedge x_1\wedge x_2\wedge x_3.                  \tag{4}
\]
Thus every member with \(st\ne0\) has rank four.  The two rank-drop
parameters are intrinsic, although a projective change of the pencil
may move them to any two points of \(\mathbb P^1\).

There is no third case.  If \(\dim(U+W)=2\), then
\(\bigwedge^2(U+W)\) is one-dimensional and \(A,B\) are proportional.

For two unrelated maximal-minor systems, contraction at a fixed
\((k-2)\)-face gives precisely a pair of the form (1).  Equation (3) is
therefore the genuinely new local frontier.

## 2. What a decoder would require at \(p=17\)

Let \(z_0,\ldots,z_{17}\in E\) be the eighteen remaining coordinate
vectors in a link and assume
\[
 (A(z_i,z_j),B(z_i,z_j))\ne(0,0)
 \quad(i\ne j).                                      \tag{5}
\]
The projective edge statistic is
\[
 \rho_{ij}=[A(z_i,z_j):B(z_i,z_j)]
 \in\mathbb P^1(\mathbb F_{17}).                     \tag{6}
\]

Any decoder \(h:\mathbb P^1(\mathbb F_{17})\to\mathbb F_{17}\) that
survives this link must make the seventeen edges at every vertex
rainbow.  In particular:

1. the raw labels (6) are pairwise distinct around every vertex;
2. if all eighteen projective labels occur, \(h\) has one double fibre
   \(\{\alpha,\beta\}\);
3. every label outside that double fibre is a perfect matching of
   \(K_{18}\), while the \(\alpha\)- and \(\beta\)-classes together form
   the seventeenth perfect matching.

In the shared-factor case, the zero graph of every pencil member is
parallelism among points of a projective line.  That rank-two geometry
created the oval/internal-point contradiction.

For a rank-four member, its zero relation is instead a symplectic
orthogonality relation in a four-dimensional space.  A perfect-matching
zero graph is no longer forced to arise from projective parallel pairs.
The next section gives an exact example.

## 3. Exact \(p=17\) rank-four perfect-matching control

Use the eighteen points of the normal rational curve
\[
 z_t=(1,t,t^2,t^3)\quad(t\in\mathbb F_{17}),\qquad
 z_\infty=(0,0,0,1).                                 \tag{7}
\]
Alternating-form coefficients below are listed in the order
\[
 01,\ 02,\ 03,\ 12,\ 13,\ 23.
\]
Define
\[
\begin{aligned}
 A&=(9,2,6,4,13,4),\\
 B&=(0,15,11,7,4,14).                                \tag{8}
\end{aligned}
\]
Both endpoints are visibly decomposable:
\[
\begin{aligned}
 A&=(1,0,9,8)\wedge(0,9,2,6),\\
 B&=(1,5,0,7)\wedge(0,0,15,11).                      \tag{9}
\end{aligned}
\]
The four displayed one-forms are independent, so this is the generic
case (3), not a hidden Grassmann line.

Their sum is
\[
 C=A+B=(9,0,0,11,0,1),                               \tag{10}
\]
whose Pfaffian is
\[
 \operatorname{Pf}(C)=9\ne0.
\]
Thus \(C\) has rank four.  More generally, every \(A+\lambda B\) with
\(\lambda\in\mathbb F_{17}^{\times}\) has rank four; only \(A\) and
\(B\) are rank two.

Take \(d=3\), a nonsquare modulo \(17\).  Direct expansion on (7) gives
\[
 C(z_s,z_t)=(t-s)(st-3)^2
 \quad(s,t\in\mathbb F_{17}),                         \tag{11}
\]
and
\[
 C(z_s,z_\infty)=s^2.                                \tag{12}
\]
Consequently the off-diagonal zero graph of this rank-four form is
\[
\begin{split}
 \{&\{0,\infty\},\{1,3\},\{2,10\},\{4,5\},\{6,9\},\\
   &\{7,15\},\{8,11\},\{12,13\},\{14,16\}\}.
                                                               \tag{13}
\end{split}
\]
It is a perfect matching of \(K_{18}\).  There are no fixed points in
the finite involution \(t\mapsto3/t\), precisely because \(3\) is a
nonsquare.

The endpoint feature pair is defined on all \(153\) edges.  On an edge
of (13), \(A\) and \(B\) are nonzero opposites, not simultaneous zeros.
Thus (13) is a valid zero class of a genuinely generic two-coordinate
ratio pencil.

This is the promised positive control: **a rank-four pencil member can
already satisfy exactly the perfect-matching condition that the decoder
would impose on a singleton label.**  The oval argument cannot replace
that member by nine projective parallel pairs, because its alternating
rank is four.

## 4. Why this control is not a decoder witness

The raw ratio-class sizes for (8) are
\[
\begin{split}
(&7,10,12,8,11,9,11,10,10,\\
 &7,7,8,7,0,7,11,9,9).                               \tag{14}
\end{split}
\]
Around the eighteen vertices, the numbers of distinct raw labels are
\[
(10,9,10,10,10,10,9,10,10,10,10,10,10,10,10,9,10,10).
                                                               \tag{15}
\]
Since a decoder cannot separate two equal raw labels, (15) is far short
of the required seventeen.  This exact control therefore proves only
that the *individual rank-four matching condition* survives.

The values \(9\) and \(10\) have a structural explanation.  For an
alternating form \(F\) on the normal rational curve,
\[
 F(z_s,z_t)=(t-s)q_F(s,t),                            \tag{16}
\]
where \(q_F(s,t)\), as a function of \(t\) with \(s\) fixed, has degree
at most two.  Hence a ratio of two such forms is a rational function of
degree at most two after cancelling \(t-s\).

Over a field of odd order, a separable degree-two rational map on
\(\mathbb P^1\) has a projective involution exchanging the two points
in each generic fibre.  That involution has either zero or two rational
fixed points.  Its image on \(\mathbb P^1(\mathbb F_{17})\) therefore
has respectively
\[
 {18\over2}=9\quad\hbox{or}\quad {18+2\over2}=10
\]
values.  This accounts exactly for (15).  A degree-one row can be
injective, but the displayed generic control has degree two at every
vertex.

## 5. What is proved and what remains open

Proved:

* the complete congruence/projective classification (2)--(4);
* the exact decoder constraints on a \(K_{18}\) link;
* an explicit generic rank-four pencil with no common-zero edge;
* an explicit rank-four member whose zero graph is a perfect matching;
* exact failure of the full decoder for that control.

Not proved:

* that every generic rank-four pencil fails the seventeen-label
  star-injectivity condition;
* that every possible set of eighteen vectors is equivalent to the
  normal rational curve (it is not);
* existence or nonexistence of a generic rank-four local decoder
  witness on another point configuration;
* any global colouring of \(J(32,16)\).

Thus the earlier oval proof is now sharply delimited.  It closes the
rank-two Grassmann line, while (13) demonstrates the first exact
rank-four phenomenon that survives it.  Simultaneously realizing the
other sixteen matching classes is the remaining two-coordinate local
problem, and global compatibility would still remain after that.

Run the audit with:

```bash
python3 -B \
  collaboration/rank4_plucker_ratio/verify_rank4_plucker_ratio.py
```
