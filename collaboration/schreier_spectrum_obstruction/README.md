# Schreier-spectrum modules beyond the endpoint bound

## Status and scope

Assume throughout that an even-\(k\) cover

\[
O_k=KG(2k-1,k-1)\longrightarrow K_{k+1}
\]

exists, fix one fibre \({\cal C}\), and let \(R\) join two fibre blocks
when their intersection has size one.  Put \(v=2k-1\), \(r=k-1\), and
\(n=|{\cal C}|=\binom vr/(k+1)\).

The results below are exact necessary conditions.  They do **not** construct
or exclude the \(k=16\) cover and do **not** settle Erdős--Rosenfeld problem
835.

## 1. The strengthened spectrum

Let

\[
{\cal H}_0=\langle{\bf1}\rangle .
\]

Let \({\cal H}_1\) be the span of the point-incidence differences
\(f_p-f_q\), where \(f_p(B)=[p\in B]\).  For \(k\ge6\), let
\({\cal H}_2\) be the orthogonal complement of the point-incidence space
inside the span of the pair-incidence columns
\(f_{\{p,q\}}(B)=[\{p,q\}\subset B]\).

### Theorem (even \(k\ge6\))

The three spaces are mutually orthogonal and \(R\)-invariant, and

\[
\begin{array}{c|c|c}
\text{space}&\text{dimension}&R\text{-eigenvalue}\\ \hline
{\cal H}_0&1&\binom{k}{2}\\[2mm]
{\cal H}_1&2k-2&
\displaystyle\frac{-k^2+4k-2}{2}\\[2mm]
{\cal H}_2&(2k-1)(k-2)&
\displaystyle\frac{(k-2)(k-5)}2 .
\end{array}
\tag{1}
\]

On

\[
{\cal K}=({\cal H}_0\oplus{\cal H}_1\oplus{\cal H}_2)^\perp
\]

the spectrum of \(R\) is contained in

\[
\boxed{
\frac{-k^2+6k-6}{2}\leq
\operatorname{Spec}(R|_{\cal K})\leq
\frac{k^2-5k-12}{2}.}
\tag{2}
\]

For \(k=16\), this becomes

\[
\boxed{
\operatorname{Spec}(R)
=\{120^1,(-97)^{30},77^{434}\}
\mathbin{\uplus}\Lambda,\qquad
\Lambda\subseteq[-83,82].}
\tag{3}
\]

Here the displayed \(434\)-dimensional pair module is forced, but \(77\)
could also occur in \(\Lambda\).  In contrast, (2) proves that \(-97\) has
**exactly** multiplicity \(30\).  Thus the previous interval
\([-97,101]\) improves to a separated least eigenspace, a gap of fourteen
above it, and nonprincipal upper bound \(82\).

The \(k=6\) control closes exactly.  The derived Witt fibre has
\(n=66\), and (1) accounts for dimensions \(1,10,44\) with eigenvalues
\(15,-7,2\).  The remaining dimension is eleven, while both endpoints in
(2) equal \(-3\).  Hence the theorem recovers

\[
15^1,\qquad(-7)^{10},\qquad2^{44},\qquad(-3)^{11},
\]

the independently known exact Witt spectrum.  The pair-module statement
is not asserted at \(k=4\): there the design has strength only two and the
full pair-incidence rank used below is unavailable.

## 2. Compressed Odd idempotents

Let \(\mathcal A\) be the adjacency matrix of \(O_k\), let
\(\iota:\mathbb R^{\cal C}\to\mathbb R^{V(O_k)}\) extend a fibre vector by
zero, and let \(E_j\) be the global spectral idempotent for

\[
\theta_j=(-1)^j(k-j).
\]

The fibre is an \(S(k-2,k-1,2k-1)\).  If \(2j\le k-2\), the design
averaging identity for products of two degree-\(j\) harmonic functions
gives

\[
\boxed{\iota^*E_j\iota=\frac1{k+1}P_{{\cal H}_j},}
\tag{4}
\]

where \({\cal H}_j\) is the restriction of the degree-\(j\) Johnson
harmonic space and \(P_{{\cal H}_j}\) is its orthogonal projector.

Indeed, for global degree-\(j\) harmonics \(h,g\), their product has
incidence degree at most \(2j\).  The design equations therefore give

\[
\sum_{B\in{\cal C}}h(B)g(B)
=\frac{|{\cal C}|}{\binom vr}
  \sum_{B\in\binom{[v]}r}h(B)g(B)
=\frac1{k+1}\langle h,g\rangle .
\]

Thus restriction is a \(1/\sqrt{k+1}\)-scaled isometry.  Multiplying the
restriction operator by its adjoint proves (4).  In particular, a fibre
vector orthogonal to \({\cal H}_1\) has no global
\(\theta_1=-(k-1)\) component, and one orthogonal to \({\cal H}_2\) has no
global \(\theta_2=k-2\) component.

There is also a direct endpoint-budget audit.  The global multiplicity of
\(-(k-1)\) is \(2k-2\), so vertex transitivity gives

\[
\operatorname{tr}(\iota^*E_1\iota)=\frac{2k-2}{k+1}.
\tag{5}
\]

Every eigenvector at the old lower endpoint has forced \(E_1\)-weight
\(1/(k+1)\).  Hence its multiplicity is at most \(2k-2\); the point
module supplies \(2k-2\) such vectors.  Equality exhausts (5), proving
both exact multiplicity and the absence of an \(E_1\) component on the
orthogonal complement.

## 3. The pair module

Fix a block \(B\), and write \(Y=[v]\setminus B\), so \(|Y|=k\).
The \(R\)-neighbours of \(B\) are indexed by the two-subsets \(e\) of
\(Y\):

\[
D_e=(Y\setminus e)\cup\{\phi_B(e)\},\qquad \phi_B(e)\in B.
\tag{6}
\]

Indeed, \(Y\setminus e\) is a \((k-2)\)-set and therefore has a unique
design extension.  Its last point cannot remain in \(Y\), because two
blocks in one cover fibre are never disjoint.  Hence its last point lies
in \(B\), as asserted.

The map \(\phi_B\) is a one-factorisation of \(K_Y\).  If two incident
edges had the same value, the corresponding design blocks would share a
\((k-2)\)-subset.  There are \(k-1\) values and \(\binom k2\) edges, so
every colour class is a perfect matching.

The point-module action now follows directly.  If \(p\in B\), exactly the
\(k/2\) edges in the factor labelled \(p\) give \(R\)-neighbours
containing \(p\).  If \(p\notin B\), the missing edge must avoid \(p\),
giving \(\binom{k-1}{2}\) choices.  Therefore
\[
 Rf_p=\binom{k-1}{2}{\bf1}
      +\frac{-k^2+4k-2}{2}f_p,
\]
which proves the \({\cal H}_1\) eigenvalue in (1).

For a fixed pair \(S\), the number of neighbours \(D\) of \(B\) containing
\(S\) depends only on \(i=|S\cap B|\):

\[
F_0=\binom{k-2}{2},\qquad F_1=\frac{k-2}{2},\qquad F_2=0.
\tag{7}
\]

For \(i=0\), the missing edge in (6) must avoid the two points of \(S\).
For \(i=1\), it lies in one fixed perfect matching and must avoid the one
outside point.  Formula (7) implies

\[
Rf_S=F_0{\bf1}+(F_1-F_0)(f_p+f_q)
       +\frac{(k-2)(k-5)}2 f_S ,
\tag{8}
\]

for \(S=\{p,q\}\).  Hence the pair-incidence span is invariant and \(R\)
acts on its quotient by the point span as the scalar in (1).  Since the
design has strength at least four, its pair-incidence matrix has full
column rank \(\binom v2\).  This gives

\[
\dim{\cal H}_2=\binom v2-v=(2k-1)(k-2).
\]

One direct rank audit is to form the pair Gram matrix.  Its entries are
\(\lambda_2,\lambda_3,\lambda_4\) according as two indexed pairs are
equal, meet in one point, or are disjoint.  It is \(1/(k+1)\) times the
corresponding Gram matrix for all \(r\)-subsets, by strength four.  The
latter is positive definite (equivalently, use the three eigenvalues of
the triangular graph \(T(v)\)), so the asserted rank is exact.

## 4. Exact two-step intersection algebra

Let \(A_s\) denote the zero-one matrix on \({\cal C}\) for block
intersection \(s\).  The one-factorisation (6) also determines every
two-step endpoint type.

For two distinct edges \(e,f\) of \(K_k\), the corresponding neighbours
of \(B\) intersect in:

* \(k-3\) points if \(e,f\) are incident; or
* \(k-3\) points if \(e,f\) are disjoint and have the same factor colour;
* \(k-4\) points otherwise.

Consequently, for every fixed first edge there are

\[
h=\frac{5(k-2)}2
\quad\text{endpoints of intersection }k-3
\]

and

\[
\ell=\frac{(k-2)(k-4)}2
\quad\text{endpoints of intersection }k-4.
\tag{9}
\]

The corresponding design intersection numbers are

\[
n_{k-3}=\frac{k(k-1)(k-2)}4,
\qquad
n_{k-4}=\frac{k(k-1)(k-2)(k-3)(k-4)}{36}.
\tag{10}
\]

For completeness,
\(\lambda_{k-3}=(k+2)/2\), so choosing the \((k-3)\)-subset inside a
fixed block and excluding the block itself gives the first formula.
Similarly
\(\lambda_{k-4}=(k+3)(k+2)/6\); subtracting the already-counted
\((k-3)\)-intersection blocks gives the second.

There is a sharper pairwise statement.  If blocks \(B,C\) meet in
\(k-3\) points, a common \(R\)-neighbour is of one of two forms.  With

\[
I=B\cap C,\quad U=B\setminus C,\quad V=C\setminus B,\quad
W=X\setminus(B\cup C),
\]

it is either \(W\cup\{q\}\), \(q\in I\), or
\((W\setminus\{w\})\cup\{u,v\}\), with \(u\in U,v\in V\).
The first type occurs at most once by the Steiner property.  For each of
the four pairs \((u,v)\), the second type also occurs at most once, again
because two candidates would share a \((k-2)\)-subset.  Thus there are at
most five common neighbours.

On the other hand, (9) counts

\[
\binom k2 h=5n_{k-3}
\]

two-step walks from each \(B\) to the \(n_{k-3}\) blocks in that relation.
The upper bound is therefore attained term by term:

\[
\boxed{(R^2)_{BC}=5\quad\text{whenever }|B\cap C|=k-3.}
\tag{11}
\]

If \(|B\cap C|=k-4\), every common neighbour is
\(W\cup\{u,v\}\), with \(u\in U\), \(v\in V\), and the selected pairs
form a matching between two three-sets.  Hence the common-neighbour count
is in \(\{0,1,2,3\}\).

Define \(Q\) to equal \(R^2\) on the \(k-4\) intersection relation and
zero elsewhere.  Equations (9)--(11) give the exact matrix identity

\[
\boxed{
R^2=\binom k2 I+5A_{k-3}+Q,\qquad
0\le Q_{BC}\le3,\qquad
Q{\bf1}=
\frac{k(k-1)(k-2)(k-4)}4{\bf1}.}
\tag{12}
\]

At \(k=16\),

\[
\boxed{
R^2=120I+5A_{13}+Q,\quad
A_{13}{\bf1}=840{\bf1},\quad
\operatorname{supp}Q\subseteq A_{12},\quad
Q_{BC}\in\{0,1,2,3\},\quad
Q{\bf1}=10080{\bf1}.}
\tag{13}
\]

In particular, every intersection-thirteen pair has five common
neighbours.  These pairs alone force

\[
2100n=37\,125\,553\,500
\]

four-cycles in \(R\).  The intersection-twelve contribution is
nonnegative and at most \(2520n\), so the rigorous structural bounds are

\[
37\,125\,553\,500\le \#C_4(R)\le81\,676\,217\,700
\tag{14}
\]

and, equivalently,

\[
45\,480n\le\operatorname{tr}R^4\le65\,640n.
\tag{15}
\]

Here one uses

\[
\#C_4(R)=\frac12\sum_{\{B,C\}}\binom{(R^2)_{BC}}2.
\]

The \(A_{13}\) contribution is exactly \(2100n\).  On the support of
\(Q\), the inequality \(q(q-1)\le2q\) for
\(q\in\{0,1,2,3\}\) bounds the extra contribution by \(2520n\), proving
(14).  The standard identity
\(\operatorname{tr}R^4=nd(2d-1)+8\#C_4(R)\) gives (15).

This large forced four-cycle population is compatible with odd girth:
only odd cycles are excluded.

### A fourth global compression

The first genuinely higher compressed Odd moment is also exact.  For
\(k\ge6\), the Odd graph has odd girth at least eleven and no four-cycles,
so a four-walk between fibre vertices can only end at even distance.
Two fibre blocks at Odd distance four meet in \(k-3\) points.  In the Odd
intersection array,
\(c_1c_2c_3c_4=1\cdot1\cdot2\cdot2=4\), while the number of closed
four-walks at a vertex is \(k(2k-1)\).  Hence

\[
\boxed{
\iota^*\mathcal A^4\iota=k(2k-1)I+4A_{k-3}.}
\tag{16}
\]

If \(x\perp{\bf1}\), its global spectral measure has second moment \(k\)
and no principal Odd component.  Hence

\[
k^2\le\langle\mathcal A^4\rangle_x\le k(k-1)^2.
\]

Combining this with (16) gives the PSD/Rayleigh constraint

\[
\boxed{
-\frac{k(k-1)}4\le
\operatorname{Spec}(A_{k-3}|_{{\bf1}^\perp})
\le\frac{k(k^2-4k+2)}4.}
\tag{17}
\]

At \(k=16\), \(A_{13}\) is \(840\)-regular and every nonprincipal
eigenvalue lies in \([-60,776]\).  In particular it is connected.  This
is a genuine fourth-moment consequence, but it is compatible with (12)
and does not produce a contradiction.

## 5. Reduced-support sign polynomials

For an \(R\)-eigenvector \(x\perp{\bf1}\), extended by zero to the Odd
graph, local bijectivity gives

\[
\iota^*\mathcal A\iota=0,\qquad
\iota^*\mathcal A^2\iota=kI,\qquad
\iota^*\mathcal A^3\iota=2R.
\]

The second identity holds because each vertex has \(k\) two-step returns
and two distinct vertices in one fibre cannot share a neighbour.  For the
third, every three-step return to the fibre projects to an ordered base
triangle, and the triangle-lift identity
\(\sum_{b,c}P_{\tau_{abc}}=2R\) counts its two orientations.  Hence

\[
\langle\mathcal A\rangle_x=0,\qquad
\langle\mathcal A^2\rangle_x=k,\qquad
\langle\mathcal A^3\rangle_x=2\mu .
\tag{18}
\]

If \(x\in{\cal K}\), (4) removes the two global spectral points
\(-(k-1)\) and \(k-2\).  On the remaining Odd spectrum, both

\[
q_-(t)=(t+k-3)(t-2)(t+1)
\]

and

\[
q_+(t)=(k-4-t)(t+3)(t+1)
\]

are nonnegative.  Substitution of (18) gives

\[
0\le\langle q_-(\mathcal A)\rangle_x
=2\mu+k^2-6k+6
\]

and

\[
0\le\langle q_+(\mathcal A)\rangle_x
=-2\mu+k^2-5k-12,
\]

which is (2).

These two bounds are optimal for the stated three-moment information.
At the lower endpoint the unique extremal measure is supported on
\(\{-(k-3),2,-1\}\); at the upper endpoint it is supported on
\(\{k-4,-3,-1\}\).  Thus a higher-degree global sign polynomial cannot
improve (2) unless one first supplies an additional compressed moment or
relation beyond (18).

At \(k=16\), the residual space \({\cal K}\) has dimension
\(17\,678\,370\).  Removing the three forced modules from the exact traces
gives

\[
\operatorname{tr}(R|_{\cal K})=-30\,628,\qquad
\operatorname{tr}\bigl((R|_{\cal K})^2\bigr)=2\,118\,590\,344,
\tag{19}
\]

and, for \(j=3,5,7,9\),

\[
\operatorname{tr}\bigl((R|_{\cal K})^j\bigr)
=30\cdot97^j-434\cdot77^j-120^j.
\tag{20}
\]

The exact values in (20) are audited by the verifier.  They are
bookkeeping identities rather than a contradiction: the residual even
moments from degree four onward are not fixed by these equations.

## 6. The odd-girth condition is locally automatic

The odd-girth-\(11\) statement at \(k=16\) is correct, but for the
intersection-one graph it follows already from elementary set geometry;
it is not an additional cover-specific restriction.

Put

\[
\delta(B,C)=r-|B\cap C|=\tfrac12|B\mathbin\triangle C|.
\]

If \(B-D-C\) is a two-step \(R\)-walk, then
\(B\setminus D\) and \(C\setminus D\) are two \((k-2)\)-subsets of the
\(k\)-set \(X\setminus D\).  They meet in at least \(k-4\) points, so
\(\delta(B,C)\le3\).

In an odd cycle of length \(2m+1\), group the path opposite one closing
edge into \(m\) two-steps.  The triangle inequality gives
\(\delta\le3m\), while the closing \(R\)-edge has
\(\delta=r-1=k-2\).  Therefore

\[
3m\ge k-2,\qquad
g_{\rm odd}(R)\ge2\left\lceil\frac{k-2}{3}\right\rceil+1.
\tag{21}
\]

For \(k=16\), (21) is exactly \(g_{\rm odd}(R)\ge11\), hence
\(\operatorname{tr}R^j=0\) for \(j=1,3,5,7,9\).  The same formula gives
the sharp small controls \(3\) at \(k=4\) and \(5\) at \(k=6\).

## 7. Remaining gap

The module splitting, reduced interval, and two-step algebra are
substantially stronger than the original scalar endpoint theorem, but they
remain feasible necessary conditions.  In particular, they do not
determine the spectrum on \({\cal K}\), force a forbidden multiplicity,
or contradict the vanishing odd traces through degree nine.  The
odd-girth equations themselves are already implied by the set geometry in
Section 6.  A contradiction would need a further cover-specific constraint
coupling \({\cal K}\) to higher compressed Odd moments or to joint
intersection matrices beyond (12).

## 8. Exact verification

Run

```sh
python3 -B \
  collaboration/schreier_spectrum_obstruction/verify_schreier_spectrum_obstruction.py
```

The standard-library verifier checks the degree-one and degree-two Gram
eigenvalues, the \(1/(k+1)\) idempotent normalisation, both forced
modules, both reduced-support extremal measures, the two-step intersection
arithmetic, the fourth-moment bounds, the exact Witt control, the
\(k=16\) four-cycle bounds, and all displayed residual moments.
