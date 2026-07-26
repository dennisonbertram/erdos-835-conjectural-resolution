# Triangle-monodromy Schreier spectrum

## Result

Assume that an even-\(k\) cover with \(k\ge4\)

\[
\pi:O_k=KG(2k-1,k-1)\longrightarrow K_{k+1}
\]

exists, fix a colour \(a\), and let \(R=R_1^a\) be the graph on the fibre
\(C_a\) in which \(A\sim D\) when \(|A\cap D|=1\).  The triangle
factorisation

\[
\sum_{\substack{b,c\ne a\\b\ne c}}P_{\tau_{abc}}=2R
\tag{1}
\]

makes \(2R\) the adjacency operator of the triangle-monodromy Schreier
multigraph.

The full Odd-graph spectrum forces every nonprincipal eigenvalue \(\mu\) of
\(R\) into the exact interval

\[
\boxed{
\frac{-k^2+4k-2}{2}\ \leq\ \mu\ \leq\
\frac{k^2-3k-6}{2}.}
\tag{2}
\]

The lower endpoint is not merely a bound.  Every fibre is a Steiner system
\(S(k-2,k-1,2k-1)\), and its point-incidence difference space has dimension
\(2k-2\) and eigenvalue

\[
\mu_{\rm pt}=\frac{-k^2+4k-2}{2}.
\tag{3}
\]

Consequently the least eigenvalue of \(R\) is exactly (3), with multiplicity
at least \(2k-2\).

For \(k=16\), a hypothetical fibre graph must therefore have

\[
|C_a|=17{,}678{,}835,\qquad d=120,
\]

\[
\boxed{\operatorname{Spec}(R)\setminus\{120\}\subseteq[-97,101],\qquad
-97\text{ has multiplicity at least }30.}
\tag{4}
\]

Equivalently, the nonprincipal spectrum of the monodromy sum in (1) lies in
\([-194,202]\), with \(-194\) of multiplicity at least \(30\).

Odd girth supplies a separate joint constraint which is stronger than the
previous single-permutation period bound:

\[
\boxed{\text{every product of }1,3,5,7,\text{ or }9
\text{ triangle monodromies based at }a\text{ is a derangement}.}
\tag{5}
\]

Equivalently, the simple Schreier graph \(R\) has odd girth at least \(11\),
so

\[
\operatorname{tr}R^3=\operatorname{tr}R^5
=\operatorname{tr}R^7=\operatorname{tr}R^9=0.
\tag{6}
\]

This is a new necessary spectral restriction, not an obstruction.  The
small-\(k\) controls below satisfy it, and no existence or nonexistence claim
for \(k=16\) follows from (4) alone.

## 1. Gauge the cover by one fibre

For \(b\ne a\), identify \(C_b\) with \(C_a\) using the matching \(m_{ba}\).
In these coordinates the \(a\)-to-\(b\) matching is the identity, while the
\(b\)-to-\(c\) block is

\[
m_{ca}m_{bc}m_{ab}=\tau_{abc}.
\]

Thus the adjacency matrix \(\mathcal A\) of the cover has block form

\[
\mathcal A=
\begin{pmatrix}
0&I&I&\cdots&I\\
I&0&P_{\tau_{ab_1b_2}}&\cdots&P_{\tau_{ab_1b_k}}\\
I&P_{\tau_{ab_2b_1}}&0&\cdots&P_{\tau_{ab_2b_k}}\\
\vdots&\vdots&\vdots&\ddots&\vdots\\
I&P_{\tau_{ab_kb_1}}&P_{\tau_{ab_kb_2}}&\cdots&0
\end{pmatrix}.
\tag{7}
\]

The relation \(\tau_{acb}=\tau_{abc}^{-1}\) makes (7) symmetric.  Summing
its lower-right off-diagonal blocks gives (1).

Let

\[
W=\{x\in\mathbb R^{C_a}:\langle x,\mathbf1\rangle=0\}.
\]

Every permutation block preserves \(W\).  The fibre-constant complement is
the ordinary \(K_{k+1}\) quotient.  On \(W^{k+1}\), the distinct eigenvalues
of \(\mathcal A\) are therefore the nonprincipal Odd-graph eigenvalues

\[
\Theta_k=\{\,(-1)^j(k-j):1\le j\le k-1\,\}
=\{-(k-1),k-2,-(k-3),\ldots,2,-1\}.
\tag{8}
\]

The usual multiplicities are
\(\binom{2k-1}{j}-\binom{2k-1}{j-1}\); removing the quotient only decreases
the multiplicity of \(-1\), not the set (8).

## 2. Odd girth for every monodromy word

Let

\[
\alpha_t=(b_t,c_t),\qquad
\tau_{\alpha_t}=\tau_{ab_tc_t},
\]

be any sequence of \(s\) ordered base triangles.  If

\[
\tau_{\alpha_s}\cdots\tau_{\alpha_1}
\]

fixes a sheet \(A\in C_a\), concatenating the corresponding triangle lifts
gives a closed walk of length \(3s\) in \(O_k\).  No reduced-word assumption
is needed: every closed odd walk contains an odd cycle no longer than the
walk.

Since the odd girth of \(O_k\) is \(2k-1\), every such product is a
derangement whenever \(s\) is odd and

\[
3s<2k-1.
\tag{9}
\]

This applies to arbitrary mixed products, not only powers of one
\(\tau_{abc}\).  In operator form, every summand in

\[
\operatorname{tr}\left(
 \sum_{b,c}P_{\tau_{abc}}
\right)^s
=2^s\operatorname{tr}R^s
\tag{10}
\]

is a nonnegative fixed-point count and is zero under (9).  Thus \(R\) has
no closed odd walk of such a length.  At \(k=16\), the first permitted odd
length is \(11\), proving (5)--(6).

This is the odd-girth input missing from a purely linear use of (1): it
controls every short odd word in the triangle generators simultaneously.

## 3. Three exact moments

Take an \(R\)-eigenvector \(x\in W\), \(Rx=\mu x\), and regard it as a
vector supported only on \(C_a\).  Local bijectivity and (1) give

\[
\frac{\langle x,\mathcal A x\rangle}{\langle x,x\rangle}=0,
\qquad
\frac{\langle x,\mathcal A^2 x\rangle}{\langle x,x\rangle}=k,
\qquad
\frac{\langle x,\mathcal A^3 x\rangle}{\langle x,x\rangle}=2\mu.
\tag{11}
\]

The first equality uses the empty diagonal fibre block.  A two-step walk
\(a\to b\to a\) returns along the inverse matching, so the \(aa\)-block of
\(\mathcal A^2\) is \(kI\).  The \(aa\)-block of
\(\mathcal A^3\) is the left side of (1), namely \(2R\).

This turns the joint triangle-monodromy spectrum into a three-moment problem
on the finite set (8).

## 4. Two sign polynomials

On every point of \(\Theta_k\), both polynomials

\[
p_-(t)=(t+k-1)(t-2)(t+1),
\tag{12}
\]

\[
p_+(t)=(k-2-t)(t+3)(t+1)
\tag{13}
\]

are nonnegative.  For (12), the negative spectral points lie between
\(-(k-1)\) and \(-1\), while the positive points are at least \(2\).
For (13), the negative points are \(-1\) or at most \(-3\), and the positive
points are at most \(k-2\).

Functional calculus on \(\mathcal A|_{W^{k+1}}\) therefore gives

\[
\langle x,p_-(\mathcal A)x\rangle\ge0,\qquad
\langle x,p_+(\mathcal A)x\rangle\ge0.
\]

Substitute the three moments (11):

\[
2\mu+k(k-2)-2(k-1)\ge0,
\]

\[
-2\mu+k(k-6)+3(k-2)\ge0.
\]

These are exactly the lower and upper inequalities in (2).  Unlike an
interval-only interlacing estimate, this argument uses the alternating,
integer support of the complete Odd-graph spectrum.

## 5. The lower endpoint is forced

A perfect code in \(O_k\) is an
\(S(k-2,k-1,2k-1)\).  Indeed, two code blocks cannot share a
\((k-2)\)-subset, since they would then have a common Odd-graph neighbour.
Counting incidences between code blocks and \((k-2)\)-subsets shows that
every such subset occurs exactly once.

Put \(r=k-1\) and \(v=2k-1\).  The number of design blocks containing a
fixed \(s\)-set, for \(s\le r-1\), is

\[
\lambda_s=
\frac{\binom{v-s}{r-1-s}}{r-s},
\tag{14}
\]

and a specified block itself has \(\lambda_r=1\).

Fix a block \(B\) and a point \(p\).  If \(p\in B\), inclusion-exclusion
over \(B\setminus\{p\}\) gives the number of \(R\)-neighbours of \(B\)
which contain \(p\):

\[
A_{\rm in}=
\sum_{j=0}^{r-1}(-1)^j\binom{r-1}{j}\lambda_{j+1}
=\frac{k}{2}.
\tag{15}
\]

If \(p\notin B\), choose the unique point of \(D\cap B\) first.  The last
two inclusion-exclusion terms vanish: one would prescribe more than \(r\)
points, and the other would prescribe a second block sharing \(r-1\)
points with \(B\).  Hence

\[
A_{\rm out}=
r\sum_{j=0}^{r-3}(-1)^j\binom{r-1}{j}\lambda_{j+2}
=\binom{k-1}{2}.
\tag{16}
\]

The binomial simplifications in (15)--(16) are checked exactly by the
verifier.

For the point-incidence column
\(f_p(B)=[p\in B]\), equations (15)--(16) say

\[
Rf_p=A_{\rm out}\mathbf1+
(A_{\rm in}-A_{\rm out})f_p.
\tag{17}
\]

Thus every point difference \(f_p-f_q\) is an eigenvector with eigenvalue

\[
A_{\rm in}-A_{\rm out}
=\frac{-k^2+4k-2}{2}.
\]

The point-incidence Gram matrix has a positive eigenvalue on the
\((2k-2)\)-dimensional point-difference space, so these vectors have that
full dimension.  This proves (3), and (2) now proves that it is the exact
least eigenvalue.

There is an additional equality consequence.  Since (12) is positive
semidefinite and vanishes on every point-difference vector, each such vector,
when extended by zero outside \(C_a\), has global spectral support only at

\[
\boxed{\{-(k-1),\,2,\,-1\}.}
\tag{18}
\]

The squared projection weights, divided by the squared norm of the vector,
are forced by (11):

\[
\frac1{k+1},\qquad
\frac{2k-1}{3(k+1)},\qquad
\frac13,
\tag{19}
\]

respectively.  Formulae (18)--(19) are a sharper exact restriction than the
scalar endpoint alone.

## 6. Consequences at \(k=16\)

The triangle-monodromy Schreier graph \(R\) must satisfy all of the following:

* it is \(120\)-regular on \(17{,}678{,}835\) vertices;
* it is connected, because every nonprincipal eigenvalue is at most
  \(101<120\);
* its least eigenvalue is exactly \(-97\), with multiplicity at least \(30\);
* its point-difference vectors have global Odd-graph spectral weights
  \(1/17,31/51,1/3\) on eigenvalues \(-15,2,-1\);
* every product of \(1,3,5,7,\) or \(9\) triangle generators is fixed-point
  free, and \(R\) has odd girth at least \(11\);
* its Hoffman bound is
  \[
  \alpha(R)\le\frac{97}{217}|C_a|;
  \]
* it is triangle-free.  If adjacent blocks \(B,D\) have
  \(|B\cap D|=1\), only two ground points lie outside \(B\cup D\).
  A common \(R\)-neighbour \(E\) can use at most one point of \(B\) and at
  most one point of \(D\), hence at most four points in total (only three if
  it uses \(B\cap D\)).  This is impossible for a
  \((k-1)\)-block when \(k\ge6\).

The last property is design-theoretic and independent of the spectral
argument.  Together these give a concrete, exact target for any future
monodromy construction or contradiction.

## 7. Small-\(k\) controls

The verifier keeps genuine covers separate from single-code controls.

* \(k=2\): \(O_2=K_3\) is the genuine one-sheet cover.  Here \(W=0\), so
  there is no nonprincipal fibre spectrum to constrain.
* \(k=4\): the Fano \(S(2,3,7)\) code has \(R=K_7\), with spectrum
  \(6^1,(-1)^6\).  Both endpoints of (2) equal \(-1\), and its odd
  girth \(3\) meets the bound \(3s\ge7\).
* \(k=6\): the Witt \(S(4,5,11)\) code has exact spectrum
  \[
  15^1,\quad2^{44},\quad(-3)^{11},\quad(-7)^{10}.
  \]
  The interval (2) is \([-7,6]\), the ten-dimensional point module
  attains its lower endpoint, and its odd girth is \(5\), meeting
  \(3s\ge11\).

The \(k=4,6\) objects are individual perfect codes, not full covers.  They
show that the new fibre-spectrum conditions are sharp and compatible with
the known local controls; they do not establish the missing partitions.

## 8. Reproduction and scope

Run the standard-library verifier:

```sh
python3 -B \
  collaboration/triangle_monodromy_spectrum/verify_triangle_monodromy_spectrum.py
```

It checks the Odd spectra and both sign polynomials at \(k=4,6,16\), the
Steiner inclusion-exclusion counts and endpoint equality, the Fano control,
and the exact four-eigenvalue Witt control.

This note does not prove that the permutations in (1) exist, does not
construct a cover, and does not settle Erdős--Rosenfeld problem 835.
