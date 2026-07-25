# Reference-order no-go for the block-local sign rowspace route

## Scope

This note closes one proposed route from Lemma 6 of
`fixed_base_parity_judgment.md`.  It does **not** prove or disprove the
fixed-base parity conjecture and has no implication for Erdős--Rosenfeld
Problem #835.

The proposed route was:

1. replace the Grassmann product sign \(E(B)\) by a linear block weight
   \[
   E(B)=c_A(-1)^{h_A\cdot x_B};
   \tag{1}
   \]
2. prove that \(h_A\) belongs to the binary rowspace of the facet
   incidence matrix restricted to non-\(A\) blocks;
3. conclude that \(h_A\cdot x_B\), and hence \(E(B)\), is constant on all
   exact designs \(B\) disjoint from \(A\).

There are two separate problems.  First, the exterior product has
essential pairwise crossing signs, so even-degree commutativity does not
by itself produce (1).  Second, the strongest natural block-local
candidate has reference-order-dependent rowspace membership.  Exact
computation at \(r=3,5\) proves both points.

## 1. The natural local sign

Let \(A\) be an \(S(r-1,r,2r+1)\), and let \(\kappa\notin A\).  The sphere
encoding gives a unique pair
\[
 P_0\in A,\qquad p\notin P_0,\qquad
 \kappa=X\setminus(P_0\cup\{p\}).
 \tag{2}
\]
For \(w\in\kappa\), let
\[
 P_w=(\kappa\setminus\{w\})\cup\{x_w\}\in A.
 \tag{3}
\]
The points \(x_w\) are distinct and equal
\(X\setminus(\kappa\cup\{p\})\).  Indeed, equality \(x_w=x_{w'}\) would
make two \(A\)-blocks share an \((r-1)\)-set, while \(x_w=p\) would make
\(P_w\) disjoint from \(P_0\).

Thus there is a block-local bijection
\[
 \theta_\kappa:X\setminus\kappa\longrightarrow\kappa\cup\{p\},
 \qquad
 \theta_\kappa(p)=p,\quad \theta_\kappa(x_w)=w.
 \tag{4}
\]
After choosing one total order \(\prec\) on \(X\), define
\[
 h_{A,\prec}(\kappa)=
 \begin{cases}
 0,&\operatorname{sign}_\prec(\theta_\kappa)=+1,\\
 1,&\operatorname{sign}_\prec(\theta_\kappa)=-1.
 \end{cases}
 \tag{5}
\]
This is the most direct point-labelled block sign suggested by the two
lists in the monomial \(u_\kappa\).

Let \(W'_A\) be the facet-versus-block incidence matrix with all
\((r-1)\)-subsets as rows and only non-\(A\) \(r\)-sets as columns.
Every exact design \(B\) disjoint from \(A\) satisfies
\[
 W'_A x_B=\mathbf1.
 \tag{6}
\]
Therefore \(h_{A,\prec}\in\operatorname{rowspace}_2W'_A\) would make
\(h_{A,\prec}\cdot x_B\) constant on that exact-design slice.

## 2. Exact lexicographic results

The deterministic bases and lexicographic point order used by the
verifier give:

### \(r=3\)

\[
\operatorname{rank}_2W'_A=15,\qquad
\operatorname{wt}(h_{A,<})=18,\qquad
h_{A,<}\in\operatorname{rowspace}_2W'_A.
\tag{7}
\]
An exact rowspace certificate is the sum of the eight facet rows
\[
 01,\ 04,\ 12,\ 15,\ 25,\ 34,\ 35,\ 45.
\tag{8}
\]
Moreover \(h_{A,<}\cdot x_B=0\) for all eight Fano mates.

### \(r=5\)

\[
\operatorname{rank}_2W'_A=210,\qquad
\operatorname{wt}(h_{A,<})=198,\qquad
h_{A,<}\notin\operatorname{rowspace}_2W'_A.
\tag{9}
\]
The six blocks
\[
\begin{split}
01245,\ 01248,\ 01258,\ 01458,\ 02458,\ 12458
\end{split}
\tag{10}
\]
are all the \(5\)-subsets of \(Y=\{0,1,2,4,5,8\}\).  Their indicator
\(z_Y\) is supported only on non-\(A\) blocks and satisfies
\[
 W'_A z_Y=0,\qquad h_{A,<}\cdot z_Y=1.
\tag{11}
\]
The first identity is transparent: every \(4\)-subset of \(Y\) occurs
in exactly two of its six \(5\)-facets.  Equation (11) is an explicit
certificate for the nonmembership in (9).

Nevertheless,
\[
 h_{A,<}\cdot x_B=0
\tag{12}
\]
for every one of the 144 exhaustively enumerated Witt mates.  The mate
difference span has dimension \(44\), so its orthogonal space has
dimension \(396-44=352\), much larger than the \(210\)-dimensional facet
rowspace.  Thus (12) is a relation valid on the enumerated nonlinear
exact-design slice, not a consequence of the facet equations.

## 3. The decisive reference-order counterexample

Membership (7) is not invariant.  Keep the same labelled Fano base but
change the point order from
\[
 0<1<2<3<4<5<6
\quad\text{to}\quad
 1\prec0\prec2\prec3\prec4\prec5\prec6.
\tag{13}
\]
Then
\[
 h_{A,\prec}\notin\operatorname{rowspace}_2W'_A.
\tag{14}
\]
An exact witness is the boundary of
\(Y=\{0,2,3,5\}\):
\[
 z_Y=023+025+035+235,\qquad
 W'_Az_Y=0,\qquad h_{A,\prec}\cdot z_Y=1.
\tag{15}
\]
Yet \(h_{A,\prec}\cdot x_B=0\) for all eight exact mates, just as before.

Exhausting all \(7!=5040\) point orders gives rowspace membership for
only \(336\) orders.  Hence the apparent split
\[
 \text{“yes at \(r=3\), no at \(r=5\)”}
\]
under lexicographic conventions is not an \(r\bmod4\) phenomenon.  It is
already destroyed at fixed \(r=3\) by a harmless reference-order change.

This matters because changing the reference order in the definition of
each \(\operatorname{sign}(\pi_P^B)\) multiplies \(E(B)\) by a factor
depending on the fixed sphere \(P\), but not on \(B\).  Thus constancy of
\(E\) is reference-order invariant, whereas membership of (5) is not.

## 4. Why Lemma 6 does not supply a linear \(h_A\)

Fix global orders of the sphere-content coordinates \(e_{(P,y)}\) and
the sphere-slot coordinates \(f_{(P,s)}\).  Inside each \(u_\kappa\),
order its \(r+1\) incidences in the same way in the \(e\)-list and
\(f\)-list.  Since a non-\(A\) block uses every sphere at most once, the
two lists have the same sequence of primary sphere labels.  Their
internal inversion parities cancel.  In the deterministic \(r=3,5\)
instances the resulting local orientation vector is identically zero,
as the symbolic argument predicts.

The top-degree coefficient instead contains cross terms.  For two
compatible non-\(A\) blocks define
\[
 q_A(\kappa,\lambda)=
 \operatorname{inv}(I_\kappa^e,I_\lambda^e)+
 \operatorname{inv}(I_\kappa^f,I_\lambda^f)\pmod2,
\tag{16}
\]
where a cross inversion compares one coordinate from each displayed
list.  Because \(r+1\) is even, (16) is independent of which block is
listed first.  Direct sorting of the exterior product gives
\[
 E(B)=(-1)^{
 \sum_{\{\kappa,\lambda\}\subset B}q_A(\kappa,\lambda)}
\tag{17}
\]
under the verifier's fixed volume convention.  The quadratic form is
not zero: for example, \(q_A=1\) on
\[
\{013,025\}\quad(r=3),\qquad
\{01235,01247\}\quad(r=5).
\tag{18}
\]

Thus even-degree commutativity removes dependence on the order of the
whole \(u_\kappa\)'s; it does not remove the pairwise coordinate-sorting
signs.  Replacing (17) by (1) on every exact design would require an
additional affine-linearization theorem for this quadratic form.  No
such theorem follows from Lemma 6.  At \(r=15\), its constancy on the
mate slice is precisely the still-open \(E\)-constancy problem.

The separate proposed identity
\[
 E(B)E(C)=(-1)^{b-|B\cap C|}
\tag{19}
\]
is likewise not supplied by this calculation.  As recorded in
`fixed_base_parity_judgment.md`, (19) is the open cycle-parity assertion
Q1.  The present rowspace no-go neither proves nor refutes it.

## 5. Reproducibility

Run:

```text
python3 -B evidence/verify_block_local_sign_rowspace_no_go.py
```

The script uses exact binary arithmetic and exhaustive exact cover.
