# Global star-sign gluing audit

This note tests a sign obstruction that is genuinely global across the
overlapping one-factorization links of a hypothetical large set.  It
recovers the familiar obstruction at the Fano parameter, but at the
first open parameter \(r=15\) every scalar sign closes consistently.
Moreover the normalized local sign vectors of \(K_{18}\)
one-factorizations have full affine span, ruling out any further
affine-linear identity on the isolated star signs.

Throughout, let
\[
v=2r+1
\]
and suppose that \(r+2\) systems
\[
\mathcal D_c=S(r-1,r,v)
\qquad(c\in\mathcal C)
\]
partition all \(r\)-subsets.  This is the boundary form forced by a
hypothetical \(LS(r,r+1,2r+2)\).

## 1. Signs of matchings and one-factorizations

For an ordered \(2m\)-set and a perfect matching \(M\), order the
endpoints within every edge increasingly, order the edges by their
first endpoints, and let
\[
\operatorname{pfsgn}(M)
\]
be the sign of the resulting flattened permutation.  Equivalently it
is \((-1)^{\operatorname{cr}(M)}\), where crossings are counted in the
linear order.

Let \(\mathcal F=(M_c)_{c=1}^{2m-1}\) be a labelled
one-factorization of \(K_{2m}\).  At a vertex \(x\), the factors give a
bijection
\[
\pi_x:\{1,\ldots,2m-1\}\longrightarrow V\setminus\{x\}.
\]
Use the displayed factor order and the inherited vertex order.

**Lemma 1 (flag-transposition identity).**
\[
\prod_c\operatorname{pfsgn}(M_c)
=
(-1)^{\binom m2}\prod_x\operatorname{sgn}(\pi_x).
\tag{1}
\]

**Proof.**
Consider the \(2m(2m-1)\) flags \((x,c)\).  The one-factorization maps
\((x,c)\) to the directed edge \((x,\pi_x(c))\).  In vertex-major
order its sign is the product of the star signs on the right.

Compute the same sign by first transposing the
\(2m\)-by-\((2m-1)\) flag rectangle into factor-major order.  The
transpose sign is
\[
(-1)^{\binom{2m}{2}\binom{2m-1}{2}}=1.
\]
Within factor \(c\), reorder the vertices into the flattened edge
order of \(M_c\); this contributes
\(\operatorname{pfsgn}(M_c)\).  Edge blocks have size two, so
reordering the edge blocks into global lexicographic order contributes
no sign.

It remains to pass from the edge-major directed-edge order
\[
(a,b),(b,a)\quad(a<b)
\]
to the vertex-major directed-edge order.  Its inversion number is
\[
\frac{(2m)(2m-1)(2m-2)(6m-1)}{24},
\]
whose parity is \(\binom m2\).  This gives (1). \(\square\)

The last parity can also be checked directly by separating pairs of
arcs according to whether their underlying edges meet.

## 2. A universal sign for Steiner triple systems

Let \(\mathcal T\) be an \(STS(n)\), \(n\) odd.  At every point \(x\),
the triples through \(x\) give a perfect matching \(M_x\) on
\(V\setminus\{x\}\).  Define
\[
H(\mathcal T)=\prod_x\operatorname{pfsgn}(M_x).
\]

**Lemma 2 (universal STS sign).**
\[
\boxed{H(\mathcal T)=(-1)^{\binom n4}.}
\tag{2}
\]
In particular this sign is independent of the Steiner triple system.

**Proof.**
Add a last point \(\alpha\).  For every \(x\in V\), adjoin the edge
\(\alpha x\) to \(M_x\).  The resulting \(n\) matchings form a
one-factorization of \(K_{n+1}\).  Put \(m=(n+1)/2\).

At \(\alpha\), the star permutation is the identity.  At \(v\in V\),
the star permutation is the row \(x\mapsto v*x\) of the Steiner
quasigroup, with the fixed output \(v\) moved to the final point
\(\alpha\).  The row is one fixed point and \((n-1)/2\)
transpositions.  Hence its sign is
\[
(-1)^{(n-1)/2+n-1-v}.
\]
The product of these signs over \(v=0,\ldots,n-1\) is \(+1\).
Lemma 1 therefore says that the product of the enlarged matching signs
is \((-1)^{\binom m2}\).

Pairing \(x\) with the final point changes the matching sign by
\((-1)^{n-1-x}\).  Multiplication over all \(x\) gives
\[
H(\mathcal T)
=(-1)^{\binom m2+\binom n2}
=(-1)^{\binom n4},
\]
where the last equality is the elementary parity identity valid for
odd \(n\). \(\square\)

## 3. The sign of all links of one boundary system

For \(\mathcal D=S(r-1,r,2r+1)\), every \((r-2)\)-set \(R\) has a
perfect-matching link \(M_{\mathcal D}(R)\) on \(V\setminus R\).  Put
\[
G(\mathcal D)=
\prod_{|R|=r-2}\operatorname{pfsgn}(M_{\mathcal D}(R)).
\]

**Lemma 3.**
\[
G(\mathcal D)=
\left((-1)^{\binom{r+4}{4}}\right)^{\binom{2r+1}{r-3}}.
\tag{3}
\]

**Proof.**
Fix an \((r-3)\)-set \(Q\).  The derived blocks
\[
\{D\setminus Q:Q\subset D\in\mathcal D\}
\]
form an \(STS(r+4)\).  Its point-link at \(x\notin Q\) is exactly
\(M_{\mathcal D}(Q\cup\{x\})\).  Lemma 2 computes the product over
all \(x\notin Q\).  Multiplying over \(Q\), every \(R\) occurs
\(|R|=r-2\) times.  Since \(r-2\) is odd, the left side remains
\(G(\mathcal D)\), proving (3). \(\square\)

For \(r=3\), this gives \(G=-1\); for \(r=5\), \(G=+1\), exactly as
the complete Fano and Witt computations report.

## 4. Gluing the local one-factorizations

For each \((r-2)\)-set \(R\), the \(r+2\) matching links of the
systems \(\mathcal D_c\) form a one-factorization
\(\mathcal F_R\) of \(K_{r+3}\).  At a local vertex \(x\notin R\),
its star permutation is precisely the global colour-extension
permutation at the facet
\[
F=R\cup\{x\}.
\]
Every facet \(F\) occurs in this way \(r-1\) times, once for each
choice of \(x\in F\).  Because \(r-1\) is even,
\[
\prod_R\prod_{x\notin R}\operatorname{sgn}(\pi_{R,x})=+1.
\tag{4}
\]

With \(m=(r+3)/2\), Lemma 1 consequently gives
\[
\prod_R\prod_c\operatorname{pfsgn}(M_c(R))
=
\left((-1)^{\binom m2}\right)^{\binom{2r+1}{r-2}}.
\tag{5}
\]
Regrouping the same factors by colour and applying Lemma 3 gives the
necessary scalar identity
\[
\left(
 \left((-1)^{\binom{r+4}{4}}\right)^
 {\binom{2r+1}{r-3}}
\right)^{r+2}
=
\left((-1)^{\binom{(r+3)/2}{2}}\right)^
 {\binom{2r+1}{r-2}}.
\tag{6}
\]

At the first open parameter \(r=15\),
\[
\binom{19}{4}\equiv0,\qquad
\binom{9}{2}\equiv0\pmod2.
\]
Both sides of (6) are therefore \(+1\).  The complete scalar
star-sign gluing invariant gives no contradiction.

For contrast, at the Fano parameter each isolated
one-factorization of \(K_6\) has star-sign product \(-1\).  Seven
links would give product \(-1\), while the overlap count (4) gives
\(+1\).  Thus this mechanism correctly detects the small
nonexistence, but that row rigidity disappears at \(K_{18}\).

## 5. Exact local no-go at \(K_{18}\)

`verify_star_sign_gluing.py` verifies two normalized
one-factorizations of \(K_{18}\) with opposite factorization signs.
More strongly, it takes the cyclic factorization, applies deterministic
vertex relabellings, renormalizes factor labels at vertex \(0\), and
adjoins one explicit opposite-sign factorization.  Their star-sign
vectors have affine rank \(17\), the maximum possible because the
normalization fixes the star at vertex \(0\).

Consequently there is no nontrivial affine-linear identity over
\(\mathbb F_2\) satisfied by the normalized \(18\)-component local
star-sign vectors.  Any successful global obstruction must use
nonlinear information or compatibility beyond these isolated signs;
linear cohomological gluing of the star parities is exhausted by the
identities above.

