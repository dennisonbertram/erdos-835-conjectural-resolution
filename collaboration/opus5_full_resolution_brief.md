# Claude Opus 5 full-resolution brief: Erdős–Rosenfeld Problem #835

You are the principal mathematical investigator for a serious attempt to
resolve Erdős–Rosenfeld Problem #835. Work at maximum reasoning effort. Cost is
not a stopping condition. Invoke `/efficient-frontier` first if that skill is
available, using your own highest-value reasoning on the decisive mathematics
and delegating only bounded scans or mechanical computations.

## Exact objective

Determine whether there exists any integer \(k>2\) for which the \(k\)-subsets
of \([2k]\) admit a colouring with \(k+1\) colours such that the \(k+1\)
constituent \(k\)-subsets of every \((k+1)\)-subset receive all \(k+1\)
colours.

Equivalently, determine whether

\[
\chi(J(2k,k))=k+1
\]

for some \(k>2\), or equivalently whether a large set

\[
LS(k-1,k,2k)
\]

exists for some \(k>2\).

The intended conjectural answer is no, but you must seriously pursue both a
nonexistence proof and a construction. Do not call the problem solved unless
every implication is complete.

## Current frontier

Read these files before choosing an attack:

- `README.md`
- `erdos_835_conjectural_resolution.md`
- `collaboration/fable_brief.md`
- every directly relevant file under `evidence/`, especially:
  - `constructive_no_go.md`
  - `three_way_trade.md`
  - `fable_trade_quadratic.md`
  - `odd_matching_cells.md`
  - `global_latin_compatibility.md`
  - `modular_kernel/module_audit_p17.md`
  - `modular_kernel/pair_trade_dimension_no_go.md`
  - `odd_graph_local_ball/ABOUT.md`
  - `odd_graph_local_ball/radius4_reduction.md`
  - `state_sdp_p17/ABOUT.md`
- the exact verifier sources adjacent to those notes.

Treat all existing claims as hypotheses until you audit them. The current
record says:

1. A \(k+1\)-colouring is equivalent to \(LS(k-1,k,2k)\).
2. Known divisibility arguments leave only \(k=p-1\) for a prime \(p\).
3. Cases through \(k=14\) are excluded; the first open case is \(k=16\).
4. A hypothetical \(LS(15,16,32)\) forces a tower including
   \(LS(4,5,21)\), \(LS(3,4,20)\), and \(LS(2,3,19)\).
5. Several symmetric, affine, tensor, parity, local-ball, and SDP routes have
   been tested without closing the asymmetric case.

## Your assignment

Do the heavy mathematical lifting, not merely a review:

1. Re-derive the exact equivalences and identify the narrowest logically
   sufficient obstruction.
2. Attack the first open case \(k=16\) from several genuinely different
   directions:
   - compatibility across the full derived-large-set tower;
   - trades and integral/modular lattices, especially characteristic 17;
   - Odd-graph covering monodromy and intersection arrays;
   - representation theory of the relevant Johnson association scheme;
   - constraints coupling all colour classes rather than one Steiner system;
   - exact finite reductions that could admit checkable SAT, ILP, SDP, or
     proof certificates.
3. Determine whether any successful \(k=16\) obstruction generalizes to all
   prime cases \(k=p-1\). Conversely, actively search for a construction in
   a surviving prime case.
4. Use subagents and computation when useful, but personally inspect every
   decisive bridge. A solver status without a completeness proof and a
   replayable certificate is not a theorem.
5. Iterate. If an approach fails, record the exact reason and move to a
   mathematically different attack. Do not stop merely because the first few
   ideas fail.

## Workspace and outputs

Do not overwrite the existing note or evidence. Put all new work under:

`collaboration/opus5/`

Maintain:

- `collaboration/opus5/STATUS.md` — live state, strongest proved lemma,
  active blocker, and next attack;
- `collaboration/opus5/PROOF.md` — only complete proof material;
- `collaboration/opus5/IDEAS.md` — promising but unproved arguments and
  explicit failure points;
- any verifier source and exact outputs needed for finite claims.

Before declaring success, provide:

1. a self-contained proof or construction resolving the full existential
   problem;
2. an explicit audit of every existing and new finite claim;
3. reproducible commands and independently checkable certificates where
   computation is essential;
4. a section titled `Why this proves the full problem`, distinguishing the
   full statement from the \(k=16\) case and from restricted symmetry cases.

If the full problem remains open, do not manufacture closure. Return the
strongest new unconditional theorem, its complete proof, the exact remaining
gap, and the next executable attack.
