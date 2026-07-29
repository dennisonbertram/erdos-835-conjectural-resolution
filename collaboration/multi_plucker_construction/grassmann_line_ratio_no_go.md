# A no-go theorem for ratios along a Grassmann line

Status: **this excludes one genuinely two-coordinate Plücker family.  It
does not exclude two unrelated minors, a three-coordinate tuple, or an
arbitrary colouring, and it does not solve Erdős--Rosenfeld Problem
#835.**

Let \(p\geq5\) be an odd prime, put \(k=p-1\), and let
\(V=\mathbb F_p^{\,2k}\) with its ordered coordinate basis.  Fix
linearly independent \(k\)-forms
\[
 \omega_0=\theta\wedge x,\qquad
 \omega_1=\theta\wedge y,                              \tag{1}
\]
where \(\theta\) is a decomposable \((k-1)\)-form.  Thus the whole pencil
\[
 a\omega_0+b\omega_1=\theta\wedge(ax+by)              \tag{2}
\]
is decomposable.  In matrix language, \(\omega_0\) and \(\omega_1\) are
the maximal-minor systems of two \(k\)-by-\(2k\) matrices sharing
\(k-1\) rows.  Equivalently, their projective span is a line contained
in the Plücker Grassmannian.

For a \(k\)-set \(S=\{s_1<\cdots<s_k\}\), write
\[
 P(S)=\omega_0(e_{s_1},\ldots,e_{s_k}),\qquad
 Q(S)=\omega_1(e_{s_1},\ldots,e_{s_k}).                \tag{3}
\]
Assume \((P(S),Q(S))\ne(0,0)\) for every \(S\), so that the projective
ratio
\[
 \rho(S)=[P(S):Q(S)]\in\mathbb P^1(\mathbb F_p)       \tag{4}
\]
is defined.

## The theorem

There is no map
\[
 h:\mathbb P^1(\mathbb F_p)\longrightarrow\mathbb F_p
\]
for which
\[
 c(S)=h(\rho(S))                                      \tag{5}
\]
is a proper \(p\)-colouring of \(J(2k,k)\).

The decoder \(h\) is completely arbitrary.  In particular, the theorem
allows an arbitrary projective change of the two retained coordinates
and an arbitrary lookup table after taking their ratio.

For \(p=17\), this rules out the corresponding shared-\(15\)-row,
two-minor construction for a \(17\)-colouring of \(J(32,16)\).

## 1. Star rigidity

For \(\lambda=[a:b]\in\mathbb P^1(\mathbb F_p)\), put
\[
 \omega_\lambda=a\omega_0+b\omega_1.
\]
The zero class of \(\omega_\lambda\) is one projective ratio class in
(4), with the harmless dual identification
\([P:Q]=[-b:a]\).

If (5) were proper, every \((k-1)\)-star would contain \(p\) distinct
ratio values and all \(p\) decoded colours.  We first use this local
injectivity to show that all \(p+1\) ratio values occur already in one
rank-two link.  Only then will we use the fibre sizes of \(h\).

## 2. The exact rank-two link

Fix any coordinate \((k-2)\)-set \(R\).  There remain
\[
 2k-(k-2)=p+1
\]
coordinates; call their index set \(X\).  Contract (2) by the ordered
basis vectors indexed by \(R\):
\[
 \eta_\lambda=\iota_R\omega_\lambda\in
 \bigwedge\nolimits^2(\mathbb F_p^X)^\ast.            \tag{6}
\]
Contracting a decomposable form by a decomposable multivector leaves a
decomposable form (or zero), so every \(\eta_\lambda\) has alternating
rank at most two.

The two endpoint forms in (6) are linearly independent.  If they were
proportional, then either an edge would have feature \((0,0)\), or all
edges of the complete graph on \(X\) would have the same ratio; both
possibilities contradict properness on a star.  Thus (6) is a genuine
projective line of nonzero decomposable two-forms.

For \(i,j\in X\), the edge \(ij\) represents the \(k\)-set
\(R\cup\{i,j\}\).  At vertex \(i\), its \(p\) incident edge ratios are
the ratios on the star \(R\cup\{i\}\), so they are pairwise distinct.

## 3. A decomposable pencil is a projective-plane chord pencil

Write two independent members of (6) as
\[
 A=a\wedge b,\qquad B=c\wedge d.
\]
Because \(A+B\) is decomposable and \(p\) is odd,
\[
 0=(A+B)\wedge(A+B)=2A\wedge B.
\]
Hence \(a,b,c,d\) span a three-dimensional space \(W\).  (They cannot
span only two dimensions because \(A,B\) are independent.)

Choose a basis \(f_1,f_2,f_3\) of \(W\).  Each coordinate \(i\in X\)
gives a projective point
\[
 Z_i=[f_1(e_i):f_2(e_i):f_3(e_i)]
       \in\operatorname{PG}(2,p).                     \tag{8}
\]
None is zero, and no two \(Z_i\)'s coincide: either event would make the
feature pair zero on an edge.  The standard identification
\(\bigwedge^2 W\cong W^\ast\) assigns to every \(\eta_\lambda\) a point
\(N_\lambda\) such that, up to one fixed nonzero choice of volume form,
\[
 \eta_\lambda(i,j)=
 \det(Z_i,Z_j,N_\lambda).                             \tag{9}
\]
As \(\lambda\) ranges over \(\mathbb P^1(\mathbb F_p)\), the
\(N_\lambda\)'s range bijectively over the points of one projective line
\(L\).

The \(p+1\) points
\[
 {\cal O}=\{Z_i:i\in X\}
\]
form an oval.  Indeed, if three of them were collinear on a line
\(M\ne L\), then \(M\cap L=N_\lambda\) for some \(\lambda\), and two
edges incident with the same vertex would have the same ratio by (9).
If two of them lay on \(L\), their feature pair would vanish identically.
Both alternatives are forbidden.

No centre \(N_\lambda\) lies on \(\mathcal O\), because then all \(p\)
edges incident with that oval point would have the same zero parameter.
Moreover, every \(N_\lambda\) lies on at least one chord of
\(\mathcal O\).  Otherwise
\(\mathcal O\cup\{N_\lambda\}\) would be a \((p+2)\)-arc, impossible in
a projective plane of odd order by the elementary odd-order arc bound.
Indeed, at any point of a hypothetical \((p+2)\)-arc, its \(p+1\)
joining lines to the other \(p+1\) arc points exhaust all lines through
that point.  Hence the arc has no tangent.  The lines through any point
outside the arc would therefore partition its \(p+2\) points into pairs,
which is impossible because \(p+2\) is odd.
It follows from (9) that all \(p+1\) projective ratio values already
occur in this one link.

The decoder \(h\) is consequently a surjection from a \((p+1)\)-set to
a \(p\)-set.  It has exactly one double fibre
\(\{\alpha,\beta\}\), while its other \(p-1\) fibres are singletons.
Every vertex-star contains all \(p-1\) singleton labels and exactly one
of \(\alpha,\beta\).  Therefore each singleton label forms a perfect
matching of \(K_{p+1}\).  Under the dual zero-class identification,
there are \(p-1\) parameters \(\lambda\) for which
\[
 \eta_\lambda(i,j)=0                                  \tag{7}
\]
is a perfect matching.

For every one of the \(p-1\) parameters in (7), every point of
\mathcal O\) is paired with one other point on a secant through
\(N_\lambda\).  Thus no tangent to \(\mathcal O\) passes through
\(N_\lambda\): each such \(N_\lambda\) is an internal point of the oval.
The one line \(L\) would therefore have to contain at least
\[
 p-1                                                     \tag{10}
\]
internal points.

## 4. A line cannot contain that many internal points

Segre's theorem says that every oval in
\(\operatorname{PG}(2,p)\), for \(p\) odd, is a nonsingular conic.
Move it projectively to
\[
 {\cal C}:Y^2-XZ=0.                                  \tag{11}
\]
The tangents through a point \(N=[X:Y:Z]\notin{\cal C}\) are governed by
the quadratic discriminant
\[
 D(N)=Y^2-XZ.
\]
The point is internal exactly when \(D(N)\) is a nonsquare.

Restricting \(D\) to a projective line gives a binary quadratic form.
On a tangent, secant, or external line, respectively, the number of
internal points is
\[
 0,\qquad {p-1\over2},\qquad {p+1\over2}.             \tag{12}
\]
This is the elementary quadratic-character census for a binary
quadratic with one, two, or no projective zeros.  In particular, every
line contains at most \((p+1)/2\) internal points.

For \(p>3\),
\[
 p-1>{p+1\over2},
\]
contradicting (10).  This proves the theorem.

## 5. Finite audit and boundary control

The dependency-free verifier
`verify_grassmann_line_ratio_no_go.py` checks:

* all \(307\) points and \(307\) lines of
  \(\operatorname{PG}(2,17)\);
* the exact conic/tangent/internal classification;
* the line census
  \[
  \max_L|L\cap\mathrm{Int}({\cal C})|=9;
  \]
* the required contradiction \(16>9\);
* the determinant identity (9) for a concrete decomposable pencil; and
* the sharp \(p=3\) boundary, where \(p-1=(p+1)/2=2\), so this argument
  correctly gives no contradiction for the known \(k=2\) case.  The
  verifier actually constructs the local \(K_4\) chord pencil: its two
  internal centre labels are retained and its two external centre
  labels fuse to the third colour.

Run:

```bash
python3 -B \
  collaboration/multi_plucker_construction/verify_grassmann_line_ratio_no_go.py
```

Segre's theorem is the only non-enumerated finite-geometry input.  A
modern self-contained exposition is Brian Kronenthal,
[*Arcs, Ovals, and Segre's
Theorem*](https://faculty.kutztown.edu/kronenthal/Research/ArcsOvalsSegre.pdf),
Theorem 2.4.  The original result is B. Segre,
[*Ovals in a finite projective
plane*](https://doi.org/10.4153/CJM-1955-045-x), *Canadian Journal of
Mathematics* **7** (1955), 414--416.

## Exact scope

This closes the projectively invariant two-minor ratio ansatz when the
two Plücker vectors span a line **inside** the Grassmannian, equivalently
when the two matrices can be represented with \(k-1\) common rows.  It
also explains the obstruction geometrically: the decoder would demand
sixteen internal conic points on one line in the \(p=17\) link, while a
line contains at most nine.

In fact the proof is local and slightly broader: it excludes any
two-coordinate projective statistic for which, at even one
\((k-2)\)-face \(R\), the two contracted forms are independent and
their entire pencil has alternating rank at most two.  The common-row
Grassmann-line family satisfies this at every \(R\).

It does **not** cover:

* two unrelated decomposable \(k\)-forms, whose generic pencil leaves
  the Grassmannian and whose contracted links may have rank four;
* a decoder of the affine pair \((P,Q)\) that retains common-scale
  information instead of only \([P:Q]\);
* three or more Plücker coordinates;
* a general \(LS(15,16,32)\) or a general colouring of \(J(32,16)\).

Thus this is a strict next-family exclusion after the single-minor
closure, not a resolution of Problem #835.
