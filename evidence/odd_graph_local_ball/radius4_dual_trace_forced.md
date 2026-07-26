# The dual trace is forced at radius four, and the naive parity test is vacuous

Date: 2026-07-26.  Companion to `radius5_minimal_trace_forced.md` (the
per-\(ij\) fibering, which needs radius five); this note settles the
per-\(uv\) fibering, which is forced **one radius earlier**.  Both
lemmas below are proved for every even \(k\) from the radius-4
conditions of `radius4_reduction.md` alone — no cyclic action, golf
chart, Wallis choice, or radius-5 assumption.  Scope: structure of any
unrestricted local ball; **not** a construction, not an obstruction,
and not a result on Erdős–Rosenfeld #835.

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
**#835 is not solved**, and no claim beyond the two proved lemmas and
the recorded run statuses is made here.
