# Degree-three state refinement: exact commutators and the finite frontier

## Status and scope

Assume that a \(k=16\) cover

\[
O_{16}=KG(31,15)\longrightarrow K_{17}
\]

exists, fix one fibre \({\cal C}\), and let \(R\) join two fibre blocks
meeting in one point.  Write \(A_s\) for the fibre intersection-\(s\)
matrix, \(P=P_3\) for the projector onto the degree-three harmonic space
\({\cal H}_3\), and

\[
n=|{\cal C}|=17\,678\,835,\qquad d=\dim{\cal H}_3=4030.
\]

This note refines the degree-three support theorem to a pointwise local
state.  Its main conclusions are:

* the first \(R\)-leakage is exactly the orientation asymmetry of a
  one-factorization statistic;
* the four state matrices of \(Q\) are exactly the four possible values of
  a masked entry of \(RP\);
* the first \(Q\)-leakage is another explicit integer commutator;
* all degree-at-most-three pairwise moment equations remain feasible.

There is no contradiction and no construction here.  In particular, this
does **not** exclude \(k=16\) and does not settle Erdős--Rosenfeld problem
#835.

## 1. The degree-three Johnson kernel

The fibre is an \(S(14,15,31)\).  For \(B,C\in{\cal C}\), put
\(s=|B\cap C|\).  Normalize the degree-three kernel by

\[
K=\frac ndP.
\]

Then \(K_{BC}=\psi(s)\), where

\[
\boxed{
\psi(u)=
\frac{261u^3-5684u^2+39730u-88725}{109200}.
}
\tag{1}
\]

Fix \(B\), set \(Y=[31]\setminus B\), and let

\[
D_e=(Y\setminus e)\cup\{\phi_B(e)\},
\qquad e\in\binom Y2,
\tag{2}
\]

be the \(120\) \(R\)-neighbours of \(B\).  The map
\(\phi_B:E(K_Y)\to B\) is a one-factorization: for each \(b\in B\),
the edges with colour \(b\) form a perfect matching of \(Y\).

For a second block \(C\), define

\[
I=B\cap C,\qquad U=C\setminus B,\qquad
a=|U|=15-s,
\]

and the integer state

\[
\boxed{
x_{BC}=
\#\{e\in\binom U2:\phi_B(e)\in I\}.
}
\tag{3}
\]

This state is rooted: in general \(x_{BC}\) need not equal \(x_{CB}\).

## 2. Exact pointwise action of \(R\)

For \(r=0,1,2\), let \(x_r\) count edges \(e\) with
\(|e\cap U|=r\) and \(\phi_B(e)\in I\).  Thus \(x_2=x_{BC}\).
For each colour in \(I\), compare the numbers of matching edges internal
to \(U\), internal to \(Y\setminus U\), and crossing between them.
Since \(|Y\setminus U|=s+1\), summing

\[
2u_c+c_c=a,\qquad 2w_c+c_c=s+1
\]

over the \(s\) colours in \(I\) gives

\[
x_0=x_{BC}+s(s-7),\qquad
x_1=s(15-s)-2x_{BC}.
\tag{4}
\]

Moreover,

\[
|D_e\cap C|=a-r+\mathbf1_{\{\phi_B(e)\in I\}}.
\tag{5}
\]

Substituting (4)--(5) into

\[
(RK)_{BC}=\sum_{e\in\binom Y2}\psi(|D_e\cap C|)
\]

and using the constant third finite difference of the cubic (1) yields

\[
\boxed{
(RK)_{BC}=\frac{h_s+1566x_{BC}}{109200}
\qquad(1\le s\le13),
}
\tag{6}
\]

where

\[
\begin{array}{c|rrrrrrr}
s&1&2&3&4&5&6&7\\ \hline
h_s&
3244696&1772511&795240&218923&-50400&-106689&-43904
\end{array}
\]

\[
\begin{array}{c|rrrrrr}
s&8&9&10&11&12&13\\ \hline
h_s&
43995&63048&-80705&-481224&-1232469&-2428400.
\end{array}
\]

Because \(R\), \(K\), and \(P\) are symmetric,
\((KR)_{BC}=(RK)_{CB}\).  The scalar part of (6) depends only on \(s\)
and cancels under reversal.  The numerical normalization also collapses:

\[
\frac dn\frac{1566}{109200}=\frac1{305900}.
\]

Consequently, with

\[
\Delta_{BC}=x_{BC}-x_{CB},
\]

we obtain the exact pointwise commutator

\[
\boxed{
[R,P]:=RP-PR=\frac{\Delta}{305900}.
}
\tag{7}
\]

Thus the possible failure of \(R\) to preserve \({\cal H}_3\) is not an
abstract positive operator: it is precisely the rooted
one-factorization asymmetry \(\Delta\).

## 3. The leakage Gram and \(\operatorname{tr}Z^2\)

In the orthogonal decomposition
\(\mathbb R^{\cal C}={\cal H}_3\oplus{\cal H}_3^\perp\), write

\[
R=\begin{pmatrix}A&L^*\\L&C_0\end{pmatrix},
\qquad
A=PRP,\qquad L=(I-P)RP.
\tag{8}
\]

Then

\[
[R,P]=\begin{pmatrix}0&-L^*\\L&0\end{pmatrix}.
\]

It follows from (7) that

\[
\boxed{
D:=L^*L
=\frac1{305900^2}P\Delta^{\mathsf T}\Delta P.
}
\tag{9}
\]

If the last sum below runs over unordered pairs of fibre blocks, then

\[
\boxed{
\operatorname{tr}D
=\frac{\displaystyle\sum_{\{B,C\}}\Delta_{BC}^2}
       {93\,574\,810\,000}.
}
\tag{10}
\]

The degree-three support theorem writes

\[
A=-63P+15Z,\qquad 0\preceq Z\preceq\frac35P
\]

and gives
\(\operatorname{tr}D=47\,740-225\operatorname{tr}(Z^2)\).
Therefore (10) sharpens the trace interval to an exact discrete identity:

\[
\boxed{
\operatorname{tr}(Z^2)
=\frac{9548}{45}
-\frac{\displaystyle\sum_{\{B,C\}}\Delta_{BC}^2}
 {225\cdot93\,574\,810\,000}.
}
\tag{11}
\]

In particular, the upper endpoint
\(\operatorname{tr}(Z^2)=9548/45\) occurs exactly when every rooted state
is reversal-symmetric, \(x_{BC}=x_{CB}\).

## 4. The four \(Q\)-states are masked \(RP\)-entries

Suppose \(|B\cap C|=12\).  Put
\(A_0=B\setminus C\), so \(|A_0|=|U|=3\).  The three edges of the
triangle on \(U\) have distinct one-factorization colours, and the common
\(R\)-neighbour count is

\[
q_{BC}=Q_{BC}
=\#\{e\in\binom U2:\phi_B(e)\in A_0\}.
\tag{12}
\]

Hence \(x_{BC}=3-q_{BC}\).  Substituting \(s=12\) into (6), and restoring
the factor \(d/n\), gives

\[
\boxed{
(RP)_{BC}
=-\frac{45473}{17742200}-\frac{q_{BC}}{305900}
\qquad(|B\cap C|=12).
}
\tag{13}
\]

Define the four symmetric zero-one state matrices

\[
(Q_r)_{BC}
=\mathbf1_{\{|B\cap C|=12,\ q_{BC}=r\}},
\qquad 0\le r\le3.
\tag{14}
\]

Then

\[
A_{12}=Q_0+Q_1+Q_2+Q_3,\qquad
Q=Q_1+2Q_2+3Q_3,
\tag{15}
\]

and (13) says that the four \(Q_r\) are exactly the four equally spaced
levels of \(A_{12}\circ(RP)\).

For a fixed \(B\), let \(n_r(B)\) be the row sum of \(Q_r\), and put

\[
\tau_B=n_2(B)+3n_3(B)
=\sum_C\binom{q_{BC}}2.
\tag{16}
\]

The row sum and support size give

\[
\sum_{r=0}^3n_r(B)=14560,\qquad
n_1(B)+2n_2(B)+3n_3(B)=10080.
\tag{17}
\]

There is also the exact local bound

\[
\boxed{0\le\tau_B\le1680.}
\tag{18}
\]

One proof counts triples \((\{E,F\},D)\) with
\(E,F\in N_R(B)\), \(|E\cap F|=13\), and
\(D\ne B\) a common \(R\)-neighbour of \(E,F\).
There are \(2100\) choices of \(\{E,F\}\) and four choices of \(D\),
for \(8400\) triples.  Each of the \(840\) blocks \(D\) with
\(|B\cap D|=13\) contributes at least eight of the ten pairs among its
five common neighbours with \(B\), for at least \(6720\) triples.  A
block with \(|B\cap D|=12\) contributes
\(\binom{q_{BD}}2\), because its common neighbours with \(B\) correspond
to edges of one triangle and hence meet pairwise in \(13\) points.
Thus \(6720+\tau_B\le8400\).

Equations (16)--(18) improve the pointwise square-row bound to

\[
\boxed{
\sum_CQ_{BC}^2=10080+2\tau_B\le13440.
}
\tag{19}
\]

## 5. The first \(Q\)-leakage is another integer commutator

The full degree-three relation theorem gives

\[
A_{13}P=(R+372I)P.
\tag{20}
\]

Taking transposes shows
\([A_{13},P]=[R,P]\).  Since

\[
Q=R^2-120I-5A_{13},
\]

the commutator identity
\([R^2,P]=R[R,P]+[R,P]R\), together with (7), gives

\[
\boxed{
[Q,P]=\frac{\Gamma}{305900},\qquad
\Gamma:=R\Delta+\Delta R-5\Delta.
}
\tag{21}
\]

The matrix \(\Gamma\) is an integer skew-symmetric matrix.  In the block
form (8), if

\[
N=(I-P)QP,
\]

then

\[
[Q,P]=\begin{pmatrix}0&-N^*\\N&0\end{pmatrix},
\qquad
N=C_0L+L(A-5I).
\tag{22}
\]

Thus the previously unforced complementary orientation \(C_0L\) is
captured exactly by \(\Gamma\):

\[
\boxed{
N=\frac1{305900}\Gamma P.
}
\tag{23}
\]

Orthogonally decomposing \(QP=PQP+N\) now gives the operator identity

\[
\boxed{
PQ^2P
=(PQP)^2
+\frac1{305900^2}P\Gamma^{\mathsf T}\Gamma P.
}
\tag{24}
\]

In particular,

\[
\boxed{
\operatorname{tr}\!\left(PQ^2P-(PQP)^2\right)
=\frac{\displaystyle\sum_{\{B,C\}}\Gamma_{BC}^2}
       {93\,574\,810\,000}.
}
\tag{25}
\]

The known compression

\[
PQP=225Z^2-1965Z+2304P+D
\tag{26}
\]

therefore does not determine \(PQ^2P\).  The exact missing datum is the
integer state commutator \(\Gamma\), or equivalently the leakage in
(22)--(25).

## 6. Pairwise degree-three moments remain feasible

Fix \(B,C\) with \(|B\cap C|=12\), and write \(q=q_{BC}\).  Define

\[
N_t=\#\{D\in{\cal C}:|B\cap D|=12,\ |C\cap D|=t\}.
\tag{27}
\]

Set

\[
\begin{aligned}
\psi_0(t)&=1,\\
\psi_1(t)&=\frac{-225+31t}{240},\\
\psi_2(t)&=\frac{1470-421t+29t^2}{1680},\\
\psi_3(t)&=\psi(t).
\end{aligned}
\]

The exact actions of \(A_{12}\) on
\({\cal H}_0,{\cal H}_1,{\cal H}_2,{\cal H}_3\) give

\[
\begin{aligned}
\sum_tN_t\psi_0(t)&=14560,\\
\sum_tN_t\psi_1(t)&=8918\psi_1(12),\\
\sum_tN_t\psi_2(t)&=5148\psi_2(12),\\
\sum_tN_t\psi_3(t)&=2022\psi_3(12)-12(RK)_{BC}.
\end{aligned}
\tag{28}
\]

Set geometry and the forbidden intersection \(14\) give
\(t\in\{9,10,11,12,13,15\}\), with \(N_{15}=1\).
Solving (28) leaves exactly one integer \(z=N_{13}\):

\[
\boxed{
\begin{array}{c|rrrrrr}
t&9&10&11&12&13&15\\ \hline
N_t&
3490-12q+z&
6606+36q-4z&
3075-36q+6z&
1388+12q-4z&
z&
1 .
\end{array}}
\tag{29}
\]

Every \(q\in\{0,1,2,3\}\) is feasible already with \(z=0\).
More generally, all entries in (29) are nonnegative whenever

\[
0\le z\le347+3q.
\tag{30}
\]

Even adjoining the forced degree-at-most-two \(Q\)-moments does not
remove any of the four states.  Put

\[
M_t=\sum_{\substack{D:\ |B\cap D|=12\\|C\cap D|=t}}q_{BD}.
\tag{31}
\]

The actions
\(QP_0=10080P_0\), \(QP_1=6174P_1\), and
\(QP_2=3564P_2\) require

\[
\sum_tM_t\psi_j(t)=
\begin{cases}
10080,&j=0,\\
6174\psi_1(12),&j=1,\\
3564\psi_2(12),&j=2.
\end{cases}
\tag{32}
\]

For \(z=0\), the following nonnegative integral table satisfies (32),
has \(M_{15}=q\), and obeys \(0\le M_t\le3N_t\):

\[
\boxed{
\begin{array}{c|rrrrrr}
t&9&10&11&12&13&15\\ \hline
M_t&
1710-5q&
6696+9q&
0&
1674-5q&
0&
q .
\end{array}}
\tag{33}
\]

Thus the first three raw moments, the full \(H_3\) raw moment, and the
first three \(Q\)-weighted moments admit exact integer witnesses for
every state \(q=0,1,2,3\).  A pairwise moment LP cannot be the missing
contradiction.

## 7. A minimal finite combinatorial formulation

The state equations above have a useful one-root exact-cover form.
Fix \(B\) and write \(F_a=\phi_B^{-1}(a)\) for its fifteen perfect
matchings on \(Y\).

For each pair \(P=\{a,b\}\subset B\), the eight blocks meeting \(B\)
in \(B\setminus P\) add the edges of a perfect matching \(G_P\) on
\(Y\).  It is disjoint from \(F_a\cup F_b\).  If
\(A=\{a,b,c\}\), then \(G_{ab},G_{ac},G_{bc}\) are pairwise
edge-disjoint.

For each triple \(A\subset B\), exactly \(32\) blocks meet \(B\) in
\(B\setminus A\).  Write their three-point outside parts as
\({\cal T}_A\subseteq\binom Y3\).  Two members of \({\cal T}_A\)
cannot share an edge, and none can contain an edge of
\(G_{ab}\cup G_{ac}\cup G_{bc}\).  The three matchings contain
\(24\) edges, while the \(32\) triples contain \(96\) distinct edges.
Consequently

\[
\boxed{
{\cal T}_A\text{ is a triangle decomposition of }
K_{16}-(G_{ab}\cup G_{ac}\cup G_{bc}).
}
\tag{34}
\]

There is a dual coupling.  Let \(e,f\) be two incident edges of an
outside triangle \(U\), let their \(F\)-colours be \(a,b\), and let
\(g\) be the third edge of \(U\).  The five-common-neighbour identity
for the corresponding intersection-\(13\) pair gives

\[
\boxed{
\sum_{\substack{A\in\binom B3\\\{a,b\}\subset A}}
\mathbf1_{\{U\in{\cal T}_A\}}
=1-\mathbf1_{\{g\in G_{ab}\}}.
}
\tag{35}
\]

Equations (34)--(35) give a finite Boolean model with:

* \(105\) perfect matchings \(G_{ab}\) on a \(16\)-set;
* \(455\cdot560\) possible triangle choices
  \(y_{A,U}=\mathbf1_{\{U\in{\cal T}_A\}}\);
* exact edge-cover constraints for every cubic leave in (34);
* the shared trace constraints (35).

This is a necessary one-root truncation, not a cover construction.  A
certificate of infeasibility would rule out the hypothetical cover, but a
feasible witness would prove only local consistency.  To determine
\(\Delta\) and \(\Gamma\), one must additionally couple the rooted
one-factorizations at both ends of every fibre pair.  That two-root/global
coupling is exactly what the scalar and pairwise moment systems omit.

## 8. Exact verification

Run

```sh
python3 -B \
  collaboration/h3_state_refinement/verify_h3_state_refinement.py
```

The verifier uses only exact integers and `Fraction`.  It checks the four
Johnson kernels, all thirteen pointwise \(h_s\) identities, the
\(305900\) normalization, the four \(Q\)-levels, the leakage trace
denominators, every entry of the moment witnesses (29) and (33), the
\(\tau_B\) arithmetic, and the finite-model counts.
