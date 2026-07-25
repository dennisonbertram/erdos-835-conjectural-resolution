# The unprojected fourth-moment completion of the colour algebra

Date: 2026-07-25.

This note identifies exactly what first appears when one goes beyond the
projected product
\[
  \beta(x,y)=P_K(xy)
\]
in the top Johnson constituent.  It gives a positive-semidefinite residual
decomposition of every unprojected fourth moment and a sharp
sum-of-squares equality.  The equality is already equivalent to a genuine
tight colouring.

This is therefore an exact boundary theorem, not a solution of
Erdős--Rosenfeld Problem #835.  At \(k=16\) it reformulates the missing
condition; it does not prove that condition either possible or impossible.

## 1. Setting and audit of the projected contractions

Put
\[
 p=k+1,\qquad
 X=\binom{[2k]}k,\qquad N=|X|,\qquad d=N/p,
\]
and let \(W=W_{k-1,k}(2k)\), \(K=\ker_{\mathbb R}W\).  Let \(P=P_K\)
be orthogonal projection onto \(K\).  The all-one vector belongs to
\(K^\perp\).

The projected cubic system \(C_p\) asks for \(q_a\in K\),
\(a\in\{0,\ldots,p-1\}\), satisfying
\[
\begin{aligned}
 \sum_aq_a&=0,\\
 \langle q_a,q_b\rangle&=N(p\delta_{ab}-1),\\
 P(q_aq_b)&=b_{ab}:=
 p\delta_{ab}q_a-q_a-q_b.
\end{aligned}                                                    \tag{1}
\]
Thus \(b_{aa}=(p-2)q_a\) and \(b_{ab}=-q_a-q_b\) for \(a\ne b\).

The claim that every contraction made only from \(\beta\), the \(q_a\)'s,
and the inner product is model-consistent is correct, with an important
scope qualification.  The span \(U=\langle q_a\rangle\) is
\(\beta\)-closed by (1).  Hence every rooted \(\beta\)-word reduces,
by induction on the tree, to a linear combination of the \(q_a\)'s.
Every inner product of two such words then reduces to the Gram matrix in
(1).  All reductions are simultaneously realized on the \(p\)-point
model
\[
 \chi_a(t)=p\boldsymbol1_{\{a=t\}}-1,\qquad
 \beta_{\rm mod}(x,y)=\pi(xy),
 \qquad
 \langle x,y\rangle_{\rm mod}=d\sum_t x(t)y(t),
\]
where \(\pi\) kills constants.  Indeed,
\[
\begin{aligned}
 \pi(\chi_a^2)&=(p-2)\chi_a,\\
 \pi(\chi_a\chi_b)&=-\chi_a-\chi_b\quad(a\ne b),\\
 \langle\chi_a,\chi_b\rangle_{\rm mod}
 &=N(p\delta_{ab}-1).
\end{aligned}
\]
Consequently these projected contractions cannot contradict \(C_p\).
This statement does **not** include traces over an ambient basis of \(K\),
unprojected products, or \(P(q_aq_bq_c)\).  Those operations see the
part of a product in \(K^\perp\), which is precisely the new datum below.
In particular, the argument does not rule out Hilbert--Schmidt,
Schatten, or other positive forms that sum over ambient directions.

## 2. The exact \(K^\perp\) residual

Write
\[
 c_{ab}=p\delta_{ab}-1,\qquad
 R_{ab}=(I-P)(q_aq_b),\qquad
 Z_{ab}=R_{ab}-c_{ab}\boldsymbol1.                       \tag{2}
\]
For every solution of \(C_p\),
\[
 Z_{ab}\in K^\perp\cap\boldsymbol1^\perp.                \tag{3}
\]
Indeed,
\[
 \langle R_{ab},\boldsymbol1\rangle
 =\langle q_aq_b,\boldsymbol1\rangle
 =\langle q_a,q_b\rangle=Nc_{ab}.
\]

Let
\[
 M_{ab,cd}=\langle q_aq_b,q_cq_d\rangle
\]
be the unprojected fourth-moment matrix, indexed by unordered colour
pairs.  Orthogonality of \(K\) and \(K^\perp\) gives the exact
decomposition
\[
\boxed{\displaystyle
 M_{ab,cd}
 =\langle b_{ab},b_{cd}\rangle
  +Nc_{ab}c_{cd}
  +\langle Z_{ab},Z_{cd}\rangle.}                        \tag{4}
\]
The first two terms are exactly the \(p\)-point-model fourth moment.
Thus, at the level of unprojected fourth moments, the entire layer beyond
the projected cubic is the Gram matrix
\[
 Q_{ab,cd}:=\langle Z_{ab},Z_{cd}\rangle.                \tag{5}
\]
In particular:

* \(Q\succeq0\);
* \(Q\) has the full four-index symmetry inherited from pointwise
  multiplication;
* \(\sum_bZ_{ab}=0\), and hence all corresponding colour-sum contractions
  of \(Q\) vanish;
* \(\operatorname{rank}Q\le\dim(K^\perp\cap\boldsymbol1^\perp)\).

No assumption of a colouring was used in (2)--(5); these are identities
for every real solution of \(C_p\).

For a genuine tight colouring, \(q_a=p\boldsymbol1_{C_a}-\boldsymbol1\)
and pointwise multiplication gives
\[
 q_aq_b=b_{ab}+c_{ab}\boldsymbol1.                       \tag{6}
\]
Therefore every \(Z_{ab}\) and \(Q\) vanishes.

## 3. Explicit model fourth moments

For a tight colouring the value of \(M_{ab,cd}\) depends only on the
multiplicity partition of the four colour indices.  With
\[
 A=p^2-3p+3,
\]
the five values are
\[
\begin{array}{c|c}
\text{multiplicities of }a,b,c,d&M_{ab,cd}\\ \hline
4&N(p-1)A\\
3+1&-NA\\
2+2&N(2p-3)\\
2+1+1&N(p-3)\\
1+1+1+1&-3N.
\end{array}                                             \tag{7}
\]
For example, (7) follows directly by summing
\[
 d\sum_{t=0}^{p-1}
 \prod_{x\in(a,b,c,d)}(p\delta_{tx}-1).
\]
Equivalently, it follows from (4) after putting \(Q=0\).

The corresponding projected triple products are
\[
P(q_aq_bq_c)=
\begin{cases}
 Aq_a,&a=b=c,\\
 -(p-2)q_a+q_b,&\text{indices }a,a,b,\ a\ne b
   \quad\text{(\(a\) repeated)},\\
 q_a+q_b+q_c,&a,b,c\text{ distinct}.
\end{cases}                                             \tag{8}
\]
These are not consequences of \(C_p\): they use the missing residual.

## 4. A sharp fourth-moment completion theorem

The full matrix \(Q\) is more information than is needed.

**Theorem.**  Suppose \(q_0,\ldots,q_{p-1}\) solve \(C_p\).  Then
\[
\boxed{\displaystyle
 \sum_a\sum_{S\in X}q_a(S)^4
 \ \ge\ pN(p-1)(p^2-3p+3).}                            \tag{9}
\]
Equality holds if and only if the functions
\[
 f_a=\frac{\boldsymbol1+q_a}{p}
\]
are the indicators of a partition of \(X\) into \(p\) systems
\(S(k-1,k,2k)\).  Hence \(C_p\) plus the single aggregate equality in
(9) is equivalent to a tight \(p\)-colouring.

**Proof.**  For a fixed \(a\), (4) on the pair \(aa,aa\) gives
\[
 \sum_Sq_a(S)^4
 =N(p-1)A+\|Z_{aa}\|^2.                                \tag{10}
\]
For completeness, this is also just Cauchy--Schwarz.  The cubic equation
gives \(P(q_a^2)=(p-2)q_a\).  Its orthogonal residual \(R_{aa}\) has
\[
 \langle R_{aa},\boldsymbol1\rangle
 =\|q_a\|^2=N(p-1),
\]
so
\[
 R_{aa}=(p-1)\boldsymbol1+Z_{aa},
\qquad
 \|R_{aa}\|^2=N(p-1)^2+\|Z_{aa}\|^2.
\]
This is the equality case decomposition behind Cauchy--Schwarz:
\(\|R_{aa}\|^2\ge N(p-1)^2\), with equality exactly when
\(R_{aa}=(p-1)\boldsymbol1\).  Adding the squared norm
\((p-2)^2\|q_a\|^2\) of the projected part gives (10) exactly.

Summing (10) proves (9).  Equality in (9) forces every \(Z_{aa}=0\), so
\[
 q_a^2=(p-2)q_a+(p-1)\boldsymbol1
\]
pointwise.  Thus every value of \(q_a\) is one of the two roots
\(-1,p-1\).  At each \(S\in X\), the relation \(\sum_aq_a(S)=0\) then
forces exactly one colour to take the value \(p-1\).  Hence the \(f_a\)'s
are zero-one indicators forming a partition.

Finally, every \((k-1)\)-set has \(k+1=p\) extensions to a \(k\)-set, so
\(W\boldsymbol1=p\boldsymbol1\).  Since \(Wq_a=0\),
\[
 Wf_a=p^{-1}(W\boldsymbol1+Wq_a)=\boldsymbol1.
\]
Each \(f_a\) is therefore an \(S(k-1,k,2k)\).  The converse follows from
(6), or by direct substitution. \(\square\)

The same theorem shows that, within \(C_p\), any of the following
apparently stronger additions is equivalent to (9):

1. all fourth moments equal the table (7);
2. \(Q=0\);
3. \(P(q_a^3)=Aq_a\) for every \(a\);
4. \(q_a^2=(p-2)q_a+(p-1)\boldsymbol1\) for every \(a\).

Thus the first unprojected fourth-moment layer does distinguish a true
colouring from every false projected solution, but it does so by becoming
exactly the original colouring problem.

## 5. Exact controls and the \(k=16\) boundary

For \(k=2,p=3,N=6\), the three perfect matchings of \(K_4\) give a tight
colouring.  Here \(A=3\), each fourth moment in the first row of (7) is
\(36\), and the aggregate in (9) is \(108\).

For \(k=4,p=5,N=70\), equality would produce five pairwise disjoint
\(S(3,4,8)\)'s.  Exact-cover enumeration gives all thirty labelled
systems; their disjointness graph is 8-regular and triangle-free, so its
clique number is \(2\), not \(5\).  The strengthened system is therefore
exactly infeasible at this false control.  Notice that each individual
\(S(3,4,8)\) does attain the one-colour fourth-moment equality
\[
 \sum_Sq(S)^4=3640;
\]
the obstruction is simultaneous compatibility of all five colours.
This result does not decide whether the projected cubic \(C_5\) alone is
feasible.

At \(k=16,p=17\),
\[
\begin{aligned}
N&=601\,080\,390,& A&=241,\\
N(p-1)A&=2\,317\,765\,983\,840,\\
pN(p-1)A&=39\,402\,021\,725\,280.
\end{aligned}
\]
A solution of \(C_{17}\) reaches this aggregate lower bound exactly when
it is the desired tight colouring.  No independent upper bound, strict
lower gap, or contradiction at \(p=17\) is proved here.

## 6. Verification

Run

```bash
python3 -B evidence/verify_unprojected_fourth_moment_completion.py
```

The checker uses only Python integer arithmetic.  It independently checks
the model multiplication and fourth-moment table, the \(k=2\) tight
colouring, all thirty exact-cover-generated \(S(3,4,8)\)'s and their
complete disjointness graph, and the displayed \(p=17\) arithmetic.
