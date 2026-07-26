# Global finite-field frame moments: an exact no-go theorem

Date: 2026-07-26.

## Outcome

The global normalized-tight-frame consequence does **not** give a
contradiction for either derived \(k=16\) layer by third moments, fourth
moments, ordinary operator moments, or Schur-power ranks alone.  In fact there
is a uniform abstract countermodel satisfying all of those identities, at
every moment order, for

* the true \(k=2\) control;
* the false \(k=4\) and \(k=6\) Johnson controls; and
* the target \(LS(4,5,21)\) and \(LS(3,4,20)\) parameter sets.

This is a rigorous **no-go result for moment-only arguments**, not a
construction of any large set and not a solution of Erdős--Rosenfeld Problem
#835.  The countermodel deliberately does **not** respect Johnson
subset-incidence.  A proof using the actual intersection relations of
subsets, a Johnson/Terwilliger relation beyond the identities below, or a
classification of the deleted kernel remains possible.

The exact standard-library verifier is
`verify_global_frame_moment_no_go.py`.

## 1. Frame identities supplied by a hypothetical layer

Put
\[
 p=17,\qquad q=p-1=16,
\]
and let \(s=t+1\) be the block size.  Fix one deleted system \(D\), let
\(R\) be the number of \(t\)-set rows, and put
\[
 d=R/s=|D|,\qquad N=qd.
\]
The evaluation vectors \(v_S\) from the deleted-colour theorem lie in a
nondegenerate \(q-1=15\) dimensional space.  Every deleted star contains
\(q\) remaining blocks and has
\[
 \sum_{S\text{ in the star}}v_S=0,\qquad
 \bigl(b(v_S,v_T)\bigr)_{S,T}=I_q+J_q.            \tag{1}
\]
Because \(q=-1\) in \(\mathbb F_p\), \(I_q+J_q\) is an idempotent of rank
\(q-1\).  Every block belongs to \(s\) stars, so summing the local frame
operators gives
\[
 \sum_S v_Sv_S^*=dI,\qquad \sum_Sv_S=0.           \tag{2}
\]

Let \(G=(b(v_S,v_T))\), and let \(A\) be adjacency in the residual co-star
graph.  Besides
\[
 G^2=dG,\qquad G\mathbf1=0,\qquad
 \operatorname{rank}G=q-1,                        \tag{3}
\]
the local zero sums give the useful global relation
\[
 AG=GA=-sG.                                       \tag{4}
\]
Indeed, the neighbors of \(S\) split among its \(s\) stars, and in each star
the sum of the other \(q-1\) vectors is \(-v_S\).  Distinct stars through
\(S\) share no other block.

Equations (2)--(4) determine all *ordinary operator moments*:
\[
 G^m=d^{m-1}G\quad(m\ge1).                        \tag{5}
\]
They do not, by themselves, determine entrywise third or fourth moments.
If one grants the stronger canonical full-colouring hierarchy, however,
vectors of the same nonzero colour coincide and different colours have
inner product one.  With \(d\) blocks of every colour this gives, for every
fixed \(S\),
\[
 \sum_T b(v_S,v_T)^r
   =d\,2^r+(q-1)d
   =d(2^r-2)\pmod p.                              \tag{6}
\]
Thus the canonical third and fourth rooted moments would be
\[
 M_3(S)=6d,\qquad M_4(S)=14d.                     \tag{7}
\]
The construction below realizes even this stronger hierarchy.

## 2. Uniform countermodel theorem

**Theorem.**  Let \(p\) be an odd prime, \(q=p-1\), and suppose
\[
 p\nmid d,\qquad d>(s-1)(q-1).                   \tag{8}
\]
There is a linear \(q\)-uniform hypergraph with \(qd\) vertices and \(sd\)
rows, every vertex in \(s\) rows, together with vectors in a nondegenerate
\((q-1)\)-space over \(\mathbb F_p\), having all of the following properties.

1. Every row is a zero-centroid \(I_q+J_q\) simplex frame.
2. The global frame has centroid zero and frame constant \(d\).
3. Its Gram matrix satisfies (3), while the co-row adjacency satisfies (4)
   and has degree \(s(q-1)\).
4. For every \(r\ge1\),
   \[
   G^{\circ r}=J+(2^r-1)E,\qquad
   \operatorname{rank}(G^{\circ r})\le q,         \tag{9}
   \]
   where \(E\) is the same-fibre equivalence matrix.
5. Every rooted entry moment has exactly the value (6).  Among the nonedges
   from a vertex, \(d-1\) inner products are \(2\), and
   \((q-1)d-s(q-1)\) are \(1\), so all corresponding nonedge moment
   identities hold as well.

**Proof.**  Take the vertex set
\[
 V=\{(a,x):0\le a<q,\ x\in\mathbb Z/d\mathbb Z\}
\]
and, for \(0\le j<s\) and \(y\in\mathbb Z/d\mathbb Z\), take the row
\[
 H_{j,y}=\{(a,y+ja):0\le a<q\}.                  \tag{10}
\]
Every row contains one vertex from each of the \(q\) fibres, and every vertex
is in one row of each direction \(j\), hence in \(s\) rows.  If two vertices
in different fibres lay together in directions \(j,j'\), then
\[
 d\mid(j-j')(a-b).
\]
The nonzero integer on the right has absolute value at most
\((s-1)(q-1)<d\), so \(j=j'\); the offset is then also equal.  Thus no pair
lies in two rows, proving linearity and degree \(s(q-1)\).

In
\[
 H_0=\{z\in\mathbb F_p^q:\textstyle\sum_i z_i=0\}
\]
assign every \((a,x)\) the vector
\[
 w_a=e_a+\mathbf1.                               \tag{11}
\]
The restriction of the dot product to \(H_0\) is nondegenerate, and
\[
 w_a\mathbin{\cdot}w_b=1+\delta_{ab},\qquad
 \sum_aw_a=0.
\]
Consequently every row is the required simplex and its frame operator on
\(H_0\) is the identity.  Globally each \(w_a\) occurs \(d\) times, proving
(2).

The Gram entry is \(2\) for two vertices in the same fibre and \(1\)
otherwise.  Hence
\[
 G=J+E.
\]
Using
\[
 J^2=qdJ=-dJ,\quad JE=EJ=dJ,\quad E^2=dE
\]
gives \(G^2=dG\) and \(G\mathbf1=0\); its compression to fibre-constant
vectors is \(d(I_q+J_q)\), so its rank is \(q-1\).  Summing the other
vertices in each of the \(s\) rows through a vertex gives \(-s w_a\), which
proves \(AG=GA=-sG\).  Entrywise powers give (9), and counting the \(d\)
same-fibre and \((q-1)d\) cross-fibre entries proves (6) and the stated
nonedge distribution.  This proves every claim. \(\square\)

## 3. Exact parameters and moment values

All five cases satisfy (8).

| case | \(p\) | \(s\) | \(d\) | rows \(sd\) | vertices \(qd\) | \(d\bmod p\) | \(M_3\) | \(M_4\) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| \(k=2\), true control | 3 | 2 | 2 | 4 | 4 | 2 | 0 | 1 |
| \(k=4\), false control | 5 | 4 | 14 | 56 | 56 | 4 | 4 | 1 |
| \(k=6\), false control | 7 | 6 | 132 | 792 | 792 | 6 | 1 | 0 |
| derived \(LS(4,5,21)\) | 17 | 5 | 1197 | 5985 | 19152 | 7 | 8 | 13 |
| derived \(LS(3,4,20)\) | 17 | 4 | 285 | 1140 | 4560 | 13 | 10 | 12 |

The false \(k=4,6\) controls are especially diagnostic: an argument using
only the identities realized by this theorem cannot distinguish them from
the target.  The theorem does **not** claim that the abstract hypergraphs are
Johnson systems or that the false controls exist in the original problem.

## 4. Association-scheme and Krein scope

The usual Krein obstruction is a positivity statement over the real numbers;
there is no ordered-field positivity after reduction to \(\mathbb F_p\).
More importantly, the countermodel realizes the local simplex, tight-frame,
adjacency-eigenspace, ordinary-moment, entry-moment, and Schur-rank data all
at once.  Repackaging only those data in association-scheme language cannot
yield a contradiction.

This does **not** rule out an exact Johnson-scheme argument.  The vertices in
(10) are labelled by fibre and cyclic coordinate, not by \((t+1)\)-subsets,
and the rows are cyclic transversals, not \(t\)-subset stars.  The model has
no reason to satisfy the higher Johnson intersection numbers, the full
distance relations, or compatibility with a deleted Steiner system.
Those Johnson-specific relations are precisely what a successful
Terwilliger, modular intersection-algebra, or global-gluing attack would
still have to use.

## 5. Separate \(k=6\) warning

`K6_NONMATE_ISOTROPIC_LINE.md` and
`verify_k6_lambda3_witness.py` record an exact \(5\!-\!(12,6,3)\) witness in
the complement of the canonical Witt system.  It gives a genuine
non-Steiner-mate isotropic line with local multiplicity \(3+3\), rather than
the mate profile \(5+1\).  Therefore the 144 mate lines do not exhaust the
full \(k=6\) quadratic cone.  This is independent of the abstract
countermodel theorem and prevents treating the mate-sector enumeration as a
classification.

## 6. Reproduction

Run:

```bash
python3 -B collaboration/global_frame_moment_attack/verify_global_frame_moment_no_go.py
python3 -B collaboration/global_frame_moment_attack/verify_k6_lambda3_witness.py
```

The first verifier exhaustively constructs every row in all five abstract
models, checks row linearity and degrees, and checks all frame and moment
identities through powers \(1,\ldots,p-1\).  Its final line is:

```text
ALL GLOBAL FRAME-MOMENT COUNTERMODELS PASSED
```

The second independently reconstructs \(W_{12}\), verifies the frozen
396-block witness, and ends:

```text
K6 NON-MATE ISOTROPIC-LINE WITNESS: PASS
```

## Scope

Proved: a parameter-uniform exact countermodel to every obstruction using
only the displayed local/global frame, adjacency, scalar moment, operator
moment, or Schur-rank identities.

Not proved: existence of either target large set, existence of either false
control in Johnson geometry, a classification of the full quadratic cone,
or any contradiction for \(k=16\).  Erdős--Rosenfeld Problem #835 remains
open.
