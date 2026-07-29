# Closing the \(p\equiv7\pmod8\) maximal-minor link

Status: **a uniform obstruction to one algebraic construction family, not
an obstruction to arbitrary colourings and not a solution of
Erdős--Rosenfeld Problem #835.**

Let \(p\equiv7\pmod8\) be prime, \(p\ge23\), and put \(k=p-1\).  This note
proves that no matrix
\[
 G\in\mathbb F_p^{\,k\times2k}
\]
can colour the \(k\)-subsets of its ordered columns by
\[
 c(S)=\det G_S
\]
so that every \((k-1)\)-star is rainbow.  A fixed relabelling of the field
values does not help.

Together with the already proved \(p\equiv1\pmod4\) obstruction in
`evidence/algebraic_construction_no_go.md` and the
\(p\equiv3\pmod8\) obstruction in `evidence/determinant_link_p19.md`,
this closes the single-maximal-minor proposal at every prime \(p>7\).
The cases \(p=5,7\) are already excluded for arbitrary colourings by the
known small-parameter results.  Thus a single maximal minor cannot solve
Problem #835 at any \(k>2\).  The conclusion does not cover ratios or
tuples of several Plücker coordinates.

The dependency-free finite audit is
`verify_maximal_minor_p7mod8_closure.py`.

## 1. The ordered rank-two link

Assume such a determinant rule exists and fix any \(p-3\) columns.  They
are independent: otherwise, after adjoining one further column, every
extension to a maximal minor would be zero, contradicting a rainbow star.
Project the remaining \(p+1\) columns to the two-dimensional quotient.
After absorbing the fixed signs caused by the frozen columns, obtain
ordered nonzero vectors
\[
 u_0,\ldots,u_p\in\mathbb F_p^2
\]
such that at every \(i\) the symmetric ordered labels
\[
 \{\det(u_j,u_i):j<i\}\ \cup\
 \{\det(u_i,u_j):j>i\}
\tag{1}
\]
are exactly \(\mathbb F_p\).

Every vector has one parallel mate, because zero occurs exactly once in
each row.  Hence the vectors occupy
\[
 m={p+1\over2}
\]
projective directions, twice each.

The first-power sum in every row of (1) is zero.  Put
\[
 W=\sum_j u_j,\qquad P_i=\sum_{j<i}u_j,\qquad Q_i=W-2P_i.
\]
Then
\[
 \det(u_i,Q_i)=0,\qquad Q_{i+1}=Q_i-2u_i.              \tag{2}
\]
At least one of \(Q_0,Q_1,Q_2\) is zero; otherwise \(u_0,u_1,u_2\)
would occupy one projective direction.  Starting at the first zero,
(2) pairs successive vectors and forces the mate ratio to be \(-1\).
The first zero cannot be \(Q_2\): forward pairing would give
\(\sum_{j\ge2}u_j=0\), while \(Q_2=0\) gives
\(W=2(u_0+u_1)\), and the total sum gives \(W=u_0+u_1\); hence
\(Q_0=W=0\), a contradiction.  If \(Q_0=0\), all vectors pair
successively with ratio \(-1\).  If \(Q_1=0\), the vectors from index
one onward pair successively with ratio \(-1\), while the two boundary
vectors \(u_0,u_p\) have ratio \(+1\).  Consequently every projective
pair has equal squared scale.

Choose an unused projective direction and move it to infinity.  The used
directions have distinct slopes \(t_1,\ldots,t_m\).  Write
\[
 z_e=a_e^2\in(\mathbb F_p^\times)^2
\]
for the common squared scale in direction \(e\).  Squaring a row of (1)
shows that for every \(e\)
\[
 \left\{z_f(t_f-t_e)^2:f\ne e\right\}
   =(\mathbb F_p^\times)^2.                            \tag{3}
\]
The common row factor \(z_e\) was suppressed; it is a square.

## 2. The top two even moments

Write \(p=8q+7\), so
\[
 m=4q+4,\qquad r={m-2\over2}=2q+1.
\]
For \(1\le s\le r\), power sums of the quadratic residues in (3) give
\[
 F_s(x):=\sum_f z_f^s(t_f-x)^{2s},\qquad
 F_s(t_e)=0\quad(1\le e\le m).
\]
Since \(2s\le m-2\), the polynomial has more roots than its degree:
\[
 F_s=0.                                                \tag{4}
\]
Let
\[
 P(X)=\prod_f(X-t_f).
\]
The standard Vandermonde annihilator says that vectors \(w_f\) satisfying
\(\sum_f w_ft_f^j=0\) for \(0\le j\le d\) are exactly
\[
 w_f={R(t_f)\over P'(t_f)},\qquad
 \deg R\le m-d-2.                                     \tag{5}
\]

At \(s=r\), equations (4)--(5) give
\[
 z_f^r={C\over P'(t_f)}.                               \tag{6}
\]
At \(s=r-1\), which is positive because \(p\ge23\), they give
\[
 z_f^{r-1}={R(t_f)\over P'(t_f)},\qquad\deg R\le2.      \tag{7}
\]
Dividing (6) by (7),
\[
 z_f={C\over R(t_f)}.                                  \tag{8}
\]
In particular \(R(t_f)\ne0\), and all \(m=(p+1)/2\) values
\(R(t_f)\) have one quadratic character.

## 3. The quadratic-character split

The same-character condition from (8) leaves three cases.

For a nonconstant linear polynomial, or a quadratic whose discriminant is
a nonzero square, at most
\((p-1)/2=m-1\) field elements give one prescribed nonzero character.
Those cases cannot contain all \(m\) slopes.

If the quadratic discriminant is zero, or if \(R\) is constant, then
\[
 R\text{ is a nonzero constant},\qquad\text{or}\qquad
 R(X)=a(X-b)^2                                      \tag{9}
\]
with \(b\notin\{t_f\}\).

In the constant case put \(y_f=t_f\).  In the second case put
\[
 y_f={1\over t_f-b}.
\]
Equation (8) and the fact that all \(z_f\) are squares turn (3), after a
row-dependent square scaling, into
\[
 \left\{(y_f-y_e)^2:f\ne e\right\}
   =(\mathbb F_p^\times)^2
\quad\text{for every }e.                               \tag{10}
\]
Thus \(Y=\{y_1,\ldots,y_m\}\) contains no nontrivial three-term arithmetic
progression: if \(y_f+y_g=2y_e\) with distinct endpoints, the two
differences in (10) have the same square.

There is one remaining possibility: \(R\) is an irreducible quadratic.
After an affine change and a harmless scalar, write
\[
 R(s)=s^2-d,\qquad \chi(d)=-1.
\]
The character census has exactly \(m\) values of its majority sign, so the
slopes must be the whole set
\[
 T=\{s:\chi(s^2-d)=-1\};                              \tag{11}
\]
here \(\chi(-1)=-1\), and \(0\notin T\).

Fix \(t\in T\).  On \(T\) define
\[
 \phi_t(s)=
 { (t^2+d)s-2dt\over 2ts-t^2-d}.                      \tag{12}
\]
The denominator cannot vanish on \(T\): at its putative zero,
\(s^2-d\) would be a square.  Direct calculation gives
\[
\begin{aligned}
 \phi_t(\phi_t(s))&=s,\\
 \phi_t(s)^2-d
  &={ (t^2-d)^2(s^2-d)\over(2ts-t^2-d)^2},\\
 {(\phi_t(s)-t)^2\over\phi_t(s)^2-d}
  &={ (s-t)^2\over s^2-d}.                            \tag{13}
\end{aligned}
\]
Thus \(\phi_t\) preserves \(T\) and pairs equal values in the \(t\)-th
row of (3).  Its only fixed points on \(T\) are \(t\) and \(d/t\):
the fixed-point equation factors as
\[
 (s-t)(ts-d)=0.
\]
After deleting \(t\), one point is fixed and the other \(m-2\) points
are paired.  Hence that row has at most \(1+(m-2)/2=m/2\) distinct
nonzero values, instead of the required \(m-1\).  The irreducible case
is impossible as well.

## 4. No progression-free half-plus-one set

It remains to exclude (10).  This is impossible by a short argument that does not invoke
an asymptotic additive-combinatorics theorem.

Suppose \(Y\subset\mathbb F_p\) has
\[
 |Y|=m={p+1\over2}
\]
and no nontrivial three-term progression.  For \(y\in Y\), the two
\(m\)-sets \(Y\) and \(2y-Y\) meet only in \(y\), so their union is all of
\(\mathbb F_p\).

Put
\[
 S_1=\sum_{z\in Y}z,\qquad S_2=\sum_{z\in Y}z^2.
\]
Because \(p>3\), the sum of the squares of all field elements is zero.
Summing squares in
\[
 \mathbb F_p=Y\cup(2y-Y),\qquad Y\cap(2y-Y)=\{y\},
\]
and using \(4m\equiv2\pmod p\), gives
\[
 y^2-4S_1y+2S_2=0.                                    \tag{11}
\]
Equation (11) holds for every \(y\in Y\), but its left side is a monic
quadratic and \(|Y|=m>2\).  This contradiction proves that (10), the
rank-two link, and the proposed maximal-minor colouring are impossible.

## 5. Sharp local control

The use of the next-to-top moment is essential.  At the exceptional prime
\(p=7\), the eight ordered vectors
\[
\begin{split}
&(1,0),(6,0),(3,3),(4,4),\\
&(3,6),(4,1),(3,5),(4,2)
\end{split}
\]
have every row of symmetric ordered determinants equal to
\(\mathbb F_7\).  Thus the rank-two link itself genuinely survives at
\(p=7\), even though the full \(k=6\) colouring is known not to exist.

This positive control is also why the theorem above starts at \(p=23\),
the first prime congruent to \(7\bmod8\) for which the second moment in
(7) is available.

## Exact scope

This proof closes a natural projective/determinantal ansatz uniformly.
It does not constrain a general large set \(LS(k-1,k,2k)\), a general
Odd-graph cover, or a construction using several coupled minors.  The
Erdős--Rosenfeld existential problem remains open.
