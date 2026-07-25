# Equality-case local structure for \(S(k-1,k,2k)\)

## Honest outcome

This audit extracts the full first two nontrivial layers forced by a
hypothetical Steiner system
\[
 {\cal D}=S(k-1,k,2k).
\]
These are precisely the parameters attaining the Tits bound
\[
 v\ge (t+1)(k-t+1)
\]
after setting the design strength \(t=k-1\).
It gives a new, exact necessary condition at the open parameter \(k=16\):
relative to every complementary pair of blocks, a \(120\)-by-\(120\)
linked one-factorization matrix must extend, in both directions, to 560
coupled decompositions of complements of cubic graphs into 32 triangles.

The condition is verified on the two known equality systems
\(S(3,4,8)\) and \(S(5,6,12)\).  It does **not** yet contradict \(k=16\).
In particular, the natural Bruck--Ryser determinant shortcut fails because
the relevant pair intersections are forced to be nonuniform.

Run

```bash
python3 evidence/verify_tits_equality_local.py
```

for a standard-library-only exact verification.

## 1. Literature boundary

Mendelsohn proved that an \(S(t-1,t,2t+1)\), when it exists, has a
unique extension to an \(S(t,t+1,2t+2)\).  Thus
\[
 S(k-2,k-1,2k-1)
 \quad\Longleftrightarrow\quad
 S(k-1,k,2k).
\tag{1.1}
\]
This is the equivalence between the single systems
\(S(14,15,31)\) and \(S(15,16,32)\).

The title of the short 1974 paper of Assmus and Hermoso can be
misleading in this context: its nonexistence theorem assumes a
flag-transitive automorphism group.  No transitivity may be assumed for
the open case.  The modern record still lists only the systems at
\(k=4,6\), and the unrestricted \(k=16\) constituent remains open.

The block-intersection calculations below are the elementary
intersection-triangle calculation of Gross specialized to these
parameters.  No group action is used anywhere in this note.

Primary sources:

- N. S. Mendelsohn, [A Theorem on Steiner
  Systems](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DE878868DEAB0C05C5D2FD1829E4A656/S0008414X00047775a.pdf/a-theorem-on-steiner-systems.pdf),
  *Canadian Journal of Mathematics* 22 (1970), 1010--1015.
- E. F. Assmus, Jr. and M. T. Hermoso,
  [Non-Existence of Steiner Systems of Type
  \(S(d-1,d,2d)\)](https://eudml.org/doc/172090),
  *Mathematische Zeitschrift* 138 (1974), 171--172.
- B. H. Gross, [Intersection Triangles and Block Intersection Numbers
  of Steiner Systems](https://eudml.org/doc/172114),
  *Mathematische Zeitschrift* 139 (1974), 87--104.

## 2. Complementary blocks and every nonblock bijection

Fix a block \(B\).  Let \(a_i\) be the number of blocks meeting \(B\)
in exactly \(i\) points.  Counting pairs consisting of a block and an
\(s\)-subset of its intersection with \(B\) gives
\[
 \sum_{i=s}^{k}\binom{i}{s}a_i
 =
 \binom{k}{s}\lambda_s,\qquad
 \lambda_s=
 \frac{\binom{2k-s}{k-1-s}}{k-s}
 \quad(0\le s\le k-1),
\tag{2.1}
\]
with \(a_k=1\).  Back substitution determines every \(a_i\).
For even \(k\), it gives
\[
 a_0=1,\qquad a_1=a_{k-1}=0.
\tag{2.2}
\]
The only \(k\)-set disjoint from \(B\) is \(B^c\), so (2.2) proves
that every block occurs with its complement.

Now let \(X\) be a \(k\)-set which is not a block.  For every \(x\in X\),
the facet \(X-\{x\}\) has a unique block extension.  It cannot extend
back to \(X\), hence there is a unique
\[
 \phi_X(x)\in X^c
 \quad\text{such that}\quad
 X-\{x\}+\{\phi_X(x)\}\in{\cal D}.
\tag{2.3}
\]
If \(\phi_X(x)=\phi_X(y)\) for distinct \(x,y\), the two resulting
blocks meet in \(k-1\) points, which is impossible.  Therefore
\[
 \boxed{\phi_X:X\longrightarrow X^c\ \text{is a bijection}.}
\tag{2.4}
\]
Complementation gives
\[
 \phi_{X^c}=\phi_X^{-1}.
\tag{2.5}
\]

There is also a useful exact transition law.  Let
\[
 Y=X-\{a\}+\{b\},\qquad b\ne\phi_X(a),
\]
so \(Y\) is again a nonblock, and put \(c=\phi_X^{-1}(b)\).
Identify the domains \(X,Y\) by sending \(a\) to \(b\), and identify
their complements by sending \(b\) to \(a\).  Relative to these
identifications, the permutation
\[
 \phi_X^{-1}\phi_Y\in\operatorname{Sym}(X)
\tag{2.6}
\]
fixes exactly \(a,c\) and deranges the other \(k-2\) points.

Indeed, the two fixed points follow directly from the two facets
\(X-a\) and \(X-c\).  Any third fixed point would give two distinct
blocks meeting in \(k-1\) points.  In the complete controls, the
derangement is always one cycle:
\[
\begin{array}{c|c|c}
k&\text{adjacent nonblock pairs}&\text{relative cycle type}\\ \hline
4&336&(1,1,2)\\
6&11\,880&(1,1,4).
\end{array}
\tag{2.7}
\]
The proof only forces two fixed points; the single-cycle conclusion in
(2.7) must not be extrapolated to \(k=16\).

## 3. The complete fixed-block hierarchy

Put \(C=B^c\).  For \(0\le i\le k\), define the square zero-one matrix
\[
 G_i(A,E)=1
 \quad\Longleftrightarrow\quad
 A\cup(C\setminus E)\in{\cal D},
\tag{3.1}
\]
where \(A\in\binom Bi\) and \(E\in\binom Ci\).
Complementation says
\[
 G_i(A,E)=G_{k-i}(B\setminus A,C\setminus E).
\tag{3.2}
\]

The Steiner axiom becomes one exact recursion.  Given
\[
 A\in\binom Bj,\qquad F\in\binom C{j+1},
\]
the set \(A\cup(C\setminus F)\) has size \(k-1\).  Its unique block is
obtained either by adding a point of \(B\setminus A\) or a point of
\(F\).  Hence
\[
 \boxed{
 \sum_{a\in B\setminus A}G_{j+1}(A+a,F)
 +
 \sum_{c\in F}G_j(A,F-c)=1.
 }
\tag{3.3}
\]
This holds for every \(0\le j<k\).  In matrix form, with \(D_i\) the
ordinary facet-versus-\(i\)-set incidence matrix,
\[
 D_iG_i+G_{i-1}D_i=J.
\tag{3.4}
\]

Inclusion--exclusion over the supersets of a fixed
\(A\in\binom Bi\) shows that the number of blocks whose intersection
with \(B\) is exactly \(A\) depends only on \(i\).  Hence the row and
column degrees of \(G_i\) are \(a_i/\binom ki\).  At \(k=16\), the
complete intersection distribution and the corresponding degrees are
\[
\begin{array}{c|rrrrrrrrrrrrrrrrr}
i&0&1&2&3&4&5&6&7&8&9&10&11&12&13&14&15&16\\ \hline
a_i&
1&0&960&17\,920&196\,560&1\,118\,208&
3\,779\,776&7\,687\,680&9\,755\,460&
7\,687\,680&3\,779\,776&1\,118\,208&
196\,560&17\,920&960&0&1\\
\deg G_i&
1&0&8&32&108&256&472&672&758&
672&472&256&108&32&8&0&1.
\end{array}
\tag{3.5}
\]
Every entry is integral; the intersection triangle supplies no
numerical contradiction at \(k=16\).

## 4. The edge layer: linked one-factorizations

Write \(G=G_2\), with rows indexed by edges of \(K_B\) and columns by
edges of \(K_C\).

### Theorem 4.1

The matrix \(G\) has all of the following properties.

1. Every row is the incidence vector of a perfect matching of \(K_C\),
   and every column is the incidence vector of a perfect matching of
   \(K_B\).
2. For each \(a\in B\), the \(k-1\) row matchings indexed by the edges
   through \(a\) form a one-factorization of \(K_C\).  The dual
   statement holds for each \(c\in C\).
3. If \(R\) is the point-edge incidence matrix of \(K_k\), then
   \[
   RG=J,\qquad GR^{\mathsf T}=J.
   \tag{4.1}
   \]
4. Over \(\mathbb Q\),
   \[
   \operatorname{rank}G
   \le \binom{k}{2}-k+1.
   \tag{4.2}
   \]

### Proof

Put \(j=1\) in (3.3).  Since \(G_1=0\), for a point \(a\in B\) and
an edge \(E\in\binom C2\), exactly one edge \(A\) through \(a\)
satisfies \(G(A,E)=1\).  Thus each column is a perfect matching, and
the columns at a fixed point of \(C\) partition all edges of \(K_B\).
Interchanging \(B,C\) gives the row statements.  These assertions are
exactly (4.1).

The matrix \(R\) has rank \(k\) over \(\mathbb Q\), since
\[
 RR^{\mathsf T}=(k-2)I+J
\]
is nonsingular.  For every \(u\perp\mathbf1\), equation (4.1) gives
\[
 GR^{\mathsf T}u=0.
\]
The image \(R^{\mathsf T}(\mathbf1^\perp)\) has dimension \(k-1\);
this proves (4.2). \(\square\)

At \(k=16\), \(G\) is therefore a \(120\)-by-\(120\) degree-eight
matrix with
\[
 \boxed{\operatorname{rank}_{\mathbb Q}G\le105.}
\tag{4.3}
\]
Both controls attain equality.  In fact the verifier exhibits a
maximal minor of determinant \(\pm1\):
\[
\begin{array}{c|c|c}
k&\operatorname{rank}_{\mathbb Q}G&
\text{unimodular maximal minor}\\ \hline
4&3&-1\\
6&10&+1.
\end{array}
\tag{4.4}
\]

## 5. Why the first Bruck--Ryser determinant collapses

For disjoint row edges \(A,A'\subset B\), let
\[
 h(A,A')=
 |\{E:G(A,E)=G(A',E)=1\}|.
\tag{5.1}
\]
Rows that share a point have zero common columns, because their
matchings occur as different factors in the same one-factorization.
Every column contains \(k/2\) mutually disjoint row edges.  Double
counting a column together with two of its row edges gives
\[
 \sum_{\{A,A'\}:A\cap A'=\varnothing}h(A,A')
 =
 \binom{k}{2}\binom{k/2}{2}.
\tag{5.2}
\]
There are \(3\binom{k}{4}\) unordered pairs of disjoint edges, so their
average overlap is
\[
 \boxed{\frac{k}{2(k-3)}}.
\tag{5.3}
\]

For \(k=4\), all three overlaps are two.   For \(k=6\), all 45
overlaps are one.  But at \(k=16\),
\[
 \#\{\text{disjoint row pairs}\}=5460,\qquad
 \sum h=3360,\qquad
 \operatorname{avg}h=\frac8{13}.
\tag{5.4}
\]
Thus a hypothetical system is forced to be nonuniform already at this
local layer.  Since \(0\le h\le8\), (5.4) forces at least 2100 zero
overlaps and at least 420 positive overlaps.

A symmetric-design or association-scheme shortcut would require
\(h(A,A')\) to depend only on whether the two edges meet.  Equation
(5.3) proves that this cannot happen at \(k=16\).  Therefore the
constant-Gram hypothesis needed for the obvious Bruck--Ryser
determinant is not a consequence of the Steiner axioms; imposing it
would silently assume the missing symmetry.

## 6. Equivalent linked Latin-square form

The same \(G\) can be expressed without matrices.  For \(a\in B\) and
\(b\in C\), the middle set
\[
 X_{a,b}=B-\{a\}+\{b\}
\]
is a nonblock.  Relabel the domain point \(b\) as \(a\), and the
codomain point \(a\) as \(b\), in its bijection \(\phi_{X_{a,b}}\).
This gives a permutation
\[
 \sigma_{a,b}:B\longrightarrow C,\qquad
 \sigma_{a,b}(a)=b.
\tag{6.1}
\]
For fixed \(b\), define
\[
 L_b(a,x)=\sigma_{a,b}(x).
\tag{6.2}
\]

### Theorem 6.1

For every \(b\in C\):

- \(L_b\) is a symmetric Latin square with symbol set \(C\);
- every diagonal entry is \(b\);
- for every \(a\ne x\), the map
  \[
  b\longmapsto L_b(a,x)
  \tag{6.3}
  \]
  is a fixed-point-free involution of \(C\).

Moreover,
\[
 L_b(a,x)=y
 \quad\Longleftrightarrow\quad
 G(\{a,x\},\{b,y\})=1.
\tag{6.4}
\]

### Proof

Rows are permutations by (2.4).  If \(L_b(a,x)=y\), then
\[
 B-\{a,x\}+\{b,y\}
\tag{6.5}
\]
is a block.  Interchanging \(a,x\) proves symmetry.  Interchanging
\(b,y\) in the same block proves
\[
 L_y(a,x)=b.
\]
The value \(y=b\) is impossible off the diagonal because a row is a
permutation and its diagonal value is already \(b\).  This proves the
fixed-point-free involution assertion.  Complementing (6.5) gives
(6.4). \(\square\)

This is the precise Latin-square/one-factorization object supplied by
equality in the bound.  Ordinary Latin-square parity gives no
contradiction: the off-diagonal symbol maps in (6.3) are already
products of \(k/2\) transpositions, exactly matching the standard
parity identity.

## 7. The triangle layer: a stronger necessary condition

The next recursion is substantially stronger than an isolated
one-factorization condition.

Fix \(F\in\binom C3\).  Its three edges index three columns of \(G_2\);
let \(H_F\) be the union of their three perfect matchings on \(B\).
The matchings are pairwise edge-disjoint, because two edges of \(F\)
meet and hence occur in the same star one-factorization on the
\(C\)-side.  Thus \(H_F\) is a simple cubic graph on \(B\).

Put \(j=2\) in (3.3).  For every edge \(A\subset B\),
\[
 \sum_{a\in B\setminus A}G_3(A+a,F)
 =
 1-\sum_{\substack{E\subset F\\|E|=2}}G_2(A,E).
\tag{7.1}
\]
The right side is zero precisely on the edges of \(H_F\), and is one
on every other edge.  Consequently:

### Theorem 7.1

For every \(F\in\binom C3\), the triples
\[
 \{A\in\binom B3:G_3(A,F)=1\}
\tag{7.2}
\]
are a triangle decomposition of
\[
 K_B-H_F.
\tag{7.3}
\]
The dual statement holds after interchanging \(B,C\).

At \(k=16\), \(K_{16}-H_F\) is 12-regular with 96 edges, so every one
of the \(\binom{16}{3}=560\) column triples forces exactly
\[
 \boxed{96/3=32\text{ triangles}.}
\tag{7.4}
\]
The same 560 requirements hold in the row direction, and all of the
chosen triangles must be entries of one common \(G_3\).  This coupling,
not mere divisibility, is the new finite target.

The individual leave condition cannot by itself settle the case:
Meszka and Rosa's exhaustive census reports that every cubic graph on
16 vertices is the leave of a partial triple system.  Their result
shows why the simultaneous row/column compatibility in \(G_3\) is
essential.

Source: M. Meszka and A. Rosa,
[Cubic leaves](https://ajc.maths.uq.edu.au/pdf/61/ajc_v61_p114.pdf),
*Australasian Journal of Combinatorics* 61 (2015), 114--129.

The controls behave exactly as predicted:

\[
\begin{array}{c|c|c|c}
k&|F|\text{-choices}&H_F&\text{triangles in }K_k-H_F\\ \hline
4&4&K_4&0\\
6&20&\text{cubic}&2.
\end{array}
\tag{7.5}
\]
For \(k=6\), the complement is two disjoint triangles in every case.

## 8. Exact frontier

Equations (3.2)--(3.4) continue through all sixteen layers.  At the
next step, \(G_4\) must decompose the triples not already covered by
the four relevant columns of \(G_3\), and so on.  This hierarchy is an
exact finite formulation of a constituent \(S(15,16,32)\) around one
block pair.

What is now proved:

- every nonblock has its canonical bijection to its complement;
- adjacent bijections have exactly two forced fixed points;
- every block pair carries the linked Latin-square matrix \(G_2\);
- \(G_2\) has degree eight and rational rank at most 105;
- its 5460 disjoint-row overlaps have total 3360 and must be
  nonuniform;
- every triple of columns and every triple of rows must extend to a
  32-triangle decomposition, with all choices coupled by one \(G_3\).

What is not proved:

- that no such coupled pair \((G_2,G_3)\) exists at \(k=16\);
- that the relative derangement in (2.6) is one cycle at \(k=16\);
- that \(G_2\) has maximal rank at \(k=16\); or
- that any sign or determinant extracted from these layers is
  contradictory.

Thus the equality attack has produced a rigorous, smaller necessary
object and has ruled out the naive uniform Bruck--Ryser route, but it
has not yet proved nonexistence of \(S(14,15,31)\).

### Explicit residual lemma

Let \(D\) be the \(120\)-by-\(560\) edge-versus-triple incidence
matrix of a 16-set.  A clean sufficient statement for finishing this
route is:

> **Coupled cubic-leave lemma (open).**  There do not exist zero-one
> matrices
> \[
>  G_2\in\{0,1\}^{120\times120},\qquad
>  G_3\in\{0,1\}^{560\times560}
> \]
> such that the rows and columns of \(G_2\) have the linked
> one-factorization properties in Theorem 4.1 and, with independent
> copies \(D_B,D_C\) of \(D\),
> \[
> \begin{aligned}
> D_BG_3+G_2D_C&=J,\\
> D_CG_3^{\mathsf T}+G_2^{\mathsf T}D_B&=J.
> \end{aligned}
> \tag{8.1}
> \]

Equation (8.1) says exactly that all 560 cubic leaves decompose into
32 triangles in both directions using one common \(G_3\).  A proof of
this lemma would rule out even a two-layer truncation of the required
system and therefore prove nonexistence of \(S(15,16,32)\).  The lemma
is not established here; it is the precise remaining theorem for this
equality route.
