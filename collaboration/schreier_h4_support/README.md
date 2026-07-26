# Degree-four Schreier support, its exact operator cone, and the 17-fibre rank audit

## Status and scope

Assume that an unrestricted \(k=16\) cover

\[
O_{16}=KG(31,15)\longrightarrow K_{17}
\]

exists.  Fix a colour fibre \({\cal C}\), let \(A_s\) be the zero-one
matrix joining fibre blocks with intersection \(s\), and put \(R=A_1\).
Let \(\mathcal A\) be the global Odd-graph adjacency matrix and let
\(\iota:\mathbb R^{\cal C}\to\mathbb R^{V(O_{16})}\) extend a fibre
vector by zero.

This note derives exact necessary consequences on the degree-four
Johnson harmonic space.  It also gives finite operator relaxations
satisfying all consequences derived here.  Those witnesses are **not**
block designs, graph covers, or solutions of Erdős--Rosenfeld problem
835.

## 1. Design quadrature forces six-point global support

Let \(E_j\) be the global Johnson/Odd idempotent with eigenvalue

\[
\theta_j=(-1)^j(16-j),
\]

and let \({\cal H}_4\) be the restriction to \({\cal C}\) of the
degree-four harmonic space.  Its dimension is

\[
d_4=\binom{31}{4}-\binom{31}{3}=26970.
\]

The fibre is an \(S(14,15,31)\).  If \(f\) is degree four and \(g\) is
degree \(j\leq10\), then \(fg\) has incidence degree at most
\(4+j\leq14\).  Design quadrature gives

\[
\sum_{B\in{\cal C}}f(B)g(B)
=\frac1{17}\sum_{B\in\binom{[31]}{15}}f(B)g(B).
\]

The right side vanishes unless \(j=4\), while restriction on degree
four is a \(1/\sqrt{17}\)-scaled isometry.  Hence

\[
\boxed{
\iota{\cal H}_4
\subseteq E_4\oplus E_{11}\oplus E_{12}\oplus
E_{13}\oplus E_{14}\oplus E_{15}.
}
\tag{1}
\]

Equivalently, with \(P_4\) the orthogonal projector onto
\({\cal H}_4\),

\[
\boxed{
q_4(\mathcal A)\iota P_4=0,
}
\tag{2}
\]

where

\[
\begin{aligned}
q_4(t)
&=(t-12)(t+5)(t-4)(t+3)(t-2)(t+1)\\
&=t^6-9t^5-59t^4+225t^3+706t^2-1008t-1440.
\end{aligned}
\]

This is an operator statement, not merely an averaged moment
calculation.

## 2. Exact endpoint traces

For \(0\leq s\leq15\), let \(n_s\) be the number of fibre blocks
meeting a fixed fibre block in \(s\) points.  The fourteen-design
equations, together with \(n_{15}=1\), determine all \(n_s\).  The
values needed below are

\[
n_1=120,\qquad n_2=3360,\qquad
n_{12}=14560,\qquad n_{13}=840,
\]

and \(n_0=n_{14}=0\).

The normalized degree-four Johnson zonal kernel is

\[
\psi_4(u)=
\frac34-\frac{28}{75}\binom u1+\frac{27}{175}\binom u2
-\frac{108}{2275}\binom u3+\frac3{364}\binom u4.
\tag{3}
\]

In particular,

\[
\psi_4(1)=\frac{113}{300},\quad
\psi_4(2)=\frac{331}{2100},\quad
\psi_4(12)=\frac{31}{350},\quad
\psi_4(13)=\frac{37}{150}.
\]

Thus the normalized traces of the four local relation compressions are

\[
\frac1{d_4}\operatorname{tr}(P_4A_sP_4)
=n_s\psi_4(s),
\]

so

\[
\rho_1=\frac{226}{5},\quad
\rho_2=\frac{2648}{5},\quad
\rho_{12}=\frac{6448}{5},\quad
\rho_{13}=\frac{1036}{5}.
\tag{4}
\]

Put

\[
W_j=P_4\iota^*E_j\iota P_4.
\]

The degree-four component is \(W_4=P_4/17\).  Either the projector
kernel formula

\[
\frac{\operatorname{tr}W_j}{d_4}
=\frac{\dim E_j}{\binom{31}{15}}
\left(\sum_{s=0}^{15}n_s\psi_4(s)\psi_j(s)\right)
\tag{5}
\]

or the first six averaged moments give

\[
\boxed{
\begin{array}{c|rrrrrr}
j&4&11&12&13&14&15\\ \hline
\operatorname{tr}(W_j)/d_4&
\frac1{17}&\frac{10}{119}&\frac{16}{175}&\frac{54}{175}&
\frac{128}{525}&\frac{16}{75}.
\end{array}}
\tag{6}
\]

The averaged global moments through degree six are

\[
1,\quad0,\quad16,\quad\frac{452}{5},\quad
\frac{6624}{5},\quad\frac{72004}{5},\quad\frac{887872}{5}.
\tag{7}
\]

## 3. The exact two-operator endpoint cone

All equations in this section act on \({\cal H}_4\), so \(P_4\) is
written as \(I\).  Set

\[
X=W_{14},\qquad Y=W_{15}.
\]

The zeroth, first, and second operator moments solve to

\[
\boxed{
\begin{aligned}
W_{11}&=-\frac{26}{153}I+\frac59(X+Y),\\
W_{12}&=\frac{16}{63}I-\frac59X-\frac8{63}Y,\\
W_{13}&=\frac67I-X-\frac{10}{7}Y,\\
W_{14}&=X,\qquad W_{15}=Y.
\end{aligned}}
\tag{8}
\]

Consequently, the complete one-variable spectral positivity cone is

\[
\boxed{
\begin{gathered}
X\succeq0,\qquad Y\succeq0,\\
X+Y\succeq\frac{26}{85}I,\qquad
35X+8Y\preceq16I,\qquad
7X+10Y\preceq6I.
\end{gathered}}
\tag{9}
\]

The exact trace budgets are

\[
\boxed{
\begin{aligned}
\operatorname{tr}X&=\frac{230144}{35},&
\operatorname{tr}Y&=\frac{28768}{5},\\
\operatorname{tr}W_{11}&=\frac{269700}{119},&
\operatorname{tr}W_{12}&=\frac{86304}{35},&
\operatorname{tr}W_{13}&=\frac{291276}{35}.
\end{aligned}}
\tag{10}
\]

There is a strict rational feasible point

\[
\boxed{
X=\frac{128}{525}I,\qquad Y=\frac{16}{75}I.
}
\tag{11}
\]

The three nontrivial slacks in (9) are respectively

\[
\frac{18}{119}I,\qquad \frac{144}{25}I,\qquad\frac{54}{25}I.
\]

Small independent trace-zero rational perturbations of \(X\) and \(Y\)
remain feasible.  Thus two self-adjoint parameters are genuinely
needed by this relaxation; no further operator equality follows from
the first three moments and positivity.

The strict point makes every \(W_j\) a positive scalar multiple of
\(I\).  Since

\[
\begin{array}{c|rrrrrr}
j&4&11&12&13&14&15\\ \hline
\dim E_j&
26970&40320150&56448210&65132550&58929450&35357670,
\end{array}
\]

all rank constraints are satisfied.  Fractional traces cause no
integrality obstruction: the \(W_j\) are effects, not projections.

## 4. Restricted walks and the three-map right module

The spectral moments obtained from (8) are

\[
\begin{aligned}
M_3&=116I-70X-40Y,\\
M_4&=1248I+140X+200Y,\\
M_5&=15220I-2030X-1520Y,\\
M_6&=174656I+5740X+7120Y.
\end{aligned}
\]

Combining these with

\[
\begin{aligned}
\iota^*\mathcal A^3\iota&=2R,\\
\iota^*\mathcal A^4\iota&=496I+4A_{13},\\
\iota^*\mathcal A^5\iota&=178R+12A_2,\\
\iota^*\mathcal A^6\iota&=22576I+524A_{13}+36A_{12},
\end{aligned}
\]

gives the exact compressions

\[
\boxed{
\begin{aligned}
P_4RP_4&=58I-35X-20Y,\\
P_4A_{13}P_4&=188I+35X+50Y,\\
P_4A_2P_4&=408I+350X+170Y,\\
P_4A_{12}P_4&=1488I-350X-530Y.
\end{aligned}}
\tag{12}
\]

Restricting (2) gives

\[
\boxed{
(A_{12}-3A_2+8A_{13}-32R+88I)P_4=0.
}
\tag{13}
\]

There is a second, stronger relation.  Let

\[
g_4(t)=(t+5)(t-4)(t+3)(t-2)(t+1).
\]

It vanishes on all five endpoint eigenspaces and
\(g_4(12)=265200\).  Since
\(\iota^*E_4\iota P_4=P_4/17\),

\[
\iota^*g_4(\mathcal A)\iota P_4=15600P_4.
\]

The degree-five restricted walks therefore give

\[
\boxed{
(A_2+A_{13}+11R-1234I)P_4=0.
}
\tag{14}
\]

Equations (13)--(14) imply

\[
A_2P_4=(1234I-11R-A_{13})P_4,\qquad
A_{12}P_4=(3614I-R-11A_{13})P_4.
\tag{15}
\]

Reducing every Odd distance polynomial modulo \(q_4\), then using
(14), proves the stronger universal statement

\[
\boxed{
A_sP_4=(a_sI+b_sR+c_sA_{13})P_4
\quad(0\leq s\leq15),
}
\tag{16}
\]

with

\[
\begin{array}{c|rrr}
s&a_s&b_s&c_s\\ \hline
0&0&0&0\\
1&0&1&0\\
2&1234&-11&-1\\
3&-2535&55&11\\
4&19110&-165&-55\\
5&-59488&330&165\\
6&84084&-462&-330\\
7&-99099&462&462\\
8&118404&-330&-462\\
9&-87516&165&330\\
10&31746&-55&-165\\
11&-9555&11&55\\
12&3614&-1&-11\\
13&0&0&1\\
14&0&0&0\\
15&1&0&0
\end{array}
\tag{17}
\]

This is a three-map **right module**.  It does not say that
\({\cal H}_4\) is invariant under \(R\) or \(A_{13}\).  Thus it does not
turn the rational compression eigenvalues into algebraic integers.

## 5. A quadratic leakage check

The one-factorization structure of the \(R\)-neighbourhood of a fibre
block fixes the ordered intersections of two \(R\)-neighbours:

\[
120\text{ pairs at }s=15,\qquad
4200\text{ pairs at }s=13,\qquad
10080\text{ pairs at }s=12.
\]

It follows that

\[
\boxed{
\operatorname{tr}(P_4R^2)
=d_4\left(120+4200\psi_4(13)+10080\psi_4(12)\right)
=55256136.
}
\tag{18}
\]

For \(B=P_4RP_4\), positivity of the leakage gives

\[
\operatorname{tr}(B^2)\leq55256136.
\]

At the scalar witness (11), \(B=(226/5)I\) and the leakage is

\[
55256136-\operatorname{tr}(B^2)
=\frac{776736}{5}
=d_4\frac{144}{25}>0.
\tag{19}
\]

Thus this first quadratic/inertia test is compatible as well.

## 6. Coupling all seventeen fibres

Let \(D_c\) be the diagonal projection onto colour \(c\).  The
projections are orthogonal and sum to \(I\).  For \(a,b\leq7\),
fourteen-design quadrature gives

\[
E_aD_cE_b=\frac{\delta_{ab}}{17}E_a.
\tag{20}
\]

Therefore, for

\[
L=\bigoplus_{a=0}^7E_a,\qquad
V_c=\sqrt{17}\,D_c|_L,
\]

the seventeen \(V_c\) are mutually orthogonal isometries.  The trivial
colour module maps back to \(L\); the standard sixteen-dimensional
colour module tensored with \(L\) embeds isometrically in \(L^\perp\).

For fixed \(a\), put

\[
T_{j,c}=E_jD_c|_{E_a}.
\]

Then

\[
\sum_cT_{j,c}=0\quad(j\ne a),
\]

and the endpoint maps obey

\[
\boxed{
\sum_{j=15-a}^{15}T_{j,c}^*T_{j,d}
=\frac{17\delta_{cd}-1}{289}I.
}
\tag{21}
\]

This is exactly the Gram matrix of the regular simplex of seventeen
colours.

If \(w_{a,j}\) is the normalized single-fibre trace of the \(j\)-th
effect, concatenating the scaled maps
\(\sqrt{17}T_{j,c}\) gives the necessary rank bound

\[
\boxed{
17w_{a,j}\dim E_a\leq\dim E_j.
}
\tag{22}
\]

For \(a=4\), the lowest endpoint \(j=11\) requires rank at least

\[
\left\lceil\frac{269700}{7}\right\rceil=38529,
\]

far below \(\dim E_{11}=40320150\).

For \(a=7\), the endpoint weights at \(j=8,\ldots,15\) are

\[
\frac{1748}{284427},\\
\frac{161}{16731},\\
\frac{115}{1859},\\
\frac{9200}{117117},\\
\frac{1840}{9009},\\
\frac{200}{1001},\\
\frac{200}{819},\\
\frac{16}{117}.
\tag{23}
\]

The lowest endpoint \(j=8\) requires rank at least \(197806\), while
\(\dim E_8=5259150\).

Even stacking every \(a=0,\ldots,7\), the exact fractions of the
available endpoint spaces consumed by the trace lower bound are

\[
\boxed{
\begin{array}{c|cccccccc}
j&8&9&10&11&12&13&14&15\\ \hline
\text{required}/\dim E_j&
\frac{1748}{46475}&\frac{1748}{46475}&
\frac{16}{169}&\frac{16}{169}&
\frac{80}{539}&\frac{80}{539}&
\frac{80}{437}&\frac{80}{437}.
\end{array}}
\tag{24}
\]

The largest is only \(80/437<0.184\).  Hence the global multiplicity
route does not contradict the cover.

There is also an explicit relaxation witness for all seventeen
degree-four maps.  Let

\[
C_0=\{u\in\mathbb R^{17}:\sum_cu_c=0\},\qquad
q_c=e_c-\frac1{17}{\bf1},
\]

and choose isometries
\(J_j:C_0\otimes\mathbb R^{26970}\to E_j\) for
\(j=11,\ldots,15\).  The target dimensions all exceed
\(16\cdot26970\).  Put

\[
\alpha_j^2=
\frac{17}{16}w_{4,j}
=\left(
\frac5{56},\frac{17}{175},\frac{459}{1400},
\frac{136}{525},\frac{17}{75}
\right),
\]

whose sum is one, and define

\[
S_{4,c}=\frac1{\sqrt{17}}I,\qquad
S_{j,c}x=\alpha_jJ_j(q_c\otimes x).
\tag{25}
\]

Then

\[
S_c^*S_d=\delta_{cd}I,\qquad
\sum_cS_{j,c}=0,\qquad
S_{j,c}^*S_{j,c}=w_{4,j}I.
\]

Thus the strict scalar point (11) extends to the complete
seventeen-colour simplex coupling.  Completing the mutually orthogonal
ranges to equal projections gives a finite Hilbert-space model of the
colour-projection identities.

There is an analogous, non-scalar finite witness for \(a=7\).  On
\(C_0\otimes\mathbb R^{\dim E_7}\), decompose \(C_0\) into the eight
real two-dimensional Fourier modules of the cyclic group of order
seventeen.  On these modules choose diagonal effects \(G_j\),
\(8\leq j\leq15\), which commute with the cyclic action, sum to \(I\),
and have traces

\[
\operatorname{tr}G_j=17w_{7,j}\dim E_7.
\]

Such effects are obtained by partitioning \(8\dim E_7\) scalar slots
with column sums \(\operatorname{tr}G_j/2\), allowing one fractional
slot at each boundary, and repeating every scalar on its
two-dimensional Fourier module.  Their ranks are at most
\(2\lceil\operatorname{tr}G_j/2\rceil+2<\dim E_j\).  Factoring
\(G_j=L_j^*L_j\) through \(E_j\) gives a combined isometry.  Cyclic
invariance makes every colour \(q_c\) have the same block trace
\(w_{7,j}\dim E_7\), while \(\sum_jG_j=I\) gives the regular-simplex
Gram identity (21).

This model does **not** impose the fixed entrywise kernels of the
Johnson scheme or produce zero-one block incidence data.  It proves
only that support, moment, positivity, rank, and first Schur/color
associativity constraints are mutually compatible.

## 7. Conclusion

The degree-four method produces:

1. an exact six-eigenspace support theorem;
2. a complete two-operator endpoint cone;
3. a three-map right module for every fibre relation;
4. exact local leakage and global seventeen-fibre rank tests.

Every resulting relaxation is feasible, including strict rational and
seventeen-colour operator witnesses.  A contradiction must therefore
use information not present here, such as nonlinear products of the
uncontrolled leakage maps, sphere-resolved Terwilliger data, or the
fixed entrywise Johnson kernels.
