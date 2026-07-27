# The degree-three commutator rank route: a support theorem and a no-go

## Status

Assume that a hypothetical \(k=16\) fibre
\({\cal C}=S(14,15,31)\) exists.  Retain the notation of
`collaboration/h3_state_refinement/README.md`: \(R\) is the
intersection-one matrix, \(P=P_3\) is the degree-three projector,

\[
x_{BC}=\#\{e\in\tbinom{C\setminus B}{2}:
              \phi_B(e)\in B\cap C\},
\qquad
\Delta_{BC}=x_{BC}-x_{CB},
\]

and

\[
[R,P]=\frac{\Delta}{305900}.
\tag{1}
\]

This note proves a genuinely stronger support restriction on \(\Delta\)
and records exactly what follows from its skew-integrality and rank.  It
does **not** obtain a contradiction and does not settle problem 835.

## 1. Exact vanishing on the \(12\)- and \(13\)-intersection layers

### Proposition 1

\[
\boxed{\Delta_{BC}=0\quad\text{if }|B\cap C|\in\{12,13,14,15\}.}
\tag{2}
\]

The cases \(14\) and distinct \(15\) do not occur in a Steiner fibre, and
the diagonal is automatic.  The two substantive cases are as follows.

If \(|B\cap C|=12\), the state-refinement identity gives

\[
x_{BC}=3-q_{BC},
\qquad q_{BC}=Q_{BC},
\]

where \(Q=R^2-120I-5A_{13}\) is symmetric.  Hence
\(q_{BC}=q_{CB}\), and therefore \(x_{BC}=x_{CB}\).

Now suppose \(|B\cap C|=13\).  Put

\[
I=B\cap C,\quad U=C\setminus B,\quad
V=B\setminus C,\quad W=[31]\setminus(B\cup C).
\]

Thus \(|U|=|V|=2\) and \(|W|=14\).  There is just one edge \(U\).
The rooted construction at \(B\) says that the unique fibre block
containing the \(14\)-set \(W\) is

\[
D=W\cup\{\phi_B(U)\},\qquad \phi_B(U)\in B.
\]

The rooted construction at \(C\), applied to its unique edge \(V\), says
that the same unique block is

\[
D=W\cup\{\phi_C(V)\},\qquad \phi_C(V)\in C.
\]

Uniqueness of the block containing \(W\) forces
\(\phi_B(U)=\phi_C(V)=b\in I\).  Consequently

\[
\boxed{x_{BC}=x_{CB}=1\qquad(|B\cap C|=13).}
\]

The common block is

\[
D=W\cup\{b\}\qquad(b\in I).
\tag{3}
\]

It is a common \(R\)-neighbour \(D\) of \(B,C\) whose
singleton intersections with \(B\) and \(C\) are the same point \(b\).

Consequently any nonzero entry of \(\Delta\) lies on an intersection
layer \(1\le |B\cap C|\le11\).  In particular the four \(Q\)-states on
the \(12\)-intersection layer cannot themselves witness degree-three
leakage.

## 2. The exact rank consequences

Write the orthogonal block decomposition

\[
R=\begin{pmatrix}A&L^*\\L&C\end{pmatrix}
\quad\text{on}\quad
{\cal H}_3\oplus{\cal H}_3^\perp .
\]

Equation (1) gives

\[
\Delta=305900
\begin{pmatrix}0&-L^*\\L&0\end{pmatrix}.
\tag{4}
\]

Therefore

\[
\boxed{
P\Delta P=0,\quad
(I-P)\Delta(I-P)=0,\quad
P\Delta+\Delta P=\Delta,
}
\tag{5}
\]

and

\[
\boxed{
\operatorname{rank}_{\mathbb Q}\Delta
=2\operatorname{rank}L\le 2\dim{\cal H}_3=8060.
}
\tag{6}
\]

Thus the rank is even.  Every principal Pfaffian of order \(8062\)
vanishes, but this is only a reformulation of (6).

The row sums also vanish.  Indeed \(P\mathbf1=0\) on the nonconstant
harmonic module and \(R\mathbf1=120\mathbf1\), so

\[
\Delta\mathbf1=305900(RP-PR)\mathbf1=0.
\]

The corrected full right action

\[
A_{13}P=(R+372I)P
\tag{7}
\]

has exactly the same leakage:

\[
(I-P)A_{13}P=(I-P)RP=L
\]

and, after transposition,

\[
[A_{13},P]=[R,P]=\Delta/305900.
\tag{8}
\]

Hence (7) supplies no second independent leakage map and does not improve
the ceiling (6).

Similarly, for
\(\Gamma=R\Delta+\Delta R-5\Delta=305900[Q,P]\),

\[
\operatorname{rank}\Gamma\le8060.
\]

This is a separate commutator bound, not a lower bound for \(\Delta\).

## 3. Why skewness, parity, row sums, and Pfaffians cannot close the route

The purely integral consequences are far too weak.  For every
\(0\le r\le4030\), there is an integral skew-symmetric matrix of rank
\(2r\), with zero diagonal, zero row sums, and all nonzero entries equal
to \(\pm1\).  Take \(r\) disjoint oriented triangles, each with block

\[
T=\begin{pmatrix}
0&1&-1\\
-1&0&1\\
1&-1&0
\end{pmatrix},
\tag{9}
\]

and append zero rows and columns.  Each \(T\) has row sum zero and rank
two.

This is deliberately an **abstract rank countermodel**, not a Steiner
fibre and not a realization of its actual intersection-layer support
graph.  It proves that a contradiction cannot follow merely from

* integral skew-symmetry;
* even rank and Pfaffian vanishing;
* zero row sums;
* the entry bound \(|\Delta_{BC}|\ge1\) on nonzero entries.

A successful rank attack must use a genuinely global coupling of the
rooted one-factorizations or the true Johnson-layer support graph, strong
enough to force a large nonsingular minor.  Proposition 1 narrows that
graph, but the abstract triangle model by itself does not prove that the
same ranks occur on the actual support mask.

## 4. The endpoint \(\Delta=0\) is not killed by algebraic integrality

If \(\Delta=0\), then \(R\) preserves \({\cal H}_3\).  The already forced
dimension and first two trace data admit the following integral spectrum:

\[
\boxed{
-61^{1914},\quad -60^{396},\quad -59^{720},\quad -58^{1000}.
}
\tag{10}
\]

Its multiplicities sum to \(4030\), its trace is \(-240994\), and under
\(Z=(R+63I)/15\) it has eigenvalues
\(2/15,1/5,4/15,1/3\), all in \([0,3/5]\), with the forced
\(\operatorname{tr}Z=12896/15\) and the zero-leakage endpoint
\(\operatorname{tr}Z^2=9548/45\).

Thus even forcing \(\Delta=0\) would not by itself create an
algebraic-integer or endpoint-positivity contradiction.  One would still
need a higher relation, a forbidden multiplicity, or a global
combinatorial obstruction.

## 5. Exact audit

Run

```sh
python3 -B \
  collaboration/h3_delta_rank_attack/verify_h3_delta_rank_attack.py
```

The checker verifies the two layer arguments in their finite state form,
representative direct sums of the rank-two triangle block together with
the additive rank formula for every admissible number of blocks, the
corrected \(A_{13}\) leakage algebra, and all arithmetic in the compatible
\(\Delta=0\) spectrum.
