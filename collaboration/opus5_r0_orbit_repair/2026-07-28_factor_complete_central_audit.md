# Central audit of the complete full-row factor theorem

Date: 2026-07-28.

## Verdict

The argument in
`2026-07-28_cut_sufficiency_agent_factor_gate.md` together with
`2026-07-28_cut_sufficiency_agent_factor_complete.md` is sound:

\[
(C)+\text{the full eleven-row equations}
\Longrightarrow
\exists H\subseteq G,\qquad d_H(v)=3-t(v).
\]

An independent audit found that the first draft omitted the three size
triples \((5,6,2),(5,7,1),(5,8,0)\).  They are now explicitly eliminated
in Section 3 of the repaired proof and rechecked below.  No conclusion in
this audit relies on the incomplete draft.

This audit proves only existence of the simple \(b\)-factor.  It does not
promote the factor to the three prescribed perfect matchings.

## Criterion and normalization

For disjoint \(A,B\), with
\(C=V\setminus(A\cup B)\), the instantiated Tutte--Lovász deficiency is

\[
\Delta(A,B)
=b(A)+\sum_{v\in B}d_{G-A}(v)-b(B)-q(A,B).
\]

The full row ledger gives
\(d_G(v)-b(v)=8-u(v)\), so both displayed normalizations in the proof
recompute exactly:

\[
\Delta=b(A)+8|B|-u(B)-e_G(A,B)-q,
\]
\[
\Delta=b(A)-b(B)+2e(G[B])+e_G(B,C)-q.
\]

Summing the counted-component parities gives
\(\Delta\equiv b(V)=30\equiv0\pmod2\).  The minimum-degree component bound
\(|K|\ge8-|A|-|B|\) also follows directly from \(\delta(G)\ge7\).

The earlier gate's eliminations for \(B=\varnothing\), \(|A|\le4\), and
\(|A|=5,|B|\le4\) were rechecked.  In particular, every place where a
crude lower bound is \(-1\) legitimately closes by evenness, and every
place where equality makes the residual set independent has the stated
six-, seven-, or eight-set demand under (C).

## The rigid \(5+5+3\) case

The equality case forces

\[
b(A)=6,\quad R_i\subseteq A,\quad D[C]=K_3,\quad
d_D(v)=5,\ e_D(v,A)=0\ (v\in B).
\]

If \(m=e_D(B,C)\), counted-singleton parity and the \(B\)-degree sum give
\[
d_D(c,B)\in\{1,3\},\qquad
25=2e(D[B])+m.
\]
The eight-set cut \(B\cup C\) gives \(m\le7\), while simplicity gives
\(m\ge5\), hence \(m=5\) or \(7\).

- If \(m=5\), then \(D[B]=K_5\) and the \(B\)-degrees from \(C\) are
  \(3,1,1\).  The six-set consisting of \(B\) and the degree-three vertex
  has two residual edges but demand three.
- If \(m=7\), then \(e(D[B])=9\) and the degrees are \(3,3,1\).  The
  seven-set consisting of \(B\) and the two degree-three vertices has five
  residual edges but demand six.

Thus both equality profiles contradict (C).

## The remaining \(|A|=5\) equality cases

For every \(|B|\ge2\), the crude \(|A|=5\) bound is \(-2\), so after the
\(5+5+3\) case one must still check
\[
(5,6,2),\quad(5,7,1),\quad(5,8,0).
\]
Equality forces all selected rows into \(A\), deleted degree five and no
deleted \(A\)-neighbour on every \(B\) vertex, and counted singleton
components in an edgeless \(G[C]\).

- For \((5,8,0)\), the \(B\)-degree sum gives twenty deleted edges in the
  all-avoiding eight-set \(B\), while (C) permits at most nineteen.
- For \((5,7,1)\), if \(m=e_D(B,C)\), the seven-set cut gives \(m\ge5\)
  and the eight-set cut gives \(m\le3\).
- For \((5,6,2)\), counted parity makes the two \(B\)-degrees from \(C\)
  even and at most four.  The six- and eight-set cuts force their sum to
  be six, hence the profile is \(2,4\).  Adding the degree-four vertex to
  \(B\) makes an all-avoiding seven-set with sixteen deleted edges, one
  more than (C) permits.

These calculations close the omission in the first draft.

## Exhaustion for \(|A|\ge6\)

Writing \(a=|A|\), \(k=|B|\), the general bound

\[
\Delta\ge4a-22+(5-a)k
\]
leaves, after the parity test, exactly

\[
(6,4,3),(6,5,2),(6,6,1),(6,7,0),
\]
\[
(7,4,2),(7,5,1),(7,6,0),
\quad(8,4,1),(8,5,0),\quad(9,4,0).
\]

There are no omitted size pairs: direct enumeration of
\(a\ge6,\ 1\le k\le13-a\) reproduces this list.

For \(C=\varnothing\), substitution into
\(\Delta=30-2b(B)+2e(G[B])\) gives the four formulas in the proof.
The six- and seven-set cut estimates close the only two cases not already
nonnegative from \(b(B)\le3|B|\).

For \(C\ne\varnothing\), substitution of
\(b(X)=3|X|-t(X)\) gives

\[
\Delta=30-6k-3c+2r_B+r_C+2e(G[B])+e_G(B,C)-q.
\]

The identities used to regroup this expression were expanded and checked
term by term.  The bounds
\[
r_U+e(G[U])\ge6\quad(a=6),\qquad
r_U+e(G[U])\ge3\quad(a=7)
\]
are exactly the row-by-row inequalities
\(x+\max(0,2-x)\ge2\) and
\(x+\max(0,1-x)\ge1\).

The only multi-branch case is \((6,5,2)\).  Equality forces
\(G[B]\) edgeless and, writing
\(m_j=e_D(c_j,B)\), gives
\[
m_1+m_2=4+e(G[C])+n_1+n_2\le5.
\]
The two six-set cuts give \(m_j\le2+n_j\).  The three possible
\((e(G[C]),n_1+n_2,m_1+m_2)\) values are exactly
\((1,0,5),(0,0,4),(0,1,5)\), and the stated counted-singleton parities
exclude them respectively.  The other five nonempty-\(C\) cases reduce
directly to a lower bound of \(-1\), an independent six-set, or a positive
quantity, exactly as claimed.

Therefore every Tutte--Lovász deficiency is nonnegative.

## Remaining gap

The theorem supplies an exact-degree subgraph, but prescribed colouring is
a nowhere-zero \(\mathbb F_2^2\) boundary-flow condition.  Explicit
uncolourable \(b\)-factors exist in every Venn type, so the next theorem
must choose a favourable factor using ambient alternating switches; it
cannot assert that the factor obtained above is automatically colourable.
