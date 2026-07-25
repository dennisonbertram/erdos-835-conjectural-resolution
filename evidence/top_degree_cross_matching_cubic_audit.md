# Cross-matching cubic identities from idempotence

This note supplies a top-degree identity that genuinely couples different
perfect matchings.  It also records a sharp limitation: all cross-matching
*linear* constraints and the global first and second moments of the
zero-one indicators still have a real, global solution at the known-false
parameter \(k=4\).  Thus the cubic identity is a new necessary condition,
not a solution of Erdős--Rosenfeld Problem #835.

Let \(p=k+1\) be prime, \(X=\binom{[2k]}k\), and assume for this section
that a tight \(p\)-colouring exists.  Write \(f_a=\boldsymbol1_{C_a}\) for
the colour indicators, and put

\[
 q_a=p f_a-\boldsymbol1\qquad(a\in\mathbb F_p).
\tag{1}
\]

If \(W=W_{k-1,k}(2k)\), then the rainbow lower stars give
\(Wf_a=\boldsymbol1\), while \(W\boldsymbol1=p\boldsymbol1\).  Hence

\[
 q_a\in K:=\ker_{\mathbb Q}W,\qquad \sum_aq_a=0.
\tag{2}
\]

Denote orthogonal projection onto \(K\) by \(P_K\).  For every unoriented
perfect matching \(M\), fix an arbitrary orientation once and use it to
define the top polytabloid \(e_M\).  These polytabloids have the exact frame
operator

\[
 \sum_M e_Me_M^{\mathsf T}=p!P_K.
\tag{3}
\]
This is the frame identity proved in
`top_degree_pairing_derivative_audit.md`.

## The projected-idempotence identity

The pointwise zero-one identities have a particularly simple top
projection.  For all colours \(a,b\),

\[
 \boxed{\quad
 P_K(q_aq_b)=
 \begin{cases}
 (p-2)q_a,&a=b,\\
 -q_a-q_b,&a\ne b.
 \end{cases}
 \quad}
\tag{4}
\]

Indeed, \(f_a^2=f_a\) and \(f_af_b=0\) for \(a\ne b\) give, before
projection,

\[
 q_a^2=(p-2)q_a+(p-1)\boldsymbol1,
 \qquad
 q_aq_b=-q_a-q_b-\boldsymbol1 \quad(a\ne b).
\tag{5}
\]
The constant terms vanish under \(P_K\), proving (4).

Define the integral top derivatives and the triple-overlap tensor by

\[
 D_M(a)=\langle q_a,e_M\rangle,
 \qquad
 T_{MNL}=\sum_{S\in X}e_M(S)e_N(S)e_L(S).
\tag{6}
\]

The signed colour count of the earlier note is
\(\Delta_M(a)=D_M(a)/p\).  By (3), every \(q_a\in K\) has the exact
reconstruction

\[
 q_a={1\over p!}\sum_N D_N(a)e_N.
\tag{7}
\]

Taking the inner product of (4) with \(e_M\) and inserting (7) twice
gives the promised cubic system:

\[
 \boxed{\quad
 {1\over(p!)^2}\sum_{N,L}D_N(a)D_L(b)T_{MNL}
 =
 \begin{cases}
 (p-2)D_M(a),&a=b,\\
 -D_M(a)-D_M(b),&a\ne b.
 \end{cases}
 \quad}
\tag{8}
\]

The equation indexed by \(M\) couples the derivative factors \(D_N,D_L\)
through the three-polytabloid tensor \(T_{MNL}\); the indices are allowed to
coincide.  In particular, the system cannot be recovered from a distribution
of the signed count vector for one matching, even if that distribution has
the exact quadratic frame covariance.  This is the specific missing
information in the weighted local-cube witness of the earlier audit.

The derivatives also satisfy the ordinary four-point Plücker
straightening relations coordinatewise, because those are identities among
the functions \(e_M\).  Thus (8) combines that simultaneous
cross-matching linear structure with a genuine zero-one consequence.

## A global cross-matching quadratic relaxation remains feasible at \(k=4\)

It is useful to separate (8) from the consequences that are only
quadratic.  From (1) one obtains

\[
 \langle q_a,q_b\rangle=
 \begin{cases}
 p d(p-1),&a=b,\\
 -pd,&a\ne b,
 \end{cases}
 \qquad d={1\over p}\binom{2k}k.
\tag{9}
\]

Consider the following relaxation:

1. choose real \(q_0,\ldots,q_{p-1}\in K\) with \(\sum_aq_a=0\);
2. impose exactly the Gram matrix (9);
3. set \(f_a=p^{-1}(\boldsymbol1+q_a)\), but do **not** require its
   coordinates to be zero or one.

This is already a global, not matching-by-matching, relaxation.  Equation
(3) makes all of its matching derivatives simultaneous; consequently they
satisfy every Plücker straightening relation and the full quadratic
frame identity.  Moreover,

\[
 Wf_a=\boldsymbol1,\qquad \sum_af_a=\boldsymbol1,\qquad
 \langle f_a,f_b\rangle=d\,\delta_{ab}.
\tag{10}
\]
Thus it retains the global partition equations and pairwise inner products
(9)--(10), but not pointwise idempotence.

At the false control \(k=4,p=5,d=14\), it has an explicit real solution.
The top space \(K\) has dimension \(14\), so take any orthonormal
four-frame \(u_1,\ldots,u_4\) in it.  Let \(h_a\in\mathbb R^4\) be the
five rows of the normalized Helmert matrix; equivalently,

\[
 h_ah_b^{\mathsf T}=\delta_{ab}-{1\over5},\qquad\sum_ah_a=0.
\tag{11}
\]

Then

\[
 q_a=\sqrt{350}\sum_{i=1}^4h_{a,i}u_i
\tag{12}
\]

satisfies (9), since its diagonal and off-diagonal inner products are
\(280\) and \(-70\), respectively.  This construction is checked
entirely with rational Gram arithmetic by the companion verifier, which
also constructs the required four-frame from matching polytabloids.

There is nevertheless no tight five-colouring of \(J(8,4)\): the exact
control enumerates all 30 labelled \(S(3,4,8)\)'s and finds that at most
two are pairwise block-disjoint.  So this relaxation is an exact
cross-matching countermodel to every argument that uses only (2),
Plücker straightening, and the global partition equations and pairwise
inner products (9)--(10).  It does
not satisfy (4) in general; the cubic projected-idempotence equations are
strictly additional.

## Controls and scope

For \(k=2,p=3\), the unique tight colouring of \(J(4,2)\) satisfies
(4), (7), and every equation (8) directly.  For \(k=4,p=5\), the same
verifier independently confirms the exact non-colouring control and the
feasibility of the global quadratic relaxation above.

This neither proves nor disproves a tight \(17\)-colouring of
\(J(32,16)\).  It identifies a concrete next barrier: any successful
top-degree proof must use (8), stronger pointwise information, or another
condition not implied by the global quadratic relaxation.

Run

```bash
python3 -B evidence/verify_top_degree_cross_matching_cubic.py
```

for the exact \(k=2\) cubic check, the \(k=4\) false control, and the
rational Gram construction of the \(k=4\) relaxation.
