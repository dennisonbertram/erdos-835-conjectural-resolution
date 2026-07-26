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

**The residual pair-orientation product, made explicit (derived, not
yet forced).**  For a column relabelling \(\tau\), the uncancelled
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

So the multiset of generic hole pairs is exactly the edge set of the
functional graph of \(\psi_{i,u}\) on \(V\setminus\{u\}\) — a disjoint
union of \(\psi\)-paths and \(\psi\)-cycles whose two exceptional
vertices are \(w_\infty\) (the \(M_i\)-\(\infty\)-partner of \(u\),
never a \(v_1\)) and \(L_i^{-1}(u)\) (never a \(v_2\)), coinciding
exactly when \(M_i(u,L_i^{-1}(u))=\infty\).  Hence
\(R_\tau(i,u)=\prod_{e\in\psi_{i,u}\text{-graph}}\varepsilon_\tau(e)\):
the residual is a \(\pm1\) function of the \(L_i,M_i\) data alone
(radius-4 data — no \(N\) required), and the global question is
whether \(\prod_{(i,u)}R_\tau(i,u)\), or a fibering-matched partial
product, is forced to \(1\) by conditions 1–3.  This is precisely
where the programme now stands: no cancellation is claimed.

**Sign programme status (explicitly untested).**  The candidate
nonlinear invariant — products of \(\operatorname{sgn}\) of the
\(\Phi_{i,u,x}\) bijections across flags, compared through the two
fiberings — is well-defined once reference orderings are fixed, but
**no radius-5 witness exists on which to falsify it**: the shared
\(N\)-table does not exist for the Wallis chart at \(k=16\) (star
theorem), the \(k=4\) suite verdicts on disk read UNSAT at both radii,
and the \(k=6\) radius-5 log now also reads `s UNSATISFIABLE`
(certificates pending).  Until either a small-\(k\) witness appears
(none may exist) or the suite's UNSATs are certified, no sign lemma is
proposed as fact.  If the small-\(k\) local nonexistence pattern is
certified, the productive question inverts: whether the LOCAL ball
already fails at \(k=16\) — with the certified small-\(k\) mechanisms
as lifting templates — rather than which invariant separates a ball
that exists.

## Ground-truth computations in progress (statuses at write time)

To honour falsify-first discipline, every future proposed lemma will be
tested against exact small-even-\(k\) ground truth.  A background
decision suite (session scratchpad `small_k_balls/`) is running:

- Gate: the encoder PASSES on the known-good \(k=16\) Wallis chart —
  `k16_r4_wallisfix.cadical.log`: `s SATISFIABLE`, with the decoded
  control witness recorded (`k16_r4_encoder_control_witness.json`).
- \(k=4\): solver verdicts on disk read **radius-4 UNSAT and radius-5
  UNSAT** (`k4_r4.cadical.log`, `k4_r5.cadical.log`, DRAT files
  present) — *pending drat-trim verification and the agent's
  certificate report before being treated as proved*.  If confirmed,
  the unrestricted radius-4 local ball already fails at \(k=4\): a
  purely local proof of that case.
- \(k=6\): radius-4 and radius-5 cadical runs in progress (no verdict
  lines yet); CP-SAT second engine in progress.
- \(k=8\): radius-4 and radius-5 cadical runs in progress.

A \(k=6\) radius-5 witness would become the mandatory falsification
instance for all proposed invariants; a certified \(k=6\) local
nonexistence would be a new *local* proof of the \(k=6\) case of #835
and a lifting template.  Certificates (witness JSON + independent
semantic verifier, or DRAT + drat-trim) will be exported when the runs
land.

## Scope at k=16

These lemmas constrain every unrestricted radius-5 local ball of
\(O_{16}\); they construct nothing and exclude nothing at \(k=16\).
**#835 is not solved**, and no claim beyond the three proved lemmas and
the recorded run statuses is made here.
