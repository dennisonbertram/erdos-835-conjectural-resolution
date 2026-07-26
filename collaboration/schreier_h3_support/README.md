# Degree-three Schreier support and the one-operator frontier

## Status and scope

Assume that an unrestricted \(k=16\) cover

\[
O_{16}=KG(31,15)\longrightarrow K_{17}
\]

exists.  Fix one fibre \({\cal C}\), let \(R\) join two fibre blocks
meeting in one point, and write \(A_s\) for the zero-one matrix for
fibre-block intersection \(s\).  Let \(\mathcal A\) be the global Odd
graph adjacency matrix and let
\(\iota:\mathbb R^{\cal C}\to\mathbb R^{V(O_{16})}\) extend a fibre
vector by zero.

This note proves exact necessary consequences on the degree-three
harmonic space.  They do **not** construct or exclude a cover and do not
settle Erdős--Rosenfeld problem 835.

## 1. A five-point global support theorem

Let \(E_j\) be the global Johnson/Odd idempotent with eigenvalue

\[
\theta_j=(-1)^j(16-j),
\]

and let \({\cal H}_3\) be the restriction to \({\cal C}\) of the
degree-three Johnson harmonic space.  Its dimension is

\[
d_3=\binom{31}{3}-\binom{31}{2}=4030.
\]

The fibre is an \(S(14,15,31)\).  If \(f\) is a global degree-three
harmonic and \(g\) is a global degree-\(j\) harmonic with \(j\leq 11\),
then \(fg\) has incidence degree at most \(3+j\leq14\).  Design
quadrature therefore gives

\[
\sum_{B\in{\cal C}}f(B)g(B)
=\frac1{17}\sum_{B\in\binom{[31]}{15}}f(B)g(B).
\]

The right side vanishes unless \(j=3\).  Restriction on the degree-three
space is a \(1/\sqrt{17}\)-scaled isometry, so for every
\(x\in{\cal H}_3\),

\[
E_j\iota x=0\quad(0\leq j\leq11,\ j\ne3),
\qquad
\|E_3\iota x\|^2=\frac1{17}\|x\|^2.
\]

Consequently,

\[
\boxed{\iota{\cal H}_3
\subseteq E_3\oplus E_{12}\oplus E_{13}\oplus E_{14}\oplus E_{15}.}
\tag{1}
\]

Equivalently,

\[
\boxed{
(\mathcal A+13I)(\mathcal A-4I)(\mathcal A+3I)
(\mathcal A-2I)(\mathcal A+I)\,\iota P_3=0,
}
\tag{2}
\]

where \(P_3\) is the orthogonal projector onto \({\cal H}_3\).
This conclusion is design-forced; it does not require an averaged
moment argument.

There is also an independent trace-zero certificate.  On the four
excluded residual eigenvalues \(8,-7,6,-5\),

\[
g(t)=(t-4)(t+3)(t-2)(t+1)
\]

is strictly positive, while it vanishes at \(4,-3,2,-1\).  The averaged
first four restricted moments make the residual expectation of \(g\)
zero.  Positivity then removes those four eigenspaces operatorwise.

## 2. All remaining freedom is one positive operator

On \({\cal H}_3\), put

\[
W_j=P_3\iota^*E_j\iota P_3,\qquad Z=W_{15}.
\]

Here and below \(P_3\) is the identity when an equation is read as an
operator equation on \({\cal H}_3\).  We have \(W_3=P_3/17\).
The zeroth, first, and second restricted moments are

\[
P_3,\qquad 0,\qquad16P_3.
\]

Solving these three operator equations at the four remaining
eigenvalues \(4,-3,2,-1\) gives

\[
\boxed{
\begin{aligned}
W_{12}&=\frac{10}{119}P_3+\frac37Z,\\
W_{13}&=\frac9{35}P_3-\frac37Z,\\
W_{14}&=\frac35P_3-Z,\\
W_{15}&=Z.
\end{aligned}}
\tag{3}
\]

Every \(W_j\) is positive semidefinite.  In fact the middle two upper
bounds coincide, and (3) is equivalent to

\[
\boxed{0\preceq Z\preceq\frac35P_3.}
\tag{4}
\]

The next four compressed global moments are

\[
\boxed{
\begin{aligned}
P_3\iota^*\mathcal A^3\iota P_3&=-126P_3+30Z,\\
P_3\iota^*\mathcal A^4\iota P_3&=1732P_3+60Z,\\
P_3\iota^*\mathcal A^5\iota P_3&=-21798P_3+510Z,\\
P_3\iota^*\mathcal A^6\iota P_3&=284500P_3+1380Z.
\end{aligned}}
\tag{5}
\]

Using the exact restricted-walk identities

\[
\begin{aligned}
\iota^*\mathcal A^3\iota&=2R,\\
\iota^*\mathcal A^4\iota&=496I+4A_{13},\\
\iota^*\mathcal A^5\iota&=178R+12A_2,\\
\iota^*\mathcal A^6\iota&=22576I+524A_{13}+36A_{12},
\end{aligned}
\]

we obtain

\[
\boxed{
\begin{aligned}
P_3RP_3&=-63P_3+15Z,\\
P_3A_{13}P_3&=309P_3+15Z,\\
P_3A_2P_3&=-882P_3-180Z,\\
P_3A_{12}P_3&=2778P_3-180Z.
\end{aligned}}
\tag{6}
\]

In particular,

\[
\boxed{P_3(A_{13}-R)P_3=372P_3.}
\tag{7}
\]

There is a stronger right-action statement.  Put

\[
g(t)=(t-4)(t+3)(t-2)(t+1).
\]

On the support (1), \(g\) vanishes at the four endpoint eigenvalues and
\(g(-13)=30\,600\).  Thus

\[
g(\mathcal A)\iota P_3=30\,600E_3\iota P_3.
\]

Restricting this identity and its first two multiples by \(\mathcal A\)
gives

\[
\boxed{
\begin{aligned}
A_{13}P_3&=(R+372I)P_3,\\
A_2P_3&=(-12R-1638I)P_3,\\
A_{12}P_3&=(-12R+2022I)P_3.
\end{aligned}}
\tag{8}
\]

The same polynomial-reduction argument applies to every Odd distance
matrix.  Consequently every fibre intersection relation satisfies

\[
\boxed{A_sP_3=(\alpha_s I+\beta_sR)P_3,}
\tag{9}
\]

with the following exact coefficients:

\[
\begin{array}{c|rrrrrrrr}
s&0&1&2&3&4&5&6&7\\ \hline
\alpha_s&0&0&-1638&-2193&-26100&35442&-4026&72765\\
\beta_s&0&1&-12&66&-220&495&-792&924
\end{array}
\]

\[
\begin{array}{c|rrrrrrrr}
s&8&9&10&11&12&13&14&15\\ \hline
\alpha_s&-88110&1694&-4884&14655&2022&372&0&1\\
\beta_s&-792&495&-220&66&-12&1&0&0.
\end{array}
\]

Hence all first-degree relation leakages are aligned:

\[
(I-P_3)A_sP_3=\beta_s(I-P_3)RP_3.
\tag{10}
\]

Expanding the annihilator (2) and restricting it to the fibre also gives
the useful checks

\[
\boxed{
(12A_2+44A_{13}+100R+3288I)P_3=0,
}
\tag{11}
\]

\[
\boxed{
(36A_{12}+132A_2+368A_{13}+1648R+6528I)P_3=0.
}
\tag{12}
\]

Unlike the degree-two result, the individual relations need not preserve
\({\cal H}_3\); equation (10) says that their possible failure to do so
is exactly the same one-operator failure as for \(R\).

## 3. Exact trace and leakage window

The Johnson kernel gives

\[
\operatorname{tr}(P_3R)=-240\,994.
\]

Taking the trace of the first line of (6) therefore yields

\[
\boxed{
\operatorname{tr}Z=\frac{12\,896}{15},
\qquad
\frac{\operatorname{tr}Z}{4030}=\frac{16}{75}.
}
\tag{13}
\]

The two-step fibre identity gives

\[
\operatorname{tr}(P_3R^2)=14\,417\,914.
\]

Let

\[
L=(I-P_3)RP_3.
\]

Since \(L^*L=P_3R^2P_3-(P_3RP_3)^2\), equations (6) and (13) give

\[
\boxed{
\|L\|_F^2=47\,740-225\,\operatorname{tr}(Z^2).
}
\tag{14}
\]

Combining nonnegativity of (14) with Cauchy--Schwarz gives

\[
\boxed{
\frac{206\,336}{1125}
\leq\operatorname{tr}(Z^2)
\leq\frac{9548}{45}.
}
\tag{15}
\]

Equivalently,

\[
\boxed{
\operatorname{tr}\left(Z-\frac{16}{75}P_3\right)^2
\leq\frac{3596}{125}.
}
\tag{16}
\]

The rank inequality
\((\operatorname{tr}Z)^2\leq\operatorname{rank}(Z)\operatorname{tr}(Z^2)\)
then forces

\[
\boxed{\operatorname{rank}Z\geq3484.}
\tag{17}
\]

These bounds are strong but compatible.

There is one further useful consequence for the non-Johnson matrix
\(Q\).  From

\[
R^2=120I+5A_{13}+Q
\]

and the first line of (8),

\[
\boxed{QP_3=(R^2-5R-1980I)P_3.}
\tag{18}
\]

Writing \(A=P_3RP_3=-63P_3+15Z\) and \(D=L^*L\), its compression is

\[
\boxed{
P_3QP_3
=225Z^2-1965Z+2304P_3+D.
}
\tag{19}
\]

The scalar polynomial in (19) decreases from \(2304\) to \(1206\) on
\([0,3/5]\), so \(P_3QP_3\) is positive semidefinite.  This still gives
no contradiction.  In the block form

\[
R=\begin{pmatrix}A&L^*\\L&C\end{pmatrix},
\]

the first unforced \(Q\)-leakage is

\[
(I-P_3)QP_3=CL+L(A-5I),
\]

which depends on the unknown complementary block \(C\) and the
orientation of \(L\), not merely on \(Z\) and its traces.

## 4. A finite witness that closes the scalar-moment attack

At the upper endpoint in (15), (14) permits \(L=0\).  The following
formal spectrum for \(P_3RP_3\) satisfies every trace, square-trace,
positivity, and support constraint above:

\[
\boxed{
-61^{1914},\quad -60^{396},\quad -59^{720},\quad -58^{1000}.
}
\tag{20}
\]

The corresponding \(Z\)-eigenvalues are

\[
\left(\frac2{15}\right)^{1914},\quad
\left(\frac15\right)^{396},\quad
\left(\frac4{15}\right)^{720},\quad
\left(\frac13\right)^{1000}.
\]

They lie in \([0,3/5]\), have the traces in (13) and at the upper
endpoint of (15), and make (6) integral at the \(R\)-level.  This is
only a moment-level witness, not a matrix or cover construction.  It
proves that the displayed one-operator, trace, rank, and integrality
conditions alone cannot yield a contradiction.

The first genuinely unforced data is the operator \(D=L^*L\) beyond its
trace tradeoff with \(Z^2\), followed by the orientation term \(CL\).
Equivalent combinatorial targets include the state-refined matrices
\(1_{\{Q_{BC}=a\}}\), dual-idempotent/Terwilliger blocks, or a restriction
that couples the \(Z\)-eigenvectors to the one-factorisations around
fibre blocks.

Run the exact standard-library verifier with

```sh
python3 -B collaboration/schreier_h3_support/verify_schreier_h3_support.py
```
