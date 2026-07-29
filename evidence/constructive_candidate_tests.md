# Exact failures of two \(k=16\) candidate formulas

These are reproducible counterexamples to two concrete algebraic formulas.
They are not nonexistence proofs for arbitrary colourings.

Run

```bash
python3 evidence/verify_constructive_candidates.py
```

to check all finite-field arithmetic, Pfaffians, and repeated colours.

## 1. A \(P^1(\mathbb F_{16})\) leading-coefficient formula

The exact odd-neighbour lift reduces the \(k=16\) problem to a proper
17-colouring of \(J(30,15)\).  Write the 30 points as
\[
\mathbb F_{16}^{\times}\times\{0,1\}.
\]
For a 15-set \(S\), put
\[
\begin{aligned}
A&=\{a:(a,0)\in S\},\\
B&=\{a:(a,1)\in S\},\\
C&=\mathbb F_{16}^{\times}\setminus B.
\end{aligned}
\]
Then \(|A|=|C|\).  Define
\[
P_A(X)=\prod_{a\in A}(X-a),\qquad
P_C(X)=\prod_{a\in C}(X-a),
\]
and \(D_{A,C}=P_A-P_C\).  If
\[
D_{A,C}=d_rX^r+d_{r-1}X^{r-1}+\cdots,\qquad d_r\ne0,
\]
the most immediate projective-line colour is
\[
\ell(A,C)=d_{r-1}/d_r\in\mathbb F_{16},
\]
with \(D_{A,C}=0\) assigned the extra colour \(\infty\).

This formula has a useful-looking covariance: adding or deleting a point
common to \(A\) and \(C\) multiplies or divides \(D_{A,C}\) by a linear
factor, translating \(\ell\) by that point.  Nevertheless it is not proper.

Use the polynomial presentation
\[
\mathbb F_{16}=\mathbb F_2[\alpha]/(\alpha^4+\alpha+1),
\]
representing field elements by the integers \(0,\ldots,15\) via their
four binary coefficients.  Let
\[
\begin{aligned}
A_1&=\{3,4,5,7,9,13,15\},\\
A_2&=\{1,3,4,5,7,9,15\},\\
C&=\{2,3,6,9,12,14,15\}.
\end{aligned}
\]
The corresponding 15-sets are adjacent: they have the same second-layer
part and their first-layer parts differ by replacing 13 with 1.

In low-to-high coefficient order, exact multiplication gives
\[
\begin{aligned}
D_{A_1,C}&=(13,15,9,5,1,4,13),\\
D_{A_2,C}&=(3,2,4,10,7,3,1).
\end{aligned}
\]
Thus
\[
\ell(A_1,C)=4/13=3=\ell(A_2,C).
\]
The proposed formula assigns the same colour to adjacent vertices.

## 2. The Paley-conference Pfaffian formula

Put the 32 ground points on
\[
\mathbb P^1(\mathbb F_{31})
=\{0,1,\ldots,30,\infty\}.
\]
Let \(\chi\) be the quadratic character of \(\mathbb F_{31}\), and form the
alternating \(32\times32\) matrix \(M\) over \(\mathbb F_{17}\) by
\[
\begin{aligned}
M_{ij}&=\chi(j-i) &&(0\le i<j\le30),\\
M_{i,\infty}&=-1 &&(0\le i\le30),\\
M_{ji}&=-M_{ij},\qquad M_{ii}=0.
\end{aligned}
\]
The canonical Pfaffian proposal is
\[
c(S)=\operatorname{Pf}(M[S])\in\mathbb F_{17},
\qquad |S|=16.
\]

Take the 15-set
\[
T=\{0,1,2,3,4,7,9,12,15,17,23,24,27,30,\infty\}.
\]
In increasing order, the seventeen points outside \(T\) are
\[
5,6,8,10,11,13,14,16,18,19,20,21,22,25,26,28,29.
\]
The exact Pfaffian colours of the seventeen extensions \(T\cup\{x\}\) are,
in that order,
\[
(0,4,6,2,12,8,6,6,8,10,7,2,15,11,0,12,9).
\]
Only eleven distinct values occur.  In particular, this star is not
rainbow.

Multiplying row and column \(i\) by a nonzero scalar \(s_i\) multiplies
the principal Pfaffian on \(S\) by \(\prod_{i\in S}s_i\).  On the displayed
star, this cannot repair the two zero values.  Consequently every matrix
diagonally equivalent to this Paley conference matrix fails as well.

## 3. Every postprocessing of the 32nd-root sum

The Fermat-prime identity
\[
32\mid(17^2-1)
\]
suggests labelling the ground points by the 32nd roots of unity in
\(\mathbb F_{17^2}\), summing the labels of a 16-set, and mapping the sum
to seventeen colours by a trace, norm, power map, or arbitrary lookup.
An exact subset-sum calculation rules out **every** postprocessing of this
additive statistic.

Use
\[
K=\mathbb F_{17}[\beta]/(\beta^2-3).
\]
The element 3 is a quadratic nonresidue modulo 17, and \(\beta\) has order
32.  Let
\[
H=\langle\beta\rangle\subset K^\times,\qquad |H|=32.
\]
The verifier establishes the following two exact statements.

1. \(H-H=K\).
2. For every distinct \(x,y\in H\) and every \(a\in K\), there is a
   15-subset \(T\subset H\setminus\{x,y\}\) with
   \[
   \sum_{t\in T}t=a.
   \]

The second check only needs the 31 cases \(\{1,r\}\), \(r\in H\setminus
\{1\}\), because multiplication by \(x^{-1}\) is an additive bijection
and preserves \(H\).  For each case, the verifier uses the exact recurrence
\[
D_{j+1,s}(z)
=D_{j,s}(z)+D_{j,s-1}(z-h_j)
\]
for subset-sum counts after processing the next allowed root \(h_j\).  It
checks that all 289 entries at level \(s=15\) are positive.

Now let \(h:K\to\Omega\) be any map with \(|\Omega|=17\), and propose
\[
c(S)=h\left(\sum_{s\in S}s\right),\qquad S\in\binom H{16}.
\]
Choose distinct \(u,v\in K\) with \(h(u)=h(v)\).  By \(H-H=K\), choose
\(x,y\in H\) with \(x-y=u-v\).  By statement 2, choose a 15-set
\(T\subset H\setminus\{x,y\}\) whose sum is \(u-x\).  Then
\[
\sum(T\cup\{x\})=u,\qquad
\sum(T\cup\{y\})=u-x+y=v.
\]
These two 16-sets are adjacent and receive the same colour.

Thus trace, norm, arbitrary polynomial postprocessing, and arbitrary table
lookup of the 32nd-root sum all fail.  This conclusion is specific to the
additive statistic; it does not rule out formulas with higher-order
interactions among the selected roots.

## 4. The affine barycentre in the cyclic \(LS(4,5,21)\) model

For the forced \(LS(4,5,21)\), put the points on
\[
 \mathbb F_{17}\cup\{q_1,q_2,q_3,q_4\}
\]
and require translation by \(t\) on the finite points to add \(t\) to the
colour.  The most general point-additive affine barycentre has four fixed
weights \(w_1,\ldots,w_4\in\mathbb F_{17}\) and colours a five-set \(B\)
containing \(r\ge1\) finite points by
\[
 c(B)=\frac{\displaystyle
   \sum_{x\in B\cap\mathbb F_{17}}x+
   \sum_{q_i\in B}w_i}{r}.
 \tag{4.1}
\]
The denominator is forced by translation equivariance.  No choice of the
four weights works.

Write \(W=w_1+\cdots+w_4\).  Fix \(j\), and take the four-set consisting of
one finite point \(x\) and the three fixed points other than \(q_j\).
Extending it by a finite point \(y\ne x\) gives the sixteen colours
\[
 \frac{x+y+W-w_j}{2}.
\]
As \(y\) ranges over \(\mathbb F_{17}\setminus\{x\}\), these are all field
elements except
\[
 x+\frac{W-w_j}{2}.
\]
The remaining extension, by \(q_j\), has colour \(x+W\).  For the star to
be rainbow these two expressions must agree.  Hence
\[
 w_j=-W.
\]
This holds for all four \(j\), so \(W=-4W\), whence \(5W=0\).  Therefore
\(W=0\) and every \(w_j=0\).

Now take a four-set with two finite and two fixed points.  Its two
extensions by the two remaining fixed points have the same value in
(4.1), because all four fixed weights are zero.  The star is not rainbow.
Thus even the full four-parameter affine barycentre family fails.
