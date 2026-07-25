# Simultaneous transposition flows are exactly integrable

## Outcome

This note proves an exact equivalence, not a solution of Erdős--Rosenfeld
Problem #835.

For one deleted point-pair, the transposition flow of
`transposition_flow_cocycle.md` is a genuine relaxation.  For the
**simultaneous family over all point-pairs**, however, reversal, the
same-star triangle identities, and the pairwise kernel equations already
force a single global potential on the middle layer.  Adding full support
then recovers precisely a tight colouring.  The row-derangement,
Frobenius, anti-complement, rank-two, and Plücker conditions are automatic.

Consequently this result advances the structural understanding of the
flow formulation, but it does not decide whether the required
full-support global potential exists at \(k=16\).

## 1. The exact integrability theorem

Let \(X\) have \(2k\) points, put \(r=k-1\), and let \(F\) be a field.
Suppose that, for every \(B\in\binom Xr\) and every ordered pair of
distinct \(x,y\in X\setminus B\), a value
\[
 a_{xy}(B)\in F
 \tag{1.1}
\]
is given.  Assume:

\[
\begin{aligned}
 a_{yx}(B)&=-a_{xy}(B), &&\text{(reversal)} \tag{R}\\
 a_{xy}(B)+a_{yz}(B)+a_{zx}(B)&=0,
 &&\text{(same-star triangle)} \tag{T}\\
 \sum_{w\in X\setminus(C\cup\{x,y\})}
 a_{xy}(C\cup\{w\})&=0.
 &&\text{(pair kernel)} \tag{K}
\end{aligned}
\]
Here (T) holds for distinct \(x,y,z\notin B\), while (K) holds for
\(C\in\binom X{r-1}\) and distinct \(x,y\notin C\).

**Simultaneous-flow integrability theorem.**  Conditions (R), (T), and
(K) imply that there is a function
\[
 g:\binom X{r+1}\longrightarrow F
 \tag{1.2}
\]
such that
\[
 \boxed{a_{xy}(B)=g(B\cup\{x\})-g(B\cup\{y\}).}
 \tag{1.3}
\]
The function \(g\) is unique up to addition of one global constant.
Moreover, if \(M=W_{r,r+1}(2k)\), then
\[
 Mg=\lambda\mathbf1
 \tag{1.4}
\]
for some \(\lambda\in F\).

Conversely, every \(g\) satisfying (1.4) gives through (1.3) a family
satisfying (R), (T), and (K).

### Step 1: the kernel forces every cross-star hexagon

Fix \(C\in\binom X{r-1}\) and distinct \(x,y,z\notin C\).  Add the
three instances
\[
 K(C;y,z)+K(C;z,x)+K(C;x,y).
\]
For each
\(w\in X\setminus(C\cup\{x,y,z\})\), the three terms with base
\(C\cup\{w\}\) cancel by (T).  Exactly three terms remain:
\[
 \boxed{
 a_{yz}(C\cup\{x\})+
 a_{zx}(C\cup\{y\})+
 a_{xy}(C\cup\{z\})=0.}
 \tag{1.5}
\]
Thus the missing cross-star holonomy is not an additional axiom: it is
an exact linear consequence of the three pair-kernel rows and the
same-star triangles.

### Step 2: local potentials

For each \(B\), choose \(o_B\in X\setminus B\), put
\[
 h_B(o_B)=0,\qquad h_B(u)=a_{u,o_B}(B).
 \tag{1.6}
\]
Equations (R) and (T) give
\[
 a_{uv}(B)=h_B(u)-h_B(v).
 \tag{1.7}
\]

### Step 3: the Johnson-graph holonomy vanishes

Use the \(r\)-subsets as the vertices of \(J(2k,r)\).  If \(B,B'\)
are adjacent, put \(A=B\cup B'\), \(u=A\setminus B\), and
\(v=A\setminus B'\).  On the oriented edge \(B\to B'\), define
\[
 q(B,B')=h_B(u)-h_{B'}(v).
 \tag{1.8}
\]

Every triangle in a Johnson graph is of one of two types.

- In an **upper triangle**, the three vertices are facets of one
  \((r+1)\)-set \(A\).  The three terms in (1.8) telescope.
- In a **lower triangle**, the vertices are
  \(C+x,C+y,C+z\).  Its \(q\)-sum is exactly the left side of (1.5).

Hence \(q\) sums to zero on every Johnson triangle.

For completeness, the cycle space of \(J(n,r)\) is generated over
every field by its triangles.  A standard exchange-word reduction first
expresses every closed walk as a sum of triangles and elementary
squares.  An elementary square has the form
\[
\begin{split}
 S+a+c&\longrightarrow S+b+c\longrightarrow S+b+d\\
      &\longrightarrow S+a+d\longrightarrow S+a+c.
\end{split}
\tag{1.9}
\]
The vertex \(S+a+b\) is adjacent to all four displayed vertices, so
the square boundary is the sum of the four resulting triangle
boundaries.  This also proves the assertion over the integers, hence
over every field.

It follows that \(q\) has zero sum around every cycle.  Since the
Johnson graph is connected, there are scalars \(t_B\) such that
\[
 q(B,B')=t_{B'}-t_B.
 \tag{1.10}
\]

### Step 4: reconstruction

For \(A\in\binom X{r+1}\), choose any facet \(B\subset A\) and set
\[
 g(A)=h_B(A\setminus B)+t_B.
 \tag{1.11}
\]
If \(B,B'\subset A\) are two facets, (1.8) and (1.10) say precisely
that the two values in (1.11) agree.  Thus \(g\) is well-defined, and
(1.7) proves (1.3).

If \(g'\) has the same flows, \(g'-g\) is constant on every lower
star.  The middle-layer Johnson graph is connected, so this difference
is one global constant.  This proves uniqueness.

Finally, write
\[
 S(B)=\sum_{u\in X\setminus B}g(B\cup\{u\})=(Mg)(B).
\]
For \(B=C+x\) and \(B'=C+y\), (K), after substituting (1.3), is
\[
 S(C+x)-g(C+x+y)-S(C+y)+g(C+x+y)=0.
\]
Thus \(S(B)=S(B')\) on every edge of \(J(2k,r)\), so it has a common
value \(\lambda\), proving (1.4).  The calculation reverses, proving
the converse. \(\square\)

## 2. Exact equivalence at \(k=16\)

Now take \(k=16\), \(F=\mathbb F_{17}\), and impose full support:
\[
 a_{xy}(B)\ne0
 \quad(x\ne y,\ x,y\notin B).
 \tag{2.1}
\]
By (1.3), the seventeen values
\[
 \{g(B+x):x\in X\setminus B\}
\]
are pairwise distinct.  They therefore equal all of
\(\mathbb F_{17}\), whose sum is zero.  Hence \(\lambda=0\) in
(1.4), and \(g\) is exactly a tight \(17\)-colouring of \(J(32,16)\).
The converse is the transposition-flow construction.

Therefore:
\[
\boxed{
\begin{array}{c}
\text{full-support simultaneous family satisfying (R), (T), (K)}
\\[2mm]\Longleftrightarrow\\[2mm]
\text{tight \(17\)-colouring of \(J(32,16)\).}
\end{array}}
\tag{2.2}
\]

This equivalence uses only the kernel and cocycle conditions.  Once
(2.2) holds, the row derangements, \(a^{16}=1\), \(a^{17}=a\), and
anti-complementarity follow from the reconstructed colouring.  They do
not further narrow the simultaneous family.

The global linear space before full support also has a concise
description:
\[
 \frac{M^{-1}\langle\mathbf1\rangle}{\langle\mathbf1\rangle}.
 \tag{2.3}
\]
Wilson's factors for \(M=W_{15,16}(32)\) are
\[
 16,15,\ldots,1,
\]
all nonzero modulo \(17\), so \(M\) has full row rank.  Consequently
the space in (2.3) has dimension
\[
 \binom{32}{16}-\binom{32}{15}
 =601\,080\,390-565\,722\,720
 =35\,357\,670.
 \tag{2.4}
\]
Full support forces the codimension-one sector \(Mg=0\), modulo the
constant vector (which also lies in \(\ker M\) in characteristic
\(17\)).

## 3. Rank, Plücker, and topology: exact boundary

For a fixed \(B\), let \(A_B=(a_{xy}(B))\) on \(X\setminus B\).
Equation (1.7) gives
\[
 A_B=h_B\mathbf1^{\mathsf T}-\mathbf1h_B^{\mathsf T}.
 \tag{3.1}
\]
Thus \(\operatorname{rank}A_B\le2\), with equality under full support,
and every four distinct outside points satisfy
\[
 a_{xy}a_{zw}-a_{xz}a_{yw}+a_{xw}a_{yz}=0.
 \tag{3.2}
\]
These Plücker equations are just another form of the same-star gradient
condition; they are not a new obstruction.

Topologically, (1.8) is the only possible gluing class in
\(H^1(J(32,15);\mathbb F_{17})\).  The kernel equations force its
value on every lower triangle to vanish, upper triangles telescope,
and triangle boundaries span the cycle space.  Hence this class is
always zero.  There is no surviving first-cohomology obstruction after
(R), (T), and (K).

The unresolved difficulty is therefore exactly the original nonlinear
one: does the sector \(Mg=0\) contain a vector whose difference on
every adjacent pair of \(16\)-sets is nonzero?

## 4. Exact \(k=4\) and \(k=6\) controls

The theorem explains the small negative cases without creating false
countermodels.

- At \(k=4\), the single full-support flow in
  `transposition_flow_cocycle.md` cannot extend to a simultaneous family
  satisfying (R), (T), and (K).  Such an extension would reconstruct a
  forbidden tight \(5\)-colouring of \(J(8,4)\).
- At \(k=6\), even a single Witt \(S(5,6,12)\) exists, but a
  full-support simultaneous family would reconstruct seven disjoint
  colour classes.  The exhaustive Witt control shows that at most two
  can be mutually disjoint.

The verifier performs three independent exact checks:

1. formal coefficient cancellation proving (1.5) for \(k=4,6,16\);
2. modular cycle ranks for \(J(8,3)\) over \(\mathbb F_5\) and
   \(J(12,5)\) over \(\mathbb F_7\);
3. the existing exhaustive Fano/Witt exact-cover controls.

For the cycle-rank check:
\[
\begin{array}{c|r|r|r|r|r}
k&|V|&|E|&|E|-|V|+1&
\operatorname{rank}(\text{lower triangles})&
\operatorname{rank}(\text{all triangles})\\ \hline
4&56&420&365&280&365\\
6&792&13\,860&13\,069&10\,395&13\,069
\end{array}
\tag{4.1}
\]
Thus the triangle span is the complete cycle space in both adversarial
controls.

Run:

```text
python3 -B evidence/verify_simultaneous_flow_integrability.py
```

