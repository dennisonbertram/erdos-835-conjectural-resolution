# Schreier--Krein follow-up: an exact \(H_2\) support theorem

## Status

Assume that an unrestricted \(k=16\) cover

\[
O_{16}=KG(31,15)\longrightarrow K_{17}
\]

exists.  Fix one fibre \({\cal C}\), let \(R\) join fibre blocks meeting
in one point, and let \(A_s\) be the zero-one matrix for fibre-block
intersection \(s\).  Write \(\mathcal A\) for the adjacency matrix of the
Odd graph and \(\iota\) for extension by zero from the fibre.

Everything below is an exact necessary consequence.  It gives a new
quartic support theorem and exact higher compressions, but it produces
**no contradiction** and does not settle problem 835.

## 1. The initial Krein algebra is automatic

Let \(E_j\) be the \(j\)-th Johnson/Odd spectral idempotent and put

\[
P_j=17\,\iota^*E_j\iota .
\]

Because the fibre is an \(S(14,15,31)\), \(P_j\) is the orthogonal
projector onto the restricted degree-\(j\) harmonic space
\({\cal H}_j\) for \(0\le j\le7\).  If \(a+b\le7\), restriction of the
Johnson-scheme Krein identity gives

\[
\boxed{
P_a\circ P_b=\frac1n\sum_{\ell}q_{ab}^{\ell}P_\ell ,
\qquad n=|{\cal C}|=17\,678\,835.}
\tag{1}
\]

Thus every Schur product involving only \({\cal H}_1,{\cal H}_2\)
closes inside \({\cal H}_0\oplus\cdots\oplus{\cal H}_4\), with exactly
the ordinary Johnson Krein parameters.  The relevant nonzero parameters
are

\[
\begin{array}{c|ccccc}
(a,b)\backslash\ell&0&1&2&3&4\\ \hline
(1,1)&30&1/232&465/232&&\\
(1,2)&&6727/232&5/522&217/72&\\
(2,2)&434&217/1566&175739/3132&217/6750&81809/13500 .
\end{array}
\tag{2}
\]

They are all positive.  Hence ordinary Krein nonnegativity and Schur-rank
tests cannot obstruct the cover: (1) is already forced by the
fourteen-design property, without using \(R\).

For comparison, at \(k=6\) the exact available closure is

\[
P_1\circ P_1
=\frac1{66}\left(10P_0+\frac1{27}P_1+\frac{55}{27}P_2\right).
\tag{3}
\]

Its rank is \(1+10+44=55=\binom{10+1}{2}\), so the Witt control meets,
rather than violates, the symmetric-square absolute bound.

## 2. A forced four-point global support for \({\cal H}_2\)

Let \(x\in{\cal H}_2\) be a unit vector and \(y=\iota x\).  The compressed
idempotent theorem gives

\[
\|E_2y\|^2=\frac1{17},\qquad
\|E_jy\|^2=0\quad(j=0,1,3,4,5,6,7).
\tag{4}
\]

The fixed \(E_2\) spectral point is \(\theta_2=14\).  The remaining
allowed Odd spectral points are

\[
8,-7,6,-5,4,-3,2,-1.
\]

Local covering identities and the \(R\)-eigenvalue \(77\) on
\({\cal H}_2\) give the first four moments

\[
\langle\mathcal A^0\rangle_y=1,\quad
\langle\mathcal A\rangle_y=0,\quad
\langle\mathcal A^2\rangle_y=16,\quad
\langle\mathcal A^3\rangle_y=154.
\tag{5}
\]

On the eight residual spectral points,

\[
h(t)=\frac15(5t-6)(t+3)(t-2)(t+1)
=t^4+\frac45t^3-\frac{37}{5}t^2+\frac{36}{5}
\tag{6}
\]

is nonnegative.  Subtracting the fixed \(1/17\) mass at \(14\), (5)
therefore gives

\[
\langle\mathcal A^4\rangle_y\ge2292.
\tag{7}
\]

This lower bound is attained on average over an orthonormal basis of
\({\cal H}_2\).  Indeed

\[
\iota^*\mathcal A^4\iota=496I+4A_{13}
\]

and the Johnson kernel of \(P_2\) gives

\[
\frac1{434}\operatorname{tr}(P_2A_{13})=449.
\tag{8}
\]

Writing \(\theta_j\) for the Odd eigenvalue of \(E_j\), define the residual
operator
\[
 G=\left.\iota^*
   \left(\sum_{j=8}^{15}h(\theta_j)E_j\right)
   \iota\right|_{{\cal H}_2}.
\]
It is positive semidefinite, and its quadratic form is exactly the
left-hand side of (7) minus \(2292\).  Equation (8) says that
\(\operatorname{tr}G=0\), so \(G=0\).  Equality holds for every \(x\), and
polarization yields the exact support theorem

\[
\boxed{
(\mathcal A-14I)(\mathcal A+3I)
(\mathcal A-2I)(\mathcal A+I)\,\iota{\cal H}_2=0.}
\tag{9}
\]

More precisely, every unit \(x\in{\cal H}_2\) has the same global Odd
spectral measure

\[
\boxed{
\frac1{17}\delta_{14}
+\frac{29}{85}\delta_{-3}
+\frac4{15}\delta_2
+\frac13\delta_{-1}.}
\tag{10}
\]

This is stronger than a scalar Rayleigh bound: it removes every global
Odd component \(E_3,\ldots,E_{12}\) from the zero-extension of
\({\cal H}_2\).

The \(k=6\) control has the analogous, already exhaustive measure

\[
\frac17\delta_4+\frac9{35}\delta_{-3}
+\frac4{15}\delta_2+\frac13\delta_{-1},
\tag{11}
\]

which agrees with the derived Witt cover.

## 3. Exact fourth-, fifth-, and sixth-moment compressions

Here is a direct derivation of the walk identities used below.  Let \(D_i\)
be the distance-\(i\) matrix of the Odd graph.  Away from the diameter
boundary its intersection array gives

\[
 \mathcal A D_i=b_{i-1}D_{i-1}+c_{i+1}D_{i+1},
\]

where

\[
\begin{array}{c|cc}
d&b_d&c_d\\ \hline
2j&k-j&j\\
2j+1&k-1-j&j+1.
\end{array}
\]

Iterating this recurrence through degree six gives

\[
\begin{aligned}
\mathcal A^4
 &=k(2k-1)D_0+(4k-3)D_2+4D_4,\\
\mathcal A^5
 &=(6k^2-8k+3)D_1+(12k-14)D_3+12D_5,\\
\mathcal A^6
 &=k(6k^2-8k+3)D_0+(18k^2-34k+17)D_2\\
 &\qquad +(36k-52)D_4+36D_6.
\end{aligned}
\]

Two distinct blocks in one Steiner fibre are neither disjoint nor
intersection-\((k-2)\) pairs.  Also \(D_3,D_5,D_4,D_6\) correspond,
respectively, to block intersections \(1,2,k-3,k-4\).  Restricting the
three displayed identities to the fibre therefore gives

\[
\begin{aligned}
\iota^*\mathcal A^4\iota
 &=k(2k-1)I+4A_{k-3},\\
\iota^*\mathcal A^5\iota
 &=(12k-14)R+12A_2,\\
\iota^*\mathcal A^6\iota
 &=k(6k^2-8k+3)I+(36k-52)A_{k-3}+36A_{k-4}.
\end{aligned}
\tag{12}
\]

At \(k=16\), (10) has moments

\[
m_4=2292,\qquad m_5=31\,562,\qquad m_6=443\,180.
\]

Consequently

\[
\boxed{
\begin{aligned}
A_{13}P_2&=449P_2,\\
A_2P_2&=1488P_2,\\
A_{12}P_2&=5148P_2.
\end{aligned}}
\tag{13}
\]

These are full right-action identities, not merely compressions.  One
direct derivation applies \(\iota^*\) to the annihilator (9) and its first
two multiples by \(\mathcal A\); the restricted walk identities (12) then
give the three displayed equations.  Symmetry gives the corresponding
left identities.

Combining the first line with \(RP_2=77P_2\) and

\[
R^2=120I+5A_{13}+Q
\]

gives the further exact compression

\[
\boxed{QP_2=3564P_2.}
\tag{14}
\]

Thus every ordinary word in \(R,A_{13},A_2,A_{12},Q\) acts scalarly on
\({\cal H}_2\); the corresponding block moment matrices have zero Schur
complement.  This does not construct a joint pair \((R,Q)\).  In
particular, \(0\le Q_{BC}\le3(A_{12})_{BC}\) does not imply a
Loewner-order inequality.  The first entry-sensitive information is
\(Q^{\circ2}\), or equivalently the four state matrices
\(1_{\{Q_{BC}=a\}}\), \(0\le a\le3\), and it is not fixed by
(13)--(14).

## 4. Exact harmonic trace budgets

For \(0\le j\le7\), let \(m_j=\dim{\cal H}_j\),
\(T_j=\operatorname{tr}(P_jR)\), and
\(S_j=\operatorname{tr}(P_jR^2)=\|RP_j\|_F^2\).  The Johnson kernels,
the row sum of \(Q\), and the two-step identity determine:

\[
\begin{array}{c|r|r|r|r}
j&m_j&T_j&S_j&S_j-T_j^2/m_j\\ \hline
0&1&120&14\,400&0\\
1&30&-2\,910&282\,270&0\\
2&434&33\,418&2\,573\,186&0\\
3&4\,030&-240\,994&14\,417\,914&32\,364/5\\
4&26\,970&1\,219\,044&55\,256\,136&776\,736/5\\
5&138\,446&-4\,568\,718&152\,547\,714&1\,780\,020\\
6&566\,370&13\,026\,510&312\,555\,330&12\,945\,600\\
7&1\,893\,294&-28\,399\,410&492\,984\,630&66\,993\,480
\end{array}
\tag{15}
\]

Every last-column entry is nonnegative, as required by

\[
\|RP_j\|_F^2\ge
\|P_jRP_j\|_F^2\ge\frac{\operatorname{tr}(P_jR)^2}{m_j}.
\]

The first three equalities recover the known invariant modules.
The positive slack for \(j=3,\ldots,7\) is compatible with mixing among
the remaining modules and supplies no multiplicity or integrality
contradiction.

## 5. Scope of the no-go

The calculation closes the most direct unrestricted Schur/Krein route:

* all \(H_1/H_2\) Schur products have the ordinary nonnegative Johnson
  Krein coefficients automatically;
* the new quartic support and full \(H_2\) relation actions are exact;
* their displayed scalar, rank, trace, and multiplicity budgets are
  compatible; and
* entrywise bounds on \(Q\) cannot be promoted to semidefinite order.

A future contradiction would need state-refined or higher-harmonic joint
information about \(Q\) and \(R\), not another scalar Krein nonnegativity
check or an ordinary \(H_2\) operator word.

Run the standard-library audit with

```sh
python3 -B \
  collaboration/schreier_krein_followup/verify_schreier_krein_followup.py
```
