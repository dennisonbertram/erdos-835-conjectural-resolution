# The 13-primary signed-consistency screen for the cyclic fan quotient

## Result

Fix the committed cyclic \(LS(2,3,19)\) used in
`../h3_simultaneous_fan_attack_2/verify_fan_kernel_reduction.py`.  Its
\(C_{17}\)-quotient fan hypergraph has

\[
  2964\text{ cells},\qquad 1140\text{ groups},\qquad
  |G|=13,\qquad \deg(\text{cell})=5.
\]

Let \(B_0\) be the \(1140\times2964\) group-versus-cell incidence matrix.
The exact result of this screen is

\[
  \boxed{B_0x=\mathbf 1\text{ has a signed integral solution over }\mathbb Z.}
\]

Consequently it is solvable over \(\mathbb Z_{13}\) and modulo \(13^e\) for
every \(e\geq1\), in particular modulo \(13^2=169\).  Thus this fixed cyclic
link has **no signed integral linear obstruction** to a fan.

This is not a fan.  The integral solution may have arbitrary signed
coordinates, not coordinates in \(\{0,1\}\), and it does not resolve the
nonlinear simultaneous-rainbow condition.

## 1. Reconstruction of \(B_0\)

The verifier independently reconstructs the cyclic large set from the two
starters and forty phases, checks all \(\binom{19}{2}\) pair stars, then forms
the diagonal translation action

\[
  (Q,c)\longmapsto(Q+t,c+t),\qquad t\in\mathbb Z_{17}.
\]

There are 2,964 allowed cell orbits.  The quotient groups are:

- 228 quadruple orbits \(Q\);
- 912 allowed triple-colour orbits \((T,c)\), namely 57 point-translation
  orbits of triples and 16 non-link colour offsets per orbit.

Every quotient group contains thirteen distinct cell orbits and every cell
belongs to one \(Q\)-group and four \((T,c)\)-groups.

## 2. The 57 exact integral row dependencies

Let \(\mathcal R\) be one of the 57 point-translation orbits of triples.
For a quadruple orbit \(Q\), let \(m_{\mathcal R}(Q)\) be the number of its
four faces whose point orbit is \(\mathcal R\).  There is an exact integral
row relation

\[
 \sum_{\substack{(T,c)\\[T]=\mathcal R}}\! B_{0,(T,c)}
 -
 \sum_Q m_{\mathcal R}(Q)B_{0,Q}=0. \tag{1}
\]

Indeed, a cell \((Q,c)\) occurs once in the first sum for every face of \(Q\)
belonging to \(\mathcal R\), and exactly the same number of times in the
second sum.

There are sixteen \((T,c)\)-row orbits above each \(\mathcal R\), and

\[
 \sum_Qm_{\mathcal R}(Q)=16.
\]

Therefore the coefficients in (1) also sum to zero.  Each relation
annihilates the right-hand side \(\mathbf1\).

The 57 relations are independent: each has coefficient \(+1\) on its own
disjoint set of sixteen triple-colour rows.  Hence

\[
 \operatorname{rank}_{\mathbb Q}B_0\leq1140-57=1083. \tag{2}
\]

The verifier checks all 57 relations entry-by-entry over the integers,
checks their right-hand-side sums, and hashes their canonical sparse
encoding.

## 3. Exact 13-primary Smith conclusion

Sparse Gaussian elimination over \(\mathbb F_{13}\) gives

\[
  \operatorname{rank}_{\mathbb F_{13}}B_0=1083. \tag{3}
\]

Since reduction modulo a prime cannot increase rational rank, (2) and (3)
give

\[
 \operatorname{rank}_{\mathbb Q}B_0
 =\operatorname{rank}_{\mathbb F_{13}}B_0=1083. \tag{4}
\]

Let \(d_1,\ldots,d_{1083}\) be the nonzero Smith invariant factors of
\(B_0\).  The rank modulo 13 is the number of these factors not divisible by
13.  Equality (4) therefore proves

\[
 13\nmid d_i\qquad(1\leq i\leq1083). \tag{5}
\]

The relations in Section 2 form a full basis of the rational left kernel,
and each annihilates \(\mathbf1\).  Thus \(\mathbf1\) lies in the rational
column space, so its class \([\mathbf1]\) in
\(\operatorname{coker}(B_0)=\mathbb Z^{1140}/B_0\mathbb Z^{2964}\) is
torsion.

Every row of \(B_0\) has thirteen entries equal to one.  Therefore

\[
 B_0\mathbf1_{2964}=13\mathbf1_{1140},
\]

and hence \(13[\mathbf1]=0\) in the cokernel.  On the other hand, (5) says
that the torsion subgroup of the cokernel has no element of order 13: its
invariant factors are precisely the nonzero \(d_i\), none divisible by 13.
It follows that \([\mathbf1]=0\), which is exactly the existence of
\(x\in\mathbb Z^{2964}\) satisfying \(B_0x=\mathbf1\).  This proves the
boxed integral result.

For an additional concrete audit, the verifier constructs compatible
solutions modulo \(13,13^2,\ldots,13^6\).  At each stage it solves the exact
base-field residual equation

\[
 B_0\delta_e =
 \frac{\mathbf1-B_0x_e}{13^e}\pmod {13},
 \qquad
 x_{e+1}=x_e+13^e\delta_e,
\]

then checks all 1,140 equations directly at the new modulus.

## 4. Why the quotient is relevant

For signed consistency modulo \(13^e\), the \(C_{17}\) quotient loses
nothing.  If the full fixed-link system has a solution \(x\), then

\[
 \bar x=17^{-1}\sum_{g\in C_{17}}g x
\]

is a \(C_{17}\)-invariant solution because \(17\) is invertible modulo
\(13^e\).  Conversely, a quotient solution lifts to an invariant full
solution.  The same averaging argument works over \(\mathbb Z_{13}\).

This equivalence is only about signed modular or 13-adic consistency.
Averaging does not preserve \(\{0,1\}\)-coordinates, and division by 17 is
not an integer operation over \(\mathbb Z\).  Thus an arbitrary full-system
integer solution would not necessarily descend integrally.  In the direction
needed here, however, the quotient integer solution lifts directly by making
the value constant on every cell orbit.  Hence the full fixed-link incidence
system also has a signed integral solution.

## 5. Reproduction

Run:

```bash
/opt/homebrew/bin/python3 collaboration/fan_13adic_screen/verify_fan_13adic_screen.py
```

The verifier uses only the Python standard library.  It reconstructs all
objects rather than reading a precomputed matrix.  `RUN_LOG.txt` records the
canonical output and the SHA-256 digests of the row-dependency certificate
and the six explicit modular solution vectors.

## Scope

Proved:

- exact signed integral solvability of \(B_0x=\mathbf1\);
- a signed integral solution of the full fixed-link incidence system, obtained
  by lifting the quotient solution;
- exact solvability of \(B_0x=\mathbf1\) modulo every power of 13;
- equivalently, solvability over \(\mathbb Z_{13}\);
- all 1,083 nonzero Smith factors are 13-adic units.

Not proved:

- a \(0/1\) exact cover;
- a simultaneous 13-fan;
- a non-\(C_{17}\)-invariant fan;
- any unrestricted construction or theorem resolving Problem #835.
