# A universal four-Pfaffian descent for the principal-Pfaffian ansatz

This note derives an exact necessary condition for a colouring of the form

\[
 c(S)=\operatorname{Pf}(M[S])\in\mathbb F_p,
 \qquad |S|=p-1,
\tag{1}
\]

where \(M\) is an alternating \((2p-2)\)-by-\((2p-2)\) matrix and
\(p\ge5\) is odd.  It does **not** prove that (1) is impossible.

## 1. The zero fibre is already a Steiner system

If (1) is rainbow on every \((p-2)\)-star, then every field value occurs
once on that star.  In particular

\[
 \mathcal Z=\{S:|S|=p-1,\ \operatorname{Pf}(M[S])=0\}
\tag{2}
\]

is an \(S(p-2,p-1,2p-2)\).  The same is true of every colour fibre;
together they are the forced large set from a hypothetical solution of
Problem #835.

The Pfaffian hypothesis has a further local consequence.  Choose a
nonzero \((p-1)\)-Pfaffian.  Repeated Pfaffian expansion shows that it has
a \((p-5)\)-subset \(Q\) with

\[
 q=\operatorname{Pf}(M[Q])\ne0.
\tag{3}
\]

Indeed, each nonzero Pfaffian expansion has a nonzero term, reducing its
size by two; repeat twice.

## 2. Exact Schur-complement identity

Put \(U=[2p-2]\setminus Q\), so \(|U|=p+3\).  In block order
\(Q,U\), write

\[
 M=\begin{pmatrix}M_Q&B\\-B^T&D\end{pmatrix},
 \qquad A_0=D+B^TM_Q^{-1}B.
\tag{4}
\]

For \(u\in U\), set

\[
 s_u=(-1)^{|\{x\in Q:x>u\}|},\qquad
 A_{uv}=s_us_v(A_0)_{uv}.
\tag{5}
\]

The signs exactly correct the fact that a principal submatrix is ordered
in the original point order rather than in block order.  The Pfaffian
Schur-complement identity therefore gives, for every four-set
\(B\subset U\),

\[
 \operatorname{Pf}(M[Q\cup B])
   =q\operatorname{Pf}(A[B]).
\tag{6}
\]

This is also the relevant Pfaffian Plücker/Dodgson reduction: all
four-Pfaffians of the complementary alternating form are actual colours,
up to the one nonzero scalar \(q\).

## 3. Forced small derived large set

For every three-set \(E\subset U\), the original star on \(Q\cup E\)
has its \(p\) possible fourth points in \(U\setminus E\).  By (6),

\[
 \bigl\{\operatorname{Pf}(A[E\cup\{u\}]):u\in U\setminus E\bigr\}
   =\mathbb F_p.
\tag{7}
\]

Thus the 4-Pfaffians of the \((p+3)\)-by-\((p+3)\) alternating matrix
\(A\) themselves give a tight \(p\)-colouring of 4-subsets of \(p+3\)
points, rainbow on every 3-star.  In particular, their zero locus is an

\[
 S(3,4,p+3),
\tag{8}
\]

and the full fibres form \(LS(3,4,p+3)\).  At \(p=17\), this is the
known forced \(LS(3,4,20)\) condition, now with the additional demand
that its colours arise as principal 4-Pfaffians of one alternating form.

For \(p=5\), (3) has \(Q=\varnothing\), so this is the original
4-Pfaffian problem on eight points.  For \(p=7,11\), it gives exact
10- and 14-point 4-Pfaffian controls.  The descent alone does not rule out
these controls: large sets of the indicated parameters are the underlying
combinatorial obstruction, and the additional Pfaffian equations still
need to be exploited.

## 4. Exact verification

`verify_pfaffian_descent_identities.py` checks (6) over \(\mathbb F_p\)
on twelve independently seeded random alternating matrices for each of
\(p=5,7,11\), and every four-subset after choosing a nonzero \(Q\).
It uses a separate modular Pfaffian-elimination routine and modular matrix
inversion.

```bash
python3 evidence/verify_pfaffian_descent_identities.py
```

The test is evidence for the bookkeeping and signs in (6), not a proof of
the general identity; the proof is the standard block Pfaffian identity,
with the explicitly displayed ordering correction (5).

## Scope

This leaves the unrestricted principal-Pfaffian family alive.  A useful
next attack is to impose the quadratic Pfaffian/Plücker relations on a
candidate \(LS(3,4,p+3)\), starting with the exact \(p=5,7,11\) controls
and then \(p=17\).  The local one-factorization condition by itself is
not contradictory: after fixing \(p-3\) points, its Schur complement is
an unrestricted alternating \((p+1)\)-by-\((p+1)\) matrix.
