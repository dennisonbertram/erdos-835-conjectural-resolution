# The dual trace is forced at radius four, and the naive parity test is vacuous

Date: 2026-07-26.  Companion to `radius5_minimal_trace_forced.md` (the
per-\(ij\) fibering, which needs radius five); this note settles the
per-\(uv\) fibering, which is forced **one radius earlier**.  Lemmas 1
and 2 below are proved for every even \(k\) from the radius-4
conditions of `radius4_reduction.md` alone; Lemma 3 combines those
conditions with the forced radius-5 trace.  None uses a cyclic action,
golf chart, or Wallis choice.  Scope: structure of any unrestricted
local ball; **not** a construction, not an obstruction, and not a
result on Erdős–Rosenfeld #835.

Notation as in `radius4_reduction.md`: \(|V|=k\) (even),
\(\mathcal C=V\sqcup\{\infty\}\), \(A\) the \(k-1\) indices; conditions
1–4 define \((L,M,N)\) at radius 4.

## Lemma 1 (dual forced trace)

In every radius-4 structure, for every edge \(uv\) of \(K_V\) and every
colour \(x\in\mathcal C\), the \(x\)-coloured class of \(N_{uv}\) is a
**perfect matching** on its allowed index set
\(\{i\in A: x\notin\{M_i(uv),L_i(u),L_i(v)\}\}\), whose size is

\[
 k-2\ \ (x\in\{u,v,\infty\}),\qquad
 k-4\ \ (x\in\mathcal C\setminus\{u,v,\infty\}).
\]

*Proof.*  Condition 4 gives \(N_{uv}\) at index \(i\) exactly the
palette \(\mathcal C\setminus\{M_i(uv),L_i(u),L_i(v)\}\), of size
\((k+1)-3=k-2=\deg_{K_A}(i)\).  A proper edge-colouring whose palette
size equals the degree uses every palette colour exactly once at every
vertex; hence the \(x\)-class covers every allowed index — a perfect
matching on the allowed set.  Sizes: for \(x=\infty\), no \(L\)-value
is \(\infty\) and \(M_i(uv)=\infty\) for exactly one \(i\) (condition
3), so \(k-2\) indices allow \(\infty\).  For \(x=u\): \(M_i(uv)\ne u\)
always, \(L_i(u)\ne u\) (derangement), and \(L_i(v)=u\) for exactly one
\(i\) (column condition at \(v\), \(u\ne v\)): \(k-2\).  Symmetrically
for \(x=v\).  For generic \(x\): each of
\(\{i:M_i(uv)=x\}\), \(\{i:L_i(u)=x\}\), \(\{i:L_i(v)=x\}\) is a
single index (conditions 3 and 1), giving \(k-1-3=k-4\) by Lemma 2.
The count closes: \(3\cdot\frac{k-2}2+(k-2)\cdot\frac{k-4}2
=\binom{k-1}2=|E(K_A)|\). \(\square\)

At \(k=16\) this is the \(3\times7+14\times6=105\) hole-matching
structure that `cyclic17_vertex_degree_structure.md` §1 derived inside
the fixed-Wallis cyclic ansatz — here obtained ansatz-free, at radius
four.  Consequence for searches: the per-\(uv\) decomposition
constraints may be imposed on the unrestricted radius-4 layer without
loss.

## Lemma 2 (the three holes are always distinct; naive parity is vacuous)

For generic \(x\notin\{u,v,\infty\}\), the three forbidding indices
\(i_M\) (with \(M_{i_M}(uv)=x\)), \(i_u\) (with \(L_{i_u}(u)=x\)), and
\(i_v\) (with \(L_{i_v}(v)=x\)) are **pairwise distinct** in every
radius-4 structure.  Consequently every allowed set of Lemma 1 has
even size automatically, for every even \(k\): the obvious parity
necessary condition ("allowed sets must be even to carry perfect
matchings") can never fail, and yields no obstruction at any even
\(k\).

*Proof.*  \(i_M=i_u\) would force \(M_i(uv)=L_i(u)\) at \(i=i_M\),
contradicting condition 2 (the \(M_i\)-palette at \(u\) omits
\(L_i(u)\)); \(i_M=i_v\) likewise via the palette at \(v\); and
\(i_u=i_v\) would force \(L_i(u)=L_i(v)\), contradicting injectivity of
\(L_i\).  Hence the union has size exactly 3, the generic allowed size
is \(k-4\), and both \(k-2\) and \(k-4\) are even. \(\square\)

Any genuine cross-slice obstruction must therefore live beyond
first-order parity: in signed/oriented structure, spectral or
association-scheme positivity, or second-order double counting across
the two forced fiberings (per-\(ij\): prescribed-link
\(LS(2,3,k+3)\) slices; per-\(uv\): hole-matching decompositions of
\(K_{k-1}\)).

## Lemma 3 (flag fibering: prescribed partial permutations; radius 5)

Fix a flag \((i,u)\), \(i\in A\), \(u\in V\), and a colour \(x\).  In
any radius-5 structure the cell set
\(\Phi_{i,u,x}=\{(j,v):j\ne i,\ v\ne u,\ N_{uv}(ij)=x\}\) is a partial
matching of the \((k-2)\times(k-1)\) rectangle, of exact size

\[
 0\ (x=L_i(u)),\qquad k-2\ (x\in\{u,\infty\}),\qquad
 k-3\ (\text{all other finite }x),
\]

with explicitly forced missed rows/columns:

- rows: none missed for \(x\in\{u,\infty\}\); for generic \(x\) exactly
  the row \(j_0\) with \(L_{j_0}(u)=x\); all rows missed for
  \(x=L_i(u)\);
- columns: for \(x=\infty\), exactly the \(M_i\)-\(\infty\)-partner of
  \(u\); for \(x=u\), exactly \(v=L_i^{-1}(u)\); for generic \(x\), the
  two (always distinct) columns \(v_1=\) the \(M_i\)-\(x\)-partner of
  \(u\) and \(v_2=L_i^{-1}(x)\).

*Proof.*  Fix \(j\ne i\).  The entries in row \(j\) are precisely the
colours on the edges \(uv\) incident with \(u\) in the matching
\(D^{(ij)}_x\) of `radius5_minimal_trace_forced.md`.  Hence at most one
entry of that row can equal \(x\).  Moreover, the forced trace says
that the row is hit unless \(x\) is finite and
\[
 u\in\{L_i^{-1}(x),L_j^{-1}(x)\},
\]
equivalently unless \(x\in\{L_i(u),L_j(u)\}\).  Thus:

- \(x=\infty\) and \(x=u\) hit every one of the \(k-2\) rows;
- \(x=L_i(u)\) hits none;
- every other finite \(x\) misses exactly the unique row \(j_0\ne i\)
  satisfying \(L_{j_0}(u)=x\), by the rainbow column condition on
  the \(L_j(u)\).

Now fix a column \(v\ne u\).  The entries in that column are the
colours on the edges \(ij\) incident with \(i\) in the proper
edge-colouring \(N_{uv}\), so again at most one can equal \(x\).
Condition 4 of `radius4_reduction.md` says that the column is hit
exactly when
\[
 x\notin\{M_i(uv),L_i(u),L_i(v)\}.
\]
For \(x=\infty\), only the first equality can occur, at the unique
\(\infty\)-coloured \(M_i\)-edge incident with \(u\).  For \(x=u\),
the first two equalities are impossible by the \(M_i\) palette and
derangement conditions, while \(L_i(v)=u\) holds at the unique
\(v=L_i^{-1}(u)\).  For finite
\(x\notin\{u,L_i(u)\}\), exactly two columns are missed: the unique
\(M_i\)-\(x\)-partner \(v_1\) of \(u\), and
\(v_2=L_i^{-1}(x)\).  They are distinct, since the palette at \(v_2\)
forbids \(M_i(uv_2)=L_i(v_2)=x\).

The row and column counts agree in every case.  Since both projections
are injective, each nonempty colour class is the claimed partial
matching with exactly the stated complements.  Finally,
\[
 (k-2)+(k-2)+0+(k-2)(k-3)=(k-2)(k-1),
\]
so the colour classes account for every cell of the rectangle.
\(\square\)

Each generic class is thus a **bijection with prescribed
domain/codomain complements** — a canonical carrier for sign
invariants.  Per instruction, this matching structure is NOT presented
as a \(k=16\) obstruction: it is a forced-structure lemma only.

## Lemma 4 (uniform omission over a flag; foundation of the sign calculus)

Fix a flag \((i,u)\) and run \(x\) over all \(k\) colours
\(\mathcal C\setminus\{L_i(u)\}\) (sixteen colours when \(k=16\)).
Then in any radius-5 structure:

- every row \(j\ne i\) is omitted from the domain of \(\Phi_{i,u,x}\)
  for **exactly one** \(x\), namely \(x=L_j(u)\) (always a generic
  colour, since \(L_j(u)\notin\{u,\infty,L_i(u)\}\));
- every column \(v\ne u\) is omitted for **exactly two** \(x\): once as
  the \(M_i\)-partner (\(x=M_i(uv)\), landing in the \(\infty\)-class
  when \(M_i(uv)=\infty\)), and once as the \(L_i\)-preimage
  (\(x=L_i(v)\), landing in the \(u\)-class when \(L_i(v)=u\)).

*Proof.*  Rows: by Lemma 3 the row \(j\) is missed exactly at generic
\(x=L_j(u)\); derangement and the rainbow column at \(u\) exclude
\(u\), \(\infty\) and \(L_i(u)\) as values of \(L_j(u)\).  Columns:
each \(v\) is the \(M_i\)-partner of \(u\) for the single colour
\(M_i(uv)\) (never \(L_i(u)\), by the \(M_i\)-palette at \(u\)), and
the \(L_i\)-preimage for the single colour \(L_i(v)\) (never
\(L_i(u)\), by injectivity; equal to \(u\) exactly when
\(v=L_i^{-1}(u)\)).  Lemma 3's case list shows these are precisely the
omissions. \(\square\)

This uniformity is necessary input to a reference-order-free sign
product, but it does **not by itself prove cancellation**.  Indeed, the
cofactor formula shows that the product of the row-restriction signs
does cancel under a row relabelling: there are two full domains and
the generic domains omit each of the \(k-2\) rows once.  On the column
side, however, the generic fibers omit *pairs*.  Even though every
column occurs in two omitted sets, the product retains the orientation
signs induced on those two-element hole sets.  Those pair-orientation
terms need a further global identity; counting omissions twice is not
enough.  The remaining programme is therefore to assemble the
oriented hole-pair terms over flags and compare the per-\(ij\) and
per-\(uv\) fiberings, or to produce a certified witness falsifying the
candidate.

## Theorem (flag Latin-square augmentation; verified)

Fix a flag \((i,u)\).  On rows \((A\setminus\{i\})\cup\{m,l\}\),
columns \((V\setminus\{u\})\cup\{*\}\), symbols
\(\mathcal C\setminus\{L_i(u)\}\), define
\(Q(j,v)=N_{uv}(ij)\), \(Q(j,*)=L_j(u)\), \(Q(m,v)=M_i(uv)\),
\(Q(m,*)=u\), \(Q(l,v)=L_i(v)\), \(Q(l,*)=\infty\).  In every radius-5
structure \(Q\) is a **Latin square of order \(k\)**: rows \(j\) are
rainbow by the forced radius-5 trace (Lemma 3's missing pair
\(\{L_i(u),L_j(u)\}\) is restored by the \(*\) entry), rows \(m,l\) by
conditions 2 and 1, columns \(v\) by condition 4 (its missing triple
restored by the two dummy entries), column \(*\) by condition 1.  Its
symbol permutations are exactly the Lemma-3 partial permutations
completed by their prescribed missing rows/columns.  Verifier:
`verify_flag_latin_square.py` — checks the universal parity identity
\(\prod_{\rm rows}\operatorname{sgn}\cdot\prod_{\rm cols}
\operatorname{sgn}\cdot\prod_{\rm syms}\operatorname{sgn}
=(-1)^{n(n-1)/2}\) on 210 random Latin squares (n = 2..8), and the
N-free parts of the augmentation (rows \(m,l\), column \(*\)) rainbow
at all 240 flags of the audited k=16 Wallis chart.

For completeness, the parity identity has a short permutation proof.
Order the row, column and symbol sets, and let \(R,C,S\) be the three
products of permutation signs.  The bijection
\((r,c)\mapsto(r,Q(r,c))\) on ordered pairs has sign \(R\).  The
bijection \((r,s)\mapsto(s,c_s(r))\), where \(c_s(r)\) is the column
containing symbol \(s\) in row \(r\), has sign
\((-1)^{k(k-1)/2}S\): transpose the two \(k\)-element coordinates,
then apply the \(k\) symbol permutations.  Their composition is
\((r,c)\mapsto(Q(r,c),c)\), whose sign is \(C\) (grouping it by
columns introduces two identical coordinate-transposition signs,
which cancel).  Hence
\[
 C=(-1)^{k(k-1)/2}RS,\qquad
 RCS=(-1)^{k(k-1)/2}.
\]

## Theorem (exact global Alon--Tarsi product)

For even \(k\), let \(T\) be the order-\(k\) Latin square on rows
\(A\cup\{e\}\), columns and symbols \(V\), defined by
\[
 T(i,u)=L_i(u),\qquad T(e,u)=u.
\]
Let \(S_i\) be the symmetric idempotent Latin square of order \(k+1\)
on \(\mathcal C\) defined by
\[
 S_i(u,u)=u,\quad S_i(u,v)=M_i(uv),\quad
 S_i(u,\infty)=S_i(\infty,u)=L_i(u),\quad
 S_i(\infty,\infty)=\infty.
\]
Write \(\delta(S_i)\) for the product of the \(k+1\) row-permutation
signs.  Then every radius-5 structure satisfies
\[
 \boxed{\displaystyle
 \prod_{i\in A,\ u\in V}\operatorname{AT}(Q^{i,u})
 =(-1)^{k(k-1)/2}\operatorname{AT}(T)
  \prod_{i\in A}\delta(S_i). }\tag{5}
\]
Here \(\operatorname{AT}\) is row-sign product times column-sign
product; it is intrinsic at even order.

*Proof.*  Fix induced orders on \(A,V,\mathcal C=V\cup\{\infty\}\),
with dummy labels last.  We use the cofactor identity
\[
 \operatorname{sgn}(f_a)\operatorname{sgn}(f_b)
 =(-1)^{\operatorname{pos}(a)+\operatorname{pos}(b)+1},\tag{6}
\]
where \(f_a,f_b\) append respectively \(*\mapsto b\) and
\(*\mapsto a\) to a common bijection onto
\(\mathcal C\setminus\{a,b\}\).  It follows by deleting the appended
entry from each permutation; the two common signs square to one.

Pair row \(j\) of \(Q^{i,u}\) with row \(i\) of \(Q^{j,u}\).  Their
common \(N\)-part has image
\(\mathcal C\setminus\{L_i(u),L_j(u)\}\), so (6) applies.  For fixed
\(u\), the exponent is
\[
 (k-2)\sum_i\operatorname{pos}(L_i(u))+\binom{k-1}{2};
\]
after multiplying over the \(k\) values of \(u\) it is even.  Thus
all existing rows contribute \(1\).  Pairing column \(v\) of
\(Q^{i,u}\) with column \(u\) of \(Q^{i,v}\) gives (6) with
\(L_i(u),L_i(v)\); for fixed \(i\) the images run over all pairs of
\(V\), and the exponent is \(k\binom{k}{2}\), again even.  Thus all
existing columns contribute \(1\).

The \(l\)-rows are cofactors of
\(v\mapsto L_i(v),\infty\mapsto\infty\); their product over \(u\) is
\(\operatorname{sgn}(L_i)^k(-1)^{k(k-1)}=1\).  The \(m\)-rows are
cofactors of the finite rows of \(S_i\), with \(u\) moved to the dummy
position, and contribute
\(\delta(S_i)\operatorname{sgn}(L_i)\) over \(u\).  Finally extend the
\(*\)-column before deletion to
\(\Lambda_u(i)=L_i(u),\Lambda_u(m)=u,\Lambda_u(l)=\infty\).
Multiplying its cofactors gives
\((-1)^{k(k-1)/2}C(T)\).  Since
\(R(T)=\prod_i\operatorname{sgn}(L_i)\), multiplication yields (5).
\(\square\)

`collaboration/opus5/radius5_followup/verify_formula_F.py` independently
checks the deletion and completion identities on 3,000 random
instances, the five factors on all 1,680 \(k=6\) radius-3 families and
the \(k=16\) Wallis \(L,M\) data, and the genuine \(k=2\) equality.
Those \(k=6,16\) runs test the \(L,M\)-only factorization; they are not
radius-5 witnesses.  Formula (5) is a structural evaluation, not a
contradiction.

**The residual pair-orientation product and its global cancellation.**
For a column relabelling \(\tau\), the uncancelled
factor at flag \((i,u)\) is
\(R_\tau(i,u)=\prod_{x\ \mathrm{generic}}
\varepsilon_\tau\bigl(\{v_1(x),v_2(x)\}\bigr)\), where
\(\varepsilon_\tau(S)=-1\) exactly when \(\tau\) reverses the relative
order of the two holes.  The hole pairs have a clean shape: since
\(v_2(x)=L_i^{-1}(x)\) and \(v_1(x)\) is the \(M_i\)-partner of \(u\)
in colour \(x\), the pair at \(x\) is \(\{v,\psi_{i,u}(v)\}\) for
\(v=L_i^{-1}(x)\), where

\[
 \psi_{i,u}(v)\ :=\ \text{the }M_i\text{-partner of }u
 \text{ in colour }L_i(v).
\]

Here \(v\in V\setminus\{u,L_i^{-1}(u)\}\), exactly the values for which
\(L_i(v)\) is generic.  The map is a bijection
\[
 \psi_{i,u}:
 V\setminus\{u,L_i^{-1}(u)\}\longrightarrow
 V\setminus\{u,w_\infty\}.
\]
Thus the multiset of generic hole pairs is the undirected edge
multiset of its partial functional graph on \(V\setminus\{u\}\).
This graph is a disjoint union of directed cycles plus one directed
path from \(w_\infty\) to \(L_i^{-1}(u)\); when those vertices
coincide, the path degenerates to an isolated vertex.  Here
\(w_\infty\), the \(M_i\)-\(\infty\)-partner of \(u\), is never a
\(v_1\), while \(L_i^{-1}(u)\) is never a \(v_2\); they coincide
exactly when \(M_i(u,L_i^{-1}(u))=\infty\).  A directed 2-cycle
contributes its undirected edge twice.  Hence
\(R_\tau(i,u)=\prod_{e\in\psi_{i,u}\text{-graph}}\varepsilon_\tau(e)\):
the residual is a \(\pm1\) function of the \(L_i,M_i\) data alone
(radius-4 data — no \(N\) required).  In fact it cancels globally:
\[
 \prod_uR_\tau(i,u)=
 \prod_{v\in V}\varepsilon_\tau(\{v,L_i(v)\}),\qquad
 \prod_{i,u}R_\tau(i,u)=1.\tag{7}
\]
For the first equality, fix \(v\), put \(x=L_i(v)\), and vary \(u\)
over the support \(V\setminus\{v,L_i(v)\}\) of the \(x\)-matching of
\(M_i\).  Its mate map is a permutation of that support, so each
\(\varepsilon_\tau(\{v,z\})\), \(z\ne v,L_i(v)\), occurs once.
Restoring the omitted factor leaves the displayed product because
every edge in the full ordered product occurs twice.  For the second
equality, condition 1 makes \(L_i(v)\) run through \(V\setminus\{v\}\);
every unordered pair again occurs twice.  This proves
reference-independence of the global **generic partial-fiber**
contribution.  The companion `partial_fiber_sign_head.md` strengthens this:
the absolute orientation product \(E(L,M)\) is \(+1\) for every admissible
even-\(k\) chart.

**Sign programme status.**  Formula (5) evaluates the global flag
Alon--Tarsi product from \(L,M\), and the universal Latin identity
implies that the completed symbol-sign product is the same global
invariant.  After \(E(L,M)=+1\), it fixes the required global product of
partial-fiber signs to the right side of (5), but this is the same cofactor
calculation rather than an independent theorem about the shared
\(N\)-table.  A genuinely independent per-\(ij\), per-\(uv\), or joint
formula could still exclude charts by conflicting with (5).  The certified
star theorem
excludes only the fixed-Wallis **cyclic-17 slice-family ansatz** and
does not exclude an arbitrary shared \(N\)-table on the Wallis chart.

## Certified small-\(k\) controls

The complete package, commands, hashes and independent audit are in
`small_k_balls/`.

- The \(k=16\) Wallis-fixed radius-4 encoder gate is SAT; its complete
  6,850,440-clause model and all 120 semantic \(N\)-slices pass.
- \(k=4\) radius 4 and radius 5 are UNSAT with independently checked
  DRAT certificates.
- \(k=6\) radius 5 is UNSAT with an independently checked DRAT
  certificate (13,633,410 resolution steps).
- The package makes no certified claim for \(k=6\) radius 4 or either
  \(k=8\) run.

There is therefore no positive radius-5 control beyond the degenerate
\(k=2\) case.  The \(k=16\) Wallis data test the \(L,M\)-only factors
in (5), but do not instantiate the flag squares \(Q^{i,u}\).

## Scope at k=16

These lemmas constrain every unrestricted radius-5 local ball of
\(O_{16}\); they construct nothing and exclude nothing at \(k=16\).
**#835 is not solved**, and no claim beyond the proved structural
statements and the explicitly qualified run statuses is made here.
