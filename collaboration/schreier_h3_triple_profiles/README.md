# Exact triple-containment profiles and the first state-refined frontier

## Status and scope

Assume that an unrestricted \(k=16\) cover

\[
O_{16}=KG(31,15)\longrightarrow K_{17}
\]

exists. Fix one fibre \({\cal C}\), hence a hypothetical
\(S(14,15,31)\), and one block \(B\in{\cal C}\). This note determines
every ordinary fibre-relation count through a fixed triple. It then
shows that these counts, the local one-factorisation, and all known
degree-at-most-two \(Q\)-contractions have a strictly positive rational
local witness.

These are exact necessary consequences. They neither construct nor
exclude a cover and do not settle Erdős--Rosenfeld problem 835.

## 1. The twelve binomial-moment equations

Let \(S\) be a triple, put

\[
i=|B\cap S|,
\qquad
n_s(B,S)=
\#\{D\in{\cal C}:S\subseteq D,\ |B\cap D|=s\}.
\]

For \(0\le r\le11\), count pairs \((T,D)\) in which

\[
T\in\binom{B\setminus S}{r},
\qquad
S\cup T\subseteq D\in{\cal C}.
\]

Since

\[
\lambda_t
=\frac{\binom{31-t}{14-t}}{15-t}
\]

is the number of fibre blocks through a fixed \(t\)-set, the count gives

\[
\boxed{
\sum_s\binom{s-i}{r}n_s(B,S)
=\binom{15-i}{r}\lambda_{r+3}
\quad(0\le r\le11).
}
\tag{1}
\]

The boundary data is

\[
n_s=0\ (s<i),\qquad n_0=n_{14}=0,\qquad
n_{15}=\mathbf1_{\{i=3\}}.
\tag{2}
\]

Here \(n_{14}=0\) follows from the Steiner uniqueness condition. The
fixed-block intersection equations give \(n_0=0\).

For \(i=0,1\), equation (1) has one remaining null direction after
(2). It is

\[
\beta_s=(-1)^{s-1}\binom{12}{s-1},
\qquad 1\le s\le13.
\tag{3}
\]

This is exactly the coefficient of \(R\) in the previously proved
right-action formula

\[
A_sP_3=(\alpha_sI+\beta_sR)P_3.
\]

Thus the only extra datum needed by (1) is the \(R\)-count \(n_1\).

## 2. The complete profiles

Entries not displayed are zero.

For \(i=0\), the entries \(s=1,\ldots,12\) are

\[
\boxed{
\begin{array}{c|rrrrrrrrrrrr}
s&1&2&3&4&5&6&7&8&9&10&11&12\\ \hline
n_s&
78&1716&19305&102960&303732&504504&
487773&270270&84370&13728&1053&26.
\end{array}}
\tag{4}
\]

For \(i=1\), put \(\varepsilon=n_1\). There are two palindromic
possibilities:

\[
\boxed{
\begin{array}{c|rrrrrrrrrrrrr}
&\multicolumn{13}{c}{s=1,\ldots,13}\\ \hline
\varepsilon=6&
6&292&5401&42724&177144&403656&531069&
403656&177144&42724&5401&292&6\\
\varepsilon=7&
7&280&5467&42504&177639&402864&531993&
402864&177639&42504&5467&280&7.
\end{array}}
\tag{5}
\]

Their difference is precisely the vector (3).

For \(i=2\), the entries \(s=2,\ldots,13\) are the reverse of (4):

\[
\boxed{
26,1053,13728,84370,270270,487773,
504504,303732,102960,19305,1716,78.
}
\tag{6}
\]

For \(i=3\), the entries \(s=3,\ldots,13\) are

\[
\boxed{
108,3072,31152,147840,375210,532224,
436128,202752,53460,7040,528,
}
\tag{7}
\]

and \(n_{15}=1\). Every row sums to

\[
\lambda_3=1\,789\,515.
\]

## 3. Why the \(R\)-counts are \(78\), \(6\), and \(7\)

Write \(O=B^c\), so \(|O|=16\). The \(R\)-neighbours through
\(a\in B\) are

\[
\{a\}\cup(O\setminus e),
\qquad e\in F_a,
\]

where the fifteen \(F_a\) form a one-factorisation of \(K_O\).

If \(S\subset O\), then exactly three factors contain an edge of the
triangle \(S\). In each of those factors six matching edges avoid \(S\);
in each of the other twelve factors five avoid it. Hence

\[
n_1=3\cdot6+12\cdot5=78.
\tag{8}
\]

If \(S=\{a,x,y\}\) with \(a\in B\) and \(x,y\in O\), only \(F_a\)
contributes. Seven edges of \(F_a\) avoid \(\{x,y\}\) when
\(\{x,y\}\in F_a\), and six avoid it otherwise. Therefore

\[
\boxed{
n_1(B,\{a,x,y\})=
\begin{cases}
7,&\{x,y\}\in F_a,\\
6,&\{x,y\}\notin F_a.
\end{cases}}
\tag{9}
\]

There are \(15\cdot8=120\) triples of the first type and
\(15\cdot112=1680\) of the second.

## 4. Global and pairwise consistency

The fixed-block intersection distribution is

\[
\begin{array}{c|rrrrrrrr}
s&0&1&2&3&4&5&6&7\\ \hline
N_s&0&120&3360&49140&349440&1417416&3363360&4877730
\end{array}
\]

\[
\begin{array}{c|rrrrrrrr}
s&8&9&10&11&12&13&14&15\\ \hline
N_s&4324320&2362360&768768&147420&14560&840&0&1.
\end{array}
\]

For every \(i\) and \(s\), the profiles satisfy the complete double
count

\[
\boxed{
\sum_{\substack{S\in\binom{[31]}3\\|S\cap B|=i}}
n_s(B,S)
=N_s\binom{s}{i}\binom{15-s}{3-i}.
}
\tag{10}
\]

For \(i=1\), the left side uses 1680 copies of the \(\varepsilon=6\)
row and 120 copies of the \(\varepsilon=7\) row. Thus the local
one-factorisation split and every global relation count agree exactly.
In particular, (1)--(10) have integer solutions and yield no congruence
obstruction.

There is a sharper local formulation at intersection twelve. Encode

\[
D=(B\setminus A)\cup U,
\qquad
A\in\binom B3,\quad U\in\binom O3,
\]

and let \(X_{A,U}\) be the indicator that this \(D\) is a fibre block.
The profiles imply

\[
\sum_A X_{A,U}=26,\qquad
\sum_U X_{A,U}=32.
\tag{11}
\]

The second identity follows from the \(i=3\) row by inverting the
disjointness matrix on \(\binom B3\); all of its Johnson eigenvalues are
nonzero.

For \(a\in B\) and \(e\in\binom O2\), put

\[
M_{a,e}=\sum_{\substack{A\ni a\\U\supset e}}X_{A,U}.
\]

Since fourteen triples \(U\) contain \(e\), equations (5) and (11) give

\[
\boxed{
M_{a,e}=
\begin{cases}
84,&e\in F_a,\\
72,&e\notin F_a.
\end{cases}}
\tag{12}
\]

Summing (12) over the fifteen edges through a fixed \(x\in O\) gives

\[
\sum_{\substack{A\ni a\\U\ni x}}X_{A,U}=546.
\]

Combining this with the \(i=2\) profile gives the pairwise margin

\[
\boxed{
\sum_{\substack{A\supset\{a,b\}\\U\ni x}}X_{A,U}=78
\quad(a\ne b).
}
\tag{13}
\]

All row, column, matching-edge, and pair-point margins are therefore
mutually consistent.

## 5. The \(q\)-state and a positive rational witness

For a triangle \(U\subset O\), let \(c(U)\subset B\) be the three
factor labels of its edges. They are distinct. For a selected pair
\((A,U)\), the common-\(R\)-neighbour state is

\[
\boxed{q(A,U)=|A\cap c(U)|\in\{0,1,2,3\}.}
\tag{14}
\]

Indeed a common neighbour exists for \(a\in A\) exactly when \(F_a\)
contains one of the three edges of \(U\).

The known identity \(QP_2=3564P_2\) is equivalently
\(Q=(9/13)A_{12}\) on the pair-incidence span. For a pair meeting \(B\)
in \(0,1,2\) points, respectively, the ordinary and \(q\)-weighted
intersection-twelve counts are

\[
\boxed{
(364,2184,9152),
\qquad
(252,1512,6336)=\frac9{13}(364,2184,9152).
}
\tag{15}
\]

All constraints through (15) have the following strictly positive
rational witness:

\[
\boxed{
\overline X_{A,U}
=\frac9{182}+\frac{q(A,U)}{78}.
}
\tag{16}
\]

Its four values, for \(q=0,1,2,3\), are

\[
\frac9{182},\quad\frac{17}{273},\quad
\frac{41}{546},\quad\frac8{91}.
\]

To audit (16), the raw domain sizes and first \(q\)-moments for the five
triple types are

\[
\begin{array}{c|rr|r}
\text{type}&\#(A,U)&\sum q&\sum\overline X\\ \hline
i=0&455&273&26\\
i=1,\ e\in F_a&5096&2184&280\\
i=1,\ e\notin F_a&5096&3120&292\\
i=2&30030&18018&1716\\
i=3&123200&73920&7040.
\end{array}
\tag{17}
\]

For the three pair types, the raw \(q\)-state distributions are

\[
\begin{array}{c|rrrr|rr}
&q=0&q=1&q=2&q=3&
\sum\overline X&\sum q\overline X\\ \hline
0\text{ points in }B&3080&2772&504&14&364&252\\
1\text{ point in }B&18480&16632&3024&84&2184&1512\\
2\text{ points in }B&77440&69696&12672&352&9152&6336.
\end{array}
\tag{18}
\]

Thus no real linear combination of the displayed triple profiles,
pairwise margins, or pair-harmonic \(Q\)-constraints can be a
separating contradiction. The witness is rational, not zero-one; it is
not a local design construction.

## 6. The first genuinely free statistic

For fixed \(B\), define

\[
N_j(B)=
\#\{D:|B\cap D|=12,\ q_{BD}=j\}.
\]

The known data gives only

\[
\sum_{j=0}^3N_j=14560,\qquad
\sum_{j=0}^3jN_j=10080.
\tag{19}
\]

Put

\[
\tau_B=\sum_D\binom{q_{BD}}2=N_2+3N_3.
\]

Writing \(u=N_3\), all state counts are

\[
\boxed{
\begin{aligned}
N_3&=u,\\
N_2&=\tau_B-3u,\\
N_1&=10080-2\tau_B+3u,\\
N_0&=4480+\tau_B-u.
\end{aligned}}
\tag{20}
\]

Taken **in isolation**, equations (19)--(20) have nonnegative integral
solutions precisely for

\[
\boxed{
\tau_B\in\{0,1,\ldots,10078,10080\}.
}
\tag{21}
\]

The isolated value \(10079\) is impossible in that two-equation relaxation:
it would require
\(N_3\ge3360\) from \(N_1\ge0\), but \(N_2\ge0\) requires
\(N_3\le3359\).

This is **not** the live bound once the five-common-neighbour double count is
included.  The independently proved local identity in
[`../h3_state_refinement/README.md`](../h3_state_refinement/README.md) gives

\[
0\leq\tau_B\leq1680,\qquad
\sum_D Q_{BD}^2=10080+2\tau_B.
\tag{22}
\]

Every integer in the true interval \(0,\ldots,1680\) satisfies the elementary
row-state equations (19)--(20), so the isolated exclusion at \(10079\) has no
frontier significance.  The missing information is the actual value and
cross-root compatibility of \(\tau_B\), not its elementary feasibility.

The rational witness (16) has

\[
\tau_B=\frac{21600}{13};
\]

its nonintegrality is another reminder that (16) is only an interior
point of the real relaxation.

Combinatorially, the missing second-state datum is already visible for
each pair \(a,b\in B\). Let

\[
H_{ab}=\{U:\{a,b\}\subseteq c(U)\};
\]

then \(|H_{ab}|=16\), and put

\[
T_{ab}=
\sum_{\substack{A\supset\{a,b\}\\U\in H_{ab}}}X_{A,U}.
\]

The pair-point margin (13) does not determine this special
colour-triangle correlation, while

\[
\boxed{\tau_B=\sum_{\{a,b\}\in\binom B2}T_{ab}.}
\tag{23}
\]

At the triple level, an even finer first unknown is

\[
m(B,S)=
\sum_{\substack{D\supseteq S\\|B\cap D|=12}}q_{BD},
\tag{24}
\]

namely \(Q\) acting on the degree-three incidence module. Equations
(19)--(24), or equivalently the four state matrices
\(\mathbf1_{\{Q=j\}}\), are the first data not fixed by the ordinary
\(A_s\) right action.

## 7. Cyclic zero-one probe

As a stronger non-proof diagnostic, normalize

\[
O=\mathbb Z_{15}\cup\{\infty\},\qquad
F_a=\{\{\infty,a\}\}\cup
\{\{a-d,a+d\}:1\le d\le7\}.
\]

Requiring \(X\) to be invariant under simultaneous translation leaves
16,990 binary pair-orbits.

Two bounded searches were run on 2026-07-26:

* the 301-constraint model containing (11)--(13) returned
  `UNKNOWN` after 60.48 seconds
  (68,183 branches, 39 conflicts);
* the 332-constraint model also containing all constraints (15)
  returned `UNKNOWN` after 121.01 seconds
  (248,780 branches, 123,662 conflicts).

An independent SCIP run on the 301-constraint model also returned
`NOT_SOLVED` after 121.83 seconds and 74 nodes. These are explicitly
nonverdicts: they prove neither feasibility nor infeasibility of the
cyclic binary slice.

The CP-SAT models and independent witness checks are reproducible with

```sh
python3 -B \
  collaboration/schreier_h3_triple_profiles/search_cyclic_binary_slice.py \
  --seconds 60

python3 -B \
  collaboration/schreier_h3_triple_profiles/search_cyclic_binary_slice.py \
  --include-q --seconds 120
```

The exact conclusion is therefore the closure in Sections 1--6. A
useful next computation must resolve a zero-one state-refined slice or
constrain (22)--(23); repeating ordinary triple moments cannot add
information.

Run the exact, standard-library verifier with

```sh
python3 -B \
  collaboration/schreier_h3_triple_profiles/verify_schreier_h3_triple_profiles.py
```
