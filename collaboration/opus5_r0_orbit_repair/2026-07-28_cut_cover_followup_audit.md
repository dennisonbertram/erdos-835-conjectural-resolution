# Audit of the Opus 5 obstruction-covering proof

Date: 2026-07-28.

## Execution and verdict

Claude Opus 5 was run at maximum effort, without tools, on the exact prompt
in `2026-07-28_cut_cover_followup_prompt.md`. It returned a solver-free
edge/degree ledger that closes the requested \(|A_U|=6\) branch and the
residual cut-covering problem.

After independent reconstruction, the central ledger and all of its
coexistence conclusions are accepted. Together with the already-certified
pair gate and incompatibility theorem, they prove the full cut-feasible
repair-selection theorem recorded in
`2026-07-28_cut_selection_theorem.md`.

This does not prove cut sufficiency. The remaining local gap is still to
turn a cut-feasible triple into three pairwise edge-disjoint perfect
matchings.

## 1. Accepted Opus ledger

Let \(U_1,U_2\) have orders \(n_1,n_2\), internal \(D\)-edge counts
\(\delta_1,\delta_2\), and intersection \(S\) of order \(s\). Put
\(P_i=U_i\setminus U_{3-i}\), \(Z=V\setminus(U_1\cup U_2)\), and
\(\sigma=e(D[S])\).

Partitioning all \(27\) edges gives
\[
e(D[Z])+e_D(Z,V\setminus Z)+e_D(P_1,P_2)
=27-\delta_1-\delta_2+\sigma.
\]
Therefore
\[
\binom{s}{2}\ge\delta_1+\delta_2-27. \tag{1}
\]

The terms of \(e(D[U_1])+e(D[U_2])\) incident with \(S\) contribute at
most \(5s\), while the two remainders have at most
\(\binom{n_i-s}{2}\) internal edges. Hence
\[
5s\ge
\delta_1+\delta_2
-\binom{n_1-s}{2}
-\binom{n_2-s}{2}. \tag{2}
\]

Applying (1)--(2) to the four possible obstruction types proves:

1. distinct thirteen-edge six-sets are disjoint;
2. a sixteen- or seventeen-edge seven-set coexisting with a
   thirteen-edge six-set contains it;
3. at most one binding seven-set exists;
4. a twenty-edge eight-set coexists with no dense six- or binding
   seven-set; and
5. the seventeen- and sixteen-edge seven-set types cannot coexist.

The arithmetic verifier reproduces every surviving intersection.

## 2. The \(|A_U|=6\) branch

For a thirteen-edge six-set \(U\), write
\(\tau=e_D(U,V\setminus U)\). If six triple rows avoid \(U\), they use
eighteen of the
\[
\sum_{v\notin U}\rho(v)=21-\tau
\]
available row incidences outside \(U\). Thus \(\tau\le3\).

Equations (1)--(2) then show:

- another dense six-set is disjoint and has a disjoint \(A\)-set;
- a seventeen-edge seven-set would contain \(U\) and require four of
  the \(\tau\) crossing edges, impossible;
- a sixteen-edge seven-set contains \(U\), so its \(A\)-set is contained
  in \(A_U\) and cannot contain the missing seventh row; and
- a tight eight-set cannot coexist with \(U\).

Opus therefore found that every one of the fifteen candidates consisting
of the missing row and two rows of \(A_U\) escapes every genuinely
three-way obstruction cut.

The raw response correctly flagged pair compatibility as an assumption
behind that last phrase. The independent audit closes it: the full-row
incompatibility theorem reduces an incompatible pair to a \(K_6-e\)
core with fourteen internal edges, and such a core cannot coexist with
the thirteen-edge six-set. This is proved in detail in
`../r0_three_family_helly_gate/2026-07-28_dense_cut_overlap_audit.md`.
Consequently all fifteen candidates really are individually and pairwise
compatible, and all fifteen satisfy every cut.

## 3. The residual \(|A_U|\le5\) cover

Opus's coexistence table yields a stronger count than is needed:

- two disjoint dense six-cuts cover at most ten row triples in total;
- one dense six-cut nested in a sixteen-edge seven-cut adds no new
  triples;
- one dense six-cut nested in a seventeen-edge seven-cut covers at most
  eleven row triples in total;
- a single binding seven-cut covers at most ten row triples; and
- a tight eight-cut occurs alone and covers at most one row triple.

For the only nontrivial nested case, put \(a=|A_U|\le5\), let \(\mu\)
count rows in \(A_U\) that contain the added seventh-set vertex, and let
\(\nu\) count new \(B\)-rows outside \(A_U\). The row budget is
\[
3a-\mu+2\nu\le14-\tau_Y,
\]
and the number of new triples beyond \(\binom a3\) is
\[
\binom{a-\mu}{2}\nu.
\]
Exact integer enumeration gives a maximum total of eleven.

Thus arbitrary obstruction cuts cover at most eleven of all thirty-five
row triples in the residual regime. Pair compatibility still has to be
imposed before applying the small-cut catalogue. The proof in
`2026-07-28_cut_selection_theorem.md` does this using the exact form
\(K_t\mathbin{\dot\cup}(7-t)K_1\) of the incompatibility graph:

- without a \(K_6-e\) core, all thirty-five triples are compatible;
- with the core, dense six- and seventeen-edge seven-cuts are impossible;
- the only possible sixteen-edge seven-cut contains the core and covers
  no independent triple; and
- at least five independent triples exist for \(t\le5\), while the
  unique tight eight-cut covers at most one.

At least four compatible triples therefore survive in the worst case.

## 4. Audit of the caveats in the raw response

Opus listed four potential gaps:

1. The row-incidence interpretation is not inferred here: equation
   \(\rho(v)=d_D(v)-1\) and the exact seven-triple/four-five-set
   inventory are explicit hypotheses.
2. Exhaustiveness of the four cut types was independently audited in
   `2026-07-28_cut_selection_audit.md`; compatibility is supplied by the
   certified pair gate as described above.
3. The degree-five cap is indeed load-bearing and is an explicit exact
   hypothesis.
4. Realisability of every extremal ledger pattern is unnecessary because
   the proof uses only upper bounds and impossibility implications.

No raw Opus assertion is promoted beyond these independently checked
dependencies.

## 5. Verification

Run:

```sh
python3 collaboration/opus5_r0_orbit_repair/verify_cut_selection_counting.py
python3 collaboration/r0_three_ten_obstruction/verify_r0_incompatibility_graph.py
python3 collaboration/opus5_r0_orbit_repair/verify_rigid_cut_repair_arithmetic.py
```

The first command checks the complete intersection table, the dense-cut
and seventeen-edge cover maxima, the nested maximum of eleven, and all
independent-triple counts. The latter two commands recheck the certified
compatibility dependency and the rigid \(|A_U|=7\) repair arithmetic.
