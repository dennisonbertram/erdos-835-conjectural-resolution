# Structural audit of an unrestricted rank-four ordered link over
# \(\mathbb F_{19}\)

## Scope

This note records unconditional consequences of a hypothetical unrestricted
rank-four ordered link over \(\mathbb F_{19}\).  It repairs two small defects
in the exploratory Opus 5 derivation from which the argument started:

1. a split rank-two quadric in \(\operatorname{PG}(3,19)\) has \(742\)
   points, not \(741\);
2. vanishing of the two-dimensional residual Gram matrix puts the residual
   vectors on one isotropic line; it does not force them all to be zero.

The corrected residual argument still proves that the residual has rank two.
Nothing here decides whether an unrestricted rank-four link exists.  In
particular this is not a principal-Pfaffian construction and is not a
solution of Erdős--Rosenfeld Problem #835.

## 1. Ordered-link convention and exact row structure

Let \(B\) be a \(20\times20\) alternating matrix over
\(\mathbb F_{19}\), with rows and columns indexed by
\(0,1,\ldots,19\).  Put
\[
 \epsilon_{ij}=\begin{cases}1&i<j,\\-1&i>j,\end{cases}
 \qquad
 \sigma_i(j)=\epsilon_{ij}B_{ij}.
\]
The ordered-link condition is that, for every \(i\), the map
\(\sigma_i:\{j:j\ne i\}\to\mathbb F_{19}\) is a bijection.

### Lemma 1.1

For every row \(i\):

1. exactly one off-diagonal entry is zero and, for each nonzero sign class
   \(\{a,-a\}\), exactly two entries belong to that class;
2. if \(j<k\) realize one sign class, then
   \[
   B_{ij}=B_{ik}\iff j<i<k,
   \]
   while
   \[
   B_{ij}=-B_{ik}\iff j,k\text{ lie on the same side of }i.
   \]

**Proof.**  Bijectivity makes the two signed values in a fixed sign class
equal to \(a\) and \(-a\).  If the two unsigned entries agree, their signed
values are opposite exactly when \(\epsilon_{ij}\ne\epsilon_{ik}\), which
means that \(j,k\) straddle \(i\).  If the unsigned entries are opposite,
the signed values are opposite exactly when the two \(\epsilon\)'s agree.
The converse reconstructs all nineteen distinct signed values. \(\square\)

### Corollary 1.2

The off-diagonal zero entries form a perfect matching on the twenty
indices.  Moreover
\[
 j\longmapsto B_{0j}\quad(1\le j\le19)
\]
and
\[
 j\longmapsto-B_{19,j}\quad(0\le j<19)
\]
are bijections onto \(\mathbb F_{19}\).

The zero relation is symmetric and every vertex has degree one, proving the
matching assertion.  At either endpoint every other index lies on one side,
so Lemma 1.1 gives the displayed panoramic rows.

## 2. The signed moment identities

For \(1\le k\le18\),
\[
 \sum_{c\in\mathbb F_{19}}c^k
 =\begin{cases}0&1\le k<18,\\-1&k=18.\end{cases}
\]
Applying this to each signed row gives:

### Theorem 2.1

For every \(i\):

- if \(k\in\{2,4,\ldots,16\}\), then
  \[
  \sum_jB_{ij}^k=0,
  \qquad
  \sum_jB_{ij}^{18}=-1;
  \]
- if \(k\in\{1,3,\ldots,17\}\), then
  \[
  \sum_{j>i}B_{ij}^k=\sum_{j<i}B_{ij}^k. \tag{2.1}
  \]

The odd *unsigned* row moments do not generally vanish.  Summing (2.1) for
\(k=1\) over all \(i\) does give the global identity
\[
\sum_{i<j}B_{ij}=0. \tag{2.2}
\]

## 3. The rank-four symplectic model and its zig-zag

Assume \(\operatorname{rank}B=4\).  There is a four-dimensional symplectic
space \(V\) and spanning vectors \(u_0,\ldots,u_{19}\) such that
\[
B_{ij}=\langle u_i,u_j\rangle.
\]
Put
\[
w=\sum_{j=0}^{19}u_j,\qquad
W_i=\sum_{j=i}^{19}u_j,\qquad
Y_i=2W_i-w
\]
and set \(W_{20}=0\).

### Theorem 3.1

The degree-one identities (2.1) are equivalent to
\[
Y_0=w,\quad Y_{20}=-Y_0,\quad
Y_i-Y_{i+1}=2u_i,\quad
\langle Y_i,Y_{i+1}\rangle=0
\quad(0\le i<20). \tag{3.1}
\]

**Proof.**  The difference between the two sides of (2.1) at \(k=1\) is
\[
\langle u_i,W_{i+1}\rangle
-\langle u_i,w-W_i\rangle
=\langle u_i,2W_{i+1}-w\rangle
=\langle u_i,Y_{i+1}\rangle.
\]
Since \(Y_i=Y_{i+1}+2u_i\), this vanishes exactly when consecutive \(Y\)'s
are orthogonal.  The remaining identities follow directly from the
definitions. \(\square\)

This is only the linear moment.  It does not encode the higher odd moments
or row bijectivity.

## 4. The second-moment quadric

Define
\[
\Phi(v)=\sum_i\langle u_i,v\rangle u_i,\qquad
Q(v)=\sum_i\langle v,u_i\rangle^2.
\]

### Theorem 4.1

The following statements hold.

1. \(\Phi\in\mathfrak{sp}(V)\) and
   \(Q(v)=\langle\Phi v,v\rangle\).
2. The Gram matrix of the normalized polar form
   \[
   \frac{Q(v+z)-Q(v)-Q(z)}2,
   \]
   evaluated on the \(u_i\), is
   \[
   BB^{\mathsf T}=-B^2.
   \]
3. Since the \(u_i\) span \(V\),
   \[
   \operatorname{rank}Q
   =\operatorname{rank}\Phi
   =\operatorname{rank}(B^2)
   =4-\dim(\ker B\cap\operatorname{im}B). \tag{4.1}
   \]
4. \(Q(u_i)=0\) for every \(i\), and hence
   \(\operatorname{diag}(B^2)=0\) and
   \(\operatorname{tr}(B^2)=0\).

**Proof.**  The expression
\[
\langle\Phi v,z\rangle
=\sum_i\langle u_i,v\rangle\langle u_i,z\rangle
\]
is symmetric in \(v,z\), which is the symplectic-Lie-algebra identity and
also gives the formula for \(Q\).  If \(U:\mathbb F_{19}^{20}\to V\) has
columns \(u_i\), and
\(\psi(v)=(\langle u_i,v\rangle)_i\), then
\[
B=\psi U,\qquad U\psi=\Phi,\qquad B^2=\psi\Phi U.
\]
Here \(U\) is surjective and \(\psi\) injective, giving all rank
equalities.  Finally \(Q(u_i)=\sum_jB_{ij}^2=0\) is the \(k=2\) case of
Theorem 2.1. \(\square\)

### Theorem 4.2

\[
\operatorname{rank}Q\in\{0,2,3,4\}.
\]
If the rank is two, the quadric is split.  Rank one and anisotropic rank two
are impossible.

**Proof.**  All twenty nonzero projective points \([u_i]\) lie on \(Q=0\)
and span \(\operatorname{PG}(V)\).  A rank-one quadric has a hyperplane as
its zero locus.  An anisotropic rank-two quadric has only its
two-dimensional radical as its rational zero locus.  Neither can contain a
spanning set. \(\square\)

For reference, the numbers of projective zeros in the surviving types are
\[
\begin{array}{c|c}
\text{type}&\#Q(\mathbb F_{19})=0\text{ in }\operatorname{PG}(3,19)\\ \hline
\text{split rank }2&742\\
\text{rank }3&381\\
\text{hyperbolic rank }4&400\\
\text{elliptic rank }4&362.
\end{array}
\]
Thus point counting alone cannot eliminate any surviving type.

The eighteenth moment has the incidence interpretation
\[
M_{18}(z):=\sum_i\langle z,u_i\rangle^{18}
=20-\#\{i:u_i\in z^\perp\}\pmod{19}. \tag{4.2}
\]
At \(z=u_i\), Theorem 2.1 says \(M_{18}(u_i)=-1\), so the polar plane of
each \(u_i\) contains exactly two indexed vectors: \(u_i\) itself and its
unique matched orthogonal partner.

## 5. Endpoint reduction when \(B_{0,19}\ne0\)

Let \(a=B_{0,19}\).  If \(a\ne0\), scale the whole alternating form and
normalize \(a=1\).  Then
\(\langle u_0,u_{19}\rangle=1\), so
\[
V=\langle u_0,u_{19}\rangle\perp H'
\]
with \(H'\) a symplectic plane.  For \(1\le i\le18\), put
\[
x_i=B_{0i},\qquad y_i=B_{i,19}
\]
and write
\[
u_i=y_i u_0+x_i u_{19}+s_i e+t_i f
\]
in a symplectic basis \(e,f\) of \(H'\).  The panoramic endpoint rows show
that both \(x\) and \(y\) are bijections
\[
\{1,\ldots,18\}\longrightarrow\mathbb F_{19}\setminus\{1\}. \tag{5.1}
\]
For middle indices,
\[
\boxed{
B_{ij}=y_ix_j-x_iy_j+s_it_j-t_is_j.} \tag{5.2}
\]

Let
\[
R_{ij}=B_{ij}-(y_ix_j-x_iy_j).
\]
Then \(R\) has rank exactly two.

**Proof.**  Equation (5.2) shows that \(R\) is the Gram matrix of the
vectors \(v_i=s_ie+t_if\), so its alternating rank is zero or two.  If it
were zero, all the \(v_i\) would be mutually orthogonal.  In a symplectic
plane their span would therefore have dimension at most one.  All twenty
vectors \(u_i\) would then lie in
\(\langle u_0,u_{19}\rangle\perp L\), where \(L\subset H'\) is an
isotropic line.  The symplectic form restricted to that three-dimensional
space has rank two, forcing \(\operatorname{rank}B\le2\), a contradiction.
\(\square\)

## 6. Exact remaining gap

The proved reduction leaves all of the following open:

1. the nilpotent branch \(Q=0\), equivalently \(B^2=0\);
2. the split-rank-two, rank-three, and both rank-four quadric types;
3. compatibility of the endpoint formula (5.2) with the fourth through
   sixteenth moments and all nineteen row bijections;
4. the separate endpoint branch \(B_{0,19}=0\).

The endpoint formula is a smaller exact search space, but no complete
enumeration or contradiction is supplied here.  A verifier for the finite
field sums, corrected quadric counts, zig-zag algebra, and endpoint expansion
is adjacent as `verify_p19_unrestricted_rank4_structure.py`.
